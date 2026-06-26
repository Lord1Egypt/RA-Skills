#!/usr/bin/env python3
"""Validate whether a Proof Loop task is allowed to be called done."""

from __future__ import annotations

import argparse
import json
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
        return True
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

    if verdict:
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
                if status not in VALID_STATUSES:
                    failures.append(f"{cid} has invalid status {status!r}")
                elif status != PASS:
                    failures.append(f"{cid} is {status}, expected PASS")

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
