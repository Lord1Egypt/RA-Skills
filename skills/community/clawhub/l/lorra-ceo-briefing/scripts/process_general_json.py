import json
import sys

def process_data():
    try:
        with open('reports/2026-02-02/general_data_raw.json', 'r') as f:
            data = json.load(f)
            
        # Global Scan
        print("=== GLOBAL SCAN (Top 20) ===")
        global_scan = data.get('global_scan', [])
        # Sort by heat if available? The fetcher usually returns them in some order.
        # Let's just take the first 20.
        for i, item in enumerate(global_scan[:20]):
            print(f"{i+1}. Source: {item.get('source')} | Time: {item.get('time')} | Heat: {item.get('heat')}")
            print(f"   Title: {item.get('title')}")
            print(f"   URL: {item.get('url')}")
            if item.get('hn_url'):
                print(f"   HN URL: {item.get('hn_url')}")
            print(f"   Content Snippet: {item.get('content', '')[:200]}...")
            print()

        # HN AI
        print("\n=== HN AI (Top 10) ===")
        hn_ai = data.get('hn_ai', [])
        for i, item in enumerate(hn_ai[:10]):
            print(f"{i+1}. Time: {item.get('time')}")
            print(f"   Title: {item.get('title')}")
            print(f"   URL: {item.get('url')}")
            print(f"   HN URL: {item.get('hn_url')}")
            print(f"   Content Snippet: {item.get('content', '')[:200]}...")
            print()

        # GitHub Trending
        print("\n=== GITHUB TRENDING (Top 12) ===")
        gh_trend = data.get('github_trending', [])
        for i, item in enumerate(gh_trend[:12]):
            print(f"{i+1}. Time: {item.get('time')}")
            print(f"   Title: {item.get('title')}")
            print(f"   URL: {item.get('url')}")
            # Stats are usually in title or content for github fetcher? 
            # Let's inspect content.
            print(f"   Content Snippet: {item.get('content', '')[:300]}...")
            print()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    process_data()
