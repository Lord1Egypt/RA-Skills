from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_server_info(
) -> Dict[str, Any]:
    """
    Server version + runtime settings (timeouts, retries, cache, concurrency).
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777419070397443", "get_server_info", arguments)

def resolve_team_id(
    query: str,
    limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    Resolve team name/city/nickname → team_id.
    
    Args:
        query: null
        limit: null
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "limit": limit
    }
    
    return call_api("1777419070397443", "resolve_team_id", arguments)

def resolve_player_id(
    query: str,
    active_only: Optional[bool] = None,
    limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    Resolve player name → player_id (official stats endpoint).
    
    Args:
        query: null
        active_only: null
        limit: null
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "active_only": active_only,
        "limit": limit
    }
    
    return call_api("1777419070397443", "resolve_player_id", arguments)

def find_game_id(
    date: Optional[str] = None,
    home_team: Optional[str] = None,
    away_team: Optional[str] = None,
    team: Optional[str] = None,
    lookback_days: Optional[int] = None,
    limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    Find game_id by date and matchup. If date omitted, finds most recent matchup via schedule.
    
    Args:
        date: null
        home_team: null
        away_team: null
        team: null
        lookback_days: null
        limit: null
    
    Returns:
        
    """
    arguments = {
        "date": date,
        "home_team": home_team,
        "away_team": away_team,
        "team": team,
        "lookback_days": lookback_days,
        "limit": limit
    }
    
    return call_api("1777419070397443", "find_game_id", arguments)

def get_todays_scoreboard(
) -> Dict[str, Any]:
    """
    Today's games.
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777419070397443", "get_todays_scoreboard", arguments)

def get_scoreboard_by_date(
    date: str
) -> Dict[str, Any]:
    """
    Games for a specific date.
    
    Args:
        date: null
    
    Returns:
        
    """
    arguments = {
        "date": date
    }
    
    return call_api("1777419070397443", "get_scoreboard_by_date", arguments)

def get_game_details(
    game_id: str
) -> Dict[str, Any]:
    """
    Detailed game info for a specific game_id.
    
    Args:
        game_id: null
    
    Returns:
        
    """
    arguments = {
        "game_id": game_id
    }
    
    return call_api("1777419070397443", "get_game_details", arguments)

def get_box_score(
    game_id: str
) -> Dict[str, Any]:
    """
    Full box score for a game_id.
    
    Args:
        game_id: null
    
    Returns:
        
    """
    arguments = {
        "game_id": game_id
    }
    
    return call_api("1777419070397443", "get_box_score", arguments)

def search_players(
    query: str
) -> Dict[str, Any]:
    """
    Search players by name substring.
    
    Args:
        query: null
    
    Returns:
        
    """
    arguments = {
        "query": query
    }
    
    return call_api("1777419070397443", "search_players", arguments)

def get_player_info(
    player_id: str
) -> Dict[str, Any]:
    """
    Player bio/profile info.
    
    Args:
        player_id: null
    
    Returns:
        
    """
    arguments = {
        "player_id": player_id
    }
    
    return call_api("1777419070397443", "get_player_info", arguments)

def get_player_season_stats(
    player_id: str,
    season: Optional[str] = None
) -> Dict[str, Any]:
    """
    Player stats for a season.
    
    Args:
        player_id: null
        season: null
    
    Returns:
        
    """
    arguments = {
        "player_id": player_id,
        "season": season
    }
    
    return call_api("1777419070397443", "get_player_season_stats", arguments)

def get_player_game_log(
    player_id: str,
    season: Optional[str] = None
) -> Dict[str, Any]:
    """
    Player game log for a season.
    
    Args:
        player_id: null
        season: null
    
    Returns:
        
    """
    arguments = {
        "player_id": player_id,
        "season": season
    }
    
    return call_api("1777419070397443", "get_player_game_log", arguments)

def get_player_career_stats(
    player_id: str
) -> Dict[str, Any]:
    """
    Player career totals/averages.
    
    Args:
        player_id: null
    
    Returns:
        
    """
    arguments = {
        "player_id": player_id
    }
    
    return call_api("1777419070397443", "get_player_career_stats", arguments)

def get_player_hustle_stats(
    player_id: str,
    season: Optional[str] = None
) -> Dict[str, Any]:
    """
    Player hustle stats.
    
    Args:
        player_id: null
        season: null
    
    Returns:
        
    """
    arguments = {
        "player_id": player_id,
        "season": season
    }
    
    return call_api("1777419070397443", "get_player_hustle_stats", arguments)

def get_league_hustle_leaders(
    stat_category: Optional[str] = None,
    season: Optional[str] = None
) -> Dict[str, Any]:
    """
    League leaders in a hustle stat category.
    
    Args:
        stat_category: null
        season: null
    
    Returns:
        
    """
    arguments = {
        "stat_category": stat_category,
        "season": season
    }
    
    return call_api("1777419070397443", "get_league_hustle_leaders", arguments)

def get_player_defense_stats(
    player_id: str,
    season: Optional[str] = None
) -> Dict[str, Any]:
    """
    Opponent FG% when defended by player.
    
    Args:
        player_id: null
        season: null
    
    Returns:
        
    """
    arguments = {
        "player_id": player_id,
        "season": season
    }
    
    return call_api("1777419070397443", "get_player_defense_stats", arguments)

def get_all_time_leaders(
    stat_category: Optional[str] = None,
    limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    All-time leaders for a stat category.
    
    Args:
        stat_category: null
        limit: null
    
    Returns:
        
    """
    arguments = {
        "stat_category": stat_category,
        "limit": limit
    }
    
    return call_api("1777419070397443", "get_all_time_leaders", arguments)

