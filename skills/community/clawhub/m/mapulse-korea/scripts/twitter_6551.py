"""
OpenTwitter (6551.io) integration for Mapulse
Replaces dead Nitter + expensive Twitter API v2
"""

import os
import json
import requests

API_BASE = "https://ai.6551.io/open"
TOKEN = os.environ.get("TWITTER_TOKEN", "")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

# 금융 속보 계정 (Mapulse 기본 모니터링)
SENTINEL_ACCOUNTS = [
    "DeItaone",       # Walter Bloomberg (fastest breaking)
    "FirstSquawk",    # Market headlines
    "LiveSquawk",     # Live market commentary
    "zerohedge",      # Financial analysis
    "unusual_whales", # Options/unusual activity
    "WatcherGuru",    # Crypto/macro alerts
    "FinancialJuice", # Economic data releases
]


def _load_token():
    """Load token from environment variables."""
    global TOKEN, HEADERS
    if TOKEN:
        return TOKEN
    TOKEN = os.environ.get("TWITTER_TOKEN", "")
    if TOKEN:
        HEADERS["Authorization"] = f"Bearer {TOKEN}"
    return TOKEN
    return ""


def _post(endpoint, data):
    """POST to 6551 API"""
    _load_token()
    if not TOKEN:
        return {"error": "TWITTER_TOKEN not configured"}
    try:
        r = requests.post(f"{API_BASE}/{endpoint}", headers=HEADERS, json=data, timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def get_user(username):
    """사용자 프로필"""
    return _post("twitter_user_info", {"username": username})


def get_user_tweets(username, count=10, product="Latest"):
    """사용자 최근 트윗"""
    return _post("twitter_user_tweets", {
        "username": username,
        "maxResults": count,
        "product": product,
    })


def search_tweets(keywords, count=20, product="Top", min_likes=0, lang=None):
    """트윗 검색"""
    data = {
        "keywords": keywords,
        "maxResults": count,
        "product": product,
    }
    if min_likes:
        data["minLikes"] = min_likes
    if lang:
        data["lang"] = lang
    return _post("twitter_search", data)


def search_stock_tweets(stock_name, ticker=None, count=10):
    """종목 관련 트윗 검색"""
    query = f"{stock_name} stock"
    if ticker:
        query += f" OR ${ticker}"
    return search_tweets(query, count=count, product="Top", min_likes=10)


def get_sentinel_latest(accounts=None, count=5):
    """속보 계정 최신 트윗 통합"""
    accounts = accounts or SENTINEL_ACCOUNTS
    all_tweets = []
    for acc in accounts:
        result = get_user_tweets(acc, count=count)
        tweets = result.get("data", result) if isinstance(result, dict) else result
        if isinstance(tweets, list):
            for t in tweets:
                t["_source_account"] = acc
                all_tweets.append(t)
    # 시간순 정렬
    all_tweets.sort(key=lambda x: x.get("createdAt", ""), reverse=True)
    return all_tweets[:count * 2]


def get_deleted_tweets(username, count=10):
    """삭제된 트윗"""
    return _post("twitter_deleted_tweets", {"username": username, "maxResults": count})


def get_kol_followers(username):
    """KOL 팔로워"""
    return _post("twitter_kol_followers", {"username": username})


# ─── Formatters ───

def format_tweets(tweets, lang="ko", max_items=5):
    """트윗 목록 포맷"""
    if not tweets:
        return "트윗을 찾을 수 없습니다." if lang == "ko" else "未找到推文" if lang == "zh" else "No tweets found"
    
    lines = []
    items = tweets if isinstance(tweets, list) else tweets.get("data", [])
    
    for t in items[:max_items]:
        text = t.get("text", t.get("content", ""))[:120]
        user = t.get("userScreenName", t.get("_source_account", ""))
        likes = t.get("favoriteCount", t.get("likeCount", 0))
        rt = t.get("retweetCount", 0)
        time_str = t.get("createdAt", "")[:16]
        
        line = f"🐦 **@{user}** [{time_str}]"
        line += f"\n  {text}"
        if likes or rt:
            line += f"\n  ❤️{likes} 🔄{rt}"
        lines.append(line)
    
    return "\n\n".join(lines)


def format_sentinel(tweets, lang="ko"):
    """속보 피드 포맷 (자동 번역)"""
    title = "🚨 **금융 속보**" if lang == "ko" else "🚨 **金融快讯**" if lang == "zh" else "🚨 **Breaking News**"
    
    items = tweets if isinstance(tweets, list) else []
    if not items:
        return title
    
    # 트윗 텍스트 수집 + 일괄 번역
    raw_texts = [t.get("text", "")[:100] for t in items[:8]]
    if lang in ("ko", "zh") and raw_texts:
        try:
            from news_6551 import _translate_batch
            translated = _translate_batch(raw_texts, lang)
        except Exception:
            translated = raw_texts
    else:
        translated = raw_texts
    
    lines = [title, ""]
    for idx, t in enumerate(items[:8]):
        acc = t.get("_source_account", t.get("userScreenName", ""))
        time_str = t.get("createdAt", "")
        if "T" in time_str:
            time_str = time_str[11:16]
        elif len(time_str) > 16:
            parts = time_str.split()
            time_str = parts[3][:5] if len(parts) > 3 else time_str[:5]
        
        text = translated[idx] if idx < len(translated) else raw_texts[idx]
        lines.append(f"⚡ [{time_str}] @{acc}")
        lines.append(f"  {text}")
        lines.append("")
    
    return "\n".join(lines)


# ─── Test ───

if __name__ == "__main__":
    print("=== Sentinel Latest ===")
    tweets = get_sentinel_latest(count=3)
    print(format_sentinel(tweets))
    
    print("\n=== Search: Samsung stock ===")
    results = search_stock_tweets("Samsung", "005930.KS", count=3)
    items = results.get("data", results) if isinstance(results, dict) else results
    print(format_tweets(items if isinstance(items, list) else [], max_items=3))
