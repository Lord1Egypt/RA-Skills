from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def list_icons(
) -> Dict[str, Any]:
    """
    Get a list of all available Hugeicons icons
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659866627", "list_icons", arguments)

def search_icons(
    query: str
) -> Dict[str, Any]:
    """
    Search for icons by name or tags. Use commas to search for multiple icons (e.g. 'home, notification, settings')
    
    Args:
        query: Search query to find relevant icons. Separate multiple searches with commas
    
    Returns:
        
    """
    arguments = {
        "query": query
    }
    
    return call_api("1777316659866627", "search_icons", arguments)

def get_platform_usage(
    platform: str
) -> Dict[str, Any]:
    """
    Get platform-specific usage instructions for Hugeicons
    
    Args:
        platform: Platform name (react, vue, angular, svelte, react-native, flutter, html)
    
    Returns:
        
    """
    arguments = {
        "platform": platform
    }
    
    return call_api("1777316659866627", "get_platform_usage", arguments)

def get_icon_glyphs(
    icon_name: str
) -> Dict[str, Any]:
    """
    Get all glyphs (unicode characters) for a specific icon across all available styles
    
    Args:
        icon_name: The name of the icon (e.g., 'home-01', 'notification-02')
    
    Returns:
        
    """
    arguments = {
        "icon_name": icon_name
    }
    
    return call_api("1777316659866627", "get_icon_glyphs", arguments)

def get_icon_glyph_by_style(
    icon_name: str,
    style: str
) -> Dict[str, Any]:
    """
    Get the glyph (unicode character) for a specific icon with a particular style
    
    Args:
        icon_name: The name of the icon (e.g., 'home-01', 'notification-02')
        style: The icon style
    
    Returns:
        
    """
    arguments = {
        "icon_name": icon_name,
        "style": style
    }
    
    return call_api("1777316659866627", "get_icon_glyph_by_style", arguments)

