#!/usr/bin/env python3
"""
Multi-Query Pipeline — runs the pipeline across all required query scenarios.
Covers all 5 query types from the requirements:
1. 最火 AI 滤镜/特效 Top 10
2. 热门舞蹈挑战 Top 10  
3. 热门病毒视频 Top 10
4. KOL 爆款内容 Top 5
5. 病毒视频预测（早期信号）

Usage:
    python3 run_multi_query.py                # All scenarios
    python3 run_multi_query.py --scenario 1   # Single scenario
"""

import sys, os, json, time, argparse
from datetime import datetime, timezone

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load env tokens
def _ensure_env():
    bashrc = os.path.expanduser("~/.bashrc")
    if os.path.exists(bashrc):
        with open(bashrc) as f:
            for line in f:
                line = line.strip()
                if line.startswith("export "):
                    line = line[7:]
                for key in ["APIFY_TOKEN", "TWITTER_TOKEN", "OPENNEWS_TOKEN"]:
                    if line.startswith(f"{key}=") and not os.environ.get(key):
                        val = line.split("=", 1)[1].strip().strip('"').strip("'")
                        os.environ[key] = val

_ensure_env()

from sources.tiktok import fetch_tiktok_trending, extract_tiktok_trends
from sources.youtube import fetch_youtube_trending, extract_youtube_trends
from sources.facebook_ads import fetch_facebook_ads, extract_ads_intelligence
from sources.reddit import fetch_reddit_search, extract_reddit_trends
from sources.google_trends import fetch_google_trends, extract_trends_summary

# ─── Query Scenarios ───────────────────────────────────────────

SCENARIOS = {
    1: {
        "name": "🎨 最火 AI 滤镜/特效 Top 10",
        "queries": {
            "tiktok": ["ai filter", "ai effect", "face filter"],
            "youtube": ["ai filter effect", "ai photo filter"],
            "facebook_ads": ["ai filter app", "ai photo editor"],
            "reddit": ["ai filter"],
            "google_trends": ["ai filter", "face filter", "ai effect", "photo filter", "beauty filter"],
        }
    },
    2: {
        "name": "💃 热门舞蹈挑战 Top 10",
        "queries": {
            "tiktok": ["dance challenge", "viral dance", "tiktok dance"],
            "youtube": ["dance challenge 2026", "viral dance tiktok"],
            "reddit": ["dance challenge viral"],
            "google_trends": ["dance challenge", "viral dance", "tiktok dance", "dance trend"],
        }
    },
    3: {
        "name": "🔥 热门病毒视频 Top 10",
        "queries": {
            "tiktok": ["viral video", "trending video", "viral meme"],
            "youtube": ["viral video 2026", "trending now"],
            "reddit": ["viral video"],
            "google_trends": ["viral video", "trending video", "viral meme", "tiktok viral"],
        }
    },
    4: {
        "name": "👀 KOL 爆款内容 Top 5",
        "queries": {
            "tiktok": ["ai photo generator", "ai image"],
            "youtube": ["ai generator review", "ai photo app"],
            "facebook_ads": ["ai photo generator", "ai image generator"],
            "google_trends": ["ai photo generator", "ai image generator", "ai art generator"],
        }
    },
    5: {
        "name": "🔮 病毒视频预测（早期信号）",
        "queries": {
            "tiktok": ["new filter", "new trend", "new effect"],
            "youtube": ["new ai filter", "new tiktok trend"],
            "reddit": ["new ai filter", "new trend"],
            "google_trends": ["new ai filter", "new trend 2026", "viral prediction"],
        }
    },
}


def run_scenario(scenario_id: int, max_results: int = 15) -> dict:
    """Run a single query scenario across all available sources."""
    scenario = SCENARIOS[scenario_id]
    print(f"\n{'='*60}")
    print(f"🎯 Scenario {scenario_id}: {scenario['name']}")
    print(f"{'='*60}")
    
    results = {}
    queries = scenario["queries"]
    
    # TikTok
    if "tiktok" in queries:
        try:
            all_items = []
            for q in queries["tiktok"]:
                print(f"  📡 TikTok: '{q}'")
                raw = fetch_tiktok_trending(q, max_results=max_results)
                all_items.extend(raw)
            results["tiktok"] = extract_tiktok_trends(all_items)[:10]
            print(f"  ✅ TikTok: {len(results['tiktok'])} items")
        except Exception as e:
            print(f"  ❌ TikTok: {e}")
    
    # YouTube
    if "youtube" in queries:
        try:
            all_items = []
            for q in queries["youtube"]:
                print(f"  📡 YouTube: '{q}'")
                raw = fetch_youtube_trending(q, max_results=max_results)
                all_items.extend(raw)
            results["youtube"] = extract_youtube_trends(all_items)[:10]
            print(f"  ✅ YouTube: {len(results['youtube'])} items")
        except Exception as e:
            print(f"  ❌ YouTube: {e}")
    
    # Facebook Ads
    if "facebook_ads" in queries:
        try:
            all_items = []
            for q in queries["facebook_ads"]:
                print(f"  📡 Facebook Ads: '{q}'")
                raw = fetch_facebook_ads(q, max_results=max_results)
                all_items.extend(raw)
            results["facebook_ads"] = extract_ads_intelligence(all_items)[:10]
            print(f"  ✅ Facebook Ads: {len(results['facebook_ads'])} items")
        except Exception as e:
            print(f"  ❌ Facebook Ads: {e}")
    
    # Reddit
    if "reddit" in queries:
        try:
            all_items = []
            for q in queries["reddit"]:
                print(f"  📡 Reddit: '{q}'")
                raw = fetch_reddit_search(q, max_results=max_results)
                all_items.extend(raw)
            results["reddit"] = extract_reddit_trends(all_items)[:10]
            print(f"  ✅ Reddit: {len(results['reddit'])} items")
        except Exception as e:
            print(f"  ❌ Reddit: {e}")
    
    # Google Trends
    if "google_trends" in queries:
        try:
            kws = queries["google_trends"][:5]
            print(f"  📡 Google Trends: {kws}")
            results["google_trends"] = fetch_google_trends(kws)
            print(f"  ✅ Google Trends: fetched")
        except Exception as e:
            print(f"  ❌ Google Trends: {e}")
    
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", type=int, default=0, help="Scenario ID (1-5), 0=all")
    parser.add_argument("--max-results", type=int, default=10, help="Max results per query")
    args = parser.parse_args()
    
    total_start = time.time()
    all_scenario_results = {}
    
    scenarios_to_run = [args.scenario] if args.scenario > 0 else list(SCENARIOS.keys())
    
    for sid in scenarios_to_run:
        results = run_scenario(sid, args.max_results)
        all_scenario_results[sid] = results
    
    total_elapsed = time.time() - total_start
    
    # Save results
    ts = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')
    output_path = os.path.join(OUTPUT_DIR, f"multi_query_{ts}.json")
    with open(output_path, "w") as f:
        json.dump(all_scenario_results, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n{'='*60}")
    print(f"📊 ALL SCENARIOS COMPLETE — {total_elapsed:.1f}s total")
    print(f"{'='*60}")
    for sid, results in all_scenario_results.items():
        name = SCENARIOS[sid]["name"]
        sources = [k for k, v in results.items() if v]
        print(f"  {name}: {len(sources)} sources")
    print(f"\n📦 Saved: {output_path}")


if __name__ == "__main__":
    main()
