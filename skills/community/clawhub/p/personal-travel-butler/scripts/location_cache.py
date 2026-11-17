#!/usr/bin/env python3
"""Local cache system for offline location access"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta

class LocationCache:
    def __init__(self, cache_dir=None):
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.cache_path = self.get_cache_path()
        
    def get_cache_path(self):
        """Get the path to the local cache file"""
        return self.cache_dir / "location_cache.json" if self.cache_dir else None
        
    def save_to_cache(self, query, results):
        """Save search results to local cache"""
        if not self.cache_path:
            return False
            
        try:
            # Load existing cache or create new one
            if self.cache_path.exists():
                with open(self.cache_path, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
            else:
                cache = {}
                
            # Add new results with timestamp and metadata
            cache[query] = {
                'results': results,
                'timestamp': datetime.now().isoformat(),
                'source': 'api_search',
                'expires_at': (datetime.now() + timedelta(days=30)).isoformat()  # Cache for 30 days
            }
            
            # Save back to file
            with open(self.cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
                
            return True
            
        except Exception as e:
            print(f"⚠️  Cache save failed: {e}")
            return False
            
    def get_from_cache(self, query):
        """Get results from local cache if available and not expired"""
        if not self.cache_path or not self.cache_path.exists():
            return None
            
        try:
            with open(self.cache_path, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                
            if query in cache:
                cached_data = cache[query]
                expires_at = datetime.fromisoformat(cached_data['expires_at'])
                
                # Check if cache is still valid (not expired)
                if datetime.now() < expires_at:
                    return cached_data['results']
                else:
                    # Remove expired cache entry
                    del cache[query]
                    with open(self.cache_path, 'w', encoding='utf-8') as f:
                        json.dump(cache, f, ensure_ascii=False, indent=2)
                    
        except Exception as e:
            print(f"⚠️  Cache read failed: {e}")
            
        return None
        
    def clear_expired_cache(self):
        """Remove expired entries from cache"""
        if not self.cache_path or not self.cache_path.exists():
            return 0
            
        try:
            with open(self.cache_path, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                
            expired_count = 0
            current_time = datetime.now()
            
            for query, data in list(cache.items()):
                expires_at = datetime.fromisoformat(data['expires_at'])
                if current_time >= expires_at:
                    del cache[query]
                    expired_count += 1
                    
            # Save cleaned cache
            with open(self.cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
                
            return expired_count
            
        except Exception as e:
            print(f"⚠️  Cache cleanup failed: {e}")
            return 0

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python location_cache.py status")
        print("  python location_cache.py clear-expired")
        sys.exit(1)
        
    action = sys.argv[1]
    
    if action == "status":
        cache = LocationCache()
        print("📊 Local Cache Status:")
        
    elif action == "clear-expired":
        cache = LocationCache()
        removed = cache.clear_expired_cache()
        print(f"🧹 Removed {removed} expired entries from local cache")

if __name__ == "__main__":
    main()
