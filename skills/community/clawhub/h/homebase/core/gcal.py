"""
gcal.py — the one place homebase talks to Google Calendar.

Every call goes through the `gog` CLI (gogcli.sh, an OpenClaw project), which
owns the OAuth refresh token in the macOS Keychain and mints access tokens per
invocation. Nothing here imports googleapiclient, handles credentials, or reads
a GOOGLE_* env var — that is the entire point of the module.

Verified 2026-09-07 that a launchd-spawned process can read gog's Keychain
entries, which is what the runners depend on. Re-verify with
`launchctl kickstart`, never a manual shell run: a manual run inherits your
login session and proves nothing about launchd's.

Returns are deliberately Google-shaped — `start`/`end` as
{'dateTime': ...} or {'date': ...} — because gog mirrors the API's own shape.
Callers that already parsed Google's response (calendar_aggregator's event
builder) keep working without a translation layer, which is what makes this
swap small rather than a rewrite.

Two flags here are load-bearing and must not be dropped:

  --all-pages  `gog calendar events` defaults to --max=10. Without this, a
               busy fortnight silently returns the first 10 events and every
               consumer concludes the rest do not exist. Silent truncation is
               the failure shape that has already cost this workspace real
               school mail; it must not be reachable from a default.
  --force      `gog calendar delete` refuses to act non-interactively without
               it, and reports the refusal on a SUCCESSFUL exit. A caller
               would read that as "deleted" and move on.
"""

import json
import os
import subprocess
from typing import Dict, List, Optional

# Absolute-path-able for launchd, which supplies only /usr/bin:/bin and would
# not otherwise find a Homebrew binary. Overridable so tests can point it at a
# path that cannot exist and fail loudly instead of reaching the network.
GOG_BIN = os.environ.get("GOG_BIN", "gog")

_TIMEOUT_SECONDS = 60

# Google's partial-response syntax, passed through by --fields.
#
# extendedProperties and the rest are not returned by default. `items(...)` is
# required because this is a list response — a bare field list is rejected with
# "Invalid field selection id". nextPageToken must be named explicitly or
# --all-pages has no token to follow and quietly returns page one.
#
# recurringEventId is not decoration: trip_detector skips recurring events
# unless their title carries a trip keyword, and without this field every
# recurring event reads as one-off. Adding a consumer means adding its field
# here — a missing one is absent, not an error.
_EVENT_FIELDS = (
    "items(id,summary,start,end,location,description,status,"
    "recurringEventId),nextPageToken"
)


class GogError(RuntimeError):
    """A gog invocation failed. Carries stderr, where gog puts the reason
    (stdout stays parseable)."""


def _gog(*args: str) -> Dict:
    """Run gog with JSON output and return the parsed payload.

    Always --no-input: these run unattended under launchd, where a prompt is a
    hang rather than a question.
    """
    cmd = [GOG_BIN, *args, "--json", "--no-input"]
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=_TIMEOUT_SECONDS
        )
    except FileNotFoundError as e:
        raise GogError(f"gog not found on PATH (GOG_BIN={GOG_BIN!r})") from e
    except subprocess.TimeoutExpired as e:
        raise GogError(
            f"gog timed out after {_TIMEOUT_SECONDS}s: {' '.join(args[:3])}"
        ) from e

    if proc.returncode != 0:
        raise GogError(
            f"gog {' '.join(args[:3])} failed (rc={proc.returncode}): "
            f"{(proc.stderr or proc.stdout or '').strip()[:300]}"
        )
    try:
        return json.loads(proc.stdout or "{}")
    except json.JSONDecodeError as e:
        raise GogError(
            f"gog {' '.join(args[:3])} returned unparseable JSON: "
            f"{proc.stdout[:200]}"
        ) from e


# ─── Reads ───────────────────────────────────────────────────────────────────

def list_events(calendar_id: str, time_min: str, time_max: str,
                query: str = "") -> List[Dict]:
    """Every event on `calendar_id` between `time_min` and `time_max`.

    Both bounds are RFC3339. Google-shaped dicts come back, so callers can read
    `e['start']['dateTime']` / `e['start']['date']` exactly as they did against
    the API directly.

    Raises GogError rather than returning [] on failure. An empty list and a
    failed call mean opposite things to a caller deciding whether to drop
    cached events, and conflating them is how a transient outage turns into a
    calendar that looks empty.
    """
    payload = _gog(
        "calendar", "events", calendar_id,
        "--from", time_min,
        "--to", time_max,
        "--all-pages",
        "--fields", _EVENT_FIELDS,
        *(["--query", query] if query else []),
    )
    return payload.get("events") or []


# ─── Writes ──────────────────────────────────────────────────────────────────

def create_event(calendar_id: str, summary: str, start: str, end: str,
                 all_day: bool = False, description: str = "",
                 location: str = "", timezone: str = "") -> Dict:
    """Create one event. `start`/`end` are RFC3339 for timed events, or
    YYYY-MM-DD when `all_day`.

    For all-day events gog is given the dates as-is: the caller owns the
    inclusive/exclusive question, because Google's all-day `end.date` is
    EXCLUSIVE and homebase deliberately speaks in inclusive end dates
    everywhere else (see calendar_manager's `end_date` argument).
    """
    args = ["calendar", "create", calendar_id, "--summary", summary,
            "--from", start, "--to", end]
    if all_day:
        args.append("--all-day")
    elif timezone:
        args += ["--timezone", timezone]
    if description:
        args += ["--description", description]
    if location:
        args += ["--location", location]
    return _gog(*args)


def delete_event(calendar_id: str, event_id: str) -> None:
    """Delete one event by Google's own id. Idempotent: an event that is
    already gone is the desired end state, not an error."""
    try:
        _gog("calendar", "delete", calendar_id, event_id, "--force")
    except GogError as e:
        if any(code in str(e) for code in ("404", "410", "notFound", "deleted")):
            return
        raise


def update_event(calendar_id: str, event_id: str, summary: str = None,
                 start: str = None, end: str = None, all_day: bool = False,
                 timezone: str = "") -> Dict:
    """Patch one event by id. Only the fields passed are changed.

    A PATCH, unlike the full-body PUT this replaced. That matters: the old
    code round-tripped the whole event, so any field it did not understand was
    rewritten from whatever the read returned. Sending only what changed can't
    clobber a field it never looked at.

    `all_day` must be set when start/end are date-only, or gog sends them as
    timestamps and Google converts an all-day event into a timed one.
    """
    args = ["calendar", "update", calendar_id, event_id]
    if summary:
        args += ["--summary", summary]
    if start:
        args += ["--from", start]
    if end:
        args += ["--to", end]
    if all_day:
        args.append("--all-day")
    elif timezone and (start or end):
        args += ["--timezone", timezone]
    return _gog(*args)


# ─── Health ──────────────────────────────────────────────────────────────────

def auth_status() -> Dict:
    """What gog thinks of its own credentials. Replaces the GOOGLE_* env-var
    probe that used to stand in for a health check — that probe could not tell
    a missing secret from an interpreter with no keyring, and it never asked
    Google anything."""
    return _gog("auth", "status")
