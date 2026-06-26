#!/usr/bin/env python3
"""CLI tool to query gold, USD index, and oil prices."""

import json
import re
import sys
from datetime import datetime

try:
    import akshare as ak
    import requests
except ImportError:
    print(json.dumps({"error": "Missing dependencies. Please run: pip install akshare requests"}))
    sys.exit(1)

_SINA_HEADERS = {"Referer": "https://finance.sina.com.cn"}


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _parse_sina_hq(code: str) -> list:
    resp = requests.get(
        f"https://hq.sinajs.cn/list={code}",
        headers=_SINA_HEADERS,
        timeout=10,
    )
    resp.raise_for_status()
    m = re.search(r'"(.+)"', resp.text)
    if not m or not m.group(1):
        raise ValueError(f"Sina quote {code} returned empty data")
    return m.group(1).split(",")


def _calc_change(price: float, prev: float) -> tuple:
    change = round(price - prev, 2)
    change_pct = round(change / prev * 100, 2) if prev else 0.0
    return change, change_pct


def get_china_gold() -> dict:
    try:
        df = ak.futures_zh_spot(symbol="AU0", market="CF", adjust="0")
        if df is None or df.empty:
            raise ValueError("Empty data from akshare")
        row = df.iloc[-1]
        price = float(row["current_price"])
        prev = float(row["last_settle_price"]) or float(row["last_close"])
        change, change_pct = _calc_change(price, prev)
        return {
            "name": "中国黄金 Au99.99",
            "symbol": "AU9999",
            "price": price,
            "change": change,
            "change_pct": change_pct,
            "unit": "元/克",
            "update_time": _now_str(),
        }
    except Exception as e:
        return {"symbol": "AU9999", "error": str(e)}


def get_international_gold() -> dict:
    try:
        fields = _parse_sina_hq("hf_GC")
        price = float(fields[0])
        prev = float(fields[3]) if fields[3] else price
        change, change_pct = _calc_change(price, prev)
        return {
            "name": "国际黄金 COMEX",
            "symbol": "XAUUSD",
            "price": price,
            "change": change,
            "change_pct": change_pct,
            "unit": "USD/oz",
            "update_time": _now_str(),
        }
    except Exception as e:
        return {"symbol": "XAUUSD", "error": str(e)}


def get_usd_index() -> dict:
    try:
        fields = _parse_sina_hq("DINIW")
        price = float(fields[8])
        prev = float(fields[3]) if fields[3] else price
        change, change_pct = _calc_change(price, prev)
        return {
            "name": "美元指数 DXY",
            "symbol": "USIDX",
            "price": price,
            "change": change,
            "change_pct": change_pct,
            "unit": "",
            "update_time": _now_str(),
        }
    except Exception as e:
        return {"symbol": "USIDX", "error": str(e)}


def get_oil_price() -> dict:
    try:
        fields = _parse_sina_hq("hf_CL")
        price = float(fields[0])
        prev = float(fields[3]) if fields[3] else price
        change, change_pct = _calc_change(price, prev)
        return {
            "name": "WTI 原油",
            "symbol": "WTI",
            "price": price,
            "change": change,
            "change_pct": change_pct,
            "unit": "USD/桶",
            "update_time": _now_str(),
        }
    except Exception as e:
        return {"symbol": "WTI", "error": str(e)}


def get_gold_oil_ratio() -> dict:
    """Gold/Oil ratio with investment signal and advice."""
    gold = get_international_gold()
    oil = get_oil_price()

    if gold.get("error") or oil.get("error"):
        return {"symbol": "GORATIO", "error": "Failed to fetch gold or oil price"}

    gold_price = gold["price"]
    oil_price = oil["price"]

    if oil_price <= 0:
        return {"symbol": "GORATIO", "error": "Oil price is zero"}

    ratio = round(gold_price / oil_price, 2)

    if ratio > 40:
        level, signal = "极度偏高", "🔴 衰退/危机信号"
        advice = (
            "金油比处于历史极高区间（参考：2020年COVID危机峰值约70）。"
            "建议：① 减少黄金敞口，等待回调；② 原油极度低估，可分批布局多头；③ 控制整体仓位。"
        )
    elif ratio > 25:
        level, signal = "偏高", "🟠 避险情绪偏强"
        advice = (
            "金油比高于历史均值，反映经济下行预期。"
            "建议：① 黄金动能强但上涨空间收窄，注意止盈；② 可轻仓关注原油多头机会。"
        )
    elif ratio > 15:
        level, signal = "正常", "🟡 处于历史均值区间"
        advice = (
            "金油比位于长期均值区间（约15-25）。"
            "建议：维持均衡配置，以各自基本面驱动为主进行交易。"
        )
    elif ratio > 10:
        level, signal = "偏低", "🟢 经济扩张信号"
        advice = (
            "大宗商品需求旺盛，经济扩张。"
            "建议：① 黄金相对便宜，可逢低增配；② 原油短期偏强但警惕回调。"
        )
    else:
        level, signal = "极度偏低", "🔵 通胀/供给冲击信号"
        advice = (
            "原油可能严重高估或通胀失控。"
            "建议：① 高度警惕原油回调风险；② 大幅增配黄金作为抗通胀资产。"
        )

    return {
        "symbol": "GORATIO",
        "name": "金油比",
        "ratio": ratio,
        "gold_price": gold_price,
        "oil_price": oil_price,
        "level": level,
        "signal": signal,
        "advice": advice,
        "update_time": _now_str(),
    }


_FETCHERS = {
    "AU9999": get_china_gold,
    "XAUUSD": get_international_gold,
    "USIDX": get_usd_index,
    "WTI": get_oil_price,
    "GORATIO": get_gold_oil_ratio,
}


def main():
    symbol = sys.argv[1].upper() if len(sys.argv) > 1 else "ALL"

    if symbol == "ALL":
        result = [fn() for fn in _FETCHERS.values()]
    elif symbol in _FETCHERS:
        result = _FETCHERS[symbol]()
    else:
        result = {"error": f"Unknown symbol: {symbol}", "valid_symbols": list(_FETCHERS.keys()) + ["ALL"]}

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
