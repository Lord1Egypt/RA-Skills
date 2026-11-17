"""
attribution.py — which scheduled dose a confirm credits (issue #1 §4, PR 2).

Nearest-in-time rule: the candidates are the most recent past occurrence
that is unresolved or missed, plus the next future occurrence when the
confirm falls within EARLY_WINDOW of it. The confirm credits the nearer
candidate. When both qualify but the confirm sits between the early
window and the midpoint (possible only when the schedule gap is shorter
than 2× the window), it is genuinely unclear which dose was meant — the
caller must ask (exit 4) instead of guessing.

All comparisons run on aware UTC datetimes (issue §0). Local wall time
is used only through the occurrence helpers (keys and display).
"""

from datetime import date, datetime, time, timedelta, timezone
from typing import Optional, Tuple
from zoneinfo import ZoneInfo

import occurrence as _occ
from clock import parse_instant
from event_store import outcome

UTC = timezone.utc

# A confirm taken now credits the next future occurrence when it is due
# within this window (issue §4: 90 min default, one easy-to-tune constant).
EARLY_WINDOW = timedelta(minutes=90)

# confirm --all within DIGEST_GRACE after the digest uses the wide window
# ('all taken' replied to the morning digest before the first dose fires).
ALL_AFTER_DIGEST_WINDOW = timedelta(hours=6)
DIGEST_GRACE = timedelta(minutes=60)

# How far back a still-unresolved/missed occurrence can absorb a confirm.
WALKBACK = timedelta(days=7)

# Ambiguity is possible only when the two doses are closer than this.
_MIN_AMBIGUITY_GAP = 2 * EARLY_WINDOW


# ── Event views (med-scoped wrappers over event_store) ────────────────────────

def generation(events, med_id: str, occurrence_key: str) -> int:
    """Current generation of an occurrence: how often it was undone."""
    return sum(
        1 for e in events
        if e.get("event") == "undone"
        and e.get("med_id") == med_id
        and e.get("occurrence_key") == occurrence_key
    )


def outcome_for(events, med_id: str, occurrence_key: str, gen: int = 0) -> Optional[str]:
    """Terminal outcome of (med, occurrence, generation), or None (unresolved)."""
    return outcome(events, occurrence_key, gen, med_id=med_id)


def unresolved_or_missed(events, med_id: str, occurrence_key: str) -> bool:
    """True when a confirm may still credit this occurrence."""
    return outcome_for(events, med_id, occurrence_key,
                       generation(events, med_id, occurrence_key)) in (None, "missed")


# ── Duplicate window ──────────────────────────────────────────────────────────

def min_gap(med: dict) -> timedelta:
    """
    Minimum spacing between logged doses for this med (issue §4).

    Per-med min_gap_hours when set; otherwise half the shortest scheduled
    gap: once daily → 12h, 08:00/20:00 → 6h, interval N → N/2,
    weekly → from its days (Mon–Fri 19:00 → 12h, Tue+Sat → 36h, one day a
    week → 3.5d; #25), as_needed → 4h.
    """
    mgh = med.get("min_gap_hours")
    if mgh:
        return timedelta(hours=float(mgh))
    sched = med.get("schedule") or {}
    freq = sched.get("frequency")
    if freq == "interval":
        return timedelta(hours=float(sched.get("interval_hours") or 4) / 2)
    if freq == "weekly" and sched.get("day_of_week"):
        # minute-of-week of every dose, then the shortest cyclic gap (#25):
        # a flat 24h treated a Mon–Fri med's next-day dose as a duplicate
        week = 7 * 24 * 60
        days = _occ.day_indexes(sched["day_of_week"])
        slots = sorted(d * 24 * 60 + _hhmm_minutes(t)
                       for d in days for t in (sched.get("times") or ["08:00"]))
        gaps = [(slots[(i + 1) % len(slots)] - slots[i]) % week or week
                for i in range(len(slots))]
        return timedelta(minutes=min(gaps) / 2)
    if freq == "as_needed":
        return timedelta(hours=4)
    times = sorted(sched.get("times") or ["08:00"])
    if len(times) == 1:
        return timedelta(hours=12)
    minutes = [_hhmm_minutes(t) for t in times]
    gaps = [(minutes[i + 1] - minutes[i]) % (24 * 60) for i in range(len(minutes) - 1)]
    gaps.append((minutes[0] - minutes[-1]) % (24 * 60))   # wrap past midnight
    return timedelta(minutes=min(gaps) / 2)


def _hhmm_minutes(hhmm: str) -> int:
    h, m = map(int, hhmm.split(":"))
    return h * 60 + m


def _taken_instant(event: dict) -> datetime:
    raw = event.get("taken_at_utc") or event.get("ts_utc")
    return parse_instant(raw)


