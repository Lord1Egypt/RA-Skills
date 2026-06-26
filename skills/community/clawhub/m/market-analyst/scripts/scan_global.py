#!/usr/bin/env python3
"""
Global Market Scanner — scan US, crypto, forex, commodities via TradingView
Usage:
  python3 scan_global.py --market us [--rsi 40] [--limit 20]
  python3 scan_global.py --market crypto [--rsi 40]
  python3 scan_global.py --market forex
  python3 scan_global.py --market commodities
  python3 scan_global.py --market all [--rsi 40]
"""
import urllib.request, json, sys, argparse

# TradingView scanner endpoints & configs per market
MARKET_CONFIGS = {
    "us": {
        "url": "https://scanner.tradingview.com/america/scan",
        "label": "🇺🇸 US Equities",
        "filters": [
            {"left": "exchange", "operation": "in_range", "right": ["NASDAQ", "NYSE", "AMEX"]},
            {"left": "market_cap_basic", "operation": "greater", "right": 10_000_000_000},  # >$10B
        ],
        "columns": ["name", "close", "change", "volume", "RSI", "EMA20", "EMA50", "EMA200",
                    "MACD.macd", "MACD.signal", "BB.lower", "price_52_week_high", "price_52_week_low",
                    "market_cap_basic", "price_earnings_ttm"],
        "volume_min": 1_000_000,
        "currency": "USD",
    },
    "nasdaq": {
        "url": "https://scanner.tradingview.com/america/scan",
        "label": "🇺🇸 NASDAQ",
        "filters": [
            {"left": "exchange", "operation": "equal", "right": "NASDAQ"},
            {"left": "market_cap_basic", "operation": "greater", "right": 5_000_000_000},
        ],
        "columns": ["name", "close", "change", "volume", "RSI", "EMA20", "EMA50", "EMA200",
                    "MACD.macd", "MACD.signal", "BB.lower", "price_52_week_high", "price_52_week_low",
                    "market_cap_basic", "price_earnings_ttm"],
        "volume_min": 500_000,
        "currency": "USD",
    },
    "nyse": {
        "url": "https://scanner.tradingview.com/america/scan",
        "label": "🇺🇸 NYSE",
        "filters": [
            {"left": "exchange", "operation": "equal", "right": "NYSE"},
            {"left": "market_cap_basic", "operation": "greater", "right": 5_000_000_000},
        ],
        "columns": ["name", "close", "change", "volume", "RSI", "EMA20", "EMA50", "EMA200",
                    "MACD.macd", "MACD.signal", "BB.lower", "price_52_week_high", "price_52_week_low",
                    "market_cap_basic", "price_earnings_ttm"],
        "volume_min": 500_000,
        "currency": "USD",
    },
    "crypto": {
        "url": "https://scanner.tradingview.com/crypto/scan",
        "label": "🪙 Crypto",
        "filters": [
            {"left": "exchange", "operation": "in_range", "right": ["BINANCE", "COINBASE", "BYBIT"]},
            {"left": "volume", "operation": "greater", "right": 10_000_000},
        ],
        "columns": ["name", "close", "change", "volume", "RSI", "EMA20", "EMA50", "EMA200",
                    "MACD.macd", "MACD.signal", "BB.lower", "price_52_week_high", "price_52_week_low"],
        "volume_min": 0,
        "currency": "USD",
    },
    "forex": {
        "url": "https://scanner.tradingview.com/forex/scan",
        "label": "💱 Forex",
        "filters": [
            {"left": "name", "operation": "in_range",
             "right": ["EURUSD", "USDJPY", "GBPUSD", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD",
                       "EURGBP", "EURJPY", "GBPJPY", "AUDJPY", "USDVND"]},
        ],
        "columns": ["name", "close", "change", "RSI", "EMA20", "EMA50", "EMA200",
                    "MACD.macd", "MACD.signal", "BB.lower", "BB.upper",
                    "price_52_week_high", "price_52_week_low"],
        "volume_min": 0,
        "currency": "",
    },
    "commodities": {
        "url": "https://scanner.tradingview.com/cfd/scan",
        "label": "🏆 Commodities",
        "filters": [
            {"left": "name", "operation": "in_range",
             "right": ["XAUUSD", "XAGUSD", "USOIL", "UKOIL", "NGAS", "COPPER"]},
        ],
        "columns": ["name", "close", "change", "RSI", "EMA20", "EMA50", "EMA200",
                    "MACD.macd", "MACD.signal", "BB.lower", "BB.upper",
                    "price_52_week_high", "price_52_week_low"],
        "volume_min": 0,
        "currency": "USD",
    },
}


