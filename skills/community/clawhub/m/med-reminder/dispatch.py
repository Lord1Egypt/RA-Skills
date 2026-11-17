#!/usr/bin/env python3
"""
dispatch.py — Med reminder dispatch entry point (Python 3.9+, stdlib only)

Called by Task Scheduler / crontab. Since issue #1 PR 2 the only engine is
`tick` (see tick.py): every run evaluates each med's occurrences and acts on
the highest due stage. The legacy subcommands are thin wrappers that just run
the tick — no logic of their own — so leftover scheduled jobs are harmless.
They are kept for one release.

Subcommands:
    tick [--tick-minutes N]     Run one tick (default interval 5 minutes)
    fire/check/miss <id> <i>    Legacy wrappers → tick
    digest / reset-deferred     Legacy wrappers → tick

Flags:
    --dry-run    Print actions without sending messages or writing state
    --state PATH Path to meds-state.json (overrides MEDS_STATE_FILE;
                 baked into registered tasks by setup-tasks.py)

Environment:
    MEDS_STATE_FILE   Path to meds-state.json   (default: same dir as script)
    MEDS_LOG_FILE     Path to dispatch.log       (default: same dir as script)
    MEDS_SEND_CMD     Shell command to send a message (receives text on stdin)
                      Falls back to send-message.sh in the skill directory.
"""

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# ── Python version guard ───────────────────────────────────────────────────────

if sys.version_info < (3, 9):
    sys.exit(f"Python 3.9+ required — found {sys.version.split()[0]}")

# Console output includes unicode (em-dashes, arrows) that cp1252 consoles
# can't encode — degrade gracefully instead of crashing
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

# ── Paths ─────────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent.resolve()
STATE_FILE  = Path(os.environ.get("MEDS_STATE_FILE", SCRIPT_DIR / "meds-state.json"))
LOG_FILE    = Path(os.environ.get("MEDS_LOG_FILE",   SCRIPT_DIR / "dispatch.log"))
SEND_CMD    = os.environ.get("MEDS_SEND_CMD", "")

sys.path.insert(0, str(SCRIPT_DIR))
import safe_write as _safe_write_mod
from clock import Clock, get_clock
from safe_write import safe_write as _safe_write_fn

log = logging.getLogger("dispatch")

# ── Logging ───────────────────────────────────────────────────────────────────

def setup_logging(dry_run: bool) -> None:
    _safe_write_mod.configure_root_logging(
        "dispatch", LOG_FILE, logging.DEBUG if dry_run else logging.INFO)

# ── State I/O ─────────────────────────────────────────────────────────────────

def load_state() -> dict:
    if not STATE_FILE.exists():
        sys.exit(
            f"State file not found: {STATE_FILE}\n"
            "Run: cp meds-state.template.json meds-state.json"
        )
    with STATE_FILE.open(encoding="utf-8") as f:
        return json.load(f)

def save_state(state: dict, dry_run: bool) -> None:
    if dry_run:
        payload = json.dumps(state, indent=2)
        log.info("[DRY RUN] Would write state (first 300 chars):\n%s", payload[:300])
        return
    try:
        _safe_write_fn(state)
    except (ValueError, RuntimeError) as e:
        sys.exit(f"safe_write failed: {e}")
    log.debug("State saved OK")

# ── Messaging ─────────────────────────────────────────────────────────────────
#
# Sends are at-least-once with leases (issue #1 §3.6): the tick writes a
# send_intent under transact, sends ONCE here outside the lock with a hard
# timeout, and records sent/send_failed in a second transact. Retries happen
# on later ticks — never as an in-process sleep loop.

SEND_TIMEOUT_DEFAULT = 60  # seconds per send subprocess


def _bash_executable() -> str:
    """
    Resolve bash for send-message.sh. Scheduled tasks on Windows don't inherit
    the user's PATH, so plain 'bash' fails there — fall back to the standard
    Git for Windows locations.
    """
    bash = shutil.which("bash")
    if bash:
        return bash
    for cand in (r"C:\Program Files\Git\bin\bash.exe",
                 r"C:\Program Files (x86)\Git\bin\bash.exe"):
        if Path(cand).exists():
            return cand
    return "bash"  # let the shell's own error speak


