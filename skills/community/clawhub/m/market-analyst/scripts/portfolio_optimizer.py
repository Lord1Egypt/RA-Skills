#!/usr/bin/env python3
"""
Portfolio Optimizer — Analyze existing portfolio → recommend optimal rebalance.

Fetch real-time data from TradingView, compute Markowitz Mean-Variance optimization.

Usage:
  python3 portfolio_optimizer.py --portfolio "MBB:30,FPT:25,GOLD:20,BNB:15,CASH:10" --capital 500000000 --risk balanced
  python3 portfolio_optimizer.py --portfolio "VCB:40,HPG:30,TCB:30" --capital 200000000 --risk conservative
  python3 portfolio_optimizer.py --portfolio "AAPL:25,NVDA:25,VOO:25,XAUUSD:25" --capital 1000000000 --risk aggressive
"""

import urllib.request, json, sys, argparse, math
from datetime import datetime

# ── Asset mapping: ticker → TradingView endpoint + symbol ──

ASSET_MAP = {
    # VN Stocks
    "MBB": ("vietnam", "HOSE:MBB"), "FPT": ("vietnam", "HOSE:FPT"),
    "VCB": ("vietnam", "HOSE:VCB"), "TCB": ("vietnam", "HOSE:TCB"),
    "HPG": ("vietnam", "HOSE:HPG"), "VNM": ("vietnam", "HOSE:VNM"),
    "MSN": ("vietnam", "HOSE:MSN"), "VIC": ("vietnam", "HOSE:VIC"),
    "VHM": ("vietnam", "HOSE:VHM"), "ACB": ("vietnam", "HOSE:ACB"),
    "STB": ("vietnam", "HOSE:STB"), "SSI": ("vietnam", "HOSE:SSI"),
    "GAS": ("vietnam", "HOSE:GAS"), "PVS": ("vietnam", "HOSE:PVS"),
    "MCH": ("vietnam", "HOSE:MCH"), "REE": ("vietnam", "HOSE:REE"),
    "PNJ": ("vietnam", "HOSE:PNJ"), "DGC": ("vietnam", "HOSE:DGC"),
    "VRE": ("vietnam", "HOSE:VRE"), "CTG": ("vietnam", "HOSE:CTG"),
    "BID": ("vietnam", "HOSE:BID"), "SHB": ("vietnam", "HNX:SHB"),
    # US Stocks
    "AAPL": ("america", "NASDAQ:AAPL"), "NVDA": ("america", "NASDAQ:NVDA"),
    "MSFT": ("america", "NASDAQ:MSFT"), "GOOG": ("america", "NASDAQ:GOOG"),
    "GOOGL": ("america", "NASDAQ:GOOGL"), "META": ("america", "NASDAQ:META"),
    "AMZN": ("america", "NASDAQ:AMZN"), "TSLA": ("america", "NASDAQ:TSLA"),
    "AMD": ("america", "NASDAQ:AMD"), "NFLX": ("america", "NASDAQ:NFLX"),
    "JPM": ("america", "NYSE:JPM"), "V": ("america", "NYSE:V"),
    "JNJ": ("america", "NYSE:JNJ"), "WMT": ("america", "NYSE:WMT"),
    "LLY": ("america", "NYSE:LLY"), "UNH": ("america", "NYSE:UNH"),
    # US ETFs
    "VOO": ("america", "AMEX:VOO"), "SPY": ("america", "AMEX:SPY"),
    "QQQ": ("america", "NASDAQ:QQQ"), "VTI": ("america", "AMEX:VTI"),
    "IVV": ("america", "AMEX:IVV"), "VT": ("america", "AMEX:VT"),
    "BND": ("america", "NASDAQ:BND"), "GLD": ("america", "AMEX:GLD"),
    "IAU": ("america", "AMEX:IAU"), "XLE": ("america", "AMEX:XLE"),
    "ARKK": ("america", "AMEX:ARKK"), "SOXX": ("america", "NASDAQ:SOXX"),
    # Crypto
    "BTC": ("crypto", "BINANCE:BTCUSDT"), "BTCUSDT": ("crypto", "BINANCE:BTCUSDT"),
    "ETH": ("crypto", "BINANCE:ETHUSDT"), "ETHUSDT": ("crypto", "BINANCE:ETHUSDT"),
    "BNB": ("crypto", "BINANCE:BNBUSDT"), "BNBUSDT": ("crypto", "BINANCE:BNBUSDT"),
    "SOL": ("crypto", "BINANCE:SOLUSDT"), "SOLUSDT": ("crypto", "BINANCE:SOLUSDT"),
    "XRP": ("crypto", "BINANCE:XRPUSDT"), "ADA": ("crypto", "BINANCE:ADAUSDT"),
    "DOGE": ("crypto", "BINANCE:DOGEUSDT"), "DOT": ("crypto", "BINANCE:DOTUSDT"),
    # Commodities (use america endpoint for ETF proxies)
    "GOLD": ("america", "AMEX:GLD"), "XAUUSD": ("america", "AMEX:GLD"),
    "SILVER": ("america", "AMEX:SLV"), "XAGUSD": ("america", "AMEX:SLV"),
    "OIL": ("america", "AMEX:USO"), "WTI": ("america", "AMEX:USO"),
    "BRENT": ("america", "AMEX:BNO"),
    # Forex
    "EURUSD": ("forex", "FX:EURUSD"), "USDJPY": ("forex", "FX:USDJPY"),
    "GBPUSD": ("forex", "FX:GBPUSD"), "AUDUSD": ("forex", "FX:AUDUSD"),
}

