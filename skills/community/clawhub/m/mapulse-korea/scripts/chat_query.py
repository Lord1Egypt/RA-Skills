#!/usr/bin/env python3
"""
Mapulse — 对话查询引擎 (组件3)
自然语言问答韩国股市

支持查询:
  "삼성 오늘 어때?" / "삼성今天怎么样?"
  "왜 빠졌어?" / "为什么跌了?"
  "외국인 뭐 사?" / "外资在买什么?"
  "코스피 전망" / "KOSPI怎么看?"
  "내 포트폴리오" / "我的组合分析"
  "비교 삼성 SK" / "对比三星和SK"

用法:
  python3 chat_query.py "삼성 오늘 어때?"
  python3 chat_query.py "KOSPI 왜 빠졌어?"
  python3 chat_query.py demo
"""

import sys
import os
import re
import json
import time
import datetime

try:
    import requests
except ImportError:
    requests = None

sys.path.insert(0, os.path.dirname(__file__))

from fetch_briefing import (
    find_trading_date, get_stock, fetch_all,
    STOCK_NAMES, INDEX_ETFS, DEFAULT_WATCHLIST, fmt_arrow,
    _resolve_stock_name
)


# ─── 종목 매칭 ───

# 확장 별명/종목 로드
try:
    from extended_aliases import EXTENDED_ALIASES, EXTENDED_STOCK_NAMES, THEME_KEYWORDS
    STOCK_NAMES.update(EXTENDED_STOCK_NAMES)
except ImportError:
    EXTENDED_ALIASES = {}
    THEME_KEYWORDS = []

# 한글이름 → 티커 역매핑
NAME_TO_TICKER = {v: k for k, v in STOCK_NAMES.items()}
# 별명/약칭
ALIASES = {
    # 한국어
    "삼성": "005930", "삼전": "005930", "samsung": "005930",
    "하이닉스": "000660", "sk하이닉스": "000660", "skhynix": "000660",
    "네이버": "035420", "naver": "035420",
    "카카오": "035720", "kakao": "035720",
    "lg에너지": "373220", "엘지에너지": "373220",
    "셀트리온": "068270",
    "lg화학": "051910", "엘지화학": "051910",
    "삼성sdi": "006400", "sdi": "006400",
    "현대차": "005380", "현대자동차": "005380", "hyundai": "005380",
    "기아": "000270", "kia": "000270",
    "sk이노": "096770", "sk이노베이션": "096770",
    "두산에너": "034020", "두산에너빌리티": "034020",
    "포스코인터": "003670", "포스코": "003670",
    "한전": "015760", "한국전력": "015760",
    "엔씨": "036570", "엔씨소프트": "036570", "ncsoft": "036570",
    "하이브": "352820", "hybe": "352820",
    "코스피": "KOSPI", "kospi": "KOSPI",
    "코스닥": "KOSDAQ", "kosdaq": "KOSDAQ",
    # 中文
    "三星": "005930", "三星电子": "005930",
    "海力士": "000660", "sk海力士": "000660",
    "现代": "005380", "现代汽车": "005380",
    "起亚": "000270",
    "lg电子": "066570", "lg化学": "051910", "lg能源": "373220",
    "赛特瑞恩": "068270",
    "韩国电力": "015760",
    "浦项": "003670", "浦项制铁": "003670",
    "sk创新": "096770",
    "三星sdi": "006400",
    "生态普罗": "086520", "ecoPro": "086520",
    "hive": "352820",
}

# 확장 별명 병합
ALIASES.update(EXTENDED_ALIASES)

# 별명을 길이 내림차순으로 정렬 — 최장 매칭 우선 (삼성바이오로직스 > 삼성바이오 > 삼성)
_ALIASES_SORTED = sorted(ALIASES.items(), key=lambda x: len(x[0]), reverse=True)
# 정식 이름도 길이 내림차순
_NAMES_SORTED = sorted(NAME_TO_TICKER.items(), key=lambda x: len(x[0]), reverse=True)


def resolve_ticker(text):
    """텍스트에서 종목 코드 추출 (최장 매칭 우선)"""
    t = text.lower().strip()

    # 직접 티커
    if re.match(r'^\d{6}$', t):
        return t

    # 별명 (길이 내림차순 → 최장 매칭)
    for alias, ticker in _ALIASES_SORTED:
        if alias in t:
            return ticker

    # 정식 이름 (길이 내림차순)
    for name, ticker in _NAMES_SORTED:
        if name.lower() in t:
            return ticker

    return None


def resolve_multiple_tickers(text):
    """텍스트에서 여러 종목 추출 (최장 매칭 우선)"""
    tickers = []
    t = text.lower()
    matched_spans = []  # 이미 매칭된 위치 추적

    for alias, ticker in _ALIASES_SORTED:
        if ticker in ("KOSPI", "KOSDAQ"):
            continue
        idx = t.find(alias)
        if idx == -1:
            continue
        # 이미 매칭된 범위와 겹치면 skip
        end = idx + len(alias)
        overlap = False
        for s, e in matched_spans:
            if idx < e and end > s:
                overlap = True
                break
        if overlap:
            continue
        if ticker not in tickers:
            tickers.append(ticker)
            matched_spans.append((idx, end))

    return tickers


# ─── 의도 분류 ───

class Intent:
    STOCK_PRICE = "stock_price"       # 개별 종목 조회
    WHY_DROP = "why_drop"             # 왜 빠졌어
    WHY_RISE = "why_rise"             # 왜 올랐어
    MARKET_OVERVIEW = "market_overview"  # 시장 전체
    FOREIGN_FLOW = "foreign_flow"     # 외국인 동향
    COMPARE = "compare"               # 종목 비교
    SECTOR = "sector"                 # 섹터 분석
    OUTLOOK = "outlook"               # 전망
    COMMUNITY = "community"           # 커뮤니티 감성/분위기
    NEWS = "news"                     # 뉴스
    RESEARCH = "research"             # 증권사 리서치
    SUPPLY_DEMAND = "supply_demand"   # 수급 (외국인/기관/개인)
    COMMODITY = "commodity"           # 원자재/귀금속 (금,은,구리,원유 등)
    CRYPTO = "crypto"                 # 암호화폐 가격
    DISCLOSURE = "disclosure"         # 공시
    FINANCIAL = "financial"           # 재무제표
    EXCHANGE_RATE = "exchange_rate"   # 환율
    FEAR_GREED = "fear_greed"         # 공포탐욕지수/VIX
    SECTOR_RANKING = "sector_ranking" # 업종/행업 등락 랭킹
    HOT_RANK = "hot_rank"             # 실시간 인기 종목
    CHAT = "chat"                     # 자유 대화
    UNKNOWN = "unknown"


