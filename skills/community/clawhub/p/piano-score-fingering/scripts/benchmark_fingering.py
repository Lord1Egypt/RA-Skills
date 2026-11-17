#!/usr/bin/env python3
"""Measure exact fingering agreement against a PIG reference excerpt.

The PIG source is supplied by the caller and is never copied into this Skill.
It is useful for regression testing because it carries a finger label for every
note.  The result is an exact-match metric, not a claim that alternatives are
musically invalid.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

from fingering_core import Hand, INote
from fingering_core.models import keypos_midi
from generate_fingering_plan import postprocess


PCS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
BLACK = {1, 3, 6, 8, 10}


def midi(name: str) -> int:
    step = name[0].upper()
    if step not in PCS or not name[-1].isdigit():
        raise ValueError(f"unsupported PIG pitch: {name!r}")
    accidental, octave = name[1:-1], int(name[-1])
    return (octave + 1) * 12 + PCS[step] + accidental.count("#") - accidental.count("b") - accidental.count("-")


def load_pig(path: Path) -> list[tuple[float, float, int, int, int]]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line or line.startswith("//"):
            continue
        fields = line.split()
        if len(fields) < 8:
            raise ValueError(f"PIG row {line_number} has fewer than 8 fields")
        finger_text = fields[7].split("_", 1)[0]
        finger = abs(int(finger_text))
        if finger not in {1, 2, 3, 4, 5}:
            raise ValueError(f"PIG row {line_number} has invalid finger {finger_text!r}")
        rows.append((float(fields[1]), float(fields[2]), midi(fields[3]), int(fields[6]), finger))
    if not rows:
        raise ValueError("PIG file has no playable notes")
    return rows


def evaluate(rows: list[tuple[float, float, int, int, int]], left: bool, max_notes: int, depth: int) -> dict:
    rows = [row for row in rows if bool(row[3]) is left]
    if max_notes:
        rows = rows[:max_notes]
    events: dict[float, list[tuple[float, float, int, int, int]]] = defaultdict(list)
    for row in rows:
        events[row[0]].append(row)
    notes: list[INote] = []
    expected: list[int] = []
    for event_id, (onset, members) in enumerate(sorted(events.items())):
        members.sort(key=lambda row: row[2])
        for chord_row, row in enumerate(members):
            pitch = row[2]
            notes.append(INote(
                pitch=pitch,
                x=keypos_midi(INote(pitch=pitch)),
                time=onset,
                duration=max(0.0, row[1] - row[0]),
                measure=1,
                chordnr=chord_row,
                NinChord=len(members),
                chordID=event_id,
                isChord=len(members) > 1,
                isBlack=pitch % 12 in BLACK,
            ))
            expected.append(row[4])
    solver = Hand(notes, side="left" if left else "right", size="M")
    solver.verbose = False
    solver.max_auto_depth = depth
    started = time.perf_counter()
    solver.generate()
    # Benchmark the Skill's actual production chain, including deterministic
    # accompaniment/chord repairs, rather than only its raw search core.
    records = []
    for index, (note, truth) in enumerate(zip(notes, expected)):
        records.append({
            "note_id": f"benchmark-{left}-{index}",
            "measure_index": 1,
            "onset": note.time,
            "event_index": int(note.chordID),
            "chord_id": f"benchmark-{left}-{note.chordID}",
            "chord_row": note.chordnr,
            "chord_size": note.NinChord,
            "pitch_midi": int(note.pitch),
            "finger": int(note.fingering),
            "locked": False,
            "placement": "below" if left else "above",
        })
    postprocess(records, "LH" if left else "RH")
    predicted = [int(record["finger"]) for record in records]
    matches = sum(a == b for a, b in zip(predicted, expected))
    return {
        "hand": "LH" if left else "RH",
        "notes": len(expected),
        "exact_matches": matches,
        "exact_accuracy": matches / len(expected),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="caller-supplied PIG reference file")
    parser.add_argument("-o", "--output", type=Path, help="optional JSON report")
    parser.add_argument("--max-notes", type=int, default=0, help="cap each hand for a quick regression")
    parser.add_argument("--max-auto-depth", type=int, choices=range(4, 8), default=4)
    parser.add_argument("--minimum", type=float, default=0.0, help="fail when aggregate exact accuracy is lower")
    args = parser.parse_args()
    if args.max_notes < 0 or not 0 <= args.minimum <= 1:
        parser.error("--max-notes must be non-negative and --minimum must be 0..1")
    rows = load_pig(args.input)
    results = [evaluate(rows, left=False, max_notes=args.max_notes, depth=args.max_auto_depth), evaluate(rows, left=True, max_notes=args.max_notes, depth=args.max_auto_depth)]
    total = sum(item["notes"] for item in results)
    matched = sum(item["exact_matches"] for item in results)
    report = {"metric": "exact reference-finger agreement", "results": results, "aggregate_accuracy": matched / total, "notes": total}
    text = json.dumps(report, ensure_ascii=False, indent=2)
    print(text)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    return 0 if report["aggregate_accuracy"] >= args.minimum else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