# Special non-tradeable assets
SPECIAL_ASSETS = {
    "CASH": {"type": "cash", "return": 0.055, "volatility": 0.005, "label": "Cash/Bank deposit"},
    "BOND": {"type": "bond", "return": 0.065, "volatility": 0.02, "label": "VN Bonds"},
    "SAVINGS": {"type": "cash", "return": 0.055, "volatility": 0.002, "label": "Savings"},
    "USBOND": {"type": "bond", "return": 0.045, "volatility": 0.05, "label": "US Treasury"},
}

COLUMNS_EQUITY = [
    "name", "close", "change", "volume", "RSI", "EMA20", "EMA50", "EMA200",
    "MACD.macd", "MACD.signal", "BB.upper", "BB.lower",
    "price_52_week_high", "price_52_week_low",
    "Perf.W", "Perf.1M", "Perf.3M", "Perf.6M", "Perf.YTD", "Perf.Y",
    "Volatility.D", "price_earnings_ttm",
]

# Crypto & forex don't have price_earnings_ttm
COLUMNS_NO_PE = [
    "name", "close", "change", "volume", "RSI", "EMA20", "EMA50", "EMA200",
    "MACD.macd", "MACD.signal", "BB.upper", "BB.lower",
    "price_52_week_high", "price_52_week_low",
    "Perf.W", "Perf.1M", "Perf.3M", "Perf.6M", "Perf.YTD", "Perf.Y",
    "Volatility.D",
]

def get_columns(market):
    if market in ("crypto", "forex"):
        return COLUMNS_NO_PE
    return COLUMNS_EQUITY

RISK_PROFILES = {
    "conservative": {
        "label": "🛡️ Conservative",
        "max_single": 0.25,
        "max_equity": 0.40,
        "max_crypto": 0.05,
        "min_safe": 0.35,      # cash + bonds + gold
        "target_vol": 0.12,
        "target_sharpe": 0.8,
    },
    "balanced": {
        "label": "⚖️ Balanced",
        "max_single": 0.30,
        "max_equity": 0.60,
        "max_crypto": 0.15,
        "min_safe": 0.20,
        "target_vol": 0.18,
        "target_sharpe": 1.0,
    },
    "aggressive": {
        "label": "🔥 Aggressive",
        "max_single": 0.35,
        "max_equity": 0.80,
        "max_crypto": 0.25,
        "min_safe": 0.05,
        "target_vol": 0.25,
        "target_sharpe": 1.2,
    },
}

RF_RATE = 0.055  # risk-free rate VN


