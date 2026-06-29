#!/usr/bin/env python3
"""100 块锚定法验算。用法: python calc_anchor.py --pb 40.4 --pe 35.22"""
from __future__ import annotations

import argparse
import sys


def calc(
    pb: float,
    pe: float | None = None,
    net_profit_ttm: float | None = None,
    market_cap: float | None = None,
) -> dict[str, float]:
    if pb <= 0:
        raise ValueError(f"PB must be > 0, got {pb}")
    net_assets = 100 / pb
    if pe is not None and pe > 0:
        profit = 100 / pe
    elif net_profit_ttm is not None and market_cap is not None and market_cap > 0:
        profit = (net_profit_ttm / market_cap) * 100
    else:
        raise ValueError("Need pe>0, or net_profit_ttm+market_cap for loss path")
    roe = profit / net_assets if net_assets else 0.0
    return {"net_assets_100": net_assets, "profit_100": profit, "roe_100": roe}


def _self_check() -> None:
    r = calc(pb=40.4, pe=35.22)
    assert abs(r["net_assets_100"] - 100 / 40.4) < 0.01
    assert abs(r["profit_100"] - 100 / 35.22) < 0.01
    assert abs(r["roe_100"] - r["profit_100"] / r["net_assets_100"]) < 0.001
    loss = calc(pb=0.33, net_profit_ttm=-59.52, market_cap=365.08)
    assert loss["profit_100"] < 0
    print("OK")


def main() -> None:
    p = argparse.ArgumentParser(description="100-block anchor valuation check")
    p.add_argument("--pb", type=float, help="Price-to-book ratio")
    p.add_argument("--pe", type=float, help="TTM PE (profitable companies)")
    p.add_argument("--net-profit-ttm", type=float, help="TTM net profit (loss path)")
    p.add_argument("--market-cap", type=float, help="Actual market cap (loss path)")
    p.add_argument("--self-check", action="store_true", help="Run built-in asserts")
    args = p.parse_args()
    if args.self_check:
        _self_check()
        return
    if args.pb is None:
        p.error("--pb is required unless --self-check")
    try:
        r = calc(args.pb, args.pe, args.net_profit_ttm, args.market_cap)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"net_assets_100={r['net_assets_100']:.4f}")
    print(f"profit_100={r['profit_100']:.4f}")
    print(f"roe_100={r['roe_100']:.2%}")


if __name__ == "__main__":
    main()
