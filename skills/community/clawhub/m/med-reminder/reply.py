#!/usr/bin/env python3
"""
reply.py — AI reply handler for med reminder skill.

Called by the AI agent when the user sends a dose confirmation or deferral.
Separate from dispatch.py (the scheduler) because these have different:
  - failure modes: user is present, errors should be descriptive stdout
  - call patterns: invoked by the AI, not by a scheduler
  - retry semantics: agent can re-invoke; scheduler uses advisory skip

Subcommands (issue #1 §6 — all writes go through transact):
    init --timezone TZ --quiet-start HH:MM --quiet-end HH:MM --channel NAME
                               Create meds-state.json (first run only)
    confirm <med-id>           Mark one med as taken (prescribed dose)
    confirm --all              Mark all scheduled, non-paused meds as taken
    skip <med-id>              Skip a dose (past/current, or --dose HH:MM)
    snooze <med-id>            Push the pending dose's reminder later
    defer   <med-id>           Deprecated alias for snooze
    undo <med-id>              Undo the most recent taken/skipped (24h)
    pause/unpause <med-id>     Stop or resume reminders for one med
    reconstitute <med-id> --vial-mg X --diluent-ml Y
                               Log a vial mix; reminders then show syringe units
    restock <med-id> --qty N | --set N
                               Add N inventory units, or record N on hand
    add-med --json -           Add a med from a JSON object on stdin
    edit-med <med-id> --json - Edit a med from a JSON object on stdin
    set-quiet-hours HH:MM HH:MM
    remove <med-id> --yes      Remove a med (history lines remain)
    status                     Read-only summary
    show-state                 Print the state sha256 for CLI writers

Any id-taking command accepts --position N instead of a med id: it picks
the Nth med from today's digest order (global.last_digest_order).

Options:
    --dose-taken TEXT          Actual dose if different from prescribed (confirm only)
    --dose HH:MM               Pin the scheduled dose being confirmed (confirm only)
    --taken-at HH:MM           When the dose was taken — most recent past wall time
    --force NONCE              Override a duplicate refusal (nonce from the exit-3 message)
    --dry-run                  Print without writing state
    --state PATH               Path to meds-state.json (overrides MEDS_STATE_FILE)

Exit codes (confirm): 3 = duplicate: that dose is already logged, or a log
within the med's minimum gap that isn't simply the next scheduled dose (a
--force nonce is printed); 4 = ambiguous which dose (the agent asks).

Environment:
    MEDS_STATE_FILE   Path to meds-state.json   (default: same dir as script)
    MEDS_LOG_FILE     Path to reply.log          (default: same dir as script)
"""

import argparse
import copy
import json
import logging
import math
import os
import re
import sys
from pathlib import Path

if sys.version_info < (3, 9):
    sys.exit(f"Python 3.9+ required — found {sys.version.split()[0]}")

# Console output includes unicode (em-dashes) that cp1252 consoles can't encode
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

# Import shared helpers from dispatch — no scheduler-side code brought in
import dispatch as _dispatch_mod
import event_store as _event_store_mod
import inventory as _inv
import occurrence as _occurrence_mod
import reconstitution as _rc
import safe_write as _safe_write_mod
from clock import Clock, get_clock, parse_instant
from dispatch import (
    compute_next_due,
    find_med,
    get_tz,
    load_state,
)
from attribution import (
    ALL_AFTER_DIGEST_WINDOW,
    DIGEST_GRACE,
    EARLY_WINDOW,
    attribute,
    duplicate_of,
    generation as occurrence_generation,
    min_gap,
    nearest_dose_occurrence,
    outcome_for,
    resolve_taken_at,
    when_label,
)
from datetime import datetime, timedelta, timezone
from occurrence import Occurrence
from secrets import token_hex
from typing import Optional
from zoneinfo import ZoneInfo

log = logging.getLogger("reply")

# Exit codes (issue #1 §4): 3 duplicate within min-gap, 4 ambiguous dose.
EXIT_DUPLICATE = 3
EXIT_AMBIGUOUS = 4
EXIT_BAD_OPTION = 2

# A printed duplicate-override nonce is valid for this long (issue §4).
NONCE_TTL = timedelta(minutes=10)

# Snooze bounds (issue #1 §6, #11): default 120 minutes, allowed 5–240, and
# the wake must land before the dose closes at the next dose. `defer` is
# the deprecated alias capped at min(120, cap).
SNOOZE_DEFAULT = 120
SNOOZE_MIN = 5
SNOOZE_MAX = 240
DEFER_MINUTES = 120

# Undo only reaches the most recent taken/skipped, within 24h (issue §6).
UNDO_WINDOW = timedelta(hours=24)

_HHMM_RE = re.compile(r"^([01][0-9]|2[0-3]):[0-5][0-9]$")


def setup_logging(dry_run: bool) -> None:
    log_path = Path(os.environ.get("MEDS_LOG_FILE", SCRIPT_DIR / "reply.log"))
    _safe_write_mod.configure_root_logging(
        "reply", log_path, logging.DEBUG if dry_run else logging.INFO)


# ── Confirm (issue #1 §4) ──────────────────────────────────────────────────────

def _fmt_12h(dt: datetime) -> str:
    """08:05 → '8:05am', 20:00 → '8:00pm'."""
    return f"{dt.hour % 12 or 12}:{dt.minute:02d}{'am' if dt.hour < 12 else 'pm'}"


def _taken_instant(event: dict) -> datetime:
    return parse_instant(event.get("taken_at_utc") or event["ts_utc"])


def _find_med(state: dict, med_id: str) -> Optional[dict]:
    return next((m for m in state["meds"] if m["id"] == med_id), None)


def _resolve_target(state: dict, med_id: Optional[str], position: Optional[int],
                    tz, now: datetime) -> dict:
    """
    The med a reply targets: by id, or --position N into today's recorded
    digest order (issue #1 §6). A previous day's order is refused — the
    listing may have changed — and a position reply echoes the resolved
    name so the user can catch a mismatch.
    """
    if position is not None:
        if med_id is not None:
            print("Error: pass either a med id or --position, not both.")
            raise SystemExit(EXIT_BAD_OPTION)
        g = state["global"]
        order = g.get("last_digest_order") or []
        recorded = g.get("last_digest_date")
        today = now.astimezone(tz).date().isoformat()
        if recorded != today:
            print(f"Error: no digest order for today (last recorded "
                  f"{recorded or 'never'}) — use the med's name or id.")
            raise SystemExit(EXIT_BAD_OPTION)
        if not 1 <= position <= len(order):
            print(f"Error: --position must be 1–{len(order)} (today's digest "
                  f"listed {len(order)} med(s)).")
            raise SystemExit(EXIT_BAD_OPTION)
        med_id = order[position - 1]
    med = find_med(state, med_id)
    if position is not None:
        print(f"Position {position}: {med['name']} ({med['id']}).")
    return med


def _digest_window_open(history, now: datetime) -> bool:
    """
    True within DIGEST_GRACE after the last delivered digest — the only
    case where the wide 6h early window applies (issue §4).
    """
    last = None
    for e in history:
        if e.get("event") == "sent" and e.get("stage") == "digest":
            ts = parse_instant(e["ts_utc"])
            if last is None or ts > last:
                last = ts
    return last is not None and now - last <= DIGEST_GRACE


def _decide_credit(med: dict, history, taken_at, tz, dose_pin=None,
                   early_window=EARLY_WINDOW):
    """
    Pure decision: which occurrence (if any) a confirm credits.
    Raises SystemExit(4) on ambiguity, SystemExit(EXIT_BAD_OPTION) on a
    bad --dose. Returns the Occurrence or None (unattributed).
    """
    if dose_pin is not None:
        if not med["schedule"].get("times"):
            print(f"Error: {med['name']} has no scheduled dose times to pin.")
            raise SystemExit(EXIT_BAD_OPTION)
        try:
            return nearest_dose_occurrence(med, dose_pin, taken_at, tz)
        except ValueError as e:
            print(f"Error: {e}")
            raise SystemExit(EXIT_BAD_OPTION)

    kind, payload = attribute(med, history, taken_at, tz, early_window)
    if kind == "ambiguous":
        past, future = payload
        print(f"Which dose do you mean for {med['name']}?")
        print(f"  1) {_fmt_12h(past.local)} ({past.local:%a}) — the dose you may have taken late")
        print(f"  2) {_fmt_12h(future.local)} ({future.local:%a}) — early, ahead of schedule")
        print("Reply with the time you took it, e.g. 'took it at 8'.")
        log.info("CONFIRM [%s] ambiguous between %s and %s — asking",
                 med["id"], past.key, future.key)
        raise SystemExit(EXIT_AMBIGUOUS)
    return payload if kind == "credit" else None


