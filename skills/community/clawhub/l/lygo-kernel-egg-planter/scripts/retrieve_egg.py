#!/usr/bin/env python3
"""Retrieve eggs only after tamper verify passes (bulletproof)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from _stack_paths import resolve_stack_root  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--egg", default=None)
    ap.add_argument("--stack-root", default=None)
    ap.add_argument("--force", action="store_true", help="Skip verify (unsafe)")
    args = ap.parse_args()

    stack = resolve_stack_root(args.stack_root)
    tool = stack / "tools" / "retrieve_kernel_egg.py"
    if not tool.is_file():
        print(f"Missing stack tool: {tool}", file=sys.stderr)
        return 1

    if not args.force and not args.list:
        rc = subprocess.call(
            [sys.executable, str(SCRIPT_DIR / "verify_eggs.py"), "--stack-root", str(stack)]
        )
        if rc != 0:
            print("Retrieve blocked: tamper verify failed (use --force at your own risk)", file=sys.stderr)
            return 2

    cmd = [sys.executable, str(tool)]
    if args.list:
        cmd.append("--list")
    elif args.egg:
        cmd.extend(["--egg", args.egg])
    else:
        cmd.append("--list")
    return subprocess.call(cmd, cwd=stack)


if __name__ == "__main__":
    raise SystemExit(main())