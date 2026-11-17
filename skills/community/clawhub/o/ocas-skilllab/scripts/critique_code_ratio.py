#!/usr/bin/env python3
"""
critique_code_ratio.py — Measure code ratio of a SKILL.md file.

Usage:
    python3 critique_code_ratio.py <path-to-SKILL.md>

Output:
    JSON with total_lines, code_lines, ratio, pass/fail

Exit codes:
    0 = ratio under 20% (pass)
    1 = ratio 20-30% (warning)
    2 = ratio over 30% (fail)
"""

import sys
import json


def measure_code_ratio(path: str) -> dict:
    with open(path) as f:
        lines = f.read().split("\n")

    in_block = False
    code_lines = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_block = not in_block
            continue
        if in_block:
            code_lines += 1

    total = len(lines)
    ratio = (code_lines / total * 100) if total else 0.0

    if ratio < 20:
        status = "pass"
        exit_code = 0
    elif ratio < 30:
        status = "warning"
        exit_code = 1
    else:
        status = "fail"
        exit_code = 2

    return {
        "total_lines": total,
        "code_lines": code_lines,
        "ratio": round(ratio, 1),
        "status": status,
        "exit_code": exit_code,
    }


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h"):
        print(__doc__)
        sys.exit(0)
    if len(sys.argv) < 2:
        print("Usage: python3 critique_code_ratio.py <path-to-SKILL.md>", file=sys.stderr)
        sys.exit(1)

    result = measure_code_ratio(sys.argv[1])
    print(json.dumps(result, indent=2))
    sys.exit(result["exit_code"])