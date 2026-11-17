#!/usr/bin/env python3
"""
Restaurant Tracker for Homebase
Logs restaurant visits via receipt photos, manual entry, or calendar events.
Tracks ratings, items ordered, and provides smart recommendations.
"""

import fcntl
import json
import os
import re
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

from core.config_loader import SKILL_DIR
from utils import write_json_atomic, locked_file

DATA_FILE      = os.path.join(SKILL_DIR, "household", "restaurants.json")

def _load_family_members():
    try:
        from core.config_loader import config
        return config.family_members_dict
    except Exception:
        return {}

FAMILY_MEMBERS = _load_family_members()

MEAL_KEYWORDS = {
    "breakfast": ["breakfast", "brunch", "morning", "eggs", "pancakes", "waffle"],
    "lunch":     ["lunch", "midday", "afternoon"],
    "dinner":    ["dinner", "evening", "night", "supper"],
}


# ─── Data Management ──────────────────────────────────────────────────────────

def load_data() -> Dict:
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            try:
                return json.load(f)
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
    return {"visits": [], "pending_ratings": {}}


def save_data(data: Dict):
    write_json_atomic(DATA_FILE, data)


# ─── Meal Type Detection ──────────────────────────────────────────────────────

def detect_meal_type(text: str = "", time_str: str = None) -> str:
    """Detect meal type from text context or time of day."""
    text_lower = text.lower()
    for meal, keywords in MEAL_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return meal

    if time_str:
        try:
            hour = int(time_str.split(':')[0])
            if 5 <= hour < 11:  return "breakfast"
            if 11 <= hour < 15: return "lunch"
            if 15 <= hour < 22: return "dinner"
        except Exception:
            pass

    # Default to current time
    hour = datetime.now().hour
    if 5 <= hour < 11:  return "breakfast"
    if 11 <= hour < 15: return "lunch"
    return "dinner"


# ─── Receipt Photo Parsing ────────────────────────────────────────────────────
# In native OpenClaw mode, the agent reads receipt photos directly using its
# native vision capability. The agent extracts the fields and calls
# tools.py log_restaurant_visit to save. parse_receipt_photo() has been removed.


# ─── Log Visit ────────────────────────────────────────────────────────────────

def log_visit(restaurant: str, date: str = None, meal_type: str = None,
              items: List[str] = None, total: float = None,
              source: str = "manual") -> Dict:
    """Log a restaurant visit, or enrich the existing one for the same meal.

    Three callers reach this for what is often the same dinner: the calendar
    auto-detector fires the evening before with nothing but a name, the agent
    logs a receipt photo later that night with items and a total, and someone
    may also say "we ate at X" in chat. Appending each one left two or three
    visits and two or three rating prompts for one meal, so a call matching an
    existing (date, restaurant) merges into it instead of appending.

    Merging only ever fills in: values the caller supplies replace what is
    there, values it omits leave the record alone. A calendar entry arriving
    after a receipt therefore cannot blank out the items and total.

    Same-day repeat visits to one restaurant collapse into a single record.
    That is deliberate — keying on meal_type as well would re-open the
    duplicate hole every time the calendar's guess and the receipt's clock
    disagreed, which is the common case, not the rare one.
    """
    with locked_file(DATA_FILE):
        data = load_data()

        name = _titlecase_venue(restaurant)
        day  = date or datetime.now().strftime("%Y-%m-%d")

        existing = next(
            (v for v in data["visits"]
             if v["date"] == day and v["restaurant"].lower() == name.lower()),
            None
        )

        if existing:
            if items:
                existing["items"] = items
            if total is not None:
                existing["total"] = total
            save_data(data)
            # `_merged` tells the formatter to say "updated" rather than
            # "logged". Returned on a copy so it never reaches the state file.
            return dict(existing, _merged=True)

        # max(existing) + 1, not len() + 1: pending_ratings is keyed on this
        # id, so a length-derived id collides with a live key the moment any
        # visit is ever removed.
        # Clear of every id in use, including keys in pending_ratings that no
        # longer have a visit. The two sets already diverge in the live file,
        # and pending_ratings is keyed on this id, so reusing one silently
        # overwrites another restaurant's pending rating.
        used_ids = {v.get("id") or 0 for v in data["visits"]}
        used_ids |= {int(k) for k in (data.get("pending_ratings") or {})
                     if str(k).isdigit()}
        next_id = max(used_ids, default=0) + 1
        visit = {
            "id":               next_id,
            "restaurant":       name,
            "date":             day,
            "meal_type":        meal_type or detect_meal_type(),
            "items":            items or [],
            "total":            total,
            "rating":           None,
            "individual_ratings": {},
            "notes":            "",
            "source":           source,
            "logged_at":        datetime.now().isoformat()
        }

        data["visits"].append(visit)

        # Set pending rating reminder for each family member
        data["pending_ratings"][str(visit["id"])] = {
            "restaurant": visit["restaurant"],
            "date":       visit["date"],
            "pending_for": list(FAMILY_MEMBERS.values()),  # ["Alex", "Sam"]
            "reminded":   []
        }

        save_data(data)
        return visit


