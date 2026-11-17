"""
occurrence.py — UTC dose-occurrence helpers (issue #1 PR 1).

Hard rule (issue §0): every comparison and offset runs on aware UTC
datetimes. Local wall time is used only to build occurrence keys and
display strings. Same-timezone arithmetic is wall-clock arithmetic and is
wrong across DST, so builders convert to UTC immediately.

DST rules (issue §3): a nonexistent wall time (02:30 on a spring-forward
day) normalizes forward to the first real instant after it; an ambiguous
wall time (01:30 on a fall-back day) takes the first instance (fold=0).
Python's zoneinfo gives exactly this for fold=0 datetimes.
"""

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from typing import Optional
from zoneinfo import ZoneInfo

UTC = timezone.utc

# Day-of-week keys in Python weekday() order (mon=0) — matches dispatch.DAY_KEYS
DAY_KEYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")


def day_indexes(day_of_week) -> tuple:
    """
    Weekday numbers (mon=0) a weekly schedule fires on. Accepts the legacy
    single string ('tue') or the PR 7 list form (['tue','sat']). Empty when
    unset — readers normalize, so stored form never matters here.
    """
    if not day_of_week:
        return ()
    if isinstance(day_of_week, str):
        return (DAY_KEYS.index(day_of_week),)
    return tuple(DAY_KEYS.index(d) for d in day_of_week)


@dataclass(frozen=True)
class Occurrence:
    """
    A single scheduled dose occurrence.

    utc — the instant it is due (aware UTC; all math happens here)
    key — stable identity across events: "{local_date}T{HH:MM}#{i}" for
          wall-time schedules, the UTC instant itself for interval
          schedules (no fall-back collision, issue §3)
    tz  — the med's timezone; used for keys and display only
    """

    utc: datetime
    key: str
    tz: ZoneInfo

    @property
    def local(self) -> datetime:
        """Wall time in the med's timezone (display/keys only, never math)."""
        return self.utc.astimezone(self.tz)

    @property
    def local_display(self) -> str:
        """e.g. 'Tue Apr 21 8:00am PDT'."""
        l = self.local
        h12 = l.hour % 12 or 12
        ampm = "am" if l.hour < 12 else "pm"
        return f"{l:%a %b %d} {h12}:{l.minute:02d}{ampm} {l:%Z}"


def _to_utc(dt: datetime) -> datetime:
    """Aware datetime → UTC. Naive input is assumed UTC (never schedule time)."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def at_local(day: date, hhmm: str, tz: ZoneInfo, index: int = 0) -> Occurrence:
    """Wall-time occurrence (once_daily / twice_daily / weekly)."""
    h, m = map(int, hhmm.split(":"))
    local = datetime.combine(day, time(h, m), tzinfo=tz)  # fold=0
    key = f"{day.isoformat()}T{hhmm}#{index}"
    return Occurrence(utc=local.astimezone(UTC), key=key, tz=tz)


def at_utc(instant: datetime, tz: ZoneInfo) -> Occurrence:
    """Interval-style occurrence keyed by the UTC instant itself."""
    u = _to_utc(instant)
    if u.microsecond:
        u = u.replace(microsecond=0)
    return Occurrence(utc=u, key=u.strftime("%Y-%m-%dT%H:%M:%SZ"), tz=tz)


def occurrences_between(sched: dict, lo: datetime, hi: datetime, tz: ZoneInfo) -> list:
    """
    Wall-time occurrences whose UTC instant falls in (lo, hi], in UTC order.

    Weekly meds enumerate only local dates whose weekday is in day_of_week
    (single day or list — PR 7). Interval and as_needed meds return [] —
    interval enumeration is anchored on next_due by the tick (PR 2). lo/hi
    may carry any (or no) timezone.
    """
    freq = sched.get("frequency")
    if freq in ("interval", "as_needed") or not sched.get("times"):
        return []
    lo_utc, hi_utc = _to_utc(lo), _to_utc(hi)

    weekly_days = day_indexes(sched.get("day_of_week")) if freq == "weekly" else ()

    day = lo_utc.astimezone(tz).date() - timedelta(days=1)   # local-date margin
    end = hi_utc.astimezone(tz).date() + timedelta(days=1)
    out = []
    while day <= end:
        if not weekly_days or day.weekday() in weekly_days:
            for i, t in enumerate(sched["times"]):
                occ = at_local(day, t, tz, i)
                if lo_utc < occ.utc <= hi_utc:
                    out.append(occ)
        day += timedelta(days=1)
    out.sort(key=lambda o: o.utc)
    return out


def most_recent_past(sched: dict, asof: datetime, tz: ZoneInfo) -> Optional[Occurrence]:
    """Most recent wall-time occurrence at or before `asof`. None for interval/as_needed."""
    period = timedelta(days=7 if sched.get("frequency") == "weekly" else 1)
    window = occurrences_between(sched, _to_utc(asof) - 2 * period, asof, tz)
    return window[-1] if window else None


# An unresolved dose is closed as missed when the med's next dose arrives
# (#11), but never later than CLOSE_CAP after it was due — a weekly med is
# not nagged for a week. 25h, not 24h, so a daily dose across a DST
# fall-back (a 25h day) still closes at the next dose.
CLOSE_CAP = timedelta(hours=25)


def close_instant(sched: dict, due_utc: datetime, tz: ZoneInfo) -> datetime:
    """When a dose due at `due_utc` that is still unresolved is closed as
    missed: the next dose's instant, at most CLOSE_CAP after `due_utc`."""
    due = _to_utc(due_utc)
    cap = due + CLOSE_CAP
    if sched.get("frequency") == "interval":
        return min(due + timedelta(hours=float(sched["interval_hours"])), cap)
    nxt = occurrences_between(sched, due, cap, tz)
    return nxt[0].utc if nxt else cap


