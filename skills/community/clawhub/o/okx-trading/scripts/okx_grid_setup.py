#!/usr/bin/env python3
"""Step 1 of the grid gate: propose a grid, do not execute.

A grid is a set of evenly-spaced buy limits below the current price (and,
once those fill, sells one level up). v1 supports spot only.

Sizing convention: --quote-sz-per-level is USDT per buy order. Per-level base
size is computed from the level price (sz = quote_sz_per_level / level_price).

The whole grid is confirmed once with YES <id>; subsequent fills inside the
grid do NOT require further confirmation. The bounded daily-cap guardrail is
re-checked inside okx_grid_step.py and halts the grid on breach.
"""
from __future__ import annotations

import argparse
import sys

from _guardrails import GuardrailError, check_daily_room, check_symbol
from _okx_client import inst_type_for, market_api
from _pending import PENDING_DIR, save_pending


def _level_prices(low: float, high: float, levels: int) -> list[float]:
    if levels < 2:
        raise ValueError("--levels must be >= 2")
    step = (high - low) / (levels - 1)
    return [round(low + i * step, 8) for i in range(levels)]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--instId", required=True)
    p.add_argument("--low", type=float, required=True)
    p.add_argument("--high", type=float, required=True)
    p.add_argument("--levels", type=int, required=True)
    p.add_argument("--quote-sz-per-level", type=float, required=True)
    p.add_argument(
        "--min-profit-gap",
        type=float,
        default=0.0,
        help="Refuse sells priced below avg_entry * (1 + gap). 0 = off. Typical: 0.005 (0.5%%).",
    )
    p.add_argument(
        "--max-position-base",
        type=float,
        default=0.0,
        help="Skip buys when total position (base ccy) >= this. 0 = off.",
    )
    p.add_argument(
        "--trailing-pct",
        type=float,
        default=0.0,
        help="When current price is within this fraction of the band edge, auto-recenter. 0 = off (halt instead). Typical: 0.1.",
    )
    p.add_argument(
        "--max-rescales",
        type=int,
        default=0,
        help="Maximum autonomous re-centers permitted across the lifetime of the grid. Only meaningful if --trailing-pct > 0.",
    )
    args = p.parse_args()

    if args.low >= args.high:
        print("--low must be strictly less than --high", file=sys.stderr)
        return 2
    if args.quote_sz_per_level <= 0:
        print("--quote-sz-per-level must be positive", file=sys.stderr)
        return 2
    if args.min_profit_gap < 0 or args.max_position_base < 0:
        print("--min-profit-gap and --max-position-base must be non-negative", file=sys.stderr)
        return 2
    if args.trailing_pct < 0 or args.trailing_pct >= 0.5:
        print("--trailing-pct must be in [0, 0.5)", file=sys.stderr)
        return 2
    if args.max_rescales < 0:
        print("--max-rescales must be non-negative", file=sys.stderr)
        return 2
    if args.trailing_pct > 0 and args.max_rescales == 0:
        print("--trailing-pct > 0 requires --max-rescales > 0 (else trailing can never fire)", file=sys.stderr)
        return 2

    try:
        inst_type = inst_type_for(args.instId)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2
    if inst_type != "SPOT":
        print(f"Grids are spot-only in v1; got {inst_type} for {args.instId}", file=sys.stderr)
        return 2

    # Reference price.
    tick = market_api().get_ticker(instId=args.instId)
    if tick.get("code") != "0" or not tick.get("data"):
        print(f"Could not fetch ticker for {args.instId}: {tick.get('msg')!r}", file=sys.stderr)
        return 1
    ref_px = float(tick["data"][0]["last"])

    try:
        prices = _level_prices(args.low, args.high, args.levels)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 2

    initial_buys = [px for px in prices if px < ref_px]
    deferred_sells = [px for px in prices if px >= ref_px]

    total_initial_deployment = args.quote_sz_per_level * len(initial_buys)

    # Guardrails: symbol allow-list and daily cap on the *initial deployment*.
    # Per-trade cap is intentionally NOT applied (each level can be small) but
    # the user is implicitly approving the initial USDT outlay.
    try:
        check_symbol(args.instId)
        check_daily_room(total_initial_deployment)
    except GuardrailError as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 3

    payload = {
        "instId": args.instId,
        "low": args.low,
        "high": args.high,
        "levels": args.levels,
        "quote_sz_per_level": args.quote_sz_per_level,
        "ref_price_at_propose": ref_px,
        "level_prices": prices,
        "initial_buy_prices": initial_buys,
        "initial_sell_prices": deferred_sells,
        "total_initial_deployment_usdt": round(total_initial_deployment, 4),
        "min_profit_gap": args.min_profit_gap,
        "max_position_base": args.max_position_base,
        "trailing_pct": args.trailing_pct,
        "max_rescales": args.max_rescales,
    }
    pid, _token = save_pending("grid", payload)
    pending_path = PENDING_DIR / f"{pid}.json"

    print(f"Grid proposal id: {pid}")
    print(f"Pending file: {pending_path}")
    print(f"  instId           : {args.instId}")
    print(f"  range            : {args.low} – {args.high}")
    print(f"  levels           : {args.levels}  (step = {(args.high - args.low) / (args.levels - 1):.4f})")
    print(f"  per-level USDT   : {args.quote_sz_per_level}")
    print(f"  ref price        : {ref_px}")
    print(f"  initial buys     : {len(initial_buys)} orders below ref ({initial_buys[:5]}{' …' if len(initial_buys) > 5 else ''})")
    print(f"  deferred sells   : {len(deferred_sells)} (placed automatically after each buy fills one level up)")
    print(f"  initial outlay   : ~{total_initial_deployment:.2f} USDT")
    if args.min_profit_gap > 0:
        print(f"  cost-basis floor : sells refused below avg_entry * (1 + {args.min_profit_gap})")
    if args.max_position_base > 0:
        print(f"  position cap     : buys halted when position >= {args.max_position_base} (base ccy)")
    if args.trailing_pct > 0:
        print(
            f"  auto-rescale     : YES \xe2\x80\x94 recenters when price is within {args.trailing_pct*100:.1f}% of edge, "
            f"up to {args.max_rescales} time(s). Confirming this proposal authorises bounded autonomous rebalancing."
        )
    else:
        print(f"  auto-rescale     : OFF (grid halts when price exits range)")
    print()
    print(f"To confirm in chat: YES {pid}")
    print(f"To discard       : NO {pid}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
