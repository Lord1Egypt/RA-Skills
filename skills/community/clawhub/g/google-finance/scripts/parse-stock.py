#!/usr/bin/env python3
# SECURITY MANIFEST
# Accessed variables : none (no environment variables read)
# File operations    : READ/WRITE ~/.openclaw/workspace/stock-tracker-state.json only
# Network            : Google Finance (public, unauthenticated)
# External endpoints : https://www.google.com/finance/quote/*
# Credentials        : none handled or stored
# User data leaving machine: none
"""
parse-stock.py — Helper script for the google-finance skill.

Usage:
  python3 parse-stock.py --check                      # Check all watchlist stocks
  python3 parse-stock.py --check --symbol AAPL        # Check single stock
  python3 parse-stock.py --list                       # Show watchlist
  python3 parse-stock.py --add AAPL                   # Add to watchlist
  python3 parse-stock.py --remove TSLA                # Remove from watchlist

This script fetches data from Google Finance (no API key required).
"""

import json
import sys
import argparse
import math
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# State management
# ──────────────────────────────────────────────────────────────────────────────

STATE_PATH = Path.home() / ".openclaw" / "workspace" / "stock-tracker-state.json"

DEFAULT_WATCHLIST = ["NVDA:NASDAQ", "AAPL:NASDAQ", "META:NASDAQ", "GOOGL:NASDAQ"]

def load_state() -> dict:
    if STATE_PATH.exists():
        with open(STATE_PATH) as f:
            return json.load(f)
    return {"watchlist": list(DEFAULT_WATCHLIST), "lastChecked": None, "snapshots": {}}

def save_state(state: dict):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)

def add_symbol(symbol: str):
    symbol = normalize_symbol(symbol)
    state = load_state()
    if symbol not in state["watchlist"]:
        state["watchlist"].append(symbol)
        save_state(state)
        print(f"✅ Added {symbol} to watchlist.")
    else:
        print(f"ℹ️  {symbol} already in watchlist.")

def remove_symbol(symbol: str):
    symbol = normalize_symbol(symbol)
    state = load_state()
    if symbol in state["watchlist"]:
        state["watchlist"].remove(symbol)
        state["snapshots"].pop(symbol, None)
        save_state(state)
        print(f"🗑️  Removed {symbol} from watchlist.")
    else:
        print(f"⚠️  {symbol} not found in watchlist.")

def list_watchlist():
    state = load_state()
    if not state["watchlist"]:
        print("📋 Watchlist is empty. Use --add SYMBOL to add stocks.")
    else:
        print("📋 Current watchlist:")
        for sym in state["watchlist"]:
            snap = state["snapshots"].get(sym)
            if snap:
                ts = snap.get("ts", "never")[:19]
                price = snap.get("price", "?")
                change = snap.get("change_pct", 0)
                print(f"  • {sym:<20} ${price:<10} {change:+.2f}%  (last: {ts})")
            else:
                print(f"  • {sym:<20} (no data yet)")

def update_snapshot(symbol: str, price: float, change_pct: float, extra: dict = None):
    symbol = normalize_symbol(symbol)
    state = load_state()
    state["lastChecked"] = datetime.now(timezone.utc).isoformat()
    state["snapshots"][symbol] = {
        "price": price,
        "change_pct": change_pct,
        "ts": datetime.now(timezone.utc).isoformat(),
        **(extra or {}),
    }
    save_state(state)

def normalize_symbol(symbol: str) -> str:
    """Normalize symbol format: AAPL -> AAPL:NASDAQ, AAPL:NASDAQ -> AAPL:NASDAQ"""
    symbol = symbol.upper().strip()
    if ":" not in symbol:
        # Default exchange mapping
        defaults = {
            "NVDA": "NASDAQ", "AAPL": "NASDAQ", "META": "NASDAQ", "GOOGL": "NASDAQ",
            "MSFT": "NASDAQ", "AMZN": "NASDAQ", "TSLA": "NASDAQ", "AMD": "NASDAQ",
            "INTC": "NASDAQ", "NFLX": "NASDAQ", "GOOG": "NASDAQ", "AVGO": "NASDAQ",
            "JPM": "NYSE", "V": "NYSE", "JNJ": "NYSE", "WMT": "NYSE", "BAC": "NYSE",
        }
        exchange = defaults.get(symbol, "NASDAQ")
        return f"{symbol}:{exchange}"
    return symbol

def get_ticker(symbol: str) -> str:
    """Extract ticker from symbol (AAPL:NASDAQ -> AAPL)"""
    return symbol.split(":")[0].upper()

