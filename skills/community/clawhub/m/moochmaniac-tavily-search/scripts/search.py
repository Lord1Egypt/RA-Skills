#!/usr/bin/env python3
"""
Tavily Search API wrapper for OpenClaw
Performs web searches optimized for AI agent consumption
"""

import os
import sys
import json
import requests
from typing import Optional, Dict, Any

def search_tavily(
    query: str,
    max_results: int = 5,
    search_depth: str = "basic",
    include_answer: bool = False,
    include_images: bool = False,
    include_raw_content: bool = False
) -> Dict[str, Any]:
    """
    Search using Tavily API
    
    Args:
        query: Search query string
        max_results: Number of results (1-10, default 5)
        search_depth: "basic" or "advanced" (default "basic")
        include_answer: Include AI-generated answer (default False)
        include_images: Include relevant images (default False)
        include_raw_content: Include full page content (default False)
    
    Returns:
        dict: Search results with structure:
            - query: The search query
            - results: List of results with url, title, content, score
            - answer: AI-generated answer (if requested)
            - images: List of image URLs (if requested)
    """
    
    # Get API key from secrets or environment
    api_key = None
    # Try multiple possible paths
    possible_paths = [
        "workspace/secrets/tavily_api_key",  # From OpenClaw workspace root
        "secrets/tavily_api_key",  # Relative to current dir
        os.path.expanduser("~/.openclaw/workspace/workspace/secrets/tavily_api_key")
    ]
    
    secrets_path = None
    for path in possible_paths:
        if os.path.exists(path):
            secrets_path = path
            break
    
    if os.path.exists(secrets_path):
        with open(secrets_path) as f:
            api_key = f.read().strip()
    else:
        api_key = os.getenv("TAVILY_API_KEY")
    
    if not api_key:
        return {
            "error": "Tavily API key not found. Store in ~/.openclaw/workspace/secrets/tavily_api_key"
        }
    
    # Build request
    payload = {
        "api_key": api_key,
        "query": query,
        "max_results": max_results,
        "search_depth": search_depth,
        "include_answer": include_answer,
        "include_images": include_images,
        "include_raw_content": include_raw_content
    }
    
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Search failed: {str(e)}"}


def format_results(data: Dict[str, Any]) -> str:
    """Format search results for readable output"""
    
    if "error" in data:
        return f"Error: {data['error']}"
    
    output = []
    output.append(f"Query: {data.get('query', 'N/A')}")
    output.append(f"Response time: {data.get('response_time', 'N/A')}s")
    output.append("")
    
    # AI answer if present
    if data.get("answer"):
        output.append("=== AI Answer ===")
        output.append(data["answer"])
        output.append("")
    
    # Search results
    results = data.get("results", [])
    output.append(f"=== Results ({len(results)}) ===")
    output.append("")
    
    for i, result in enumerate(results, 1):
        output.append(f"[{i}] {result.get('title', 'Untitled')}")
        output.append(f"    URL: {result.get('url', 'N/A')}")
        output.append(f"    Score: {result.get('score', 0):.3f}")
        
        content = result.get('content', '')
        if content:
            # Truncate long content
            if len(content) > 300:
                content = content[:297] + "..."
            output.append(f"    {content}")
        
        output.append("")
    
    # Images if present
    images = data.get("images", [])
    if images:
        output.append(f"=== Images ({len(images)}) ===")
        for img in images:
            output.append(f"  - {img}")
        output.append("")
    
    return "\n".join(output)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: search.py <query> [--max-results N] [--depth basic|advanced] [--answer] [--images]")
        print("\nExamples:")
        print("  search.py 'OpenClaw AI framework'")
        print("  search.py 'latest WordPress news' --max-results 3 --answer")
        print("  search.py 'casino bonuses' --depth advanced --images")
        sys.exit(1)
    
    # Parse arguments
    query = sys.argv[1]
    max_results = 5
    search_depth = "basic"
    include_answer = False
    include_images = False
    
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--max-results" and i + 1 < len(sys.argv):
            max_results = int(sys.argv[i + 1])
            i += 2
        elif arg == "--depth" and i + 1 < len(sys.argv):
            search_depth = sys.argv[i + 1]
            i += 2
        elif arg == "--answer":
            include_answer = True
            i += 1
        elif arg == "--images":
            include_images = True
            i += 1
        elif arg == "--json":
            # Just return raw JSON
            data = search_tavily(query, max_results, search_depth, include_answer, include_images)
            print(json.dumps(data, indent=2))
            sys.exit(0)
        else:
            i += 1
    
    # Perform search
    data = search_tavily(
        query=query,
        max_results=max_results,
        search_depth=search_depth,
        include_answer=include_answer,
        include_images=include_images
    )
    
    # Output formatted results
    print(format_results(data))
