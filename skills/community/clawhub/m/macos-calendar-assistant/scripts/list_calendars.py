#!/usr/bin/env python3
"""Deprecated compatibility wrapper.

Use `swift scripts/list_calendars.swift` directly.
"""

import subprocess
import sys
from pathlib import Path


def main():
    script = Path(__file__).resolve().parent / "list_calendars.swift"
    p = subprocess.run(["swift", str(script)], capture_output=True, text=True)
    if p.returncode != 0:
        print(p.stderr or p.stdout, file=sys.stderr)
        sys.exit(1)
    print(p.stdout)


if __name__ == "__main__":
    main()
