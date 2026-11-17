#!/usr/bin/env python3
"""Render a non-delivery PNG preview of proposed/verified notehead anchors.

Blue crosses are normal candidates or verified anchors; orange crosses mark
``candidate_confidence < 0.75``.  This never mutates the plan and is for
visual review only, not a substitute for the recognition gate.
"""

from __future__ import annotations

import argparse
import struct
import sys
import zlib
from pathlib import Path

from audit_source_clearance import source_image
from plan_io import finite_number, load_plan, page_map
from render_fingering_pdf import png_pixels


def write_png(path: Path, width: int, height: int, pixels: bytes) -> None:
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    rows = b"".join(b"\x00" + pixels[row * width * 3:(row + 1) * width * 3] for row in range(height))
    payload = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    payload += chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b"")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def mark(pixels: bytearray, width: int, height: int, x: int, y: int, colour: tuple[int, int, int]) -> None:
    for dx, dy in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1), (-2, 0), (2, 0), (0, -2), (0, 2)):
        xx, yy = x + dx, y + dy
        if 0 <= xx < width and 0 <= yy < height:
            start = (yy * width + xx) * 3
            pixels[start:start + 3] = bytes(colour)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--page", type=int, default=1)
    args = parser.parse_args()
    plan = load_plan(args.plan)
    page = page_map(plan).get(args.page)
    if page is None:
        raise ValueError(f"page {args.page} is not declared")
    width, height, raw, colorspace = png_pixels(source_image(args.plan, page).read_bytes())
    if colorspace != "/DeviceRGB":
        raise ValueError("source PNG must be RGB/RGBA")
    sx = width / finite_number(page["width"], "page.width")
    sy = height / finite_number(page["height"], "page.height")
    pixels = bytearray(raw)
    count = low = 0
    for note in plan["notes"]:
        if int(note.get("page", 0)) != args.page:
            continue
        try:
            x = round(finite_number(note["page_x"], "page_x") * sx)
            y = round(finite_number(note["page_y"], "page_y") * sy)
        except (KeyError, ValueError):
            continue
        confidence = float(note.get("candidate_confidence", 1.0))
        is_low = confidence < 0.75
        mark(pixels, width, height, x, y, (231, 111, 0) if is_low else (22, 87, 170))
        count += 1
        low += int(is_low)
    write_png(args.output, width, height, bytes(pixels))
    print(f"Rendered {count} anchor crosses ({low} low-confidence): {args.output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, TypeError, zlib.error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
