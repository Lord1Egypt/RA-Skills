#!/usr/bin/env python3
"""
Search integration - Use SearXNG for web search queries.
Integrates with smart-router to augment responses with web data.
"""

import sys
import json
from pathlib import Path
from typing import Iterator, Optional, Dict, List

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / ".." / "searxng" / "scripts"))

try:
    from search import SearXNGClient, load_config as load_searx_config
    SEARXNG_AVAILABLE = True
except ImportError:
    SEARXNG_AVAILABLE = False


def is_search_query(task: str) -> bool:
    """Detect if task requires web search."""
    import re
    
    search_patterns = [
        r'\bsearch\s+(for|the)\b',
        r'\blook\s+up\b',
        r'\bfind\s+(information|news|data|latest)\s+(about|on)\b',
        r'\bcurrent\s+(events|news|prices|weather)\b',
        r'\bwhat\s+is\s+the\s+(latest|current|recent)\b',
        r'\bhow\s+much\s+is\b',
        r'\bweather\s+in\b',
        r'\bwho\s+won\b',
        r'\blatest\s+(news|update|version)\b',
        r'\bstock\s+price\b',
        r'\bwhen\s+did\s+.*\bhappen\b',
    ]
    
    task_lower = task.lower()
    for pattern in search_patterns:
        if re.search(pattern, task_lower):
            return True
    
    return False


def search_and_augment(
    task: str,
    limit: int = 5,
    category: str = "general"
) -> Iterator[str]:
    """
    Search web and return formatted results.
    
    Yields:
        Search results formatted for LLM consumption
    """
    if not SEARXNG_AVAILABLE:
        yield "\n[Search integration not available - SearXNG skill not found]\n"
        return
    
    try:
        # Load SearXNG config
        config_path = Path(__file__).parent.parent / ".." / "searxng" / "config" / "searxng.yaml"
        config = load_searx_config(str(config_path) if config_path.exists() else None)
        
        # Create client
        client = SearXNGClient(
            base_url=config.get("base_url", "https://searx.be"),
            rate_limit=config.get("performance", {}).get("rate_limit", 0.5)
        )
        
        yield f"\n[Searching web for: {task[:50]}...]\n"
        
        # Perform search
        results = client.search(
            query=task,
            category=category,
            limit=limit
        )
        
        search_results = results.get("results", [])
        
        if not search_results:
            yield "[No results found]\n"
            return
        
        # Format results for LLM
        yield f"\n--- WEB SEARCH RESULTS ({len(search_results)} found) ---\n\n"
        
        for i, result in enumerate(search_results, 1):
            title = result.get("title", "No title")
            url = result.get("url", "")
            content = result.get("content", "")[:300]  # Limit content length
            
            yield f"{i}. {title}\n"
            if url:
                yield f"   Source: {url}\n"
            if content:
                yield f"   Summary: {content}...\n"
            yield "\n"
        
        # Add suggestions if any
        suggestions = results.get("suggestions", [])
        if suggestions:
            yield f"--- Related searches: {', '.join(suggestions[:3])} ---\n"
        
        yield "\n--- END SEARCH RESULTS ---\n\n"
        
    except Exception as e:
        yield f"\n[Search failed: {e}]\n"


def get_search_context(task: str, limit: int = 3) -> str:
    """
    Get search results as formatted string for LLM context.
    
    Args:
        task: Search query
        limit: Max results to include
        
    Returns:
        Formatted search results string
    """
    if not SEARXNG_AVAILABLE:
        return ""
    
    try:
        config_path = Path(__file__).parent.parent / ".." / "searxng" / "config" / "searxng.yaml"
        config = load_searx_config(str(config_path) if config_path.exists() else None)
        
        client = SearXNGClient(
            base_url=config.get("base_url", "https://searx.be")
        )
        
        results = client.search(query=task, limit=limit)
        
        search_results = results.get("results", [])
        
        if not search_results:
            return ""
        
        context_parts = ["\n<web_search_context>"]
        context_parts.append(f"Search results for: {task}\n")
        
        for i, result in enumerate(search_results, 1):
            title = result.get("title", "No title")
            content = result.get("content", "")[:200]
            
            context_parts.append(f"[{i}] {title}")
            if content:
                context_parts.append(f"    {content}")
            context_parts.append("")
        
        context_parts.append("</web_search_context>\n")
        
        return "\n".join(context_parts)
        
    except Exception:
        return ""


class SearchAugmentedRouter:
    """
    Router wrapper that adds web search capability.
    
    Automatically detects search queries and augments with web results.
    """
    
    def __init__(self, base_router):
        """
        Initialize with base router.
        
        Args:
            base_router: SmartRouter instance or similar
        """
        self.router = base_router
    
    def route(self, task: str, conversation_id: Optional[str] = None):
        """
        Route task with search augmentation if needed.
        
        Args:
            task: User task/query
            conversation_id: Optional conversation ID
            
        Yields:
            Response chunks (may include search results)
        """
        # Check if search needed
        if is_search_query(task):
            # First yield search results
            yield from search_and_augment(task)
            
            # Then route the task with context
            # Note: In practice, you'd want to inject search results into the prompt
            yield "\n[Now routing to appropriate model...]\n\n"
        
        # Route to appropriate model
        yield from self.router.route(task, conversation_id)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Search Integration Test")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=5, help="Max results")
    args = parser.parse_args()
    
    print(f"Testing search integration...")
    print(f"Query: {args.query}")
    print(f"Needs search: {is_search_query(args.query)}")
    print("-" * 70)
    
    for chunk in search_and_augment(args.query, limit=args.limit):
        print(chunk, end='')
