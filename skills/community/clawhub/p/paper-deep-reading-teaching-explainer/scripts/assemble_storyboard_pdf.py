#!/usr/bin/env python3
"""Assemble staged storyboard images into a 16:9 PDF.

This helper is intentionally simple and local-only. It does not call external APIs.
It fits each image onto a 16:9 page without clipping and writes a multi-page PDF.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable, List

try:
    from PIL import Image, ImageOps
    from PIL import JpegImagePlugin  # noqa: F401 - registers JPEG encoder for PDF export
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required: pip install pillow") from exc

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"}


def natural_key(path: Path):
    text = path.name.lower()
    # prefer Chinese storyboard numbers like 第12幕 when present
    nums = [int(n) for n in re.findall(r"第\s*(\d+)\s*幕|(?:^|[_-])(\d+)(?:[_-]|\.)", text) for n in n if n]
    return (nums[0] if nums else 10**9, [int(s) if s.isdigit() else s for s in re.split(r"(\d+)", text)])


def collect_images(input_dir: Path, explicit: Iterable[str] | None = None) -> List[Path]:
    if explicit:
        paths = [Path(p) for p in explicit]
    else:
        paths = [p for p in input_dir.rglob("*") if p.suffix.lower() in IMAGE_EXTS]
    paths = [p for p in paths if p.exists() and p.is_file()]
    return sorted(paths, key=natural_key)


def fit_to_canvas(img: Image.Image, page_size=(1920, 1080), background=(255, 255, 255)) -> Image.Image:
    img = ImageOps.exif_transpose(img).convert("RGB")
    page_w, page_h = page_size
    scale = min(page_w / img.width, page_h / img.height)
    new_w = max(1, int(img.width * scale))
    new_h = max(1, int(img.height * scale))
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", page_size, background)
    x = (page_w - new_w) // 2
    y = (page_h - new_h) // 2
    canvas.paste(resized, (x, y))
    return canvas


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble storyboard images into a 16:9 PDF.")
    parser.add_argument("--input-dir", type=Path, default=Path("."), help="Directory containing final storyboard images.")
    parser.add_argument("--output", type=Path, required=True, help="Output PDF path.")
    parser.add_argument("images", nargs="*", help="Optional explicit image paths. If supplied, input-dir scan is skipped.")
    parser.add_argument("--page-width", type=int, default=1920, help="Canvas width in pixels, default 1920.")
    parser.add_argument("--page-height", type=int, default=1080, help="Canvas height in pixels, default 1080.")
    args = parser.parse_args()

    images = collect_images(args.input_dir, args.images if args.images else None)
    if not images:
        raise SystemExit("No images found. Provide --input-dir or explicit image paths.")

    pages = []
    for path in images:
        with Image.open(path) as img:
            pages.append(fit_to_canvas(img, (args.page_width, args.page_height)))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    first, rest = pages[0], pages[1:]
    first.save(args.output, save_all=True, append_images=rest, resolution=150)

    print(f"Wrote {args.output} with {len(pages)} pages.")
    for i, p in enumerate(images, 1):
        print(f"{i:02d}: {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
