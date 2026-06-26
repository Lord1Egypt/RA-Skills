#!/usr/bin/env python3
"""Discard a pending IBKR proposal (the 'NO <id>' path).

No confirmation token required — cancelling a proposal before any IBKR order
has been placed is always safe.
"""
from __future__ import annotations

import argparse
import sys

from _audit import append as audit_append
from _pending import PendingError, delete_pending, load_pending


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--id", required=True)
    args = p.parse_args()

    try:
        record = load_pending(args.id)
    except PendingError as e:
        print(str(e), file=sys.stderr)
        return 1

    delete_pending(args.id)
    payload = record.get("payload") or {}
    audit_append(
        "proposal_cancelled",
        id=args.id,
        symbol=payload.get("symbol"),
        side=payload.get("side"),
        notional_usd=payload.get("notional_usd"),
    )
    print(f"Discarded proposal {args.id}: {payload.get('side','?')} {payload.get('symbol','?')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
