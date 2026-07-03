from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_player_stats(
    username: str,
    gamemode: Optional[str] = "main"
) -> Dict[str, Any]:
    """
    Retrieve comprehensive statistics for a specific OSRS player including skills, activities, and boss kill counts
    
    Args:
        username: OSRS player username (1-12 characters)
        gamemode: Player game mode
    
    Returns:
        
    """
    arguments = {
        "username": username,
        "gamemode": gamemode
    }
    
    return call_api("1777316659429379", "get_player_stats", arguments)

def get_skill_leaderboard(
    skill: str,
    gamemode: Optional[str] = "main",
    page: Optional[float] = 1.0
) -> Dict[str, Any]:
    """
    Get top players for a specific skill
    
    Args:
        skill: Skill name
        gamemode: Player game mode filter
        page: Page number (25 players per page)
    
    Returns:
        
    """
    arguments = {
        "skill": skill,
        "gamemode": gamemode,
        "page": page
    }
    
    return call_api("1777316659429379", "get_skill_leaderboard", arguments)

def get_activity_leaderboard(
    activity: str,
    gamemode: Optional[str] = "main",
    page: Optional[float] = 1.0
) -> Dict[str, Any]:
    """
    Get top players for activities (bosses, minigames, clues)
    
    Args:
        activity: Activity or boss name
        gamemode: Player game mode filter
        page: Page number (25 players per page)
    
    Returns:
        
    """
    arguments = {
        "activity": activity,
        "gamemode": gamemode,
        "page": page
    }
    
    return call_api("1777316659429379", "get_activity_leaderboard", arguments)

def compare_players(
    usernames: null,
    focus: Optional[str] = "all"
) -> Dict[str, Any]:
    """
    Compare statistics between multiple OSRS players
    
    Args:
        usernames: List of 2-5 player usernames to compare
        focus: Comparison focus area
    
    Returns:
        
    """
    arguments = {
        "usernames": usernames,
        "focus": focus
    }
    
    return call_api("1777316659429379", "compare_players", arguments)

