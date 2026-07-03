#!/usr/bin/env python3
"""Plant Δ9 Champion Kernel Eggs via stack tools (consent-gated)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from _stack_paths import require_consent, resolve_stack_root  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Plant 15 Δ9 champion kernel eggs")
    ap.add_argument("--i-consent", action="store_true")
    ap.add_argument("--stack-root", default=None)
    ap.add_argument("--skip-army", action="store_true")
    args = ap.parse_args()
    require_consent(args.i_consent)
    stack = resolve_stack_root(args.stack_root)
    cmd = [sys.executable, str(stack / "tools" / "champion_egg_planter.py"), "--i-consent"]
    if args.skip_army:
        cmd.append("--skip-army")
    return subprocess.call(cmd, cwd=stack)


if __name__ == "__main__":
    raise SystemExit(main())