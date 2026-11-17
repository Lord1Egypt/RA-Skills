#!/usr/bin/env python3
"""Trade live MLB prediction markets through Simmer. Paper mode is the default."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

from simmer_sdk.sizing import SIZING_CONFIG_SCHEMA, size_position
from simmer_sdk.skill import get_config_path, load_config, update_config

from mlb_state import (
    DailyTradeState,
    TradeStateStore,
    UninitializedTradeStateError,
)
from mlb_strategy import (
    StrategyConfig,
    fair_probability_for_team,
    infer_yes_team,
    select_trade,
    source_allowed,
)

_stdout_reconfigure = getattr(sys.stdout, "reconfigure", None)
if callable(_stdout_reconfigure):
    try:
        _stdout_reconfigure(line_buffering=True)
    except OSError:
        pass

SKILL_SLUG = "mlb-live-trader"
TRADE_SOURCE = "sdk:mlb-live-trader"
ESPN_SCOREBOARD_URL = (
    "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
)
ESPN_SUMMARY_URL = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/summary"
MIN_SHARES_PER_ORDER = 5.0
CONFIG_PATH = Path(__file__).with_name("config.json")


class StatePathResolver:
    """Resolve one conservative risk ledger across local skill installs."""

    def __init__(
        self,
        *,
        environment: Mapping[str, str] | None = None,
        home: Path | None = None,
    ) -> None:
        """Initialize state-location inputs.

        Args:
            environment: Environment containing state-home and path overrides.
            home: Injectable user home for deterministic tests.
        """
        self._environment = environment if environment is not None else os.environ
        self._home = home or Path.home()

    def resolve(self) -> Path:
        """Return an installation-independent owner-local ledger path.

        Returns:
            Explicit shared path or an XDG skill-wide state path.

        Raises:
            ValueError: If an explicit state path is not absolute.
        """
        explicit = self._environment.get("SIMMER_MLB_STATE_PATH")
        if explicit:
            explicit_path = Path(explicit)
            if not explicit_path.is_absolute():
                raise ValueError("SIMMER_MLB_STATE_PATH must be absolute")
            return explicit_path

        state_home_value = self._environment.get("XDG_STATE_HOME")
        if state_home_value:
            state_home = Path(state_home_value)
            if not state_home.is_absolute():
                raise ValueError("XDG_STATE_HOME must be absolute")
        else:
            state_home = self._home / ".local" / "state"
        return state_home / "simmer" / SKILL_SLUG / "live_state.json"

    def legacy_path(self) -> Path:
        """Return the pre-v2.2 installation-local ledger path.

        Returns:
            Path eligible for one-time migration into the central ledger.
        """
        return Path(__file__).with_name("live_state.json")


_SDK_SIZING_SCHEMA: dict[str, dict[str, Any]] = {
    "position_sizing": {
        **SIZING_CONFIG_SCHEMA["position_sizing"],
        "env": "SIMMER_POSITION_SIZING",
    },
    "kelly_multiplier": {
        **SIZING_CONFIG_SCHEMA["kelly_multiplier"],
        "env": "SIMMER_KELLY_MULTIPLIER",
        "default": 0.20,
    },
    "min_ev": {
        **SIZING_CONFIG_SCHEMA["min_ev"],
        "env": "SIMMER_MIN_EV",
    },
}

CONFIG_SCHEMA: dict[str, dict[str, Any]] = {
    **_SDK_SIZING_SCHEMA,
    "paper_min_edge": {
        "env": "SIMMER_MLB_PAPER_MIN_EDGE",
        "default": 0.02,
        "type": float,
    },
    "live_min_edge": {
        "env": "SIMMER_MLB_LIVE_MIN_EDGE",
        "default": 0.03,
        "type": float,
    },
    "early_inning_penalty": {
        "env": "SIMMER_MLB_EARLY_PENALTY",
        "default": 0.02,
        "type": float,
    },
    "middle_inning_penalty": {
        "env": "SIMMER_MLB_MIDDLE_PENALTY",
        "default": 0.01,
        "type": float,
    },
    "summary_penalty": {
        "env": "SIMMER_MLB_SUMMARY_PENALTY",
        "default": 0.0125,
        "type": float,
    },
    "score_penalty": {
        "env": "SIMMER_MLB_SCORE_PENALTY",
        "default": 0.04,
        "type": float,
    },
    "stale_after_seconds": {
        "env": "SIMMER_MLB_STALE_AFTER",
        "default": 30.0,
        "type": float,
    },
    "stale_penalty_per_minute": {
        "env": "SIMMER_MLB_STALE_PENALTY",
        "default": 0.005,
        "type": float,
    },
    "max_stale_penalty": {
        "env": "SIMMER_MLB_MAX_STALE_PENALTY",
        "default": 0.02,
        "type": float,
    },
    "wide_spread_after": {
        "env": "SIMMER_MLB_WIDE_SPREAD_AFTER",
        "default": 0.04,
        "type": float,
    },
    "spread_penalty_multiplier": {
        "env": "SIMMER_MLB_SPREAD_PENALTY",
        "default": 0.50,
        "type": float,
    },
    "max_spread_penalty": {
        "env": "SIMMER_MLB_MAX_SPREAD_PENALTY",
        "default": 0.03,
        "type": float,
    },
    "fallback_fee_bps": {
        "env": "SIMMER_MLB_FALLBACK_FEE_BPS",
        "default": 0.0,
        "type": float,
    },
    "execution_buffer": {
        "env": "SIMMER_MLB_EXECUTION_BUFFER",
        "default": 0.0,
        "type": float,
    },
    "max_quote_age_seconds": {
        "env": "SIMMER_MLB_MAX_QUOTE_AGE",
        "default": 60.0,
        "type": float,
    },
    "max_signal_age_seconds": {
        "env": "SIMMER_MLB_MAX_SIGNAL_AGE",
        "default": 90.0,
        "type": float,
    },
    "max_signal_future_skew_seconds": {
        "env": "SIMMER_MLB_MAX_SIGNAL_FUTURE_SKEW",
        "default": 5.0,
        "type": float,
    },
    "max_spread_paper": {
        "env": "SIMMER_MLB_MAX_SPREAD_PAPER",
        "default": 0.14,
        "type": float,
    },
    "max_spread_live": {
        "env": "SIMMER_MLB_MAX_SPREAD_LIVE",
        "default": 0.10,
        "type": float,
    },
    "max_position_usd": {
        "env": "SIMMER_MLB_MAX_POSITION",
        "default": 5.0,
        "type": float,
    },
    "max_bankroll_fraction": {
        "env": "SIMMER_MLB_MAX_BANKROLL_FRACTION",
        "default": 0.05,
        "type": float,
    },
    "min_trade_usd": {"env": "SIMMER_MLB_MIN_TRADE", "default": 1.0, "type": float},
    "max_trades_per_run": {
        "env": "SIMMER_MLB_MAX_TRADES_RUN",
        "default": 4,
        "type": int,
    },
    "max_live_trades_per_day": {
        "env": "SIMMER_MLB_MAX_TRADES_DAY",
        "default": 12,
        "type": int,
    },
    "live_daily_budget_usd": {
        "env": "SIMMER_MLB_DAILY_BUDGET",
        "default": 25.0,
        "type": float,
    },
    "paper_bankroll_usd": {
        "env": "SIMMER_MLB_PAPER_BANKROLL",
        "default": 100.0,
        "type": float,
    },
    "allow_score_fallback_paper": {
        "env": "SIMMER_MLB_SCORE_FALLBACK_PAPER",
        "default": True,
        "type": bool,
    },
    "allow_score_fallback_live": {
        "env": "SIMMER_MLB_SCORE_FALLBACK_LIVE",
        "default": False,
        "type": bool,
    },
    "context_max_slippage": {
        "env": "SIMMER_MLB_MAX_SLIPPAGE",
        "default": 0.12,
        "type": float,
    },
    "synthetic_spread": {
        "env": "SIMMER_MLB_SYNTHETIC_SPREAD",
        "default": 0.01,
        "type": float,
    },
    "market_query": {"env": "SIMMER_MLB_MARKET_QUERY", "default": "MLB", "type": str},
    "order_type": {"env": "SIMMER_MLB_ORDER_TYPE", "default": "FAK", "type": str},
}

CONFIG_LIMITS: dict[str, tuple[float, float]] = {
    "kelly_multiplier": (0.05, 1.0),
    "min_ev": (0.0, 0.2),
    "paper_min_edge": (0.0, 0.2),
    "live_min_edge": (0.0, 0.2),
    "early_inning_penalty": (0.0, 0.1),
    "middle_inning_penalty": (0.0, 0.1),
    "summary_penalty": (0.0, 0.1),
    "score_penalty": (0.0, 0.15),
    "stale_after_seconds": (5.0, 180.0),
    "stale_penalty_per_minute": (0.0, 0.03),
    "max_stale_penalty": (0.0, 0.1),
    "wide_spread_after": (0.0, 0.2),
    "spread_penalty_multiplier": (0.0, 2.0),
    "max_spread_penalty": (0.0, 0.1),
    "fallback_fee_bps": (0.0, 1000.0),
    "execution_buffer": (0.0, 0.05),
    "max_quote_age_seconds": (5.0, 300.0),
    "max_signal_age_seconds": (5.0, 300.0),
    "max_signal_future_skew_seconds": (0.0, 30.0),
    "max_spread_paper": (0.01, 0.5),
    "max_spread_live": (0.01, 0.5),
    "max_position_usd": (1.0, 1000.0),
    "max_bankroll_fraction": (0.001, 0.5),
    "min_trade_usd": (1.0, 100.0),
    "max_trades_per_run": (1.0, 20.0),
    "max_live_trades_per_day": (1.0, 100.0),
    "live_daily_budget_usd": (1.0, 10000.0),
    "paper_bankroll_usd": (10.0, 100000.0),
    "context_max_slippage": (0.0, 0.5),
    "synthetic_spread": (0.0, 0.1),
}


@dataclass(frozen=True)
class LiveGame:
    game_id: str
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    inning: int
    detail: str
    competition: Mapping[str, Any]
    same_matchup_events: int = 1


@dataclass(frozen=True)
class GameSignal:
    game: LiveGame
    home_probability: float
    source: str
    age_seconds: float
    observed_monotonic: float | None = None


@dataclass(frozen=True)
class Quote:
    """Executable outcome prices and top-of-book metadata."""

    yes_ask: float | None
    no_ask: float | None
    spread: float
    fee_bps: float | None
    yes_ask_size: float | None = None
    no_ask_size: float | None = None
    quote_age_seconds: float | None = None
    quote_timestamp: float | None = None


class ConfigLoader(Protocol):
    """Load a resolved Simmer skill configuration."""

    def __call__(
        self,
        schema: Mapping[str, Mapping[str, Any]],
        skill_file: str,
        *,
        slug: str,
    ) -> Mapping[str, Any]:
        """Return resolved values for one skill."""


class ConfigUpdater(Protocol):
    """Persist approved Simmer skill configuration overrides."""

    def __call__(
        self, updates: Mapping[str, Any], skill_file: str
    ) -> Mapping[str, Any]:
        """Persist and return the merged configuration."""


class ConfigPathResolver(Protocol):
    """Resolve the SDK-owned configuration path."""

    def __call__(self, skill_file: str) -> str | Path:
        """Return the path used by the Simmer config adapter."""


class PositionSizeFunction(Protocol):
    """Calculate a position through the Simmer sizing contract."""

    def __call__(
        self,
        *,
        p_win: float,
        market_price: float,
        bankroll: float,
        method: str,
        kelly_multiplier: float,
        min_ev: float,
        max_fraction: float,
    ) -> float:
        """Return a proposed order amount in dollars."""


class RuntimeConfigValidator:
    """Validate high-impact runtime settings before they reach the SDK."""

    _POSITION_SIZING_METHODS = frozenset({"fixed", "kelly", "fractional_kelly"})
    _ORDER_TYPES = frozenset({"FAK", "FOK", "GTC", "GTD"})

    def validate(self, config: Mapping[str, Any]) -> dict[str, Any]:
        """Return a validated copy of runtime configuration values.

        Args:
            config: Resolved or partial runtime configuration.

        Returns:
            A mutable validated copy.

        Raises:
            ValueError: If any runtime setting has an unsafe type or value.
        """
        values = dict(config)
        for key, specification in CONFIG_SCHEMA.items():
            if key not in values:
                continue
            expected_type = specification["type"]
            raw_value = values[key]
            if expected_type is bool and not isinstance(raw_value, bool):
                raise ValueError(f"{key} must be a boolean")
            if expected_type is str and not isinstance(raw_value, str):
                raise ValueError(f"{key} must be a string")
        for key, (minimum, maximum) in CONFIG_LIMITS.items():
            if key not in values:
                continue
            raw_value = values[key]
            expected_type = CONFIG_SCHEMA[key]["type"]
            if isinstance(raw_value, bool) or not isinstance(raw_value, (int, float)):
                raise ValueError(f"{key} must be numeric")
            if expected_type is int and not isinstance(raw_value, int):
                raise ValueError(f"{key} must be an integer")
            numeric_value = float(raw_value)
            if not math.isfinite(numeric_value):
                raise ValueError(f"{key} must be finite")
            if not minimum <= numeric_value <= maximum:
                raise ValueError(f"{key} must be between {minimum:g} and {maximum:g}")
        method = values.get("position_sizing")
        if method is not None and str(method) not in self._POSITION_SIZING_METHODS:
            allowed = ", ".join(sorted(self._POSITION_SIZING_METHODS))
            raise ValueError(f"position_sizing must be one of: {allowed}")
        order_type = values.get("order_type")
        if order_type is not None:
            normalized_order_type = str(order_type).strip().upper()
            if normalized_order_type not in self._ORDER_TYPES:
                allowed_order_types = ", ".join(sorted(self._ORDER_TYPES))
                raise ValueError(f"order_type must be one of: {allowed_order_types}")
            values["order_type"] = normalized_order_type
        return values


class ConfigValueParser:
    """Coerce human-readable configuration values without silent fallback."""

    _TRUE_VALUES = frozenset({"1", "true", "yes", "on"})
    _FALSE_VALUES = frozenset({"0", "false", "no", "off"})

    @classmethod
    def coerce(cls, value: Any, expected_type: type) -> Any:
        """Convert one boundary value to its declared configuration type.

        Args:
            value: Raw CLI or environment value.
            expected_type: Declared schema type.

        Returns:
            Typed configuration value.

        Raises:
            ValueError: If the value cannot be converted unambiguously.
        """
        if expected_type is bool:
            if isinstance(value, bool):
                return value
            normalized = str(value).strip().lower()
            if normalized in cls._TRUE_VALUES:
                return True
            if normalized in cls._FALSE_VALUES:
                return False
            raise ValueError("Expected an explicit boolean value")
        return expected_type(value)


class RuntimeConfigRepository:
    """Load and update runtime settings through the public Simmer SDK API."""

    def __init__(
        self,
        *,
        loader: ConfigLoader = load_config,
        updater: ConfigUpdater = update_config,
        path_resolver: ConfigPathResolver = get_config_path,
        skill_file: str = __file__,
        validator: RuntimeConfigValidator | None = None,
        environment: Mapping[str, str] | None = None,
    ) -> None:
        """Initialize the SDK config adapter.

        Args:
            loader: Public SDK config loader.
            updater: Public SDK config updater.
            path_resolver: Public SDK config-path resolver.
            skill_file: Entrypoint used to locate ``config.json``.
            validator: Boundary validator for high-impact settings.
            environment: Injectable environment containing SDK overrides.
        """
        self._loader = loader
        self._updater = updater
        self._path_resolver = path_resolver
        self._skill_file = skill_file
        self._validator = validator or RuntimeConfigValidator()
        self._environment = environment if environment is not None else os.environ

    def load(self) -> dict[str, Any]:
        """Return the fully resolved runtime configuration.

        Returns:
            A mutable copy of the resolved configuration.

        Raises:
            TypeError: If the SDK returns an invalid config payload.
            RuntimeError: Propagated from the SDK for invalid configuration.
        """
        self._validate_raw_config_sources()
        resolved = self._loader(CONFIG_SCHEMA, self._skill_file, slug=SKILL_SLUG)
        if not isinstance(resolved, Mapping):
            raise TypeError("Simmer configuration must resolve to a mapping")
        return self._validator.validate(resolved)

    def save(self, updates: Mapping[str, Any]) -> dict[str, Any]:
        """Persist validated configuration overrides.

        Args:
            updates: Parsed setting names and values.

        Returns:
            The SDK's merged configuration.

        Raises:
            TypeError: If the SDK returns an invalid config payload.
            RuntimeError: Propagated from the SDK when persistence fails.
        """
        self._validate_raw_config_sources()
        validated = self._validator.validate(updates)
        saved = self._updater(validated, self._skill_file)
        if not isinstance(saved, Mapping):
            raise TypeError("Simmer configuration update must return a mapping")
        return self._validator.validate(saved)

    def path(self) -> Path:
        """Return the SDK-owned local configuration path.

        Returns:
            Absolute or relative path reported by the SDK.
        """
        return Path(self._path_resolver(self._skill_file))

    def _validate_raw_config_sources(self) -> None:
        """Reject malformed file and environment values before SDK fallback."""
        self._validate_persisted_config()
        for key, specification in CONFIG_SCHEMA.items():
            environment_name = specification.get("env")
            if not isinstance(environment_name, str):
                continue
            raw_value = self._environment.get(environment_name)
            if raw_value is None:
                continue
            try:
                parsed = ConfigValueParser.coerce(
                    raw_value,
                    specification["type"],
                )
                self._validator.validate({key: parsed})
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"{environment_name} contains an invalid value"
                ) from exc

    def _validate_persisted_config(self) -> None:
        """Reject a corrupt local file before the SDK can fall back silently."""
        config_path = self.path()
        try:
            serialized = config_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return
        except OSError as exc:
            raise RuntimeError(f"Cannot read Simmer config at {config_path}") from exc
        try:
            payload = json.loads(serialized)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Simmer config at {config_path} contains invalid JSON"
            ) from exc
        if not isinstance(payload, Mapping):
            raise RuntimeError(f"Simmer config at {config_path} must be a JSON object")
        unknown_keys = sorted(set(payload).difference(CONFIG_SCHEMA))
        if unknown_keys:
            names = ", ".join(unknown_keys)
            raise ValueError(f"Simmer config contains unknown settings: {names}")
        self._validator.validate(payload)


@dataclass(frozen=True)
class PositionSizingRequest:
    """Inputs required to size one approved trade candidate."""

    bankroll: float
    fair_probability: float
    market_price: float
    method: str
    kelly_multiplier: float
    min_ev: float
    max_position_usd: float
    max_bankroll_fraction: float
    min_trade_usd: float


class SdkPositionSizer:
    """Apply Simmer sizing and hard venue/strategy caps without flooring up."""

    def __init__(self, size_function: PositionSizeFunction = size_position) -> None:
        """Initialize the sizing adapter.

        Args:
            size_function: Injectable Simmer sizing implementation.
        """
        self._size_function = size_function

    def size(self, request: PositionSizingRequest) -> float:
        """Return a bounded order amount or zero when it is too small.

        Args:
            request: Validated sizing inputs for one candidate.

        Returns:
            Dollar amount rounded to cents, or zero when the SDK result cannot
            satisfy the minimum order without increasing risk.
        """
        cap = min(
            request.max_position_usd,
            request.bankroll * request.max_bankroll_fraction,
        )
        venue_minimum = max(
            0.01,
            request.min_trade_usd,
            MIN_SHARES_PER_ORDER * request.market_price,
        )
        if request.bankroll <= 0 or cap < venue_minimum:
            return 0.0

        proposed = self._size_function(
            p_win=request.fair_probability,
            market_price=request.market_price,
            bankroll=request.bankroll,
            method=request.method,
            kelly_multiplier=request.kelly_multiplier,
            min_ev=request.min_ev,
            max_fraction=request.max_bankroll_fraction,
        )
        if not isinstance(proposed, (int, float)) or not math.isfinite(float(proposed)):
            return 0.0
        amount = round(min(float(proposed), cap), 2)
        if amount < venue_minimum:
            return 0.0
        return amount


class MarketDiscoveryError(RuntimeError):
    """Raised when every Simmer market-discovery request fails."""


class MarketCatalog:
    """Read active Polymarket-backed markets through the public Simmer API."""

    _FIELDS = (
        "id",
        "market_id",
        "question",
        "title",
        "name",
        "description",
        "slug",
        "subtitle",
        "event_title",
        "status",
        "yes_label",
        "yes_outcome",
        "outcome",
        "selection",
        "token_name",
        "outcomes",
        "outcome_names",
        "tokens",
        "outcome_prices",
        "outcomePrices",
        "current_probability",
        "probability",
        "price",
        "resolves_at",
        "is_live_now",
        "opens_at",
        "resolution_criteria",
        "best_bid",
        "best_ask",
        "best_bid_size",
        "best_ask_size",
        "spread",
        "spread_pct",
        "quote_ts",
        "quote_age_seconds",
        "fee_rate_bps",
        "taker_fee_bps",
        "liquidity_tier",
        "polymarket_token_id",
        "polymarket_no_token_id",
        "polymarket_condition_id",
        "polymarket_neg_risk",
    )

    def __init__(self, client: Any, *, limit: int = 100) -> None:
        self._client = client
        self._limit = limit

    def find_active(self, *, query: str) -> list[dict[str, Any]]:
        """Return active MLB markets using filtered, volume-sorted requests."""
        attempts = (
            {"q": query},
            {"tags": "mlb"},
        )
        failures: list[Exception] = []
        for selector in attempts:
            try:
                rows = self._client.get_markets(
                    status="active",
                    venue="polymarket",
                    sort="volume",
                    limit=self._limit,
                    **selector,
                )
            except Exception as exc:
                failures.append(exc)
                continue
            markets = [self._to_mapping(row) for row in rows]
            markets = [
                market
                for market in markets
                if market.get("id") or market.get("market_id")
            ]
            if markets:
                return markets
        if failures and len(failures) == len(attempts):
            raise MarketDiscoveryError("Simmer market discovery failed") from failures[
                -1
            ]
        return []

    @classmethod
    def _to_mapping(cls, market: Any) -> dict[str, Any]:
        if isinstance(market, Mapping):
            return dict(market)
        return {
            field: getattr(market, field)
            for field in cls._FIELDS
            if hasattr(market, field)
        }


class MarketTimingPolicy:
    """Bind a live contract to the current ESPN game window."""

    _MIN_RESOLUTION_DELTA_SECONDS = 0.0
    _MAX_RESOLUTION_DELTA_SECONDS = 12.0 * 60.0 * 60.0

    def rejection_reason(
        self,
        market: Mapping[str, Any],
        game: LiveGame,
    ) -> str | None:
        """Return why market timing cannot represent the current live game.

        Args:
            market: Simmer market metadata.
            game: Matched live ESPN game.

        Returns:
            A stable rejection reason, or ``None`` for a current game window.
        """
        if market.get("is_live_now") is not True:
            return "market is not confirmed live"
        if game.same_matchup_events != 1:
            return "same-day matchup is an ambiguous doubleheader"
        game_time = self._parse_timestamp(game.competition.get("date"))
        resolution_time = self._parse_timestamp(market.get("resolves_at"))
        if game_time is None or resolution_time is None:
            return "market or game timing is unavailable"
        delta = (resolution_time - game_time).total_seconds()
        if not (
            self._MIN_RESOLUTION_DELTA_SECONDS
            <= delta
            <= self._MAX_RESOLUTION_DELTA_SECONDS
        ):
            return "market resolution does not match the live game window"
        return None

    @staticmethod
    def _parse_timestamp(value: Any) -> datetime | None:
        if not value:
            return None
        try:
            parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        except ValueError:
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)


class MarketContextReader:
    """Read Simmer diagnostics for the strategy's own probability estimate."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def get(
        self,
        market_id: str,
        *,
        fair_yes_probability: float,
    ) -> Mapping[str, Any] | None:
        """Return Polymarket context calculated against the supplied fair value."""
        context = self._client.get_market_context(
            market_id,
            venue="polymarket",
            my_probability=fair_yes_probability,
        )
        return context if isinstance(context, Mapping) else None


