#!/usr/bin/env python3
"""Propose system/measure crops for a clean, computer-typeset score PNG.

This is a *visual review aid*, not OMR.  It uses only image geometry to split
one already-rendered score page into small evidence crops.  A host model must
still verify every proposed boundary, clef, note, rest, and anchor before the
result may enter a fingering plan.  The script deliberately emits
``review_required: true`` and never writes musical facts.
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
import zlib
from pathlib import Path

from render_fingering_pdf import png_pixels


def dark(red: int, green: int, blue: int) -> bool:
    """Treat neutral notation ink as dark, ignoring coloured annotations."""
    return max(red, green, blue) < 150 and max(red, green, blue) - min(red, green, blue) < 26


def runs(values: list[int], allowed_gap: int = 0) -> list[tuple[int, int]]:
    """Group sorted coordinates, tolerating a short blank gap."""
    if not values:
        return []
    result: list[tuple[int, int]] = []
    start = previous = values[0]
    for value in values[1:]:
        if value - previous > allowed_gap + 1:
            result.append((start, previous))
            start = value
        previous = value
    result.append((start, previous))
    return result


def png_rgb(path: Path) -> tuple[int, int, bytes]:
    width, height, pixels, colorspace = png_pixels(path.read_bytes())
    if colorspace != "/DeviceRGB":
        raise ValueError("input PNG must be RGB/RGBA")
    return width, height, pixels


def write_png(path: Path, width: int, height: int, pixels: bytes) -> None:
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    rows = b"".join(b"\x00" + pixels[row * width * 3:(row + 1) * width * 3] for row in range(height))
    content = b"\x89PNG\r\n\x1a\n"
    content += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    content += chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b"")
    path.write_bytes(content)


def crop(pixels: bytes, width: int, height: int, bbox: list[int]) -> tuple[int, int, bytes]:
    x0, y0, x1, y1 = bbox
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(width, x1), min(height, y1)
    if x1 <= x0 or y1 <= y0:
        raise ValueError("empty crop")
    rows = [pixels[(row * width + x0) * 3:(row * width + x1) * 3] for row in range(y0, y1)]
    return x1 - x0, y1 - y0, b"".join(rows)


def line_centres(width: int, height: int, pixels: bytes) -> list[int]:
    """Find long horizontal staff strokes, excluding normal notehead rows."""
    counts = []
    for y in range(height):
        row = y * width * 3
        counts.append(sum(dark(*pixels[row + x * 3:row + x * 3 + 3]) for x in range(width)))
    maximum = max(counts, default=0)
    if maximum <= 0:
        return []
    # Staff lines cross most of the printed system.  A relative threshold
    # keeps this resolution independent and ignores isolated title glyphs.
    candidates = [index for index, count in enumerate(counts) if count >= max(90, int(maximum * 0.58))]
    return [round((start + end) / 2) for start, end in runs(candidates, allowed_gap=1)]


def staff_pairs(lines: list[int]) -> list[tuple[list[int], list[int]]]:
    """Return treble/bass five-line groups with broadly uniform spacing."""
    groups: list[list[int]] = []
    for offset in range(max(0, len(lines) - 4)):
        candidate = lines[offset:offset + 5]
        gaps = [right - left for left, right in zip(candidate, candidate[1:])]
        if min(gaps, default=0) < 4:
            continue
        if max(gaps) / min(gaps) <= 1.35:
            groups.append(candidate)
    pairs: list[tuple[list[int], list[int]]] = []
    used: set[tuple[int, ...]] = set()
    for top in groups:
        key = tuple(top)
        if key in used:
            continue
        spacing = sum(right - left for left, right in zip(top, top[1:])) / 4
        for bottom in groups:
            if bottom[0] <= top[-1] + spacing * 2.4:
                continue
            if bottom[0] - top[-1] > spacing * 10.0:
                continue
            if abs((sum(right - left for left, right in zip(bottom, bottom[1:])) / 4) - spacing) > spacing * 0.4:
                continue
            pairs.append((top, bottom))
            used.add(key)
            used.add(tuple(bottom))
            break
    return pairs


def barline_xs(pixels: bytes, width: int, height: int, y0: int, y1: int) -> list[int]:
    # System context can legitimately extend above/below a cropped source
    # image.  Clamp before byte indexing; negative slices otherwise yield an
    # incomplete RGB tuple and make clean score crops fail unexpectedly.
    y0, y1 = max(0, y0), min(height, y1)
    if y1 <= y0:
        return []
    band_height = max(1, y1 - y0)
    counts: list[int] = []
    continuous: list[int] = []
    for x in range(width):
        dark_rows = [
            y for y in range(y0, y1)
            if dark(*pixels[(y * width + x) * 3:(y * width + x) * 3 + 3])
        ]
        counts.append(len(dark_rows))
        # A note stem can be very tall, and two stems on the grand staff can
        # even satisfy a total-ink threshold.  A true barline has one nearly
        # continuous run spanning the gap between staves; require that run.
        continuous.append(max((end - start + 1 for start, end in runs(dark_rows, allowed_gap=1)), default=0))
    candidates = [
        x for x, count in enumerate(counts)
        if count >= max(24, int(band_height * 0.56))
        and continuous[x] >= int(band_height * 0.62)
    ]
    return [round((start + end) / 2) for start, end in runs(candidates, allowed_gap=1)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="one locally rendered clean score PNG")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--first-measure", type=int, default=1)
    parser.add_argument("--measure-padding", type=int, default=12, help="horizontal context retained past each barline")
    parser.add_argument("--no-crops", action="store_true", help="write only the proposed-boundary JSON")
    args = parser.parse_args()
    if args.page < 1 or args.first_measure < 1 or args.measure_padding < 0 or args.measure_padding > 80:
        parser.error("page/first-measure must be positive; measure-padding must be 0..80")
    width, height, pixels = png_rgb(args.input)
    pairs = staff_pairs(line_centres(width, height, pixels))
    if not pairs:
        raise ValueError("could not find paired five-line staves; use a clean rendered page and review manually")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    systems: list[dict] = []
    measure_index = args.first_measure
    for system_index, (treble, bass) in enumerate(pairs, 1):
        space = sum(right - left for left, right in zip(treble, treble[1:])) / 4
        y0 = round(treble[0] - space * 2.4)
        y1 = round(bass[-1] + space * 2.4)
        bars = barline_xs(pixels, width, height, y0, y1)
        # A single detected bar cannot delimit a usable measure.  Preserve
        # the system for review, but do not invent boundaries.
        measures: list[dict] = []
        for left, right in zip(bars, bars[1:]):
            # Repeat/end barlines are often detected as two nearby vertical
            # strokes.  They are not a tiny measure.  Seven staff spaces is
            # intentionally conservative: an unusually short pickup is left
            # for manual addition rather than silently shifting every later
            # measure index.
            if right - left < space * 7:
                continue
            # Noteheads, accidentals and clefs can visually extend across a
            # barline.  Keep review evidence padded, but retain an unpadded
            # barline box for timing/layout projection.
            padded_left = max(0, left - args.measure_padding)
            padded_right = min(width, right + 1 + args.measure_padding)
            measure = {
                "page": args.page, "measure_index": measure_index,
                "bbox": [padded_left, y0, padded_right, y1],
                "barline_bbox": [left, y0, right + 1, y1],
            }
            for hand, lines in (("RH", treble), ("LH", bass)):
                hand_bbox = [padded_left, round(lines[0] - space * 2.0), padded_right, round(lines[-1] + space * 2.0)]
                filename = f"p{args.page}-m{measure_index:03d}-{hand}.png"
                measure[hand] = {"bbox": hand_bbox, "evidence_crop": filename}
                if not args.no_crops:
                    crop_width, crop_height, crop_pixels = crop(pixels, width, height, hand_bbox)
                    write_png(args.out_dir / filename, crop_width, crop_height, crop_pixels)
            measures.append(measure)
            measure_index += 1
        systems.append({
            "system_id": f"p{args.page}-system-{system_index}",
            "bbox": [0, y0, width, y1],
            "treble_staff_line_y": treble,
            "bass_staff_line_y": bass,
            "detected_barline_x": bars,
            "measures": measures,
        })
    report = {
        "source_image": str(args.input), "page": args.page, "width": width, "height": height,
        "review_required": True,
        "warning": "Geometry proposals only. Verify every system, barline, crop, clef and measure index against the raw page before creating recognition facts.",
        "systems": systems,
    }
    output = args.out_dir / "proposed-regions.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    count = sum(len(system["measures"]) for system in systems)
    print(f"Proposed {len(systems)} system(s), {count} measure(s): {output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, TypeError, zlib.error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
