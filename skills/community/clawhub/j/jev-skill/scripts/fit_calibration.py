#!/usr/bin/env python3
"""Fit a deployment-specific temperature profile from a Jev report.

Use a held-out calibration-tagged split from the same provider/model. The
result is a small JSON profile that ``jev_harness.py`` can apply on a later
run; it never contains raw state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from jev_calibration import CalibrationError, PROFILE_SCHEMA, fit_temperature


def canonical_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def read_report(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CalibrationError(f"report not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CalibrationError(f"invalid report JSON: {exc}") from exc
    if not isinstance(value, dict) or not isinstance(value.get("records"), list):
        raise CalibrationError("report must contain a records array")
    return value


def collect_samples(report: dict[str, Any], fit_tag: str | None) -> tuple[dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]], int]:
    by_type: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_question: dict[str, list[dict[str, Any]]] = defaultdict(list)
    selected_cases = 0
    for record in report["records"]:
        if not isinstance(record, dict) or record.get("ok") is not True:
            continue
        tags = record.get("tags", [])
        if fit_tag and fit_tag not in tags:
            continue
        answers = record.get("answers", {})
        if not isinstance(answers, dict):
            continue
        selected_cases += 1
        for evaluation in record.get("evaluations", []):
            if not isinstance(evaluation, dict):
                continue
            question_id = evaluation.get("id")
            question_type = evaluation.get("type")
            answer = answers.get(question_id)
            if not isinstance(question_id, str) or not isinstance(answer, dict):
                continue
            if question_type == "noul":
                sample = {
                    "kind": "binary",
                    "probability": answer.get("noul"),
                    "label": bool(evaluation.get("expected")),
                }
            elif question_type == "choice":
                sample = {
                    "kind": "categorical",
                    "probabilities": answer.get("probabilities"),
                    "label": evaluation.get("expected"),
                }
            elif question_type == "score":
                expected_level = evaluation.get("expected_level")
                if isinstance(expected_level, (int, float)) and not isinstance(expected_level, bool) and float(expected_level).is_integer():
                    expected_label = str(int(expected_level))
                else:
                    expected_label = str(expected_level)
                sample = {
                    "kind": "categorical",
                    "probabilities": answer.get("probabilities"),
                    "label": expected_label,
                }
            else:
                continue
            by_type[question_type].append(sample)
            by_question[f"{question_id}\u0000{question_type}"].append(sample)
    return dict(by_type), dict(by_question), selected_cases


def fit_group(samples: list[dict[str, Any]], minimum_samples: int) -> tuple[float | None, str | None]:
    if len(samples) < minimum_samples:
        return None, f"only {len(samples)} samples; minimum is {minimum_samples}"
    try:
        return fit_temperature(samples), None
    except (CalibrationError, KeyError, TypeError, ValueError, OverflowError) as exc:
        return None, str(exc)


def build_profile(
    report: dict[str, Any],
    report_path: Path,
    *,
    fit_tag: str | None,
    minimum_samples: int,
    by_question: bool,
) -> dict[str, Any]:
    if minimum_samples < 1:
        raise CalibrationError("minimum samples must be positive")
    by_type_samples, by_question_samples, selected_cases = collect_samples(report, fit_tag)
    if not by_type_samples:
        qualifier = f" tagged {fit_tag!r}" if fit_tag else ""
        raise CalibrationError(f"report has no successful labeled evaluations{qualifier}")

    temperatures: dict[str, float] = {}
    counts: dict[str, int] = {}
    warnings: list[str] = []
    for question_type in ("noul", "choice", "score"):
        samples = by_type_samples.get(question_type, [])
        if not samples:
            continue
        temperature, warning = fit_group(samples, minimum_samples)
        counts[question_type] = len(samples)
        if temperature is None:
            temperatures[question_type] = 1.0
            warnings.append(f"{question_type}: {warning}; using neutral temperature 1.0")
        else:
            temperatures[question_type] = temperature

    profile: dict[str, Any] = {
        "schema_version": PROFILE_SCHEMA,
        "profile_id": canonical_hash({
            "report_sha256": hashlib.sha256(report_path.read_bytes()).hexdigest(),
            "fit_tag": fit_tag,
            "minimum_samples": minimum_samples,
            "by_question": by_question,
        })[:16],
        "method": {
            "name": "temperature_scaling",
            "objective": "mean_negative_log_likelihood",
            "fit_tag": fit_tag,
            "minimum_samples": minimum_samples,
            "selected_cases": selected_cases,
        },
        "source": {
            "report_sha256": hashlib.sha256(report_path.read_bytes()).hexdigest(),
            "provider": report.get("config", {}).get("provider"),
            "model": report.get("config", {}).get("model"),
            "question_sha256": report.get("config", {}).get("question_sha256"),
            "case_sha256": report.get("config", {}).get("case_sha256"),
        },
        "temperatures": temperatures,
        "counts": counts,
        "warnings": warnings,
    }
    if by_question:
        fitted_questions: dict[str, dict[str, float]] = {}
        question_counts: dict[str, int] = {}
        for key, samples in sorted(by_question_samples.items()):
            question_id, question_type = key.split("\u0000", 1)
            temperature, warning = fit_group(samples, minimum_samples)
            question_counts[f"{question_id}:{question_type}"] = len(samples)
            if temperature is None:
                if warning:
                    warnings.append(f"{question_id}/{question_type}: {warning}; falling back to global temperature")
                continue
            fitted_questions.setdefault(question_id, {})[question_type] = temperature
        profile["by_question"] = fitted_questions
        profile["question_counts"] = question_counts
    return profile


def main() -> int:
    parser = argparse.ArgumentParser(description="Fit Jev temperature scaling from a labeled harness report")
    parser.add_argument("report", type=Path, help="Harness report JSON")
    parser.add_argument("--output", required=True, type=Path, help="Write the calibration profile JSON")
    parser.add_argument("--fit-tag", default="calibration", help="Only use cases with this tag; pass an empty string to use all cases")
    parser.add_argument("--min-samples", type=int, default=20, help="Minimum labeled answers per fitted group")
    parser.add_argument("--by-question", action="store_true", help="Also fit a question-specific temperature when sufficiently supported")
    args = parser.parse_args()
    fit_tag = args.fit_tag or None
    try:
        report = read_report(args.report)
        profile = build_profile(
            report,
            args.report,
            fit_tag=fit_tag,
            minimum_samples=args.min_samples,
            by_question=args.by_question,
        )
    except CalibrationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(profile, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "profile": str(args.output),
        "profile_id": profile["profile_id"],
        "temperatures": profile["temperatures"],
        "counts": profile["counts"],
        "warnings": profile["warnings"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