class QuoteExtractor:
    """Build executable YES and NO quotes from Simmer top-of-book data."""

    def __init__(self, *, synthetic_spread: float) -> None:
        self._synthetic_spread = synthetic_spread

    def extract(
        self,
        market: Mapping[str, Any],
        context: Mapping[str, Any] | None,
    ) -> Quote:
        """Prefer real order-book prices and use midpoint estimates only as fallback."""
        prices = _prices_from_outcomes(market)
        yes_bid = _first_number(market.get("best_bid"))
        explicit_yes = _first_number(
            market.get("yes_ask"),
            market.get("best_ask"),
            market.get("ask_price"),
            _nested_number(context, ("yes_ask", "best_ask", "ask_price")),
        )
        reported_spread = _first_number(
            market.get("spread"),
            market.get("spread_pct"),
            _nested_number(context, ("spread", "spread_pct", "bid_ask_spread")),
        )
        book_spread = (
            explicit_yes - yes_bid
            if explicit_yes is not None and yes_bid is not None
            else None
        )
        if book_spread is not None and book_spread < 0:
            spread = book_spread
        elif book_spread is not None:
            spread = max(
                self._synthetic_spread,
                book_spread,
                reported_spread if reported_spread is not None else 0.0,
            )
        else:
            spread = (
                reported_spread
                if reported_spread is not None
                else self._synthetic_spread
            )
        explicit_no = _first_number(
            market.get("no_ask"),
            market.get("best_no_ask"),
            _nested_number(context, ("no_ask", "best_no_ask")),
        )

        midpoint = _first_number(
            market.get("current_probability"),
            market.get("probability"),
            market.get("price"),
            prices[0] if prices else None,
        )
        no_midpoint = (
            prices[1]
            if len(prices) > 1
            else (1.0 - midpoint if midpoint is not None else None)
        )
        half_spread = spread / 2.0
        yes_ask = (
            explicit_yes
            if explicit_yes is not None
            else (midpoint + half_spread if midpoint is not None else None)
        )
        is_neg_risk = market.get("polymarket_neg_risk") is True
        no_ask: float | None
        if explicit_no is not None:
            no_ask = explicit_no
        elif is_neg_risk:
            no_ask = None
        elif yes_bid is not None:
            no_ask = 1.0 - yes_bid
        else:
            no_ask = no_midpoint + half_spread if no_midpoint is not None else None

        if yes_ask is not None:
            yes_ask = min(0.99, max(0.01, yes_ask))
        if no_ask is not None:
            no_ask = min(0.99, max(0.01, no_ask))

        fee_bps = _first_number(
            market.get("fee_rate_bps"),
            market.get("taker_fee_bps"),
            _nested_number(context, ("fee_rate_bps", "taker_fee_bps", "base_fee_bps")),
        )
        explicit_no_size = _first_number(
            market.get("no_ask_size"),
            market.get("best_no_ask_size"),
            _nested_number(context, ("no_ask_size", "best_no_ask_size")),
        )
        no_ask_size = (
            explicit_no_size
            if explicit_no is not None
            else (None if is_neg_risk else _first_number(market.get("best_bid_size")))
        )
        return Quote(
            yes_ask=yes_ask,
            no_ask=no_ask,
            spread=spread,
            fee_bps=fee_bps,
            yes_ask_size=_first_number(market.get("best_ask_size")),
            no_ask_size=no_ask_size,
            quote_age_seconds=_first_number(market.get("quote_age_seconds")),
            quote_timestamp=_first_number(market.get("quote_ts")),
        )


