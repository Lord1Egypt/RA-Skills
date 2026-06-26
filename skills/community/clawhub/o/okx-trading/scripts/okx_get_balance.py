#!/usr/bin/env python3
"""Print the OKX unified-account balance summary."""
from __future__ import annotations

import sys

from _okx_client import account_api, env_summary


def main() -> int:
    api = account_api()
    resp = api.get_account_balance()
    if resp.get("code") != "0":
        print(f"OKX error: {resp.get('msg')!r}", file=sys.stderr)
        return 1

    data = resp.get("data") or []
    if not data:
        print("No balance data returned.")
        return 0
    summary = data[0]
    total_eq = summary.get("totalEq", "0")
    print(f"{env_summary()}")
    print(f"Total equity (USDT-est): {total_eq}")
    print()
    print(f"{'CCY':<8} {'Equity':>14} {'Available':>14} {'Frozen':>12}")
    for d in sorted(summary.get("details") or [], key=lambda x: -float(x.get("eqUsd") or 0)):
        eq = d.get("eq", "0")
        if float(eq or 0) == 0:
            continue
        print(f"{d.get('ccy', ''):<8} {eq:>14} {d.get('availBal', ''):>14} {d.get('frozenBal', ''):>12}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
