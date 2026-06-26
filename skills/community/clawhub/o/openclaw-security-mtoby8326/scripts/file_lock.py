"""Cross-platform file lock using atomic exclusive-create.

Usage:
    from file_lock import FileLock

    with FileLock('/path/to/data.json.lock'):
        # read / write data.json safely
        ...

The lock is acquired by atomically creating a `.lock` file (O_CREAT | O_EXCL).
If another process holds the lock, we spin-wait with 50ms intervals up to a
configurable timeout.  On timeout, the stale lock file is force-removed and
acquisition is retried once (guards against dead processes leaving orphan locks).

Stdlib-only.  Works on Windows and POSIX.
"""

import os
import time


class FileLockTimeout(Exception):
    """Raised when the lock cannot be acquired within the timeout."""


class FileLock:
    """Context manager for file-based mutual exclusion.

    Parameters:
        lock_path:      Full path to the lock file (e.g. ``data.json.lock``).
        timeout:        Maximum seconds to wait for the lock (default 5).
        poll_interval:  Seconds between acquisition attempts (default 0.05).
    """

    def __init__(self, lock_path: str, *, timeout: float = 5.0,
                 poll_interval: float = 0.05):
        self.lock_path = lock_path
        self.timeout = timeout
        self.poll_interval = poll_interval
        self._fd = None

    # ------------------------------------------------------------------
    def acquire(self) -> None:
        deadline = time.monotonic() + self.timeout
        while True:
            try:
                self._fd = os.open(
                    self.lock_path,
                    os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                )
                return  # lock acquired
            except (FileExistsError, OSError):
                if time.monotonic() >= deadline:
                    # Timeout — attempt stale-lock recovery once
                    self._remove_stale()
                    try:
                        self._fd = os.open(
                            self.lock_path,
                            os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                        )
                        return
                    except (FileExistsError, OSError):
                        raise FileLockTimeout(
                            f'Could not acquire lock: {self.lock_path}'
                        )
                time.sleep(self.poll_interval)

    def release(self) -> None:
        if self._fd is not None:
            try:
                os.close(self._fd)
            except OSError:
                pass
            self._fd = None
        self._remove_stale()

    # ------------------------------------------------------------------
    def _remove_stale(self) -> None:
        try:
            os.remove(self.lock_path)
        except OSError:
            pass

    # ------------------------------------------------------------------
    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        return False
