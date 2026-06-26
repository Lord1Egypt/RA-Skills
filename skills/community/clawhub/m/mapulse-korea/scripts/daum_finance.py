#!/usr/bin/env python3
"""
Mapulse — Daum Finance API 数据源
已验证可用的7个Daum API端点

数据:
  1. 个股全量数据 (市值/PER/PBR/外资/52周/行业/财务)
  2. 批量查询 (一次最多20个)
  3. 日K线历史
  4. KOSPI/KOSDAQ 真实指数 + 投资者别
  5. 全市场投资者别净买入
  6. WICS 行业分类 + 涨跌
  7. 实时热搜排名
"""

import requests
import json

DAUM_BASE = "https://finance.daum.net/api"
DAUM_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://finance.daum.net",
}


# ──────────────────────────────────────────────
# 1. 个股全量数据
# ──────────────────────────────────────────────

def fetch_daum_stock(ticker):
    """개별 종목 전체 데이터 — 한 번의 요청으로 50+ 필드
    
    Returns dict with keys:
      name, market, tradePrice, changeRate, changePrice, change,
      marketCap, marketCapRank, foreignRatio,
      eps, bps, dps, per, pbr, debtRatio,
      high52wPrice, high52wDate, low52wPrice, low52wDate,
      wicsSectorCode, wicsSectorName, wicsSectorChangeRate,
      sales, operatingProfit, netIncome,
      companySummary, accTradeVolume, accTradePrice,
      openingPrice, highPrice, lowPrice,
      listedShareCount, parValue, listingDate,
      upperLimitPrice, lowerLimitPrice,
      prevClosingPrice, marketStatus
    """
    try:
        r = requests.get(
            f"{DAUM_BASE}/quotes/A{ticker}",
            headers=DAUM_HEADERS,
            timeout=8,
        )
        if r.status_code != 200:
            return None
        d = r.json()
        if "symbolCode" not in d:
            return None
        return d
    except Exception:
        return None


# ──────────────────────────────────────────────
# 2. 批量查询
# ──────────────────────────────────────────────

def fetch_daum_batch(tickers):
    """여러 종목 일괄 조회 (최대 20개/회)
    
    Returns list of quote dicts, or empty list on failure.
    """
    if not tickers:
        return []
    try:
        codes = ",".join([f"A{t}" for t in tickers[:20]])
        r = requests.get(
            f"{DAUM_BASE}/quotesv4?codes={codes}",
            headers=DAUM_HEADERS,
            timeout=10,
        )
        if r.status_code != 200:
            return []
        d = r.json()
        return d.get("quotes", [])
    except Exception:
        return []


# ──────────────────────────────────────────────
# 3. 日K线
# ──────────────────────────────────────────────

def fetch_daum_chart(ticker, days=10):
    """일봉 차트 데이터
    
    Returns list of dicts with:
      date, tradePrice, openingPrice, highPrice, lowPrice,
      change, changePrice, changeRate,
      candleAccTradeVolume, candleAccTradePrice
    """
    try:
        headers = dict(DAUM_HEADERS)
        headers["Referer"] = f"https://finance.daum.net/quotes/A{ticker}"
        r = requests.get(
            f"{DAUM_BASE}/charts/A{ticker}/days?limit={days}&adjusted=true",
            headers=headers,
            timeout=8,
        )
        if r.status_code != 200:
            return []
        d = r.json()
        return d.get("data", [])
    except Exception:
        return []


# ──────────────────────────────────────────────
# 4. KOSPI/KOSDAQ 真实指数
# ──────────────────────────────────────────────

def fetch_daum_indices():
    """KOSPI/KOSDAQ 실제 지수 + 투자자별 순매수
    
    Returns dict:
      { "KOSPI": [{date, tradePrice, change, changePrice, accTradeVolume,
                    individualStraightPurchasePrice, foreignStraightPurchasePrice,
                    institutionStraightPurchasePrice}],
        "KOSDAQ": [...] }
    """
    try:
        headers = dict(DAUM_HEADERS)
        headers["Referer"] = "https://finance.daum.net/domestic"
        r = requests.get(
            f"{DAUM_BASE}/domestic/trend/market/indexes",
            headers=headers,
            timeout=8,
        )
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


# ──────────────────────────────────────────────
# 5. 全市场投资者别
# ──────────────────────────────────────────────

def fetch_daum_investors():
    """전 시장 투자자별 순매수 (외국인/기관/개인/프로그램)
    
    Returns dict:
      { "KOSPI": [{date, individualStraightPurchasePrice, foreignStraightPurchasePrice,
                    institutionStraightPurchasePrice, programStraightPurchasePrice}],
        "KOSDAQ": [...] }
    """
    try:
        headers = dict(DAUM_HEADERS)
        headers["Referer"] = "https://finance.daum.net/domestic"
        r = requests.get(
            f"{DAUM_BASE}/domestic/trend/market/investors",
            headers=headers,
            timeout=8,
        )
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


