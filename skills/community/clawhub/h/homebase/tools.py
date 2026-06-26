"""
tools.py — Household Assistant Tool Library

Pure data tools called by the OpenClaw agent via bash:
    python3 tools.py <action> '<json_args>'

Each tool:
  - Reads or writes household data (calendar, meals, grocery, health, etc.)
  - Returns a formatted string ready to return verbatim to WhatsApp
  - Contains NO LLM calls — the OpenClaw agent (whichever model is configured)
    is the intelligence layer. Homebase is model-agnostic.

To add a new tool:
  1. Add a function here with a clear docstring
  2. Add it to execute_tool() dispatch table
  3. Document it in agent.md
"""

from __future__ import annotations
import os
import sys
from typing import Any, Dict, Optional

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)

# ─── Interpreter self-heal ───────────────────────────────────────────────────
# When the OpenClaw daemon spawns a cron-triggered agent, the agent's bash PATH
# (set by ~/Library/LaunchAgents/com.openclaw.daemon.plist) is
# /opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin — `python3` on
# that PATH resolves to /usr/bin/python3 (CommandLineTools) which has no
# `keyring` module. The result is that core/keychain_secrets.py silently
# returns empty strings for GOOGLE_*, callers misreport "credentials missing,"
# and false-alarm DMs go out to the owner. Re-exec under the homebase venv
# python whenever keyring is unavailable so every tool that imports keychain
# state gets the right interpreter, regardless of how it was launched.
_VENV_PY = os.path.join(SKILL_DIR, ".venv", "bin", "python")
if os.path.realpath(sys.executable) != os.path.realpath(_VENV_PY) and os.path.exists(_VENV_PY):
    try:
        import keyring  # noqa: F401
    except ImportError:
        os.execv(_VENV_PY, [_VENV_PY] + sys.argv)


# ─── Tool Implementations ─────────────────────────────────────────────────────

def get_todays_events() -> str:
    from features.calendar.calendar_aggregator import FamilyCalendarAggregator
    agg = FamilyCalendarAggregator(SKILL_DIR)
    agg.sync_with_google_calendar()
    events = agg.get_events_for_today()
    if not events:
        return "📅 No events today — enjoy the free day! 🎉"
    from datetime import datetime
    today = datetime.now().strftime("%A, %B %d")
    lines = [f"📅 *Today's Events — {today}*\n"]
    for e in events:
        t = e.get("time", "All day")
        if t in ("00:00", "All day"):
            display = "All day"
        else:
            h, m = map(int, t.split(":"))
            ampm = "AM" if h < 12 else "PM"
            h = h % 12 or 12
            display = f"{h}:{m:02d} {ampm}"
        lines.append(f"  • {e['title']} at {display}")
    return "\n".join(lines)


def add_calendar_event(title: str, date: str, time: str = None,
                       duration: int = 60) -> str:
    from features.calendar.calendar_manager import create_event
    result = create_event(title=title, date_str=date, time_str=time,
                          duration_minutes=duration, is_all_day=(time is None))
    time_display = f" at {time}" if time else " (all day)"
    return f"✅ *Event created!*\n\n📅 {title}\n📆 {date}{time_display}\n_Added to family calendar_"


def delete_calendar_event(title: str) -> str:
    from features.calendar.calendar_manager import delete_event
    success, result = delete_event(title)
    if success:
        return f"🗑️ Deleted *{result}* from the calendar."
    return f"🤔 {result}"


def update_calendar_event(search_title: str, new_date: str = None,
                          new_time: str = None, new_title: str = None) -> str:
    from features.calendar.calendar_manager import update_event
    success, result = update_event(search_title, new_title, new_date, new_time)
    if success:
        parts = []
        if new_date: parts.append(new_date)
        if new_time: parts.append(f"at {new_time}")
        if new_title: parts.append(f"renamed to '{new_title}'")
        detail = " ".join(parts) if parts else "updated"
        return f"✅ *{result}* → {detail}"
    return f"🤔 {result}"