def fetch_tradingview_data(tickers_map):
    """Fetch data for multiple assets from TradingView. tickers_map: {ticker: (market, tv_symbol)}"""
    # Group by market endpoint
    by_market = {}
    for ticker, (market, tv_sym) in tickers_map.items():
        by_market.setdefault(market, []).append((ticker, tv_sym))

    results = {}
    for market, items in by_market.items():
        tv_symbols = [tv_sym for _, tv_sym in items]
        ticker_lookup = {tv_sym: ticker for ticker, tv_sym in items}
        columns = get_columns(market)

        payload = {
            "symbols": {"tickers": tv_symbols},
            "columns": columns,
        }

        url = f"https://scanner.tradingview.com/{market}/scan"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read())
        except Exception as e:
            print(f"  ⚠️ Fetch error {market}: {e}")
            continue

        for item in data.get("data", []):
            full_sym = item["s"]
            d = item["d"]
            ticker = ticker_lookup.get(full_sym, full_sym.split(":")[-1])

            col_map = {c: i for i, c in enumerate(columns)}

            def _get(name):
                idx = col_map.get(name)
                return d[idx] if idx is not None and idx < len(d) else None

            results[ticker] = {
                "name": _get("name"),
                "close": _get("close"),
                "change": _get("change"),
                "volume": _get("volume"),
                "rsi": _get("RSI"),
                "ema20": _get("EMA20"),
                "ema50": _get("EMA50"),
                "ema200": _get("EMA200"),
                "macd": _get("MACD.macd"),
                "macd_signal": _get("MACD.signal"),
                "bb_upper": _get("BB.upper"),
                "bb_lower": _get("BB.lower"),
                "high_52w": _get("price_52_week_high"),
                "low_52w": _get("price_52_week_low"),
                "perf_w": _get("Perf.W"),
                "perf_1m": _get("Perf.1M"),
                "perf_3m": _get("Perf.3M"),
                "perf_6m": _get("Perf.6M"),
                "perf_ytd": _get("Perf.YTD"),
                "perf_1y": _get("Perf.Y"),
                "volatility_d": _get("Volatility.D"),
                "pe": _get("price_earnings_ttm"),
                "market": market,
            }

    return results


def classify_asset(ticker, market=None):
    """Classify asset."""
    if ticker in SPECIAL_ASSETS:
        return SPECIAL_ASSETS[ticker]["type"]
    if market == "crypto":
        return "crypto"
    if market == "cfd":
        return "commodity"
    if market == "forex":
        return "forex"
    if ticker in ("BND", "AGG", "BNDX", "BOND", "USBOND"):
        return "bond"
    if ticker in ("GLD", "IAU", "GOLD", "XAUUSD"):
        return "commodity"
    return "equity"


def estimate_annual_return(data):
    """Estimate annual return from TradingView perf data."""
    if data is None:
        return 0.0
    perf_1y = data.get("perf_1y")
    if perf_1y is not None:
        return perf_1y / 100.0
    # Fallback: extrapolate from shorter periods
    perf_6m = data.get("perf_6m")
    if perf_6m is not None:
        return (1 + perf_6m / 100.0) ** 2 - 1
    perf_3m = data.get("perf_3m")
    if perf_3m is not None:
        return (1 + perf_3m / 100.0) ** 4 - 1
    return 0.0


def estimate_volatility(data):
    """Estimate annualized volatility."""
    if data is None:
        return 0.15
    vol_d = data.get("volatility_d")
    if vol_d is not None and vol_d > 0:
        return vol_d * math.sqrt(252) / 100.0
    # Rough estimate from 52w range
    h52 = data.get("high_52w")
    l52 = data.get("low_52w")
    close = data.get("close")
    if h52 and l52 and close and h52 > l52:
        range_pct = (h52 - l52) / close
        return range_pct * 0.4  # rough approximation
    return 0.25


def calc_portfolio_metrics(weights, returns, vols, corr_matrix):
    """Calculate portfolio return, volatility, Sharpe."""
    n = len(weights)
    port_return = sum(w * r for w, r in zip(weights, returns))

    # Portfolio variance = w' * Σ * w
    port_var = 0.0
    for i in range(n):
        for j in range(n):
            port_var += weights[i] * weights[j] * vols[i] * vols[j] * corr_matrix[i][j]

    port_vol = math.sqrt(max(port_var, 0))
    port_sharpe = (port_return - RF_RATE) / port_vol if port_vol > 0 else 0

    return port_return, port_vol, port_sharpe


