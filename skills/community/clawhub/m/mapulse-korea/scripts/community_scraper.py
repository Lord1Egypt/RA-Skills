"""
Mapulse Community Scraper — 커뮤니티 감성 수집
Sources:
  1. Naver 종토방 (기존 forum_scraper.py) — 작동 ✅
  2. Naver OpenTalk (기존 forum_scraper.py) — 작동 ✅
  3. Naver 카페 검색 (Google RSS proxy) — 대안
  4. 팍스넷/DC Inside → Google News RSS 경유
  5. Twitter/X (6551.io API) — 배터 소진 주의

Anti-bot 대응:
  팍스넷, DC Inside, Naver 카페 직접 접근 불가 (2026.03 확인)
  → Google RSS + Naver 종토방 + 6551 Twitter로 우회
"""

import requests
import re
import os
import json
from typing import List, Dict, Optional

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


# ──────────────────────────────────────────────
# 1. Naver 종토방 + OpenTalk (기존 forum_scraper 래핑)
# ──────────────────────────────────────────────

def fetch_naver_community(ticker, count=20):
    """Naver 종토방 + OpenTalk 통합"""
    results = {"jongtobang": [], "opentalk": [], "source": "naver"}
    try:
        from forum_scraper import fetch_jongtobang, fetch_naver_ssr
        
        posts = fetch_jongtobang(ticker, pages=2)
        results["jongtobang"] = posts[:count]
        
        ssr = fetch_naver_ssr(ticker)
        if ssr and ssr.get("opentalk"):
            results["opentalk"] = ssr["opentalk"][:10]
    except Exception as e:
        results["error"] = str(e)
    
    return results


# ──────────────────────────────────────────────
# 2. Google RSS 경유 커뮤니티 검색
# ──────────────────────────────────────────────

def fetch_community_via_google(stock_name, sources=None, count=10):
    """Google News RSS로 커뮤니티 글 검색 (팍스넷, DC, 카페 포함)"""
    if sources is None:
        sources = ["paxnet", "dcinside", "cafe.naver"]
    
    results = []
    
    # 키워드 검색
    query = f"{stock_name} 주식"
    try:
        url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
        r = requests.get(url, headers=HEADERS, timeout=8)
        if r.status_code == 200:
            titles = re.findall(r'<title><!\[CDATA\[(.+?)\]\]></title>|<title>([^<]+)</title>', r.text)
            links = re.findall(r'<link>([^<]+)</link>', r.text)
            sources_found = re.findall(r'<source[^>]*>([^<]+)</source>', r.text)
            
            for i, (t1, t2) in enumerate(titles[1:count+1]):  # skip feed title
                title = (t1 or t2).strip()
                link = links[i+1] if i+1 < len(links) else ""
                source = sources_found[i] if i < len(sources_found) else "Google"
                results.append({
                    "title": title,
                    "link": link,
                    "source": source,
                    "type": "news_community",
                })
    except:
        pass
    
    return results


# ──────────────────────────────────────────────
# 3. Twitter 커뮤니티 (6551.io)
# ──────────────────────────────────────────────

def fetch_twitter_community(stock_name, count=5):
    """6551.io Twitter 검색으로 커뮤니티 감성"""
    try:
        from twitter_6551 import search_stock_tweets
        result = search_stock_tweets(stock_name, count=count)
        items = result.get("data", result) if isinstance(result, dict) else result
        if isinstance(items, list):
            return [{"text": t.get("text", "")[:120], 
                     "user": t.get("userScreenName", ""),
                     "likes": t.get("favoriteCount", 0),
                     "source": "twitter"} for t in items[:count]]
    except:
        pass
    return []


# ──────────────────────────────────────────────
# 통합 커뮤니티 데이터 + 감성 분석
# ──────────────────────────────────────────────

