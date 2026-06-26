#!/usr/bin/env python3
"""Validate or score lightweight code-audit eval outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List


def load_evals(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema(data: Dict[str, object]) -> List[str]:
    errors: List[str] = []
    if data.get("skill_name") != "code-audit":
        errors.append("skill_name must be code-audit")
    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        errors.append("evals must be a non-empty list")
        return errors
    for index, item in enumerate(evals):
        if not item.get("prompt"):
            errors.append(f"eval {index} missing prompt")
        if not item.get("expected_output"):
            errors.append(f"eval {index} missing expected_output")
        assertions = item.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            errors.append(f"eval {index} missing assertions")
    return errors


def score_outputs(data: Dict[str, object], outputs_dir: Path) -> List[str]:
    failures: List[str] = []
    for item in data["evals"]:
        eval_id = str(item["id"])
        output_path = outputs_dir / f"{eval_id}.md"
        if not output_path.exists():
            failures.append(f"eval {eval_id}: missing output {output_path}")
            continue
        output = output_path.read_text(encoding="utf-8", errors="ignore").lower()
        for assertion in item.get("assertions", []):
            kind = assertion.get("type")
            text = str(assertion.get("text") or "").lower()
            if kind == "contains" and text not in output:
                failures.append(f"eval {eval_id}: expected output to contain {text!r}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evals", default=str(Path(__file__).resolve().parents[1] / "evals" / "evals.json"))
    parser.add_argument("--outputs-dir", default="", help="Optional directory containing <eval-id>.md outputs.")
    args = parser.parse_args()

    data = load_evals(Path(args.evals))
    failures = validate_schema(data)
    if args.outputs_dir:
        failures.extend(score_outputs(data, Path(args.outputs_dir)))

    if failures:
        print(json.dumps({"passed": False, "failures": failures}, indent=2))
        return 1
    print(json.dumps({"passed": True, "eval_count": len(data["evals"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
