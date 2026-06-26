#!/usr/bin/env python3
"""
Firecrawl API wrapper for OpenClaw
Scrape, crawl, and search web content with AI-optimized output
"""

import os
import sys
import json
import requests
import time
from typing import Optional, Dict, Any, List

def get_api_key() -> Optional[str]:
    """Get Firecrawl API key from secrets or environment"""
    possible_paths = [
        "workspace/secrets/firecrawl_api_key",
        "secrets/firecrawl_api_key",
        os.path.expanduser("~/.openclaw/workspace/workspace/secrets/firecrawl_api_key")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path) as f:
                return f.read().strip()
    
    return os.getenv("FIRECRAWL_API_KEY")


def scrape_url(
    url: str,
    formats: List[str] = ["markdown"],
    include_tags: Optional[List[str]] = None,
    exclude_tags: Optional[List[str]] = None,
    only_main_content: bool = True,
    wait_for: Optional[int] = None,
    timeout: int = 30000
) -> Dict[str, Any]:
    """
    Scrape a single URL
    
    Args:
        url: URL to scrape
        formats: Output formats - ["markdown"], ["html"], ["markdown", "html"], ["screenshot"]
        include_tags: HTML tags to include (e.g., ["article", "main"])
        exclude_tags: HTML tags to exclude (e.g., ["nav", "footer"])
        only_main_content: Extract only main content (default True)
        wait_for: Milliseconds to wait before scraping
        timeout: Request timeout in milliseconds
    
    Returns:
        dict: Scrape results with markdown, html, screenshot, metadata
    """
    api_key = get_api_key()
    if not api_key:
        return {"error": "Firecrawl API key not found"}
    
    payload = {
        "url": url,
        "formats": formats,
        "onlyMainContent": only_main_content,
        "timeout": timeout
    }
    
    if include_tags:
        payload["includeTags"] = include_tags
    if exclude_tags:
        payload["excludeTags"] = exclude_tags
    if wait_for:
        payload["waitFor"] = wait_for
    
    try:
        response = requests.post(
            "https://api.firecrawl.dev/v1/scrape",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Scrape failed: {str(e)}"}


def crawl_website(
    url: str,
    max_depth: int = 2,
    limit: int = 10,
    formats: List[str] = ["markdown"],
    exclude_paths: Optional[List[str]] = None,
    include_paths: Optional[List[str]] = None,
    ignore_sitemap: bool = False
) -> Dict[str, Any]:
    """
    Crawl an entire website
    
    Args:
        url: Base URL to crawl
        max_depth: Maximum crawl depth (default 2)
        limit: Maximum pages to crawl (default 10)
        formats: Output formats
        exclude_paths: URL patterns to exclude
        include_paths: URL patterns to include
        ignore_sitemap: Ignore sitemap.xml
    
    Returns:
        dict: Crawl job ID and status URL
    """
    api_key = get_api_key()
    if not api_key:
        return {"error": "Firecrawl API key not found"}
    
    payload = {
        "url": url,
        "maxDepth": max_depth,
        "limit": limit,
        "scrapeOptions": {
            "formats": formats
        },
        "ignoreSitemap": ignore_sitemap
    }
    
    if exclude_paths:
        payload["excludePaths"] = exclude_paths
    if include_paths:
        payload["includePaths"] = include_paths
    
    try:
        response = requests.post(
            "https://api.firecrawl.dev/v1/crawl",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Crawl failed: {str(e)}"}


def get_crawl_status(crawl_id: str) -> Dict[str, Any]:
    """Get status of crawl job"""
    api_key = get_api_key()
    if not api_key:
        return {"error": "Firecrawl API key not found"}
    
    try:
        response = requests.get(
            f"https://api.firecrawl.dev/v1/crawl/{crawl_id}",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Status check failed: {str(e)}"}


def search_web(
    query: str,
    limit: int = 5,
    formats: List[str] = ["markdown"]
) -> Dict[str, Any]:
    """
    Search the web and scrape results
    
    Args:
        query: Search query
        limit: Number of results (default 5)
        formats: Output formats for scraped pages
    
    Returns:
        dict: Search results with scraped content
    """
    api_key = get_api_key()
    if not api_key:
        return {"error": "Firecrawl API key not found"}
    
    payload = {
        "query": query,
        "limit": limit,
        "scrapeOptions": {
            "formats": formats
        }
    }
    
    try:
        response = requests.post(
            "https://api.firecrawl.dev/v1/search",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Search failed: {str(e)}"}


def format_scrape_output(data: Dict[str, Any]) -> str:
    """Format scrape output for display"""
    if "error" in data:
        return f"Error: {data['error']}"
    
    if not data.get("success"):
        return f"Scrape failed: {data.get('error', 'Unknown error')}"
    
    result_data = data.get("data", {})
    output = []
    
    # Metadata
    metadata = result_data.get("metadata", {})
    output.append(f"=== {metadata.get('title', 'Untitled')} ===")
    output.append(f"URL: {result_data.get('url', 'N/A')}")
    output.append(f"Status: {metadata.get('statusCode', 'N/A')}")
    output.append(f"Credits used: {data.get('creditsUsed', 0)}")
    output.append("")
    
    # Content
    if "markdown" in result_data:
        output.append("=== Markdown Content ===")
        markdown = result_data["markdown"]
        # Truncate if too long
        if len(markdown) > 2000:
            output.append(markdown[:2000])
            output.append(f"\n... (truncated, {len(markdown)} total chars)")
        else:
            output.append(markdown)
    
    return "\n".join(output)


def format_crawl_output(data: Dict[str, Any]) -> str:
    """Format crawl output for display"""
    if "error" in data:
        return f"Error: {data['error']}"
    
    if not data.get("success"):
        return f"Crawl failed: {data.get('error', 'Unknown error')}"
    
    output = []
    output.append("=== Crawl Job Started ===")
    output.append(f"Job ID: {data.get('id', 'N/A')}")
    output.append(f"Status URL: {data.get('url', 'N/A')}")
    output.append("")
    output.append("Check status with:")
    output.append(f"  python3 scripts/scrape.py --crawl-status {data.get('id', 'N/A')}")
    
    return "\n".join(output)


def format_search_output(data: Dict[str, Any]) -> str:
    """Format search output for display"""
    if "error" in data:
        return f"Error: {data['error']}"
    
    if not data.get("success"):
        return f"Search failed: {data.get('error', 'Unknown error')}"
    
    results = data.get("data", [])
    output = []
    output.append(f"=== Search Results ({len(results)}) ===")
    output.append("")
    
    for i, result in enumerate(results, 1):
        output.append(f"[{i}] {result.get('title', 'Untitled')}")
        output.append(f"    URL: {result.get('url', 'N/A')}")
        
        markdown = result.get("markdown", "")
        if markdown:
            preview = markdown[:200]
            if len(markdown) > 200:
                preview += "..."
            output.append(f"    {preview}")
        
        output.append("")
    
    return "\n".join(output)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Firecrawl Scraper - Web scraping to clean markdown/JSON")
        print("\nUsage:")
        print("  Scrape: scrape.py <url> [--formats markdown,html] [--main-only]")
        print("  Crawl:  scrape.py --crawl <url> [--depth 2] [--limit 10]")
        print("  Search: scrape.py --search <query> [--limit 5]")
        print("  Status: scrape.py --crawl-status <job-id>")
        print("\nExamples:")
        print("  scrape.py https://example.com")
        print("  scrape.py https://docs.site.com --formats markdown")
        print("  scrape.py --crawl https://example.com --depth 3 --limit 20")
        print("  scrape.py --search 'AI agent frameworks' --limit 5")
        print("  scrape.py --crawl-status abc123")
        sys.exit(1)
    
    # Parse arguments
    if sys.argv[1] == "--crawl":
        # Crawl mode
        if len(sys.argv) < 3:
            print("Error: --crawl requires a URL")
            sys.exit(1)
        
        url = sys.argv[2]
        max_depth = 2
        limit = 10
        
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--depth" and i + 1 < len(sys.argv):
                max_depth = int(sys.argv[i + 1])
                i += 2
            elif sys.argv[i] == "--limit" and i + 1 < len(sys.argv):
                limit = int(sys.argv[i + 1])
                i += 2
            else:
                i += 1
        
        result = crawl_website(url, max_depth=max_depth, limit=limit)
        if "--json" in sys.argv:
            print(json.dumps(result, indent=2))
        else:
            print(format_crawl_output(result))
    
    elif sys.argv[1] == "--search":
        # Search mode
        if len(sys.argv) < 3:
            print("Error: --search requires a query")
            sys.exit(1)
        
        query = sys.argv[2]
        limit = 5
        
        if "--limit" in sys.argv:
            idx = sys.argv.index("--limit")
            if idx + 1 < len(sys.argv):
                limit = int(sys.argv[idx + 1])
        
        result = search_web(query, limit=limit)
        if "--json" in sys.argv:
            print(json.dumps(result, indent=2))
        else:
            print(format_search_output(result))
    
    elif sys.argv[1] == "--crawl-status":
        # Status check
        if len(sys.argv) < 3:
            print("Error: --crawl-status requires a job ID")
            sys.exit(1)
        
        job_id = sys.argv[2]
        result = get_crawl_status(job_id)
        print(json.dumps(result, indent=2))
    
    else:
        # Scrape mode
        url = sys.argv[1]
        formats = ["markdown"]
        only_main = True
        
        if "--formats" in sys.argv:
            idx = sys.argv.index("--formats")
            if idx + 1 < len(sys.argv):
                formats = sys.argv[idx + 1].split(",")
        
        if "--full" in sys.argv:
            only_main = False
        
        result = scrape_url(url, formats=formats, only_main_content=only_main)
        
        if "--json" in sys.argv:
            print(json.dumps(result, indent=2))
        else:
            print(format_scrape_output(result))
