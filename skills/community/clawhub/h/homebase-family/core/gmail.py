"""
gmail.py — the one place homebase talks to Gmail.

Every call goes through the `gog` CLI, which owns the OAuth refresh token in
the macOS credential store and mints short-lived tokens per invocation. Nothing here imports
googleapiclient, handles credentials, or reads a GOOGLE_* env var.

Returns are Google-shaped: `get_message` hands back the raw Gmail message
(`payload`, `internalDate`, `labelIds`, …) exactly as the API defines it,
because gog passes it through unchanged. That is what lets the MIME walkers in
core/pdf_attachments.py and the body/attachment helpers in the bills and school
features keep working untouched — this migration replaced the transport, not
the parsing.

Read-only by construction: there is no send, no label write, no trash. Both
consumers only ever read mail and keep their own dedup ledgers. If a caller
ever needs to write, add it deliberately rather than by generalising `_gog`.
"""

import base64
import json
import os
import re
import subprocess
import tempfile
from typing import Dict, List, Optional

# Absolute-path-able for launchd, which supplies only /usr/bin:/bin and would
# not otherwise find a Homebrew binary. Overridable so tests can point it at a
# path that cannot exist and fail loudly instead of reaching the network.
GOG_BIN = os.environ.get("GOG_BIN", "gog")

# Generous relative to calendar: a message with a large PDF is a real payload,
# and a bill that times out comes back on Thursday rather than being lost, but
# only because the ledger is advanced by the caller after delivery.
_TIMEOUT_SECONDS = 120


# Go's url.Error puts the quoted request URL ahead of the reason. A search URL
# carries the whole query and runs ~250 chars, so capping gog's stderr kept the
# URL and cut the reason: on 2026-10-28 08:07 a token refresh failure was
# logged as `round trip: base token ` and nothing more, and the school
# monitor's network check never saw the text it keys on.
_REQUEST_URL = re.compile(r'"https?://[^"]*"')


def _reason(text: str) -> str:
    return _REQUEST_URL.sub('"<url>"', text.strip())[:300]


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
            f"{_reason(proc.stderr or proc.stdout or '')}"
        )
    try:
        return json.loads(proc.stdout or "{}")
    except json.JSONDecodeError as e:
        raise GogError(
            f"gog {' '.join(args[:3])} returned unparseable JSON: "
            f"{proc.stdout[:200]}"
        ) from e


def search(query: str, max_results: int = 10,
           all_pages: bool = False) -> List[str]:
    """Message ids matching a Gmail query string, newest first.

    `gog gmail messages search`, not `gog gmail search`: the latter returns one
    row per THREAD. Both dedup ledgers here are keyed on message id, and a
    thread with two bills in it would collapse to one row and lose the second.

    `--max` is passed explicitly because gog's default is 10 — fine as a
    default, but it must be the caller's decision rather than an accident.

    `all_pages` is for callers that filter the result against a processed
    ledger. A fixed first page of newest ids fills up with mail already
    handled, and anything older than the page is never returned at all — it
    ages out of the query's lookback without once being looked at. With it,
    `max_results` is only the page size; bound the result with the query's
    own `newer_than:` instead.
    """
    args = ["gmail", "messages", "search", query, "--max", str(max_results)]
    if all_pages:
        args.append("--all")
    payload = _gog(*args)
    rows = payload.get("messages") or payload.get("results") or []
    if isinstance(payload, list):
        rows = payload
    return [r["id"] for r in rows if isinstance(r, dict) and r.get("id")]


def get_message(msg_id: str, fmt: str = "full") -> Dict:
    """One message in Gmail's own shape — `payload`, `internalDate`, headers.

    Callers walk `payload` themselves (MIME parts, attachment ids, inline
    bodies). Reshaping it here would mean re-implementing that walk for every
    consumer, so the raw structure is the contract.
    """
    payload = _gog("gmail", "get", msg_id, "--format", fmt)
    return payload.get("message") or payload


def get_attachment(msg_id: str, attachment_id: str) -> Optional[bytes]:
    """Raw bytes of one attachment, or None if gog returned no content.

    gog always writes the attachment to a file, `--inline` or not: `--inline`
    only *also* returns it as base64. Left to its default, that file lands in
    gog's own gmail-attachments directory and stays there for good — every
    bill PDF and school flyer ever read (found 2026-11-27, flagged by
    ClawHub's scan). So each download goes to a private temp directory that is
    deleted before this returns, and the bytes come from the JSON.

    Over gog's inline limit (3 MB by default) there is no base64, and this
    returns None rather than a path the caller would treat as bytes; the file
    is deleted with the directory either way.
    """
    with tempfile.TemporaryDirectory(prefix="homebase-att-") as tmp:
        payload = _gog("gmail", "attachment", msg_id, attachment_id,
                       "--inline", "--out", tmp + os.sep)
    data = payload.get("contentBase64") or payload.get("data")
    if not data:
        return None
    return base64.urlsafe_b64decode(data)
