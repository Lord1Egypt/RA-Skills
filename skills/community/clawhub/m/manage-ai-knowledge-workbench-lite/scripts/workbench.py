#!/usr/bin/env python3
"""Portable launcher for the vendored deterministic workbench runtime."""

from __future__ import annotations

from pathlib import Path
import sys


RUNTIME = Path(__file__).resolve().parent / "runtime"
sys.dont_write_bytecode = True
sys.path.insert(0, str(RUNTIME))

from workbench.lite_cli import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
