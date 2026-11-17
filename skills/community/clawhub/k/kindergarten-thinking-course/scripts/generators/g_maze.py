# -*- coding: utf-8 -*-
"""迷宫"""
from common import *


def gen_maze(level, rng, lang="zh"):
    T = I18N[lang]
    w = h = 5 if level <= 2 else 7
    grid = [[{"N": True, "S": True, "E": True, "W": True} for _ in range(w)] for _ in range(h)]
    visited = [[False] * w for _ in range(h)]
    stack = [(0, 0)]
    visited[0][0] = True
    while stack:
        x, y = stack[-1]
        neigh = []
        for dx, dy, wall in [(0, -1, "N"), (0, 1, "S"), (1, 0, "E"), (-1, 0, "W")]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx]:
                neigh.append((nx, ny, wall))
        if neigh:
            nx, ny, wall = rng.choice(neigh)
            if wall == "N":
                grid[y][x]["N"] = False; grid[ny][nx]["S"] = False
            elif wall == "S":
                grid[y][x]["S"] = False; grid[ny][nx]["N"] = False
            elif wall == "E":
                grid[y][x]["E"] = False; grid[ny][nx]["W"] = False
            else:
                grid[y][x]["W"] = False; grid[ny][nx]["E"] = False
            visited[ny][nx] = True
            stack.append((nx, ny))
        else:
            stack.pop()
    rows = ""
    for y in range(h):
        cells = ""
        for x in range(w):
            c = grid[y][x]
            bt = "border-top:3px solid #333;" if c["N"] else ""
            bb = "border-bottom:3px solid #333;" if c["S"] else ""
            bl = "border-left:3px solid #333;" if c["W"] else ""
            br = "border-right:3px solid #333;" if c["E"] else ""
            mark = "🚪" if (x == 0 and y == 0) else ("🎁" if (x == w - 1 and y == h - 1) else "")
            cells += f'<td style="{bt}{bb}{bl}{br}text-align:center;font-size:16px;">{mark}</td>'
        rows += f"<tr>{cells}</tr>"
    html = f'<table class="maze"><tbody>{rows}</tbody></table>'
    instr = T["instr_maze"]
    ans = T["ans_maze"]
    return T["title_maze"], instr, html, ans


TOPICS = {
    "maze": gen_maze,
}
