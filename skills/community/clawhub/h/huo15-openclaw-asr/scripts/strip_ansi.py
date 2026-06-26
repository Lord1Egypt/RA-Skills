#!/usr/bin/env python3
"""Strip ANSI escape sequences from text; useful for terminal/session logs."""

import re
import sys

ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def strip_ansi(s: str) -> str:
    return ANSI_RE.sub("", s)


def main() -> int:
    if len(sys.argv) < 2:
        data = sys.stdin.read()
    else:
        with open(sys.argv[1], encoding="utf-8", errors="replace") as f:
            data = f.read()
    sys.stdout.write(strip_ansi(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
