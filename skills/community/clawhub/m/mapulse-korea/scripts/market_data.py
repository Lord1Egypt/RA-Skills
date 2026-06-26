"""
Mapulse Enhanced Market Data Sources
New data: exchange rate, VIX, Fear & Greed, global indices, 
          stock disclosure, financial summary, price history,
          sector comparison
"""

import requests
import json
import time
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


# ──────────────────────────────────────────────
# 1. Exchange Rates (환율)
# ──────────────────────────────────────────────

def fetch_exchange_rates():
    """주요 환율 (USD/KRW, USD/CNY, USD/JPY, EUR/USD)"""
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        rates = r.json().get("rates", {})
        return {
            "USD/KRW": rates.get("KRW"),
            "USD/CNY": rates.get("CNY"),
            "USD/JPY": rates.get("JPY"),
            "EUR/USD": round(1 / rates.get("EUR", 1), 4) if rates.get("EUR") else None,
            "updated": r.json().get("date"),
        }
    except:
        return None


# ──────────────────────────────────────────────
# 2. Fear & Greed Index (공포탐욕지수)
# ──────────────────────────────────────────────

def fetch_fear_greed():
    """Crypto Fear & Greed Index (0-100)"""
    try:
        r = requests.get("https://api.alternative.me/fng/?limit=7", timeout=5)
        data = r.json().get("data", [])
        if not data:
            return None
        current = data[0]
        return {
            "value": int(current["value"]),
            "label": current["value_classification"],
            "history": [{"value": int(d["value"]), "label": d["value_classification"]} for d in data[:7]],
        }
    except:
        return None


# ──────────────────────────────────────────────
# 3. VIX (변동성지수)
# ──────────────────────────────────────────────

def fetch_vix():
    """VIX from Google Finance scraping"""
    try:
        r = requests.get("https://www.google.com/finance/quote/VIX:INDEXCBOE", headers=HEADERS, timeout=5)
        m = re.search(r'data-last-price="([^"]+)"', r.text)
        if m:
            return {"value": float(m.group(1))}
    except:
        pass
    return None


# ──────────────────────────────────────────────
# 4. Global Indices (글로벌 지수)
# ──────────────────────────────────────────────

def fetch_kospi():
    """KOSPI 지수"""
    try:
        r = requests.get("https://m.stock.naver.com/api/index/KOSPI/basic", timeout=5)
        d = r.json()
        return {
            "name": "KOSPI",
            "price": d.get("closePrice"),
            "change": d.get("compareToPreviousClosePrice"),
            "change_pct": d.get("fluctuationsRatio"),
            "status": d.get("marketStatus"),
        }
    except:
        return None


def fetch_kosdaq():
    """KOSDAQ 지수"""
    try:
        r = requests.get("https://m.stock.naver.com/api/index/KOSDAQ/basic", timeout=5)
        d = r.json()
        return {
            "name": "KOSDAQ",
            "price": d.get("closePrice"),
            "change": d.get("compareToPreviousClosePrice"),
            "change_pct": d.get("fluctuationsRatio"),
            "status": d.get("marketStatus"),
        }
    except:
        return None


def fetch_us_indices():
    """S&P500 via Yahoo Finance"""
    try:
        r = requests.get(
            "https://query2.finance.yahoo.com/v8/finance/chart/%5EGSPC?range=1d&interval=1d",
            headers=HEADERS, timeout=5,
        )
        d = r.json()
        meta = d["chart"]["result"][0]["meta"]
        price = meta["regularMarketPrice"]
        prev = meta["previousClose"]
        return {
            "S&P500": {
                "price": round(price, 2),
                "prev": round(prev, 2),
                "change": round(price - prev, 2),
                "change_pct": round((price - prev) / prev * 100, 2),
            }
        }
    except:
        return None


