#!/usr/bin/env python3
"""
verify.py — Static SymPy verification for math worksheets.

Reads a structured JSON file of problems and answers. No user-generated
code is ever executed — only the structured data is evaluated.

Input format: /tmp/verify_TOPIC_DATE.json
  {
    "topic": "graphing polynomials",
    "problems": [
      {"id": 1, "type": "solve",  "expr": "x**2 - 5*x + 6",     "expected": [2, 3]},
      {"id": 2, "type": "factor", "expr": "x**2 - 7*x + 12",    "expected": "(x - 3)*(x - 4)"},
      {"id": 3, "type": "eval",   "expr": "(x-1)*(x+2)", "at": {"x": 0}, "expected": -2},
      {"id": 4, "type": "zeros",  "expr": "x*(x-3)**2",          "expected": [0, 3]},
      {"id": 5, "type": "expand", "expr": "(x+2)**3",            "expected": "x**3 + 6*x**2 + 12*x + 8"},
      {"id": 6, "type": "manual", "desc": "Graph sketch — verify visually"}
    ]
  }

Supported types:
  solve   — solves expr=0 for x, checks roots match expected list
  factor  — factors expr, checks string form matches expected
  eval    — evaluates expr at given variable values, checks result
  zeros   — finds zeros of expr, checks they match expected list
  expand  — expands expr, checks string form matches expected
  manual  — flagged for human review, never fails automatically

Exit codes:
  0 — all automated checks passed
  1 — one or more checks FAILED (fix answer key before compiling)
  2 — no failures, but some problems need manual review
"""

import json
import sys
import os
from sympy import (
    symbols, solve, factor, expand, sympify,
    Rational, simplify, nsimplify
)

def run_verification(json_path):
    with open(json_path) as f:
        data = json.load(f)

    problems = data.get("problems", [])
    topic = data.get("topic", "unknown")

    print(f"Verifying: {topic} ({len(problems)} problems)\n")

    results = []
    for p in problems:
        pid = p.get("id", "?")
        ptype = p.get("type", "manual")

        try:
            if ptype == "manual":
                results.append((pid, "MANUAL", p.get("desc", "manual review")))

            elif ptype == "solve":
                x = symbols('x')
                expr = sympify(p["expr"])
                roots = sorted([nsimplify(r) for r in solve(expr, x)])
                expected = sorted([nsimplify(e) for e in p["expected"]])
                ok = roots == expected
                results.append((pid, "PASS" if ok else "FAIL",
                    f"solve({p['expr']}) → {roots} (expected {expected})"))

            elif ptype == "zeros":
                x = symbols('x')
                expr = sympify(p["expr"])
                roots = sorted(set([nsimplify(r) for r in solve(expr, x)]))
                expected = sorted(set([nsimplify(e) for e in p["expected"]]))
                ok = roots == expected
                results.append((pid, "PASS" if ok else "FAIL",
                    f"zeros({p['expr']}) → {roots} (expected {expected})"))

            elif ptype == "factor":
                x = symbols('x')
                expr = sympify(p["expr"])
                factored = str(factor(expr))
                expected = str(sympify(p["expected"]))
                ok = simplify(sympify(factored) - sympify(expected)) == 0
                results.append((pid, "PASS" if ok else "FAIL",
                    f"factor({p['expr']}) → {factored} (expected {p['expected']})"))

            elif ptype == "expand":
                x = symbols('x')
                expr = sympify(p["expr"])
                expanded = str(expand(expr))
                expected = str(sympify(p["expected"]))
                ok = simplify(sympify(expanded) - sympify(expected)) == 0
                results.append((pid, "PASS" if ok else "FAIL",
                    f"expand({p['expr']}) → {expanded} (expected {p['expected']})"))

            elif ptype == "eval":
                subs = {symbols(k): nsimplify(v) for k, v in p["at"].items()}
                expr = sympify(p["expr"])
                result = expr.subs(subs)
                expected = nsimplify(p["expected"])
                ok = simplify(result - expected) == 0
                results.append((pid, "PASS" if ok else "FAIL",
                    f"eval({p['expr']} at {p['at']}) → {result} (expected {expected})"))

            else:
                results.append((pid, "MANUAL", f"unknown type '{ptype}' — manual review"))

        except Exception as e:
            results.append((pid, "FAIL", f"Error evaluating problem {pid}: {e}"))

    # Print results
    for pid, status, desc in results:
        icon = {"PASS": "✅", "FAIL": "❌", "MANUAL": "👁 "}.get(status, "?")
        print(f"  {icon} [{status}] Problem {pid}: {desc}")

    failures = [r for r in results if r[1] == "FAIL"]
    manuals  = [r for r in results if r[1] == "MANUAL"]
    passes   = [r for r in results if r[1] == "PASS"]

    print(f"\n{len(passes)} passed · {len(failures)} failed · {len(manuals)} manual")

    if failures:
        print("\n❌ Fix the answer key before compiling.")
        return 1
    if manuals:
        print("\n👁  Manual review needed for some problems — safe to compile.")
        return 2
    print("\n✅ All checks passed — safe to compile.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <verify_TOPIC_DATE.json>", file=sys.stderr)
        sys.exit(1)

    json_path = sys.argv[1]
    if not os.path.exists(json_path):
        print(f"Error: file not found: {json_path}", file=sys.stderr)
        sys.exit(1)

    sys.exit(run_verification(json_path))