# ──────────────────────────────────────────────
# 6. WICS 行业分类
# ──────────────────────────────────────────────

def fetch_daum_sectors():
    """WICS 업종 분류 + 등락률 + 구성 종목
    
    Returns list of dicts:
      [{sectorCode, sectorName, changeRate, stockCount,
        accTradeVolume, accTradePrice,
        includedStocks: [{name, symbolCode, change, changeRate, tradePrice, marketCap, foreignRatio}]}]
    """
    try:
        headers = dict(DAUM_HEADERS)
        headers["Referer"] = "https://finance.daum.net/domestic"
        r = requests.get(
            f"{DAUM_BASE}/sector/wics",
            headers=headers,
            timeout=8,
        )
        if r.status_code != 200:
            return []
        d = r.json()
        return d.get("data", [])
    except Exception:
        return []


# ──────────────────────────────────────────────
# 7. 热搜排名
# ──────────────────────────────────────────────

def fetch_daum_hot_ranks():
    """실시간 검색 순위
    
    Returns list of dicts:
      [{rank, rankChange, name, symbolCode, tradePrice, change, changeRate, 
        accTradeVolume, accTradePrice, isNew}]
    """
    try:
        r = requests.get(
            f"{DAUM_BASE}/search/ranks",
            headers=DAUM_HEADERS,
            timeout=8,
        )
        if r.status_code != 200:
            return []
        d = r.json()
        return d.get("data", [])
    except Exception:
        return []


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _fmt_krw(value):
    """숫자를 한국 원화 표시 (조/억 단위)"""
    if value is None:
        return "-"
    try:
        v = float(value)
    except (ValueError, TypeError):
        return str(value)
    if abs(v) >= 1e12:
        return f"{v/1e12:,.1f}조"
    if abs(v) >= 1e8:
        return f"{v/1e8:,.0f}억"
    if abs(v) >= 1e4:
        return f"{v/1e4:,.0f}만"
    return f"{v:,.0f}"


def _fmt_pct(value):
    """비율을 퍼센트로 변환 (0.04 → +4.00%)"""
    if value is None:
        return "-"
    try:
        v = float(value) * 100
        return f"{v:+.2f}%"
    except (ValueError, TypeError):
        return str(value)


def _change_emoji(change_str):
    """Daum change 필드 → 이모지"""
    if change_str == "RISE":
        return "🔴📈"
    elif change_str == "FALL":
        return "🔵📉"
    else:
        return "⚪"


def _pct_emoji(rate):
    """변동률 → 이모지"""
    if rate is None:
        return "⚪"
    try:
        v = float(rate)
        if v > 0:
            return "🔴📈"
        elif v < 0:
            return "🔵📉"
        return "⚪"
    except:
        return "⚪"


# ──────────────────────────────────────────────
# Formatters
# ──────────────────────────────────────────────

def format_daum_stock(data, lang="ko"):
    """포맷: 개별 종목 상세 (시총/PER/PBR/52주/외국인/업종)"""
    if not data:
        return ""

    name = data.get("name", "")
    ticker = str(data.get("symbolCode", "")).replace("A", "")
    price = data.get("tradePrice")
    change_rate = data.get("changeRate")
    emoji = _change_emoji(data.get("change", ""))

    lines = [f"{emoji} *{name} ({ticker})*"]

    # 가격
    if price is not None:
        lines.append(f"💰 {price:,.0f}원 ({_fmt_pct(change_rate)})")

    # 시가총액 + 순위
    mcap = data.get("marketCap")
    rank = data.get("marketCapRank")
    if mcap:
        rank_str = f" (#{rank})" if rank else ""
        lines.append(f"📊 시총: {_fmt_krw(mcap)}{rank_str}")

    # PER / PBR / EPS
    per = data.get("per")
    pbr = data.get("pbr")
    eps = data.get("eps")
    bps = data.get("bps")
    vals = []
    if per:
        vals.append(f"PER {per}")
    if pbr:
        vals.append(f"PBR {pbr}")
    if eps:
        vals.append(f"EPS {eps:,.0f}")
    if vals:
        lines.append(f"📈 {' | '.join(vals)}")

    # 배당
    dps = data.get("dps")
    if dps and price:
        div_yield = dps / price * 100
        lines.append(f"💎 배당: {dps:,.0f}원 ({div_yield:.2f}%)")

    # 외국인
    fr = data.get("foreignRatio")
    if fr is not None:
        lines.append(f"🌍 외국인: {fr*100:.2f}%")

    # 52주 범위
    h52 = data.get("high52wPrice")
    l52 = data.get("low52wPrice")
    if h52 and l52 and price:
        range_pct = (price - l52) / (h52 - l52) * 100 if h52 != l52 else 50
        bar_len = 10
        filled = max(0, min(bar_len, int(range_pct / 100 * bar_len)))
        bar = "▓" * filled + "░" * (bar_len - filled)
        lines.append(f"📐 52주: {l52:,.0f} [{bar}] {h52:,.0f}")

    # 업종
    sector = data.get("wicsSectorName")
    sector_rate = data.get("wicsSectorChangeRate")
    if sector:
        sr = f" ({_fmt_pct(sector_rate)})" if sector_rate is not None else ""
        lines.append(f"🏭 업종: {sector}{sr}")

    # 부채비율
    debt = data.get("debtRatio")
    if debt is not None:
        lines.append(f"💳 부채비율: {debt*100:.1f}%")

    # 다국어 변환 (간단한 키 변환)
    if lang == "zh":
        replacements = {
            "시총": "市值", "배당": "股息", "외국인": "外资",
            "업종": "行业", "부채비율": "负债率",
        }
        result = "\n".join(lines)
        for ko, zh in replacements.items():
            result = result.replace(ko, zh)
        return result
    elif lang == "en":
        replacements = {
            "시총": "MCap", "배당": "Div", "외국인": "Foreign",
            "업종": "Sector", "부채비율": "Debt Ratio",
        }
        result = "\n".join(lines)
        for ko, en in replacements.items():
            result = result.replace(ko, en)
        return result

    return "\n".join(lines)