def add_rating(visit_id: int = None, restaurant: str = None,
               rating: int = None, notes: str = "",
               sender: str = "") -> Tuple[bool, str]:
    """Add individual rating for a visit based on sender."""
    if not rating or not (1 <= rating <= 5):
        return False, "Rating must be between 1 and 5"

    with locked_file(DATA_FILE):
        data = load_data()

        # Resolve sender name
        sender_name = FAMILY_MEMBERS.get(sender, "Unknown")

        # Find visit by ID or most recent unrated visit to restaurant
        visit = None
        if visit_id:
            visit = next((v for v in data["visits"] if v["id"] == visit_id), None)
        elif restaurant:
            matches = [v for v in data["visits"]
                      if restaurant.lower() in v["restaurant"].lower()]
            if matches:
                visit = sorted(matches, key=lambda x: x["date"], reverse=True)[0]
        else:
            # Most recent visit where this sender hasn't rated yet
            for v in reversed(data["visits"]):
                already_rated = v.get("individual_ratings", {})
                if sender_name not in already_rated:
                    visit = v
                    break

        if not visit:
            return False, "No unrated visit found"

        # Store individual rating
        if "individual_ratings" not in visit:
            visit["individual_ratings"] = {}
        visit["individual_ratings"][sender_name] = {"rating": rating, "notes": notes}

        # Update aggregate rating (average of all individual ratings)
        all_ratings = [r["rating"] for r in visit["individual_ratings"].values()]
        visit["rating"] = round(sum(all_ratings) / len(all_ratings), 1)

        # Remove this person from pending
        pending = data["pending_ratings"].get(str(visit["id"]))
        if pending:
            pending_for = pending.get("pending_for", [])
            if sender_name in pending_for:
                pending_for.remove(sender_name)
            # If everyone rated, remove entirely
            if not pending_for:
                data["pending_ratings"].pop(str(visit["id"]), None)
            else:
                pending["pending_for"] = pending_for

        save_data(data)
        return True, visit["restaurant"]


# ─── Recommendations ──────────────────────────────────────────────────────────

def get_recommendations(meal_type: str = None, limit: int = 5) -> List[Dict]:
    """
    Smart recommendations based on:
    - High ratings (4-5 stars)
    - Not visited in last 30 days
    - Matching meal type if specified
    """
    data = load_data()
    visits = data["visits"]

    if not visits:
        return []

    # Group by restaurant
    restaurants = {}
    for v in visits:
        name = v["restaurant"]
        if name not in restaurants:
            restaurants[name] = {
                "name":        name,
                "visits":      [],
                "avg_rating":  0,
                "last_visit":  None,
                "meal_types":  set()
            }
        restaurants[name]["visits"].append(v)
        if v.get("rating"):
            restaurants[name]["avg_rating"] = (
                sum(x.get("rating", 0) for x in restaurants[name]["visits"] if x.get("rating")) /
                sum(1 for x in restaurants[name]["visits"] if x.get("rating"))
            )
        if v["date"] > (restaurants[name]["last_visit"] or ""):
            restaurants[name]["last_visit"] = v["date"]
        restaurants[name]["meal_types"].add(v.get("meal_type", ""))

    cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    candidates = []
    for name, info in restaurants.items():
        # Filter by meal type if specified
        if meal_type and meal_type not in info["meal_types"]:
            continue
        # Skip unrated places with only one visit
        if info["avg_rating"] == 0 and len(info["visits"]) == 1:
            continue

        score = info["avg_rating"]
        # Bonus for not visited recently
        if info["last_visit"] and info["last_visit"] < cutoff:
            score += 0.5

        candidates.append({
            "name":       name,
            "avg_rating": round(info["avg_rating"], 1),
            "visit_count": len(info["visits"]),
            "last_visit": info["last_visit"],
            "score":      score,
            "meal_types": list(info["meal_types"])
        })

    return sorted(candidates, key=lambda x: x["score"], reverse=True)[:limit]


