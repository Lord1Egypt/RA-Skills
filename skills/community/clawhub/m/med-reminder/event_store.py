"""
event_store.py — append-only history.jsonl event store (issue #1 PR 1).

history.jsonl is the source of truth for dose events; meds-state.json is a
cache (issue §0). One JSON object per line:

    {id, ts_utc, med_id, event, occurrence_key, occurrence_utc, generation,
     stage, dose_prescribed, dose_taken, taken_at_utc, ref, attempt,
     lease_until_utc, error, vial_mg, diluent_ml, qty}

Appends flush + fsync so a crash never loses a recorded event. Readers
dedupe by id and skip a torn last line (a crash mid-append), so a forced
retry never duplicates history.

Event vocabulary: taken, skipped, missed, undone, snoozed, send_intent,
sent, send_failed, clock_anomaly, reconstituted (PR 8a: a vial mix,
{vial_mg, diluent_ml}, no occurrence), restocked / counted (PR 8b: {qty}
inventory units added / on hand, no occurrence). `reminded`/`late_nudge_sent` are dead —
expressed as send_intent/sent with `stage` set (issue §1).
"""

import json
import logging
import os
import re
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Iterable, Optional
from zoneinfo import ZoneInfo

import occurrence as _occurrence
from clock import parse_instant

log = logging.getLogger("event_store")

VALID_EVENTS = frozenset({
    "taken", "skipped", "missed", "undone", "snoozed",
    "send_intent", "sent", "send_failed", "clock_anomaly", "reconstituted",
    "restocked", "counted",
})

VALID_STAGES = frozenset({
    "reminder", "snooze_reminder", "nudge", "catchup", "overnight", "digest",
    "delivery",   # #21: a note naming one message that keeps failing
})
# Repeat nudges (#11) are "nudge-<minutes after the dose was due>"
_REPEAT_NUDGE = re.compile(r"^nudge-[0-9]+$")

# Serialization field order (issue §1); absent fields are omitted, not nulled.
_EVENT_FIELDS = (
    "id", "ts_utc", "med_id", "event",
    "occurrence_key", "occurrence_utc", "generation", "stage",
    "dose_prescribed", "dose_taken", "taken_at_utc",
    "ref", "attempt", "lease_until_utc", "error",
    "vial_mg", "diluent_ml", "qty",
)
_OPTIONAL_FIELDS = _EVENT_FIELDS[4:]


def _iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()


def new_event(med_id: str, event: str, ts_utc: datetime,
              occurrence=None, **fields) -> dict:
    """
    Build one event dict. `occurrence` (occurrence.Occurrence) fills
    occurrence_key/occurrence_utc; other optional fields per _EVENT_FIELDS.
    An explicit `id` overrides the generated uuid4 (used by migration).
    """
    if event not in VALID_EVENTS:
        raise ValueError(f"unknown event '{event}' (valid: {sorted(VALID_EVENTS)})")
    ev = {
        "id": fields.pop("id", None) or str(uuid.uuid4()),
        "ts_utc": _iso(ts_utc),
        "med_id": med_id,
        "event": event,
    }
    if occurrence is not None:
        ev["occurrence_key"] = occurrence.key
        ev["occurrence_utc"] = _iso(occurrence.utc)
    for key in _OPTIONAL_FIELDS:
        if key in fields:
            val = fields.pop(key)
            if val is not None:
                ev[key] = val
    if "stage" in ev and ev["stage"] not in VALID_STAGES \
            and not _REPEAT_NUDGE.match(ev["stage"]):
        raise ValueError(f"unknown stage '{ev['stage']}' (valid: {sorted(VALID_STAGES)})")
    if fields:
        raise TypeError(f"unknown event fields: {sorted(fields)}")
    return ev


