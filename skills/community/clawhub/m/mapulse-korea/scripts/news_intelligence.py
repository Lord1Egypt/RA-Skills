#!/usr/bin/env python3
"""
Mapulse News Intelligence 🧠
一手数据源 + AI影响分析层

L0: 官方原始数据 (Fed, ECB, US Gov, EDGAR)
L2: 社交/快讯 (RSS wire-level)
L3: 主流财经媒体 (CNBC, WSJ, FT, Reuters)
+  AI Impact Layer: 每条新闻→对韩股的影响评估
"""

import requests
import re
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
}


# ═══════════════════════════════════════════
#  L0: 官方原始数据源
# ═══════════════════════════════════════════

def fetch_fed_latest():
    """美联储最新声明/会议纪要 (FRED RSS)"""
    results = []
    try:
        # Fed RSS - 政策声明
        resp = requests.get(
            "https://www.federalreserve.gov/feeds/press_monetary.xml",
            headers=HEADERS, timeout=8
        )
        if resp.status_code == 200:
            items = re.findall(
                r'<item>.*?<title>([^<]+)</title>.*?<link>([^<]+)</link>.*?<pubDate>([^<]+)</pubDate>',
                resp.text, re.DOTALL
            )
            for title, link, date in items[:3]:
                results.append({
                    "title": title.strip(),
                    "link": link.strip(),
                    "date": date.strip(),
                    "source": "Fed",
                    "level": "L0",
                    "category": "central_bank",
                })
    except:
        pass
    return results


def fetch_ecb_latest():
    """ECB 최新决策"""
    results = []
    try:
        resp = requests.get(
            "https://www.ecb.europa.eu/rss/press.html",
            headers=HEADERS, timeout=8
        )
        if resp.status_code == 200:
            items = re.findall(
                r'<item>.*?<title>([^<]+)</title>.*?<link>([^<]+)</link>',
                resp.text, re.DOTALL
            )
            for title, link in items[:3]:
                results.append({
                    "title": title.strip(),
                    "link": link.strip(),
                    "source": "ECB",
                    "level": "L0",
                    "category": "central_bank",
                })
    except:
        pass
    return results


def fetch_us_economic_calendar():
    """미국 경제지표 일정 (investing.com economic calendar RSS)"""
    results = []
    try:
        resp = requests.get(
            "https://kr.investing.com/rss/economic_calendar.rss",
            headers=HEADERS, timeout=8
        )
        if resp.status_code == 200:
            items = re.findall(
                r'<item>.*?<title>(?:<!\[CDATA\[)?(.+?)(?:\]\]>)?</title>.*?<link>([^<]+)</link>',
                resp.text, re.DOTALL
            )
            for title, link in items[:5]:
                results.append({
                    "title": title.strip(),
                    "link": link.strip(),
                    "source": "Economic Calendar",
                    "level": "L0",
                    "category": "macro",
                })
    except:
        pass
    return results


# ═══════════════════════════════════════════
#  L3: 주류 재경 매체 (Wire-level RSS)
# ═══════════════════════════════════════════

WIRE_FEEDS = [
    {
        "name": "Reuters Business",
        "url": "https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best",
        "category": "wire",
    },
    {
        "name": "CNBC Top",
        "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114",
        "category": "wire",
    },
    {
        "name": "FT Markets",
        "url": "https://www.ft.com/markets?format=rss",
        "category": "wire",
    },
    {
        "name": "WSJ Markets",
        "url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
        "category": "wire",
    },
    {
        "name": "Yahoo Finance",
        "url": "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC&region=US&lang=en-US",
        "category": "wire",
    },
    {
        "name": "Bloomberg Asia",
        "url": "https://feeds.bloomberg.com/markets/news.rss",
        "category": "wire",
    },
]

# 한국 프리미엄 소스
KR_FEEDS = [
    {
        "name": "한국경제",
        "url": "https://www.hankyung.com/feed/finance",
        "category": "kr_premium",
    },
    {
        "name": "매일경제",
        "url": "https://www.mk.co.kr/rss/30100041/",
        "category": "kr_premium",
    },
    {
        "name": "조선비즈",
        "url": "https://biz.chosun.com/rss/finance/",
        "category": "kr_premium",
    },
    {
        "name": "연합뉴스 경제",
        "url": "https://www.yna.co.kr/rss/economy.xml",
        "category": "kr_premium",
    },
]


