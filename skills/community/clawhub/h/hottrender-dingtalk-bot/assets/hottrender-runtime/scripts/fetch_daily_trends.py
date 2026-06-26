#!/usr/bin/env python3
"""Fetch four-region daily hotspot trends."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.crawler import DEFAULT_DAILY_PLATFORMS, DEFAULT_REGIONS, fetch_daily_trends, parse_csv, write_result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch daily hotspot trends for jp/us/tw/kr.")
    parser.add_argument("--regions", default=",".join(DEFAULT_REGIONS), help="Comma-separated regions: jp,us,tw,kr")
    parser.add_argument("--platforms", default=",".join(DEFAULT_DAILY_PLATFORMS), help="Comma-separated platforms")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--config", default="", help="Provider config YAML path")
    parser.add_argument("--output", default="out/daily_trends.md", help="Output .md or .json path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = fetch_daily_trends(
        regions=parse_csv(args.regions, DEFAULT_REGIONS),
        platforms=parse_csv(args.platforms, DEFAULT_DAILY_PLATFORMS),
        limit=max(args.limit, 1),
        config_path=args.config or None,
    )
    write_result(payload, args.output)
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
