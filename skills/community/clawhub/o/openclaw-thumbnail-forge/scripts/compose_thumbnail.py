#!/usr/bin/env python3
"""
Compose a finished thumbnail from a source frame with a title, optional
subtitle, gradient bar, optional logo overlay, and a chosen color scheme.

Usage:
  python3 compose_thumbnail.py <input_image> <output_image> --title TEXT
                                                            [--subtitle TEXT]
                                                            [--color-scheme NAME]
                                                            [--position top|bottom|center]
                                                            [--font PATH]
                                                            [--logo PATH]
                                                            [--logo-corner CORNER]
                                                            [--logo-scale FLOAT]
                                                            [--no-contrast-boost]

Color schemes shipped: bold-yellow, clean-white, red-alert, cool-blue, tech-green
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Tuple, Optional

try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
except ImportError:
    print("error: Pillow not installed. Run: pip install Pillow", file=sys.stderr)
    sys.exit(2)

SAFE_PATH_RE = re.compile(r"^[\w./\-+ @=:%,()'\[\]]+$")

COLOR_SCHEMES = {
    "bold-yellow": {
        "title": (255, 220, 0, 255),
        "outline": (15, 15, 15, 255),
        "shadow": (0, 0, 0, 200),
        "subtitle": (255, 255, 255, 230),
        "bar": (0, 0, 0, 170),
    },
    "clean-white": {
        "title": (255, 255, 255, 255),
        "outline": (10, 10, 10, 255),
        "shadow": (0, 0, 0, 180),
        "subtitle": (220, 220, 220, 230),
        "bar": (0, 0, 0, 140),
    },
    "red-alert": {
        "title": (255, 60, 60, 255),
        "outline": (10, 10, 10, 255),
        "shadow": (0, 0, 0, 200),
        "subtitle": (255, 255, 255, 230),
        "bar": (10, 0, 0, 180),
    },
    "cool-blue": {
        "title": (90, 200, 255, 255),
        "outline": (10, 10, 30, 255),
        "shadow": (0, 0, 0, 200),
        "subtitle": (240, 240, 240, 230),
        "bar": (0, 0, 30, 170),
    },
    "tech-green": {
        "title": (60, 240, 130, 255),
        "outline": (10, 20, 10, 255),
        "shadow": (0, 0, 0, 200),
        "subtitle": (240, 240, 240, 230),
        "bar": (0, 20, 0, 170),
    },
}

LOGO_CORNERS = {"top-left", "top-right", "bottom-left", "bottom-right"}


def safe_path(p: str) -> Path:
    if not SAFE_PATH_RE.match(p):
        raise ValueError(f"Refusing path with unsafe characters: {p!r}")
    return Path(p).expanduser()


def find_default_font() -> Optional[Path]:
    """Try to locate a usable TTF font on the system."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for c in candidates:
        if Path(c).is_file():
            return Path(c)
    return None


def fit_font(font_path: Optional[Path], text: str, max_width: int, max_height: int,
             min_size: int = 18, max_size: int = 200) -> ImageFont.ImageFont:
    """Binary-search the largest font size that fits the text into the box."""
    lo, hi = min_size, max_size
    best = None
    while lo <= hi:
        mid = (lo + hi) // 2
        if font_path is not None:
            try:
                font = ImageFont.truetype(str(font_path), mid)
            except OSError:
                font = ImageFont.load_default()
                return font
        else:
            font = ImageFont.load_default()
            return font
        bbox = font.getbbox(text)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        if w <= max_width and h <= max_height:
            best = font
            lo = mid + 1
        else:
            hi = mid - 1
    if best is None:
        try:
            best = ImageFont.truetype(str(font_path), min_size) if font_path else ImageFont.load_default()
        except OSError:
            best = ImageFont.load_default()
    return best


def wrap_text(text: str, font: ImageFont.ImageFont, max_width: int) -> list:
    """Word-wrap text to lines that fit within max_width."""
    words = text.split()
    lines = []
    current = ""
    for w in words:
        test = (current + " " + w).strip()
        bbox = font.getbbox(test)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines or [text]


