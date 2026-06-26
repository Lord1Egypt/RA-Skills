#!/usr/bin/env python3
"""Shared helpers for moomoo/futu OpenAPI scripts."""

from __future__ import annotations

import importlib
import math
import os
import re
from typing import Iterable

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 11111
DEFAULT_UNLOCK_ENV = "MOOMOO_UNLOCK_PASSWORD"
SUPPORTED_QUOTE_MARKETS = ("US", "HK", "SG", "JP", "SH", "SZ")
SUPPORTED_TRADE_MARKETS = ("US", "HK", "SG", "JP")
_TICKER_RE = re.compile(r"^(?P<market>[A-Z]{2,3})\.(?P<symbol>[A-Z0-9][A-Z0-9._-]*)$")


def load_openapi_module():
    """Load futu-api or moomoo-api lazily."""
    for module_name in ("futu", "moomoo"):
        try:
            return importlib.import_module(module_name), module_name
        except ImportError:
            continue

    raise ImportError(
        "Neither futu-api nor moomoo-api is installed. "
        "Run: pip install futu-api  or  pip install moomoo-api"
    )


def normalize_market_code(raw_value: str, allowed_markets: Iterable[str] | None = None) -> str:
    value = (raw_value or "").strip().upper()
    if not value:
        raise ValueError("Market code is required.")
    if allowed_markets and value not in set(allowed_markets):
        raise ValueError(
            f"Unsupported market '{value}'. Options: {', '.join(sorted(allowed_markets))}"
        )
    return value


def normalize_ticker(raw_value: str, allowed_markets: Iterable[str] | None = None) -> str:
    value = (raw_value or "").strip().upper()
    match = _TICKER_RE.match(value)
    if not match:
        raise ValueError(
            f"Invalid ticker '{raw_value}'. Use MARKET.CODE format like US.AAPL or HK.00700."
        )

    market = match.group("market")
    if allowed_markets and market not in set(allowed_markets):
        raise ValueError(
            f"Unsupported market '{market}' for ticker '{raw_value}'. "
            f"Options: {', '.join(sorted(allowed_markets))}"
        )
    return value


def parse_ticker_list(raw_values, allowed_markets: Iterable[str] | None = None) -> list[str]:
    tickers: list[str] = []
    seen: set[str] = set()

    for raw_value in raw_values:
        for candidate in str(raw_value).split(","):
            candidate = candidate.strip()
            if not candidate:
                continue
            ticker = normalize_ticker(candidate, allowed_markets=allowed_markets)
            if ticker not in seen:
                seen.add(ticker)
                tickers.append(ticker)

    if not tickers:
        raise ValueError("At least one ticker is required.")

    return tickers


def market_code_from_ticker(ticker: str) -> str:
    return normalize_ticker(ticker).split(".", 1)[0]


def get_trade_market(api, *, ticker: str | None = None, market_code: str | None = None):
    ticker_market = market_code_from_ticker(ticker) if ticker else None
    explicit_market = (
        normalize_market_code(market_code, SUPPORTED_TRADE_MARKETS)
        if market_code
        else None
    )

    if ticker_market and explicit_market and ticker_market != explicit_market:
        raise ValueError(
            f"Ticker market '{ticker_market}' does not match --market '{explicit_market}'."
        )

    resolved_market = explicit_market or ticker_market
    if not resolved_market:
        raise ValueError(
            "Trade market is required. Pass --market or provide a ticker with MARKET.CODE format."
        )

    try:
        return getattr(api.TrdMarket, resolved_market)
    except AttributeError as exc:
        raise ValueError(f"Trade market '{resolved_market}' is not supported by the SDK.") from exc


def ensure_positive_int(value: int, label: str):
    if value <= 0:
        raise ValueError(f"{label} must be greater than 0.")
    return value


def ensure_non_negative_int(value: int, label: str):
    if value < 0:
        raise ValueError(f"{label} must be 0 or greater.")
    return value


def ensure_positive_number(value: float, label: str):
    if value <= 0:
        raise ValueError(f"{label} must be greater than 0.")
    return value


def env_password(env_name: str) -> str:
    password = os.environ.get(env_name)
    if not password:
        raise ValueError(
            f"Environment variable {env_name} is not set. "
            "Live trading requires an unlock password so the account can be unlocked and re-locked."
        )
    return password


def format_value(value) -> str:
    if value is None:
        return "N/A"

    try:
        if math.isnan(value):
            return "N/A"
    except (TypeError, ValueError):
        pass

    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, float):
        return f"{value:,.4f}".rstrip("0").rstrip(".")
    return str(value)
