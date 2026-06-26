#!/usr/bin/env python3
"""
Market Oracle — Market Data Fetcher
Fetches real-time and historical price data for metals, oil, crypto, and stocks via yfinance.
"""

import argparse
import json
import sys
from datetime import datetime

try:
    import yfinance as yf
except ImportError:
    print("ERROR: yfinance not installed. Run: pip install yfinance", file=sys.stderr)
    sys.exit(1)


# Default asset watchlist with readable names
ASSET_REGISTRY = {
    # Metals
    'gold':    {'ticker': 'GC=F',    'name': '黄金 (Gold)',        'category': 'metals'},
    'silver':  {'ticker': 'SI=F',    'name': '白银 (Silver)',      'category': 'metals'},
    'copper':  {'ticker': 'HG=F',    'name': '铜 (Copper)',        'category': 'metals'},
    'platinum':{'ticker': 'PL=F',    'name': '铂金 (Platinum)',    'category': 'metals'},

    # Oil & Energy
    'oil':     {'ticker': 'CL=F',    'name': '原油 WTI',           'category': 'oil'},
    'wti':     {'ticker': 'CL=F',    'name': '原油 WTI',           'category': 'oil'},
    'brent':   {'ticker': 'BZ=F',    'name': '布伦特原油',          'category': 'oil'},
    'natgas':  {'ticker': 'NG=F',    'name': '天然气',              'category': 'oil'},

    # Crypto
    'btc':     {'ticker': 'BTC-USD', 'name': '比特币 (BTC)',       'category': 'crypto'},
    'eth':     {'ticker': 'ETH-USD', 'name': '以太坊 (ETH)',       'category': 'crypto'},
    'sol':     {'ticker': 'SOL-USD', 'name': 'Solana (SOL)',       'category': 'crypto'},
    'xrp':     {'ticker': 'XRP-USD', 'name': 'Ripple (XRP)',       'category': 'crypto'},
    'doge':    {'ticker': 'DOGE-USD','name': 'Dogecoin (DOGE)',    'category': 'crypto'},

    # Stock Indices
    'spy':     {'ticker': 'SPY',     'name': 'S&P 500 ETF',        'category': 'stocks'},
    'qqq':     {'ticker': 'QQQ',     'name': '纳斯达克100 ETF',    'category': 'stocks'},
    'dia':     {'ticker': 'DIA',     'name': '道琼斯 ETF',         'category': 'stocks'},
    'dji':     {'ticker': '^DJI',    'name': '道琼斯指数',          'category': 'stocks'},
    'nasdaq':  {'ticker': '^IXIC',   'name': '纳斯达克综合指数',    'category': 'stocks'},
    'sp500':   {'ticker': '^GSPC',   'name': 'S&P 500 指数',       'category': 'stocks'},
    'sse':     {'ticker': '000001.SS','name': '上证指数',           'category': 'stocks'},
    'hsi':     {'ticker': '^HSI',    'name': '恒生指数',            'category': 'stocks'},

    # Currency
    'usdx':    {'ticker': 'DX-Y.NYB','name': '美元指数',            'category': 'currency'},
    'usdjpy':  {'ticker': 'JPY=X',   'name': '美元/日元',           'category': 'currency'},
    'usdcny':  {'ticker': 'CNY=X',   'name': '美元/人民币',         'category': 'currency'},
}

# Default "all" watchlist — representative assets from each category
DEFAULT_ALL = ['gold', 'silver', 'oil', 'brent', 'btc', 'eth', 'spy', 'qqq', 'dji', 'usdx']


def resolve_assets(asset_str):
    """Resolve asset names to ticker info."""
    if asset_str.lower() == 'all':
        return [(name, ASSET_REGISTRY[name]) for name in DEFAULT_ALL]

    assets = []
    for item in asset_str.split(','):
        item = item.strip().lower()
        if item in ASSET_REGISTRY:
            assets.append((item, ASSET_REGISTRY[item]))
        else:
            # Treat as raw ticker
            assets.append((item, {'ticker': item.upper(), 'name': item.upper(), 'category': 'custom'}))
    return assets


