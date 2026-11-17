#!/usr/bin/env python3
"""
safe_write.py — atomic state writes, OS file locks, and pure transactions.

Pure-Python replacement for safe-write.sh. No bash / Git Bash required.
Uses os.replace() for atomic rename (works on NTFS since Python 3.3).

Usage (CLI — reads new state from stdin):
    python3 safe_write.py --expected-sha256 <sha> < new-state.json

    The sha256 is the version token of the file as the caller last read it
    ('absent' when creating a new file). A stale token aborts the write, so
    two writers outside the lock can't clobber each other (issue #1 §2).

Usage (imported):
    from safe_write import safe_write, transact
    safe_write(new_state_dict)                    # whole-file write (dispatch)
    safe_write(new_state, expected_sha256=sha)    # token-checked write
    transact(fn, clock)                           # lock → load → pure fn →
                                                  # validate → append events →
                                                  # atomic write → unlock

Environment overrides:
    MEDS_STATE_FILE    path to meds-state.json   (default: same dir as this file)
    MEDS_LOG_FILE      path to write log         (default: same dir as this file)
    MEDS_HISTORY_FILE  path to history.jsonl     (default: next to the state file)
"""

import argparse
import contextlib
import copy
import hashlib
import json
import logging
import os
import re
import shutil
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Union

import event_store
from clock import get_clock

# CLI output includes unicode (em-dashes) that cp1252 consoles can't encode
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR     = Path(__file__).parent.resolve()
STATE_FILE     = Path(os.environ.get("MEDS_STATE_FILE",  SCRIPT_DIR / "meds-state.json"))
LOG_FILE       = Path(os.environ.get("MEDS_LOG_FILE",    SCRIPT_DIR / "safe-write.log"))

LOCK_WAIT    = 30   # seconds to wait for the state lock before giving up
REPLACE_TRIES = 5   # Windows os.replace PermissionError retries
REPLACE_DELAY = 0.2  # seconds between retries

log = logging.getLogger("safe_write")

# ── Derived paths ──────────────────────────────────────────────────────────────
# Computed from STATE_FILE at call time so --state overrides (which rebind
# safe_write.STATE_FILE after import) propagate to every artifact.

def lock_file() -> Path:
    return Path(str(STATE_FILE) + ".lock")

def backup_file() -> Path:
    return Path(str(STATE_FILE) + ".bak")

def backup_old_file() -> Path:
    return Path(str(STATE_FILE) + ".bak.old")   # previous .bak generation

def tmp_file() -> Path:
    return Path(str(STATE_FILE) + ".tmp")

def history_file() -> Path:
    env = os.environ.get("MEDS_HISTORY_FILE")
    return Path(env) if env else STATE_FILE.parent / "history.jsonl"


# ── Logging ────────────────────────────────────────────────────────────────────

