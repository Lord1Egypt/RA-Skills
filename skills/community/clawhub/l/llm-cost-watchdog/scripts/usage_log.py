"""
Usage log: the one place every cost-watchdog component writes to.

Format: JSON Lines in ~/.cost-watchdog/, one entry per LLM call.

Current-day writes go to `usage.jsonl`. On the first append of a new day,
`usage.jsonl` is renamed to `usage.YYYY-MM-DD.jsonl` (the date of its
most recent entry) and a fresh `usage.jsonl` is started. Aggregation
walks rolled files in reverse date order, skipping any whose filename
date is outside the requested window — so 10M-row histories don't hurt
`session_total(since=last_24h)`.

Entry schema:
    ts              float     — unix time
    source          str       — "openclaw" | "openai-wrap" | ...
    model           str       — whatever the source reported
    model_family    str       — canonical family (claude-haiku-4-5 etc.)
    provider        str
    input_tokens    int
    output_tokens   int
    cache_read_tokens   int
    cache_write_tokens  int
    cost_input      float
    cost_output     float
    cost_total      float
    session_id      str|None
    extra           dict
"""
from __future__ import annotations

import contextlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Optional

try:
    import fcntl  # POSIX only
    _HAS_FCNTL = True
except ImportError:
    _HAS_FCNTL = False

LOG_DIR = Path(os.environ.get("CW_LOG_DIR", Path.home() / ".cost-watchdog"))
LOG_DIR.mkdir(parents=True, exist_ok=True)

USAGE_LOG = LOG_DIR / "usage.jsonl"

_ROLLED_RE = re.compile(r"^usage\.(\d{4}-\d{2}-\d{2})\.jsonl$")


# ---------------------------------------------------------------------------
# Canonicalization (imported lazily to avoid bootstrapping cycles)
# ---------------------------------------------------------------------------

def _canonical_family(name: Optional[str]) -> Optional[str]:
    if not name:
        return name
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from model_canon import canonical_family
        return canonical_family(name)
    except ImportError:
        return name


# ---------------------------------------------------------------------------
# Rotation
# ---------------------------------------------------------------------------

def _today_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _first_line_date(path: Path) -> Optional[str]:
    """Return the UTC date of the first entry, or None on failure."""
    if not path.exists() or path.stat().st_size == 0:
        return None
    try:
        with path.open("rb") as f:
            first = f.readline().decode("utf-8", errors="replace").strip()
        if not first:
            return None
        entry = json.loads(first)
        ts = entry.get("ts")
        if ts is None:
            return None
        return datetime.fromtimestamp(float(ts), tz=timezone.utc).strftime("%Y-%m-%d")
    except (OSError, ValueError, json.JSONDecodeError):
        return None


def _rotate_if_stale() -> None:
    """
    If USAGE_LOG's first entry is from a previous UTC day, rename it to
    usage.<that-date>.jsonl so today's writes start in a fresh file.
    """
    date = _first_line_date(USAGE_LOG)
    if not date or date == _today_date():
        return
    rolled = LOG_DIR / f"usage.{date}.jsonl"
    # If a rolled file already exists for that date (shouldn't normally
    # happen, but crash+restart can cause it), append into it.
    if rolled.exists():
        try:
            with USAGE_LOG.open("rb") as src, rolled.open("ab") as dst:
                dst.write(src.read())
            USAGE_LOG.unlink()
            return
        except OSError:
            return
    try:
        USAGE_LOG.rename(rolled)
    except OSError:
        pass


def _rolled_files() -> List[Path]:
    """All rolled daily files, newest first."""
    out = []
    for p in LOG_DIR.iterdir():
        m = _ROLLED_RE.match(p.name)
        if m:
            out.append((m.group(1), p))
    out.sort(reverse=True)  # newest date first
    return [p for _, p in out]


def _file_date(path: Path) -> Optional[str]:
    """Extract the YYYY-MM-DD from a rolled filename, or None if it's the live file."""
    m = _ROLLED_RE.match(path.name)
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# Append
# ---------------------------------------------------------------------------

_LOCK_FILE = LOG_DIR / ".usage.lock"


@contextlib.contextmanager
def _file_lock():
    """
    Advisory exclusive lock on a sidecar file. On non-POSIX we no-op
    (Windows dev machines) — behavior is correctness on Linux/macOS.
    """
    if not _HAS_FCNTL:
        yield
        return
    with _LOCK_FILE.open("w") as f:
        try:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            yield
        finally:
            try:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            except OSError:
                pass


