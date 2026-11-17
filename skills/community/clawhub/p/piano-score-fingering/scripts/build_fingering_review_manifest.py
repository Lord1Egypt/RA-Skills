#!/usr/bin/env python3
"""Create small, score-context review tasks for unstable fingering choices."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from plan_io import load_plan, note_sort_key


def note_view(note: dict) -> dict:
    return {
        "note_id": note["note_id"], "measure": int(note["measure_index"]),
        "onset": note["onset"], "hand": note["hand"], "pitch_midi": int(note["pitch_midi"]),
        "pitch": f"{note.get('pitch_step', '?')}{int(note.get('pitch_alter', 0) or 0):+d}/{note.get('pitch_octave', '?')}",
        "duration": note["duration"], "chord_id": note["chord_id"],
        "chord_row": int(note["chord_row"]), "chord_size": int(note["chord_size"]),
        "current_finger": int(note.get("finger", 0)),
        "tie_group": note.get("tie_group"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="default generated fingering plan")
    parser.add_argument("stability_audit", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--context-events", type=int, default=4)
    args = parser.parse_args()
    if args.context_events < 1 or args.context_events > 16:
        parser.error("context-events must be 1..16")
    plan = load_plan(args.plan)
    audit = json.loads(args.stability_audit.read_text(encoding="utf-8"))
    unstable = audit.get("unstable_notes", [])
    if not isinstance(unstable, list):
        raise ValueError("stability audit must provide unstable_notes")
    by_id = {str(note["note_id"]): note for note in plan.get("notes", [])}
    candidates = {str(row.get("note_id")): row for row in unstable if isinstance(row, dict)}
    # Keep the complete hand stream.  A difficult choice at a barline often
    # depends on the arrival/departure notes in the adjacent bar, so context
    # must never be clipped to the task's own measure.
    by_hand: dict[str, list[dict]] = defaultdict(list)
    for note in plan.get("notes", []):
        by_hand[str(note["hand"]).upper()].append(note)
    grouped: dict[tuple[int, str], list[dict]] = defaultdict(list)
    for hand, notes in by_hand.items():
        for note in notes:
            if str(note["note_id"]) in candidates:
                grouped[(int(note["measure_index"]), hand)].append(note)
    tasks = []
    for (measure, hand), selected in sorted(grouped.items()):
        sequence = sorted(by_hand[hand], key=note_sort_key)
        locations = {str(note["note_id"]): index for index, note in enumerate(sequence)}
        indexes = [locations[str(note["note_id"])] for note in selected]
        start, end = max(0, min(indexes) - args.context_events), min(len(sequence), max(indexes) + args.context_events + 1)
        alternatives = []
        shallow_option = []
        deep_option = []
        for note in selected:
            row = candidates[str(note["note_id"])]
            allowed_fingers = sorted({
                int(note.get("finger", 0)),
                int(row["shallow_finger"]),
                int(row["deep_finger"]),
            } - {0})
            alternatives.append({
                "note_id": note["note_id"],
                "current_finger": int(note.get("finger", 0)),
                "shallow_finger": int(row["shallow_finger"]),
                "deep_finger": int(row["deep_finger"]),
                "allowed_fingers": allowed_fingers,
            })
            shallow_option.append({"note_id": note["note_id"], "finger": int(row["shallow_finger"])})
            deep_option.append({"note_id": note["note_id"], "finger": int(row["deep_finger"])})
        tasks.append({
            "task_id": f"m{measure}-{hand}", "measure": measure, "hand": hand,
            "reason": "two bounded searches disagree; decide only after reading the local musical phrase",
            "alternatives": alternatives,
            "candidate_options": [
                {"option_id": "shallow", "description": "default bounded-search phrase", "assignments": shallow_option},
                {"option_id": "deep", "description": "deeper-look-ahead phrase", "assignments": deep_option},
            ],
            "context": [note_view(note) for note in sequence[start:end]],
            "decision_rule": (
                "Check ties, repeated notes, chord order, hand span, key/accidentals and phrase direction. "
                "Choose one whole-phrase candidate only when it is clearly more playable; do not mix fingers from two options. Otherwise preserve the default phrase and mark unresolved."
            ),
        })
    manifest = {
        "schema_version": "1.0",
        "purpose": "targeted musical review for search-disagreement scopes; not a score-fact correction",
        "plan_fact_lock": plan.get("recognition", {}).get("fact_lock", {}),
        "tasks": tasks,
        "decision_output_format": {
            "decisions": [
                {"task_id": "<from tasks>", "option_id": "shallow|deep", "reason": "<brief musical basis>", "resolved": True}
            ]
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(tasks)} targeted fingering review task(s): {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