def get_all_teams(
) -> Dict[str, Any]:
    """
    All teams.
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777419070397443", "get_all_teams", arguments)

def get_team_roster(
    team_id: str,
    season: Optional[str] = None
) -> Dict[str, Any]:
    """
    Team roster.
    
    Args:
        team_id: null
        season: null
    
    Returns:
        
    """
    arguments = {
        "team_id": team_id,
        "season": season
    }
    
    return call_api("1777419070397443", "get_team_roster", arguments)

def get_standings(
    season: Optional[str] = None
) -> Dict[str, Any]:
    """
    League standings.
    
    Args:
        season: null
    
    Returns:
        
    """
    arguments = {
        "season": season
    }
    
    return call_api("1777419070397443", "get_standings", arguments)

def get_league_leaders(
    stat_type: Optional[str] = None,
    season: Optional[str] = None,
    limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    Current season per-game league leaders for a stat category (Points/Assists/Rebounds/etc.).
    
    Args:
        stat_type: Stat type like 'Points', 'Assists', 'Rebounds', 'Steals', 'Blocks', 'FG%', '3P%', 'FT%'
        season: Season in format YYYY-YY (defaults to current season)
        limit: Number of leaders to return (default 10, max 50)
    
    Returns:
        
    """
    arguments = {
        "stat_type": stat_type,
        "season": season,
        "limit": limit
    }
    
    return call_api("1777419070397443", "get_league_leaders", arguments)

def get_schedule(
    team_id: str,
    days_ahead: Optional[int] = None
) -> Dict[str, Any]:
    """
    Team upcoming schedule.
    
    Args:
        team_id: null
        days_ahead: null
    
    Returns:
        
    """
    arguments = {
        "team_id": team_id,
        "days_ahead": days_ahead
    }
    
    return call_api("1777419070397443", "get_schedule", arguments)

def get_player_awards(
    player_id: str
) -> Dict[str, Any]:
    """
    Player awards/accolades.
    
    Args:
        player_id: null
    
    Returns:
        
    """
    arguments = {
        "player_id": player_id
    }
    
    return call_api("1777419070397443", "get_player_awards", arguments)

def get_season_awards(
    season: Optional[str] = None
) -> Dict[str, Any]:
    """
    Major awards for a season.
    
    Args:
        season: null
    
    Returns:
        
    """
    arguments = {
        "season": season
    }
    
    return call_api("1777419070397443", "get_season_awards", arguments)

def get_shot_chart(
    player_id: str,
    season: Optional[str] = None,
    game_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Shot chart data summary.
    
    Args:
        player_id: null
        season: null
        game_id: null
    
    Returns:
        
    """
    arguments = {
        "player_id": player_id,
        "season": season,
        "game_id": game_id
    }
    
    return call_api("1777419070397443", "get_shot_chart", arguments)

def get_shooting_splits(
    player_id: str,
    season: Optional[str] = None
) -> Dict[str, Any]:
    """
    Shooting splits summary.
    
    Args:
        player_id: null
        season: null
    
    Returns:
        
    """
    arguments = {
        "player_id": player_id,
        "season": season
    }
    
    return call_api("1777419070397443", "get_shooting_splits", arguments)

def get_play_by_play(
    game_id: str,
    start_period: Optional[int] = None,
    end_period: Optional[int] = None
) -> Dict[str, Any]:
    """
    Play-by-play summary.
    
    Args:
        game_id: null
        start_period: null
        end_period: null
    
    Returns:
        
    """
    arguments = {
        "game_id": game_id,
        "start_period": start_period,
        "end_period": end_period
    }
    
    return call_api("1777419070397443", "get_play_by_play", arguments)

def get_game_rotation(
    game_id: str
) -> Dict[str, Any]:
    """
    Rotation/substitution summary.
    
    Args:
        game_id: null
    
    Returns:
        
    """
    arguments = {
        "game_id": game_id
    }
    
    return call_api("1777419070397443", "get_game_rotation", arguments)

def get_player_advanced_stats(
    player_id: str,
    season: Optional[str] = None
) -> Dict[str, Any]:
    """
    Player advanced metrics summary.
    
    Args:
        player_id: null
        season: null
    
    Returns:
        
    """
    arguments = {
        "player_id": player_id,
        "season": season
    }
    
    return call_api("1777419070397443", "get_player_advanced_stats", arguments)

def get_team_advanced_stats(
    team_id: str,
    season: Optional[str] = None
) -> Dict[str, Any]:
    """
    Team advanced metrics summary.
    
    Args:
        team_id: null
        season: null
    
    Returns:
        
    """
    arguments = {
        "team_id": team_id,
        "season": season
    }
    
    return call_api("1777419070397443", "get_team_advanced_stats", arguments)