def utc_formatter(tag: str) -> logging.Formatter:
    """
    Per-handler formatter whose converter is gmtime, so the trailing Z is
    true UTC (issue #1 §7). The class-wide logging.Formatter.converter is
    never touched — other libraries' handlers keep their own convention.
    """
    fmt = logging.Formatter(
        f"%(asctime)s [{tag}] %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )
    fmt.converter = time.gmtime
    return fmt


def _redaction_source() -> dict:
    """Best-effort state read for logging config — redaction must never crash a run."""
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def redaction_enabled() -> bool:
    """MEDS_LOG_REDACT=1 or global.log_redact (issue #1 §7)."""
    if os.environ.get("MEDS_LOG_REDACT") == "1":
        return True
    return bool(_redaction_source().get("global", {}).get("log_redact"))


def _name_map() -> dict:
    """med name → med id, for redacting names out of logs."""
    out = {}
    for med in _redaction_source().get("meds", []):
        if isinstance(med, dict) and med.get("name") and med.get("id"):
            out[med["name"]] = med["id"]
    return out


class RedactFilter(logging.Filter):
    """
    Rewrite rendered records with med ids in place of med names (issue #1 §7).
    Attached per handler, so sender stderr reaching a log.warning is redacted
    the same as any other message.
    """

    def __init__(self):
        super().__init__()
        self._names = _name_map()

    def filter(self, record: logging.LogRecord) -> bool:
        if self._names:
            msg = record.getMessage()
            if any(n in msg for n in self._names):
                for name, mid in self._names.items():
                    msg = msg.replace(name, mid)
                record.msg = msg
                record.args = None
        return True


def configure_root_logging(tag: str, log_path: Path, level: int,
                           stream=None) -> None:
    """
    Root logging with true-UTC formatters on every handler and optional
    redaction. Shared by dispatch.py, reply.py and this module's CLI, so
    their Z timestamps all mean UTC (issue #1 §7).
    """
    redact = redaction_enabled()
    handlers = [
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler(stream if stream is not None else sys.stdout),
    ]
    for h in handlers:
        h.setFormatter(utc_formatter(tag))
        if redact:
            h.addFilter(RedactFilter())
    logging.basicConfig(level=level, handlers=handlers)


def _setup_logging() -> None:
    if log.handlers:
        return
    configure_root_logging("safe_write", LOG_FILE, logging.INFO)

# ── Validation (mirrors safe-write.sh inline Python) ──────────────────────────

_HHMM = re.compile(r"^([01][0-9]|2[0-3]):[0-5][0-9]$")
_ISO  = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$")
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

_VALID_TYPES    = {"pill","liquid","injection","patch","inhaler","other"}
_VALID_FREQS    = {"once_daily","twice_daily","interval","weekly","as_needed"}
# `deferred` stays readable forever; new code never writes it (issue #1 §1)
_VALID_STATUSES = {"pending","reminded","confirmed","late","missed","deferred"}
_VALID_EVENTS   = {"taken","missed","late_nudge_sent","deferred"}
# Canonical day order for list-valued day_of_week (PR 7): sorted mon..sun
_DAY_ORDER      = ("mon","tue","wed","thu","fri","sat","sun")
_VALID_DAYS     = set(_DAY_ORDER)
_VALID_SYRINGES = {"U-100","U-50"}
_MED_ID         = re.compile(r"^med-[0-9]{3,}$")


def _die(msg: str) -> None:
    raise ValueError(msg)


def validate(state: dict) -> None:
    """Raise ValueError with a human-readable message if state is invalid."""
    if not isinstance(state, dict):
        _die("State must be a JSON object")

    for field in ("version", "global", "meds"):
        if field not in state:
            _die(f"Missing top-level field: '{field}'")

    if state["version"] != "1":
        _die(f"Unknown schema version '{state['version']}' (expected '1')")

    if not isinstance(state["meds"], list):
        _die("'meds' must be an array")

    g = state["global"]
    for field in ("timezone", "quiet_hours", "paused", "digest_time", "delivery_channel"):
        if field not in g:
            _die(f"global.{field} is required")

    if not isinstance(g["paused"], bool):
        _die("global.paused must be a boolean")

    if not isinstance(g["delivery_channel"], str) or not g["delivery_channel"].strip():
        _die("global.delivery_channel must be a non-empty string (e.g. 'whatsapp', 'telegram', 'sms')")

    for field in ("start", "end"):
        if field not in g["quiet_hours"]:
            _die(f"global.quiet_hours.{field} is required")
        if not _HHMM.match(g["quiet_hours"][field] or ""):
            _die(f"global.quiet_hours.{field} must be HH:MM (24h, zero-padded)")

    if not _HHMM.match(g["digest_time"] or ""):
        _die(f"global.digest_time must be HH:MM (24h, zero-padded)")

    # Optional privacy switch (issue #1 §7): logs use med ids only
    if not isinstance(g.get("log_redact", False), bool):
        _die("global.log_redact must be a boolean (optional)")

    # Optional tick-engine bookkeeping (issue #1): watermark set by the migration
    tick = state.get("tick")
    if tick is not None:
        wm = tick.get("watermark_utc")
        if wm is not None and not _ISO.match(str(wm)):
            _die("tick.watermark_utc must be ISO 8601 with timezone or null")

    seen_ids: set = set()
    for i, med in enumerate(state["meds"]):
        p = f"meds[{i}]"

        for field in ("id","name","type","dose","unit","paused","schedule","escalation","state"):
            if field not in med:
                _die(f"{p}.{field} is required")

        mid = med["id"]
        if not _MED_ID.match(mid or ""):
            _die(f"{p}.id '{mid}' must match pattern med-NNN")
        if mid in seen_ids:
            _die(f"{p}: duplicate id '{mid}'")
        seen_ids.add(mid)

        if med["type"] not in _VALID_TYPES:
            _die(f"{p}.type must be one of {sorted(_VALID_TYPES)}")

        if not isinstance(med["dose"], str) or not med["dose"].strip():
            _die(f"{p}.dose must be a non-empty string")

        if not isinstance(med["unit"], str) or not med["unit"].strip():
            _die(f"{p}.unit must be a non-empty string")

        if not isinstance(med["paused"], bool):
            _die(f"{p}.paused must be a boolean")

        # Optional syringe for the reconstitution calculator (PR 8a, #10)
        if med.get("syringe") is not None and med["syringe"] not in _VALID_SYRINGES:
            _die(f"{p}.syringe must be one of {sorted(_VALID_SYRINGES)} or absent")

        # Optional inventory tracking (PR 8b, #10)
        inv_unit = med.get("inventory_unit")
        if inv_unit is not None and (not isinstance(inv_unit, str) or not inv_unit.strip()):
            _die(f"{p}.inventory_unit must be a non-empty string (e.g. 'vial') or absent")
        dpu = med.get("doses_per_unit")
        if dpu is not None and (isinstance(dpu, bool) or not isinstance(dpu, (int, float))
                                or not dpu > 0):
            _die(f"{p}.doses_per_unit must be a positive number or absent")
        reorder = med.get("reorder_when_below_days")
        if reorder is not None and (isinstance(reorder, bool) or not isinstance(reorder, int)
                                    or reorder < 1):
            _die(f"{p}.reorder_when_below_days must be a positive integer or absent")

        # Optional calendar bounds (PR 6): local dates in global.timezone;
        # end_date is inclusive. Null/absent = unbounded on that side.
        bounds = {}
        for field in ("start_date", "end_date"):
            val = med.get(field)
            if val is None:
                continue
            if not isinstance(val, str) or not _DATE.match(val):
                _die(f"{p}.{field} must be a YYYY-MM-DD date or null (got '{val}')")
            try:
                bounds[field] = date.fromisoformat(val)
            except ValueError:
                _die(f"{p}.{field} '{val}' is not a real calendar date")
        if "start_date" in bounds and "end_date" in bounds \
                and bounds["end_date"] < bounds["start_date"]:
            _die(f"{p}: end_date ({med['end_date']}) must be on or after "
                 f"start_date ({med['start_date']})")

        sched = med["schedule"]
        if "frequency" not in sched:
            _die(f"{p}.schedule.frequency is required")
        freq = sched["frequency"]
        if freq not in _VALID_FREQS:
            _die(f"{p}.schedule.frequency must be one of {sorted(_VALID_FREQS)}")

        if freq == "interval":
            ih = sched.get("interval_hours")
            if ih is None or not isinstance(ih, int) or ih < 1 or ih > 168:
                _die(f"{p}.schedule.interval_hours must be integer 1-168 when frequency is 'interval'")
        elif freq != "as_needed":
            times = sched.get("times")
            if not times or not isinstance(times, list) or len(times) == 0:
                _die(f"{p}.schedule.times required when frequency is '{freq}'")
            for t in times:
                if not _HHMM.match(str(t)):
                    _die(f"{p}.schedule.times contains invalid time '{t}' (expected HH:MM)")

        # Day-of-week for weekly meds (absent in older state files): a single
        # day string (legacy) or a canonical list — sorted mon..sun, deduped (PR 7)
        day = sched.get("day_of_week")
        if day is None:
            if freq == "weekly":
                _die(f"{p}.schedule.day_of_week is required for weekly meds "
                     "(e.g. 'mon' or ['mon','fri']) — without it reminders fire daily")
        elif isinstance(day, str):
            if day not in _VALID_DAYS:
                _die(f"{p}.schedule.day_of_week must be one of {sorted(_VALID_DAYS)} "
                     "(or a list of them, or null)")
        elif isinstance(day, list):
            if not day:
                _die(f"{p}.schedule.day_of_week can't be an empty list — name at "
                     "least one day (e.g. ['tue','sat']) or use null")
            bad = [d for d in day if d not in _VALID_DAYS]
            if bad:
                _die(f"{p}.schedule.day_of_week has unknown day(s) {bad} — valid "
                     f"days are {_DAY_ORDER}")
            if len(set(day)) != len(day):
                _die(f"{p}.schedule.day_of_week has duplicate day(s) {day} — list "
                     "each day once (they are deduped on save)")
            if [d for d in _DAY_ORDER if d in set(day)] != day:
                _die(f"{p}.schedule.day_of_week must be sorted mon..sun and deduped "
                     f"(got {day}, e.g. ['mon','fri'])")
        else:
            _die(f"{p}.schedule.day_of_week must be a day string, a list of days, "
                 "or null")

        esc = med["escalation"]
        for field in ("late_threshold_minutes","missed_threshold_minutes","late_message","missed_message"):
            if field not in esc:
                _die(f"{p}.escalation.{field} is required")

        if not isinstance(esc["late_threshold_minutes"], int) or esc["late_threshold_minutes"] < 1:
            _die(f"{p}.escalation.late_threshold_minutes must be a positive integer")
        if not isinstance(esc["missed_threshold_minutes"], int) or esc["missed_threshold_minutes"] < 1:
            _die(f"{p}.escalation.missed_threshold_minutes must be a positive integer")
        # No late < missed ordering check since #11: late_threshold_minutes is
        # the nudge cadence and missed_threshold_minutes is retired (still
        # required so pre-#11 readers load the file, but never read).

        mstate = med["state"]
        for field in ("status","last_taken","last_reminded","next_due","missed_count","history"):
            if field not in mstate:
                _die(f"{p}.state.{field} is required")

        if mstate["status"] not in _VALID_STATUSES:
            _die(f"{p}.state.status must be one of {sorted(_VALID_STATUSES)}")

        if not isinstance(mstate["missed_count"], int) or mstate["missed_count"] < 0:
            _die(f"{p}.state.missed_count must be a non-negative integer")

        if not isinstance(mstate["history"], list):
            _die(f"{p}.state.history must be an array")

        for field in ("last_taken", "last_reminded", "next_due"):
            val = mstate[field]
            if val is not None and not _ISO.match(str(val)):
                _die(f"{p}.state.{field} must be ISO 8601 with timezone or null")

        # Optional per-dose confirmation anchor (absent in older state files)
        cd = mstate.get("confirmed_dose")
        if cd is not None and not _ISO.match(str(cd)):
            _die(f"{p}.state.confirmed_dose must be ISO 8601 with timezone or null")

        for j, entry in enumerate(mstate["history"]):
            ep = f"{p}.state.history[{j}]"
            for field in ("timestamp", "event", "dose_prescribed"):
                if field not in entry:
                    _die(f"{ep}.{field} is required")
            if entry["event"] not in _VALID_EVENTS:
                _die(f"{ep}.event must be one of {sorted(_VALID_EVENTS)}")
            if not _ISO.match(str(entry["timestamp"])):
                _die(f"{ep}.timestamp must be ISO 8601 with timezone")


# ── OS file lock (issue #1 §2) ─────────────────────────────────────────────────
#
# fcntl.flock (POSIX) / msvcrt.locking (Windows) on <state>.lock. Both are
# stdlib, released when the process dies, and need no stale timeout.

if sys.platform == "win32":
    import msvcrt

    def _try_lock(fh) -> bool:
        try:
            fh.seek(0)
            msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)
            return True
        except OSError:
            return False

    def _unlock(fh) -> None:
        try:
            fh.seek(0)
            msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 1)
        except OSError:
            pass
