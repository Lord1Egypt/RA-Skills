#!/usr/bin/env python3
"""
Search OpenClaw documentation using the official docs site.
This script uses web search to find relevant documentation pages.
"""
import sys
import json
import subprocess
import urllib.parse

def search_openclaw_docs(query: str) -> dict:
    """
    Search OpenClaw documentation for the given query.
    
    Args:
        query: Search query string
        
    Returns:
        Dictionary with search results containing titles, URLs, and snippets
    """
    # This would integrate with a proper search API
    # For now, we'll use the web_search tool through the agent
    return {
        "query": query,
        "search_site": "docs.openclaw.ai",
        "message": "Use web_search tool with site:docs.openclaw.ai filter"
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 search_docs.py <query>")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    result = search_openclaw_docs(query)
    print(json.dumps(result, indent=2))