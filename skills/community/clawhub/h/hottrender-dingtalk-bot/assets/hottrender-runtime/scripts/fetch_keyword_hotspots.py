#!/usr/bin/env python3
"""Fetch vertical/custom-keyword hotspot search results."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.crawler import (
    DEFAULT_KEYWORD_PLATFORMS,
    DEFAULT_REGIONS,
    fetch_keyword_hotspots,
    parse_csv,
    write_result,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch custom keyword hotspots.")
    parser.add_argument("--keywords", required=True, help="Comma-separated custom keywords, e.g. 乙游,短剧,AI男友")
    parser.add_argument("--regions", default=",".join(DEFAULT_REGIONS), help="Comma-separated regions: jp,us,tw,kr")
    parser.add_argument("--platforms", default=",".join(DEFAULT_KEYWORD_PLATFORMS), help="Comma-separated platforms")
    parser.add_argument("--time-range", default="7d")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--config", default="", help="Provider config YAML path")
    parser.add_argument("--output", default="out/keyword_hotspots.md", help="Output .md or .json path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = fetch_keyword_hotspots(
        keywords=parse_csv(args.keywords, []),
        regions=parse_csv(args.regions, DEFAULT_REGIONS),
        platforms=parse_csv(args.platforms, DEFAULT_KEYWORD_PLATFORMS),
        time_range=args.time_range,
        limit=max(args.limit, 1),
        config_path=args.config or None,
    )
    write_result(payload, args.output)
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