def append_events(path, events: Iterable[dict], logger=None) -> list:
    """
    Append events whose id is not already stored (one JSON line each,
    flush + fsync). Returns the events actually appended.

    Callers must hold the state lock — safe_write.transact does.
    """
    path = Path(path)
    events = list(events)
    if not events:
        return []

    known = set()
    if path.exists():
        with path.open(encoding="utf-8") as f:
            for line in f:
                try:
                    known.add(json.loads(line)["id"])
                except (json.JSONDecodeError, KeyError, TypeError):
                    continue  # a torn tail must not block appends; load_events reports it

    fresh, seen = [], set()
    for ev in events:
        eid = ev.get("id")
        if not eid or eid in known or eid in seen:
            continue
        seen.add(eid)
        fresh.append(ev)
    if not fresh:
        return []

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for ev in fresh:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())
    return fresh


def load_events(path, logger=None) -> list:
    """
    All stored events in file order, deduped by id (last line wins).

    A torn last line — a crash mid-append — is skipped and logged. A bad
    line anywhere else is real corruption and raises ValueError.
    """
    path = Path(path)
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        lines = f.read().split("\n")
    if lines and lines[-1] == "":
        lines.pop()  # trailing newline

    events, index = [], {}
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        try:
            ev = json.loads(line)
            eid = ev["id"]
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            if i == len(lines) - 1:
                (logger or log).warning(
                    "event_store: torn last line skipped (%d bytes): %s", len(line), e)
                continue
            raise ValueError(f"history corrupt at line {i + 1}: {e}") from e
        if eid in index:
            events[index[eid]] = ev  # last wins, order preserved
        else:
            index[eid] = len(events)
            events.append(ev)
    return events


# ── Outcome resolution ─────────────────────────────────────────────────────────
#
# Terminal outcome per (occurrence, generation). Precedence (issue §1):
# taken > skipped > missed — a late `taken` overrides an earlier `missed`,
# so adherence counts the dose as taken (late).

_PRECEDENCE = {"taken": 3, "skipped": 2, "missed": 1}


def outcome(events: Iterable[dict], occurrence_key: str, generation: int = 0,
            med_id: Optional[str] = None) -> Optional[str]:
    """
    Resolve the terminal outcome of (occurrence, generation), or None.

    med_id scopes the lookup when given — wall-time keys are only unique
    per med (two meds can both have "2026-04-21T08:00#0").
    """
    best, best_rank, best_ts = None, 0, ""
    for ev in events:
        if med_id is not None and ev.get("med_id") != med_id:
            continue
        if ev.get("occurrence_key") != occurrence_key:
            continue
        if int(ev.get("generation") or 0) != generation:
            continue
        rank = _PRECEDENCE.get(ev.get("event"))
        if rank is None:
            continue
        ts = str(ev.get("ts_utc") or "")
        if rank > best_rank or (rank == best_rank and ts > best_ts):
            best, best_rank, best_ts = ev["event"], rank, ts
    return best


# ── Keyed migration (issue §1) ─────────────────────────────────────────────────
#
# One-time, idempotent. state.history entries become store events keyed from
# their timestamp and the schedule; confirmed_dose anchors the last `taken`
# exactly. Deterministic ids (`mig-<sha256…>`) mean a crash between the
# history append and the state write heals on the next attempt: the re-run
# appends nothing new.

# legacy state.history event → store event
_LEGACY_EVENT_MAP = {
    "taken": "taken",
    "missed": "missed",
    "late_nudge_sent": "sent",   # stage=nudge (issue §1)
    "deferred": "skipped",
}


def migration_event_id(med_id: str, event: str, stage: Optional[str],
                       occurrence_key: str, ts_utc: str) -> str:
    raw = "|".join((med_id, event, stage or "", occurrence_key, ts_utc))
    return "mig-" + sha256(raw.encode("utf-8")).hexdigest()[:24]