def _wall_match(sched: dict, instant: datetime, tz: ZoneInfo) -> Optional[Occurrence]:
    """Occurrence whose local wall time matches `instant`'s (any fold)."""
    freq = sched.get("frequency")
    if freq in ("interval", "as_needed") or not sched.get("times"):
        return None
    local = _to_utc(instant).astimezone(tz)
    for i, t in enumerate(sched["times"]):
        h, m = map(int, t.split(":"))
        if (local.hour, local.minute) == (h, m):
            return at_local(local.date(), t, tz, i)
    return None


def for_instant(sched: dict, instant: datetime, tz: ZoneInfo) -> Occurrence:
    """
    Occurrence for a known scheduled instant (e.g. state.confirmed_dose).
    Matches the local wall time against times[]; interval/as_needed or no
    match → keyed by the UTC instant.
    """
    occ = _wall_match(sched, instant, tz)
    return occ if occ is not None else at_utc(instant, tz)


def covered_occurrence(sched: dict, taken_at: datetime, tz: ZoneInfo,
                       early_window: timedelta = timedelta(hours=6)) -> Optional[Occurrence]:
    """
    The occurrence a confirm at `taken_at` credits, under the pre-tick rules
    (kept for the PR 1 migration so legacy 'taken' entries key exactly like
    dispatch.covered_dose_occurrence keyed them). Credits the next upcoming
    occurrence when it is due within early_window and nearer than the most
    recent past one. None for interval / as_needed.
    """
    freq = sched.get("frequency")
    if freq in ("interval", "as_needed") or not sched.get("times"):
        return None
    period = timedelta(days=7 if freq == "weekly" else 1)
    asof_utc = _to_utc(taken_at)
    local_now = asof_utc.astimezone(tz)

    weekly_days = day_indexes(sched.get("day_of_week")) if freq == "weekly" else ()
    # Each (time, weekday) pair contributes its most recent past instance —
    # one pair per time for daily meds, one per listed day for weekly (PR 7;
    # a legacy weekly with no day_of_week keeps its daily-pair behavior).
    weekdays = weekly_days or (local_now.date().weekday(),)
    pasts, futures = [], []
    for i, t in enumerate(sched["times"]):
        for wd in weekdays:
            day = local_now.date() - timedelta(days=(local_now.date().weekday() - wd) % 7)
            past = at_local(day, t, tz, i)
            if past.utc > asof_utc:
                past = at_local(day - period, t, tz, i)
            pasts.append(past)
            futures.append(at_local(past.local.date() + period, t, tz, i))

    nearest_past = max(pasts, key=lambda o: o.utc)
    next_future = min(futures, key=lambda o: o.utc)
    until_future = next_future.utc - asof_utc
    if until_future <= early_window and until_future < (asof_utc - nearest_past.utc):
        return next_future
    return nearest_past
