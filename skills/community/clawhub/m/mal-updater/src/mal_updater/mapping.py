from __future__ import annotations

import re
import unicodedata
from collections import deque
from dataclasses import dataclass
from difflib import SequenceMatcher
from itertools import combinations
from typing import Any

_AUTO_APPROVAL_BLOCKERS = (
    "season_number_mismatch=",
    "installment_hint_conflict=",
    "episode_evidence_exceeds_candidate_count=",
    "completed_evidence_exceeds_candidate_count=",
)

_RELATION_EXPANSION_MEDIA_TYPES = {"tv", "ova", "ona", "special", "movie"}
_RELATION_EXPANSION_MAX_SEEDS = 2
_RELATION_EXPANSION_MAX_VISITS = 6
_RELATION_EXPANSION_MAX_DEPTH = 2
_RELATION_EXPANSION_FIELDS = (
    "id,title,alternative_titles,media_type,status,num_episodes,start_season,related_anime"
)

from .mal_client import MalApiError, MalClient

_TITLE_CLEANUPS = [
    re.compile(r"\(english dub\)", re.IGNORECASE),
    re.compile(r"\(dub\)", re.IGNORECASE),
    re.compile(r"\benglish dub\b", re.IGNORECASE),
    re.compile(r"\bfrench dub\b", re.IGNORECASE),
    re.compile(r"\bbroadcast version\b", re.IGNORECASE),
    re.compile(r"\buncensored\b", re.IGNORECASE),
    re.compile(r"\bseason\s+\d+\b", re.IGNORECASE),
    re.compile(r"\bpart\s+\d+\b", re.IGNORECASE),
]
_QUERY_CLEANUPS = _TITLE_CLEANUPS[:6]
_NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")
_ALPHA_DIGIT_BOUNDARY_RE = re.compile(r"(?<=[a-z])(?=\d)|(?<=\d)(?=[a-z])")
_SEARCH_SPACING_REWRITES = (
    (re.compile(r"\bseason\s*(\d+)\b", re.IGNORECASE), r"Season \1"),
    (re.compile(r"\bpart\s*(\d+)\b", re.IGNORECASE), r"Part \1"),
    (re.compile(r"\bcour\s*(\d+)\b", re.IGNORECASE), r"Cour \1"),
)
_NON_INSTALLMENT_SUBTITLE_SPLIT_RE = re.compile(r"\s*(?::|\||[–—]|\s-\s|\()\s*")
_AUXILIARY_TITLE_PATTERNS = (
    (re.compile(r"\bpv\b", re.IGNORECASE), "pv"),
    (re.compile(r"\bpromo\b", re.IGNORECASE), "promo"),
    (re.compile(r"\bcommercial\b", re.IGNORECASE), "commercial"),
    (re.compile(r"\bcm\b", re.IGNORECASE), "cm"),
    (re.compile(r"\brecaps?\b", re.IGNORECASE), "recap"),
    (re.compile(r"\bextras?\b", re.IGNORECASE), "extra"),
    (re.compile(r"\bpicture\s+drama\b", re.IGNORECASE), "picture_drama"),
    (re.compile(r"\brelay\s+pvs?\b", re.IGNORECASE), "relay_pv"),
)
_ROMAN_TOKEN_RE = re.compile(r"\b(i|ii|iii|iv|v|vi|vii|viii|ix|x)\b", re.IGNORECASE)
_ORDINAL_SEASON_RE = re.compile(
    r"\b(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\s+season\b",
    re.IGNORECASE,
)
_ORDINAL_COUR_RE = re.compile(
    r"\b(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|\d+(?:st|nd|rd|th))\s+cour\b",
    re.IGNORECASE,
)
_COUR_NUMBER_RE = re.compile(r"\bcour\s*(\d+)\b", re.IGNORECASE)
_FINAL_SEASON_RE = re.compile(r"\b(?:the\s+)?final\s+season\b", re.IGNORECASE)
_PLUS_INSTALLMENT_RE = re.compile(r"[+＋](?:!+)?(?:\s*[)\]]\s*)?$")
_SEASON_RANGE_RE = re.compile(r"\bseasons?\s+\d+\s*[-/]\s*\d+\b", re.IGNORECASE)
_STANDALONE_SEASON_RE = re.compile(r"^season\s+\d+$", re.IGNORECASE)
_STANDALONE_PART_RE = re.compile(r"^part\s+\d+$", re.IGNORECASE)
_STANDALONE_COUR_RE = re.compile(
    r"^(?:cour\s+\d+|(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|\d+(?:st|nd|rd|th))\s+cour)$",
    re.IGNORECASE,
)
_STANDALONE_FINAL_SEASON_RE = re.compile(r"^final\s+season(?:\s+part\s+\d+)?$", re.IGNORECASE)
_INSTALLMENT_ONLY_EXTENSION_RE = re.compile(
    r"^(?:"
    r"season\s*\d+|"
    r"\d+(?:st|nd|rd|th)\s+season|"
    r"(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\s+season|"
    r"part\s*\d+|"
    r"cour\s*\d+|"
    r"(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|\d+(?:st|nd|rd|th))\s+cour|"
    r"final\s+season(?:\s+part\s+\d+)?|"
    r"[ivx]+"
    r")(?:\s+(?:season\s*\d+|part\s*\d+|cour\s*\d+|[ivx]+))*$",
    re.IGNORECASE,
)

_ORDINAL_TO_NUMBER = {
    "first": 1,
    "second": 2,
    "third": 3,
    "fourth": 4,
    "fifth": 5,
    "sixth": 6,
    "seventh": 7,
    "eighth": 8,
    "ninth": 9,
    "tenth": 10,
}

_ROMAN_TO_NUMBER = {
    "i": 1,
    "ii": 2,
    "iii": 3,
    "iv": 4,
    "v": 5,
    "vi": 6,
    "vii": 7,
    "viii": 8,
    "ix": 9,
    "x": 10,
}

_NUMBER_TO_ORDINAL = {
    1: "1st",
    2: "2nd",
    3: "3rd",
    4: "4th",
    5: "5th",
    6: "6th",
    7: "7th",
    8: "8th",
    9: "9th",
    10: "10th",
}

_NUMBER_TO_ROMAN = {
    1: "I",
    2: "II",
    3: "III",
    4: "IV",
    5: "V",
    6: "VI",
    7: "VII",
    8: "VIII",
    9: "IX",
    10: "X",
}

_SUPPLEMENTAL_QUERY_ALIASES = {
    "million arthur": ["Hangyakusei Million Arthur"],
    "the faraway paladin the lord of the rust mountains": ["The Faraway Paladin: The Lord of the Rust Mountains"],
}

_SUPPLEMENTAL_TITLE_CANDIDATE_IDS = {
    "the legendary hero is dead": [51706],
    "monster girl doctor": [40708],
    "girls bravo": [241, 487],
    "magical sempai": [38610],
    "harem in the labyrinth of another world": [44524],
    "scarlet nexus": [48492],
    "kamikatsu working for god in a godless world": [51693],
    "ladies versus butlers": [7148],
    "onmyo kaiten re birth verse": [61150],
    "jujutsu kaisen 0": [48561],
    "the faraway paladin the lord of the rust mountains": [50664],
    "konosuba god s blessing on this wonderful world 3": [49458],
    "is this a zombie of the dead": [10790],
    "i was reincarnated as the 7th prince so i can take my time perfecting my magical ability 2nd season": [59095],
}


@dataclass(slots=True)
class SeriesMappingInput:
    provider: str
    provider_series_id: str
    title: str
    season_title: str | None = None
    season_number: int | None = None
    max_episode_number: int | None = None
    completed_episode_count: int | None = None
    max_completed_episode_number: int | None = None


@dataclass(slots=True)
class MappingCandidate:
    mal_anime_id: int
    title: str
    alternative_titles: list[str]
    media_type: str | None
    status: str | None
    num_episodes: int | None
    score: float
    matched_query: str
    match_reasons: list[str]
    raw: dict[str, Any]


