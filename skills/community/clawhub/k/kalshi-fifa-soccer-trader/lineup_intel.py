#!/usr/bin/env python3
"""
Lineup intelligence: formation-aware OVR and injury signal detection.

Reads player data from ratings.json and cross-references against
lineup_cache.json (recent confirmed starters from TheSportsDB).

Exports:
    formation_xi(players, formation)       -> list of selected player dicts
    formation_ovr(team_data, formation)    -> float effective OVR
    injury_signals(team_data, cache_entry) -> list of warning strings
    effective_lineup_ovr(team_name)        -> (float, list[str])  OVR + signals
"""

import json
import unicodedata
from pathlib import Path
from typing import Optional, List, Tuple

ROOT = Path(__file__).parent
RATINGS_PATH = ROOT / "ratings.json"
LINEUP_CACHE_PATH = ROOT / "lineup_cache.json"

# ---------------------------------------------------------------------------
# Position classification
# ---------------------------------------------------------------------------

POS_GROUP = {
    "GK": "GK",
    "CB": "DEF", "LB": "DEF", "RB": "DEF", "LWB": "DEF", "RWB": "DEF", "SW": "DEF",
    "CM": "MID", "CDM": "MID", "CAM": "MID", "LM": "MID", "RM": "MID",
    "ST": "FWD", "CF": "FWD", "LW": "FWD", "RW": "FWD",
    "LS": "FWD", "RS": "FWD", "LF": "FWD", "RF": "FWD",
}

# Slot counts for each formation
FORMATION_SLOTS = {
    "4-3-3":  {"GK": 1, "DEF": 4, "MID": 3, "FWD": 3},
    "4-4-2":  {"GK": 1, "DEF": 4, "MID": 4, "FWD": 2},
    "4-2-3-1":{"GK": 1, "DEF": 4, "MID": 5, "FWD": 1},
    "3-5-2":  {"GK": 1, "DEF": 3, "MID": 5, "FWD": 2},
    "5-3-2":  {"GK": 1, "DEF": 5, "MID": 3, "FWD": 2},
    "5-4-1":  {"GK": 1, "DEF": 5, "MID": 4, "FWD": 1},
}
DEFAULT_FORMATION = "4-3-3"


def _normalize(s: str) -> str:
    """Lowercase + strip accents for fuzzy matching."""
    return "".join(
        c for c in unicodedata.normalize("NFD", s.lower())
        if unicodedata.category(c) != "Mn"
    )


# ---------------------------------------------------------------------------
# Formation XI builder
# ---------------------------------------------------------------------------

def formation_xi(players: list, formation: str = DEFAULT_FORMATION) -> list:
    """
    Pick the best 11 players for a given formation from a squad list.
    Each player dict must have 'ovr' and 'position' keys.
    Returns list of selected player dicts (sorted by OVR desc).
    """
    slots = FORMATION_SLOTS.get(formation, FORMATION_SLOTS[DEFAULT_FORMATION])
    by_group = {"GK": [], "DEF": [], "MID": [], "FWD": [], "UNK": []}

    for p in sorted(players, key=lambda x: x.get("ovr", 0), reverse=True):
        pos = (p.get("position") or "").upper()
        group = POS_GROUP.get(pos, "UNK")
        by_group[group].append(p)

    selected = []
    used_ids = set()

    def pick(group, n):
        count = 0
        for p in by_group[group]:
            pid = id(p)
            if pid not in used_ids and count < n:
                selected.append(p)
                used_ids.add(pid)
                count += 1
        # If we couldn't fill the group, pull from UNK
        if count < n:
            for p in by_group["UNK"]:
                pid = id(p)
                if pid not in used_ids and count < n:
                    selected.append(p)
                    used_ids.add(pid)
                    count += 1

    for group in ("GK", "DEF", "MID", "FWD"):
        pick(group, slots.get(group, 0))

    # If still short (e.g. a squad with few forwards), fill with best remaining
    remaining_needed = 11 - len(selected)
    if remaining_needed > 0:
        all_players = sorted(players, key=lambda x: x.get("ovr", 0), reverse=True)
        for p in all_players:
            if id(p) not in used_ids and remaining_needed > 0:
                selected.append(p)
                remaining_needed -= 1

    return sorted(selected, key=lambda x: x.get("ovr", 0), reverse=True)


def formation_ovr(team_data: dict, formation: str = DEFAULT_FORMATION) -> float:
    """Compute average OVR of the best-fit 11 players for a given formation."""
    players = team_data.get("players", [])
    if not players:
        return team_data.get("top11_avg_ovr") or team_data.get("ovr") or 75.0
    xi = formation_xi(players, formation)
    if not xi:
        return team_data.get("top11_avg_ovr") or team_data.get("ovr") or 75.0
    return round(sum(p["ovr"] for p in xi) / len(xi), 1)


