#!/usr/bin/env python3
"""
weekly_meal_planner.py — Weekly Meal Plan Draft + Approval Flow

The OpenClaw agent composes the per-kid weekly plan by picking from the
deterministic menu pool returned by ``MealTracker.get_weekly_pool``. This
file owns the pending/locked file lifecycle (`save_pending`, `lock_plan`,
`cmd_approve`, etc.) and a Python-side fallback `generate_weekly_plan`
that uses the same resolver — useful for tests and CLI smoke runs.

Per CLAUDE.md #2, this file never sends WhatsApp directly: every command
function returns a formatted string, the agent layer delivers it.
"""

import json
import os
import random
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from core.config_loader import config, SKILL_DIR
from features.meals.meal_tracker import MealTracker, _apply_constraints
from utils import write_json_atomic

HOUSEHOLD_DIR = os.path.join(SKILL_DIR, "household")
PENDING_FILE  = os.path.join(HOUSEHOLD_DIR, "meal_plan_pending.json")
LOCKED_FILE   = os.path.join(HOUSEHOLD_DIR, "weekly_meal_plan.json")

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

MAX_REVISIONS = 2   # After 2 rounds of changes, auto-lock


def _pick_avoiding(options: List[str], used: List[str]) -> str:
    """Pick from options, preferring items not already used this week."""
    fresh = [o for o in options if o not in used]
    pool = fresh if fresh else options
    return random.choice(pool) if pool else "TBD"


def generate_weekly_plan() -> Dict:
    """
    Python-side fallback weekly plan generator.

    Builds a full Mon–Sun plan for all kids by picking from the resolver
    pool returned by ``MealTracker.get_weekly_pool``. Honors lunch
    constraints relative to the picked breakfast on the same day. Used by
    the CLI ``draft`` command and the test suite; the production cron job
    has the OpenClaw agent compose the plan instead and call
    ``save_meal_plan`` directly.
    """
    tracker = MealTracker(SKILL_DIR)
    pool = tracker.get_weekly_pool(days=len(DAYS))
    kids = config.kids
    include_dinner = config.include_dinner
    dinner_options = config.dinner_options

    # Seed with recent history to avoid carry-over from last week
    kid_used = {}
    for kid in kids:
        name = kid.name.lower()
        kid_used[name] = {
            "breakfast": list(tracker.get_recent_meals(name, "breakfast", days=3)),
            "lunch": list(tracker.get_recent_meals(name, "lunch", days=3)),
        }

    used_dinners: List[str] = []
    plan: Dict[str, dict] = {}

    for day in DAYS:
        day_plan: Dict[str, dict] = {}

        # Pick shared family dinner for this day (same for all kids)
        family_dinner = None
        if include_dinner and dinner_options:
            family_dinner = _pick_avoiding(dinner_options, used_dinners)
            used_dinners.append(family_dinner)

        for kid in kids:
            name        = kid.name.lower()
            day_pool    = pool.get(day, {}).get(name, {})
            breakfast_options = day_pool.get("breakfast", [])
            lunch_options_raw = day_pool.get("lunch", [])
            side_options      = day_pool.get("sides", []) or ["Fruit"]
            constraints       = list((kid.slot("lunch").get("constraints") or []))

            breakfast = _pick_avoiding(breakfast_options, kid_used[name]["breakfast"])
            lunch_pool = _apply_constraints(lunch_options_raw, constraints, breakfast)
            lunch = _pick_avoiding(lunch_pool or lunch_options_raw, kid_used[name]["lunch"])
            side  = random.choice(side_options) if side_options else "Fruit"

            note = ""
            if "egg" in (breakfast or "").lower() and "no_eggs_at_lunch_if_eggs_at_breakfast" in constraints:
                note = "Had eggs for breakfast"

            kid_used[name]["breakfast"].append(breakfast)
            kid_used[name]["lunch"].append(lunch)

            entry = {
                "breakfast": breakfast,
                "lunch":     lunch,
                "side":      side,
                "note":      note,
            }

            if include_dinner and family_dinner:
                dinner = family_dinner
                if "egg" in (breakfast or "").lower() and "egg" in dinner.lower():
                    alt = _pick_avoiding(
                        [d for d in dinner_options if "egg" not in d.lower()],
                        used_dinners,
                    )
                    dinner = alt
                entry["dinner"] = dinner

            day_plan[name] = entry

        plan[day] = day_plan

    return plan


