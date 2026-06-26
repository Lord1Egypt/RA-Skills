#!/usr/bin/env python3

from pathlib import Path
import sys


RUNTIME_DIR = Path(__file__).resolve().parent / "runtime"
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

from openclaw_capture_skill.cli import main


if __name__ == "__main__":
    raise SystemExit(main())