def _next_due_for(med: dict, occ, taken_at: datetime, tz) -> Optional[datetime]:
    """Legacy next_due re-anchor; interval meds re-anchor on taken_at."""
    sched = med["schedule"]
    if sched["frequency"] == "as_needed":
        return None
    if sched["frequency"] == "interval":
        return taken_at + timedelta(hours=float(sched["interval_hours"]))
    return compute_next_due(med, occ.utc if occ is not None else taken_at, tz)


def _apply_taken(state: dict, med: dict, occ, taken_at: datetime,
                 dose_taken: Optional[str], history_view) -> dict:
    """Build the `taken` event + legacy state updates (pure)."""
    gen = 0
    if occ is not None:
        gen = occurrence_generation(history_view, med["id"], occ.key)
    event = _event_store_mod.new_event(
        med["id"], "taken", taken_at, occurrence=occ, generation=gen,
        dose_prescribed=f"{med['dose']}{med['unit']}",
        dose_taken=dose_taken, taken_at_utc=taken_at.isoformat(),
    )
    tz = ZoneInfo(state["global"]["timezone"])
    mstate = med["state"]
    mstate["status"] = "confirmed"
    mstate["last_taken"] = taken_at.isoformat()
    if occ is not None and med["schedule"]["frequency"] not in ("interval", "as_needed"):
        mstate["confirmed_dose"] = occ.utc.isoformat()
    nd = _next_due_for(med, occ, taken_at, tz)
    mstate["next_due"] = nd.isoformat() if nd else None
    return event


def _offer_nonce(state: dict, med_id: str, taken_at: datetime, now: datetime) -> str:
    nonce = token_hex(4)
    tick = state.setdefault("tick", {})
    offers = {k: v for k, v in (tick.get("force_nonces") or {}).items()
              if parse_instant(v["expires_utc"]) > now}
    offers[nonce] = {"med_id": med_id, "taken_at_utc": taken_at.isoformat(),
                     "expires_utc": (now + NONCE_TTL).isoformat()}
    tick["force_nonces"] = offers
    return nonce


def _valid_nonce(state: dict, med_id: str, nonce: str, now: datetime) -> bool:
    offer = ((state.get("tick") or {}).get("force_nonces") or {}).get(nonce)
    return bool(offer and offer.get("med_id") == med_id
                and parse_instant(offer["expires_utc"]) > now)


def handle_confirm(med_id: str, dose_taken: Optional[str], dry_run: bool,
                   clock: Optional[Clock] = None, dose_pin: str = None,
                   taken_at_raw: str = None, force: str = None,
                   position: Optional[int] = None) -> None:
    clock = clock or get_clock()
    state = load_state()
    tz = get_tz(state)
    now = clock.now_utc()
    med = _resolve_target(state, med_id, position, tz, now)
    med_id = med["id"]                     # --position resolves to the real id

    if med.get("paused"):
        log.info("SKIP [confirm] %s — med is paused", med_id)
        print(f"Skipped: {med['name']} is paused.")
        return

    if taken_at_raw:
        try:
            taken_at = resolve_taken_at(taken_at_raw, tz, now)
        except ValueError as e:
            print(f"Error: {e}")
            raise SystemExit(EXIT_BAD_OPTION)
    else:
        taken_at = now

    history = _event_store_mod.load_events(_safe_write_mod.history_file())
    occ = _decide_credit(med, history, taken_at, tz, dose_pin)

    gap = min_gap(med)
    last = duplicate_of(history, med, occ, taken_at)

    if dry_run:
        if last is not None:
            print(f"[DRY RUN] Would refuse: already logged "
                  f"{when_label(_taken_instant(last), tz, now)}.")
        else:
            slot = _fmt_12h(occ.local) if occ else "no scheduled dose"
            print(f"[DRY RUN] Would log {med['name']} as your {slot} dose.")
        return

    outcome = {}

    def fn(state_copy, history_view):
        med_c = _find_med(state_copy, med_id)
        if med_c is None:
            raise ValueError(f"med {med_id} disappeared mid-confirm")
        # re-decide under the lock — a tick or another confirm may have acted
        occ_c = _decide_credit(med_c, history_view, taken_at, tz, dose_pin)
        last_c = duplicate_of(history_view, med_c, occ_c, taken_at)
        dup_c = last_c is not None

        if dup_c and not (force and _valid_nonce(state_copy, med_id, force, now)):
            if force:
                print("Error: that override nonce is not valid (wrong or older "
                      "than 10 minutes). Here is a fresh one.")
            nonce = _offer_nonce(state_copy, med_id, taken_at, now)
            outcome["duplicate"] = (last_c, occ_c, nonce)
            return state_copy, []

        if dup_c and force:
            state_copy.setdefault("tick", {}).get("force_nonces", {}).pop(force, None)
        event = _apply_taken(state_copy, med_c, occ_c, taken_at, dose_taken, history_view)
        outcome["ok"] = (occ_c, med_c["state"].get("next_due"))
        return state_copy, [event]

    _safe_write_mod.transact(fn, clock=clock)

    if "duplicate" in outcome:
        last_ev, dup_occ, nonce = outcome["duplicate"]
        at = _taken_instant(last_ev).astimezone(tz)
        same_dose = dup_occ is not None and last_ev.get("occurrence_key") == dup_occ.key
        why = (f"That's your {_fmt_12h(dup_occ.local)} dose — it's already logged."
               if same_dose else
               f"That's within the {int(gap.total_seconds() // 3600)}-hour "
               f"minimum gap for this med.")
        print(f"Already logged {med['name']} {when_label(at, tz, now)}. {why}")
        print(f"If you really took it again, rerun with: --force {nonce} "
              f"(valid 10 minutes)")
        log.info("CONFIRM [%s] refused as duplicate of %s", med_id, at.isoformat())
        raise SystemExit(EXIT_DUPLICATE)

    occ, next_due = outcome["ok"]
    if occ is not None:
        print(f"Logged as your {_fmt_12h(occ.local)} dose.")
    else:
        print("Couldn't tell which scheduled dose this was — logged it "
              "without a schedule slot.")
    nd_str = ""
    if next_due:
        nd_dt = parse_instant(next_due).astimezone(tz)
        nd_str = f" Next due: {nd_dt:%a} {_fmt_12h(nd_dt)}."
    draw = _rc.med_draw(med, history, now) if dose_taken is None else None
    units = f" ({_rc.units_phrase(draw)})" if draw else ""
    print(f"{med['name']} {med['dose']}{med['unit']}{units}.{nd_str}")
    log.info("CONFIRM [%s] credited %s", med_id, occ.key if occ else "(unattributed)")


def handle_confirm_all(dose_taken: Optional[str], dry_run: bool,
                       clock: Optional[Clock] = None) -> None:
    clock = clock or get_clock()
    state = load_state()
    tz = get_tz(state)
    now = clock.now_utc()
    history = _event_store_mod.load_events(_safe_write_mod.history_file())
    early = ALL_AFTER_DIGEST_WINDOW if _digest_window_open(history, now) else EARLY_WINDOW

    notes, credited = [], []

    def fn(state_copy, history_view):
        events = []
        for med in state_copy["meds"]:
            if med.get("paused"):
                notes.append(f"{med['name']} (paused)")
                continue
            if med["schedule"]["frequency"] == "as_needed":
                notes.append(f"{med['name']} (as-needed — confirm individually if taken)")
                continue
            try:
                occ = _decide_credit(med, history_view, now, tz, None, early)
            except SystemExit:
                notes.append(f"{med['name']} (which dose? confirm it individually)")
                continue
            if duplicate_of(history_view, med, occ, now) is not None:
                notes.append(f"{med['name']} (already logged recently)")
                continue
            events.append(_apply_taken(state_copy, med, occ, now, dose_taken, history_view))
            credited.append(med["name"])
        return state_copy, events

    if dry_run:
        print(f"[DRY RUN] Would confirm {len(state['meds'])} med(s).")
        return

    _safe_write_mod.transact(fn, clock=clock)

    if credited:
        print(f"Confirmed: {', '.join(credited)}.")
    if notes:
        print(f"Skipped: {', '.join(notes)}.")
    if not credited and not notes:
        print("Nothing to confirm — no active meds found.")