def classify_intent(text):
    """의도 분류 — 분석 질문 우선 → 키워드 → LLM fallback"""
    t = text.lower().strip()

    # ── 분석/영향/정책/전략 질문 감지 → AI CHAT (Opus) ──
    # "금투세 폐지되나요?", "미국 금리 인하 한국에 좋나요?", "전쟁 나면 주식 어떻게?"
    analysis_keywords = [
        # 한국어
        "영향", "어떤", "어떻게", "미치", "전망", "분석", "대응",
        "리스크", "위험", "기회", "전략", "해석", "의미",
        "진짜", "가능", "폐지", "정책", "세금", "금투세", "밸류업",
        "공매도", "배당", "분배", "금리", "이자", "인하", "인상",
        "전쟁", "지정학", "버블", "거품", "언제", "시기", "타이밍",
        "사도 될까", "팔아야", "기다려야", "분할매수", "물타기",
        "10만전", "10만원", "5000", "위기", "기회",
        # 中文
        "影响", "怎么", "如何", "风险", "机会", "分析", "策略",
        "真的", "可能", "废除", "政策", "税", "利率", "降息", "加息",
        "战争", "泡沫", "什么时候", "时机", "该不该", "买入", "卖出",
        "分批", "抄底", "等回调",
        # English
        "impact", "affect", "risk", "opportunity", "mean", "implication",
        "what does", "how will", "how does", "should i", "is it time",
        "really", "possible", "bubble", "war", "rate cut", "policy",
    ]
    # 테마 키워드 (정책/전략/매크로) → AI CHAT
    if any(w.lower() in t for w in THEME_KEYWORDS):
        ticker = resolve_ticker(t)
        if not ticker or ticker in ("KOSPI", "KOSDAQ") or str(ticker).startswith("__"):
            return Intent.CHAT
    
    # 커뮤니티/분위기 (analysis_keywords보다 우선: "분위기 어떤가요" 등이 CHAT로 빠지지 않도록)
    if any(w in t for w in ["분위기", "감성", "여론", "커뮤니티", "종토방", "토론", "반응",
                             "sentiment", "community", "mood", "论坛", "舆论", "氛围", "气氛",
                             "투자자 심리", "投资者情绪", "investor sentiment", "시장 심리"]):
        return Intent.COMMUNITY

    if len(t) > 6 and any(w in t for w in analysis_keywords):
        # 특정 종목 + 분석 키워드 = WHY/OUTLOOK
        ticker = resolve_ticker(t)
        if ticker and ticker not in ("KOSPI", "KOSDAQ"):
            if any(w in t for w in ["왜 빠", "왜 떨어", "为什么跌", "why drop", "why down"]):
                return Intent.WHY_DROP
            if any(w in t for w in ["왜 올", "왜 상승", "为什么涨", "why up", "why rise"]):
                return Intent.WHY_RISE
            # 종목 + 분석질문 → 종목 조회 (deep analysis)
            return Intent.STOCK_PRICE
        # 종목 없는 일반 분석/정책 질문 → AI CHAT (Opus)
        return Intent.CHAT

    # Twitter 속보
    if any(w in t for w in ["속보", "twitter", "트위터", "sentinel", "speed", "推特",
                             "breaking", "wire", "速报", "실시간 속보"]):
        return Intent.NEWS

    # 하락/상승 + 이유 감지 (뉴스보다 우선)
    import re as _re
    if _re.search(r"하락.*이유|빠[졌진].*이유|떨어[졌진].*이유|이유.*하락|이유.*빠|이유.*떨어|왜.*떨어|왜.*하락|왜.*빠[졌진]|跌.*为什么|为什么.*跌|下跌.*原因|why.*drop|why.*fall|why.*down", t):
        return Intent.WHY_DROP
    if _re.search(r"상승.*이유|오[른름].*이유|올[랐라].*이유|이유.*상승|이유.*올|왜.*올[랐라]|왜.*상승|涨.*为什么|为什么.*涨|上涨.*原因|why.*up|why.*rise", t):
        return Intent.WHY_RISE

    # 뉴스
    if any(w in t for w in ["뉴스", "기사", "소식", "news", "新闻", "消息",
                             "최근", "오늘", "today", "recent", "今天", "最近"]):
        return Intent.NEWS

    # 증권사 리서치/목표가
    if any(w in t for w in ["리서치", "리포트", "목표가", "증권사", "애널", "research",
                             "report", "target", "analyst", "研报", "目标价", "券商"]):
        return Intent.RESEARCH

    # 수급 동향
    if any(w in t for w in ["수급", "매매동향", "외국인", "기관", "개인", "순매수", "순매도",
                             "foreign", "institution", "外资", "机构", "散户", "资金流向"]):
        return Intent.SUPPLY_DEMAND

    # 왜 빠졌어/올랐어
    if any(w in t for w in ["왜 빠", "왜 떨어", "왜 하락", "为什么跌", "why drop", "why down", "why fall",
                             "하락.*이유", "빠진.*이유", "떨어진.*이유", "이유가", "원인이",
                             "跌.*原因", "下跌.*为什么", "drop.*reason"]):
        return Intent.WHY_DROP
    if any(w in t for w in ["왜 올", "왜 상승", "为什么涨", "why up", "why rise",
                             "상승.*이유", "오른.*이유", "涨.*原因", "上涨.*为什么", "rise.*reason"]):
        return Intent.WHY_RISE

    # 비교
    if any(w in t for w in ["비교", "对比", "compare", "vs"]):
        return Intent.COMPARE

    # 전망
    if any(w in t for w in ["전망", "outlook", "怎么看", "내일", "tomorrow", "预测", "明天"]):
        return Intent.OUTLOOK

    # 업종/행업 랭킹
    if any(w in t for w in ["섹터", "sector", "板块", "업종", "행업", "行业", "업종별",
                             "sector ranking", "industry", "업종현황", "行业排行"]):
        return Intent.SECTOR_RANKING

    # 실시간 인기 종목
    if any(w in t for w in ["인기", "핫", "hot", "trending", "热门", "人气", "인기종목",
                             "热搜", "검색순위", "rank", "ranking", "순위"]):
        return Intent.HOT_RANK

    # 공시/공고
    if any(w in t for w in ["공시", "공고", "disclosure", "filing", "公告", "披露"]):
        return Intent.DISCLOSURE

    # 재무/실적
    if any(w in t for w in ["재무", "실적", "매출", "영업이익", "순이익", "financial", "earnings",
                             "revenue", "profit", "财务", "营收", "利润", "业绩", "财报",
                             "per", "pbr", "roe", "eps"]):
        return Intent.FINANCIAL

    # 환율
    if any(w in t for w in ["환율", "원달러", "원/달러", "달러", "엔화", "위안",
                             "exchange rate", "usd/krw", "汇率", "美元", "韩元", "日元", "人民币"]):
        return Intent.EXCHANGE_RATE

    # 공포탐욕/VIX/변동성
    if any(w in t for w in ["공포", "탐욕", "fear", "greed", "vix", "변동성", "volatility",
                             "恐慌", "贪婪", "恐惧", "波动"]):
        return Intent.FEAR_GREED

    # 시장 전체
    if any(w in t for w in ["시장", "코스피", "코스닥", "kospi", "kosdaq", "市场", "시황",
                             "大盘", "指数", "index"]):
        return Intent.MARKET_OVERVIEW

    # 원자재/귀금속 (금, 은, 구리, 원유 등)
    # 단, 종목 별명이 먼저 매칭되면 commodity가 아님 (은행주 ≠ 은)
    ticker_check = resolve_ticker(t)
    if not ticker_check or str(ticker_check).startswith("__"):
        try:
            from commodities import resolve_commodity
            mode, _ = resolve_commodity(t)
            if mode:
                return Intent.COMMODITY
        except:
            pass

    # 암호화폐
    try:
        from crypto import is_crypto_query
        if is_crypto_query(t):
            return Intent.CRYPTO
    except:
        pass

    # 종목명 매칭 → 개별 종목 조회
    ticker = resolve_ticker(t)
    if ticker and ticker not in ("KOSPI", "KOSDAQ"):
        # 미국주식/테마 → AI CHAT
        if str(ticker).startswith("__"):
            return Intent.CHAT
        return Intent.STOCK_PRICE

    # 키워드 미매칭 → LLM 의도 분류 fallback
    try:
        from llm import classify_intent_llm
        llm_intent = classify_intent_llm(text)

        intent_map = {
            "stock_price": Intent.STOCK_PRICE,
            "news": Intent.NEWS,
            "why_drop": Intent.WHY_DROP,
            "why_rise": Intent.WHY_RISE,
            "community": Intent.COMMUNITY,
            "supply_demand": Intent.SUPPLY_DEMAND,
            "research": Intent.RESEARCH,
            "compare": Intent.COMPARE,
            "market_overview": Intent.MARKET_OVERVIEW,
            "outlook": Intent.OUTLOOK,
            "disclosure": Intent.DISCLOSURE,
            "financial": Intent.FINANCIAL,
            "exchange_rate": Intent.EXCHANGE_RATE,
            "fear_greed": Intent.FEAR_GREED,
            "help": Intent.UNKNOWN,  # help → 도움말
            "chat": Intent.CHAT,
        }
        return intent_map.get(llm_intent, Intent.CHAT)
    except:
        return Intent.UNKNOWN


# ─── 응답 생성 ───

def handle_stock_price(ticker, date_str, user_query=None, deep_analysis=True):
    """개별 종목 조회 — 데이터 수집 + AI 분석 (deep=True일때만 Opus)"""
    data = get_stock(ticker, date_str)
    if not data:
        return f"❌ {ticker} 데이터를 가져올 수 없습니다."

    name = _resolve_stock_name(ticker)
    arrow = fmt_arrow(data["change_pct"])

    # 기본 데이터 라인
    lines = [
        f"{arrow} *{name} ({ticker})*",
        f"📊 종가: ₩{data['close']:,} ({data['change_pct']:+.1f}%)",
        f"📦 거래량: {data['volume']:,}",
        f"📅 {date_str}",
    ]

    # Daum + Naver 확장 데이터 (시총/PER/PBR/52주/외국인/업종)
    try:
        from market_data import fetch_enhanced_stock, format_enhanced_stock
        enhanced = fetch_enhanced_stock(ticker)
        if enhanced:
            enhanced_text = format_enhanced_stock(enhanced)
            if enhanced_text:
                lines.append("")
                lines.append(enhanced_text)
    except:
        pass

    # 실시간 부가 정보 수집
    context = {"price": data}
    try:
        from forum_scraper import fetch_naver_ssr, fetch_naver_news
        ssr = fetch_naver_ssr(ticker)
        if ssr:
            if ssr["deal_trends"]:
                d = ssr["deal_trends"][0]
                lines.append(f"\n*수급:* 외국인 {d['foreign']} | 기관 {d['institution']} | 개인 {d['individual']}")
                context["supply_demand"] = ssr["deal_trends"][:3]

            if ssr["researches"]:
                r = ssr["researches"][0]
                link = r.get("link", "")
                if link:
                    lines.append(f"*리서치:* {r['broker']} — [{r['title']}]({link})")
                else:
                    lines.append(f"*리서치:* {r['broker']} — {r['title']}")
                context["research"] = [{"broker": x["broker"], "title": x["title"], "link": x.get("link","")} for x in ssr["researches"][:3]]

            if ssr.get("industry_compare"):
                context["peers"] = [{"name": c["name"], "change": c["change_pct"]} for c in ssr["industry_compare"][:5]]

        news = fetch_naver_news(ticker, count=5)
        if news:
            lines.append(f"\n*최신 뉴스:*")
            for n in news[:3]:
                linked = make_news_link(n)
                lines.append(f"  • [{n.get('source','')}] {linked}")
            context["news"] = [n["title"] for n in news[:5]]
    except:
        pass

    # 공시 추가 (최근 3건)
    try:
        from market_data import fetch_disclosure
        disc = fetch_disclosure(ticker, count=3)
        if disc:
            lines.append(f"\n📋 *최근 공시:*")
            for d in disc[:3]:
                lines.append(f"  • [{d['datetime'][:10]}] {d['title'][:50]}")
            context["disclosure"] = disc
    except:
        pass

    # 최근 시세 추이 (7일)
    try:
        from market_data import fetch_price_history
        hist = fetch_price_history(ticker, days=7)
        if hist and len(hist) > 1:
            trend_str = " → ".join([f"{h['change_pct']}%" for h in hist[:5]])
            lines.append(f"\n📈 *5일 추이:* {trend_str}")
            context["price_history"] = hist[:7]
    except:
        pass

    # AI 분석 — 분석/왜 질문일 때만 Opus, 단순 조회는 Haiku 요약
    if deep_analysis and user_query and any(w in (user_query or "").lower() for w in 
        ["분석", "왜", "why", "为什么", "怎么", "어때", "전망", "outlook", "趋势", "추세", "analysis"]):
        try:
            from llm import analyze_stock
            ai = analyze_stock(ticker, name, context, user_query)
            if ai:
                lines.append(f"\n🤖 *AI 분석:*\n{ai}")
        except:
            pass
    elif context.get("news") or context.get("research"):
        # 단순 조회: Haiku로 한줄 요약
        try:
            from llm import call_llm, MODEL_FAST, detect_language
            lang = detect_language(user_query or "")
            lang_inst = {"ko": "한국어", "zh": "中文", "en": "English"}.get(lang, "한국어")
            summary = call_llm(
                messages=[{"role": "user", "content": f"이 종목 데이터를 {lang_inst}로 2-3문장 핵심 요약:\n{json.dumps(context, ensure_ascii=False, default=str)[:500]}"}],
                model=MODEL_FAST, max_tokens=150, temperature=0.2,
            )
            if summary:
                lines.append(f"\n💡 {summary}")
        except:
            pass

    return "\n".join(lines)