def migrate_state(state: dict, now_utc: datetime) -> tuple:
    """
    Migrate legacy state into events. Returns (new_state, events); events is
    empty when the watermark is already set. Sets
    state.tick.watermark_utc = now_utc (the migration instant — nothing
    before it is ever enumerated, so migration day produces no phantom
    misses). The input state is not mutated.
    """
    if (state.get("tick") or {}).get("watermark_utc"):
        return state, []
    tz = ZoneInfo(state["global"]["timezone"])
    events = []
    for med in state.get("meds", []):
        events.extend(_migration_events_for_med(med, tz))
    new_state = deepcopy(state)
    new_state.setdefault("tick", {})["watermark_utc"] = _iso(now_utc)
    return new_state, events


def _migration_events_for_med(med: dict, tz: ZoneInfo) -> list:
    mstate = med.get("state") or {}
    hist = mstate.get("history") or []
    cd_raw = mstate.get("confirmed_dose")
    confirmed = parse_instant(cd_raw) if cd_raw else None
    if not hist and confirmed is None:
        return []
    sched = med.get("schedule") or {}
    last_taken_i = None
    for i in range(len(hist) - 1, -1, -1):
        if hist[i].get("event") == "taken":
            last_taken_i = i
            break

    events = []
    for i, entry in enumerate(hist):
        legacy = entry.get("event")
        event = _LEGACY_EVENT_MAP.get(legacy)
        if event is None:
            continue  # unknown legacy event — left behind, not invented
        ts = parse_instant(entry["timestamp"])
        stage = "nudge" if legacy == "late_nudge_sent" else None
        if legacy == "taken":
            if i == last_taken_i and confirmed is not None:
                occ = _occurrence.for_instant(sched, confirmed, tz)
            else:
                occ = (_occurrence.covered_occurrence(sched, ts, tz)
                       or _occurrence.at_utc(ts, tz))
        else:
            # a miss/nudge/defer logged at T refers to the most recent dose
            occ = (_occurrence.most_recent_past(sched, ts, tz)
                   or _occurrence.at_utc(ts, tz))
        events.append(new_event(
            med["id"], event, ts,
            id=migration_event_id(med["id"], event, stage, occ.key, _iso(ts)),
            occurrence=occ, stage=stage,
            dose_prescribed=entry.get("dose_prescribed"),
            dose_taken=entry.get("dose_taken"),
        ))

    if confirmed is not None and last_taken_i is None:
        # confirmed status whose taken entry was trimmed away — anchor it anyway
        occ = _occurrence.for_instant(sched, confirmed, tz)
        events.append(new_event(
            med["id"], "taken", confirmed,
            id=migration_event_id(med["id"], "taken", None, occ.key, _iso(confirmed)),
            occurrence=occ,
            dose_prescribed=f"{med.get('dose', '')}{med.get('unit', '')}" or None,
        ))
    return events


# ── state.history mirror (one release, for rollback) ──────────────────────────
#
# The last MIRROR_MAX events are mirrored into state.history in legacy format
# so pre-PR2 code keeps reading consistent state. Only legacy-representable
# events are mirrored; new code never writes `deferred` (issue §1).

MIRROR_MAX = 30

_MIRROR_EVENT_MAP = {"taken": "taken", "missed": "missed"}


def mirror_entry(event: dict) -> Optional[dict]:
    """Legacy state.history entry for a store event, or None if unrepresentable."""
    ev = event.get("event")
    if ev == "sent" and (event.get("stage") == "nudge"
                         or _REPEAT_NUDGE.match(event.get("stage") or "")):
        legacy = "late_nudge_sent"
    elif ev in _MIRROR_EVENT_MAP:
        legacy = _MIRROR_EVENT_MAP[ev]
    else:
        return None
    entry = {
        "timestamp": event.get("ts_utc"),
        "event": legacy,
        "dose_prescribed": event.get("dose_prescribed") or "",
    }
    if event.get("dose_taken") is not None:
        entry["dose_taken"] = event["dose_taken"]
    return entry