def _resolve_send_cmd() -> str:
    send_helper = SCRIPT_DIR / "send-message.sh"
    if SEND_CMD:
        return SEND_CMD
    if send_helper.exists():
        return f'"{_bash_executable()}" "{send_helper}"'
    return ""


def _kill_tree(popen) -> None:
    """
    Kill a shell=True subprocess and its children. On Windows run()'s
    timeout only kills cmd.exe — the sender grandchild inherits the pipes,
    so communicate() would block until it exits on its own. A tree kill
    actually cancels a hung sender.
    """
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(popen.pid)],
                           capture_output=True)
        else:
            import signal
            os.killpg(os.getpgid(popen.pid), signal.SIGKILL)
    except (OSError, PermissionError, ProcessLookupError):
        popen.kill()


def send_once(text: str, timeout: int = SEND_TIMEOUT_DEFAULT,
              dry_run: bool = False) -> tuple:
    """
    One send attempt through MEDS_SEND_CMD / send-message.sh (message on
    stdin, exit 0 = delivered). Returns (ok, stderr). A hung sender is
    killed — tree, not just the shell — at `timeout` seconds and counts
    as a failure.
    """
    if dry_run:
        print(f"\n{'-' * 56}\n[DRY RUN] Message:\n{text}\n{'-' * 56}\n")
        return True, ""
    cmd = _resolve_send_cmd()
    if not cmd:
        log.error("No message sender configured")
        return False, "no sender configured"
    kwargs = {}
    if os.name != "nt":
        kwargs["start_new_session"] = True   # own process group → killable tree
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, encoding="utf-8", errors="replace",
                         **kwargs)
    try:
        _, stderr = p.communicate(input=text, timeout=timeout)
    except subprocess.TimeoutExpired:
        _kill_tree(p)
        try:
            p.communicate(timeout=5)
        except Exception:
            pass
        log.warning("Send timed out after %ss (%d chars)", timeout, len(text))
        return False, f"sender timed out after {timeout}s"
    if p.returncode == 0:
        log.info("Message sent (%d chars)", len(text))
        return True, ""
    err = (stderr or "").strip()
    log.warning("Send failed (exit %d): %s", p.returncode, err)
    return False, err or f"sender exited {p.returncode}"


def send_message(text: str, dry_run: bool, clock: Optional[Clock] = None) -> None:
    """Compatibility wrapper (doctor --send-test): one attempt, exit 1 on failure."""
    ok, err = send_once(text, dry_run=dry_run)
    if not ok:
        sys.exit(f"Send failed: {err}")

# ── Timezone ──────────────────────────────────────────────────────────────────

def get_tz(state: dict) -> ZoneInfo:
    name = state["global"]["timezone"]
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError:
        hint = (
            "\nOn Windows, run: pip install tzdata"
            if sys.platform == "win32" else ""
        )
        sys.exit(
            f"Unknown timezone '{name}'.{hint}\n"
            "Use an IANA name like 'America/Los_Angeles' or 'America/Chicago'.\n"
            "Full list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"
        )

# ── Time helpers ──────────────────────────────────────────────────────────────

def parse_hhmm(hhmm: str, tz: ZoneInfo, base: datetime) -> datetime:
    """Return base's calendar date at HH:MM in tz (timezone-aware)."""
    h, m = map(int, hhmm.split(":"))
    local = base.astimezone(tz)
    return local.replace(hour=h, minute=m, second=0, microsecond=0)

# Day-of-week keys for weekly meds, in Python weekday() order (mon=0)
DAY_KEYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")

def most_recent_weekly_time(day: str, hhmm: str, tz: ZoneInfo, now: datetime) -> datetime:
    """Most recent past occurrence of (day-of-week, HH:MM) relative to now."""
    target = DAY_KEYS.index(day)
    t = parse_hhmm(hhmm, tz, now)
    t -= timedelta(days=(t.weekday() - target) % 7)
    if t > now:
        t -= timedelta(days=7)
    return t

def in_quiet_hours(now: datetime, quiet: dict, tz: ZoneInfo) -> bool:
    """True if now is inside the quiet window. Handles midnight-spanning windows."""
    start = parse_hhmm(quiet["start"], tz, now)
    end   = parse_hhmm(quiet["end"],   tz, now)
    local = now.astimezone(tz)
    if start <= end:
        return start <= local < end   # same-day window
    return local >= start or local < end  # midnight-spanning (e.g. 22:00–07:00)