def last_taken_before(events, med_id: str, taken_at: datetime) -> Optional[dict]:
    """The most recent `taken` event for this med strictly before taken_at."""
    best = None
    best_at = None
    for e in events:
        if e.get("event") != "taken" or e.get("med_id") != med_id:
            continue
        at = _taken_instant(e)
        if at < taken_at and (best_at is None or at > best_at):
            best, best_at = e, at
    return best


def duplicate_of(events, med: dict, occ, taken_at: datetime) -> Optional[dict]:
    """
    The earlier `taken` this confirm would duplicate, or None (#25).

    - Crediting a dose that is already logged taken (e.g. a --dose pin) is
      always a duplicate.
    - Otherwise only a log within min_gap of the previous one can be — and
      not when this confirm credits the next scheduled dose after the one
      the previous log credited (normal progression: yesterday's dose, then
      today's), however close they are. A back-fill of an OLDER dose, an
      early credit of a future dose, or an unattributed log right after a
      dose still counts.
    """
    if occ is not None:
        gen = generation(events, med["id"], occ.key)
        if outcome_for(events, med["id"], occ.key, gen) == "taken":
            return next((e for e in reversed(list(events))
                         if e.get("event") == "taken" and e.get("med_id") == med["id"]
                         and e.get("occurrence_key") == occ.key
                         and int(e.get("generation") or 0) == gen), None)
    last = last_taken_before(events, med["id"], taken_at)
    if last is None or taken_at - _taken_instant(last) >= min_gap(med):
        return None
    if (occ is not None and last.get("occurrence_utc")
            and parse_instant(last["occurrence_utc"]) < occ.utc <= taken_at):
        return None
    return last


def when_label(instant: datetime, tz: ZoneInfo, ref: datetime) -> str:
    """'today at 8:45pm' / 'yesterday at 8:45pm' / 'Mon at 8:45pm' /
    'Oct 14 at 8:45pm' — the local day of `instant` relative to `ref` (#25)."""
    local = instant.astimezone(tz)
    days = (ref.astimezone(tz).date() - local.date()).days
    clock_str = f"{local.hour % 12 or 12}:{local.minute:02d}{'am' if local.hour < 12 else 'pm'}"
    if days == 0:
        day = "today"
    elif days == 1:
        day = "yesterday"
    elif 1 < days < 7:
        day = f"{local:%a}"
    else:
        day = f"{local:%b} {local.day}"
    return f"{day} at {clock_str}"


def taken_within(events, med_id: str, lo: datetime, hi: datetime) -> Optional[dict]:
    """A `taken` event (attributed or not) with taken_at in [lo, hi]."""
    for e in events:
        if e.get("event") != "taken" or e.get("med_id") != med_id:
            continue
        if lo <= _taken_instant(e) <= hi:
            return e
    return None


# ── Instant resolution ────────────────────────────────────────────────────────

def resolve_taken_at(hhmm: str, tz: ZoneInfo, now: datetime) -> datetime:
    """
    Most recent past instant with this wall time, at most 24h back
    (issue §4). On a DST-ambiguous wall time the FIRST instance
    (fold=0) wins, even if the second has already passed.
    """
    h, m = map(int, hhmm.split(":"))
    now_utc = now.astimezone(UTC)
    today = now_utc.astimezone(tz).date()
    for offset in range(2):   # today, yesterday
        day = today - timedelta(days=offset)
        instants = []
        for fold in (0, 1):
            local = datetime.combine(day, time(h, m), tzinfo=tz).replace(fold=fold)
            instants.append(local.astimezone(UTC))
        qualifying = sorted({
            u for u in instants
            if now_utc - timedelta(hours=24) <= u <= now_utc
        })
        if qualifying:
            return qualifying[0]   # first instance of the most recent day
    raise ValueError(
        f"--taken-at {hhmm}: no such wall time in the last 24 hours")


def nearest_dose_occurrence(med: dict, hhmm: str, taken_at: datetime,
                            tz: ZoneInfo) -> "_occ.Occurrence":
    """
    --dose HH:MM: pin the occurrence. HH:MM must match a scheduled
    times[] entry exactly; the nearest instance of that wall time to
    taken_at is credited (weekly meds: nearest instance on any listed
    day_of_week — single day or list, PR 7).
    """
    sched = med["schedule"]
    if hhmm not in (sched.get("times") or []):
        raise ValueError(
            f"--dose {hhmm} is not a scheduled time for {med['name']} "
            f"(scheduled: {', '.join(sched.get('times') or [])})")
    index = sched["times"].index(hhmm)
    asof = taken_at.astimezone(UTC)
    local_day = asof.astimezone(tz).date()
    weekly_days = _occ.day_indexes(sched.get("day_of_week")) \
        if sched.get("frequency") == "weekly" else ()
    best = None
    for offset in range(-8, 9):   # ±8 days covers weekly meds
        day = local_day + timedelta(days=offset)
        if weekly_days and day.weekday() not in weekly_days:
            continue
        cand = _occ.at_local(day, hhmm, tz, index)
        if best is None or abs((cand.utc - asof).total_seconds()) < \
                abs((best.utc - asof).total_seconds()):
            best = cand
    return best