def fetch_all_community(ticker, stock_name, count=15):
    """모든 소스 통합 + 관련도 정렬"""
    all_items = []
    
    # 1. Naver 종토방 (가장 풍부)
    naver = fetch_naver_community(ticker, count=count)
    for p in naver.get("jongtobang", []):
        all_items.append({
            "text": p.get("title", ""),
            "source": "종토방",
            "source_icon": "📝",
            "likes": p.get("likes", 0),
            "views": p.get("views", 0),
            "link": p.get("link", ""),
            "relevance": _calc_relevance(p.get("title", ""), stock_name, p.get("views", 0), p.get("likes", 0)),
        })
    
    for p in naver.get("opentalk", []):
        all_items.append({
            "text": p.get("text", ""),
            "source": "OpenTalk",
            "source_icon": "💬",
            "likes": p.get("likes", 0),
            "views": 0,
            "relevance": _calc_relevance(p.get("text", ""), stock_name, 0, p.get("likes", 0)),
        })
    
    # 2. Google News (커뮤니티/뉴스)
    google = fetch_community_via_google(stock_name, count=5)
    for g in google:
        all_items.append({
            "text": g["title"],
            "source": g["source"],
            "source_icon": "📰",
            "likes": 0,
            "views": 0,
            "link": g.get("link", ""),
            "relevance": _calc_relevance(g["title"], stock_name, 100, 0),  # 뉴스는 기본 관련도 높음
        })
    
    # 3. Twitter
    tweets = fetch_twitter_community(stock_name, count=3)
    for t in tweets:
        all_items.append({
            "text": t["text"],
            "source": f"@{t['user']}",
            "source_icon": "🐦",
            "likes": t.get("likes", 0),
            "views": 0,
            "relevance": _calc_relevance(t["text"], stock_name, 0, t.get("likes", 0)),
        })
    
    # 관련도순 정렬
    all_items.sort(key=lambda x: x.get("relevance", 0), reverse=True)
    
    return all_items[:count]


def _calc_relevance(text, stock_name, views=0, likes=0):
    """관련도 점수 (0-100)"""
    score = 0
    t = text.lower()
    name = stock_name.lower()
    
    # 종목명 포함 +30
    if name in t or any(w in t for w in name.split()):
        score += 30
    
    # 분석 키워드 +20
    analysis_words = ["전망", "분석", "매수", "매도", "목표", "실적", "영향",
                      "하락", "상승", "급등", "급락", "이유", "원인", "기회"]
    score += sum(10 for w in analysis_words if w in t)
    score = min(score, 50)  # 키워드 최대 50
    
    # 인기도 +20
    try:
        views = int(str(views).replace(",", "")) if views else 0
        likes = int(str(likes).replace(",", "")) if likes else 0
    except:
        views, likes = 0, 0
    if views > 100:
        score += 10
    if views > 500:
        score += 10
    if likes > 5:
        score += 10
    if likes > 20:
        score += 10
    score = min(score, 100)
    
    return score


# ──────────────────────────────────────────────
# 포맷
# ──────────────────────────────────────────────

def format_community(items, stock_name, lang="ko"):
    """커뮤니티 포맷 (관련도순)"""
    if not items:
        return "커뮤니티 데이터가 없습니다." if lang == "ko" else "无社区数据" if lang == "zh" else "No community data"
    
    title = f"💬 **{stock_name} 커뮤니티**" if lang == "ko" else f"💬 **{stock_name} 社区动态**" if lang == "zh" else f"💬 **{stock_name} Community**"
    
    lines = [title, ""]
    
    # 소스별 그룹핑
    sources_seen = set()
    for item in items[:12]:
        src = item["source"]
        icon = item.get("source_icon", "📝")
        text = item["text"][:80]
        rel = item.get("relevance", 0)
        
        # 관련도 표시
        rel_bar = "🔥" if rel >= 60 else "📌" if rel >= 30 else "💭"
        
        likes = item.get("likes", 0)
        views = item.get("views", 0)
        stats = ""
        if likes:
            stats += f" ❤️{likes}"
        if views:
            stats += f" 👀{views}"
        
        lines.append(f"{rel_bar} {icon} [{src}]{stats}")
        lines.append(f"  {text}")
        lines.append("")
    
    # 소스 출처 표시
    all_sources = list(set(item["source"] for item in items))
    src_label = "출처" if lang == "ko" else "来源" if lang == "zh" else "Sources"
    lines.append(f"📊 {src_label}: {', '.join(all_sources[:5])}")
    
    return "\n".join(lines)


# ──────────────────────────────────────────────
# Test
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print("=== 삼성전자 커뮤니티 ===")
    items = fetch_all_community("005930", "삼성전자", count=10)
    print(format_community(items, "삼성전자"))
    print(f"\nTotal items: {len(items)}")