def scan_market(market, rsi_threshold=None, limit=20):
    """Scan a specific market via TradingView scanner."""
    if market not in MARKET_CONFIGS:
        print(f"❌ Market '{market}' không hợp lệ. Chọn: {', '.join(MARKET_CONFIGS.keys())}")
        return []

    config = MARKET_CONFIGS[market]
    filters = list(config["filters"])

    # Add RSI filter if specified
    if rsi_threshold:
        filters.append({"left": "RSI", "operation": "less", "right": rsi_threshold})

    # Add volume filter
    if config["volume_min"] > 0:
        filters.append({"left": "volume", "operation": "greater", "right": config["volume_min"]})

    payload = {
        "filter": filters,
        "columns": config["columns"],
        "sort": {"sortBy": "RSI" if rsi_threshold else "volume", "sortOrder": "asc" if rsi_threshold else "desc"},
        "range": [0, limit],
    }

    # Forex/commodities use symbols instead of filter
    if market in ("forex", "commodities"):
        symbols_list = config["filters"][0]["right"]
        # Forex: dùng FX_IDC prefix, commodities: dùng TVC
        if market == "forex":
            tickers = [f"FX_IDC:{s}" for s in symbols_list]
        else:
            tickers = [f"TVC:{s}" for s in symbols_list]
        payload = {
            "symbols": {"tickers": tickers},
            "columns": config["columns"],
        }

    req = urllib.request.Request(
        config["url"],
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
    except Exception as e:
        print(f"⚠️ Connection error {config['label']}: {e}")
        return []

    results = []
    is_equity = market in ("us", "nasdaq", "nyse", "crypto")

    for item in data.get("data", []):
        sym = item["s"].split(":")[-1]
        d = item["d"]

        if is_equity:
            # Equities/crypto have volume column
            name, close, chg, vol = d[0], d[1], d[2], d[3]
            rsi, ema20, ema50, ema200 = d[4], d[5], d[6], d[7]
            macd, macd_sig = d[8], d[9]
            bb_low = d[10]
            h52, l52 = d[11], d[12]
            mcap = d[13] if len(d) > 13 else None
            pe = d[14] if len(d) > 14 else None
        else:
            # Forex/commodities have no volume
            name, close, chg = d[0], d[1], d[2]
            vol = None
            rsi, ema20, ema50, ema200 = d[3], d[4], d[5], d[6]
            macd, macd_sig = d[7], d[8]
            bb_low = d[9]
            h52, l52 = d[11], d[12]
            mcap, pe = None, None

        if close is None:
            continue

        # Scoring
        score = 0
        signals = []

        if rsi is not None:
            if rsi < 30:
                score += 3; signals.append("RSI extreme oversold")
            elif rsi < 40:
                score += 2; signals.append(f"RSI oversold ({rsi:.1f})")
            elif rsi > 70:
                signals.append(f"⚠️ Overbought ({rsi:.1f})")

        if close and ema200 and close > ema200:
            score += 2; signals.append("Above EMA200 ✓")
        elif close and ema200:
            signals.append("Below EMA200 ✗")

        if macd is not None and macd_sig is not None and macd > macd_sig:
            score += 1; signals.append("MACD bullish")

        if close and bb_low and close <= bb_low * 1.02:
            score += 2; signals.append("Near BB Lower")

        pos52 = ((close - l52) / (h52 - l52) * 100) if (h52 and l52 and h52 != l52) else None
        if pos52 is not None and pos52 < 20:
            score += 2; signals.append(f"Near 52W low ({pos52:.0f}%)")

        results.append({
            "symbol": sym, "name": name, "close": close, "change": chg,
            "volume": vol, "rsi": rsi, "ema200": ema200, "score": score,
            "signals": signals, "pos52": pos52, "mcap": mcap, "pe": pe,
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    # Print results
    print(f"\n{'='*95}")
    print(f"  {config['label']} Scanner {'| RSI < ' + str(rsi_threshold) if rsi_threshold else ''}")
    print(f"{'='*95}")

    if is_equity:
        print(f"{'Mã':<10} {'Giá':>10} {'%':>7} {'RSI':>6} {'Score':>6} {'Vol(M)':>8} {'P/E':>7}  Signals")
        print("-" * 95)
        for r in results:
            vol_m = f"{r['volume']/1e6:.1f}" if r['volume'] else "N/A"
            pe_str = f"{r['pe']:.1f}" if r['pe'] else "N/A"
            signals_str = ", ".join(r['signals'][:3])
            print(f"{r['symbol']:<10} {r['close']:>10,.2f} {r['change']:>+6.2f}% {r['rsi'] or 0:>6.1f} {r['score']:>6}  {vol_m:>6}M {pe_str:>7}  {signals_str}")
    else:
        print(f"{'Mã':<12} {'Giá':>12} {'%':>7} {'RSI':>6} {'Score':>6}  Signals")
        print("-" * 95)
        for r in results:
            signals_str = ", ".join(r['signals'][:3])
            rsi_val = f"{r['rsi']:.1f}" if r['rsi'] else "N/A"
            print(f"{r['symbol']:<12} {r['close']:>12,.4f} {r['change']:>+6.2f}% {rsi_val:>6} {r['score']:>6}  {signals_str}")

    print(f"\nTotal: {len(results)} results")
    return results


def scan_all(rsi_threshold=None, limit=10):
    """Scan all markets."""
    all_results = {}
    for market in ["us", "crypto", "forex", "commodities"]:
        all_results[market] = scan_market(market, rsi_threshold, limit)
    return all_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Global Market Scanner — TradingView")
    parser.add_argument("--market", default="us",
                       help="Market: us, nasdaq, nyse, crypto, forex, commodities, all (default: us)")
    parser.add_argument("--rsi", type=float, default=None, help="RSI threshold (VD: 40)")
    parser.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")
    args = parser.parse_args()

    if args.market == "all":
        scan_all(args.rsi, args.limit)
    else:
        scan_market(args.market, args.rsi, args.limit)