def format_plan_for_whatsapp(plan: Dict, revision: int = 0, is_final: bool = False) -> str:
    """Format the weekly plan JSON into a WhatsApp message."""
    today = datetime.now()
    week_label = (today + timedelta(days=(7 - today.weekday()) % 7)).strftime("%b %d")
    include_dinner = config.include_dinner

    if is_final:
        header = f"✅ *Meal Plan Locked — Week of {week_label}*"
    elif revision == 0:
        header = (
            f"📋 *Draft Meal Plan — Week of {week_label}*\n"
            f"_Reply \"looks good\" to lock it in, or suggest any changes._"
        )
    else:
        remaining = MAX_REVISIONS - revision
        header = (
            f"📋 *Revised Plan (round {revision + 1}) — Week of {week_label}*\n"
            f"_Reply \"looks good\" to approve. {remaining} more revision(s) allowed._"
        )

    meal_labels = "Breakfast | Lunch | Dinner" if include_dinner else "Breakfast | Lunch"
    lines = [header, ""]

    for day in DAYS:
        lines.append(f"📅 *{day.capitalize()}*")
        day_plan = plan.get(day, {})
        for kid_key, meals in day_plan.items():
            if include_dinner and meals.get("dinner"):
                line = f"  • {kid_key.capitalize()}: {meals.get('breakfast')} | {meals.get('lunch')} | {meals.get('dinner')}"
            else:
                line = f"  • {kid_key.capitalize()}: {meals.get('breakfast')} | {meals.get('lunch')}"
            lines.append(line)
        lines.append("")

    if not is_final:
        lines.append(f"_Format: {meal_labels}_")
        lines.append("_Auto-approves Sunday 9 PM if no reply. 🔒_")

    return "\n".join(lines)


def load_pending() -> Optional[Dict]:
    if not os.path.exists(PENDING_FILE): return None
    with open(PENDING_FILE, "r") as f:
        data = json.load(f)
    return data if data.get("status") == "pending" else None


def save_pending(plan: Dict, revision: int = 0):
    os.makedirs(HOUSEHOLD_DIR, exist_ok=True)
    now = datetime.now()

    # Auto-approve deadline: Sunday 9 PM (gives family all weekend to review)
    today = now.date()
    days_until_sun = (6 - today.weekday()) % 7  # 6 = Sunday
    if days_until_sun == 0 and now.hour >= 21:
        days_until_sun = 7  # already past Sunday 9 PM, target next Sunday
    sunday = today + timedelta(days=days_until_sun)
    expires_at = datetime.combine(sunday, datetime.min.time()).replace(
        hour=21, minute=0, second=0, microsecond=0
    )

    payload = {
        "status": "pending",
        "revision": revision,
        "plan": plan,
        "sent_at": now.isoformat(),
        "expires_at": expires_at.isoformat(),
    }
    write_json_atomic(PENDING_FILE, payload)


