#!/usr/bin/env python3
"""
Mapulse — 원자재 & 귀금속 모듈
금, 은, 구리, 원유, 철광석, 리튬 등 원자재 시세 + 한국 증시 영향 분석

데이터: Yahoo Finance API (무료, 키 불필요)
"""

import requests
import json
import re
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}


# ═══════════════════════════════════════════
#  원자재 정의
# ═══════════════════════════════════════════

# 카테고리별 원자재 정의
COMMODITIES = {
    # ── 귀금속 Precious Metals ──
    "gold": {
        "ticker": "GC=F", "name_ko": "금", "name_zh": "黄金", "name_en": "Gold",
        "unit": "oz", "category": "precious_metal",
        "kr_impact": "금 상승 → 안전자산 선호 → 원화약세 → 외국인 이탈 가능",
        "kr_stocks": ["015760"],  # 한국전력 (방어주)
    },
    "silver": {
        "ticker": "SI=F", "name_ko": "은", "name_zh": "白银", "name_en": "Silver",
        "unit": "oz", "category": "precious_metal",
        "kr_impact": "은 상승 → 산업+안전 이중 수요 → 전자부품 원가 영향",
        "kr_stocks": ["009150"],  # 삼성전기
    },
    "platinum": {
        "ticker": "PL=F", "name_ko": "백금", "name_zh": "铂金", "name_en": "Platinum",
        "unit": "oz", "category": "precious_metal",
        "kr_impact": "백금 상승 → 자동차 촉매 원가↑ → 현대·기아 영향",
        "kr_stocks": ["005380", "000270"],
    },
    "palladium": {
        "ticker": "PA=F", "name_ko": "팔라듐", "name_zh": "钯金", "name_en": "Palladium",
        "unit": "oz", "category": "precious_metal",
        "kr_impact": "팔라듐 상승 → 배기가스 촉매 비용↑ → 자동차 산업 영향",
        "kr_stocks": ["005380", "000270"],
    },

    # ── 에너지 Energy ──
    "oil_wti": {
        "ticker": "CL=F", "name_ko": "WTI 원유", "name_zh": "WTI原油", "name_en": "WTI Crude",
        "unit": "bbl", "category": "energy",
        "kr_impact": "유가↑ → 정유사 수혜, 항공·화학 비용↑, 소비위축",
        "kr_stocks": ["096770", "003490"],  # SK이노, 대한항공
    },
    "oil_brent": {
        "ticker": "BZ=F", "name_ko": "브렌트 원유", "name_zh": "布伦特原油", "name_en": "Brent Crude",
        "unit": "bbl", "category": "energy",
        "kr_impact": "국제유가 기준 → 한국 수입 원가 직결",
        "kr_stocks": ["096770"],
    },
    "natural_gas": {
        "ticker": "NG=F", "name_ko": "천연가스", "name_zh": "天然气", "name_en": "Natural Gas",
        "unit": "MMBtu", "category": "energy",
        "kr_impact": "가스↑ → 발전비용↑ → 한전 적자 확대 / LNG선사 수혜",
        "kr_stocks": ["015760"],
    },

    # ── 산업금속 Industrial Metals ──
    "copper": {
        "ticker": "HG=F", "name_ko": "구리", "name_zh": "铜", "name_en": "Copper",
        "unit": "lb", "category": "industrial_metal",
        "kr_impact": "구리 상승 → 경기회복 신호 + 전선/PCB 원가↑",
        "kr_stocks": ["009150", "066570"],  # 삼성전기, LG전자
    },
    "aluminum": {
        "ticker": "ALI=F", "name_ko": "알루미늄", "name_zh": "铝", "name_en": "Aluminum",
        "unit": "lb", "category": "industrial_metal",
        "kr_impact": "알루미늄↑ → 전자제품·자동차 경량화 부품 원가↑",
        "kr_stocks": ["066570", "005380"],
    },

    # ── 배터리/EV 원자재 Battery Metals ──
    "lithium_etf": {
        "ticker": "LIT", "name_ko": "리튬·배터리 ETF", "name_zh": "锂电池ETF", "name_en": "Lithium & Battery ETF",
        "unit": "", "category": "battery_metal",
        "kr_impact": "리튬 상승 → 배터리 원가↑ / 리튬 채굴·가공 기업 수혜",
        "kr_stocks": ["373220", "006400", "051910"],  # LG에너지, 삼성SDI, LG화학
    },

    # ── 철강/광물 Mining ──
    "iron_bhp": {
        "ticker": "BHP", "name_ko": "철광석 (BHP)", "name_zh": "铁矿石(BHP)", "name_en": "Iron Ore (BHP proxy)",
        "unit": "", "category": "mining",
        "kr_impact": "철광석↑ → 포스코 원가↑ but 가격전가 가능",
        "kr_stocks": ["003670"],  # 포스코인터내셔널
    },
    "steel_etf": {
        "ticker": "SLX", "name_ko": "철강 ETF", "name_zh": "钢铁ETF", "name_en": "Steel ETF",
        "unit": "", "category": "mining",
        "kr_impact": "철강 경기 → 건설·조선 연동",
        "kr_stocks": ["003670"],
    },

    # ── 환율 FX ──
    "usdkrw": {
        "ticker": "USDKRW=X", "name_ko": "달러/원 환율", "name_zh": "美元/韩元", "name_en": "USD/KRW",
        "unit": "₩", "category": "fx",
        "kr_impact": "환율↑ → 수출기업 수혜 / 외국인 투자 부담↑",
        "kr_stocks": ["005930", "000660"],
    },
}