def fetch_asset_data(ticker_symbol, period='1d', interval='15m'):
    """Fetch price data for a single ticker."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period=period, interval=interval)

        if hist.empty:
            return None

        current = hist.iloc[-1]
        open_price = hist.iloc[0]['Open'] if len(hist) > 0 else current['Open']

        # Calculate changes
        price_now = float(current['Close'])
        price_open = float(open_price)
        change = price_now - price_open
        change_pct = (change / price_open * 100) if price_open != 0 else 0

        # High/Low for the period
        period_high = float(hist['High'].max())
        period_low = float(hist['Low'].min())

        # Volume
        total_volume = int(hist['Volume'].sum()) if 'Volume' in hist.columns else 0

        # Trend detection (simple: compare last 3 data points)
        if len(hist) >= 3:
            recent = hist['Close'].tail(3).tolist()
            if recent[-1] > recent[-2] > recent[-3]:
                trend = '↑ 上涨'
            elif recent[-1] < recent[-2] < recent[-3]:
                trend = '↓ 下跌'
            else:
                trend = '→ 震荡'
        else:
            trend = '— 数据不足'

        return {
            'price': round(price_now, 4),
            'open': round(price_open, 4),
            'high': round(period_high, 4),
            'low': round(period_low, 4),
            'change': round(change, 4),
            'change_pct': round(change_pct, 4),
            'volume': total_volume,
            'trend': trend,
            'data_points': len(hist),
            'last_updated': str(hist.index[-1]),
        }
    except Exception as e:
        return {'error': str(e)}


def format_price(price):
    """Format price for display."""
    if price >= 10000:
        return f"${price:,.0f}"
    elif price >= 100:
        return f"${price:,.2f}"
    elif price >= 1:
        return f"${price:.4f}"
    else:
        return f"${price:.6f}"


def format_change(change_pct):
    """Format change percentage with arrow."""
    if change_pct > 0:
        return f"🟢 +{change_pct:.2f}%"
    elif change_pct < 0:
        return f"🔴 {change_pct:.2f}%"
    else:
        return f"⚪ {change_pct:.2f}%"


def main():
    parser = argparse.ArgumentParser(description='Fetch market data for metals, oil, crypto, stocks')
    parser.add_argument('--assets', '-a', default='all',
                        help='Comma-separated asset names or "all" (default: all)')
    parser.add_argument('--period', '-p', default='1d',
                        help='History period: 1d/5d/1mo/3mo/6mo/1y (default: 1d)')
    parser.add_argument('--interval', '-i', default='15m',
                        help='Data interval: 1m/5m/15m/1h/1d (default: 15m)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--history', action='store_true',
                        help='Include price history in output (JSON only)')

    args = parser.parse_args()
    assets = resolve_assets(args.assets)

    results = {}
    categories = {}

    for name, info in assets:
        ticker = info['ticker']
        display_name = info['name']
        category = info['category']

        data = fetch_asset_data(ticker, period=args.period, interval=args.interval)

        if data and 'error' not in data:
            data['display_name'] = display_name
            data['ticker'] = ticker
            data['category'] = category
            results[name] = data

            if category not in categories:
                categories[category] = []
            categories[category].append((name, data))
        else:
            err = data.get('error', 'Unknown error') if data else 'No data returned'
            print(f"[WARN] Failed to fetch {display_name} ({ticker}): {err}", file=sys.stderr)

    if args.json:
        output = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'period': args.period,
            'interval': args.interval,
            'count': len(results),
            'assets': results
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        # Pretty print
        print(f"📊 市场数据快照")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 周期: {args.period} | 间隔: {args.interval}")
        print("=" * 78)

        category_names = {
            'metals': '🥇 贵金属',
            'oil': '🛢️  能源',
            'crypto': '₿  加密货币',
            'stocks': '📈 股票/指数',
            'currency': '💱 汇率',
            'custom': '📌 自定义',
        }

        for cat_key in ['metals', 'oil', 'crypto', 'stocks', 'currency', 'custom']:
            if cat_key not in categories:
                continue

            print(f"\n{category_names.get(cat_key, cat_key)}")
            print(f"{'─' * 78}")
            print(f"  {'资产':<18} {'价格':>12} {'变化':>14} {'高':>10} {'低':>10} {'趋势'}")
            print(f"  {'─' * 74}")

            for name, data in categories[cat_key]:
                dn = data['display_name']
                price = format_price(data['price'])
                change = format_change(data['change_pct'])
                high = format_price(data['high'])
                low = format_price(data['low'])
                trend = data['trend']
                print(f"  {dn:<18} {price:>12} {change:>14} {high:>10} {low:>10} {trend}")

        print(f"\n{'=' * 78}")
        print(f"📡 数据来源: Yahoo Finance | 共 {len(results)} 个资产")

    if not results:
        print("\n⚠️  无法获取任何市场数据，请检查网络连接。", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