def fetch_all_indices():
    """KOSPI + KOSDAQ + S&P500"""
    result = {}
    kospi = fetch_kospi()
    if kospi:
        result["KOSPI"] = kospi
    kosdaq = fetch_kosdaq()
    if kosdaq:
        result["KOSDAQ"] = kosdaq
    us = fetch_us_indices()
    if us:
        result.update(us)
    return result


# ──────────────────────────────────────────────
# 5. Stock Disclosure (공시)
# ──────────────────────────────────────────────

def fetch_disclosure(ticker, count=5):
    """종목 공시 (Naver)"""
    try:
        r = requests.get(
            f"https://m.stock.naver.com/api/stock/{ticker}/disclosure?page=1&size={count}",
            timeout=5,
        )
        data = r.json()
        if not isinstance(data, list):
            return []
        return [
            {
                "title": d.get("title", ""),
                "datetime": d.get("datetime", ""),
                "author": d.get("author", ""),
                "id": d.get("disclosureId"),
            }
            for d in data[:count]
        ]
    except:
        return []


# ──────────────────────────────────────────────
# 6. Financial Summary (재무요약)
# ──────────────────────────────────────────────

def fetch_financial_summary(ticker):
    """연간 재무 요약 (매출액, 영업이익, 순이익, PER, PBR)"""
    try:
        r = requests.get(
            f"https://m.stock.naver.com/api/stock/{ticker}/finance/annual",
            timeout=5,
        )
        d = r.json()
        info = d.get("financeInfo", {})
        periods = info.get("trTitleList", [])
        rows = info.get("rowList", [])

        result = {"periods": [p["title"] for p in periods], "data": {}}
        for row in rows:
            title = row.get("title", "")
            cols = row.get("columns", [])
            values = []
            for col in cols:
                val = col.get("value")
                values.append(val)
            if title and values:
                result["data"][title] = values
        return result
    except:
        return None


# ──────────────────────────────────────────────
# 7. Stock Basic Info (기본정보 확장)
# ──────────────────────────────────────────────

def fetch_stock_detail(ticker):
    """종목 상세 (시가총액, PER, PBR, 배당수익률, 외국인비율 등)"""
    try:
        r = requests.get(f"https://m.stock.naver.com/api/stock/{ticker}/basic", timeout=5)
        d = r.json()
        return {
            "name": d.get("stockName"),
            "price": d.get("closePrice"),
            "change": d.get("compareToPreviousClosePrice"),
            "change_pct": d.get("fluctuationsRatio"),
            "market_status": d.get("marketStatus"),
            "exchange": d.get("stockExchangeName"),
        }
    except:
        return None


# ──────────────────────────────────────────────
# 8. Price History (최근 시세)
# ──────────────────────────────────────────────

def fetch_price_history(ticker, days=10):
    """최근 n일 시세"""
    try:
        r = requests.get(
            f"https://m.stock.naver.com/api/stock/{ticker}/price?page=1&pageSize={days}",
            timeout=5,
        )
        data = r.json()
        if not isinstance(data, list):
            return []
        return [
            {
                "date": d.get("localTradedAt"),
                "close": d.get("closePrice"),
                "change": d.get("compareToPreviousClosePrice"),
                "change_pct": d.get("fluctuationsRatio"),
                "open": d.get("openPrice"),
                "high": d.get("highPrice"),
                "low": d.get("lowPrice"),
                "volume": d.get("accumulatedTradingVolume"),
            }
            for d in data[:days]
        ]
    except:
        return []


# ──────────────────────────────────────────────
# 9. Market Overview (시장 종합)
# ──────────────────────────────────────────────

def fetch_market_overview():
    """시장 종합: KOSPI + KOSDAQ + 환율 + VIX + Fear&Greed"""
    overview = {}

    indices = fetch_all_indices()
    if indices:
        overview["indices"] = indices

    fx = fetch_exchange_rates()
    if fx:
        overview["exchange_rates"] = fx

    vix = fetch_vix()
    if vix:
        overview["vix"] = vix

    fng = fetch_fear_greed()
    if fng:
        overview["fear_greed"] = fng

    return overview


