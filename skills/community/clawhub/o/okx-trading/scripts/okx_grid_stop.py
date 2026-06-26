#!/usr/bin/env python3
"""Execute the cancellation of a grid: cancels every active order then deletes
the strategy file. Token-gated against okx_grid_propose_stop.py."""
from __future__ import annotations

import argparse
import sys

from _okx_client import trade_api
from _pending import (
    PendingError,
    delete_pending,
    delete_strategy,
    load_pending,
    load_strategy,
    validate_token,
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--id", required=True, help="Pending grid-stop proposal id")
    p.add_argument("--confirmation-token", required=True)
    args = p.parse_args()

    try:
        record = load_pending(args.id)
        validate_token(record, args.confirmation_token)
    except PendingError as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 3
    if record.get("kind") != "grid_stop":
        print(f"REFUSED: proposal {args.id} is not a grid_stop", file=sys.stderr)
        return 3

    strategy_id = record["payload"]["strategy_id"]
    try:
        strategy = load_strategy(strategy_id)
    except PendingError as e:
        # Strategy may have been deleted concurrently — clean up the pending and exit.
        delete_pending(args.id)
        print(str(e), file=sys.stderr)
        return 1

    api = trade_api()
    inst_id = strategy["instId"]
    cancelled = 0
    failed: list[str] = []
    for order in strategy.get("active_orders") or []:
        ord_id = order.get("ordId")
        if not ord_id:
            continue
        resp = api.cancel_order(instId=inst_id, ordId=ord_id)
        data = (resp.get("data") or [{}])[0]
        if resp.get("code") == "0" and data.get("sCode") == "0":
            cancelled += 1
        else:
            failed.append(f"{ord_id}({data.get('sMsg') or resp.get('msg')})")

    delete_strategy(strategy_id)
    delete_pending(args.id)

    print(f"Grid {strategy_id} stopped.")
    print(f"  cancelled : {cancelled}")
    if failed:
        print(f"  failed    : {len(failed)} — {failed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