def estimate_correlation(types_i, types_j):
    """Estimate correlation between 2 asset classes."""
    if types_i == types_j:
        return 0.85  # same asset class → high correlation
    corr_table = {
        ("equity", "equity"): 0.75,
        ("equity", "bond"): -0.10,
        ("equity", "commodity"): 0.15,
        ("equity", "crypto"): 0.40,
        ("equity", "cash"): 0.0,
        ("equity", "forex"): 0.20,
        ("bond", "commodity"): 0.10,
        ("bond", "crypto"): -0.05,
        ("bond", "cash"): 0.30,
        ("bond", "forex"): 0.15,
        ("commodity", "crypto"): 0.25,
        ("commodity", "cash"): 0.0,
        ("commodity", "forex"): 0.30,
        ("crypto", "cash"): 0.0,
        ("crypto", "forex"): 0.15,
        ("cash", "forex"): 0.10,
    }
    key = (types_i, types_j)
    rev_key = (types_j, types_i)
    return corr_table.get(key, corr_table.get(rev_key, 0.3))


def build_correlation_matrix(asset_types):
    """Build correlation matrix based on asset class."""
    n = len(asset_types)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = 1.0
            else:
                matrix[i][j] = estimate_correlation(asset_types[i], asset_types[j])
    return matrix


def optimize_markowitz(returns, vols, corr_matrix, risk_profile, asset_types):
    """Simple Markowitz optimization via grid search (no numpy dependency)."""
    n = len(returns)
    profile = RISK_PROFILES[risk_profile]
    target_vol = profile["target_vol"]

    best_sharpe = -999
    best_weights = [1.0 / n] * n

    # For small portfolios (≤5 assets), do grid search
    # For larger, use heuristic
    if n <= 5:
        step = 0.05
        _optimize_grid(n, returns, vols, corr_matrix, profile, asset_types,
                       best_sharpe, best_weights, step)
        # Try finer grid around best
        best_sharpe_final, best_weights_final = _optimize_grid_result(
            n, returns, vols, corr_matrix, profile, asset_types, step)
        if best_sharpe_final > best_sharpe:
            best_sharpe = best_sharpe_final
            best_weights = best_weights_final
    else:
        # Heuristic: weight by Sharpe ratio, constrained
        best_weights = _heuristic_weights(returns, vols, profile, asset_types)
        port_r, port_v, best_sharpe = calc_portfolio_metrics(
            best_weights, returns, vols, corr_matrix)

    return best_weights, best_sharpe


def _optimize_grid_result(n, returns, vols, corr_matrix, profile, asset_types, step):
    """Grid search optimization."""
    best_sharpe = -999
    best_weights = [1.0 / n] * n

    def recurse(idx, remaining, current_weights):
        nonlocal best_sharpe, best_weights
        if idx == n - 1:
            w = list(current_weights) + [remaining]
            if not _check_constraints(w, profile, asset_types):
                return
            pr, pv, ps = calc_portfolio_metrics(w, returns, vols, corr_matrix)
            if ps > best_sharpe:
                best_sharpe = ps
                best_weights = w[:]
            return

        max_w = min(remaining, profile["max_single"])
        w = 0.0
        while w <= max_w + 0.001:
            recurse(idx + 1, remaining - w, current_weights + [w])
            w += step

    recurse(0, 1.0, [])
    return best_sharpe, best_weights


def _optimize_grid(*args):
    pass  # Placeholder, actual work done in _optimize_grid_result


def _check_constraints(weights, profile, asset_types):
    """Check if weights satisfy risk profile constraints."""
    n = len(weights)
    for i in range(n):
        if weights[i] < -0.001 or weights[i] > profile["max_single"] + 0.01:
            return False

    # Check asset class limits
    equity_w = sum(w for w, t in zip(weights, asset_types) if t == "equity")
    crypto_w = sum(w for w, t in zip(weights, asset_types) if t == "crypto")
    safe_w = sum(w for w, t in zip(weights, asset_types) if t in ("cash", "bond", "commodity"))

    if equity_w > profile["max_equity"] + 0.01:
        return False
    if crypto_w > profile["max_crypto"] + 0.01:
        return False
    # min_safe is soft constraint for optimization
    return True


