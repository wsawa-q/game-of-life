import pygame
import os

pygame.init()
# CELLs are 16px, so to have 1px space between them
# we assign SIZE to be DESIRED_SIZE + (DESIRED_SIZE / 16) * 1
SPACE_FOR_BUTTONS = 100
SIZE = WIDTH, HEIGHT = 1024 + 64, 512 + 32
WIN = pygame.display.set_mode((SIZE[0], SIZE[1] + SPACE_FOR_BUTTONS))
pygame.display.set_caption("GAME OF LIFE")

# GLOBAL COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# FPS counter
FPS = 30
clock = pygame.time.Clock()
font = pygame.font.SysFont('', 36)
fps_text = font.render(str(FPS), True, WHITE)

# Grid
grid = [[0 for _ in range((WIDTH - 64) // 16)] for _ in range((HEIGHT - 32) // 16)]
initial_grid = [[0 for _ in range((WIDTH - 64) // 16)] for _ in range((HEIGHT - 32) // 16)]
grid_width = len(grid[0])
grid_height = len(grid)
# -------------------------------------------------------------------------------- #

### ---------------------------------- ASSETS ---------------------------------- ###
# CELLS
ALIVE_CELL = pygame.image.load(os.path.join('Assets', 'yellow16.png'))
DEAD_CELL = pygame.image.load(os.path.join('Assets', 'gray16.png'))

# BUTTONS
START_BUTTON = pygame.image.load(os.path.join('Assets', 'button_start.png'))
START_BUTTON_RECT = START_BUTTON.get_rect()
START_BUTTON_RECT.x = (WIDTH - START_BUTTON.get_width()) // 2
START_BUTTON_RECT.y = HEIGHT + (SPACE_FOR_BUTTONS - START_BUTTON.get_height()) // 2

RESET_BUTTON = pygame.image.load(os.path.join('Assets', 'button_reset.png'))
RESET_BUTTON_RECT = RESET_BUTTON.get_rect()
RESET_BUTTON_RECT.x = WIDTH - RESET_BUTTON_RECT.width - 100
RESET_BUTTON_RECT.y = HEIGHT + (SPACE_FOR_BUTTONS - RESET_BUTTON.get_height()) // 2

STOP_BUTTON = pygame.image.load(os.path.join('Assets', 'button_stop.png'))
STOP_BUTTON_RECT = STOP_BUTTON.get_rect()
STOP_BUTTON_RECT.x = RESET_BUTTON_RECT.x - STOP_BUTTON_RECT.width - 30
STOP_BUTTON_RECT.y = HEIGHT + (SPACE_FOR_BUTTONS - STOP_BUTTON.get_height()) // 2

NEW_BUTTON = pygame.image.load(os.path.join('Assets', 'button_new.png'))
NEW_BUTTON_RECT = NEW_BUTTON.get_rect()
NEW_BUTTON_RECT.x = 100
NEW_BUTTON_RECT.y = HEIGHT + (SPACE_FOR_BUTTONS - NEW_BUTTON.get_height()) // 2

PLUS_BUTTON = pygame.image.load(os.path.join('Assets', 'plus-sign.png'))
PLUS_BUTTON_RECT = PLUS_BUTTON.get_rect()
PLUS_BUTTON_RECT.x = NEW_BUTTON_RECT.width + NEW_BUTTON_RECT.x + 30
PLUS_BUTTON_RECT.y = HEIGHT + (SPACE_FOR_BUTTONS - PLUS_BUTTON.get_height()) // 2

MINUS_BUTTON = pygame.image.load(os.path.join('Assets', 'minus-sign.png'))
MINUS_BUTTON_RECT = MINUS_BUTTON.get_rect()
MINUS_BUTTON_RECT.x = PLUS_BUTTON_RECT.x + PLUS_BUTTON_RECT.width + 50
MINUS_BUTTON_RECT.y = HEIGHT + (SPACE_FOR_BUTTONS - MINUS_BUTTON.get_height()) // 2

# -------------------------------------------------------------------------------- #


# Returns the next generation grid
def nextGen(grid, m, n):
    # Create array future[m][n] filled with 0
    future = [[0 for _ in range(n)] for _ in range(m)]

    # Loop through every cell
    for h in range(m):
        for k in range(n):
            # find No of Neighbours that are alive
            alive_neighbours = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (h + i) < 0:
                        if (k + j) < 0:
                            alive_neighbours += grid[m - 1][n - 1]
                        elif (k + j) > (n - 1):
                            alive_neighbours += grid[m - 1][0]
                        else:
                            alive_neighbours += grid[m - 1][k + j]
                    elif (h + i) > (m - 1):
                        if (k + j) < 0:
                            alive_neighbours += grid[0][n - 1]
                        elif (k + j) > (n - 1):
                            alive_neighbours += grid[0][0]
                        else:
                            alive_neighbours += grid[0][k + j]
                    else:
                        if (k + j) < 0:
                            alive_neighbours += grid[h + i][n - 1]
                        elif (k + j) > (n - 1):
                            alive_neighbours += grid[h + i][0]
                        else:
                            alive_neighbours += grid[h + i][k + j]

            # The cell needs to be subtracted from
            # its neighbours as it was counted before
            alive_neighbours -= grid[h][k]

            # RULES

            # Cell is lonely and dies
            if grid[h][k] == 1 and alive_neighbours < 2:
                future[h][k] = 0
            # Cell dies due to over population
            elif grid[h][k] == 1 and alive_neighbours > 3:
                future[h][k] = 0
            # A new cell is born
            elif grid[h][k] == 0 and alive_neighbours == 3:
                future[h][k] = 1
            # Remains the same
            else:
                future[h][k] = grid[h][k]

    return future


def screen_refresh():
    global grid
    WIN.fill(BLACK)
    draw_board(grid, grid_height, grid_width)
    draw_buttons()
    pygame.display.update()


# Game of Life
def gol(grid, m, n):
    future = nextGen(grid, m, n)
    array_copy(future, grid, m, n)
    screen_refresh()


def draw_board(grid, m, n):
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                WIN.blit(ALIVE_CELL, (j * 17, i * 17))
            else:
                WIN.blit(DEAD_CELL, (j * 17, i * 17))


def draw_buttons():
    WIN.blit(START_BUTTON, START_BUTTON_RECT)
    WIN.blit(STOP_BUTTON, STOP_BUTTON_RECT)
    WIN.blit(RESET_BUTTON, RESET_BUTTON_RECT)
    WIN.blit(NEW_BUTTON, NEW_BUTTON_RECT)
    WIN.blit(PLUS_BUTTON, PLUS_BUTTON_RECT)
    WIN.blit(MINUS_BUTTON, MINUS_BUTTON_RECT)
    WIN.blit(fps_text, (PLUS_BUTTON_RECT.x + PLUS_BUTTON_RECT.width + 10, PLUS_BUTTON_RECT.y + 5 ))


def array_copy(from_arr, to_arr, height, width):
    for m in range(height):
        for n in range(width):
            to_arr[m][n] = from_arr[m][n]


def main():
    global grid, initial_grid, FPS, fps_text
    run, game_run = True, False
    while run:
        clock.tick(FPS)
        screen_refresh()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = pos[0], pos[1]

                if pos[1] <= HEIGHT:
                    n = pos[0] // ((WIDTH - 64) // 64 + 1)
                    m = pos[1] // ((HEIGHT - 32) // 32 + 1)
                    grid[m][n] = 1 if grid[m][n] == 0 else 0
                elif START_BUTTON_RECT.collidepoint(pos[0], pos[1]):
                    array_copy(grid, initial_grid, grid_height, grid_width)
                    game_run = True
                elif NEW_BUTTON_RECT.collidepoint(pos[0], pos[1]):
                    game_run = False
                    grid = [[0 for x in range((WIDTH - 64) // 16)] for y in range((HEIGHT - 32) // 16)]
                elif RESET_BUTTON_RECT.collidepoint(pos[0], pos[1]):
                    game_run = False
                    array_copy(initial_grid, grid, grid_height, grid_width)
                elif STOP_BUTTON_RECT.collidepoint(pos[0], pos[1]):
                    game_run = False
                elif PLUS_BUTTON_RECT.collidepoint(pos[0], pos[1]):
                    if FPS < 60:
                        FPS += 5
                        fps_text = font.render(str(FPS), True, WHITE)
                elif MINUS_BUTTON_RECT.collidepoint(pos[0], pos[1]):
                    if FPS > 5:
                        FPS -= 5
                        fps_text = font.render(str(FPS), True, WHITE)

        if game_run:
            gol(grid, grid_height, grid_width)

    pygame.quit()


if __name__ == '__main__':
    main()