# ── Snooze / defer / skip (issue #1 §6) ────────────────────────────────────────

def _most_recent_occurrence(med: dict, now: datetime, tz):
    """
    The latest occurrence at or before `now`. Interval meds walk the anchor
    chain (state.next_due, else active_since); as-needed meds have none.
    """
    sched = med["schedule"]
    freq = sched.get("frequency")
    if freq == "as_needed":
        return None
    if freq == "interval":
        step = timedelta(hours=float(sched["interval_hours"]))
        anchor = None
        for raw in ((med.get("state") or {}).get("next_due"), med.get("active_since_utc")):
            if raw:
                anchor = parse_instant(raw)
                break
        if anchor is None:
            return None
        asof = now.astimezone(timezone.utc)
        k = (asof - anchor) // step if asof >= anchor else -1
        return _occurrence_mod.at_utc(anchor + k * step, tz) if k >= 0 else None
    return _occurrence_mod.most_recent_past(sched, now, tz)


def _current_dose(med: dict, history, now: datetime, tz):
    """
    The dose a skip/snooze reply targets: the most recent occurrence at or
    before `now` — nothing before active_since_utc was ever tracked. Returns
    (occurrence, generation, outcome) or (None, None, None).
    """
    occ = _most_recent_occurrence(med, now, tz)
    if occ is None:
        return None, None, None
    since = med.get("active_since_utc")
    if since and occ.utc < parse_instant(since):
        return None, None, None
    gen = occurrence_generation(history, med["id"], occ.key)
    return occ, gen, outcome_for(history, med["id"], occ.key, gen)


def _snooze_minutes(med: dict, occ, tz, requested: Optional[int],
                    defer_alias: bool, now: datetime) -> int:
    """
    Resolve the snooze duration: default 120, range 5–240, and the wake
    must land before the dose closes at the next dose (#11). An explicit
    duration past that is refused with the spec's message; the default
    shrinks to fit. `defer` uses min(120, cap).
    """
    close = _occurrence_mod.close_instant(med["schedule"], occ.utc, tz)
    cap = (close - now).total_seconds() / 60.0 - 1   # wake strictly before the close
    if requested is None and not defer_alias:
        minutes = min(SNOOZE_DEFAULT, int(cap))
        if minutes < SNOOZE_MIN:
            print(f"Error: snoozing {med['name']} would run into your next "
                  "dose; skip instead?")
            raise SystemExit(EXIT_BAD_OPTION)
        return minutes
    minutes = SNOOZE_DEFAULT if requested is None else requested
    if defer_alias:
        minutes = min(DEFER_MINUTES, int(cap))
        if minutes < SNOOZE_MIN:
            print(f"Error: snoozing {med['name']} would run into your next "
                  "dose; skip instead?")
            raise SystemExit(EXIT_BAD_OPTION)
        return minutes
    if not SNOOZE_MIN <= minutes <= SNOOZE_MAX:
        print(f"Error: --minutes must be {SNOOZE_MIN}–{SNOOZE_MAX} (got {minutes}).")
        raise SystemExit(EXIT_BAD_OPTION)
    if minutes > cap + 1e-9:
        print(f"Error: snoozing {med['name']} for {minutes} minutes would "
              "run into your next dose; skip instead?")
        raise SystemExit(EXIT_BAD_OPTION)
    return minutes


def handle_snooze(med_id: str, minutes: Optional[int], dry_run: bool,
                  clock: Optional[Clock] = None, position: Optional[int] = None,
                  defer_alias: bool = False) -> None:
    """
    Snooze the pending dose: writes `snoozed{occurrence, until}` with the
    wake instant in `ref` (the format tick.snooze_until_for reads). The
    reminder re-fires at `until` and nudges resume every late_threshold
    from there; the cap keeps `until` before the next dose closes it (#11).
    """
    clock = clock or get_clock()
    state = load_state()
    tz = get_tz(state)
    now = clock.now_utc()
    med = _resolve_target(state, med_id, position, tz, now)

    if med.get("paused"):
        print(f"Note: {med['name']} is paused — nothing to snooze.")
        return
    if med["schedule"]["frequency"] == "as_needed":
        print(f"Error: {med['name']} is as-needed — there is no scheduled dose to snooze.")
        raise SystemExit(EXIT_BAD_OPTION)

    history = _event_store_mod.load_events(_safe_write_mod.history_file())
    occ, gen, res = _current_dose(med, history, now, tz)
    if occ is None:
        print(f"Error: no dose of {med['name']} is due right now — nothing to snooze.")
        raise SystemExit(EXIT_BAD_OPTION)
    if res is not None:
        state_desc = {"taken": "logged as taken", "skipped": "skipped",
                      "missed": "logged missed"}[res]
        print(f"Error: the {_fmt_12h(occ.local)} dose of {med['name']} was "
              f"already {state_desc}.")
        raise SystemExit(EXIT_BAD_OPTION)

    minutes = _snooze_minutes(med, occ, tz, minutes, defer_alias, now)
    until = now + timedelta(minutes=minutes)

    if dry_run:
        print(f"[DRY RUN] Would snooze {med['name']} until "
              f"{_fmt_12h(until.astimezone(tz))} ({minutes} minutes).")
        return

    outcome = {}

    def fn(state_copy, history_view):
        med_c = _find_med(state_copy, med["id"])
        if med_c is None:
            raise ValueError(f"med {med['id']} disappeared mid-snooze")
        # re-derive under the lock — another reply may have resolved the dose
        occ_c, gen_c, res_c = _current_dose(med_c, history_view, now, tz)
        if occ_c is None or occ_c.key != occ.key or res_c is not None:
            outcome["conflict"] = True
            return state_copy, []
        until_c = now + timedelta(minutes=minutes)
        outcome["ok"] = (occ_c, until_c)
        return state_copy, [_event_store_mod.new_event(
            med["id"], "snoozed", now, occurrence=occ_c, generation=gen_c,
            ref=until_c.isoformat(),
        )]

    _safe_write_mod.transact(fn, clock=clock)

    if outcome.get("conflict"):
        print(f"Error: the {_fmt_12h(occ.local)} dose of {med['name']} was just "
              "logged by another reply — nothing snoozed.")
        raise SystemExit(EXIT_BAD_OPTION)

    occ_ok, until_ok = outcome["ok"]
    print(f"Snoozed {med['name']} until {_fmt_12h(until_ok.astimezone(tz))} "
          f"({minutes} minutes).")
    if defer_alias:
        print("Note: 'defer' is deprecated — it snoozes now; use 'snooze' next time.")
    log.info("SNOOZE [%s] %s until %s", med["id"], occ_ok.key, until_ok.isoformat())


def handle_defer(med_id: str, dry_run: bool, clock: Optional[Clock] = None,
                 position: Optional[int] = None) -> None:
    """Deprecated alias for snooze, minutes = min(120, cap) (issue #1 §6)."""
    handle_snooze(med_id, None, dry_run, clock=clock, position=position,
                  defer_alias=True)