def fetch_rss_feed(feed_info, max_items=5):
    """RSS 피드에서 뉴스 추출"""
    results = []
    try:
        resp = requests.get(feed_info["url"], headers=HEADERS, timeout=8)
        if resp.status_code != 200:
            return results

        text = resp.text

        # RSS item 추출 (다양한 포맷 대응)
        items = re.findall(
            r'<item>.*?<title>(?:<!\[CDATA\[)?\s*(.+?)\s*(?:\]\]>)?</title>'
            r'.*?<link>(?:<!\[CDATA\[)?\s*(.+?)\s*(?:\]\]>)?</link>',
            text, re.DOTALL
        )

        for title, link in items[:max_items]:
            title = title.strip()
            title = re.sub(r'<[^>]+>', '', title)  # HTML 태그 제거
            title = title.replace("&amp;", "&").replace("&quot;", '"').replace("&#39;", "'").replace("&lt;", "<").replace("&gt;", ">")
            link = link.strip()

            if title and len(title) > 5:
                results.append({
                    "title": title,
                    "link": link,
                    "source": feed_info["name"],
                    "level": "L3",
                    "category": feed_info["category"],
                })
    except:
        pass
    return results


# ═══════════════════════════════════════════
#  AI Impact Analysis Layer
# ═══════════════════════════════════════════

# 키워드 → 영향 매핑 (AI 대신 규칙 기반 빠른 분석)
IMPACT_RULES = {
    # 매크로
    "rate hike|금리 인상|기준금리.*인상|加息": {"direction": "🔴", "impact": "금리↑ → 원화약세 → 외국인유출 → 코스피↓", "sectors": ["금융+", "반도체-", "성장주-"]},
    "rate cut|금리 인하|기준금리.*인하|降息": {"direction": "🟢", "impact": "금리↓ → 유동성↑ → 위험자산 선호 → 코스피↑", "sectors": ["성장주+", "반도체+", "바이오+"]},
    "inflation|인플레|CPI|물가.*상승": {"direction": "🔴", "impact": "물가↑ → 긴축 우려 → 성장주 압력", "sectors": ["소비재-", "에너지+"]},
    "recession|경기.*침체|불황|리세션": {"direction": "🔴", "impact": "경기침체 → 수출↓ → 한국 수출주 타격", "sectors": ["반도체-", "자동차-", "화학-"]},

    # 지정학
    "war|전쟁|침공|missile|미사일|이란|Iran|tariff|관세": {"direction": "🔴", "impact": "지정학 리스크 → 안전자산 선호 → 원화약세 → 외국인 이탈", "sectors": ["방산+", "수출주-"]},
    "ceasefire|휴전|평화.*협상|종전": {"direction": "🟢", "impact": "리스크 해소 → 위험자산 회귀 → 코스피 반등", "sectors": ["수출주+", "운송+"]},

    # 반도체
    "semiconductor|반도체|HBM|AI chip|엔비디아|NVIDIA|TSMC": {"direction": "🟢", "impact": "반도체 수요↑ → 삼성전자·SK하이닉스 수혜", "sectors": ["삼성전자+", "SK하이닉스+", "장비주+"]},
    "chip ban|수출.*규제|반도체.*제재|칩.*제재": {"direction": "🔴", "impact": "반도체 수출 규제 → 중국向 매출 타격", "sectors": ["삼성전자-", "SK하이닉스-"]},

    # 환율
    "dollar.*strong|달러.*강세|환율.*상승|원.*약세": {"direction": "🔴", "impact": "원화약세 → 외국인자금 유출 → 수입비용↑", "sectors": ["수출주±", "항공-", "정유-"]},
    "dollar.*weak|달러.*약세|환율.*하락|원.*강세": {"direction": "🟢", "impact": "원화강세 → 외국인자금 유입 → 수입비용↓", "sectors": ["내수주+", "항공+"]},

    # 유가
    "oil.*surge|유가.*급등|oil.*spike|원유.*상승": {"direction": "🔴", "impact": "유가↑ → 생산비용↑ → 소비위축", "sectors": ["정유+", "항공-", "화학±"]},
    "oil.*drop|유가.*하락|oil.*fall|원유.*급락": {"direction": "🟢", "impact": "유가↓ → 비용↓ → 소비여력↑", "sectors": ["항공+", "화학+", "정유-"]},

    # AI/Tech
    "AI|artificial intelligence|인공지능|GPT|LLM|생성형": {"direction": "🟢", "impact": "AI 산업 성장 → 반도체·클라우드 수혜", "sectors": ["삼성전자+", "네이버+", "카카오+"]},

    # EV/배터리
    "EV|electric vehicle|전기차|배터리|battery": {"direction": "🟢", "impact": "전기차/배터리 수요 → 한국 배터리 3사 수혜", "sectors": ["LG에너지+", "삼성SDI+", "에코프로+"]},
}