# ---------------------------------------------------------------------------
# Name matching (TheSportsDB full name ↔ ratings.json abbreviated name)
# ---------------------------------------------------------------------------

def _match_player(full_name: str, players: list) -> Optional[dict]:
    """
    Match a full player name (e.g. 'Alexander Isak') to an abbreviated
    player entry (e.g. {'name': 'A. Isak', 'ovr': 86, 'position': 'ST'}).

    Strategy:
    1. Split full_name into [first, *rest]; last = rest[-1] if rest else first
    2. Normalize both; check first_initial + last_name prefix match
    3. Fallback: pure last-name substring match
    """
    norm_full = _normalize(full_name)
    parts = full_name.strip().split()
    if not parts:
        return None

    first_initial = parts[0][0].lower()
    last_name = _normalize(parts[-1]) if len(parts) > 1 else _normalize(parts[0])

    for p in players:
        abbr = p.get("name", "")
        norm_abbr = _normalize(abbr)

        # "A. Isak" → initial="a", rest="isak"
        abbr_parts = norm_abbr.replace("...", "").split(".")
        if len(abbr_parts) >= 2:
            a_initial = abbr_parts[0].strip()
            a_last = abbr_parts[-1].strip().rstrip(".")
        else:
            a_initial = ""
            a_last = abbr_parts[0].strip()

        # Last name prefix match (handles truncated "Gyöker..." → "gyoker")
        last_prefix = a_last[:6] if len(a_last) >= 6 else a_last
        if last_name.startswith(last_prefix) or a_last.startswith(last_name[:6]):
            if not a_initial or a_initial == first_initial:
                return p

    # Fallback: any player whose abbreviated last name appears in the full name
    for p in players:
        abbr = p.get("name", "")
        norm_abbr = _normalize(abbr.replace("...", "").split(".")[-1].strip())
        if len(norm_abbr) >= 4 and norm_abbr in norm_full:
            return p

    return None


# ---------------------------------------------------------------------------
# Injury signals
# ---------------------------------------------------------------------------

def injury_signals(team_data: dict, cache_entry: Optional[dict]) -> List[str]:
    """
    Compare team's top-5 players by OVR against TheSportsDB recent starters.
    Return warning strings for any top players not confirmed in recent lineups.

    cache_entry format:
        { "recent_starters": ["Alexander Isak", ...], "last_event_date": "2026-06-04",
          "last_event": "Sweden 2-2 Greece", "n_events_checked": 3 }
    """
    signals = []
    players = sorted(team_data.get("players", []), key=lambda x: x.get("ovr", 0), reverse=True)
    top_players = players[:5]

    if not cache_entry or not cache_entry.get("recent_starters"):
        signals.append("⚠  No recent lineup data — using static ratings")
        return signals

    recent = cache_entry["recent_starters"]
    last_date = cache_entry.get("last_event_date", "?")
    last_event = cache_entry.get("last_event", "?")
    n_checked = cache_entry.get("n_events_checked", 1)

    # Note staleness if last event was > 90 days ago (rough heuristic)
    try:
        from datetime import date
        event_date = date.fromisoformat(last_date)
        days_ago = (date.today() - event_date).days
        if days_ago > 90:
            signals.append(f"⚠  Most recent data is {days_ago}d old ({last_event})")
    except Exception:
        pass

    for p in top_players:
        matched = _match_player_against_recent(p, recent)
        if not matched:
            signals.append(
                f"❓ {p['name']} (OVR {p['ovr']}) — not confirmed in last {n_checked} lineup(s); possible injury/rest"
            )

    return signals


