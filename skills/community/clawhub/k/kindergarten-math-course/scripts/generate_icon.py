#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成幼儿园数学 Skill 的图标：256x256 PNG。
蓝底 + 白色点阵大字 "123" + 彩色算盘小点，无第三方依赖。
"""

import zlib
import struct
import math
from pathlib import Path

W = H = 256
BLUE = (74, 111, 227)
WHITE = (255, 255, 255)

# 5x7 点阵数字字体
DIGIT_FONT = {
    "1": [
        "..1..",
        ".11..",
        "..1..",
        "..1..",
        "..1..",
        "..1..",
        ".111.",
    ],
    "2": [
        ".111.",
        "...1.",
        "..1..",
        ".1...",
        "1....",
        "1....",
        "11111",
    ],
    "3": [
        ".111.",
        "...1.",
        "..1..",
        "...1.",
        "...1.",
        "...1.",
        ".111.",
    ],
}

# 数字对应的行宽
DIGIT_W = 5
DIGIT_H = 7


def blend(pix, x, y, color, alpha=1.0):
    if 0 <= x < W and 0 <= y < H:
        r, g, b, a = pix[y][x]
        pix[y][x] = (
            int(r * (1 - alpha) + color[0] * alpha),
            int(g * (1 - alpha) + color[1] * alpha),
            int(b * (1 - alpha) + color[2] * alpha),
            255,
        )


def fill_rounded_rect(pix, x0, y0, x1, y1, radius, color):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            dx = max(0, x0 + radius - x, x - (x1 - radius))
            dy = max(0, y0 + radius - y, y - (y1 - radius))
            dist = math.hypot(dx, dy)
            if dist <= radius:
                blend(pix, x, y, color, 1.0)


def draw_digit(pix, digit, x0, y0, cell, color, gap=None):
    """按点阵绘制一个数字，cell 为单点边长，gap 为点数之间的间隙。"""
    glyph = DIGIT_FONT[digit]
    gap = gap or max(1, int(cell * 0.10))
    for ry, row in enumerate(glyph):
        for rx, ch in enumerate(row):
            if ch == "1":
                px = x0 + rx * (cell + gap)
                py = y0 + ry * (cell + gap)
                for yy in range(py, py + cell):
                    for xx in range(px, px + cell):
                        blend(pix, xx, yy, color, 1.0)


def draw_dot(pix, cx, cy, color, r=7):
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            d = math.hypot(x - cx, y - cy)
            if d <= r:
                pix[y][x] = color + (255,)


def main():
    import sys
    # 输出路径：默认 skill/assets/icon.png，可传 --out 指定
    out = Path(__file__).resolve().parent.parent / "assets" / "icon.png"
    argv = sys.argv[1:]
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])
    out = out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    pix = [[BLUE + (255,) for _ in range(W)] for _ in range(H)]
    # 圆角背景
    fill_rounded_rect(pix, 8, 8, 247, 247, 40, BLUE)

    # 三个数字 "123"，自适应宽度排布在一行
    # 5 列点阵，每格 cell，相邻格间隙 gap；数字间 spacing
    cell = 11
    gap = 2
    spacing = 18
    digit_w = 5 * (cell + gap) - gap  # = 63
    total_w = 3 * digit_w + 2 * spacing
    start_x = (W - total_w) // 2
    top_y = (H - 7 * (cell + gap) + gap) // 2
    for i, d in enumerate("123"):
        draw_digit(pix, d, start_x + i * (digit_w + spacing), top_y, cell, WHITE, gap)

    # 彩色算盘小点
    draw_dot(pix, 44, 62, (255, 213, 79), 9)     # 黄
    draw_dot(pix, 70, 42, (244, 143, 177), 7)    # 粉
    draw_dot(pix, 208, 210, (129, 199, 132), 9)  # 绿
    draw_dot(pix, 224, 186, (255, 213, 79), 7)   # 黄
    draw_dot(pix, 128, 44, (244, 143, 177), 6)   # 粉

    # 写 PNG
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
    Path(out).write_bytes(sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", compressed) + chunk(b"IEND", b""))
    print(f"图标已生成: {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()