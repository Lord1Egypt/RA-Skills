from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_all_icon_sets(
) -> Dict[str, Any]:
    """
    Browse all available icon collections from Iconify (200+ icon sets with 200,000+ icons). Returns a list of all icon sets with their metadata including name, total icons, author, license, and sample icons.
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659568643", "get_all_icon_sets", arguments)

def get_icon_set(
    prefix: str
) -> Dict[str, Any]:
    """
    Retrieve detailed information about a specific icon set including all available icons in that set. Provide the icon set prefix (e.g., 'mdi', 'fa', 'bi').
    
    Args:
        prefix: The icon set prefix (e.g., 'mdi', 'fa', 'bi', 'tabler')
    
    Returns:
        
    """
    arguments = {
        "prefix": prefix
    }
    
    return call_api("1777316659568643", "get_icon_set", arguments)

def search_icons(
    query: str,
    prefix: Optional[str] = None,
    limit: Optional[float] = None
) -> Dict[str, Any]:
    """
    Search through Iconify's icon collection with flexible query parameters. Returns matching icons from all icon sets or a specific set.
    
    Args:
        query: Search query (e.g., 'home', 'arrow', 'user')
        prefix: Optional: limit search to specific icon set prefix
        limit: Optional: maximum number of results (default: 64, max: 999)
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "prefix": prefix,
        "limit": limit
    }
    
    return call_api("1777316659568643", "search_icons", arguments)

def get_icon_data(
    icon: str
) -> Dict[str, Any]:
    """
    Retrieve specific icon data with usage examples for popular frameworks (React, Vue, Svelte, etc.). Provide the full icon name in format 'prefix:icon-name' (e.g., 'mdi:home', 'fa:user').
    
    Args:
        icon: Full icon name in format 'prefix:icon-name' (e.g., 'mdi:home', 'fa:user', 'bi:heart')
    
    Returns:
        
    """
    arguments = {
        "icon": icon
    }
    
    return call_api("1777316659568643", "get_icon_data", arguments)