def get_exchange(symbol: str) -> str:
    """Extract exchange from symbol (AAPL:NASDAQ -> NASDAQ)"""
    parts = symbol.split(":")
    return parts[1].upper() if len(parts) > 1 else "NASDAQ"

# ──────────────────────────────────────────────────────────────────────────────
# Google Finance Data Fetching
# ──────────────────────────────────────────────────────────────────────────────

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

def parse_volume(s: str) -> float:
    """Parse volume string like '51.56M' or '1.2B' to number."""
    if not s:
        return 0
    s = s.replace(',', '').strip().upper()
    multiplier = 1
    if s.endswith('T'):
        multiplier = 1_000_000_000_000
        s = s[:-1]
    elif s.endswith('B'):
        multiplier = 1_000_000_000
        s = s[:-1]
    elif s.endswith('M'):
        multiplier = 1_000_000
        s = s[:-1]
    elif s.endswith('K'):
        multiplier = 1_000
        s = s[:-1]
    try:
        return float(s) * multiplier
    except ValueError:
        return 0

def parse_price(s: str) -> float:
    """Parse price string like '$257.46' to float."""
    if not s:
        return 0
    s = s.replace('$', '').replace(',', '').strip()
    try:
        return float(s)
    except ValueError:
        return 0

def fetch_google_finance(symbol: str) -> dict:
    """Fetch stock data from Google Finance. Returns dict with price, change, etc."""
    ticker = get_ticker(symbol)
    exchange = get_exchange(symbol)
    
    # Google Finance URL
    url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
    
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8')
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        return {"error": f"Failed to fetch {ticker}: {e}"}
    except Exception as e:
        return {"error": f"Error fetching {ticker}: {e}"}
    
    result = {
        "symbol": symbol,
        "ticker": ticker,
        "exchange": exchange,
        "currency": "USD",
    }
    
    # Extract price from data-last-price attribute
    price_match = re.search(r'data-last-price="([0-9.]+)"', html)
    if not price_match:
        return {"error": f"Could not parse price for {ticker}"}
    result["price"] = float(price_match.group(1))
    
    # Extract stats from the stats table (mfs7Fc = label, P6K39c = value)
    stats_pattern = r'<div class="mfs7Fc"[^>]*>([^<]+)</div>.*?<div class="P6K39c"[^>]*>([^<]+)'
    stats = re.findall(stats_pattern, html, re.DOTALL)
    
    stats_dict = {}
    for label, value in stats:
        label = label.strip().lower()
        value = value.strip()
        stats_dict[label] = value
    
    # Previous close
    if "previous close" in stats_dict:
        prev_close = parse_price(stats_dict["previous close"])
        result["prev_close"] = prev_close
        if prev_close > 0:
            change = result["price"] - prev_close
            change_pct = (change / prev_close) * 100
            result["change"] = round(change, 2)
            result["change_pct"] = round(change_pct, 2)
    
    # Day range
    if "day range" in stats_dict:
        day_range = stats_dict["day range"]
        parts = day_range.replace('$', '').split('-')
        if len(parts) == 2:
            result["day_low"] = parse_price(parts[0])
            result["day_high"] = parse_price(parts[1])
    
    # Year (52-week) range
    if "year range" in stats_dict:
        year_range = stats_dict["year range"]
        parts = year_range.replace('$', '').split('-')
        if len(parts) == 2:
            result["week52_low"] = parse_price(parts[0])
            result["week52_high"] = parse_price(parts[1])
    
    # Market cap
    if "market cap" in stats_dict:
        cap_str = stats_dict["market cap"].split()[0]  # "3.79T USD" -> "3.79T"
        result["market_cap"] = parse_volume(cap_str)
    
    # Average volume
    if "avg volume" in stats_dict:
        result["avg_volume"] = parse_volume(stats_dict["avg volume"])
    
    # P/E ratio
    if "p/e ratio" in stats_dict:
        try:
            result["pe"] = float(stats_dict["p/e ratio"].replace(',', ''))
        except ValueError:
            pass
    
    # Dividend yield
    if "dividend yield" in stats_dict:
        div_str = stats_dict["dividend yield"].replace('%', '')
        try:
            result["dividend_yield"] = float(div_str)
        except ValueError:
            pass
    
    # Company name from page title or zzDege class
    name_match = re.search(r'<div class="zzDege"[^>]*>([^<]+)', html)
    if name_match:
        result["company_name"] = name_match.group(1).strip()
    else:
        # Fallback to title
        title_match = re.search(r'<title>([^(]+)', html)
        if title_match:
            result["company_name"] = title_match.group(1).strip()
        else:
            result["company_name"] = ticker
    
    # Default change_pct if not calculated
    if "change_pct" not in result:
        result["change_pct"] = 0
        result["change"] = 0
    
    # Sector (default to technology for common tech stocks)
    tech_stocks = {"AAPL", "MSFT", "GOOGL", "GOOG", "META", "NVDA", "AMD", "INTC", "AVGO", "TSLA", "AMZN", "NFLX"}
    if ticker in tech_stocks:
        result["sector"] = "technology"
    else:
        result["sector"] = "unknown"
    
    result["headlines"] = []  # Headlines would require separate Google News fetch
    
    return result

