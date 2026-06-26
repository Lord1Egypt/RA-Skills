#!/usr/bin/env python3
"""Deprecated v0.x round command."""

from __future__ import annotations

import sys


def main() -> int:
    print(
        "update_round.py is deprecated in One Person Company OS v1.0. "
        "Use the business-loop commands: update_focus.py, advance_offer.py, "
        "advance_pipeline.py, advance_product.py, advance_delivery.py, "
        "update_cash.py, calibrate_business.py, or record_asset.py.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
