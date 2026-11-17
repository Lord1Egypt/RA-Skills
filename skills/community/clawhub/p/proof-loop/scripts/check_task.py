#!/usr/bin/env python3
"""Validate local artifact consistency; this does not authenticate a verifier or attest execution."""

from __future__ import annotations

import argparse
import json
import re
from artifact_validation import validate
from pathlib import Path
from typing import Any

PASS = "PASS"
VALID_STATUSES = {"PASS", "FAIL", "UNKNOWN"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check .agent/tasks/<TASK_ID>/ proof artifacts")
    parser.add_argument("task_dir", help="Path to .agent/tasks/<TASK_ID>")
    return parser.parse_args()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"FAIL invalid JSON in {path}: {exc}") from exc


def problems_are_clear(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8").strip()
    return text == ""


def main() -> int:
    args = parse_args()
    task_dir = Path(args.task_dir)
    failures: list[str] = []

    if not task_dir.is_dir():
        print(f"FAIL task directory not found: {task_dir}")
        return 1

    spec_path = task_dir / "spec.md"
    verdict_path = task_dir / "verdict.json"
    problems_path = task_dir / "problems.md"

    if not spec_path.exists():
        failures.append("missing spec.md")
    if not verdict_path.exists():
        failures.append("missing verdict.json")

    verdict: dict[str, Any] = {}
    if verdict_path.exists():
        loaded = load_json(verdict_path)
        if not isinstance(loaded, dict):
            failures.append("verdict.json must be an object")
        else:
            verdict = loaded

    schema = load_json(Path(__file__).resolve().parents[1] / "schemas" / "verdict.schema.json")
    failures.extend(validate(verdict, schema, "verdict.json"))
    spec_ids = []
    if spec_path.exists():
        spec = spec_path.read_text(encoding="utf-8")
        # Accept the documented AC1: and **AC1:** declaration forms only.
        spec_ids = re.findall(r"^\s*(?:[-*]\s+)?(?:\*\*)?(AC[1-9][0-9]*)(?:\*\*)?:(?:\*\*)?\s+\S.*$", spec, re.MULTILINE)
        if not spec_ids or len(spec_ids) != len(set(spec_ids)):
            failures.append("spec.md needs non-empty, unique AC declarations")
    if verdict:
        if verdict.get("task_id") != task_dir.name:
            failures.append("task_id does not match task directory")
        if verdict.get("phase") != "verify":
            failures.append("phase must be verify")
        if verdict.get("agent") == "unassigned":
            failures.append("verifier agent is unassigned")
        criteria = verdict.get("criteria")
        if isinstance(criteria, list):
            ids = [c.get("id") for c in criteria if isinstance(c, dict)]
            if any(not isinstance(i, str) for i in ids) or sorted(str(i) for i in ids) != sorted(spec_ids):
                failures.append("verdict criteria must match every spec AC exactly once")
        if verdict.get("overall") != PASS:
            failures.append(f"overall is {verdict.get('overall')!r}, expected PASS")

        criteria = verdict.get("criteria")
        if not isinstance(criteria, list) or not criteria:
            failures.append("criteria must be a non-empty list")
        else:
            for index, criterion in enumerate(criteria, start=1):
                if not isinstance(criterion, dict):
                    failures.append(f"criterion #{index} must be an object")
                    continue
                cid = criterion.get("id", f"#{index}")
                status = criterion.get("status")
                if not isinstance(status, str) or status not in VALID_STATUSES:
                    failures.append(f"{cid} has invalid status {status!r}")
                elif status != PASS:
                    failures.append(f"{cid} is {status}, expected PASS")

    evidence_path = task_dir / "evidence.md"
    if not evidence_path.is_file() or not evidence_path.read_text(encoding="utf-8").strip():
        failures.append("missing or empty evidence.md")
    evidence_json = task_dir / "evidence.json"
    if evidence_json.exists():
        evidence = load_json(evidence_json)
        evidence_schema = load_json(Path(__file__).resolve().parents[1] / "schemas" / "evidence.schema.json")
        failures.extend(validate(evidence, evidence_schema, "evidence.json"))
        if isinstance(evidence, dict) and evidence.get("task_id") != task_dir.name:
            failures.append("evidence task_id does not match task directory")
    if not problems_path.is_file():
        failures.append("missing problems.md")
    if not problems_are_clear(problems_path):
        failures.append("problems.md is not empty")

    if failures:
        print("PROOF_LOOP_FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"PROOF_LOOP_PASS {task_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
