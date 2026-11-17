#!/usr/bin/env python3
"""Restrict an OMR fingering candidate to visual noteheads with safe geometry.

This is deliberately a presentation fallback, not recognition approval.  It
keeps fingers only where Audiveris supplied a transactionally attached
``anchor_candidate``; every other note remains unlabelled so an OMR miss can
never shift a long run of printed numbers onto later noteheads.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from plan_io import load_plan, save_plan
from source_provenance import file_digest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="fingered local OMR candidate plan")
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()

    plan = load_plan(args.input)
    if str(plan.get("source", {}).get("type", "")).lower() != "omr_candidate":
        raise ValueError("provisional output requires source.type=omr_candidate")

    kept = hidden = 0
    for note in plan.get("notes", []):
        finger = int(note.get("finger", 0) or 0)
        if finger not in {1, 2, 3, 4, 5}:
            continue
        anchored = note.get("anchor_candidate") is True and all(
            key in note for key in ("page", "page_x", "page_y")
        )
        if anchored:
            kept += 1
            note["provisional_label"] = True
        else:
            hidden += 1
            note["finger"] = 0
            note["provisional_label"] = False
            for field in ("label_x", "label_offset", "chord_label_x", "chord_label_offset"):
                note.pop(field, None)

    if not kept:
        raise ValueError("candidate has no transactionally attached notehead anchors to render")
    recognition = plan.setdefault("recognition", {})
    assets = [item for item in recognition.get("source_assets", []) if isinstance(item, dict) and item.get("role") != "rendered_page"]
    for page in plan.get("pages", []):
        try:
            number = int(page["page"])
            image = Path(str(page["image"])).resolve()
        except (KeyError, TypeError, ValueError):
            continue
        if not image.is_file():
            raise ValueError(f"page {number}: rendered source image is missing")
        assets.append({
            "role": "rendered_page", "page": number, "path": str(image),
            "sha256": file_digest(image), "bytes": image.stat().st_size,
        })
    recognition["source_assets"] = assets
    provisional = recognition.setdefault("provisional_omr", {})
    provisional.update({
        "status": "review_required",
        "labelled_noteheads": kept,
        "unlabelled_notes": hidden,
        "rule": "only transactionally attached candidate anchors are printed",
    })
    save_plan(args.output, plan)
    print(f"Wrote provisional plan with {kept} anchored labels; withheld {hidden} unanchored labels.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}")
        raise SystemExit(1)
