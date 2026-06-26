#!/usr/bin/env python3
"""
Minimax Web Search API client.
Performs web searches via MiniMax Token Plan API.

Usage:
    python3 minimax_search.py --api-key KEY --query "search query"

Example:
    python3 minimax_search.py --api-key KEY --query "MiniMax M2.7 release notes"
"""

import argparse
import json
import sys
import urllib.request
import urllib.error


def call_search_api(api_key: str, query: str) -> dict:
    """Call MiniMax Search API."""
    url = "https://api.minimaxi.com/v1/coding_plan/search"
    
    payload = {
        "q": query
    }
    
    data = json.dumps(payload).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'MM-API-Source': 'minimax-coding-plan-mcp'
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ''
        print(f"API Error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Request Error: {e}", file=sys.stderr)
        sys.exit(1)


def format_results(result: dict) -> str:
    """Format search results as readable text."""
    lines = []
    
    base_resp = result.get('base_resp', {})
    if base_resp.get('status_code', 0) != 0:
        return f"API Error: {base_resp.get('status_msg', 'Unknown error')}"
    
    organic = result.get('organic', [])
    if organic:
        lines.append("=== Search Results ===")
        for i, item in enumerate(organic, 1):
            title = item.get('title', 'No title')
            link = item.get('link', '')
            snippet = item.get('snippet', '')
            date = item.get('date', '')
            
            lines.append(f"\n[{i}] {title}")
            if date:
                lines.append(f"    Date: {date}")
            lines.append(f"    Link: {link}")
            if snippet:
                lines.append(f"    {snippet}")
    
    related = result.get('related_searches', [])
    if related:
        lines.append("\n=== Related Searches ===")
        for item in related:
            query = item.get('query', '')
            if query:
                lines.append(f"  - {query}")
    
    return '\n'.join(lines) if lines else "No results found"


def main():
    parser = argparse.ArgumentParser(description='Minimax Web Search')
    parser.add_argument('--api-key', required=True, help='Minimax API key')
    parser.add_argument('--query', required=True, help='Search query')
    
    args = parser.parse_args()
    
    result = call_search_api(args.api_key, args.query)
    print(format_results(result))


if __name__ == '__main__':
    main()
