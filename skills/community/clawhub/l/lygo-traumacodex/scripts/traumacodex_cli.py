#!/usr/bin/env python3
"""TraumaCodex CLI — in-package only (ClawHub-safe). No subprocess. No external stack exec."""
from __future__ import annotations

import sys
from pathlib import Path

# Import sibling module only (same package) — no subprocess, no LYGO_STACK_ROOT exec
sys.path.insert(0, str(Path(__file__).resolve().parent))
from traumacodex_core import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
