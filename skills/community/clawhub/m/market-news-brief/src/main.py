#!/usr/bin/env python3

# pyright: reportMissingImports=false

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "yfinance",
# ]
# ///
#
"""
Market News Brief - Get broad market headlines and proxy index moves from Yahoo Finance.
"""

import sys

from mutex import acquire_lock
from service import format_output, get_market_news_brief


def main():
    """Entry point - accepts an optional market scope and defaults to GLOBAL."""
    scope = sys.argv[1] if len(sys.argv) > 1 else "GLOBAL"
    with acquire_lock():
        result = get_market_news_brief(scope)
    print(format_output(result))


if __name__ == "__main__":
    main()