# 별명 매핑 (다국어)
COMMODITY_ALIASES = {
    # 한국어
    "금": "gold", "골드": "gold", "금값": "gold", "금시세": "gold",
    "은": "silver", "실버": "silver", "은값": "silver",
    "백금": "platinum", "플래티넘": "platinum",
    "팔라듐": "palladium",
    "원유": "oil_wti", "유가": "oil_wti", "오일": "oil_wti", "wti": "oil_wti",
    "브렌트": "oil_brent", "brent": "oil_brent",
    "천연가스": "natural_gas", "가스": "natural_gas",
    "구리": "copper", "동": "copper", "코퍼": "copper",
    "알루미늄": "aluminum",
    "리튬": "lithium_etf", "배터리원자재": "lithium_etf",
    "철광석": "iron_bhp", "철": "iron_bhp",
    "철강": "steel_etf",
    "환율": "usdkrw", "달러": "usdkrw", "원달러": "usdkrw",

    # 中文
    "黄金": "gold", "金价": "gold", "金": "gold",
    "白银": "silver", "银": "silver", "银价": "silver",
    "铂金": "platinum",
    "钯金": "palladium",
    "原油": "oil_wti", "油价": "oil_wti", "石油": "oil_wti",
    "布伦特": "oil_brent",
    "天然气": "natural_gas",
    "铜": "copper", "铜价": "copper",
    "铝": "aluminum",
    "锂": "lithium_etf", "锂电池": "lithium_etf",
    "铁矿石": "iron_bhp", "铁矿": "iron_bhp", "铁": "iron_bhp",
    "钢铁": "steel_etf",
    "汇率": "usdkrw", "美元": "usdkrw", "韩元": "usdkrw",
    "矿": "all_metals", "矿物": "all_metals", "矿物质": "all_metals",
    "贵金属": "precious_metals", "贵金": "precious_metals",

    # English
    "gold": "gold", "silver": "silver", "platinum": "platinum",
    "palladium": "palladium", "oil": "oil_wti", "crude": "oil_wti",
    "copper": "copper", "aluminum": "aluminum", "aluminium": "aluminum",
    "lithium": "lithium_etf", "iron": "iron_bhp", "steel": "steel_etf",
    "forex": "usdkrw", "fx": "usdkrw",
}

# 카테고리 한글명
CATEGORY_NAMES = {
    "precious_metal": {"ko": "귀금속", "zh": "贵金属", "en": "Precious Metals"},
    "energy": {"ko": "에너지", "zh": "能源", "en": "Energy"},
    "industrial_metal": {"ko": "산업금속", "zh": "工业金属", "en": "Industrial Metals"},
    "battery_metal": {"ko": "배터리 원자재", "zh": "电池原材料", "en": "Battery Metals"},
    "mining": {"ko": "광업/철강", "zh": "矿业/钢铁", "en": "Mining/Steel"},
    "fx": {"ko": "환율", "zh": "汇率", "en": "Forex"},
}


# ═══════════════════════════════════════════
#  데이터 수집
# ═══════════════════════════════════════════

