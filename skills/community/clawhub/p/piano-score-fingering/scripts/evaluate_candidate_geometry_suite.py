#!/usr/bin/env python3
"""Aggregate provisional OMR label geometry without claiming semantic accuracy.

This benchmark is intentionally separate from the verified visual benchmark.
It measures whether candidate notehead anchors survive layout and PDF export,
and how many candidate notes could be printed.  Pitch, rhythm, ties, chords and
hand assignment remain outside this metric until raw-page review locks them.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from plan_io import load_plan


def read_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def resolve(base: Path, raw: object) -> Path:
    if not isinstance(raw, str) or not raw:
        raise ValueError("missing artifact path")
    path = Path(raw)
    return path if path.is_absolute() else base / path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--minimum-placement", type=float, default=0.90)
    parser.add_argument("--minimum-coverage", type=float, default=0.80)
    parser.add_argument("--minimum-holdout-pieces", type=int, default=0)
    parser.add_argument("--minimum-holdout-labels", type=int, default=0)
    args = parser.parse_args()
    if (
        not 0 < args.minimum_placement <= 1 or not 0 < args.minimum_coverage <= 1
        or args.minimum_holdout_pieces < 0 or args.minimum_holdout_labels < 0
    ):
        parser.error("minimums must be in (0, 1]")
    manifest = read_object(args.manifest)
    if manifest.get("schema_version") != "candidate-geometry-suite-v1":
        raise ValueError("manifest.schema_version must be candidate-geometry-suite-v1")
    pieces = manifest.get("pieces")
    if not isinstance(pieces, list) or len(pieces) < 3:
        raise ValueError("candidate geometry suite needs at least three pieces")
    base = args.manifest.parent
    rows = []
    total_notes = total_labels = total_owned = total_anchored = total_clear = total_recovered = 0
    roles = {
        "development": {"pieces": 0, "notes": 0, "labels": 0, "owned": 0, "anchored": 0, "clear": 0, "recovered": 0},
        "holdout": {"pieces": 0, "notes": 0, "labels": 0, "owned": 0, "anchored": 0, "clear": 0, "recovered": 0},
    }
    for entry in pieces:
        identifier = str(entry.get("id", ""))
        role = str(entry.get("benchmark_role", "development")).lower()
        if role not in roles:
            raise ValueError(f"{identifier}: benchmark_role must be development or holdout")
        plan = load_plan(resolve(base, entry.get("plan")))
        placement = read_object(resolve(base, entry.get("placement")))
        source_anchor = read_object(resolve(base, entry.get("source_anchor")))
        source_clearance = read_object(resolve(base, entry.get("source_clearance")))
        rendered = read_object(resolve(base, entry.get("rendered")))
        if str(plan.get("source", {}).get("type", "")).lower() != "omr_candidate":
            raise ValueError(f"{identifier}: plan is not an OMR candidate")
        notes = len(plan.get("notes", []))
        labels = sum(int(note.get("finger", 0) or 0) in {1, 2, 3, 4, 5} for note in plan.get("notes", []))
        if labels < 1 or any(int(report["labels" if "labels" in report else "anchors"]) != labels for report in (
            placement, source_anchor, source_clearance, rendered
        )):
            raise ValueError(f"{identifier}: audit denominator does not equal printed labels")
        if any(
            note.get("anchor_candidate") is not True
            for note in plan.get("notes", [])
            if int(note.get("finger", 0) or 0) in {1, 2, 3, 4, 5}
        ):
            raise ValueError(f"{identifier}: a printed label lacks a transactional candidate anchor")
        owned = int(placement["unambiguous_labels"])
        anchored = int(source_anchor["valid_anchors"])
        clear = int(source_clearance["clear_labels"])
        recovered = int(rendered["recovered_labels"])
        total_notes += notes; total_labels += labels; total_owned += owned
        total_anchored += anchored; total_clear += clear; total_recovered += recovered
        role_totals = roles[role]
        role_totals["pieces"] += 1; role_totals["notes"] += notes; role_totals["labels"] += labels
        role_totals["owned"] += owned; role_totals["anchored"] += anchored
        role_totals["clear"] += clear; role_totals["recovered"] += recovered
        rows.append({
            "id": identifier, "benchmark_role": role, "notes": notes, "printed_labels": labels,
            "coverage": labels / notes if notes else 0.0,
            "unambiguous_owners": owned, "ownership_accuracy": owned / labels,
            "valid_source_anchors": anchored, "source_anchor_accuracy": anchored / labels,
            "clear_labels": clear, "source_clearance_accuracy": clear / labels,
            "recovered_labels": recovered, "rendered_accuracy": recovered / labels,
            "placement_accuracy": min(owned, anchored, clear, recovered) / labels,
        })
    coverage = total_labels / total_notes
    placement_accuracy = min(total_owned, total_anchored, total_clear, total_recovered) / total_labels
    role_rows = {}
    for role, values in roles.items():
        labels = values["labels"]
        notes = values["notes"]
        role_rows[role] = values | {
            "coverage": labels / notes if notes else None,
            "placement_accuracy": min(values["owned"], values["anchored"], values["clear"], values["recovered"]) / labels if labels else None,
        }
    holdout_required = args.minimum_holdout_pieces > 0 or args.minimum_holdout_labels > 0
    holdout = role_rows["holdout"]
    holdout_passed = (
        not holdout_required or (
            holdout["pieces"] >= args.minimum_holdout_pieces
            and holdout["labels"] >= args.minimum_holdout_labels
            and holdout["coverage"] is not None and holdout["coverage"] >= args.minimum_coverage
            and holdout["placement_accuracy"] is not None and holdout["placement_accuracy"] >= args.minimum_placement
        )
    )
    result = {
        "scope": "candidate notehead geometry and rendered labels only; score semantics remain review-required",
        "pieces": rows,
        "by_role": role_rows,
        "holdout": {"required": holdout_required, "passed": holdout_passed},
        "overall": {
            "pieces": len(rows), "notes": total_notes, "printed_labels": total_labels,
            "coverage": coverage, "unambiguous_owners": total_owned,
            "ownership_accuracy": total_owned / total_labels,
            "valid_source_anchors": total_anchored,
            "source_anchor_accuracy": total_anchored / total_labels,
            "clear_labels": total_clear,
            "source_clearance_accuracy": total_clear / total_labels,
            "recovered_labels": total_recovered,
            "rendered_accuracy": total_recovered / total_labels,
            "placement_accuracy": placement_accuracy,
            "passed": coverage >= args.minimum_coverage and placement_accuracy >= args.minimum_placement and holdout_passed,
        },
        "minimums": {"coverage": args.minimum_coverage, "placement": args.minimum_placement},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["overall"]["passed"] else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        raise SystemExit(1)