def handle_news(ticker=None):
    """종목 뉴스 또는 전체 시장 뉴스 (6551 OpenNews + Naver fallback)"""
    try:
        from forum_scraper import fetch_naver_news, fetch_naver_ssr, STOCK_MAP

        # 특정 종목 뉴스
        if ticker:
            name = STOCK_MAP.get(ticker, _resolve_stock_name(ticker))
            lines = [f"📰 *{name} ({ticker}) 최신 뉴스*", ""]

            # 1. Naver 뉴스 (한국)
            news = fetch_naver_news(ticker, count=10)
            if news:
                for i, n in enumerate(news[:5], 1):
                    linked = make_news_link(n)
                    lines.append(f"{i}. [{n.get('source','')}] {linked}")

            # 2. 6551 OpenNews (글로벌)
            try:
                from news_6551 import search_news, format_news
                global_news = search_news(name, limit=5)
                articles = global_news.get("data", []) if isinstance(global_news, dict) else []
                if articles:
                    lines.append(f"\n🌐 *글로벌 뉴스:*")
                    for a in articles[:3]:
                        rating = a.get("aiRating", {})
                        summary = rating.get("enSummary", rating.get("summary", ""))
                        source = a.get("newsType", "")
                        score = rating.get("score", "")
                        signal = rating.get("signal", "")
                        signal_e = {"long": "🟢", "short": "🔴"}.get(signal, "⚪")
                        if summary:
                            lines.append(f"  {signal_e} [{source}] {summary[:80]} (Score:{score})")
            except:
                pass

            # 3. Twitter 관련 트윗
            try:
                from twitter_6551 import search_stock_tweets
                tweets = search_stock_tweets(name, count=3)
                items = tweets.get("data", tweets) if isinstance(tweets, dict) else tweets
                if isinstance(items, list) and items:
                    lines.append(f"\n🐦 *Twitter:*")
                    for t in items[:3]:
                        text = t.get("text", "")[:80]
                        user = t.get("userScreenName", "")
                        lines.append(f"  @{user}: {text}")
            except:
                pass

            # 리서치
            ssr = fetch_naver_ssr(ticker)
            if ssr and ssr["researches"]:
                lines.append(f"\n*📋 증권사 리서치:*")
                for r in ssr["researches"][:3]:
                    lines.append(f"  • {r['broker']}: {r['title']}")

            if len(lines) <= 2:
                return f"📰 {name} 관련 뉴스가 없습니다."
            return "\n".join(lines)

        # 전체 시장 뉴스
        else:
            return handle_market_news()

    except Exception as e:
        return f"❌ 뉴스 조회 오류: {e}"


def fetch_global_news(count=5):
    """국제 금융시장 뉴스 (Investing.com KR RSS + Yahoo Finance)"""
    global_news = []
    seen = set()

    # 1. Investing.com 한국어 RSS
    try:
        resp = requests.get(
            "https://kr.investing.com/rss/news.rss",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=8
        )
        if resp.status_code == 200:
            titles = re.findall(r'<title><!\[CDATA\[(.+?)\]\]></title>|<title>([^<]+)</title>', resp.text)
            links = re.findall(r'<link>([^<]+)</link>', resp.text)
            for i, (t1, t2) in enumerate(titles):
                title = (t1 or t2).strip()
                link = links[i] if i < len(links) else ""
                if title and len(title) > 10 and title not in seen and "모든 뉴스" not in title:
                    seen.add(title)
                    global_news.append({"title": title, "link": link, "source": "Investing.com"})
    except:
        pass

    # 2. Yahoo Finance S&P 500 RSS (영어)
    try:
        resp = requests.get(
            "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC&region=US&lang=en-US",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=8
        )
        if resp.status_code == 200:
            items = re.findall(r'<item>.*?<title>([^<]+)</title>.*?<link>([^<]+)</link>', resp.text, re.DOTALL)
            for title, link in items:
                title = title.strip()
                if title and title not in seen:
                    seen.add(title)
                    global_news.append({"title": title, "link": link, "source": "Yahoo Finance"})
    except:
        pass

    return global_news[:count]


def _shorten_url(url):
    """URL 단축 (is.gd)"""
    if not url or len(url) < 50:
        return url
    try:
        if not requests:
            return url
        r = requests.get(
            f"https://is.gd/create.php?format=simple&url={requests.utils.quote(url)}",
            timeout=3
        )
        if r.status_code == 200 and r.text.startswith("http"):
            return r.text.strip()
    except:
        pass
    return url


def make_news_link(news_item):
    """뉴스 제목을 파란색 클릭 가능 링크로 (Markdown)"""
    title = news_item.get("title", "")[:60]
    link = news_item.get("link", "")

    if link:
        short = _shorten_url(link)
        return f"[{title}]({short})"

    return title


def handle_market_news():
    """전체 시장 뉴스 — 뉴스 수집 + 중복 제거 + AI 시장 분석"""
    
    all_news = []     # 수집된 뉴스
    all_tweets = []   # 수집된 트윗
    
    # 1차: 6551 OpenNews
    try:
        from news_6551 import get_latest, _extract_articles
        result = get_latest(limit=15)
        articles = _extract_articles(result)
        if articles:
            all_news = articles
    except:
        pass
    
    # 2차: Twitter 속보
    try:
        from twitter_6551 import get_sentinel_latest
        sentinel = get_sentinel_latest(count=8)
        if sentinel:
            all_tweets = sentinel if isinstance(sentinel, list) else []
    except:
        pass
    
    # 뉴스가 전혀 없으면 fallback
    if not all_news and not all_tweets:
        try:
            from news_intelligence import get_intelligence_report, format_intelligence
            news = get_intelligence_report()
            if news:
                return format_intelligence(news)
        except:
            pass
        return _handle_market_news_fallback()
    
    # ── 중복 제거 (유사 콘텐츠 필터링) ──
    seen_keys = set()
    unique_news = []
    
    def _dedup_key(text):
        """핵심 단어 추출로 유사 콘텐츠 감지"""
        import re
        t = text.lower().strip()
        # 숫자/특수문자 제거, 핵심 단어만
        words = re.findall(r'[a-z가-힣\u4e00-\u9fff]{3,}', t)
        return " ".join(sorted(words[:8]))
    
    for a in all_news:
        rating = a.get("aiRating", {})
        summary = rating.get("enSummary", rating.get("summary", a.get("text", "")))[:100]
        key = _dedup_key(summary)
        if key and key not in seen_keys:
            seen_keys.add(key)
            unique_news.append(a)
    
    unique_tweets = []
    for t in all_tweets:
        text = t.get("text", "")[:40].lower().strip()
        if text and text not in seen_keys:
            seen_keys.add(text)
            unique_tweets.append(t)
    
    # ── 포맷: 뉴스 (중복 제거 후) ──
    from news_6551 import format_market_brief
    brief = format_market_brief(unique_news[:8])
    
    # ── 포맷: 트윗 (중복 제거 후) ──
    if unique_tweets:
        from twitter_6551 import format_sentinel
        brief += "\n\n" + format_sentinel(unique_tweets[:6])
    
    # ── AI 시장 분석 추가 ──
    try:
        from llm import call_llm, MODEL_FAST
        # 뉴스 + 트윗 요약을 컨텍스트로 AI 분석
        news_ctx = []
        for a in unique_news[:6]:
            rating = a.get("aiRating", {})
            s = rating.get("enSummary", rating.get("summary", ""))
            score = rating.get("score", 0)
            signal = rating.get("signal", "")
            if s:
                news_ctx.append(f"[{signal}/{score}] {s[:80]}")
        for t in unique_tweets[:4]:
            text = t.get("text", "")[:80]
            acc = t.get("_source_account", t.get("userScreenName", ""))
            if text:
                news_ctx.append(f"[@{acc}] {text}")
        
        if news_ctx:
            ctx_str = "\n".join(news_ctx)
            lang = "ko"  # 기본 한국어
            analysis = call_llm(
                messages=[{
                    "role": "system",
                    "content": "You are a Korean stock market analyst. Analyze the following news and provide: 1) Key market impact on KOSPI/KOSDAQ 2) Risk factors 3) Sector implications. Write in Korean. Be concise (150 words max)."
                }, {
                    "role": "user",
                    "content": f"오늘의 주요 뉴스:\n{ctx_str}\n\n한국 증시에 미치는 영향을 분석해주세요."
                }],
                model=MODEL_FAST, max_tokens=300, temperature=0.2,
            )
            if analysis:
                brief += f"\n\n🧠 *시장 영향 분석*\n{analysis}"
    except:
        pass
    
    return brief


