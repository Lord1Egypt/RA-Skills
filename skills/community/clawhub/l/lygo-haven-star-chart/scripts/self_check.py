#!/usr/bin/env python3
"""Mirror install smoke check — no subprocess; optional in-process feed verify."""

from __future__ import annotations

import json

from _stack_paths import resolve_stack_root
from _stack_tools import load_tool

ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]

REQ = [
    ROOT / "SKILL.md",
    ROOT / "references" / "AGENT_CONTRACT.md",
    ROOT / "references" / "SECURITY.md",
    ROOT / "references" / "SUBMISSION_TRAINING.md",
    ROOT / "references" / "SKILLSPECTOR_AUDIT.md",
    ROOT / "scripts" / "_stack_paths.py",
    ROOT / "scripts" / "_stack_tools.py",
    ROOT / "scripts" / "gate_submission.py",
    ROOT / "scripts" / "verify_feed.py",
    ROOT / "scripts" / "agent_flow.py",
]
missing = [str(p) for p in REQ if not p.exists()]
if missing:
    print("MISSING", missing)
    raise SystemExit(2)

try:
    stack = resolve_stack_root()
except SystemExit:
    print("OK mirror (set LYGO_STACK_ROOT to run stack verify)")
else:
    feed = load_tool(stack, "haven_star_chart_feed.py")
    rows = feed.read_ledger()
    ok, errs = feed.verify_chain(rows)
    print(json.dumps({"stack": str(stack), "chain_valid": ok, "entries": len(rows), "errors": errs}))
    if not ok:
        print("WARN feed chain invalid")
        raise SystemExit(1)

print("OK lygo-haven-star-chart self_check")
raise SystemExit(0)