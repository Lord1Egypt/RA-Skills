# SPDX-License-Identifier: Apache-2.0
"""Key-management tools — agent-driven API key configuration.

Lets an agent (zeroclaw / openclaw / hermes / claude-desktop) prompt the
user for an API key and POST it directly to the container, instead of
requiring host shell access to edit `/data/keys.env`.

Designed so an MD-skill-only agent install path can configure keys via
either MCP (`portfolio_keys_set`) or plain REST (`POST /api/portfolio/keys/set`).

Persistence: writes to `/data/keys.env` mode 0600 via `setup_api._save_keys`,
which makes the keys survive container restart (the `/data` volume is
bind-mounted per compose.yml).

Liveness: also pushes the new keys into `os.environ` so subprocesses
spawned by the bridge after the call (i.e. the next portfolio_ask) inherit
them. No bridge restart required.

Allowlist: only KNOWN_KEYS may be set via this surface. This prevents an
agent from setting arbitrary container env vars that could affect engine
behavior. Adding a new settable key requires updating the KNOWN_KEYS
catalogue in setup_api.py and rebuilding the image.
"""
from __future__ import annotations

import os
from typing import Any

from .. import _runtime  # for logger
from .._runtime import logger


_ALLOWLIST: set[str] | None = None


def _allowlist() -> set[str]:
    """Return the set of settable key names. Reuses setup_api.KNOWN_KEYS."""
    global _ALLOWLIST
    if _ALLOWLIST is None:
        try:
            from investorclaw_bridge.setup_api import KNOWN_KEYS
            _ALLOWLIST = {k["name"] for k in KNOWN_KEYS}
        except Exception:
            # Conservative fallback if setup_api isn't importable —
            # the canonical six keys per compose.yml's optional_keys.
            _ALLOWLIST = {
                "TOGETHER_API_KEY",
                "OPENAI_API_KEY",
                "FINNHUB_KEY",
                "FRED_API_KEY",
                "NEWSAPI_KEY",
                "ALPHA_VANTAGE_KEY",
                "MASSIVE_API_KEY",
                "MARKETAUX_API_KEY",
            }
    return _ALLOWLIST


def _read_existing() -> dict[str, str]:
    """Delegate to setup_api._read_existing_keys (or a thin reimplementation
    if setup_api isn't importable). Returns {KEY_NAME: VALUE}.
    """
    try:
        from investorclaw_bridge.setup_api import _read_existing_keys
        return _read_existing_keys()
    except Exception:
        from pathlib import Path
        keys_file = Path(os.environ.get("IC_KEYS_FILE", "/data/keys.env"))
        if not keys_file.exists():
            return {}
        keys: dict[str, str] = {}
        for raw in keys_file.read_text().splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            keys[k.strip()] = v.strip().strip('"').strip("'")
        return keys


def _persist(updates: dict[str, str]) -> None:
    """Persist via setup_api (which writes mode 0600, sorts, dedupes)."""
    from investorclaw_bridge.setup_api import _save_keys
    _save_keys(updates)


def _push_into_environ(updates: dict[str, str]) -> None:
    """Mirror the keys into the bridge's os.environ so subprocesses pick
    them up immediately. Only sets keys with a non-empty value; empty
    values are deletions (also reflected here).
    """
    for name, value in updates.items():
        if value:
            os.environ[name] = value
        else:
            os.environ.pop(name, None)


# ──────────────────────────────────────────────────────────────────────
# Pure tool handlers (transport-agnostic)
# ──────────────────────────────────────────────────────────────────────


async def portfolio_keys_status() -> dict[str, Any]:
    """Return which keys are currently configured (NOT their values)."""
    existing = _read_existing()
    allowlist = _allowlist()
    return {
        "configured": sorted(k for k in allowlist if existing.get(k)),
        "settable": sorted(allowlist),
        "missing": sorted(k for k in allowlist if not existing.get(k)),
        "keys_file": os.environ.get("IC_KEYS_FILE", "/data/keys.env"),
    }