# ──────────────────────────────────────────────────────────────────────────────
# Scoring engine
# ──────────────────────────────────────────────────────────────────────────────

SECTOR_PE = {
    "technology": 28, "consumer discretionary": 24, "healthcare": 20,
    "financials": 14, "energy": 12, "utilities": 16, "industrials": 20,
}

def week52_position(price: float, low: float, high: float) -> float:
    if high <= low:
        return 0.5
    return (price - low) / (high - low)

def score_momentum(change_pct: float, position_52w: float) -> tuple:
    reasons = []
    score = 0

    if change_pct > 3:
        score += 2; reasons.append(f"✅ Strong daily gain (+{change_pct:.1f}%)")
    elif change_pct > 1:
        score += 1; reasons.append(f"✅ Positive daily change (+{change_pct:.1f}%)")
    elif change_pct < -3:
        score -= 2; reasons.append(f"❌ Sharp daily drop ({change_pct:.1f}%)")
    elif change_pct < -1:
        score -= 1; reasons.append(f"❌ Negative daily change ({change_pct:.1f}%)")
    else:
        reasons.append(f"→ Flat day ({change_pct:+.1f}%)")

    if position_52w is not None:
        if position_52w > 0.90:
            score -= 1; reasons.append(f"⚠️  Near 52-week high ({position_52w*100:.0f}%) — overbought")
        elif position_52w > 0.75:
            score += 1; reasons.append(f"✅ In upper 25% of 52-week range ({position_52w*100:.0f}%)")
        elif position_52w < 0.10:
            score += 1; reasons.append(f"✅ Near 52-week low ({position_52w*100:.0f}%) — oversold")
        elif position_52w < 0.25:
            score -= 1; reasons.append(f"⚠️  In lower 25% of 52-week range ({position_52w*100:.0f}%)")

    return score, reasons

def score_volume(current_vol: float, avg_vol: float, change_pct: float) -> tuple:
    if avg_vol <= 0 or current_vol <= 0:
        return 0, []
    ratio = current_vol / avg_vol
    score = 0
    reasons = []
    up = change_pct >= 0

    if ratio > 2.0:
        score = 2 if up else -2
        reasons.append(f"{'✅' if up else '❌'} Volume {ratio:.1f}× avg ({'buying' if up else 'selling'})")
    elif ratio > 1.5:
        score = 1 if up else -1
        reasons.append(f"{'✅' if up else '❌'} Volume {ratio:.1f}× avg, price {'up' if up else 'down'}")
    elif ratio < 0.5:
        score = -1; reasons.append(f"⚠️  Low volume {ratio:.1f}× avg")
    else:
        reasons.append(f"→ Normal volume ({ratio:.1f}× avg)")

    return score, reasons

def score_valuation(pe: float, sector: str = "technology") -> tuple:
    if pe is None:
        return 0, []
    benchmark = SECTOR_PE.get(sector.lower(), 22)
    reasons = []
    score = 0

    if pe < 0:
        score = -1; reasons.append(f"⚠️  Negative P/E (losses)")
    else:
        ratio = pe / benchmark
        if ratio < 0.7:
            score = 2; reasons.append(f"✅ P/E {pe:.1f}× — undervalued vs sector ({benchmark}×)")
        elif ratio < 1.0:
            score = 1; reasons.append(f"✅ P/E {pe:.1f}× — below sector avg ({benchmark}×)")
        elif ratio < 1.5:
            reasons.append(f"→ P/E {pe:.1f}× — inline with sector ({benchmark}×)")
        elif ratio < 2.0:
            score = -1; reasons.append(f"⚠️  P/E {pe:.1f}× — elevated vs sector ({benchmark}×)")
        else:
            score = -2; reasons.append(f"❌ P/E {pe:.1f}× — very high vs sector ({benchmark}×)")

    return score, reasons

