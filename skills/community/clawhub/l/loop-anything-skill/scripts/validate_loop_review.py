#!/usr/bin/env python3
"""Validate a Loop Anything final review run.

Usage:
  python scripts/validate_loop_review.py --manifest loop-run-manifest.json reviewer-a.txt reviewer-b.txt [...]

This script is intentionally lightweight. It checks the minimum mechanical
conditions for final approval:
  - a manifest is provided
  - at least two reviewer files
  - at least two distinct facets
  - the run is not degraded
  - isolation is confirmed
  - final evidence is present
  - each file contains Verdict: PASS
  - each file contains Score: 120
  - each final review includes evidence checked
  - each file has no must-fix issues
  - each file contains a 120-level approval statement
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def has_no_must_fix(text: str) -> bool:
    lower = text.lower()
    if "must-fix issues" not in lower:
        return False
    return bool(re.search(r"must-fix issues\s*:\s*(?:\n\s*)?-\s*(none|无)", text, re.I))


def has_evidence_checked(text: str) -> bool:
    match = re.search(
        r"evidence checked\s*:\s*(.+?)(?:\n\s*(?:must-fix issues|optional improvements|120-level approval statement)\s*:|\Z)",
        text,
        re.I | re.S,
    )
    if not match:
        return False
    value = match.group(1).strip().lower()
    return bool(value) and value not in {"none", "- none", "n/a", "na", "无"}


def validate_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    errors: list[str] = []

    if not re.search(r"verdict\s*:\s*pass\b", text, re.I):
        errors.append("missing `Verdict: PASS`")
    if not re.search(r"score\s*:\s*120\b", text, re.I):
        errors.append("missing `Score: 120`")
    if not has_no_must_fix(text):
        errors.append("must-fix issues are not explicitly none")
    if not has_evidence_checked(text):
        errors.append("missing non-empty `Evidence checked:`")
    if not re.search(r"120-level approval statement\s*:\s*(?!\s*N/A\b).+", text, re.I | re.S):
        errors.append("missing non-N/A 120-level approval statement")

    return errors


def validate_manifest(path: Path, review_paths: list[Path]) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"manifest is not valid JSON: {exc}"]

    runtime = data.get("runtime") or {}
    if not runtime.get("subagent_mechanism"):
        errors.append("manifest runtime.subagent_mechanism is required")
    if runtime.get("degraded") is not False:
        errors.append("manifest runtime.degraded must be false for full approval")
    if runtime.get("isolation_confirmed") is not True:
        errors.append("manifest runtime.isolation_confirmed must be true")

    facets = data.get("facets") or []
    if len(facets) < 2:
        errors.append("manifest must contain at least two facets")
    names = [str(facet.get("name", "")).strip().lower() for facet in facets]
    missions = [str(facet.get("mission", "")).strip().lower() for facet in facets]
    rationales = [str(facet.get("distinctness_rationale", "")).strip() for facet in facets]
    if len(set(names)) != len(names):
        errors.append("facet names must be distinct")
    if len(set(missions)) != len(missions):
        errors.append("facet missions must be distinct")
    if any(not rationale for rationale in rationales):
        errors.append("each facet needs distinctness_rationale")

    evidence_items = data.get("evidence_items") or []
    if not evidence_items:
        errors.append("manifest evidence_items must be non-empty")

    final_verdicts = data.get("final_verdicts") or []
    if len(final_verdicts) < len(facets):
        errors.append("manifest final_verdicts must cover every facet")
    for verdict in final_verdicts:
        if str(verdict.get("verdict", "")).upper() != "PASS" or verdict.get("score") != 120:
            errors.append("all manifest final_verdicts must be PASS with score 120")
            break

    manifest_outputs = {
        Path(str(facet.get("reviewer_output", ""))).name
        for facet in facets
        if facet.get("reviewer_output")
    }
    provided_outputs = {path.name for path in review_paths}
    if manifest_outputs and not manifest_outputs.issubset(provided_outputs):
        errors.append("manifest reviewer_output files must match provided reviewer files")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) < 4 or argv[0] != "--manifest":
        return fail("usage: validate_loop_review.py --manifest loop-run-manifest.json review_a.txt review_b.txt [...]")

    manifest_path = Path(argv[1])
    paths = [Path(arg) for arg in argv[2:]]
    if len(paths) < 2:
        return fail("provide at least two reviewer output files")

    if not manifest_path.exists():
        return fail(f"missing manifest: {manifest_path}")
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        return fail(f"missing files: {', '.join(missing)}")

    failed = False
    manifest_errors = validate_manifest(manifest_path, paths)
    if manifest_errors:
        failed = True
        print(f"FAIL: {manifest_path}")
        for error in manifest_errors:
            print(f"  - {error}")

    for path in paths:
        errors = validate_file(path)
        if errors:
            failed = True
            print(f"FAIL: {path}")
            for error in errors:
                print(f"  - {error}")

    if failed:
        return 1

    print(f"PASS: manifest and {len(paths)} reviewer outputs reached full Loop Anything approval")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
