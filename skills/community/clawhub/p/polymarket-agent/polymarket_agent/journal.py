"""Append-only journal of everything that touches money.

AUDIT FIX (Medium — "Missing User Warnings", 4 occurrences): v1.0.2 could
execute real orders leaving no trace at all. With no trail there is no way for
the user to audit what the agent did, nor any way to enforce a daily cap.

The journal is the SOURCE OF TRUTH for the daily spend used by the guard-rails,
so it is written BEFORE the order is sent (intent) and updated afterwards with
the outcome. An order that vanishes mid-flight stays recorded as `submitted`
and keeps counting against the limit — it fails to the safe side.
"""
from __future__ import annotations

import json
import os
import stat
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Iterator, List, Optional

from .paths import harden_file, journal_path

MAX_JOURNAL_BYTES = 5 * 1024 * 1024

#: Past this age, an order still marked open in the journal is treated as dead
#: if there has been no reconciliation with the exchange.
STALE_OPEN_SECONDS = 7 * 24 * 60 * 60


@dataclass
class Entry:
    """One journal line."""

    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")
    )
    ts: float = field(default_factory=time.time)
    kind: str = "order"  # order | halt | config | autonomous
    status: str = "submitted"  # intent | submitted | filled | rejected | failed | dry_run
    side: str = ""
    token_id: str = ""
    market: str = ""
    price: float = 0.0
    size: float = 0.0
    notional: float = 0.0
    order_id: str = ""
    detail: str = ""

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)


