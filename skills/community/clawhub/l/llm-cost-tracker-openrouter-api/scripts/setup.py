#!/usr/bin/env python3
"""
llm-cost-tracker setup script.
Validates environment and installs dependencies.
"""
import sys
import subprocess
import os
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
REQUIREMENTS = SKILL_DIR / "requirements.txt"
SCRIPTS_DIR = SKILL_DIR / "scripts"

def main():
    errors = []

    # Check Python version
    if sys.version_info < (3, 7):
        print(f"[ERROR] Python 3.7+ required, got {sys.version_info.major}.{sys.version_info.minor}")
        errors.append("Python version")

    # Check scripts dir
    if not SCRIPTS_DIR.is_dir():
        print(f"[ERROR] scripts/ directory not found at {SCRIPTS_DIR}")
        errors.append("scripts dir")
    else:
        required = ["collect_usage.py", "prune_usage.py", "run_tracker.py"]
        for s in required:
            p = SCRIPTS_DIR / s
            if not p.is_file():
                print(f"[ERROR] Required script missing: {s}")
                errors.append(f"script:{s}")

    # Install deps
    if REQUIREMENTS.is_file():
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(REQUIREMENTS)],
                             capture_output=True, text=True)
        if result.returncode == 0:
            print("[OK] Dependencies installed")
        else:
            # Check if it's just already-installed noise
            if "already satisfied" in result.stderr.lower() or result.returncode == 0:
                print("[OK] Dependencies already satisfied")
            else:
                print(f"[WARN] pip install: {result.stderr.strip().splitlines()[-1] if result.stderr else 'assume ok'}")

    if errors:
        print(f"\n[FAIL] Setup incomplete — {len(errors)} issue(s)")
        return 1
    print("\n[OK] Setup complete")
    return 0

if __name__ == "__main__":
    sys.exit(main())
