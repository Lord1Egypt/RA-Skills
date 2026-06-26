"""TikTok trends via Apify clockworks/tiktok-scraper"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apify_client import run_actor

ACTOR_ID = "clockworks~tiktok-scraper"

# Search keywords relevant to MyShell product categories
SEARCH_QUERIES = [
    "ai filter", "ai photo", "face filter", "dance challenge",
    "ai art", "viral filter", "ai generator"
]


def fetch_tiktok_trending(query: str = "ai filter", max_results: int = 20) -> list:
    """Fetch TikTok videos for a search query."""
    input_data = {
        "searchQueries": [query],
        "resultsPerPage": max_results,
        "searchSection": "/video",
        "shouldDownloadVideos": False,
        "shouldDownloadCovers": False,
        "shouldDownloadSlideshowImages": False,
    }
    return run_actor(ACTOR_ID, input_data)


def fetch_tiktok_hashtag(hashtag: str = "aifilter", max_results: int = 20) -> list:
    """Fetch TikTok videos for a specific hashtag."""
    input_data = {
        "hashtags": [hashtag],
        "resultsPerPage": max_results,
        "shouldDownloadVideos": False,
        "shouldDownloadCovers": False,
    }
    return run_actor(ACTOR_ID, input_data)


def extract_tiktok_trends(items: list) -> list:
    """Extract key metrics from TikTok scraper results."""
    trends = []
    for item in items:
        trends.append({
            "id": item.get("id", ""),
            "desc": (item.get("text", "") or "")[:100],
            "author": item.get("authorMeta", {}).get("name", "unknown"),
            "plays": item.get("playCount", 0),
            "likes": item.get("diggCount", 0),
            "comments": item.get("commentCount", 0),
            "shares": item.get("shareCount", 0),
            "music": item.get("musicMeta", {}).get("musicName", ""),
            "hashtags": [h.get("name", "") for h in item.get("hashtags", [])],
            "url": item.get("webVideoUrl", ""),
            "createTime": item.get("createTimeISO", ""),
        })
    # Sort by plays descending
    trends.sort(key=lambda x: x["plays"], reverse=True)
    return trends


if __name__ == "__main__":
    import json
    query = sys.argv[1] if len(sys.argv) > 1 else "ai filter"
    print(f"Fetching TikTok data for: {query}")
    raw = fetch_tiktok_trending(query, max_results=15)
    trends = extract_tiktok_trends(raw)
    
    # Save raw + processed
    with open(f"/tmp/omni-channel-agent/output/tiktok_raw.json", "w") as f:
        json.dump(raw, f, indent=2, ensure_ascii=False)
    with open(f"/tmp/omni-channel-agent/output/tiktok_trends.json", "w") as f:
        json.dump(trends, f, indent=2, ensure_ascii=False)
    
    print(f"\nTop {min(10, len(trends))} TikTok results for '{query}':")
    for i, t in enumerate(trends[:10], 1):
        plays = f"{t['plays']:,}" if t['plays'] else "N/A"
        print(f"  {i:2d}. {t['desc'][:50]:50s} | ▶{plays:>12s} | ❤{t['likes']:,}")