def lock_plan(plan: Dict, reason: str = "family_approved"):
    os.makedirs(HOUSEHOLD_DIR, exist_ok=True)

    today = datetime.now().date()
    days_until_monday = (7 - today.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7
    week_start = today + timedelta(days=days_until_monday)

    locked_data = {
        "week_of": week_start.strftime("%Y-%m-%d"),
        "locked_at": datetime.now().isoformat(),
        "locked_reason": reason,
        "plan": plan,
    }
    write_json_atomic(LOCKED_FILE, locked_data)

    # Mark pending as approved
    if os.path.exists(PENDING_FILE):
        with open(PENDING_FILE, "r") as f:
            pending = json.load(f)
        pending["status"] = "approved"
        write_json_atomic(PENDING_FILE, pending)


def apply_revision(plan: Dict, change_request: str) -> Dict:
    """
    Stub — revisions are handled natively by the OpenClaw agent.
    Returns the plan unchanged; the agent applies the change and calls save_meal_plan directly.
    """
    return plan


def cmd_draft() -> str:
    """
    Generate a new draft meal plan and return the formatted message.
    The OpenClaw agent reads stdout and delivers the message to the family
    group itself — Python does not send WhatsApp messages directly.
    """
    plan = generate_weekly_plan()
    save_pending(plan, revision=0)
    return format_plan_for_whatsapp(plan, revision=0)


def cmd_approve() -> str:
    """
    Lock in the current pending plan after family approval and return the
    locked plan as a formatted message. The agent layer delivers it.
    """
    pending = load_pending()
    if not pending:
        return "No pending meal plan to approve."

    plan = pending["plan"]
    lock_plan(plan, reason="family_approved")
    return format_plan_for_whatsapp(plan, is_final=True)


def cmd_revise(change_request: str) -> str:
    """
    Apply a family change request, save the revised plan, and return the
    revised message. The agent layer delivers it.
    """
    pending = load_pending()
    if not pending:
        return "No pending meal plan to revise."

    revision = pending.get("revision", 0)

    if revision >= MAX_REVISIONS:
        plan = pending["plan"]
        lock_plan(plan, reason="max_revisions_reached")
        message = format_plan_for_whatsapp(plan, is_final=True)
        message += "\n\n_Max revision rounds reached — plan locked in as-is. 🔒_"
        return message

    original_plan = pending["plan"]
    revised_plan = apply_revision(original_plan, change_request)
    new_revision = revision + 1

    save_pending(revised_plan, revision=new_revision)
    return format_plan_for_whatsapp(revised_plan, revision=new_revision)


def cmd_auto_approve() -> str:
    """
    Auto-approve the pending plan at 9 PM Sunday if no family response received.
    Called by the Sunday 9 PM scheduled task. Returns the locked message; the
    agent layer delivers it to the family group.
    """
    pending = load_pending()
    if not pending:
        return "No pending meal plan."

    plan = pending["plan"]
    lock_plan(plan, reason="auto_approved_timeout")
    message = format_plan_for_whatsapp(plan, is_final=True)
    message += "\n\n_Auto-approved — no changes requested by Sunday 9 PM. 🔒_"
    return message


def get_todays_meals_from_locked_plan() -> Optional[Dict]:
    """
    Returns the meal plan for the current day from the locked file,
    if it exists and is for the current week.
    """
    if not os.path.exists(LOCKED_FILE):
        return None

    try:
        with open(LOCKED_FILE, "r") as f:
            data = json.load(f)

        week_of = data.get("week_of")
        if not week_of:
            return None

        week_start = datetime.strptime(week_of, "%Y-%m-%d").date()
        week_end = week_start + timedelta(days=6)
        today = datetime.now().date()

        if not (week_start <= today <= week_end):
            return None

        plan = data.get("plan", {})
        today_name = today.strftime("%A").lower()
        return plan.get(today_name)
    except Exception:
        return None


if __name__ == "__main__":
    # Top-level guard so cron always exits cleanly with a parseable status.
    import traceback as _tb
    if len(sys.argv) < 2:
        print("Usage: weekly_meal_planner.py draft|approve|revise|auto-approve|status")
        sys.exit(1)
    try:
        cmd = sys.argv[1].lower()
        if cmd == "draft":
            print(cmd_draft())
        elif cmd == "approve":
            print(cmd_approve())
        elif cmd == "revise":
            if len(sys.argv) < 3:
                print("Usage: weekly_meal_planner.py revise '<change request>'")
                sys.exit(1)
            print(cmd_revise(sys.argv[2]))
        elif cmd == "auto-approve":
            print(cmd_auto_approve())
        elif cmd == "status":
            pending = load_pending()
            print("PENDING" if pending else "NONE")
        else:
            print(f"Unknown command: {cmd}")
            sys.exit(1)
    except Exception as _e:
        print(json.dumps({
            "status": "crashed",
            "command": sys.argv[1] if len(sys.argv) > 1 else "",
            "error": str(_e),
            "traceback": _tb.format_exc(),
        }, indent=2))
        sys.exit(1)
