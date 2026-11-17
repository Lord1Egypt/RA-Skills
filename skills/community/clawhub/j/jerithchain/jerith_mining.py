"""Mining client.

JER's mining model: the NODE performs the proof-of-work, enforces
cooldowns, applies the reward schedule, and appends the block. The skill
only RELAYS an eligibility request and reports the node's verdict — it
never mints, never fabricates rewards, never touches chain state.

Two sources map onto the node's API:
  "explicit"  — user asked to mine (`jerith-skill mine`)
  "passive"   — conversational mining tied to a message id (dedup handled
                by the node via _seen_once)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from jerith_client import Client

_ATTEMPT_FILE = Path.home() / ".config" / "jerith" / "mine-attempts.json"


def _today() -> str:
    return time.strftime("%Y-%m-%d", time.gmtime())


def _attempts_today() -> int:
    try:
        st = json.loads(_ATTEMPT_FILE.read_text())
        return int(st.get("count", 0)) if st.get("date") == _today() else 0
    except (OSError, json.JSONDecodeError, ValueError):
        return 0


def _record_attempt() -> None:
    _ATTEMPT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with _ATTEMPT_FILE.open("w") as f:
        json.dump({"date": _today(), "count": _attempts_today() + 1}, f)


class MiningDisabled(Exception):
    pass


def mine(cfg: dict, discord_id: str, source: str = "explicit",
         guild_id: str = "", channel_id: str = "",
         message_id: str = "") -> dict:
    """Request a mining attempt from the node. Returns the node's verdict.
    Raises MiningDisabled if disabled or daily client throttle is hit."""
    if source not in ("explicit", "passive"):
        raise MiningDisabled(f"unknown mining source {source!r}")
    if not cfg["mining"]["enabled"] and source == "explicit":
        raise MiningDisabled(
            "PoW mining is disabled in skill config "
            "(mining.enabled=false) — enable it explicitly if you want "
            "this machine to mine")
    limit = int(cfg["conversation_mining"]["daily_attempt_limit"])
    if _attempts_today() >= limit:
        raise MiningDisabled(
            f"daily mining attempt limit reached ({limit}) — client-side "
            f"throttle, try tomorrow")
    _record_attempt()
    res = Client(cfg).mine(discord_id, source, guild_id, channel_id, message_id)
    # pass through ONLY node-provided fields; never invent success
    return {
        "ok": bool(res.get("ok")),
        "reason": res.get("reason", ""),
        "message": res.get("message", ""),
        "reward_uj": res.get("reward_uj"),
        "reward_jer": res.get("reward_jer"),
        "block_height": res.get("block_height"),
        "block_hash": res.get("block_hash"),
        "difficulty_bits": res.get("difficulty_bits"),
        "credited_address": res.get("credited_address"),
        "redirected_to_owner": res.get("redirected_to_owner"),
    }
