"""YouTube via Apify bernardo/youtube-scraper"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apify_client import run_actor

ACTOR_ID = "streamers~youtube-scraper"


def fetch_youtube_trending(query: str = "ai filter", max_results: int = 20) -> list:
    """Fetch YouTube videos for a search query."""
    input_data = {
        "searchQueries": [query],
        "maxResults": max_results,
        "maxResultsShorts": 5,
    }
    return run_actor(ACTOR_ID, input_data)


def extract_youtube_trends(items: list) -> list:
    """Extract key metrics from YouTube scraper results."""
    trends = []
    for item in items:
        trends.append({
            "title": (item.get("title", "") or "")[:80],
            "channel": item.get("channelName", "") or item.get("channelTitle", ""),
            "views": item.get("viewCount", 0) or item.get("views", 0),
            "likes": item.get("likes", 0),
            "comments": item.get("commentsCount", 0) or item.get("numberOfComments", 0),
            "duration": item.get("duration", ""),
            "publishedAt": item.get("date", "") or item.get("publishedAt", ""),
            "url": item.get("url", ""),
            "isShort": item.get("isShort", False),
        })
    trends.sort(key=lambda x: x["views"], reverse=True)
    return trends


if __name__ == "__main__":
    import json
    query = sys.argv[1] if len(sys.argv) > 1 else "ai filter"
    print(f"Fetching YouTube data for: {query}")
    raw = fetch_youtube_trending(query, max_results=15)
    trends = extract_youtube_trends(raw)
    
    with open(f"/tmp/omni-channel-agent/output/youtube_raw.json", "w") as f:
        json.dump(raw, f, indent=2, ensure_ascii=False)
    with open(f"/tmp/omni-channel-agent/output/youtube_trends.json", "w") as f:
        json.dump(trends, f, indent=2, ensure_ascii=False)
    
    print(f"\nTop {min(10, len(trends))} YouTube results for '{query}':")
    for i, t in enumerate(trends[:10], 1):
        views = f"{t['views']:,}" if t['views'] else "N/A"
        print(f"  {i:2d}. {t['title'][:50]:50s} | ▶{views:>12s} | {t['channel']}")
