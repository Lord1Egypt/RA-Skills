"""Lock mechanism — prevents double execution via PID file + flock."""

from __future__ import annotations
import fcntl
import os
from typing import Optional

LOCK_FILE = "/tmp/night-shift.lock"


def acquire_lock() -> Optional[int]:
    """Acquire exclusive lock. Returns fd on success, None if already running."""
    try:
        fd = open(LOCK_FILE, "w")
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fd.write(str(os.getpid()))
        fd.flush()
        return fd
    except (BlockingIOError, IOError, OSError):
        try:
            fd.close()
        except Exception:
            pass
        return None


def is_locked() -> bool:
    """Check if night-shift is currently running."""
    if not os.path.exists(LOCK_FILE):
        return False
    try:
        with open(LOCK_FILE) as f:
            pid = int(f.read().strip())
        return _pid_exists(pid)
    except (ValueError, FileNotFoundError):
        return False


def get_lock_pid() -> Optional[int]:
    """Get PID of running night-shift, if any."""
    if not os.path.exists(LOCK_FILE):
        return None
    try:
        with open(LOCK_FILE) as f:
            return int(f.read().strip())
    except (ValueError, FileNotFoundError):
        return None


def release_lock(fd: int):
    """Release the lock and clean up."""
    try:
        fcntl.flock(fd, fcntl.LOCK_UN)
        fd.close()
    except Exception:
        pass
    try:
        os.remove(LOCK_FILE)
    except FileNotFoundError:
        pass


def _pid_exists(pid: int) -> bool:
    """Check if a process with given PID exists."""
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False
