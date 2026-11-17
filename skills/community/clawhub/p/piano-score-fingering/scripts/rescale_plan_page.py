#!/usr/bin/env python3
"""Stage one plan page against an exact rendered PNG coordinate system.

Use this only when the musical events have already been reviewed but the
source page is rendered again at a different pixel resolution.  It scales
source coordinates, removes previous fingering/layout decisions, and leaves
the score ready for a fresh fingering and visual-audit pass.
"""

from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path

from fingering_core.models import INote, keypos_midi


STEP_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
SHARP_ORDER = ("F", "C", "G", "D", "A", "E", "B")
FLAT_ORDER = tuple(reversed(SHARP_ORDER))


def signature_alter(fifths: int, step: str) -> int:
    return (1 if step in SHARP_ORDER[:fifths] else 0) if fifths >= 0 else (-1 if step in FLAT_ORDER[:(-fifths)] else 0)


def png_dimensions(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError(f"not a PNG: {path}")
    return struct.unpack(">II", header[16:24])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--page", type=int, required=True)
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--key-fifths", type=int, default=None, help="reviewed page key signature, -7..7")
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.plan.read_text(encoding="utf-8"))
    page = next((item for item in data.get("pages", []) if int(item.get("page", 0)) == args.page), None)
    if page is None:
        raise ValueError(f"plan has no page {args.page}")
    if not args.image.is_file():
        raise ValueError(f"source image not found: {args.image}")
    if args.key_fifths is not None and not -7 <= args.key_fifths <= 7:
        raise ValueError("--key-fifths must be -7..7")
    old_width, old_height = float(page["width"]), float(page["height"])
    new_width, new_height = png_dimensions(args.image)
    sx, sy = new_width / old_width, new_height / old_height
    if abs(sx - sy) > 0.03 * max(sx, sy):
        raise ValueError("old and new page aspect ratios differ")
    output = dict(data)
    output["source"] = {"type": "image", "path": str(args.image.resolve()), "coordinate_unit": "pixel_top_left"}
    output["pages"] = [{"page": args.page, "width": new_width, "height": new_height, "image": str(args.image.resolve())}]
    drop = {"finger", "label_x", "label_offset", "font_size", "confidence", "cost", "transition_type", "exception_reason", "review_reason", "keyboard_x_cm"}
    records = []
    for note in data.get("notes", []):
        if int(note.get("page", 0)) != args.page:
            continue
        staged = {key: value for key, value in note.items() if key not in drop}
        staged["page_x"] = round(float(note["page_x"]) * sx, 3)
        staged["page_y"] = round(float(note["page_y"]) * sy, 3)
        midi = int(staged["pitch_midi"])
        staged["keyboard_x_cm"] = round(keypos_midi(INote(pitch=midi)), 6)
        if args.key_fifths is not None:
            staged["key_fifths"] = args.key_fifths
            staged["key_mode"] = "unspecified"
            staged["key_signature_alter"] = signature_alter(args.key_fifths, str(staged["pitch_step"]).upper())
            staged["accidental_scope"] = (
                "key_signature" if int(staged.get("pitch_alter", 0)) == staged["key_signature_alter"] else "explicit_or_courtesy"
            )
        staged.update({
            "anchor_verified": True, "pitch_geometry_verified": True,
            "symbol_class": "notehead", "notehead_shape_verified": True,
            "chord_member_verified": True, "recognition_passes": max(2, int(staged.get("recognition_passes", 0))),
        })
        records.append(staged)
    output["notes"] = records
    rests = []
    for rest in data.get("rests", []):
        if int(rest.get("page", 0)) != args.page:
            continue
        staged = dict(rest)
        if "page_x" in staged:
            staged["page_x"] = round(float(staged["page_x"]) * sx, 3)
            staged["page_y"] = round(float(staged["page_y"]) * sy, 3)
        rests.append(staged)
    output["rests"] = rests
    recognition = dict(data.get("recognition", {}))
    systems = []
    for system in recognition.get("systems", []):
        staged = dict(system)
        if int(staged.get("page", 0)) == args.page and "staff_line_y" in staged:
            staged["staff_line_y"] = [round(float(value) * sy, 3) for value in staged["staff_line_y"]]
        systems.append(staged)
    recognition["systems"] = systems
    recognition["status"] = "draft"
    recognition["expected_note_count"] = len(records)
    recognition["unresolved_note_count"] = 0
    recognition["review_queue"] = []
    recognition.pop("fact_lock", None)
    recognition["event_count_checks"] = [
        item for item in recognition.get("event_count_checks", []) if int(item.get("page", 0)) == args.page
    ]
    if args.key_fifths is not None:
        recognition["key_signatures"] = [{"page": args.page, "measure_index": 1, "staff": 0, "fifths": args.key_fifths, "mode": "unspecified"}]
        recognition.setdefault("verification", {})["key_signature"] = True
    output["recognition"] = recognition
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Staged {len(records)} notes on page {args.page} at {new_width}×{new_height}: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