class QuotePolicy:
    """Apply hard spread and freshness limits before strategy evaluation."""

    def __init__(
        self,
        *,
        max_spread: float,
        max_age_seconds: float,
        require_age: bool,
        clock: Callable[[], float] | None = None,
        wall_clock: Callable[[], float] | None = None,
    ) -> None:
        """Initialize snapshot-relative quote safety limits.

        Args:
            max_spread: Maximum executable bid/ask spread.
            max_age_seconds: Maximum total age at evaluation time.
            require_age: Whether missing server age metadata must reject.
            clock: Injectable monotonic clock used to include local delay.
            wall_clock: Injectable epoch clock used to include response transit.
        """
        self._max_spread = max_spread
        self._max_age_seconds = max_age_seconds
        self._require_age = require_age
        self._clock = clock or time.monotonic
        self._wall_clock = wall_clock or time.time
        self._snapshot_time = self._clock()

    def rejection_reason(self, quote: Quote) -> str | None:
        """Return a concise rejection reason, or None when the quote is usable."""
        if not math.isfinite(quote.spread) or quote.spread < 0:
            return "quote spread is invalid"
        if quote.spread > self._max_spread:
            return f"spread {quote.spread:.1%} exceeds limit"
        local_age = max(0.0, self._clock() - self._snapshot_time)
        age_candidates: list[float] = []
        if quote.quote_age_seconds is not None:
            if (
                not math.isfinite(quote.quote_age_seconds)
                or quote.quote_age_seconds < 0
            ):
                return "quote age is invalid"
            age_candidates.append(quote.quote_age_seconds + local_age)
        if quote.quote_timestamp is not None:
            if not math.isfinite(quote.quote_timestamp):
                return "quote timestamp is invalid"
            timestamp_age = self._wall_clock() - quote.quote_timestamp
            if timestamp_age < 0:
                return "quote timestamp is in the future"
            age_candidates.append(timestamp_age)
        if not age_candidates:
            return "quote age is unavailable" if self._require_age else None
        total_age = max(age_candidates)
        if total_age > self._max_age_seconds:
            return f"quote age {total_age:.0f}s exceeds limit"
        return None


def _parse_bool(value: Any) -> bool:
    """Delegate strict boolean parsing to the configuration value parser."""
    return bool(ConfigValueParser.coerce(value, bool))


def _coerce(value: Any, type_fn: type) -> Any:
    """Delegate boundary coercion to the class-based parser."""
    return ConfigValueParser.coerce(value, type_fn)


def load_runtime_config() -> dict[str, Any]:
    """Load settings through the canonical Simmer config adapter.

    Returns:
        Resolved runtime configuration.
    """
    return RuntimeConfigRepository().load()


def save_config(updates: Mapping[str, Any]) -> dict[str, Any]:
    """Persist settings through the canonical Simmer config adapter.

    Args:
        updates: Parsed configuration overrides.

    Returns:
        Merged configuration returned by the SDK.
    """
    return RuntimeConfigRepository().save(updates)


class SimmerClientProvider:
    """Create and cache Simmer clients without crossing execution boundaries."""

    def __init__(
        self,
        *,
        client_factory: Callable[..., Any] | None = None,
        readonly_factory: Callable[..., Any] | None = None,
        environment: Mapping[str, str] | None = None,
    ) -> None:
        """Initialize mode-keyed client construction.

        Args:
            client_factory: Injectable mutable Simmer client constructor.
            readonly_factory: Injectable ``SimmerClient.readonly`` constructor.
            environment: Environment mapping containing API and venue settings.
        """
        self._client_factory = client_factory
        self._readonly_factory = readonly_factory
        self._environment = environment if environment is not None else os.environ
        self._clients: dict[tuple[bool, bool], Any] = {}

    def get(self, *, live: bool) -> Any:
        """Return a mutable client scoped to exactly one execution mode.

        Args:
            live: Whether the client may submit real orders.

        Returns:
            Mode-scoped Simmer client.

        Raises:
            RuntimeError: If the SDK or API key is unavailable.
        """
        return self._get(live=live, readonly=False)

    def get_readonly(self, *, live: bool) -> Any:
        """Return a read-only client for paper or live portfolio inspection.

        Args:
            live: Portfolio namespace to inspect without enabling mutations.

        Returns:
            SDK-enforced read-only Simmer client.
        """
        return self._get(live=live, readonly=True)

    def _get(self, *, live: bool, readonly: bool) -> Any:
        key = (live, readonly)
        if key in self._clients:
            return self._clients[key]
        mutable_factory, readonly_factory = self._factories()
        api_key = self._environment.get("SIMMER_API_KEY")
        if not api_key:
            raise RuntimeError("SIMMER_API_KEY is not set")
        venue = self._environment.get("TRADING_VENUE", "polymarket")
        if live:
            if venue.strip().lower() != "polymarket":
                raise RuntimeError(
                    "Live MLB trading requires Polymarket (TRADING_VENUE=polymarket)"
                )
            venue = "polymarket"
        factory = readonly_factory if readonly else mutable_factory
        client = factory(api_key=api_key, venue=venue, live=live)
        self._clients[key] = client
        return client

    def _factories(self) -> tuple[Callable[..., Any], Callable[..., Any]]:
        if self._client_factory is not None and self._readonly_factory is not None:
            return self._client_factory, self._readonly_factory
        try:
            from simmer_sdk import SimmerClient
        except ImportError as exc:
            raise RuntimeError(
                "simmer-sdk is not installed; run: pip install 'simmer-sdk==0.24.6'"
            ) from exc
        mutable_factory = self._client_factory or SimmerClient
        readonly_factory = self._readonly_factory or SimmerClient.readonly
        return mutable_factory, readonly_factory


