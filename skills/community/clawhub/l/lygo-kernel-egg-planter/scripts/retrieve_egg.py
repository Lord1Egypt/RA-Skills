#!/usr/bin/env python3
"""Retrieve eggs only after tamper verify passes. No force/skip bypass."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from _stack_paths import require_consent, resolve_stack_root  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Retrieve kernel eggs after tamper verify. "
            "Listing and retrieval require --i-consent (or LYGO_EGG_PLANT_CONSENT). "
            "No --force: QUARANTINE always blocks retrieve."
        )
    )
    ap.add_argument("--list", action="store_true", help="List eggs after verify")
    ap.add_argument("--egg", default=None, help="Egg id to retrieve (metadata/payload via stack tool)")
    ap.add_argument("--stack-root", default=None)
    ap.add_argument(
        "--i-consent",
        action="store_true",
        help="Required: explicit consent to access egg registry content",
    )
    args = ap.parse_args()

    # Consent for any retrieve/list access (audit finding: was missing)
    require_consent(args.i_consent)

    stack = resolve_stack_root(args.stack_root)
    tool = stack / "tools" / "retrieve_kernel_egg.py"
    if not tool.is_file():
        print(f"Missing stack tool: {tool}", file=sys.stderr)
        return 1

    # Always verify first — no bypass
    rc = subprocess.call(
        [sys.executable, str(SCRIPT_DIR / "verify_eggs.py"), "--stack-root", str(stack)]
    )
    if rc != 0:
        print(
            "Retrieve blocked: tamper verify failed (QUARANTINE). "
            "No force path — repair eggs/registry first.",
            file=sys.stderr,
        )
        return 2

    cmd = [sys.executable, str(tool)]
    if args.list or not args.egg:
        cmd.append("--list")
    else:
        cmd.extend(["--egg", args.egg])
    return subprocess.call(cmd, cwd=stack)


if __name__ == "__main__":
    raise SystemExit(main())
