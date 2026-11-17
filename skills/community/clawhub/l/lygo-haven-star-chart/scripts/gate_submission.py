#!/usr/bin/env python3
"""Validate submission via in-process gate import (allowlisted, no subprocess)."""

from __future__ import annotations

import json
import sys

from _stack_paths import resolve_stack_root, validate_local_json_path
from _stack_tools import load_tool


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: gate_submission.py <submission.json>")
        return 2
    stack = resolve_stack_root()
    sub_path = validate_local_json_path(sys.argv[1], stack=stack)
    gate = load_tool(stack, "haven_star_chart_gate.py")
    sub = json.loads(sub_path.read_text(encoding="utf-8"))
    result = gate.validate_submission(sub)
    print(json.dumps(result, indent=2))
    return 0 if result.get("all_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())