def _heuristic_weights(returns, vols, profile, asset_types):
    """Heuristic weight allocation for larger portfolios."""
    n = len(returns)
    # Score each asset by risk-adjusted return
    scores = []
    for i in range(n):
        sharpe_i = (returns[i] - RF_RATE) / vols[i] if vols[i] > 0 else 0
        scores.append(max(sharpe_i, 0.01))

    total = sum(scores)
    weights = [s / total for s in scores]

    # Apply constraints
    for i in range(n):
        weights[i] = min(weights[i], profile["max_single"])

    # Re-normalize
    total = sum(weights)
    if total > 0:
        weights = [w / total for w in weights]

    return weights


def max_drawdown_estimate(vol, years=1):
    """Rough max drawdown estimate from volatility."""
    return -vol * math.sqrt(years) * 1.5


def parse_portfolio(portfolio_str):
    """Parse 'MBB:30,FPT:25,GOLD:20' → [(ticker, weight_pct), ...]"""
    items = []
    for part in portfolio_str.split(","):
        part = part.strip()
        if ":" in part:
            ticker, weight = part.split(":", 1)
            items.append((ticker.strip().upper(), float(weight.strip())))
        else:
            items.append((part.strip().upper(), 0))

    total = sum(w for _, w in items)
    if abs(total - 100) > 1:
        print(f"  ⚠️ Total weight = {total}% (should = 100%). Will normalize.")
        if total > 0:
            items = [(t, w / total * 100) for t, w in items]
    return items


def fmt_vnd(value):
    """Format VND amount."""
    if abs(value) >= 1e9:
        return f"{value/1e9:.2f} tỷ"
    if abs(value) >= 1e6:
        return f"{value/1e6:.1f} triệu"
    return f"{value:,.0f}"


def fmt_pct(value):
    """Format percentage."""
    if value is None:
        return "N/A"
    return f"{value*100:+.1f}%"


