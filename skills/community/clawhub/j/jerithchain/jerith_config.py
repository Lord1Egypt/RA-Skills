"""Configuration for the JerithChain OpenClaw skill.

Conservative by default: mining disabled, confirmation required for any
send over 1 JER, daily limit 10 JER. All monetary values in the skill are
integer micro-JER (uJ); the YAML-ish JSON config uses human JER floats
only at the config boundary and converts once, here.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

DEFAULT_CONFIG = {
    "rpc_url": "http://127.0.0.1:8300",
    "network": "mainnet",
    "wallet_path": "~/.config/jerith/skill-wallet.json",
    "spending": {
        "automatic_send_limit_jer": 1.0,     # sends at or below this need no prompt
        "daily_limit_jer": 10.0,             # max total sends per UTC day
        "require_confirmation": True,        # confirm before any send (in chat)
    },
    "mining": {
        "enabled": False,                    # PoW mining via node is opt-in
        "max_duration_seconds": 120,
    },
    "conversation_mining": {
        "enabled": True,                     # ask node on explicit user request
        "daily_attempt_limit": 50,           # client-side throttle
    },
    "default_discord_id": "",                # mining credit identity (or pass --discord-id)
    "explorer_url": "http://127.0.0.1:8303",  # read-only explorer for history/supply
    "http_timeout_seconds": 20,
    "cache_seconds": 15,                     # short cache for status/balance
}


def config_path() -> Path:
    return Path(os.environ.get(
        "JERITH_SKILL_CONFIG",
        Path.home() / ".config" / "jerith" / "skill-config.json"))


def load_config() -> dict:
    p = config_path()
    cfg = json.loads(json.dumps(DEFAULT_CONFIG))  # deep copy
    if p.exists():
        try:
            user = json.loads(p.read_text())
        except json.JSONDecodeError:
            raise SystemExit(f"jerith: config at {p} is not valid JSON")
        for k, v in user.items():
            if isinstance(v, dict) and isinstance(cfg.get(k), dict):
                cfg[k].update(v)
            else:
                cfg[k] = v
    return cfg


def save_config(cfg: dict) -> None:
    p = config_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(cfg, indent=2))


def jer_to_uj(amount_jer: float) -> int:
    """Convert JER to uJ exactly. Rejects more than 6 decimal places and
    negative/absurd values — no float arithmetic beyond the boundary."""
    if not isinstance(amount_jer, (int, float)) or amount_jer != amount_jer:
        raise ValueError("amount must be a number")
    scaled = round(float(amount_jer) * 1_000_000)
    if abs(float(amount_jer) * 1_000_000 - scaled) > 1e-6:
        raise ValueError("amount has more than 6 decimal places (uJ precision)")
    if scaled <= 0 or scaled > 10**15:
        raise ValueError("amount out of range")
    return int(scaled)


def uj_to_jer(uj: int) -> float:
    return int(uj) / 1_000_000
