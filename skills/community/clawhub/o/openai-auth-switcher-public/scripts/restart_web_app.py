#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
STOP = CURRENT_DIR / 'stop_web_app.py'
INSTALL = CURRENT_DIR / 'install_web_app.py'


def main() -> int:
    subprocess.run(['python3', str(STOP)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    proc = subprocess.run(['python3', str(INSTALL), '--json'], capture_output=True, text=True)
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    return proc.returncode


if __name__ == '__main__':
    raise SystemExit(main())