def draw_outlined_text(draw: ImageDraw.ImageDraw, xy: Tuple[int, int], text: str,
                       font: ImageFont.ImageFont, fill, outline, shadow,
                       outline_width: int = 3, shadow_offset: Tuple[int, int] = (3, 3)):
    x, y = xy
    # Shadow
    draw.text((x + shadow_offset[0], y + shadow_offset[1]), text, font=font, fill=shadow)
    # Outline (8 directions)
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx == 0 and dy == 0:
                continue
            draw.text((x + dx, y + dy), text, font=font, fill=outline)
    # Main fill
    draw.text((x, y), text, font=font, fill=fill)


def add_gradient_bar(img: Image.Image, position: str, bar_color: Tuple[int, int, int, int],
                     height_fraction: float = 0.35) -> Image.Image:
    """Overlay a vertical gradient bar so text on top stays readable."""
    W, H = img.size
    bar_h = int(H * height_fraction)
    overlay = Image.new("RGBA", (W, bar_h), (0, 0, 0, 0))
    r, g, b, a_max = bar_color
    pixels = overlay.load()
    for y in range(bar_h):
        if position == "top":
            alpha = int(a_max * (1 - y / bar_h))
        elif position == "bottom":
            alpha = int(a_max * (y / bar_h))
        else:  # center
            mid = bar_h / 2
            alpha = int(a_max * (1 - abs(y - mid) / mid))
        for x in range(W):
            pixels[x, y] = (r, g, b, alpha)

    if position == "top":
        target_y = 0
    elif position == "bottom":
        target_y = H - bar_h
    else:
        target_y = (H - bar_h) // 2

    base = img.convert("RGBA")
    base.alpha_composite(overlay, (0, target_y))
    return base