def format_daum_indices(data, lang="ko"):
    """포맷: KOSPI/KOSDAQ 실제 지수 + 투자자별"""
    if not data:
        return ""

    title = {"ko": "📊 **지수 현황**", "zh": "📊 **指数行情**", "en": "📊 **Index Overview**"}.get(lang, "📊 **지수 현황**")
    lines = [title, ""]

    for market in ["KOSPI", "KOSDAQ"]:
        entries = data.get(market, [])
        if not entries:
            continue
        latest = entries[0]
        price = latest.get("tradePrice", 0)
        change = latest.get("change", "")
        change_price = latest.get("changePrice", 0)
        emoji = _change_emoji(change)

        sign = "+" if change == "RISE" else "-" if change == "FALL" else ""
        pct = (change_price / (price - change_price) * 100) if price != change_price else 0

        lines.append(f"{emoji} **{market}**: {price:,.2f} ({sign}{change_price:,.2f} / {sign}{abs(pct):.2f}%)")

        # 투자자별
        foreign = latest.get("foreignStraightPurchasePrice", 0)
        inst = latest.get("institutionStraightPurchasePrice", 0)
        indiv = latest.get("individualStraightPurchasePrice", 0)

        f_emoji = "🟢" if foreign and foreign > 0 else "🔴" if foreign and foreign < 0 else "⚪"
        i_emoji = "🟢" if inst and inst > 0 else "🔴" if inst and inst < 0 else "⚪"
        p_emoji = "🟢" if indiv and indiv > 0 else "🔴" if indiv and indiv < 0 else "⚪"

        if lang == "ko":
            lines.append(f"  {f_emoji} 외국인: {_fmt_krw(foreign)} | {i_emoji} 기관: {_fmt_krw(inst)} | {p_emoji} 개인: {_fmt_krw(indiv)}")
        elif lang == "zh":
            lines.append(f"  {f_emoji} 外资: {_fmt_krw(foreign)} | {i_emoji} 机构: {_fmt_krw(inst)} | {p_emoji} 散户: {_fmt_krw(indiv)}")
        else:
            lines.append(f"  {f_emoji} Foreign: {_fmt_krw(foreign)} | {i_emoji} Inst: {_fmt_krw(inst)} | {p_emoji} Indiv: {_fmt_krw(indiv)}")
        lines.append("")

    return "\n".join(lines)


