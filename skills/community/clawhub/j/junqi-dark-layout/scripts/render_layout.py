#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROWS = 6
COLS = 5
VALID_CELLS = {
    0,1,2,3,4,
    5,7,9,
    10,11,13,14,
    15,17,19,
    20,21,22,23,24,
    25,26,27,28,29,
}
HQ_CELLS = {26, 28}
MINE_CELLS = {20,21,22,23,24,25,27,29}
FRONT_ROW_CELLS = {0,1,2,3,4}

CELL_W = 170
CELL_H = 112
MARGIN = 36
HEADER_H = 120
FOOTER_H = 120

BG = (245, 240, 228)
CARD = (252, 249, 241)
GRID = (82, 70, 54)
TEXT = (34, 30, 26)
SUBTEXT = (100, 90, 78)
HQ_FILL = (220, 236, 255)
MINE_FILL = (236, 245, 232)
FRONT_FILL = (255, 243, 233)
NORMAL_FILL = (250, 247, 239)
BLOCK_FILL = (227, 220, 209)
PIECE_FILL = (255, 255, 255)
PIECE_BORDER = (153, 130, 100)
ACCENT = (176, 101, 67)


def load_font(size: int):
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def validate(layout):
    if len(layout) != ROWS * COLS:
        raise ValueError(f"layout must contain {ROWS * COLS} cells")


def draw_layout(title: str, subtitle: str, layout, notes, output: Path):
    width = MARGIN * 2 + COLS * CELL_W + 24
    height = HEADER_H + MARGIN + ROWS * CELL_H + FOOTER_H
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)

    title_font = load_font(42)
    subtitle_font = load_font(24)
    cell_font = load_font(28)
    small_font = load_font(18)
    note_font = load_font(20)

    card_box = (18, 18, width - 18, height - 18)
    draw.rounded_rectangle(card_box, radius=28, fill=CARD, outline=(220, 210, 195), width=2)

    draw.text((MARGIN, 28), title, fill=TEXT, font=title_font)
    draw.text((MARGIN, 76), subtitle, fill=ACCENT, font=subtitle_font)
    draw.text((width - 390, 80), "A版：25格清晰实用阵型卡", fill=SUBTEXT, font=small_font)

    top = HEADER_H
    for r in range(ROWS):
        for c in range(COLS):
            idx = r * COLS + c
            x1 = MARGIN + c * CELL_W
            y1 = top + r * CELL_H
            x2 = x1 + CELL_W - 10
            y2 = y1 + CELL_H - 10

            if idx not in VALID_CELLS:
                draw.rounded_rectangle((x1, y1, x2, y2), radius=16, fill=BLOCK_FILL, outline=(200, 190, 178), width=2)
                draw.text((x1 + 52, y1 + 38), "禁摆位", fill=SUBTEXT, font=small_font)
                continue

            fill = NORMAL_FILL
            if idx in FRONT_ROW_CELLS:
                fill = FRONT_FILL
            if idx in MINE_CELLS:
                fill = MINE_FILL
            if idx in HQ_CELLS:
                fill = HQ_FILL

            draw.rounded_rectangle((x1, y1, x2, y2), radius=16, fill=fill, outline=GRID, width=3)
            pos_label = f"第{r+1}排·{c+1}列"
            draw.text((x1 + 12, y1 + 10), pos_label, fill=SUBTEXT, font=small_font)

            inner = (x1 + 14, y1 + 34, x2 - 14, y2 - 14)
            draw.rounded_rectangle(inner, radius=12, fill=PIECE_FILL, outline=PIECE_BORDER, width=2)

            piece = layout[idx]
            bbox = draw.textbbox((0, 0), piece, font=cell_font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            tx = x1 + (x2 - x1 - tw) / 2
            ty = y1 + 38 + (y2 - y1 - 56 - th) / 2
            draw.text((tx, ty), piece, fill=TEXT, font=cell_font)

    notes_y = HEADER_H + ROWS * CELL_H + 16
    draw.text((MARGIN, notes_y), "简要说明", fill=TEXT, font=subtitle_font)
    for i, note in enumerate(notes[:3]):
        draw.text((MARGIN, notes_y + 34 + i * 28), f"• {note}", fill=SUBTEXT, font=note_font)

    output.parent.mkdir(parents=True, exist_ok=True)
    img.save(output)


def main():
    parser = argparse.ArgumentParser(description="Render a Junqi 25-cell layout card")
    parser.add_argument("--title", default="军棋暗棋摆阵")
    parser.add_argument("--subtitle", default="稳健型｜均衡")
    parser.add_argument("--layout", required=True)
    parser.add_argument("--notes", default='[]')
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    layout = json.loads(args.layout)
    notes = json.loads(args.notes)
    validate(layout)
    draw_layout(args.title, args.subtitle, layout, notes, Path(args.output))
    print(args.output)


if __name__ == "__main__":
    main()