def get_pending_reminders() -> List[Dict]:
    """Get per-person reminders for visits needing rating after 2+ hours."""
    data = load_data()
    reminders = []
    cutoff = (datetime.now() - timedelta(hours=2)).isoformat()

    # Build reverse map: name → phone
    name_to_phone = {v: k for k, v in FAMILY_MEMBERS.items()}

    for visit_id, info in data["pending_ratings"].items():
        visit = next((v for v in data["visits"] if str(v["id"]) == visit_id), None)
        if not visit or visit["logged_at"] >= cutoff:
            continue

        pending_for = info.get("pending_for", list(FAMILY_MEMBERS.values()))
        reminded    = info.get("reminded", [])

        for name in pending_for:
            if name not in reminded:
                phone = name_to_phone.get(name, "")
                reminders.append({
                    "visit_id":   int(visit_id),
                    "restaurant": info["restaurant"],
                    "date":       info["date"],
                    "person":     name,
                    "phone":      phone
                })

    return reminders


# ─── Format for WhatsApp ──────────────────────────────────────────────────────

def format_visit_confirmation(visit: Dict) -> str:
    """Format visit log confirmation + rating request."""
    items_str = ", ".join(visit["items"][:5]) if visit["items"] else "items not recorded"

    verb = "Updated" if visit.get("_merged") else "Logged"
    lines = [
        f"🍽️ *{verb}: {visit['restaurant']}*",
        f"  📅 {visit['date']} — {visit['meal_type'].title()}",
    ]
    if items_str != "items not recorded":
        lines.append(f"  🍴 {items_str}")
    if visit.get("total"):
        lines.append(f"  💰 ${visit['total']:.2f}")

    # Don't re-ask for a rating the family has already given. A receipt often
    # arrives after someone rated the meal from the calendar entry.
    if not visit.get("individual_ratings"):
        lines.append("")
        lines.append("How was it? Reply with a rating 1-5 ⭐")
        lines.append("_e.g. 'rate [Restaurant] 4' or just '4'_")

    return "\n".join(lines)


def format_recommendations(recs: List[Dict], meal_type: str = None) -> str:
    """Format restaurant recommendations for WhatsApp."""
    if not recs:
        return "🍽️ No recommendations yet — log some restaurant visits first!"

    meal_str = f" for {meal_type}" if meal_type else ""
    lines = [f"🍽️ *Restaurant Recommendations{meal_str}*\n"]

    for i, r in enumerate(recs, 1):
        stars = "⭐" * int(r["avg_rating"]) if r["avg_rating"] else "unrated"
        last  = r["last_visit"] or "never"
        lines.append(
            f"{i}. *{r['name']}* {stars}\n"
            f"   Visited {r['visit_count']}x — last: {last}"
        )

    return "\n".join(lines)


def format_top_list() -> str:
    """Format top rated restaurants."""
    data = load_data()
    if not data["visits"]:
        return "🍽️ No restaurants logged yet!"

    # Get all rated visits grouped by restaurant
    restaurants = {}
    for v in data["visits"]:
        if not v.get("rating"):
            continue
        name = v["restaurant"]
        if name not in restaurants:
            restaurants[name] = {"ratings": [], "visits": 0, "individual": {}}
        restaurants[name]["ratings"].append(v["rating"])
        restaurants[name]["visits"] += 1
        # Collect most recent individual ratings
        for person, info in v.get("individual_ratings", {}).items():
            if person != "Unknown":
                restaurants[name]["individual"][person] = info 

    if not restaurants:
        return "🍽️ No rated restaurants yet — try rating some visits!"

    ranked = sorted(
        [{"name": k,
          "avg": round(sum(v["ratings"])/len(v["ratings"]), 1),
          "count": v["visits"],
          "individual": v.get("individual", {})}
         for k,v in restaurants.items()],
        key=lambda x: x["avg"], reverse=True
    )

    lines = ["🏆 *Top Restaurants*\n"]
    for i, r in enumerate(ranked[:10], 1):
        stars = "⭐" * int(r["avg"])
        individual = r.get("individual", {})
        if len(individual) >= 2:
            parts = " | ".join(f"{name}: {info['rating']}⭐" for name, info in individual.items())
            lines.append(f"{i}. *{r['name']}* {stars} avg\n   ({parts}) — {r['count']} visit(s)")
        elif len(individual) == 1:
            name, info = list(individual.items())[0]
            lines.append(f"{i}. *{r['name']}* {stars} ({name}: {info['rating']}⭐) — {r['count']} visit(s)")
        else:
            lines.append(f"{i}. *{r['name']}* {stars} ({r['avg']}) — {r['count']} visit(s)")

    return "\n".join(lines)


# ─── Calendar Integration ─────────────────────────────────────────────────────

