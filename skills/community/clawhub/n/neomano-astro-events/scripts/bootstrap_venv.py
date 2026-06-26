#!/usr/bin/env python3
"""Bootstrap venv for neomano-astro-events.

Uses Skyfield for ephemeris calculations.
"""

import subprocess
import sys
from pathlib import Path


def run(cmd):
    print("+", " ".join(cmd))
    subprocess.check_call(cmd)


def main():
    base = Path(__file__).resolve().parents[1]
    venv = base / ".venv"
    if not (venv / "bin" / "python").exists():
        run([sys.executable, "-m", "venv", str(venv)])
    py = str(venv / "bin" / "python")
    run([py, "-m", "pip", "install", "--upgrade", "pip"])
    run([py, "-m", "pip", "install", "skyfield", "pytz"])
    print(f"✓ venv ready at {venv}")


if __name__ == "__main__":
    raise SystemExit(main())
