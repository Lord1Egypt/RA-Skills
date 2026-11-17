#!/usr/bin/env python3
"""Validate a blind pairwise benchmark and compute conservative quality claims."""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
import math
from pathlib import Path
from typing import Any

from evidence import EvidenceError, load_object, sha256_file


DIMENSIONS = (
    "composition", "authored_specificity", "narrative", "color_light",
    "material_coherence", "ai_residue", "series_rhythm", "carrier_fit"
)


def parse_time(value: Any, label: str, blockers: list[str]) -> datetime | None:
    if not isinstance(value, str):
        blockers.append(f"{label} must be an ISO 8601 timestamp")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        blockers.append(f"{label} is not a valid ISO 8601 timestamp")
        return None
    if parsed.tzinfo is None:
        blockers.append(f"{label} must include a timezone")
        return None
    return parsed.astimezone(timezone.utc)


def wilson_interval(successes: float, total: int, z: float) -> tuple[float, float]:
    """Wilson interval over independent pair-level preference values."""
    if total <= 0:
        return 0.0, 1.0
    proportion = successes / total
    denominator = 1 + z * z / total
    center = (proportion + z * z / (2 * total)) / denominator
    radius = (
        z
        * math.sqrt(proportion * (1 - proportion) / total + z * z / (4 * total * total))
        / denominator
    )
    return max(0.0, center - radius), min(1.0, center + radius)


def system_for_side(item: dict[str, Any], side: str) -> str:
    if side == "tie":
        return "tie"
    return str((item.get("assignment") or {}).get(f"{side}_system", "invalid"))


