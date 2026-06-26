#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


if __name__ == "__main__":
    target = Path(__file__).resolve().parent / "reference_media.py"
    raise SystemExit(subprocess.call([sys.executable, str(target), *sys.argv[1:]]))
