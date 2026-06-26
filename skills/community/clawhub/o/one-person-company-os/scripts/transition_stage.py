#!/usr/bin/env python3
"""Deprecated v0.x stage command."""

from __future__ import annotations

import sys


def main() -> int:
    print(
        "transition_stage.py is deprecated in One Person Company OS v1.0. "
        "v1.0 does not write stage state; use update_focus.py to change the primary arena "
        "and business-loop bottleneck.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
