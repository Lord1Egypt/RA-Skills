#!/usr/bin/env python3
"""Find fingering choices that change under two bounded search horizons.

This is a confidence audit, not a second fingering algorithm.  Agreement does
not prove an editorial choice is unique; disagreement is useful evidence that
the affected page/measure/hand deserves focused human review before a result
is presented as fully checked.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

from plan_io import load_plan


def write_report(path: Path, report: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def generate(input_plan: Path, output: Path, depth: int, *, provisional_omr: bool) -> dict:
    command = [
        sys.executable, str(Path(__file__).resolve().parent / "generate_fingering_plan.py"),
        str(input_plan), "-o", str(output), "--ignore-existing", "--max-auto-depth", str(depth), "--quiet",
    ]
    if provisional_omr:
        command.append("--provisional-omr")
    completed = subprocess.run(command, capture_output=True, text=True)
    if completed.returncode:
        detail = (completed.stderr or completed.stdout).strip()
        raise ValueError(f"depth {depth} generation failed: {detail}")
    return load_plan(output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="locked semantic plan or a generated plan with intact recognition facts")
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--shallow-depth", type=int, default=4, choices=range(4, 8))
    parser.add_argument("--deep-depth", type=int, default=7, choices=range(4, 8))
    parser.add_argument("--minimum", type=float, default=0.90)
    args = parser.parse_args()
    if not 0 < args.minimum <= 1 or args.shallow_depth >= args.deep_depth:
        parser.error("minimum must be 0..1 and shallow-depth must be lower than deep-depth")
    try:
        plan = load_plan(args.plan)
        provisional_omr = str(plan.get("source", {}).get("type", "")).lower() == "omr_candidate"
        with tempfile.TemporaryDirectory(prefix="piano-fingering-stability-") as temporary:
            directory = Path(temporary)
            shallow = generate(args.plan, directory / "shallow.json", args.shallow_depth, provisional_omr=provisional_omr)
            deep = generate(args.plan, directory / "deep.json", args.deep_depth, provisional_omr=provisional_omr)
        shallow_by_id = {str(note["note_id"]): note for note in shallow.get("notes", [])}
        deep_by_id = {str(note["note_id"]): note for note in deep.get("notes", [])}
        base_by_id = {str(note["note_id"]): note for note in plan.get("notes", [])}
        base_ids = [str(note["note_id"]) for note in plan.get("notes", [])]
        if set(base_ids) != set(shallow_by_id) or set(base_ids) != set(deep_by_id):
            raise ValueError("candidate outputs changed the note inventory")
        unstable: list[dict] = []
        reviewed_unstable: list[dict] = []
        by_scope: dict[tuple[int, int, str], list[str]] = defaultdict(list)
        for note_id in base_ids:
            left, right = shallow_by_id[note_id], deep_by_id[note_id]
            if int(left.get("finger", 0)) == int(right.get("finger", 0)):
                continue
            current = base_by_id[note_id]
            scope = (int(left.get("page", 0) or 0), int(left["measure_index"]), str(left["hand"]).upper())
            row = {
                "note_id": note_id, "page": scope[0], "measure": scope[1], "hand": scope[2],
                "pitch_midi": int(left["pitch_midi"]),
                "shallow_finger": int(left.get("finger", 0)), "deep_finger": int(right.get("finger", 0)),
            }
            # A scoped review deliberately chooses one of these two existing
            # phrase candidates. Keep the raw disagreement visible, but do
            # not make a completed review task perpetually fail the delivery
            # gate on every subsequent audit.
            if (
                current.get("review_decision")
                and int(current.get("finger", 0)) in {row["shallow_finger"], row["deep_finger"]}
            ):
                reviewed_unstable.append(row | {"review_decision": str(current["review_decision"])})
                continue
            by_scope[scope].append(note_id)
            unstable.append(row)
        total = len(base_ids)
        stable = total - len(unstable)
        accuracy = stable / total if total else 0.0
        raw_unstable = len(unstable) + len(reviewed_unstable)
        report = {
            "metric": "search-horizon fingering agreement after recorded local review (confidence signal, not editorial ground truth)",
            "shallow_depth": args.shallow_depth,
            "deep_depth": args.deep_depth,
            "provisional_omr": provisional_omr,
            "notes": total,
            "stable_notes": stable,
            "stability_accuracy": accuracy,
            "raw_unstable_notes": raw_unstable,
            "raw_stability_accuracy": (total - raw_unstable) / total if total else 0.0,
            "reviewed_unstable_notes": reviewed_unstable,
            "minimum": args.minimum,
            "passed": bool(total and accuracy >= args.minimum),
            "review_scopes": [
                {"page": page, "measure": measure, "hand": hand, "unstable_notes": len(note_ids), "note_ids": note_ids}
                for (page, measure, hand), note_ids in sorted(by_scope.items())
            ],
            "unstable_notes": unstable,
        }
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        report = {
            "metric": "search-horizon fingering agreement (confidence signal, not editorial ground truth)",
            "passed": False,
            "status": "unavailable",
            "error": str(exc),
            "stability_accuracy": 0.0,
            "review_scopes": [],
            "unstable_notes": [],
        }
        write_report(args.output, report)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2
    write_report(args.output, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
