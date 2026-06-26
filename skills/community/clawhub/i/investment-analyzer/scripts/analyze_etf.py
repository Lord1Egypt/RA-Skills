#!/usr/bin/env python3
import argparse
import json
import sys
from datetime import datetime, timedelta

try:
    import yfinance as yf
except ImportError:
    print(json.dumps({"success": False, "error": "yfinance not installed. Run: pip install yfinance"}))
    sys.exit(1)

CURRENT_HOLDINGS = ["TEC.TO"]
MER_THRESHOLD = 0.0035
MER_REJECT = 0.0075
RETURN_BENCHMARK = 0.10
OVERLAP_FLAG_THRESHOLD = 0.40


def get_top_holdings(ticker_obj):
    try:
        info = ticker_obj.info
        holdings = []
        for i in range(1, 11):
            key = f"holding{i}"
            if key in info:
                holdings.append(info[key])
        return holdings
    except Exception:
        return []


def calc_cagr(hist, years):
    if hist is None or len(hist) < 2:
        return None
    try:
        end_price = hist["Close"].iloc[-1]
        start_price = hist["Close"].iloc[0]
        if start_price <= 0:
            return None
        return (end_price / start_price) ** (1 / years) - 1
    except Exception:
        return None


def analyze(ticker_symbol):
    t = yf.Ticker(ticker_symbol)
    info = t.info

    name = info.get("longName") or info.get("shortName", ticker_symbol)
    mer = info.get("annualReportExpenseRatio") or info.get("expenseRatio")
    currency = info.get("currency", "CAD")
    category = info.get("category", "N/A")
    fund_family = info.get("fundFamily", "N/A")

    now = datetime.now()
    hist_5y = t.history(start=(now - timedelta(days=365 * 5)).strftime("%Y-%m-%d"))
    hist_10y = t.history(start=(now - timedelta(days=365 * 10)).strftime("%Y-%m-%d"))
    hist_3y = t.history(start=(now - timedelta(days=365 * 3)).strftime("%Y-%m-%d"))

    cagr_3y = calc_cagr(hist_3y, 3)
    cagr_5y = calc_cagr(hist_5y, 5)
    cagr_10y = calc_cagr(hist_10y, 10)

    current_holdings_data = {}
    for h in CURRENT_HOLDINGS:
        ht = yf.Ticker(h)
        current_holdings_data[h] = get_top_holdings(ht)

    new_holdings = get_top_holdings(t)
    overlap_counts = {}
    for held, held_list in current_holdings_data.items():
        if not held_list or not new_holdings:
            overlap_counts[held] = None
            continue
        overlap = len(set(new_holdings) & set(held_list)) / max(len(new_holdings), 1)
        overlap_counts[held] = round(overlap, 2)

    thresholds = {}
    if mer is not None:
        thresholds["mer_ok"] = bool(mer <= MER_THRESHOLD)
        thresholds["mer_not_rejected"] = bool(mer < MER_REJECT)
    thresholds["return_3y_ok"] = bool(cagr_3y is not None and cagr_3y >= RETURN_BENCHMARK)
    thresholds["return_5y_ok"] = bool(cagr_5y is not None and cagr_5y >= RETURN_BENCHMARK)
    high_overlap = any(v is not None and v > OVERLAP_FLAG_THRESHOLD for v in overlap_counts.values())
    thresholds["low_overlap"] = bool(not high_overlap)

    passed = sum(1 for v in thresholds.values() if v)
    total = len(thresholds)

    diversification_note = ""
    if ticker_symbol.upper() == "TEC.TO" or high_overlap:
        diversification_note = "⚠️ High overlap with existing TEC.TO — does NOT improve diversification."
    else:
        diversification_note = "✅ Adds diversification beyond current tech concentration."

    if passed >= total - 1 and thresholds.get("mer_not_rejected", True):
        verdict = "✅ ADD"
        reason = "Meets return and cost thresholds and improves portfolio diversification."
    elif passed >= total // 2 and thresholds.get("mer_not_rejected", True):
        verdict = "⚠️ INVESTIGATE"
        reason = "Partially meets thresholds. Review MER, returns, and overlap carefully."
    else:
        verdict = "❌ SKIP"
        reason = "Does not meet minimum ETF criteria (high MER, poor returns, or too much overlap)."

    return {
        "success": True,
        "ticker": ticker_symbol.upper(),
        "name": name,
        "currency": currency,
        "category": category,
        "fund_family": fund_family,
        "metrics": {
            "MER_pct": round(float(mer) * 100, 3) if mer else "N/A",
            "CAGR_3y_pct": round(float(cagr_3y) * 100, 2) if cagr_3y is not None else "N/A",
            "CAGR_5y_pct": round(float(cagr_5y) * 100, 2) if cagr_5y is not None else "N/A",
            "CAGR_10y_pct": round(float(cagr_10y) * 100, 2) if cagr_10y is not None else "N/A",
        },
        "overlap_with_current_holdings": overlap_counts,
        "diversification_note": diversification_note,
        "thresholds": thresholds,
        "conclusion": {"verdict": verdict, "reason": reason},
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze an ETF for investment.")
    parser.add_argument("ticker", help="ETF ticker symbol (e.g. XEQT.TO, VFV.TO)")
    args = parser.parse_args()
    result = analyze(args.ticker)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