def _handle_market_news_fallback():
    """Intelligence 실패 시 기존 방식 fallback"""
    from forum_scraper import fetch_naver_news, fetch_naver_ssr, fetch_realtime_price

    MAJOR_TICKERS = [
        "005930", "000660", "035420", "035720", "373220",
        "005380", "000270", "068270", "051910", "006400",
    ]

    lines = [f"📰 *한국 증시 오늘의 뉴스*", f"⏰ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]

    all_news = []
    seen = set()
    for ticker in MAJOR_TICKERS:
        try:
            news = fetch_naver_news(ticker, count=3)
            name = _resolve_stock_name(ticker)
            for n in news:
                if n["title"][:30] not in seen:
                    seen.add(n["title"][:30])
                    n["stock"] = name
                    all_news.append(n)
        except:
            continue

    all_news.sort(key=lambda x: x.get("datetime", ""), reverse=True)
    for i, n in enumerate(all_news[:15], 1):
        linked = make_news_link(n)
        lines.append(f"{i}. *[{n.get('stock','')}]* {linked}")

    return "\n".join(lines)


def handle_research(ticker):
    """증권사 리서치/목표가"""
    try:
        from forum_scraper import fetch_naver_ssr, STOCK_MAP
        name = STOCK_MAP.get(ticker, _resolve_stock_name(ticker))

        ssr = fetch_naver_ssr(ticker)
        if not ssr or not ssr["researches"]:
            return f"📋 {name} 증권사 리서치 데이터가 없습니다."

        lines = [f"📋 *{name} ({ticker}) 증권사 리서치*", ""]
        for r in ssr["researches"]:
            tp = f" | 조회 {r['target_price']}" if r.get("target_price") else ""
            link = r.get("link", "")
            title_text = r['title']
            if link:
                title_text = f"[{r['title']}]({link})"
            lines.append(f"• *{r['broker']}* ({r['date']})")
            lines.append(f"  {title_text}{tp}")
            lines.append("")

        return "\n".join(lines)
    except Exception as e:
        return f"❌ 리서치 조회 오류: {e}"


def handle_supply_demand(ticker):
    """수급 동향 (외국인/기관/개인)"""
    try:
        from forum_scraper import fetch_naver_ssr, fetch_realtime_price, STOCK_MAP
        name = STOCK_MAP.get(ticker, _resolve_stock_name(ticker))

        ssr = fetch_naver_ssr(ticker)
        if not ssr or not ssr["deal_trends"]:
            return f"📈 {name} 수급 데이터가 없습니다."

        # 실시간 가격
        rt = fetch_realtime_price(ticker)

        lines = [f"📈 *{name} ({ticker}) 수급 동향*", ""]

        if rt:
            arrow = "🔴" if rt["change"] < 0 else "🟢"
            lines.append(f"💰 {arrow} ₩{rt['price']:,} ({rt['change']:+,} / {rt['change_pct']:+.2f}%)")
            lines.append("")

        lines.append("| 일자 | 외국인 | 기관 | 개인 |")
        lines.append("|---|---|---|---|")
        for d in ssr["deal_trends"]:
            lines.append(f"| {d['date']} | {d['foreign']} | {d['institution']} | {d['individual']} |")

        if ssr["deal_trends"]:
            d = ssr["deal_trends"][0]
            if d.get("foreign_ratio"):
                lines.append(f"\n외국인 보유비율: {d['foreign_ratio']}")

        return "\n".join(lines)
    except Exception as e:
        return f"❌ 수급 조회 오류: {e}"


def handle_why_move(ticker, date_str, direction="drop"):
    """왜 올랐어/빠졌어"""
    data = get_stock(ticker, date_str)
    if not data:
        return f"❌ 데이터를 가져올 수 없습니다."

    name = _resolve_stock_name(ticker)
    pct = data["change_pct"]

    # 섹터 분석
    from crash_alert import CRASH_PATTERNS
    sector = "default"
    for sec_name, sec_info in CRASH_PATTERNS.items():
        if ticker in sec_info["tickers"]:
            sector = sec_name
            break

    # 동종 종목 체크
    peers = []
    sec_tickers = CRASH_PATTERNS.get(sector, {}).get("tickers", [])
    for peer in sec_tickers:
        if peer != ticker:
            p = get_stock(peer, date_str)
            if p:
                peers.append(p)

    # 시장 상태
    idx = get_stock(INDEX_ETFS["KOSPI"]["ticker"], date_str)
    market_status = ""
    if idx:
        if idx["change_pct"] < -1:
            market_status = "KOSPI 전체 약세 (시장 전반 리스크오프)"
        elif idx["change_pct"] > 1:
            market_status = "KOSPI 전체 강세 (시장 전반 리스크온)"

    # 구성
    lines = [
        f"🧠 *{name} 분석*\n",
        f"📊 오늘: ₩{data['close']:,} ({pct:+.1f}%)",
        f"📦 거래량: {data['volume']:,}\n",
        f"*분석:*",
    ]

    if abs(pct) < 1:
        lines.append(f"• 소폭 변동 — 특별한 이슈 감지되지 않음")
    elif pct < -3:
        lines.append(f"• {'급락' if pct < -5 else '하락'} 수준 — 주의 필요")
    elif pct > 3:
        lines.append(f"• {'급등' if pct > 5 else '상승'} — 모멘텀 주의")

    if market_status:
        lines.append(f"• {market_status}")

    if peers:
        peer_moves = [f"{STOCK_NAMES.get(p['ticker'], p['ticker'])} {p['change_pct']:+.1f}%"
                      for p in peers]
        same_dir = sum(1 for p in peers if (p["change_pct"] < 0) == (pct < 0))
        if same_dir > 0:
            lines.append(f"• {sector.upper()} 섹터 동반 {'하락' if pct < 0 else '상승'}: {', '.join(peer_moves)}")
        else:
            lines.append(f"• 섹터 내 차별화: {', '.join(peer_moves)}")

    # LLM 심층 분석 추가
    try:
        from forum_scraper import fetch_naver_ssr, fetch_naver_news
        from llm import analyze_stock

        ssr = fetch_naver_ssr(ticker) or {}
        news = fetch_naver_news(ticker, count=5)

        context = {
            "price": data,
            "sector": sector,
            "peers": [{"name": STOCK_NAMES.get(p["ticker"], p["ticker"]), "change": p["change_pct"]} for p in peers],
            "market": market_status,
            "news": [n["title"] for n in news[:5]],
            "supply": ssr.get("deal_trends", [{}])[:1],
            "research": [{"broker": r["broker"], "title": r["title"]} for r in ssr.get("researches", [])[:3]],
        }

        query = f"{name} 왜 {'빠졌어' if direction == 'drop' else '올랐어'}?"
        ai_analysis = analyze_stock(ticker, name, context, query)
        lines.append(f"\n🤖 *AI 분석:*\n{ai_analysis}")
    except Exception as e:
        lines.append(f"\n📋 DART 공시는 DART API Key 설정 후 자동 매칭됩니다.")

    lines.append(f"\n⚠️ 정보 제공 목적이며 투자 조언이 아닙니다.")

    return "\n".join(lines)


def handle_market_overview(date_str):
    """시장 전체 개요 (확장: 실제지수 + 투자자별 + 환율 + VIX + Fear&Greed + 업종)"""
    watchlist = [t.strip() for t in DEFAULT_WATCHLIST.split(",")]
    data = fetch_all(date_str, watchlist)

    lines = [f"📊 *한국 증시 현황 — {date_str}*\n"]

    # 실제 지수 (Daum) 우선, fallback to ETF proxy
    real_idx_used = False
    try:
        from market_data import fetch_real_indices, format_real_indices
        real_idx = fetch_real_indices()
        if real_idx and ("KOSPI" in real_idx or "KOSDAQ" in real_idx):
            lines.append(format_real_indices(real_idx))
            real_idx_used = True
    except:
        pass

    if not real_idx_used:
        # 기존 ETF 프록시 fallback
        for name, d in data["indices"].items():
            a = fmt_arrow(d["change_pct"])
            lines.append(f"{a} {name}: {d['close']:,} ({d['change_pct']:+.1f}%)")

    # TOP 상승/하락
    lines.append(f"\n*상승 TOP 3:*")
    for d in data["gainers"][:3]:
        lines.append(f"🟢 {d['name']} {d['change_pct']:+.1f}%")

    lines.append(f"\n*하락 TOP 3:*")
    for d in data["losers"][:3]:
        lines.append(f"🔴 {d['name']} {d['change_pct']:+.1f}%")

    # 추가 데이터 (환율 + VIX + Fear&Greed + S&P500)
    try:
        from market_data import fetch_exchange_rates, fetch_vix, fetch_fear_greed, fetch_us_indices
        
        fx = fetch_exchange_rates()
        if fx and fx.get("USD/KRW"):
            lines.append(f"\n💱 *환율*")
            lines.append(f"  USD/KRW: {fx['USD/KRW']:,.2f}")
            if fx.get("USD/JPY"):
                lines.append(f"  USD/JPY: {fx['USD/JPY']:,.2f}")

        us = fetch_us_indices()
        if us and "S&P500" in us:
            sp = us["S&P500"]
            a = "📈" if sp["change"] > 0 else "📉"
            lines.append(f"\n🇺🇸 S&P500: {sp['price']:,.2f} ({sp['change_pct']:+.2f}%) {a}")

        vix = fetch_vix()
        if vix:
            v = vix["value"]
            vlabel = "Low" if v < 15 else "Normal" if v < 25 else "⚠High" if v < 35 else "🚨Extreme"
            lines.append(f"😱 VIX: {v:.1f} ({vlabel})")
            if v >= 25:
                lines.append(f"  ↳ VIX 25+ 최근 사례: 외국인 순매도 가속, 단기 변동성 확대 구간")
            elif v >= 20:
                lines.append(f"  ↳ VIX 20-25: 경계 수준, 급변 가능성 주시")

        fng = fetch_fear_greed()
        if fng:
            v = fng["value"]
            emoji = "😱" if v < 25 else "😟" if v < 45 else "😐" if v < 55 else "😊" if v < 75 else "🤑"
            lines.append(f"{emoji} Fear&Greed: {v}/100 ({fng['label']})")
            if v < 25:
                lines.append(f"  ↳ 극단적 공포: 역사적 반등 확률 높으나 추가 하락 가능")
            elif v < 40:
                lines.append(f"  ↳ 공포 구간: 보수적 포지션 유지 권장")
            elif v > 75:
                lines.append(f"  ↳ 탐욕 구간: 차익실현 검토 시점")
    except:
        pass

    # 업종 요약 (상위 3 상승/하락)
    try:
        from market_data import fetch_sector_ranking
        from daum_finance import format_daum_sectors
        sectors = fetch_sector_ranking()
        if sectors:
            lines.append("")
            lines.append(format_daum_sectors(sectors, top_n=3))
    except:
        pass

    return "\n".join(lines)


def handle_compare(tickers, date_str):
    """종목 비교"""
    if len(tickers) < 2:
        return "❌ 비교하려면 2개 이상의 종목이 필요합니다."

    lines = [f"📊 *종목 비교 — {date_str}*\n"]
    for ticker in tickers[:5]:
        data = get_stock(ticker, date_str)
        if data:
            name = _resolve_stock_name(ticker)
            a = fmt_arrow(data["change_pct"])
            lines.append(
                f"{a} {name}: ₩{data['close']:,} ({data['change_pct']:+.1f}%) "
                f"Vol: {data['volume']:,}"
            )
    return "\n".join(lines)


def handle_outlook(date_str):
    """전망"""
    idx = get_stock(INDEX_ETFS["KOSPI"]["ticker"], date_str)
    lines = [f"🔮 *시장 전망 판단 요소*\n"]

    if idx:
        if idx["change_pct"] < -2:
            lines.append(f"📉 KOSPI 2%+ 하락 — 단기 약세 신호")
            lines.append(f"• 추가 하락 시 기술적 지지선 확인 필요")
            lines.append(f"• 외국인 순매도 지속 여부가 핵심")
        elif idx["change_pct"] > 2:
            lines.append(f"📈 KOSPI 2%+ 상승 — 단기 강세 신호")
            lines.append(f"• 거래량 동반 상승인지 확인 필요")
        else:
            lines.append(f"➡️ KOSPI 보합권 — 방향성 탐색 중")

    lines.extend([
        f"\n*주요 변수:*",
        f"• 미국 CPI/금리 결정",
        f"• 국제 유가 동향",
        f"• 외국인 투자 흐름",
        f"• 중국 경기 지표",
        f"\n⚠️ 시장 전망은 참고용이며 투자 판단의 근거가 될 수 없습니다.",
    ])
    return "\n".join(lines)


# ─── 메인 라우터 ───

def handle_community(ticker):
    """커뮤니티 종합 분석 (종토방 + Google + Twitter)"""
    try:
        name = _resolve_stock_name(ticker)
        from community_scraper import fetch_all_community, format_community
        items = fetch_all_community(ticker, name, count=12)
        if items:
            return format_community(items, name)
    except Exception as e:
        pass
    
    # fallback: 기존 forum_scraper
    try:
        from forum_scraper import get_full_report, format_report
        report = get_full_report(ticker)
        return format_report(report)
    except Exception as e:
        return f"❌ 커뮤니티 분석 오류: {e}"


def _detect_lang(text):
    """언어 감지"""
    if re.search(r'[가-힣]', text):
        return "ko"
    if re.search(r'[\u4e00-\u9fff]', text):
        return "zh"
    return "en"


def _localize_response(result, text):
    """데이터 응답을 사용자 언어로 변환 (LLM 사용)"""
    lang = _detect_lang(text)
    if lang == "ko":
        return result  # 기본 한국어, 변환 불필요

    # 중국어/영어 → LLM 번역
    try:
        from llm import call_llm, MODEL_FAST
        lang_name = "Chinese" if lang == "zh" else "English"
        translated = call_llm(
            messages=[
                {"role": "system", "content": f"Translate this Korean stock market report to {lang_name}. Keep all numbers, stock names, and emojis. Output ONLY the translation."},
                {"role": "user", "content": result},
            ],
            model=MODEL_FAST,
            max_tokens=800,
            temperature=0,
        )
        return translated or result
    except:
        return result


def handle_sector_ranking(text):
    """업종 등락 랭킹 (Daum WICS)"""
    try:
        from market_data import fetch_sector_ranking
        from daum_finance import format_daum_sectors
        lang = _detect_lang(text)
        sectors = fetch_sector_ranking()
        if sectors:
            return format_daum_sectors(sectors, lang=lang, top_n=5)
        return "❌ 업종 데이터를 가져올 수 없습니다."
    except Exception as e:
        return f"❌ 업종 조회 오류: {e}"


def handle_hot_rank(text):
    """실시간 인기 종목 (Daum 검색 순위)"""
    try:
        from market_data import fetch_hot_stocks
        from daum_finance import format_daum_hot_ranks
        lang = _detect_lang(text)
        ranks = fetch_hot_stocks()
        if ranks:
            return format_daum_hot_ranks(ranks, lang=lang, top_n=10)
        return "❌ 인기 종목 데이터를 가져올 수 없습니다."
    except Exception as e:
        return f"❌ 인기 종목 조회 오류: {e}"


def process_query_fast(text, date_str=None, user_id=None):
    """Phase 1: 즉시 데이터 응답 (LLM 없음, 1-5초)"""
    date_str = date_str or find_trading_date()
    intent = classify_intent(text)
    ticker = resolve_ticker(text)

    # 컨텍스트 추론
    if user_id:
        try:
            from conversation import resolve_from_context
            ctx_ticker, _ = resolve_from_context(user_id, text, ticker)
            if ctx_ticker and not ticker:
                # 커뮤니티/시장 등 일반 질문은 컨텍스트 종목 주입 안함
                if intent not in (Intent.COMMUNITY, Intent.MARKET_OVERVIEW, Intent.FEAR_GREED,
                                  Intent.SECTOR_RANKING, Intent.HOT_RANK):
                    ticker = ctx_ticker
                    if intent in (Intent.UNKNOWN, Intent.CHAT):
                        intent = Intent.STOCK_PRICE
        except:
            pass

    # 데이터만 (LLM 없이)
    lang = _detect_lang(text)
    if intent == Intent.COMMODITY:
        try:
            from commodities import query_commodity
            result, handled = query_commodity(text, lang)
            if not handled:
                result = "❌ 원자재를 인식하지 못했습니다. 금/은/구리/원유 등을 입력해주세요."
        except Exception as e:
            result = f"❌ 원자재 시세 조회 오류: {e}"
    elif intent == Intent.CRYPTO:
        try:
            from crypto import resolve_crypto, fetch_price, format_price
            symbol = resolve_crypto(text)
            if symbol:
                data = fetch_price(symbol)
                result = format_price(data)
            else:
                result = "❌ 코인을 인식하지 못했습니다."
        except Exception as e:
            result = f"❌ 코인 가격 조회 오류: {e}"
    elif intent == Intent.STOCK_PRICE and ticker:
        result = handle_stock_price(ticker, date_str, user_query=text, deep_analysis=False)
    elif intent == Intent.MARKET_OVERVIEW:
        result = handle_market_overview(date_str)
    elif intent == Intent.NEWS:
        result = handle_news(ticker)
    elif intent == Intent.COMMUNITY:
        # 부정/범위전환 감지: "카카오 말고 한국 전체" 등
        _t_lower = text.lower()
        _neg = any(p in _t_lower for p in ["말고", "아니라", "아니고", "대신", "빼고", "제외", "不要", "不是", "not that", "instead"])
        _gen = any(p in _t_lower for p in ["한국", "전반", "전체", "시장", "코스피", "코스닥", "韩国", "整体", "市场", "korea", "market", "overall", "투자자", "investor", "投资者"])
        if _neg or _gen:
            ticker = None  # 일반 시장 → 개별종목 무시
        t = ticker or "005930"
        if not ticker:
            # 전체 시장 분위기 → fast에서는 간단 안내, deep에서 본격 분석
            result = "🔍 한국 전체 투자자 분위기를 분석 중입니다... 잠시만 기다려주세요."
        else:
            result = handle_community(t)
    elif intent == Intent.RESEARCH:
        t = ticker or "005930"
        result = handle_research(t)
    elif intent in (Intent.SUPPLY_DEMAND, Intent.FOREIGN_FLOW):
        t = ticker or "005930"
        result = handle_supply_demand(t)
    elif intent == Intent.COMPARE:
        tickers = resolve_multiple_tickers(text)
        if len(tickers) >= 2:
            result = handle_compare(tickers, date_str)
        else:
            result = "❌ 비교할 종목을 2개 이상 언급해주세요."
    elif intent == Intent.SECTOR_RANKING:
        result = handle_sector_ranking(text)
    elif intent == Intent.HOT_RANK:
        result = handle_hot_rank(text)
    elif intent in (Intent.CHAT, Intent.UNKNOWN):
        # 대화는 Phase1에서 Haiku로 빠르게
        try:
            from llm import chat_response
            result = chat_response(text)
        except:
            result = "💬 잠시 후 다시 시도해주세요."
    elif intent in (Intent.WHY_DROP, Intent.WHY_RISE):
        if ticker:
            # 특정 종목 하락/상승 원인 → 그 종목 데이터
            result = handle_stock_price(ticker, date_str, user_query=text, deep_analysis=False)
        else:
            # 시장 전체 하락/상승 원인 → 시장 개요 + "분석 중" 안내
            result = "🔍 시장 전체 하락/상승 원인을 분석 중입니다... 잠시만 기다려주세요."
            try:
                result = handle_market_overview(date_str)
            except:
                pass
    elif intent == Intent.OUTLOOK:
        result = handle_outlook(date_str)
    else:
        if ticker:
            result = handle_stock_price(ticker, date_str, user_query=text, deep_analysis=False)
        else:
            try:
                from llm import chat_response
                result = chat_response(text)
            except:
                result = "❓ 종목명을 입력해주세요."

    # 투자 조언 합규 필터 적용
    if result:
        try:
            from llm import compliance_filter
            result = compliance_filter(result, lang=_detect_lang(text))
        except Exception:
            pass

    # 컨텍스트 저장
    if user_id:
        try:
            from conversation import update_context
            update_context(user_id, ticker=ticker, intent=intent, query=text, response=result[:300] if result else "")
        except:
            pass

    return result


def _fetch_global_news_for_stock(name_en, ticker):
    """종목 관련 글로벌 외매 뉴스 — Google News + Yahoo + Bing"""
    if not requests:
        return []

    EN_NAMES = {
        "005930": "Samsung Electronics", "000660": "SK Hynix",
        "035420": "Naver Corp", "035720": "Kakao Corp", "005380": "Hyundai Motor",
        "000270": "Kia Corp", "068270": "Celltrion", "373220": "LG Energy Solution",
        "051910": "LG Chem", "006400": "Samsung SDI", "066570": "LG Electronics",
        "096770": "SK Innovation", "036570": "NCsoft", "352820": "HYBE",
        "086520": "EcoPro", "196170": "Alteogen",
    }
    YAHOO_TICKERS = {
        "005930": "005930.KS", "000660": "000660.KS", "035420": "035420.KS",
        "035720": "035720.KS", "005380": "005380.KS", "000270": "000270.KS",
    }

    query = EN_NAMES.get(ticker, name_en)
    H = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    results = []
    seen = set()

    # 1. Google News RSS (최고 품질, source 포함)
    try:
        resp = requests.get(
            f"https://news.google.com/rss/search?q={query.replace(' ','+')}+stock&hl=en-US&gl=US&ceid=US:en",
            headers=H, timeout=8
        )
        if resp.status_code == 200:
            items = re.findall(r'<item>(.*?)</item>', resp.text, re.DOTALL)
            for item_xml in items[:5]:
                title_m = re.search(r'<title>([^<]+)</title>', item_xml)
                link_m = re.search(r'<link>([^<]+)</link>', item_xml)
                source_m = re.search(r'<source[^>]*>([^<]+)</source>', item_xml)
                if title_m:
                    title = title_m.group(1).strip()
                    # 去掉 "- Source" 后缀
                    title_clean = re.sub(r'\s*-\s*[^-]+$', '', title)
                    source_name = source_m.group(1).strip() if source_m else "Google"
                    if title_clean[:20] not in seen:
                        seen.add(title_clean[:20])
                        results.append({
                            "title": title_clean,
                            "link": link_m.group(1).strip() if link_m else "",
                            "source": source_name,
                            "desc": "",  # Google News没有desc
                        })
    except:
        pass

    # 2. Yahoo Finance RSS (有 description!)
    yt = YAHOO_TICKERS.get(ticker)
    if yt:
        try:
            resp = requests.get(
                f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={yt}&region=US&lang=en-US",
                headers=H, timeout=8
            )
            if resp.status_code == 200:
                items = re.findall(r'<item>(.*?)</item>', resp.text, re.DOTALL)
                for item_xml in items[:5]:
                    title_m = re.search(r'<title>([^<]+)</title>', item_xml)
                    link_m = re.search(r'<link>([^<]+)</link>', item_xml)
                    desc_m = re.search(r'<description>([^<]+)</description>', item_xml)
                    if title_m:
                        title = title_m.group(1).strip()
                        if title[:20] not in seen:
                            seen.add(title[:20])
                            results.append({
                                "title": title,
                                "link": link_m.group(1).strip() if link_m else "",
                                "source": "Yahoo",
                                "desc": desc_m.group(1).strip()[:120] if desc_m else "",
                            })
        except:
            pass

    # 3. Bing News fallback
    if len(results) < 3:
        try:
            resp = requests.get(
                f"https://www.bing.com/news/search?q={query.replace(' ','+')}+stock&format=rss",
                headers=H, timeout=8
            )
            if resp.status_code == 200:
                items = re.findall(r'<item>.*?<title>([^<]+)</title>.*?<link>([^<]+)</link>', resp.text, re.DOTALL)
                for title, link in items[:3]:
                    title = title.strip()
                    if title[:20] not in seen:
                        seen.add(title[:20])
                        results.append({"title": title, "link": link.strip(), "source": "Bing"})
        except:
            pass

    return results[:7]


def process_query_deep(text, date_str=None, user_id=None):
    """Phase 2: AI 심층 분석 + 외매 뉴스 + 포럼 정수 + 클릭 가능 링크"""
    date_str = date_str or find_trading_date()
    intent = classify_intent(text)
    ticker = resolve_ticker(text)

    # ── 부정/범위전환 감지 (process_query_fast와 동일) ──
    _t_lower = text.lower()
    _neg = any(p in _t_lower for p in ["말고", "아니라", "아니고", "대신", "빼고", "제외", "不要", "不是", "not that", "instead"])
    _gen = any(p in _t_lower for p in ["한국", "전반", "전체", "시장", "코스피", "코스닥", "韩国", "整体", "市场", "korea", "market", "overall", "투자자", "investor", "投资者"])
    if (_neg or _gen) and intent in (Intent.COMMUNITY, Intent.MARKET_OVERVIEW, Intent.FEAR_GREED, Intent.SECTOR_RANKING, Intent.HOT_RANK):
        ticker = None

    if user_id:
        try:
            from conversation import resolve_from_context
            ctx_ticker, _ = resolve_from_context(user_id, text, ticker)
            if ctx_ticker and not ticker:
                # 일반 질문은 컨텍스트 종목 주입 안함
                if intent not in (Intent.COMMUNITY, Intent.MARKET_OVERVIEW, Intent.FEAR_GREED,
                                  Intent.SECTOR_RANKING, Intent.HOT_RANK):
                    ticker = ctx_ticker
        except:
            pass

    # COMMUNITY 전체 시장 분위기 → deep에서 전체 시장 분석 제공
    if intent == Intent.COMMUNITY and not ticker:
        try:
            from llm import call_llm, MODEL_DEEP, SYSTEM_ANALYST
            import datetime as _dt
            _today = _dt.datetime.now().strftime("%Y-%m-%d")
            market_ctx = ""
            try:
                from market_data import fetch_real_indices, fetch_exchange_rates, fetch_vix, fetch_fear_greed
                idx = fetch_real_indices()
                if idx:
                    for k, v in idx.items():
                        market_ctx += f"{k}: {v.get(price,)} ({v.get(change_pct,)}%)\n"
                rates = fetch_exchange_rates()
                if rates:
                    for k, v in rates.items():
                        market_ctx += f"{k}: {v}\n"
                vix = fetch_vix()
                if vix:
                    market_ctx += f"VIX: {vix[value]:.1f}\n"
                fng = fetch_fear_greed()
                if fng:
                    market_ctx += f"Fear&Greed: {fng[value]}/100 ({fng[label]})\n"
            except:
                pass
            messages = [
                {"role": "system", "content": SYSTEM_ANALYST + f"\n\n현재 날짜: {_today}\n\n이 질문은 특정 종목이 아닌 한국 주식시장 전체의 투자자 심리/커뮤니티 분위기에 대한 질문입니다. 실제 시장 데이터를 기반으로 현재 투자자 심리를 분석해주세요. 개별 종목(카카오 등) 분석을 하지 마세요. 한국 시장 전체의 분위기를 분석하세요."},
            ]
            if market_ctx:
                messages.append({"role": "system", "content": f"현재 시장 데이터:\n{market_ctx}"})
            messages.append({"role": "user", "content": text})
            result = call_llm(messages=messages, model=MODEL_DEEP, max_tokens=2500, temperature=0.3)
            if result:
                # Trust badge
                try:
                    from trust_badge import generate_trust_badge
                    lang = _detect_lang(text)
                    badge = generate_trust_badge({}, "community", lang=lang)
                    if badge:
                        result = result + badge
                except:
                    pass
                return result
        except:
            pass
        return None

    # WHY_DROP/RISE 시장 전체 (ticker 없음) → 시장 분석
    if intent in (Intent.WHY_DROP, Intent.WHY_RISE) and not ticker:
        direction = "하락" if intent == Intent.WHY_DROP else "상승"
        try:
            from llm import call_llm, MODEL_DEEP, SYSTEM_ANALYST
            import datetime as _dt
            _today = _dt.datetime.now().strftime("%Y-%m-%d")
            market_ctx = ""
            try:
                from market_data import fetch_real_indices, fetch_exchange_rates, fetch_vix, fetch_fear_greed
                idx = fetch_real_indices()
                if idx:
                    for k, v in idx.items():
                        market_ctx += f"{k}: {v.get(price,)} ({v.get(change_pct,)}%)\n"
                rates = fetch_exchange_rates()
                if rates:
                    for k, v in rates.items():
                        market_ctx += f"{k}: {v}\n"
                vix = fetch_vix()
                if vix:
                    market_ctx += f"VIX: {vix[value]:.1f}\n"
                fng = fetch_fear_greed()
                if fng:
                    market_ctx += f"Fear&Greed: {fng[value]}/100 ({fng[label]})\n"
            except:
                pass
            messages = [
                {"role": "system", "content": SYSTEM_ANALYST + f"\n\n현재 날짜: {_today}\n\n사용자가 오늘 한국 주식시장 전체 {direction} 원인을 묻고 있습니다. 특정 종목(삼성전자 등)이 아닌 KOSPI/KOSDAQ 전체 시장의 {direction} 원인을 분석해주세요. 매크로(환율, 지정학, 금리), 섹터, 수급 관점에서 분석하세요. 개별 종목 분석을 하지 마세요."},
            ]
            if market_ctx:
                messages.append({"role": "system", "content": f"현재 시장 데이터:\n{market_ctx}"})
            messages.append({"role": "user", "content": text})
            result = call_llm(messages=messages, model=MODEL_DEEP, max_tokens=2500, temperature=0.3)
            if result:
                try:
                    from trust_badge import generate_trust_badge
                    _lang = _detect_lang(text)
                    badge = generate_trust_badge({}, str(intent), lang=_lang)
                    if badge:
                        result = result + badge
                except:
                    pass
                return result
        except:
            pass
        return None

    # 분석이 필요한 경우만
    needs_deep = intent in (Intent.STOCK_PRICE, Intent.WHY_DROP, Intent.WHY_RISE, Intent.OUTLOOK, Intent.COMMUNITY)
    if not needs_deep:
        return None
    if intent in (Intent.CHAT, Intent.UNKNOWN):
        return None

    t = ticker or "005930"
    name = STOCK_NAMES.get(t, t)

    # ═══ 데이터 수집 ═══
    context = {}
    display_lines = []
    try:
        data = get_stock(t, date_str)
        if data:
            context["price"] = data
    except:
        pass

    # 1) 네이버 SSR (수급/리서치/뉴스)
    news_links = []
    try:
        from forum_scraper import fetch_naver_ssr, fetch_naver_news, get_full_report
        ssr = fetch_naver_ssr(t)
        if ssr:
            context["supply_demand"] = ssr.get("deal_trends", [])[:3]
            context["research"] = [{"broker": r["broker"], "title": r["title"]} for r in ssr.get("researches", [])[:3]]
            context["peers"] = [{"name": c["name"], "change": c["change_pct"]} for c in ssr.get("industry_compare", [])[:5]]

        news = fetch_naver_news(t, count=5)
        context["news"] = [n["title"] for n in news[:5]]
        news_links = news[:5]
    except:
        pass

    # 2) 외매 글로벌 뉴스
    global_news = _fetch_global_news_for_stock(name, t)
    if global_news:
        context["global_news"] = [n["title"] for n in global_news]

    # 3) 네이버 커뮤니티 (OpenTalk + 종토방)
    forum_data = None
    try:
        from forum_scraper import get_full_report
        report = get_full_report(t)
        if report:
            forum_data = report
            s = report.get("sentiment", {})
            context["community_sentiment"] = {
                "label": s.get("label", ""),
                "bull": s.get("bull", 0), "bear": s.get("bear", 0),
                "ratio": s.get("ratio", 0.5),
            }
            context["hot_keywords"] = report.get("keywords", [])[:5]
            opentalk = report.get("opentalk", [])
            context["opentalk_sample"] = [f"{m.get('nickname','')}: {m.get('content','')[:60]}" for m in opentalk[:5]]
            jt = report.get("jongtobang", [])
            context["jongtobang_sample"] = [p.get("title", "")[:50] for p in jt[:5]]
    except:
        pass

    if not context:
        return None

    # ═══ Opus AI 분석 ═══
    try:
        from llm import analyze_stock
        ai = analyze_stock(t, name, context, text)
    except:
        ai = None

    # ═══ 조립: AI분석 + 외매 + 포럼 정수 + 링크 ═══
    lines = [f"🤖 *AI 심층 분석 — {name}*"]

    if ai:
        lines.append(f"\n{ai}")

    # 외매 글로벌 뉴스 (요약 포함)
    if global_news:
        # Haiku로 전체 제목 한번에 번역+요약
        lang = _detect_lang(text)
        try:
            from llm import call_llm, MODEL_FAST
            titles_text = "\n".join([f"{i+1}. {n['title']}" + (f" — {n.get('desc','')}" if n.get('desc') else "") for i, n in enumerate(global_news[:5])])
            lang_inst = {"ko": "한국어", "zh": "中文", "en": "English"}.get(lang, "한국어")
            summary = call_llm(
                messages=[{"role": "user", "content": f"다음 영어 금융 뉴스를 {lang_inst}로 번역하고 각 뉴스의 핵심을 1줄로 요약하세요. 번호를 유지하세요:\n\n{titles_text}"}],
                model=MODEL_FAST, max_tokens=400, temperature=0,
            )
            if summary:
                lines.append(f"\n*🌍 관련 외신:*")
                # 각 번호에 링크 매칭
                for i, n in enumerate(global_news[:5]):
                    # summary에서 해당 번호 줄 추출
                    pattern = rf'{i+1}[.\)]\s*(.+?)(?:\n|$)'
                    match = re.search(pattern, summary)
                    summary_line = match.group(1).strip() if match else n["title"][:55]
                    if n.get("link"):
                        short = _shorten_url(n['link'])
                        lines.append(f"  {i+1}. [{summary_line}]({short}) _— {n['source']}_")
                    else:
                        lines.append(f"  {i+1}. {summary_line} _— {n['source']}_")
            else:
                raise Exception("no summary")
        except:
            # fallback: 제목만 (파란색 링크)
            lines.append(f"\n*🌍 관련 외신:*")
            for n in global_news[:5]:
                short = _shorten_url(n['link']) if n.get('link') else ''
                if short:
                    lines.append(f"  • [{n['title'][:55]}]({short}) _— {n['source']}_")
                else:
                    lines.append(f"  • {n['title'][:55]} _— {n['source']}_")

    # 국내 뉴스 (링크 + 요약)
    if news_links:
        # Haiku로 한줄 요약
        try:
            from llm import call_llm, MODEL_FAST
            kr_titles = "\n".join([f"{i+1}. {n['title']}" for i, n in enumerate(news_links[:5])])
            lang_inst = {"ko": "한국어", "zh": "中文", "en": "English"}.get(_detect_lang(text), "한국어")
            kr_summary = call_llm(
                messages=[{"role": "user", "content": f"다음 한국 주식 뉴스의 핵심을 {lang_inst}로 각 1줄 요약하세요. 번호를 유지하세요:\n\n{kr_titles}"}],
                model=MODEL_FAST, max_tokens=300, temperature=0,
            )
            if kr_summary:
                lines.append(f"\n*📰 국내 뉴스:*")
                for i, n in enumerate(news_links[:5]):
                    pattern = rf'{i+1}[.\)]\s*(.+?)(?:\n|$)'
                    match = re.search(pattern, kr_summary)
                    summary_line = match.group(1).strip() if match else n["title"][:50]
                    short = _shorten_url(n.get('link', ''))
                    if short:
                        lines.append(f"  {i+1}. [{summary_line}]({short})")
                    else:
                        lines.append(f"  {i+1}. {summary_line}")
            else:
                raise Exception("no summary")
        except:
            lines.append(f"\n*📰 국내 뉴스:*")
            for n in news_links[:5]:
                linked = make_news_link(n)
                lines.append(f"  • [{n.get('source','')}] {linked}")

    # 포럼 정수
    if forum_data:
        s = forum_data.get("sentiment", {})
        lines.append(f"\n*🎭 커뮤니티 감성:* {s.get('label', '')}")
        lines.append(f"  매수 {s.get('bull',0)} | 매도 {s.get('bear',0)} | 비율 {s.get('ratio',0.5)*100:.0f}%")

        # 핫 키워드
        kw = forum_data.get("keywords", [])
        if kw:
            kw_str = " ".join([f"#{w}({c})" for w, c in kw[:6]])
            lines.append(f"  🔥 {kw_str}")

        # OpenTalk 정수 (감성 분류된 것만)
        opentalk = forum_data.get("opentalk", [])
        hot_talks = [m for m in opentalk if m.get("sentiment") in ("🟢", "🔴")][:4]
        if hot_talks:
            lines.append(f"\n*💬 실시간 토론 정수:*")
            for m in hot_talks:
                content = m["content"].replace("\n", " ")[:55]
                lines.append(f"  {m.get('sentiment','⚪')} {m.get('nickname','')}: {content}")

        # 종토방 인기글 (조회수 높은 순)
        jt = forum_data.get("jongtobang", [])
        hot_jt = sorted([p for p in jt if p.get("views")], key=lambda x: int(str(x.get("views","0")).replace(",","")), reverse=True)[:4]
        if not hot_jt:
            hot_jt = [p for p in jt if p.get("sentiment") in ("🟢", "🔴")][:4]
        if hot_jt:
            lines.append(f"\n*📝 종토방 인기글:*")
            for p in hot_jt:
                sent = p.get("sentiment", "⚪")
                title = p["title"][:45]
                views = p.get("views", "")
                v = f" (👁{views})" if views else ""
                lines.append(f"  {sent} {title}{v}")

    # ═══ 신뢰 증강 배지 (Trust Enhancement Badge) ═══
    try:
        from trust_badge import should_attach_badge, generate_trust_badge
        intent_str = str(intent).lower().replace("intent.", "") if intent else ""
        if should_attach_badge(intent_str):
            badge = generate_trust_badge(context, intent_str, lang=_detect_lang(text))
            if badge:
                lines.append(badge)
    except Exception:
        pass

    lines.append(f"\n⚠️ 정보 제공 목적. 투자 조언 아님.")
    return "\n".join(lines)


def process_query(text, date_str=None, user_id=None):
    """레거시 호환: 단일 응답 (fast + deep 합침)"""
    date_str = date_str or find_trading_date()
    intent = classify_intent(text)
    ticker = resolve_ticker(text)
    lang = _detect_lang(text)

    # 대화 컨텍스트에서 종목 추론
    if user_id:
        try:
            from conversation import resolve_from_context
            ctx_ticker, _ = resolve_from_context(user_id, text, ticker)
            if ctx_ticker and not ticker:
                # 커뮤니티/시장총괄 등 일반 질문은 컨텍스트 종목을 주입하지 않음
                if intent not in (Intent.COMMUNITY, Intent.MARKET_OVERVIEW, Intent.FEAR_GREED,
                                  Intent.SECTOR_RANKING, Intent.HOT_RANK):
                    ticker = ctx_ticker
                    if intent in (Intent.UNKNOWN, Intent.CHAT):
                        intent = Intent.STOCK_PRICE
        except:
            pass

    # 결과 생성 후 컨텍스트 저장
    result = _process_query_inner(text, date_str, intent, ticker, lang, user_id)

    # 투자 조언 합규 필터 적용
    if result:
        try:
            from llm import compliance_filter
            result = compliance_filter(result, lang=lang)
        except Exception:
            pass

    if user_id:
        try:
            from conversation import update_context
            update_context(
                user_id,
                ticker=ticker,
                intent=intent,
                query=text,
                response=result[:300] if result else "",
            )
        except:
            pass

    return result


def _process_query_inner(text, date_str, intent, ticker, lang, user_id):

    # ── 否定/범围切换 감지: ticker가 문맥에서 부정된 경우 무시 ──
    t_lower = text.lower()
    negation_in_text = any(p in t_lower for p in [
        "말고", "아니라", "아니고", "대신", "빼고", "제외",
        "不要", "不是", "别看", "不用", "not that", "instead", "rather than",
    ])
    general_in_text = any(p in t_lower for p in [
        "한국", "전반", "전체", "시장", "코스피", "코스닥",
        "韩国", "整体", "全体", "市场", "大盘",
        "korea", "market", "overall", "general", "whole",
    ])
    # 如果有否定信号或整体范围，且intent是通用类型，清除ticker
    if (negation_in_text or general_in_text) and intent in (
        Intent.COMMUNITY, Intent.MARKET_OVERVIEW, Intent.FEAR_GREED,
        Intent.SECTOR_RANKING, Intent.HOT_RANK,
    ):
        ticker = None

    # 데이터 응답 → 사용자 언어로 자동 변환
    def _L(result):
        """데이터 응답 다국어 변환 (한국어 아니면 LLM 번역)"""
        if lang == "ko":
            return result
        return _localize_response(result, text)

    if intent == Intent.STOCK_PRICE and ticker:
        return handle_stock_price(ticker, date_str, user_query=text)

    elif intent == Intent.WHY_DROP:
        if ticker:
            return handle_why_move(ticker, date_str, "drop")
        else:
            # 시장 전체 하락 원인 → LLM 시장 분석
            try:
                from llm import call_llm, MODEL_DEEP, SYSTEM_ANALYST
                import datetime as _dt
                _today = _dt.datetime.now().strftime("%Y-%m-%d")
                market_ctx = ""
                try:
                    from market_data import fetch_real_indices, fetch_exchange_rates, fetch_vix, fetch_fear_greed
                    idx = fetch_real_indices()
                    if idx:
                        for k, v in idx.items():
                            market_ctx += f"{k}: {v.get(price,)} ({v.get(change_pct,)}%)\n"
                    rates = fetch_exchange_rates()
                    if rates:
                        for k, v in rates.items():
                            market_ctx += f"{k}: {v}\n"
                    vix = fetch_vix()
                    if vix:
                        market_ctx += f"VIX: {vix[value]:.1f}\n"
                    fng = fetch_fear_greed()
                    if fng:
                        market_ctx += f"Fear&Greed: {fng[value]}/100 ({fng[label]})\n"
                except:
                    pass
                messages = [
                    {"role": "system", "content": SYSTEM_ANALYST + f"\n\n현재 날짜: {_today}\n\n사용자가 오늘 시장 전체 하락 원인을 묻고 있습니다. 특정 종목이 아닌 KOSPI/KOSDAQ 전체 시장의 하락 원인을 분석해주세요. 실제 데이터 기반으로 구체적인 원인을 제시하세요."},
                ]
                if market_ctx:
                    messages.append({"role": "system", "content": f"현재 시장 데이터:\n{market_ctx}"})
                messages.append({"role": "user", "content": text})
                result = call_llm(messages=messages, model=MODEL_DEEP, max_tokens=2500, temperature=0.3)
                if result:
                    try:
                        from trust_badge import generate_trust_badge
                        badge = generate_trust_badge({}, "why_drop", lang=lang)
                        if badge:
                            result = result + badge
                    except:
                        pass
                    return _L(result)
            except:
                pass
            return _L(handle_market_overview(date_str))

    elif intent == Intent.WHY_RISE:
        if ticker:
            return handle_why_move(ticker, date_str, "rise")
        else:
            try:
                from llm import call_llm, MODEL_DEEP, SYSTEM_ANALYST
                import datetime as _dt
                _today = _dt.datetime.now().strftime("%Y-%m-%d")
                market_ctx = ""
                try:
                    from market_data import fetch_real_indices, fetch_exchange_rates, fetch_vix, fetch_fear_greed
                    idx = fetch_real_indices()
                    if idx:
                        for k, v in idx.items():
                            market_ctx += f"{k}: {v.get(price,)} ({v.get(change_pct,)}%)\n"
                except:
                    pass
                messages = [
                    {"role": "system", "content": SYSTEM_ANALYST + f"\n\n현재 날짜: {_today}\n\n사용자가 오늘 시장 전체 상승 원인을 묻고 있습니다. 특정 종목이 아닌 KOSPI/KOSDAQ 전체 시장의 상승 원인을 분석해주세요."},
                ]
                if market_ctx:
                    messages.append({"role": "system", "content": f"현재 시장 데이터:\n{market_ctx}"})
                messages.append({"role": "user", "content": text})
                result = call_llm(messages=messages, model=MODEL_DEEP, max_tokens=2500, temperature=0.3)
                if result:
                    try:
                        from trust_badge import generate_trust_badge
                        badge = generate_trust_badge({}, "why_rise", lang=lang)
                        if badge:
                            result = result + badge
                    except:
                        pass
                    return _L(result)
            except:
                pass
            return _L(handle_market_overview(date_str))

    elif intent == Intent.MARKET_OVERVIEW:
        result_mo = handle_market_overview(date_str)
        try:
            from trust_badge import generate_trust_badge
            badge = generate_trust_badge({}, "market_overview", lang=lang)
            if badge:
                result_mo = result_mo + badge
        except Exception:
            pass
        return _L(result_mo)

    elif intent == Intent.COMPARE:
        tickers = resolve_multiple_tickers(text)
        if len(tickers) >= 2:
            return _L(handle_compare(tickers, date_str))
        return _L("❌ 비교할 종목을 2개 이상 언급해주세요. 예: 비교 삼성 SK하이닉스")

    elif intent == Intent.OUTLOOK:
        return _L(handle_outlook(date_str))

    elif intent == Intent.COMMUNITY:
        # 일반 시장 분위기 vs 특정 종목 커뮤니티 판별
        general_keywords = ["한국", "시장", "전반", "전체", "overall", "market", "整体", 
                           "全体", "韩国", "korea", "kospi", "코스피", "코스닥",
                           "투자자", "investor", "投资者"]
        is_general = any(w in text.lower() for w in general_keywords) or not ticker
        
        if is_general:
            # 전체 시장 분위기 → CHAT/deep 분석으로 전달 (특정 종목 X)
            try:
                from llm import call_llm, MODEL_DEEP, SYSTEM_ANALYST
                import datetime as _dt
                _today = _dt.datetime.now().strftime("%Y-%m-%d")
                
                # 시장 데이터 수집
                market_ctx = ""
                try:
                    from market_data import fetch_real_indices, fetch_exchange_rates, fetch_vix, fetch_fear_greed
                    idx = fetch_real_indices()
                    if idx:
                        for k, v in idx.items():
                            market_ctx += f"{k}: {v.get(price,)} ({v.get(change_pct,)}%)\n"
                    rates = fetch_exchange_rates()
                    if rates:
                        for k, v in rates.items():
                            market_ctx += f"{k}: {v}\n"
                    vix = fetch_vix()
                    if vix:
                        market_ctx += f"VIX: {vix[value]:.1f}\n"
                    fng = fetch_fear_greed()
                    if fng:
                        market_ctx += f"Fear&Greed: {fng[value]}/100 ({fng[label]})\n"
                except:
                    pass
                
                messages = [
                    {"role": "system", "content": SYSTEM_ANALYST + f"\n\n현재 날짜: {_today}\n\n이 질문은 특정 종목이 아닌 한국 주식시장 전체의 투자자 심리/커뮤니티 분위기에 대한 질문입니다. 실제 시장 데이터를 기반으로 현재 투자자 심리를 분석해주세요. 추측이 아닌 데이터에 근거한 분석을 제공하세요."},
                ]
                if market_ctx:
                    messages.append({"role": "system", "content": f"현재 시장 데이터:\n{market_ctx}"})
                messages.append({"role": "user", "content": text})
                
                result = call_llm(messages=messages, model=MODEL_DEEP, max_tokens=2500, temperature=0.3)
                if not result:
                    result = "죄송합니다. 다시 시도해주세요."
            except Exception as e:
                result = f"❌ 시장 분위기 분석 오류: {e}"
        else:
            # 특정 종목 커뮤니티
            t = ticker or "005930"
            result = handle_community(t)
        
        try:
            from trust_badge import generate_trust_badge
            ctx = {}
            if not is_general:
                ctx = {}  # handle_community doesnt return context
            badge = generate_trust_badge(ctx, "community", lang=lang)
            if badge:
                result = result + badge
        except Exception:
            pass
        return _L(result)

    elif intent == Intent.NEWS:
        return _L(handle_news(ticker))

    elif intent == Intent.RESEARCH:
        t = ticker or "005930"
        return _L(handle_research(t))

    elif intent == Intent.SUPPLY_DEMAND or intent == Intent.FOREIGN_FLOW:
        t = ticker or "005930"
        return _L(handle_supply_demand(t))

    elif intent == Intent.COMMODITY:
        try:
            from commodities import query_commodity
            result, handled = query_commodity(text, lang)
            if handled:
                return result
        except Exception as e:
            return f"❌ 원자재 시세 조회 오류: {e}"

    elif intent == Intent.DISCLOSURE:
        try:
            from market_data import fetch_disclosure, format_disclosure
            t = ticker or "005930"
            disc = fetch_disclosure(t, count=10)
            return _L(format_disclosure(disc, lang))
        except Exception as e:
            return f"❌ 공시 조회 오류: {e}"

    elif intent == Intent.FINANCIAL:
        try:
            from market_data import fetch_financial_summary, format_financial_summary, fetch_price_history, format_price_history
            t = ticker or "005930"
            fin = fetch_financial_summary(t)
            result = format_financial_summary(fin, lang)
            hist = fetch_price_history(t, days=7)
            if hist:
                result += "\n\n" + format_price_history(hist, lang)
            return _L(result) if result else "재무 데이터를 찾을 수 없습니다."
        except Exception as e:
            return f"❌ 재무 조회 오류: {e}"

    elif intent == Intent.EXCHANGE_RATE:
        try:
            from market_data import fetch_exchange_rates
            fx = fetch_exchange_rates()
            if not fx:
                return "❌ 환율 데이터 조회 실패"
            lines = ["💱 **환율** (실시간)" if lang == "ko" else "💱 **汇率** (实时)" if lang == "zh" else "💱 **Exchange Rates** (Live)"]
            for pair in ["USD/KRW", "USD/CNY", "USD/JPY", "EUR/USD"]:
                if pair in fx and fx[pair]:
                    lines.append(f"  {pair}: {fx[pair]:,.2f}")
            lines.append(f"\n📅 {fx.get('updated', '')}")
            return _L("\n".join(lines))
        except Exception as e:
            return f"❌ 환율 조회 오류: {e}"

    elif intent == Intent.FEAR_GREED:
        try:
            from market_data import fetch_fear_greed, fetch_vix
            lines = []
            fng = fetch_fear_greed()
            if fng:
                v = fng["value"]
                emoji = "😱" if v < 25 else "😟" if v < 45 else "😐" if v < 55 else "😊" if v < 75 else "🤑"
                label = fng["label"]
                title = "공포탐욕 지수" if lang == "ko" else "恐惧贪婪指数" if lang == "zh" else "Fear & Greed Index"
                lines.append(f"{emoji} **{title}: {v}/100** ({label})")
                hist = fng.get("history", [])
                if len(hist) > 1:
                    trend_title = "최근 7일" if lang == "ko" else "近7天" if lang == "zh" else "Last 7 days"
                    lines.append(f"\n📊 {trend_title}:")
                    for h in hist:
                        e2 = "😱" if h["value"] < 25 else "😟" if h["value"] < 45 else "😐" if h["value"] < 55 else "😊" if h["value"] < 75 else "🤑"
                        lines.append(f"  {e2} {h['value']} ({h['label']})")
            vix = fetch_vix()
            if vix:
                v = vix["value"]
                vlabel = "🟢 Low" if v < 15 else "🟡 Normal" if v < 25 else "🟠 High" if v < 35 else "🔴 Extreme"
                lines.append(f"\n😱 **VIX: {v:.1f}** ({vlabel})")
            return _L("\n".join(lines)) if lines else "❌ 데이터 조회 실패"
        except Exception as e:
            return f"❌ 공포탐욕 조회 오류: {e}"

    elif intent == Intent.SECTOR_RANKING:
        return _L(handle_sector_ranking(text))

    elif intent == Intent.HOT_RANK:
        return _L(handle_hot_rank(text))

    elif intent == Intent.CHAT:
        try:
            from llm import call_llm, MODEL_DEEP, SYSTEM_ANALYST
            # 시장 데이터 컨텍스트 수집 (분석 질문에 실제 데이터 제공)
            market_ctx = ""
            try:
                from market_data import fetch_real_indices, fetch_exchange_rates, fetch_vix, fetch_fear_greed
                idx = fetch_real_indices()
                if idx:
                    for mkt in ["KOSPI", "KOSDAQ"]:
                        info = idx.get(mkt, {})
                        if info:
                            market_ctx += f"{mkt}: {info.get('price',0):,.2f} ({info.get('change_pct',0):+.2f}%) 외국인:{info.get('foreign',0)} 기관:{info.get('institution',0)}\n"
                fx = fetch_exchange_rates()
                if fx and fx.get("USD/KRW"):
                    market_ctx += f"USD/KRW: {fx['USD/KRW']:,.2f}\n"
                vix = fetch_vix()
                if vix:
                    market_ctx += f"VIX: {vix['value']:.1f}\n"
                fng = fetch_fear_greed()
                if fng:
                    market_ctx += f"Fear&Greed: {fng['value']}/100 ({fng['label']})\n"
            except:
                pass

            messages = [
                {"role": "system", "content": SYSTEM_ANALYST + "\n\nProvide in-depth analysis. Use the market data below as context. Answer in the same language as the user's question."},
            ]
            if market_ctx:
                messages.append({"role": "system", "content": f"현재 시장 데이터:\n{market_ctx}"})
            messages.append({"role": "user", "content": text})

            result = call_llm(messages=messages, model=MODEL_DEEP, max_tokens=2500, temperature=0.3)
            if not result:
                return "죄송합니다. 다시 시도해주세요."
            # Attach trust badge for applicable intents
            try:
                from trust_badge import should_attach_badge, generate_trust_badge
                intent_str = str(intent).lower().replace("intent.", "") if intent else ""
                if should_attach_badge(intent_str):
                    badge = generate_trust_badge({}, intent_str, lang=_detect_lang(text))
                    if badge:
                        result = result + badge
            except Exception:
                pass
            return result
        except:
            return "💬 자유 대화 기능 준비 중입니다."

    else:
        if ticker:
            return handle_stock_price(ticker, date_str, user_query=text)
        try:
            from llm import chat_response
            return chat_response(text)  # LLM 자체 언어 대응
        except:
            return ("🇰🇷 *Mapulse — 한국 주식 AI 분석*\n\n"
                    "*📊 종목 조회*\n"
                    "  삼성 / 하이닉스 / 카카오\n\n"
                    "*📰 뉴스*\n"
                    "  오늘 뉴스 / 삼성 뉴스\n\n"
                    "*🧠 분석*\n"
                    "  삼성 왜 빠졌어? / 카카오 왜 올랐어?\n\n"
                    "*🎭 커뮤니티*\n"
                    "  삼성 분위기 / 하이닉스 여론\n\n"
                    "*📈 수급*\n"
                    "  삼성 수급 / 외국인 삼성\n\n"
                    "*📋 리서치*\n"
                    "  삼성 리서치 / 삼성 목표가\n\n"
                    "*🏭 업종*\n"
                    "  업종 / 행업 / 行业 / sector\n\n"
                    "*🔥 인기*\n"
                    "  인기 / 핫 / 热门 / trending\n\n"
                    "*🌍 원자재*\n"
                    "  금시세 / 은 / 구리 / 원유 / 철광석\n"
                    "  黄金 / 白银 / 铜 / 原油 / 大宗商品\n\n"
                    "*💬 자유 대화*\n"
                    "  아무 질문이나 해보세요!")


# ─── 데모 ───

def demo():
    print()
    print("  ╔══════════════════════════════════════════╗")
    print("  ║  💬 Mapulse — 대화 쿼리 엔진    ║")
    print("  ║  자연어로 한국 주식 정보 조회               ║")
    print("  ╚══════════════════════════════════════════╝")

    date_str = find_trading_date()
    print(f"\n  📅 거래일: {date_str}")

    queries = [
        "삼성 오늘 어때?",
        "SK이노 왜 빠졌어?",
        "코스피 시황",
        "비교 삼성 하이닉스 LG에너지",
        "코스피 전망",
        "엔씨소프트 왜 올랐어?",
    ]

    for q in queries:
        print(f"\n{'━' * 50}")
        print(f"  💬 \"{q}\"")
        print(f"{'━' * 50}\n")
        result = process_query(q, date_str)
        for line in result.split("\n"):
            print(f"  {line}")

    print(f"\n{'━' * 50}")
    print("  ✅ 대화 쿼리 엔진 데모 완료")
    print(f"{'━' * 50}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "demo":
        demo()
    else:
        query = " ".join(sys.argv[1:])
        print(process_query(query))
