"""
Build a 3-panel teaser image: 参考图 -> AI 像素图 -> 拼豆图纸.

Used by README.md to showcase end-to-end results. Writes a webp.

usage:
    python make_teaser.py \\
        path/to/ref.jpg \\
        path/to/ai_pixel.png \\
        path/to/pattern.png \\
        --subtitle "白底 · 14 色 · 542 颗" \\
        --accent "#1f6feb" \\
        --out assets/teaser_latte.webp

The three positional inputs are: original photo (or generated reference),
AI-drawn pixel image, and the final printable pattern.
"""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CANVAS_BG = "#FFFFFF"
TITLE_COLOR = "#111111"
FLOW_COLOR = "#444444"
ARROW_COLOR = "#888888"

DEFAULT_FONT_REGULAR = "/usr/share/fonts/truetype/dfonts/dfonts/dfonts/dfonts/msyh.ttc"
DEFAULT_FONT_BOLD = "/usr/share/fonts/truetype/dfonts/msyhbd.ttc"

PANEL_TITLES = ("参考图", "AI 像素图", "拼豆图纸")
PANEL_HINTS = ("你的照片", "gpt-image-2 + 强约束 prompt", None)  # 第三栏的副标题由 --subtitle 提供
FLOW_CAPTION = "照片 → spec.json → 中文 prompt → AI 像素图 → 提色 → Lab/CIEDE2000 snap → 可打印图纸 + 采购清单"


def load_font(path: str | None, size: int) -> ImageFont.FreeTypeFont:
    """Load TrueType font; gracefully fall back to PIL default if missing."""
    candidates = [path] if path else []
    candidates += [DEFAULT_FONT_BOLD, DEFAULT_FONT_REGULAR]
    for cand in candidates:
        if cand and Path(cand).exists():
            try:
                return ImageFont.truetype(cand, size)
            except OSError:
                continue
    return ImageFont.load_default()


def fit_image(img: Image.Image, max_w: int, max_h: int) -> Image.Image:
    """Resize keeping aspect ratio so it fits inside (max_w, max_h)."""
    w, h = img.size
    scale = min(max_w / w, max_h / h)
    return img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)


def draw_text_centered(
    draw: ImageDraw.ImageDraw,
    text: str,
    cx: int,
    y: int,
    font: ImageFont.FreeTypeFont,
    color: str,
) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text((cx - w // 2, y), text, font=font, fill=color)


def draw_arrow(draw: ImageDraw.ImageDraw, x1: int, x2: int, y: int, color: str) -> None:
    draw.line([(x1, y), (x2 - 12, y)], fill=color, width=3)
    draw.polygon(
        [(x2, y), (x2 - 14, y - 9), (x2 - 14, y + 9)],
        fill=color,
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ref", help="reference photo (column 1)")
    ap.add_argument("ai_pixel", help="AI-drawn pixel image (column 2)")
    ap.add_argument("pattern", help="final pindou pattern image (column 3)")
    ap.add_argument("--subtitle", required=True,
                    help='subtitle for column 3, e.g. "白底 · 14 色 · 542 颗"')
    ap.add_argument("--accent", default="#1f6feb",
                    help="accent color for the column-3 subtitle (hex)")
    ap.add_argument("--out", required=True, help="output path (.webp / .png)")
    ap.add_argument("--panel-h", type=int, default=720,
                    help="max panel image height in px (default 720)")
    ap.add_argument("--panel-w", type=int, default=560,
                    help="max panel image width in px (default 560)")
    ap.add_argument("--margin", type=int, default=40)
    ap.add_argument("--gap", type=int, default=90,
                    help="horizontal space between panels (also where the arrow lives)")
    ap.add_argument("--font", default=None,
                    help="override TTF/TTC font path (default: Microsoft YaHei if present)")
    args = ap.parse_args()

    refs = [Image.open(args.ref).convert("RGB"),
            Image.open(args.ai_pixel).convert("RGB"),
            Image.open(args.pattern).convert("RGB")]
    fitted = [fit_image(im, args.panel_w, args.panel_h) for im in refs]

    title_font = load_font(args.font, 34)
    sub_font = load_font(args.font, 22)
    flow_font = load_font(args.font, 22)

    # Vertical layout: top-margin, title, gap, image (panel_h), gap, subtitle, gap, flow, bottom-margin
    title_h = 50
    sub_h = 36
    flow_h = 40
    img_top = args.margin + title_h
    img_bottom = img_top + args.panel_h
    sub_top = img_bottom + 14
    flow_top = sub_top + sub_h + 30

    canvas_w = args.margin * 2 + args.panel_w * 3 + args.gap * 2
    canvas_h = flow_top + flow_h + args.margin

    canvas = Image.new("RGB", (canvas_w, canvas_h), CANVAS_BG)
    draw = ImageDraw.Draw(canvas)

    panel_centers = [
        args.margin + args.panel_w // 2,
        args.margin + args.panel_w + args.gap + args.panel_w // 2,
        args.margin + (args.panel_w + args.gap) * 2 + args.panel_w // 2,
    ]
    subtitles = [PANEL_HINTS[0], PANEL_HINTS[1], args.subtitle]
    sub_colors = [args.accent, args.accent, args.accent]

    for i, (img, cx, title, sub, sub_color) in enumerate(
        zip(fitted, panel_centers, PANEL_TITLES, subtitles, sub_colors)
    ):
        draw_text_centered(draw, title, cx, args.margin, title_font, TITLE_COLOR)
        # Center each image inside its panel slot vertically + horizontally
        iw, ih = img.size
        x = cx - iw // 2
        y = img_top + (args.panel_h - ih) // 2
        canvas.paste(img, (x, y))
        draw_text_centered(draw, sub, cx, sub_top, sub_font, sub_color)

    arrow_y = img_top + args.panel_h // 2
    for i in range(2):
        x1 = args.margin + args.panel_w * (i + 1) + args.gap * i + 14
        x2 = args.margin + args.panel_w * (i + 1) + args.gap * (i + 1) - 14
        draw_arrow(draw, x1, x2, arrow_y, ARROW_COLOR)

    draw_text_centered(draw, FLOW_CAPTION, canvas_w // 2, flow_top, flow_font, FLOW_COLOR)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.suffix.lower() == ".webp":
        canvas.save(out_path, "WEBP", quality=92, method=6)
    else:
        canvas.save(out_path)
    print(f"[teaser] saved -> {out_path} ({canvas_w}x{canvas_h})")


if __name__ == "__main__":
    main()