def get_meal_suggestions() -> str:
    from features.meals.meal_tracker import MealTracker
    from core.config_loader import config
    meals = MealTracker(SKILL_DIR)
    suggestions = meals.get_meal_suggestions()
    lines = ["🍽️ *Kids Meal Plan*\n"]
    for kid in config.kids:
        key = kid.name.lower()
        data = suggestions.get(key, {})
        if not data:
            continue
        lines.append(f"{kid.emoji_char} *{kid.name}*")
        lines.append(f"  Breakfast: {data.get('breakfast', 'TBD')}")
        lines.append(f"  Lunch: {data.get('lunch', 'TBD')}")
        lines.append(f"  Side: {data.get('side', 'TBD')}")
        if data.get("note"):
            lines.append(f"  {data['note']}")
        lines.append("")
    return "\n".join(lines)


def log_kids_meal(child: str, meal_type: str, food: str) -> str:
    from features.meals.meal_tracker import MealTracker
    from datetime import datetime
    meals    = MealTracker(SKILL_DIR)
    today    = datetime.now().strftime("%Y-%m-%d")
    in_cat, _ = meals.log_meal(child.lower(), meal_type, food.title(), today)
    base = (
        f"✅ Logged *{child.title()}*: {food.title()} ({meal_type})\n"
        "_I'll use this to vary tomorrow's suggestions._"
    )
    if not in_cat:
        base += "\n_(New menu item — added to the catalog review queue.)_"
    return base


def get_snack_schedule() -> str:
    from features.school.snack_manager import SnackManager
    snacks = SnackManager(SKILL_DIR)
    if snacks.is_school_closed_today():
        return "🏫 No school today — no snack schedule."
    result = snacks.format_for_briefing()
    return result if result else "🍎 No snack schedule loaded for today."


def get_grocery_list(store: str = None) -> str:
    from features.shopping.shopping_list import ShoppingList
    sl = ShoppingList(SKILL_DIR)
    return sl.format_for_whatsapp(store_filter=store)


def add_to_grocery_list(items: list, store: str = "general",
                        quantity: int = 1) -> str:
    from features.shopping.shopping_list import ShoppingList, STORE_LABELS
    sl    = ShoppingList(SKILL_DIR)
    added = []
    for item in items:
        sl.add(item, quantity, store)
        added.append(item.title())
    store_label = STORE_LABELS.get(store, store.title())
    if len(added) == 1:
        return f"✅ Added *{added[0]}* → {store_label}"
    items_str = ", ".join(f"*{i}*" for i in added)
    return f"✅ Added {items_str} → {store_label}"


def remove_from_grocery_list(items: list) -> str:
    from features.shopping.shopping_list import ShoppingList
    sl      = ShoppingList(SKILL_DIR)
    removed = []
    missing = []
    for item in items:
        if sl.remove(item):
            removed.append(item.title())
        else:
            missing.append(item.title())
    lines = []
    if removed:
        lines.append("✅ Removed: " + ", ".join(f"*{i}*" for i in removed))
    if missing:
        lines.append("🤔 Not on list: " + ", ".join(missing))
    return "\n".join(lines) if lines else "🤔 Nothing to remove."


def log_restaurant_visit(restaurant: str, meal_type: str = None,
                         date: str = None, items: list = None,
                         total: float = None) -> str:
    from features.dining.restaurant_tracker import log_visit, format_visit_confirmation, detect_meal_type
    meal = meal_type or detect_meal_type()
    visit = log_visit(restaurant=restaurant, date=date, meal_type=meal,
                      items=items or [], total=total, source="manual")
    return format_visit_confirmation(visit)


def rate_restaurant(rating: int, restaurant: str = None,
                    notes: str = "", sender: str = "") -> str:
    from features.dining.restaurant_tracker import add_rating, load_data, FAMILY_MEMBERS
    sender_name = FAMILY_MEMBERS.get(sender, "")
    # Auto-find most recent unrated if no restaurant specified
    if not restaurant and sender_name:
        data = load_data()
        for v in reversed(data["visits"]):
            if sender_name not in v.get("individual_ratings", {}):
                restaurant = v["restaurant"]
                break
    if not restaurant:
        data = load_data()
        unrated = [v for v in reversed(data["visits"]) if not v.get("rating")]
        if unrated:
            restaurant = unrated[0]["restaurant"]
        else:
            return "🤔 No unrated visits found. Which restaurant?"
    ok, result = add_rating(restaurant=restaurant, rating=rating,
                            notes=notes, sender=sender)
    if ok:
        stars = "⭐" * rating
        name_str = f" ({sender_name})" if sender_name else ""
        return f"✅ Rated *{result}* {stars}{name_str}"
    return f"🤔 {result}"


