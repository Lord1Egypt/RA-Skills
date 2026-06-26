#!/usr/bin/env python3
"""Estimate spoken runtime based on word count.

Default speaking rate is 145 words per minute.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path


MIN_SECONDS = 180
MAX_SECONDS = 300


def estimate_seconds(text: str, wpm: int) -> int:
    words = len([w for w in text.split() if w.strip()])
    return math.ceil((words / max(wpm, 1)) * 60)


def main() -> int:
    parser = argparse.ArgumentParser(description="Estimate narrated runtime")
    parser.add_argument("--file", type=Path, required=True, help="Text file to analyze")
    parser.add_argument("--wpm", type=int, default=145, help="Words per minute")
    args = parser.parse_args()

    text = args.file.read_text(encoding="utf-8")
    seconds = estimate_seconds(text, args.wpm)
    in_range = MIN_SECONDS <= seconds <= MAX_SECONDS

    print(f"file={args.file}")
    print(f"estimated_seconds={seconds}")
    print(f"target_range_seconds={MIN_SECONDS}-{MAX_SECONDS}")
    print(f"in_target_range={'yes' if in_range else 'no'}")

    return 0 if in_range else 2


if __name__ == "__main__":
    raise SystemExit(main())
