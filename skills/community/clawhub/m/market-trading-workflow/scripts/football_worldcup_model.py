#!/usr/bin/env python3
"""Data-driven World Cup football model for Polymarket fair prices.

This module builds a transparent national-team strength model from public
competitive-match results (martj42/international_results). It uses:
- competitive matches only (friendlies excluded)
- opponent-strength adjustment via an internal Elo ladder
- recent form over the last 10 competitive matches with recency weights
- goals scored / conceded, adjusted by opponent strength
- optional pre-match research enrichment from FotMob-style match details when
  an event or match id is available (xG, lineups, injuries, suspensions)

It is intentionally lightweight: the goal is to produce a practical fair-price
baseline for Polymarket, not a perfect tournament simulator.
"""

from __future__ import annotations

import csv
import io
import json
import math
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from team_names import (
    TEAM_ALIAS_GROUPS as ALIASES,
    canonical_team as shared_canonical_team,
    normalize_team_text as shared_normalize_team_text,
)

RESULTS_URL = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"
CACHE_PATH = Path.home() / ".cache" / "hermes" / "international_results.csv"
FOTMOB_MATCH_DETAILS_URL = "https://www.fotmob.com/api/data/matchDetails"
FOTMOB_TEAM_FIXTURES_URL = "https://www.fotmob.com/api/data/pageableFixtures"

CONTINENT = {
    "Argentina": "South America",
    "Brazil": "South America",
    "Uruguay": "South America",
    "Colombia": "South America",
    "Chile": "South America",
    "Peru": "South America",
    "Paraguay": "South America",
    "Ecuador": "South America",
    "Bolivia": "South America",
    "Venezuela": "South America",
    "United States": "North America",
    "Canada": "North America",
    "Mexico": "North America",
    "Costa Rica": "North America",
    "Panama": "North America",
    "Jamaica": "North America",
    "Haiti": "North America",
    "Honduras": "North America",
    "El Salvador": "North America",
    "Guatemala": "North America",
    "Nicaragua": "North America",
    "Germany": "Europe",
    "France": "Europe",
    "Spain": "Europe",
    "Portugal": "Europe",
    "England": "Europe",
    "Netherlands": "Europe",
    "Belgium": "Europe",
    "Croatia": "Europe",
    "Italy": "Europe",
    "Austria": "Europe",
    "Switzerland": "Europe",
    "Denmark": "Europe",
    "Poland": "Europe",
    "Scotland": "Europe",
    "Wales": "Europe",
    "Northern Ireland": "Europe",
    "Serbia": "Europe",
    "Slovenia": "Europe",
    "Slovakia": "Europe",
    "Romania": "Europe",
    "Hungary": "Europe",
    "Ukraine": "Europe",
    "Georgia": "Europe",
    "Albania": "Europe",
    "Czechia": "Europe",
    "Türkiye": "Europe",
    "Morocco": "Africa",
    "Senegal": "Africa",
    "Tunisia": "Africa",
    "South Africa": "Africa",
    "Algeria": "Africa",
    "Egypt": "Africa",
    "Nigeria": "Africa",
    "Cameroon": "Africa",
    "Ghana": "Africa",
    "Ivory Coast": "Africa",
    "DR Congo": "Africa",
    "Japan": "Asia",
    "South Korea": "Asia",
    "Qatar": "Asia",
    "Saudi Arabia": "Asia",
    "Australia": "Asia",
    "Iran": "Asia",
    "United Arab Emirates": "Asia",
    "Oman": "Asia",
    "Iraq": "Asia",
    "Uzbekistan": "Asia",
    "Kuwait": "Asia",
    "Jordan": "Asia",
    "China PR": "Asia",
    "Malaysia": "Asia",
    "Thailand": "Asia",
    "Vietnam": "Asia",
    "Indonesia": "Asia",
    "New Zealand": "Oceania",
}

TEAM_MARKET_CONFIG = {
    "win the 2026 fifa world cup": {"kind": "win"},
    "reach the round of 16 at the 2026 fifa world cup": {"kind": "round16"},
    "win their group": {"kind": "group"},
    "qualify for the knockout stage": {"kind": "round16"},
}


@dataclass
class TeamProfile:
    team: str
    elo: float
    attack: float
    defense: float
    form: float
    opp_elo: float
    rating: float = 0.0
    percentile: float = 0.0


@dataclass
class MatchRecord:
    date: datetime
    team: str
    opponent: str
    gf: int
    ga: int
    result: float
    opp_elo: float
    tournament: str

def normalize(text: str) -> str:
    return shared_normalize_team_text(text)