def get_restaurant_recommendations(meal_type: str = None) -> str:
    from features.dining.restaurant_tracker import get_recommendations, format_recommendations
    recs = get_recommendations(meal_type)
    return format_recommendations(recs, meal_type)


def get_top_restaurants() -> str:
    from features.dining.restaurant_tracker import format_top_list
    return format_top_list()


def handle_meal_plan_response(change_request: str = "") -> str:
    """
    Route a WhatsApp reply to the pending weekly meal plan draft.

    - Empty / falsy change_request  → approve and lock the plan.
    - Non-empty change_request      → apply the change, resend revised plan.

    If no plan is pending, returns a friendly no-op message.
    """
    from features.meals.weekly_meal_planner import load_pending, cmd_approve, cmd_revise
    pending = load_pending()
    if not pending:
        return "No meal plan is waiting for approval right now."

    if change_request and change_request.strip():
        return cmd_revise(change_request.strip())
    else:
        return cmd_approve()


def get_morning_briefing() -> str:
    """
    Return structured briefing data as JSON for the agent to compose.
    Uses --data-only so Python handles no WA delivery — the agent composes and replies.
    """
    import subprocess, logging
    # Use sys.executable so the child inherits the venv python (with keyring),
    # not whatever bare `python3` happens to resolve to on the daemon's PATH.
    result = subprocess.run(
        [sys.executable, "-m", "features.briefing.morning_briefing", "--data-only"],
        capture_output=True, text=True,
        cwd=SKILL_DIR, timeout=120
    )
    if result.returncode == 0:
        return result.stdout.strip()
    err_snippet = (result.stderr or result.stdout or "no output").strip()[:500]
    logging.error("[morning_briefing] failed (exit %d): %s", result.returncode, err_snippet)
    return f"❌ Briefing failed: {err_snippet[:120]}"


def fetch_school_emails(count: int = 5) -> str:
    """
    Fetch the most recent school emails including extracted PDF text.
    Returns JSON list of {id, subject, date, sender, body, pdf_text}.
    The agent uses this to identify and add calendar events.
    """
    import json as _json
    from features.school.school_email_monitor import SchoolEmailMonitor
    from features.school.school_calendar_sync import extract_pdf_attachments

    monitor = SchoolEmailMonitor(SKILL_DIR)
    emails = monitor.fetch_recent_school_emails(skip_processed=False)[:count]
    if not emails:
        return "[]"

    gmail_svc = monitor.get_gmail_service()
    results = []
    for e in emails:
        pdf_texts = []
        if e.get("has_pdf_attachment") and gmail_svc:
            pdf_texts = extract_pdf_attachments(gmail_svc, e["id"], e.get("_payload", {}))

        results.append({
            "id":      e.get("id"),
            "subject": e.get("subject"),
            "date":    e.get("date"),
            "sender":  e.get("sender"),
            "body":    e.get("body", "")[:4000], # Cap size
            "pdf_text": "\n\n".join(pdf_texts)[:4000]
        })

    return _json.dumps(results, indent=2)


def mark_email_synced(email_id: str) -> str:
    """Mark an email as processed so it won't be checked for calendar events again."""
    from features.school.school_email_monitor import SchoolEmailMonitor
    monitor = SchoolEmailMonitor(SKILL_DIR)
    monitor.calendar_synced_ids.add(email_id)
    monitor._save_calendar_synced_ids()
    return f"✅ Email {email_id} marked as synced."


def sync_school_calendar() -> str:
    """
    Deprecated: Manually trigger a school email → Google Calendar sync.
    New flow: Agent calls fetch_school_emails and then add_calendar_event.
    """
    return "⚠️ This tool is deprecated. Use fetch_school_emails instead."


def log_medication(child: str, medication: str,
                   dose_mg: float = None, dose_ml: float = None,
                   timestamp: str = None) -> str:
    from features.health.health_tracker import log_medication as _log_medication
    return _log_medication(child=child, medication=medication,
                           dose_mg=dose_mg, dose_ml=dose_ml,
                           timestamp=timestamp)


def log_fever(child: str, temp_f: float = None,
              subjective: bool = False, timestamp: str = None) -> str:
    from features.health.health_tracker import log_fever as _log_fever
    return _log_fever(child=child, temp_f=temp_f,
                      subjective=subjective, timestamp=timestamp)


