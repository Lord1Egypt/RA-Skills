"""
growth_state.py — L3 local next-step suggestion state management

Responsibilities:
- Read/write growth_state.json
- Determine if each tip type should be shown (onboarding, automation, preference, workflow)
- Update shown counts, cooldown periods, and completion status
- Maintain basic usage counters and usage pattern tracking

Cooldown Mechanism:
- onboarding tip: Low frequency suggestion after first successful news fetch
- preference setup hint: Guide users to set news preferences
- automation setup hint: Guide users to set up daily automated delivery
- workflow integration hint: Guide users to use workflow templates

Each tip type has independent cooldown periods.
"""

import json
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from lib.runtime_paths import get_growth_state_path

# Default cooldown periods (days)
DEFAULT_ONBOARDING_TIP_COOLDOWN_DAYS = 14
DEFAULT_PREFERENCE_TIP_COOLDOWN_DAYS = 14
DEFAULT_AUTOMATION_TIP_COOLDOWN_DAYS = 7
DEFAULT_WORKFLOW_TIP_COOLDOWN_DAYS = 14

# Default maximum show count per tip type
DEFAULT_MAX_SHOW_COUNT = 3


_EMPTY_STATE = {
    "version": "v1",
    "first_successful_news_at": None,
    "onboarding_tip": {
        "shown_count": 0,
        "last_shown_at": None,
        "cooldown_until": None,
        "completed": False,
    },
    "automation_hint": {
        "shown_count": 0,
        "last_shown_at": None,
        "cooldown_until": None,
        "dismissed_until": None,
        "completed": False,
    },
    "preference_hint": {
        "shown_count": 0,
        "last_shown_at": None,
        "cooldown_until": None,
        "completed": False,
    },
    "workflow_hint": {
        "shown_count": 0,
        "last_shown_at": None,
        "cooldown_until": None,
        "completed": False,
    },
    "usage_counters": {
        "latest_news_success_count": 0,
        "date_news_success_count": 0,
        "consecutive_active_days": 0,
        "last_active_local_date": None,
    },
}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_time(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        normalized = value.replace("Z", "+00:00")
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except Exception:
        return None


def _format_time(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


import copy


def _deep_copy_state(template: dict) -> dict:
    """Deep copy state template to avoid shared mutable object reference"""
    return copy.deepcopy(template)


def _new_state() -> dict:
    return _deep_copy_state(_EMPTY_STATE)


def _normalize_tip_state(raw_tip: dict, default_tip: dict) -> dict:
    """Normalize individual tip state"""
    if not isinstance(raw_tip, dict):
        return _deep_copy_state(default_tip)
    normalized = _deep_copy_state(default_tip)
    for key in ("shown_count", "completed"):
        if isinstance(raw_tip.get(key), int):
            normalized[key] = raw_tip[key]
        elif isinstance(raw_tip.get(key), bool):
            normalized[key] = bool(raw_tip[key])
    for key in ("last_shown_at", "cooldown_until", "dismissed_until"):
        value = raw_tip.get(key)
        if isinstance(value, str) and _parse_time(value):
            normalized[key] = value
    return normalized


def _normalize_state(raw) -> dict:
    state = _new_state()
    if not isinstance(raw, dict):
        return state

    if raw.get("version") == "v1":
        state["version"] = "v1"

    first_news = raw.get("first_successful_news_at")
    if isinstance(first_news, str) and _parse_time(first_news):
        state["first_successful_news_at"] = first_news

    # Normalize each tip state
    state["onboarding_tip"] = _normalize_tip_state(
        raw.get("onboarding_tip", {}), _EMPTY_STATE["onboarding_tip"]
    )
    state["automation_hint"] = _normalize_tip_state(
        raw.get("automation_hint", {}), _EMPTY_STATE["automation_hint"]
    )
    state["preference_hint"] = _normalize_tip_state(
        raw.get("preference_hint", {}), _EMPTY_STATE["preference_hint"]
    )
    state["workflow_hint"] = _normalize_tip_state(
        raw.get("workflow_hint", {}), _EMPTY_STATE["workflow_hint"]
    )

    # Normalize usage counters
    counters = raw.get("usage_counters", {})
    if isinstance(counters, dict):
        for key in (
            "latest_news_success_count",
            "date_news_success_count",
            "consecutive_active_days",
        ):
            if isinstance(counters.get(key), int):
                state["usage_counters"][key] = counters[key]
        last_active = counters.get("last_active_local_date")
        if isinstance(last_active, str):
            state["usage_counters"]["last_active_local_date"] = last_active

    return state


def load_growth_state() -> dict:
    path = get_growth_state_path()
    if not path.exists():
        state = _new_state()
        save_growth_state(state)
        return state
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        raw = {}
    state = _normalize_state(raw)
    save_growth_state(state)
    return state


def save_growth_state(state: dict) -> None:
    path = get_growth_state_path()
    normalized = _normalize_state(state)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(
        json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    tmp_path.replace(path)


def _cooldown_until(days: int) -> str:
    return _format_time(_utc_now() + timedelta(days=days))


def _is_in_cooldown(tip_state: dict, cooldown_field: str, now: Optional[datetime] = None) -> bool:
    until = _parse_time(tip_state.get(cooldown_field))
    if not until:
        return False
    return until > (now or _utc_now())


# ===== onboarding tip =====


def should_show_onboarding_tip(state: dict, now: Optional[datetime] = None) -> bool:
    """Check if onboarding tip should be shown"""
    tip = state.get("onboarding_tip", {})
    if tip.get("completed", False):
        return False
    if tip.get("shown_count", 0) >= DEFAULT_MAX_SHOW_COUNT:
        return False
    if _is_in_cooldown(tip, "cooldown_until", now):
        return False
    return True


def mark_onboarding_tip_shown(
    state: dict, cooldown_days: int = DEFAULT_ONBOARDING_TIP_COOLDOWN_DAYS
) -> dict:
    state = _normalize_state(state)
    tip = state["onboarding_tip"]
    tip["shown_count"] = tip.get("shown_count", 0) + 1
    tip["last_shown_at"] = _format_time(_utc_now())
    tip["cooldown_until"] = _cooldown_until(cooldown_days)
    return state


def mark_onboarding_completed(state: dict) -> dict:
    state = _normalize_state(state)
    state["onboarding_tip"]["completed"] = True
    return state


# ===== preference hint =====


def should_show_preference_hint(state: dict, now: Optional[datetime] = None) -> bool:
    tip = state.get("preference_hint", {})
    if tip.get("completed", False):
        return False
    if tip.get("shown_count", 0) >= DEFAULT_MAX_SHOW_COUNT:
        return False
    if _is_in_cooldown(tip, "cooldown_until", now):
        return False
    return True


def mark_preference_hint_shown(
    state: dict, cooldown_days: int = DEFAULT_PREFERENCE_TIP_COOLDOWN_DAYS
) -> dict:
    state = _normalize_state(state)
    tip = state["preference_hint"]
    tip["shown_count"] = tip.get("shown_count", 0) + 1
    tip["last_shown_at"] = _format_time(_utc_now())
    tip["cooldown_until"] = _cooldown_until(cooldown_days)
    return state


def mark_preference_setup_completed(state: dict) -> dict:
    state = _normalize_state(state)
    state["preference_hint"]["completed"] = True
    return state


# ===== automation hint =====


def should_show_automation_hint(state: dict, now: Optional[datetime] = None) -> bool:
    tip = state.get("automation_hint", {})
    if tip.get("completed", False):
        return False
    if tip.get("shown_count", 0) >= DEFAULT_MAX_SHOW_COUNT:
        return False
    if _is_in_cooldown(tip, "cooldown_until", now):
        return False
    if _is_in_cooldown(tip, "dismissed_until", now):
        return False
    return True


def mark_automation_hint_shown(
    state: dict, cooldown_days: int = DEFAULT_AUTOMATION_TIP_COOLDOWN_DAYS
) -> dict:
    state = _normalize_state(state)
    tip = state["automation_hint"]
    tip["shown_count"] = tip.get("shown_count", 0) + 1
    tip["last_shown_at"] = _format_time(_utc_now())
    tip["cooldown_until"] = _cooldown_until(cooldown_days)
    return state


def mark_automation_setup_completed(state: dict) -> dict:
    state = _normalize_state(state)
    state["automation_hint"]["completed"] = True
    return state


def mark_automation_dismissed(
    state: dict, dismissed_days: int = 30
) -> dict:
    state = _normalize_state(state)
    state["automation_hint"]["dismissed_until"] = _cooldown_until(dismissed_days)
    return state


# ===== workflow hint =====


def should_show_workflow_hint(state: dict, now: Optional[datetime] = None) -> bool:
    tip = state.get("workflow_hint", {})
    if tip.get("completed", False):
        return False
    if tip.get("shown_count", 0) >= DEFAULT_MAX_SHOW_COUNT:
        return False
    if _is_in_cooldown(tip, "cooldown_until", now):
        return False
    return True


def mark_workflow_hint_shown(
    state: dict, cooldown_days: int = DEFAULT_WORKFLOW_TIP_COOLDOWN_DAYS
) -> dict:
    state = _normalize_state(state)
    tip = state["workflow_hint"]
    tip["shown_count"] = tip.get("shown_count", 0) + 1
    tip["last_shown_at"] = _format_time(_utc_now())
    tip["cooldown_until"] = _cooldown_until(cooldown_days)
    return state


def mark_workflow_used(state: dict) -> dict:
    state = _normalize_state(state)
    state["workflow_hint"]["completed"] = True
    return state


# ===== usage counters =====


def record_news_success(state: dict, scope: str = "latest") -> dict:
    """Record news fetch success, update usage counter"""
    state = _normalize_state(state)
    counters = state["usage_counters"]

    if scope == "latest":
        counters["latest_news_success_count"] = counters.get("latest_news_success_count", 0) + 1
    elif scope == "date":
        counters["date_news_success_count"] = counters.get("date_news_success_count", 0) + 1

    # Record first success time
    if not state.get("first_successful_news_at"):
        state["first_successful_news_at"] = _format_time(_utc_now())

    return state


def select_growth_tip(state: dict, preferences_set: bool = False) -> Optional[str]:
    """
    Select which growth tip type should be shown currently.

    Returns: "onboarding", "preference", "automation", "workflow", or None
    """
    # Priority: onboarding > preference > automation > workflow
    if should_show_onboarding_tip(state):
        return "onboarding"

    if not preferences_set and should_show_preference_hint(state):
        return "preference"

    # automation only shown when user has a certain usage frequency
    usage_count = (
        state.get("usage_counters", {}).get("latest_news_success_count", 0)
        + state.get("usage_counters", {}).get("date_news_success_count", 0)
    )
    if usage_count >= 2 and should_show_automation_hint(state):
        return "automation"

    if usage_count >= 3 and should_show_workflow_hint(state):
        return "workflow"

    return None


def mark_tip_shown(state: dict, tip_type: str) -> dict:
    """
    Unified entry point: Mark a tip as shown and enter cooldown.

    tip_type: "onboarding", "preference", "automation", "workflow"
    """
    if tip_type == "onboarding":
        return mark_onboarding_tip_shown(state)
    elif tip_type == "preference":
        return mark_preference_hint_shown(state)
    elif tip_type == "automation":
        return mark_automation_hint_shown(state)
    elif tip_type == "workflow":
        return mark_workflow_hint_shown(state)
    return state
