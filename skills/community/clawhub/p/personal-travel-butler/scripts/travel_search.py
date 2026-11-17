#!/usr/bin/env python3
"""Unified search manager for travel database - combines all search capabilities"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None

class TravelSearchManager:
    def __init__(self, db_path=None):
        self.db_path = Path(db_path) if db_path else None
        
    def search_location(self, query):
        """Main unified search function that tries all available sources"""
        
        print(f"🔍 Searching for: {query}")
        search_start = datetime.now()
        
        # 1. Check local cache first (fastest)
        print("📦 Checking local cache...")
        cached_results = self._check_cache(query)
        
        # 2. Try DuckDuckGo search (always available, good backup)
        print("🌐 Searching web sources...")
        ddg_results = self._search_duckduckgo(query)
        
        # 3. Try location APIs (if configured)
        print("📍 Checking location APIs...")
        api_results = self._search_location_apis(query)
        
        # 4. Run multi-source verification (comprehensive but slower)
        print("🔍 Running comprehensive verification...")
        verify_results = self._run_verification(query)
        
        # Compile all results with timing and source info
        search_duration = (datetime.now() - search_start).total_seconds()
        
        combined_results = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'search_duration_seconds': search_duration,
            'sources_used': [],
            'results': {
                'cache_hit': bool(cached_results),
                'web_search': ddg_results,
                'location_apis': api_results, 
                'verification': verify_results
            }
        }
        
        # Add source information to results
        if cached_results:
            combined_results['sources_used'].append('cache')
        if ddg_results:
            combined_results['sources_used'].append('web_search')
        if api_results:
            combined_results['sources_used'].append('location_apis')
        if verify_results:
            combined_results['sources_used'].append('verification')
            
        return combined_results
        
    def _check_cache(self, query):
        """Check if results are available in local cache"""
        # TODO: Implement with location_cache.py integration
        return None
        
    def _search_duckduckgo(self, query):
        """Search using DuckDuckGo as primary web source"""
        if DDGS is None:
            print("DuckDuckGo search requires the optional duckduckgo-search package.")
            return None
        try:
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=10):
                    results.append({
                        'title': r.get('title', ''),
                        'url': r.get('href', ''),
                        'snippet': r.get('body', '')[:200],
                        'source': 'duckduckgo'
                    })
            return results if results else None
        except Exception as e:
            print(f"⚠️  DuckDuckGo search failed: {e}")
            return None
            
    def _search_location_apis(self, query):
        """Search using location APIs (Amap/Baidu) if configured"""
        # TODO: Integrate with location_api.py
        return None
        
    def _run_verification(self, query):
        """Run comprehensive verification across multiple platforms"""
        # TODO: Integrate with multi_source_verify.py
        return None
        
    def format_search_results(self, results):
        """Format search results for display"""
        
        print(f"\n📊 Search Results Summary:")
        print(f"   Query: {results['query']}")
        print(f"   Duration: {results['search_duration_seconds']:.2f}s")
        print(f"   Sources used: {', '.join(results['sources_used'])}")
        
        # Display web search results (most reliable)
        if results['results']['web_search']:
            print(f"\n🌐 Web Search Results ({len(results['results']['web_search'])} found):")
            for i, result in enumerate(results['results']['web_search'][:5], 1):
                print(f"   {i}. {result['title']}")
                if result.get('snippet'):
                    print(f"      {result['snippet'][:100]}...")
                if result.get('url'):
                    print(f"      🔗 {result['url']}")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python travel_search.py search <query>")
        sys.exit(1)
        
    action = sys.argv[1]
    
    if action == "search":
        query = ' '.join(sys.argv[2:])
        
        manager = TravelSearchManager()
        results = manager.search_location(query)
        manager.format_search_results(results)

if __name__ == "__main__":
    main()
