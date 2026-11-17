#!/usr/bin/env python3
"""Promote explicitly reviewed visual notehead anchors, never candidates by default.

The input review is a human/host-produced JSON object.  It must name every
candidate note exactly once after inspecting the raw score crop.  This tool
only records that review; it does not infer a notehead or set the remaining
recognition gates, which remain the responsibility of the caller.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from plan_io import load_plan, save_plan


SCHEMA = "visual-anchor-review-v1"


def reviewed_ids(review: dict, expected: set[str], *, key: str, label: str) -> dict[str, dict]:
    if review.get("schema_version") != SCHEMA:
        raise ValueError(f"review.schema_version must be {SCHEMA!r}")
    entries = review.get(key)
    if not isinstance(entries, list):
        raise ValueError(f"review.{key} must be a list")
    confirmed: dict[str, dict] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ValueError(f"review.anchors[{index}] must be an object")
        record_id = str(entry.get(f"{label}_id", "")).strip()
        if not record_id or record_id not in expected:
            raise ValueError(f"review.{key}[{index}] has unknown/empty {label}_id")
        if record_id in confirmed:
            raise ValueError(f"review.{key} contains duplicate {record_id}")
        if entry.get("confirmed") is not True:
            raise ValueError(f"{record_id}: every {label} must be explicitly confirmed")
        confirmed[record_id] = entry
    missing = expected - set(confirmed)
    if missing:
        raise ValueError(f"review misses {len(missing)} candidate {label}(s): {sorted(missing)[:8]}")
    return confirmed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="candidate visual plan")
    parser.add_argument("review", type=Path, help=f"{SCHEMA} JSON completed after raw-crop review")
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.resolve() == args.plan.resolve():
        raise ValueError("output must not overwrite the candidate plan")
    plan = load_plan(args.plan)
    candidates = [note for note in plan.get("notes", []) if note.get("anchor_candidate") is True]
    if not candidates or len(candidates) != len(plan.get("notes", [])):
        raise ValueError("plan must contain a complete candidate anchor set")
    ids = {str(note["note_id"]) for note in candidates}
    if len(ids) != len(candidates):
        raise ValueError("candidate plan has duplicate note_id values")
    review = json.loads(args.review.read_text(encoding="utf-8"))
    reviewed_ids(review, ids, key="anchors", label="note")
    rests = list(plan.get("rests", []))
    rest_ids = {str(rest.get("rest_id", "")) for rest in rests}
    if len(rest_ids) != len(rests) or "" in rest_ids:
        raise ValueError("candidate plan has duplicate/empty rest_id values")
    reviewed_rests = reviewed_ids(review, rest_ids, key="rests", label="rest")
    for note in candidates:
        note["anchor_verified"] = True
        note["pitch_geometry_verified"] = True
        note["symbol_class"] = "notehead"
        note["notehead_shape_verified"] = True
        note["chord_member_verified"] = int(note.get("chord_size", 1)) > 1
        note["anchor_candidate"] = False
        note["anchor_method"] = "manual_visual_anchor_review"
        note["origin"] = "direct_visual_notehead"
    for rest in rests:
        entry = reviewed_rests[str(rest["rest_id"])]
        try:
            rest["page_x"] = float(entry["page_x"])
            rest["page_y"] = float(entry["page_y"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"{rest['rest_id']}: confirmed rest needs numeric page_x/page_y") from exc
        rest["rest_candidate"] = False
        rest["rest_shape_verified"] = True
    recognition = plan.setdefault("recognition", {})
    recognition["anchor_review"] = {
        "schema_version": SCHEMA,
        "reviewed_notes": len(candidates),
        "reviewed_rests": len(rests),
        "source": "raw_score_crop",
    }
    policy = recognition.setdefault("confidence_policy", {})
    policy.update({
        "require_direct_notehead_anchors": True,
        "require_notehead_shape_evidence": True,
        "require_rest_inventory": True,
        "require_measure_region_coverage": True,
        "require_measure_symbol_checks": True,
    })
    recognition["status"] = "review"
    recognition.pop("fact_lock", None)
    save_plan(args.output, plan)
    print(json.dumps({"reviewed_notes": len(candidates), "reviewed_rests": len(rests), "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
