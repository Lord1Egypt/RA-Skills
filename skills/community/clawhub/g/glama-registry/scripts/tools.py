from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def search_mcp_servers(
    query: str
) -> Dict[str, Any]:
    """
    
Search the Glama MCP registry for MCP servers matching the query string.
Args:
    query (str): Search keywords (e.g., 'telegram', 'docker')
Returns:
    list: List of MCP servers (dicts) matching the query

    
    Args:
        query: null
    
    Returns:
        
    """
    arguments = {
        "query": query
    }
    
    return call_api("1777419067003907", "search_mcp_servers", arguments)

