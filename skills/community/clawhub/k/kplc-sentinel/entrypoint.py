import json
import sys
import logging
import sqlite3
from init_db import init_db, get_db

logger = logging.getLogger(__name__)
from parser import parse_kplc_sms
from logic import (
    add_purchase, add_reading, predict_blackout, calculate_burn_rate,
    set_profile, get_profile, get_all_profile, is_onboarded, reset_profile,
    monthly_summary, yearly_summary, price_trend_data, check_outages,
    set_budget, budget_data, estimate_days, comparison_insights_data
)

MENU_OPTIONS = [
    ("balance", "Check remaining power"),
    ("budget", "Budget status"),
    ("insights", "Week-over-week usage"),
    ("monthly", "This month's summary"),
    ("yearly", "Yearly summary"),
    ("spending", "Spending + price trend"),
    ("price", "Cost-per-unit trend"),
    ("outage", "Planned outages in your area"),
    ("profile", "Household info"),
    ("setup", "Onboard / re-setup"),
]

ONBOARDING_QUESTIONS = [
    ("occupants", "How many people live in your household?"),
    ("area", "What area/estate do you live in? (e.g. Kilimani, Umoja, Kitengela)"),
    ("appliances", "List your main electric appliances (e.g. fridge, TV, iron, water heater):"),
]

_COMMANDS = None

def _get_commands():
    global _COMMANDS
    if _COMMANDS is None:
        _COMMANDS = [
            (("reset", "clear"), _cmd_reset),
            (("setup", "start", "hello", "hi", "hey"), _cmd_setup),
            (("help", "menu", "?"), lambda t, l: _cmd_menu()),
            (("budget",), _cmd_budget),
            (("insight", "compare", "pattern"), _cmd_insights),
            (("monthly", "this month"), _cmd_monthly),
            (("yearly", "this year", "annual"), _cmd_yearly),
            (("spending", "spend"), _cmd_spending),
            (("price", "tariff"), _cmd_price),
            (("outage", "interruption", "maintenance"), _cmd_outage),
            (("balance", "power", "units"), _cmd_balance),
            (("profile", "household", "info"), _cmd_profile),
        ]
    return _COMMANDS


def handle_message(text):
    try:
        return _handle_message(text)
    except sqlite3.Error:
        logger.exception("Database error")
        return {"action": "error", "error": "database"}


MAX_INPUT_LEN = 5000
MAX_PROFILE_LEN = 200

def _handle_message(text):
    text = text.strip()[:MAX_INPUT_LEN]

    # Auto-detect forwarded KPLC SMS (no prefix needed)
    parsed = parse_kplc_sms(text)
    if parsed["success"]:
        is_dup = not add_purchase(parsed["token"], parsed["units"], parsed["amount"], text)
        if is_dup:
            return {"action": "duplicate_token", "token": parsed["token_display"]}
        result = {
            "action": "token_recorded",
            "token": parsed["token_display"],
            "units": parsed["units"],
            "amount": parsed["amount"],
            "estimate_source": "meter" if calculate_burn_rate() else "appliances",
        }
        days = estimate_days(parsed["units"])
        if days:
            result["estimated_days"] = round(days, 1)
        remaining = predict_blackout()
        if remaining:
            result["total_runway_hours"] = round(remaining, 1)
            result["tip"] = _get_tip(remaining)
        bdata = budget_data()
        if bdata and bdata["percent"] >= 80:
            result["budget_warning"] = bdata
        return result

    # All other messages require 'stima' prefix
    lower = text.lower()
    if not lower.startswith("stima"):
        return None

    text = text[5:].strip()
    lower = text.lower()

    # Onboarding flow
    pending = get_profile("onboarding_step")
    if pending is not None:
        if not text:
            if pending.isdigit() and int(pending) < len(ONBOARDING_QUESTIONS):
                return {"action": "onboarding_prompt", "question": ONBOARDING_QUESTIONS[int(pending)][1]}
            return None
        return _handle_onboarding(pending, text)

    if not text:
        return _cmd_menu()

    # Menu number selection
    if lower.isdigit() and get_profile("menu_pending"):
        choice = int(lower)
        if 1 <= choice <= len(MENU_OPTIONS):
            set_profile("menu_pending", None)
            cmd = MENU_OPTIONS[choice - 1][0]
            return _handle_message(f"stima {cmd}")
        set_profile("menu_pending", None)

    # Manual reading (plain number)
    try:
        balance = float(text)
        return _cmd_reading(balance)
    except ValueError:
        pass

    for prefixes, handler in _get_commands():
        if any(lower == p or lower.startswith(p + " ") for p in prefixes):
            return handler(text, lower)

    return None


