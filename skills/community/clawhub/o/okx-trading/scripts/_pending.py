"""Pending-trade store. Implements the human-in-the-loop gate.

Layout:  ~/.aeon/okx/pending/<id>.json       — proposed trade awaiting YES
         ~/.aeon/okx/strategies/<id>.json    — confirmed long-running strategies
         ~/.aeon/okx/notional_log.jsonl      — append-only execution log

A proposal stores:
    id            — short identifier surfaced to the user
    confirmation_token — 32-char hex; never shown to the user, only used
                         programmatically by okx_execute_trade.py / okx_grid_apply.py
    kind          — "trade" | "grid"
    payload       — kind-specific dict (see okx_propose_trade, okx_grid_setup)
    created_at    — UTC ISO
    expires_at    — UTC ISO (created_at + 10 min for trades, 30 min for grids)

Execution scripts MUST call validate_token() before placing any order.
"""
from __future__ import annotations

import json
import os
import secrets
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.path.expanduser("~/.aeon/okx"))
PENDING_DIR = ROOT / "pending"
STRATEGY_DIR = ROOT / "strategies"
NOTIONAL_LOG = ROOT / "notional_log.jsonl"

TRADE_TTL_SECONDS = 10 * 60
GRID_TTL_SECONDS = 30 * 60


class PendingError(Exception):
    pass


def _ensure_dirs() -> None:
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    STRATEGY_DIR.mkdir(parents=True, exist_ok=True)


def new_id() -> str:
    # 8 hex chars — short enough to type into Telegram, large enough to avoid
    # casual collisions (~4B entropy) given proposal expiry of 10 min.
    return secrets.token_hex(4)


def _new_token() -> str:
    return secrets.token_hex(16)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _path(pid: str) -> Path:
    return PENDING_DIR / f"{pid}.json"


def save_pending(kind: str, payload: dict, ttl_seconds: int | None = None) -> tuple[str, str]:
    """Create a new pending record. Returns (id, confirmation_token)."""
    _ensure_dirs()
    if ttl_seconds is None:
        ttl_seconds = TRADE_TTL_SECONDS if kind == "trade" else GRID_TTL_SECONDS

    pid = new_id()
    token = _new_token()
    record = {
        "id": pid,
        "confirmation_token": token,
        "kind": kind,
        "payload": payload,
        "created_at": now_iso(),
        "expires_at_epoch": int(time.time()) + ttl_seconds,
    }
    path = _path(pid)
    path.write_text(json.dumps(record, indent=2))
    os.chmod(path, 0o600)
    return pid, token


def load_pending(pid: str) -> dict:
    path = _path(pid)
    if not path.exists():
        raise PendingError(f"No pending proposal with id '{pid}' (expired or never existed)")
    record = json.loads(path.read_text())
    if int(time.time()) > record["expires_at_epoch"]:
        try:
            path.unlink()
        except FileNotFoundError:
            pass
        raise PendingError(f"Proposal '{pid}' has expired")
    return record


def validate_token(record: dict, token: str) -> None:
    expected = record.get("confirmation_token")
    if not expected or not secrets.compare_digest(expected, token):
        raise PendingError("confirmation_token does not match — refusing to execute")


def delete_pending(pid: str) -> None:
    path = _path(pid)
    if path.exists():
        path.unlink()


def list_pending() -> list[dict]:
    _ensure_dirs()
    out: list[dict] = []
    now = int(time.time())
    for path in sorted(PENDING_DIR.glob("*.json")):
        try:
            record = json.loads(path.read_text())
        except Exception:
            continue
        if now > record.get("expires_at_epoch", 0):
            try:
                path.unlink()
            except FileNotFoundError:
                pass
            continue
        # Hide the token when listing — only id is user-facing.
        record.pop("confirmation_token", None)
        out.append(record)
    return out


def save_strategy(strategy_id: str, payload: dict) -> Path:
    _ensure_dirs()
    path = STRATEGY_DIR / f"{strategy_id}.json"
    path.write_text(json.dumps(payload, indent=2))
    os.chmod(path, 0o600)
    return path


def load_strategy(strategy_id: str) -> dict:
    path = STRATEGY_DIR / f"{strategy_id}.json"
    if not path.exists():
        raise PendingError(f"No strategy with id '{strategy_id}'")
    return json.loads(path.read_text())


def update_strategy(strategy_id: str, payload: dict) -> None:
    save_strategy(strategy_id, payload)


def delete_strategy(strategy_id: str) -> None:
    path = STRATEGY_DIR / f"{strategy_id}.json"
    if path.exists():
        path.unlink()


def list_strategies() -> list[dict]:
    _ensure_dirs()
    out: list[dict] = []
    for path in sorted(STRATEGY_DIR.glob("*.json")):
        try:
            out.append(json.loads(path.read_text()))
        except Exception:
            continue
    return out


def append_notional_log(entry: dict) -> None:
    """Record a completed execution for the daily-notional guardrail."""
    _ensure_dirs()
    entry = dict(entry)
    entry.setdefault("ts_iso", now_iso())
    entry.setdefault("date_utc", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    with NOTIONAL_LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def today_notional_usdt() -> float:
    """Sum of notional executed today (UTC)."""
    if not NOTIONAL_LOG.exists():
        return 0.0
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    total = 0.0
    for line in NOTIONAL_LOG.read_text().splitlines():
        try:
            entry = json.loads(line)
        except Exception:
            continue
        if entry.get("date_utc") == today:
            total += float(entry.get("notional_usdt", 0.0))
    return total
