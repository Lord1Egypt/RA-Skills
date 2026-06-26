#!/usr/bin/env python3
"""Propose stopping a grid. Creates a pending kind='grid_stop' that the user
must confirm before okx_grid_stop.py will actually cancel orders."""
from __future__ import annotations

import argparse
import sys

from _pending import PENDING_DIR, PendingError, load_strategy, save_pending


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--strategy-id", required=True)
    args = p.parse_args()

    try:
        strategy = load_strategy(args.strategy_id)
    except PendingError as e:
        print(str(e), file=sys.stderr)
        return 1

    payload = {
        "strategy_id": args.strategy_id,
        "instId": strategy.get("instId"),
        "active_order_count": len(strategy.get("active_orders") or []),
    }
    pid, _token = save_pending("grid_stop", payload)
    pending_path = PENDING_DIR / f"{pid}.json"

    print(f"Grid-stop proposal id: {pid}")
    print(f"Pending file: {pending_path}")
    print(f"  strategy_id : {args.strategy_id}")
    print(f"  instId      : {strategy.get('instId')}")
    print(f"  active orders that will be cancelled: {len(strategy.get('active_orders') or [])}")
    print()
    print(f"To confirm in chat: YES {pid}")
    print(f"To keep the grid : NO {pid}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
