#!/usr/bin/env python3
"""Discard a pending proposal (the 'NO <id>' path).

Does NOT require a confirmation token — cancelling a proposal is always safe
because no order has been placed yet.
"""
from __future__ import annotations

import argparse
import sys

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
    print(f"Discarded proposal {args.id}: {record.get('kind','?')} on {payload.get('instId','?')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
