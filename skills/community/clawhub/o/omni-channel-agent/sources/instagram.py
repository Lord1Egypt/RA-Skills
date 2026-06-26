"""Instagram via Apify apify/instagram-scraper"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apify_client import run_actor

ACTOR_ID = "apify~instagram-scraper"


def fetch_instagram_posts(query: str = "aifilter", max_results: int = 20) -> list:
    """Fetch Instagram posts for a hashtag."""
    input_data = {
        "directUrls": [f"https://www.instagram.com/explore/tags/{query}/"],
        "resultsType": "posts",
        "resultsLimit": max_results,
    }
    return run_actor(ACTOR_ID, input_data)


def fetch_instagram_profile(username: str, max_results: int = 12) -> list:
    """Fetch posts from a specific Instagram profile (for KOL tracking)."""
    input_data = {
        "directUrls": [f"https://www.instagram.com/{username}/"],
        "resultsType": "posts",
        "resultsLimit": max_results,
    }
    return run_actor(ACTOR_ID, input_data)


def extract_instagram_trends(items: list) -> list:
    """Extract key metrics from Instagram scraper results."""
    trends = []
    for item in items:
        if not isinstance(item, dict):
            continue
        likes = item.get("likesCount", 0) or 0
        comments = item.get("commentsCount", 0) or 0
        views = item.get("videoViewCount", 0) or item.get("videoPlayCount", 0) or 0
        total_engagement = likes + comments
        
        trends.append({
            "id": item.get("id", ""),
            "shortCode": item.get("shortCode", ""),
            "caption": (item.get("caption", "") or "")[:100],
            "owner": item.get("ownerUsername", "") or item.get("ownerFullName", "") or "unknown",
            "likes": likes,
            "comments": comments,
            "views": views,
            "type": item.get("type", "Image"),
            "hashtags": item.get("hashtags", []),
            "url": item.get("url", ""),
            "timestamp": item.get("timestamp", ""),
            "engagement_rate": 0,  # Need follower count to calculate
        })
    trends.sort(key=lambda x: x["likes"] + x.get("views", 0), reverse=True)
    return trends


if __name__ == "__main__":
    import json
    query = sys.argv[1] if len(sys.argv) > 1 else "aifilter"
    print(f"Fetching Instagram data for: #{query}")
    raw = fetch_instagram_posts(query, max_results=15)
    trends = extract_instagram_trends(raw)
    
    with open(f"/tmp/omni-channel-agent/output/instagram_raw.json", "w") as f:
        json.dump(raw, f, indent=2, ensure_ascii=False)
    with open(f"/tmp/omni-channel-agent/output/instagram_trends.json", "w") as f:
        json.dump(trends, f, indent=2, ensure_ascii=False)
    
    print(f"\nTop {min(10, len(trends))} Instagram results for #{query}:")
    for i, t in enumerate(trends[:10], 1):
        likes = f"{t['likes']:,}" if t['likes'] else "N/A"
        print(f"  {i:2d}. @{t['owner']:20s} | ❤{likes:>10s} | 💬{t['comments']:,} | {t['type']}")