else:
    import fcntl

    def _try_lock(fh) -> bool:
        try:
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except OSError:
            return False

    def _unlock(fh) -> None:
        try:
            fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
        except OSError:
            pass


@contextlib.contextmanager
def file_lock(timeout: float = None, poll: float = 0.05, _path=None):
    """
    Exclusive lock on the state's lock file. Raises RuntimeError when still
    held after `timeout` seconds (default LOCK_WAIT). A leftover lock
    *directory* (the pre-PR1 mkdir lock) can only be stale — that
    implementation removed it on release — so it is cleared on sight.
    """
    if timeout is None:
        timeout = LOCK_WAIT
    path = Path(_path) if _path else lock_file()
    if path.is_dir():
        try:
            path.rmdir()
        except OSError:
            pass
    fh = open(path, "a+b")
    try:
        if os.fstat(fh.fileno()).st_size == 0:
            fh.write(b"\0")   # a byte for Windows to lock
            fh.flush()
        deadline = time.monotonic() + timeout
        while not _try_lock(fh):
            if time.monotonic() >= deadline:
                raise RuntimeError(
                    f"Could not acquire lock after {timeout}s — another process may be writing"
                )
            time.sleep(poll)
        try:
            yield fh
        finally:
            _unlock(fh)
    finally:
        fh.close()