def log_symptom(child: str, symptoms: str, timestamp: str = None) -> str:
    from features.health.health_tracker import log_symptom as _log_symptom
    return _log_symptom(child=child, symptoms=symptoms, timestamp=timestamp)


def get_health_summary(child: str, days: int = 3) -> str:
    from features.health.health_tracker import get_health_summary as _get_health_summary
    return _get_health_summary(child=child, days=days)


def update_child_weight(child: str, weight_kg: float) -> str:
    from features.health.health_tracker import update_child_weight as _update_child_weight
    return _update_child_weight(child=child, weight_kg=weight_kg)


def schedule_medication_reminder(child: str, medication: str,
                                  remind_at: str) -> str:
    from features.health.health_tracker import schedule_medication_reminder as _schedule_reminder
    return _schedule_reminder(child=child, medication=medication,
                              remind_at=remind_at)


def log_kid_observation(child: str, text: str, category: str = "general",
                        tags: list = None, trip_context: str = None) -> str:
    from features.trips.trip_detector import log_kid_observation as _log_obs
    return _log_obs(child=child, text=text, category=category,
                    tags=tags or [], trip_context=trip_context or None)


def get_kid_profile(child: str) -> str:
    from features.trips.trip_detector import get_kid_profile as _get_profile
    return _get_profile(child=child)


def get_trip_prep(event_title: str, location: str) -> str:
    from features.trips.trip_detector import run_manual
    return run_manual(event_title=event_title, location=location)


def get_weather() -> str:
    """
    Return structured weather data (HTTP only, no LLM).
    The agent composes the clothing suggestion itself from this data.
    Fast HTTP-only path — safe to call before assembling the briefing.
    """
    from features.briefing.weather import fetch_weather, weather_code_to_description
    from core.config_loader import config
    weather = fetch_weather()
    if not weather:
        return "🌤️ Weather unavailable right now."
    rain_note = (
        f"\n  ☂️ {weather['rain_chance']}% chance of rain — pack an umbrella"
        if weather["rain_chance"] >= 40 else ""
    )
    return (
        f"🌤️ *Weather — {config.city or 'Local'}*\n"
        f"  {weather['condition']}, {weather['temp_current']}°F "
        f"(feels like {weather['temp_feels_like']}°F)\n"
        f"  High {weather['temp_high']}°F / Low {weather['temp_low']}°F | "
        f"Wind {weather['wind_speed']} mph | Humidity {weather['humidity']}%"
        f"{rain_note}"
    )


# ─── Config-aware store keywords (used by shopping_list) ─────────────────────

def get_store_keywords():
    """Return store keyword mapping from config."""
    try:
        from core.config_loader import config
        return config.all_store_keywords
    except Exception:
        return {}  # Fallback to defaults in shopping_list.py



# ─── Tool Executor ────────────────────────────────────────────────────────────

