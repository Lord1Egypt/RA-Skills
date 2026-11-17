#!/usr/bin/env python3
"""Report fingering positions that change under an adjacent hand-size preset.

The chosen plan remains authoritative.  This is a confidence audit: a nearby
physical calibration is generated from the same locked score, then only its
disagreements are surfaced as compact page/measure/hand review scopes.
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


SIZES = ("XXS", "XS", "S", "M", "L", "XL", "XXL")


def write_report(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def inferred_size(plan: dict) -> str:
    generation = plan.get("generation", {})
    settings = plan.get("settings", {})
    candidate = str(generation.get("hand_size") or settings.get("hand_size") or "M").upper()
    return candidate if candidate in SIZES else "M"


def neighbour(size: str) -> str:
    index = SIZES.index(size)
    # Prefer the next narrower preset. It makes the comparison a local
    # calibration check rather than an artificial small-vs-large contrast.
    return SIZES[index - 1] if index else SIZES[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_plan", type=Path, help="locked semantic plan used to create the chosen result")
    parser.add_argument("chosen_plan", type=Path, help="already generated plan whose fingers remain authoritative")
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--alternate-hand-size", choices=SIZES)
    args = parser.parse_args()
    try:
        source = load_plan(args.source_plan)
        chosen = load_plan(args.chosen_plan)
        primary = inferred_size(chosen)
        alternate = args.alternate_hand_size or neighbour(primary)
        with tempfile.TemporaryDirectory(prefix="piano-hand-size-audit-") as temporary:
            candidate_path = Path(temporary) / "alternate.json"
            command = [
                sys.executable, str(Path(__file__).with_name("generate_fingering_plan.py")),
                str(args.source_plan), "-o", str(candidate_path), "--ignore-existing",
                "--hand-size", alternate, "--quiet",
            ]
            completed = subprocess.run(command, capture_output=True, text=True)
            if completed.returncode:
                detail = (completed.stderr or completed.stdout).strip()
                raise ValueError(f"alternate {alternate} generation failed: {detail}")
            candidate = load_plan(candidate_path)
        by_chosen = {str(note["note_id"]): note for note in chosen.get("notes", [])}
        by_candidate = {str(note["note_id"]): note for note in candidate.get("notes", [])}
        if set(by_chosen) != set(by_candidate):
            raise ValueError("alternate output changed the note inventory")
        differing: list[dict] = []
        scopes: dict[tuple[int, int, str], list[str]] = defaultdict(list)
        for note_id, original in by_chosen.items():
            other = by_candidate[note_id]
            if int(original.get("finger", 0)) == int(other.get("finger", 0)):
                continue
            scope = (int(original.get("page", 0) or 0), int(original["measure_index"]), str(original["hand"]).upper())
            scopes[scope].append(note_id)
            differing.append({
                "note_id": note_id, "page": scope[0], "measure": scope[1], "hand": scope[2],
                "pitch_midi": int(original["pitch_midi"]),
                "chosen_finger": int(original.get("finger", 0)),
                "alternate_finger": int(other.get("finger", 0)),
            })
        total = len(by_chosen)
        report = {
            "metric": "adjacent hand-size fingering agreement (confidence signal, not editorial ground truth)",
            "chosen_hand_size": primary,
            "alternate_hand_size": alternate,
            "notes": total,
            "stable_notes": total - len(differing),
            "stability_accuracy": (total - len(differing)) / total if total else 0.0,
            "passed": not differing,
            "review_scopes": [
                {"page": page, "measure": measure, "hand": hand,
                 "unstable_notes": len(note_ids), "note_ids": note_ids}
                for (page, measure, hand), note_ids in sorted(scopes.items())
            ],
            "unstable_notes": differing,
        }
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        report = {
            "metric": "adjacent hand-size fingering agreement (confidence signal, not editorial ground truth)",
            "passed": False, "status": "unavailable", "error": str(exc),
            "stability_accuracy": 0.0, "review_scopes": [], "unstable_notes": [],
        }
    write_report(args.output, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report.get("passed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
