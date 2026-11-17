#!/usr/bin/env python3
"""Location API integration for travel database - Amap/Baidu Maps"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None

class LocationAPI:
    def __init__(self, db_path=None):
        self.db_path = Path(db_path) if db_path else None
        
    def search_amap(self, query):
        """Search using Amap (高德地图) API"""
        # Configure AMAP_API_KEY in the local environment or project .env file.
        api_key = os.getenv('AMAP_API_KEY', '')
        if not api_key:
            print("⚠️  Amap API key not configured")
            return None
            
        url = f"https://restapi.amap.com/v3/place/text?key={api_key}&keywords={query}"
        # Implementation would go here
        
    def search_baidu(self, query):
        """Search using Baidu Maps API"""
        api_key = os.getenv('BAIDU_MAPS_API_KEY', '')
        if not api_key:
            print("⚠️  Baidu Maps API key not configured")
            return None
            
        url = f"https://api.map.baidu.com/place/v2/search?query={query}&output=json&ak={api_key}"
        # Implementation would go here
        
    def search_duckduckgo(self, query):
        """Search using DuckDuckGo as backup"""
        if DDGS is None:
            print("DuckDuckGo search requires the optional duckduckgo-search package.")
            return None
        try:
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=5):
                    results.append({
                        'title': r.get('title', ''),
                        'url': r.get('href', ''),
                        'snippet': r.get('body', '')[:200]
                    })
            return results if results else None
        except Exception as e:
            print(f"⚠️  DuckDuckGo search failed: {e}")
            return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python location_api.py search <query>")
        sys.exit(1)
        
    action = sys.argv[1]
    
    if action == "search":
        query = ' '.join(sys.argv[2:])
        api = LocationAPI()
        
        # Try multiple sources in order of preference
        print(f"🔍 Searching for: {query}")
        
        # 1. Try Amap first (if configured)
        print("\n📍 Trying Amap API...")
        amap_results = api.search_amap(query)
        
        # 2. Try Baidu Maps (if configured)  
        print("🗺️  Trying Baidu Maps API...")
        baidu_results = api.search_baidu(query)
        
        # 3. DuckDuckGo as backup (always available)
        print("🌐 Trying DuckDuckGo search...")
        ddg_results = api.search_duckduckgo(query)
        
        # Return best available results
        if ddg_results:
            print(f"\n✅ Found {len(ddg_results)} results via DuckDuckGo:")
            for i, result in enumerate(ddg_results[:3], 1):
                print(f"{i}. {result['title']}")
                if result.get('snippet'):
                    print(f"   {result['snippet'][:100]}...")
                if result.get('url'):
                    print(f"   🔗 {result['url']}")
                print()

if __name__ == "__main__":
    main()