def fmt_12h(hhmm: str) -> str:
    """'08:00' → '8:00am', '20:00' → '8:00pm'"""
    h, m = map(int, hhmm.split(":"))
    suffix = "am" if h < 12 else "pm"
    return f"{h % 12 or 12}:{m:02d}{suffix}"

def fmt_days(days) -> str:
    """
    Day-of-week label for weekly schedules: 'tue' → 'Tue', ['tue','sat'] →
    'Tue+Sat', ['mon'..'fri'] → 'Mon–Fri' (runs of 3+ compress to First–Last).
    Accepts either stored form; empty input → ''.
    """
    if not days:
        return ""
    if isinstance(days, str):
        days = [days]
    idxs = sorted({DAY_KEYS.index(d) for d in days})
    parts, start = [], idxs[0]
    for prev, cur in zip(idxs, idxs[1:] + [None]):
        if cur != prev + 1:                  # the run that started at `start` ended
            if prev - start >= 2:
                parts.append(f"{DAY_KEYS[start].title()}–{DAY_KEYS[prev].title()}")
            else:
                parts.extend(DAY_KEYS[i].title() for i in range(start, prev + 1))
            start = cur
    return "+".join(parts)

# ── Next-due calculation ──────────────────────────────────────────────────────

def compute_next_due(med: dict, after: datetime, tz: ZoneInfo) -> Optional[datetime]:
    """
    Next scheduled dose after `after`. Returns None for as_needed.

    Frequency handling:
      once_daily  — next occurrence of times[0]
      twice_daily — soonest of times[0] or times[1]
      interval    — after + interval_hours
      weekly      — next occurrence of times[0] at least 6 days from after
      as_needed   — None
    """
    sched = med["schedule"]
    freq  = sched["frequency"]

    if freq == "as_needed":
        return None

    if freq == "interval":
        return after + timedelta(hours=sched["interval_hours"])

    # Time-of-day based frequencies
    times = sched["times"]
    candidates = []
    for t in times:
        candidate = parse_hhmm(t, tz, after)
        if candidate <= after:
            candidate += timedelta(days=1)
        candidates.append(candidate)

    if freq == "weekly":
        day = sched.get("day_of_week")
        if day:
            # Next occurrence of (day, times[0]) — most recent one + 7 days.
            # Multi-day schedules (PR 7) take the soonest of each day's next.
            days = [day] if isinstance(day, str) else day
            return min(most_recent_weekly_time(d, times[0], tz, after)
                       + timedelta(days=7) for d in days)
        # Legacy weekly without day_of_week: advance soonest candidate ~a week out
        base = min(candidates)
        while (base - after) < timedelta(days=6):
            base += timedelta(days=7)
        return base

    # once_daily or twice_daily
    return min(candidates)

# ── Template expansion ────────────────────────────────────────────────────────

def expand(template: str, med: dict) -> str:
    return (
        template
        .replace("{name}", med["name"])
        .replace("{dose}", med["dose"])
        .replace("{unit}", med["unit"])
    )

# ── History ───────────────────────────────────────────────────────────────────

def append_history(
    med: dict,
    event: str,
    dose_taken: Optional[str] = None,
    notes: str = "",
    clock: Optional[Clock] = None,
) -> None:
    clock = clock or get_clock()
    entry: dict = {
        "timestamp": clock.now_iso(),
        "event": event,
        "dose_prescribed": f"{med['dose']}{med['unit']}",
        "dose_taken": dose_taken,
    }
    if notes:
        entry["notes"] = notes
    med["state"]["history"].append(entry)

# ── Med lookup ────────────────────────────────────────────────────────────────

def find_med(state: dict, med_id: str) -> dict:
    for med in state["meds"]:
        if med["id"] == med_id:
            return med
    known = [m["id"] for m in state["meds"]]
    sys.exit(f"Med '{med_id}' not found. Known IDs: {known}")