_CLIENT_PROVIDER = SimmerClientProvider()


def get_client(*, live: bool) -> Any:
    """Delegate mutable client access to the mode-scoped provider.

    Args:
        live: Whether the client may submit real orders.

    Returns:
        Mode-scoped Simmer client.
    """
    return _CLIENT_PROVIDER.get(live=live)


def get_readonly_client(*, live: bool) -> Any:
    """Delegate status access to the SDK-enforced read-only provider.

    Args:
        live: Portfolio namespace to inspect.

    Returns:
        Read-only Simmer client.
    """
    return _CLIENT_PROVIDER.get_readonly(live=live)


def http_json(
    url: str, params: Mapping[str, Any] | None = None, timeout: float = 12.0
) -> Any:
    """Read JSON from the fixed ESPN HTTPS adapter boundary.

    Args:
        url: Approved ESPN endpoint URL.
        params: Optional query parameters.
        timeout: Network timeout in seconds.

    Returns:
        Decoded JSON payload.

    Raises:
        ValueError: If the URL is outside the approved ESPN HTTPS host.
        RuntimeError: If ESPN is unavailable or returns invalid JSON.
    """
    parsed_url = urlparse(url)
    if parsed_url.scheme != "https" or parsed_url.hostname != "site.api.espn.com":
        raise ValueError("http_json requires an approved ESPN HTTPS URL")
    if params:
        url = f"{url}?{urlencode(params)}"
    request = Request(url, headers={"User-Agent": "mlb-live-trader/2.2.1"})
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code} from {url}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach {url}: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON from {url}") from exc


def _to_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def _probability(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if number > 1.0:
        number /= 100.0
    if 0.0 <= number <= 1.0:
        return number
    return None


@dataclass(frozen=True)
class ScoreboardGameRow:
    """One complete ESPN scoreboard event before live-state filtering."""

    game_id: str
    home: tuple[str, int]
    away: tuple[str, int]
    state: str
    status: Mapping[str, Any]
    competition: Mapping[str, Any]

    @property
    def matchup_key(self) -> tuple[str, str]:
        """Return an order-independent team-pair identity."""
        first, second = sorted((self.home[0], self.away[0]))
        return first, second


class ScoreboardParser:
    """Parse the full ESPN slate before selecting in-progress games."""

    def parse(self, payload: Mapping[str, Any]) -> list[LiveGame]:
        """Return complete live games annotated with matchup multiplicity.

        Args:
            payload: ESPN scoreboard response.

        Returns:
            In-progress games. Each includes the number of same-team events in
            the full returned slate so doubleheaders can fail closed.
        """
        events = payload.get("events", [])
        if not isinstance(events, Sequence) or isinstance(events, (str, bytes)):
            return []
        rows = [
            row
            for event in events
            if isinstance(event, Mapping)
            for row in [self._parse_event(event)]
            if row is not None
        ]
        matchup_counts: dict[tuple[str, str], int] = {}
        for row in rows:
            matchup_counts[row.matchup_key] = matchup_counts.get(row.matchup_key, 0) + 1

        games: list[LiveGame] = []
        for row in rows:
            if row.state != "in":
                continue
            inning = _to_int(
                row.status.get("period")
                or row.competition.get("situation", {}).get("inning")
            )
            status_type = row.status.get("type") or {}
            games.append(
                LiveGame(
                    game_id=row.game_id,
                    home_team=row.home[0],
                    away_team=row.away[0],
                    home_score=row.home[1],
                    away_score=row.away[1],
                    inning=max(1, inning),
                    detail=str(
                        status_type.get("shortDetail")
                        or row.status.get("displayClock")
                        or "live"
                    ),
                    competition=row.competition,
                    same_matchup_events=matchup_counts[row.matchup_key],
                )
            )
        return games

    @staticmethod
    def _parse_event(event: Mapping[str, Any]) -> ScoreboardGameRow | None:
        competitions = event.get("competitions", [])
        if not isinstance(competitions, Sequence) or not competitions:
            return None
        first_competition = competitions[0]
        if not isinstance(first_competition, Mapping):
            return None
        competition = dict(first_competition)
        if event.get("date") and not competition.get("date"):
            competition["date"] = event["date"]
        status_value = competition.get("status") or event.get("status") or {}
        if not isinstance(status_value, Mapping):
            return None
        status = dict(status_value)
        status_type = status.get("type") or {}
        if not isinstance(status_type, Mapping):
            return None
        state = str(status_type.get("state", "")).lower()

        home: tuple[str, int] | None = None
        away: tuple[str, int] | None = None
        competitors = competition.get("competitors", [])
        if not isinstance(competitors, Sequence):
            return None
        for competitor in competitors:
            if not isinstance(competitor, Mapping):
                continue
            team_value = competitor.get("team") or {}
            if not isinstance(team_value, Mapping):
                continue
            team = team_value.get("displayName") or team_value.get("name")
            parsed = (str(team or ""), _to_int(competitor.get("score")))
            if not parsed[0]:
                continue
            if competitor.get("homeAway") == "home":
                home = parsed
            elif competitor.get("homeAway") == "away":
                away = parsed
        if home is None or away is None:
            return None
        return ScoreboardGameRow(
            game_id=str(event.get("id", "")),
            home=home,
            away=away,
            state=state,
            status=status,
            competition=competition,
        )


def fetch_live_games() -> list[LiveGame]:
    """Delegate ESPN scoreboard parsing to the full-slate parser."""
    payload = http_json(ESPN_SCOREBOARD_URL)
    return ScoreboardParser().parse(payload if isinstance(payload, Mapping) else {})


def _probability_from_object(value: Any) -> float | None:
    if not isinstance(value, Mapping):
        return None
    for key in ("homeWinPercentage", "homeWinProbability", "home_win_probability"):
        parsed = _probability(value.get(key))
        if parsed is not None:
            return parsed
    return None


def score_fallback_probability(game: LiveGame) -> float:
    score_diff = game.home_score - game.away_score
    innings_left = max(0.5, 9.5 - float(game.inning))
    home_advantage = 0.12 * min(1.0, innings_left / 9.0)
    logit = (0.90 * score_diff / math.sqrt(innings_left)) + home_advantage
    return 1.0 / (1.0 + math.exp(-logit))


class GameSignalBuilder:
    """Build deterministic ESPN signals behind an injectable clock and I/O port."""

    def __init__(
        self,
        *,
        http_reader: Callable[..., Any] | None = None,
        clock: Callable[[], datetime] | None = None,
        monotonic_clock: Callable[[], float] | None = None,
    ) -> None:
        """Initialize the ESPN signal adapter.

        Args:
            http_reader: Injectable JSON reader for ESPN summary requests.
            clock: Injectable aware UTC clock for freshness decisions.
            monotonic_clock: Injectable elapsed-time clock for downstream age.
        """
        self._http_reader = http_reader or http_json
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._monotonic_clock = monotonic_clock or time.monotonic

    def build(
        self,
        game: LiveGame,
        config: Mapping[str, Any],
        *,
        live: bool,
    ) -> GameSignal | None:
        """Return a usable signal or fail closed on unverifiable live evidence.

        Args:
            game: Parsed in-progress MLB game.
            config: Resolved runtime configuration.
            live: Whether the signal may authorize a real trade.

        Returns:
            A validated signal, or ``None`` when evidence is unavailable,
            stale, future-dated, or mismatched to the current ESPN play.
        """
        situation = game.competition.get("situation", {})
        last_play = (
            situation.get("lastPlay", {}) if isinstance(situation, Mapping) else {}
        )
        last_play_id = str(last_play.get("id") or "")
        direct = _probability_from_object(last_play.get("probability", {}))
        if direct is not None:
            age = self._timestamp_age(
                last_play.get("wallclock") or last_play.get("startDate")
            )
            if not live or self._is_fresh(age, config):
                return self._create_signal(
                    game,
                    direct,
                    "live",
                    max(0.0, age or 0.0),
                )

        summary = self._http_reader(ESPN_SUMMARY_URL, {"event": game.game_id})
        rows = summary.get("winprobability", []) if isinstance(summary, Mapping) else []
        for row in reversed(rows):
            parsed = _probability_from_object(row)
            if parsed is None:
                continue
            age = self._timestamp_age(row.get("wallclock") or row.get("timestamp"))
            row_play_id = str(row.get("playId") or row.get("play_id") or "")
            if live and (
                not self._is_fresh(age, config)
                or not last_play_id
                or not row_play_id
                or row_play_id != last_play_id
            ):
                continue
            return self._create_signal(
                game,
                parsed,
                "summary",
                max(0.0, age if age is not None else 15.0),
            )

        allowed = (
            config["allow_score_fallback_live"]
            if live
            else config["allow_score_fallback_paper"]
        )
        if allowed:
            return self._create_signal(
                game,
                score_fallback_probability(game),
                "score",
                0.0,
            )
        return None

    def _create_signal(
        self,
        game: LiveGame,
        probability: float,
        source: str,
        age_seconds: float,
    ) -> GameSignal:
        """Create one signal with its downstream elapsed-time baseline."""
        return GameSignal(
            game=game,
            home_probability=probability,
            source=source,
            age_seconds=age_seconds,
            observed_monotonic=float(self._monotonic_clock()),
        )

    def _timestamp_age(self, value: Any) -> float | None:
        if not value:
            return None
        text = str(value).replace("Z", "+00:00")
        try:
            parsed = datetime.fromisoformat(text)
        except ValueError:
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        now = self._clock()
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)
        return (
            now.astimezone(timezone.utc) - parsed.astimezone(timezone.utc)
        ).total_seconds()

    @staticmethod
    def _is_fresh(age: float | None, config: Mapping[str, Any]) -> bool:
        if age is None:
            return False
        return (
            -float(config["max_signal_future_skew_seconds"])
            <= age
            <= float(config["max_signal_age_seconds"])
        )


class SignalFreshnessPolicy:
    """Revalidate total signal age after downstream processing delays."""

    def __init__(self, clock: Callable[[], float] | None = None) -> None:
        """Initialize the deterministic elapsed-time source.

        Args:
            clock: Injectable monotonic clock.
        """
        self._clock = clock or time.monotonic

    def current_age(
        self,
        signal: GameSignal,
        *,
        live: bool,
        max_age_seconds: float,
    ) -> float | None:
        """Return total signal age or ``None`` when live evidence is unsafe.

        Args:
            signal: Signal carrying its initial wall-clock age and observation.
            live: Whether the value may authorize a live order.
            max_age_seconds: Hard live freshness limit.

        Returns:
            Current non-negative age, or ``None`` for invalid or stale evidence.
        """
        age = float(signal.age_seconds)
        if not math.isfinite(age) or age < 0:
            return None
        observed = signal.observed_monotonic
        if observed is None:
            return None if live else age
        current = float(self._clock())
        if (
            not math.isfinite(observed)
            or not math.isfinite(current)
            or current < observed
        ):
            return None
        current_age = age + (current - observed)
        if live and current_age > max_age_seconds:
            return None
        return current_age