def execute_tool(name: str, args: Dict[str, Any],
                 sender: str = "") -> str:
    """
    Execute a tool by name with given arguments.
    Returns formatted string response.
    Passes sender to tools that need it (e.g. rate_restaurant).
    """
    try:
        dispatch = {
            "get_todays_events":            lambda: get_todays_events(),
            "add_calendar_event":           lambda: add_calendar_event(**args),
            "delete_calendar_event":        lambda: delete_calendar_event(**args),
            "update_calendar_event":        lambda: update_calendar_event(**args),
            "get_meal_suggestions":         lambda: get_meal_suggestions(),
            "log_kids_meal":                lambda: log_kids_meal(**args),
            "get_snack_schedule":           lambda: get_snack_schedule(),
            "get_grocery_list":             lambda: get_grocery_list(**args),
            "add_to_grocery_list":          lambda: add_to_grocery_list(**args),
            "remove_from_grocery_list":     lambda: remove_from_grocery_list(**args),
            "log_restaurant_visit":         lambda: log_restaurant_visit(**args),
            "rate_restaurant":              lambda: rate_restaurant(**args, sender=sender),
            "get_restaurant_recommendations": lambda: get_restaurant_recommendations(**args),
            "get_top_restaurants":          lambda: get_top_restaurants(),
            "handle_meal_plan_response":    lambda: handle_meal_plan_response(**args),
            "get_morning_briefing":         lambda: get_morning_briefing(),
            "get_weather":                  lambda: get_weather(),
            "sync_school_calendar":         lambda: sync_school_calendar(),
            "fetch_school_emails":          lambda: fetch_school_emails(**args),
            "mark_email_synced":            lambda: mark_email_synced(**args),
            # Kid profiles & trip prep
            "log_kid_observation":          lambda: log_kid_observation(**args),
            "get_kid_profile":              lambda: get_kid_profile(**args),
            "get_trip_prep":                lambda: get_trip_prep(**args),
            # Health tracker
            "log_medication":               lambda: log_medication(**args),
            "log_fever":                    lambda: log_fever(**args),
            "log_symptom":                  lambda: log_symptom(**args),
            "get_health_summary":           lambda: get_health_summary(**args),
            "update_child_weight":          lambda: update_child_weight(**args),
            "schedule_medication_reminder": lambda: schedule_medication_reminder(**args),
        }
        dispatch.update({
            # New native-mode tools
            "save_snack_schedule":      lambda: save_snack_schedule(**args),
            "get_pending_meal_plan":    lambda: get_pending_meal_plan(),
            "approve_meal_plan":        lambda: handle_meal_plan_response(change_request=""),
            "save_meal_plan":           lambda: save_meal_plan(**args),
            "get_meal_history":         lambda: get_meal_history(**args),
            "get_weekly_meal_pool":     lambda: get_weekly_meal_pool(**args),
            "get_pending_catalog_reviews": lambda: get_pending_catalog_reviews(),
            "apply_catalog_review":     lambda: apply_catalog_review(**args),
            "get_trip_data":            lambda: get_trip_data(**args),
            "mark_trip_prep_sent":      lambda: mark_trip_prep_sent(**args),
            "draft_meal_plan":          lambda: draft_meal_plan(),
            "get_morning_meal_checkin_text": lambda: get_morning_meal_checkin_text(),
        })
        if name not in dispatch:
            return f"❌ Unknown tool: {name}"
        return dispatch[name]()
    except Exception as e:
        return f"❌ {name} failed: {str(e)[:100]}"


# ─── Native-mode data tools (no LLM — the OpenClaw agent does the reasoning) ──

def save_snack_schedule(month: int, year: int, type: str, days: list) -> str:
    """Save a snack schedule extracted by the agent from a photo."""
    from features.school.snack_manager import SnackManager
    mgr   = SnackManager(SKILL_DIR)
    count = 0
    closed = 0
    for entry in days:
        try:
            day      = int(entry["day"])
            date_str = f"{int(year)}-{int(month):02d}-{int(day):02d}"
            existing = mgr.schedule.get(date_str, {
                "morning": "", "afternoon": "", "school_closed": False
            })
            if type == "morning":
                existing["morning"] = entry.get("morning", "")
            else:
                existing["afternoon"] = entry.get("afternoon", "")
            if entry.get("school_closed"):
                existing["school_closed"] = True
                closed += 1
            from datetime import datetime as _dt
            existing["updated_at"] = _dt.now().isoformat()
            mgr.schedule[date_str] = existing
            count += 1
        except (ValueError, KeyError):
            continue
    mgr._save()
    lines = [f"✅ *Snack schedule saved!*",
             f"📅 {type.title()} snacks for {year}-{month:02d}",
             f"📝 {count} days loaded"]
    if closed:
        lines.append(f"🚫 {closed} school closure(s) noted")
    today_snack = mgr.format_for_briefing()
    if today_snack:
        lines.append(f"\n{today_snack}")
    return "\n".join(lines)


def get_pending_meal_plan() -> str:
    """Return the current pending meal plan as JSON for the agent to inspect/revise."""
    import json as _json
    from features.meals.weekly_meal_planner import load_pending, PENDING_FILE
    pending = load_pending()
    if not pending:
        return '{"status": "no_pending_plan"}'
    return _json.dumps({"status": "pending", "plan": pending}, indent=2)


