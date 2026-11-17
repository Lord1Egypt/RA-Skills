"""Domain rules for MLB market matching and trade selection.

The market matcher deliberately fails closed unless a market is an
unambiguous full-game winner contract for the requested MLB matchup.
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

TEAM_ALIASES: dict[str, tuple[str, ...]] = {
    "Arizona Diamondbacks": (
        "arizona diamondbacks",
        "diamondbacks",
        "d backs",
        "dbacks",
        "ari",
    ),
    "Athletics": (
        "athletics",
        "oakland athletics",
        "sacramento athletics",
        "a s",
        "oak",
        "ath",
    ),
    "Atlanta Braves": ("atlanta braves", "braves", "atl"),
    "Baltimore Orioles": ("baltimore orioles", "orioles", "bal"),
    "Boston Red Sox": ("boston red sox", "red sox", "bos"),
    "Chicago Cubs": ("chicago cubs", "cubs", "chc"),
    "Chicago White Sox": ("chicago white sox", "white sox", "cws"),
    "Cincinnati Reds": ("cincinnati reds", "reds", "cin"),
    "Cleveland Guardians": ("cleveland guardians", "guardians", "cle"),
    "Colorado Rockies": ("colorado rockies", "rockies", "col"),
    "Detroit Tigers": ("detroit tigers", "tigers", "det"),
    "Houston Astros": ("houston astros", "astros", "hou"),
    "Kansas City Royals": ("kansas city royals", "kc royals", "royals", "kcr"),
    "Los Angeles Angels": ("los angeles angels", "la angels", "angels", "laa"),
    "Los Angeles Dodgers": ("los angeles dodgers", "la dodgers", "dodgers", "lad"),
    "Miami Marlins": ("miami marlins", "marlins", "mia"),
    "Milwaukee Brewers": ("milwaukee brewers", "brewers", "mil"),
    "Minnesota Twins": ("minnesota twins", "twins", "min"),
    "New York Mets": ("new york mets", "ny mets", "mets", "nym"),
    "New York Yankees": ("new york yankees", "ny yankees", "yankees", "nyy"),
    "Philadelphia Phillies": ("philadelphia phillies", "phillies", "phi"),
    "Pittsburgh Pirates": ("pittsburgh pirates", "pirates", "pit"),
    "San Diego Padres": ("san diego padres", "padres", "sd", "sdp"),
    "San Francisco Giants": ("san francisco giants", "sf giants", "giants", "sfg"),
    "Seattle Mariners": ("seattle mariners", "mariners", "sea"),
    "St. Louis Cardinals": (
        "st louis cardinals",
        "saint louis cardinals",
        "cardinals",
        "stl",
    ),
    "Tampa Bay Rays": ("tampa bay rays", "rays", "tb", "tbr"),
    "Texas Rangers": ("texas rangers", "rangers", "tex"),
    "Toronto Blue Jays": ("toronto blue jays", "blue jays", "tor"),
    "Washington Nationals": ("washington nationals", "nationals", "nats", "wsh"),
}

_GENERIC_OUTCOMES = {"yes", "no", "true", "false", "over", "under"}


def normalize_text(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().replace("&", " and ")
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text).split())


def _contains_alias(text: str, alias: str) -> bool:
    return re.search(rf"(?:^|\s){re.escape(alias)}(?:$|\s)", text) is not None


def canonical_team(name: str) -> str:
    normalized = normalize_text(name)
    for canonical, aliases in TEAM_ALIASES.items():
        candidates = (
            normalize_text(canonical),
            *(normalize_text(alias) for alias in aliases),
        )
        if any(normalized == candidate for candidate in candidates):
            return canonical
    return name.strip()


def teams_in_text(text: Any, allowed: Iterable[str] | None = None) -> list[str]:
    normalized = normalize_text(text)
    allowed_set = None
    if allowed is not None:
        allowed_set = {canonical_team(team) for team in allowed}

    matches: list[str] = []
    for canonical, aliases in TEAM_ALIASES.items():
        if allowed_set is not None and canonical not in allowed_set:
            continue
        candidates = sorted(
            {normalize_text(canonical), *(normalize_text(alias) for alias in aliases)},
            key=len,
            reverse=True,
        )
        if any(_contains_alias(normalized, alias) for alias in candidates if alias):
            matches.append(canonical)
    return matches


def _iter_outcome_labels(value: Any) -> Iterable[str]:
    if value is None:
        return []
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("["):
            try:
                return _iter_outcome_labels(json.loads(stripped))
            except json.JSONDecodeError:
                return [value]
        return [value]
    if isinstance(value, Mapping):
        labels: list[str] = []
        for key in ("name", "label", "outcome", "title", "selection"):
            if value.get(key):
                labels.append(str(value[key]))
        return labels
    if isinstance(value, Sequence):
        labels = []
        for item in value:
            labels.extend(_iter_outcome_labels(item))
        return labels
    return [str(value)]


def market_text(market: Mapping[str, Any]) -> str:
    parts = []
    for key in (
        "question",
        "title",
        "name",
        "description",
        "slug",
        "subtitle",
        "event_title",
    ):
        value = market.get(key)
        if value:
            parts.append(str(value))
    return " | ".join(parts)


class MarketMatchPolicy:
    """Match YES to a team only for safe full-game MLB winner markets."""

    _NON_WINNER_PATTERN = re.compile(
        r"\b(?:"
        r"hits?|home\s+runs?|homers?|strikeouts?|rbis?|"
        r"runs?|scores?|earned\s+runs?|walks?|total\s+bases?|"
        r"stolen\s+bases?|outs?\s+recorded|pitches?|"
        r"run\s+line|totals?|over|under|spread|cover"
        r")\b"
    )
    _PARTIAL_OR_MULTI_GAME_PATTERN = re.compile(
        r"\b(?:"
        r"innings?|first\s+(?:5|five)|series|double\s*header|"
        r"game\s+(?:1|2|one|two)"
        r")\b"
    )
    _FUTURE_PATTERN = re.compile(
        r"\b(?:"
        r"playoffs?|postseason|world\s+series|pennant|wild\s+card|"
        r"(?:al|nl)\s+(?:east|central|west)|division|regular\s+season|"
        r"most\s+valuable\s+player|mvp|cy\s+young|rookie\s+of\s+the\s+year"
        r")\b"
    )
    _SIGNED_HANDICAP_PATTERN = re.compile(r"(?:^|\s)[+-]\d+(?:\.\d+)?(?:$|\s)")
    _WINNER_PATTERNS = (
        re.compile(r"\bwill\s+(.{1,100}?)\s+(?:win|beat|defeat)\b"),
        re.compile(r"\bdoes\s+(.{1,100}?)\s+win\b"),
        re.compile(r"^(.{1,100}?)\s+to\s+win\b"),
        re.compile(r"^(.{1,100}?)\s+(?:wins?|beats?|defeats?)\b"),
    )

    def infer_yes_team(
        self,
        market: Mapping[str, Any],
        home_team: str,
        away_team: str,
    ) -> str | None:
        """Return the team represented by YES for a full-game winner market.

        Explicit outcome metadata takes precedence over question parsing, but
        it never overrides a market-type exclusion. Text-only fallback is
        accepted only when win, beat, or defeat wording names exactly one of
        the two teams.

        Args:
            market: Simmer market metadata.
            home_team: Home team from the matched MLB game.
            away_team: Away team from the matched MLB game.

        Returns:
            The canonical YES team, or ``None`` when the market type or team
            mapping is unsafe or ambiguous.
        """
        text = market_text(market)
        if self._is_excluded_market(text):
            return None

        allowed = (canonical_team(home_team), canonical_team(away_team))
        if not self._matches_current_game(market, text, allowed):
            return None
        explicit_team = self._explicit_yes_team(market, allowed)
        if explicit_team is not None:
            return explicit_team

        normalized_text = normalize_text(text)
        for pattern in self._WINNER_PATTERNS:
            match = pattern.search(normalized_text)
            if match is None:
                continue
            found = teams_in_text(match.group(1), allowed)
            if len(found) == 1:
                return found[0]
        return None

    def _is_excluded_market(self, text: str) -> bool:
        normalized = normalize_text(text)
        return any(
            pattern.search(candidate) is not None
            for pattern, candidate in (
                (self._NON_WINNER_PATTERN, normalized),
                (self._PARTIAL_OR_MULTI_GAME_PATTERN, normalized),
                (self._FUTURE_PATTERN, normalized),
                (self._SIGNED_HANDICAP_PATTERN, text.lower()),
            )
        )

    def _matches_current_game(
        self,
        market: Mapping[str, Any],
        text: str,
        allowed: Sequence[str],
    ) -> bool:
        """Require the contract identity to describe the current matchup.

        Args:
            market: Simmer market metadata.
            text: Combined human-readable market fields.
            allowed: Canonical home and away team names.

        Returns:
            Whether no foreign opponent is present and the contract supplies
            both matchup teams.
        """
        identity_values = [text]
        identity_values.extend(
            str(value) for value in self._explicit_values(market) if value
        )
        identity_values.extend(
            _iter_outcome_labels(market.get("outcomes") or market.get("outcome_names"))
        )
        identity_values.extend(_iter_outcome_labels(market.get("tokens")))
        referenced = set(teams_in_text(" | ".join(identity_values)))
        allowed_set = set(allowed)
        if referenced.difference(allowed_set):
            return False
        return referenced == allowed_set

    def _explicit_yes_team(
        self,
        market: Mapping[str, Any],
        allowed: Sequence[str],
    ) -> str | None:
        for value in self._explicit_values(market):
            found = teams_in_text(value, allowed)
            if len(found) == 1:
                return found[0]
        return None

    def _explicit_values(self, market: Mapping[str, Any]) -> list[Any]:
        values = [
            market[key]
            for key in (
                "yes_label",
                "yes_outcome",
                "outcome",
                "selection",
                "token_name",
            )
            if market.get(key) is not None
        ]

        outcomes = market.get("outcomes") or market.get("outcome_names")
        labels = list(_iter_outcome_labels(outcomes))
        if labels and normalize_text(labels[0]) not in _GENERIC_OUTCOMES:
            values.append(labels[0])

        tokens = market.get("tokens")
        if (
            isinstance(tokens, Sequence)
            and not isinstance(tokens, (str, bytes))
            and tokens
        ):
            first_token_labels = list(_iter_outcome_labels(tokens[0]))
            if first_token_labels:
                values.append(first_token_labels[0])
        return values


_DEFAULT_MARKET_MATCH_POLICY = MarketMatchPolicy()


def infer_yes_team(
    market: Mapping[str, Any],
    home_team: str,
    away_team: str,
) -> str | None:
    """Return the team represented by YES when matching is unambiguous.

    Args:
        market: Simmer market metadata.
        home_team: Home team from the matched MLB game.
        away_team: Away team from the matched MLB game.

    Returns:
        The canonical YES team, or ``None`` when matching fails closed.
    """
    return _DEFAULT_MARKET_MATCH_POLICY.infer_yes_team(
        market,
        home_team,
        away_team,
    )


def fair_probability_for_team(
    home_probability: float,
    target_team: str,
    home_team: str,
    away_team: str,
) -> float | None:
    """Map ESPN's home probability to the market's YES team without shrinking it."""
    target = canonical_team(target_team)
    home = canonical_team(home_team)
    away = canonical_team(away_team)
    if target == home:
        return home_probability
    if target == away:
        return 1.0 - home_probability
    return None


@dataclass(frozen=True)
class StrategyConfig:
    paper_min_edge: float = 0.02
    live_min_edge: float = 0.03
    early_inning_penalty: float = 0.02
    middle_inning_penalty: float = 0.01
    summary_penalty: float = 0.0125
    score_penalty: float = 0.04
    stale_after_seconds: float = 30.0
    stale_penalty_per_minute: float = 0.005
    max_stale_penalty: float = 0.02
    wide_spread_after: float = 0.04
    spread_penalty_multiplier: float = 0.50
    max_spread_penalty: float = 0.03
    fallback_fee_bps: float = 0.0
    execution_buffer: float = 0.0


@dataclass(frozen=True)
class TradeDecision:
    side: str
    price: float
    fair_probability: float
    gross_edge: float
    fee_per_share: float
    net_edge: float
    required_edge: float
    edge_margin: float


def source_allowed(source: str, mode: str, allow_score_live: bool = False) -> bool:
    if source != "score":
        return True
    return mode == "paper" or allow_score_live


def required_edge(
    mode: str,
    inning: int,
    source: str,
    age_seconds: float,
    spread: float,
    config: StrategyConfig,
) -> float:
    threshold = config.live_min_edge if mode == "live" else config.paper_min_edge

    if inning <= 3:
        threshold += config.early_inning_penalty
    elif inning <= 6:
        threshold += config.middle_inning_penalty

    if source == "summary":
        threshold += config.summary_penalty
    elif source == "score":
        threshold += config.score_penalty

    if age_seconds > config.stale_after_seconds:
        stale_minutes = (age_seconds - config.stale_after_seconds) / 60.0
        threshold += min(
            config.max_stale_penalty,
            stale_minutes * config.stale_penalty_per_minute,
        )

    if spread > config.wide_spread_after:
        threshold += min(
            config.max_spread_penalty,
            (spread - config.wide_spread_after) * config.spread_penalty_multiplier,
        )

    return round(threshold, 6)


def estimate_fee_per_share(
    price: float, fee_bps: float | None, fallback_bps: float = 0.0
) -> float:
    """Convert a fee rate into a per-share cost. No invented one-cent fee."""
    rate_bps = fallback_bps if fee_bps is None else max(0.0, fee_bps)
    return max(0.0, price) * rate_bps / 10_000.0


def select_trade(
    *,
    fair_yes_probability: float,
    yes_ask: float | None,
    no_ask: float | None,
    mode: str,
    inning: int,
    source: str,
    age_seconds: float,
    spread: float,
    fee_bps: float | None,
    config: StrategyConfig,
) -> TradeDecision | None:
    threshold = required_edge(mode, inning, source, age_seconds, spread, config)
    candidates: list[TradeDecision] = []

    for side, fair_probability, price in (
        ("yes", fair_yes_probability, yes_ask),
        ("no", 1.0 - fair_yes_probability, no_ask),
    ):
        if price is None or not 0.01 < price < 0.99:
            continue
        fee = estimate_fee_per_share(price, fee_bps, config.fallback_fee_bps)
        gross_edge = fair_probability - price
        net_edge = gross_edge - fee - config.execution_buffer
        margin = net_edge - threshold
        if margin < 0:
            continue
        candidates.append(
            TradeDecision(
                side=side,
                price=price,
                fair_probability=fair_probability,
                gross_edge=gross_edge,
                fee_per_share=fee,
                net_edge=net_edge,
                required_edge=threshold,
                edge_margin=margin,
            )
        )

    if not candidates:
        return None
    return max(candidates, key=lambda item: (item.edge_margin, item.net_edge))
