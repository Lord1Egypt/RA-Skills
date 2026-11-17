#!/usr/bin/env python3
"""Attach generated semantic fingers to a separate visual-anchor plan safely."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from plan_io import load_plan, save_plan


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fingered_semantic_plan", type=Path)
    parser.add_argument("visual_plan", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()
    semantic = load_plan(args.fingered_semantic_plan)
    visual = load_plan(args.visual_plan)
    lookup = {str(note["note_id"]): note for note in semantic["notes"]}
    missing: list[str] = []
    for note in visual["notes"]:
        source = lookup.get(str(note["note_id"]))
        if source is None:
            missing.append(str(note["note_id"]))
            continue
        if int(source["pitch_midi"]) != int(note["pitch_midi"]) or str(source["hand"]) != str(note["hand"]):
            raise ValueError(f"{note['note_id']}: semantic/visual identity mismatch")
        note["finger"] = int(source.get("finger", 0))
        note["source"] = str(source.get("source", "generated"))
        note["transition_type"] = source.get("transition_type")
        note["exception_reason"] = source.get("exception_reason")
        # Anchor verification state remains owned by the visual plan.
    if missing:
        raise ValueError(f"visual plan has {len(missing)} note(s) absent from semantic plan: {', '.join(missing[:8])}")
    visual.setdefault("generation", {})
    visual["generation"].update({"complete": True, "mode": "semantic-to-visual-merge"})
    save_plan(args.output, visual)
    print(f"Merged fingers into {len(visual['notes'])} visual notes: {args.output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
