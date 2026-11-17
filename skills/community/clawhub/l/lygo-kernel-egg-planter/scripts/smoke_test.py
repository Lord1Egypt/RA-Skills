#!/usr/bin/env python3
"""One-shot bulletproof self-check: preflight → verify → list (no plant)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def run(script: str, extra: list[str] | None = None) -> int:
    cmd = [sys.executable, str(SCRIPT_DIR / script)]
    if extra:
        cmd.extend(extra)
    return subprocess.call(cmd)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stack-root", default=None)
    args = ap.parse_args()
    root_args = ["--stack-root", args.stack_root] if args.stack_root else []

    steps = [
        ("preflight.py", root_args),
        ("verify_eggs.py", root_args),
        # list requires consent after v1.3 SkillSpector harden
        ("retrieve_egg.py", ["--i-consent", "--list", *root_args]),
    ]
    for name, extra in steps:
        rc = run(name, extra)
        if rc != 0:
            print(f"smoke_test FAIL at {name} (exit {rc})", file=sys.stderr)
            return rc
    print("smoke_test: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())