def handle_skip(med_id: str, dose_pin: Optional[str], dry_run: bool,
                clock: Optional[Clock] = None,
                position: Optional[int] = None) -> None:
    """
    Skip a dose: writes `skipped` — the occurrence never becomes missed.
    Without --dose only a past or current occurrence is targeted; a future
    one requires --dose (the agent confirms which dose is meant).
    """
    clock = clock or get_clock()
    state = load_state()
    tz = get_tz(state)
    now = clock.now_utc()
    med = _resolve_target(state, med_id, position, tz, now)

    if med.get("paused"):
        print(f"Note: {med['name']} is paused — its doses aren't tracked while paused.")
        return

    history = _event_store_mod.load_events(_safe_write_mod.history_file())

    if dose_pin is not None:
        try:
            occ = nearest_dose_occurrence(med, dose_pin, now, tz)
        except ValueError as e:
            print(f"Error: {e}")
            raise SystemExit(EXIT_BAD_OPTION)
    else:
        occ, _, _ = _current_dose(med, history, now, tz)
        if occ is None:
            print(f"Error: no dose of {med['name']} is due right now — to skip "
                  "a future dose, add --dose HH:MM.")
            raise SystemExit(EXIT_BAD_OPTION)

    gen = occurrence_generation(history, med["id"], occ.key)
    res = outcome_for(history, med["id"], occ.key, gen)
    if res == "taken":
        print(f"Error: the {_fmt_12h(occ.local)} dose of {med['name']} is "
              "already logged as taken — undo it first, or use --dose HH:MM "
              "for a later dose.")
        raise SystemExit(EXIT_BAD_OPTION)
    if res == "skipped":
        print(f"Error: the {_fmt_12h(occ.local)} dose of {med['name']} is "
              "already skipped.")
        raise SystemExit(EXIT_BAD_OPTION)

    if dry_run:
        print(f"[DRY RUN] Would skip {med['name']} {_fmt_12h(occ.local)} dose.")
        return

    outcome = {}

    def fn(state_copy, history_view):
        med_c = _find_med(state_copy, med["id"])
        if med_c is None:
            raise ValueError(f"med {med['id']} disappeared mid-skip")
        gen_c = occurrence_generation(history_view, med["id"], occ.key)
        if outcome_for(history_view, med["id"], occ.key, gen_c) in ("taken", "skipped"):
            outcome["conflict"] = True
            return state_copy, []
        outcome["ok"] = (occ, gen_c)
        return state_copy, [_event_store_mod.new_event(
            med["id"], "skipped", now, occurrence=occ, generation=gen_c,
            dose_prescribed=f"{med['dose']}{med['unit']}",
        )]

    _safe_write_mod.transact(fn, clock=clock)

    if outcome.get("conflict"):
        print(f"Error: the {_fmt_12h(occ.local)} dose of {med['name']} was just "
              "logged by another reply — not skipped.")
        raise SystemExit(EXIT_BAD_OPTION)

    occ_ok, _ = outcome["ok"]
    print(f"Skipped {med['name']} {_fmt_12h(occ_ok.local)} dose.")
    log.info("SKIP [%s] %s", med["id"], occ_ok.key)


# ── Undo (issue #1 §6) ─────────────────────────────────────────────────────────

def _undoable_event(history, med_id: str, now: datetime) -> Optional[dict]:
    """
    The most recent `taken` or `skipped` for this med within 24h that has
    no matching `undone` — or None. `undone{ref}` names the event it
    undoes, so a second undo finds nothing.
    """
    undone_refs = {e.get("ref") for e in history
                   if e.get("event") == "undone" and e.get("med_id") == med_id}
    best, best_ts = None, None
    for e in history:
        if e.get("event") not in ("taken", "skipped") or e.get("med_id") != med_id:
            continue
        if e.get("id") in undone_refs:
            continue
        ts = parse_instant(e["ts_utc"])
        if ts > now or ts < now - UNDO_WINDOW:
            continue
        if best_ts is None or ts > best_ts:
            best, best_ts = e, ts
    return best


def handle_undo(med_id: str, dry_run: bool, clock: Optional[Clock] = None,
                position: Optional[int] = None) -> None:
    """
    Undo the most recent taken or skipped dose (within 24h): writes
    `undone{ref}`, bumping the occurrence's generation so it is unresolved
    again. Before T+late the tick re-reminds; after T+missed it writes a
    silent missed (PR 2's stage logic — nothing to do here but record).
    """
    clock = clock or get_clock()
    state = load_state()
    tz = get_tz(state)
    now = clock.now_utc()
    med = _resolve_target(state, med_id, position, tz, now)

    history = _event_store_mod.load_events(_safe_write_mod.history_file())
    ref_ev = _undoable_event(history, med["id"], now)
    if ref_ev is None:
        print(f"Error: nothing to undo for {med['name']} — no taken or "
              "skipped dose in the last 24 hours.")
        raise SystemExit(1)

    if dry_run:
        print(f"[DRY RUN] Would undo the {ref_ev['event']} event for "
              f"{med['name']} from {_fmt_12h(parse_instant(ref_ev['ts_utc']).astimezone(tz))}.")
        return

    outcome = {}

    def fn(state_copy, history_view):
        med_c = _find_med(state_copy, med["id"])
        if med_c is None:
            raise ValueError(f"med {med['id']} disappeared mid-undo")
        ev_c = _undoable_event(history_view, med["id"], now)
        if ev_c is None or ev_c["id"] != ref_ev["id"]:
            outcome["conflict"] = True
            return state_copy, []
        occ_c = None
        if ev_c.get("occurrence_key"):
            occ_c = Occurrence(utc=parse_instant(ev_c["occurrence_utc"]),
                               key=ev_c["occurrence_key"], tz=tz)
        # legacy status is a rollback cache — never leave it claiming confirmed
        if ev_c["event"] == "taken" and med_c["state"].get("status") == "confirmed":
            med_c["state"]["status"] = "pending"
        outcome["ok"] = ev_c
        return state_copy, [_event_store_mod.new_event(
            med["id"], "undone", now, occurrence=occ_c,
            generation=int(ev_c.get("generation") or 0), ref=ev_c["id"],
        )]

    _safe_write_mod.transact(fn, clock=clock)

    if outcome.get("conflict"):
        print("Error: nothing to undo — another reply just changed it.")
        raise SystemExit(1)

    ev = outcome["ok"]
    occ = None
    if ev.get("occurrence_key"):
        occ = Occurrence(utc=parse_instant(ev["occurrence_utc"]),
                         key=ev["occurrence_key"], tz=tz)
    slot = f" {_fmt_12h(occ.local)} dose" if occ is not None else " dose"
    if ev["event"] == "taken":
        at = _taken_instant(ev).astimezone(tz)
        print(f"Undid: {med['name']}{slot} — you had logged it taken at {_fmt_12h(at)}.")
    else:
        print(f"Undid: skipped {med['name']}{slot}.")
    if occ is not None:
        late = timedelta(minutes=med["escalation"]["late_threshold_minutes"])
        close = _occurrence_mod.close_instant(med["schedule"], occ.utc, tz)
        if now < occ.utc + late:
            print("You'll be reminded again.")
        elif now >= close:
            print("The next dose is already due — it will be logged as missed, silently.")
        else:
            print("You'll be nudged again.")
    log.info("UNDO [%s] %s", med["id"], ev["id"])


# ── Pause / unpause (issue #1 §6) ──────────────────────────────────────────────

def handle_pause(med_id: str, dry_run: bool, clock: Optional[Clock] = None,
                 position: Optional[int] = None) -> None:
    clock = clock or get_clock()
    state = load_state()
    tz = get_tz(state)
    now = clock.now_utc()
    med = _resolve_target(state, med_id, position, tz, now)

    if med.get("paused"):
        print(f"Note: {med['name']} is already paused.")
        return
    if dry_run:
        print(f"[DRY RUN] Would pause {med['name']}.")
        return

    def fn(state_copy, history_view):
        med_c = _find_med(state_copy, med["id"])
        if med_c is None:
            raise ValueError(f"med {med['id']} disappeared mid-pause")
        med_c["paused"] = True
        return state_copy, []

    _safe_write_mod.transact(fn, clock=clock)
    print(f"Paused {med['name']} — no reminders while it's paused.")
    log.info("PAUSE [%s]", med["id"])


def handle_unpause(med_id: str, dry_run: bool, clock: Optional[Clock] = None,
                   position: Optional[int] = None) -> None:
    """Unpause re-anchors tracking (active_since_utc = now): doses during
    the pause are never enumerated, so unpausing causes no phantom misses."""
    clock = clock or get_clock()
    state = load_state()
    tz = get_tz(state)
    now = clock.now_utc()
    med = _resolve_target(state, med_id, position, tz, now)

    if not med.get("paused"):
        print(f"Note: {med['name']} isn't paused.")
        return
    if dry_run:
        print(f"[DRY RUN] Would unpause {med['name']} (tracking restarts from now).")
        return

    def fn(state_copy, history_view):
        med_c = _find_med(state_copy, med["id"])
        if med_c is None:
            raise ValueError(f"med {med['id']} disappeared mid-unpause")
        med_c["paused"] = False
        med_c["active_since_utc"] = now.isoformat()
        return state_copy, []

    _safe_write_mod.transact(fn, clock=clock)
    print(f"Unpaused {med['name']} — tracking resumes from now; nothing during "
          "the pause is logged missed.")
    log.info("UNPAUSE [%s]", med["id"])


# ── Reconstitution (PR 8a, #10) ────────────────────────────────────────────────