def save_meal_plan(plan: dict, revision: int = 0) -> str:
    """Save an agent-generated or agent-revised meal plan as pending.

    Validates every menu pick against the kid's resolved catalog before
    writing. If the plan contains items not in the catalog, returns a
    structured ❌ error string the agent should reply with verbatim. If
    the plan is valid except for lunch/breakfast egg conflicts, those are
    auto-corrected and the corrections appended to the formatted output.

    NOTE: This function does NOT send anything to WhatsApp. It writes the
    pending file and returns the formatted text. The agent layer is
    responsible for posting the returned text to the family group via
    ``openclaw message send``. Per CLAUDE.md principle #7, no Python
    function in this skill ever sends WhatsApp directly.
    """
    from features.meals.meal_tracker import MealTracker
    from features.meals.weekly_meal_planner import save_pending, format_plan_for_whatsapp
    tracker = MealTracker(SKILL_DIR)
    result  = tracker.validate_plan(plan)
    if not result.get("ok"):
        errs = result.get("errors") or ["unknown validation error"]
        # Cap the error string so it stays WhatsApp-readable
        return "❌ Plan rejected:\n" + "\n".join(f"  • {e}" for e in errs[:6])

    save_pending(plan, revision=revision)
    formatted = format_plan_for_whatsapp(plan, revision=revision)
    corrections = result.get("corrections") or []
    if corrections:
        lines = ["", "_Auto-corrections:_"]
        for c in corrections[:6]:
            lines.append(
                f"_• {c['day'].capitalize()} {c['kid'].capitalize()} "
                f"{c['slot']}: {c['from']} → {c['to']}_"
            )
        formatted = formatted + "\n" + "\n".join(lines)
    return formatted


def get_weekly_meal_pool(days: int = 7) -> str:
    """Return the per-day, per-kid, per-slot menu pool as JSON.

    The agent picks exactly one item from each list to compose a weekly
    plan and then calls ``save_meal_plan``. Constraints are not pre-applied;
    ``save_meal_plan``'s validator handles them.
    """
    import json as _json
    from features.meals.meal_tracker import MealTracker
    tracker = MealTracker(SKILL_DIR)
    return _json.dumps(tracker.get_weekly_pool(days=days), indent=2)


def get_pending_catalog_reviews() -> str:
    """Return the catalog-pending list as JSON for the agent to format/ask about."""
    import json as _json
    from features.meals.meal_tracker import MealTracker
    tracker = MealTracker(SKILL_DIR)
    return _json.dumps({"pending": tracker.get_pending_reviews()}, indent=2)


def apply_catalog_review(decisions: list) -> str:
    """Apply a structured list of catalog accept/reject decisions.

    Args:
      decisions: list of {"index": <int>, "decision": "accept"|"reject"}.
        Indices refer to the current pending list (zero-based).

    The Python validator rejects the entire batch if any index is out of
    range, duplicated, or has an unknown decision. This is the
    defense-in-depth safeguard against the agent fabricating approvals
    for nonexistent items.
    """
    import json as _json
    from features.meals.meal_tracker import MealTracker
    tracker = MealTracker(SKILL_DIR)
    result  = tracker.apply_catalog_decisions(decisions or [])
    if not result.get("ok"):
        return f"❌ {result.get('error', 'unknown error')}"
    added    = result.get("added", [])
    rejected = result.get("rejected", [])
    parts = []
    if added:
        parts.append(f"✅ Added {len(added)} item(s) to the catalog:")
        for a in added:
            parts.append(f"  • {a['kid'].capitalize()} {a['slot']}: {a['meal']}")
    if rejected:
        parts.append(f"🗑️ Rejected {len(rejected)} item(s).")
    return "\n".join(parts) if parts else "Nothing to apply."


def get_meal_history(days: int = 14) -> str:
    """Return recent meal log as JSON — used by the agent to generate a varied weekly plan."""
    import json as _json
    from features.meals.meal_tracker import MealTracker
    from datetime import datetime as _dt, timedelta as _td
    tracker = MealTracker(SKILL_DIR)
    cutoff  = (_dt.now() - _td(days=days)).strftime("%Y-%m-%d")
    recent  = {d: v for d, v in tracker.history.items() if d >= cutoff}
    return _json.dumps(recent, indent=2) if recent else "{}"


def get_trip_data(event_title: str, location: str) -> str:
    """
    Return structured trip data (profiles + env tags + weather) as JSON.
    The agent uses this to compose the trip prep message — no LLM called here.
    """
    import json as _json
    from datetime import datetime as _dt, timedelta as _td
    from features.trips.trip_detector import (
        load_kid_profiles, fetch_trip_weather,
        infer_environment_tags,
    )
    profiles  = load_kid_profiles()
    env_tags  = infer_environment_tags(event_title, location)
    today     = _dt.now().strftime("%Y-%m-%d")
    in4       = (_dt.now() + _td(days=4)).strftime("%Y-%m-%d")
    weather   = fetch_trip_weather(location, today, in4)
    return _json.dumps({
        "trip_title": event_title,
        "location":   location,
        "env_tags":   env_tags,
        "weather":    weather,
        "profiles":   {k: v.get("observations", []) for k, v in profiles.items()},
    }, indent=2)


