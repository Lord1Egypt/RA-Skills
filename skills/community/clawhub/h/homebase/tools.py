#!/usr/bin/env python3
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
from typing import Any, Dict

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)

# ─── Interpreter self-heal ───────────────────────────────────────────────────
# When the OpenClaw daemon spawns an agent, its bash PATH is
# /opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin — `python3`
# there resolves to /usr/bin/python3 (CommandLineTools), which has none of this
# skill's dependencies. Re-exec under the homebase venv so a tool behaves the
# same however it was launched.
#
# The canary was `keyring` until 2026-09-07, because the failure it caught was
# core/keychain_secrets.py silently returning empty GOOGLE_* values and callers
# then reporting "credentials missing" — a false alarm DMed to the owner.
# Credentials moved to gog and keyring went with them, so the canary is now
# pypdf: still venv-only, and still something a bill fetch genuinely needs.
_VENV_PY = os.path.join(SKILL_DIR, ".venv", "bin", "python")
if os.path.realpath(sys.executable) != os.path.realpath(_VENV_PY) and os.path.exists(_VENV_PY):
    try:
        import pypdf  # noqa: F401
    except ImportError:
        os.execv(_VENV_PY, [_VENV_PY] + sys.argv)


# ─── Tool Implementations ─────────────────────────────────────────────────────

def _format_time_12h(t: str) -> str:
    """Convert a stored 'HH:MM' (or the 'All day' / '00:00' sentinels) to a
    friendly 12-hour display string, e.g. '14:30' -> '2:30 PM'."""
    if t in ("00:00", "All day"):
        return "All day"
    h, m = map(int, t.split(":"))
    ampm = "AM" if h < 12 else "PM"
    h = h % 12 or 12
    return f"{h}:{m:02d} {ampm}"


def _format_events_list(events: list, header_label: str) -> str:
    # Events with no title (e.g. a work calendar whose org policy strips
    # summaries from synced busy blocks) carry no information worth
    # showing — the time slot is still tracked internally for conflict
    # checks (see recommender._busy_blocks_for_date), just never displayed.
    events = [e for e in events if e.get("title") != "Untitled"]
    if not events:
        return f"📅 No events on {header_label} — enjoy the free day! 🎉"
    lines = [f"📅 *Events — {header_label}*\n"]
    for e in events:
        display = _format_time_12h(e.get("time", "All day"))
        lines.append(f"  • {e['title']} at {display}")
    return "\n".join(lines)


def _format_kids_meals(meals_by_kid: dict, header: str) -> str:
    from core.config_loader import config
    lines = [f"🍽️ *Kids Meal Plan — {header}*\n"]
    for kid in config.kids:
        key = kid.name.lower()
        data = meals_by_kid.get(key, {})
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


def get_meal_suggestions() -> str:
    from features.meals.meal_tracker import MealTracker
    meals = MealTracker(SKILL_DIR)
    suggestions = meals.get_meal_suggestions()
    return _format_kids_meals(suggestions, "Today")