def build_game_signal(
    game: LiveGame, config: Mapping[str, Any], *, live: bool
) -> GameSignal | None:
    """Delegate compatibility calls to the class-based signal builder.

    Args:
        game: Parsed in-progress MLB game.
        config: Resolved runtime configuration.
        live: Whether the signal may authorize a real trade.

    Returns:
        Validated ESPN signal or ``None``.
    """
    return GameSignalBuilder().build(game, config, live=live)


def fetch_markets(client: Any, query: str) -> list[dict[str, Any]]:
    return MarketCatalog(client).find_active(query=query)


class FiniteNumberParser:
    """Normalize untrusted numeric metadata without admitting NaN or infinity."""

    @staticmethod
    def parse(value: Any) -> float | None:
        """Return one finite float or ``None`` for unusable input.

        Args:
            value: Untrusted SDK or HTTP boundary value.

        Returns:
            Finite floating-point value, or ``None``.
        """
        try:
            parsed = float(value)
        except (TypeError, ValueError):
            return None
        return parsed if math.isfinite(parsed) else None


_NUMBER_PARSER = FiniteNumberParser()


def _number(value: Any) -> float | None:
    """Delegate legacy numeric parsing calls to the finite parser."""
    return _NUMBER_PARSER.parse(value)


def _first_number(*values: Any) -> float | None:
    for value in values:
        parsed = _number(value)
        if parsed is not None:
            return parsed
    return None


def _prices_from_outcomes(market: Mapping[str, Any]) -> list[float]:
    value = market.get("outcome_prices") or market.get("outcomePrices")
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            value = []
    if not isinstance(value, Sequence):
        return []
    prices = []
    for item in value:
        parsed = _number(item)
        if parsed is not None:
            prices.append(parsed)
    return prices


def _nested_number(mapping: Any, keys: Sequence[str]) -> float | None:
    if not isinstance(mapping, Mapping):
        return None
    for key in keys:
        parsed = _number(mapping.get(key))
        if parsed is not None:
            return parsed
    for value in mapping.values():
        if isinstance(value, Mapping):
            parsed = _nested_number(value, keys)
            if parsed is not None:
                return parsed
    return None


def extract_quote(
    market: Mapping[str, Any],
    context: Mapping[str, Any] | None,
    synthetic_spread: float,
) -> Quote:
    return QuoteExtractor(synthetic_spread=synthetic_spread).extract(market, context)


class ContextSafeguardPolicy:
    """Evaluate Simmer context without allowing unknown live safety state."""

    _BLOCKING_ACTIONS = ("skip", "hold", "avoid", "do not trade", "block")

    def __init__(self, *, max_slippage: float, require_context: bool) -> None:
        """Initialize context requirements.

        Args:
            max_slippage: Maximum estimated execution slippage.
            require_context: Whether missing context must block execution.
        """
        self._max_slippage = max_slippage
        self._require_context = require_context

    def evaluate(self, context: Mapping[str, Any] | None) -> tuple[bool, str]:
        """Return whether a candidate passes SDK context safeguards.

        Args:
            context: Context payload returned by Simmer.

        Returns:
            ``(allowed, reason)`` with a stable human-readable block reason.
        """
        if not context:
            if self._require_context:
                return False, "market context unavailable"
            return True, ""

        warnings = context.get("warnings", [])
        if not isinstance(warnings, Sequence) or isinstance(warnings, str):
            warnings = [warnings]
        warning_text = " ".join(str(item).upper() for item in warnings)
        if "MARKET RESOLVED" in warning_text or "MARKET CLOSED" in warning_text:
            return False, "market is closed"
        if any(term in warning_text for term in ("CONFLICT", "ALREADY HOLD")):
            return False, "market context reports a conflict"

        positions = context.get("positions", {})
        if isinstance(positions, Mapping):
            venue_position = positions.get("polymarket")
            if isinstance(venue_position, Mapping) and venue_position.get(
                "has_position"
            ):
                return False, "existing Polymarket position in this market"

        discipline = context.get("discipline", {})
        if isinstance(discipline, Mapping):
            if str(discipline.get("warning_level", "")).lower() == "severe":
                return False, "severe flip-flop warning"
            if self._blocking_recommendation(discipline):
                return False, "discipline recommends skipping the trade"

        edge = context.get("edge", {})
        if isinstance(edge, Mapping) and self._blocking_recommendation(edge):
            return False, "edge analysis recommends skipping the trade"

        slippage = _nested_number(
            context,
            ("slippage_pct", "estimated_slippage", "slippage"),
        )
        if slippage is not None and slippage > self._max_slippage:
            return False, f"slippage {slippage:.1%} exceeds limit"
        return True, ""

    @classmethod
    def _blocking_recommendation(cls, container: Mapping[str, Any]) -> bool:
        for key in ("recommendation", "recommended_action", "action", "decision"):
            value = str(container.get(key) or "").lower()
            if any(term in value for term in cls._BLOCKING_ACTIONS):
                return True
        return False


def check_context(
    context: Mapping[str, Any] | None,
    max_slippage: float,
) -> tuple[bool, str]:
    """Evaluate optional context for compatibility callers.

    Args:
        context: Simmer context payload, when available.
        max_slippage: Maximum accepted execution slippage.

    Returns:
        ``(allowed, reason)`` for a context-optional check.
    """
    return ContextSafeguardPolicy(
        max_slippage=max_slippage,
        require_context=False,
    ).evaluate(context)


def portfolio_balance(portfolio: Any, fallback: float) -> float:
    if isinstance(portfolio, Mapping):
        for key in ("balance_usdc", "available_balance", "cash_balance", "balance"):
            value = _number(portfolio.get(key))
            if value is not None and value >= 0:
                return value
    return fallback


def strategy_config(config: Mapping[str, Any]) -> StrategyConfig:
    keys = StrategyConfig.__dataclass_fields__.keys()
    return StrategyConfig(**{key: config[key] for key in keys})


@dataclass(frozen=True)
class LivePreflightDecision:
    """Represent one fail-closed SDK readiness decision."""

    allowed: bool
    reason: str = ""
    terminal_error: bool = False
    client_preflight_id: str | None = None


class LivePreflightChecker(Protocol):
    """Define the narrow live-readiness boundary used by orchestration."""

    def check(
        self,
        client: Any,
        *,
        planned_amount: float,
        exposure_cap_usd: float,
    ) -> LivePreflightDecision:
        """Return whether one planned Polymarket trade is ready."""
        ...


class SdkLivePreflightChecker:
    """Validate one planned order through the pinned Simmer SDK contract."""

    def check(
        self,
        client: Any,
        *,
        planned_amount: float,
        exposure_cap_usd: float,
    ) -> LivePreflightDecision:
        """Call Simmer preflight and reject blockers or malformed responses.

        Args:
            client: Mode-scoped mutable Simmer client.
            planned_amount: Final bounded order size in USDC.
            exposure_cap_usd: Conservative cross-venue exposure cap.

        Returns:
            A decision that distinguishes normal blockers from boundary errors.
        """
        try:
            result = client.preflight(
                venue="polymarket",
                planned_amount=planned_amount,
                exposure_cap_usd=exposure_cap_usd,
            )
        except Exception:
            return LivePreflightDecision(
                allowed=False,
                reason="Simmer Polymarket preflight call failed",
                terminal_error=True,
            )

        resolved_venue = getattr(result, "resolved_venue", None)
        if (
            not isinstance(resolved_venue, str)
            or resolved_venue.strip().lower() != "polymarket"
        ):
            return LivePreflightDecision(
                allowed=False,
                reason="Simmer preflight did not resolve to Polymarket",
                terminal_error=True,
            )

        ok_to_trade = getattr(result, "ok_to_trade", None)
        blockers_value = getattr(result, "blockers", None)
        if not isinstance(ok_to_trade, bool) or not isinstance(blockers_value, list):
            return LivePreflightDecision(
                allowed=False,
                reason="Simmer Polymarket preflight returned an invalid result",
                terminal_error=True,
            )

        blockers = tuple(str(blocker) for blocker in blockers_value)
        if blockers or not ok_to_trade:
            detail = ", ".join(blockers) if blockers else "UNSPECIFIED_BLOCKER"
            return LivePreflightDecision(
                allowed=False,
                reason=f"Simmer Polymarket preflight blocked: {detail}",
            )

        spendable_balance_value = getattr(result, "spendable_balance", None)
        if (
            isinstance(spendable_balance_value, bool)
            or not isinstance(spendable_balance_value, (int, float))
            or not math.isfinite(float(spendable_balance_value))
        ):
            return LivePreflightDecision(
                allowed=False,
                reason=(
                    "Simmer Polymarket preflight returned no finite spendable balance"
                ),
                terminal_error=True,
            )
        if float(spendable_balance_value) < planned_amount:
            return LivePreflightDecision(
                allowed=False,
                reason="Simmer Polymarket preflight blocked: INSUFFICIENT_BALANCE",
            )

        client_preflight_id = getattr(result, "client_preflight_id", None)
        if not isinstance(client_preflight_id, str) or not client_preflight_id.strip():
            return LivePreflightDecision(
                allowed=False,
                reason="Simmer Polymarket preflight returned no client_preflight_id",
                terminal_error=True,
            )
        return LivePreflightDecision(
            allowed=True,
            client_preflight_id=client_preflight_id.strip(),
        )


