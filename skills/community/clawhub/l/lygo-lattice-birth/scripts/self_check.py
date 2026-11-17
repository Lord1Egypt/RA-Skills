#!/usr/bin/env python3
"""Verify lygo-lattice-birth skill can load stack tools in-process."""

from __future__ import annotations

import json

from _stack_paths import resolve_stack_root
from _stack_tools import ALLOWED_TOOLS, load_tool


def main() -> int:
    stack = resolve_stack_root()
    report = {"stack_root": str(stack), "tools": {}}
    for name in sorted(ALLOWED_TOOLS):
        mod = load_tool(stack, name)
        report["tools"][name] = "ok" if mod else "fail"
    report["signature"] = "Δ9Φ963-LATTICE-BIRTH-SELF-CHECK-v1"
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())