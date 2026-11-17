#!/usr/bin/env python3
"""
Options Wheel Strategy Screener — scan tickers for cash-secured put
candidates suited to the wheel strategy, using free Yahoo Finance data
via yfinance (no API key required).

For each ticker, finds the nearest expiration within a target DTE (days
to expiration) window, picks the put strike closest to a target delta
approximation (using moneyness as a simple proxy since yfinance does not
provide live greeks), and estimates annualized return on capital if the
put expires worthless.

This is a screening/idea-generation tool, not a broker or execution
system, and does not place trades.

Usage:
    python3 wheel_screener.py AAPL MSFT KO PEP --dte 30 --otm-pct 5
    python3 wheel_screener.py AAPL --dte 21 --otm-pct 8 --min-premium-yield 1.0
"""

import argparse
import sys
from datetime import datetime

import yfinance as yf


def pick_expiration(expirations, target_dte):
    today = datetime.now().date()
    best = None
    best_diff = None
    for exp_str in expirations:
        exp_date = datetime.strptime(exp_str, "%Y-%m-%d").date()
        dte = (exp_date - today).days
        if dte <= 0:
            continue
        diff = abs(dte - target_dte)
        if best_diff is None or diff < best_diff:
            best, best_diff = (exp_str, dte), diff
    return best


def screen_ticker(symbol, target_dte, otm_pct, min_premium_yield):
    t = yf.Ticker(symbol)
    hist = t.history(period="1d")
    if hist.empty:
        return {"symbol": symbol, "error": "no price data"}
    spot = float(hist["Close"].iloc[-1])

    expirations = t.options
    if not expirations:
        return {"symbol": symbol, "error": "no options chain available"}

    picked = pick_expiration(expirations, target_dte)
    if not picked:
        return {"symbol": symbol, "error": "no valid future expiration found"}
    exp_str, dte = picked

    chain = t.option_chain(exp_str)
    puts = chain.puts
    if puts.empty:
        return {"symbol": symbol, "error": "no puts listed for this expiration"}

    target_strike = spot * (1 - otm_pct / 100)
    puts = puts.copy()
    puts["strike_diff"] = (puts["strike"] - target_strike).abs()
    puts = puts.sort_values("strike_diff")
    row = puts.iloc[0]

    strike = float(row["strike"])
    bid = float(row["bid"]) if row["bid"] == row["bid"] else 0.0
    ask = float(row["ask"]) if row["ask"] == row["ask"] else 0.0
    mid_premium = (bid + ask) / 2 if (bid or ask) else float(row.get("lastPrice", 0) or 0)
    volume = int(row["volume"]) if row["volume"] == row["volume"] else 0
    open_interest = int(row["openInterest"]) if row["openInterest"] == row["openInterest"] else 0
    iv = float(row["impliedVolatility"]) if row["impliedVolatility"] == row["impliedVolatility"] else None

    capital_required = strike * 100
    premium_income = mid_premium * 100
    period_yield_pct = (premium_income / capital_required * 100) if capital_required else 0
    annualized_pct = period_yield_pct * (365 / dte) if dte else 0

    result = {
        "symbol": symbol,
        "spot": round(spot, 2),
        "expiration": exp_str,
        "dte": dte,
        "strike": strike,
        "pct_otm": round((spot - strike) / spot * 100, 2),
        "mid_premium": round(mid_premium, 2),
        "capital_required": round(capital_required, 2),
        "period_yield_pct": round(period_yield_pct, 2),
        "annualized_yield_pct": round(annualized_pct, 2),
        "implied_volatility": round(iv * 100, 1) if iv else None,
        "volume": volume,
        "open_interest": open_interest,
        "meets_min_yield": annualized_pct >= min_premium_yield * (365 / dte) if min_premium_yield else True,
    }
    return result


def main():
    ap = argparse.ArgumentParser(description="Screen tickers for wheel-strategy cash-secured put candidates")
    ap.add_argument("tickers", nargs="+", help="Ticker symbols to screen, e.g. AAPL MSFT KO")
    ap.add_argument("--dte", type=int, default=30, help="Target days to expiration (default 30)")
    ap.add_argument("--otm-pct", type=float, default=5.0,
                     help="Target %% out-of-the-money for the put strike (default 5.0)")
    ap.add_argument("--min-premium-yield", type=float, default=0.0,
                     help="Minimum period premium yield %% to flag as meeting target (default 0, no filter)")
    args = ap.parse_args()

    results = []
    for sym in args.tickers:
        try:
            r = screen_ticker(sym.upper(), args.dte, args.otm_pct, args.min_premium_yield)
        except Exception as e:
            r = {"symbol": sym.upper(), "error": str(e)}
        results.append(r)

    print(f"{'Symbol':8}{'Spot':>9}{'Strike':>9}{'%OTM':>7}{'DTE':>5}{'Premium':>9}"
          f"{'PeriodYld%':>11}{'AnnYld%':>9}{'IV%':>7}{'OI':>7}")
    print("-" * 90)
    for r in results:
        if "error" in r:
            print(f"{r['symbol']:8}  ERROR: {r['error']}")
            continue
        flag = " *" if r.get("meets_min_yield") and args.min_premium_yield else ""
        print(f"{r['symbol']:8}{r['spot']:>9.2f}{r['strike']:>9.2f}{r['pct_otm']:>7.1f}"
              f"{r['dte']:>5}{r['mid_premium']:>9.2f}{r['period_yield_pct']:>11.2f}"
              f"{r['annualized_yield_pct']:>9.1f}{(r['implied_volatility'] or 0):>7.1f}"
              f"{r['open_interest']:>7}{flag}")

    print("\nNote: premium yields are estimates based on mid-price quotes and assume the "
          "put expires worthless. This is idea generation only — verify live quotes and "
          "liquidity (bid/ask spread, open interest) before placing any trade. Not financial advice.")


if __name__ == "__main__":
    main()
