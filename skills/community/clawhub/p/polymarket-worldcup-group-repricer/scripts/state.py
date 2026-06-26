"""Atomic position/exposure state. Live and dry-run state are SEPARATE files; all
read-modify-write goes through an fcntl lock so overlapping cron runs can't double-spend."""

import fcntl
import json
import os
from contextlib import contextmanager

_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _path(live):
    return os.path.join(_DIR, "state_live.json" if live else "state_dry.json")


@contextmanager
def locked_state(live):
    """Yield the state dict under an exclusive lock; persist on clean exit."""
    path = _path(live)
    lockpath = path + ".lock"
    with open(lockpath, "a+") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        try:
            state = _load(path)
            yield state
            _save(path, state)
        finally:
            fcntl.flock(lk, fcntl.LOCK_UN)


def _load(path):
    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {"positions": {}, "open_exposure_usd": 0.0}


def _save(path, state):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, path)


def has_position(state, market_id):
    return market_id in state["positions"]


def add_position(state, market_id, kind, side, cost, price, reason):
    """Record a fill and debit exposure by ACTUAL cost (not requested notional)."""
    state["positions"][market_id] = {
        "kind": kind, "side": side, "cost": float(cost),
        "entry_price": float(price), "reason": reason, "status": "open",
    }
    state["open_exposure_usd"] = round(state.get("open_exposure_usd", 0.0) + float(cost), 6)


def close_position(state, market_id, proceeds):
    pos = state["positions"].get(market_id)
    if not pos or pos["status"] != "open":
        return
    pos["status"] = "closed"
    pos["proceeds"] = float(proceeds)
    state["open_exposure_usd"] = round(
        max(0.0, state.get("open_exposure_usd", 0.0) - pos["cost"]), 6)


def exposure_allows(state, new_cost, budget):
    return state.get("open_exposure_usd", 0.0) + new_cost <= budget
