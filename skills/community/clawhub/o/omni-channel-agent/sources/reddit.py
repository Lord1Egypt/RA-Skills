"""Reddit via Apify trudax/reddit-scraper"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apify_client import run_actor

ACTOR_ID = "trudax~reddit-scraper-lite"

# Subreddits relevant to AI image generation trends
RELEVANT_SUBREDDITS = [
    "StableDiffusion", "midjourney", "AIart", "artificial",
    "comfyui", "sdforall", "aiArt", "deepfakes"
]


def fetch_reddit_posts(
    subreddits: list = None,
    sort: str = "hot",
    max_results: int = 20
) -> list:
    """Fetch Reddit posts from relevant subreddits."""
    if subreddits is None:
        subreddits = RELEVANT_SUBREDDITS[:4]
    
    input_data = {
        "startUrls": [{"url": f"https://www.reddit.com/r/{sub}/"} for sub in subreddits],
        "maxItems": max_results,
        "maxPostCount": max_results,
        "skipComments": True,
    }
    return run_actor(ACTOR_ID, input_data)


def fetch_reddit_search(query: str = "ai filter", max_results: int = 20) -> list:
    """Search Reddit for a specific query."""
    input_data = {
        "startUrls": [{"url": f"https://www.reddit.com/search/?q={query}&sort=relevance&t=week"}],
        "maxItems": max_results,
        "maxPostCount": max_results,
        "skipComments": True,
    }
    return run_actor(ACTOR_ID, input_data)


def extract_reddit_trends(items: list) -> list:
    """Extract key metrics from Reddit scraper results."""
    trends = []
    for item in items:
        trends.append({
            "title": (item.get("title", "") or "")[:100],
            "subreddit": (item.get("parsedCommunityName", "") or 
                         item.get("communityName", "") or 
                         item.get("subreddit", "")).replace("r/", ""),
            "upvotes": item.get("upVotes", 0) or item.get("score", 0) or item.get("upvoteCount", 0),
            "comments": item.get("numberOfComments", 0) or item.get("numComments", 0) or item.get("commentCount", 0),
            "author": item.get("username", "") or item.get("author", ""),
            "url": item.get("url", ""),
            "createdAt": item.get("createdAt", "") or item.get("postedAt", ""),
            "isVideo": item.get("isVideo", False),
        })
    trends.sort(key=lambda x: x["upvotes"], reverse=True)
    return trends


if __name__ == "__main__":
    import json
    query = sys.argv[1] if len(sys.argv) > 1 else "ai filter"
    print(f"Fetching Reddit data for: {query}")
    raw = fetch_reddit_search(query, max_results=15)
    trends = extract_reddit_trends(raw)
    
    with open(f"/tmp/omni-channel-agent/output/reddit_raw.json", "w") as f:
        json.dump(raw, f, indent=2, ensure_ascii=False)
    with open(f"/tmp/omni-channel-agent/output/reddit_trends.json", "w") as f:
        json.dump(trends, f, indent=2, ensure_ascii=False)
    
    print(f"\nTop {min(10, len(trends))} Reddit results for '{query}':")
    for i, t in enumerate(trends[:10], 1):
        print(f"  {i:2d}. r/{t['subreddit']:20s} | ⬆{t['upvotes']:>6,} | 💬{t['comments']:>4,} | {t['title'][:40]}")
