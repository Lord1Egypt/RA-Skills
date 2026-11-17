#!/usr/bin/env python3
"""Compare generated fingers with explicit source fingering anchors.

Use this only for an external, caller-supplied score that already contains
editorial fingerings.  Unmarked notes are intentionally excluded: one
editorial solution is useful test evidence but not a universal ground truth.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from plan_io import load_plan


def _bucket_duration(value: float) -> str:
    """Keep timing diagnostics coarse so different divisions remain comparable."""
    if value <= 0.25 + 1.0e-6:
        return "<=sixteenth"
    if value <= 0.5 + 1.0e-6:
        return "eighth"
    if value <= 1.0 + 1.0e-6:
        return "quarter"
    return ">quarter"


def _summarize(rows: list[tuple[str, bool]]) -> dict[str, dict[str, float | int]]:
    """Return stable contextual denominators without turning one editor into truth."""
    grouped: dict[str, list[bool]] = defaultdict(list)
    for key, agrees in rows:
        grouped[key].append(agrees)
    return {
        key: {
            "anchors": len(values),
            "matches": sum(values),
            "accuracy": sum(values) / len(values),
        }
        for key, values in sorted(grouped.items())
    }


def measure_range(value: str) -> tuple[int, int]:
    parts = value.split("-", 1)
    start = int(parts[0])
    end = int(parts[1]) if len(parts) == 2 else start
    if start < 1 or end < start:
        raise ValueError("measure range must satisfy 1 <= start <= end")
    return start, end


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path, help="plan extracted from a pre-fingered source score")
    parser.add_argument("generated", type=Path, help="matching plan generated with --ignore-existing")
    parser.add_argument("--measure-range", type=measure_range)
    parser.add_argument("--minimum", type=float, default=0.80)
    parser.add_argument(
        "--max-mismatches",
        type=int,
        default=100,
        help="include at most this many contextual mismatch rows in the report (default: 100)",
    )
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    # ``0`` is useful in diagnostic mode: callers can request a complete
    # mismatch report before deciding what release threshold applies.  It must
    # not turn a valid comparison into a command-line error, because the
    # pipeline's delivery contract is to produce evidence even when a score
    # fails its quality gate.
    if not 0 <= args.minimum <= 1:
        parser.error("--minimum must be in [0, 1]")
    if args.max_mismatches < 0:
        parser.error("--max-mismatches must be non-negative")
    reference = load_plan(args.reference)
    generated = load_plan(args.generated)
    by_id = {str(note["note_id"]): note for note in generated["notes"]}
    start, end = args.measure_range or (1, 10**9)
    per_hand: dict[str, list[bool]] = defaultdict(list)
    missing: list[str] = []
    mismatched_identity: list[str] = []
    mismatch_rows: list[dict] = []
    by_hand_chord: list[tuple[str, bool]] = []
    by_hand_key: list[tuple[str, bool]] = []
    by_hand_duration: list[tuple[str, bool]] = []
    by_measure: list[tuple[str, bool]] = []
    for note in reference["notes"]:
        if not note.get("locked") or not start <= int(note["measure_index"]) <= end:
            continue
        candidate = by_id.get(str(note["note_id"]))
        if candidate is None:
            missing.append(str(note["note_id"]))
            continue
        if (int(candidate["pitch_midi"]), str(candidate["hand"])) != (int(note["pitch_midi"]), str(note["hand"])):
            mismatched_identity.append(str(note["note_id"]))
            continue
        agrees = int(candidate.get("finger", 0)) == int(note["finger"])
        hand = str(note["hand"])
        per_hand[hand].append(agrees)
        by_hand_chord.append((f"{hand}|chord-{int(note['chord_size'])}", agrees))
        key_type = "black" if int(note["pitch_midi"]) % 12 in {1, 3, 6, 8, 10} else "white"
        by_hand_key.append((f"{hand}|{key_type}", agrees))
        by_hand_duration.append((f"{hand}|{_bucket_duration(float(note['duration']))}", agrees))
        by_measure.append((f"m{int(note['measure_index'])}", agrees))
        if not agrees and len(mismatch_rows) < args.max_mismatches:
            mismatch_rows.append({
                "note_id": str(note["note_id"]),
                "measure": int(note["measure_index"]),
                "hand": str(note["hand"]),
                "pitch_midi": int(note["pitch_midi"]),
                "onset": float(note["onset"]),
                "duration": float(note["duration"]),
                "chord_size": int(note["chord_size"]),
                "expected_finger": int(note["finger"]),
                "generated_finger": int(candidate.get("finger", 0)),
                "generated_transition": candidate.get("transition_type"),
                "generated_reason": candidate.get("exception_reason"),
            })
    total = sum(len(values) for values in per_hand.values())
    matched = sum(sum(values) for values in per_hand.values())
    report = {
        "metric": "exact agreement with explicit source fingering anchors",
        "measure_range": f"{start}-{end}" if args.measure_range else "all",
        "anchors": total,
        "matches": matched,
        "accuracy": matched / total if total else 0.0,
        "per_hand": {
            hand: {"anchors": len(values), "matches": sum(values), "accuracy": sum(values) / len(values)}
            for hand, values in sorted(per_hand.items())
        },
        "missing_note_ids": missing,
        "identity_mismatches": mismatched_identity,
        "mismatch_details": mismatch_rows,
        "breakdowns": {
            "by_hand_and_chord_size": _summarize(by_hand_chord),
            "by_hand_and_key_type": _summarize(by_hand_key),
            "by_hand_and_duration": _summarize(by_hand_duration),
            "by_measure": _summarize(by_measure),
        },
    }
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    return 0 if total and report["accuracy"] >= args.minimum and not missing and not mismatched_identity else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
