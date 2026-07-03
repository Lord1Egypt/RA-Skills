from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def fetch_runbook(
    topic: str
) -> Dict[str, Any]:
    """
    Fetch a specific Kubernetes runbook by topic
    
    Args:
        topic: The runbook topic/slug to fetch
    
    Returns:
        
    """
    arguments = {
        "topic": topic
    }
    
    return call_api("1777419067651075", "fetch_runbook", arguments)

def search_runbooks(
    query: str
) -> Dict[str, Any]:
    """
    Search through Kubernetes runbooks by keyword
    
    Args:
        query: Search query for finding relevant runbooks
    
    Returns:
        
    """
    arguments = {
        "query": query
    }
    
    return call_api("1777419067651075", "search_runbooks", arguments)

def list_topics(
) -> Dict[str, Any]:
    """
    List all available Kubernetes runbook topics
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777419067651075", "list_topics", arguments)