# Titles that name a *venue*. "dinner with X" is deliberately absent: it names
# company, not a place, and the old list had it. Combined with a splitter that
# accepted "dinner " as a delimiter, "Dinner with Rohan and Meera" was logged
# as a restaurant called "With Rohan And Meera" — 10 of the 18 names in
# restaurants.json arrived that way, and they fed get_top_restaurants back to
# the family as places to eat.
_VENUE_KEYWORDS = (
    "dinner at", "lunch at", "breakfast at", "brunch at",
    "eat at", "eating at", "restaurant", "cafe",
)

# Only a locative preposition introduces a venue name. Splitting on the meal
# word itself is what turned company into a restaurant.
_VENUE_SPLITTER = " at "

# What follows " at " is not always a place. "Dinner at 6pm" is an ordinary
# calendar title, and the first version of this filter logged a restaurant
# called "6Pm"; "Lunch at work" logged "Work". Closing the "dinner with X"
# class while leaving these open just swapped one source of junk names for
# another, and they all feed get_top_restaurants back to the family.
_NOT_A_VENUE = re.compile(
    r"^(?:\d{1,2}(?::\d{2})?\s*(?:am|pm)?"       # 6pm, 6:30, 18:00
    r"|noon|midnight"
    r"|home|work|school|the\s+office|office)$",
    re.IGNORECASE,
)


def _titlecase_venue(name: str) -> str:
    """Title-case a venue without mangling an interior apostrophe.

    ``str.title()`` turns "denny's" into "Denny'S", and that mangled form is
    what reached restaurants.json and came back to the family as a place to
    eat — while _looks_like_a_home names Denny's specifically as a chain it is
    trying to protect.
    """
    return re.sub(
        r"[A-Za-z'\u2019]+",
        lambda m: m.group(0)[:1].upper() + m.group(0)[1:].lower(),
        name,
    )


def _looks_like_a_home(name: str) -> bool:
    """True for "Kabir and Nisha's" — a friend's house, not a restaurant.

    A trailing possessive alone is not enough to reject on: Denny's, Applebee's
    and Cheesecake Factory-adjacent chains all end that way. What marks a home
    is a possessive over a *pair of first names*, so the conjunction is the
    signal that matters.
    """
    low = name.lower().rstrip(". ")
    if not (low.endswith("'s") or low.endswith("’s") or low.endswith("s'")):
        return False
    return " and " in low or " & " in low


def check_calendar_for_restaurants(calendar_events: List[Dict]) -> List[Dict]:
    """
    Detect restaurant visits from calendar events.
    Looks for a venue named after a locative "at": 'dinner at X', 'lunch at X'.

    Returns a list of {restaurant, date, meal_type, source} dicts. (The
    annotation said List[str] and never matched the return value.)
    """
    found = []
    for event in calendar_events:
        title = event.get("title", "").lower()
        if not any(kw in title for kw in _VENUE_KEYWORDS):
            continue
        if _VENUE_SPLITTER not in title:
            continue

        restaurant_name = _titlecase_venue(
            title.split(_VENUE_SPLITTER, 1)[1].strip())
        if len(restaurant_name) <= 2:
            continue
        # "Dinner at 6pm" / "Lunch at work" — a time or a generic place.
        if _NOT_A_VENUE.match(restaurant_name):
            continue
        # "Dinner at Elena's with the Nolans" — the tail is company, not venue.
        if restaurant_name.lower().startswith("with "):
            continue
        if _looks_like_a_home(restaurant_name):
            continue

        found.append({
            "restaurant": restaurant_name,
            "date": event.get("date"),
            "meal_type": detect_meal_type(title, event.get("time")),
            "source": "calendar"
        })
    return found


# ─── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: restaurant_tracker.py [list|top|recommend|log <name>|rate <name> <1-5>]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "list":
        data = load_data()
        for v in sorted(data["visits"], key=lambda x: x["date"], reverse=True)[:10]:
            r = "⭐"*v["rating"] if v.get("rating") else "unrated"
            print(f"{v['date']} — {v['restaurant']} ({v['meal_type']}) {r}")
    elif cmd == "top":
        print(format_top_list())
    elif cmd == "recommend":
        meal = sys.argv[2] if len(sys.argv) > 2 else None
        recs = get_recommendations(meal)
        print(format_recommendations(recs, meal))
    elif cmd == "log" and len(sys.argv) > 2:
        name = " ".join(sys.argv[2:])
        visit = log_visit(name)
        print(format_visit_confirmation(visit))
    elif cmd == "rate" and len(sys.argv) > 3:
        name   = sys.argv[2]
        rating = int(sys.argv[3])
        notes  = " ".join(sys.argv[4:]) if len(sys.argv) > 4 else ""
        ok, result = add_rating(restaurant=name, rating=rating, notes=notes)
        print(f"✅ Rated {result} {rating}⭐" if ok else f"❌ {result}")
