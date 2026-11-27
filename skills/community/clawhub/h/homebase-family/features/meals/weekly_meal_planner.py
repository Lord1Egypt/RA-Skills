#!/usr/bin/env python3
"""
weekly_meal_planner.py — Weekly Meal Plan Draft + Approval Flow

DEPRECATED AS A SCHEDULED FEATURE (2026-08-31). Not deleted, and not broken.

The weekly cadence this file was written for — a Saturday 6 PM draft that
the family revised by reply — ran as an OpenClaw cron job. Cron was emptied on
2026-08-17, and no launchd runner replaced it, so nothing calls `cmd_draft` on
a schedule any more. A plan locks only when a family member approves it: the
timeout lock that once ran Sunday night was removed on 2026-11-27. The code is
kept deliberately: every function still works when invoked, the tools are
still dispatchable (`draft_meal_plan`, `handle_meal_plan_response`,
`save_meal_plan`, `approve_meal_plan`), and `get_meals_for_date` is read on
every single briefing — it is the source of the kids' locked menu.

So: the *lifecycle* is live and on-demand; only the *timer* is gone. If the
cadence is ever wanted back, it is a launchd runner under
~/.openclaw/workspace/claude-runners/, not a cron job (see skill CLAUDE.md
principle 2). Do not wire these back into `openclaw cron`.

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

MAX_REVISIONS = 2   # After 2 rounds of changes, ask the family to approve as-is


# One implementation, in MealTracker. This module used to carry a second
# `_pick_avoiding` with the same name and purpose but a raw string compare,
# where MealTracker's case-folds and collapses whitespace first — so the two
# gave different answers for the same menu ("Idli Sambar" vs "idli  sambar").
_pick_avoiding = MealTracker.pick_avoiding


def generate_weekly_plan() -> Dict:
    """
    Python-side fallback weekly plan generator.

    Builds a full Mon–Sun plan for all kids by picking from the resolver
    pool returned by ``MealTracker.get_weekly_pool``. Applies lunch
    constraints relative to the picked breakfast on the same day; if the
    constraints rule out every lunch option, it falls back to the full lunch
    pool rather than leaving the slot empty. Used by
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


def _plan_week_start(today) -> str:
    """The Monday a plan made `today` is for: today on a Monday, else the
    coming one. The week is decided ONCE, when the draft is saved, and carried
    in the pending file; label and lock used to recompute it with different
    rules, so a weekend draft approved on Monday said "Week of Oct 19" and was
    stored as Oct 26 — and the week it named then had no plan."""
    return (today + timedelta(days=(7 - today.weekday()) % 7)).strftime("%Y-%m-%d")


def format_plan_for_whatsapp(plan: Dict, revision: int = 0, is_final: bool = False,
                             week_of: Optional[str] = None) -> str:
    """Format the weekly plan JSON into a WhatsApp message."""
    week_of = week_of or _plan_week_start(datetime.now().date())
    week_label = datetime.strptime(week_of, "%Y-%m-%d").strftime("%b %d")
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
        # No deadline line: nothing locks a plan on a timer. A person approves.
        lines.append("_Reply to approve or request changes. 🔒_")

    return "\n".join(lines)


def load_pending() -> Optional[Dict]:
    if not os.path.exists(PENDING_FILE): return None
    with open(PENDING_FILE, "r") as f:
        data = json.load(f)
    return data if data.get("status") == "pending" else None


def save_pending(plan: Dict, revision: int = 0) -> str:
    """Write the pending plan; returns the week it is for. A revision keeps
    the week of the draft it revises."""
    os.makedirs(HOUSEHOLD_DIR, exist_ok=True)
    now = datetime.now()
    current = load_pending() if revision > 0 else None
    week_of = (current or {}).get("week_of") or _plan_week_start(now.date())

    payload = {
        "status": "pending",
        "revision": revision,
        "plan": plan,
        "sent_at": now.isoformat(),
        "week_of": week_of,
    }
    write_json_atomic(PENDING_FILE, payload)
    return week_of


def lock_plan(plan: Dict, reason: str = "family_approved",
              week_of: Optional[str] = None):
    os.makedirs(HOUSEHOLD_DIR, exist_ok=True)

    locked_data = {
        "week_of": week_of or _plan_week_start(datetime.now().date()),
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


def cmd_draft() -> str:
    """
    Generate a new draft meal plan and return the formatted message.

    No longer called on a schedule — the Saturday 6 PM cron job that drove it
    was removed on 2026-08-17 (see module docstring). The agent's on-demand
    path is `get_weekly_meal_pool` + `save_meal_plan`, which lets the model
    compose; this is the deterministic Python fallback. The caller reads
    stdout and delivers — Python does not send WhatsApp messages directly.
    """
    plan = generate_weekly_plan()
    week_of = save_pending(plan, revision=0)
    return format_plan_for_whatsapp(plan, revision=0, week_of=week_of)


def cmd_approve() -> str:
    """
    Lock in the current pending plan after family approval and return the
    locked plan as a formatted message. The agent layer delivers it.
    """
    pending = load_pending()
    if not pending:
        return "No pending meal plan to approve."

    plan = pending["plan"]
    lock_plan(plan, reason="family_approved", week_of=pending.get("week_of"))
    return format_plan_for_whatsapp(plan, is_final=True, week_of=pending.get("week_of"))


def cmd_revise(change_request: str) -> str:
    """
    A family member asked to change the pending meal plan. Applying a
    free-text change request requires model reasoning, which does not
    belong in this Python layer (CLAUDE.md principle #2) — this does NOT
    modify or save anything. It returns the current plan plus the change
    request so the agent can construct the revised plan itself and save it
    via ``save_meal_plan(plan=..., revision=<current revision + 1>)``.
    """
    pending = load_pending()
    if not pending:
        return "No pending meal plan to revise."

    revision = pending.get("revision", 0)

    if revision >= MAX_REVISIONS:
        # Nothing locks without a person saying so. This used to lock the plan
        # as-is and drop the request, from a call documented as changing
        # nothing.
        return (
            f"MAX_REVISIONS_REACHED: nothing changed. The plan has had "
            f"{revision} revision(s), the most allowed. Tell the family the "
            f"change was not applied and ask whether to approve the current "
            f"plan as-is; lock it only if they say yes (approve_meal_plan).\n"
            f"Change requested: {change_request}"
        )

    return (
        "NEEDS_REVISION: build the revised plan yourself from the change "
        f"request and current plan below, then call save_meal_plan with "
        f"revision={revision + 1}.\n"
        f"Change requested: {change_request}\n"
        f"Current plan: {json.dumps(pending['plan'])}"
    )



def get_meals_for_date(date_str: str) -> Optional[Dict]:
    """
    Returns the meal plan for `date_str` (YYYY-MM-DD) from the locked file,
    if it exists and `date_str` falls within that plan's locked week.
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
        target = datetime.strptime(date_str, "%Y-%m-%d").date()

        if not (week_start <= target <= week_end):
            return None

        plan = data.get("plan", {})
        day_name = target.strftime("%A").lower()
        return plan.get(day_name)
    except Exception:
        return None


def get_todays_meals_from_locked_plan() -> Optional[Dict]:
    """
    Returns the meal plan for the current day from the locked file,
    if it exists and is for the current week.
    """
    return get_meals_for_date(datetime.now().strftime("%Y-%m-%d"))


if __name__ == "__main__":
    # Top-level guard so cron always exits cleanly with a parseable status.
    import traceback as _tb
    if len(sys.argv) < 2:
        print("Usage: weekly_meal_planner.py draft|approve|revise|status")
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