def canonical_team(name: str) -> str:
    return shared_canonical_team(name)

def slugify(text: str) -> str:
    text = normalize(text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def team_continent(team: str) -> str:
    return CONTINENT.get(canonical_team(team), "Other")


def competition_weight(tournament: str) -> float:
    t = tournament.lower()
    if "world cup" in t:
        return 1.6
    if "euro" in t or "copa am" in t or "africa cup" in t or "asian cup" in t or "gold cup" in t:
        return 1.45
    if "nations league" in t or "qualif" in t or "qualification" in t:
        return 1.15
    if "finals" in t or "championship" in t:
        return 1.25
    return 1.0


def goal_multiplier(goal_diff: int) -> float:
    gd = abs(goal_diff)
    return 1.0 + min(gd, 4) * 0.08


def _get_json(url: str, params: Optional[Dict[str, Any]] = None, timeout: int = 30) -> Dict[str, Any]:
    response = requests.get(
        url,
        params=params,
        timeout=timeout,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()
    data = response.json()
    return data if isinstance(data, dict) else {"data": data}


def fetch_fotmob_match_details(match_id: str) -> Dict[str, Any]:
    return _get_json(FOTMOB_MATCH_DETAILS_URL, {"matchId": match_id})


def fetch_fotmob_team_fixtures(team_id: str, cursor: Optional[str] = None) -> Dict[str, Any]:
    params: Dict[str, Any] = {"teamId": team_id}
    if cursor:
        params["cursor"] = cursor
    return _get_json(FOTMOB_TEAM_FIXTURES_URL, params)


def _recursive_find(payload: Any, key_matcher) -> List[Tuple[str, Any]]:
    found: List[Tuple[str, Any]] = []
    stack: List[Tuple[str, Any]] = [("", payload)]
    while stack:
        path, node = stack.pop()
        if isinstance(node, dict):
            for key, value in node.items():
                child_path = f"{path}.{key}" if path else str(key)
                if key_matcher(key, value):
                    found.append((child_path, value))
                stack.append((child_path, value))
        elif isinstance(node, list):
            for idx, value in enumerate(node):
                stack.append((f"{path}[{idx}]", value))
    return found


def _research_summary_from_payload(payload: Any) -> Dict[str, Any]:
    if not payload:
        return {}

    def is_xg(key: str, value: Any) -> bool:
        k = key.lower()
        return "xg" in k or "expectedgoals" in k or "expected_goals" in k

    def is_lineup(key: str, value: Any) -> bool:
        k = key.lower()
        return "lineup" in k or "starting" in k or "starter" in k or "formation" in k

    def is_injury(key: str, value: Any) -> bool:
        k = key.lower()
        return "injur" in k or "suspend" in k or "doubt" in k or "out" == k

    def is_news(key: str, value: Any) -> bool:
        k = key.lower()
        return "news" in k or "availability" in k or "teamnews" in k

    return {
        "xg": _recursive_find(payload, is_xg)[:20],
        "lineups": _recursive_find(payload, is_lineup)[:20],
        "injuries": _recursive_find(payload, is_injury)[:20],
        "news": _recursive_find(payload, is_news)[:20],
    }


def build_research_snapshot(match_id: Optional[str] = None, team_id: Optional[str] = None) -> Dict[str, Any]:
    snapshot: Dict[str, Any] = {"sources": []}
    if match_id:
        try:
            details = fetch_fotmob_match_details(match_id)
            snapshot["sources"].append({"source": "fotmob.matchDetails", "match_id": match_id})
            snapshot["match_details"] = _research_summary_from_payload(details)
        except Exception as exc:
            snapshot["match_details_error"] = str(exc)
    if team_id:
        try:
            fixtures = fetch_fotmob_team_fixtures(team_id)
            snapshot["sources"].append({"source": "fotmob.pageableFixtures", "team_id": team_id})
            snapshot["team_fixtures"] = _research_summary_from_payload(fixtures)
        except Exception as exc:
            snapshot["team_fixtures_error"] = str(exc)
    return snapshot


def market_research_snapshot(market: Dict[str, Any]) -> Dict[str, Any]:
    for key in ("match_id", "matchId", "fotmob_match_id", "event_id", "eventId", "_event_id"):
        value = market.get(key)
        if value:
            return build_research_snapshot(match_id=str(value))
    return {"sources": [], "note": "No match/event id available for FotMob enrichment"}


def fetch_results_csv(force_refresh: bool = False) -> str:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not force_refresh and CACHE_PATH.exists() and CACHE_PATH.stat().st_size > 1000:
        # Reuse the cache only briefly so tournament results flow into the model quickly.
        age_hours = (datetime.utcnow() - datetime.utcfromtimestamp(CACHE_PATH.stat().st_mtime)).total_seconds() / 3600.0
        if age_hours <= 1.0:
            return CACHE_PATH.read_text()
    r = requests.get(RESULTS_URL, timeout=60)
    r.raise_for_status()
    CACHE_PATH.write_text(r.text)
    return r.text


def load_matches(force_refresh: bool = False) -> List[Dict[str, Any]]:
    text = fetch_results_csv(force_refresh=force_refresh)
    reader = csv.DictReader(io.StringIO(text))
    rows: List[Dict[str, Any]] = []
    for row in reader:
        if "friendly" in row["tournament"].lower():
            continue
        rows.append(row)
    rows.sort(key=lambda r: r["date"])
    return rows


def build_team_model(force_refresh: bool = False) -> Tuple[Dict[str, TeamProfile], Dict[str, List[MatchRecord]]]:
    matches = load_matches(force_refresh=force_refresh)
    ratings: Dict[str, float] = defaultdict(lambda: 1500.0)
    histories: Dict[str, List[MatchRecord]] = defaultdict(list)

    for row in matches:
        date = datetime.fromisoformat(row["date"])
        home = canonical_team(row["home_team"])
        away = canonical_team(row["away_team"])
        try:
            hs = int(row["home_score"])
            as_ = int(row["away_score"])
        except Exception:
            continue
        tournament = row["tournament"]

        home_elo = ratings[home]
        away_elo = ratings[away]

        if hs > as_:
            home_res, away_res = 1.0, 0.0
        elif hs < as_:
            home_res, away_res = 0.0, 1.0
        else:
            home_res = away_res = 0.5

        expected_home = 1.0 / (1.0 + 10 ** ((away_elo - home_elo) / 400.0))
        importance = competition_weight(tournament)
        k = 20.0 * importance * goal_multiplier(hs - as_)
        ratings[home] = home_elo + k * (home_res - expected_home)
        ratings[away] = away_elo + k * (away_res - (1.0 - expected_home))

        histories[home].append(MatchRecord(date, home, away, hs, as_, home_res, away_elo, tournament))
        histories[away].append(MatchRecord(date, away, home, as_, hs, away_res, home_elo, tournament))

    profiles, histories = summarize_profiles(ratings, histories)
    return profiles, histories


def summarize_profiles(ratings: Dict[str, float], histories: Dict[str, List[MatchRecord]]) -> Tuple[Dict[str, TeamProfile], Dict[str, List[MatchRecord]]]:
    # Compute raw features for all teams.
    raw: Dict[str, Dict[str, float]] = {}
    for team, hist in histories.items():
        if not hist:
            continue
        last10 = hist[-10:]
        weights = [1.5 if i < 3 else 1.0 if i < 7 else 0.7 for i in range(len(last10))]
        weights = list(reversed(weights))  # most recent has the largest weight
        total_w = sum(weights) or 1.0
        gf = ga = form = opp = 0.0
        for w, rec in zip(weights, last10):
            opp_w = 1.25 if rec.opp_elo >= 1700 else 1.0 if rec.opp_elo >= 1500 else 0.75
            gf += rec.gf * w * opp_w
            ga += rec.ga * w * opp_w
            form += rec.result * 3.0 * w * opp_w
            opp += rec.opp_elo * w
        raw[team] = {
            "elo": ratings[team],
            "attack": gf / total_w,
            "defense": ga / total_w,
            "form": form / (3.0 * total_w),
            "opp_elo": opp / total_w,
        }

    # Normalise across teams to combine different scales.
    keys = ["elo", "attack", "defense", "form", "opp_elo"]
    means = {k: sum(v[k] for v in raw.values()) / max(1, len(raw)) for k in keys}
    stds = {
        k: math.sqrt(sum((v[k] - means[k]) ** 2 for v in raw.values()) / max(1, len(raw))) or 1.0
        for k in keys
    }

    profiles: Dict[str, TeamProfile] = {}
    for team, feat in raw.items():
        z_elo = (feat["elo"] - means["elo"]) / stds["elo"]
        z_attack = (feat["attack"] - means["attack"]) / stds["attack"]
        z_defense = (feat["defense"] - means["defense"]) / stds["defense"]
        z_form = (feat["form"] - means["form"]) / stds["form"]
        z_opp = (feat["opp_elo"] - means["opp_elo"]) / stds["opp_elo"]

        rating = 1500.0 + 95.0 * z_elo + 35.0 * z_attack - 35.0 * z_defense + 45.0 * z_form + 18.0 * z_opp
        profiles[team] = TeamProfile(
            team=team,
            elo=feat["elo"],
            attack=feat["attack"],
            defense=feat["defense"],
            form=feat["form"],
            opp_elo=feat["opp_elo"],
            rating=rating,
        )

    # Percentiles across all teams.
    ordered = sorted(profiles.values(), key=lambda p: p.rating, reverse=True)
    n = max(1, len(ordered) - 1)
    for i, prof in enumerate(ordered):
        prof.percentile = 1.0 - (i / n if n else 0.0)
    return profiles, histories


def tier_from_percentile(p: float) -> str:
    if p >= 0.90:
        return "elite"
    if p >= 0.70:
        return "strong"
    if p >= 0.40:
        return "medium"
    return "default"


def softmax_probabilities(profiles: Dict[str, TeamProfile], teams: Iterable[str], temperature: float = 120.0) -> Dict[str, float]:
    selected = []
    for team in teams:
        if team in profiles:
            selected.append(team)
    if not selected:
        return {}
    max_score = max(profiles[t].rating for t in selected)
    raw = {t: math.exp((profiles[t].rating - max_score) / temperature) for t in selected}
    total = sum(raw.values()) or 1.0
    return {t: v / total for t, v in raw.items()}


def h2h_outcome_probabilities(team_a: str, team_b: str, profiles: Dict[str, TeamProfile]) -> Optional[Dict[str, float]]:
    prof_a = profiles.get(team_a)
    prof_b = profiles.get(team_b)
    if prof_a is None or prof_b is None:
        return None
    diff = prof_a.rating - prof_b.rating
    win_base = 1.0 / (1.0 + math.exp(-diff / 145.0))
    draw = 0.16 + 0.14 * math.exp(-abs(diff) / 180.0)
    draw = max(0.06, min(0.32, draw))
    non_draw = max(0.01, 1.0 - draw)
    win_a = non_draw * win_base
    win_b = max(0.01, non_draw - win_a)
    total = win_a + draw + win_b
    if total <= 0:
        return None
    return {"win_a": win_a / total, "draw": draw / total, "win_b": win_b / total}


def market_fair_yes(market: Dict[str, Any], profiles: Dict[str, TeamProfile]) -> Optional[Dict[str, Any]]:
    question = str(market.get('question', '')).lower()
    event_title = str(market.get('_event_title', '')).lower()
    event_slug = str(market.get('_event_slug', '')).lower()
    text = f"{question} {event_title} {event_slug}".lower()

    # Head-to-head / match winner markets.
    h2h_match = re.search(
        r"^(?:will\s+)?(.+?)\s+(?:beat|defeat|outscore|win against|win over|to beat|to defeat|to win against)\s+(.+?)(?:\?|$)",
        question,
    )
    if not h2h_match:
        h2h_match = re.search(
            r"^(.+?)\s+vs\.?\s+(.+?)(?:\s*[-–—].*|\?|$)",
            event_title or question,
        )
    if h2h_match:
        team_a = canonical_team(h2h_match.group(1).strip())
        team_b = canonical_team(h2h_match.group(2).strip())
        probs = h2h_outcome_probabilities(team_a, team_b, profiles)
        if probs is not None:
            if "draw" in text or "tie" in text:
                return {"fair_yes": probs["draw"], "confidence": "High" if abs(profiles[team_a].rating - profiles[team_b].rating) >= 120 else "Medium"}
            win_match = re.search(r"^(?:will\s+)?(.+?)\s+win(?:\b|\s+on\b|\s+the\b)", question)
            if win_match:
                target = canonical_team(win_match.group(1).strip())
                fair = probs["win_b"] if target == team_b else probs["win_a"]
                confidence = "High" if abs(profiles[team_a].rating - profiles[team_b].rating) >= 120 else "Medium"
                return {"fair_yes": fair, "confidence": confidence}
            if re.search(r"\b(beat|defeat|outscore|win against|win over|to beat|to defeat|to win against)\b", question):
                confidence = "High" if abs(profiles[team_a].rating - profiles[team_b].rating) >= 120 else "Medium"
                return {"fair_yes": probs["win_a"], "confidence": confidence}
            if "winner" in text or "moneyline" in text or "match winner" in text:
                confidence = "High" if abs(profiles[team_a].rating - profiles[team_b].rating) >= 120 else "Medium"
                return {"fair_yes": probs["win_a"], "confidence": confidence}

    if "which continent will win the world cup" in text:
        # Use only the strongest current candidates so the continent split is not
        # diluted by every historical team in the database.
        ordered = sorted(profiles.values(), key=lambda p: p.rating, reverse=True)
        candidate_teams = [p.team for p in ordered[:32]]
        team_probs = softmax_probabilities(profiles, candidate_teams, temperature=80.0)
        cont_sum: Dict[str, float] = defaultdict(float)
        for team, p in team_probs.items():
            cont_sum[team_continent(team)] += p
        for cont in ["north america", "south america", "europe", "africa", "asia", "oceania"]:
            if cont in text:
                val = cont_sum.get(cont.title(), cont_sum.get(cont, 0.0))
                if val <= 0:
                    val = 0.005
                confidence = "High" if cont_sum else "Low"
                return {"fair_yes": max(0.0, min(1.0, val)), "confidence": confidence}
        return {"fair_yes": 0.005, "confidence": "Low"}

    # Tournament futures / outrights.
    future_match = re.search(
        r"^will\s+(.+?)\s+(win\s+(?:the\s+)?(?:\d{4}\s+)?(?:fifa\s+)?(?:world cup|euro(?:pean championship)?|uefa euro|uefa european championship)|reach\s+the\s+round\s+of\s+16\s+at\s+the\s+.+?|win\s+their\s+group|qualify\s+for\s+the\s+knockout\s+stage)\b",
        question,
    )
    if not future_match:
        if "to score" in text or "goalkeeper to score" in text:
            return {"fair_yes": 0.02, "confidence": "Low"}
        return None

    team_name = canonical_team(future_match.group(1).strip())
    market_type = future_match.group(2).strip()
    prof = profiles.get(team_name)
    if prof is None:
        return {"fair_yes": 0.02, "confidence": "Low"}

    tier = tier_from_percentile(prof.percentile)

    # Use data-driven team tiering to convert the football model into market priors.
    if "win" in market_type and ("world cup" in market_type or "euro" in market_type or "european championship" in market_type):
        # Absolute probability: softmax share over all modeled teams.
        team_probs = softmax_probabilities(profiles, profiles.keys(), temperature=125.0)
        fair = team_probs.get(team_name, 0.001)
        return {"fair_yes": fair, "confidence": "High" if tier != "default" else "Medium"}

    if "round of 16" in market_type or "knockout stage" in market_type:
        priors = {"elite": 0.88, "strong": 0.68, "medium": 0.42, "default": 0.22}
        base = priors[tier]
        fair = base * 0.65 + 0.10 * prof.percentile
        return {"fair_yes": max(0.02, min(0.95, fair)), "confidence": "High" if tier != "default" else "Medium"}

    if "win their group" in market_type:
        priors = {"elite": 0.56, "strong": 0.34, "medium": 0.18, "default": 0.08}
        base = priors[tier]
        fair = base * 0.60 + 0.08 * prof.percentile
        return {"fair_yes": max(0.01, min(0.80, fair)), "confidence": "High" if tier != "default" else "Medium"}

    return None


def build_fair_map(markets: Iterable[Dict[str, Any]], profiles: Optional[Dict[str, TeamProfile]] = None, force_refresh: bool = False) -> Dict[str, Dict[str, Any]]:
    if profiles is None:
        profiles, _ = build_team_model(force_refresh=force_refresh)
    out: Dict[str, Dict[str, Any]] = {}
    for market in markets:
        pred = market_fair_yes(market, profiles)
        if not pred:
            continue
        for key in [market.get("slug"), market.get("question"), market.get("_event_slug"), market.get("_event_title")]:
            if key:
                out[normalize(str(key))] = pred
                out[slugify(str(key))] = pred
                break
    return out


def export_debug_summary(path: str, force_refresh: bool = False) -> None:
    profiles, _ = build_team_model(force_refresh=force_refresh)
    payload = [
        {
            "team": p.team,
            "elo": round(p.elo, 2),
            "attack": round(p.attack, 3),
            "defense": round(p.defense, 3),
            "form": round(p.form, 3),
            "opp_elo": round(p.opp_elo, 2),
            "rating": round(p.rating, 2),
            "percentile": round(p.percentile, 4),
        }
        for p in sorted(profiles.values(), key=lambda x: x.rating, reverse=True)
    ]
    Path(path).write_text(json.dumps(payload, indent=2))


if __name__ == "__main__":
    profiles, _ = build_team_model()
    print(json.dumps({"teams": len(profiles), "top": [p.team for p in sorted(profiles.values(), key=lambda x: x.rating, reverse=True)[:10]]}, indent=2))