def score_news(headlines: list) -> tuple:
    if not headlines:
        return 0, []
    
    pos_kw = ["beat", "record", "growth", "partnership", "buyback", "dividend", "approved", "launched", "upgrade"]
    neg_kw = ["miss", "layoffs", "recall", "investigation", "sec", "lawsuit", "fine", "downgrade", "loss", "bankruptcy"]
    
    combined = " ".join(h.lower() for h in headlines)
    pos = sum(1 for kw in pos_kw if kw in combined)
    neg = sum(1 for kw in neg_kw if kw in combined)
    
    raw = pos * 0.5 - neg * 0.5
    score = max(-3, min(3, int(math.ceil(raw))))
    
    reasons = []
    if pos or neg:
        reasons.append(f"→ News: {pos} positive / {neg} negative keywords")
    
    return score, reasons

def compute_signal(total: int) -> tuple:
    if total >= 4:
        signal = "🟢 BUY"
    elif total <= -4:
        signal = "🔴 SELL"
    else:
        signal = "🟡 HOLD"

    abs_t = abs(total)
    if abs_t >= 7:
        confidence = "HIGH"
    elif abs_t >= 4:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    return signal, confidence

# ──────────────────────────────────────────────────────────────────────────────
# Report formatter
# ──────────────────────────────────────────────────────────────────────────────

def build_report(symbol: str, data: dict) -> str:
    price = data.get("price", 0.0)
    change_pct = data.get("change_pct", 0.0)
    avg_volume = data.get("avg_volume", 0)
    pe = data.get("pe")
    week52_high = data.get("week52_high")
    week52_low = data.get("week52_low")
    company_name = data.get("company_name", symbol)
    sector = data.get("sector", "technology")
    headlines = data.get("headlines", [])

    pos52 = None
    if week52_high and week52_low:
        pos52 = week52_position(price, week52_low, week52_high)

    m_score, m_reasons = score_momentum(change_pct, pos52)
    v_score, v_reasons = score_volume(avg_volume, avg_volume, change_pct)  # Using avg as proxy
    val_score, val_reasons = score_valuation(pe, sector)
    n_score, n_reasons = score_news(headlines)

    total = max(-10, min(10, m_score + v_score + val_score + n_score))
    signal, confidence = compute_signal(total)

    lines = [
        "─" * 54,
        f"📈 {symbol} ({company_name})",
        "─" * 54,
        f"Price:        ${price:,.2f}   ({change_pct:+.1f}% today)",
    ]

    if week52_high and week52_low:
        lines.append(f"52-week:      ${week52_low:,.2f} – ${week52_high:,.2f}  (position: {(pos52 or 0)*100:.0f}%)")
    
    if avg_volume > 0:
        vol_str = f"{avg_volume/1e6:.1f}M" if avg_volume >= 1e6 else f"{avg_volume/1e3:.0f}K"
        lines.append(f"Avg Volume:   {vol_str}")

    lines += [
        "",
        "Scoring:",
        f"  Momentum    {m_score:+d}",
        f"  Volume      {v_score:+d}",
        f"  Valuation   {val_score:+d}",
        f"  News        {n_score:+d}",
        "  " + "─" * 16,
        f"  Total       {total:+d}  →  {signal}  [Confidence: {confidence}]",
        "",
        "Factors:",
    ]
    for r in m_reasons + v_reasons + val_reasons + n_reasons:
        lines.append(f"  {r}")

    if headlines:
        lines += ["", "Headlines:"]
        for h in headlines[:5]:
            lines.append(f"  • {h}")

    lines += ["", "Recommendation:"]
    if "BUY" in signal:
        sl = price * 0.95
        t1 = price * 1.08
        lines.append(f"  Consider buying. Stop-loss: ${sl:,.2f} | Target: ${t1:,.2f}")
    elif "SELL" in signal:
        cover = price * 0.92
        lines.append(f"  Consider reducing position. Cover target: ${cover:,.2f}")
    else:
        lines.append("  Hold current position. Wait for stronger signal.")

    lines += [
        "",
        "─" * 54,
        "⚠️  Not financial advice. Data from Google Finance.",
        "─" * 54,
    ]
    return "\n".join(lines)

