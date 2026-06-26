#!/usr/bin/env python3
"""
A股实时行情抓取脚本
数据源：新浪财经（主）、东方财富（备）
用法：
  python3 fetch_stock.py --code 600519
  python3 fetch_stock.py --code 000001 sz000001 300750
  python3 fetch_stock.py --index
  python3 fetch_stock.py --hot-sectors
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://finance.sina.com.cn",
    "Accept-Language": "zh-CN,zh;q=0.9",
}


def get_market_prefix(code: str) -> str:
    """根据股票代码判断市场前缀"""
    code = code.strip().upper()
    if code.startswith("SH") or code.startswith("SZ"):
        return code[:2].lower(), code[2:]
    code = re.sub(r"[^0-9]", "", code)
    if code.startswith(("60", "68", "51", "58", "11")):
        return "sh", code
    elif code.startswith(("00", "30", "15", "12", "16", "13")):
        return "sz", code
    return "sh", code  # default


def fetch_url(url: str, extra_headers: dict = None) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    if extra_headers:
        for k, v in extra_headers.items():
            req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            charset = "gbk" if "sina" in url or "sinajs" in url else "utf-8"
            return resp.read().decode(charset, errors="replace")
    except Exception as e:
        return ""


def parse_sina_stock(raw: str, symbol: str) -> dict:
    """解析新浪财经股票数据"""
    match = re.search(r'"([^"]*)"', raw)
    if not match:
        return {}
    parts = match.group(1).split(",")
    if len(parts) < 32:
        return {}
    try:
        name = parts[0]
        prev_close = float(parts[2]) if parts[2] else 0
        open_price = float(parts[1]) if parts[1] else 0
        current = float(parts[3]) if parts[3] else 0
        high = float(parts[4]) if parts[4] else 0
        low = float(parts[5]) if parts[5] else 0
        volume = int(parts[8]) if parts[8] else 0  # 手
        amount = float(parts[9]) if parts[9] else 0  # 元
        date_str = parts[30] if len(parts) > 30 else ""
        time_str = parts[31] if len(parts) > 31 else ""

        change = current - prev_close
        change_pct = (change / prev_close * 100) if prev_close else 0
        turnover_approx = volume / 1000  # 粗略换手（无流通股数据）

        return {
            "symbol": symbol,
            "name": name,
            "current": round(current, 2),
            "change": round(change, 2),
            "change_pct": round(change_pct, 2),
            "open": round(open_price, 2),
            "high": round(high, 2),
            "low": round(low, 2),
            "prev_close": round(prev_close, 2),
            "volume_lot": volume,  # 手
            "amount_yuan": round(amount, 2),
            "amount_yi": round(amount / 1e8, 2),
            "date": date_str,
            "time": time_str,
            "source": "新浪财经",
            "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    except (ValueError, IndexError):
        return {}


def fetch_single_stock(code: str) -> dict:
    """抓取单只股票行情"""
    prefix, clean_code = get_market_prefix(code)
    symbol = f"{prefix}{clean_code}"
    url = f"http://hq.sinajs.cn/list={symbol}"
    raw = fetch_url(url)
    if raw:
        data = parse_sina_stock(raw, symbol)
        if data:
            return data

    # 备用：东方财富
    market = 1 if prefix == "sh" else 0
    url2 = (
        f"http://push2.eastmoney.com/api/qt/stock/get"
        f"?secid={market}.{clean_code}"
        f"&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f107,f169,f170,f171"
    )
    raw2 = fetch_url(url2, {"Referer": "https://www.eastmoney.com"})
    if raw2:
        try:
            obj = json.loads(raw2)
            d = obj.get("data", {}) or {}
            if d.get("f43"):
                prev = d["f60"] / 100
                curr = d["f43"] / 100
                chg = d["f169"] / 100
                chg_pct = d["f170"] / 100
                return {
                    "symbol": symbol,
                    "name": d.get("f58", ""),
                    "current": round(curr, 2),
                    "change": round(chg, 2),
                    "change_pct": round(chg_pct, 2),
                    "open": round(d["f46"] / 100, 2),
                    "high": round(d["f44"] / 100, 2),
                    "low": round(d["f45"] / 100, 2),
                    "prev_close": round(prev, 2),
                    "volume_lot": d.get("f47", 0),
                    "amount_yuan": d.get("f48", 0),
                    "amount_yi": round(d.get("f48", 0) / 1e8, 2),
                    "turnover_pct": round(d.get("f171", 0) / 100, 2),
                    "source": "东方财富",
                    "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
        except Exception:
            pass

    return {"error": f"无法获取 {code} 的行情数据", "symbol": symbol}


def fetch_index() -> list:
    """抓取主要大盘指数"""
    symbols = "s_sh000001,s_sz399001,s_sz399006,s_sh000688"
    names_map = {
        "s_sh000001": "上证指数",
        "s_sz399001": "深证成指",
        "s_sz399006": "创业板指",
        "s_sh000688": "科创50",
    }
    url = f"http://hq.sinajs.cn/list={symbols}"
    raw = fetch_url(url)
    results = []
    if raw:
        for sym, name in names_map.items():
            pattern = rf'hq_str_{re.escape(sym)}="([^"]*)"'
            m = re.search(pattern, raw)
            if m:
                parts = m.group(1).split(",")
                if len(parts) >= 5:
                    try:
                        results.append({
                            "name": parts[0] or name,
                            "current": float(parts[1]),
                            "change": float(parts[2]),
                            "change_pct": float(parts[3]),
                            "volume_yi_lot": round(float(parts[4]) / 1e8, 2),
                            "amount_yi": round(float(parts[5]) / 1e8, 2) if len(parts) > 5 else 0,
                            "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "source": "新浪财经",
                        })
                    except (ValueError, IndexError):
                        pass
    return results


def fetch_hot_sectors() -> list:
    """抓取热点板块（东方财富概念板块涨幅榜）"""
    url = (
        "http://push2.eastmoney.com/api/qt/clist/get"
        "?pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281"
        "&fltt=2&invt=2&fid=f3"
        "&fs=m:90+t:2+f:!50"
        "&fields=f2,f3,f4,f12,f14,f20,f128,f136,f207,f208,f209"
    )
    raw = fetch_url(url, {"Referer": "https://www.eastmoney.com"})
    results = []
    if raw:
        try:
            obj = json.loads(raw)
            items = obj.get("data", {}).get("diff", [])
            for item in items:
                results.append({
                    "name": item.get("f14", ""),
                    "change_pct": round(item.get("f3", 0), 2),
                    "leading_stock": item.get("f128", ""),
                    "leading_change_pct": round(item.get("f136", 0), 2),
                    "amount_yi": round(item.get("f20", 0) / 1e8, 2),
                })
        except Exception:
            pass
    return results


def fmt_stock(d: dict) -> str:
    if "error" in d:
        return f"❌ {d['error']}"
    sign = "+" if d["change"] >= 0 else ""
    emoji = "🔴" if d["change"] >= 0 else "🟢"
    lines = [
        f"{emoji} {d['name']}（{d['symbol'].upper()}）",
        f"  当前价：{d['current']} 元",
        f"  涨跌幅：{sign}{d['change_pct']}%  涨跌额：{sign}{d['change']}",
        f"  今开：{d['open']}  最高：{d['high']}  最低：{d['low']}  昨收：{d['prev_close']}",
        f"  成交量：{d['volume_lot']:,} 手  成交额：{d['amount_yi']} 亿",
    ]
    if "turnover_pct" in d:
        lines.append(f"  换手率：{d['turnover_pct']}%")
    lines.append(f"  数据来源：{d['source']} | 更新时间：{d.get('time', '')} {d['fetch_time']}")
    return "\n".join(lines)


def fmt_index(items: list) -> str:
    lines = ["📊 大盘指数实时行情"]
    for d in items:
        sign = "+" if d["change"] >= 0 else ""
        emoji = "🔴" if d["change"] >= 0 else "🟢"
        lines.append(
            f"  {emoji} {d['name']}: {d['current']:,.2f}  {sign}{d['change']:+.2f} ({sign}{d['change_pct']}%)"
            f"  成交额 {d['amount_yi']} 亿"
        )
    if items:
        lines.append(f"  更新时间：{items[0]['fetch_time']}")
    return "\n".join(lines)


def fmt_sectors(items: list) -> str:
    lines = ["🔥 热点板块涨幅榜（概念板块 TOP20）"]
    for i, d in enumerate(items, 1):
        sign = "+" if d["change_pct"] >= 0 else ""
        lines.append(
            f"  {i:2d}. {d['name']:<12} {sign}{d['change_pct']}%"
            f"  龙头：{d['leading_stock']}({sign}{d['leading_change_pct']}%)"
            f"  成交额：{d['amount_yi']}亿"
        )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="A股实时行情抓取")
    parser.add_argument("--code", nargs="+", help="股票代码，支持多个（如 600519 000001）")
    parser.add_argument("--index", action="store_true", help="查询大盘指数")
    parser.add_argument("--hot-sectors", action="store_true", help="查询热点板块")
    parser.add_argument("--json", action="store_true", help="输出原始JSON")
    args = parser.parse_args()

    if args.index:
        data = fetch_index()
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(fmt_index(data))
        return

    if args.hot_sectors:
        data = fetch_hot_sectors()
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(fmt_sectors(data))
        return

    if args.code:
        results = []
        for code in args.code:
            d = fetch_single_stock(code)
            results.append(d)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            for d in results:
                print(fmt_stock(d))
                print()
        return

    parser.print_help()


if __name__ == "__main__":
    main()