# ── Version token ──────────────────────────────────────────────────────────────

def state_token(path=None) -> tuple:
    """
    (st_mtime_ns, sha256) of the state file — identifies the exact version a
    writer last read ('absent' sha when the file doesn't exist yet). Guards
    writers outside the lock (issue #1 §2).
    """
    p = Path(path) if path else STATE_FILE
    try:
        mtime_ns = p.stat().st_mtime_ns
    except FileNotFoundError:
        return (0, "absent")
    with p.open("rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    return (mtime_ns, digest)


def load_state() -> tuple:
    """
    (state, token) from STATE_FILE. Raises FileNotFoundError when missing —
    dispatch.load_state owns the friendly CLI error.
    """
    data = STATE_FILE.read_bytes()
    state = json.loads(data.decode("utf-8"))
    return state, (STATE_FILE.stat().st_mtime_ns, hashlib.sha256(data).hexdigest())


# ── File security (issue #1 §2) ────────────────────────────────────────────────

def apply_process_umask() -> None:
    """Private-by-default file creation (POSIX)."""
    os.umask(0o077)


def _secure(path: Path) -> None:
    if sys.platform == "win32":
        return  # documented no-op: Windows chmod only toggles the read-only bit
    try:
        if path.exists() and (path.stat().st_mode & 0o777) != 0o600:
            path.chmod(0o600)
    except OSError:
        pass


def secure_private_files(extra=()) -> None:
    """chmod 600 existing state, backups, history and log (first run; POSIX)."""
    paths = [STATE_FILE, backup_file(), backup_old_file(), history_file(), LOG_FILE]
    paths.extend(extra)
    for p in paths:
        _secure(p)


# ── Core write ─────────────────────────────────────────────────────────────────

def _atomic_write_state(state: dict) -> None:
    """tmp (0600, fsync) → backup rotation → os.replace, with Windows retries."""
    tmp = tmp_file()
    payload = json.dumps(state, indent=2)
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())
    try:
        if STATE_FILE.exists():
            if backup_file().exists():
                os.replace(backup_file(), backup_old_file())
            shutil.copy2(STATE_FILE, backup_file())
        # Windows: os.replace raises PermissionError while a reader (editor,
        # antivirus) holds the target open — retry briefly (issue #1 §2)
        for attempt in range(REPLACE_TRIES):
            try:
                os.replace(tmp, STATE_FILE)
                return
            except PermissionError:
                if attempt == REPLACE_TRIES - 1:
                    raise
                time.sleep(REPLACE_DELAY)
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)


