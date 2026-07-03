from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def arxiv_search(
    query: str,
    max_results: Optional[int] = 10.0
) -> Dict[str, Any]:
    """
    Search for papers on arXiv.
    
    Args:
        query: null
        max_results: null
    
    Returns:
        null
    """
    arguments = {
        "query": query,
        "max_results": max_results
    }
    
    return call_api("1777419061413891", "arxiv_search", arguments)

def dblp_search(
    query: str,
    max_results: Optional[int] = 10.0
) -> Dict[str, Any]:
    """
    Search DBLP database for computer science papers.
    
    Args:
        query: null
        max_results: null
    
    Returns:
        null
    """
    arguments = {
        "query": query,
        "max_results": max_results
    }
    
    return call_api("1777419061413891", "dblp_search", arguments)