def fetch_commodity(key):
    """단일 원자재 시세 조회 (Yahoo Finance)"""
    info = COMMODITIES.get(key)
    if not info:
        return None

    try:
        resp = requests.get(
            f"https://query1.finance.yahoo.com/v8/finance/chart/{info['ticker']}",
            params={"interval": "1d", "range": "5d"},
            headers=HEADERS, timeout=10,
        )
        if resp.status_code != 200:
            return None

        data = resp.json()["chart"]["result"][0]
        meta = data["meta"]
        price = meta.get("regularMarketPrice", 0)
        prev = meta.get("chartPreviousClose", 0)
        chg_pct = ((price - prev) / prev * 100) if prev else 0
        chg_abs = price - prev

        # 5일 히스토리
        closes = data.get("indicators", {}).get("quote", [{}])[0].get("close", [])
        closes = [c for c in closes if c is not None]

        return {
            "key": key,
            "ticker": info["ticker"],
            "name_ko": info["name_ko"],
            "name_zh": info["name_zh"],
            "name_en": info["name_en"],
            "price": price,
            "prev_close": prev,
            "change_pct": round(chg_pct, 2),
            "change_abs": round(chg_abs, 2),
            "currency": meta.get("currency", "USD"),
            "unit": info.get("unit", ""),
            "category": info["category"],
            "kr_impact": info["kr_impact"],
            "kr_stocks": info.get("kr_stocks", []),
            "history_5d": closes[-5:] if closes else [],
            "market_state": meta.get("marketState", ""),
        }
    except Exception as e:
        return None


def fetch_category(category):
    """카테고리별 원자재 시세"""
    results = []
    for key, info in COMMODITIES.items():
        if info["category"] == category:
            data = fetch_commodity(key)
            if data:
                results.append(data)
    return results


def fetch_all_commodities():
    """전체 원자재 시세"""
    results = []
    for key in COMMODITIES:
        data = fetch_commodity(key)
        if data:
            results.append(data)
    return results


# ═══════════════════════════════════════════
#  해석 (resolve)
# ═══════════════════════════════════════════

def resolve_commodity(text):
    """텍스트에서 원자재 식별

    Returns:
        ("single", key) - 단일 원자재
        ("category", cat_name) - 카테고리 전체
        ("all", None) - 전체
        (None, None) - 매칭 실패
    """
    t = text.lower().strip()

    # 전체 조회 키워드
    if any(w in t for w in ["전체", "모든", "원자재", "전부", "commodities", "all",
                             "全部", "所有", "大宗商品", "원자재 시세"]):
        return ("all", None)

    # 카테고리 키워드
    if any(w in t for w in ["귀금속", "贵金属", "precious"]):
        return ("category", "precious_metal")
    if any(w in t for w in ["에너지", "能源", "energy"]):
        return ("category", "energy")
    if any(w in t for w in ["산업금속", "공업금속", "工业金属", "industrial metal"]):
        return ("category", "industrial_metal")
    if any(w in t for w in ["배터리", "电池", "battery"]):
        return ("category", "battery_metal")
    if any(w in t for w in ["광업", "铁", "mining", "矿业", "矿物", "矿物质", "矿"]):
        return ("category", "mining")

    # 별명 매칭
    for alias, key in COMMODITY_ALIASES.items():
        if alias in t:
            if key == "all_metals":
                return ("all", None)
            if key == "precious_metals":
                return ("category", "precious_metal")
            return ("single", key)

    return (None, None)


# ═══════════════════════════════════════════
#  포맷팅
# ═══════════════════════════════════════════

def _arrow(pct):
    if pct > 0: return "🟢"
    if pct < 0: return "🔴"
    return "⚪"


def _name(data, lang="zh"):
    """언어별 이름"""
    if lang == "ko": return data["name_ko"]
    if lang == "en": return data["name_en"]
    return data["name_zh"]


def _trend(history):
    """5일 추세 시각화"""
    if len(history) < 2:
        return ""
    first, last = history[0], history[-1]
    if last > first * 1.02:
        return "📈"
    elif last < first * 0.98:
        return "📉"
    return "➡️"


def format_single(data, lang="zh"):
    """단일 원자재 상세"""
    a = _arrow(data["change_pct"])
    n = _name(data, lang)
    unit_str = f"/{data['unit']}" if data["unit"] else ""
    trend = _trend(data["history_5d"])

    lines = [
        f"{a} *{n}* ({data['ticker']})",
        f"💰 ${data['price']:,.2f}{unit_str} ({data['change_pct']:+.2f}%) {trend}",
    ]

    # 5일 히스토리
    if data["history_5d"]:
        hist_str = " → ".join([f"${p:,.0f}" for p in data["history_5d"]])
        lines.append(f"📊 5일: {hist_str}")

    # 한국 증시 영향
    lines.append(f"\n🇰🇷 *한국 영향:* {data['kr_impact']}")

    if data["kr_stocks"]:
        from fetch_briefing import STOCK_NAMES
        stocks = [STOCK_NAMES.get(t, t) for t in data["kr_stocks"]]
        lines.append(f"📌 관련 종목: {', '.join(stocks)}")

    return "\n".join(lines)