@dataclass(slots=True)
class MappingResult:
    series: SeriesMappingInput
    status: str
    confidence: float
    chosen_candidate: MappingCandidate | None
    candidates: list[MappingCandidate]
    rationale: list[str]
    bundle_companion_candidate: MappingCandidate | None = None
    bundle_companion_candidates: list[MappingCandidate] | None = None



def _normalize_with_cleanup_patterns(value: str | None, cleanup_patterns: list[re.Pattern[str]]) -> str:
    if not value:
        return ""
    normalized = unicodedata.normalize("NFKD", value)
    normalized = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    lowered = normalized.lower().replace("’", "'")
    lowered = _ALPHA_DIGIT_BOUNDARY_RE.sub(" ", lowered)
    for pattern in cleanup_patterns:
        lowered = pattern.sub(" ", lowered)
    lowered = lowered.replace("&", " and ")
    lowered = _NON_ALNUM_RE.sub(" ", lowered)
    lowered = re.sub(r"\b(\d+)\s+(st|nd|rd|th)\b", r"\1\2", lowered)
    return " ".join(lowered.split())


def normalize_title(value: str | None) -> str:
    return _normalize_with_cleanup_patterns(value, _TITLE_CLEANUPS)


def normalize_title_strict(value: str | None) -> str:
    return _normalize_with_cleanup_patterns(value, _QUERY_CLEANUPS)


def _search_query_cleanup(value: str) -> str:
    cleaned = unicodedata.normalize("NFKC", value).replace("’", "'")
    for pattern in _QUERY_CLEANUPS:
        cleaned = pattern.sub(" ", cleaned)
    cleaned = re.sub(r"\(\s*\)", " ", cleaned)
    cleaned = re.sub(r"\s*[-:|–—]\s*(?=$|\()", " ", cleaned)
    for pattern, replacement in _SEARCH_SPACING_REWRITES:
        cleaned = pattern.sub(replacement, cleaned)
    return " ".join(cleaned.split()).strip()


def _season_title_needs_base_title(title: str, season_title: str) -> bool:
    title_norm = normalize_title(title)
    season_norm = _search_query_cleanup(season_title).lower()
    if not season_norm or not title_norm:
        return False
    if title_norm in normalize_title(season_title):
        return False
    return bool(
        _STANDALONE_SEASON_RE.fullmatch(season_norm)
        or _STANDALONE_PART_RE.fullmatch(season_norm)
        or _STANDALONE_COUR_RE.fullmatch(season_norm)
        or _STANDALONE_FINAL_SEASON_RE.fullmatch(season_norm)
    )


def _fallback_queries(query: str) -> list[str]:
    variants: list[str] = []
    for delimiter in (":", "|", " – ", " — ", " - ", "("):
        if delimiter in query:
            shortened = query.split(delimiter, 1)[0].strip()
            if shortened and shortened not in variants:
                variants.append(shortened)
    words = query.split()
    if len(words) > 8:
        shortened = " ".join(words[:8]).strip()
        if shortened and shortened not in variants:
            variants.append(shortened)
    return variants


def _trim_non_installment_subtitle(value: str | None) -> str:
    if not value:
        return ""
    cleaned = _search_query_cleanup(value)
    if not cleaned:
        return ""
    match = _NON_INSTALLMENT_SUBTITLE_SPLIT_RE.search(cleaned)
    if not match:
        return ""
    base = cleaned[: match.start()].strip()
    suffix = cleaned[match.end() :].strip()
    if not base or not suffix:
        return ""
    if _extract_title_hints(suffix):
        return ""
    if any(pattern.search(suffix) for pattern, _ in _AUXILIARY_TITLE_PATTERNS):
        return ""
    if re.search(r"\b(movie|film|ova|ona|special|edition|collection|compilation)\b", suffix, re.IGNORECASE):
        return ""
    if len(normalize_title_strict(base).split()) < 2:
        return ""
    return normalize_title_strict(base)


def _season_number_query_variants(title: str, season_number: int | None) -> list[str]:
    if not title or season_number is None or season_number < 2:
        return []
    variants = [
        f"{title} Season {season_number}",
        f"{title} {_NUMBER_TO_ORDINAL.get(season_number, f'{season_number}th')} Season",
        f"{title} {season_number}",
    ]
    roman = _NUMBER_TO_ROMAN.get(season_number)
    if roman:
        variants.append(f"{title} {roman}")
    return variants


def _season_title_is_installment_only_extension(title: str, season_title: str | None) -> bool:
    if not season_title:
        return False
    title_norm = normalize_title_strict(title)
    season_norm = normalize_title_strict(season_title)
    if not title_norm or not season_norm or not season_norm.startswith(title_norm):
        return False
    suffix = season_norm[len(title_norm):].strip()
    if not suffix:
        return True
    return bool(_INSTALLMENT_ONLY_EXTENSION_RE.fullmatch(suffix))



def build_search_queries(series: SeriesMappingInput) -> list[str]:
    queries: list[str] = []

    def add_query(value: str | None) -> None:
        if not value:
            return
        raw = " ".join(str(value).split()).strip()
        if raw and raw not in queries:
            queries.append(raw)
        cleaned = _search_query_cleanup(raw)
        if cleaned and cleaned not in queries:
            queries.append(cleaned)

    add_query(series.season_title)
    season_title_needs_base = bool(series.season_title and _season_title_needs_base_title(series.title, series.season_title))
    season_title_is_installment_only = _season_title_is_installment_only_extension(series.title, series.season_title)
    if season_title_needs_base:
        add_query(f"{series.title} {series.season_title}")
    should_add_generic_season_variants = (
        not series.season_title
        or season_title_needs_base
        or season_title_is_installment_only
        or normalize_title_strict(series.season_title) == normalize_title_strict(series.title)
    )
    if should_add_generic_season_variants:
        for variant in _season_number_query_variants(series.title, series.season_number):
            add_query(variant)

    alias_keys = {
        normalize_title_strict(series.title),
        normalize_title_strict(series.season_title),
    }
    for key in alias_keys:
        aliases = list(_SUPPLEMENTAL_QUERY_ALIASES.get(key, []))
        if key == "million arthur" and (series.season_number or 0) >= 2:
            aliases = []
        for alias in aliases:
            add_query(alias)

    should_add_base_title = season_title_needs_base or not (
        series.season_title
        and (series.season_number or 0) >= 2
        and not season_title_is_installment_only
        and normalize_title_strict(series.season_title) != normalize_title_strict(series.title)
    )
    if should_add_base_title:
        add_query(series.title)
    return queries or [_search_query_cleanup(series.title)]


