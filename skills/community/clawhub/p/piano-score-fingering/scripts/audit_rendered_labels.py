#!/usr/bin/env python3
"""Verify that coloured fingering glyphs survived at their planned anchors.

This is a post-render check.  Give it a PNG rendered from the *output* PDF at
the same page size/aspect ratio as the source page.  It deliberately detects
only the renderer's blue (RH) and burgundy (LH) ink, so black source notation
cannot be mistaken for a newly printed fingering mark.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from plan_io import finite_number, load_plan, page_map
from render_fingering_pdf import COLORS, png_pixels


def is_label_ink(red: int, green: int, blue: int, hand: str) -> bool:
    """Accept anti-aliased pixels close to the renderer's declared colour."""
    target = COLORS[hand]
    expected = tuple(round(component * 255) for component in target)
    distance = abs(red - expected[0]) + abs(green - expected[1]) + abs(blue - expected[2])
    # White anti-aliasing moves all channels upwards, while the source score is
    # near-neutral black.  The hue test avoids matching either.
    return distance <= 150 and max(red, green, blue) - min(red, green, blue) >= 24


def rendered_position(
    note: dict,
    members: list[dict],
    sx: float,
    sy: float,
    height: float,
    source_dpi: float,
) -> tuple[float, float, float]:
    """Mirror the renderer's baseline calculation in top-left PNG coordinates."""
    size = finite_number(note.get("font_size", 10), "font_size")
    # The plan is expressed in source-image pixels, while the label is a PDF
    # point size.  After the PDF is rasterized, a 10 pt glyph is not 10 PNG
    # pixels.  The old audit mixed these units, causing false "unexpected
    # ink" failures immediately after a legitimate clearance repair.
    font_px = size * sx * source_dpi / 72.0
    stacked = len(members) > 1 and note.get("chord_label_layout", "stacked") == "stacked"
    if stacked:
        x = finite_number(note.get("chord_label_x", sum(float(item["page_x"]) for item in members) / len(members)), "chord_label_x") * sx
        anchors = [height - float(item["page_y"]) * sy for item in members]
        offset = finite_number(note.get("chord_label_offset", note.get("label_offset", 20)), "chord_label_offset") * sy
        row = int(note.get("chord_row", 0))
        baseline = max(anchors) + offset + row * font_px * 1.15 if note["placement"] == "above" else min(anchors) - offset + row * font_px * 1.15
    else:
        x = finite_number(note.get("label_x", note["page_x"]), "label_x") * sx
        anchor = height - float(note["page_y"]) * sy
        offset = finite_number(note.get("label_offset", 20), "label_offset") * sy
        baseline = anchor + offset if note["placement"] == "above" else anchor - offset
    # The PDF writer positions the glyph with this baseline adjustment.
    return x, height - (baseline - font_px * 0.34), font_px


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("rendered_png", type=Path, help="PNG rendered from the final one-page PDF")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument(
        "--source-dpi", type=float, default=144.0,
        help="the --dpi used by render_fingering_pdf.py (default: 144)",
    )
    parser.add_argument("--minimum", type=float, default=0.90)
    parser.add_argument("--max-unexpected-ink", type=int, default=1,
                        help="maximum coloured fingering pixels allowed outside all planned label zones")
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    if not 0 < args.minimum <= 1:
        parser.error("--minimum must be in (0, 1]")
    if args.max_unexpected_ink < 0:
        parser.error("--max-unexpected-ink must be non-negative")
    if args.source_dpi < 36 or args.source_dpi > 600:
        parser.error("--source-dpi must be between 36 and 600")
    plan = load_plan(args.plan)
    page = page_map(plan).get(args.page)
    if page is None:
        raise ValueError(f"page {args.page} is not declared by the plan")
    if args.rendered_png.suffix.lower() != ".png":
        raise ValueError("rendered output must be PNG; render the PDF page before auditing")
    width, height, pixels, colorspace = png_pixels(args.rendered_png.read_bytes())
    if colorspace != "/DeviceRGB":
        raise ValueError("rendered PNG must be RGB/RGBA")
    source_width = finite_number(page["width"], "page.width")
    source_height = finite_number(page["height"], "page.height")
    sx, sy = width / source_width, height / source_height
    if abs(sx - sy) > 0.03 * max(sx, sy):
        raise ValueError("rendered PNG aspect ratio conflicts with plan page")
    notes = [note for note in plan["notes"] if int(note.get("page", 0)) == args.page and int(note.get("finger", 0)) in {1, 2, 3, 4, 5}]
    events: dict[tuple, list[dict]] = {}
    for note in notes:
        key = (note.get("part"), note.get("measure_index"), note.get("onset"), note.get("event_index"), note.get("chord_id"), note.get("hand"))
        events.setdefault(key, []).append(note)
    found = 0
    failures: list[str] = []
    # Record the full neighbourhood of every expected label.  Recovering a
    # label at each expected anchor is insufficient: a stale/misaligned plan
    # can otherwise print an additional digit without being noticed.
    expected_ink_zone = bytearray(width * height)
    label_windows: dict[str, tuple[int, int, int, int]] = {}
    for note in notes:
        key = (note.get("part"), note.get("measure_index"), note.get("onset"), note.get("event_index"), note.get("chord_id"), note.get("hand"))
        x, y, font_px = rendered_position(note, events[key], sx, sy, float(height), args.source_dpi)
        radius_x = max(7, round(font_px * 0.9))
        radius_y = max(8, round(font_px * 1.1))
        left, right = max(0, round(x) - radius_x - 3), min(width, round(x) + radius_x + 4)
        top, bottom = max(0, round(y) - radius_y - 3), min(height, round(y) + radius_y + 4)
        label_windows[str(note["note_id"])] = (left, top, right, bottom)
        for yy in range(top, bottom):
            offset = yy * width
            expected_ink_zone[offset + left:offset + right] = b"\x01" * (right - left)
        ink = 0
        for yy in range(max(0, round(y) - radius_y), min(height, round(y) + radius_y + 1)):
            start = yy * width * 3
            for xx in range(max(0, round(x) - radius_x), min(width, round(x) + radius_x + 1)):
                red, green, blue = pixels[start + xx * 3:start + xx * 3 + 3]
                if is_label_ink(red, green, blue, str(note["hand"])):
                    ink += 1
        if ink >= 2:
            found += 1
        else:
            failures.append(f"{note['note_id']}: rendered label ink not found near planned anchor")
    unexpected_ink = 0
    for yy in range(height):
        start = yy * width * 3
        mask_start = yy * width
        for xx in range(width):
            if expected_ink_zone[mask_start + xx]:
                continue
            red, green, blue = pixels[start + xx * 3:start + xx * 3 + 3]
            if is_label_ink(red, green, blue, "RH") or is_label_ink(red, green, blue, "LH"):
                unexpected_ink += 1
    if unexpected_ink > args.max_unexpected_ink:
        failures.append(
            f"unexpected coloured fingering ink outside planned label zones: {unexpected_ink} pixel(s)"
        )
    report = {
        "metric": "rendered coloured-label recovery at planned anchors",
        "page": args.page,
        "labels": len(notes),
        "recovered_labels": found,
        "unexpected_label_ink_pixels": unexpected_ink,
        "max_unexpected_label_ink_pixels": args.max_unexpected_ink,
        "placement_accuracy": found / len(notes) if notes else 0.0,
        "failures": failures,
    }
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    return 0 if report["placement_accuracy"] >= args.minimum and not failures else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