# ── Candidates and the decision ───────────────────────────────────────────────

def _active_since(med: dict) -> Optional[datetime]:
    raw = med.get("active_since_utc")
    return parse_instant(raw) if raw else None


def find_candidates(med: dict, events, taken_at: datetime, tz: ZoneInfo
                    ) -> Tuple[Optional[_occ.Occurrence], Optional[_occ.Occurrence]]:
    """
    (past, future) creditable occurrences for a confirm at taken_at.

    past — the most recent past occurrence that is unresolved or missed
           (walking back up to WALKBACK; nothing before active_since_utc)
    future — the next future occurrence after taken_at
    Both None for as_needed meds (no schedule to credit).
    """
    sched = med["schedule"]
    if sched.get("frequency") == "as_needed":
        return None, None

    if sched.get("frequency") == "interval":
        return _interval_candidates(med, events, taken_at, tz)

    asof = taken_at.astimezone(UTC)
    since = _active_since(med)
    period = timedelta(days=7 if sched.get("frequency") == "weekly" else 1)

    past = None
    for occ in reversed(_occ.occurrences_between(sched, asof - WALKBACK, asof, tz)):
        if since is not None and occ.utc < since:
            break
        if unresolved_or_missed(events, med["id"], occ.key):
            past = occ
            break

    futures = _occ.occurrences_between(sched, asof, asof + 2 * period + timedelta(days=1), tz)
    if since is not None:
        futures = [o for o in futures if o.utc >= since]
    future = futures[0] if futures else None
    return past, future


def _interval_candidates(med: dict, events, taken_at: datetime, tz: ZoneInfo
                         ) -> Tuple[Optional[_occ.Occurrence], Optional[_occ.Occurrence]]:
    """
    Interval meds anchor on state.next_due (kept as legacy state by the
    tick; re-anchored on each confirm). Occurrences are the anchor chain
    anchor + k·interval, keyed by UTC instant (no DST collision).
    """
    sched = med["schedule"]
    step = timedelta(hours=float(sched["interval_hours"]))
    mstate = med.get("state") or {}
    anchor = None
    for raw in (mstate.get("next_due"), med.get("active_since_utc")):
        if raw:
            anchor = parse_instant(raw)
            break
    if anchor is None:
        return None, None

    asof = taken_at.astimezone(UTC)
    since = _active_since(med)
    # largest k with anchor + k·step ≤ taken_at
    k_past = (asof - anchor) // step if asof >= anchor else -1

    past = None
    k = k_past
    while k >= 0 and (asof - (anchor + k * step)) <= WALKBACK:
        occ = _occ.at_utc(anchor + k * step, tz)
        if since is not None and occ.utc < since:
            break
        if unresolved_or_missed(events, med["id"], occ.key):
            past = occ
            break
        k -= 1
    future = _occ.at_utc(anchor + (k_past + 1) * step, tz)
    if since is not None and future.utc < since:
        future = None
    return past, future


def choose(past: Optional[_occ.Occurrence], future: Optional[_occ.Occurrence],
           taken_at: datetime, early_window: timedelta = EARLY_WINDOW) -> Tuple[str, object]:
    """
    Decide which candidate a confirm credits (issue §4).

    Returns one of:
      ("credit", occurrence)     the dose to log
      ("ambiguous", (past, future))  both plausible — caller must ask (exit 4)
      ("unattributed", None)     no candidate — log without a schedule slot

    The future is creditable once taken_at enters its early window. When
    both candidates qualify and taken_at is still before the midpoint
    (possible only on gaps < 2× the window), the confirm is ambiguous.
    """
    asof = taken_at.astimezone(UTC)
    if future is not None and asof >= future.utc - early_window:
        if past is not None and asof < past.utc + (future.utc - past.utc) / 2:
            return "ambiguous", (past, future)
        return "credit", future
    if past is not None:
        return "credit", past
    return "unattributed", None


def attribute(med: dict, events, taken_at: datetime, tz: ZoneInfo,
              early_window: timedelta = EARLY_WINDOW) -> Tuple[str, object]:
    """find_candidates + choose in one call."""
    past, future = find_candidates(med, events, taken_at, tz)
    return choose(past, future, taken_at, early_window)
