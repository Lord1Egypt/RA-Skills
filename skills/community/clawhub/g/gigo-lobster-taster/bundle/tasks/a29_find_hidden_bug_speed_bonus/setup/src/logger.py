"""Logging stub (not the bug)."""

import sys


def info(msg: str) -> None:
    print(f"[info] {msg}", file=sys.stderr)
