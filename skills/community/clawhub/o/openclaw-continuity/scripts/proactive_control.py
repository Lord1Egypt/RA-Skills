#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Proactive Control Layer — event-driven proactive + toggle/priority chain.

This module defines:
1. Event-driven proactive triggers (from V2 event store)
2. Toggle resolution chain (which switch overrides which)
3. Priority chain for outbound source arbitration

== TOGGLE RESOLUTION (highest to lowest) ==

  1. rest_suppress      — user said going to sleep → blocks ALL proactive
  2. work_dnd           — user said in work mode → blocks ALL proactive
  3. quiet_hours        — time-based → blocks UNLESS active task hook
  4. routine_phase      — sleep/wake/active phase → phase.proactive_enabled
  5. proactive_enabled  — master on/off from settings.json
  6. followup_threshold — interval_hours + cooldown_minutes per-phase

If ANY higher-level toggle blocks, lower levels are irrelevant.

== OUTBOUND SOURCE PRIORITY (highest to lowest) ==

  1. event_driven_hook  — V2 event store: due/active events with hook params  [NEW]
  2. task_hook          — existing pending health/progress/tomorrow hooks
  3. recent_task_hook   — recently dispatched task hook holding thread
  4. emotional_hook     — existing watchful state hooks
  5. recent_emotional   — recently dispatched emotional hook holding thread
  6. proactive_chat     — arbiter-eligible proactive outreach
  7. rhythm_nudge       — inactivity-based rhythm stage
  8. cron_info          — scheduled cron info push

== EVENT-DRIVEN PROACTIVE ==

Events that can trigger proactive outreach:
  - defer         → "user said set aside; follow up when interval met"
  - wake_followup → "user said resume after sleep; trigger in wake_window"
  - checkin       → "user asked for periodic check; use next_check_at"
  - health_event  → "health incident; follow up within 2-4h"
  - emotional_event → "emotional incident; follow up within 1-2h"
  - unresolved_topic → "open thread; follow up on next active_day"

These live in the event store and produce hooks via should_auto_generate_hook().
The control layer here decides IF and WHEN those hooks should fire, respecting
the toggle chain above.

== WHAT IS SHARED vs HOST-PRIVATE ==

SHARED (this file + defaults/settings.json):
  - Toggle resolution logic
  - Priority chain order
  - Event-to-proactive mapping rules
  - Default settings (all conservative: proactive=off, rhythm=off)

HOST-PRIVATE (host settings.json, profile.json):
  - proactive_chat.enabled = true/false
  - interval_hours, quiet_hours, cooldown_minutes
  - routine_schedule times (sleep_time, wake_time)
  - Phase-specific overrides (wake_window interval = 0.5h etc)
  - max_proactive_per_day
  - Profile: chronotype, care_nudge_time, household_schedule
