#!/usr/bin/env python3
"""
travel_window.py — "Is the household away, and where?"

A different question from the one `trip_detector.py` answers. That module is
about trip *prep*: what to pack, what the kids need, what the destination is
like. This one answers a narrower thing the daily briefings need every single
run — on this date, is the family at home in Irvine or somewhere else? — and
the answer redirects weather and suppresses home-only content.

The source of truth is a calendar event, deliberately. The launchd runners
never talk to the OpenClaw agent; they shell out to `homebase` and nothing
else. So anything the agent merely *knows* is invisible to them. The calendar
is the one surface both already read, it syncs from Google on every run, and
it can be edited from any phone. A private travel state file would be a second
source of truth that drifts — the failure this repo already hit when a cron
job carried a stale copy of a prompt for a full major version.

The convention is an all-day event spanning the trip:

    Trip to Seattle        location: Seattle, WA        Aug 29 – Sep 6

Both halves matter. All-day is what distinguishes the trip *window* from
events *inside* it — "Flight UA2316 LAX to SEA" is timed, so it never trips
travel mode on its own, which is correct: the flight is an appointment, the
trip is the span.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Dict, List, Optional

# Title patterns that mean "the household is somewhere else."
#
# Deliberately NARROWER than trip_detector.TRIP_KEYWORDS. That list exists to
# cast a wide net for candidate events a human then judges, so it can afford
# "weekend" and "visit". This list drives an unattended decision that redirects
# a family's weather for days at a time, and a false positive is expensive and
# silent — "Weekend farmers market" must never convince the briefing the family
# left town. Every pattern here has to be something a person would only write
# when they are actually going away.
#
# Each is (regex, destination_group). A destination group of 0 means the
# pattern carries no destination and it must come from the event's location.
_TRAVEL_PATTERNS = [
    (re.compile(r"^trip\s+to\s+(.+)$", re.I), 1),
    (re.compile(r"^travel(?:ling|ing)?\s+to\s+(.+)$", re.I), 1),
    (re.compile(r"^(.+?)\s+trip$", re.I), 1),
    (re.compile(r"^vacation\s+(?:in|to|at)\s+(.+)$", re.I), 1),
    (re.compile(r"^(?:in|visiting)\s+(.+?)\s*\((?:trip|travel|away)\)$", re.I), 1),
    (re.compile(r"^out\s+of\s+town$", re.I), 0),
    (re.compile(r"^vacation$", re.I), 0),
]

# Trailing noise people put in trip titles that is not part of the place name.
_DEST_TRAILERS = re.compile(
    r"\s*[\(\[].*?[\)\]]\s*$|\s*[-–—]\s*(?:family|work|solo|with .*)$", re.I
)


def _clean_destination(raw: str) -> str:
    """Strip parentheticals and trailing qualifiers off a parsed destination."""
    cleaned = _DEST_TRAILERS.sub("", (raw or "").strip()).strip(" -–—,")
    return cleaned


def _match_travel_event(event: Dict) -> Optional[str]:
    """
    Return the destination if `event` declares a travel window, else None.

    Requires an all-day event: a timed one is something that happens during a
    day, not a statement about where the household is sleeping.
    """
    if (event.get("time") or "") != "All day":
        return None

    title = (event.get("title") or "").strip()
    if not title:
        return None

    for pattern, group in _TRAVEL_PATTERNS:
        m = pattern.match(title)
        if not m:
            continue
        # The event's own location field wins when set — it is structured data
        # a human filled in, and it geocodes far better than a title fragment
        # ("Seattle, WA" vs "Seattle for Ammu's birthday").
        location = (event.get("location") or "").strip()
        if location:
            return location
        if group and m.group(group):
            return _clean_destination(m.group(group))
        # Matched a destination-less pattern ("Out of town") with no location
        # set. That is a real travel window with an unknown where — the caller
        # still needs to know home content is wrong, so say away with no
        # destination rather than pretending the family is home.
        return ""
    return None


def get_travel_window(date: str, events: List[Dict]) -> Dict:
    """
    Travel status for `date`, given events already loaded from the calendar.

    Pure and caller-fed: takes events rather than reading the calendar itself,
    so the briefings can pass the set they already synced and this stays
    trivially testable. `tools.get_travel_status` is the wiring.

    Returns `{"away": False}` at home, or when away::

        {"away": true, "destination": "Seattle, WA", "start": "2026-08-29",
         "end": "2026-09-06", "day": 3, "of": 9, "last_day": false,
         "title": "Trip to Seattle"}

    `day`/`of` exist so a brief can say "day 3 of 9" without doing calendar
    math, and `last_day` because the day you fly home is not a day you dress
    for the destination.
    """
    for event in sorted(events, key=lambda e: (e.get("date") or "")):
        start = event.get("date") or ""
        end = event.get("end_date") or start
        if not start or not (start <= date <= end):
            continue

        destination = _match_travel_event(event)
        if destination is None:
            continue

        try:
            d0 = datetime.strptime(start, "%Y-%m-%d").date()
            d1 = datetime.strptime(end, "%Y-%m-%d").date()
            dn = datetime.strptime(date, "%Y-%m-%d").date()
            day = (dn - d0).days + 1
            total = (d1 - d0).days + 1
        except ValueError:
            day, total = 1, 1

        # Departure day is not a day at the destination. They wake up at home,
        # spend the morning there, and leave. A 6:05 AM briefing that morning
        # is written for people standing in their own kitchen — it needs home's
        # weather, because that is what they are about to walk out into.
        #
        # The return day is NOT symmetrical: they wake at the destination and
        # fly home midday, so that morning still belongs to the destination.
        # Hence `day > 1` rather than anything involving `last_day`.
        at_destination = day > 1

        return {
            "away":        True,
            "destination": destination,
            # So consumers can drop this event from a displayed timeline. The
            # trip is a state, not an appointment, and it is already said in
            # this very dict — listing it again as "All day — Trip to Seattle"
            # under a header that reads "Seattle (day 4 of 9)" is the same fact
            # twice. Matched by id rather than title so an unrelated event that
            # happens to share the name is never silently swallowed.
            "event_id":    event.get("id") or "",
            # Where the forecast should come from, already decided. Callers get
            # a value to use rather than a rule to reimplement — the runner
            # shell in particular should not be encoding trip policy.
            # Empty means "use home".
            "weather_location": destination if at_destination else "",
            "at_destination":   at_destination,
            "departure_day":    day == 1,
            "start":       start,
            "end":         end,
            "day":         day,
            "of":          total,
            "last_day":    date == end,
            "title":       event.get("title") or "",
        }

    return {"away": False}


def travel_status_json(date: Optional[str] = None, sync: bool = False) -> str:
    """
    `get_travel_window` against the cached family calendar, as a JSON string.

    Defaults to no sync: the briefing tools that call this have already synced
    in the same run, and a second Google round-trip would add an auth failure
    path to the one job that must not acquire new ways to break at 6am.
    """
    from core.config_loader import SKILL_DIR
    from features.calendar.calendar_aggregator import FamilyCalendarAggregator

    target = date or datetime.now().strftime("%Y-%m-%d")
    agg = FamilyCalendarAggregator(SKILL_DIR)
    if sync:
        # force: agent.md documents '{"sync":true}' as the cold-call
        # option, and the new TTL would otherwise let it reuse a cache.
        agg.sync_with_google_calendar(force=True)

    return json.dumps(
        get_travel_window(target, list(agg.calendar.values())),
        separators=(",", ":"),
    )
