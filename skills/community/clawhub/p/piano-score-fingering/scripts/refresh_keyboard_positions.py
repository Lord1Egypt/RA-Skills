#!/usr/bin/env python3
"""Refresh derived piano-key coordinates in an older score-fact plan.

This migration deliberately changes no musical fact, visual anchor, or
fingering.  It only recomputes ``keyboard_x_cm`` from each stored MIDI pitch,
then returns the plan to verified state so the normal recognition lock gate
must run again before fingering generation.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from fingering_core import INote, keypos_midi
from plan_io import load_plan, save_plan


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.resolve() == args.input.resolve():
        raise ValueError("output must not overwrite the source plan")
    plan = load_plan(args.input)
    for note in plan.get("notes", []):
        note["keyboard_x_cm"] = keypos_midi(INote(pitch=int(note["pitch_midi"])))
        # The caller requested a fresh run. Existing digits must never become
        # an implicit input to the new fingering solve.
        note["finger"] = 0
        note["locked"] = False
        note["source"] = "unassigned"
    recognition = plan.setdefault("recognition", {})
    recognition.pop("fact_lock", None)
    recognition["status"] = "verified"
    save_plan(args.output, plan)
    print(f"Refreshed {len(plan.get('notes', []))} keyboard coordinates: {args.output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise SystemExit(f"ERROR: {exc}")