def get_kids_meals(date: str = None) -> str:
    """
    Return the kids' meal plan for a specific date (YYYY-MM-DD), or today
    if `date` is omitted. Reads the LOCKED weekly plan — the actual
    approved menu for that day — by resolving the date to a weekday key
    in code. Use this for "what are the kids eating <day>" questions;
    do NOT read weekly_meal_plan.json directly or use get_meal_suggestions
    (that returns rotation suggestions, not the approved plan for a
    specific day, and doesn't accept a date).
    """
    from datetime import datetime
    from features.meals.weekly_meal_planner import get_meals_for_date
    if date:
        try:
            parsed = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return f"❌ Invalid date: {date!r}. Use YYYY-MM-DD."
    else:
        parsed = datetime.now()
        date = parsed.strftime("%Y-%m-%d")
    meals_by_kid = get_meals_for_date(date)
    if not meals_by_kid:
        return f"🤔 No locked meal plan covers {parsed.strftime('%A, %B %d')}."
    return _format_kids_meals(meals_by_kid, parsed.strftime("%A, %B %d"))


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
    - Non-empty change_request      → does NOT apply the change. Returns a
      "NEEDS_REVISION: ..." instruction with the current plan; you must
      build the revised plan yourself and call save_meal_plan directly.

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

    Python handles no WA delivery — the agent composes and replies.

    This used to shell out to `python -m features.briefing.morning_briefing
    --data-only`, paying an interpreter start plus a re-import of the Google
    client stack to reach a plain importable function in the same package.
    (The `--data-only` flag was decorative: that module's __main__ never read
    sys.argv.) The module keeps its __main__ for the launchd runner; this
    tool calls the function.
    """
    import json as _json
    import logging
    from features.briefing.morning_briefing import get_briefing_data
    from utils import time_limit
    try:
        # 120s: the bound the subprocess used to carry, lost when this stopped
        # shelling out. googleapiclient's 60s default is per REQUEST, which a
        # paginated sync multiplies, so without a ceiling a hung Google call
        # holds the launchd runner open with nothing to report.
        with time_limit(120):
            return _json.dumps(get_briefing_data(), indent=2, default=str)
    except Exception as e:
        logging.error("[morning_briefing] failed: %s", e, exc_info=True)
        return f"❌ Briefing failed: {str(e)[:120]}"


def get_travel_status(date: str = None, sync: bool = False) -> str:
    """
    Whether the household is away on `date` (default today), and where.

    Returns `{"away": false}` at home, or when away:
    `{"away": true, "destination": "Seattle, WA", "start": ..., "end": ...,
      "day": 3, "of": 9, "last_day": false, "title": "Trip to Seattle"}`.

    Driven by an all-day calendar event spanning the trip — `Trip to Seattle`
    with location `Seattle, WA` — because the calendar is the only surface both
    the OpenClaw agent and the launchd runners already read. See
    features/trips/travel_window.py for why it is not a state file.

    Pass sync=True for a cold call; the briefing tools leave it False because
    they have already synced in the same run.
    """
    from features.trips.travel_window import travel_status_json
    return travel_status_json(date=date, sync=sync)


def get_message_targets() -> str:
    """
    The household's delivery targets and the ids a caller needs to act on its
    behalf. Returns JSON:
    `{"owner": "...@s.whatsapp.net", "group": "...@g.us", "group_name": "...",
      "alert_webhook": "https://ntfy.sh/..." | null,
      "calendar_id": "...@group.calendar.google.com" | null}`.

    Exists so callers outside this skill never keep their own copy of the
    family's phone number and group id. They are config.json's to own — a
    second copy in a runner's config drifts the day the group changes.

    `calendar_id` is here for the same reason and one more: runners call `gog`
    directly for calendar work, and gog defaults to the account's *primary*
    calendar — a personal one — when no id is given, reading or writing the
    wrong calendar while exiting 0. Resolving it here means the id never has
    to be written into a tracked runner file to be available.

    `alert_webhook` is an out-of-band failure channel, and the reason it is
    here rather than in a caller's own config is the same one: workspace/ has
    a GitHub remote and claude-runners/*/config.env is tracked, while this file
    is gitignored in both repos. It is deliberately NOT a WhatsApp target —
    the whole point is that it does not travel over the gateway, so it still
    reaches somebody when the gateway is what broke.

    Normalizes whatever shape config.json holds (bare digits, +E164, or a full
    jid) into a sendable jid.
    """
    import json as _json
    from core.config_loader import config

    def as_jid(value, domain):
        if not value:
            return None
        value = str(value).strip()
        if "@" in value:
            return value
        return f"{value.lstrip('+')}@{domain}"

    raw = getattr(config, "_data", None) or {}
    app = raw.get("app") or {}
    wa = raw.get("whatsapp") or {}

    return _json.dumps({
        "owner":         as_jid(app.get("owner_phone"), "s.whatsapp.net"),
        "group":         as_jid(wa.get("group_id"), "g.us"),
        "group_name":    wa.get("group_name"),
        "alert_webhook": (raw.get("alerts") or {}).get("ntfy_url"),
        "calendar_id":   (raw.get("calendar") or {}).get("id"),
    })


def get_weather_context(start_hour: int = 8, end_hour: int = 17,
                        location: str = None, date: str = None) -> str:
    """
    Hourly conditions across the school-day window, plus UV index, air quality
    and sun times. Returns JSON.

    Use this for "what should the kids wear" rather than get_weather: the daily
    high is usually a mid-afternoon number that says nothing about an 8am
    drop-off, and it carries no UV or air-quality reading at all. The
    morning-to-midday swing is what decides whether to send a layer.

    `date` (YYYY-MM-DD) targets a specific day; defaults to today. The evening
    brief passes tomorrow.

    Returns {"status": "unavailable"} rather than raising if the upstream API
    is down — callers should degrade to get_weather, not abort.
    """
    import json as _json
    from features.briefing.weather import fetch_weather_context
    data = fetch_weather_context(start_hour=start_hour, end_hour=end_hour,
                                 location=location, date=date)
    if not data:
        return _json.dumps({"status": "unavailable"})
    return _json.dumps(data, separators=(",", ":"))


def get_evening_prep() -> str:
    """
    Tomorrow's calendar + kids' meals as structured JSON, for the evening
    brief composer to reason over "what has to happen tonight" — pack,
    defrost, sign, charge, set an alarm.

    Weather is fetched separately (see get_weather_context with date=), same
    split as the morning brief. This tool stays a pure calendar+meals
    composer. School snacks are provided by the school on site, so they are
    not part of the evening decision.
    """
    import json as _json
    from datetime import datetime, timedelta
    from features.calendar.calendar_aggregator import FamilyCalendarAggregator
    from features.school.snack_manager import SnackManager
    from features.meals.weekly_meal_planner import get_meals_for_date

    target = datetime.now() + timedelta(days=1)
    date_iso = target.strftime("%Y-%m-%d")

    agg = FamilyCalendarAggregator(SKILL_DIR)
    # The "evening calendar sync" SKILL.md refers to: this is where a dinner on
    # the calendar gets auto-logged, so a receipt photographed later that night
    # merges into it rather than creating a second visit.
    agg.sync_with_google_calendar(detect_restaurants=True, force=True)

    from features.trips.travel_window import get_travel_window
    travel = get_travel_window(date_iso, list(agg.calendar.values()))

    # Resolved before the loop because the projection below drops `id`, so the
    # trip event can only be recognised while the raw event is still in hand.
    # It is a state, not a thing to pack for, and `travel` already says it —
    # it reaches this list on departure eve only, where the message is about
    # the flight rather than the abstraction containing it.
    travel_event_id = travel.get("event_id") or None

    events = []
    early_start_hour = None
    for event in sorted(agg.get_events_by_date(date_iso),
                        key=lambda e: e.get("time") or ""):
        if event.get("title") in (None, "", "Untitled"):
            continue
        if travel_event_id and event.get("id") == travel_event_id:
            continue
        events.append({
            "title":       event.get("title"),
            "time":        event.get("time"),
            "end_time":    event.get("end_time"),
            "description": (event.get("description") or "")[:1500],
        })
        t = event.get("time")
        if t and t not in ("00:00", "All day"):
            try:
                h = int(t.split(":")[0])
                if h < 9 and (early_start_hour is None or h < early_start_hour):
                    early_start_hour = h
            except (ValueError, IndexError):
                pass

    school_day = not SnackManager(SKILL_DIR).is_school_closed(date_iso) and not travel["away"]

    # The locked meal plan is a plan for cooking at home. Away, "take the
    # chicken out to defrost" is advice about a fridge in another state, so the
    # plan is withheld rather than left for the composer to second-guess.
    #
    # Departure eve is the exception, and `at_destination` is what names it:
    # tomorrow the family wakes up here, in this kitchen, and leaves later.
    # That night is a home night with a flight after it — the last one on which
    # anything can be prepared properly.
    away_tomorrow = travel.get("at_destination", False)
    kids_meals = None if away_tomorrow else get_meals_for_date(date_iso)

    return _json.dumps({
        "date":             target.strftime("%A, %B %d"),
        "date_iso":         date_iso,
        "weekday":          target.strftime("%A"),
        "events":           events,
        "school_day":       school_day,
        "kids_meals":       kids_meals,
        "early_start_hour": early_start_hour,
        "travel":           travel,
    }, separators=(",", ":"))


def get_school_roster() -> str:
    """
    Return who the school writes about: the school's name, and for each kid the
    teacher names and classroom sender address used to attribute an email to a
    child. Callers that classify school mail need this and should not carry
    their own copy — these are real names and addresses, and config.json is the
    only place they are allowed to live (principle 9).

    Returns JSON: {"school": str, "kids": [{"name", "teachers", "email_sender"}]}.
    """
    import json as _json
    from core.config_loader import config
    return _json.dumps({
        "school": config.school_name,
        "kids": [
            {
                "name": k.name,
                "teachers": k.teachers,
                "email_sender": k.email_sender,
            }
            for k in config.kids
        ],
    }, separators=(",", ":"))


def fetch_school_emails(count: int = 5) -> str:
    """
    Fetch the most recent school emails including extracted PDF text and image paths.
    Returns JSON list of {id, subject, date, sender, body, pdf_text, image_paths}.
    The agent uses this to identify and add calendar events.
    """
    import json as _json
    from features.school.school_email_monitor import SchoolEmailMonitor
    from features.school.school_calendar_sync import (
        download_image_attachments, cleanup_old_attachments,
    )
    from core.pdf_attachments import extract_pdf_attachments

    attachments_dir = os.path.join(SKILL_DIR, "attachments")
    cleanup_old_attachments(attachments_dir)

    monitor = SchoolEmailMonitor(SKILL_DIR)
    emails = monitor.fetch_recent_school_emails(skip_processed=True)[:count]
    if not emails:
        # An empty list and a broken token used to look identical from here.
        # The fetch records why it failed instead of printing a WhatsApp
        # message onto the front of this JSON, so say which it was.
        if monitor.auth_status:
            payload = {"status": monitor.auth_status,
                       "error": monitor.auth_detail,
                       "emails": []}
            # Only the FIRST auth failure carries text: the fetch sets
            # auth_message and persists the "already notified" flag in the same
            # breath, so the alert is single-use. Dropping it here spent that
            # one shot on a caller that never saw it, and every later run then
            # stayed silent by design — a revoked token produced no
            # notification, ever.
            if monitor.auth_message:
                payload["summary"] = monitor.auth_message
            return _json.dumps(payload)
        return "[]"

    results = []
    for e in emails:
        pdf_texts = []
        image_paths = []

        if e.get("has_pdf_attachment"):
            pdf_texts = extract_pdf_attachments(e["id"], e.get("_payload", {}))

        if e.get("has_inline_image"):
            image_paths = download_image_attachments(
                e["id"], e.get("_payload", {}), attachments_dir
            )

        results.append({
            "id":          e.get("id"),
            "subject":     e.get("subject"),
            "date":        e.get("date"),
            "sender":      e.get("sender"),
            "body":        e.get("body", "")[:4000],
            "pdf_text":    "\n\n".join(pdf_texts)[:4000],
            "image_paths": image_paths,
        })

    return _json.dumps(results, indent=2)


def mark_email_synced(email_id: str) -> str:
    """Mark an email as processed so it won't be checked for calendar events again."""
    from features.school.school_email_monitor import SchoolEmailMonitor
    monitor = SchoolEmailMonitor(SKILL_DIR)
    monitor._mark_processed(email_id)
    monitor.mark_calendar_synced(email_id)
    return f"✅ Email {email_id} marked as synced."


def fetch_bill_emails(count: int = 1) -> str:
    """
    Fetch ONE recent bill email (from a configured biller in
    config.json's bills.billers[]). Returns JSON of {status, count,
    emails:[...], target} where each email is {id, subject, sender, date,
    biller_name, body, has_pdf, pdf_unreadable, pdf_text} and target is
    {jid, name} for the
    primary family WhatsApp group (or null if unconfigured) — the caller
    posts the polished summary there.

    `has_pdf` means a PDF was ATTACHED, not that it was readable.
    `pdf_unreadable` means one was attached but yielded no text (a scan, or a
    reader failure) — treat that as notice-only rather than claiming usage
    detail you do not have. So: has_pdf and not pdf_unreadable is a full
    statement (pdf_text carries the amounts, usage and tier table); everything
    else is notice-only, with `body` all there is. All are real bills; only
    the full statement can be summarized for consumption.
    Mail from a biller that is not a bill at all — outage alert, marketing,
    payment receipt — also comes back here now, and it is the caller's job to
    recognize and drop it.

    Hard-capped to one email per call, matching the school-email-monitor
    pattern that works around gemma4:26b's silent-stop-after-first-item
    failure mode.

    **This does not mark anything processed.** Call `mark_bill_processed`
    with the email's id once the summary has actually been delivered. Until
    you do, the same bill comes back on the next call — which is what makes
    a failed send retryable instead of losing the bill.

    The caller is responsible for reading pdf_text and composing a
    high-level consumption summary plus tips genuinely grounded in that
    text — no summarization or tip generation happens in Python.
    """
    import json as _json
    from features.bills.watcher import BillsWatcher

    # Enforce the hard cap regardless of caller.
    count = 1

    watcher = BillsWatcher(SKILL_DIR)

    if not watcher.enabled:
        return _json.dumps({"status": "disabled", "emails": [], "target": None})

    try:
        emails = watcher.fetch_emails(max_results=count * 2, take=count)
    except Exception as e:
        # `auth_failed` stays the status the runner keys on — bills/run.sh
        # treats it as fatal and alerts the owner, because a broken token that
        # only got logged would hide for weeks.
        #
        # The three-way vocabulary that used to live here (env_broken /
        # no_creds / auth_failed) went with the credential probe it described.
        # It distinguished "this interpreter has no keyring" from "the secrets
        # are empty" from "Google said no" — questions about homebase's own
        # credentials, which homebase no longer has. `gog auth status` answers
        # the equivalent about gog, and gog's stderr comes through here.
        return _json.dumps({"status": "auth_failed", "error": str(e)[:300],
                            "emails": [], "target": None})

    return _json.dumps(
        {
            "status": "emails_found" if emails else "no_new_emails",
            "count": len(emails),
            "emails": emails,
            "target": watcher.family_group,
        },
        indent=2,
    )


def mark_bill_processed(email_id: str) -> str:
    """Mark a bill email as handled so it is never fetched or posted again.

    Second half of the two-phase contract described in `fetch_bill_emails`:
    fetch, deliver, then mark. This is a one-way ledger — there is no
    unmark — so only call it after the summary has genuinely been sent.
    """
    from features.bills.watcher import BillsWatcher
    watcher = BillsWatcher(SKILL_DIR)
    watcher.mark_processed(email_id)
    return f"✅ Bill {email_id} marked as processed."


# ─── School-event dedup + pending confirmation queue ─────────────────────────
#
# Flow: for each candidate event extracted from a school email, the caller
# lists existing events on that date and judges similarity, dropping
# duplicates. Since 2026-09-07 that lookup is a direct `gog calendar events`
# call in claude-runners/school/run.sh, not a homebase tool. Remaining events go into pending_school_events.json via
# save_pending_school_events(), and a proposal is posted to the family group.
# Nothing is written to Google Calendar until the family replies "yes",
# which triggers confirm_pending_school_events() — the only path that
# actually writes to the calendar, via calendar_manager.create_event().

_PENDING_SCHOOL_EVENTS_FILE = os.path.join(
    SKILL_DIR, "calendar_data", "pending_school_events.json"
)
_PENDING_MAX_AGE_DAYS = 3


def _load_pending_school_events() -> dict:
    import json as _json
    if not os.path.exists(_PENDING_SCHOOL_EVENTS_FILE):
        return {}
    try:
        with open(_PENDING_SCHOOL_EVENTS_FILE) as f:
            return _json.load(f)
    except Exception:
        return {}


def _save_pending_school_events(data: dict) -> None:
    from utils import write_json_atomic
    write_json_atomic(_PENDING_SCHOOL_EVENTS_FILE, data)


def _purge_stale_pending(data: dict) -> dict:
    """Drop entries older than _PENDING_MAX_AGE_DAYS. Mutates and returns data."""
    from datetime import datetime, timedelta
    cutoff = datetime.now() - timedelta(days=_PENDING_MAX_AGE_DAYS)
    stale = []
    for eid, entry in data.items():
        try:
            proposed_at = datetime.fromisoformat(entry.get("proposed_at", ""))
            if proposed_at < cutoff:
                stale.append(eid)
        except Exception:
            stale.append(eid)
    for eid in stale:
        del data[eid]
    return data


def save_pending_school_events(email_id: str, events: list) -> str:
    """
    Save proposed school events for family confirmation. `events` is a list
    of dicts with keys: title, date, time (optional). Overwrites any existing
    pending entry for the same email_id. Returns a short status string.
    """
    from datetime import datetime
    if not email_id:
        return "❌ save_pending_school_events: email_id required"
    if not isinstance(events, list) or not events:
        return "❌ save_pending_school_events: events must be a non-empty list"
    for ev in events:
        if not ev.get("title") or not ev.get("date"):
            return "❌ save_pending_school_events: each event needs title + date"

    data = _load_pending_school_events()
    data = _purge_stale_pending(data)
    data[email_id] = {
        "proposed_at": datetime.now().isoformat(),
        "events": events,
    }
    _save_pending_school_events(data)
    return f"✅ {len(events)} event(s) pending confirmation for email {email_id}"


def get_pending_school_events() -> str:
    """Return JSON of all pending school events, auto-purging stale entries."""
    import json as _json
    data = _load_pending_school_events()
    before = len(data)
    data = _purge_stale_pending(data)
    if len(data) != before:
        _save_pending_school_events(data)
    return _json.dumps(data, indent=2)


def confirm_pending_school_events(email_id: str = "") -> str:
    """
    Create calendar events for a pending entry and clear it.
    If email_id is empty, confirms ALL pending entries (for "add all" replies).
    Returns a summary string with per-event results.
    """
    from features.calendar.calendar_manager import create_event
    data = _load_pending_school_events()
    data = _purge_stale_pending(data)
    if not data:
        return "🤔 No pending school events to confirm."

    targets = [email_id] if email_id else list(data.keys())
    if email_id and email_id not in data:
        return f"🤔 No pending events for email {email_id}."

    created = []
    failed = []
    for eid in targets:
        entry = data.get(eid)
        if not entry:
            continue
        for ev in entry.get("events", []):
            title = ev["title"]
            date = ev["date"]
            time_str = ev.get("time") or None
            try:
                create_event(
                    title=title,
                    date_str=date,
                    time_str=time_str,
                    duration_minutes=60,
                    is_all_day=(time_str is None),
                )
                created.append(f"{title} ({date})")
            except Exception as e:
                failed.append(f"{title} ({date}): {str(e)[:80]}")
        del data[eid]

    _save_pending_school_events(data)

    lines = []
    if created:
        lines.append(f"✅ Added {len(created)} event(s):")
        lines.extend(f"  • {c}" for c in created)
    if failed:
        lines.append(f"⚠️ {len(failed)} failed:")
        lines.extend(f"  • {f}" for f in failed)
    return "\n".join(lines) if lines else "🤔 Nothing to add."


def reject_pending_school_events(email_id: str = "") -> str:
    """Drop a pending entry (or all pending entries) without creating events."""
    data = _load_pending_school_events()
    if not data:
        return "🤔 No pending school events."
    if email_id:
        if email_id not in data:
            return f"🤔 No pending events for email {email_id}."
        count = len(data[email_id].get("events", []))
        del data[email_id]
        _save_pending_school_events(data)
        return f"🗑️ Dropped {count} pending event(s) for email {email_id}."
    total = sum(len(v.get("events", [])) for v in data.values())
    _save_pending_school_events({})
    return f"🗑️ Dropped {total} pending event(s) across {len(data)} email(s)."


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
    from features.briefing.weather import fetch_weather
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
            "get_meal_suggestions":         lambda: get_meal_suggestions(),
            "get_kids_meals":               lambda: get_kids_meals(**args),
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
            "get_weather_context":          lambda: get_weather_context(**args),
            "get_message_targets":          lambda: get_message_targets(),
            "get_evening_prep":             lambda: get_evening_prep(),
            "get_school_roster":            lambda: get_school_roster(),
            "fetch_school_emails":          lambda: fetch_school_emails(**args),
            "fetch_bill_emails":             lambda: fetch_bill_emails(**args),
            "mark_email_synced":            lambda: mark_email_synced(**args),
            "save_pending_school_events":    lambda: save_pending_school_events(**args),
            "get_pending_school_events":     lambda: get_pending_school_events(),
            "confirm_pending_school_events": lambda: confirm_pending_school_events(**args),
            "reject_pending_school_events":  lambda: reject_pending_school_events(**args),
            # Kid profiles & trip prep
            "log_kid_observation":          lambda: log_kid_observation(**args),
            "get_kid_profile":              lambda: get_kid_profile(**args),
            "get_trip_prep":                lambda: get_trip_prep(**args),
            "get_travel_status":            lambda: get_travel_status(**args),
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
            "mark_bill_processed":      lambda: mark_bill_processed(**args),
        })
        # Discovery. `❌ Unknown tool: X` on its own is a dead end: the caller
        # cannot tell a typo from a tool that never existed, and the only way
        # out was reading a 53KB source file in 100-line slices. On 2026-09-08
        # the agent invented `check_school_emails`, got the bare error, tried
        # `tools.py --help` (which lands here too, as tool "--help"), got the
        # same bare error, and spent four minutes on it before the turn died.
        if name in ("--help", "-h", "help", "list", "list_tools"):
            return ("Usage: tools.py <tool> '<json_args>'\n"
                    "       tools.py <tool> - <<'JSONEOF'   (args on stdin)\n\n"
                    f"{len(dispatch)} tools:\n  " + "\n  ".join(sorted(dispatch)))
        if name not in dispatch:
            import difflib as _difflib
            close = _difflib.get_close_matches(name, dispatch, n=3, cutoff=0.5)
            hint = f" Did you mean: {', '.join(close)}?" if close else ""
            return (f"❌ Unknown tool: {name}.{hint}\n"
                    f"Run `tools.py --help` for all {len(dispatch)} tool names.")
        return dispatch[name]()
    except Exception as e:
        return f"❌ {name} failed: {str(e)[:100]}"


# ─── Native-mode data tools (no LLM — the OpenClaw agent does the reasoning) ──

def _normalize_snack(text) -> str:
    """Case- and whitespace-insensitive form, for comparing two extractions."""
    return " ".join(str(text or "").split()).lower()


def save_snack_schedule(month: int, year: int, type: str, days: list,
                        force: bool = False) -> str:
    """Save a snack schedule extracted by the agent from a photo.

    Refuses a write whose column would come out a near-copy of the column
    already stored for the same dates. That is the fingerprint of the same
    photo being read twice, not of a school menu — see the collision guard
    below.
    """
    from features.school.snack_manager import SnackManager
    from datetime import datetime as _dt

    if type not in ("morning", "afternoon"):
        return ("❌ save_snack_schedule: type must be exactly 'morning' or "
                f"'afternoon' (got {type!r}). Anything else used to be "
                "silently written as afternoon.")

    other = "afternoon" if type == "morning" else "morning"
    mgr   = SnackManager(SKILL_DIR)

    # Build the whole result first. Nothing is written until the collision
    # guard below has had a look at it.
    staged     = {}
    count      = 0
    closed     = 0
    comparable = 0
    identical  = []
    for entry in days:
        try:
            day      = int(entry["day"])
            date_str = f"{int(year)}-{int(month):02d}-{int(day):02d}"
            existing = dict(mgr.schedule.get(date_str, {
                "morning": "", "afternoon": "", "school_closed": False
            }))
            incoming = entry.get(type, "")
            existing[type] = incoming
            is_closed = bool(entry.get("school_closed")) or bool(
                existing.get("school_closed"))
            if entry.get("school_closed"):
                existing["school_closed"] = True
                closed += 1
            existing["updated_at"] = _dt.now().isoformat()
            staged[date_str] = existing
            count += 1
            # A closed day legitimately carries the same "No School" text in
            # both columns, so it proves nothing either way.
            prior_other = _normalize_snack(
                mgr.schedule.get(date_str, {}).get(other, ""))
            if not is_closed and prior_other and _normalize_snack(incoming):
                comparable += 1
                if _normalize_snack(incoming) == prior_other:
                    identical.append(date_str)
        except (ValueError, KeyError):
            continue

    # ─── Collision guard ─────────────────────────────────────────────────
    # A school does not print a month where every morning snack equals that
    # day's afternoon snack; two reads of the SAME photo do. On 2026-09-08 the
    # agent re-ran `view_image` against the afternoon calendar's path while
    # asking for "the morning snack schedule", got the afternoon items back
    # under a "Morning" heading, and saved them over a correct morning column
    # it had already stored 9 minutes earlier. The duplicate was visible in
    # this function's own success message and was waved off twice, so the
    # check has to fail the write rather than warn about it.
    if identical and not force and len(identical) >= 3 \
            and len(identical) >= 0.6 * comparable:
        sample = ", ".join(identical[:3])
        return ("❌ *Refused — this looks like the same photo read twice.*\n"
                f"{len(identical)} of {comparable} days would end up with "
                f"identical {type} and {other} snacks (e.g. {sample}).\n"
                f"Check that the image path you passed to `view_image` is the "
                f"{type.upper()} calendar and not the {other} one — they are "
                "separate photos with separate staged paths. Re-read the right "
                "file, or pass \"force\": true if the menu really is identical.")

    for date_str, entry in staged.items():
        mgr.schedule[date_str] = entry
    mgr._save()

    lines = ["✅ *Snack schedule saved!*",
             f"📅 {type.title()} snacks for {year}-{month:02d}",
             f"📝 {count} days loaded"]
    if closed:
        lines.append(f"🚫 {closed} school closure(s) noted")
    if identical:
        lines.append(f"⚠️ {len(identical)} day(s) have identical {type} and "
                     f"{other} snacks — verify against the photo")
    today_snack = mgr.format_for_briefing()
    if today_snack:
        lines.append(f"\n{today_snack}")
    return "\n".join(lines)


def get_pending_meal_plan() -> str:
    """Return the current pending meal plan as JSON for the agent to inspect/revise."""
    import json as _json
    from features.meals.weekly_meal_planner import load_pending
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

    # No credential bootstrap here any more (2026-09-07). This used to load
    # GOOGLE_* from Keychain before any tool imported them, because a plain
    # `python3 tools.py <action>` shell session had no credentials while the
    # daemon-spawned context did — so CLI debugging failed with "missing
    # credentials" against a production path that was fine. gog resolves its
    # own token per invocation, so both contexts behave identically and there
    # is nothing to preload.

    if len(_sys.argv) < 2:
        print("Usage: tools.py <action> [json_args]")
        print("Example: tools.py get_morning_briefing")
        print("Example: tools.py add_to_grocery_list '{\"items\":[\"milk\"],\"store\":\"costco\"}'")
        _sys.exit(1)

    _action = _sys.argv[1]
    _args   = {}
    _sender = ""

    if len(_sys.argv) > 2 and _sys.argv[2] == "-":
        # Explicit stdin sentinel — read json_args from stdin instead of argv.
        # Lets the caller heredoc extracted text past the shell entirely,
        # avoiding single-quote breakage on apostrophes (e.g. "Cheez It's").
        # Opt-in only: every other invocation form is untouched, so this
        # can't hang a zero-arg call on stdin that the exec host never closes.
        _stdin_data = _sys.stdin.read().strip()
        try:
            _args = _json.loads(_stdin_data)
        except _json.JSONDecodeError as _e:
            print(f"❌ Invalid JSON args on stdin: {_e}")
            _sys.exit(1)
    elif len(_sys.argv) > 2 and _sys.argv[2] in ("--help", "-h", "help"):
        # Per-tool signature. The agent's natural discovery move is
        # `tools.py <tool> --help`, which used to land in the JSON parser and
        # come back "Invalid JSON args" — so on 2026-09-10 a single
        # add_to_grocery_list call cost seven exec calls: three guessed kwargs
        # (item, name), this dead --help, an inline-python introspection
        # attempt, and a grep of this file. A signature is the cheapest thing
        # that ends that loop, and unlike prose in a doc it cannot be skipped.
        import inspect as _inspect
        _fn = globals().get(_action)
        if not callable(_fn):
            print(execute_tool("--help", {}))
            _sys.exit(0)
        print(f"{_action}{_inspect.signature(_fn)}")
        _doc = _inspect.getdoc(_fn)
        if _doc:
            print(f"\n{_doc}")
        _params = [p for p in _inspect.signature(_fn).parameters.values()
                   if p.name != "sender"]
        if _params:
            _ex = {}
            for _p in _params:
                if _p.default is _inspect.Parameter.empty:
                    # `from __future__ import annotations` makes every
                    # annotation a STRING, so compare by name, not identity.
                    _ann = _p.annotation
                    _ann = getattr(_ann, "__name__", _ann)
                    _ex[_p.name] = ({"list": [], "int": 0, "float": 0.0,
                                     "bool": False}.get(str(_ann), "..."))
            print(f"\nExample: tools.py {_action} '{_json.dumps(_ex)}'")
        _sys.exit(0)
    elif len(_sys.argv) > 2:
        try:
            _args = _json.loads(_sys.argv[2])
        except _json.JSONDecodeError as _e:
            print(f"❌ Invalid JSON args: {_e}\n"
                  f"Run `tools.py {_action} --help` for this tool's signature.")
            _sys.exit(1)

    # sender is optional 3rd arg (phone number for rate_restaurant context)
    if len(_sys.argv) > 3:
        _sender = _sys.argv[3]

    _result = execute_tool(_action, _args, sender=_sender)
    print(_result)
