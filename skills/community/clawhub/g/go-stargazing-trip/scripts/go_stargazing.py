#!/usr/bin/env python3
"""Compatibility entrypoint for go-stargazing-trip.

Keep this wrapper only for backward compatibility.
Preferred external entrypoint is `go_stargazing_trip.py`.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from dynamic_sampling_prototype import main


if __name__ == "__main__":
    main()
