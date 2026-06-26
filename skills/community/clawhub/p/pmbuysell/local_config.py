"""
Self-contained config loader for the `pmbuysell.skills` package.

Design goal:
  - Skills should not import modules outside `pmbuysell/skills/`.
  - Read configuration from `pmbuysell/.env` (and optionally `pm/.env`) to keep UX consistent.

This module intentionally only implements what skills need (account parsing + redeem-related vars).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


_SKILLS_DIR = Path(__file__).resolve().parent            # .../pmbuysell/skills
_PMBUYSELL_DIR = _SKILLS_DIR.parent                      # .../pmbuysell
_PROJECT_DIR = _PMBUYSELL_DIR.parent                     # .../pm (project root for our usage)

_ENV_PATHS = [
    _PMBUYSELL_DIR / ".env",  # preferred
    _PROJECT_DIR / ".env",    # optional fallback (compatible with older layouts)
]

_ENV_LOADED = False
_ACCOUNTS_CACHE: dict[str, dict[str, str]] | None = None


def _ensure_env_loaded() -> None:
    global _ENV_LOADED
    if _ENV_LOADED:
        return
    for p in _ENV_PATHS:
        if p.exists():
            load_dotenv(dotenv_path=p, override=True)
    _ENV_LOADED = True


def _load_accounts_from_json(raw: str) -> dict[str, dict[str, str]]:
    raw = (raw or "").strip()
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}

    out: dict[str, dict[str, str]] = {}
    for k, v in data.items():
        if not isinstance(v, dict):
            continue
        pk = v.get("private_key")
        funder = v.get("funder")
        if not pk or not funder:
            continue
        out[str(k).strip().upper()] = {"private_key": str(pk).strip(), "funder": str(funder).strip()}
    return out


def _load_accounts_from_flat_env(ids_raw: str) -> dict[str, dict[str, str]]:
    ids_raw = (ids_raw or "").strip()
    if not ids_raw:
        return {}
    out: dict[str, dict[str, str]] = {}
    for raw_id in ids_raw.split(","):
        acc_id = raw_id.strip()
        if not acc_id:
            continue
        upper = acc_id.upper()
        pk = os.getenv(f"{upper}_PRIVATE_KEY") or os.getenv(f"{acc_id}_PRIVATE_KEY")
        funder = os.getenv(f"{upper}_FUNDER") or os.getenv(f"{acc_id}_FUNDER")
        if not pk or not funder:
            continue
        out[upper] = {"private_key": str(pk).strip(), "funder": str(funder).strip()}
    return out


def _get_accounts_cached() -> dict[str, dict[str, str]]:
    global _ACCOUNTS_CACHE
    if _ACCOUNTS_CACHE is not None:
        return _ACCOUNTS_CACHE

    _ensure_env_loaded()
    accounts = _load_accounts_from_json(os.getenv("PM_ACCOUNTS_JSON", ""))
    if not accounts:
        accounts = _load_accounts_from_flat_env(os.getenv("PM_ACCOUNT_IDS", ""))

    _ACCOUNTS_CACHE = accounts
    return accounts


def get_account(account_id: str) -> dict[str, str] | None:
    acc = (account_id or "").strip().upper()
    if not acc:
        return None
    return _get_accounts_cached().get(acc)


def list_account_ids() -> list[str]:
    return sorted(_get_accounts_cached().keys())


def get_relayer_settings() -> tuple[str | None, int]:
    """Returns (relayer_url, chain_id). chain_id defaults to CHAIN_ID (137) if not set."""
    _ensure_env_loaded()
    relayer_url = os.getenv("RELAYER_URL")
    chain_id_raw = os.getenv("CHAIN_ID")
    try:
        chain_id = int(str(chain_id_raw).strip()) if chain_id_raw and str(chain_id_raw).strip() else CHAIN_ID
    except Exception:
        chain_id = CHAIN_ID
    return (str(relayer_url).strip() if relayer_url and str(relayer_url).strip() else None), chain_id


def get_builder_api_creds_for_account(account_id: str) -> tuple[str | None, str | None, str | None]:
    _ensure_env_loaded()
    acc = (account_id or "").strip().upper()
    if not acc:
        return None, None, None
    k = os.getenv(f"{acc}_BUILDER_API_KEY")
    s = os.getenv(f"{acc}_BUILDER_SECRET")
    p = os.getenv(f"{acc}_BUILDER_PASSPHRASE")
    return (k.strip() if k else None), (s.strip() if s else None), (p.strip() if p else None)


# ========== CLOB / chain (for polymarket_client, multi_account) ==========


def _get_str(name: str, default: str | None = None) -> str | None:
    v = os.getenv(name)
    if v is None or str(v).strip() == "":
        return default
    return str(v).strip()


def _get_int(name: str, default: int) -> int:
    v = os.getenv(name)
    if v is None:
        return default
    try:
        return int(str(v).strip())
    except (TypeError, ValueError):
        return default


def _get_float(name: str, default: float) -> float:
    v = os.getenv(name)
    if v is None:
        return default
    try:
        return float(str(v).strip())
    except (TypeError, ValueError):
        return default


def _get_bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    x = str(v).strip().lower()
    if x in {"1", "true", "yes", "y", "on"}:
        return True
    if x in {"0", "false", "no", "n", "off"}:
        return False
    return default


def _init_clob_chain() -> tuple[str, int]:
    _ensure_env_loaded()
    host = _get_str("CLOB_HOST", "https://clob.polymarket.com") or "https://clob.polymarket.com"
    cid = _get_int("CHAIN_ID", 137)
    return host, cid


_CLOB_HOST, CHAIN_ID = _init_clob_chain()
CLOB_HOST: str = _CLOB_HOST


def get_auto_buy_min_amount(default: float = 1.0) -> float:
    _ensure_env_loaded()
    return max(0.0, _get_float("AUTO_BUY_MIN_AMOUNT", default))


def get_auto_buy_max_amount(default: float = 50.0) -> float:
    _ensure_env_loaded()
    return max(0.0, _get_float("AUTO_BUY_MAX_AMOUNT", default))


def get_balance_cache_ttl_sec(default: int = 10) -> int:
    _ensure_env_loaded()
    return max(0, _get_int("BALANCE_CACHE_TTL_SEC", default))


def get_collateral_token() -> str | None:
    _ensure_env_loaded()
    return _get_str("COLLATERAL_TOKEN")


def get_auto_redeem_dry_run_default(default: bool = False) -> bool:
    _ensure_env_loaded()
    return _get_bool("AUTO_REDEEM_DRY_RUN", default)

