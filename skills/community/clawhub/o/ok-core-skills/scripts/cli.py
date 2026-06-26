#!/usr/bin/env python3
"""Backward-compatible shim.

Prefer:  uv run --project <skill-dir> ok-cli <command>
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ok.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