class TradeExecutor:
    """Submit one bounded order and classify confirmation uncertainty."""

    _CONFIRMED_FAILURE_STATES = frozenset(
        {
            "rejected",
            "failed",
            "cancelled",
            "canceled",
            "expired",
            "not_submitted",
            "skipped",
        }
    )

    def execute(
        self,
        client: Any,
        *,
        live: bool,
        market_id: str,
        side: str,
        amount: float,
        price: float,
        order_type: str,
        reasoning: str,
    ) -> dict[str, Any]:
        """Return a structured confirmed, rejected, or ambiguous outcome.

        Args:
            client: Mode-scoped Simmer client.
            live: Whether this request targets real execution.
            market_id: Runtime-discovered market identifier.
            side: YES or NO side.
            amount: Dollar amount reserved for this attempt.
            price: Bounded executable limit price.
            order_type: Simmer order type.
            reasoning: Public, secret-free execution rationale.

        Returns:
            Structured result containing an explicit ``ambiguous`` flag.
        """
        client_live = getattr(client, "live", live)
        if bool(client_live) != live:
            return {
                "success": False,
                "ambiguous": False,
                "error": "Simmer client execution mode does not match the request",
            }

        kwargs = {
            "market_id": market_id,
            "side": side,
            "amount": amount,
            "source": TRADE_SOURCE,
            "reasoning": reasoning,
            "skill_slug": SKILL_SLUG,
            "order_type": order_type,
        }
        if live:
            kwargs["venue"] = "polymarket"
        if order_type.upper() in {"GTC", "GTD", "FOK", "FAK"}:
            kwargs["price"] = price
        try:
            sdk_result = client.trade(**kwargs)
        except Exception as exc:
            return {
                "success": False,
                "ambiguous": True,
                "error": str(exc),
            }

        result = {
            "success": bool(getattr(sdk_result, "success", False)),
            "simulated": bool(getattr(sdk_result, "simulated", False)),
            "trade_id": getattr(sdk_result, "trade_id", None),
            "order_id": getattr(sdk_result, "order_id", None),
            "fill_status": getattr(sdk_result, "fill_status", None),
            "skip_reason": getattr(sdk_result, "skip_reason", None),
            "error": getattr(sdk_result, "error", None),
            "error_code": getattr(sdk_result, "error_code", None),
            "error_hint": getattr(sdk_result, "error_hint", None),
        }
        if result["success"] and result["simulated"] != (not live):
            result["success"] = False
            result["ambiguous"] = True
            result["error"] = "Simmer result execution mode does not match the request"
            return result
        result["ambiguous"] = self._is_ambiguous_failure(result)
        return result

    def _is_ambiguous_failure(self, result: Mapping[str, Any]) -> bool:
        if result.get("success"):
            return False
        if result.get("trade_id") or result.get("order_id"):
            return True
        fill_status = str(result.get("fill_status") or "").strip().lower()
        if fill_status in self._CONFIRMED_FAILURE_STATES:
            return False
        if result.get("skip_reason") and fill_status in {
            "",
            "unknown",
            "not_submitted",
            "skipped",
        }:
            return False
        return True


def execute_trade(
    client: Any,
    *,
    live: bool,
    market_id: str,
    side: str,
    amount: float,
    price: float,
    order_type: str,
    reasoning: str,
) -> dict[str, Any]:
    """Delegate one order to the class-based execution adapter.

    Args:
        client: Mode-scoped Simmer client.
        live: Whether this request targets real execution.
        market_id: Runtime-discovered market identifier.
        side: YES or NO side.
        amount: Dollar amount reserved for this attempt.
        price: Bounded executable limit price.
        order_type: Simmer order type.
        reasoning: Public, secret-free execution rationale.

    Returns:
        Structured result with confirmation uncertainty classified.
    """
    return TradeExecutor().execute(
        client,
        live=live,
        market_id=market_id,
        side=side,
        amount=amount,
        price=price,
        order_type=order_type,
        reasoning=reasoning,
    )


class AutomatonReporter:
    """Emit the single JSON record consumed by managed Simmer runs."""

    def __init__(self, *, enabled: bool, writer: Callable[[str], None] = print) -> None:
        """Initialize a managed-run reporter.

        Args:
            enabled: Whether the process is managed by Automaton.
            writer: Injectable line writer for deterministic tests.
        """
        self._enabled = enabled
        self._writer = writer
        self._emitted = False

    def emit(self, report: Mapping[str, Any]) -> None:
        """Emit at most one structured report line.

        Args:
            report: Internal strategy counters and optional failure details.
        """
        if not self._enabled or self._emitted:
            return
        payload: dict[str, Any] = {
            "signals": int(report.get("signals_found", report.get("signals", 0))),
            "trades_attempted": int(report.get("trades_attempted", 0)),
            "trades_executed": int(report.get("trades_executed", 0)),
        }
        skip_reason = report.get("skip_reason")
        if not skip_reason and payload["signals"] == 0:
            skip_reason = "no_signal"
        if skip_reason:
            payload["skip_reason"] = str(skip_reason)

        errors = report.get("execution_errors")
        if isinstance(errors, Sequence) and not isinstance(errors, (str, bytes)):
            normalized_errors = [str(error) for error in errors if error]
        else:
            normalized_errors = []
        if (
            not normalized_errors
            and report.get("status") == "error"
            and report.get("message")
        ):
            normalized_errors = [str(report["message"])]
        if normalized_errors:
            payload["execution_errors"] = normalized_errors

        self._writer(
            json.dumps(
                {"automaton": payload},
                separators=(",", ":"),
                sort_keys=True,
            )
        )
        self._emitted = True


def emit_automaton_report(report: Mapping[str, Any]) -> None:
    """Emit a managed Automaton report through the class-based adapter.

    Args:
        report: Internal strategy counters and optional failure details.
    """
    AutomatonReporter(
        enabled=bool(os.environ.get("AUTOMATON_MANAGED")),
    ).emit(report)


class PositionPresenter:
    """Render SDK position dataclasses without exposing unrelated fields."""

    def __init__(self, *, writer: Callable[[str], None] = print) -> None:
        """Initialize the position view.

        Args:
            writer: Injectable line writer for deterministic tests.
        """
        self._writer = writer

    def show(self, client: Any) -> bool:
        """Fetch and render current positions.

        Args:
            client: Simmer client or deterministic fake.

        Returns:
            ``True`` when the read succeeded, otherwise ``False``.
        """
        try:
            positions = client.get_positions(
                venue=getattr(client, "venue", "polymarket")
            )
        except Exception as exc:
            self._writer(f"Could not fetch positions: {exc}")
            return False
        if not positions:
            self._writer("No open positions.")
            return True
        for position in positions:
            if is_dataclass(position) and not isinstance(position, type):
                values = asdict(position)
            elif isinstance(position, Mapping):
                values = dict(position)
            else:
                values = {
                    "question": getattr(position, "question", None),
                    "market_id": getattr(position, "market_id", None),
                    "shares_yes": getattr(position, "shares_yes", 0),
                    "shares_no": getattr(position, "shares_no", 0),
                }
            market = (
                values.get("question") or values.get("market_id") or "unknown market"
            )
            legs = []
            for side, raw_shares in (
                ("YES", values.get("shares_yes", 0)),
                ("NO", values.get("shares_no", 0)),
            ):
                shares = _number(raw_shares) or 0.0
                if shares:
                    legs.append(f"{side} {shares:g} shares")
            self._writer(f"{market}: {', '.join(legs) if legs else '0 shares'}")
        return True


def show_positions(client: Any) -> bool:
    """Render current positions through the class-based presenter.

    Args:
        client: Simmer client or deterministic fake.

    Returns:
        ``True`` when the read succeeded, otherwise ``False``.
    """
    return PositionPresenter().show(client)


class LiveAccountActivityClient(Protocol):
    """Expose only the read APIs needed to prove an account is clean."""

    def get_positions(self, *, venue: str) -> Any:
        """Return current positions for one venue."""

    def get_trades(
        self,
        *,
        venue: str,
        since: str,
        include_failed: bool,
        limit: int,
        offset: int,
    ) -> Any:
        """Return recent trade receipts for one venue."""


class LiveAccountActivityProbe:
    """Prove that no live account activity can survive a ledger reset."""

    _LOOKBACK = timedelta(hours=96)

    def __init__(self, clock: Callable[[], datetime] | None = None) -> None:
        """Initialize the aware UTC clock used for the receipt window.

        Args:
            clock: Injectable aware timestamp source.
        """
        self._clock = clock or (lambda: datetime.now(timezone.utc))

    def assert_clean(self, client: LiveAccountActivityClient) -> None:
        """Raise unless read-only evidence proves the account is empty.

        Args:
            client: SDK read-only client.

        Raises:
            RuntimeError: If activity exists or the proof is unavailable.
        """
        now = self._clock()
        if not isinstance(now, datetime) or now.tzinfo is None:
            raise RuntimeError(
                "Live-state initialization clock must be an aware timestamp"
            )
        try:
            positions = client.get_positions(venue="polymarket")
        except Exception as exc:
            raise RuntimeError(
                "Cannot prove that open Polymarket positions are absent"
            ) from exc
        if not isinstance(positions, list):
            raise RuntimeError("Polymarket positions response is invalid")
        if positions:
            raise RuntimeError(
                "open Polymarket positions prevent live-state initialization"
            )

        since = (
            (now.astimezone(timezone.utc) - self._LOOKBACK)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z")
        )
        try:
            history = client.get_trades(
                venue="polymarket",
                since=since,
                include_failed=True,
                limit=200,
                offset=0,
            )
        except Exception as exc:
            raise RuntimeError(
                "Cannot prove that recent Polymarket trade receipts are absent"
            ) from exc
        if not isinstance(history, Mapping):
            raise RuntimeError("Polymarket trade history response is invalid")
        trades = history.get("trades")
        total_count = history.get("total_count")
        if (
            not isinstance(trades, list)
            or isinstance(total_count, bool)
            or not isinstance(total_count, int)
            or total_count < 0
            or total_count != len(trades)
        ):
            raise RuntimeError("Polymarket trade history response is invalid")
        if trades:
            raise RuntimeError(
                "recent Polymarket trade receipts prevent live-state initialization"
            )


@dataclass(frozen=True)
class LiveStateInitializationResult:
    """Describe whether explicit live-state initialization created a ledger."""

    state: DailyTradeState
    created: bool


