#!/usr/bin/env python3
"""Deprecated v0.x round command."""

from __future__ import annotations

import sys


def main() -> int:
    print(
        "start_round.py is deprecated in One Person Company OS v1.0. "
        "Use update_focus.py, advance_product.py, advance_pipeline.py, "
        "advance_delivery.py, update_cash.py, or record_asset.py instead.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
