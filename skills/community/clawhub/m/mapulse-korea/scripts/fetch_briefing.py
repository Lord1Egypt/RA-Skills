#!/usr/bin/env python3
"""
Mapulse — 轻量数据获取脚本
直接输出格式化的Telegram/WhatsApp简报

用法:
  python3 fetch_briefing.py              # 最新交易日
  python3 fetch_briefing.py 2026-03-13   # 指定日期
  python3 fetch_briefing.py --json       # JSON输出
"""

import sys
import os
import json
import datetime
import time

try:
    from pykrx import stock as krx
except ImportError:
    raise ImportError("pykrx not installed. Run: pip install pykrx")


# ─── 配置 ───

DEFAULT_WATCHLIST = "005930,000660,035420,035720,373220,068270,051910,006400"

STOCK_NAMES = {
    "005930": "삼성전자", "000660": "SK하이닉스", "035420": "NAVER",
    "035720": "카카오", "373220": "LG에너지솔루션", "068270": "셀트리온",
    "051910": "LG화학", "006400": "삼성SDI", "005380": "현대자동차",
    "000270": "기아", "096770": "SK이노베이션", "034020": "두산에너빌리티",
    "003670": "포스코인터내셔널", "012330": "현대모비스", "028260": "삼성물산",
    "015760": "한국전력", "030200": "KT", "009150": "삼성전기",
    "066570": "LG전자", "003490": "대한항공", "036570": "엔씨소프트",
    "352820": "하이브", "090430": "아모레퍼시픽",
    "069500": "KODEX 200", "229200": "KODEX 코스닥150",
}

INDEX_ETFS = {
    "KOSPI": {"ticker": "069500", "name": "KODEX 200"},
    "KOSDAQ": {"ticker": "229200", "name": "KODEX 코스닥150"},
}


# ─── 데이터 수집 ───

def find_trading_date(target=None):
    """최근 거래일 찾기"""
    dt = datetime.datetime.strptime(target, "%Y-%m-%d") if target else datetime.datetime.now()
    for i in range(10):
        d = dt - datetime.timedelta(days=i)
        ds = d.strftime("%Y%m%d")
        try:
            df = krx.get_market_ohlcv(ds, ds, "005930")
            if df is not None and len(df) > 0 and float(df.iloc[0]["거래량"]) > 0:
                return d.strftime("%Y-%m-%d")
        except:
            continue
    return dt.strftime("%Y-%m-%d")


def _resolve_stock_name(ticker):
    """종목명 조회: STOCK_NAMES → KRX API fallback"""
    name = STOCK_NAMES.get(ticker)
    if name:
        return name
    try:
        name = krx.get_market_ticker_name(ticker)
        if name:
            STOCK_NAMES[ticker] = name  # 캐시
            return name
    except:
        pass
    return ticker


def get_stock(ticker, date_str):
    """단일 종목 OHLCV + 변동률"""
    d = date_str.replace("-", "")
    start = (datetime.datetime.strptime(date_str, "%Y-%m-%d") - datetime.timedelta(days=7)).strftime("%Y%m%d")
    try:
        df = krx.get_market_ohlcv(start, d, ticker)
        if df is None or len(df) < 1:
            return None
        cur = df.iloc[-1]
        prev = df.iloc[-2] if len(df) >= 2 else cur
        close = float(cur["종가"])
        prev_c = float(prev["종가"])
        chg = ((close - prev_c) / prev_c * 100) if prev_c else 0
        return {
            "ticker": ticker,
            "name": _resolve_stock_name(ticker),
            "close": int(close),
            "change_pct": round(chg, 2),
            "volume": int(cur["거래량"]),
        }
    except:
        return None


def fetch_all(date_str, watchlist_tickers):
    """전체 데이터 수집"""
    result = {"date": date_str, "indices": {}, "watchlist": [], "all_stocks": []}

    # 지수
    for name, etf in INDEX_ETFS.items():
        data = get_stock(etf["ticker"], date_str)
        if data:
            result["indices"][name] = data

    # 관심종목 + 주요종목
    all_tickers = list(set(watchlist_tickers + list(STOCK_NAMES.keys())))
    all_tickers = [t for t in all_tickers if t not in ["069500", "229200"]]

    for ticker in all_tickers:
        data = get_stock(ticker, date_str)
        if data and data["volume"] > 0:
            result["all_stocks"].append(data)
            if ticker in watchlist_tickers:
                result["watchlist"].append(data)
        time.sleep(0.08)

    result["all_stocks"].sort(key=lambda x: x["change_pct"], reverse=True)
    # 상승 TOP: 실제 상승(>0%)만, 하락 TOP: 실제 하락(<0%)만
    result["gainers"] = [s for s in result["all_stocks"] if s["change_pct"] > 0][:5]
    result["losers"] = [s for s in result["all_stocks"] if s["change_pct"] < 0][-5:][::-1]

    return result


# ─── 포맷팅 ───

def fmt_arrow(pct):
    if pct > 0: return "🟢"
    if pct < 0: return "🔴"
    return "⚪"


def format_briefing(data, paid=False):
    """텔레그램/왓츠앱 포맷 출력"""
    lines = []
    lines.append(f"📊 *한국 증시 시황 — {data['date']}*")
    lines.append("")

    # 지수
    lines.append("*지수 마감*")
    for name, d in data["indices"].items():
        a = fmt_arrow(d["change_pct"])
        lines.append(f"{a} {name}: {d['close']:,} ({d['change_pct']:+.1f}%)")
    lines.append("")

    # 관심종목
    if data["watchlist"]:
        lines.append("*관심 종목*")
        for d in data["watchlist"]:
            a = fmt_arrow(d["change_pct"])
            lines.append(f"{a} {d['name']}: ₩{d['close']:,} ({d['change_pct']:+.1f}%)")
        lines.append("")

    # 상승 TOP
    lines.append("*상승 TOP 5*")
    for d in data["gainers"]:
        lines.append(f"🟢 {d['name']} {d['change_pct']:+.1f}%")

    lines.append("")
    lines.append("*하락 TOP 5*")
    for d in data["losers"]:
        lines.append(f"🔴 {d['name']} {d['change_pct']:+.1f}%")

    # AI 분석
    if paid:
        lines.append("")
        lines.append("*AI 분석*")
        lines.append("(Agent가 뉴스와 데이터를 종합하여 분석을 제공합니다)")

    return "\n".join(lines)


# ─── 메인 ───

def main():
    target = None
    json_mode = "--json" in sys.argv
    for arg in sys.argv[1:]:
        if not arg.startswith("-"):
            target = arg

    watchlist_str = os.environ.get("KOREA_STOCK_WATCHLIST", DEFAULT_WATCHLIST)
    watchlist = [t.strip() for t in watchlist_str.split(",") if t.strip()]

    print("🔍 데이터 수집 중...", file=sys.stderr)
    date_str = find_trading_date(target)
    print(f"📅 거래일: {date_str}", file=sys.stderr)

    data = fetch_all(date_str, watchlist)

    if json_mode:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(format_briefing(data))


if __name__ == "__main__":
    main()