def _match_player_against_recent(player: dict, recent_starters: List[str]) -> bool:
    """Return True if a ratings.json player appeared in the recent starters list."""
    abbr = player.get("name", "")
    norm_abbr = _normalize(abbr.replace("...", ""))
    abbr_parts = norm_abbr.split(".")
    a_initial = abbr_parts[0].strip() if len(abbr_parts) >= 2 else ""
    a_last = abbr_parts[-1].strip() if abbr_parts else norm_abbr

    for full_name in recent_starters:
        norm_full = _normalize(full_name)
        parts = full_name.strip().split()
        if not parts:
            continue
        f_initial = parts[0][0].lower()
        f_last = _normalize(parts[-1]) if len(parts) > 1 else _normalize(parts[0])

        last_prefix = a_last[:5] if len(a_last) >= 5 else a_last
        if (f_last.startswith(last_prefix) or a_last.startswith(f_last[:5])):
            if not a_initial or a_initial == f_initial:
                return True
    return False


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def effective_lineup_ovr(
    team_name: str,
    formation: str = DEFAULT_FORMATION,
    verbose: bool = False,
) -> Tuple[float, List[str]]:
    """
    Return (effective_ovr, signals) for a team using formation + injury intelligence.

    Falls back gracefully:
        1. Formation-aware OVR from ratings.json players (preferred)
        2. top11_avg_ovr from ratings.json
        3. composite ovr from ratings.json
    """
    signals = []

    # Load ratings
    if not RATINGS_PATH.exists():
        return 75.0, ["⚠  ratings.json not found"]

    with open(RATINGS_PATH) as f:
        data = json.load(f)

    team_data = None
    key = team_name.lower()
    for t in data.get("teams", []):
        if t["name"].lower() == key:
            team_data = t
            break
        for alias in t.get("aliases", []):
            if alias.lower() == key:
                team_data = t
                break
        if team_data:
            break

    if not team_data:
        return 75.0, [f"⚠  {team_name} not found in ratings.json"]

    # Load lineup cache
    cache_entry = None
    if LINEUP_CACHE_PATH.exists():
        with open(LINEUP_CACHE_PATH) as f:
            cache = json.load(f)
        cache_entry = cache.get(team_name.lower())

    # Formation OVR
    players = team_data.get("players", [])
    if players:
        xi = formation_xi(players, formation)
        f_ovr = round(sum(p["ovr"] for p in xi) / len(xi), 1) if xi else None

        # Apply injury adjustment: remove missing top players, sub in next best
        inj_signals = injury_signals(team_data, cache_entry)
        signals.extend(inj_signals)

        # Find top players absent from recent lineups and replace in XI
        if cache_entry and cache_entry.get("recent_starters"):
            xi_adjusted = []
            removed = []
            for p in xi:
                if _match_player_against_recent(p, cache_entry["recent_starters"]):
                    xi_adjusted.append(p)
                else:
                    removed.append(p)

            # Only adjust if we have ≥ 3 confirmed players (otherwise data too sparse)
            if len(xi_adjusted) >= 3 and removed:
                used = {id(p) for p in xi_adjusted}
                for backup in sorted(players, key=lambda x: x.get("ovr", 0), reverse=True):
                    if id(backup) not in used and backup not in xi_adjusted:
                        # Don't add a player who is themselves flagged as absent
                        if _match_player_against_recent(backup, cache_entry["recent_starters"]):
                            xi_adjusted.append(backup)
                            used.add(id(backup))
                            if len(xi_adjusted) == 11:
                                break

                if len(xi_adjusted) >= 8:
                    adj_ovr = round(sum(p["ovr"] for p in xi_adjusted) / len(xi_adjusted), 1)
                    if verbose and abs(adj_ovr - f_ovr) >= 1:
                        signals.append(
                            f"ℹ  Injury adjustment: {f_ovr} → {adj_ovr} "
                            f"(removed {', '.join(p['name'] for p in removed[:3])})"
                        )
                    f_ovr = adj_ovr

        if verbose:
            signals.insert(0, f"ℹ  Formation {formation} XI OVR = {f_ovr}")

        return f_ovr, signals

    # Fallback
    fallback = team_data.get("top11_avg_ovr") or team_data.get("ovr") or 75.0
    signals.append(f"ℹ  No player data — using top11_avg_ovr={fallback}")
    return float(fallback), signals


# ---------------------------------------------------------------------------
# Pretty print helper (used by fetch_lineups.py demo)
# ---------------------------------------------------------------------------

def print_xi(team_name: str, formation: str = DEFAULT_FORMATION) -> None:
    """Print a formatted formation XI for a team."""
    if not RATINGS_PATH.exists():
        print(f"ratings.json not found")
        return

    with open(RATINGS_PATH) as f:
        data = json.load(f)

    team_data = None
    for t in data.get("teams", []):
        if t["name"].lower() == team_name.lower():
            team_data = t
            break
        for alias in t.get("aliases", []):
            if alias.lower() == team_name.lower():
                team_data = t
                break
        if team_data:
            break

    if not team_data:
        print(f"Team '{team_name}' not found")
        return

    players = team_data.get("players", [])
    xi = formation_xi(players, formation)
    f_ovr = round(sum(p["ovr"] for p in xi) / len(xi), 1) if xi else "?"

    print(f"\n{team_data['name']} — {formation} (avg OVR: {f_ovr})")
    print(f"{'Player':<22} {'Pos':<5} {'OVR'}")
    print("-" * 36)
    for p in xi:
        print(f"  {p.get('name','?'):<20} {p.get('position','?'):<5} {p.get('ovr','?')}")
    print(f"  {'AVERAGE':<20}       {f_ovr}")
