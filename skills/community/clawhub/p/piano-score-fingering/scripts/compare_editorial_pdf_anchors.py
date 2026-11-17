#!/usr/bin/env python3
"""Compare a generated visual plan with manually reviewed editorial PDF anchors.

The reference JSON intentionally contains only anchors that a reviewer can see
on the editorial source: page, hand, source-notehead centre and finger.  It is
therefore usable when a score has no matching MusicXML with embedded fingering.
This is an evaluator only; it never changes a plan or promotes candidate
coordinates to verified anchors.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from plan_io import load_plan


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="generated plan with page anchors and fingers")
    parser.add_argument("reference", type=Path, help="editorial-pdf-anchors-v1 JSON")
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--tolerance", type=float, default=14.0, help="maximum notehead distance in source units")
    args = parser.parse_args()
    if args.tolerance <= 0:
        parser.error("--tolerance must be positive")

    ref_data = json.loads(args.reference.read_text(encoding="utf-8"))
    if ref_data.get("schema_version") != "editorial-pdf-anchors-v1":
        raise ValueError("reference.schema_version must be editorial-pdf-anchors-v1")
    anchors = ref_data.get("anchors")
    if not isinstance(anchors, list) or not anchors:
        raise ValueError("reference.anchors must be a non-empty list")

    coordinate_unit = ref_data.get("coordinate_unit", "pdf_point")
    if coordinate_unit not in {"pdf_point", "pixel"}:
        raise ValueError("reference.coordinate_unit must be pdf_point or pixel")
    image_pages = {
        int(item["page"]): (float(item["width"]), float(item["height"]))
        for item in ref_data.get("page_images", [])
    }
    if coordinate_unit == "pixel" and not image_pages:
        raise ValueError("pixel references need page_images with page, width and height")

    plan = load_plan(args.plan)
    plan_pages = {
        int(item["page"]): (float(item["width"]), float(item["height"]))
        for item in plan.get("pages", [])
    }
    candidates = []
    for note in plan.get("notes", []):
        if not all(key in note for key in ("page", "page_x", "page_y", "hand", "finger")):
            continue
        candidates.append(note)
    used: set[str] = set()
    matches = []
    failures = []
    for index, anchor in enumerate(anchors):
        try:
            page = int(anchor["page"])
            hand = str(anchor["hand"]).upper()
            x, y = float(anchor["note_x"]), float(anchor["note_y"])
            finger = int(anchor["finger"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"anchors[{index}] needs page, hand, note_x, note_y and finger") from exc
        if hand not in {"RH", "LH"} or finger not in {1, 2, 3, 4, 5}:
            raise ValueError(f"anchors[{index}] has invalid hand/finger")
        if coordinate_unit == "pixel":
            if page not in image_pages or page not in plan_pages:
                raise ValueError(f"anchors[{index}] page needs both source and plan dimensions")
            image_width, image_height = image_pages[page]
            page_width, page_height = plan_pages[page]
            if min(image_width, image_height, page_width, page_height) <= 0:
                raise ValueError(f"anchors[{index}] has non-positive page dimensions")
            x = x * page_width / image_width
            y = y * page_height / image_height
        pitch = anchor.get("pitch_midi")
        options = []
        for note in candidates:
            if str(note["note_id"]) in used or int(note["page"]) != page or str(note["hand"]).upper() != hand:
                continue
            if pitch is not None and int(note["pitch_midi"]) != int(pitch):
                continue
            distance = math.hypot(float(note["page_x"]) - x, float(note["page_y"]) - y)
            if distance <= args.tolerance:
                options.append((distance, note))
        if not options:
            failures.append({"anchor_index": index, "reason": "no matching generated notehead"})
            continue
        distance, note = min(options, key=lambda pair: pair[0])
        used.add(str(note["note_id"]))
        matches.append({
            "anchor_index": index,
            "note_id": note["note_id"],
            "distance": round(distance, 3),
            "expected_finger": finger,
            "generated_finger": int(note["finger"]),
            "finger_match": int(note["finger"]) == finger,
        })

    comparable = len(matches)
    finger_matches = sum(item["finger_match"] for item in matches)
    report = {
        "metric": "agreement with manually reviewed editorial PDF anchors",
        "reference_title": ref_data.get("title"),
        "anchors": len(anchors),
        "matched_noteheads": comparable,
        "notehead_match_accuracy": comparable / len(anchors),
        "finger_matches": finger_matches,
        "fingering_accuracy": finger_matches / comparable if comparable else 0.0,
        "tolerance": args.tolerance,
        "reference_coordinate_unit": coordinate_unit,
        "matches": matches,
        "failures": failures,
        "warning": "This report is only valid when the reference anchors were independently read from the editorial PDF.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("anchors", "matched_noteheads", "notehead_match_accuracy", "fingering_accuracy")}, ensure_ascii=False))
    return 0 if comparable else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        raise SystemExit(1)
