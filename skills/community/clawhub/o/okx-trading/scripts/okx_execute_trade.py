#!/usr/bin/env python3
"""Step 4 of the trade gate: execute a previously-proposed trade.

Refuses unless --confirmation-token matches the token stored in the pending
file. Re-checks guardrails (notional caps may have been hit by another fill
since propose time). Logs the executed notional for the daily-cap accounting.
"""
from __future__ import annotations

import argparse
import json
import sys

from _guardrails import GuardrailError, check_all
from _okx_client import trade_api
from _pending import (
    PendingError,
    append_notional_log,
    delete_pending,
    load_pending,
    validate_token,
)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--id", required=True, help="Proposal id from okx_propose_trade.py")
    p.add_argument(
        "--confirmation-token",
        required=True,
        help="Read this from ~/.aeon/okx/pending/<id>.json — DO NOT fabricate.",
    )
    args = p.parse_args()

    try:
        record = load_pending(args.id)
        validate_token(record, args.confirmation_token)
    except PendingError as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 3

    if record.get("kind") != "trade":
        print(f"REFUSED: proposal {args.id} is kind={record.get('kind')!r}, not 'trade'", file=sys.stderr)
        return 3

    payload = record["payload"]
    api_params = payload["api_params"]

    # Re-check guardrails — circumstances may have changed since the proposal.
    try:
        check_all(payload["instId"], float(payload["notional_usdt"]))
    except GuardrailError as e:
        print(f"REFUSED at execute time: {e}", file=sys.stderr)
        return 3

    # Place the order.
    resp = trade_api().place_order(**api_params)
    if resp.get("code") != "0":
        # Don't delete pending on transient errors — let the user retry.
        print(f"OKX rejected order: {resp.get('msg')!r}", file=sys.stderr)
        print(json.dumps(resp, indent=2))
        return 1

    # Best-effort: extract the assigned ordId.
    data = resp.get("data") or [{}]
    ord_id = data[0].get("ordId", "?") if data else "?"
    sCode = data[0].get("sCode", "0") if data else "0"
    sMsg = data[0].get("sMsg", "") if data else ""

    if sCode != "0":
        print(f"OKX inner error sCode={sCode}: {sMsg!r}", file=sys.stderr)
        print(json.dumps(resp, indent=2))
        return 1

    # Log notional toward daily cap.
    append_notional_log({
        "id": record["id"],
        "ordId": ord_id,
        "instId": payload["instId"],
        "side": payload["side"],
        "notional_usdt": payload["notional_usdt"],
    })

    # Consume the pending record so it cannot be replayed.
    delete_pending(args.id)

    print(f"Order placed.")
    print(f"  proposal id : {record['id']}")
    print(f"  ord id      : {ord_id}")
    print(f"  instId      : {payload['instId']}")
    print(f"  side        : {payload['side']}")
    print(f"  notional    : ~{payload['notional_usdt']:.2f} USDT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
