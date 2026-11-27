"""
Shared utilities for Homebase.
"""
import contextlib
import fcntl
import json
import os
import sys
import tempfile
import time
from datetime import datetime
from typing import Any


# ─── Atomic JSON writes ─────────────────────────────────────────────────────
#
# Every state file write goes through this. Reason: a naked
# ``open(path, "w") + json.dump`` will leave a truncated/empty file behind if
# the process is killed mid-write (cron timeout, OOM, sigkill, disk full).
# The next run then crashes on JSONDecodeError. For a skill that runs
# unattended for weeks, that single failure mode is the difference between
# "self-heals" and "wakes you up Saturday morning".
#
# How to apply: replace
#     with open(path, "w") as f:
#         json.dump(data, f, indent=2)
# with
#     write_json_atomic(path, data)

def write_json_atomic(path: str, data: Any, indent: int = 2) -> None:
    """Write JSON to ``path`` atomically: tempfile in same dir → fsync → rename."""
    dir_path = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(dir_path, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=".tmp.", suffix=".json", dir=dir_path)
    try:
        with os.fdopen(fd, "w") as tmp:
            json.dump(data, tmp, indent=indent, default=str)
            tmp.flush()
            os.fsync(tmp.fileno())
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise

# ─── Cross-process file lock ────────────────────────────────────────────────
#
# write_json_atomic prevents a *corrupt* file from a crash mid-write, but it
# does nothing to prevent a *lost update*: two processes that each load a
# JSON file, mutate their own in-memory copy, and call write_json_atomic
# will race on the final os.replace(), and whichever finishes last silently
# discards the other's change. Locking your own freshly-created temp file
# (as a couple of call sites used to) doesn't help — no other process can
# ever see or contend for that file.
#
# Callers must hold this lock for the *entire* read-modify-write critical
# section (reload from disk, mutate, save) — locking only the final write
# still loses updates if two processes both loaded stale data first.

LOCK_TIMEOUT_SECONDS = 30.0


@contextlib.contextmanager
def locked_file(path: str, timeout: float = LOCK_TIMEOUT_SECONDS):
    """Exclusive cross-process lock scoped to ``path``, via a sibling
    ``<path>.lock`` file.

    BOUNDED. The acquire retries non-blocking until ``timeout`` and then
    raises TimeoutError. A plain blocking flock has no deadline, and these
    locks now sit on the 6:05 AM briefing path — waiting forever there means
    the briefing never sends at all, which is strictly worse than sending
    without whatever bookkeeping the lock protects. Callers doing bookkeeping
    (rather than guarding real state) should catch TimeoutError and continue.
    """
    dir_path = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(dir_path, exist_ok=True)
    lock_path = path + ".lock"
    with open(lock_path, "a") as lock_f:
        deadline = time.monotonic() + timeout
        while True:
            try:
                fcntl.flock(lock_f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                if time.monotonic() >= deadline:
                    raise TimeoutError(
                        f"could not acquire {lock_path} within {timeout}s")
                time.sleep(0.05)
        try:
            yield
        finally:
            fcntl.flock(lock_f, fcntl.LOCK_UN)


@contextlib.contextmanager
def time_limit(seconds: int):
    """Wall-clock ceiling for a block, via SIGALRM.

    Restores a bound that was lost when a tool stopped shelling out: the
    subprocess carried `timeout=120`, and the in-process call that replaced it
    carried nothing, so a hung Google API call could hold a launchd runner
    open indefinitely. A per-REQUEST timeout does not bound a paginated
    sync multiplies without limit.

    No-op off the main thread, where SIGALRM cannot be installed.
    """
    import signal

    def _fire(signum, frame):
        raise TimeoutError(f"exceeded {seconds}s")

    try:
        previous = signal.signal(signal.SIGALRM, _fire)
    except ValueError:
        yield
        return
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)


def read_id_list(path: str) -> list:
    """The on-disk ordered ID record for a dedup ledger. Missing file -> [].

    One implementation. The school monitor and the bills watcher each grew
    their own copy of this exists/open/json.load/list dance, and the cap rule
    below was unified across them while the read half was not.
    """
    if os.path.exists(path):
        with open(path, "r") as f:
            return list(json.load(f))
    return []


class AuthErrorFlag:
    """"Have we already told a human about this auth failure?" persisted.

    Both Gmail consumers need exactly this: alert on the first failure, stay
    silent until the token is fixed and breaks again. They had near-verbatim
    copies differing only in a log prefix, and this diff edited one of them
    and not the other, which is how two copies start to drift.
    """

    def __init__(self, path: str, label: str):
        self.path = path
        self.label = label

    def notified(self) -> bool:
        try:
            if os.path.exists(self.path):
                with open(self.path) as f:
                    return json.load(f).get("notified", False)
        except Exception:
            pass
        return False

    def set(self, notified: bool) -> None:
        try:
            write_json_atomic(self.path, {
                "notified": notified,
                "updated_at": datetime.now().isoformat(),
            })
        except Exception as e:
            print(f"[{self.label}] Warning: could not save auth_error_state: {e}",
                  file=sys.stderr)


# ─── Bounded, ordered ID ledgers ────────────────────────────────────────────
#
# Dedup ledgers (processed emails, synced calendar entries, handled bills) are
# capped so they don't grow forever. The cap has to be applied to an *ordered*
# sequence: `list(some_set)[-500:]` looks like "keep the newest 500" and is
# not — a set has no order, so which 500 survive is a hash-ordering accident.
# Past the cap that silently drops recent IDs, and a dropped ID means an email
# already handled comes back: duplicate school calendar proposals, or a bill
# posted to the family group a second time.
#
# So the on-disk list stays the ordered record and the set is only ever an
# in-memory membership index.

def append_capped_id(existing: list, new_id: str, cap: int = 500) -> list:
    """Append ``new_id`` (deduped, order-preserving) and keep the last ``cap``."""
    merged = list(dict.fromkeys(list(existing) + [new_id]))
    return merged[-cap:]


# Note: All LLM interactions have been removed from this skill.
# Python tools must return raw or structured data to the OpenClaw agent,
# which uses whichever model OpenClaw is configured with to reason about the data.


