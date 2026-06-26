#!/usr/bin/env python3
"""Entity validation helpers for verified player output."""

from __future__ import annotations

import re
from typing import Any

from nba_player_names import normalize_player_identity as canonical_player_identity

PLAYER_SEPARATORS = (" (", " |", " -")


def normalize_player_name(value: str | None) -> str:
    text = re.sub(r"\s+", " ", (value or "").strip()).casefold()
    return text


def normalize_player_identity(value: str | None) -> str:
    return canonical_player_identity(value)


def extract_primary_name(text: str | None) -> str:
    value = (text or "").strip()
    for separator in PLAYER_SEPARATORS:
        if separator in value:
            return value.split(separator, 1)[0].strip()
    return value


def roster_names(roster_items: list[dict[str, Any]] | None) -> set[str]:
    names: set[str] = set()
    for item in roster_items or []:
        for display_name in (item.get("displayName"), item.get("shortName")):
            normalized = normalize_player_identity(display_name)
            if normalized:
                names.add(normalized)
    return names


def boxscore_names(game: dict[str, Any]) -> set[str]:
    names: set[str] = set()
    for lines in (game.get("starters") or {}).values():
        for item in lines or []:
            normalized = normalize_player_identity(item)
            if normalized:
                names.add(normalized)
    for lines in (game.get("leaders") or {}).values():
        for item in lines or []:
            normalized = normalize_player_identity(extract_primary_name(item))
            if normalized:
                names.add(normalized)
    for lines in (game.get("keyPlayers") or {}).values():
        for item in lines or []:
            normalized = normalize_player_identity(extract_primary_name(item))
            if normalized:
                names.add(normalized)
    for play in game.get("playTimeline") or []:
        for key in ("playerName", "secondaryPlayerName", "tertiaryPlayerName"):
            normalized = normalize_player_identity(play.get(key))
            if normalized:
                names.add(normalized)
    return names


def _team_id_to_abbr(game: dict[str, Any]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for side in ("away", "home"):
        team = game.get(side) or {}
        team_id = str(team.get("id") or "").strip()
        abbr = str(team.get("abbr") or "").strip()
        if team_id and abbr:
            mapping[team_id] = abbr
    return mapping


def _boxscore_names_by_team(game: dict[str, Any]) -> dict[str, set[str]]:
    results: dict[str, set[str]] = {}
    for side in ("away", "home"):
        abbr = str((game.get(side) or {}).get("abbr") or "").strip()
        if abbr:
            results[abbr] = set()
    for group_name in ("starters", "leaders", "keyPlayers"):
        for abbr, lines in (game.get(group_name) or {}).items():
            team_names = results.setdefault(str(abbr), set())
            for item in lines or []:
                normalized = normalize_player_identity(extract_primary_name(item))
                if normalized:
                    team_names.add(normalized)
    team_map = _team_id_to_abbr(game)
    for play in game.get("playTimeline") or []:
        abbr = team_map.get(str(play.get("teamId") or "").strip())
        if not abbr:
            continue
        normalized = normalize_player_identity(play.get("playerName"))
        if normalized:
            results.setdefault(abbr, set()).add(normalized)
    return results


def verified_player_names_by_team(game: dict[str, Any], rosters_by_abbr: dict[str, list[dict[str, Any]]]) -> dict[str, set[str]]:
    results: dict[str, set[str]] = {}
    authoritative_by_team: dict[str, set[str]] = {}
    for abbr, players in (game.get("boxscorePlayersByTeam") or {}).items():
        names = {
            normalize_player_identity(item.get("displayName") or item.get("playerName") or item.get("name"))
            for item in players or []
            if normalize_player_identity(item.get("displayName") or item.get("playerName") or item.get("name"))
        }
        if names:
            authoritative_by_team[str(abbr)] = names
    for abbr, players in ((game.get("fullStats") or {}).get("players") or {}).items():
        names = authoritative_by_team.setdefault(str(abbr), set())
        for item in players or []:
            normalized = normalize_player_identity(item.get("playerName"))
            if normalized:
                names.add(normalized)
    for abbr, names in (game.get("activeParticipantsByTeam") or {}).items():
        authoritative = authoritative_by_team.setdefault(str(abbr), set())
        for item in names or []:
            normalized = normalize_player_identity(item)
            if normalized:
                authoritative.add(normalized)

    roster_backed_by_team = {
        str(abbr): roster_names(roster)
        for abbr, roster in rosters_by_abbr.items()
    }
    boxscore_fallback = _boxscore_names_by_team(game)

    for abbr in {*(rosters_by_abbr.keys()), *boxscore_fallback.keys(), *authoritative_by_team.keys()}:
        abbr = str(abbr)
        if authoritative_by_team.get(abbr):
            results[abbr] = set(authoritative_by_team[abbr])
        elif roster_backed_by_team.get(abbr):
            results[abbr] = set(roster_backed_by_team[abbr])
        else:
            results[abbr] = set(boxscore_fallback.get(abbr, set()))
    return results


def verified_player_names(game: dict[str, Any], rosters_by_abbr: dict[str, list[dict[str, Any]]]) -> set[str]:
    names_by_team = verified_player_names_by_team(game, rosters_by_abbr)
    names: set[str] = set()
    for team_names in names_by_team.values():
        names.update(team_names)
    return names


def legacy_verified_player_names(game: dict[str, Any], rosters_by_abbr: dict[str, list[dict[str, Any]]]) -> set[str]:
    names: set[str] = set()
    roster_backed_names: set[str] = set()
    for roster in rosters_by_abbr.values():
        roster_backed_names.update(roster_names(roster))
    if roster_backed_names:
        names.update(roster_backed_names)
        for play in game.get("playTimeline") or []:
            for key in ("playerName", "secondaryPlayerName", "tertiaryPlayerName"):
                normalized = normalize_player_identity(play.get(key))
                if normalized:
                    names.add(normalized)
        return names
    names.update(boxscore_names(game))
    return names


def filter_named_lines(lines: list[str], allowed_names: set[str]) -> list[str]:
    if not lines or not allowed_names:
        return lines[:]
    filtered: list[str] = []
    for line in lines:
        primary_name = normalize_player_identity(extract_primary_name(line))
        if primary_name in allowed_names or not primary_name:
            filtered.append(line)
    return filtered


def filter_headlines(headlines: list[str], blocked_names: set[str]) -> list[str]:
    if not blocked_names:
        return headlines[:]
    results: list[str] = []
    blocked = [name for name in blocked_names if name]
    for headline in headlines:
        lowered = normalize_player_name(headline)
        if any(name in lowered for name in blocked):
            continue
        results.append(headline)
    return results


def blocked_names(candidate_lines: list[str], allowed_names: set[str]) -> set[str]:
    blocked: set[str] = set()
    for line in candidate_lines:
        primary = normalize_player_identity(extract_primary_name(line))
        if primary and primary not in allowed_names:
            blocked.add(primary)
    return blocked


def fallback_matchup_text(game: dict[str, Any], *, lang: str) -> str:
    away_abbr = game.get("away", {}).get("abbr") or "AWAY"
    home_abbr = game.get("home", {}).get("abbr") or "HOME"
    if lang == "zh":
        return f"{away_abbr} 后场/锋线轮换 vs {home_abbr} 后场/锋线轮换"
    return f"{away_abbr} backcourt/wing group vs {home_abbr} backcourt/wing group"
