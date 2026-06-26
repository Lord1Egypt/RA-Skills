#!/usr/bin/env python3
"""Smoke tests (no live Odoo calls)."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def test_manager_help():
    script = ROOT / "src" / "odoo_manager.py"
    r = subprocess.run(
        [sys.executable, str(script), "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert r.returncode == 0, r.stderr
    assert "check_sales" in r.stdout


if __name__ == "__main__":
    test_manager_help()
    print("tests.py: ok")
