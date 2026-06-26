"""Google Trends via pytrends (free, no API key needed)"""
import sys, os, json

def fetch_google_trends(keywords: list = None, timeframe: str = "now 7-d", geo: str = "US") -> dict:
    """Fetch Google Trends data for given keywords."""
    try:
        from pytrends.request import TrendReq
    except ImportError:
        print("[Google Trends] pytrends not installed, installing...")
        os.system("pip install pytrends --break-system-packages -q")
        from pytrends.request import TrendReq
    
    if keywords is None:
        keywords = ["ai filter", "ai photo", "face filter", "ai art", "ai generator"]
    
    # pytrends allows max 5 keywords per request
    pytrends = TrendReq(hl="en-US", tz=360)
    
    results = {
        "interest_over_time": {},
        "related_queries": {},
        "related_topics": {},
        "trending_searches": [],
    }
    
    # Interest over time
    try:
        pytrends.build_payload(keywords[:5], cat=0, timeframe=timeframe, geo=geo)
        iot = pytrends.interest_over_time()
        if not iot.empty:
            results["interest_over_time"] = {
                col: iot[col].tolist() for col in iot.columns if col != "isPartial"
            }
            results["dates"] = [str(d) for d in iot.index.tolist()]
    except Exception as e:
        print(f"[Google Trends] Interest over time error: {e}")
    
    # Related queries for each keyword
    try:
        for kw in keywords[:5]:
            pytrends.build_payload([kw], timeframe=timeframe, geo=geo)
            related = pytrends.related_queries()
            if kw in related and related[kw]["top"] is not None:
                results["related_queries"][kw] = related[kw]["top"].to_dict("records")[:10]
    except Exception as e:
        print(f"[Google Trends] Related queries error: {e}")
    
    # Trending searches (daily)
    try:
        trending = pytrends.trending_searches(pn="united_states")
        results["trending_searches"] = trending[0].tolist()[:20]
    except Exception as e:
        print(f"[Google Trends] Trending searches error: {e}")
    
    return results


def extract_trends_summary(data: dict) -> list:
    """Extract a summary of trends for reporting."""
    summary = []
    
    # Top related queries across all keywords
    for kw, queries in data.get("related_queries", {}).items():
        for q in queries[:5]:
            summary.append({
                "keyword": kw,
                "related_query": q.get("query", ""),
                "value": q.get("value", 0),
            })
    
    summary.sort(key=lambda x: x["value"], reverse=True)
    return summary


if __name__ == "__main__":
    keywords = sys.argv[1:] if len(sys.argv) > 1 else ["ai filter", "ai photo", "face filter", "ai art", "ai generator"]
    print(f"Fetching Google Trends for: {keywords}")
    data = fetch_google_trends(keywords)
    
    with open(f"/tmp/omni-channel-agent/output/google_trends.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    summary = extract_trends_summary(data)
    print(f"\nTop related queries:")
    for i, s in enumerate(summary[:15], 1):
        print(f"  {i:2d}. [{s['keyword']}] → {s['related_query']} (value: {s['value']})")
    
    if data.get("trending_searches"):
        print(f"\nUS Trending Searches (today):")
        for i, t in enumerate(data["trending_searches"][:10], 1):
            print(f"  {i:2d}. {t}")