# ──────────────────────────────────────────────
# Formatters
# ──────────────────────────────────────────────

def _arrow(val):
    """등락 화살표"""
    if val is None:
        return ""
    try:
        v = float(str(val).replace(",", "").replace("%", ""))
        if v > 0:
            return "🔴📈"
        elif v < 0:
            return "🔵📉"
        else:
            return "⚪"
    except:
        return ""


def format_market_overview(data, lang="ko"):
    """시장 종합 포맷"""
    lines = []

    if lang == "ko":
        lines.append("📊 **시장 종합**\n")
    elif lang == "zh":
        lines.append("📊 **市场总览**\n")
    else:
        lines.append("📊 **Market Overview**\n")

    # Indices
    indices = data.get("indices", {})
    for name, info in indices.items():
        if isinstance(info, dict):
            price = info.get("price", "")
            change_pct = info.get("change_pct", "")
            arrow = _arrow(change_pct)
            lines.append(f"{arrow} **{name}**: {price} ({change_pct}%)")

    # Exchange rates
    fx = data.get("exchange_rates", {})
    if fx:
        lines.append("")
        if lang == "ko":
            lines.append("💱 **환율**")
        elif lang == "zh":
            lines.append("💱 **汇率**")
        else:
            lines.append("💱 **Exchange Rates**")
        for pair in ["USD/KRW", "USD/CNY", "USD/JPY", "EUR/USD"]:
            if pair in fx and fx[pair]:
                lines.append(f"  {pair}: {fx[pair]:,.2f}")

    # VIX
    vix = data.get("vix", {})
    if vix:
        v = vix.get("value", 0)
        label = "🟢 Low" if v < 15 else "🟡 Normal" if v < 25 else "🟠 High" if v < 35 else "🔴 Extreme"
        lines.append(f"\n😱 **VIX**: {v:.1f} ({label})")

    # Fear & Greed
    fng = data.get("fear_greed", {})
    if fng:
        v = fng.get("value", 0)
        label = fng.get("label", "")
        emoji = "😱" if v < 25 else "😟" if v < 45 else "😐" if v < 55 else "😊" if v < 75 else "🤑"
        lines.append(f"{emoji} **Fear & Greed**: {v} ({label})")

    return "\n".join(lines)


def format_disclosure(disclosures, lang="ko"):
    """공시 포맷"""
    if not disclosures:
        return "공시 없음" if lang == "ko" else "无公告" if lang == "zh" else "No disclosures"

    title = "📋 **공시**" if lang == "ko" else "📋 **公告**" if lang == "zh" else "📋 **Disclosures**"
    lines = [title]
    for d in disclosures[:5]:
        dt = d.get("datetime", "")[:10]
        t = d.get("title", "")
        lines.append(f"• [{dt}] {t}")
    return "\n".join(lines)


def format_financial_summary(fin, lang="ko"):
    """재무요약 포맷"""
    if not fin:
        return ""

    title = "📈 **재무요약**" if lang == "ko" else "📈 **财务摘要**" if lang == "zh" else "📈 **Financial Summary**"
    lines = [title]

    periods = fin.get("periods", [])
    if periods:
        lines.append("  " + " | ".join(periods))

    data = fin.get("data", {})
    key_metrics = ["매출액", "영업이익", "당기순이익", "ROE(지배주주)", "부채비율", "EPS(원)"]
    for metric in key_metrics:
        if metric in data:
            vals = data[metric]
            vals_str = " | ".join([str(v) if v else "-" for v in vals])
            lines.append(f"  {metric}: {vals_str}")

    return "\n".join(lines)


