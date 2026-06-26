#!/usr/bin/env python3
"""Step 4 of the IBKR trade gate: execute a previously-proposed trade.

Refuses unless --confirmation-token matches the token stored in the pending
file. Re-checks guardrails (notional caps may have been hit by another fill
since propose time). Logs the executed notional for the daily-cap accounting.
"""
from __future__ import annotations

import argparse
import json
import sys

from _audit import append as audit_append
from _guardrails import GuardrailError, check_all
from _ibkr_client import connect, env_summary
from _pending import (
    PendingError,
    append_notional_log,
    delete_pending,
    load_pending,
    validate_token,
)


def _build_contract(p: dict):
    from ib_async import Stock

    c = Stock(p["symbol"], p["exchange"], p["currency"])
    if p.get("primaryExchange"):
        c.primaryExchange = p["primaryExchange"]
    if p.get("conId"):
        c.conId = int(p["conId"])
    return c


def _build_order(p: dict):
    from ib_async import Order

    o = Order()
    o.action = p["action"]
    o.totalQuantity = float(p["totalQuantity"])
    o.orderType = p["orderType"]
    o.tif = p.get("tif", "DAY")
    o.outsideRth = bool(p.get("outsideRth", False))
    o.transmit = bool(p.get("transmit", True))
    if p["orderType"] == "LMT":
        o.lmtPrice = float(p["lmtPrice"])
    return o


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--id", required=True, help="Proposal id from ibkr_propose_trade.py")
    p.add_argument(
        "--confirmation-token",
        required=True,
        help="Read this from ~/.aeon/ibkr/pending/<id>.json — DO NOT fabricate.",
    )
    p.add_argument("--wait-fill-seconds", type=float, default=10.0,
                   help="How long to wait for fills/state after placing. Default 10s.")
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

    try:
        check_all(payload["symbol"], float(payload["notional_usd"]))
    except GuardrailError as e:
        audit_append("daily_cap_breach", id=record["id"], symbol=payload["symbol"], reason=str(e))
        print(f"REFUSED at execute time: {e}", file=sys.stderr)
        return 3

    # Critical: ib_async will refuse to place an order on a readonly session.
    ib = connect(readonly=False)
    try:
        contract = _build_contract(payload["contract"])
        qualified = ib.qualifyContracts(contract)
        if not qualified:
            print(f"Could not qualify contract at execute time for {payload['symbol']}", file=sys.stderr)
            return 1
        contract = qualified[0]
        order = _build_order(payload["order"])

        trade = ib.placeOrder(contract, order)
        ib.sleep(args.wait_fill_seconds)

        # Drain any pending events.
        ib.waitOnUpdate(timeout=2.0)

        ord_id = trade.order.orderId
        status = trade.orderStatus.status
        filled = float(trade.orderStatus.filled or 0)
        avg_fill = float(trade.orderStatus.avgFillPrice or 0)
        remaining = float(trade.orderStatus.remaining or 0)

        if status in ("ApiCancelled", "Cancelled", "Inactive"):
            audit_append(
                "proposal_rejected",
                id=record["id"],
                symbol=payload["symbol"],
                ord_id=ord_id,
                status=status,
            )
            print(f"IBKR rejected/cancelled order: {status}", file=sys.stderr)
            print(json.dumps({"status": status, "log": [str(le) for le in trade.log[-5:]]}, indent=2))
            return 1

        # Optimistically log the proposed notional (filled price gets logged when status flips to Filled).
        actual_notional = filled * avg_fill if filled and avg_fill else float(payload["notional_usd"])
        append_notional_log({
            "id": record["id"],
            "ord_id": ord_id,
            "symbol": payload["symbol"],
            "side": payload["side"],
            "notional_usd": actual_notional,
        })
        audit_append(
            "proposal_executed",
            id=record["id"],
            symbol=payload["symbol"],
            ord_id=ord_id,
            status=status,
            filled=filled,
            avg_fill=avg_fill,
            remaining=remaining,
            notional_usd=round(actual_notional, 4),
        )

        delete_pending(args.id)

        print(env_summary())
        print(f"Order placed.")
        print(f"  proposal id : {record['id']}")
        print(f"  ord id      : {ord_id}")
        print(f"  symbol      : {payload['symbol']}")
        print(f"  side        : {payload['side']}")
        print(f"  status      : {status}")
        print(f"  filled      : {filled} @ ${avg_fill:.4f}")
        print(f"  remaining   : {remaining}")
        print(f"  notional    : ~${actual_notional:.2f}")
    finally:
        ib.disconnect()
    return 0


if __name__ == "__main__":
    sys.exit(main())