def handle_reconstitute(med_id: str, vial_mg: float, diluent_ml: float,
                        dry_run: bool, clock: Optional[Clock] = None,
                        position: Optional[int] = None) -> None:
    """
    Log a vial mix as a `reconstituted` event. From then on reminders,
    nudges and the confirm echo carry the syringe units for the prescribed
    dose. Computes units for the dose the user chose — never suggests one.
    """
    clock = clock or get_clock()
    state = load_state()
    tz = get_tz(state)
    now = clock.now_utc()
    med = _resolve_target(state, med_id, position, tz, now)

    for label, val in (("--vial-mg", vial_mg), ("--diluent-ml", diluent_ml)):
        if not (math.isfinite(val) and val > 0):
            print(f"Error: {label} must be a positive number (got {val}).")
            raise SystemExit(EXIT_BAD_OPTION)
    mcg = _rc.dose_mcg(med)
    if mcg is None:
        print(f"Error: {med['name']} is dosed in {med['dose']}{med['unit']} — "
              "units can only be computed for a dose in mcg or mg.")
        raise SystemExit(EXIT_BAD_OPTION)
    draw = _rc.compute(mcg, vial_mg, diluent_ml, _rc.syringe_of(med))
    dose = f"{med['dose']}{med['unit']}"
    if draw.doses_per_vial < 1:
        print(f"Error: a {dose} dose is more than the whole vial "
              f"({_rc.fmt_num(vial_mg)} mg) — check the vial strength.")
        raise SystemExit(EXIT_BAD_OPTION)

    lines = [
        f"{_rc.fmt_num(vial_mg)} mg in {_rc.fmt_num(diluent_ml)} mL = "
        f"{_rc.fmt_num(draw.conc_mg_per_ml)} mg/mL.",
        f"{dose} = {_rc.units_phrase(draw)} on your {draw.syringe} "
        f"({_rc.fmt_num(draw.volume_ml, 3)} mL).",
        f"This vial holds about {math.floor(draw.doses_per_vial + 1e-9)} doses at {dose}.",
    ] + [f"Check: {w}" for w in draw.warnings]

    if dry_run:
        print(f"[DRY RUN] Would log a mix for {med['name']}:")
        for line in lines:
            print(line)
        return

    def fn(state_copy, history_view):
        if _find_med(state_copy, med["id"]) is None:
            raise ValueError(f"med {med['id']} disappeared mid-reconstitute")
        return state_copy, [_event_store_mod.new_event(
            med["id"], "reconstituted", now,
            vial_mg=vial_mg, diluent_ml=diluent_ml)]

    _safe_write_mod.transact(fn, clock=clock)
    print(f"Logged mix for {med['name']}:")
    for line in lines:
        print(line)
    log.info("RECONSTITUTE [%s] %s mg / %s mL", med["id"], vial_mg, diluent_ml)


# ── Inventory (PR 8b, #10) ─────────────────────────────────────────────────────

def handle_restock(med_id: str, qty: Optional[float], set_qty: Optional[float],
                   dry_run: bool, clock: Optional[Clock] = None,
                   position: Optional[int] = None) -> None:
    """
    `--qty N` logs `restocked{qty}` (N inventory units added — the first
    one starts tracking); `--set N` logs `counted{qty}` (a recount: N on
    hand now). On hand is always derived, never stored.
    """
    clock = clock or get_clock()
    state = load_state()
    tz = get_tz(state)
    now = clock.now_utc()
    med = _resolve_target(state, med_id, position, tz, now)
    unit = med.get("inventory_unit")
    if not unit:
        print(f"Error: {med['name']} has no inventory_unit — set one first, e.g. "
              f"edit-med {med['id']} with {{\"inventory_unit\": \"vial\"}}.")
        raise SystemExit(EXIT_BAD_OPTION)
    if (qty is None) == (set_qty is None):
        print("Error: pass exactly one of --qty (units added) or --set (units on hand).")
        raise SystemExit(EXIT_BAD_OPTION)
    value = qty if qty is not None else set_qty
    if not math.isfinite(value) or value < 0 or (qty is not None and value == 0):
        print(f"Error: {'--qty must be positive' if qty is not None else '--set must be 0 or more'}"
              f" (got {value}).")
        raise SystemExit(EXIT_BAD_OPTION)
    kind = "restocked" if qty is not None else "counted"

    if dry_run:
        print(f"[DRY RUN] Would log {kind} {value:g} {unit} for {med['name']}.")
        return

    def fn(state_copy, history_view):
        if _find_med(state_copy, med["id"]) is None:
            raise ValueError(f"med {med['id']} disappeared mid-restock")
        return state_copy, [_event_store_mod.new_event(med["id"], kind, now, qty=value)]

    _safe_write_mod.transact(fn, clock=clock)
    history = _event_store_mod.load_events(_safe_write_mod.history_file())
    line = _inv.status_line(med, history, now)
    verb = f"Added {value:g} {unit}" if qty is not None else f"Recorded {value:g} {unit} on hand"
    print(f"{verb} for {med['name']}." + (f" Now {line}." if line else ""))
    log.info("RESTOCK [%s] %s %s", med["id"], kind, value)


# ── Edit-time quiet-hours checks (issue #1 §6, AC 27) ─────────────────────────
#
# validate() never rejects quiet-hours conflicts (AC 26 — existing state
# must always load); add-med/edit-med/set-quiet-hours are where they're
# refused. The boundary mirrors the engine: a nudge in the FIRST 30 min of
# quiet hours still sends (AC 28), so only the muted part rejects.

def _hhmm_mins(hhmm: str) -> int:
    h, m = map(int, hhmm.split(":"))
    return h * 60 + m


def _mins_hhmm(mins: int) -> str:
    return f"{(mins // 60) % 24:02d}:{mins % 60:02d}"


def _in_quiet_window(t: int, quiet: dict) -> bool:
    start, end = _hhmm_mins(quiet["start"]), _hhmm_mins(quiet["end"])
    if start <= end:
        return start <= t < end
    return t >= start or t < end          # midnight-spanning


def _in_muted_quiet(t: int, quiet: dict) -> bool:
    """Inside quiet hours past the 30-min head — where nudges are muted."""
    return _in_quiet_window(t, quiet) and ((t - _hhmm_mins(quiet["start"])) % 1440) >= 30


def quiet_conflicts(med: dict, quiet: dict) -> list:
    """
    Edit-time conflicts for one med against a quiet window: a dose time
    inside quiet hours, or a T+late nudge inside the muted part (with a
    suggested fix). Interval/as-needed meds fire around the clock — their
    optional quiet_policy field governs them, not this check.
    """
    sched = med.get("schedule") or {}
    if sched.get("frequency") in ("interval", "as_needed"):
        return []
    late = (med.get("escalation") or {}).get("late_threshold_minutes")
    out = []
    for t in sched.get("times") or []:
        tm = _hhmm_mins(t)
        if _in_quiet_window(tm, quiet):
            out.append(
                f"{med.get('name')}: dose at {t} is inside quiet hours "
                f"({quiet['start']}–{quiet['end']}) — move the dose before "
                f"{quiet['start']} or adjust quiet hours")
        if late is None:
            continue
        nudge = (tm + late) % 1440
        if _in_muted_quiet(nudge, quiet):
            out.append(
                f"{med.get('name')}: the late nudge at {_mins_hhmm(nudge)} "
                f"(T+{late}m after {t}) would be muted by quiet hours — move "
                "the dose earlier, lower late_threshold_minutes, or start "
                f"quiet hours from {_mins_hhmm(nudge)}")
    return out


def _reject_quiet_conflicts(conflicts: list) -> None:
    if not conflicts:
        return
    for c in conflicts:
        print(f"Error: {c}.")
    raise SystemExit(EXIT_BAD_OPTION)


def _parse_med_json(json_text: str) -> dict:
    try:
        med = json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON for the med: {e}")
        raise SystemExit(EXIT_BAD_OPTION)
    if not isinstance(med, dict):
        print("Error: expected one JSON med object.")
        raise SystemExit(EXIT_BAD_OPTION)
    return med


def _validated_candidate(state: dict, meds: list) -> None:
    """Validate a candidate state (raises ValueError) with a friendly exit."""
    candidate = dict(state)
    candidate["meds"] = meds
    try:
        _safe_write_mod.validate(candidate)
    except ValueError as e:
        print(f"Error: the med didn't validate: {e}")
        raise SystemExit(EXIT_BAD_OPTION)


