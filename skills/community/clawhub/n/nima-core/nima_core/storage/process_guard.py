#!/usr/bin/env python3
"""
LadybugDB Multi-Process Guard
==============================
Prevents database corruption from concurrent gateway processes.

Problem: When multiple OpenClaw gateways run simultaneously, they all
write to ladybug.lbug → file lock conflicts → corruption → crash cycle.

Solution:
1. PID file tracking — only one gateway can run at a time
2. File lock detection — detect active writers before opening DB
3. Graceful cleanup — remove stale PID on exit
4. Zombie process detection — warn about orphaned gateways

Usage in gateway startup:
    from nima_core.storage.process_guard import acquire_gateway_lock, release_gateway_lock
    
    acquire_gateway_lock()  # Exits if another gateway is running
    # ... gateway runs ...
    release_gateway_lock()  # Cleanup on exit
"""

import os
import sys
import signal
import fcntl
import atexit
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# PID file location
PID_DIR = Path.home() / ".nima" / "run"
PID_FILE = PID_DIR / "gateway.pid"
LOCK_FD = None  # File descriptor for lock


# ── PID file management ──────────────────────────────────────────────────────

def _ensure_pid_dir():
    """Ensure PID directory exists."""
    PID_DIR.mkdir(parents=True, exist_ok=True)


def _get_stale_pid() -> Optional[int]:
    """Check if PID file exists and process is still running."""
    if not PID_FILE.exists():
        return None
    
    try:
        pid = int(PID_FILE.read_text().strip())
        # Check if process is running
        os.kill(pid, 0)
        return pid
    except (ValueError, ProcessLookupError, PermissionError):
        # PID file stale or process dead
        return None
    except Exception as e:
        logger.debug("Error reading PID file: %s", e)
        return None


def acquire_gateway_lock():
    """
    Acquire exclusive lock for gateway process.
    
    Checks:
    1. Another gateway already running (exit if so)
    2. Create PID file with our PID
    3. Register cleanup on exit
    
    Raises:
        RuntimeError: If another gateway is already running
    """
    _ensure_pid_dir()
    
    # Check for existing gateway
    existing_pid = _get_stale_pid()
    if existing_pid:
        raise RuntimeError(
            f"Gateway already running (PID {existing_pid}). "
            f"Stop it first: kill {existing_pid} or 'openclaw gateway stop'"
        )
    
    # Write our PID
    PID_FILE.write_text(str(os.getpid()))
    
    # Register cleanup
    atexit.register(release_gateway_lock)
    
    # Handle signals for clean shutdown
    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGQUIT):
        signal.signal(sig, _signal_handler)
    
    logger.info("Gateway lock acquired (PID %d)", os.getpid())


def _signal_handler(signum, frame):
    """Handle termination signals gracefully."""
    logger.info("Gateway received signal %d, cleaning up...", signum)
    release_gateway_lock()
    # MUST exit to prevent second writer
    import sys
    sys.exit(0)


def release_gateway_lock():
    """Release gateway lock and cleanup PID file."""
    global LOCK_FD
    
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
            if pid == os.getpid():
                PID_FILE.unlink()
                logger.info("Gateway lock released")
        except Exception as e:
            logger.error("Error releasing lock: %s", e)
    
    # Reset signal handlers
    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGQUIT):
        signal.signal(sig, signal.SIG_DFL)


# ── File lock detection ──────────────────────────────────────────────────────

def check_db_write_lock(db_path: Path) -> bool:
    """
    Check if DB file is currently write-locked by another process.
    
    Uses fcntl flock to test if file is locked.
    
    Returns:
        True if file is locked (another process writing), False if free
    """
    if not db_path.exists():
        return False
    
    try:
        fd = db_path.open('r+')
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            # Got lock - file is not locked by others
            fcntl.flock(fd, fcntl.LOCK_UN)
            fd.close()
            return False
        except (IOError, OSError):
            # Lock failed - another process has it
            fd.close()
            return True
    except Exception as e:
        logger.debug("Lock check error: %s", e)
        return False  # Assume free on error


# ── Zombie process cleanup ───────────────────────────────────────────────────

def find_zombie_gateways() -> list:
    """
    Find orphaned gateway processes (stale PIDs).
    
    Returns:
        List of zombie PIDs (dead processes with PID files)
    """
    if not PID_FILE.exists():
        return []
    
    try:
        pid = int(PID_FILE.read_text().strip())
        # Check if process is actually running
        try:
            os.kill(pid, 0)
            # Process is running - check if it's actually a gateway
            try:
                cmdline = Path(f"/proc/{pid}/cmdline").read_text().replace('\0', ' ')
                if 'openclaw' in cmdline or 'gateway' in cmdline:
                    return []  # Not a zombie - active gateway
            except Exception as exc:
                logger.debug("Cannot read cmdline for PID %d: %s", pid, exc)
                pass  # Can't read cmdline, treat as potential zombie
            # Running but not a gateway - zombie PID file
            return [pid]
        except (ProcessLookupError, PermissionError):
            # Process dead - definitely a zombie
            return [pid]
    except Exception as exc:
        logger.debug("Error checking zombie gateways: %s", exc)
        return []
    
    return []


def cleanup_zombie_gateways():
    """Remove stale PID file if process is dead."""
    zombies = find_zombie_gateways()
    if zombies:
        logger.info("Found zombie gateway PID file, cleaning up")
        if PID_FILE.exists():
            PID_FILE.unlink()
        return True
    return False


# ── Health check integration ────────────────────────────────────────────────

def process_health() -> dict:
    """
    Check process/gateway health.
    
    Returns:
        Dict with process status info
    """
    return {
        'gateway_running': _get_stale_pid() is not None,
        'gateway_pid': _get_stale_pid(),
        'pid_file_exists': PID_FILE.exists(),
        'zombies': find_zombie_gateways(),
        'current_pid': os.getpid() if not _get_stale_pid() else None,
    }