# ── handlers ─────────────────────────────────────────────────────────────

def _cmd_menu():
    set_profile("menu_pending", "1")
    return {
        "action": "menu",
        "options": [{"number": i, "label": label} for i, (_, label) in enumerate(MENU_OPTIONS, 1)],
    }


def _handle_onboarding(pending, text):
    try:
        step = int(pending)
    except (ValueError, TypeError):
        set_profile("onboarding_step", None)
        return {"action": "onboarding_error"}
    if step < 0 or step >= len(ONBOARDING_QUESTIONS):
        set_profile("onboarding_step", None)
        return {"action": "onboarding_error"}
    key = ONBOARDING_QUESTIONS[step][0]
    set_profile(key, text[:MAX_PROFILE_LEN])
    step += 1
    if step < len(ONBOARDING_QUESTIONS):
        set_profile("onboarding_step", str(step))
        return {"action": "onboarding_prompt", "question": ONBOARDING_QUESTIONS[step][1]}
    set_profile("onboarding_step", None)
    return {"action": "onboarding_complete", "profile": get_all_profile()}


def _cmd_reading(balance):
    if balance < 0:
        return {"action": "error", "error": "negative_reading"}
    try:
        add_reading(balance, "Manual entry")
    except ValueError as e:
        return {"action": "error", "error": str(e)}
    remaining = predict_blackout()
    result = {"action": "reading_recorded", "balance": balance}
    if remaining:
        result["runway_hours"] = round(remaining, 1)
        result["estimate_source"] = "meter" if calculate_burn_rate() else "appliances"
        result["tip"] = _get_tip(remaining)
    return result


def _cmd_setup(text, lower):
    if not is_onboarded():
        set_profile("onboarding_step", "0")
        return {"action": "onboarding_prompt", "question": ONBOARDING_QUESTIONS[0][1], "welcome": True}
    return {"action": "already_onboarded"}


def _cmd_reset(text, lower):
    reset_profile()
    set_profile("onboarding_step", "0")
    return {"action": "profile_reset", "question": ONBOARDING_QUESTIONS[0][1]}


def _cmd_budget(text, lower):
    parts = text.split()
    if len(parts) >= 2:
        try:
            amt = float(parts[1].replace(",", ""))
            set_budget(amt)
            return {"action": "budget_set", "amount": amt}
        except ValueError:
            pass
    data = budget_data()
    if data:
        return {"action": "budget_status", **data}
    return {"action": "no_budget"}


def _cmd_insights(text, lower):
    data = comparison_insights_data()
    if data:
        return {"action": "insights", **data}
    return {"action": "no_data", "feature": "insights"}


def _cmd_monthly(text, lower):
    return {"action": "monthly_summary", **monthly_summary()}


def _cmd_yearly(text, lower):
    return {"action": "yearly_summary", **yearly_summary()}


def _cmd_spending(text, lower):
    return {"action": "spending", "monthly": monthly_summary(), "price_trend": price_trend_data()}


def _cmd_price(text, lower):
    data = price_trend_data()
    if data["months"]:
        return {"action": "price_trend", **data}
    return {"action": "no_data", "feature": "price trends"}


def _cmd_outage(text, lower):
    return {"action": "outage_check", **check_outages()}


def _cmd_balance(text, lower):
    remaining = predict_blackout()
    if remaining:
        return {
            "action": "balance",
            "runway_hours": round(remaining, 1),
            "estimate_source": "meter" if calculate_burn_rate() else "appliances",
            "tip": _get_tip(remaining),
        }
    return {"action": "no_data", "feature": "balance"}


def _cmd_profile(text, lower):
    profile = get_all_profile()
    if not profile:
        return {"action": "no_profile"}
    result = {"action": "profile", **profile}
    data = budget_data()
    if data:
        result["budget"] = data
    return result


# ── helpers ──────────────────────────────────────────────────────────────

_HEAVY_APPLIANCES = {"heater", "iron", "oven", "geyser", "water heater", "boiler"}

def _get_tip(hours_remaining):
    if hours_remaining >= 12:
        return None
    appliances = get_profile("appliances")
    if not appliances:
        return None
    import re
    items = [a.strip().lower() for a in re.split(r'[,/]|\band\b', appliances) if a.strip()]
    heavy = [a for a in items if any(h in a for h in _HEAVY_APPLIANCES)]
    return f"avoid running {', '.join(heavy)}" if heavy else None


if __name__ == "__main__":
    init_db()
    msg = sys.stdin.read().strip()
    if msg:
        result = handle_message(msg)
        if result:
            print(json.dumps(result))
