"""Shared team-name normalization and alias helpers for the trading workflow.

Keep this module as the single source of truth for canonical team names so both
research pricing and market discovery normalize labels the same way.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Dict, Iterable, List

# Canonical team names -> known aliases.
TEAM_ALIAS_GROUPS: Dict[str, List[str]] = {
    "United States": ["USA", "US", "U.S.A.", "United States of America"],
    "South Korea": ["Korea Republic", "Korea Rep.", "Republic of Korea", "ROK", "Korea", "Korea (South)", "South Korea (Republic of Korea)"],
    "North Korea": ["Korea DPR", "DPR Korea", "Democratic People's Republic of Korea", "Korea (North)"],
    "Bosnia and Herzegovina": ["Bosnia", "Bosnia-Herzegovina", "Bosnia Herzegovina", "Bosnia & Herzegovina", "BiH", "B&H"],
    "Ivory Coast": ["Côte d'Ivoire", "Côte d Ivoire", "Côte d’Ivoire", "Cote d'Ivoire", "Cote d Ivoire", "Cote d’Ivoire", "Cote dIvoire", "Cote D'Ivoire", "Cote D Ivoire", "Ivory Coast"],
    "DR Congo": ["Democratic Republic of Congo", "Democratic Republic of the Congo", "Congo DR", "Congo, DR", "Congo DR Congo", "DRC", "Congo-Kinshasa"],
    "Republic of the Congo": ["Congo", "Congo Republic", "Congo-Brazzaville", "Republic of Congo"],
    "Cape Verde": ["Cabo Verde", "Republic of Cabo Verde"],
    "Türkiye": ["Turkey", "Turkiye", "Turkiye Republic", "Turkiye Republic of"],
    "Czechia": ["Czech Republic", "Czech Rep.", "Czech Republic (Czechia)"],
    "Russia": ["Russian Federation"],
    "Iran": ["IR Iran", "Islamic Republic of Iran"],
    "Hong Kong": ["Hong Kong, China", "Hong Kong China"],
    "Macau": ["Macao"],
    "United Arab Emirates": ["UAE", "U.A.E.", "Emirates", "United Arab Emirates (UAE)"],
}

# Teams that should be kept as-is in the model and/or reported label sets.
CANONICAL_TEAMS: List[str] = sorted(
    {
        *TEAM_ALIAS_GROUPS.keys(),
        *[alias for aliases in TEAM_ALIAS_GROUPS.values() for alias in aliases],
        # Common teams without alternate spellings still need to remain canonical.
        "Argentina",
        "Australia",
        "Austria",
        "Albania",
        "Algeria",
        "Belgium",
        "Brazil",
        "Cameroon",
        "Canada",
        "Chile",
        "China PR",
        "Colombia",
        "Costa Rica",
        "Croatia",
        "Denmark",
        "Ecuador",
        "Egypt",
        "England",
        "France",
        "Georgia",
        "Germany",
        "Ghana",
        "Hungary",
        "Indonesia",
        "Iraq",
        "Japan",
        "Jordan",
        "Kuwait",
        "Malaysia",
        "Mexico",
        "Morocco",
        "Netherlands",
        "New Zealand",
        "Nigeria",
        "Northern Ireland",
        "Oman",
        "Paraguay",
        "Peru",
        "Poland",
        "Portugal",
        "Qatar",
        "Romania",
        "Saudi Arabia",
        "Scotland",
        "Senegal",
        "Serbia",
        "Slovakia",
        "Slovenia",
        "South Africa",
        "Spain",
        "Switzerland",
        "Thailand",
        "Tunisia",
        "Ukraine",
        "United Kingdom",
        "Uruguay",
        "Uzbekistan",
        "Vietnam",
        "Wales",
    }
)


def normalize_team_text(text: str) -> str:
    text = text.strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[’'\"]", "", text)
    text = re.sub(r"&", " and ", text)
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _build_alias_index() -> Dict[str, str]:
    index: Dict[str, str] = {}
    for canonical, aliases in TEAM_ALIAS_GROUPS.items():
        for candidate in [canonical, *aliases]:
            index.setdefault(normalize_team_text(candidate), canonical)
    return index


TEAM_ALIAS_INDEX = _build_alias_index()


def canonical_team(name: str) -> str:
    normalized = normalize_team_text(name)
    if normalized in TEAM_ALIAS_INDEX:
        return TEAM_ALIAS_INDEX[normalized]

    # Gentle fallback: compare token-normalized forms to catch punctuation/casing
    # variants that are not explicitly listed, but keep this conservative so we
    # do not collapse unrelated teams.
    compact = normalized.replace(" ", "")
    for alias_norm, canonical in TEAM_ALIAS_INDEX.items():
        if compact == alias_norm.replace(" ", ""):
            return canonical

    return " ".join(part.capitalize() for part in normalized.split())


def expand_team_query_aliases(raw_query: str) -> List[str]:
    """Expand a search query with canonical aliases relevant to team names.

    This is intentionally one-way: the original query stays first, and aliases are
    only appended when the query already references a known team label.
    """

    base = raw_query.strip()
    if not base:
        return []

    normalized = normalize_team_text(base)
    expanded = [base]

    for canonical, aliases in TEAM_ALIAS_GROUPS.items():
        candidates = [canonical, *aliases]
        if any(normalize_team_text(candidate) in normalized for candidate in candidates):
            for candidate in candidates:
                if candidate not in expanded:
                    expanded.append(candidate)

    return expanded


def score_team_question_match(question: str, candidate: str) -> int:
    q = normalize_team_text(question)
    c = normalize_team_text(candidate)
    score = 0
    if c == q:
        score += 100
    if c in q:
        score += 50
    if q in c:
        score += 40
    for token in c.split():
        if token and token in q:
            score += 5
    return score
