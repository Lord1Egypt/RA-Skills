#!/usr/bin/env python3
"""Score rule-compliance of a generated fingering plan, per assigned note.

This is not an editorial-fingering comparator.  It measures whether each
generated label participates in a mechanically and musically valid local
action.  Use it alongside compare_reference_fingerings.py, never instead of
an explicit source-fingering comparison when one is available.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from plan_io import load_plan, note_sort_key


def event_key(note: dict) -> tuple:
    return (note["part"], note["hand"], note["measure_index"], note["onset"], note["event_index"], note["chord_id"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--minimum", type=float, default=0.80)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    # Diagnostic callers need a report even when they intentionally defer the
    # release threshold.  Accept zero as that no-gate mode; the report still
    # records every violation and a normal threshold continues to gate exit 0.
    if not 0 <= args.minimum <= 1:
        parser.error("--minimum must be in [0, 1]")
    plan = load_plan(args.plan)
    all_notes = list(plan["notes"])
    notes = [note for note in all_notes if int(note.get("finger", 0)) in {1, 2, 3, 4, 5}]
    bad: dict[str, set[str]] = defaultdict(set)
    for note in all_notes:
        if int(note.get("finger", 0)) not in {1, 2, 3, 4, 5}:
            bad[str(note.get("note_id", "unknown"))].add("missing final finger")
    by_hand: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for note in notes:
        by_hand[(str(note["part"]), str(note["hand"]))].append(note)
        if int(note["finger"]) not in {1, 2, 3, 4, 5}:
            bad[str(note["note_id"])].add("invalid finger")

    for (_, hand), sequence in by_hand.items():
        sequence.sort(key=note_sort_key)
        events: dict[tuple, list[dict]] = defaultdict(list)
        for note in sequence:
            events[event_key(note)].append(note)
        ordered = [sorted(group, key=lambda note: int(note["pitch_midi"])) for _, group in sorted(events.items())]
        for group in ordered:
            fingers = [int(note["finger"]) for note in group]
            if len(fingers) > 1:
                if len(set(fingers)) != len(fingers):
                    for note in group: bad[str(note["note_id"])].add("reused finger in chord")
                expected = sorted(fingers, reverse=hand == "LH")
                if fingers != expected:
                    for note in group: bad[str(note["note_id"])].add("chord finger order")
        # Keep the physical-event position.  Filtering all chords first and
        # then zipping singleton notes falsely treats e.g. ``single -> chord
        # -> single`` as one continuous single-note line, even though the hand
        # has made an intervening action.  This used to create false
        # same-finger violations and downgrade otherwise usable output.
        singles = [(index, group[0]) for index, group in enumerate(ordered) if len(group) == 1]
        for (prior_position, prior), (current_position, current) in zip(singles, singles[1:]):
            if current_position - prior_position > 1 or current.get("preceding_rest"):
                continue
            same_pitch = int(prior["pitch_midi"]) == int(current["pitch_midi"])
            same_finger = int(prior["finger"]) == int(current["finger"])
            reset = current.get("connection") == "detached" or current.get("transition_type") in {"leap", "substitution", "repeated_note"}
            if not same_pitch and same_finger and not reset:
                bad[str(prior["note_id"])].add("same finger on connected new pitch")
                bad[str(current["note_id"])].add("same finger on connected new pitch")
        if hand == "LH":
            for prior, current in zip(ordered, ordered[1:]):
                if len(prior) != 1 or len(current) != 2:
                    continue
                bass = prior[0]
                if int(bass["pitch_midi"]) >= min(int(note["pitch_midi"]) for note in current):
                    continue
                if int(bass["finger"]) != 5 and bass.get("exception_verified") is not True:
                    bad[str(bass["note_id"])].add("outer bass is not finger 5")
                span = int(current[1]["pitch_midi"]) - int(current[0]["pitch_midi"])
                if span in {3, 4} and [int(note["finger"]) for note in current] != [3, 1]:
                    for note in current: bad[str(note["note_id"])].add("LH third dyad is not 3-1")

    # The denominator is every recognised score note, not only notes which
    # already received a label.  Otherwise an omitted note makes the score
    # look better instead of lowering it.
    total = len(all_notes)
    clean = total - len(bad)
    report = {
        "metric": "per-note rule-compliance (not editorial exact match)",
        "notes": total,
        "assigned_notes": len(notes),
        "coverage": len(notes) / total if total else 0.0,
        "compliant_notes": clean,
        "quality_accuracy": clean / total if total else 0.0,
        "violations": {key: sorted(value) for key, value in sorted(bad.items())},
    }
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    return 0 if total and report["quality_accuracy"] >= args.minimum else 2


if __name__ == "__main__":
    raise SystemExit(main())
