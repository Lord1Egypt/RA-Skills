#!/usr/bin/env python3
"""Validate evidence and independence in a MoSoCanvas artifact review."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from review_integrity import validate_authorized_review


CATEGORIES = (
    "carrier", "composition", "narrative", "color_light",
    "material_physics", "ai_residue", "spec_fit"
)


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate review evidence; this script does not perform the visual review."
    )
    parser.add_argument("review", type=Path)
    parser.add_argument("--run-state", type=Path)
    parser.add_argument("--registry", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    blockers: list[str] = []
    warnings: list[str] = []
    try:
        review = load(args.review)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        review = {}
        blockers.append(f"review cannot be loaded: {exc}")

    if review.get("schema") != "moso.artifact-review/0.1":
        blockers.append("review must use moso.artifact-review/0.1")

    reviewer = review.get("reviewer") or {}
    blind = review.get("blind_pass") or {}
    spec = review.get("spec_pass") or {}
    decision = review.get("decision") or {}

    if reviewer.get("actual_artifact_inspected") is not True:
        blockers.append("reviewer must inspect the actual artifact")
    if reviewer.get("independent_from_generation") is not True:
        blockers.append("release review must be independent from the generating context")
    if blind.get("prompt_hidden") is not True:
        blockers.append("first-pass review must hide the prompt and intended interpretation")
    for key in ("first_read", "eye_path", "inferred_narrative", "observed_anomalies"):
        if key not in blind:
            blockers.append(f"blind_pass missing required field: {key}")
    for category in CATEGORIES:
        if category not in spec:
            blockers.append(f"spec_pass missing category: {category}")

    blocker_findings = 0
    unsupported_major = 0
    for category in CATEGORIES:
        findings = spec.get(category) or []
        if not isinstance(findings, list):
            blockers.append(f"spec_pass.{category} must be a list")
            continue
        for index, finding in enumerate(findings, start=1):
            if not isinstance(finding, dict):
                blockers.append(f"{category} finding {index} must be an object")
                continue
            severity = finding.get("severity")
            if severity == 3:
                blocker_findings += 1
            if severity in {2, 3} and not finding.get("alternative_explanation"):
                unsupported_major += 1
                blockers.append(
                    f"{category} finding {index} requires an alternative_explanation"
                )
            for field in ("claim", "evidence_region", "consequence", "confidence"):
                if not finding.get(field):
                    blockers.append(f"{category} finding {index} missing {field}")

    recommendation = decision.get("recommendation")
    authorized = decision.get("release_authorized")
    if blocker_findings and recommendation == "accept":
        blockers.append("review cannot recommend accept while severity-3 findings remain")
    if authorized is True and recommendation != "accept":
        blockers.append("release_authorized requires recommendation=accept")
    if reviewer.get("kind") == "same-context-assistive" and authorized is True:
        blockers.append("same-context assistive review cannot authorize release")
    blockers.extend(
        validate_authorized_review(review, args.review, args.registry)
    )

    if args.run_state:
        try:
            state = load(args.run_state)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            state = {}
            blockers.append(f"run state cannot be loaded: {exc}")
        if state.get("phase") == "accept":
            quality = state.get("quality_status") or {}
            if quality.get("user_acceptance") not in {
                "accepted", "accepted-with-tradeoff"
            }:
                blockers.append("accepted run state lacks actual user acceptance")
            if state.get("release_review_ref") not in {
                str(args.review), str(args.review.resolve())
            }:
                warnings.append("release_review_ref does not exactly match the supplied review path")

    report = {
        "schema": "moso.review-validation/0.1",
        "scope": "review-evidence-integrity-only",
        "review": str(args.review.resolve()),
        "status": "block" if blockers else "pass",
        "blocker_findings": blocker_findings,
        "unsupported_major_findings": unsupported_major,
        "blockers": blockers,
        "warnings": warnings,
        "not_evaluated": ["whether the reviewer's visual claims are factually correct"]
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
