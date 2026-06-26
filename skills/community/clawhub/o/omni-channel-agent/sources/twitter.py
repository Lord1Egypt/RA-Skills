"""X/Twitter via API v2 (free tier with Bearer token)"""
import sys, os, json
import urllib.request
import urllib.error

TWITTER_TOKEN = os.environ.get("TWITTER_TOKEN", "")
TWITTER_BASE = "https://api.twitter.com/2"


def _headers():
    return {"Authorization": f"Bearer {TWITTER_TOKEN}"}


def search_recent_tweets(query: str = "ai filter", max_results: int = 20) -> list:
    """Search recent tweets (last 7 days) using Twitter API v2."""
    if not TWITTER_TOKEN:
        print("[Twitter] No TWITTER_TOKEN set, skipping")
        return []
    
    import urllib.parse
    params = urllib.parse.urlencode({
        "query": f"{query} -is:retweet lang:en",
        "max_results": min(max_results, 100),
        "tweet.fields": "created_at,public_metrics,author_id,entities",
        "expansions": "author_id",
        "user.fields": "name,username,public_metrics",
    })
    
    url = f"{TWITTER_BASE}/tweets/search/recent?{params}"
    req = urllib.request.Request(url, headers=_headers())
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            return data.get("data", [])
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"[Twitter] HTTP {e.code}: {error_body[:300]}")
        return []
    except Exception as e:
        print(f"[Twitter] Error: {e}")
        return []


def extract_twitter_trends(items: list) -> list:
    """Extract key metrics from Twitter search results."""
    trends = []
    for item in items:
        metrics = item.get("public_metrics", {})
        trends.append({
            "text": (item.get("text", "") or "")[:140],
            "author_id": item.get("author_id", ""),
            "likes": metrics.get("like_count", 0),
            "retweets": metrics.get("retweet_count", 0),
            "replies": metrics.get("reply_count", 0),
            "quotes": metrics.get("quote_count", 0),
            "impressions": metrics.get("impression_count", 0),
            "created_at": item.get("created_at", ""),
            "id": item.get("id", ""),
        })
    trends.sort(key=lambda x: x["likes"] + x["retweets"] * 2, reverse=True)
    return trends


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "ai filter"
    print(f"Fetching Twitter data for: {query}")
    raw = search_recent_tweets(query, max_results=15)
    trends = extract_twitter_trends(raw)
    
    with open(f"/tmp/omni-channel-agent/output/twitter_raw.json", "w") as f:
        json.dump(raw, f, indent=2, ensure_ascii=False)
    with open(f"/tmp/omni-channel-agent/output/twitter_trends.json", "w") as f:
        json.dump(trends, f, indent=2, ensure_ascii=False)
    
    print(f"\nTop {min(10, len(trends))} Twitter results for '{query}':")
    for i, t in enumerate(trends[:10], 1):
        print(f"  {i:2d}. ❤{t['likes']:>5,} 🔁{t['retweets']:>4,} | {t['text'][:60]}")
