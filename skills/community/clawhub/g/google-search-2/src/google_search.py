#!/usr/bin/env python3
"""
Google Web Search Skill for OpenClaw

Search the web using Google Custom Search API.
"""

import requests
import os
from typing import List, Dict, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)


class GoogleSearch:
    """Google Custom Search client."""
    
    def __init__(self, api_key: Optional[str] = None, cx: Optional[str] = None):
        """
        Initialize Google Search client.
        
        Args:
            api_key: Google Custom Search API key. If None, will try to load from .env or environment.
            cx: Custom Search Engine ID. If None, will try to load from .env or environment.
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        self.cx = cx or os.getenv('GOOGLE_CX')
        self.base_url = 'https://www.googleapis.com/customsearch/v1'
        
        if not self.api_key or not self.cx:
            raise ValueError(
                "Google API key and CX are required. "
                "Set GOOGLE_API_KEY and GOOGLE_CX environment variables."
            )
        
    def search(self, query: str, count: int = 10) -> List[Dict]:
        """
        Search the web using Google Custom Search.
        
        Args:
            query: Search query string.
            count: Number of results to return (default: 10, max: 10).
            
        Returns:
            List of search results with title, link, and snippet.
        """
        params = {
            'q': query,
            'key': self.api_key,
            'cx': self.cx,
            'num': min(count, 10)  # API max is 10 per request
        }
        
        response = requests.get(self.base_url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if 'items' not in data:
            return []
        
        results = []
        for item in data['items']:
            results.append({
                'title': item.get('title', 'N/A'),
                'url': item.get('link', 'N/A'),
                'snippet': item.get('snippet', 'N/A'),
                'display_link': item.get('displayLink', 'N/A')
            })
        
        return results


def google_search(query: str, count: int = 10) -> str:
    """
    Search the web using Google Custom Search.
    
    Args:
        query: Search query string.
        count: Number of results to return (default: 10).
        
    Returns:
        Formatted search results as string.
    """
    try:
        searcher = GoogleSearch()
        results = searcher.search(query, count)
        
        if not results:
            return "❌ No results found."
        
        output = []
        output.append(f"🔍 Google Search Results for: {query}\n")
        output.append(f"Found {len(results)} results:\n")
        
        for i, result in enumerate(results, 1):
            title = result.get('title', 'N/A')
            url = result.get('url', 'N/A')
            snippet = result.get('snippet', 'N/A')
            display_link = result.get('display_link', 'N/A')
            
            output.append(f"{i}. **{title}**")
            output.append(f"   Source: {display_link}")
            output.append(f"   URL: {url}")
            output.append(f"   {snippet}\n")
        
        return '\n'.join(output)
    
    except Exception as e:
        return f"❌ Search failed: {str(e)}"


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python google_search.py <query> [count]")
        print("  query: Search query string")
        print("  count: Number of results (default: 10, max: 10)")
        sys.exit(1)
    
    query = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    result = google_search(query, count)
    print(result)