class LiveStateInitializer:
    """Create an empty live ledger only after read-only reconciliation."""

    def __init__(
        self,
        *,
        state_store: TradeStateStore,
        activity_probe: LiveAccountActivityProbe | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        """Initialize durable state and read-only audit collaborators.

        Args:
            state_store: Central risk-ledger repository.
            activity_probe: Optional account-evidence policy.
            clock: Injectable clock used when constructing the default probe.
        """
        self._state_store = state_store
        self._activity_probe = activity_probe or LiveAccountActivityProbe(clock)

    def initialize(
        self,
        client: LiveAccountActivityClient,
    ) -> LiveStateInitializationResult:
        """Load existing state or safely create the first empty ledger.

        Args:
            client: SDK read-only live account client.

        Returns:
            Existing or newly created live-state result.
        """
        with self._state_store.execution_lock(live=True):
            try:
                state = self._state_store.load(live=True)
            except UninitializedTradeStateError:
                self._activity_probe.assert_clean(client)
                state = self._state_store.initialize_empty()
                return LiveStateInitializationResult(state=state, created=True)
            return LiveStateInitializationResult(state=state, created=False)


def initialize_live_state(
    client: LiveAccountActivityClient,
) -> LiveStateInitializationResult:
    """Delegate explicit initialization to the class-based service.

    Args:
        client: SDK read-only live account client.

    Returns:
        Existing or newly created state result.
    """
    resolver = StatePathResolver()
    state_store = TradeStateStore(
        resolver.resolve(),
        legacy_path=resolver.legacy_path(),
    )
    return LiveStateInitializer(state_store=state_store).initialize(client)


class StrategyRunner:
    """Orchestrate one paper or live cycle through injected adapters."""

    def __init__(
        self,
        *,
        client_provider: Callable[..., Any] | None = None,
        games_provider: Callable[[], list[LiveGame]] | None = None,
        signal_builder: Callable[..., GameSignal | None] | None = None,
        market_provider: Callable[[Any, str], list[dict[str, Any]]] | None = None,
        state_store: TradeStateStore | None = None,
        quote_clock: Callable[[], float] | None = None,
        signal_freshness_policy: SignalFreshnessPolicy | None = None,
        trade_executor: TradeExecutor | None = None,
        position_sizer: SdkPositionSizer | None = None,
        live_preflight_checker: LivePreflightChecker | None = None,
    ) -> None:
        """Initialize deterministic application-layer dependencies.

        Args:
            client_provider: Mode-scoped Simmer client provider.
            games_provider: ESPN live-game provider.
            signal_builder: ESPN probability signal builder.
            market_provider: Simmer market discovery adapter.
            state_store: Persistent live risk-state adapter.
            quote_clock: Monotonic clock for snapshot aging.
            signal_freshness_policy: Hard total-age policy for ESPN evidence.
            trade_executor: Classified Simmer execution adapter.
            position_sizer: Simmer SDK position-sizing adapter.
            live_preflight_checker: Fail-closed Simmer readiness adapter.
        """
        self._client_provider = client_provider or get_client
        self._games_provider = games_provider or fetch_live_games
        self._signal_builder = signal_builder or build_game_signal
        self._market_provider = market_provider or fetch_markets
        if state_store is not None:
            self._state_store = state_store
        else:
            state_path_resolver = StatePathResolver()
            self._state_store = TradeStateStore(
                state_path_resolver.resolve(),
                legacy_path=state_path_resolver.legacy_path(),
            )
        self._quote_clock = quote_clock or time.monotonic
        self._signal_freshness_policy = (
            signal_freshness_policy or SignalFreshnessPolicy(self._quote_clock)
        )
        self._trade_executor = trade_executor or TradeExecutor()
        self._position_sizer = position_sizer or SdkPositionSizer()
        self._live_preflight_checker = (
            live_preflight_checker or SdkLivePreflightChecker()
        )

    def run(
        self,
        *,
        live: bool,
        quiet: bool,
        use_context: bool,
        config: Mapping[str, Any],
    ) -> dict[str, Any]:
        """Run one cycle while holding the whole-run live-state lock.

        Args:
            live: Whether real execution is explicitly enabled.
            quiet: Whether informational output is suppressed.
            use_context: Whether context checks are requested in paper mode.
            config: Validated runtime configuration.

        Returns:
            Structured counters for CLI and Automaton reporting.
        """
        with self._state_store.execution_lock(live=live):
            return self._run_unlocked(
                live=live,
                quiet=quiet,
                use_context=use_context,
                config=config,
            )

    def _run_unlocked(
        self,
        *,
        live: bool,
        quiet: bool,
        use_context: bool,
        config: Mapping[str, Any],
    ) -> dict[str, Any]:
        mode = "live" if live else "paper"
        report: dict[str, Any] = {
            "status": "ok",
            "mode": mode,
            "signals_found": 0,
            "candidates_found": 0,
            "trades_attempted": 0,
            "trades_executed": 0,
            "errors": 0,
            "execution_errors": [],
        }
        print(f"MLB Live Trader — {mode} mode")
        if not live:
            print(
                "Paper mode is the default. Nothing here touches the live state file."
            )

        state = self._state_store.load(live=live)
        client = self._client_provider(live=live)
        if bool(getattr(client, "live", live)) != live:
            raise RuntimeError("Simmer client execution mode does not match the run")

        try:
            portfolio = client.get_portfolio()
        except Exception:
            portfolio = None
        bankroll = portfolio_balance(
            portfolio,
            float(config["paper_bankroll_usd"]) if not live else 0.0,
        )
        if not live and bankroll <= 0:
            bankroll = float(config["paper_bankroll_usd"])
        if bankroll <= 0:
            raise RuntimeError("No available bankroll reported by Simmer")

        signals = self._collect_signals(
            live=live,
            quiet=quiet,
            config=config,
            report=report,
        )
        report["signals_found"] = len(signals)
        if not signals:
            report["skip_reason"] = "no_signal"
            if not quiet:
                print("No live MLB games with a usable probability.")
            return report

        quote_policy = QuotePolicy(
            max_spread=float(
                config["max_spread_live"] if live else config["max_spread_paper"]
            ),
            max_age_seconds=float(config["max_quote_age_seconds"]),
            require_age=live,
            clock=self._quote_clock,
        )
        markets = self._market_provider(client, str(config["market_query"]))
        if not markets:
            report["skip_reason"] = "no_market"
            if not quiet:
                print("No active MLB markets found through Simmer.")
            return report

        seen_this_run: set[str] = set()
        games_traded_this_run: set[str] = set()
        strategy = strategy_config(config)
        context_reader = MarketContextReader(client)
        timing_policy = MarketTimingPolicy()
        context_policy = ContextSafeguardPolicy(
            max_slippage=float(config["context_max_slippage"]),
            require_context=live,
        )
        skip_reasons: list[str] = []
        context_enabled = use_context or live

        for signal in signals:
            if self._run_limit_reached(report, config):
                break
            if not source_allowed(
                signal.source,
                mode,
                allow_score_live=bool(config["allow_score_fallback_live"]),
            ):
                continue

            game = signal.game
            for market in markets:
                if self._run_limit_reached(report, config):
                    break
                market_id = str(market.get("id") or market.get("market_id") or "")
                if not market_id or market_id in seen_this_run:
                    continue

                yes_team = infer_yes_team(market, game.home_team, game.away_team)
                if yes_team is None:
                    continue
                if live:
                    timing_rejection = timing_policy.rejection_reason(market, game)
                    if timing_rejection is not None:
                        skip_reasons.append(timing_rejection)
                        continue
                fair_yes = fair_probability_for_team(
                    signal.home_probability,
                    yes_team,
                    game.home_team,
                    game.away_team,
                )
                if fair_yes is None:
                    continue
                seen_this_run.add(market_id)

                if live:
                    state = self._state_store.refresh(state, live=True)
                    if self._blocked_by_live_state(
                        state=state,
                        market_id=market_id,
                        game_id=game.game_id,
                        games_traded_this_run=games_traded_this_run,
                        config=config,
                    ):
                        continue

                context = None
                if context_enabled:
                    try:
                        context = context_reader.get(
                            market_id,
                            fair_yes_probability=fair_yes,
                        )
                    except Exception as exc:
                        if live:
                            report["errors"] += 1
                            skip_reasons.append("market context unavailable")
                            if not quiet:
                                print(
                                    f"Skip {yes_team}: market context unavailable "
                                    f"({exc})"
                                )
                            continue
                    allowed, reason = context_policy.evaluate(context)
                    if not allowed:
                        skip_reasons.append(reason)
                        if not quiet:
                            print(f"Skip {yes_team}: {reason}")
                        continue

                quote = extract_quote(
                    market,
                    context,
                    float(config["synthetic_spread"]),
                )
                quote_rejection = quote_policy.rejection_reason(quote)
                if quote_rejection is not None:
                    skip_reasons.append(quote_rejection)
                    if not quiet:
                        print(f"Skip {yes_team}: {quote_rejection}")
                    continue

                signal_age = self._signal_freshness_policy.current_age(
                    signal,
                    live=live,
                    max_age_seconds=float(config["max_signal_age_seconds"]),
                )
                if signal_age is None:
                    skip_reasons.append("signal became stale before execution")
                    continue

                decision = select_trade(
                    fair_yes_probability=fair_yes,
                    yes_ask=quote.yes_ask,
                    no_ask=quote.no_ask,
                    mode=mode,
                    inning=game.inning,
                    source=signal.source,
                    age_seconds=signal_age,
                    spread=quote.spread,
                    fee_bps=quote.fee_bps,
                    config=strategy,
                )
                if decision is None:
                    continue
                report["candidates_found"] += 1

                minimum = max(
                    float(config["min_trade_usd"]),
                    MIN_SHARES_PER_ORDER * decision.price,
                )
                amount = self._position_sizer.size(
                    PositionSizingRequest(
                        bankroll=bankroll,
                        fair_probability=decision.fair_probability,
                        market_price=decision.price,
                        method=str(config["position_sizing"]),
                        kelly_multiplier=float(config["kelly_multiplier"]),
                        min_ev=float(config["min_ev"]),
                        max_position_usd=float(config["max_position_usd"]),
                        max_bankroll_fraction=float(config["max_bankroll_fraction"]),
                        min_trade_usd=float(config["min_trade_usd"]),
                    )
                )
                if amount <= 0:
                    skip_reasons.append("position below venue minimum or sizing gate")
                    continue

                final_quote_rejection = quote_policy.rejection_reason(quote)
                if final_quote_rejection is not None:
                    skip_reasons.append(final_quote_rejection)
                    continue

                client_preflight_id: str | None = None
                if live:
                    if (
                        self._signal_freshness_policy.current_age(
                            signal,
                            live=True,
                            max_age_seconds=float(config["max_signal_age_seconds"]),
                        )
                        is None
                    ):
                        skip_reasons.append("signal became stale before execution")
                        continue
                    state = self._state_store.refresh(state, live=True)
                    if self._blocked_by_live_state(
                        state=state,
                        market_id=market_id,
                        game_id=game.game_id,
                        games_traded_this_run=games_traded_this_run,
                        config=config,
                    ):
                        continue
                    remaining = float(config["live_daily_budget_usd"]) - state.spent_usd
                    amount = min(amount, max(0.0, remaining))
                    if amount < minimum:
                        continue
                    preflight = self._live_preflight_checker.check(
                        client,
                        planned_amount=amount,
                        exposure_cap_usd=float(config["live_daily_budget_usd"]),
                    )
                    if not preflight.allowed:
                        skip_reasons.append(preflight.reason)
                        report["skip_reason"] = preflight.reason
                        if preflight.terminal_error:
                            report["status"] = "error"
                            report["errors"] += 1
                            report["execution_errors"].append(preflight.reason)
                        return report
                    client_preflight_id = preflight.client_preflight_id
                    state = self._state_store.reserve_trade(
                        state,
                        live=True,
                        market_id=market_id,
                        game_id=game.game_id,
                        amount_usd=amount,
                        game_resolves_at=str(market.get("resolves_at") or "") or None,
                    )

                    post_reservation_reason = quote_policy.rejection_reason(quote)
                    if post_reservation_reason is None and (
                        self._signal_freshness_policy.current_age(
                            signal,
                            live=True,
                            max_age_seconds=float(config["max_signal_age_seconds"]),
                        )
                        is None
                    ):
                        post_reservation_reason = "signal became stale before execution"
                    if post_reservation_reason is not None:
                        state = self._state_store.release_trade(
                            state,
                            live=True,
                            market_id=market_id,
                            game_id=game.game_id,
                            amount_usd=amount,
                        )
                        skip_reasons.append(post_reservation_reason)
                        continue

                reasoning = (
                    f"ESPN {decision.fair_probability:.1%}, "
                    f"ask {decision.price:.1%}, "
                    f"net edge {decision.net_edge:.1%}, inning {game.inning}, "
                    f"source {signal.source}"
                )
                if client_preflight_id is not None:
                    reasoning = (
                        f"{reasoning}, client_preflight_id={client_preflight_id}"
                    )
                result = self._trade_executor.execute(
                    client,
                    live=live,
                    market_id=market_id,
                    side=decision.side,
                    amount=amount,
                    price=decision.price,
                    order_type=str(config["order_type"]).upper(),
                    reasoning=reasoning,
                )
                report["trades_attempted"] += 1
                if not result.get("success"):
                    report["errors"] += 1
                    self._record_execution_error(result, report, skip_reasons)
                    if result.get("ambiguous"):
                        report["status"] = "ambiguous"
                        report["skip_reason"] = (
                            "ambiguous submission; reconcile orders and positions "
                            "before rerunning"
                        )
                        if not quiet:
                            print(
                                f"Trade status is ambiguous for {yes_team}; "
                                "stopping for reconciliation."
                            )
                        return report
                    if live:
                        state = self._state_store.release_trade(
                            state,
                            live=True,
                            market_id=market_id,
                            game_id=game.game_id,
                            amount_usd=amount,
                        )
                    if not quiet:
                        print(
                            f"Trade failed for {yes_team}: "
                            f"{result.get('error') or 'confirmed rejection'}"
                        )
                    continue

                report["trades_executed"] += 1
                games_traded_this_run.add(game.game_id)
                print(
                    f"{mode.upper()} {decision.side.upper()} {yes_team} — "
                    f"${amount:.2f} at {decision.price:.3f}; "
                    f"net edge {decision.net_edge:.1%}"
                )
                break

        if skip_reasons:
            report["skip_reason"] = ", ".join(dict.fromkeys(skip_reasons))
        elif report["trades_executed"] == 0:
            report["skip_reason"] = "no_candidate"
        if not quiet:
            print(
                f"Done: {report['signals_found']} signals, "
                f"{report['candidates_found']} candidates, "
                f"{report['trades_executed']} trades."
            )
        return report

    def _collect_signals(
        self,
        *,
        live: bool,
        quiet: bool,
        config: Mapping[str, Any],
        report: dict[str, Any],
    ) -> list[GameSignal]:
        """Collect valid ESPN signals while isolating per-game failures."""
        signals: list[GameSignal] = []
        for game in self._games_provider():
            try:
                signal = self._signal_builder(game, config, live=live)
            except Exception as exc:
                report["errors"] += 1
                if not quiet:
                    print(
                        f"{game.away_team} at {game.home_team}: "
                        f"ESPN lookup failed: {exc}"
                    )
                continue
            if signal is not None:
                signals.append(signal)
        return signals

    @staticmethod
    def _run_limit_reached(
        report: Mapping[str, Any], config: Mapping[str, Any]
    ) -> bool:
        """Return whether this cycle used its bounded submission allowance."""
        return int(report["trades_attempted"]) >= int(config["max_trades_per_run"])

    @staticmethod
    def _blocked_by_live_state(
        *,
        state: Any,
        market_id: str,
        game_id: str,
        games_traded_this_run: set[str],
        config: Mapping[str, Any],
    ) -> bool:
        """Return whether durable live counters prohibit this candidate."""
        return bool(
            market_id in state.market_ids
            or game_id in state.game_ids
            or game_id in games_traded_this_run
            or state.trades >= int(config["max_live_trades_per_day"])
            or state.spent_usd >= float(config["live_daily_budget_usd"])
        )

    @staticmethod
    def _record_execution_error(
        result: Mapping[str, Any],
        report: dict[str, Any],
        skip_reasons: list[str],
    ) -> None:
        """Normalize one failed SDK result into managed-run diagnostics."""
        skip_reason = result.get("skip_reason")
        if skip_reason:
            skip_reasons.append(str(skip_reason))
        error = result.get("error") or result.get("error_hint")
        if error:
            report["execution_errors"].append(str(error))


def run_strategy(
    *,
    live: bool,
    quiet: bool,
    use_context: bool,
    config: Mapping[str, Any],
) -> dict[str, Any]:
    """Delegate a strategy cycle to the class-based orchestrator.

    Args:
        live: Whether real execution is explicitly enabled.
        quiet: Whether informational output is suppressed.
        use_context: Whether SDK context safeguards are enabled in paper mode.
        config: Validated runtime configuration.

    Returns:
        Structured run counters for CLI and Automaton reporting.
    """
    return StrategyRunner().run(
        live=live,
        quiet=quiet,
        use_context=use_context,
        config=config,
    )


def print_config(config: Mapping[str, Any]) -> None:
    for key in sorted(config):
        print(f"{key}={config[key]}")


def parse_updates(items: Sequence[str]) -> dict[str, Any]:
    """Parse and validate user-supplied configuration overrides.

    Args:
        items: Sequence of ``KEY=VALUE`` strings.

    Returns:
        Validated typed configuration updates.

    Raises:
        ValueError: If an item, key, value, or sizing method is invalid.
    """
    updates: dict[str, Any] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"Expected KEY=VALUE, got: {item}")
        key, raw = item.split("=", 1)
        if key not in CONFIG_SCHEMA:
            raise ValueError(f"Unknown config key: {key}")
        updates[key] = _coerce(raw, CONFIG_SCHEMA[key]["type"])
    return RuntimeConfigValidator().validate(updates)


