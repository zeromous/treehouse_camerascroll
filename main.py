import pygame
import pygame.mouse
import sys

# This PYGAME demo was made by Zeromous for TREEHOUSE WARS  
# [R] KEY increases the playfield height at the top
# [UP]/[DOWN] KEY scrolls the camera up and down
# Hold [SHIFT] KEY to scroll faster

GAME_PATH = "d:/gamedev/treehouse_camerascroll"

class Level:
    def __init__(self, screen_width, screen_height, max_unit_init, increment_height, font_path):
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.MAX_UNIT_INIT = max_unit_init
        self.INCREMENT_HEIGHT = increment_height
        self.PLAYFIELD_HEIGHT = max(self.MAX_UNIT_INIT * 64 + 256, self.SCREEN_HEIGHT)
        self.font = pygame.font.Font(font_path, 14)
        self.playfield = pygame.Surface((self.SCREEN_WIDTH, self.PLAYFIELD_HEIGHT))
        self.playfield.fill((80, 168, 225))
        self.top_y = 0
        self.draw_playfield_elements(self.top_y, self.PLAYFIELD_HEIGHT)
        self.background_image = pygame.image.load( GAME_PATH + "/graphics/level/level1/0.png")
        self.playfield.blit(self.background_image, (0, 0))
        

    def draw_playfield_lines(self, y_position):
        if self.top_y < 0:
            pygame.draw.line(self.playfield, (255, 255, 255), (0, y_position - self.top_y), (self.SCREEN_WIDTH, y_position - self.top_y))
        else:
            pygame.draw.line(self.playfield, (255, 255, 255), (0, y_position), (self.SCREEN_WIDTH, y_position))

    def draw_playfield_numbers(self, y_position):
        text_surface = self.font.render(str(y_position), True, (255, 255, 255))
        
        if self.top_y < 0:
            self.playfield.blit(text_surface, (10, y_position - self.top_y + 10))
        else:
            self.playfield.blit(text_surface, (10, y_position + 10))

    def draw_playfield_elements(self, start_height, end_height):
        y_position = start_height
        if self.top_y < 0:
                self.draw_playfield_lines(self.top_y)
                self.draw_playfield_numbers(self.top_y)
                print(f"[MSG] Playfield top_y: {self.top_y}")

        else:
            while y_position < end_height:
                self.draw_playfield_lines(y_position)
                self.draw_playfield_numbers(y_position)
                y_position += 64

    def increase_playfield_height(self):
        self.PLAYFIELD_HEIGHT += self.INCREMENT_HEIGHT
        new_playfield = pygame.Surface((self.SCREEN_WIDTH, self.PLAYFIELD_HEIGHT))
        new_playfield.fill((51, 153, 255))
        new_playfield.blit(self.playfield, (0, self.INCREMENT_HEIGHT))
        self.playfield = new_playfield
        self.top_y -= self.INCREMENT_HEIGHT
        self.draw_playfield_elements(self.top_y, self.top_y + self.INCREMENT_HEIGHT)

class GameLoop:
    def __init__(self, screen_width, screen_height, level):
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.level = level
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Camera Scrolling / Growing Example [R] to Grow (SHIFT)-[UP] or (SHIFT)-[DOWN] to Scroll")
        self.camera_y = self.level.PLAYFIELD_HEIGHT - self.SCREEN_HEIGHT
        self.SCROLL_SPEED = 5
        self.r_pressed = False
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYUP and event.key == pygame.K_r:
                    self.r_pressed = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # Scroll wheel up
                        self.camera_y -= 64  # Move exactly 64 units
                        if self.camera_y < 0:
                            self.camera_y = 0
                    elif event.button == 5:  # Scroll wheel down
                        self.camera_y += 64  # Move exactly 64 units
                        if self.camera_y > self.level.PLAYFIELD_HEIGHT - self.SCREEN_HEIGHT:
                            self.camera_y = self.level.PLAYFIELD_HEIGHT - self.SCREEN_HEIGHT

            keys = pygame.key.get_pressed()
            scroll_speed = self.SCROLL_SPEED * 5 if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else self.SCROLL_SPEED

            if keys[pygame.K_UP]:
                self.camera_y -= scroll_speed
                if self.camera_y < 0:
                    self.camera_y = 0

            if keys[pygame.K_DOWN]:
                self.camera_y += scroll_speed
                if self.camera_y > self.level.PLAYFIELD_HEIGHT - self.SCREEN_HEIGHT:
                    self.camera_y = self.level.PLAYFIELD_HEIGHT - self.SCREEN_HEIGHT

            if keys[pygame.K_r] and not self.r_pressed:
                self.level.increase_playfield_height()
                self.camera_y += self.level.INCREMENT_HEIGHT
                self.r_pressed = True



            if keys[pygame.K_ESCAPE]:
                self.running = False
              
            self.screen.fill((0, 0, 0))
            camera_view = self.level.playfield.subsurface((0, self.camera_y, self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            self.screen.blit(camera_view, (0, 0))
            pygame.display.flip()
            pygame.time.Clock().tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    pygame.init()
    screen_width = 1024
    screen_height = 768
    max_unit_init = 3
    increment_height = 64
    font_path = "./fonts/vgaoem.fon"
    level = Level(screen_width, screen_height, max_unit_init, increment_height, font_path)
    game_loop = GameLoop(screen_width, screen_height, level)
    game_loop.run()