def format_category(data_list, category, lang="zh"):
    """카테고리별 원자재 요약"""
    cat_name = CATEGORY_NAMES.get(category, {}).get(lang, category)
    lines = [f"📊 *{cat_name}*", ""]

    for d in data_list:
        a = _arrow(d["change_pct"])
        n = _name(d, lang)
        unit_str = f"/{d['unit']}" if d["unit"] else ""
        trend = _trend(d["history_5d"])
        lines.append(f"{a} {n}: ${d['price']:,.2f}{unit_str} ({d['change_pct']:+.2f}%) {trend}")

    return "\n".join(lines)


def format_all(all_data, lang="zh"):
    """전체 원자재 대시보드"""
    header = {
        "ko": "🌍 *원자재 시황 대시보드*",
        "zh": "🌍 *大宗商品行情*",
        "en": "🌍 *Commodities Dashboard*",
    }.get(lang, "🌍 *大宗商品行情*")

    lines = [header, f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]

    # 그룹별 출력
    by_cat = {}
    for d in all_data:
        cat = d["category"]
        by_cat.setdefault(cat, []).append(d)

    cat_order = ["precious_metal", "energy", "industrial_metal", "battery_metal", "mining", "fx"]
    for cat in cat_order:
        items = by_cat.get(cat, [])
        if not items:
            continue
        cat_name = CATEGORY_NAMES.get(cat, {}).get(lang, cat)
        lines.append(f"*{cat_name}:*")
        for d in items:
            a = _arrow(d["change_pct"])
            n = _name(d, lang)
            unit_str = f"/{d['unit']}" if d["unit"] else ""
            trend = _trend(d["history_5d"])
            lines.append(f"  {a} {n}: ${d['price']:,.2f}{unit_str} ({d['change_pct']:+.2f}%) {trend}")
        lines.append("")

    # 핵심 영향 분석
    big_movers = [d for d in all_data if abs(d["change_pct"]) > 3]
    if big_movers:
        lines.append("*⚡ 급변 원자재 (3%+):*")
        for d in sorted(big_movers, key=lambda x: abs(x["change_pct"]), reverse=True):
            a = _arrow(d["change_pct"])
            n = _name(d, lang)
            lines.append(f"  {a} {n} {d['change_pct']:+.2f}% → {d['kr_impact']}")
        lines.append("")

    disclaimer = {
        "ko": "_⚠️ 시세는 15~20분 지연될 수 있습니다._",
        "zh": "_⚠️ 行情可能有15-20分钟延迟。_",
        "en": "_⚠️ Prices may be delayed 15-20 minutes._",
    }.get(lang, "_⚠️ 行情可能有15-20分钟延迟。_")
    lines.append(disclaimer)

    return "\n".join(lines)


# ═══════════════════════════════════════════
#  통합 쿼리 인터페이스
# ═══════════════════════════════════════════

def query_commodity(text, lang="zh"):
    """원자재 자연어 쿼리 처리

    Returns: (result_text, was_handled)
    """
    mode, key = resolve_commodity(text)

    if mode == "single" and key:
        data = fetch_commodity(key)
        if data:
            return format_single(data, lang), True
        return f"❌ {key} 데이터를 가져올 수 없습니다.", True

    elif mode == "category" and key:
        data_list = fetch_category(key)
        if data_list:
            return format_category(data_list, key, lang), True
        return f"❌ {key} 카테고리 데이터를 가져올 수 없습니다.", True

    elif mode == "all":
        all_data = fetch_all_commodities()
        if all_data:
            return format_all(all_data, lang), True
        return "❌ 원자재 데이터를 가져올 수 없습니다.", True

    return "", False


# ═══════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 55)
    print("🌍 Mapulse Commodities Module")
    print("=" * 55)

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        result, handled = query_commodity(query)
        if handled:
            print(result)
        else:
            print(f"❌ 인식할 수 없는 원자재: {query}")
    else:
        # 전체 대시보드
        print("\n데이터 수집 중...")
        all_data = fetch_all_commodities()
        print(format_all(all_data, "zh"))