class TraderCli:
    """Coordinate CLI actions and guarantee one managed-run report."""

    def __init__(
        self,
        *,
        config_loader: Callable[[], dict[str, Any]] | None = None,
        mutable_client_provider: Callable[..., Any] | None = None,
        readonly_client_provider: Callable[..., Any] | None = None,
        strategy_runner: Callable[..., dict[str, Any]] | None = None,
        positions_presenter: Callable[[Any], bool] | None = None,
        live_state_initializer: Callable[
            [LiveAccountActivityClient], LiveStateInitializationResult
        ]
        | None = None,
        reporter: Callable[[Mapping[str, Any]], None] | None = None,
    ) -> None:
        """Initialize testable CLI dependencies.

        Args:
            config_loader: Validated Simmer configuration loader.
            mutable_client_provider: Trading client provider.
            readonly_client_provider: SDK-enforced read-only client provider.
            strategy_runner: Strategy orchestration entrypoint.
            positions_presenter: Read-only portfolio presenter.
            live_state_initializer: Explicit reconciled-ledger workflow.
            reporter: Managed Automaton report adapter.
        """
        self._config_loader = config_loader or load_runtime_config
        self._mutable_client_provider = mutable_client_provider or get_client
        self._readonly_client_provider = readonly_client_provider or get_readonly_client
        self._strategy_runner = strategy_runner or run_strategy
        self._positions_presenter = positions_presenter or show_positions
        self._live_state_initializer = live_state_initializer or initialize_live_state
        self._reporter = reporter or emit_automaton_report

    def run(self, argv: Sequence[str] | None = None) -> int:
        """Execute one CLI action and emit exactly one final report.

        Args:
            argv: Optional arguments excluding the executable name.

        Returns:
            Process-style exit code.
        """
        parser = self._build_parser()
        report = self._base_report(live=False)
        try:
            try:
                args = parser.parse_args(argv)
            except SystemExit as exc:
                exit_code = int(exc.code) if isinstance(exc.code, int) else 1
                if exit_code == 0:
                    report["skip_reason"] = "help_only"
                else:
                    report.update(
                        status="error",
                        errors=1,
                        message="Command-line argument parsing failed",
                        skip_reason="argument_error",
                    )
                return exit_code

            self._validate_initialization_action(args)
            if args.initialize_live_state:
                report["mode"] = "live"
                client = self._readonly_client_provider(live=True)
                result = self._live_state_initializer(client)
                report["skip_reason"] = (
                    "live_state_initialized"
                    if result.created
                    else "live_state_already_initialized"
                )
                print(
                    "Live state initialized."
                    if result.created
                    else "Live state was already initialized."
                )
                return 0

            live = bool(args.live)
            report["mode"] = "live" if live else "paper"
            if args.set:
                updates = parse_updates(args.set)
                repository = RuntimeConfigRepository()
                repository.save(updates)
                print(
                    "Saved: "
                    + ", ".join(f"{key}={value}" for key, value in updates.items())
                )
                print(f"Saved to: {repository.path()}")
                report["skip_reason"] = "config_updated"
                return 0

            if args.positions:
                client = self._readonly_client_provider(live=live)
                if not self._positions_presenter(client):
                    report.update(
                        status="error",
                        errors=1,
                        message="Could not fetch positions",
                        skip_reason="positions_unavailable",
                    )
                    return 1
                report["skip_reason"] = "positions_only"
                return 0

            config = self._config_loader()
            if args.config:
                print_config(config)
                report["skip_reason"] = "config_only"
                return 0

            report = self._strategy_runner(
                live=live,
                quiet=args.quiet,
                use_context=not args.no_context,
                config=config,
            )
            return 0 if report.get("status") == "ok" else 1
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
            report.update(
                status="error",
                errors=1,
                message=str(exc),
                skip_reason="runtime_error",
            )
            return 1
        finally:
            self._reporter(report)

    @staticmethod
    def _validate_initialization_action(args: argparse.Namespace) -> None:
        """Reject combinations that could blur a read-only state audit."""
        if not args.initialize_live_state:
            return
        if args.live or args.paper or args.positions or args.config or args.set:
            raise ValueError(
                "--initialize-live-state must be used alone after stopping prior "
                "live schedulers"
            )

    @staticmethod
    def _base_report(*, live: bool) -> dict[str, Any]:
        """Return complete zeroed counters for non-strategy CLI actions."""
        return {
            "status": "ok",
            "mode": "live" if live else "paper",
            "signals_found": 0,
            "candidates_found": 0,
            "trades_attempted": 0,
            "trades_executed": 0,
            "errors": 0,
        }

    @staticmethod
    def _build_parser() -> argparse.ArgumentParser:
        """Build the supported command-line contract."""
        parser = argparse.ArgumentParser(
            description=(
                "Trade live MLB markets through Simmer; paper mode is default."
            )
        )
        mode = parser.add_mutually_exclusive_group()
        mode.add_argument(
            "--paper",
            "--dry-run",
            dest="paper",
            action="store_true",
            help="Use simulated trades (default)",
        )
        mode.add_argument("--live", action="store_true", help="Place real trades")
        parser.add_argument(
            "--positions",
            action="store_true",
            help="Show positions through a read-only SDK client and exit",
        )
        parser.add_argument(
            "--initialize-live-state",
            action="store_true",
            help="Read-only account audit followed by one-time live-ledger setup",
        )
        parser.add_argument(
            "--config", action="store_true", help="Show resolved config and exit"
        )
        parser.add_argument(
            "--set",
            action="append",
            default=[],
            metavar="KEY=VALUE",
            help="Save a config override",
        )
        parser.add_argument(
            "--no-context",
            "--no-safeguards",
            dest="no_context",
            action="store_true",
            help="Skip optional context checks in paper mode",
        )
        parser.add_argument(
            "--quiet",
            "-q",
            action="store_true",
            help="Only print trades and errors",
        )
        return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Delegate process entry to the class-based CLI service.

    Args:
        argv: Optional arguments excluding the executable name.

    Returns:
        Process-style exit code.
    """
    return TraderCli().run(argv)


if __name__ == "__main__":
    raise SystemExit(main())
