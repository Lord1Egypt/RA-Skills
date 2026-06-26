"""Pending-trade store. Implements the human-in-the-loop gate for IBKR.

Layout:  ~/.aeon/ibkr/pending/<id>.json       — proposed trade awaiting YES
         ~/.aeon/ibkr/notional_log.jsonl      — append-only execution log

Mirrors skills/aeon/okx-trading/_pending.py but with a separate state dir
so the two skills' gates never collide.
"""
from __future__ import annotations

import json
import os
import secrets
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.path.expanduser("~/.aeon/ibkr"))
PENDING_DIR = ROOT / "pending"
NOTIONAL_LOG = ROOT / "notional_log.jsonl"

TRADE_TTL_SECONDS = 10 * 60


class PendingError(Exception):
    pass


def _ensure_dirs() -> None:
    PENDING_DIR.mkdir(parents=True, exist_ok=True)


def new_id() -> str:
    return secrets.token_hex(4)


def _new_token() -> str:
    return secrets.token_hex(16)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _path(pid: str) -> Path:
    return PENDING_DIR / f"{pid}.json"


def save_pending(kind: str, payload: dict, ttl_seconds: int = TRADE_TTL_SECONDS) -> tuple[str, str]:
    _ensure_dirs()
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
        record.pop("confirmation_token", None)
        out.append(record)
    return out


def append_notional_log(entry: dict) -> None:
    _ensure_dirs()
    entry = dict(entry)
    entry.setdefault("ts_iso", now_iso())
    entry.setdefault("date_utc", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    with NOTIONAL_LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def today_notional_usd() -> float:
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
            total += float(entry.get("notional_usd", 0.0))
    return total
