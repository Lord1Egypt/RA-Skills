#!/usr/bin/env python3
"""memory-shield — unified entry point.

Usage:
  python3 memory_shield.py <snapshot|scan|audit> [args...]

Thin wrapper around the three scripts:
  snapshot   -> scripts/snapshot.py      (save memory digest before compaction)
  scan       -> scripts/scan_poison.py   (detect injected instructions)
  audit      -> scripts/audit.py         (diff two snapshots)

Run with no arguments to see this help; `--help` works too.
"""
import subprocess, sys
from pathlib import Path

SCRIPTS = {
    "snapshot": "snapshot.py",
    "scan": "scan_poison.py",
    "audit": "audit.py",
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print(__doc__)
        return 0
    cmd = sys.argv[1]
    if cmd not in SCRIPTS:
        print(f"unknown command: {cmd}\n\n{__doc__}", file=sys.stderr)
        return 2
    script = Path(__file__).resolve().parent / SCRIPTS[cmd]
    return subprocess.call([sys.executable, str(script)] + sys.argv[2:])


if __name__ == "__main__":
    sys.exit(main())