def _append_line(line: str) -> None:
    path = journal_path()
    flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND
    fd = os.open(str(path), flags, stat.S_IRUSR | stat.S_IWUSR)
    with os.fdopen(fd, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    harden_file(path)


def record(entry: Entry) -> Entry:
    """Append an entry. Never raises — losing the journal must not take down a
    trading session in progress, but the failure is reported on stderr so it
    does not pass silently."""
    try:
        _rotate_if_needed()
        _append_line(entry.to_json())
    except OSError as exc:  # pragma: no cover - edge-case I/O
        import sys

        print(f"[journal] failed to record: {exc}", file=sys.stderr)
    return entry


def update_status(entry_id: str, status: str, **changes: Any) -> None:
    """Record the TRANSITION as a new line (append-only, no rewriting).

    Rewriting the file would open room for corruption and for erasing the
    trail; an order's final state is the last line carrying that `id`.
    """
    payload: Dict[str, Any] = {
        "id": entry_id,
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "ts": time.time(),
        "kind": "order",
        "status": status,
    }
    payload.update(changes)
    try:
        _append_line(json.dumps(payload, ensure_ascii=False))
    except OSError:
        pass


def _rotate_if_needed() -> None:
    path = journal_path()
    try:
        if path.exists() and path.stat().st_size > MAX_JOURNAL_BYTES:
            backup = path.with_suffix(".jsonl.1")
            path.replace(backup)
            harden_file(backup)
    except OSError:
        pass


def _read_file(path) -> Iterator[Dict[str, Any]]:
    if not path.exists():
        return
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue
    except OSError:
        return


def iter_entries() -> Iterator[Dict[str, Any]]:
    """Walk the journal in chronological order, INCLUDING the rotated file.

    BUG FIX (found in review): reading only the current file meant a rotation
    zeroed accumulated spend — and the daily cap is computed from here.
    Rotating (a maintenance event) must not free up budget.
    """
    yield from _read_file(journal_path().with_suffix(".jsonl.1"))
    yield from _read_file(journal_path())


def latest_by_id() -> Dict[str, Dict[str, Any]]:
    """Final state of each order (last line wins).

    `first_ts` preserves the instant of the FIRST line for that id. Without it,
    a status update rewrote `ts` and could drag an old order into the 24h
    window (or out of it) — which distorts the spend cap in both directions.
    """
    merged: Dict[str, Dict[str, Any]] = {}
    for row in iter_entries():
        rid = row.get("id")
        if not rid:
            continue
        slot = merged.setdefault(rid, {})
        if "first_ts" not in slot:
            slot["first_ts"] = float(row.get("ts", 0.0) or 0.0)
        slot.update(row)
    return merged


#: Statuses in which the order did not (and will not) consume capital.
NON_SPENDING = {"rejected", "failed", "dry_run", "cancelled"}

#: Statuses in which the order may still be live on the exchange's book.
OPEN_STATUSES = {"submitted", "live", "matched", "delayed"}


def spend_since(seconds: float) -> float:
    """Sum of notional of BUYS that consumed capital within the window.

    Sells do not count: they return capital, they do not consume it.
    """
    cutoff = time.time() - seconds
    total = 0.0
    for row in latest_by_id().values():
        if row.get("kind") != "order":
            continue
        if str(row.get("side", "")).upper() != "BUY":
            continue
        if row.get("status") in NON_SPENDING:
            continue
        if float(row.get("first_ts", row.get("ts", 0.0)) or 0.0) < cutoff:
            continue
        total += float(row.get("notional", 0.0) or 0.0)
    return total


def recent(limit: int = 20) -> List[Dict[str, Any]]:
    rows = sorted(latest_by_id().values(), key=lambda r: r.get("ts", 0.0), reverse=True)
    return rows[:limit]


def open_order_count() -> int:
    """Estimate of live orders ACCORDING TO THE JOURNAL.

    BUG FIX (found in review — was P0): the journal alone never learns that an
    order was filled or cancelled outside the skill, so this counter only ever
    grew. On reaching `max_open_orders` (default 10) the skill blocked all
    trading forever, with no obvious way to unblock it.

    The real fix is `reconcile_open_orders()`, fed by the exchange — this
    function is only the fallback for when there is no network. That is also
    why it ignores stale entries: an order left "submitted" for more than
    STALE_OPEN_SECONDS is almost certainly dead, and it is better to
    underestimate (and let the exchange's own cap block us) than to lock the
    user out indefinitely.
    """
    cutoff = time.time() - STALE_OPEN_SECONDS
    return sum(
        1
        for row in latest_by_id().values()
        if row.get("kind") == "order"
        and row.get("status") in OPEN_STATUSES
        and float(row.get("first_ts", row.get("ts", 0.0)) or 0.0) >= cutoff
    )


def close_by_order_id(order_id: str, status: str = "cancelled",
                      detail: str = "") -> bool:
    """Close the journal entry matching an exchange order_id.

    BUG FIX (found in review): `cancel_order` wrote a NEW line with its own id,
    so the original entry stayed `submitted` — the cancelled order kept
    counting against `max_open_orders` forever.
    """
    order_id = str(order_id or "")
    if not order_id:
        return False
    for entry_id, row in latest_by_id().items():
        if str(row.get("order_id") or "") == order_id and row.get("status") in OPEN_STATUSES:
            update_status(entry_id, status, order_id=order_id, detail=detail)
            return True
    return False


def close_all_open(status: str = "cancelled", detail: str = "") -> int:
    """Close every open journal entry (used by `cancel --all`)."""
    closed = 0
    for entry_id, row in latest_by_id().items():
        if row.get("kind") == "order" and row.get("status") in OPEN_STATUSES:
            update_status(entry_id, status, detail=detail)
            closed += 1
    return closed


def reconcile_open_orders(live_order_ids: Iterable[str]) -> int:
    """Close in the journal the orders the exchange no longer lists as open.

    The exchange is the source of truth. Called before evaluating a new order,
    whenever there is network. Returns how many entries were closed.
    """
    live = {str(oid) for oid in live_order_ids if oid}
    closed = 0
    for entry_id, row in latest_by_id().items():
        if row.get("kind") != "order" or row.get("status") not in OPEN_STATUSES:
            continue
        order_id = str(row.get("order_id") or "")
        # With no order_id we cannot assert it died (it may have failed before
        # the exchange ever answered) — let the age-based discard handle it.
        if order_id and order_id not in live:
            update_status(entry_id, "closed", detail="reconciled with the exchange")
            closed += 1
    return closed
