"""价格序列：维护/读取 cache/price_series.json。

供趋势判定、动态阈值（波动率）、EMA 计算使用。独立于智能体书写的分析日志，
fetch.py 每次运行追加一个采样点，形成可靠的价格时间序列（P0-2 / P0-6）。
"""

import json

from . import paths, atomic, timeutil


def series_file():
    return paths.resolve("cache") / "price_series.json"


def load_series():
    f = series_file()
    if not f.exists():
        return []
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        s = data.get("series", [])
        return s if isinstance(s, list) else []
    except Exception:
        return []


def append_point(price_usd, ts=None, max_points=2000):
    """追加一个采样点（时间戳去重）。返回更新后的序列。"""
    series = load_series()
    ts = ts or timeutil.now_iso()
    if price_usd is None:
        return series
    if series and series[-1].get("ts") == ts:
        series[-1]["price_usd"] = price_usd
    else:
        series.append({"ts": ts, "price_usd": float(price_usd)})
    if len(series) > max_points:
        series = series[-max_points:]
    atomic.atomic_write_json(series_file(), {"series": series})
    return series


def daily_closes(series):
    """按日期分组，取每日最后一个采样点，返回升序 [{date, price}]。"""
    by_date = {}
    for p in series:
        if not p.get("ts") or p.get("price_usd") is None:
            continue
        d = str(p["ts"])[:10]
        by_date[d] = float(p["price_usd"])
    return [{"date": d, "price": by_date[d]} for d in sorted(by_date)]


def prices(series):
    return [float(p["price_usd"]) for p in series if p.get("price_usd") is not None]