async def portfolio_keys_set(keys: dict[str, str]) -> dict[str, Any]:
    """Set one or more API keys.

    Args:
        keys: mapping of KEY_NAME → value. Names not in the allowlist are
            rejected with a 400-shaped response. Empty/None values delete
            the key.

    Returns:
        {"configured": [...], "rejected": [...], "deleted": [...]}.
    """
    if not isinstance(keys, dict) or not keys:
        return {
            "error": "missing_keys",
            "detail": "Provide a non-empty mapping of KEY_NAME -> value.",
            "configured": [],
            "rejected": [],
            "deleted": [],
        }

    allowlist = _allowlist()
    rejected = sorted(k for k in keys if k not in allowlist)
    if rejected:
        return {
            "error": "rejected_keys_not_in_allowlist",
            "detail": (
                "These names are not settable via this surface. "
                "See `settable` field of /api/portfolio/keys/status."
            ),
            "configured": [],
            "rejected": rejected,
            "deleted": [],
            "settable": sorted(allowlist),
        }

    # Normalize values
    updates = {
        name: ((value or "").strip() if isinstance(value, str) else "")
        for name, value in keys.items()
    }

    # Persist + mirror into environ
    _persist(updates)
    _push_into_environ(updates)

    set_keys = sorted(k for k, v in updates.items() if v)
    deleted_keys = sorted(k for k, v in updates.items() if not v)
    logger.info(
        "mcp.keys.set",
        configured=set_keys,
        deleted=deleted_keys,
    )
    return {
        "configured": set_keys,
        "rejected": [],
        "deleted": deleted_keys,
    }


async def portfolio_keys_delete(name: str) -> dict[str, Any]:
    """Delete a single configured key by name."""
    if name not in _allowlist():
        return {
            "error": "rejected_key_not_in_allowlist",
            "detail": "Name not settable via this surface.",
            "deleted": False,
            "settable": sorted(_allowlist()),
        }
    _persist({name: ""})
    _push_into_environ({name: ""})
    logger.info("mcp.keys.delete", name=name)
    return {"deleted": True, "name": name}


# ──────────────────────────────────────────────────────────────────────
# Tool descriptors (registered via TOOL_REGISTRY in tools/__init__.py)
# ──────────────────────────────────────────────────────────────────────


def _tool(description: str, parameters: dict, required: list[str], handler) -> dict:
    return {
        "description": description,
        "parameters": parameters,
        "required": required,
        "handler": handler,
    }


KEYS_TOOLS: dict[str, dict[str, Any]] = {
    "portfolio_keys_status": _tool(
        description=(
            "Report which API keys are currently configured for ic-engine. "
            "Returns names only — never key values. Use this to check what's "
            "set before prompting the user for a missing key."
        ),
        parameters={},
        required=[],
        handler=portfolio_keys_status,
    ),
    "portfolio_keys_set": _tool(
        description=(
            "Set one or more ic-engine API keys. Persisted to /data/keys.env "
            "(mode 0600) and immediately available to the next portfolio_ask "
            "call without restart. Only the standard ic-engine keys are "
            "settable: TOGETHER_API_KEY, OPENAI_API_KEY, FINNHUB_KEY, "
            "FRED_API_KEY, NEWSAPI_KEY, ALPHA_VANTAGE_KEY. Other names are "
            "rejected. Empty values delete the key."
        ),
        parameters={
            "keys": {
                "type": "object",
                "description": (
                    "Mapping of KEY_NAME (str) -> value (str). Only allowlisted "
                    "names accepted. Empty value deletes the key."
                ),
            },
        },
        required=["keys"],
        handler=portfolio_keys_set,
    ),
    "portfolio_keys_delete": _tool(
        description=(
            "Delete a single configured ic-engine API key by name. Only "
            "allowlisted names accepted."
        ),
        parameters={
            "name": {
                "type": "string",
                "description": "Key name to delete (must be in the allowlist).",
            },
        },
        required=["name"],
        handler=portfolio_keys_delete,
    ),
}