def format_price_history(history, lang="ko"):
    """최근 시세 포맷"""
    if not history:
        return ""

    title = "📊 **최근 시세**" if lang == "ko" else "📊 **近期走势**" if lang == "zh" else "📊 **Price History**"
    lines = [title]
    for d in history[:7]:
        date = d.get("date", "")[:10]
        close = d.get("close", "")
        pct = d.get("change_pct", "")
        arrow = _arrow(pct)
        vol = d.get("volume")
        vol_str = f" vol:{vol:,}" if vol else ""
        lines.append(f"  {date} {arrow} {close} ({pct}%){vol_str}")
    return "\n".join(lines)


# ──────────────────────────────────────────────
# 10. Enhanced: Daum + Naver 통합 데이터
# ──────────────────────────────────────────────

def fetch_enhanced_stock(ticker):
    """증강 종목 조회 — Daum 전체 + Naver 보충
    
    Returns dict with:
      name, price, change_pct, market_cap, market_cap_rank,
      per, pbr, eps, bps, dps, div_yield, debt_ratio,
      foreign_ratio, foreign_exhaustion,
      high_52w, low_52w, sector_name, sector_change,
      est_per, est_eps, company_summary,
      sales, operating_profit, net_income,
      source (daum/naver/both)
    """
    result = {}
    
    # 1차: Daum (50+ 필드, 가장 풍부)
    try:
        from daum_finance import fetch_daum_stock
        daum = fetch_daum_stock(ticker)
        if daum:
            result = {
                "name": daum.get("name"),
                "price": daum.get("tradePrice"),
                "change_pct": (daum.get("changeRate") or 0) * 100,
                "change_price": daum.get("changePrice"),
                "market_cap": daum.get("marketCap"),
                "market_cap_rank": daum.get("marketCapRank"),
                "per": daum.get("per"),
                "pbr": daum.get("pbr"),
                "eps": daum.get("eps"),
                "bps": daum.get("bps"),
                "dps": daum.get("dps"),
                "div_yield": (daum.get("dps", 0) or 0) / daum["tradePrice"] * 100 if daum.get("tradePrice") and daum.get("dps") else None,
                "debt_ratio": (daum.get("debtRatio") or 0) * 100 if daum.get("debtRatio") else None,
                "foreign_ratio": (daum.get("foreignRatio") or 0) * 100 if daum.get("foreignRatio") else None,
                "high_52w": daum.get("high52wPrice"),
                "low_52w": daum.get("low52wPrice"),
                "sector_name": daum.get("wicsSectorName"),
                "sector_change": (daum.get("wicsSectorChangeRate") or 0) * 100 if daum.get("wicsSectorChangeRate") else None,
                "company_summary": daum.get("companySummary"),
                "sales": daum.get("sales"),
                "operating_profit": daum.get("operatingProfit"),
                "net_income": daum.get("netIncome"),
                "acc_volume": daum.get("accTradeVolume"),
                "acc_value": daum.get("accTradePrice"),
                "market_status": daum.get("marketStatus"),
                "source": "daum",
            }
    except Exception:
        pass
    
    # 2차: Naver 보충 (추정PER/EPS, 외인소진율)
    try:
        from naver_extended import fetch_naver_integration
        naver = fetch_naver_integration(ticker)
        if naver:
            # Naver 고유 데이터 보충
            if naver.get("est_per"):
                result["est_per"] = naver["est_per"]
            if naver.get("est_eps"):
                result["est_eps"] = naver["est_eps"]
            if naver.get("foreign_exhaustion") is not None:
                result["foreign_exhaustion"] = naver["foreign_exhaustion"]
            if naver.get("div_yield") and not result.get("div_yield"):
                result["div_yield"] = naver["div_yield"]
            if naver.get("market_cap_str"):
                result["market_cap_str"] = naver["market_cap_str"]
            
            # Daum 실패 시 Naver fallback
            if not result.get("name") and naver.get("stock_name"):
                result["name"] = naver["stock_name"]
                result["source"] = "naver"
            elif result.get("source") == "daum":
                result["source"] = "both"
    except Exception:
        pass
    
    return result if result.get("name") else None