def format_daum_sectors(data, lang="ko", top_n=5):
    """포맷: 업종 등락 랭킹"""
    if not data:
        return ""

    title = {"ko": "🏭 **업종 등락 현황**", "zh": "🏭 **行业涨跌排行**", "en": "🏭 **Sector Performance**"}.get(lang, "🏭 **업종 등락 현황**")
    lines = [title, ""]

    # 등락률 기준 정렬
    sorted_sectors = sorted(data, key=lambda x: x.get("changeRate", 0) or 0, reverse=True)

    # 상승 TOP
    risers = [s for s in sorted_sectors if (s.get("changeRate") or 0) > 0][:top_n]
    fallers = [s for s in reversed(sorted_sectors) if (s.get("changeRate") or 0) < 0][:top_n]

    if risers:
        rise_label = {"ko": "*상승 업종*", "zh": "*上涨行业*", "en": "*Rising Sectors*"}.get(lang, "*상승 업종*")
        lines.append(rise_label)
        for s in risers:
            name = s.get("sectorName", "")
            rate = s.get("changeRate", 0)
            count = s.get("stockCount", 0)
            # 대표 종목
            top_stocks = s.get("includedStocks", [])[:2]
            top_str = ", ".join([ts.get("name", "") for ts in top_stocks])
            lines.append(f"  🟢 {name} {_fmt_pct(rate)} ({count}종목) — {top_str}")

    if fallers:
        lines.append("")
        fall_label = {"ko": "*하락 업종*", "zh": "*下跌行业*", "en": "*Falling Sectors*"}.get(lang, "*하락 업종*")
        lines.append(fall_label)
        for s in fallers:
            name = s.get("sectorName", "")
            rate = s.get("changeRate", 0)
            count = s.get("stockCount", 0)
            top_stocks = s.get("includedStocks", [])[:2]
            top_str = ", ".join([ts.get("name", "") for ts in top_stocks])
            lines.append(f"  🔴 {name} {_fmt_pct(rate)} ({count}종목) — {top_str}")

    return "\n".join(lines)


def format_daum_hot_ranks(data, lang="ko", top_n=10):
    """포맷: 실시간 검색 순위"""
    if not data:
        return ""

    title = {"ko": "🔥 **실시간 인기 종목**", "zh": "🔥 **实时热门股票**", "en": "🔥 **Trending Stocks**"}.get(lang, "🔥 **실시간 인기 종목**")
    lines = [title, ""]

    for item in data[:top_n]:
        rank = item.get("rank", "")
        name = item.get("name", "")
        price = item.get("tradePrice", 0)
        rate = item.get("changeRate", 0)
        change = item.get("change", "")
        rank_change = item.get("rankChange", 0)
        is_new = item.get("isNew", False)

        emoji = _change_emoji(change)

        # 순위 변동
        if is_new:
            rank_str = " 🆕"
        elif rank_change and rank_change > 0:
            rank_str = f" ▲{rank_change}"
        elif rank_change and rank_change < 0:
            rank_str = f" ▼{abs(rank_change)}"
        else:
            rank_str = ""

        lines.append(f"  {rank}. {emoji} {name}: {price:,.0f}원 ({_fmt_pct(rate)}){rank_str}")

    return "\n".join(lines)


# ──────────────────────────────────────────────
# Test
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  🇰🇷 Daum Finance API Test")
    print("=" * 60)

    print("\n=== 1. 삼성전자 개별 조회 ===")
    stock = fetch_daum_stock("005930")
    if stock:
        print(format_daum_stock(stock))
        print(f"\n  [raw keys: {len(stock)} fields]")
    else:
        print("  ❌ Failed")

    print("\n=== 2. 배치 조회 (삼성, 하이닉스, NAVER) ===")
    batch = fetch_daum_batch(["005930", "000660", "035420"])
    for q in batch:
        print(f"  {q.get('name')}: {q.get('tradePrice'):,.0f}원 ({_fmt_pct(q.get('changeRate'))}) 시총#{q.get('marketCapRank')}")

    print("\n=== 3. 삼성전자 일봉 (5일) ===")
    chart = fetch_daum_chart("005930", 5)
    for c in chart:
        print(f"  {c.get('date')}: {c.get('tradePrice'):,.0f}원 ({_fmt_pct(c.get('changeRate'))})")

    print("\n=== 4. KOSPI/KOSDAQ 지수 ===")
    indices = fetch_daum_indices()
    if indices:
        print(format_daum_indices(indices))
    else:
        print("  ❌ Failed")

    print("\n=== 5. 투자자별 ===")
    investors = fetch_daum_investors()
    if investors:
        for market in ["KOSPI", "KOSDAQ"]:
            entries = investors.get(market, [])
            if entries:
                latest = entries[0]
                print(f"  {market}: 외국인 {_fmt_krw(latest.get('foreignStraightPurchasePrice'))} | 기관 {_fmt_krw(latest.get('institutionStraightPurchasePrice'))}")
    else:
        print("  ❌ Failed")

    print("\n=== 6. WICS 업종 ===")
    sectors = fetch_daum_sectors()
    if sectors:
        print(format_daum_sectors(sectors, top_n=3))
    else:
        print("  ❌ Failed")

    print("\n=== 7. 인기 검색 ===")
    ranks = fetch_daum_hot_ranks()
    if ranks:
        print(format_daum_hot_ranks(ranks, top_n=5))
    else:
        print("  ❌ Failed")

    print("\n" + "=" * 60)
    print("  ✅ Daum Finance API Test Complete")
    print("=" * 60)
