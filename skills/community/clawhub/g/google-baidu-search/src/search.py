#!/usr/bin/env python3
"""
Google & Baidu Web Search Skill for OpenClaw

Smart search engine selection:
- Use Baidu for Chinese content and China-related queries
- Use Google for international and English queries
"""

import requests
import os
import re
from typing import List, Dict, Optional, Literal
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)


def detect_language(query: str) -> str:
    """
    Detect if query is Chinese or English/International.
    
    Args:
        query: Search query string.
        
    Returns:
        'chinese' or 'english'
    """
    # Check for Chinese characters
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')
    if chinese_pattern.search(query):
        return 'chinese'
    
    # Check for common China-related keywords
    china_keywords = ['中国', '北京', '上海', '深圳', '广州', '香港', '台湾', 
                      'china', 'beijing', 'shanghai', 'shenzhen', 'guangzhou', 
                      'hong kong', 'taiwan', '中文', '中文']
    
    query_lower = query.lower()
    for keyword in china_keywords:
        if keyword in query_lower:
            return 'chinese'
    
    return 'english'


def select_engine(query: str, preferred: str = 'auto') -> str:
    """
    Select the best search engine based on query.
    
    Args:
        query: Search query string.
        preferred: Preferred engine ('auto', 'google', 'baidu', 'both').
        
    Returns:
        'google' or 'baidu' or 'both'
    """
    if preferred != 'auto':
        return preferred
    
    # Auto-detect based on language
    lang = detect_language(query)
    
    if lang == 'chinese':
        return 'baidu'
    else:
        return 'google'


class GoogleSearch:
    """Google Custom Search client."""
    
    def __init__(self, api_key: Optional[str] = None, cx: Optional[str] = None):
        """
        Initialize Google Search client.
        
        Args:
            api_key: Google Custom Search API key.
            cx: Custom Search Engine ID.
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
                'display_link': item.get('displayLink', 'N/A'),
                'source': 'Google',
                'engine': 'google'
            })
        
        return results


class BaiduSearch:
    """Baidu Web Search client."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Baidu Search client.
        
        Args:
            api_key: Baidu Search API key.
        """
        self.api_key = api_key or os.getenv('BAIDU_API_KEY')
        self.base_url = 'https://aip.baidubce.com/rest/2.0/search'
        
        if not self.api_key:
            raise ValueError(
                "Baidu API key is required. "
                "Set BAIDU_API_KEY environment variable."
            )
        
    def search(self, query: str, count: int = 10) -> List[Dict]:
        """
        Search the web using Baidu.
        
        Args:
            query: Search query string.
            count: Number of results to return (default: 10).
            
        Returns:
            List of search results with title, url, and snippet.
        """
        # Baidu Search API endpoint
        url = f"{self.base_url}/v1/search"
        
        params = {
            'query': query,
            'count': count,
            'ak': self.api_key
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if 'results' not in data:
            return []
        
        results = []
        for result in data['results']:
            results.append({
                'title': result.get('title', 'N/A'),
                'url': result.get('url', 'N/A'),
                'snippet': result.get('abstract', result.get('snippet', 'N/A')),
                'display_link': '',
                'source': 'Baidu',
                'engine': 'baidu'
            })
        
        return results


class SmartSearch:
    """Smart search client with automatic engine selection."""
    
    def __init__(self):
        """Initialize smart search client."""
        self.google = None
        self.baidu = None
        
        # Try to initialize Google
        try:
            self.google = GoogleSearch()
        except ValueError:
            pass
        
        # Try to initialize Baidu
        try:
            self.baidu = BaiduSearch()
        except ValueError:
            pass
        
        if not self.google and not self.baidu:
            raise ValueError(
                "At least one search engine must be configured. "
                "Set GOOGLE_API_KEY+GOOGLE_CX or BAIDU_API_KEY environment variables."
            )
    
    def search(self, query: str, engine: str = 'auto', count: int = 10) -> List[Dict]:
        """
        Search the web with automatic engine selection.
        
        Args:
            query: Search query string.
            engine: Search engine ('auto', 'google', 'baidu', 'both').
                   'auto' will select based on query language.
            count: Number of results to return.
            
        Returns:
            List of search results.
        """
        # Auto-select engine
        if engine == 'auto':
            selected_engine = select_engine(query)
        else:
            selected_engine = engine
        
        results = []
        
        if selected_engine == 'google' and self.google:
            try:
                google_results = self.google.search(query, count)
                results.extend(google_results)
            except Exception as e:
                print(f"⚠️ Google search failed: {e}")
        
        elif selected_engine == 'baidu' and self.baidu:
            try:
                baidu_results = self.baidu.search(query, count)
                results.extend(baidu_results)
            except Exception as e:
                print(f"⚠️ Baidu search failed: {e}")
        
        elif selected_engine == 'both':
            # Search both engines
            if self.google:
                try:
                    google_results = self.google.search(query, count)
                    results.extend(google_results)
                except Exception as e:
                    print(f"⚠️ Google search failed: {e}")
            
            if self.baidu:
                try:
                    baidu_results = self.baidu.search(query, count)
                    results.extend(baidu_results)
                except Exception as e:
                    print(f"⚠️ Baidu search failed: {e}")
        
        return results
    
    def get_available_engines(self) -> List[str]:
        """Get list of available search engines."""
        engines = []
        if self.google:
            engines.append('google')
        if self.baidu:
            engines.append('baidu')
        return engines


def search_web(query: str, engine: str = 'auto', count: int = 10) -> str:
    """
    Search the web with automatic engine selection.
    
    Args:
        query: Search query string.
        engine: Search engine ('auto', 'google', 'baidu', 'both').
        count: Number of results to return.
        
    Returns:
        Formatted search results as string.
    """
    try:
        searcher = SmartSearch()
        
        # Auto-select engine if needed
        if engine == 'auto':
            selected_engine = select_engine(query)
        else:
            selected_engine = engine
        
        results = searcher.search(query, selected_engine, count)
        
        if not results:
            return "❌ No results found."
        
        output = []
        output.append(f"🔍 Search Results for: {query}\n")
        output.append(f"Engine: {selected_engine.capitalize()} (Auto-selected)\n")
        output.append(f"Available engines: {', '.join(searcher.get_available_engines())}\n")
        output.append(f"Found {len(results)} results:\n")
        
        for i, result in enumerate(results, 1):
            title = result.get('title', 'N/A')
            url = result.get('url', 'N/A')
            snippet = result.get('snippet', 'N/A')
            source = result.get('source', 'N/A')
            
            output.append(f"{i}. **{title}** [{source}]")
            output.append(f"   URL: {url}")
            output.append(f"   {snippet}\n")
        
        return '\n'.join(output)
    
    except Exception as e:
        return f"❌ Search failed: {str(e)}"


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python search.py <query> [engine] [count]")
        print("  query: Search query string")
        print("  engine: auto, google, baidu, or both (default: auto)")
        print("  count: Number of results (default: 10)")
        print("\nExamples:")
        print("  python search.py \"人工智能 2026\"           # Auto-select Baidu")
        print("  python search.py \"AI trends 2026\"          # Auto-select Google")
        print("  python search.py \"AI trends\" google 10     # Force Google")
        print("  python search.py \"人工智能\" baidu 10       # Force Baidu")
        print("  python search.py \"AI\" both 10             # Search both")
        sys.exit(1)
    
    query = sys.argv[1]
    engine = sys.argv[2] if len(sys.argv) > 2 else 'auto'
    count = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    
    result = search_web(query, engine, count)
    print(result)