def analyze_impact(title):
    """뉴스 제목 → 한국 증시 영향 분석"""
    t = title.lower()

    for pattern, impact in IMPACT_RULES.items():
        if re.search(pattern, t, re.IGNORECASE):
            return impact

    return None


def format_impact(impact):
    """영향 분석 포맷"""
    if not impact:
        return ""

    direction = impact["direction"]
    desc = impact["impact"]
    sectors = " / ".join(impact["sectors"])
    return f"  {direction} {desc}\n  📌 관련: {sectors}"


# ═══════════════════════════════════════════
#  종합 Intelligence 리포트
# ═══════════════════════════════════════════

def get_intelligence_report():
    """글로벌 + 한국 뉴스 Intelligence 리포트"""

    all_news = []
    seen = set()

    # L0: 공식 소스
    print("  🔍 L0: 중앙은행/정부 공식 발표...")
    for fetcher in [fetch_fed_latest, fetch_ecb_latest, fetch_us_economic_calendar]:
        try:
            items = fetcher()
            for item in items:
                if item["title"][:30] not in seen:
                    seen.add(item["title"][:30])
                    all_news.append(item)
        except:
            pass

    # L3: Wire-level 글로벌
    print("  🔍 L3: 글로벌 금융 매체...")
    for feed in WIRE_FEEDS:
        try:
            items = fetch_rss_feed(feed, max_items=3)
            for item in items:
                if item["title"][:30] not in seen:
                    seen.add(item["title"][:30])
                    all_news.append(item)
        except:
            pass
        time.sleep(0.1)

    # 한국 프리미엄 소스
    print("  🔍 한국 프리미엄 재경 매체...")
    for feed in KR_FEEDS:
        try:
            items = fetch_rss_feed(feed, max_items=5)
            for item in items:
                if item["title"][:30] not in seen:
                    seen.add(item["title"][:30])
                    all_news.append(item)
        except:
            pass
        time.sleep(0.1)

    # AI 영향 분석
    for item in all_news:
        item["impact"] = analyze_impact(item["title"])

    return all_news


def format_intelligence(news_list):
    """Intelligence 리포트 포맷"""
    lines = [
        f"🧠 *Mapulse Intelligence Report*",
        f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
    ]

    # 영향 있는 뉴스 먼저
    impactful = [n for n in news_list if n.get("impact")]
    normal = [n for n in news_list if not n.get("impact")]

    if impactful:
        lines.append("*🎯 한국 증시 영향 뉴스:*")
        lines.append("")
        for n in impactful[:8]:
            source = n["source"]
            linked = f"[{n['title'][:55]}]({n['link']})" if n.get("link") else n["title"][:55]
            lines.append(f"• [{source}] {linked}")
            lines.append(format_impact(n["impact"]))
            lines.append("")

    # L0 공식
    l0 = [n for n in normal if n.get("level") == "L0"]
    if l0:
        lines.append("*📋 공식 발표:*")
        for n in l0[:5]:
            linked = f"[{n['title'][:55]}]({n['link']})" if n.get("link") else n["title"][:55]
            lines.append(f"  • [{n['source']}] {linked}")
        lines.append("")

    # 글로벌 와이어
    global_wire = [n for n in normal if n.get("category") == "wire"]
    if global_wire:
        lines.append("*🌍 글로벌 시장:*")
        for n in global_wire[:5]:
            linked = f"[{n['title'][:55]}]({n['link']})" if n.get("link") else n["title"][:55]
            lines.append(f"  • [{n['source']}] {linked}")
        lines.append("")

    # 한국
    kr = [n for n in normal if n.get("category") == "kr_premium"]
    if kr:
        lines.append("*🇰🇷 한국 재경:*")
        for n in kr[:8]:
            linked = f"[{n['title'][:55]}]({n['link']})" if n.get("link") else n["title"][:55]
            lines.append(f"  • [{n['source']}] {linked}")
        lines.append("")

    lines.append(f"📊 총 {len(news_list)}건 (영향분석 {len(impactful)}건)")
    return "\n".join(lines)


# ─── CLI ───

if __name__ == "__main__":
    print("=" * 55)
    print("🧠 Mapulse News Intelligence")
    print("  L0 공식 + L3 Wire + AI Impact Analysis")
    print("=" * 55)

    news = get_intelligence_report()
    print(f"\n총 {len(news)}건 수집")
    print()
    print(format_intelligence(news))