def build_summary(results: list) -> str:
    """Build a compact summary for multiple stocks."""
    lines = [
        "═" * 54,
        "📊 STOCK TRACKER SUMMARY",
        f"   {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "═" * 54,
        "",
    ]
    
    # Sort by signal: BUY first, then HOLD, then SELL
    def signal_order(r):
        if "BUY" in r.get("signal", ""): return 0
        if "SELL" in r.get("signal", ""): return 2
        return 1
    
    results.sort(key=signal_order)
    
    for r in results:
        if "error" in r:
            lines.append(f"❌ {r['symbol']}: {r['error']}")
            continue
        
        symbol = r.get("symbol", "?")
        price = r.get("price", 0)
        change = r.get("change_pct", 0)
        signal = r.get("signal", "?")
        score = r.get("score", 0)
        
        change_icon = "🔺" if change > 0 else "🔻" if change < 0 else "➖"
        lines.append(f"{signal}  {symbol:<15} ${price:>8.2f}  {change_icon} {change:+.2f}%  [score: {score:+d}]")
    
    lines += [
        "",
        "═" * 54,
        "⚠️  Not financial advice. Data from Google Finance.",
        "═" * 54,
    ]
    
    return "\n".join(lines)

# ──────────────────────────────────────────────────────────────────────────────
# Main check function
# ──────────────────────────────────────────────────────────────────────────────

def check_stocks(symbols: list = None, verbose: bool = True) -> list:
    """Check stocks and return results. If symbols is None, check all in watchlist."""
    state = load_state()
    
    if symbols is None:
        symbols = state["watchlist"]
    
    results = []
    
    for symbol in symbols:
        symbol = normalize_symbol(symbol)
        print(f"⏳ Fetching {symbol} from Google Finance...", file=sys.stderr)
        
        data = fetch_google_finance(symbol)
        
        if "error" in data:
            results.append({"symbol": symbol, "error": data["error"]})
            continue
        
        # Calculate scores
        pos52 = None
        if data.get("week52_high") and data.get("week52_low"):
            pos52 = week52_position(data["price"], data["week52_low"], data["week52_high"])
        
        m_score, _ = score_momentum(data.get("change_pct", 0), pos52)
        v_score, _ = score_volume(data.get("avg_volume", 0), data.get("avg_volume", 0), data.get("change_pct", 0))
        val_score, _ = score_valuation(data.get("pe"), data.get("sector", "technology"))
        n_score, _ = score_news(data.get("headlines", []))
        
        total = max(-10, min(10, m_score + v_score + val_score + n_score))
        signal, confidence = compute_signal(total)
        
        # Update state
        update_snapshot(symbol, data["price"], data.get("change_pct", 0))
        
        result = {
            "symbol": symbol,
            "price": data["price"],
            "change_pct": data.get("change_pct", 0),
            "signal": signal,
            "confidence": confidence,
            "score": total,
            "data": data,
        }
        results.append(result)
        
        if verbose:
            print(build_report(symbol, data))
            print()
    
    return results

# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Stock Tracker - fetch and analyze stocks from Google Finance")
    parser.add_argument("--check", action="store_true", help="Check stocks (fetches data automatically)")
    parser.add_argument("--symbol", type=str, help="Symbol to check (e.g. AAPL or AAPL:NASDAQ)")
    parser.add_argument("--add", type=str, help="Add symbol to watchlist")
    parser.add_argument("--remove", type=str, help="Remove symbol from watchlist")
    parser.add_argument("--list", action="store_true", help="List watchlist")
    parser.add_argument("--summary", action="store_true", help="Output compact summary instead of full reports")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--update-state", action="store_true", help="Update state only")
    parser.add_argument("--price", type=float, help="Price for --update-state")
    parser.add_argument("--change", type=float, help="Change percent for --update-state")
    args = parser.parse_args()

    if args.add:
        add_symbol(args.add)
    elif args.remove:
        remove_symbol(args.remove)
    elif args.list:
        list_watchlist()
    elif args.update_state and args.symbol and args.price is not None:
        update_snapshot(args.symbol, args.price, args.change or 0.0)
        print(f"✅ Snapshot updated for {args.symbol}")
    elif args.check:
        # Main check mode - fetches data automatically from Google Finance
        symbols = [args.symbol] if args.symbol else None
        results = check_stocks(symbols, verbose=not args.summary)
        
        if args.summary:
            print(build_summary(results))
        
        if args.json:
            # Remove 'data' key for cleaner JSON output
            for r in results:
                r.pop("data", None)
            print(json.dumps(results, indent=2))
    else:
        # Default: show help
        parser.print_help()

if __name__ == "__main__":
    main()