def main():
    parser = argparse.ArgumentParser(description="Portfolio Optimizer — Portfolio Analysis & Rebalance")
    parser.add_argument("--portfolio", "-p", required=True,
                        help='Portfolio: "MBB:30,FPT:25,GOLD:20,BNB:15,CASH:10" (ticker:weight%%)')
    parser.add_argument("--capital", "-c", type=float, required=True,
                        help="Total capital (VND)")
    parser.add_argument("--risk", "-r", forices=["conservative", "balanced", "aggressive"],
                        default="balanced", help="Risk appetite (default: balanced)")
    args = parser.parse_args()

    portfolio = parse_portfolio(args.portfolio)
    capital = args.capital
    risk = args.risk
    profile = RISK_PROFILES[risk]

    tickers = [t for t, _ in portfolio]
    weights_pct = [w for _, w in portfolio]
    weights = [w / 100.0 for w in weights_pct]

    print(f"\n{'='*75}")
    print(f"  📊 PORTFOLIO OPTIMIZER — Analysis & Rebalance Recommendation")
    print(f"  Capital: {fmt_vnd(capital)} | Risk Profile: {profile['label']}")
    print(f"  Time: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"{'='*75}")

    # ── Fetch data ──
    print(f"\n⏳ Fetching real-time data from TradingView...")

    # Build fetch map (skip special assets)
    fetch_map = {}
    for t in tickers:
        if t in SPECIAL_ASSETS:
            continue
        if t in ASSET_MAP:
            market, tv_sym = ASSET_MAP[t]
            fetch_map[t] = (market, tv_sym)
        else:
            # Try as VN stock by default
            fetch_map[t] = ("vietnam", f"HOSE:{t}")

    tv_data = fetch_tradingview_data(fetch_map) if fetch_map else {}

    # ── Build metrics for each asset ──
    asset_returns = []
    asset_vols = []
    asset_types = []
    asset_data = []

    for ticker, weight in portfolio:
        if ticker in SPECIAL_ASSETS:
            spec = SPECIAL_ASSETS[ticker]
            asset_returns.append(spec["return"])
            asset_vols.append(spec["volatility"])
            asset_types.append(spec["type"])
            asset_data.append({"name": spec["label"], "close": None, "rsi": None,
                             "ema200": None, "pe": None, "perf_1y": spec["return"] * 100})
        elif ticker in tv_data:
            d = tv_data[ticker]
            ret = estimate_annual_return(d)
            vol = estimate_volatility(d)
            atype = classify_asset(ticker, d.get("market"))
            asset_returns.append(ret)
            asset_vols.append(vol)
            asset_types.append(atype)
            asset_data.append(d)
        else:
            print(f"  ⚠️ Data not found for {ticker}, using default values")
            asset_returns.append(0.08)
            asset_vols.append(0.25)
            asset_types.append("equity")
            asset_data.append({"name": ticker, "close": None, "rsi": None,
                             "ema200": None, "pe": None, "perf_1y": None})

    n = len(tickers)
    corr_matrix = build_correlation_matrix(asset_types)

    # ── 1. Current Portfolio Analysis ──
    port_return, port_vol, port_sharpe = calc_portfolio_metrics(
        weights, asset_returns, asset_vols, corr_matrix)

    print(f"\n{'─'*75}")
    print(f"  📋 1. CURRENT PORTFOLIO")
    print(f"{'─'*75}")

    print(f"\n  {'Mã':<10} {'Weight':>9} {'Value':>14} {'Return 1Y':>10} {'Vol':>8} {'RSI':>6} {'Type':<12}")
    print(f"  {'─'*70}")

    for i in range(n):
        ticker = tickers[i]
        w = weights_pct[i]
        value = capital * weights[i]
        ret_str = f"{asset_returns[i]*100:+.1f}%" if asset_returns[i] else "N/A"
        vol_str = f"{asset_vols[i]*100:.1f}%"
        rsi_str = f"{asset_data[i]['rsi']:.0f}" if asset_data[i].get('rsi') else "—"
        type_labels = {
            "equity": "Equity", "crypto": "Crypto", "commodity": "Commodity",
            "bond": "Bond", "cash": "Cash", "forex": "Forex",
        }
        type_str = type_labels.get(asset_types[i], asset_types[i])
        print(f"  {ticker:<10} {w:>8.1f}% {fmt_vnd(value):>14} {ret_str:>10} {vol_str:>8} {rsi_str:>6} {type_str:<12}")

    print(f"\n  📈 Portfolio summary:")
    print(f"     Expected Return:   {port_return*100:+.1f}%/năm")
    print(f"     Volatility:        {port_vol*100:.1f}%/năm")
    print(f"     Sharpe Ratio:      {port_sharpe:.2f}")
    print(f"     Max Drawdown (est):{max_drawdown_estimate(port_vol)*100:.1f}%")

    # ── 2. Diagnostics ──
    print(f"\n{'─'*75}")
    print(f"  🔍 2. PORTFOLIO ASSESSMENT")
    print(f"{'─'*75}")

    issues = []
    suggestions = []

    # Check concentration
    for i in range(n):
        if weights[i] > profile["max_single"]:
            issues.append(f"⚠️ {tickers[i]} takes {weights_pct[i]:.0f}% — exceeds limit {profile['max_single']*100:.0f}% for {risk}")

    # Check asset class balance
    equity_w = sum(w for w, t in zip(weights, asset_types) if t == "equity")
    crypto_w = sum(w for w, t in zip(weights, asset_types) if t == "crypto")
    safe_w = sum(w for w, t in zip(weights, asset_types) if t in ("cash", "bond", "commodity"))
    commodity_w = sum(w for w, t in zip(weights, asset_types) if t == "commodity")

    if equity_w > profile["max_equity"]:
        issues.append(f"⚠️ Equity takes {equity_w*100:.0f}% — exceeds limit {profile['max_equity']*100:.0f}%")
    if crypto_w > profile["max_crypto"]:
        issues.append(f"⚠️ Crypto takes {crypto_w*100:.0f}% — exceeds limit {profile['max_crypto']*100:.0f}%")
    if safe_w < profile["min_safe"]:
        issues.append(f"⚠️ Safe assets only {safe_w*100:.0f}% — needs at least {profile['min_safe']*100:.0f}%")

    # Check diversification
    unique_types = set(asset_types)
    if len(unique_types) < 3:
        issues.append(f"⚠️ Chỉ có {len(unique_types)} asset types — lacking diversification")
    if n < 4:
        issues.append(f"⚠️ Chỉ có {n} tickers — should have at least 4-5")

    # Check volatility vs target
    if port_vol > profile["target_vol"] * 1.3:
        issues.append(f"⚠️ Volatility {port_vol*100:.0f}% higher than target {profile['target_vol']*100:.0f}% for {risk}")

    # Check individual assets
    for i in range(n):
        d = asset_data[i]
        rsi = d.get("rsi")
        ema200 = d.get("ema200")
        close = d.get("close")
        if rsi and rsi > 70:
            suggestions.append(f"📌 {tickers[i]} RSI={rsi:.0f} — overbought, consider reducing allocation")
        if close and ema200 and close < ema200:
            suggestions.append(f"📌 {tickers[i]} below EMA200 — downtrend, be cautious")
        if rsi and rsi < 30 and close and ema200 and close > ema200:
            suggestions.append(f"📌 {tickers[i]} RSI={rsi:.0f} oversold + above EMA200 — accumulation opportunity")

    if issues:
        print(f"\n  🔴 Issues detected:")
        for issue in issues:
            print(f"     {issue}")
    else:
        print(f"\n  🟢 Portfolio complies with risk profile limits {risk}")

    if suggestions:
        print(f"\n  💡 Suggestions from technical analysis:")
        for sug in suggestions:
            print(f"     {sug}")

    # Correlation matrix display
    print(f"\n  📊 Correlation matrix (estimated):")
    print(f"     {'':>8}", end="")
    for t in tickers:
        print(f" {t:>7}", end="")
    print()
    for i in range(n):
        print(f"     {tickers[i]:>8}", end="")
        for j in range(n):
            val = corr_matrix[i][j]
            print(f" {val:>+6.2f}", end="")
        print()

    # ── 3. Rebalance Optimization ──
    print(f"\n{'─'*75}")
    print(f"  🎯 3. REBALANCE RECOMMENDATION (Markowitz Mean-Variance)")
    print(f"{'─'*75}")

    opt_weights, opt_sharpe = optimize_markowitz(
        asset_returns, asset_vols, corr_matrix, risk, asset_types)

    opt_return, opt_vol, opt_sharpe = calc_portfolio_metrics(
        opt_weights, asset_returns, asset_vols, corr_matrix)

    print(f"\n  {'Mã':<10} {'Current':>9} {'Proposed':>9} {'Change':>9} {'Value mới':>14} {'Action':<15}")
    print(f"  {'─'*70}")

    for i in range(n):
        old_w = weights_pct[i]
        new_w = opt_weights[i] * 100
        diff = new_w - old_w
        new_val = capital * opt_weights[i]

        if diff > 2:
            action = f"🟢 Increase +{diff:.0f}%"
        elif diff < -2:
            action = f"🔴 Decrease {diff:.0f}%"
        else:
            action = "⚪ Keep"

        print(f"  {tickers[i]:<10} {old_w:>8.1f}% {new_w:>8.1f}% {diff:>+8.1f}% {fmt_vnd(new_val):>14} {action}")

    # ── 4. Before/after comparison ──
    print(f"\n{'─'*75}")
    print(f"  📊 4. BEFORE / AFTER REBALANCE COMPARISON")
    print(f"{'─'*75}")

    print(f"\n  {'Metric':<25} {'Before':>12} {'After':>12} {'Change':>12}")
    print(f"  {'─'*55}")
    print(f"  {'Expected Return':<25} {port_return*100:>+11.1f}% {opt_return*100:>+11.1f}% {(opt_return-port_return)*100:>+11.1f}%")
    print(f"  {'Volatility':<25} {port_vol*100:>11.1f}% {opt_vol*100:>11.1f}% {(opt_vol-port_vol)*100:>+11.1f}%")
    print(f"  {'Sharpe Ratio':<25} {port_sharpe:>12.2f} {opt_sharpe:>12.2f} {opt_sharpe-port_sharpe:>+12.2f}")
    print(f"  {'Max Drawdown (est)':<25} {max_drawdown_estimate(port_vol)*100:>11.1f}% {max_drawdown_estimate(opt_vol)*100:>11.1f}% {(max_drawdown_estimate(opt_vol)-max_drawdown_estimate(port_vol))*100:>+11.1f}%")

    # Equity class breakdown
    old_eq = sum(w for w, t in zip(weights, asset_types) if t == "equity") * 100
    new_eq = sum(w for w, t in zip(opt_weights, asset_types) if t == "equity") * 100
    old_cr = sum(w for w, t in zip(weights, asset_types) if t == "crypto") * 100
    new_cr = sum(w for w, t in zip(opt_weights, asset_types) if t == "crypto") * 100
    old_sf = sum(w for w, t in zip(weights, asset_types) if t in ("cash", "bond", "commodity")) * 100
    new_sf = sum(w for w, t in zip(opt_weights, asset_types) if t in ("cash", "bond", "commodity")) * 100

    print(f"\n  {'Allocation by type':<25} {'Before':>12} {'After':>12}")
    print(f"  {'─'*45}")
    print(f"  {'Equity':<25} {old_eq:>11.0f}% {new_eq:>11.0f}%")
    print(f"  {'Crypto':<25} {old_cr:>11.0f}% {new_cr:>11.0f}%")
    print(f"  {'Safe (cash/bond/gold)':<25} {old_sf:>11.0f}% {new_sf:>11.0f}%")

    # ── 5. Return scenarios ──
    print(f"\n{'─'*75}")
    print(f"  💰 5. RETURN SCENARIOS (after rebalance)")
    print(f"{'─'*75}")

    for years in [1, 3, 5]:
        bear_r = max(RF_RATE, opt_return - 1.0 * opt_vol)
        base_r = opt_return
        bull_r = opt_return + 0.5 * opt_vol

        bear_v = capital * (1 + bear_r) ** years
        base_v = capital * (1 + base_r) ** years
        bull_v = capital * (1 + bull_r) ** years

        print(f"\n  📅 {years} years (capital {fmt_vnd(capital)}):")
        print(f"     🐻 Bear:  {fmt_vnd(bear_v)} ({(bear_v/capital-1)*100:+.1f}%)")
        print(f"     📊 Base:  {fmt_vnd(base_v)} ({(base_v/capital-1)*100:+.1f}%)")
        print(f"     🐂 Bull:  {fmt_vnd(bull_v)} ({(bull_v/capital-1)*100:+.1f}%)")

    # ── 6. Action plan ──
    print(f"\n{'─'*75}")
    print(f"  🎬 6. IMPLEMENTATION PLAN")
    print(f"{'─'*75}")

    print(f"\n  Split rebalance into 2-3 batches over 2-4 weeks:")
    rebalance_actions = []
    for i in range(n):
        old_val = capital * weights[i]
        new_val = capital * opt_weights[i]
        diff_val = new_val - old_val
        if abs(diff_val) > capital * 0.02:  # >2% change
            if diff_val > 0:
                rebalance_actions.append((tickers[i], "BUY more", diff_val))
            else:
                rebalance_actions.append((tickers[i], "SELL some", abs(diff_val)))

    if rebalance_actions:
        for ticker, action, val in rebalance_actions:
            print(f"     → {action} {ticker}: ~{fmt_vnd(val)}")
    else:
        print(f"     ✅ Portfolio is fairly balanced, no major rebalance needed.")

    print(f"\n{'='*75}")
    print(f"  ⚠️ Analysis is for reference. Correlation & volatility are estimates.")
    print(f"  📌 Rebalance should be done 1-2 times/quarter to minimize trading fees.")
    print(f"{'='*75}\n")


if __name__ == "__main__":
    main()
