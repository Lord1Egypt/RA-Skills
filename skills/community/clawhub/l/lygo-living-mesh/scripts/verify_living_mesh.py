#!/usr/bin/env python3
"""Full living mesh verify A+B+C+D (delegates to stack tools)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _stack_invoke import invoke  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(invoke("verify_living_mesh.py"))
