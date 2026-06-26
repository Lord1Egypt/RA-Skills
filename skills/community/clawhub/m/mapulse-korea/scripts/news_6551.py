"""
OpenNews (6551.io) integration for Mapulse
72+ news sources with AI ratings and trading signals
"""

import os
import json
import requests

API_BASE = "https://ai.6551.io/open"
TOKEN = os.environ.get("OPENNEWS_TOKEN", "")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}


def _load_token():
    """Load token from environment variables."""
    global TOKEN, HEADERS
    if TOKEN:
        return TOKEN
    TOKEN = os.environ.get("OPENNEWS_TOKEN", "")
    if TOKEN:
        HEADERS["Authorization"] = f"Bearer {TOKEN}"
    return TOKEN


def _post(endpoint, data):
    """POST to 6551 API"""
    _load_token()
    if not TOKEN:
        return {"error": "OPENNEWS_TOKEN not configured"}
    try:
        r = requests.post(f"{API_BASE}/{endpoint}", headers=HEADERS, json=data, timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def _get(endpoint):
    """GET from 6551 API"""
    _load_token()
    if not TOKEN:
        return {"error": "OPENNEWS_TOKEN not configured"}
    try:
        r = requests.get(f"{API_BASE}/{endpoint}", headers=HEADERS, timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def get_latest(limit=10, page=1):
    """최신 뉴스"""
    return _post("news_search", {"limit": limit, "page": page})


def search_news(keyword, limit=10):
    """키워드 검색"""
    return _post("news_search", {"keyword": keyword, "limit": limit})


def get_high_score_news(min_score=70, limit=10):
    """고점수(중요) 뉴스"""
    return _post("news_search", {"minScore": min_score, "limit": limit})


def get_news_by_source(source, limit=10):
    """특정 소스 뉴스 (Bloomberg, Reuters, etc)"""
    return _post("news_search", {"source": source, "limit": limit})


def search_by_coin(coin, limit=10):
    """코인별 뉴스"""
    return _post("news_search", {"coin": coin, "limit": limit})


def get_news_types():
    """소스 목록"""
    return _get("news_type")


# ─── Formatters ───

def _extract_articles(response):
    """API 응답에서 기사 목록 추출"""
    if isinstance(response, list):
        return response
    if isinstance(response, dict):
        return response.get("data", response.get("items", response.get("articles", [])))
    return []


def _translate_batch(texts, target_lang="ko"):
    """LLM 일괄 번역 (영어→한국어/중국어)"""
    if not texts or target_lang == "en":
        return texts
    try:
        from llm import call_llm, MODEL_FAST
        lang_name = "Korean" if target_lang == "ko" else "Chinese"
        numbered = "\n".join([f"{i+1}. {t}" for i, t in enumerate(texts)])
        result = call_llm(
            messages=[{
                "role": "user",
                "content": f"Translate these financial news headlines to {lang_name}. Keep numbers. Output ONLY the numbered translations, one per line:\n\n{numbered}"
            }],
            model=MODEL_FAST, max_tokens=600, temperature=0,
        )
        if result:
            import re
            translated = {}
            for line in result.strip().split("\n"):
                m = re.match(r'(\d+)[.\)]\s*(.+)', line.strip())
                if m:
                    translated[int(m.group(1)) - 1] = m.group(2).strip()
            return [translated.get(i, texts[i]) for i in range(len(texts))]
    except Exception:
        pass
    return texts


def format_news(articles, lang="ko", max_items=5):
    """뉴스 포맷 (자동 번역 포함)"""
    items = _extract_articles(articles)
    if not items:
        return "뉴스를 찾을 수 없습니다." if lang == "ko" else "未找到新闻" if lang == "zh" else "No news found"
    
    # 요약 텍스트 수집
    summaries_raw = []
    for a in items[:max_items]:
        rating = a.get("aiRating", {})
        if lang == "zh":
            summary = rating.get("summary", rating.get("enSummary", ""))
        else:
            summary = rating.get("enSummary", rating.get("summary", ""))
        text = a.get("text", "")[:150]
        summaries_raw.append((summary or text)[:120])
    
    # 일괄 번역 (한국어/중국어)
    if lang in ("ko", "zh") and summaries_raw:
        translated = _translate_batch(summaries_raw, lang)
    else:
        translated = summaries_raw
    
    lines = []
    for idx, a in enumerate(items[:max_items]):
        # 소스
        source = a.get("newsType", a.get("source", ""))
        if not source:
            source = a.get("engineType", "news")
        
        # AI 평가
        rating = a.get("aiRating", {})
        score = rating.get("score", "")
        signal = rating.get("signal", "")
        grade = rating.get("grade", "")
        
        # 시그널 이모지
        signal_emoji = {"long": "🟢", "short": "🔴", "neutral": "⚪"}.get(signal, "⚪")
        
        # 점수 이모지
        if isinstance(score, (int, float)):
            score_emoji = "🔥" if score >= 80 else "📰" if score >= 50 else "📄"
        else:
            score_emoji = "📄"
        
        # 링크
        link = a.get("link", "")
        
        # 번역된 요약
        summary = translated[idx] if idx < len(translated) else ""
        
        line = f"{score_emoji} **[{source}]** {signal_emoji}"
        if grade:
            line += f" ({grade})"
        if summary:
            line += f"\n  {summary[:120]}"
        if link:
            line += f"\n  🔗 {link}"
        
        lines.append(line)
    
    return "\n\n".join(lines)


def format_market_brief(articles, lang="ko"):
    """시장 브리프 (고점수 뉴스만, 자동 번역)"""
    items = _extract_articles(articles)
    
    # 점수순 정렬
    scored = []
    for a in items:
        rating = a.get("aiRating", {})
        score = rating.get("score", 0)
        if isinstance(score, (int, float)) and score >= 50:
            scored.append((score, a))
    scored.sort(key=lambda x: -x[0])
    
    if not scored:
        return "최근 중요 뉴스가 없습니다." if lang == "ko" else "近期无重要新闻" if lang == "zh" else "No significant news recently"
    
    # 요약 텍스트 수집 + 일괄 번역
    summaries_raw = []
    for score, a in scored[:6]:
        rating = a.get("aiRating", {})
        if lang == "zh":
            summary = rating.get("summary", rating.get("enSummary", ""))
        else:
            summary = rating.get("enSummary", rating.get("summary", ""))
        summaries_raw.append((summary or "")[:120])
    
    if lang in ("ko", "zh") and summaries_raw:
        translated = _translate_batch(summaries_raw, lang)
    else:
        translated = summaries_raw
    
    title = "📊 **시장 브리프**" if lang == "ko" else "📊 **市场简报**" if lang == "zh" else "📊 **Market Brief**"
    lines = [title, ""]
    
    for idx, (score, a) in enumerate(scored[:6]):
        rating = a.get("aiRating", {})
        signal = rating.get("signal", "neutral")
        grade = rating.get("grade", "")
        signal_emoji = {"long": "🟢", "short": "🔴", "neutral": "⚪"}.get(signal, "⚪")
        source = a.get("newsType", a.get("source", ""))
        summary = translated[idx] if idx < len(translated) else ""
        
        lines.append(f"{signal_emoji} [{source}] **{grade}** (Score: {score})")
        lines.append(f"  {summary[:120]}")
        lines.append("")
    
    return "\n".join(lines)


# ─── Test ───

if __name__ == "__main__":
    print("=== Latest News ===")
    latest = get_latest(limit=5)
    print(format_news(latest, lang="zh"))
    
    print("\n=== High Score News ===")
    high = get_high_score_news(min_score=60, limit=5)
    print(format_market_brief(high, lang="zh"))
    
    print("\n=== Search: Samsung ===")
    samsung = search_news("Samsung", limit=3)
    print(format_news(samsung, lang="ko"))
