#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


FONT_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

REGULAR_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def pick_font(candidates: list[str], size: int):
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def multiline_wrap(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> str:
    lines: list[str] = []
    for raw_line in text.splitlines() or [text]:
        line = raw_line.strip()
        if not line:
            lines.append("")
            continue
        current = ""
        for ch in line:
            probe = current + ch
            if draw.textlength(probe, font=font) <= max_width or not current:
                current = probe
            else:
                lines.append(current)
                current = ch
        if current:
            lines.append(current)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate a simple Xiaohongshu text cover image.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--tag", default="测试一下")
    parser.add_argument("--footer", default="#测试笔记")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    W, H = 1080, 1440
    img = Image.new("RGB", (W, H), (255, 238, 244))
    draw = ImageDraw.Draw(img)

    for (x, y), r, color in [
        ((930, 120), 180, (255, 206, 222)),
        ((140, 1180), 150, (255, 215, 228)),
        ((840, 1180), 90, (255, 194, 214)),
    ]:
        draw.ellipse((x - r, y - r, x + r, y + r), fill=color)

    card = (110, 120, 970, 1320)
    draw.rounded_rectangle(card, radius=46, fill=(255, 252, 253), outline=(255, 226, 236), width=3)

    font_tag = pick_font(REGULAR_CANDIDATES, 36)
    font_h1 = pick_font(FONT_CANDIDATES, 88)
    font_sub = pick_font(REGULAR_CANDIDATES, 42)
    font_ft = pick_font(REGULAR_CANDIDATES, 30)

    x1, y1, x2, y2 = (180, 210, 410, 278)
    draw.rounded_rectangle((x1, y1, x2, y2), radius=34, fill=(255, 92, 138))
    draw.text((x1 + 36, y1 + 12), args.tag[:8], font=font_tag, fill="white")

    wrapped_title = multiline_wrap(draw, args.title.strip(), font_h1, 700)
    draw.multiline_text((180, 360), wrapped_title, font=font_h1, fill=(46, 37, 47), spacing=18)

    subtitle = args.subtitle.strip() or "先发一条，看看今天运气站不站我这边。"
    wrapped_sub = multiline_wrap(draw, subtitle, font_sub, 700)
    draw.multiline_text((180, 760), wrapped_sub, font=font_sub, fill=(108, 86, 96), spacing=18)

    footer_left = args.footer.strip()[:24] or "#测试笔记"
    footer_right = "OpenClaw"
    draw.text((180, 1200), footer_left, font=font_ft, fill=(165, 110, 130))
    width = draw.textlength(footer_right, font=font_ft)
    draw.text((900 - width, 1200), footer_right, font=font_ft, fill=(165, 110, 130))

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    img.save(output)
    print(str(output))


if __name__ == "__main__":
    main()
