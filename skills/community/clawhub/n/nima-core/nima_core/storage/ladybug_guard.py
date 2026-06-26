#!/usr/bin/env python3
"""
LadybugDB WAL Auto-Recovery Guard
==================================
Centralised safe-open helper for LadybugDB.

Problem: When the process is killed mid-write, the WAL file can become
corrupted.  LadybugDB then raises RuntimeError on open, which silently
fails memory captures and recall operations.

Solution: Detect WAL corruption on open, rename the bad WAL (preserving it
for post-mortem if needed), and let LadybugDB recover cleanly from the main
data file.

Usage anywhere in nima_core:
    from nima_core.storage.ladybug_guard import ladybug_open_safe, ladybug_health_check

    db, conn = ladybug_open_safe()              # uses default path
    db, conn = ladybug_open_safe('/path/to/db') # custom path
"""

import sys
import time
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

try:
    import real_ladybug as lb
    HAS_LADYBUG = True
except ImportError:
    HAS_LADYBUG = False

DEFAULT_DB_PATH  = Path.home() / ".nima" / "memory" / "ladybug.lbug"
RECOVERY_LOG     = Path.home() / ".nima" / "memory" / "wal_recovery.log"
MAX_RECOVERY_LOG = 50  # keep last N entries


# ── Core open helper ──────────────────────────────────────────────────────────

def ladybug_open_safe(db_path=None, max_retries: int = 2):
    """
    Open LadybugDB with automatic WAL corruption recovery.

    Strategy:
    1. Try normal open
    2. On WAL/corruption RuntimeError, rename the WAL file and retry
    3. After max_retries exhausted, raise so caller knows something is wrong

    Returns:
        (db, conn) tuple — conn already has LOAD VECTOR called if available

    Raises:
        RuntimeError — if DB cannot be opened even after recovery
        ImportError  — if real_ladybug is not installed
    """
    if not HAS_LADYBUG:
        raise ImportError("real_ladybug not installed")

    path     = Path(db_path) if db_path else DEFAULT_DB_PATH
    wal_path = Path(str(path) + '.wal')

    for attempt in range(max_retries):
        try:
            db   = lb.Database(str(path))
            conn = lb.Connection(db)
            try:
                conn.execute("LOAD VECTOR")
            except Exception as e:
                logger.debug("LOAD VECTOR not available (optional): %s", e)
            return db, conn

        except RuntimeError as exc:
            msg = str(exc).lower()
            is_wal_error = any(k in msg for k in ('wal', 'corrupted', 'invalid wal', 'bad wal'))

            if not is_wal_error:
                raise  # unrelated error — don't mask it

            if not wal_path.exists():
                raise RuntimeError(
                    f"LadybugDB WAL error but no WAL file to recover: {exc}"
                ) from exc

            # Rename the bad WAL so LadybugDB can recover from main file
            bak = Path(str(wal_path) + f'.bak_{int(time.time())}')
            wal_path.rename(bak)
            _log_recovery(path, bak, str(exc))
            print(f"⚠️  LadybugDB WAL corrupted — auto-recovered (renamed → {bak.name})", file=sys.stderr)

    raise RuntimeError(f"LadybugDB failed to open after {max_retries} recovery attempts on {path}")


# ── Health check ──────────────────────────────────────────────────────────────

def ladybug_health_check(db_path=None) -> dict:
    """
    Quick health check. Returns a status dict; never raises.

    Result keys:
        healthy (bool)         — DB opened and responded
        node_count (int)       — number of MemoryNode nodes
        wal_present (bool)     — WAL file exists (may or may not be corrupt)
        wal_size_kb (float)    — WAL file size in KB (0 if absent)
        recovered (bool)       — recovery was needed this call
        error (str | None)     — error message if unhealthy
    """
    result = {
        'healthy': False, 'node_count': 0,
        'wal_present': False, 'wal_size_kb': 0.0,
        'recovered': False, 'error': None,
        'checked_at': datetime.utcnow().isoformat(),
    }

    path     = Path(db_path) if db_path else DEFAULT_DB_PATH
    wal_path = Path(str(path) + '.wal')

    result['wal_present'] = wal_path.exists()
    if result['wal_present']:
        result['wal_size_kb'] = round(wal_path.stat().st_size / 1024, 1)

    # Count existing recovery backups as a health signal
    bak_count = len(list(path.parent.glob('*.wal.bak*')))
    result['wal_bak_count'] = bak_count

    try:
        db, conn = ladybug_open_safe(path)
        rows = list(conn.execute("MATCH (n:MemoryNode) RETURN count(n) as c"))
        result['node_count'] = int(rows[0][0]) if rows else 0
        result['healthy']    = True
    except Exception as exc:
        result['error'] = str(exc)

    return result


# ── Recovery log ─────────────────────────────────────────────────────────────

def _log_recovery(db_path: Path, bak_path: Path, error: str):
    """Append an entry to the recovery log (capped at MAX_RECOVERY_LOG entries)."""
    try:
        entries = []
        if RECOVERY_LOG.exists():
            try:
                entries = json.loads(RECOVERY_LOG.read_text())
            except Exception as e:
                logger.debug("Recovery log parse failed (starting fresh): %s", e)
                entries = []

        entries.append({
            'ts':       datetime.utcnow().isoformat(),
            'db':       str(db_path),
            'wal_bak':  str(bak_path),
            'error':    error,
        })
        entries = entries[-MAX_RECOVERY_LOG:]  # keep last N
        RECOVERY_LOG.write_text(json.dumps(entries, indent=2))
    except Exception as e:
        logger.debug("Recovery log write failed (non-fatal): %s", e)


def get_recovery_history(db_path: Optional[str] = None) -> list:
    """Return list of past WAL recovery events.
    
    Args:
        db_path: Optional filter — if provided, only return events for this DB path.
    """
    try:
        entries = json.loads(RECOVERY_LOG.read_text()) if RECOVERY_LOG.exists() else []
        if db_path:
            entries = [e for e in entries if e.get('db') == db_path]
        return entries
    except Exception as e:
        logger.debug("Recovery history read failed: %s", e)
        return []


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='LadybugDB WAL Guard')
    sub = parser.add_subparsers(dest='cmd')
    sub.add_parser('health',   help='Run health check and print result')
    sub.add_parser('history',  help='Show WAL recovery history')
    sub.add_parser('recover',  help='Force-recover WAL right now (rename & reopen)')
    args = parser.parse_args()

    if args.cmd == 'health' or args.cmd is None:
        result = ladybug_health_check()
        status = '✅ HEALTHY' if result['healthy'] else '❌ UNHEALTHY'
        print(f"\n{status} — LadybugDB @ {DEFAULT_DB_PATH}")
        print(f"  Nodes:       {result['node_count']:,}")
        print(f"  WAL present: {result['wal_present']} ({result['wal_size_kb']} KB)")
        print(f"  Past backups:{result['wal_bak_count']}")
        if result['error']:
            print(f"  Error:       {result['error']}")
    elif args.cmd == 'history':
        hist = get_recovery_history()
        if not hist:
            print("No WAL recovery events on record.")
        else:
            print(f"\n📋 WAL Recovery History ({len(hist)} events):")
            for e in hist[-10:]:
                print(f"  {e['ts']}  →  {Path(e['wal_bak']).name}")
                print(f"     Error: {e['error'][:80]}")
    elif args.cmd == 'recover':
        print("Force-recovering WAL...")
        db, conn = ladybug_open_safe()
        rows = list(conn.execute("MATCH (n:MemoryNode) RETURN count(n) as c"))
        print(f"✅ Recovery complete. Nodes: {rows[0][0] if rows else 0}")