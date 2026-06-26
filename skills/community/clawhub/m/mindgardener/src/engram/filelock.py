"""
Simple file locking for multi-agent safety.

Problem: Two agents running `engram extract` simultaneously might both try
to write to the same entity file, causing data loss.

Solution: Advisory file locks using fcntl (Unix) or a lockfile fallback.
Lock is per-entity-file. Held only during write operations.
"""

from __future__ import annotations

import fcntl
import os
import time
from pathlib import Path
from contextlib import contextmanager


@contextmanager
def file_lock(path: Path, timeout: float = 5.0):
    """
    Advisory file lock for safe concurrent writes.
    
    Usage:
        with file_lock(entity_path):
            entity_path.write_text(new_content)
    """
    lock_path = path.with_suffix(path.suffix + '.lock')
    lock_fd = None
    
    try:
        lock_fd = open(lock_path, 'w')
        deadline = time.monotonic() + timeout
        
        while True:
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except (IOError, OSError):
                if time.monotonic() >= deadline:
                    # Timeout — proceed without lock (better than deadlock)
                    break
                time.sleep(0.05)
        
        yield
        
    finally:
        if lock_fd:
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
                lock_fd.close()
                lock_path.unlink(missing_ok=True)
            except:
                pass


def safe_append(path: Path, content: str):
    """Append to a file with locking."""
    with file_lock(path):
        with open(path, 'a') as f:
            f.write(content)


def safe_write(path: Path, content: str):
    """Write to a file atomically (write to temp, rename)."""
    tmp_path = path.with_suffix('.tmp')
    with file_lock(path):
        tmp_path.write_text(content)
        tmp_path.rename(path)
