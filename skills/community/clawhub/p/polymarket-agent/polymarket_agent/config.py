"""Skill configuration — local JSON file, no shell-out.

AUDIT FIX (Medium — "Dangerous Code Execution", 3 occurrences): v1.0.2 read and
wrote configuration by invoking `subprocess.run(["clawdbot", "config", ...])`
with user-supplied values, and printed the resulting stdout without
sanitization ("Unvalidated Output Injection", High). Here the config is a local
JSON read/written with the stdlib — zero subprocess, zero shell.

AUDIT FIX (Medium — "Context-Inappropriate Capabilities", 94%): v1.0.2 had
unrestricted access to the host's GLOBAL config (`clawdbot config set <any
path>`). Now only the keys declared in DEFAULTS exist, with validated types and
ranges.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, fields
from typing import Any, Dict

from .paths import config_path, write_private

# Fixed endpoints — never sourced from user config (prevents redirecting signed
# orders to an arbitrary host).
CLOB_HOST = "https://clob.polymarket.com"
GAMMA_API = "https://gamma-api.polymarket.com"
DATA_API = "https://data-api.polymarket.com"
POLYGON_CHAIN_ID = 137

HTTP_TIMEOUT = 15.0

#: Closed domains accepted by `/v1/leaderboard` (validated server-side; the API
#: returns 400 along with the list if anything falls outside).
LEADERBOARD_CATEGORIES = {
    "OVERALL", "POLITICS", "SPORTS", "ESPORTS", "CRYPTO", "CULTURE",
    "MENTIONS", "WEATHER", "ECONOMICS", "TECH", "FINANCE",
}
LEADERBOARD_PERIODS = {"DAY", "WEEK", "MONTH", "ALL"}


@dataclass
class Settings:
    """Risk limits and preferences. The defaults are conservative by design:
    the safe failure is NOT to trade."""

    # ── Financial guard-rails ──────────────────────────────────────────────
    max_position_usd: float = 25.0
    """Maximum notional (price × size) of a SINGLE order, in USDC."""

    max_bankroll_pct: float = 5.0
    """Maximum percentage of the balance a single order may consume."""

    max_daily_spend_usd: float = 100.0
    """Maximum sum of buys in a UTC day (sliding window over the journal)."""

    max_open_orders: int = 10
    """Cap on simultaneously open orders."""

    min_price: float = 0.01
    max_price: float = 0.99
    """Accepted price-per-share range (outside it the order is rejected)."""

    # ── Autonomy ───────────────────────────────────────────────────────────
    autonomous_mode: bool = False
    """When false (default), every order requires human confirmation."""

    autonomous_expires_at: float = 0.0
    """UTC epoch at which autonomous mode expires on its own. 0 = off."""

    dry_run: bool = True
    """When true, orders are validated and journaled but NOT sent."""

    # ── Wallet ─────────────────────────────────────────────────────────────
    signature_type: int = 0
    """0 = EOA (the key owns the funds).
    1 = email/magic proxy; 2 = Polymarket wallet proxy (browser).
    Anyone who deposited through the Polymarket interface usually needs 1 or 2."""

    funder_address: str = ""
    """Address that HOLDS the USDC when signature_type != 0."""

    # ── Analysis preferences ───────────────────────────────────────────────
    risk_profile: str = "balanced"  # conservative | balanced | aggressive
    interests: str = "Crypto,Politics"
    min_volume_usd: float = 10_000.0
    """Markets below this are flagged as illiquid."""


_NUMERIC_BOUNDS: Dict[str, tuple[float, float]] = {
    "max_position_usd": (0.0, 100_000.0),
    "max_bankroll_pct": (0.0, 100.0),
    "max_daily_spend_usd": (0.0, 1_000_000.0),
    "max_open_orders": (0, 1_000),
    "min_price": (0.001, 0.999),
    "max_price": (0.001, 0.999),
    "signature_type": (0, 2),
    "min_volume_usd": (0.0, 1_000_000_000.0),
    "autonomous_expires_at": (0.0, 4_102_444_800.0),  # up to year 2100
}

_ALLOWED_RISK_PROFILES = {"conservative", "balanced", "aggressive"}

# Every key that exists on disk. Used to READ and to LOAD.
KNOWN_KEYS = {f.name for f in fields(Settings)}

#: Fields `poly config` may NOT write.
#:
#: SECURITY FIX (found in review): `poly auto` gates autonomous mode behind
#: `--i-understand-the-risk`, clamps the expiry to 24h and journals the
#: decision — and none of that mattered, because the same two fields sat in
#: the generic setter. `poly config --key autonomous_mode --value true` plus
#: `--key autonomous_expires_at --value 4102444800` bought unsupervised
#: real-money trading until the year 2100, through a command that reads as
#: harmless housekeeping. That is exactly the shape a prompt injection takes:
#: SKILL.md tells the agent never to run `poly auto`, and says nothing about
#: `poly config`. The gate now lives on the field, not on one command.
LOCKED_KEYS = {"autonomous_mode", "autonomous_expires_at"}

# Keys the user may change via `poly config`. Secrets are deliberately left out
# — the private key only ever enters through the keystore.
EDITABLE_KEYS = KNOWN_KEYS - LOCKED_KEYS


class ConfigError(ValueError):
    """Value rejected by config validation."""


def _coerce(key: str, raw: Any) -> Any:
    """Convert and validate a value against the type declared in the dataclass."""
    if key not in KNOWN_KEYS:
        raise ConfigError(
            f"Unknown key: {key!r}. Use `poly config --list` to see the valid ones."
        )

    declared = {f.name: f.type for f in fields(Settings)}[key]
    text = str(raw).strip()

    if declared is bool or declared == "bool":
        lowered = text.lower()
        if lowered in {"true", "1", "yes", "y", "on"}:
            return True
        if lowered in {"false", "0", "no", "n", "off"}:
            return False
        raise ConfigError(f"{key}: expected a boolean, got {text!r}.")

    if declared in (int, float) or declared in ("int", "float"):
        try:
            value = float(text)
        except ValueError as exc:
            raise ConfigError(f"{key}: expected a number, got {text!r}.") from exc
        low, high = _NUMERIC_BOUNDS.get(key, (float("-inf"), float("inf")))
        if not (low <= value <= high):
            raise ConfigError(f"{key}: must be between {low} and {high}.")
        return int(value) if declared in (int, "int") else value

    # Strings — only closed-domain fields or fields with a known format.
    if key == "risk_profile":
        if text.lower() not in _ALLOWED_RISK_PROFILES:
            raise ConfigError(
                f"risk_profile: use one of {sorted(_ALLOWED_RISK_PROFILES)}."
            )
        return text.lower()

    if key == "funder_address":
        if text and not (text.startswith("0x") and len(text) == 42):
            raise ConfigError("funder_address: invalid EVM address (0x + 40 hex).")
        return text

    if key == "interests":
        # Comma-separated list, no control characters.
        parts = [p.strip() for p in text.split(",") if p.strip()]
        if any(len(p) > 40 for p in parts) or len(parts) > 20:
            raise ConfigError("interests: at most 20 items of up to 40 characters.")
        cleaned = [p for p in parts if p.isprintable()]
        return ",".join(cleaned)

    return text


def load_settings() -> Settings:
    """Read the config from disk. Invalid values fall back to the default
    (fail-safe)."""
    path = config_path()
    if not path.exists():
        return Settings()
    try:
        with open(path, encoding="utf-8") as fh:
            raw = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return Settings()
    if not isinstance(raw, dict):
        return Settings()

    settings = Settings()
    for key, value in raw.items():
        # KNOWN_KEYS, not EDITABLE_KEYS: a locked field is still legitimately
        # written by `poly auto`, so it has to load back from disk.
        if key not in KNOWN_KEYS:
            continue
        try:
            setattr(settings, key, _coerce(key, value))
        except ConfigError:
            continue  # keep the safe default
    # Invariant: coherent price range.
    if settings.min_price >= settings.max_price:
        settings.min_price, settings.max_price = Settings.min_price, Settings.max_price
    return settings


def save_settings(settings: Settings) -> None:
    write_private(config_path(), json.dumps(asdict(settings), indent=2))


def set_value(key: str, raw: Any) -> Any:
    """Validate and persist a key. Returns the value actually written."""
    if key in LOCKED_KEYS:
        raise ConfigError(
            f"{key} is not editable here: it decides whether real-money orders "
            "go out unattended. Use `poly auto true --hours N "
            "--i-understand-the-risk` (max 24h, journaled) or `poly auto false`."
        )
    settings = load_settings()
    value = _coerce(key, raw)
    setattr(settings, key, value)
    save_settings(settings)
    return value