def _next_med_id(state: dict) -> str:
    nums = []
    for m in state["meds"]:
        try:
            nums.append(int(m["id"].split("-", 1)[1]))
        except (ValueError, IndexError, KeyError):
            continue
    return f"med-{(max(nums) + 1) if nums else 1:03d}"


# Keys whose change re-anchors tracking (issue §3: active_since is set on a
# schedule edit or a dose-time edit; renaming a med must not swallow pending
# nudges).
_SCHEDULE_KEYS = ("frequency", "times", "interval_hours", "day_of_week")


def _normalize_day_of_week(sched: dict) -> None:
    """
    Canonicalize an incoming schedule.day_of_week in place (PR 7): a list is
    deduped and sorted mon..sun — the stored canonical form — while a single
    string stays a string (compat reads). Unknown days, an empty list, or a
    non-string/non-list value get a friendly error here so the writer never
    reaches the validator with a half-useful message.
    """
    day = sched.get("day_of_week")
    if day is None or isinstance(day, str):
        return
    if not isinstance(day, list):
        print("Error: schedule.day_of_week must be a day like 'tue', a list like "
              "['tue','sat'], or null.")
        raise SystemExit(EXIT_BAD_OPTION)
    if not day:
        print("Error: schedule.day_of_week can't be an empty list — name at least "
              "one day (e.g. ['tue','sat']) or use null.")
        raise SystemExit(EXIT_BAD_OPTION)
    bad = [d for d in day if d not in _dispatch_mod.DAY_KEYS]
    if bad:
        print(f"Error: unknown day(s) {bad} in schedule.day_of_week — valid days: "
              f"{', '.join(_dispatch_mod.DAY_KEYS)}.")
        raise SystemExit(EXIT_BAD_OPTION)
    sched["day_of_week"] = sorted(set(day), key=_dispatch_mod.DAY_KEYS.index)


def _same_days(a, b) -> bool:
    """True when two day_of_week values mean the same schedule ('tue' == ['tue'])
    — swapping representations must not re-anchor tracking."""
    if isinstance(a, str):
        a = [a]
    if isinstance(b, str):
        b = [b]
    return set(a or []) == set(b or [])


def handle_add_med(json_text: str, dry_run: bool,
                   clock: Optional[Clock] = None) -> None:
    """
    Add a med from a JSON object (stdin): validate, refuse quiet-hours
    conflicts, set active_since_utc = now (nothing earlier is enumerated,
    so a new med starts with no phantom misses).
    """
    clock = clock or get_clock()
    now = clock.now_utc()
    med = _parse_med_json(json_text)
    if isinstance(med.get("schedule"), dict):
        _normalize_day_of_week(med["schedule"])
    state = load_state()

    med.setdefault("state", {"status": "pending", "last_taken": None,
                             "last_reminded": None, "next_due": None,
                             "missed_count": 0, "history": []})
    if med.get("id"):
        if any(m["id"] == med["id"] for m in state["meds"]):
            print(f"Error: a med with id {med['id']} already exists.")
            raise SystemExit(EXIT_BAD_OPTION)
    else:
        med["id"] = _next_med_id(state)

    _reject_quiet_conflicts(quiet_conflicts(med, state["global"]["quiet_hours"]))
    med["active_since_utc"] = now.isoformat()
    _validated_candidate(state, state["meds"] + [med])

    if dry_run:
        print(f"[DRY RUN] Would add {med.get('name')} ({med['id']}) — "
              "tracking starts from now.")
        return

    outcome = {}

    def fn(state_copy, history_view):
        if any(m["id"] == med["id"] for m in state_copy["meds"]):
            outcome["conflict"] = True
            return state_copy, []
        state_copy["meds"].append(copy.deepcopy(med))
        _safe_write_mod.validate(state_copy)
        return state_copy, []

    _safe_write_mod.transact(fn, clock=clock)

    if outcome.get("conflict"):
        print(f"Error: a med with id {med['id']} was just added — re-run with "
              "a different id.")
        raise SystemExit(EXIT_BAD_OPTION)
    print(f"Added {med['name']} ({med['id']}) — tracking starts now; earlier "
          "doses aren't counted.")
    log.info("ADD-MED [%s] %s", med["id"], med["name"])


def handle_edit_med(med_id: str, json_text: str, dry_run: bool,
                    clock: Optional[Clock] = None,
                    position: Optional[int] = None) -> None:
    """
    Edit a med from a JSON object (stdin). The existing runtime `state`
    block is preserved (the agent edits the prescription, never state),
    unknown optional fields pass through, and a schedule change re-anchors
    tracking via active_since_utc.
    """
    clock = clock or get_clock()
    state = load_state()
    tz = get_tz(state)
    now = clock.now_utc()
    med = _resolve_target(state, med_id, position, tz, now)
    incoming = _parse_med_json(json_text)
    if isinstance(incoming.get("schedule"), dict):
        _normalize_day_of_week(incoming["schedule"])

    if incoming.get("id") not in (None, med["id"]):
        print(f"Error: edit-med targets {med['id']} but the JSON describes "
              f"{incoming['id']}.")
        raise SystemExit(EXIT_BAD_OPTION)

    merged = dict(med)
    merged.update(incoming)
    merged["id"] = med["id"]
    merged["state"] = med["state"]        # runtime state is never agent-writable

    _reject_quiet_conflicts(quiet_conflicts(merged, state["global"]["quiet_hours"]))
    _validated_candidate(
        state, [merged if m["id"] == med["id"] else m for m in state["meds"]])

    def _sched_field_changed(key: str) -> bool:
        old, new = med["schedule"].get(key), merged["schedule"].get(key)
        # day_of_week compares semantically — 'tue' == ['tue'] (PR 7)
        if key == "day_of_week":
            return not _same_days(old, new)
        return old != new

    schedule_changed = any(_sched_field_changed(k) for k in _SCHEDULE_KEYS)

    if dry_run:
        print(f"[DRY RUN] Would update {merged.get('name')} ({med['id']}).")
        return

    def fn(state_copy, history_view):
        med_c = _find_med(state_copy, med["id"])
        if med_c is None:
            raise ValueError(f"med {med['id']} disappeared mid-edit")
        merged_c = copy.deepcopy(merged)
        if schedule_changed:
            merged_c["active_since_utc"] = now.isoformat()
        med_c.clear()                    # keep the object identity in meds[]
        med_c.update(merged_c)
        _safe_write_mod.validate(state_copy)
        return state_copy, []

    _safe_write_mod.transact(fn, clock=clock)
    note = " Schedule changed — tracking restarts from now." if schedule_changed else ""
    print(f"Updated {merged['name']} ({med['id']}).{note}")
    log.info("EDIT-MED [%s] %s", med["id"], merged["name"])


def handle_set_quiet_hours(start: str, end: str, dry_run: bool,
                           clock: Optional[Clock] = None) -> None:
    """Change quiet hours after checking every med against the new window."""
    clock = clock or get_clock()
    for label, value in (("start", start), ("end", end)):
        if not _HHMM_RE.match(value or ""):
            print(f"Error: quiet-hours {label} must be HH:MM (got '{value}').")
            raise SystemExit(EXIT_BAD_OPTION)

    state = load_state()
    new_quiet = {"start": start, "end": end}
    _reject_quiet_conflicts(
        [c for m in state["meds"] for c in quiet_conflicts(m, new_quiet)])

    if dry_run:
        print(f"[DRY RUN] Would set quiet hours to {start}–{end}.")
        return

    def fn(state_copy, history_view):
        state_copy["global"]["quiet_hours"] = {"start": start, "end": end}
        return state_copy, []

    _safe_write_mod.transact(fn, clock=clock)
    print(f"Quiet hours set to {start}–{end}.")
    log.info("SET-QUIET-HOURS %s-%s", start, end)


# ── Init (first run, #10) ──────────────────────────────────────────────────────