def safe_write(new_state: Union[dict, str, bytes],
               expected_sha256: str = None) -> None:
    """
    Validate and atomically write new_state to STATE_FILE.

    expected_sha256 (required for CLI callers): the sha256 half of the
    version token from when the caller last read the file, or 'absent' for a
    new file. A mismatch aborts — the caller must re-read and retry.
    """
    _setup_logging()

    # Parse input (dict, JSON string, or bytes)
    if isinstance(new_state, (str, bytes)):
        try:
            state = json.loads(new_state)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}") from e
    else:
        state = new_state

    validate(state)

    # Optimistic-concurrency baseline, taken before acquiring the lock
    mtime_before = STATE_FILE.stat().st_mtime if STATE_FILE.exists() else 0

    with file_lock():
        if expected_sha256 is not None:
            _, current_sha = state_token()
            if expected_sha256 != current_sha:
                raise RuntimeError(
                    f"Stale write token — state changed since read "
                    f"(on disk: {current_sha[:12]}…). Re-read and retry."
                )

        if STATE_FILE.exists():
            mtime_after = STATE_FILE.stat().st_mtime
            if mtime_after != mtime_before:
                raise RuntimeError(
                    f"Concurrent write detected — state changed since read "
                    f"(mtime {mtime_before} -> {mtime_after}). "
                    "Caller should re-read and retry."
                )

        _atomic_write_state(state)

    med_count = len(state.get("meds", []))
    ts = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    msg = f"[{ts}] [safe_write] Write OK — {med_count} med(s) — backup: {backup_file()}"
    log.info("Write OK — %d med(s) — backup: %s", med_count, backup_file())
    print(msg)


