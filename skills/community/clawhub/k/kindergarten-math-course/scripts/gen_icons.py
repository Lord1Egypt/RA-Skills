#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为四个幼儿园 Skill 各生成一枚 256x256 PNG 图标（无第三方依赖）。"""
import zlib, struct, math
from pathlib import Path

W = H = 256

THEMES = {
    "math":     {"bg": (74, 111, 227),  "fg": (255, 255, 255), "dots": [(44,62,(255,213,79)),(70,42,(244,143,177)),(208,210,(129,199,132)),(224,186,(255,213,79)),(128,44,(244,143,177))]},
    "english":  {"bg": (230, 126, 74),  "fg": (255, 255, 255), "dots": [(50,60,(255,255,255)),(206,200,(255,213,79)),(128,44,(255,255,255))]},
    "thinking": {"bg": (109, 76, 202),  "fg": (255, 255, 255), "dots": [(48,58,(129,199,132)),(208,198,(255,213,79)),(128,208,(244,143,177))]},
    "activity": {"bg": (46, 156, 137),  "fg": (255, 255, 255), "dots": [(52,64,(255,213,79)),(204,196,(244,143,177)),(128,48,(255,255,255)),(128,212,(255,213,79))]},
}

def blend(pix, x, y, color, alpha=1.0):
    if 0 <= x < W and 0 <= y < H:
        r, g, b, a = pix[y][x]
        pix[y][x] = (int(r*(1-alpha)+color[0]*alpha), int(g*(1-alpha)+color[1]*alpha), int(b*(1-alpha)+color[2]*alpha), 255)

def fill_rounded_rect(pix, x0, y0, x1, y1, radius, color):
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            dx = max(0, x0+radius-x, x-(x1-radius))
            dy = max(0, y0+radius-y, y-(y1-radius))
            if math.hypot(dx, dy) <= radius:
                blend(pix, x, y, color)

def draw_dot(pix, cx, cy, color, r=7):
    for y in range(int(cy-r-1), int(cy+r+2)):
        for x in range(int(cx-r-1), int(cx+r+2)):
            if math.hypot(x-cx, y-cy) <= r:
                blend(pix, x, y, color)

def draw_circle_outline(pix, cx, cy, r, color, thick=8):
    for y in range(int(cy-r-2), int(cy+r+3)):
        for x in range(int(cx-r-2), int(cx+r+3)):
            d = math.hypot(x-cx, y-cy)
            if r-thick/2 <= d <= r+thick/2:
                blend(pix, x, y, color)

def draw_bar(pix, x0, y0, x1, y1, color, radius=None):
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            blend(pix, x, y, color)

# --- 各主题的主图形 ---
def motif_math(pix, fg):
    # "123" 用方块点阵简画：三个竖排点块
    for i, cx in enumerate([78, 128, 178]):
        for row in range(4):
            draw_bar(pix, cx-10, 78+row*26, cx+10, 78+row*26+16, fg)

def motif_english(pix, fg):
    # "Aa"：大三角 A + 小圆 a
    for t in range(70):
        y = 70 + t
        wdt = int(t * 0.62) + 6
        blend_bar = draw_bar(pix, 128-wdt, y, 128-wdt+9, y+3, fg)
        draw_bar(pix, 128+wdt-9, y, 128+wdt, y+3, fg)
    draw_bar(pix, 96, 128, 160, 136, fg)
    draw_circle_outline(pix, 176, 178, 26, fg, 10)
    draw_bar(pix, 176-26, 172, 176+26, 180, fg)

def motif_thinking(pix, fg):
    # 四宫格拼图（右下块错位表示"思维"）
    pad = 10
    s = (247-16-3*pad)//2  # 每块边长
    x0, y0 = 16+pad, 16+pad
    for (bx, by) in [(x0, y0), (x0+s+pad, y0), (x0, y0+s+pad)]:
        fill_rounded_rect(pix, bx, by, bx+s, by+s, 18, fg)
    fill_rounded_rect(pix, x0+s+pad+14, y0+s+pad+14, x0+2*s+pad+14, y0+2*s+pad+14, 18, fg)

def motif_activity(pix, fg):
    # 调色板：大圆盘 + 三个彩点
    draw_circle_outline(pix, 128, 132, 74, fg, 16)
    draw_dot(pix, 100, 110, (255, 213, 79), 12)
    draw_dot(pix, 150, 100, (244, 143, 177), 12)
    draw_dot(pix, 168, 148, (129, 199, 132), 12)

MOTIF = {"math": motif_math, "english": motif_english, "thinking": motif_thinking, "activity": motif_activity}

def write_png(path, pix):
    raw = bytearray()
    for row in pix:
        raw.append(0)
        for r, g, b, a in row:
            raw.extend((r, g, b))
    compressed = zlib.compress(bytes(raw), 9)
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    Path(path).write_bytes(sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", compressed) + chunk(b"IEND", b""))

def main():
    base = Path(__file__).resolve().parent
    for name, th in THEMES.items():
        pix = [[th["bg"] + (255,)] * W for _ in range(H)]
        fill_rounded_rect(pix, 8, 8, 247, 247, 40, th["bg"])
        MOTIF[name](pix, th["fg"])
        for (cx, cy, c) in th["dots"]:
            draw_dot(pix, cx, cy, c, 8)
        out = base / f"icon_{name}.png"
        write_png(out, pix)
        print(f"图标已生成: {out} ({out.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