def handle_init(timezone_name: str, quiet_start: str, quiet_end: str,
                digest_time: Optional[str], channel: str, dry_run: bool) -> None:
    """
    Create meds-state.json from the interview's global answers — no meds,
    no runtime state (meds go in through add-med). Refuses when the file
    already exists, so it can never clobber a live setup. The digest
    defaults to wake time + 30 min, pulled back to 5 min before quiet
    hours when that would land inside them.
    """
    if _safe_write_mod.STATE_FILE.exists():
        print(f"Error: {_safe_write_mod.STATE_FILE} already exists — use "
              "set-quiet-hours / add-med / edit-med to change it.")
        raise SystemExit(EXIT_BAD_OPTION)
    try:
        ZoneInfo(timezone_name)
    except (ValueError, KeyError, OSError):
        print(f"Error: unknown timezone '{timezone_name}' — use an IANA name "
              "like America/Los_Angeles.")
        raise SystemExit(EXIT_BAD_OPTION)
    for label, value in (("--quiet-start", quiet_start), ("--quiet-end", quiet_end),
                         ("--digest-time", digest_time)):
        if value is not None and not _HHMM_RE.match(value):
            print(f"Error: {label} must be HH:MM (got '{value}').")
            raise SystemExit(EXIT_BAD_OPTION)
    if not channel.strip():
        print("Error: --channel must not be empty.")
        raise SystemExit(EXIT_BAD_OPTION)

    quiet = {"start": quiet_start, "end": quiet_end}
    if digest_time is None:
        digest = (_hhmm_mins(quiet_end) + 30) % 1440
        if _in_quiet_window(digest, quiet):
            digest = (_hhmm_mins(quiet_start) - 5) % 1440
        digest_time = _mins_hhmm(digest)

    state = {
        "version": "1",
        "global": {
            "timezone": timezone_name,
            "quiet_hours": quiet,
            "paused": False,
            "digest_time": digest_time,
            "delivery_channel": channel.strip(),
        },
        "meds": [],
    }
    if dry_run:
        print(f"[DRY RUN] Would create {_safe_write_mod.STATE_FILE}: "
              f"{timezone_name}, quiet hours {quiet_start}–{quiet_end}, "
              f"digest {digest_time}, channel {channel.strip()}.")
        return
    # 'absent': the write is refused if the file appeared in the meantime
    _safe_write_mod.safe_write(state, expected_sha256="absent")
    print(f"Created {_safe_write_mod.STATE_FILE}: {timezone_name}, quiet hours "
          f"{quiet_start}–{quiet_end}, digest {digest_time}. Add meds with add-med.")
    log.info("INIT %s", _safe_write_mod.STATE_FILE)


# ── Remove / status / show-state (issue #1 §6) ─────────────────────────────────

def handle_remove(med_id: str, yes: bool, dry_run: bool,
                  clock: Optional[Clock] = None,
                  position: Optional[int] = None) -> None:
    """Remove a med from state. History lines remain in history.jsonl."""
    clock = clock or get_clock()
    state = load_state()
    tz = get_tz(state)
    now = clock.now_utc()
    med = _resolve_target(state, med_id, position, tz, now)

    if not yes:
        print(f"Refusing to remove {med['name']} — rerun with --yes to confirm.")
        raise SystemExit(EXIT_BAD_OPTION)

    if dry_run:
        print(f"[DRY RUN] Would remove {med['name']} ({med['id']}).")
        return

    def fn(state_copy, history_view):
        state_copy["meds"] = [m for m in state_copy["meds"] if m["id"] != med["id"]]
        return state_copy, []

    _safe_write_mod.transact(fn, clock=clock)
    print(f"Removed {med['name']} ({med['id']}). Its history lines remain in "
          "history.jsonl.")
    log.info("REMOVE [%s] %s", med["id"], med["name"])


def _last_dose_event(history, med_id: str) -> Optional[dict]:
    best, best_ts = None, None
    for e in history:
        if e.get("med_id") != med_id or e.get("event") not in ("taken", "skipped", "missed"):
            continue
        ts = parse_instant(e["ts_utc"])
        if best_ts is None or ts > best_ts:
            best, best_ts = e, ts
    return best


def handle_status() -> None:
    """Read-only summary for the agent to relay (issue #1 §6)."""
    state = load_state()
    tz = get_tz(state)
    g = state["global"]
    quiet = g["quiet_hours"]
    print(f"{len(state['meds'])} med(s) | timezone {g['timezone']} | quiet hours "
          f"{quiet['start']}–{quiet['end']} | digest {g['digest_time']}")
    if g.get("paused"):
        print("ALL REMINDERS PAUSED (global).")
    history = _event_store_mod.load_events(_safe_write_mod.history_file())
    for i, med in enumerate(state["meds"], 1):
        sched = med["schedule"]
        freq = sched["frequency"]
        if freq == "interval":
            when = f"every {sched['interval_hours']}h"
        elif freq == "as_needed":
            when = "as needed"
        else:
            day = (f"{_dispatch_mod.fmt_days(sched.get('day_of_week'))} "
                   if freq == "weekly" and sched.get("day_of_week") else "")
            when = day + ", ".join(_dispatch_mod.fmt_12h(t) for t in sched["times"])
        line = f"{i}. {med['name']} {med['dose']}{med['unit']} — {when}"
        if med.get("paused"):
            line += " [paused]"
        last = _last_dose_event(history, med["id"])
        if last is not None:
            at = parse_instant(last["ts_utc"]).astimezone(tz)
            line += f" | last: {last['event']} {_fmt_12h(at)}"
        nd = med["state"].get("next_due")
        if nd:
            nd_local = parse_instant(nd).astimezone(tz)
            line += f" | next due: {nd_local:%a} {_fmt_12h(nd_local)}"
        stock = _inv.status_line(med, history, get_clock().now_utc())
        if stock:
            line += f" | {stock}"
        print(line)
    if not state["meds"]:
        print("No meds yet — add one with: reply.py add-med --json -")


def handle_show_state() -> None:
    """Print the state file's sha256 — the token CLI writers must pass."""
    load_state()
    print(_safe_write_mod.state_token()[1])


# ── CLI ────────────────────────────────────────────────────────────────────────

def _read_json_input(src: str) -> str:
    """'-' (or None) reads stdin; anything else is a path."""
    if src in (None, "-"):
        return sys.stdin.read()
    return Path(src).read_text(encoding="utf-8")


