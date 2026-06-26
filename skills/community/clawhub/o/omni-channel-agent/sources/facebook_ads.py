"""Facebook Ads Library via Apify apify/facebook-ads-scraper"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apify_client import run_actor

ACTOR_ID = "apify~facebook-ads-scraper"


def fetch_facebook_ads(
    search_terms: str = "ai photo generator",
    country: str = "US",
    max_results: int = 30,
    media_type: str = "all",
    active_only: bool = True,
) -> list:
    """Fetch Facebook Ads Library data via Apify scraper."""
    # Build the Facebook Ads Library URL with search parameters
    import urllib.parse
    params = urllib.parse.urlencode({
        "active_status": "active" if active_only else "all",
        "ad_type": "all",
        "country": country,
        "media_type": media_type,
        "q": search_terms,
        "search_type": "keyword_unordered",
        "sort_data[direction]": "desc",
        "sort_data[mode]": "total_impressions",
    })
    fb_url = f"https://www.facebook.com/ads/library/?{params}"
    
    input_data = {
        "startUrls": [{"url": fb_url}],
        "resultsLimit": max_results,
        "activeStatus": "active" if active_only else "all",
    }
    return run_actor(ACTOR_ID, input_data)


def extract_ads_intelligence(items: list) -> list:
    """Extract structured ad intelligence from raw scraper data."""
    ads = []
    for item in items:
        snapshot = item.get("snapshot", {}) or {}
        cards = snapshot.get("cards", []) or []
        
        # Get body text from cards or snapshot
        body = ""
        if cards:
            body = cards[0].get("body", "") or ""
        if not body:
            body = snapshot.get("body", "") or ""
        if isinstance(body, dict):
            body = body.get("text", "")
        
        # Get title/cta from snapshot or first card
        title = snapshot.get("title", "") or ""
        cta = snapshot.get("ctaText", "") or ""
        link_url = snapshot.get("linkUrl", "") or ""
        if cards and not title:
            title = cards[0].get("title", "") or ""
        if cards and not link_url:
            link_url = cards[0].get("linkUrl", "") or ""
            
        ads.append({
            "pageName": str(snapshot.get("pageName", "") or item.get("pageName", "")),
            "pageID": str(item.get("pageID", "") or item.get("pageId", "")),
            "startDate": str(item.get("startDateFormatted", "") or "")[:10],
            "endDate": str(item.get("endDateFormatted", "") or "")[:10],
            "isActive": not bool(item.get("endDateFormatted")),
            "title": str(title)[:200],
            "body": str(body)[:200],
            "ctaText": str(cta),
            "linkUrl": str(link_url),
            "pageLikes": 0,
            "hasVideo": bool(snapshot.get("videos") or any(c.get("videoHdUrl") for c in cards)),
            "hasImage": bool(snapshot.get("images") or any(c.get("originalImageUrl") for c in cards)),
            "hasCards": bool(cards),
            "adArchiveID": str(item.get("adArchiveID", "") or item.get("adArchiveId", "")),
            "collationCount": item.get("collationCount", 1),
        })
    return ads


if __name__ == "__main__":
    import json
    query = sys.argv[1] if len(sys.argv) > 1 else "ai photo generator"
    print(f"Fetching Facebook Ads for: {query}")
    raw = fetch_facebook_ads(query, max_results=20)
    ads = extract_ads_intelligence(raw)
    
    with open(f"/tmp/omni-channel-agent/output/facebook_ads_raw.json", "w") as f:
        json.dump(raw, f, indent=2, ensure_ascii=False)
    with open(f"/tmp/omni-channel-agent/output/facebook_ads.json", "w") as f:
        json.dump(ads, f, indent=2, ensure_ascii=False)
    
    print(f"\nTop {min(10, len(ads))} Facebook Ads for '{query}':")
    for i, ad in enumerate(ads[:10], 1):
        status = "🟢" if ad["isActive"] else "🔴"
        print(f"  {i:2d}. {status} {ad['pageName']:30s} | {ad['startDate']:12s} | {ad['ctaText']:15s}")
