import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def font(spec, bold=False):
    path = spec.get("font_bold" if bold else "font_regular")
    if not path:
        path = r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc"
    return ImageFont.truetype(path, spec.get("font_size", 24))


def dashed_rect(draw, box, color, width=4, dash=14, gap=8):
    x1, y1, x2, y2 = box
    for x in range(x1, x2, dash + gap):
        draw.line((x, y1, min(x + dash, x2), y1), fill=color, width=width)
        draw.line((x, y2, min(x + dash, x2), y2), fill=color, width=width)
    for y in range(y1, y2, dash + gap):
        draw.line((x1, y, x1, min(y + dash, y2)), fill=color, width=width)
        draw.line((x2, y, x2, min(y + dash, y2)), fill=color, width=width)


def arrow(draw, start, end, color, width=5):
    draw.line((start, end), fill=color, width=width)
    ex, ey = end
    sx, sy = start
    dx, dy = ex - sx, ey - sy
    length = max((dx * dx + dy * dy) ** 0.5, 1)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    draw.polygon((end, (ex - ux * 18 + px * 10, ey - uy * 18 + py * 10), (ex - ux * 18 - px * 10, ey - uy * 18 - py * 10)), fill=color)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("spec", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    image = Image.open(args.image).convert("RGB")
    draw = ImageDraw.Draw(image)
    for item in spec.get("annotations", []):
        color = item.get("color", "#3370FF")
        if item["type"] == "box":
            dashed_rect(draw, item["box"], color, item.get("width", 4))
        elif item["type"] == "arrow":
            arrow(draw, item["start"], item["end"], color, item.get("width", 5))
        elif item["type"] == "label":
            box = item["box"]
            draw.rounded_rectangle(box, radius=item.get("radius", 12), fill=item.get("fill", "#EEF4FF"), outline=color, width=item.get("width", 3))
            local = dict(spec)
            local["font_size"] = item.get("font_size", 24)
            draw.text((box[0] + item.get("padding", 18), box[1] + item.get("padding", 18)), item["text"], font=font(local, item.get("bold", True)), fill=item.get("text_color", color))
        else:
            raise ValueError(f"unknown annotation type: {item['type']}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output)
    print(args.output)


if __name__ == "__main__":
    main()