def fetch_real_indices():
    """실제 KOSPI/KOSDAQ 지수 (Daum → Naver fallback)
    
    Returns dict:
      { "KOSPI": { price, change, change_pct, foreign, institution, individual },
        "KOSDAQ": { ... } }
    """
    try:
        from daum_finance import fetch_daum_indices
        daum = fetch_daum_indices()
        if daum:
            result = {}
            for market in ["KOSPI", "KOSDAQ"]:
                entries = daum.get(market, [])
                if entries:
                    latest = entries[0]
                    price = latest.get("tradePrice", 0)
                    cp = latest.get("changePrice", 0)
                    change_str = latest.get("change", "")
                    pct = (cp / (price - cp) * 100) if price != cp and price else 0
                    if change_str == "FALL":
                        pct = -abs(pct)
                    result[market] = {
                        "price": price,
                        "change": cp if change_str != "FALL" else -cp,
                        "change_pct": round(pct, 2),
                        "foreign": latest.get("foreignStraightPurchasePrice"),
                        "institution": latest.get("institutionStraightPurchasePrice"),
                        "individual": latest.get("individualStraightPurchasePrice"),
                        "history": entries[:5],
                    }
            return result if result else None
    except Exception:
        pass
    
    # Naver fallback
    result = {}
    kospi = fetch_kospi()
    if kospi:
        result["KOSPI"] = kospi
    kosdaq = fetch_kosdaq()
    if kosdaq:
        result["KOSDAQ"] = kosdaq
    return result if result else None


def fetch_market_investors():
    """전 시장 투자자별 순매수"""
    try:
        from daum_finance import fetch_daum_investors
        return fetch_daum_investors()
    except Exception:
        return None


def fetch_sector_ranking():
    """WICS 업종 등락 랭킹"""
    try:
        from daum_finance import fetch_daum_sectors
        return fetch_daum_sectors()
    except Exception:
        return []


def fetch_hot_stocks():
    """실시간 인기 종목"""
    try:
        from daum_finance import fetch_daum_hot_ranks
        return fetch_daum_hot_ranks()
    except Exception:
        return []


def format_enhanced_stock(data, lang="ko"):
    """증강 종목 정보 포맷 (시총/PER/PBR/52주/외국인/업종)"""
    if not data:
        return ""
    
    lines = []
    
    # 시가총액 + 순위
    mcap = data.get("market_cap")
    rank = data.get("market_cap_rank")
    mcap_str = data.get("market_cap_str")
    if mcap_str:
        rank_str = f" (#{rank})" if rank else ""
        lines.append(f"📊 시총: {mcap_str}{rank_str}")
    elif mcap:
        rank_str = f" (#{rank})" if rank else ""
        if mcap >= 1e12:
            lines.append(f"📊 시총: {mcap/1e12:,.1f}조{rank_str}")
        elif mcap >= 1e8:
            lines.append(f"📊 시총: {mcap/1e8:,.0f}억{rank_str}")
    
    # PER (실적 vs 추정)
    per = data.get("per")
    est_per = data.get("est_per")
    if per:
        per_line = f"📈 PER: {per:.1f}"
        if est_per:
            per_line += f" (추정 {est_per:.1f})"
        pbr = data.get("pbr")
        if pbr:
            per_line += f" | PBR: {pbr:.2f}"
        lines.append(per_line)
    
    # 배당
    div = data.get("div_yield")
    dps = data.get("dps")
    if div and div > 0:
        dps_str = f" ({dps:,.0f}원)" if dps else ""
        lines.append(f"💎 배당: {div:.2f}%{dps_str}")
    
    # 외국인
    fr = data.get("foreign_ratio")
    fe = data.get("foreign_exhaustion")
    if fr is not None:
        f_line = f"🌍 외국인: {fr:.2f}%"
        if fe is not None and abs(fe - fr) > 0.01:
            f_line += f" (소진율 {fe:.2f}%)"
        lines.append(f_line)
    
    # 52주 범위 with position bar
    h52 = data.get("high_52w")
    l52 = data.get("low_52w")
    price = data.get("price")
    if h52 and l52 and price:
        range_pct = (price - l52) / (h52 - l52) * 100 if h52 != l52 else 50
        bar_len = 10
        filled = max(0, min(bar_len, int(range_pct / 100 * bar_len)))
        bar = "▓" * filled + "░" * (bar_len - filled)
        lines.append(f"📐 52주: {l52:,.0f} [{bar}] {h52:,.0f}")
    
    # 업종
    sector = data.get("sector_name")
    sector_chg = data.get("sector_change")
    if sector:
        sc = f" ({sector_chg:+.2f}%)" if sector_chg is not None else ""
        lines.append(f"🏭 업종: {sector}{sc}")
    
    # 부채비율
    debt = data.get("debt_ratio")
    if debt is not None and debt > 0:
        lines.append(f"💳 부채: {debt:.1f}%")
    
    # 다국어
    if lang == "zh":
        result = "\n".join(lines)
        for ko, zh in {"시총": "市值", "배당": "股息", "외국인": "外资", "소진율": "消耗率",
                        "업종": "行业", "부채": "负债", "추정": "预估"}.items():
            result = result.replace(ko, zh)
        return result
    elif lang == "en":
        result = "\n".join(lines)
        for ko, en in {"시총": "MCap", "배당": "Div", "외국인": "Foreign", "소진율": "Exhaust",
                        "업종": "Sector", "부채": "Debt", "추정": "Est"}.items():
            result = result.replace(ko, en)
        return result
    
    return "\n".join(lines)