def append_usage(entry: dict, *,
                 budget_ceiling: Optional[float] = None,
                 budget_session_id: Optional[str] = None) -> None:
    """
    Append one usage entry. If `budget_ceiling` is set, the check-and-append
    happens under a file lock so two parallel calls can't both pass the
    budget check. The caller's `budget_session_id` scopes the running total
    to a session; pass None to budget against the full log.

    Raises BudgetExceeded (from tracker.py) if the check fails.
    """
    entry = dict(entry)
    entry.setdefault("ts", time.time())
    for field in ("input_tokens", "output_tokens",
                  "cache_read_tokens", "cache_write_tokens"):
        entry.setdefault(field, 0)
    for field in ("cost_input", "cost_output", "cost_total"):
        entry.setdefault(field, 0.0)
    entry.setdefault("session_id", None)
    entry.setdefault("extra", {})
    if "model_family" not in entry:
        entry["model_family"] = _canonical_family(entry.get("model"))

    line = json.dumps(entry, separators=(",", ":")) + "\n"

    with _file_lock():
        _rotate_if_stale()
        if budget_ceiling is not None:
            current = session_total(
                session_id=budget_session_id, _skip_lock=True
            ).get("cost_total", 0.0)
            if current + entry.get("cost_total", 0.0) > budget_ceiling:
                # Import here to avoid a circular import at module load.
                from tracker import BudgetExceeded
                raise BudgetExceeded(
                    f"Budget ${budget_ceiling:.2f} exceeded: already ${current:.4f}, "
                    f"this call ~${entry['cost_total']:.4f}."
                )
        with USAGE_LOG.open("a", encoding="utf-8") as f:
            f.write(line)


# ---------------------------------------------------------------------------
# Read helpers
# ---------------------------------------------------------------------------

def _files_relevant_to(since: Optional[float]) -> List[Path]:
    """
    Return files to scan, newest first. If `since` is given, skip any rolled
    file whose filename-date is strictly before since's UTC date (its
    entries can't possibly be in-window).
    """
    files = [USAGE_LOG] if USAGE_LOG.exists() else []
    rolled = _rolled_files()
    if since is None:
        return files + rolled
    min_date = datetime.fromtimestamp(since, tz=timezone.utc).strftime("%Y-%m-%d")
    for p in rolled:
        d = _file_date(p)
        if d is None or d >= min_date:
            files.append(p)
    return files


def iter_entries(since: Optional[float] = None) -> Iterable[dict]:
    """Generator over every entry, optionally filtered by ts >= since."""
    for path in _files_relevant_to(since):
        try:
            with path.open(encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if since is not None and entry.get("ts", 0) < since:
                        continue
                    yield entry
        except OSError:
            continue


def read_recent(limit: int = 100) -> list:
    """Return the last `limit` entries (most recent first), across rolled files."""
    out = []
    for path in [USAGE_LOG] + _rolled_files():
        if not path.exists():
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for line in reversed(lines):
            if not line.strip():
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
            if len(out) >= limit:
                return out
    return out


def session_total(session_id: Optional[str] = None,
                  since: Optional[float] = None,
                  by_family: bool = False,
                  _skip_lock: bool = False) -> dict:
    """
    Aggregate cost/tokens. Filters by session_id and/or since.
    `by_family=True` groups by canonical model family instead of raw model name.
    `_skip_lock` is an internal flag: append_usage() already holds the lock
    when it calls us, so we avoid re-acquiring it.
    """
    totals = {
        "calls": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "cache_read_tokens": 0,
        "cache_write_tokens": 0,
        "cost_total": 0.0,
        "by_model": {},
    }
    for entry in iter_entries(since=since):
        if session_id is not None and entry.get("session_id") != session_id:
            continue
        totals["calls"] += 1
        totals["input_tokens"] += entry.get("input_tokens", 0)
        totals["output_tokens"] += entry.get("output_tokens", 0)
        totals["cache_read_tokens"] += entry.get("cache_read_tokens", 0)
        totals["cache_write_tokens"] += entry.get("cache_write_tokens", 0)
        totals["cost_total"] += entry.get("cost_total", 0.0)
        key = (
            entry.get("model_family") if by_family
            else entry.get("model")
        ) or "unknown"
        bucket = totals["by_model"].setdefault(key, {"calls": 0, "cost": 0.0})
        bucket["calls"] += 1
        bucket["cost"] += entry.get("cost_total", 0.0)
    return totals


def clear() -> None:
    """Remove the current-day log. Rolled files are preserved."""
    if USAGE_LOG.exists():
        USAGE_LOG.unlink()


def clear_all() -> None:
    """Remove current-day + every rolled file. Used by tests."""
    clear()
    for p in _rolled_files():
        try:
            p.unlink()
        except OSError:
            pass