# ── Pure transactions (issue #1 §2) ────────────────────────────────────────────

def _mirror_into_state(state: dict, events: list) -> None:
    """
    Mirror legacy-representable events into each med's state.history, capped
    at the last event_store.MIRROR_MAX entries (rollback for one release).
    """
    meds = {m["id"]: m for m in state.get("meds", [])}
    for ev in events:
        entry = event_store.mirror_entry(ev)
        if entry is None:
            continue
        med = meds.get(ev.get("med_id"))
        if not med:
            continue  # med removed — its history lines remain in the store
        med["state"].setdefault("history", []).append(entry)
    for med in state.get("meds", []):
        hist = med["state"].get("history") or []
        if len(hist) > event_store.MIRROR_MAX:
            med["state"]["history"] = hist[-event_store.MIRROR_MAX:]


def transact(fn, clock=None, expected_token: tuple = None,
             lock_timeout: float = LOCK_WAIT) -> dict:
    """
    Run a pure state transition under the state lock (issue #1 §2):

      1. Lock.
      2. Read state and history.
      3. fn(state_copy, history_view) -> (new_state, events). fn is PURE —
         no I/O, no sends. Re-running it never duplicates history.
      4. Validate.
      5. Append events to history.jsonl (fsync).
      6. Mirror into state.history, write state atomically.
      7. Unlock.

    Migrates legacy state first when tick.watermark_utc is unset. Returns
    the committed state.
    """
    clock = clock or get_clock()
    _setup_logging()
    with file_lock(timeout=lock_timeout):
        state, token = load_state()   # FileNotFoundError when missing
        if expected_token is not None and token != expected_token:
            raise RuntimeError(
                "Stale version token — state changed since read. Re-read and retry."
            )
        history = event_store.load_events(history_file())
        state, migration_events = event_store.migrate_state(state, clock.now_utc())
        base_history = history + migration_events

        new_state, events = fn(copy.deepcopy(state), list(base_history))
        events = list(events or [])
        validate(new_state)

        appended = event_store.append_events(history_file(), migration_events + events)
        # migration events came FROM state.history — mirroring them would double
        # it. Only new events enter the rollback mirror.
        migration_ids = {e["id"] for e in migration_events}
        _mirror_into_state(new_state, [e for e in appended if e["id"] not in migration_ids])
        _atomic_write_state(new_state)
        return new_state


# ── CLI entry point ────────────────────────────────────────────────────────────

def main() -> None:
    apply_process_umask()
    secure_private_files()
    _setup_logging()

    parser = argparse.ArgumentParser(
        description="Atomic, validated, token-checked state write.",
    )
    parser.add_argument(
        "--expected-sha256", required=True, metavar="SHA",
        help="sha256 of meds-state.json as you last read it, or 'absent' "
             "when creating a new file. A mismatch aborts the write.",
    )
    args = parser.parse_args()

    content = sys.stdin.read()
    if not content.strip():
        print("ERROR: empty input", file=sys.stderr)
        sys.exit(1)
    try:
        safe_write(content, expected_sha256=args.expected_sha256)
    except (ValueError, RuntimeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        log.error("%s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