def system_score(item: dict[str, Any], side_value: str) -> float | None:
    if side_value == "not-applicable":
        return None
    system = system_for_side(item, side_value)
    if system == "mosocanvas":
        return 1.0
    if system == "target":
        return 0.0
    if system == "tie":
        return 0.5
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("suite", type=Path)
    parser.add_argument("evaluation", type=Path)
    parser.add_argument("--at", help="ISO 8601 time for reproducible expiry checks")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    blockers: list[str] = []
    try:
        suite = load_object(args.suite, "benchmark suite")
    except EvidenceError as exc:
        suite = {}
        blockers.append(str(exc))
    try:
        evaluation = load_object(args.evaluation, "pairwise evaluation")
    except EvidenceError as exc:
        evaluation = {}
        blockers.append(str(exc))

    if suite.get("schema") != "moso.benchmark-suite/0.1":
        blockers.append("suite must use moso.benchmark-suite/0.1")
    if evaluation.get("schema") != "moso.pairwise-evaluation/0.2":
        blockers.append("evaluation must use moso.pairwise-evaluation/0.2")
    if evaluation.get("suite_id") != suite.get("id"):
        blockers.append("evaluation suite_id does not match the supplied suite")
    if args.suite.is_file():
        if str(evaluation.get("suite_sha256", "")).lower() != sha256_file(args.suite):
            blockers.append("evaluation suite_sha256 does not match the supplied suite")
    if suite.get("lane") != "matched-challenge":
        blockers.append("quality claims require the matched-challenge lane")

    now = parse_time(args.at, "--at", blockers) if args.at else datetime.now(timezone.utc)
    expires = suite.get("expires_at")
    if expires:
        expires_at = parse_time(expires, "suite.expires_at", blockers)
        if expires_at and now and now > expires_at:
            blockers.append("benchmark suite is stale")

    leakage = suite.get("leakage_control") or {}
    if leakage.get("target_hidden_during_direction") is not True:
        blockers.append("target artifacts must be hidden during direction")
    if leakage.get("target_hidden_during_generation") is not True:
        blockers.append("target artifacts must be hidden during generation")
    protocol = evaluation.get("protocol") or {}
    for key in (
        "source_hidden_during_rating", "prompt_hidden",
        "randomized_sides", "ratings_committed_before_reveal"
    ):
        if protocol.get(key) is not True:
            blockers.append(f"benchmark protocol requires {key}=true")

    suite_tasks: dict[str, dict[str, Any]] = {}
    artifact_system: dict[str, tuple[str, str]] = {}
    for task in suite.get("tasks") or []:
        task_id = str(task.get("task_id", ""))
        if not task_id or task_id in suite_tasks:
            blockers.append(f"duplicate or empty suite task_id: {task_id!r}")
            continue
        suite_tasks[task_id] = task
        for field, system in (
            ("mosocanvas_artifacts", "mosocanvas"),
            ("target_artifacts", "target"),
        ):
            for artifact in task.get(field) or []:
                artifact_id = str(artifact.get("artifact_id", ""))
                if not artifact_id or artifact_id in artifact_system:
                    blockers.append(f"duplicate or empty artifact_id: {artifact_id!r}")
                else:
                    artifact_system[artifact_id] = (task_id, system)

    thresholds = evaluation.get("thresholds") or {}
    floors = {
        "minimum_tasks": 5,
        "minimum_comparisons": 30,
        "minimum_unique_pairs": 10,
        "minimum_raters": 5,
    }
    for key, floor in floors.items():
        if thresholds.get(key, 0) < floor:
            blockers.append(f"{key} cannot be below {floor}")
    if thresholds.get("noninferiority_margin", 1) > 0.05:
        blockers.append("noninferiority_margin cannot exceed 0.05")
    if thresholds.get("exceeds_observed_preference", 0) < 0.60:
        blockers.append("exceeds_observed_preference cannot be below 0.60")

    comparisons = evaluation.get("comparisons")
    if not isinstance(comparisons, list):
        blockers.append("comparisons must be a list")
        comparisons = []
    comparison_ids: set[str] = set()
    pair_raters: set[tuple[str, str]] = set()
    pair_identity: dict[str, tuple[str, frozenset[str]]] = {}
    task_scores: dict[str, list[float]] = defaultdict(list)
    pair_scores: dict[str, list[float]] = defaultdict(list)
    dimension_scores: dict[str, list[float]] = defaultdict(list)
    rater_ids: set[str] = set()
    moso_left = 0
    target_left = 0
    artifact_defects: dict[str, int] = defaultdict(int)

    for index, item in enumerate(comparisons, start=1):
        prefix = f"comparison {index}"
        if not isinstance(item, dict):
            blockers.append(f"{prefix} must be an object")
            continue
        comparison_id = str(item.get("comparison_id", ""))
        pair_id = str(item.get("pair_id", ""))
        task_id = str(item.get("task_id", ""))
        rater_id = str(item.get("rater_id", ""))
        if not comparison_id or comparison_id in comparison_ids:
            blockers.append(f"{prefix} has duplicate or empty comparison_id")
        comparison_ids.add(comparison_id)
        if not pair_id:
            blockers.append(f"{prefix} requires pair_id")
        if (pair_id, rater_id) in pair_raters:
            blockers.append(f"rater {rater_id!r} rated pair {pair_id!r} more than once")
        pair_raters.add((pair_id, rater_id))
        if item.get("rater_independent") is not True:
            blockers.append(f"{prefix} rater is not independent")
        if rater_id:
            rater_ids.add(rater_id)
        if task_id not in suite_tasks:
            blockers.append(f"{prefix} references unknown task_id: {task_id!r}")

        left_id = str(item.get("left_artifact_id", ""))
        right_id = str(item.get("right_artifact_id", ""))
        assignment = item.get("assignment") or {}
        left_system = assignment.get("left_system")
        right_system = assignment.get("right_system")
        if {left_system, right_system} != {"mosocanvas", "target"}:
            blockers.append(f"{prefix} must assign one artifact from each system")
        for artifact_id, declared_system in (
            (left_id, left_system), (right_id, right_system)
        ):
            actual = artifact_system.get(artifact_id)
            if not actual:
                blockers.append(f"{prefix} references unknown artifact_id: {artifact_id!r}")
            elif actual != (task_id, declared_system):
                blockers.append(
                    f"{prefix} artifact {artifact_id!r} does not match task/system assignment"
                )
        identity = (task_id, frozenset((left_id, right_id)))
        if pair_id in pair_identity and pair_identity[pair_id] != identity:
            blockers.append(f"pair_id {pair_id!r} changes task or artifacts across ratings")
        pair_identity[pair_id] = identity

        committed = parse_time(
            (item.get("rating") or {}).get("committed_at"),
            f"{prefix}.rating.committed_at",
            blockers,
        )
        revealed = parse_time(
            assignment.get("revealed_at"),
            f"{prefix}.assignment.revealed_at",
            blockers,
        )
        if committed and revealed and committed > revealed:
            blockers.append(f"{prefix} source assignment was revealed before rating commitment")

        if left_system == "mosocanvas":
            moso_left += 1
        elif left_system == "target":
            target_left += 1
        score = system_score(item, (item.get("rating") or {}).get("winner_side", ""))
        if score is None:
            blockers.append(f"{prefix} has an invalid winner_side")
        else:
            pair_scores[pair_id].append(score)
            task_scores[task_id].append(score)
        for dimension, side in (item.get("dimensions") or {}).items():
            if dimension not in DIMENSIONS:
                continue
            value = system_score(item, side)
            if value is not None:
                dimension_scores[dimension].append(value)
        defects = item.get("severity3_defects") or {}
        for side, artifact_id in (("left", left_id), ("right", right_id)):
            value = defects.get(side)
            if not isinstance(value, int) or value < 0:
                blockers.append(f"{prefix} has invalid severity3 defect count for {side}")
            else:
                artifact_defects[artifact_id] = max(artifact_defects[artifact_id], value)

    task_classes = {
        suite_tasks[task_id].get("task_class")
        for task_id in task_scores
        if task_id in suite_tasks
    }
    if len(comparisons) < thresholds.get("minimum_comparisons", 30):
        blockers.append("insufficient committed pair judgments")
    if len(task_scores) < thresholds.get("minimum_tasks", 5):
        blockers.append("insufficient task coverage")
    if len(task_classes) < thresholds.get("minimum_tasks", 5):
        blockers.append("insufficient task-class coverage")
    if len(pair_scores) < thresholds.get("minimum_unique_pairs", 10):
        blockers.append("insufficient unique artifact pairs")
    if len(rater_ids) < thresholds.get("minimum_raters", 5):
        blockers.append("insufficient independent raters")
    balance_tolerance = max(2, math.ceil(len(comparisons) * 0.15))
    if abs(moso_left - target_left) > balance_tolerance:
        blockers.append("left/right system assignment is materially imbalanced")

    pair_means = [sum(values) / len(values) for values in pair_scores.values() if values]
    pair_successes = sum(pair_means)
    pair_total = len(pair_means)
    z = float(thresholds.get("confidence_z", 1.96))
    lower, upper = wilson_interval(pair_successes, pair_total, z)
    observed = pair_successes / pair_total if pair_total else 0.0
    task_results = {
        task_id: {
            "judgments": len(values),
            "preference": round(sum(values) / len(values), 4)
        }
        for task_id, values in sorted(task_scores.items())
        if values
    }
    minimum_task_preference = float(thresholds.get("minimum_task_preference", 0.4))
    weak_tasks = [
        task_id for task_id, result in task_results.items()
        if result["preference"] < minimum_task_preference
    ]

    moso_defects = sum(
        count for artifact_id, count in artifact_defects.items()
        if artifact_system.get(artifact_id, ("", ""))[1] == "mosocanvas"
    )
    target_defects = sum(
        count for artifact_id, count in artifact_defects.items()
        if artifact_system.get(artifact_id, ("", ""))[1] == "target"
    )
    defect_parity = moso_defects <= target_defects
    noninferiority_floor = 0.5 - float(thresholds.get("noninferiority_margin", 0.05))
    exceeds_floor = float(thresholds.get("exceeds_observed_preference", 0.60))

    claim = "not-demonstrated"
    if not blockers and not weak_tasks and defect_parity and lower >= noninferiority_floor:
        claim = "meets-target"
    if (
        not blockers and not weak_tasks and defect_parity
        and lower > 0.5 and observed >= exceeds_floor
    ):
        claim = "exceeds-target"

    report = {
        "schema": "moso.benchmark-report/0.2",
        "suite": str(args.suite.resolve()),
        "evaluation": str(args.evaluation.resolve()),
        "integrity_status": "block" if blockers else "pass",
        "claim": claim,
        "comparisons": len(comparisons),
        "unique_pairs": pair_total,
        "tasks": len(task_results),
        "task_classes": len(task_classes),
        "raters": len(rater_ids),
        "observed_pair_preference": round(observed, 4),
        "pair_cluster_wilson_interval": [round(lower, 4), round(upper, 4)],
        "task_results": task_results,
        "weak_tasks": weak_tasks,
        "dimension_preferences": {
            name: round(sum(values) / len(values), 4)
            for name, values in sorted(dimension_scores.items())
            if values
        },
        "severity3_defects": {"mosocanvas": moso_defects, "target": target_defects},
        "defect_parity": defect_parity,
        "left_assignment": {"mosocanvas": moso_left, "target": target_left},
        "blockers": blockers
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 1 if blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
