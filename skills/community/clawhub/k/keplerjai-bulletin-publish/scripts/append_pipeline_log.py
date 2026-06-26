#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Append a timestamped line to a pipeline log file.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a timestamped line to pipeline.log")
    parser.add_argument("--log-file", required=True, help="Absolute path to the log file")
    parser.add_argument("--message", required=True, help="Message to append")
    args = parser.parse_args()

    log_path = Path(args.log_file).expanduser().resolve()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(f"[{timestamp}] {args.message}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
