#!/usr/bin/env python3
"""
投资委员会行情抓取脚本
数据源：stooq.com（免费，无需 API key，无限流限制）
支持：美股、港股、BTC、黄金、外汇

用法：
  python3 fetch_price.py GOOGL          # 美股
  python3 fetch_price.py 700.hk         # 港股腾讯
  python3 fetch_price.py GOOGL 0700.hk NVDA  # 多标的
"""

import sys
import requests
from datetime import datetime, timedelta

HEADERS = {'User-Agent': 'Mozilla/5.0'}

# 常用符号映射（自动纠正输入）
SYMBOL_MAP = {
    'GOOGL': 'googl.us',
    'GOOG':  'goog.us',
    'NVDA':  'nvda.us',
    'AAPL':  'aapl.us',
    'MSFT':  'msft.us',
    'AMZN':  'amzn.us',
    'META':  'meta.us',
    'TSLA':  'tsla.us',
    'BABA':  'baba.us',
    'PDD':   'pdd.us',
    'QQQ':   'qqq.us',
    'SPY':   'spy.us',
    'TLT':   'tlt.us',
    '700':   '700.hk',
    '9988':  '9988.hk',
    '3690':  '3690.hk',   # 美团
    'BTC':   'btc.v',
    'ETH':   'eth.v',
    'SOL':   'sol.v',
    'GOLD':  'xauusd',
    '黄金':  'xauusd',
}

def normalize_symbol(s):
    s = s.upper()
    return SYMBOL_MAP.get(s, s.lower().replace('.HK', '.hk').replace('.US', '.us'))

def fetch_quote(symbol_raw, days_back=5):
    sym = normalize_symbol(symbol_raw)
    today = datetime.now()
    d2 = today.strftime('%Y%m%d')
    d1 = (today - timedelta(days=days_back)).strftime('%Y%m%d')
    
    url = f'https://stooq.com/q/d/l/?s={sym}&d1={d1}&d2={d2}&i=d'
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        lines = r.text.strip().split('\n')
        if len(lines) < 2:
            return None, sym
        last = lines[-1].split(',')
        return {
            'symbol_raw': symbol_raw,
            'symbol':     sym,
            'date':       last[0],
            'open':       float(last[1]),
            'high':       float(last[2]),
            'low':        float(last[3]),
            'close':      float(last[4]),
            'volume':     last[5] if len(last) > 5 else 'N/A',
            # 前一天收盘（用于计算日涨跌）
            'prev_close': float(lines[-2].split(',')[4]) if len(lines) >= 3 else None,
        }, sym
    except Exception as e:
        return None, sym

def format_quote(q):
    if not q:
        return '❌ 无数据'
    pct = ''
    if q['prev_close']:
        chg = (q['close'] - q['prev_close']) / q['prev_close'] * 100
        arrow = '📈' if chg >= 0 else '📉'
        pct = f'  {arrow} {chg:+.2f}%'
    return f"${q['close']:.2f}  (H:{q['high']:.2f} / L:{q['low']:.2f}){pct}  [{q['date']}]"

if __name__ == '__main__':
    targets = sys.argv[1:] if len(sys.argv) > 1 else ['GOOGL', '700', 'BTC']
    for t in targets:
        q, sym = fetch_quote(t)
        print(f"{t:15s} {format_quote(q)}")
