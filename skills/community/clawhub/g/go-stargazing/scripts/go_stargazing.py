#!/usr/bin/env python3
"""Stable entrypoint for go-stargazing.

This wrapper stays intentionally thin and delegates to the current engine.
Use this file as the preferred external entrypoint; keep
`dynamic_sampling_prototype.py` as the implementation file.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from dynamic_sampling_prototype import main


if __name__ == "__main__":
    main()
