#!/usr/bin/env python3
"""Enhanced search system with fallback mechanisms and better error handling"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import subprocess

class EnhancedSearchManager:
    def __init__(self, db_path=None):
        self.db_path = Path(db_path) if db_path else None
        
    def search_with_fallbacks(self, query):
        """Search with multiple fallback mechanisms"""
        
        print(f"🔍 Searching for: {query}")
        search_start = datetime.now()
        
        # 1. Check local cache first (fastest)
        print("📦 Checking local cache...")
        cached_results = self._check_cache(query)
        
        # 2. Try DuckDuckGo search (primary web source)
        print("🌐 Trying DuckDuckGo search...")
        ddg_results = self._search_duckduckgo(query)
        
        # 3. Try Bing search as backup (if DuckDuckGo fails)
        if not ddg_results:
            print("🔄 Trying Bing search as backup...")
            bing_results = self._search_bing(query)
        else:
            bing_results = None
            
        # 4. Try location APIs (if configured)
        print("📍 Checking location APIs...")
        api_results = self._search_location_apis(query)
        
        # 5. Run multi-source verification (comprehensive but slower)
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
                'web_search': ddg_results or bing_results,  # Use whichever worked
                'location_apis': api_results, 
                'verification': verify_results
            }
        }
        
        # Add source information to results
        if cached_results:
            combined_results['sources_used'].append('cache')
        if ddg_results or bing_results:
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
        try:
            import subprocess
            
            # Use the ddgs command line tool directly for better reliability
            result = subprocess.run(
                ['ddgs', 'text', query, '-n', '5'],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0 and result.stdout.strip():
                # Parse the output (ddgs outputs JSON)
                try:
                    results = json.loads(result.stdout)
                    if isinstance(results, list):
                        return [{'title': r.get('title', ''), 
                                'url': r.get('href', ''),
                                'snippet': r.get('body', '')[:200],
                                'source': 'duckduckgo'} for r in results]
                except:
                    pass
                    
        except Exception as e:
            print(f"⚠️  DuckDuckGo search failed: {e}")
            
        return None
        
    def _search_bing(self, query):
        """Search using Bing as backup"""
        try:
            import subprocess
            
            # Use curl to search Bing directly
            url = f"https://www.bing.com/search?q={query}&count=5"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            result = subprocess.run(
                ['curl', '-s', url, '-H', f'User-Agent: {headers["User-Agent"]}'],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0 and len(result.stdout) > 100:
                # Simple HTML parsing to extract search results
                import re
                
                titles = re.findall(r'<h2[^>]*>(.*?)</h2>', result.stdout)
                urls = re.findall(r'href="([^"]*?)"[^>]*class="[^"]*url"', result.stdout)
                snippets = re.findall(r'<p[^>]*>(.*?)</p>', result.stdout)
                
                if titles:
                    results = []
                    for i in range(min(len(titles), 5)):
                        result_item = {
                            'title': titles[i].strip(),
                            'url': urls[i] if i < len(urls) else '',
                            'snippet': snippets[i].strip()[:200] if i < len(snippets) else '',
                            'source': 'bing'
                        }
                        results.append(result_item)
                    return results if results else None
                    
        except Exception as e:
            print(f"⚠️  Bing search failed: {e}")
            
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
        print("  python enhanced_search.py search <query>")
        sys.exit(1)
        
    action = sys.argv[1]
    
    if action == "search":
        query = ' '.join(sys.argv[2:])
        
        manager = EnhancedSearchManager()
        results = manager.search_with_fallbacks(query)
        manager.format_search_results(results)

if __name__ == "__main__":
    main()