def _extract_season_number(value: str | None) -> int | None:
    if not value:
        return None
    if _SEASON_RANGE_RE.search(value):
        return None
    match = re.search(r"\bseason\s*(\d+)\b", value, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def _extract_part_number(value: str | None) -> int | None:
    if not value:
        return None
    match = re.search(r"\bpart\s*(\d+)\b", value, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def _extract_roman_installment_number(value: str | None) -> int | None:
    if not value:
        return None
    for match in _ROMAN_TOKEN_RE.finditer(value):
        token = match.group(1).lower()
        if len(token) == 1:
            continue
        number = _ROMAN_TO_NUMBER.get(token)
        if number is not None and number >= 2:
            return number
    return None


def _extract_ordinal_season_number(value: str | None) -> int | None:
    if not value:
        return None
    match = _ORDINAL_SEASON_RE.search(value)
    if match:
        return _ORDINAL_TO_NUMBER.get(match.group(1).lower())
    numeric_match = re.search(r"\b(\d+)(?:st|nd|rd|th)\s+season\b", value, re.IGNORECASE)
    if numeric_match:
        return int(numeric_match.group(1))
    return None


def _parse_ordinal_token(value: str) -> int | None:
    lowered = value.lower()
    if lowered in _ORDINAL_TO_NUMBER:
        return _ORDINAL_TO_NUMBER[lowered]
    match = re.fullmatch(r"(\d+)(?:st|nd|rd|th)", lowered)
    if match:
        return int(match.group(1))
    return None


def _extract_cour_number(value: str | None) -> int | None:
    if not value:
        return None
    match = _COUR_NUMBER_RE.search(value)
    if match:
        return int(match.group(1))
    match = _ORDINAL_COUR_RE.search(value)
    if not match:
        return None
    return _parse_ordinal_token(match.group(1))


def _extract_terminal_installment_number(value: str | None) -> int | None:
    if not value:
        return None
    cleaned = _search_query_cleanup(value)
    if not cleaned or len(cleaned.split()) < 2:
        return None
    numeric_match = re.search(r"\b(\d+)$", cleaned)
    if numeric_match:
        number = int(numeric_match.group(1))
        if number >= 2:
            return number
        return None
    roman_match = re.search(r"\b([ivx]+)$", cleaned, re.IGNORECASE)
    if roman_match:
        number = _ROMAN_TO_NUMBER.get(roman_match.group(1).lower())
        if number is not None and number >= 2:
            return number
    return None


def _extract_title_hints(value: str | None) -> set[str]:
    hints: set[str] = set()
    if not value:
        return hints
    cleaned = _search_query_cleanup(value)
    season_number = _extract_season_number(cleaned)
    if season_number is not None:
        hints.add(f"season:{season_number}")
    ordinal_season = _extract_ordinal_season_number(cleaned)
    if ordinal_season is not None:
        hints.add(f"season:{ordinal_season}")
    part_number = _extract_part_number(cleaned)
    if part_number is not None:
        hints.add(f"part:{part_number}")
        hints.add(f"split:{part_number}")
    cour_number = _extract_cour_number(cleaned)
    if cour_number is not None:
        hints.add(f"cour:{cour_number}")
        hints.add(f"split:{cour_number}")
    roman_number = _extract_roman_installment_number(cleaned)
    if roman_number is not None:
        hints.add(f"roman:{roman_number}")
    terminal_installment = _extract_terminal_installment_number(cleaned)
    if terminal_installment is not None:
        hints.add(f"season:{terminal_installment}")
    if _FINAL_SEASON_RE.search(cleaned):
        hints.add("final")
    if _PLUS_INSTALLMENT_RE.search(cleaned.strip()):
        hints.add("plus")
    return hints


def _candidate_title_hints(node: dict[str, Any]) -> set[str]:
    hints: set[str] = set()
    for title in _extract_titles_from_node(node):
        hints.update(_extract_title_hints(title))
    return hints


def _title_has_auxiliary_marker(value: str | None) -> str | None:
    if not value:
        return None
    for pattern, label in _AUXILIARY_TITLE_PATTERNS:
        if pattern.search(value):
            return label
    return None


def _candidate_auxiliary_markers(node: dict[str, Any]) -> set[str]:
    markers: set[str] = set()
    for title in _extract_titles_from_node(node):
        marker = _title_has_auxiliary_marker(title)
        if marker:
            markers.add(marker)
    return markers


def _has_non_base_installment_hint(hints: set[str]) -> bool:
    for hint in hints:
        if hint in {"final", "plus"}:
            return True
        if hint.startswith(("season:", "part:", "roman:", "cour:", "split:")):
            try:
                if int(hint.split(":", 1)[1]) > 1:
                    return True
            except ValueError:
                continue
    return False


def _provider_title_hints(series: SeriesMappingInput) -> set[str]:
    hints: set[str] = set()
    for value in (series.season_title, series.title):
        hints.update(_extract_title_hints(value))
    return hints


def _provider_auxiliary_markers(series: SeriesMappingInput) -> set[str]:
    return {
        marker
        for value in (series.season_title, series.title)
        for marker in [_title_has_auxiliary_marker(value)]
        if marker
    }


def _provider_episode_numbering_may_be_aggregated(
    series: SeriesMappingInput,
    provider_hints: set[str],
    candidate_hints: set[str],
    candidate_num_episodes: int,
) -> bool:
    if series.max_episode_number is None or series.max_episode_number <= candidate_num_episodes:
        return False
    if not _has_non_base_installment_hint(provider_hints):
        return False
    if not candidate_hints:
        return False

    completion_aligned = False
    max_completed = series.max_completed_episode_number
    if max_completed is not None and max_completed <= candidate_num_episodes:
        completion_aligned = True
    elif (
        series.completed_episode_count is not None
        and series.completed_episode_count <= candidate_num_episodes
    ):
        completion_aligned = True

    if completion_aligned:
        shared_installment_hints = provider_hints & candidate_hints
        if shared_installment_hints:
            return True

    provider_seasons = {hint for hint in provider_hints if hint.startswith('season:')}
    candidate_split_hints = {hint for hint in candidate_hints if hint.startswith(('part:', 'split:', 'cour:'))}
    split_aligned = False
    for season_hint in provider_seasons:
        suffix = season_hint.split(':', 1)[1]
        if any(hint.endswith(f':{suffix}') for hint in candidate_split_hints):
            split_aligned = True
            break
    if not split_aligned:
        return False
    if series.max_episode_number % candidate_num_episodes != 0:
        return False
    return True


def _provider_episode_evidence_may_have_minor_overflow(
    series: SeriesMappingInput,
    provider_hints: set[str],
    candidate_hints: set[str],
    candidate_num_episodes: int,
) -> bool:
    provider_episode_evidence = series.max_completed_episode_number or series.max_episode_number
    if provider_episode_evidence is None or provider_episode_evidence <= candidate_num_episodes:
        return False
    overflow = provider_episode_evidence - candidate_num_episodes
    if overflow != 1:
        return False
    if series.completed_episode_count is not None and series.completed_episode_count > candidate_num_episodes + 1:
        return False

    shared_installment_hints = provider_hints & candidate_hints
    if any(hint.startswith(("season:", "part:", "split:", "cour:", "roman:")) for hint in shared_installment_hints):
        return True

    provider_seasons = {hint for hint in provider_hints if hint.startswith("season:")}
    for season_hint in provider_seasons:
        suffix = season_hint.split(":", 1)[1]
        if any(hint.endswith(f":{suffix}") for hint in candidate_hints if hint.startswith(("part:", "split:", "cour:"))):
            return True

    if not _has_non_base_installment_hint(provider_hints) and not _has_non_base_installment_hint(candidate_hints):
        return True
    return False


def _candidate_season_numbers(node: dict[str, Any]) -> set[int]:
    numbers: set[int] = set()
    for hint in _candidate_title_hints(node):
        if hint.startswith("season:"):
            numbers.add(int(hint.split(":", 1)[1]))
    return numbers


def _provider_season_number(series: SeriesMappingInput) -> tuple[int | None, str | None]:
    title_season_number = _extract_season_number(series.season_title)
    metadata_season_number = series.season_number
    if title_season_number is not None and metadata_season_number is not None and title_season_number != metadata_season_number:
        return (
            title_season_number,
            f"provider_season_metadata_conflict=metadata:{metadata_season_number};title:{title_season_number}",
        )
    if title_season_number is not None:
        return title_season_number, None
    return metadata_season_number, None


def _extract_titles_from_node(node: dict[str, Any]) -> list[str]:
    titles = [str(node.get("title") or "")]
    alternative_titles = node.get("alternative_titles") or {}
    if isinstance(alternative_titles, dict):
        for key in ("synonyms", "en", "ja"):
            value = alternative_titles.get(key)
            if isinstance(value, list):
                titles.extend(str(item) for item in value if item)
            elif value:
                titles.append(str(value))
    return [title for title in titles if title]


def _score_candidate(series: SeriesMappingInput, query: str, node: dict[str, Any]) -> tuple[float, list[str]]:
    titles = _extract_titles_from_node(node)
    query_norm = normalize_title(query)
    query_strict_norm = normalize_title_strict(query)
    best_ratio = 0.0
    best_title = ""
    for title in titles:
        title_norm = normalize_title(title)
        if not title_norm:
            continue
        ratio = SequenceMatcher(None, query_norm, title_norm).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_title = title
    reasons: list[str] = []
    score = best_ratio
    best_norm = normalize_title(best_title)
    best_strict_norm = normalize_title_strict(best_title)
    extra_title_suffix = bool(
        query_strict_norm and best_strict_norm and best_strict_norm.startswith(f"{query_strict_norm} ")
    )
    if best_strict_norm == query_strict_norm and best_strict_norm:
        score = max(score, 0.995)
        reasons.append("exact_normalized_title")
    elif query_strict_norm and best_strict_norm and (
        query_strict_norm in best_strict_norm or best_strict_norm in query_strict_norm
    ):
        score += 0.03
        reasons.append("substring_title_match")

    trimmed_query_strict_norm = _trim_non_installment_subtitle(query)
    if (
        trimmed_query_strict_norm
        and best_strict_norm
        and trimmed_query_strict_norm == best_strict_norm
        and best_strict_norm != query_strict_norm
    ):
        score = max(score, 0.91)
        reasons.append("exact_base_title_after_subtitle_trim")

    provider_season_number, provider_season_conflict_reason = _provider_season_number(series)
    if provider_season_conflict_reason:
        reasons.append(provider_season_conflict_reason)
    candidate_season_numbers = _candidate_season_numbers(node)
    if provider_season_number is not None and candidate_season_numbers:
        if provider_season_number in candidate_season_numbers:
            score += 0.05
            reasons.append(f"season_number_match={provider_season_number}")
        else:
            score -= 0.08
            reasons.append(
                "season_number_mismatch="
                f"provider:{provider_season_number};candidate:{','.join(str(number) for number in sorted(candidate_season_numbers))}"
            )

    provider_hints = _provider_title_hints(series)
    candidate_hints = _candidate_title_hints(node)
    shared_hints = sorted(provider_hints & candidate_hints)
    conflicting_hints: list[str] = []

    provider_has_non_base_installment_hint = _has_non_base_installment_hint(provider_hints)
    candidate_has_non_base_installment_hint = _has_non_base_installment_hint(candidate_hints)
    if provider_has_non_base_installment_hint and not candidate_hints:
        score -= 0.06
        reasons.append("candidate_missing_installment_hint")
    elif not provider_has_non_base_installment_hint and candidate_has_non_base_installment_hint:
        score -= 0.06
        reasons.append("candidate_extra_installment_hint")

    exact_later_installment_alignment = False

    if provider_has_non_base_installment_hint and not candidate_has_non_base_installment_hint:
        provider_season_number_for_penalty, _ = _provider_season_number(series)
        if provider_season_number_for_penalty is not None and provider_season_number_for_penalty >= 2:
            candidate_season_numbers_for_penalty = _candidate_season_numbers(node)
            if not candidate_season_numbers_for_penalty or candidate_season_numbers_for_penalty == {1}:
                score -= 0.05
                reasons.append("base_installment_penalty_for_explicit_later_season")

    provider_parts = {hint for hint in provider_hints if hint.startswith("part:")}
    candidate_parts = {hint for hint in candidate_hints if hint.startswith("part:")}
    if provider_parts and candidate_parts:
        if provider_parts & candidate_parts:
            reasons.append(f"part_hint_match={','.join(sorted(provider_parts & candidate_parts))}")
            score += 0.04
        else:
            conflicting_hints.extend(sorted(provider_parts | candidate_parts))

    provider_splits = {hint for hint in provider_hints if hint.startswith("split:")}
    candidate_splits = {hint for hint in candidate_hints if hint.startswith("split:")}
    if provider_splits and candidate_splits:
        if provider_splits & candidate_splits:
            reasons.append(f"split_installment_match={','.join(sorted(provider_splits & candidate_splits))}")
            score += 0.12
        else:
            conflicting_hints.extend(sorted(provider_splits | candidate_splits))

    provider_seasons = {hint for hint in provider_hints if hint.startswith("season:")}
    if provider_seasons:
        season_to_split_matches = []
        for season_hint in provider_seasons:
            suffix = season_hint.split(":", 1)[1]
            cross_matches = [hint for hint in candidate_hints if hint.endswith(f":{suffix}") and hint.startswith(("part:", "split:", "cour:"))]
            if cross_matches:
                season_to_split_matches.extend(cross_matches)
        if season_to_split_matches:
            reasons.append(f"season_to_split_match={','.join(sorted(set(season_to_split_matches)))}")
            score += 0.05

    provider_romans = {hint for hint in provider_hints if hint.startswith("roman:")}
    candidate_romans = {hint for hint in candidate_hints if hint.startswith("roman:")}
    if provider_romans and candidate_romans:
        if provider_romans & candidate_romans:
            reasons.append(f"roman_installment_match={','.join(sorted(provider_romans & candidate_romans))}")
            score += 0.04
        else:
            conflicting_hints.extend(sorted(provider_romans | candidate_romans))

    if "final" in provider_hints and candidate_hints:
        if "final" in candidate_hints:
            reasons.append("final_season_hint_match")
            score += 0.04
        elif any(hint.startswith(("season:", "roman:")) for hint in candidate_hints):
            conflicting_hints.append("final")

    non_season_shared_hints = [hint for hint in shared_hints if not hint.startswith("season:")]
    if non_season_shared_hints:
        reasons.append(f"installment_hint_match={','.join(non_season_shared_hints)}")

    if conflicting_hints:
        penalty = 0.08
        if any(hint.startswith(("part:", "cour:", "split:")) for hint in conflicting_hints):
            penalty = 0.16
        score -= penalty
        reasons.append(f"installment_hint_conflict={','.join(conflicting_hints)}")

    if (
        (provider_has_non_base_installment_hint or (provider_season_number or 0) >= 2)
        and "exact_normalized_title" in reasons
        and (
            any(reason.startswith("season_number_match=") for reason in reasons)
            or any(reason.startswith(("part_hint_match=", "split_installment_match=", "season_to_split_match=", "roman_installment_match=")) for reason in reasons)
            or "final_season_hint_match" in reasons
        )
    ):
        score += 0.08
        exact_later_installment_alignment = True
        reasons.append("exact_later_installment_alignment")

    provider_auxiliary_markers = _provider_auxiliary_markers(series)
    candidate_auxiliary_markers = _candidate_auxiliary_markers(node)
    extra_auxiliary_markers = sorted(candidate_auxiliary_markers - provider_auxiliary_markers)
    if extra_auxiliary_markers:
        score -= 0.08
        reasons.append(f"candidate_auxiliary_content={','.join(extra_auxiliary_markers)}")

    if extra_title_suffix and not provider_has_non_base_installment_hint:
        score -= 0.04
        reasons.append("candidate_extra_title_suffix")

    candidate_num_episodes = node.get("num_episodes")
    if isinstance(candidate_num_episodes, int) and candidate_num_episodes > 0:
        provider_episode_evidence = series.max_completed_episode_number or series.max_episode_number
        if provider_episode_evidence is not None and provider_episode_evidence > candidate_num_episodes:
            if _provider_episode_numbering_may_be_aggregated(series, provider_hints, candidate_hints, candidate_num_episodes):
                score -= 0.03
                reasons.append(
                    f"aggregated_episode_numbering_suspected={provider_episode_evidence}>{candidate_num_episodes}"
                )
            elif _provider_episode_evidence_may_have_minor_overflow(series, provider_hints, candidate_hints, candidate_num_episodes):
                score -= 0.03
                reasons.append(
                    f"minor_episode_overflow_suspected={provider_episode_evidence}>{candidate_num_episodes}"
                )
            else:
                score -= 0.12
                reasons.append(
                    f"episode_evidence_exceeds_candidate_count={provider_episode_evidence}>{candidate_num_episodes}"
                )
        elif series.completed_episode_count is not None and series.completed_episode_count > candidate_num_episodes:
            if series.completed_episode_count == candidate_num_episodes + 1 and _provider_episode_evidence_may_have_minor_overflow(
                series,
                provider_hints,
                candidate_hints,
                candidate_num_episodes,
            ):
                score -= 0.03
                reasons.append(
                    f"minor_completed_episode_overflow_suspected={series.completed_episode_count}>{candidate_num_episodes}"
                )
            else:
                score -= 0.12
                reasons.append(
                    f"completed_evidence_exceeds_candidate_count={series.completed_episode_count}>{candidate_num_episodes}"
                )

    media_type = node.get("media_type")
    provider_has_explicit_season_context = any(hint.startswith("season:") for hint in provider_hints)
    candidate_matches_explicit_season_context = bool(
        provider_season_number is not None and provider_season_number in candidate_season_numbers
    ) or bool(
        provider_seasons
        and any(hint.endswith(f":{season_hint.split(':', 1)[1]}") for hint in candidate_hints for season_hint in provider_seasons)
    )
    if (
        provider_has_explicit_season_context
        and media_type in {"ova", "ona", "special", "tv_special", "pv", "movie"}
        and not provider_auxiliary_markers
        and not candidate_matches_explicit_season_context
    ):
        score -= 0.06
        reasons.append(f"{media_type}_penalty_for_explicit_season_context")

    multi_episode_provider_series = max(
        series.completed_episode_count or 0,
        series.max_completed_episode_number or 0,
        series.max_episode_number or 0,
    ) > 1
    if (
        media_type == "special"
        and not provider_auxiliary_markers
        and multi_episode_provider_series
    ):
        score -= 0.10
        reasons.append("special_penalty_for_multi_episode_series")
    elif (
        media_type in {"ova", "ona"}
        and candidate_num_episodes == 1
        and not provider_auxiliary_markers
        and multi_episode_provider_series
    ):
        score -= 0.06
        reasons.append(f"single_episode_{media_type}_penalty_for_multi_episode_series")
    elif (
        media_type in {"movie", "tv_special"}
        and candidate_num_episodes == 1
        and not provider_auxiliary_markers
        and multi_episode_provider_series
    ):
        score -= 0.06
        reasons.append(f"single_episode_{media_type}_penalty_for_multi_episode_series")
    if media_type == "movie":
        if best_strict_norm == query_strict_norm and best_strict_norm:
            reasons.append("movie_type_allowed_for_exact_title")
        else:
            score -= 0.05
            reasons.append("movie_penalty")
    score = max(0.0, min(score, 1.0))
    return score, reasons


def _candidate_positive_signal_count(candidate: MappingCandidate) -> int:
    return sum(
        1
        for reason in candidate.match_reasons
        if reason in {"exact_normalized_title", "exact_base_title_after_subtitle_trim"}
        or reason.startswith(
            (
                "season_number_match=",
                "part_hint_match=",
                "split_installment_match=",
                "season_to_split_match=",
                "roman_installment_match=",
                "installment_hint_match=",
            )
        )
        or reason == "final_season_hint_match"
        or reason == "movie_type_allowed_for_exact_title"
    )


def _candidate_penalty_count(candidate: MappingCandidate) -> int:
    penalty_prefixes = (
        "season_number_mismatch=",
        "installment_hint_conflict=",
        "candidate_missing_installment_hint",
        "candidate_extra_installment_hint",
        "base_installment_penalty_for_explicit_later_season",
        "candidate_auxiliary_content=",
        "episode_evidence_exceeds_candidate_count=",
        "completed_evidence_exceeds_candidate_count=",
    )
    penalty_reasons = sum(1 for reason in candidate.match_reasons if reason.startswith(penalty_prefixes))
    if candidate.media_type in {"special", "tv_special", "pv"}:
        penalty_reasons += 1
    return penalty_reasons


def _candidate_sort_key(candidate: MappingCandidate) -> tuple[float, int, int, int, int, int, int, str, int]:
    return (
        candidate.score,
        int("exact_normalized_title" in candidate.match_reasons),
        _candidate_positive_signal_count(candidate),
        -_candidate_penalty_count(candidate),
        int("candidate_extra_title_suffix" not in candidate.match_reasons),
        int(not re.search(r"\(\d{4}\)\s*$", candidate.title)),
        len(normalize_title_strict(candidate.matched_query)),
        candidate.title.lower(),
        -candidate.mal_anime_id,
    )


def _candidate_is_explainably_weaker(series: SeriesMappingInput, candidate: MappingCandidate) -> bool:
    weaker_prefixes = (
        "season_number_mismatch=",
        "installment_hint_conflict=",
        "candidate_missing_installment_hint",
        "candidate_extra_installment_hint",
        "base_installment_penalty_for_explicit_later_season",
        "candidate_auxiliary_content=",
        "episode_evidence_exceeds_candidate_count=",
        "completed_evidence_exceeds_candidate_count=",
    )
    if any(reason.startswith(weaker_prefixes) for reason in candidate.match_reasons):
        return True
    if candidate.media_type in {"special", "tv_special", "pv"}:
        return True
    if candidate.media_type in {"ova", "ona", "movie"} and candidate.num_episodes == 1 and max(
        series.completed_episode_count or 0,
        series.max_completed_episode_number or 0,
        series.max_episode_number or 0,
    ) > 1:
        return True
    return False



def _candidate_is_non_exact_franchise_extension(candidate: MappingCandidate) -> bool:
    if "exact_normalized_title" in candidate.match_reasons:
        return False
    if "candidate_extra_title_suffix" not in candidate.match_reasons:
        return False
    disqualifying_prefixes = (
        "season_number_match=",
        "part_hint_match=",
        "split_installment_match=",
        "season_to_split_match=",
        "roman_installment_match=",
        "installment_hint_match=",
    )
    if any(reason.startswith(disqualifying_prefixes) for reason in candidate.match_reasons):
        return False
    return True



def _candidate_has_installment_progression_reason(candidate: MappingCandidate) -> bool:
    return any(
        reason.startswith((
            "season_number_match=",
            "season_number_mismatch=",
            "part_hint_match=",
            "split_installment_match=",
            "season_to_split_match=",
            "roman_installment_match=",
            "candidate_extra_installment_hint",
        ))
        for reason in candidate.match_reasons
    ) or "final_season_hint_match" in candidate.match_reasons



def _candidate_has_explicit_followup_installment_hint(candidate: MappingCandidate) -> bool:
    if "final_season_hint_match" in candidate.match_reasons:
        return True
    for title in _extract_titles_from_node(candidate.raw):
        season_number = _extract_season_number(title) or _extract_ordinal_season_number(title)
        if season_number is None:
            ordinal_match = re.search(r"\b(\d+)(?:st|nd|rd|th)\s+season\b", title or "", re.IGNORECASE)
            if ordinal_match:
                season_number = int(ordinal_match.group(1))
        if season_number is not None and season_number >= 2:
            return True
        part_number = _extract_part_number(title)
        if part_number is not None and part_number >= 2:
            return True
        cour_number = _extract_cour_number(title)
        if cour_number is not None and cour_number >= 2:
            return True
        roman_number = _extract_roman_installment_number(title)
        if roman_number is not None and roman_number >= 2:
            return True
        if _FINAL_SEASON_RE.search(title or ""):
            return True
    return any(
        reason.startswith((
            "season_number_match=",
            "season_number_mismatch=",
            "part_hint_match=",
            "split_installment_match=",
            "season_to_split_match=",
            "roman_installment_match=",
            "installment_hint_match=",
            "candidate_extra_installment_hint",
        ))
        for reason in candidate.match_reasons
    )



def _supports_exact_title_overflow_auto_resolution(
    series: SeriesMappingInput,
    top: MappingCandidate,
    candidates: list[MappingCandidate],
    bundle_companion_candidates: list[MappingCandidate] | None = None,
) -> bool:
    if bundle_companion_candidates:
        return False
    if "supplemental_title_candidate" in top.match_reasons:
        return False
    if "exact_normalized_title" not in top.match_reasons:
        return False
    if top.media_type != "tv" or top.score < 0.88:
        return False
    if not any(reason.startswith(("episode_evidence_exceeds_candidate_count=", "completed_evidence_exceeds_candidate_count=")) for reason in top.match_reasons):
        return False
    if not _candidate_has_explicit_followup_installment_hint(top):
        for candidate in candidates[1:6]:
            if candidate.media_type == "tv" and _candidate_has_explicit_followup_installment_hint(candidate) and candidate.score >= 0.30:
                return False
    for candidate in candidates[1:6]:
        if candidate.score < top.score - 0.12:
            continue
        if _candidate_is_explainably_weaker(series, candidate):
            continue
        return False
    return True



def _supports_exact_later_installment_auto_resolution(
    series: SeriesMappingInput,
    top: MappingCandidate,
    second: MappingCandidate | None,
    bundle_companion_candidates: list[MappingCandidate] | None = None,
) -> bool:
    provider_hints = _provider_title_hints(series)
    provider_season_number, _ = _provider_season_number(series)
    if bundle_companion_candidates:
        return False
    if not (_has_non_base_installment_hint(provider_hints) or (provider_season_number or 0) >= 2):
        return False
    if "exact_later_installment_alignment" not in top.match_reasons:
        return False
    if second is None:
        return True
    if _candidate_is_explainably_weaker(series, second) and top.score - second.score >= 0.12:
        return True
    if "exact_base_title_after_subtitle_trim" in second.match_reasons and top.score - second.score >= 0.05:
        return True
    second_query_norm = normalize_title_strict(second.matched_query)
    base_query_norm = normalize_title_strict(series.title)
    if second_query_norm == base_query_norm and "exact_normalized_title" not in second.match_reasons:
        return True
    return False



def _supports_exact_bundle_auto_resolution(
    series: SeriesMappingInput,
    top: MappingCandidate,
    second: MappingCandidate | None,
    bundle_companion_candidates: list[MappingCandidate] | None,
    candidates: list[MappingCandidate],
) -> bool:
    if not bundle_companion_candidates:
        return False
    if "exact_normalized_title" not in top.match_reasons:
        return False
    if top.media_type != "tv" or top.score < 0.88:
        return False
    provider_hints = _provider_title_hints(series)
    provider_season_number, _ = _provider_season_number(series)
    if _has_non_base_installment_hint(provider_hints) or (provider_season_number or 0) >= 2:
        return False

    companion_ids = {candidate.mal_anime_id for candidate in bundle_companion_candidates}
    if not all(_candidate_is_safe_exact_bundle_pair_member(top, candidate) for candidate in bundle_companion_candidates):
        return False

    close_candidate_gap = 0.12
    for candidate in candidates[1:8]:
        if candidate.mal_anime_id in companion_ids:
            continue
        if candidate.score < top.score - close_candidate_gap:
            continue
        if _candidate_is_explainably_weaker(series, candidate):
            continue
        return False

    return True



def _candidate_shares_bundle_title_family(top: MappingCandidate, companion: MappingCandidate) -> bool:
    top_title_norm = normalize_title_strict(top.title)
    companion_title_norm = normalize_title_strict(companion.title)
    if not top_title_norm or not companion_title_norm:
        return False
    if top_title_norm == companion_title_norm:
        return True
    if companion_title_norm.startswith(f"{top_title_norm} ") or top_title_norm.startswith(f"{companion_title_norm} "):
        return True

    shared_prefix_tokens = 0
    for top_token, companion_token in zip(top_title_norm.split(), companion_title_norm.split()):
        if top_token != companion_token:
            break
        shared_prefix_tokens += 1
    return shared_prefix_tokens >= 2



def _is_low_score_bundle_companion(top: MappingCandidate, companion: MappingCandidate) -> bool:
    if not _candidate_shares_bundle_title_family(top, companion):
        return False
    if not any(
        reason.startswith(("candidate_extra_title_suffix", "candidate_extra_installment_hint", "season_number_mismatch="))
        for reason in companion.match_reasons
    ):
        return False
    return companion.score >= 0.35



def _candidate_is_safe_exact_bundle_suffix_companion(top: MappingCandidate, companion: MappingCandidate) -> bool:
    if companion.media_type != "tv":
        return False
    if not _candidate_shares_bundle_title_family(top, companion):
        return False
    if "candidate_extra_title_suffix" not in companion.match_reasons:
        return False
    disqualifying_prefixes = (
        "candidate_auxiliary_content=",
        "installment_hint_conflict=",
        "base_installment_penalty_for_explicit_later_season",
    )
    if any(reason.startswith(disqualifying_prefixes) for reason in companion.match_reasons):
        return False
    return companion.score >= max(0.70, top.score - 0.18)



def _candidate_is_safe_exact_bundle_pair_member(top: MappingCandidate, companion: MappingCandidate) -> bool:
    if companion.media_type != "tv":
        return False
    if not _candidate_shares_bundle_title_family(top, companion):
        return False
    if _candidate_has_explicit_followup_installment_hint(companion):
        return True
    if _candidate_is_safe_exact_bundle_suffix_companion(top, companion):
        return True
    if "exact_normalized_title" in companion.match_reasons and companion.score >= max(0.70, top.score - 0.18):
        return True
    return False



def _suspect_multi_entry_bundle(
    series: SeriesMappingInput,
    top: MappingCandidate,
    candidates: list[MappingCandidate],
) -> tuple[str, list[MappingCandidate]] | None:
    top_is_exact_base_match = "exact_normalized_title" in top.match_reasons
    top_has_installment_alignment = _candidate_has_installment_progression_reason(top)
    if not top_is_exact_base_match and not top_has_installment_alignment:
        return None

    provider_episode_evidence = series.max_completed_episode_number or series.max_episode_number
    if provider_episode_evidence is None or top.num_episodes is None or provider_episode_evidence <= top.num_episodes:
        return None
    if not any(reason.startswith("episode_evidence_exceeds_candidate_count=") for reason in top.match_reasons):
        return None

    plausible_companions: list[MappingCandidate] = []
    for companion in candidates[1:8]:
        if companion.num_episodes is None or companion.num_episodes <= 0:
            continue
        if companion.media_type != top.media_type or companion.media_type != "tv":
            continue
        if not _candidate_shares_bundle_title_family(top, companion):
            continue

        same_franchise_installment = _is_low_score_bundle_companion(top, companion)
        if companion.score < max(0.70, top.score - 0.18) and not same_franchise_installment:
            continue

        if top_is_exact_base_match:
            if not (
                "exact_normalized_title" in companion.match_reasons
                or any(
                    reason.startswith(("candidate_extra_title_suffix", "candidate_extra_installment_hint", "season_number_mismatch="))
                    for reason in companion.match_reasons
                )
            ):
                continue
        elif not _candidate_has_installment_progression_reason(companion):
            continue

        plausible_companions.append(companion)

    best_match: tuple[str, list[MappingCandidate]] | None = None
    best_total_episodes: int | None = None
    for companion_count in (1, 2):
        for companion_group in combinations(plausible_companions, companion_count):
            total_episodes = top.num_episodes + sum(companion.num_episodes or 0 for companion in companion_group)
            if provider_episode_evidence > total_episodes:
                continue
            if best_total_episodes is not None and total_episodes >= best_total_episodes:
                continue
            episode_parts = [str(top.num_episodes)] + [str(companion.num_episodes) for companion in companion_group if companion.num_episodes is not None]
            best_total_episodes = total_episodes
            best_match = (
                "multi_entry_bundle_suspected="
                f"{provider_episode_evidence}<={'+'.join(episode_parts)}",
                list(companion_group),
            )
    return best_match



def _supports_exact_classification(series: SeriesMappingInput, top: MappingCandidate, second: MappingCandidate | None) -> bool:
    provider_episode_evidence = max(
        series.completed_episode_count or 0,
        series.max_completed_episode_number or 0,
        series.max_episode_number or 0,
    )
    top_has_blockers = any(reason.startswith(_AUTO_APPROVAL_BLOCKERS) for reason in top.match_reasons)
    if second is None:
        return top.score >= 0.99 and not top_has_blockers
    if (
        top.media_type == "movie"
        and "exact_normalized_title" in top.match_reasons
        and top.score >= 0.99
        and provider_episode_evidence <= 1
        and second.media_type != "movie"
        and "exact_normalized_title" not in second.match_reasons
    ):
        return True
    if top.score >= 0.99 and top.score - second.score >= 0.05:
        if top_has_blockers:
            return False
        if top.media_type in {"ova", "ona", "special", "tv_special", "pv", "music", "cm"} and second.media_type not in {"ova", "ona", "special", "tv_special", "pv", "music", "cm"}:
            return False
        return True

    reasons = list(top.match_reasons)
    if any(reason.startswith(_AUTO_APPROVAL_BLOCKERS) for reason in reasons):
        return False

    top_query_norm = normalize_title_strict(top.matched_query)
    base_query_norm = normalize_title_strict(series.title)
    second_query_norm = normalize_title_strict(second.matched_query)
    has_specific_installment_context = (series.season_number or 0) >= 2 and top_query_norm != base_query_norm

    if "season_to_split_match=" in " ".join(top.match_reasons):
        if top.score >= 0.95 and _candidate_is_explainably_weaker(series, second):
            return True
        if top.score >= 0.95 and any(reason.startswith('season_number_mismatch=') for reason in second.match_reasons):
            return True
        if (
            top.score >= 0.95
            and top.media_type == second.media_type == "tv"
            and any(reason.startswith('season_number_match=') for reason in second.match_reasons)
            and not any(
                reason.startswith((
                    'season_to_split_match=',
                    'split_installment_match=',
                    'part_hint_match=',
                ))
                for reason in second.match_reasons
            )
        ):
            return True

    if (
        any(reason.startswith('season_number_match=') for reason in top.match_reasons)
        and any(
            reason.startswith((
                'aggregated_episode_numbering_suspected=',
                'minor_episode_overflow_suspected=',
                'minor_completed_episode_overflow_suspected=',
            ))
            for reason in top.match_reasons
        )
        and top.score >= 0.95
        and _candidate_is_explainably_weaker(series, second)
    ):
        return True

    if (
        "exact_normalized_title" in top.match_reasons
        and any(
            reason.startswith((
                'minor_episode_overflow_suspected=',
                'minor_completed_episode_overflow_suspected=',
            ))
            for reason in top.match_reasons
        )
        and top.media_type not in {"ova", "ona", "special", "tv_special", "pv", "music", "cm"}
        and top.score >= 0.95
        and _candidate_is_explainably_weaker(series, second)
    ):
        return True

    if "exact_normalized_title" not in top.match_reasons:
        return False
    if top.score < 0.99:
        return False
    if (
        not has_specific_installment_context
        and _candidate_is_explainably_weaker(series, second)
        and top.media_type not in {"ova", "ona", "special", "tv_special", "pv", "music", "cm"}
    ):
        return True
    if (
        not has_specific_installment_context
        and top.media_type not in {"ova", "ona", "special", "tv_special", "pv", "music", "cm"}
        and second.media_type in {"ova", "ona", "special", "tv_special", "pv", "music", "cm"}
        and "exact_normalized_title" not in second.match_reasons
    ):
        return True
    if (
        not has_specific_installment_context
        and top.media_type not in {"ova", "ona", "special", "tv_special", "pv", "music", "cm"}
        and second.media_type not in {"ova", "ona", "special", "tv_special", "pv", "music", "cm"}
        and _candidate_is_non_exact_franchise_extension(second)
    ):
        return True
    if not has_specific_installment_context:
        return False
    if _candidate_is_explainably_weaker(series, second):
        return True
    if "exact_normalized_title" not in second.match_reasons:
        return True
    if second_query_norm == base_query_norm and top_query_norm != base_query_norm:
        return True
    return False


def should_auto_approve_mapping(result: MappingResult) -> bool:
    if result.status != "exact" or result.chosen_candidate is None:
        return False
    reasons = [*result.rationale, *result.chosen_candidate.match_reasons]
    has_exact_title = "exact_normalized_title" in result.chosen_candidate.match_reasons
    has_split_cour_match = any(reason.startswith("season_to_split_match=") for reason in reasons)
    has_explainable_episode_drift_match = (
        any(reason.startswith("season_number_match=") for reason in reasons)
        and any(
            reason.startswith((
                "aggregated_episode_numbering_suspected=",
                "minor_episode_overflow_suspected=",
                "minor_completed_episode_overflow_suspected=",
            ))
            for reason in reasons
        )
    )
    second_candidate = result.candidates[1] if len(result.candidates) > 1 else None
    has_safe_bundle_resolution = _supports_exact_bundle_auto_resolution(
        result.series,
        result.chosen_candidate,
        second_candidate,
        result.bundle_companion_candidates,
        result.candidates,
    )
    has_safe_later_installment_resolution = _supports_exact_later_installment_auto_resolution(
        result.series,
        result.chosen_candidate,
        second_candidate,
        result.bundle_companion_candidates,
    )
    has_safe_exact_title_overflow_resolution = _supports_exact_title_overflow_auto_resolution(
        result.series,
        result.chosen_candidate,
        result.candidates,
        result.bundle_companion_candidates,
    )
    if not has_exact_title and not has_split_cour_match and not has_explainable_episode_drift_match and not has_safe_bundle_resolution and not has_safe_later_installment_resolution and not has_safe_exact_title_overflow_resolution:
        return False

    provider_season_number, _ = _provider_season_number(result.series)
    candidate_season_numbers = _candidate_season_numbers(result.chosen_candidate.raw)
    if provider_season_number is not None and candidate_season_numbers and candidate_season_numbers != {provider_season_number}:
        return False

    if any(reason.startswith(_AUTO_APPROVAL_BLOCKERS) for reason in reasons) and not (has_safe_bundle_resolution or has_safe_later_installment_resolution or has_safe_exact_title_overflow_resolution):
        return False
    return True


def _should_expand_related_candidates(series: SeriesMappingInput, top: MappingCandidate, second: MappingCandidate | None) -> bool:
    provider_hints = _provider_title_hints(series)
    provider_season_number, _ = _provider_season_number(series)
    has_non_base_installment_context = _has_non_base_installment_hint(provider_hints) or (
        provider_season_number is not None and provider_season_number >= 2
    )

    def _is_auxiliary_or_suffix_residue(candidate: MappingCandidate | None) -> bool:
        if candidate is None:
            return False
        return candidate.media_type in {"ova", "ona", "special", "tv_special", "movie", "pv"} or any(
            reason.startswith("candidate_auxiliary_content=") for reason in candidate.match_reasons
        ) or "candidate_extra_title_suffix" in candidate.match_reasons

    top_has_extra_suffix = "candidate_extra_title_suffix" in top.match_reasons
    top_is_auxiliary_residue = top.media_type in {"ova", "ona", "special", "tv_special", "movie", "pv"} or any(
        reason.startswith("candidate_auxiliary_content=") for reason in top.match_reasons
    )
    top_has_episode_overflow = any(
        reason.startswith(("episode_evidence_exceeds_candidate_count=", "completed_evidence_exceeds_candidate_count="))
        for reason in top.match_reasons
    )
    second_is_close_auxiliary_or_suffix_residue = bool(
        second
        and second.score >= top.score - 0.12
        and _is_auxiliary_or_suffix_residue(second)
    )

    if second_is_close_auxiliary_or_suffix_residue:
        return True
    if not has_non_base_installment_context and not top_has_extra_suffix and not top_is_auxiliary_residue:
        return False
    if top_is_auxiliary_residue:
        return True
    if top_has_extra_suffix and top.score < 0.90:
        return True
    if not has_non_base_installment_context:
        return False
    if second and top.score < 0.90:
        return True
    if top_has_episode_overflow:
        return True
    return False


def _relation_expansion_seed_key(candidate: MappingCandidate) -> tuple[int, float, int, str]:
    return (
        int(
            candidate.media_type in {"ova", "ona", "special", "tv_special", "movie", "pv"}
            or "candidate_extra_title_suffix" in candidate.match_reasons
            or any(reason.startswith("candidate_auxiliary_content=") for reason in candidate.match_reasons)
        ),
        candidate.score,
        _candidate_positive_signal_count(candidate),
        candidate.title.lower(),
    )



def _best_candidate_from_node(
    series: SeriesMappingInput,
    queries: list[str],
    node: dict[str, Any],
    *,
    discovery_reason: str,
) -> MappingCandidate | None:
    anime_id = node.get("id")
    if anime_id is None:
        return None
    best_candidate: MappingCandidate | None = None
    for query in queries:
        score, reasons = _score_candidate(series, query, node)
        candidate = MappingCandidate(
            mal_anime_id=int(anime_id),
            title=str(node.get("title") or ""),
            alternative_titles=_extract_titles_from_node(node)[1:],
            media_type=node.get("media_type"),
            status=node.get("status"),
            num_episodes=node.get("num_episodes"),
            score=score,
            matched_query=query,
            match_reasons=[*reasons, discovery_reason],
            raw=node,
        )
        if best_candidate is None or candidate.score > best_candidate.score:
            best_candidate = candidate
    return best_candidate


def _inject_supplemental_candidates(
    client: MalClient,
    series: SeriesMappingInput,
    queries: list[str],
    by_id: dict[int, MappingCandidate],
) -> None:
    if any(
        "exact_normalized_title" in candidate.match_reasons or candidate.score >= 0.90
        for candidate in by_id.values()
    ):
        return
    candidate_ids: set[int] = set()
    for key in {normalize_title_strict(series.title), normalize_title_strict(series.season_title)}:
        candidate_ids.update(_SUPPLEMENTAL_TITLE_CANDIDATE_IDS.get(key, []))
    for anime_id in sorted(candidate_ids):
        try:
            detail = client.get_anime_details(anime_id, fields="id,title,alternative_titles,media_type,status,num_episodes,start_season")
        except MalApiError:
            continue
        if not isinstance(detail, dict):
            continue
        candidate = _best_candidate_from_node(
            series,
            queries,
            detail,
            discovery_reason="supplemental_title_candidate",
        )
        if candidate is None:
            continue
        previous = by_id.get(candidate.mal_anime_id)
        if previous is None or candidate.score > previous.score:
            by_id[candidate.mal_anime_id] = candidate



def _expand_candidates_via_relations(
    client: MalClient,
    series: SeriesMappingInput,
    queries: list[str],
    by_id: dict[int, MappingCandidate],
) -> None:
    ranked = sorted(by_id.values(), key=_candidate_sort_key, reverse=True)
    if not ranked:
        return
    top = ranked[0]
    second = ranked[1] if len(ranked) > 1 else None
    if not _should_expand_related_candidates(series, top, second):
        return

    seed_candidates = sorted(ranked[:_RELATION_EXPANSION_MAX_SEEDS], key=_relation_expansion_seed_key, reverse=True)
    seed_ids = [candidate.mal_anime_id for candidate in seed_candidates]
    queue = deque((anime_id, 0) for anime_id in seed_ids)
    queued_ids = set(seed_ids)
    visited_ids: set[int] = set()

    while queue and len(visited_ids) < _RELATION_EXPANSION_MAX_VISITS:
        anime_id, depth = queue.popleft()
        if anime_id in visited_ids:
            continue
        visited_ids.add(anime_id)
        try:
            detail = client.get_anime_details(anime_id, fields=_RELATION_EXPANSION_FIELDS)
        except MalApiError:
            continue
        if not isinstance(detail, dict):
            continue
        detail_media_type = detail.get("media_type")
        if detail_media_type in _RELATION_EXPANSION_MEDIA_TYPES:
            candidate = _best_candidate_from_node(
                series,
                queries,
                detail,
                discovery_reason="related_anime_expansion",
            )
            if candidate is not None:
                previous = by_id.get(candidate.mal_anime_id)
                if previous is None or candidate.score > previous.score:
                    by_id[candidate.mal_anime_id] = candidate
        if depth >= _RELATION_EXPANSION_MAX_DEPTH:
            continue
        next_related: list[int] = []
        for relation in detail.get("related_anime") or []:
            related = relation.get("node") or {}
            related_id = related.get("id")
            if related_id is None:
                continue
            try:
                normalized_id = int(related_id)
            except (TypeError, ValueError):
                continue
            if normalized_id in queued_ids or normalized_id in visited_ids:
                continue
            next_related.append(normalized_id)
            queued_ids.add(normalized_id)
        for normalized_id in reversed(next_related):
            queue.appendleft((normalized_id, depth + 1))


def map_series(client: MalClient, series: SeriesMappingInput, limit: int = 5) -> MappingResult:
    queries = build_search_queries(series)
    by_id: dict[int, MappingCandidate] = {}
    attempted_queries: list[str] = []
    for query in queries:
        query_variants = [query, *_fallback_queries(query)]
        for variant in query_variants:
            if not variant or variant in attempted_queries:
                continue
            attempted_queries.append(variant)
            try:
                response = client.search_anime(variant, limit=limit)
            except MalApiError:
                continue
            for entry in response.get("data", []):
                node = entry.get("node") or {}
                anime_id = node.get("id")
                if anime_id is None:
                    continue
                score, reasons = _score_candidate(series, query, node)
                alternative_titles = _extract_titles_from_node(node)[1:]
                candidate = MappingCandidate(
                    mal_anime_id=int(anime_id),
                    title=str(node.get("title") or ""),
                    alternative_titles=alternative_titles,
                    media_type=node.get("media_type"),
                    status=node.get("status"),
                    num_episodes=node.get("num_episodes"),
                    score=score,
                    matched_query=variant,
                    match_reasons=reasons,
                    raw=node,
                )
                previous = by_id.get(candidate.mal_anime_id)
                if previous is None or candidate.score > previous.score:
                    by_id[candidate.mal_anime_id] = candidate
    _inject_supplemental_candidates(client, series, queries, by_id)
    _expand_candidates_via_relations(client, series, queries, by_id)
    candidates = sorted(by_id.values(), key=_candidate_sort_key, reverse=True)
    top = candidates[0] if candidates else None
    second = candidates[1] if len(candidates) > 1 else None
    rationale: list[str] = []
    if not top:
        return MappingResult(series=series, status="no_candidates", confidence=0.0, chosen_candidate=None, candidates=[], rationale=["MAL search returned no candidates"])
    margin = top.score - (second.score if second else 0.0)
    rationale.append(f"top_score={top.score:.3f}")
    rationale.append(f"margin={margin:.3f}")
    rationale.extend(top.match_reasons)
    bundle_companion_candidate: MappingCandidate | None = None
    bundle_companion_candidates: list[MappingCandidate] | None = None
    multi_entry_bundle = _suspect_multi_entry_bundle(series, top, candidates)
    if multi_entry_bundle:
        multi_entry_bundle_reason, bundle_companion_candidates = multi_entry_bundle
        rationale.append(multi_entry_bundle_reason)
        bundle_companion_candidate = bundle_companion_candidates[0] if bundle_companion_candidates else None
    if _supports_exact_classification(series, top, second) or _supports_exact_bundle_auto_resolution(
        series,
        top,
        second,
        bundle_companion_candidates,
        candidates,
    ) or _supports_exact_later_installment_auto_resolution(
        series,
        top,
        second,
        bundle_companion_candidates,
    ) or _supports_exact_title_overflow_auto_resolution(
        series,
        top,
        candidates,
        bundle_companion_candidates,
    ):
        status = "exact"
    elif top.score >= 0.90 and margin >= 0.05:
        status = "strong"
    elif top.score >= 0.78:
        status = "ambiguous"
    else:
        status = "weak"
    return MappingResult(
        series=series,
        status=status,
        confidence=top.score,
        chosen_candidate=top,
        candidates=candidates[:limit],
        rationale=rationale,
        bundle_companion_candidate=bundle_companion_candidate,
        bundle_companion_candidates=bundle_companion_candidates,
    )
