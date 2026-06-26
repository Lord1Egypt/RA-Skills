#!/usr/bin/env python3
"""Deprecated v0.x round calibration command."""

from __future__ import annotations

import sys


def main() -> int:
    print(
        "calibrate_round.py is deprecated in One Person Company OS v1.0. "
        "Use calibrate_business.py to record a bottleneck, decision, and next action.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