def main() -> None:
    _safe_write_mod.apply_process_umask()   # issue #1 §2: private files, before any are created
    parser = argparse.ArgumentParser(
        description="AI reply handler — dose confirmations and schedule replies.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Print without writing state")
    parser.add_argument("--state", default=None, metavar="PATH",
                        help="Path to meds-state.json (overrides MEDS_STATE_FILE)")

    sub = parser.add_subparsers(dest="mode", required=True, metavar="MODE")

    p_confirm = sub.add_parser("confirm", help="Mark a med as taken")
    p_confirm_grp = p_confirm.add_mutually_exclusive_group(required=True)
    p_confirm_grp.add_argument("med_id", nargs="?", default=None,
                               help="Med ID, e.g. med-001")
    p_confirm_grp.add_argument("--all", dest="confirm_all", action="store_true",
                               help="Confirm all pending/reminded/late meds")
    p_confirm_grp.add_argument("--position", type=int, default=None, metavar="N",
                               help="Pick the Nth med from today's digest order (1-based)")
    p_confirm.add_argument("--dose-taken", default="",
                           help="Actual dose if different from prescribed, e.g. '250mg'")
    p_confirm.add_argument("--dose", default=None, metavar="HH:MM",
                           help="Pin the scheduled dose being confirmed (must match a times[] entry)")
    p_confirm.add_argument("--taken-at", default=None, metavar="HH:MM", dest="taken_at",
                           help="Wall time the dose was taken (most recent past instance, <=24h back)")
    p_confirm.add_argument("--force", default=None, metavar="NONCE",
                           help="Override a duplicate refusal (nonce from the exit-3 message, valid 10 min)")

    p_skip = sub.add_parser("skip", help="Skip a dose (never logged missed)")
    p_skip.add_argument("med_id", nargs="?", default=None,
                        help="Med ID, e.g. med-001 (or use --position)")
    p_skip.add_argument("--position", type=int, default=None, metavar="N",
                        help="Pick the Nth med from today's digest order (1-based)")
    p_skip.add_argument("--dose", default=None, metavar="HH:MM",
                        help="Pin the dose being skipped (required for a future dose)")

    p_snooze = sub.add_parser("snooze", help="Push the pending dose's reminder later")
    p_snooze.add_argument("med_id", nargs="?", default=None,
                          help="Med ID, e.g. med-001 (or use --position)")
    p_snooze.add_argument("--position", type=int, default=None, metavar="N",
                          help="Pick the Nth med from today's digest order (1-based)")
    p_snooze.add_argument("--minutes", type=int, default=None, metavar="N",
                          help=f"Snooze duration (default {SNOOZE_DEFAULT}, "
                               f"range {SNOOZE_MIN}-{SNOOZE_MAX}, capped at half "
                               "the gap to the next dose)")

    p_defer = sub.add_parser(
        "defer", help="Deprecated alias for snooze (min(120, cap) minutes)")
    p_defer.add_argument("med_id", nargs="?", default=None,
                         help="Med ID, e.g. med-001 (or use --position)")
    p_defer.add_argument("--position", type=int, default=None, metavar="N",
                         help="Pick the Nth med from today's digest order (1-based)")

    p_undo = sub.add_parser("undo", help="Undo the most recent taken/skipped (24h)")
    p_undo.add_argument("med_id", nargs="?", default=None,
                        help="Med ID, e.g. med-001 (or use --position)")
    p_undo.add_argument("--position", type=int, default=None, metavar="N",
                        help="Pick the Nth med from today's digest order (1-based)")

    for name, help_text in (("pause", "Stop reminders for one med"),
                            ("unpause", "Resume reminders for one med")):
        p = sub.add_parser(name, help=help_text)
        p.add_argument("med_id", nargs="?", default=None,
                       help="Med ID, e.g. med-001 (or use --position)")
        p.add_argument("--position", type=int, default=None, metavar="N",
                       help="Pick the Nth med from today's digest order (1-based)")

    p_recon = sub.add_parser("reconstitute",
                             help="Log a vial mix (reminders then show syringe units)")
    p_recon.add_argument("med_id", nargs="?", default=None,
                         help="Med ID, e.g. med-001 (or use --position)")
    p_recon.add_argument("--position", type=int, default=None, metavar="N",
                         help="Pick the Nth med from today's digest order (1-based)")
    p_recon.add_argument("--vial-mg", type=float, required=True, metavar="MG",
                         help="Peptide in the vial, mg")
    p_recon.add_argument("--diluent-ml", type=float, required=True, metavar="ML",
                         help="Bacteriostatic water added, mL")

    p_restock = sub.add_parser("restock",
                               help="Add inventory (--qty) or record a recount (--set)")
    p_restock.add_argument("med_id", nargs="?", default=None,
                           help="Med ID, e.g. med-001 (or use --position)")
    p_restock.add_argument("--position", type=int, default=None, metavar="N",
                           help="Pick the Nth med from today's digest order (1-based)")
    p_restock.add_argument("--qty", type=float, default=None, metavar="N",
                           help="Inventory units added (in the med's inventory_unit)")
    p_restock.add_argument("--set", dest="set_qty", type=float, default=None, metavar="N",
                           help="Inventory units on hand right now (a recount)")

    p_add = sub.add_parser("add-med", help="Add a med from a JSON object on stdin")
    p_add.add_argument("--json", action="store_true",
                       help="Read the med's JSON from stdin ('-' or a path)")
    p_add.add_argument("json_src", nargs="?", default="-", metavar="-|PATH",
                       help="'-' (stdin, default) or a path to the JSON file")

    p_edit = sub.add_parser("edit-med", help="Edit a med from a JSON object on stdin")
    p_edit.add_argument("med_id", nargs="?", default=None,
                        help="Med ID, e.g. med-001 (or use --position)")
    p_edit.add_argument("--position", type=int, default=None, metavar="N",
                        help="Pick the Nth med from today's digest order (1-based)")
    p_edit.add_argument("--json", action="store_true",
                        help="Read the med's JSON from stdin ('-' or a path)")
    p_edit.add_argument("json_src", nargs="?", default="-", metavar="-|PATH",
                        help="'-' (stdin, default) or a path to the JSON file")

    p_init = sub.add_parser("init", help="Create meds-state.json (first run only)")
    p_init.add_argument("--timezone", required=True, metavar="TZ",
                        help="IANA timezone, e.g. America/Los_Angeles")
    p_init.add_argument("--quiet-start", required=True, metavar="HH:MM",
                        help="Quiet hours start (bedtime)")
    p_init.add_argument("--quiet-end", required=True, metavar="HH:MM",
                        help="Quiet hours end (wake time)")
    p_init.add_argument("--digest-time", default=None, metavar="HH:MM",
                        help="Daily digest time (default: quiet end + 30 min)")
    p_init.add_argument("--channel", required=True, metavar="NAME",
                        help="Delivery channel, e.g. telegram")

    p_quiet = sub.add_parser("set-quiet-hours", help="Set the quiet-hours window")
    p_quiet.add_argument("start", metavar="HH:MM", help="Quiet hours start")
    p_quiet.add_argument("end", metavar="HH:MM", help="Quiet hours end")

    p_remove = sub.add_parser("remove", help="Remove a med (history lines remain)")
    p_remove.add_argument("med_id", nargs="?", default=None,
                          help="Med ID, e.g. med-001 (or use --position)")
    p_remove.add_argument("--position", type=int, default=None, metavar="N",
                          help="Pick the Nth med from today's digest order (1-based)")
    p_remove.add_argument("--yes", action="store_true",
                          help="Confirm the removal")

    sub.add_parser("status", help="Read-only summary of all meds")
    sub.add_parser("show-state", help="Print the state sha256 for CLI writers")

    args = parser.parse_args()
    setup_logging(args.dry_run)

    if args.state:
        _dispatch_mod.STATE_FILE = Path(args.state)
        _safe_write_mod.STATE_FILE = Path(args.state)  # writer keeps its own copy
    _safe_write_mod.secure_private_files(
        extra=(Path(os.environ.get("MEDS_LOG_FILE", SCRIPT_DIR / "reply.log")),))

    if args.mode == "confirm":
        if args.confirm_all:
            handle_confirm_all(args.dose_taken or None, args.dry_run)
        else:
            if not args.med_id and args.position is None:
                parser.error("confirm requires a med_id, --all or --position")
            handle_confirm(args.med_id, args.dose_taken or None, args.dry_run,
                           dose_pin=args.dose, taken_at_raw=args.taken_at,
                           force=args.force, position=args.position)
    elif args.mode == "skip":
        if not args.med_id and args.position is None:
            parser.error("skip requires a med_id or --position")
        handle_skip(args.med_id, args.dose, args.dry_run, position=args.position)
    elif args.mode == "snooze":
        if not args.med_id and args.position is None:
            parser.error("snooze requires a med_id or --position")
        handle_snooze(args.med_id, args.minutes, args.dry_run,
                      position=args.position)
    elif args.mode == "defer":
        if not args.med_id and args.position is None:
            parser.error("defer requires a med_id or --position")
        handle_defer(args.med_id, args.dry_run, position=args.position)
    elif args.mode == "undo":
        if not args.med_id and args.position is None:
            parser.error("undo requires a med_id or --position")
        handle_undo(args.med_id, args.dry_run, position=args.position)
    elif args.mode == "pause":
        if not args.med_id and args.position is None:
            parser.error("pause requires a med_id or --position")
        handle_pause(args.med_id, args.dry_run, position=args.position)
    elif args.mode == "unpause":
        if not args.med_id and args.position is None:
            parser.error("unpause requires a med_id or --position")
        handle_unpause(args.med_id, args.dry_run, position=args.position)
    elif args.mode == "reconstitute":
        if not args.med_id and args.position is None:
            parser.error("reconstitute requires a med_id or --position")
        handle_reconstitute(args.med_id, args.vial_mg, args.diluent_ml,
                            args.dry_run, position=args.position)
    elif args.mode == "restock":
        if not args.med_id and args.position is None:
            parser.error("restock requires a med_id or --position")
        handle_restock(args.med_id, args.qty, args.set_qty, args.dry_run,
                       position=args.position)
    elif args.mode == "add-med":
        handle_add_med(_read_json_input(args.json_src), args.dry_run)
    elif args.mode == "edit-med":
        if not args.med_id and args.position is None:
            parser.error("edit-med requires a med_id or --position")
        handle_edit_med(args.med_id, _read_json_input(args.json_src), args.dry_run,
                        position=args.position)
    elif args.mode == "init":
        handle_init(args.timezone, args.quiet_start, args.quiet_end,
                    args.digest_time, args.channel, args.dry_run)
    elif args.mode == "set-quiet-hours":
        handle_set_quiet_hours(args.start, args.end, args.dry_run)
    elif args.mode == "remove":
        if not args.med_id and args.position is None:
            parser.error("remove requires a med_id or --position")
        handle_remove(args.med_id, args.yes, args.dry_run, position=args.position)
    elif args.mode == "status":
        handle_status()
    elif args.mode == "show-state":
        handle_show_state()


if __name__ == "__main__":
    main()
