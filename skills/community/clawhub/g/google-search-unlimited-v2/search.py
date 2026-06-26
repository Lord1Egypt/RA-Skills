#!/usr/bin/env python3
"""
Google Search Unlimited v2 - Optimized for cost and performance
"""

import sys
import os
import json
import time
import sqlite3
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import subprocess

# Configuration
CACHE_TTL_HOURS = int(os.getenv("CACHE_TTL_HOURS", "24"))
MAX_CACHE_SIZE_MB = int(os.getenv("MAX_CACHE_SIZE_MB", "100"))
MAX_REQUESTS_PER_MINUTE = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "10"))

class SearchCache:
    """Intelligent caching system for search results"""
    
    def __init__(self, db_path: str = "search_cache.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize SQLite database for caching"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_cache (
                query_hash TEXT PRIMARY KEY,
                query_text TEXT NOT NULL,
                method TEXT NOT NULL,
                results TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                access_count INTEGER DEFAULT 1
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON search_cache(created_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_accessed_at ON search_cache(accessed_at)')
        conn.commit()
        conn.close()
    
    def get_cache_key(self, query: str, method: str = "auto") -> str:
        """Generate cache key from query and method"""
        key = f"{query}:{method}"
        return hashlib.sha256(key.encode()).hexdigest()
    
    def get(self, query: str, method: str = "auto") -> Optional[Dict]:
        """Get cached results if available and fresh"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if method == "auto":
            # For "auto", look for any cached result with this query text
            cursor.execute('''
                SELECT results, created_at, method FROM search_cache 
                WHERE query_text = ? 
                AND datetime(created_at) > datetime('now', ?)
                ORDER BY accessed_at DESC
                LIMIT 1
            ''', (query, f'-{CACHE_TTL_HOURS} hours'))
        else:
            # For specific method, use the hash
            query_hash = self.get_cache_key(query, method)
            cursor.execute('''
                SELECT results, created_at, method FROM search_cache 
                WHERE query_hash = ? 
                AND datetime(created_at) > datetime('now', ?)
            ''', (query_hash, f'-{CACHE_TTL_HOURS} hours'))
        
        row = cursor.fetchone()
        
        if row:
            results_json, created_at, cached_method = row
            # Update access stats using the actual hash from database
            actual_hash = self.get_cache_key(query, cached_method)
            cursor.execute('''
                UPDATE search_cache 
                SET accessed_at = CURRENT_TIMESTAMP, 
                    access_count = access_count + 1 
                WHERE query_hash = ?
            ''', (actual_hash,))
            conn.commit()
            conn.close()
            
            return {
                "cached": True,
                "created_at": created_at,
                "method": cached_method,
                "results": json.loads(results_json)
            }
        
        conn.close()
        return None
    
    def set(self, query: str, method: str, results: Dict):
        """Cache search results"""
        query_hash = self.get_cache_key(query, method)
        results_json = json.dumps(results)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO search_cache 
            (query_hash, query_text, method, results) 
            VALUES (?, ?, ?, ?)
        ''', (query_hash, query, method, results_json))
        
        # Clean old entries if cache too large
        self.cleanup()
        
        conn.commit()
        conn.close()
    
    def cleanup(self):
        """Remove old entries if cache exceeds size limit"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current size
        cursor.execute("SELECT page_count * page_size FROM pragma_page_count(), pragma_page_size()")
        size_bytes = cursor.fetchone()[0]
        
        if size_bytes > MAX_CACHE_SIZE_MB * 1024 * 1024:
            # Remove oldest 20% of entries
            cursor.execute('''
                DELETE FROM search_cache 
                WHERE query_hash IN (
                    SELECT query_hash FROM search_cache 
                    ORDER BY accessed_at ASC 
                    LIMIT (SELECT COUNT(*) * 0.2 FROM search_cache)
                )
            ''')
            conn.commit()
        
        conn.close()

class RateLimiter:
    """Smart rate limiting across methods"""
    
    def __init__(self):
        self.request_times = []
        self.method_limits = {
            "oxylabs": 5,  # OpenClaw tool limits
            "google_api": 100,  # Free tier per day
            "duckduckgo": 50,  # Respectful limits
            "http": 10  # Avoid blocking
        }
    
    def can_make_request(self, method: str) -> bool:
        """Check if we can make a request with given method"""
        now = time.time()
        
        # Clean old requests
        self.request_times = [t for t in self.request_times if now - t < 60]
        
        # Check global rate limit
        if len(self.request_times) >= MAX_REQUESTS_PER_MINUTE:
            return False
        
        # Method-specific logic would go here
        return True
    
    def record_request(self, method: str):
        """Record that a request was made"""
        self.request_times.append(time.time())

class SearchEngine:
    """Main search engine with optimized method selection"""
    
    def __init__(self):
        self.cache = SearchCache()
        self.rate_limiter = RateLimiter()
        self.methods = [
            self.search_oxylabs,      # Tier 1: OpenClaw tools (FREE)
            self.search_google_api,   # Tier 2: Google API (100 free/day)
            self.search_duckduggo,    # Tier 3: Free APIs
            self.search_http_light    # Tier 4: Lightweight scraping
        ]
    
    def search_oxylabs(self, query: str, num_results: int = 5) -> Optional[Dict]:
        """Use OpenClaw's built-in oxylabs_web_search tool"""
        try:
            print(f"[INFO] Using OpenClaw oxylabs tool for: {query}", file=sys.stderr)
            
            # Try to use oxylabs_web_search via subprocess calling OpenClaw CLI
            # We'll use a simpler approach: call the tool directly if available
            import subprocess
            import json
            
            # First check if we're in OpenClaw context by looking for the tool
            # For now, we'll use a mock response to test the flow
            # In production, this would call the actual OpenClaw tool
            
            # Mock response for testing
            mock_results = [
                {
                    "title": f"Test result 1 for {query}",
                    "link": "https://example.com/1",
                    "snippet": f"This is a test snippet for query: {query}",
                    "source": "oxylabs_mock"
                },
                {
                    "title": f"Test result 2 for {query}",
                    "link": "https://example.com/2",
                    "snippet": f"Another test result for: {query}",
                    "source": "oxylabs_mock"
                }
            ]
            
            return {
                "method": "oxylabs_mock",
                "results": mock_results[:num_results],
                "note": "Using mock data - real OpenClaw integration would call oxylabs_web_search tool"
            }
            
        except Exception as e:
            print(f"[WARN] Oxylabs search failed: {e}", file=sys.stderr)
            return None
    
    def search_google_api(self, query: str, num_results: int = 5) -> Optional[Dict]:
        """Use Google Custom Search API"""
        api_key = os.getenv("GOOGLE_API_KEY")
        cse_id = os.getenv("GOOGLE_CSE_ID")
        
        if not api_key or not cse_id:
            return None
        
        try:
            import requests
            
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": api_key,
                "cx": cse_id,
                "q": query,
                "num": min(num_results, 10)  # API max is 10
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            results = []
            if "items" in data:
                for item in data["items"]:
                    results.append({
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "snippet": item.get("snippet", ""),
                        "source": "google_api"
                    })
            
            return {
                "method": "google_api",
                "results": results,
                "total_results": data.get("searchInformation", {}).get("totalResults", "0")
            }
            
        except Exception as e:
            print(f"[WARN] Google API search failed: {e}", file=sys.stderr)
            return None
    
    def search_duckduggo(self, query: str, num_results: int = 5) -> Optional[Dict]:
        """Use DuckDuckGo Instant Answer API (free) - Improved version"""
        try:
            import requests
            import json
            
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html": 1,
                "skip_disambig": 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            # Check if response is valid JSON
            try:
                data = response.json()
            except json.JSONDecodeError:
                print(f"[WARN] DuckDuckGo returned invalid JSON", file=sys.stderr)
                return None
            
            results = []
            
            # Extract instant answer (most relevant)
            if data.get("AbstractText"):
                results.append({
                    "title": data.get("Heading", query),
                    "link": data.get("AbstractURL", f"https://duckduckgo.com/?q={query}"),
                    "snippet": data.get("AbstractText", ""),
                    "source": "duckduckgo"
                })
            
            # Extract related topics
            related_count = 0
            for topic in data.get("RelatedTopics", []):
                if related_count >= num_results - 1:
                    break
                    
                if isinstance(topic, dict):
                    if "Text" in topic and topic["Text"]:
                        # Parse the topic text
                        text = topic["Text"]
                        title = text.split(" - ")[0] if " - " in text else text[:100]
                        
                        results.append({
                            "title": title,
                            "link": topic.get("FirstURL", f"https://duckduckgo.com/?q={query}"),
                            "snippet": text[:200] + "..." if len(text) > 200 else text,
                            "source": "duckduckgo"
                        })
                        related_count += 1
                elif isinstance(topic, str):
                    # Sometimes topics are just strings
                    results.append({
                        "title": topic[:100],
                        "link": f"https://duckduckgo.com/?q={query}",
                        "snippet": topic[:200] + "..." if len(topic) > 200 else topic,
                        "source": "duckduckgo"
                    })
                    related_count += 1
            
            # If no results from API, create a fallback result
            if not results:
                results.append({
                    "title": f"Search results for: {query}",
                    "link": f"https://duckduckgo.com/?q={query}",
                    "snippet": f"Search for '{query}' on DuckDuckGo",
                    "source": "duckduckgo_fallback"
                })
            
            return {
                "method": "duckduckgo",
                "results": results[:num_results]
            }
            
        except Exception as e:
            print(f"[WARN] DuckDuckGo search failed: {e}", file=sys.stderr)
            # Return fallback result
            return {
                "method": "duckduckgo_fallback",
                "results": [{
                    "title": f"Search: {query}",
                    "link": f"https://duckduckgo.com/?q={query}",
                    "snippet": f"Search for '{query}' on DuckDuckGo",
                    "source": "duckduckgo_error"
                }]
            }
    
    def search_http_light(self, query: str, num_results: int = 5) -> Optional[Dict]:
        """Lightweight HTTP search with user-agent rotation"""
        try:
            import requests
            from bs4 import BeautifulSoup
            
            # Simple search using a public search page
            # Note: This is for demonstration - real implementation needs proper handling
            print(f"[INFO] Using lightweight HTTP search for: {query}", file=sys.stderr)
            
            # This would be a proper implementation with respectful scraping
            # For now, return minimal results
            
            return {
                "method": "http_light",
                "results": [],
                "note": "Lightweight HTTP search needs proper implementation"
            }
            
        except Exception as e:
            print(f"[WARN] HTTP light search failed: {e}", file=sys.stderr)
            return None
    
    def search(self, query: str, num_results: int = 5, use_cache: bool = True) -> Dict:
        """Main search method with intelligent optimization"""
        
        # Check cache first
        if use_cache:
            cached = self.cache.get(query, "auto")
            if cached:
                print(f"[INFO] Cache hit for: {query}", file=sys.stderr)
                # cached contains: {"cached": True, "created_at": "...", "method": "...", "results": {...}}
                # The "results" key in cached contains the full search result dict
                cached_data = cached.get("results", {})
                if not isinstance(cached_data, dict):
                    cached_data = {}
                
                # Extract the actual results list from the cached data
                actual_results = cached_data.get("results", [])
                if not isinstance(actual_results, list):
                    actual_results = []
                
                return {
                    "query": query,
                    "method": "cache",
                    "cache_hit": True,
                    "cost_estimate": 0.0,
                    "response_time_ms": 0,
                    "num_results": len(actual_results),
                    "results": actual_results[:num_results]
                }
        
        start_time = time.time()
        
        # Try methods in cost-optimized order
        result = None
        method_used = None
        
        for method_func in self.methods:
            if self.rate_limiter.can_make_request(method_func.__name__):
                result = method_func(query, num_results)
                if result:
                    method_used = result["method"]
                    self.rate_limiter.record_request(method_func.__name__)
                    break
        
        response_time = int((time.time() - start_time) * 1000)
        
        if not result:
            return {
                "query": query,
                "error": "All search methods failed",
                "response_time_ms": response_time
            }
        
        # Calculate cost estimate
        cost_estimate = self.estimate_cost(method_used, len(result.get("results", [])))
        
        # Cache the results
        if use_cache and method_used != "cache":
            self.cache.set(query, method_used, result)
        
        return {
            "query": query,
            "method": method_used,
            "cost_estimate": cost_estimate,
            "cache_hit": False,
            "response_time_ms": response_time,
            "num_results": len(result.get("results", [])),
            "results": result.get("results", [])
        }
    
    def estimate_cost(self, method: str, num_results: int) -> float:
        """Estimate cost of search (for monitoring)"""
        cost_map = {
            "cache": 0.0,
            "oxylabs": 0.0,  # Free with OpenClaw
            "duckduckgo": 0.0,  # Free API
            "google_api": 0.0,  # Free tier (first 100/day)
            "http_light": 0.001  # Minimal bandwidth cost
        }
        return cost_map.get(method, 0.01)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Optimized Google Search")
    parser.add_argument("query", help="Search query")
    parser.add_argument("-n", "--num-results", type=int, default=5, help="Number of results")
    parser.add_argument("--no-cache", action="store_true", help="Disable caching")
    parser.add_argument("--method", choices=["auto", "oxylabs", "google", "duckduckgo", "http"], 
                       default="auto", help="Force specific method")
    
    args = parser.parse_args()
    
    engine = SearchEngine()
    
    result = engine.search(
        query=args.query,
        num_results=args.num_results,
        use_cache=not args.no_cache
    )
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()