"""

import json
import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

__version__ = "1.0.0"


# ── Toggle Resolution ──

class ToggleResult:
    """Result of toggle chain resolution."""
    __slots__ = ("allowed", "blocked_by", "active_toggles", "effective_phase", "effective_interval_hours")

    def __init__(self):
        self.allowed: bool = True
        self.blocked_by: Optional[str] = None
        self.active_toggles: Dict[str, bool] = {}
        self.effective_phase: str = "active_day"
        self.effective_interval_hours: float = 3.0

    def block(self, reason: str):
        self.allowed = False
        self.blocked_by = reason

    def to_dict(self) -> dict:
        return {
            "allowed": self.allowed,
            "blocked_by": self.blocked_by,
            "active_toggles": self.active_toggles,
            "effective_phase": self.effective_phase,
            "effective_interval_hours": self.effective_interval_hours,
        }


def resolve_toggle_chain(
    *,
    rest_suppress: Optional[dict],
    work_dnd: Optional[dict],
    quiet_hours_blocked: bool,
    phase_name: str,
    phase_proactive_enabled: bool,
    proactive_enabled: bool,
    interval_hours: float,
    has_active_task_hook: bool = False,
) -> ToggleResult:
    """Walk the toggle chain from highest to lowest priority.

    Returns ToggleResult with allowed/blocked_by and active_toggles snapshot.
    """
    r = ToggleResult()
    r.effective_phase = phase_name
    r.effective_interval_hours = interval_hours
    r.active_toggles = {
        "rest_suppress": bool(rest_suppress),
        "work_dnd": bool(work_dnd),
        "quiet_hours_blocked": quiet_hours_blocked,
        "phase_proactive_enabled": phase_proactive_enabled,
        "proactive_enabled": proactive_enabled,
        "has_active_task_hook": has_active_task_hook,
    }

    # 1. Rest suppress — blocks everything
    if rest_suppress:
        r.block("rest_suppress")
        return r

    # 2. Work DND — blocks everything
    if work_dnd:
        r.block("work_dnd")
        return r

    # 3. Quiet hours — blocks UNLESS active task hook
    if quiet_hours_blocked and not has_active_task_hook:
        r.block("quiet_hours")
        return r

    # 4. Routine phase — phase must allow proactive
    if not phase_proactive_enabled:
        r.block("routine_phase_disabled")
        return r

    # 5. Master proactive toggle
    if not proactive_enabled:
        r.block("proactive_disabled")
        return r

    # All toggles passed
    return r


# ── Event-Driven Proactive Triggers ──

# Map event types to proactive urgency windows (hours)
EVENT_PROACTIVE_WINDOWS = {
    "health_event":       {"min_hours": 1.0, "max_hours": 4.0, "priority": "high"},
    "emotional_event":    {"min_hours": 1.0, "max_hours": 3.0, "priority": "high"},
    "defer":              {"min_hours": 2.0, "max_hours": 8.0, "priority": "medium"},
    "wake_followup":      {"min_hours": 0.0, "max_hours": 1.5, "priority": "medium"},  # fires in wake_window
    "checkin":            {"min_hours": 4.0, "max_hours": 24.0, "priority": "medium"},
    "unresolved_topic":   {"min_hours": 3.0, "max_hours": 12.0, "priority": "low"},
    "reminder_intent":    {"min_hours": 0.5, "max_hours": 2.0, "priority": "high"},
    "task_progress":      {"min_hours": 4.0, "max_hours": 24.0, "priority": "medium"},
    "life_context_event": {"min_hours": 6.0, "max_hours": 48.0, "priority": "low"},
    "identity_event":     {"min_hours": 0.0, "max_hours": 0.0, "priority": "low"},  # never triggers proactive
    "work_event":         {"min_hours": 2.0, "max_hours": 8.0, "priority": "medium"},
    "relationship_event": {"min_hours": 3.0, "max_hours": 12.0, "priority": "medium"},
    "incident":           {"min_hours": 1.0, "max_hours": 6.0, "priority": "high"},
}


def find_event_driven_proactive_candidates(
    event_store,
    now_dt: datetime,
    phase_name: str = "active_day",
) -> List[dict]:
    """Find events that should trigger proactive outreach NOW.

    Checks:
    1. Event is active/due
    2. Enough time has passed since creation (min_hours)
    3. No linked hook is still pending (avoid duplicate dispatch)
    4. wake_followup only fires in wake_window phase

    Returns list of candidate dicts sorted by priority (high first).
    """
    candidates = []
    priority_order = {"high": 0, "medium": 1, "low": 2}

    for evt in event_store.events:
        status = evt.get("status", "")
        if status not in ("active", "due"):
            continue

        etype = evt.get("event_type", "custom")
        window = EVENT_PROACTIVE_WINDOWS.get(etype)
        if not window or window["max_hours"] == 0:
            continue  # This type never triggers proactive

        # wake_followup only fires in wake_window
        if etype == "wake_followup" and phase_name != "wake_window":
            continue

        created_at = evt.get("created_at", "")
        try:
            created_dt = datetime.fromisoformat(created_at)
        except (ValueError, TypeError):
            continue

        age_hours = (now_dt - created_dt).total_seconds() / 3600
        if age_hours < window["min_hours"]:
            continue  # Too soon

        # Check if event already has a pending/active hook
        linked_hooks = evt.get("linked_hook_ids", [])
        if linked_hooks:
            # If any linked hook is still pending, skip — it will handle dispatch
            # The caller should check hook_store to verify, but we skip for safety
            continue

        candidates.append({
            "event_id": evt.get("event_id", ""),
            "event_type": etype,
            "title": evt.get("title", ""),
            "priority": window["priority"],
            "age_hours": round(age_hours, 1),
            "cause_summary": evt.get("cause_summary", ""),
            "desired_followup": evt.get("desired_followup", ""),
            "_priority_rank": priority_order.get(window["priority"], 9),
        })

    candidates.sort(key=lambda c: (c["_priority_rank"], -c["age_hours"]))
    for c in candidates:
        c.pop("_priority_rank", None)
    return candidates


# ── Priority Chain Documentation ──

PRIORITY_CHAIN = """
Outbound Source Priority Chain (highest wins):

  ┌─────────────────────────────────────────────────────────┐
  │ TOGGLE CHAIN (evaluated first, top-down)                │
  │                                                         │
  │  1. rest_suppress  → blocks ALL                         │
  │  2. work_dnd       → blocks ALL                         │
  │  3. quiet_hours    → blocks unless active task hook      │
  │  4. phase_policy   → sleep=off, wake=on, active=on      │
  │  5. proactive_on   → master switch                      │
  │  6. interval/cool  → per-phase timing                   │
  └─────────────────────────────────────────────────────────┘
          │ if all passed ↓
  ┌─────────────────────────────────────────────────────────┐
  │ SOURCE PRIORITY (first eligible wins)                   │
  │                                                         │
  │  1. event_driven   → V2 event with no linked hook       │
  │  2. task_hook      → pending health/progress/tomorrow    │
  │  3. recent_task    → recently dispatched, holding thread │
  │  4. emotional_hook → pending watchful state              │
  │  5. recent_emot    → recently dispatched emotional       │
  │  6. proactive_chat → arbiter-eligible proactive          │
  │  7. rhythm_nudge   → inactivity stage                   │
  │  8. cron_info      → scheduled push                     │
  └─────────────────────────────────────────────────────────┘

Toggle values are HOST-PRIVATE (settings.json per instance).
Priority chain order is SHARED (this module).
"""


# ── CLI ──

def main():
    import sys
    args = sys.argv[1:]
    if not args:
        print(PRIORITY_CHAIN)
        return

    cmd = args[0]
    if cmd == "chain":
        print(PRIORITY_CHAIN)
    elif cmd == "toggles":
        # Show current toggle state from a live instance
        print(json.dumps({
            "note": "Run via personal_hooks.py runtime-context for live toggle state",
            "toggle_order": [
                "1. rest_suppress (user sleep)",
                "2. work_dnd (user work mode)",
                "3. quiet_hours (time-based)",
                "4. routine_phase (sleep/wake/active)",
                "5. proactive_enabled (master switch)",
                "6. interval_hours + cooldown_minutes (timing)",
            ],
        }, ensure_ascii=False, indent=2))
    elif cmd == "event-windows":
        print(json.dumps(EVENT_PROACTIVE_WINDOWS, ensure_ascii=False, indent=2))
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