# ── Tick (issue #1 §3) ────────────────────────────────────────────────────────
#
# The tick engine lives in tick.py (imported lazily to avoid a cycle: tick
# imports this module for the sender and shared helpers). The legacy
# subcommands below are thin wrappers that only call the tick, with no logic
# of their own, so any leftover scheduled job is harmless (kept one release).

def handle_tick(dry_run: bool, tick_minutes: int = 5,
                clock: Optional[Clock] = None) -> int:
    import tick
    return tick.run_tick(dry_run=dry_run, clock=clock or get_clock(),
                         tick_minutes=tick_minutes)


def handle_fire(med_id: str, dose_index: int, dry_run: bool,
                clock: Optional[Clock] = None) -> None:
    """Legacy wrapper (kept one release) — the tick owns reminders now."""
    handle_tick(dry_run, clock=clock)


def handle_check(med_id: str, dose_index: int, dry_run: bool,
                 clock: Optional[Clock] = None) -> None:
    """Legacy wrapper (kept one release) — the tick owns nudges now."""
    handle_tick(dry_run, clock=clock)


def handle_miss(med_id: str, dose_index: int, dry_run: bool,
                clock: Optional[Clock] = None) -> None:
    """Legacy wrapper (kept one release) — the tick owns missed logging now."""
    handle_tick(dry_run, clock=clock)


def handle_digest(dry_run: bool, clock: Optional[Clock] = None) -> None:
    """Legacy wrapper (kept one release) — the tick owns the digest now."""
    handle_tick(dry_run, clock=clock)


def handle_reset_deferred(dry_run: bool) -> None:
    """Legacy wrapper (kept one release) — deferred is dead state to the tick."""
    handle_tick(dry_run)

# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    _safe_write_mod.apply_process_umask()   # issue #1 §2: private files, before any are created
    parser = argparse.ArgumentParser(
        description="Med reminder dispatch. Call from Task Scheduler or crontab.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without sending messages or writing state",
    )
    parser.add_argument(
        "--state",
        default=None,
        metavar="PATH",
        help="Path to meds-state.json (overrides MEDS_STATE_FILE; baked into scheduled tasks)",
    )

    sub = parser.add_subparsers(dest="mode", required=True, metavar="MODE")

    p_tick = sub.add_parser("tick", help="Run one tick: evaluate every med's stages")
    p_tick.add_argument("--tick-minutes", type=int, default=5, metavar="N",
                        help="Scheduled tick interval in minutes (default 5); "
                             "widens the fresh-missed message window")

    p_fire = sub.add_parser("fire", help="Legacy (kept one release): runs the tick")
    p_fire.add_argument("med_id",    help="Med ID, e.g. med-001")
    p_fire.add_argument("dose_index", type=int, help="Index into schedule.times[] (0-based)")

    p_check = sub.add_parser("check", help="Legacy (kept one release): runs the tick")
    p_check.add_argument("med_id")
    p_check.add_argument("dose_index", type=int)

    p_miss = sub.add_parser("miss", help="Legacy (kept one release): runs the tick")
    p_miss.add_argument("med_id")
    p_miss.add_argument("dose_index", type=int)

    sub.add_parser("digest",         help="Legacy (kept one release): runs the tick")
    sub.add_parser("reset-deferred", help="Legacy (kept one release): runs the tick")
    # confirm / defer live in reply.py — use: python3 reply.py confirm <med-id>

    args = parser.parse_args()
    setup_logging(args.dry_run)

    if args.state:
        global STATE_FILE
        STATE_FILE = Path(args.state)
        _safe_write_mod.STATE_FILE = Path(args.state)  # writer keeps its own copy

    _safe_write_mod.secure_private_files(extra=(LOG_FILE,))   # after --state rebind

    mode = args.mode
    dr   = args.dry_run

    if mode == "tick":
        sys.exit(handle_tick(dr, tick_minutes=args.tick_minutes))
    elif mode == "fire":
        handle_fire(args.med_id, args.dose_index, dr)
    elif mode == "check":
        handle_check(args.med_id, args.dose_index, dr)
    elif mode == "miss":
        handle_miss(args.med_id, args.dose_index, dr)
    elif mode == "digest":
        handle_digest(dr)
    elif mode == "reset-deferred":
        handle_reset_deferred(dr)


if __name__ == "__main__":
    main()
