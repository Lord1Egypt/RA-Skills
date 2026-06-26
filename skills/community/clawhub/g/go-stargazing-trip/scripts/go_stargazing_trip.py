#!/usr/bin/env python3
"""Stable entrypoint for go-stargazing-trip.

This wrapper delegates to the current engine implementation kept inside this
self-contained skill package.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from dynamic_sampling_prototype import main


if __name__ == "__main__":
    main()
