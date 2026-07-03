#!/usr/bin/env python3
"""Tamper verify — wraps stack verify_kernel_eggs.py (four pillars)."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys

from _stack_paths import resolve_stack_root


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify kernel eggs (SHA + Merkle + anchors)")
    ap.add_argument("--stack-root", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    stack = resolve_stack_root(args.stack_root)
    tool = stack / "tools" / "verify_kernel_eggs.py"
    rc = subprocess.call([sys.executable, str(tool)], cwd=stack)
    out = stack / "tests" / "kernel_eggs_last_run.json"
    if args.json and out.is_file():
        print(out.read_text(encoding="utf-8"))
    elif out.is_file():
        data = json.loads(out.read_text(encoding="utf-8"))
        print(f"verdict={data.get('verdict')} all_pass={data.get('all_pass')}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())