def paste_logo(img: Image.Image, logo_path: Path, corner: str, scale: float, padding: int = 24) -> Image.Image:
    if corner not in LOGO_CORNERS:
        raise ValueError(f"Invalid logo corner: {corner}. Allowed: {sorted(LOGO_CORNERS)}")
    with Image.open(logo_path) as logo:
        logo = logo.convert("RGBA")
        target_w = int(img.size[0] * scale)
        ratio = target_w / logo.size[0]
        target_h = int(logo.size[1] * ratio)
        logo_resized = logo.resize((target_w, target_h), Image.LANCZOS)

    W, H = img.size
    if corner == "top-left":
        pos = (padding, padding)
    elif corner == "top-right":
        pos = (W - target_w - padding, padding)
    elif corner == "bottom-left":
        pos = (padding, H - target_h - padding)
    else:
        pos = (W - target_w - padding, H - target_h - padding)

    base = img.convert("RGBA")
    base.alpha_composite(logo_resized, pos)
    return base


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("input", help="Source frame image")
    parser.add_argument("output", help="Output thumbnail image")
    parser.add_argument("--title", required=True, help="Main title text")
    parser.add_argument("--subtitle", default="", help="Optional subtitle text")
    parser.add_argument("--color-scheme", choices=sorted(COLOR_SCHEMES.keys()),
                        default="bold-yellow", help="Color scheme (default: bold-yellow)")
    parser.add_argument("--position", choices=("top", "bottom", "center"),
                        default="bottom", help="Where to place the title block")
    parser.add_argument("--font", default="", help="Path to a TTF/OTF font (default: system font)")
    parser.add_argument("--logo", default="", help="Optional logo image path")
    parser.add_argument("--logo-corner", choices=sorted(LOGO_CORNERS),
                        default="top-right", help="Logo corner")
    parser.add_argument("--logo-scale", type=float, default=0.12,
                        help="Logo width as a fraction of image width (default 0.12)")
    parser.add_argument("--no-contrast-boost", action="store_true",
                        help="Disable the slight contrast boost applied to the source frame")
    parser.add_argument("--width", type=int, default=0,
                        help="Optional output width; height is auto. 0 = keep source size")
    args = parser.parse_args()

    try:
        src = safe_path(args.input).resolve()
        out = safe_path(args.output).resolve()
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if not src.exists():
        print(f"error: input not found: {src}", file=sys.stderr)
        return 2

    # Validate the title is non-empty after whitespace strip. Empty titles
    # used to silently produce a thumbnail with no text, which is a footgun.
    if not args.title or not args.title.strip():
        print("error: --title must be a non-empty string", file=sys.stderr)
        return 2
    if args.logo:
        try:
            logo_path = safe_path(args.logo).resolve()
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        if not logo_path.exists():
            print(f"error: logo not found: {logo_path}", file=sys.stderr)
            return 2
    else:
        logo_path = None

    if args.font:
        try:
            font_path = safe_path(args.font).resolve()
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        if not font_path.is_file():
            print(f"error: font not found: {font_path}", file=sys.stderr)
            return 2
    else:
        font_path = find_default_font()
        if font_path is None:
            print("warning: no system font found; falling back to Pillow default (small)", file=sys.stderr)

    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        with Image.open(src) as srcimg:
            srcimg.verify()
        with Image.open(src) as srcimg:
            img = srcimg.convert("RGBA")
    except Exception as e:
        # PIL.UnidentifiedImageError, OSError, or any decode failure -> clean message.
        print(f"error: could not read image {src}: {e.__class__.__name__}: {e}", file=sys.stderr)
        return 2

    if args.width and args.width > 0:
        ratio = args.width / img.size[0]
        new_size = (args.width, int(img.size[1] * ratio))
        img = img.resize(new_size, Image.LANCZOS)

    if not args.no_contrast_boost:
        img = ImageEnhance.Contrast(img.convert("RGB")).enhance(1.10).convert("RGBA")
        img = ImageEnhance.Color(img.convert("RGB")).enhance(1.05).convert("RGBA")

    W, H = img.size
    scheme = COLOR_SCHEMES[args.color_scheme]

    # Add gradient bar for readability
    img = add_gradient_bar(img, args.position, scheme["bar"], height_fraction=0.40)

    # Title and optional subtitle
    pad_x = int(W * 0.05)
    pad_y = int(H * 0.05)
    title_max_w = W - 2 * pad_x

    title_lines = []
    if font_path:
        title_font = fit_font(font_path, args.title, title_max_w, int(H * 0.16))
        title_lines = wrap_text(args.title, title_font, title_max_w)
        # If wrapping produced multiple lines, rebuild font size based on widest line
        if len(title_lines) > 1:
            widest = max(title_lines, key=lambda s: title_font.getbbox(s)[2] - title_font.getbbox(s)[0])
            title_font = fit_font(font_path, widest, title_max_w, int(H * 0.14))
    else:
        title_font = ImageFont.load_default()
        title_lines = [args.title]

    subtitle_font = None
    if args.subtitle and font_path:
        subtitle_font = fit_font(font_path, args.subtitle, title_max_w, int(H * 0.06),
                                 min_size=14, max_size=int(H * 0.06))

    # Compute layout
    line_h = (title_font.getbbox("Hg")[3] - title_font.getbbox("Hg")[1]) + 6
    block_h = line_h * len(title_lines)
    if args.subtitle and subtitle_font:
        sub_h = subtitle_font.getbbox("Hg")[3] - subtitle_font.getbbox("Hg")[1]
        block_h += sub_h + 12

    if args.position == "top":
        cur_y = pad_y
    elif args.position == "bottom":
        cur_y = H - block_h - pad_y
    else:
        cur_y = (H - block_h) // 2

    draw = ImageDraw.Draw(img)
    for line in title_lines:
        bbox = title_font.getbbox(line)
        line_w = bbox[2] - bbox[0]
        x = (W - line_w) // 2
        draw_outlined_text(draw, (x, cur_y), line, title_font,
                           fill=scheme["title"], outline=scheme["outline"],
                           shadow=scheme["shadow"])
        cur_y += line_h

    if args.subtitle and subtitle_font:
        cur_y += 8
        sbbox = subtitle_font.getbbox(args.subtitle)
        sw = sbbox[2] - sbbox[0]
        sx = (W - sw) // 2
        draw_outlined_text(draw, (sx, cur_y), args.subtitle, subtitle_font,
                           fill=scheme["subtitle"], outline=scheme["outline"],
                           shadow=scheme["shadow"], outline_width=2, shadow_offset=(2, 2))

    if logo_path is not None:
        img = paste_logo(img, logo_path, args.logo_corner, args.logo_scale)

    img.convert("RGB").save(out, format="PNG", optimize=True)
    print(f"Wrote {out} ({W}x{H}, {args.color_scheme}, {args.position})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
