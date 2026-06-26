#!/usr/bin/env python3
"""
VN Stock Return Estimator — fetch history from VNDirect, calculate CAGR/volatility/drawdown,
project 3 scenarios Bear/Base/Bull.

Usage:
  python3 estimate_returns.py FPT
  python3 estimate_returns.py VCB --capital 100
  python3 estimate_returns.py HPG --capital 50 --years 3
"""

import urllib.request
import json
import sys
import math
import argparse
from datetime import datetime, timedelta

RF_RATE = 0.055        # Risk-free rate: 5.5%/year (12-month bank deposit)
VN_INDEX_RETURN = 0.11 # VN-Index historical average ~11%/year

# ── Helpers ──────────────────────────────────────────────────────────────────

def fetch_history(symbol, days=1825):
    """Fetch daily OHLCV from VNDirect dChart API. Returns list of (timestamp, close)."""
    to_ts   = int(datetime.now().timestamp())
    from_ts = int((datetime.now() - timedelta(days=days)).timestamp())

    url = (
        f"https://dchart-api.vndirect.com.vn/dchart/history"
        f"?symbol={symbol}&resolution=D&from={from_ts}&to={to_ts}"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.loads(r.read())

    if not data.get("t") or not data.get("c"):
        return []

    # VNDirect returns prices in thousands of VND → multiply by 1000
    closes_raw = data["c"]
    closes = [c * 1000 if c < 10000 else c for c in closes_raw]
    return list(zip(data["t"], closes))

def calc_returns(prices):
    """List of (ts, close) → dict of metrics."""
    if len(prices) < 2:
        return None

    closes = [p[1] for p in prices]
    n = len(closes)

    # Daily returns
    daily = [(closes[i] / closes[i-1] - 1) for i in range(1, n)]

    # Volatility (annualized)
    mean_d = sum(daily) / len(daily)
    variance = sum((r - mean_d) ** 2 for r in daily) / (len(daily) - 1)
    vol = math.sqrt(variance) * math.sqrt(252)

    # Max Drawdown
    peak = closes[0]
    max_dd = 0.0
    for c in closes:
        if c > peak:
            peak = c
        dd = (c - peak) / peak
        if dd < max_dd:
            max_dd = dd

    # CAGR helper
    def cagr(start_price, end_price, years):
        if years <= 0 or start_price <= 0:
            return None
        return (end_price / start_price) ** (1 / years) - 1

    now_price = closes[-1]
    now_ts    = prices[-1][0]

    def price_n_days_ago(n_days):
        target_ts = now_ts - n_days * 86400
        # find closest price
        best = min(prices, key=lambda p: abs(p[0] - target_ts))
        return best[1], (now_ts - best[0]) / (365.25 * 86400)

    p3m,  y3m  = price_n_days_ago(90)
    p6m,  y6m  = price_n_days_ago(180)
    p1y,  y1y  = price_n_days_ago(365)
    p3y,  y3y  = price_n_days_ago(1095)
    p5y,  y5y  = price_n_days_ago(1825)

    r3m  = (now_price / p3m  - 1) * 100
    r6m  = (now_price / p6m  - 1) * 100
    r1y  = (now_price / p1y  - 1) * 100
    cagr3 = cagr(p3y,  now_price, y3y)
    cagr5 = cagr(p5y,  now_price, y5y)

    # Sharpe (using 3Y CAGR as base)
    base_cagr = cagr3 if cagr3 else (r1y / 100)
    sharpe = (base_cagr - RF_RATE) / vol if vol > 0 else 0

    return {
        "now": now_price,
        "p3m": p3m, "r3m": r3m,
        "p6m": p6m, "r6m": r6m,
        "p1y": p1y, "r1y": r1y,
        "p3y": p3y, "cagr3": cagr3,
        "p5y": p5y, "cagr5": cagr5,
        "volatility": vol,
        "max_drawdown": max_dd,
        "sharpe": sharpe,
    }

def build_scenarios(metrics):
    """Build Bear/Base/Bull annual return rates based on historical CAGR & volatility."""
    vol   = metrics["volatility"]
    # Use 3Y CAGR as base; fall back to 1Y return
    base_ann = metrics["cagr3"] if metrics["cagr3"] is not None else (metrics["r1y"] / 100)

    bear  = max(RF_RATE, base_ann - 1.0 * vol)
    base  = base_ann
    bull  = base_ann + 0.5 * vol

    return {"bear": bear, "base": base, "bull": bull}

def project(principal, annual_rate, years):
    return principal * (1 + annual_rate) ** years

# ── Main ──────────────────────────────────────────────────────────────────────

def estimate(ticker, capital_m=10.0, horizon_years=3):
    ticker = ticker.upper()
    capital = capital_m * 1_000_000  # triệu VND → VND

    print(f"\n⏳ Fetching price history for {ticker} from VNDirect...")
    try:
        prices = fetch_history(ticker, days=1825)
    except Exception as e:
        print(f"❌ VNDirect connection error: {e}")
        print("   Check internet connection and ticker name.")
        return

    if len(prices) < 30:
        print(f"❌ Insufficient data for {ticker} (only {len(prices)} sessions)")
        return

    m = calc_returns(prices)
    sc = build_scenarios(m)

    horizons = [0.5, 1, horizon_years, 5]

    def fmt_price(p):
        return f"{p:,.0f}" if p else "N/A"

    def fmt_r(r):
        if r is None: return "N/A"
        return f"{r*100:+.1f}%"

    def fmt_vnd(v):
        return f"{v/1_000_000:.1f}tr"

    print(f"\n{'='*60}")
    print(f"  📈 Return Estimate — {ticker}")
    print(f"  Investment capital: {capital_m:.0f} million VND | Current price: {fmt_price(m['now'])} VND")
    print(f"{'='*60}")

    print(f"\n  ─── History (actual) ───────────────────────────────")
    print(f"  3 months ago:  {fmt_price(m['p3m'])} VND  │  Return: {m['r3m']:+.1f}%")
    print(f"  6 months ago:  {fmt_price(m['p6m'])} VND  │  Return: {m['r6m']:+.1f}%")
    print(f"  1 year ago:    {fmt_price(m['p1y'])} VND  │  Return: {m['r1y']:+.1f}%")
    if m["cagr3"]:
        print(f"  3 years ago:    {fmt_price(m['p3y'])} VND  │  CAGR:   {m['cagr3']*100:+.1f}%/năm")
    if m["cagr5"]:
        print(f"  5 years ago:    {fmt_price(m['p5y'])} VND  │  CAGR:   {m['cagr5']*100:+.1f}%/năm")
    print(f"  Volatility/năm: {m['volatility']*100:.1f}%")
    print(f"  Max Drawdown:   {m['max_drawdown']*100:.1f}%")
    print(f"  Sharpe Ratio:   {m['sharpe']:.2f}")

    print(f"\n  ─── Scenario forecast (from price {fmt_price(m['now'])} VND) ─────────")
    header = f"  {'':18s}" + "".join(f"  {str(h)+'năm':>9}" if h >= 1 else f"  {'6 tháng':>9}" for h in horizons)
    print(header)
    print(f"  {'-'*65}")

    scenario_labels = [
        ("Bear  (bi quan) ", "bear"),
        ("Base  (trung bình)", "base"),
        ("Bull  (lạc quan)", "bull"),
    ]

    for label, key in scenario_labels:
        rate = sc[key]
        row = f"  {label:<18}"
        for h in horizons:
            ret = (1 + rate) ** h - 1
            row += f"  {ret*100:>+8.1f}%"
        # Append final value for horizon_years
        final_val = project(capital, rate, horizon_years)
        row += f"  → {fmt_vnd(final_val)}"
        print(row)

    # Comparison table
    print(f"\n  ─── Comparison {horizon_years} years (capital {capital_m:.0f}tr VND) ─────────────────")
    bank_val  = project(capital, RF_RATE,          horizon_years)
    base_val  = project(capital, sc["base"],       horizon_years)
    vni_val   = project(capital, VN_INDEX_RETURN,  horizon_years)
    profit_bank = bank_val - capital
    profit_base = base_val - capital
    profit_vni  = vni_val  - capital

    print(f"  Bank deposit 5.5%/year:      +{fmt_vnd(profit_bank):>8}  (tổng: {fmt_vnd(bank_val)})")
    print(f"  {ticker} Base case:           {'+' if profit_base>=0 else ''}{fmt_vnd(profit_base):>8}  (tổng: {fmt_vnd(base_val)})")
    print(f"  VN-Index ~11%/year:            +{fmt_vnd(profit_vni):>8}  (tổng: {fmt_vnd(vni_val)})")

    # Risk assessment
    print(f"\n  ─── Risk assessment ─────────────────────────────────")
    if m["sharpe"] >= 1.0:
        risk_label = "🟢 Good (Sharpe ≥ 1.0) — return justifies the risk"
    elif m["sharpe"] >= 0.5:
        risk_label = "🟡 Acceptable (Sharpe 0.5–1.0)"
    else:
        risk_label = "🔴 High risk (Sharpe < 0.5) — consider carefully"
    print(f"  {risk_label}")

    worst_case = project(capital, sc["bear"], horizon_years)
    worst_loss = worst_case - capital
    print(f"  Worst case ({horizon_years}năm): {fmt_vnd(worst_case)} ({worst_loss/capital*100:+.1f}%)")

    print(f"{'='*60}")
    print(f"  ⚠️  These are estimates, not guaranteed returns. DYOR.")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VN Stock Return Estimator")
    parser.add_argument("ticker",              help="Stock ticker (e.g., FPT, VCB, HPG)")
    parser.add_argument("--capital", "-c", type=float, default=10.0,
                        help="Investment capital (million VND, default: 10)")
    parser.add_argument("--years",   "-y", type=int,   default=3,
                        help="Long-term horizon for comparison (years, default: 3)")
    args = parser.parse_args()
    estimate(args.ticker, args.capital, args.years)
