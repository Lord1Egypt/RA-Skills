"""
risk.py — Risk management for Kalshi agent
Controls bet sizing, daily limits, and position tracking.
"""

import json
import os
from datetime import date, datetime
from typing import Optional


STATE_FILE = os.path.join(os.path.dirname(__file__), "risk_state.json")

# ── Limits ─────────────────────────────────────────────────────────────────
MAX_BET_DOLLARS = 5.00          # max per single bet
MAX_DAILY_DOLLARS = 20.00       # max total per day
MAX_OPEN_POSITIONS = 5          # max concurrent open bets
MIN_CONFIDENCE = "medium"       # skip "low" confidence markets
MAX_PRICE_YES = 85              # don't buy YES above this (cents)
MIN_PRICE_YES = 15              # don't buy NO below this (cents)
KELLY_FRACTION = 0.25           # fractional Kelly (conservative)

CONFIDENCE_RANK = {"low": 0, "medium": 1, "high": 2}


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {
        "date": str(date.today()),
        "daily_spent_cents": 0,
        "bets_today": [],
        "open_positions": [],
        "total_profit_cents": 0,
        "all_time_bets": 0,
    }


def save_state(state: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def get_state() -> dict:
    state = load_state()
    # Reset daily tracking if it's a new day
    if state.get("date") != str(date.today()):
        state["date"] = str(date.today())
        state["daily_spent_cents"] = 0
        state["bets_today"] = []
        save_state(state)
    return state


def daily_remaining_cents(state: dict) -> int:
    return int(MAX_DAILY_DOLLARS * 100) - state["daily_spent_cents"]


def can_bet(state: dict, amount_cents: int, confidence: str) -> tuple[bool, str]:
    """Returns (allowed, reason)."""
    # Confidence gate
    if CONFIDENCE_RANK.get(confidence, 0) < CONFIDENCE_RANK[MIN_CONFIDENCE]:
        return False, f"Confidence too low ({confidence} < {MIN_CONFIDENCE})"

    # Daily limit
    remaining = daily_remaining_cents(state)
    if amount_cents > remaining:
        return False, f"Daily limit reached (${remaining/100:.2f} remaining of ${MAX_DAILY_DOLLARS:.2f})"

    # Per-bet limit
    if amount_cents > int(MAX_BET_DOLLARS * 100):
        return False, f"Bet size ${amount_cents/100:.2f} exceeds max ${MAX_BET_DOLLARS:.2f}"

    # Open positions
    if len(state.get("open_positions", [])) >= MAX_OPEN_POSITIONS:
        return False, f"Max open positions reached ({MAX_OPEN_POSITIONS})"

    return True, "OK"


def size_bet(
    balance_cents: int,
    confidence: str,
    price_cents: int,
    edge_estimate: float = 0.05,
) -> int:
    """
    Kelly Criterion bet sizing (fractional).
    Returns bet amount in cents, capped by limits.
    
    price_cents: cost per contract (1-99)
    edge_estimate: estimated edge over market price (0.0-1.0)
    """
    p = price_cents / 100.0
    if p <= 0 or p >= 1:
        return 0

    # Kelly: f = (p*b - q) / b where b = (1-p)/p (binary market)
    b = (1 - p) / p
    q = 1 - p
    kelly = (p * b - q) / b  # = edge/price

    # Use edge estimate if Kelly is wonky
    kelly = max(kelly, edge_estimate)

    # Fractional Kelly
    fraction = KELLY_FRACTION
    if confidence == "high":
        fraction = KELLY_FRACTION * 1.5
    elif confidence == "low":
        fraction = KELLY_FRACTION * 0.5

    raw_bet = int(balance_cents * fraction * kelly)

    # Apply hard caps
    max_bet = int(MAX_BET_DOLLARS * 100)
    return max(min(raw_bet, max_bet), 100)  # minimum $1.00


def record_bet(state: dict, ticker: str, side: str, amount_cents: int, order_id: str):
    """Record a placed bet in state."""
    state["daily_spent_cents"] += amount_cents
    state["all_time_bets"] += 1
    bet = {
        "ticker": ticker,
        "side": side,
        "amount_cents": amount_cents,
        "order_id": order_id,
        "placed_at": datetime.utcnow().isoformat(),
        "status": "open",
    }
    state["bets_today"].append(bet)
    state["open_positions"].append(bet)
    save_state(state)


def record_settlement(state: dict, order_id: str, profit_cents: int):
    """Record when a bet settles."""
    state["open_positions"] = [
        p for p in state.get("open_positions", []) if p.get("order_id") != order_id
    ]
    state["total_profit_cents"] = state.get("total_profit_cents", 0) + profit_cents
    save_state(state)


def risk_summary(state: dict) -> str:
    remaining = daily_remaining_cents(state)
    profit = state.get("total_profit_cents", 0)
    sign = "+" if profit >= 0 else ""
    return (
        f"Daily budget: ${remaining/100:.2f} remaining (${MAX_DAILY_DOLLARS:.2f} max)\n"
        f"Open positions: {len(state.get('open_positions', []))}/{MAX_OPEN_POSITIONS}\n"
        f"Bets today: {len(state.get('bets_today', []))}\n"
        f"All-time P&L: {sign}${profit/100:.2f}\n"
        f"Total bets placed: {state.get('all_time_bets', 0)}"
    )