def format_real_indices(data, lang="ko"):
    """실제 지수 포맷 (투자자별 포함)"""
    if not data:
        return ""
    
    def _fmt_krw(v):
        if v is None: return "-"
        try:
            vf = float(v)
            if abs(vf) >= 1e12: return f"{vf/1e12:,.1f}조"
            if abs(vf) >= 1e8: return f"{vf/1e8:,.0f}억"
            return f"{vf:,.0f}"
        except: return str(v)
    
    lines = []
    for market in ["KOSPI", "KOSDAQ"]:
        info = data.get(market, {})
        if not info:
            continue
        price = info.get("price", 0)
        chg = info.get("change", 0)
        pct = info.get("change_pct", 0)
        
        emoji = "🔴📈" if pct > 0 else "🔵📉" if pct < 0 else "⚪"
        lines.append(f"{emoji} **{market}**: {price:,.2f} ({chg:+,.2f} / {pct:+.2f}%)")
        
        fgn = info.get("foreign")
        inst = info.get("institution")
        indiv = info.get("individual")
        if fgn is not None:
            parts = []
            for label, val in [("외국인" if lang=="ko" else "外资" if lang=="zh" else "Fgn", fgn),
                               ("기관" if lang=="ko" else "机构" if lang=="zh" else "Inst", inst),
                               ("개인" if lang=="ko" else "散户" if lang=="zh" else "Indiv", indiv)]:
                if val is not None:
                    e = "🟢" if val > 0 else "🔴"
                    parts.append(f"{e}{label} {_fmt_krw(val)}")
            lines.append(f"  {' | '.join(parts)}")
    
    return "\n".join(lines)


# ──────────────────────────────────────────────
# Test
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Market Overview ===")
    overview = fetch_market_overview()
    print(format_market_overview(overview))

    print("\n=== Samsung Disclosure ===")
    disc = fetch_disclosure("005930")
    print(format_disclosure(disc))

    print("\n=== Samsung Financial ===")
    fin = fetch_financial_summary("005930")
    print(format_financial_summary(fin))

    print("\n=== Samsung Price History ===")
    hist = fetch_price_history("005930")
    print(format_price_history(hist))

    print("\n=== Samsung Detail ===")
    detail = fetch_stock_detail("005930")
    print(json.dumps(detail, ensure_ascii=False, indent=2))
