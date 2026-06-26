#!/usr/bin/env python3
"""
Re-export a finished thumbnail to all common platform sizes in one command.

Targets:
  YouTube           1280x720
  YouTube Shorts    1080x1920
  Instagram square  1080x1080
  X / Twitter       1200x675
  LinkedIn          1200x627

Usage:
  python3 export_sizes.py <input_image> <output_dir> [--platforms LIST]
                                                     [--mode fit|cover]

Modes:
  fit    Letterbox into the target (no content lost; transparent/black bars).
  cover  Center-crop to fill the target (default; ensures the whole frame is used).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Tuple, List

try:
    from PIL import Image, ImageOps
except ImportError:
    print("error: Pillow not installed. Run: pip install Pillow", file=sys.stderr)
    sys.exit(2)

SAFE_PATH_RE = re.compile(r"^[\w./\-+ @=:%,()'\[\]]+$")

PLATFORMS = {
    "youtube":   ("youtube_1280x720.png",   1280, 720),
    "shorts":    ("shorts_1080x1920.png",   1080, 1920),
    "instagram": ("instagram_1080x1080.png", 1080, 1080),
    "x":         ("x_1200x675.png",         1200, 675),
    "linkedin":  ("linkedin_1200x627.png",  1200, 627),
}


def safe_path(p: str) -> Path:
    if not SAFE_PATH_RE.match(p):
        raise ValueError(f"Refusing path with unsafe characters: {p!r}")
    return Path(p).expanduser()


def export_cover(img: Image.Image, target: Tuple[int, int]) -> Image.Image:
    """Resize the image so it covers the target, then center-crop."""
    return ImageOps.fit(img, target, method=Image.LANCZOS, centering=(0.5, 0.5))


def export_fit(img: Image.Image, target: Tuple[int, int]) -> Image.Image:
    """Resize the image to fit inside the target with black letterboxing."""
    src = img.copy()
    src.thumbnail(target, Image.LANCZOS)
    canvas = Image.new("RGB", target, (0, 0, 0))
    px = (target[0] - src.size[0]) // 2
    py = (target[1] - src.size[1]) // 2
    canvas.paste(src.convert("RGB"), (px, py))
    return canvas


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("input", help="Source thumbnail image")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument(
        "--platforms",
        default="youtube,shorts,instagram,x,linkedin",
        help="Comma-separated list (default: all five)",
    )
    parser.add_argument(
        "--mode",
        choices=("fit", "cover"),
        default="cover",
        help="fit (letterbox) or cover (center-crop, default)",
    )
    args = parser.parse_args()

    try:
        src = safe_path(args.input).resolve()
        out_dir = safe_path(args.output_dir).resolve()
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if not src.exists():
        print(f"error: input not found: {src}", file=sys.stderr)
        return 2

    requested: List[str] = [p.strip().lower() for p in args.platforms.split(",") if p.strip()]
    for p in requested:
        if p not in PLATFORMS:
            print(f"error: unknown platform '{p}'. Allowed: {sorted(PLATFORMS.keys())}", file=sys.stderr)
            return 2

    out_dir.mkdir(parents=True, exist_ok=True)

    with Image.open(src) as srcimg:
        srcimg = srcimg.convert("RGB")
        for key in requested:
            name, w, h = PLATFORMS[key]
            target = (w, h)
            if args.mode == "cover":
                exported = export_cover(srcimg, target)
            else:
                exported = export_fit(srcimg, target)
            out_path = out_dir / name
            exported.save(out_path, format="PNG", optimize=True)
            print(f"  wrote {out_path}  ({w}x{h}, {args.mode})", file=sys.stderr)

    print(f"Exported {len(requested)} size(s) to {out_dir}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
