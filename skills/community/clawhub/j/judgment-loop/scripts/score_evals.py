#!/usr/bin/env python3
"""Validate and score reviewed Judgment Loop observations."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ACTIVATIONS = {"none", "light", "full"}
MODES = {"quick", "decision", "research", "learning", "review"}
CLASSES = {"positive", "negative", "boundary", "evidence_update"}
SEVERITIES = {"low", "medium", "high"}
UPDATES = {"change", "hold", "strengthen_stop"}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path):
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{number}: invalid JSON: {exc}") from exc
    return rows


def index_unique(rows, key, label):
    values = [row.get(key) for row in rows]
    duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
    if duplicates:
        raise SystemExit(f"Duplicate {label}: {', '.join(map(str, duplicates))}")
    return {row[key]: row for row in rows}


def validate_cases(cases):
    if not isinstance(cases, list) or not cases:
        raise SystemExit("Case manifest must be a non-empty JSON array")
    index_unique(cases, "id", "case ids")

    for case in cases:
        case_id = case["id"]
        if case.get("class") not in CLASSES:
            raise SystemExit(f"{case_id}: invalid class")
        if case.get("severity") not in SEVERITIES:
            raise SystemExit(f"{case_id}: invalid severity")
        if not case.get("domain"):
            raise SystemExit(f"{case_id}: domain is required")
        if case.get("expected_activation") not in ACTIVATIONS:
            raise SystemExit(f"{case_id}: invalid expected_activation")
        if not isinstance(case.get("turns"), list) or not case["turns"]:
            raise SystemExit(f"{case_id}: turns must be a non-empty array")

        expected_mode = case.get("expected_mode")
        if case["expected_activation"] == "none":
            if expected_mode is not None:
                raise SystemExit(f"{case_id}: inactive cases require expected_mode null")
        elif expected_mode not in MODES:
            raise SystemExit(f"{case_id}: active cases require a valid expected_mode")

        if case["class"] == "negative" and case["expected_activation"] != "none":
            raise SystemExit(f"{case_id}: negative cases must stay inactive")
        if case["class"] in {"positive", "evidence_update"} and case["expected_activation"] == "none":
            raise SystemExit(f"{case_id}: positive and update cases must be active")

        if case["class"] == "evidence_update":
            if len(case["turns"]) != 2 or case.get("expected_update") not in UPDATES:
                raise SystemExit(
                    f"{case_id}: evidence_update cases require two turns and expected_update"
                )
        elif len(case["turns"]) != 1 or "expected_update" in case:
            raise SystemExit(
                f"{case_id}: non-update cases require one turn and no expected_update"
            )


def validate_observations(observations):
    index_unique(observations, "case_id", "observation case ids")
    for row in observations:
        case_id = row["case_id"]
        activation = row.get("observed_activation")
        mode = row.get("observed_mode")
        if activation not in ACTIVATIONS:
            raise SystemExit(f"{case_id}: invalid observed_activation")
        if activation == "none" and mode is not None:
            raise SystemExit(f"{case_id}: inactive observations require observed_mode null")
        if activation != "none" and mode not in MODES:
            raise SystemExit(f"{case_id}: active observations require a valid observed_mode")
        for field in ("reviewer", "evidence", "raw_output"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                raise SystemExit(f"{case_id}: {field} is required")


def score(cases, observations):
    validate_cases(cases)
    validate_observations(observations)
    case_by_id = index_unique(cases, "id", "case ids")
    observed_by_id = index_unique(observations, "case_id", "observation case ids")
    unknown = sorted(set(observed_by_id) - set(case_by_id))
    if unknown:
        raise SystemExit(f"Unknown case_id values: {', '.join(unknown)}")

    summary = {
        "cases_total": len(cases),
        "cases_observed": len(observed_by_id),
        "expected_class_coverage": dict(Counter(case["class"] for case in cases)),
        "expected_mode_coverage": dict(
            Counter(case["expected_mode"] for case in cases if case["expected_mode"])
        ),
        "missing_cases": [],
        "false_positive_activations": [],
        "false_negatives": [],
        "depth_mismatches": [],
        "mode_mismatches": [],
        "evidence_update_errors": [],
        "correct_evidence_updates": [],
        "errors_by_severity": {severity: [] for severity in ("high", "medium", "low")},
    }

    for case in cases:
        case_id = case["id"]
        row = observed_by_id.get(case_id)
        errors = []
        if row is None:
            summary["missing_cases"].append(case_id)
            errors.append("missing")
        else:
            expected_activation = case["expected_activation"]
            observed_activation = row["observed_activation"]
            if expected_activation == "none" and observed_activation != "none":
                summary["false_positive_activations"].append(case_id)
                errors.append("false_positive")
            elif expected_activation != "none" and observed_activation == "none":
                summary["false_negatives"].append(case_id)
                errors.append("false_negative")
            elif expected_activation != observed_activation:
                summary["depth_mismatches"].append(case_id)
                errors.append("depth_mismatch")

            if (
                expected_activation != "none"
                and observed_activation != "none"
                and row["observed_mode"] != case["expected_mode"]
            ):
                summary["mode_mismatches"].append(case_id)
                errors.append("mode_mismatch")

            if case["class"] == "evidence_update":
                observed_update = row.get("observed_update")
                if observed_update not in UPDATES:
                    raise SystemExit(f"{case_id}: observed_update is required")
                if observed_update == case["expected_update"]:
                    summary["correct_evidence_updates"].append(case_id)
                else:
                    summary["evidence_update_errors"].append(case_id)
                    errors.append("evidence_update_error")

        if errors:
            summary["errors_by_severity"][case["severity"]].append(
                {"case_id": case_id, "errors": errors}
            )

    return summary


def render_markdown(summary):
    def line(label, key):
        values = summary[key]
        detail = ", ".join(values) if values else "none"
        return f"- **{label}:** {len(values)} — {detail}"

    severity_lines = []
    for severity in ("high", "medium", "low"):
        values = summary["errors_by_severity"][severity]
        ids = ", ".join(item["case_id"] for item in values) if values else "none"
        severity_lines.append(f"- **{severity.title()}-severity cases with errors:** {len(values)} — {ids}")

    return "\n".join(
        [
            "# Judgment Loop reviewed scorecard",
            "",
            f"- **Observed:** {summary['cases_observed']} / {summary['cases_total']}",
            f"- **Expected mode coverage:** {json.dumps(summary['expected_mode_coverage'], sort_keys=True)}",
            line("False-positive activations", "false_positive_activations"),
            line("False negatives", "false_negatives"),
            line("Depth mismatches", "depth_mismatches"),
            line("Mode mismatches", "mode_mismatches"),
            line("Evidence-update errors", "evidence_update_errors"),
            line("Correct evidence updates", "correct_evidence_updates"),
            line("Missing cases", "missing_cases"),
            "",
            "## Severity",
            "",
            *severity_lines,
        ]
    )


def has_errors(summary):
    return any(
        summary[key]
        for key in (
            "missing_cases",
            "false_positive_activations",
            "false_negatives",
            "depth_mismatches",
            "mode_mismatches",
            "evidence_update_errors",
        )
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=Path("evals/cases.json"))
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()

    summary = score(load_json(args.cases), load_jsonl(args.results))
    if args.format == "json":
        print(json.dumps(summary, indent=2))
    else:
        print(render_markdown(summary))
    return 1 if args.fail_on_error and has_errors(summary) else 0


if __name__ == "__main__":
    raise SystemExit(main())
