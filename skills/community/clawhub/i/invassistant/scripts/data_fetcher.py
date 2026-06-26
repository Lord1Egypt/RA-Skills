# -*- coding: utf-8 -*-
"""
InvAssistant — 数据获取模块
统一的 Yahoo Finance 数据获取，包含 429 重试和限流延迟。

接口:
  fetch_stock(symbol, days=60, retries=3)  → pd.DataFrame | None
  fetch_all(symbols, delay=3)              → dict[str, pd.DataFrame]
"""
import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import random
import sys


def fetch_stock(symbol, days=60, retries=3):
    """
    获取单只股票的历史 OHLCV 数据。

    Args:
        symbol: 股票代码 (如 "TSLA", "^VIX")
        days: 获取天数 (默认60)
        retries: 失败重试次数 (默认3)

    Returns:
        pd.DataFrame (index=Date, columns=[Open,High,Low,Close,Volume])
        失败返回 None
    """
    for attempt in range(retries):
        try:
            end_ts = int(datetime.now().timestamp())
            start_ts = int((datetime.now() - timedelta(days=days + 10)).timestamp())

            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            params = {
                "period1": start_ts,
                "period2": end_ts,
                "interval": "1d",
                "events": "history"
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            r = requests.get(url, params=params, headers=headers, timeout=20)

            if r.status_code == 429:
                wait = (attempt + 1) * 5 + random.uniform(0, 3)
                print(f"[限流] {symbol}, 等待{wait:.0f}s重试({attempt+1}/{retries})", file=sys.stderr)
                time.sleep(wait)
                continue

            if r.status_code != 200:
                print(f"[错误] {symbol} HTTP {r.status_code}", file=sys.stderr)
                return None

            data = r.json()
            if "chart" not in data or "result" not in data["chart"] or data["chart"]["result"] is None:
                print(f"[错误] {symbol} API返回异常", file=sys.stderr)
                return None

            result = data["chart"]["result"][0]
            ts = result["timestamp"]
            q = result["indicators"]["quote"][0]

            df = pd.DataFrame({
                "Date": pd.to_datetime(ts, unit="s"),
                "Open": q["open"],
                "High": q["high"],
                "Low": q["low"],
                "Close": q["close"],
                "Volume": q["volume"]
            }).set_index("Date").dropna()

            return df

        except Exception as e:
            print(f"[错误] {symbol}: {e}", file=sys.stderr)
            if attempt < retries - 1:
                time.sleep(3)

    return None


def fetch_all(symbols, delay=3, retries=3):
    """
    批量获取多只股票数据。

    Args:
        symbols: 股票代码列表
        delay: 每次请求间隔秒数 (默认3)
        retries: 每只股票的重试次数

    Returns:
        dict[str, pd.DataFrame]
    """
    data = {}
    for i, sym in enumerate(symbols):
        print(f"获取 {sym}... ({i+1}/{len(symbols)})", file=sys.stderr)
        df = fetch_stock(sym, days=60, retries=retries)
        if df is not None:
            data[sym] = df
        else:
            print(f"[警告] {sym} 数据获取失败", file=sys.stderr)

        if i < len(symbols) - 1:
            time.sleep(delay + random.uniform(0, 2))

    return data