def mark_trip_prep_sent(trip_title: str, trip_date: str, sent_key: str = "") -> str:
    """Mark a trip prep message as sent so it won't be re-sent by the cron job."""
    from features.trips.trip_detector import mark_sent
    key = sent_key or f"manual::{trip_date}"
    mark_sent(key, trip_title, trip_date)
    return f"✅ Trip prep marked as sent for {trip_title} ({trip_date})"


def get_morning_meal_checkin_text() -> str:
    """Return the canonical 'what did the kids eat?' check-in question.

    Pure data — no LLM, no I/O beyond reading config. The OpenClaw agent
    reads stdout and posts the text to the family group itself via
    `openclaw message send --channel whatsapp --target <jid> --message "..."`
    (per CLAUDE.md rule #6 + #7). The agent's own reply stays `NO_REPLY` so
    no chain-of-thought leaks. This Python helper is the single source of
    truth for the wording — no Python file in this skill ever sends
    WhatsApp messages directly.
    """
    from core.config_loader import config
    names = config.kid_names
    if not names:
        who = "the kids"
    elif len(names) == 1:
        who = names[0]
    elif len(names) == 2:
        who = f"{names[0]} and {names[1]}"
    else:
        who = ", ".join(names[:-1]) + f", and {names[-1]}"
    return (
        f"Hey! 👋 Quick check-in — what did {who} end up having for "
        f"breakfast and lunch today? Tracking favorites so I can tune "
        f"tomorrow's suggestions. 🍽️"
    )


def draft_meal_plan() -> str:
    """
    Generate a new weekly meal plan draft.
    Returns the formatted plan text. The agent delivers it via OpenClaw.
    """
    from features.meals.meal_tracker import MealTracker
    from core.config_loader import config
    tracker = MealTracker(SKILL_DIR)
    suggestions = tracker.get_meal_suggestions()
    if not suggestions:
        return "❌ No kids configured — can't generate meal plan"
    import json as _json
    return _json.dumps({"status": "draft", "suggestions": suggestions}, indent=2, default=str)


# ─── CLI entry point — called by the OpenClaw agent via bash ─────────────────

if __name__ == "__main__":
    import json as _json
    import sys as _sys
    import warnings as _warnings

    # Suppress environment-specific warnings (Python 3.9 EOL, OpenSSL, etc.)
    # to prevent them from leaking into the agent's WhatsApp responses.
    _warnings.filterwarnings("ignore")

    # Populate Google OAuth env vars from Keychain or .env BEFORE any tool
    # imports them. The OpenClaw daemon-spawned cron context calls this at
    # startup; running `python3 tools.py <action>` from a plain shell did
    # not, which made every CLI debug session fail with "missing credentials"
    # even though the production cron path was fine. The keychain_secrets
    # loader already handles both sources (Keychain preferred, .env fallback)
    # and is the canonical entry point for this skill.
    try:
        from core.keychain_secrets import load_google_secrets
        load_google_secrets()
    except Exception:
        # CLI helper — never fail tool execution because credential bootstrap
        # itself raised. The downstream tool will surface a clearer error.
        pass

    if len(_sys.argv) < 2:
        print("Usage: tools.py <action> [json_args]")
        print("Example: tools.py get_todays_events")
        print("Example: tools.py add_to_grocery_list '{\"items\":[\"milk\"],\"store\":\"costco\"}'")
        _sys.exit(1)

    _action = _sys.argv[1]
    _args   = {}
    _sender = ""

    if len(_sys.argv) > 2:
        try:
            _args = _json.loads(_sys.argv[2])
        except _json.JSONDecodeError as _e:
            print(f"❌ Invalid JSON args: {_e}")
            _sys.exit(1)

    # sender is optional 3rd arg (phone number for rate_restaurant context)
    if len(_sys.argv) > 3:
        _sender = _sys.argv[3]

    _result = execute_tool(_action, _args, sender=_sender)
    print(_result)
