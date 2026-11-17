#!/usr/bin/env python3
"""Run lightweight behavior-property evaluations for omni-ecom responses."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evals" / "cases.json"
FIXTURES = ROOT / "evals" / "fixture-responses.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def evaluate_case(case: dict[str, Any], response: str) -> list[str]:
    errors: list[str] = []
    text = response.casefold()
    for term in case.get("required_terms", []):
        if str(term).casefold() not in text:
            errors.append(f"缺少必需行为/词: {term}")
    for term in case.get("forbidden_terms", []):
        if str(term).casefold() in text:
            errors.append(f"命中禁止行为/词: {term}")
    if case.get("requires_evidence_id") and not re.search(r"\bE[0-9A-Za-z._-]+\b", response):
        errors.append("缺少证据 ID")
    return errors


def run(responses: dict[str, str]) -> dict[str, Any]:
    cases = load_json(CASES)
    results = []
    for case in cases:
        case_id = case["id"]
        errors = evaluate_case(case, str(responses.get(case_id, "")))
        results.append({"id": case_id, "category": case.get("category"), "status": "PASS" if not errors else "FAIL", "errors": errors})
    failed = [item for item in results if item["status"] == "FAIL"]
    return {"status": "PASS" if not failed else "FAIL", "total": len(results), "passed": len(results) - len(failed), "failed": len(failed), "results": results}


def main() -> int:
    parser = argparse.ArgumentParser(description="运行 omni-ecom 行为属性评测")
    parser.add_argument("--responses", help="JSON 对象：case_id -> response；省略时使用内置脱敏夹具")
    parser.add_argument("--output", help="输出评测 JSON")
    args = parser.parse_args()
    try:
        responses = load_json(Path(args.responses).resolve()) if args.responses else load_json(FIXTURES)
        if not isinstance(responses, dict):
            raise ValueError("responses 必须是对象")
        result = run({str(key): str(value) for key, value in responses.items()})
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "errors": [str(exc)]}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = Path(args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload, encoding="utf-8")
        print(output)
    else:
        print(payload, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
