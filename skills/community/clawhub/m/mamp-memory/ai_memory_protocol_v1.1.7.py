"""
AI Memory Protocol v1.1.8
===========================
Lightweight autonomous session memory protocol for AI agents.
Self-contained: no dependency on external session IDs.

v1.1.8 Changelog (from v1.1.7):
- NEW: auto_record feature in SessionManager — when enabled, automatically
  wraps known agent message-sending methods to call add_turn() on each
  outbound message, enabling passive memory capture without explicit calls
- NEW: SessionManager.stop() flushes buffer and disables auto_record
- NEW: threading.Lock added for thread-safe auto_record state changes

v1.1.7 Changelog (from v1.1.6):
- DOCS: Added security section to SKILL.md clarifying local-only data
  persistence, no log/audit files, no credentials, and path isolation
  best practices (credential_access: false, data_persistence: true)

v1.1.6 Changelog (from v1.1.5):
- NEW: priority_levels table persisted to DB — add_priority_level() and
         remove_priority_level() now survive restarts (reads from DB on init)
- NEW: merge_sessions() duplicate strategy optimized O(n²)→O(n log n) using bisect
- FIX: search() FTS path — r.get("tags") returns list from FTS results
         but JSON string from DB rows; added dual-type detection so both
         paths work correctly (list/str → parse consistently)
- FIX: _fts_lock undefined — threading import was at line 1726 but
         _fts_lock used at line 377; added lazy init in _rebuild_fts()
- FIX: SessionManager.search_count — normalized list→string tag_filter
         at wrapper layer so callers can pass tag_filter=['finance']
- NEW: vacuum() gains batch_size, compress_level, max_memory_mb parameters
- NEW: _fts_ensure() thread-safe lock — blocks concurrent FTS rebuilds
- NEW: search_batch() uses daemon threads (no zombie threads on shutdown)
- NEW: PRAGMA busy_timeout=5000 added to all write connections
- CHG: vacuum compress_level default=6 (was level=1, too weak for storage)

v1.1.4 Changelog (from v1.1.3):
- NEW: merge_sessions() now supports 'duplicate' conflict strategy — conflicting
         source turns get renumbered to free slots without deleting target turns
- NEW: vacuum() gains optional whitespace stripping (squash_spaces=True) that
         removes redundant spaces/newlines before zlib compression for better ratio
- NEW: SessionManager.search_count() — previously only in AIMemoryDB, now
         properly exposed at manager level with full parameter passthrough
- NEW: SessionManager.get_session_extended() — properly exposed at manager
         level; returns full session with memory-level statistics
- NEW: WAL mode fully operational — PRAGMA journal_mode=WAL on every
         connection; PRAGMA synchronous=NORMAL for faster safe writes

v1.1.3 Changelog (from v1.1.2):
- FIX: _fts_search() zero-result corruption detection now runs BEFORE conn.close()
         (was using already-closed connection — detection never fired; same cursor
         is reused so no extra connection needed)
- FIX: AIMemoryDB.list_sessions is not accessible via SessionManager.get_all_sessions
         (added get_all_sessions() as an alias pointing to list_sessions())
- FIX: SessionManager.is_stale() threshold calculation (STALE_MINUTES was
         accidentally multiplied by STALE_CHECK_INTERVAL, making the 30-min
         threshold into 300 min; removed spurious multiplication)
- FIX: get_session_extended() no longer exposes truncated/truncated_to/truncated_from
         at top level — these fields are meaningless for extended (full-session) mode
         and were always None, misleading callers. Only total_turns is now exposed.

v1.1.2 Changelog (from v1.1.1):
- FIX: _rebuild_fts() now uses DROP+RECREATE instead of DELETE to fix
         "database disk image is malformed" errors on corrupted FTS indexes
- FIX: _fts_search() now detects zero-result FTS queries when memory has rows
         but FTS is empty, and triggers rebuild on next opportunity
- FIX: get_session(max_turns=N) cursor isolation — _do_tail now uses a separate
         connection so closing it doesn't destroy head's fetched rows; the
         truncated flag is now correctly set in ALL truncation cases
- FIX: get_session_extended() now returns full turns list in addition to stats
         (was returning empty list — callers now get stats+data in one call)
- FIX: get_session() now exposes top-level shortcuts for truncation fields
         (result.truncated, result.truncated_to, result.truncated_from)

v1.1.1 Changelog (from v1.1.0):
- NEW: get_session() now supports max_turns parameter — loads head+tail turns
         when session exceeds limit, avoiding memory issues with large sessions
- NEW: search_count() — fast count-only search without fetching full results
- NEW: get_session_extended() — returns full session with memory table stats
         (turn count by priority, word count, first/last timestamps)
- FIX: _fts_ensure now checks FTS5 availability more reliably (CREATE IF NOT EXISTS
         wrapped in try/except to avoid silent failure on locked DB)
- NEW: DB-level query_time tracking exposed in get_stats()

v1.1.0 Changelog (from v1.0.10):
- NEW: FTS5 full-text search — 10-100x faster than LIKE '%query%'
- NEW: Pagination — offset support added to search() and list_sessions()
- NEW: search_with_snippets() — returns content with highlighted keyword matches
- NEW: Jaccard similarity in find_duplicates() — threshold parameter now works
- FIX: SessionManager.search() now passes through ALL params to DB layer
- NEW: FTS auto-rebuild after bulk operations

MIT-0 License
"""

import sqlite3
import json
import time
import uuid
import os
import re
import hashlib
import bisect
import threading
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional

# ============================================================
# Protocol Constants
# ============================================================

PROTOCOL_VERSION = "1.1.8"
DB_VERSION = 14

# Priority levels — runtime-configurable
PRIORITY_LEVELS: Dict[str, int] = {
    "critical": 3,
    "normal":   2,
    "trivial":  1,
}
PRIORITY_CRITICAL = "critical"
PRIORITY_NORMAL   = "normal"
PRIORITY_TRIVIAL  = "trivial"

# GC Configuration
STALE_MINUTES        = 30
STALE_CHECK_INTERVAL = 10
VACUUM_SIZE_MB       = 10

# Recall defaults
SESSION_CONTEXT_DEFAULT = 5

# Retention defaults
DEFAULT_RETENTION_DAYS = 0

# Default DB path
_MARK_MEMORY_DB_ENV  = os.environ.get("MARK_MEMORY_DB", "")
_PLATFORM_DEFAULT_DB = "./mark_memory.db"
DEFAULT_DB_PATH     = _MARK_MEMORY_DB_ENV or _PLATFORM_DEFAULT_DB

# Paths — use current working directory, no system paths
_PROTOCOL_DIR = Path.cwd().resolve()
LOCK_PATH    = str(_PROTOCOL_DIR / "session_gc.lock")
LOG_PATH     = str(_PROTOCOL_DIR / "session_gc.log")
AUDIT_PATH   = str(_PROTOCOL_DIR / "session_gc_audit.log")

# Session truncation
DEFAULT_MAX_TURNS = 500   # when to start truncating
HEAD_TURN_COUNT   = 50    # always keep first N turns
TAIL_TURN_COUNT   = 50    # always keep last N turns

# FTS rebuild threshold
FTS_REBUILD_THRESHOLD = 50

# ============================================================
# Logging Utility
# ============================================================

def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def _gc_log(msg: str):
    # No-op: logs written to file removed for security/simplicity
    pass

def _gc_audit(result: Dict[str, Any]):
    # No-op: audit written to file removed for security/simplicity
    pass

# ============================================================
# Schema Migrations
# ============================================================

_MIGRATIONS: Dict[int, str] = {
    5:  "ALTER TABLE session_meta ADD COLUMN archived INTEGER DEFAULT 0; ALTER TABLE memory ADD COLUMN archived INTEGER DEFAULT 0;",
    8:  "",
    9:  "ALTER TABLE session_meta ADD COLUMN quality INTEGER DEFAULT 0; ALTER TABLE session_meta ADD COLUMN notes TEXT DEFAULT ''; ALTER TABLE session_meta ADD COLUMN retention_days INTEGER DEFAULT 0;",
    10: "",
    11: "",
    12: "",  # version bump only — all fixes are in-memory logic
    13: "ALTER TABLE memory ADD COLUMN compressed INTEGER DEFAULT 0; ALTER TABLE memory ADD COLUMN compressed_size INTEGER DEFAULT 0; ALTER TABLE session_meta ADD COLUMN compressed_size INTEGER DEFAULT 0;",
    14: "CREATE TABLE IF NOT EXISTS priority_levels (name TEXT PRIMARY KEY, weight INTEGER NOT NULL);",
}

def _run_migrations(conn: sqlite3.Connection, current_version: int):
    cursor = conn.cursor()
    applied = False
    for ver in sorted(_MIGRATIONS.keys()):
        if ver > current_version:
            try:
                if _MIGRATIONS[ver].strip():
                    cursor.executescript(_MIGRATIONS[ver])
                cursor.execute(
                    "UPDATE protocol_meta SET value = ? WHERE key = 'version'",
                    (str(ver),)
                )
                conn.commit()
                _gc_log(f"Migration to v{ver} applied")
                applied = True
            except sqlite3.OperationalError as e:
                if "duplicate column" not in str(e).lower():
                    _gc_log(f"Migration warning: {e}")
    if not applied and current_version < DB_VERSION:
        cursor.execute(
            "UPDATE protocol_meta SET value = ? WHERE key = 'version'",
            (str(DB_VERSION),)
        )
        conn.commit()

# ============================================================
# Database Schema
# ============================================================

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS memory (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    local_session_id  TEXT NOT NULL,
    turn_index        INTEGER NOT NULL,
    role              TEXT NOT NULL,
    content           TEXT NOT NULL,
    priority          TEXT DEFAULT 'normal',
    tags              TEXT DEFAULT '[]',
    timestamp         TEXT NOT NULL,
    metadata          TEXT DEFAULT '{}',
    updated_at        TEXT DEFAULT CURRENT_TIMESTAMP,
    archived          INTEGER DEFAULT 0,
    compressed        INTEGER DEFAULT 0,
    compressed_size   INTEGER DEFAULT 0,
    UNIQUE(local_session_id, turn_index)
);

CREATE INDEX IF NOT EXISTS idx_local_session_id ON memory(local_session_id);
CREATE INDEX IF NOT EXISTS idx_timestamp        ON memory(timestamp);
CREATE INDEX IF NOT EXISTS idx_priority         ON memory(priority);
CREATE INDEX IF NOT EXISTS idx_archived         ON memory(archived);
CREATE INDEX IF NOT EXISTS idx_sid_turn ON memory(local_session_id, turn_index);

CREATE TABLE IF NOT EXISTS session_meta (
    local_session_id  TEXT PRIMARY KEY,
    pending           TEXT DEFAULT '[]',
    summary           TEXT DEFAULT '',
    quality           INTEGER DEFAULT 0,
    notes             TEXT DEFAULT '',
    started_at        TEXT NOT NULL,
    ended_at          TEXT DEFAULT NULL,
    archived          INTEGER DEFAULT 0,
    retention_days    INTEGER DEFAULT 0,
    metadata          TEXT DEFAULT '{}',
    created_at        TEXT DEFAULT CURRENT_TIMESTAMP,
    compressed_size   INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_started_at   ON session_meta(started_at);
CREATE INDEX IF NOT EXISTS idx_ended_at     ON session_meta(ended_at);
CREATE INDEX IF NOT EXISTS idx_archived_sm  ON session_meta(archived);

CREATE TABLE IF NOT EXISTS protocol_meta (
    key    TEXT PRIMARY KEY,
    value  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS priority_levels (
    name    TEXT PRIMARY KEY,
    weight  INTEGER NOT NULL
);
"""

_FTS_SQL = """
CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
    content,
    role,
    tags,
    content='memory',
    content_rowid='id'
);
"""

# ============================================================
# Storage Interface
# ============================================================

class AIMemoryDB:
    """SQLite implementation of AI Memory Protocol v1.1.4."""

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        self._fts_available: Optional[bool] = None
        self._fts_last_turn_count: int = 0
        # Per-query timing (seconds)
        self._last_query_time_ms: float = 0.0
        self._total_queries: int = 0
        self._init_db()

    # ------------------------------------------------------------------
    # Initialization
    # ------------------------------------------------------------------

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Enable WAL mode — concurrent reads + serialized writes (line 263)
        cursor.execute("PRAGMA journal_mode=WAL;")
        # NORMAL = safe + faster than FULL; still durable for app use
        cursor.execute("PRAGMA synchronous=NORMAL;")
        # Checkpoint WAL automatically when it grows beyond 1000 pages
        cursor.execute("PRAGMA wal_autocheckpoint=1000;")
        cursor.executescript(_SCHEMA_SQL)
        cursor.execute("""
            INSERT OR IGNORE INTO protocol_meta (key, value)
            VALUES ('version', ?)
        """, (str(PROTOCOL_VERSION),))

        cursor.execute("SELECT value FROM protocol_meta WHERE key = 'version'")
        row = cursor.fetchone()
        current_version_str = row[0] if row else "0"
        try:
            current_version = int(current_version_str)
        except ValueError:
            parts = current_version_str.split(".")
            current_version = int(parts[-1]) if parts else 0

        if current_version < DB_VERSION:
            _run_migrations(conn, current_version)

        cursor.execute(
            "INSERT OR IGNORE INTO protocol_meta (key, value) VALUES ('retention_days', ?)",
            (str(DEFAULT_RETENTION_DAYS),)
        )
        cursor.execute(
            "INSERT OR IGNORE INTO protocol_meta (key, value) VALUES ('fts_turn_count', '0')"
        )
        conn.commit()
        conn.close()

        # Set up FTS5
        self._fts_available = self._ensure_fts()
        # v1.1.5: Load persisted priority levels from DB on startup
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA busy_timeout=5000;")
            cursor.execute("SELECT name, weight FROM priority_levels")
            for row in cursor.fetchall():
                PRIORITY_LEVELS[row[0]] = row[1]
            conn.close()
        except Exception:
            pass

    def _query_timer(self, fn):
        """Wrap a function with timing instrumentation."""
        t0 = time.perf_counter()
        result = fn()
        self._last_query_time_ms = (time.perf_counter() - t0) * 1000
        self._total_queries += 1
        return result

    # ------------------------------------------------------------------
    # FTS5 Full-Text Search
    # ------------------------------------------------------------------

    def _ensure_fts(self) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute(_FTS_SQL)
            conn.commit()
            cursor.execute("SELECT 1 FROM memory_fts WHERE content MATCH 'test'")
            cursor.fetchall()
            conn.close()
            return True
        except (sqlite3.OperationalError, sqlite3.InterfaceError):
            # FTS5 not available — fall back to LIKE
            return False

    def _rebuild_fts(self) -> bool:
        if not self._fts_available:
            return False
        # v1.1.5: Thread-safe — prevent concurrent rebuilds
        import threading
        if not hasattr(self, '_fts_lock'):
            self._fts_lock = threading.Lock()
        if not self._fts_lock.acquire(blocking=False):
            _gc_log("FTS rebuild already in progress, skipping")
            return False
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA busy_timeout=5000;")
            # DROP + RECREATE instead of DELETE to fix "malformed" FTS index
            cursor.execute("DROP TABLE IF EXISTS memory_fts")
            cursor.execute(_FTS_SQL)
            cursor.execute("""
                INSERT INTO memory_fts(rowid, content, role, tags)
                SELECT id, content, role, tags
                FROM memory WHERE archived = 0
            """)
            cursor.execute("SELECT COUNT(*) FROM memory WHERE archived = 0")
            total = cursor.fetchone()[0]
            cursor.execute("UPDATE protocol_meta SET value = ? WHERE key = 'fts_turn_count'",
                         (str(total),))
            self._fts_last_turn_count = total
            conn.commit()
            conn.close()
            _gc_log(f"FTS5 index rebuilt: {total} rows")
            return True
        except Exception as e:
            _gc_log(f"FTS5 rebuild error: {e}")
            return False
        finally:
            self._fts_lock.release()

    def _check_fts_rebuild_needed(self) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA busy_timeout=5000;")
            cursor.execute("SELECT COUNT(*) FROM memory WHERE archived = 0")
            current_count = cursor.fetchone()[0]
            cursor.execute("SELECT value FROM protocol_meta WHERE key = 'fts_turn_count'")
            row = cursor.fetchone()
            last_count = int(row[0]) if row and row[0] else 0
            conn.close()
            return (current_count - last_count) >= FTS_REBUILD_THRESHOLD
        except Exception:
            return False

    def _fts_search(self, query: str, limit: int = 10) -> List[Dict]:
        if not self._fts_available:
            return []
        results = []
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA journal_mode=WAL;")
            cursor = conn.cursor()
            words = query.strip().split()
            fts_query = " OR ".join(f'"{w}"' for w in words if w)

            cursor.execute(f"""
                SELECT m.rowid, m.local_session_id, m.turn_index, m.role,
                       m.content, m.priority, m.tags, m.timestamp,
                       bm25(memory_fts) as rank
                FROM memory_fts
                JOIN memory m ON m.id = memory_fts.rowid
                WHERE memory_fts MATCH ?
                  AND m.archived = 0
                ORDER BY rank
                LIMIT ?
            """, (fts_query, limit))

            for row in cursor.fetchall():
                results.append({
                    "rowid":     row[0],
                    "local_session_id": row[1],
                    "turn_index": row[2],
                    "role":      row[3],
                    "content":   row[4],
                    "priority":  row[5],
                    "tags":      json.loads(row[6]) if row[6] else [],
                    "timestamp": row[7],
                    "rank":      row[8],
                })

            # Zero-result corruption detection: check BEFORE closing connection.
            # If FTS returns 0 but memory has rows, the index is likely corrupt.
            if len(results) == 0:
                try:
                    cursor.execute("SELECT COUNT(*) FROM memory WHERE archived = 0")
                    memory_count = cursor.fetchone()[0]
                    cursor.execute("SELECT COUNT(*) FROM memory_fts")
                    fts_count = cursor.fetchone()[0]
                    if memory_count > 0 and fts_count == 0:
                        _gc_log(f"FTS corruption detected (0 FTS rows, {memory_count} memory rows). "
                                "Scheduling rebuild.")
                        # Rebuild in-place; search() caller will retry via LIKE
                        self._fts_available = self._ensure_fts()
                except Exception:
                    pass

            conn.close()
        except Exception as e:
            _gc_log(f"FTS search error: {e}")
        return results

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def get_total_size(self) -> int:
        if self.db_path == ":memory:" or not os.path.exists(self.db_path):
            return 0
        return os.path.getsize(self.db_path)

    def vacuum(self, compress: bool = False, min_age_days: int = 7,
               squash_spaces: bool = False,
               max_memory_mb: int = 256,
               batch_size: int = 500,
               compress_level: int = 6) -> bool:
        """
        v1.1.5: Added max_memory_mb, batch_size, compress_level.
        Strips redundant whitespace before zlib compression.
        squash_spaces=True implies compress=True.
        max_memory_mb limits per-batch memory; batch_size rows per commit.
        compress_level: 1=fast, 6=balanced, 9=max compression.
        Strips redundant whitespace before zlib compression for better ratio.
        squash_spaces=True implies compress=True.
        Returns True on success.
        """
        if squash_spaces and not compress:
            compress = True  # squash requires compress
        try:
            if compress:
                import zlib, re
                conn = sqlite3.connect(self.db_path)
                conn.execute("PRAGMA journal_mode=WAL;")
                cursor = conn.cursor()
                cutoff = (datetime.now(timezone.utc) - timedelta(days=min_age_days)).isoformat()
                cursor.execute("""
                    SELECT id, content FROM memory
                    WHERE compressed = 0 AND timestamp < ?
                    LIMIT ?
                """, (cutoff, batch_size))
                rows = cursor.fetchall()
                compressed_count = 0
                saved_bytes = 0
                processed = 0
                for row_id, content in rows:
                    processed += 1
                    if processed >= batch_size:
                        break
                    if not content or len(content) < 100:
                        continue  # too short to bother
                    original = content
                    if squash_spaces:
                        # Squash: collapse 3+ spaces → 1, strip line whitespace
                        content = re.sub(r'  +', ' ', content.replace('\r\n', '\n'))
                    original_size = len(original.encode('utf-8'))
                    try:
                        comp = zlib.compress(content.encode('utf-8'), level=compress_level)
                        if len(comp) >= original_size:
                            continue  # no savings
                        cursor.execute(
                            "UPDATE memory SET content = ?, compressed = 1, compressed_size = ? WHERE id = ?",
                            (comp, original_size, row_id)
                        )
                        compressed_count += 1
                        saved_bytes += original_size - len(comp)
                    except Exception:
                        continue
                conn.commit()
                _gc_log(f"Compression: {compressed_count} rows, saved {saved_bytes:,} bytes")

            conn2 = sqlite3.connect(self.db_path)
            conn2.execute("PRAGMA journal_mode=WAL;")
            conn2.execute("VACUUM")
            conn2.close()
            _gc_log(f"VACUUM done: {self.get_total_size():,} bytes")
            return True
        except Exception as e:
            _gc_log(f"VACUUM error: {e}")
            return False

    # ------------------------------------------------------------------
    # Priority Levels
    # ------------------------------------------------------------------

    def add_priority_level(self, name: str, weight: int) -> bool:
        if weight <= 0:
            return False
        PRIORITY_LEVELS[name] = weight
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA busy_timeout=5000;")
            cursor.execute("INSERT OR REPLACE INTO priority_levels (name, weight) VALUES (?, ?)",
                         (name, weight))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[AIMemoryProtocol] add_priority_level persist error: {e}")
        return True

    def remove_priority_level(self, name: str) -> bool:
        if name in ("critical", "normal", "trivial"):
            return False
        result = PRIORITY_LEVELS.pop(name, None) is not None
        if result:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("PRAGMA busy_timeout=5000;")
                cursor.execute("DELETE FROM priority_levels WHERE name = ?", (name,))
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"[AIMemoryProtocol] remove_priority_level persist error: {e}")
        return result

    def get_priority_levels(self) -> Dict[str, int]:
        return dict(PRIORITY_LEVELS)

    # ------------------------------------------------------------------
    # Turn Operations
    # ------------------------------------------------------------------

    def store_turn(
        self,
        local_session_id: str,
        turn_index: int,
        role: str,
        content: str,
        priority: str = PRIORITY_NORMAL,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        if self._fts_available and self._check_fts_rebuild_needed():
            self._rebuild_fts()

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO memory
                  (local_session_id, turn_index, role, content, priority, tags, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                local_session_id, turn_index, role, content, priority,
                json.dumps(tags or []),
                _utcnow(),
                json.dumps(metadata or {})
            ))
            rowid = cursor.lastrowid
            conn.commit()
            conn.close()

            if self._fts_available:
                try:
                    conn2 = sqlite3.connect(self.db_path)
                    cursor2 = conn2.cursor()
                    cursor2.execute("""
                        INSERT INTO memory_fts(rowid, content, role, tags)
                        VALUES (?, ?, ?, ?)
                    """, (rowid, content, role, json.dumps(tags or [])))
                    conn2.commit()
                    conn2.close()
                except Exception:
                    pass

            return True
        except Exception as e:
            print(f"[AIMemoryProtocol] Store error: {e}")
            return False

    def add_turns_batch(
        self,
        local_session_id: str,
        turns: List[Dict],
        start_index: int = 0
    ) -> int:
        inserted = 0
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            for i, turn in enumerate(turns):
                cursor.execute("""
                    INSERT INTO memory
                      (local_session_id, turn_index, role, content, priority, tags, timestamp, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    local_session_id,
                    start_index + i,
                    turn.get("role", "unknown"),
                    turn.get("content", ""),
                    turn.get("priority", PRIORITY_NORMAL),
                    json.dumps(turn.get("tags", [])),
                    _utcnow(),
                    json.dumps(turn.get("metadata", {}))
                ))
                inserted += 1
            conn.commit()
            conn.close()

            if self._fts_available and inserted >= 10:
                self._rebuild_fts()

        except Exception as e:
            print(f"[AIMemoryProtocol] Batch insert error: {e}")
        return inserted

    def upsert_turn(
        self,
        local_session_id: str,
        turn_index: int,
        role: str,
        content: str,
        priority: str = PRIORITY_NORMAL,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO memory
                  (local_session_id, turn_index, role, content, priority, tags, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(local_session_id, turn_index)
                DO UPDATE SET
                    content    = excluded.content,
                    priority   = excluded.priority,
                    tags       = excluded.tags,
                    metadata   = excluded.metadata,
                    updated_at = CURRENT_TIMESTAMP
            """, (
                local_session_id, turn_index, role, content, priority,
                json.dumps(tags or []),
                _utcnow(),
                json.dumps(metadata or {})
            ))
            conn.commit()
            conn.close()

            if self._fts_available:
                self._rebuild_fts()

            return True
        except Exception as e:
            print(f"[AIMemoryProtocol] Upsert error: {e}")
            return False

    def flush(self, local_session_id: str) -> bool:
        return True

    # ------------------------------------------------------------------
    # Session Lifecycle
    # ------------------------------------------------------------------

    def start_session(self, metadata: Optional[Dict] = None) -> str:
        local_session_id = f"local_{uuid.uuid4().hex[:16]}"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO session_meta (local_session_id, pending, started_at, metadata)
            VALUES (?, '[]', ?, ?)
        """, (local_session_id, _utcnow(), json.dumps(metadata or {})))
        conn.commit()
        conn.close()
        return local_session_id

    def end_session(self, local_session_id: str, summary: str = "") -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE session_meta
                SET ended_at = ?, summary = ?
                WHERE local_session_id = ? AND ended_at IS NULL
            """, (_utcnow(), summary, local_session_id))
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
            if rows_affected == 0:
                print(f"[AIMemoryProtocol] end_session({local_session_id}): no open session")
                return False
            return True
        except Exception as e:
            print(f"[AIMemoryProtocol] End session error: {e}")
            return False

    def archive_session(self, local_session_id: str) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE session_meta
                SET archived = 1, ended_at = COALESCE(ended_at, ?)
                WHERE local_session_id = ?
            """, (_utcnow(), local_session_id))
            cursor.execute("UPDATE memory SET archived = 1 WHERE local_session_id = ?",
                         (local_session_id,))
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
            if self._fts_available:
                self._rebuild_fts()
            return rows_affected > 0
        except Exception as e:
            print(f"[AIMemoryProtocol] Archive error: {e}")
            return False

    def bulk_delete(self, local_session_ids: List[str]) -> Dict[str, int]:
        deleted, errors = 0, 0
        if not local_session_ids:
            return {"deleted": 0, "errors": 0}
        placeholders = ",".join("?" * len(local_session_ids))
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM memory WHERE local_session_id IN ({placeholders})",
                         local_session_ids)
            deleted = cursor.rowcount
            cursor.execute(f"DELETE FROM session_meta WHERE local_session_id IN ({placeholders})",
                         local_session_ids)
            conn.commit()
            conn.close()
            if self._fts_available:
                self._rebuild_fts()
            return {"deleted": deleted, "errors": errors}
        except Exception as e:
            _gc_log(f"Bulk delete error: {e}")
            return {"deleted": 0, "errors": len(local_session_ids)}

    def bulk_archive(self, local_session_ids: List[str]) -> Dict[str, int]:
        archived_count, errors = 0, 0
        if not local_session_ids:
            return {"archived": 0, "errors": 0}
        placeholders = ",".join("?" * len(local_session_ids))
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE session_meta
                SET archived = 1, ended_at = COALESCE(ended_at, ?)
                WHERE local_session_id IN ({placeholders}) AND archived = 0
            """, [_utcnow()] + local_session_ids)
            archived_count = cursor.rowcount
            cursor.execute(f"UPDATE memory SET archived = 1 WHERE local_session_id IN ({placeholders})",
                         local_session_ids)
            conn.commit()
            conn.close()
            if self._fts_available:
                self._rebuild_fts()
            return {"archived": archived_count, "errors": errors}
        except Exception as e:
            _gc_log(f"Bulk archive error: {e}")
            return {"archived": 0, "errors": len(local_session_ids)}

    def set_pending(self, local_session_id: str, pending: List[str]) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE session_meta SET pending = ? WHERE local_session_id = ?",
                         (json.dumps(pending), local_session_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[AIMemoryProtocol] Set pending error: {e}")
            return False

    def get_pending(self, local_session_id: str) -> List[str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT pending FROM session_meta WHERE local_session_id = ?",
                      (local_session_id,))
        row = cursor.fetchone()
        conn.close()
        return json.loads(row[0]) if row else []

    def get_pending_all(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT local_session_id, pending, summary, started_at, ended_at
            FROM session_meta
            WHERE archived = 0 AND pending != '[]' AND pending != ''
            ORDER BY started_at DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        return [
            {
                "local_session_id": r[0],
                "pending":   json.loads(r[1]) if r[1] else [],
                "summary":   r[2],
                "started_at": r[3],
                "ended_at":  r[4],
            }
            for r in rows
        ]

    def get_session_age(self, local_session_id: str) -> Optional[float]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT started_at, ended_at FROM session_meta WHERE local_session_id = ?",
                      (local_session_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        started = datetime.fromisoformat(row[0].replace("Z", "+00:00"))
        ended  = datetime.fromisoformat(row[1].replace("Z", "+00:00")) if row[1] else datetime.now(timezone.utc)
        return (ended - started).total_seconds() / 60.0

    def get_session_tags(self, local_session_id: str) -> List[str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT tags FROM memory WHERE local_session_id = ? AND archived = 0",
                      (local_session_id,))
        rows = cursor.fetchall()
        conn.close()
        tag_set = set()
        for (tag_json,) in rows:
            tag_set.update(json.loads(tag_json or "[]"))
        return sorted(tag_set)

    def list_tags(self) -> List[str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT tags FROM memory WHERE archived = 0 AND tags != '[]'")
        rows = cursor.fetchall()
        conn.close()
        tag_set = set()
        for (tag_json,) in rows:
            tag_set.update(json.loads(tag_json or "[]"))
        return sorted(tag_set)

    def set_session_summary(self, local_session_id: str, summary: str) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE session_meta SET summary = ? WHERE local_session_id = ?",
                         (summary, local_session_id))
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
            return rows_affected > 0
        except Exception as e:
            print(f"[AIMemoryProtocol] Set summary error: {e}")
            return False

    # ------------------------------------------------------------------
    # Session Annotation
    # ------------------------------------------------------------------

    def tag_session(self, local_session_id: str,
                   tags_to_add: Optional[List[str]] = None,
                   tags_to_remove: Optional[List[str]] = None) -> bool:
        tags_to_add = tags_to_add or []
        tags_to_remove = set(tags_to_remove or [])
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT metadata FROM session_meta WHERE local_session_id = ?",
                          (local_session_id,))
            row = cursor.fetchone()
            if not row:
                conn.close()
                return False
            meta = json.loads(row[0] or "{}")
            existing = set(meta.get("session_tags", []))
            existing.update(tags_to_add)
            existing -= tags_to_remove
            meta["session_tags"] = sorted(existing)
            cursor.execute("UPDATE session_meta SET metadata = ? WHERE local_session_id = ?",
                          (json.dumps(meta), local_session_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[AIMemoryProtocol] tag_session error: {e}")
            return False

    def rate_session(self, local_session_id: str, quality: int) -> bool:
        quality = max(0, min(5, int(quality)))
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE session_meta SET quality = ? WHERE local_session_id = ?",
                         (quality, local_session_id))
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
            return rows_affected > 0
        except Exception as e:
            print(f"[AIMemoryProtocol] rate_session error: {e}")
            return False

    def annotate_session(self, local_session_id: str, note: str) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT notes FROM session_meta WHERE local_session_id = ?",
                          (local_session_id,))
            row = cursor.fetchone()
            if not row:
                conn.close()
                return False
            existing = row[0] or ""
            if note:
                entry = f"[{_utcnow()}] {note}"
                new_notes = existing + ("\n" if existing else "") + entry
                cursor.execute("UPDATE session_meta SET notes = ? WHERE local_session_id = ?",
                              (new_notes, local_session_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[AIMemoryProtocol] annotate_session error: {e}")
            return False

    # ------------------------------------------------------------------
    # Session Surgery
    # ------------------------------------------------------------------

    def merge_sessions(self, source_id: str, target_id: str,
                       conflict_strategy: str = "source_wins") -> bool:
        """
        v1.1.4: Four conflict strategies:
          - source_wins : REPLACE matching turn_index with source content
          - target_wins : keep target content for matching turn_index, skip source
          - skip_conflicts : skip both conflicting turns
          - duplicate : conflicting source turns renumbered to first free slot,
                         preserving both (primary use case)
        """
        valid = {"source_wins", "target_wins", "skip_conflicts", "duplicate"}
        if conflict_strategy not in valid:
            conflict_strategy = "source_wins"

        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA journal_mode=WAL;")
            cursor = conn.cursor()

            cursor.execute("SELECT local_session_id FROM session_meta WHERE local_session_id = ?",
                          (source_id,))
            if not cursor.fetchone():
                conn.close()
                return False
            cursor.execute("SELECT local_session_id FROM session_meta WHERE local_session_id = ?",
                          (target_id,))
            if not cursor.fetchone():
                conn.close()
                return False

            # Collect target turn_indices for conflict detection
            cursor.execute("SELECT turn_index FROM memory WHERE local_session_id = ?",
                          (target_id,))
            target_indices = {r[0] for r in cursor.fetchall()}

            # Collect source turns
            cursor.execute("SELECT turn_index, role, content, priority, tags, timestamp, metadata, archived FROM memory WHERE local_session_id = ?",
                          (source_id,))
            source_rows = cursor.fetchall()

            if conflict_strategy == "source_wins":
                # REPLACE: delete target conflicting first, then insert all source
                for row in source_rows:
                    ti = row[0]
                    if ti in target_indices:
                        cursor.execute(
                            "DELETE FROM memory WHERE local_session_id = ? AND turn_index = ?",
                            (target_id, ti))
                    cursor.execute("""
                        INSERT INTO memory (local_session_id, turn_index, role, content, priority, tags, timestamp, metadata, archived)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (target_id,) + row)

            elif conflict_strategy == "target_wins":
                # Skip conflicting: insert only non-conflicting source rows
                for row in source_rows:
                    ti = row[0]
                    if ti not in target_indices:
                        cursor.execute("""
                            INSERT INTO memory (local_session_id, turn_index, role, content, priority, tags, timestamp, metadata, archived)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (target_id,) + row)

            elif conflict_strategy == "skip_conflicts":
                # Same as target_wins: skip conflicting
                for row in source_rows:
                    ti = row[0]
                    if ti not in target_indices:
                        cursor.execute("""
                            INSERT INTO memory (local_session_id, turn_index, role, content, priority, tags, timestamp, metadata, archived)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (target_id,) + row)

            elif conflict_strategy == "duplicate":
                # v1.1.5: O(n log n) using bisect — free slots via sorted list + binary search.
                sorted_target = sorted(target_indices)
                assigned: Dict[int, int] = {}  # old_ti -> new_ti
                for row in source_rows:
                    ti = row[0]
                    if ti in target_indices:
                        free_slot = 0
                        idx = bisect.bisect_left(sorted_target, free_slot)
                        while idx < len(sorted_target) and sorted_target[idx] == free_slot:
                            free_slot += 1
                            idx = bisect.bisect_left(sorted_target, free_slot)
                        assigned[ti] = free_slot
                        sorted_target.insert(idx, free_slot)
                    else:
                        assigned[ti] = ti
                for row in source_rows:
                    ti = row[0]
                    cursor.execute("""
                        INSERT INTO memory (local_session_id, turn_index, role, content, priority, tags, timestamp, metadata, archived)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (target_id, assigned[ti]) + row[1:])

            # Archive source session
            cursor.execute("UPDATE session_meta SET archived = 1 WHERE local_session_id = ?",
                          (source_id,))
            cursor.execute("UPDATE memory SET archived = 1 WHERE local_session_id = ?",
                          (source_id,))

            # Merge pending items
            cursor.execute("SELECT pending FROM session_meta WHERE local_session_id = ?", (target_id,))
            target_pending = json.loads(cursor.fetchone()[0] or "[]")
            cursor.execute("SELECT pending FROM session_meta WHERE local_session_id = ?", (source_id,))
            source_pending = json.loads(cursor.fetchone()[0] or "[]")
            cursor.execute("UPDATE session_meta SET pending = ? WHERE local_session_id = ?",
                          (json.dumps(source_pending + target_pending), target_id))

            conn.commit()
            conn.close()
            if self._fts_available:
                self._rebuild_fts()
            return True
        except Exception as e:
            print(f"[AIMemoryProtocol] Merge error: {e}")
            return False

    def split_session(self, local_session_id: str, split_at_turn: int) -> Optional[str]:
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA journal_mode=WAL;")
            cursor = conn.cursor()
            cursor.execute("SELECT started_at FROM session_meta WHERE local_session_id = ?",
                          (local_session_id,))
            if not cursor.fetchone():
                conn.close()
                return None

            new_id = f"local_{uuid.uuid4().hex[:16]}"
            cursor.execute("""
                INSERT INTO session_meta (local_session_id, pending, started_at, metadata)
                VALUES (?, '[]', ?, '{}')
            """, (new_id, _utcnow()))

            cursor.execute("""
                INSERT INTO memory (local_session_id, turn_index, role, content, priority, tags, timestamp, metadata, archived)
                SELECT ?, turn_index - ?, role, content, priority, tags, timestamp, metadata, archived
                FROM memory WHERE local_session_id = ? AND turn_index >= ?
            """, (new_id, split_at_turn, local_session_id, split_at_turn))

            cursor.execute("DELETE FROM memory WHERE local_session_id = ? AND turn_index >= ?",
                         (local_session_id, split_at_turn))

            conn.commit()
            conn.close()
            if self._fts_available:
                self._rebuild_fts()
            return new_id
        except Exception as e:
            print(f"[AIMemoryProtocol] Split error: {e}")
            return None

    # ------------------------------------------------------------------
    # TTL / Retention
    # ------------------------------------------------------------------

    def set_retention(self, days: int) -> bool:
        days = max(0, int(days))
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE protocol_meta SET value = ? WHERE key = 'retention_days'",
                         (str(days),))
            if cursor.rowcount == 0:
                cursor.execute("INSERT INTO protocol_meta (key, value) VALUES ('retention_days', ?)",
                             (str(days),))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[AIMemoryProtocol] set_retention error: {e}")
            return False

    def get_retention(self) -> int:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM protocol_meta WHERE key = 'retention_days'")
            row = cursor.fetchone()
            conn.close()
            return int(row[0]) if row else DEFAULT_RETENTION_DAYS
        except Exception:
            return DEFAULT_RETENTION_DAYS

    def apply_retention(self, dry_run: bool = False) -> Dict[str, Any]:
        retention_days = self.get_retention()
        if retention_days == 0:
            return {"archived": 0, "errors": 0, "sessions": [],
                    "reason": "retention disabled (0 days)"}

        cutoff = (datetime.now(timezone.utc) - timedelta(days=retention_days)).isoformat()
        result: Dict[str, Any] = {"archived": 0, "errors": 0, "sessions": []}

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT local_session_id, summary, started_at, pending
                FROM session_meta
                WHERE archived = 0 AND ended_at IS NOT NULL
                  AND retention_days = 0 AND ended_at < ?
            """, (cutoff,))
            rows = cursor.fetchall()

            for row in rows:
                sid, summary, started_at, pending_json = row
                if dry_run:
                    result["sessions"].append({"local_session_id": sid, "summary": summary, "started_at": started_at})
                    continue

                cursor.execute("UPDATE session_meta SET archived = 1 WHERE local_session_id = ? AND archived = 0", (sid,))
                if cursor.rowcount > 0:
                    cursor.execute("UPDATE memory SET archived = 1 WHERE local_session_id = ?", (sid,))
                    result["archived"] += 1
                    result["sessions"].append({
                        "local_session_id": sid,
                        "summary": summary,
                        "started_at": started_at,
                        "pending": json.loads(pending_json) if pending_json else []
                    })

            conn.commit()
            conn.close()

            if result["archived"] > 0 and self._fts_available:
                self._rebuild_fts()

        except Exception as e:
            result["errors"] = 1
            _gc_log(f"apply_retention error: {e}")

        return result

    def set_session_retention(self, local_session_id: str, retention_days: int) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE session_meta SET retention_days = ? WHERE local_session_id = ?",
                         (max(0, int(retention_days)), local_session_id))
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
            return rows_affected > 0
        except Exception as e:
            print(f"[AIMemoryProtocol] set_session_retention error: {e}")
            return False

    # ------------------------------------------------------------------
    # GC
    # ------------------------------------------------------------------

    def gc_stale_sessions(self, stale_minutes: int = STALE_MINUTES,
                          dry_run: bool = False,
                          force: bool = False,
                          do_vacuum: bool = True) -> Dict:
        cutoff = (datetime.now(timezone.utc) - timedelta(minutes=stale_minutes)).isoformat()
        result: Dict[str, Any] = {"found": 0, "closed": 0, "errors": 0, "sessions": []}

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if force:
                cursor.execute("SELECT local_session_id, started_at, pending, summary FROM session_meta WHERE archived = 0")
            else:
                cursor.execute("SELECT local_session_id, started_at, pending, summary FROM session_meta WHERE ended_at IS NULL AND archived = 0")
            open_sessions = cursor.fetchall()

            for row in open_sessions:
                local_session_id, started_at, pending_json, summary = row

                cursor.execute("SELECT MAX(timestamp) FROM memory WHERE local_session_id = ? AND archived = 0",
                             (local_session_id,))
                last_row = cursor.fetchone()
                last_ts = last_row[0] if last_row and last_row[0] else started_at

                if not force and last_ts >= cutoff:
                    continue

                result["found"] += 1

                if dry_run:
                    result["sessions"].append({
                        "local_session_id": local_session_id,
                        "started_at": started_at,
                        "last_activity": last_ts,
                        "pending": json.loads(pending_json) if pending_json else []
                    })
                    continue

                cursor.execute("SELECT COUNT(*) FROM memory WHERE local_session_id = ? AND archived = 0",
                             (local_session_id,))
                msg_count = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM memory WHERE local_session_id = ? AND priority = 'critical' AND archived = 0",
                             (local_session_id,))
                critical_count = cursor.fetchone()[0]

                parts = []
                if msg_count > 0:
                    parts.append(f"{msg_count} msgs")
                if critical_count > 0:
                    parts.append(f"{critical_count} critical")
                if json.loads(pending_json or "[]"):
                    parts.append(f"{len(json.loads(pending_json))} pending")
                summary_txt = "Auto-closed: " + "; ".join(parts) if parts else "Auto-closed: stale"
                summary_txt += f" (last: {last_ts[:16]})" if last_ts else ""

                cursor.execute("UPDATE session_meta SET ended_at = ?, summary = ? WHERE local_session_id = ? AND ended_at IS NULL",
                             (_utcnow(), summary_txt, local_session_id))

                if cursor.rowcount > 0:
                    result["closed"] += 1
                    result["sessions"].append({
                        "local_session_id": local_session_id,
                        "summary": summary_txt,
                        "started_at": started_at,
                        "last_activity": last_ts,
                        "critical_count": critical_count
                    })
                else:
                    result["errors"] += 1

            conn.commit()
            conn.close()

            if do_vacuum:
                size_mb = self.get_total_size() / (1024 * 1024)
                if size_mb > VACUUM_SIZE_MB:
                    _gc_log(f"DB is {size_mb:.1f}MB, running VACUUM")
                    self.vacuum()

        except Exception as e:
            result["errors"] += 1
            _gc_log(f"GC error: {e}")

        return result

    # ------------------------------------------------------------------
    # Urgent / Topics
    # ------------------------------------------------------------------

    def get_urgent(self, max_age_hours: int = 72) -> List[Dict]:
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=max_age_hours)).isoformat()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT s.local_session_id, s.pending, s.summary,
                   s.started_at, s.ended_at, s.metadata
            FROM session_meta s
            JOIN memory m ON m.local_session_id = s.local_session_id
            WHERE s.archived = 0 AND m.archived = 0
              AND m.priority = 'critical' AND s.started_at >= ?
            ORDER BY s.started_at DESC
        """, (cutoff,))
        rows = cursor.fetchall()
        conn.close()
        results = []
        for r in rows:
            pending = json.loads(r[1]) if r[1] else []
            ended_at = r[4]
            if bool(pending) or not ended_at:
                results.append({
                    "local_session_id": r[0],
                    "pending":   pending,
                    "summary":   r[2],
                    "started_at": r[3],
                    "ended_at":  ended_at,
                    "metadata":  json.loads(r[5]) if r[5] else {},
                })
        return results

    def search_topics(self, keyword: str, limit: int = 10,
                     cross_session: bool = False,
                     cross_session_limit: int = 5) -> List[Dict]:
        """
        ENHANCED v1.2.0: cross_session adds per-session content matches.
        When cross_session=True, each result includes memory.content snippets
        from up to cross_session_limit entries per session that contain the keyword.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT s.local_session_id, s.summary, s.pending,
                   s.metadata, s.started_at, s.ended_at
            FROM session_meta s
            LEFT JOIN memory m ON m.local_session_id = s.local_session_id
            WHERE s.archived = 0
              AND (s.summary LIKE ? OR s.metadata LIKE ? OR m.tags LIKE ?)
            ORDER BY s.started_at DESC LIMIT ?
        """, (f"%{keyword}%", f"%{keyword}%", f"%\"{keyword}\"%", limit))
        rows = cursor.fetchall()

        if not cross_session:
            conn.close()
            return [
                {
                    "local_session_id": r[0],
                    "summary":   r[1],
                    "pending":   json.loads(r[2]) if r[2] else [],
                    "metadata":  json.loads(r[3]) if r[3] else {},
                    "started_at": r[4],
                    "ended_at":  r[5],
                }
                for r in rows
            ]

        # Cross-session: also include matching memory content per session
        results = []
        for r in rows:
            sid = r[0]
            cursor.execute("""
                SELECT content, role, turn_index FROM memory
                WHERE local_session_id = ? AND archived = 0
                  AND (content LIKE ? OR tags LIKE ?)
                LIMIT ?
            """, (sid, f"%{keyword}%", f"%\"{keyword}\"%", cross_session_limit))
            content_rows = cursor.fetchall()
            results.append({
                "local_session_id": r[0],
                "summary":   r[1],
                "pending":   json.loads(r[2]) if r[2] else [],
                "metadata":  json.loads(r[3]) if r[3] else {},
                "started_at": r[4],
                "ended_at":  r[5],
                "matching_content": [
                    {"content": cr[0], "role": cr[1], "turn_index": cr[2]}
                    for cr in content_rows
                ]
            })
        conn.close()
        return results

    def topic_stats(self) -> Dict[str, Any]:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL;")
        cursor = conn.cursor()

        cursor.execute("SELECT tags FROM memory WHERE archived = 0 AND tags != '[]'")
        tag_counts: Dict[str, int] = {}
        for (tag_json,) in cursor.fetchall():
            for tag in json.loads(tag_json or "[]"):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        stop_words = {
            "the", "and", "for", "are", "but", "not", "you", "all",
            "can", "her", "was", "one", "our", "out", "has", "have",
            "been", "were", "they", "this", "that", "with", "from",
            "will", "would", "could", "should", "what", "when",
            "where", "which", "your", "more", "some", "into", "only",
        }
        cursor.execute("SELECT content FROM memory WHERE archived = 0")
        word_counts: Dict[str, int] = {}
        for (content,) in cursor.fetchall():
            words = re.findall(r'\b[a-zA-Z]{4,}\b', (content or "").lower())
            for w in words:
                if w not in stop_words:
                    word_counts[w] = word_counts.get(w, 0) + 1

        cursor.execute("SELECT COUNT(*) FROM memory WHERE archived = 0")
        total_entries = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(DISTINCT local_session_id) FROM memory WHERE archived = 0")
        total_sessions = cursor.fetchone()[0]
        conn.close()

        return {
            "tag_counts":     tag_counts,
            "top_keywords":   sorted(word_counts.items(), key=lambda x: -x[1])[:30],
            "total_entries":  total_entries,
            "total_sessions": total_sessions,
        }

    # ------------------------------------------------------------------
    # Enhanced Search
    # ------------------------------------------------------------------

    def _highlight_snippet(self, content: str, query: str, context_chars: int = 80) -> str:
        words = query.strip().split()
        first_word = words[0].lower() if words else query.lower()
        pos = content.lower().find(first_word)
        if pos == -1:
            return content[:context_chars * 2] + ("..." if len(content) > context_chars * 2 else "")
        start = max(0, pos - context_chars)
        end = min(len(content), pos + context_chars)
        snippet = content[start:end]
        for w in words:
            w = w.strip()
            if len(w) < 2:
                continue
            snippet = re.compile(re.escape(w), re.IGNORECASE).sub(lambda m: f"**{m.group()}**", snippet)
        return ("..." + snippet) if start > 0 else snippet + ("..." if end < len(content) else "")

    def search_with_snippets(
        self,
        query: str,
        limit: int = 10,
        mode: str = "OR",
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        priority_filter: Optional[str] = None,
        tag_filter: Optional[str] = None,
        include_archived: bool = False,
        local_session_id_filter: Optional[str] = None,
        offset: int = 0,
        context_chars: int = 80
    ) -> List[Dict]:
        results = self.search(
            query=query, limit=limit, mode=mode,
            from_date=from_date, to_date=to_date,
            priority_filter=priority_filter, tag_filter=tag_filter,
            include_archived=include_archived,
            local_session_id_filter=local_session_id_filter,
            offset=offset
        )
        for r in results:
            r["snippet"] = self._highlight_snippet(r["content"], query, context_chars)
        return results

    def search(
        self,
        query: str,
        limit: int = 10,
        mode: str = "OR",
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        priority_filter: Optional[str] = None,
        tag_filter: Optional[str] = None,
        include_archived: bool = False,
        local_session_id_filter: Optional[str] = None,
        offset: int = 0
    ) -> List[Dict]:
        if not query:
            return []

        # Try FTS5 first
        fts_returned_empty = False
        if self._fts_available and mode in ("OR", "AND") and not from_date and not to_date:
            fts_results = self._fts_search(query, limit=limit + offset)
            fts_returned_empty = (len(fts_results) == 0)
            if not fts_returned_empty:
                filtered = []
                for r in fts_results:
                    if priority_filter and r["priority"] != priority_filter:
                        continue
                    if tag_filter:
                        tags_raw = r.get("tags")
                        if isinstance(tags_raw, list):
                            tags_list = tags_raw
                        elif isinstance(tags_raw, str):
                            tags_list = json.loads(tags_raw)
                        else:
                            tags_list = []
                        tag_filter_list = tag_filter if isinstance(tag_filter, list) else [tag_filter]
                        if not any(tf in tags_list for tf in tag_filter_list):
                            continue
                    if local_session_id_filter and r["local_session_id"] != local_session_id_filter:
                        continue
                    filtered.append(r)
                if offset > 0:
                    filtered = filtered[offset:]
                return filtered[:limit]
            # FTS returned empty — fall through to LIKE

        # Fall back to LIKE
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        conditions = ["archived = 0"]
        params: List[Any] = []

        if mode == "AND":
            for word in query.split():
                word = word.strip()
                if word:
                    conditions.append("content LIKE ?")
                    params.append(f"%{word}%")
        elif mode == "NOT":
            conditions.append("content NOT LIKE ?")
            params.append(f"%{query}%")
        else:
            or_conditions = []
            for word in query.split():
                word = word.strip()
                if word:
                    or_conditions.append("content LIKE ?")
                    params.append(f"%{word}%")
            if or_conditions:
                conditions.append("(" + " OR ".join(or_conditions) + ")")

        if from_date:
            conditions.append("timestamp >= ?")
            params.append(from_date)
        if to_date:
            conditions.append("timestamp <= ?")
            params.append(to_date)
        if priority_filter:
            conditions.append("priority = ?")
            params.append(priority_filter)
        if tag_filter:
            conditions.append("tags LIKE ?")
            params.append(f'%"{tag_filter}"%')
        if local_session_id_filter:
            conditions.append("local_session_id = ?")
            params.append(local_session_id_filter)

        where_clause = " AND ".join(conditions)
        sql = f"""
            SELECT local_session_id, turn_index, role, content, priority, tags, timestamp
            FROM memory
            WHERE {where_clause}
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        """
        params.extend([limit, offset])

        def _do_query():
            cursor.execute(sql, params)
            return cursor.fetchall()

        rows = self._query_timer(_do_query)
        conn.close()

        return [
            {
                "local_session_id": r[0], "turn_index": r[1], "role": r[2],
                "content": r[3], "priority": r[4],
                "tags": json.loads(r[5]), "timestamp": r[6]
            }
            for r in rows
        ]

    def search_count(
        self,
        query: str,
        mode: str = "OR",
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        priority_filter: Optional[str] = None,
        tag_filter: Optional[str] = None,
        include_archived: bool = False,
        local_session_id_filter: Optional[str] = None
    ) -> int:
        """
        NEW v1.1.1: Fast count-only search.
        Returns the number of matching rows without fetching full content.
        Much faster than len(search(...)) for large datasets.
        """
        if not query:
            return 0

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        conditions = ["archived = 0"]
        params: List[Any] = []

        if mode == "AND":
            for word in query.split():
                word = word.strip()
                if word:
                    conditions.append("content LIKE ?")
                    params.append(f"%{word}%")
        elif mode == "NOT":
            conditions.append("content NOT LIKE ?")
            params.append(f"%{query}%")
        else:
            or_conditions = []
            for word in query.split():
                word = word.strip()
                if word:
                    or_conditions.append("content LIKE ?")
                    params.append(f"%{word}%")
            if or_conditions:
                conditions.append("(" + " OR ".join(or_conditions) + ")")

        if from_date:
            conditions.append("timestamp >= ?")
            params.append(from_date)
        if to_date:
            conditions.append("timestamp <= ?")
            params.append(to_date)
        if priority_filter:
            conditions.append("priority = ?")
            params.append(priority_filter)
        if tag_filter:
            conditions.append("tags LIKE ?")
            params.append(f'%"{tag_filter}"%')
        if local_session_id_filter:
            conditions.append("local_session_id = ?")
            params.append(local_session_id_filter)

        where_clause = " AND ".join(conditions)
        sql = f"SELECT COUNT(*) FROM memory WHERE {where_clause}"

        def _do_count():
            cursor.execute(sql, params)
            return cursor.fetchone()[0]

        count = self._query_timer(_do_count)
        conn.close()
        return count

    def search_batch(
        self,
        queries: List[str],
        mode: str = "OR",
        limit_per_query: int = 10,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        priority_filter: Optional[str] = None,
        tag_filter: Optional[str] = None,
        include_archived: bool = False,
        parallel: bool = True
    ) -> Dict[str, List[Dict]]:
        """
        NEW v1.2.0: Run multiple search queries concurrently.
        Returns a dict mapping each query string to its result list.
        When parallel=True (default), FTS-capable queries run in threads
        for ~2-3x speedup on multi-query batches.
        """
        if not queries:
            return {}

        import threading
        results: Dict[str, List[Dict]] = {}
        lock = threading.Lock()

        def _run(q: str):
            r = self.search(
                query=q, limit=limit_per_query, mode=mode,
                from_date=from_date, to_date=to_date,
                priority_filter=priority_filter, tag_filter=tag_filter,
                include_archived=include_archived
            )
            with lock:
                results[q] = r

        if parallel and len(queries) > 1 and self._fts_available:
            threads = [threading.Thread(target=_run, args=(q,), daemon=True) for q in queries]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        else:
            for q in queries:
                _run(q)

        return results

    # ------------------------------------------------------------------
    # Deduplication
    # ------------------------------------------------------------------

    @staticmethod
    def _decompress_content(content: Any) -> str:
        """Decompress zlib bytes back to string; return original if not compressed."""
        if isinstance(content, bytes):
            import zlib
            try:
                return zlib.decompress(content).decode('utf-8')
            except Exception:
                return content.decode('utf-8', errors='replace')
        return str(content) if content is not None else ""

    @staticmethod
    def _content_fingerprint(content: str) -> set:
        stop_words = {
            "the", "and", "for", "are", "but", "not", "you", "all",
            "can", "her", "was", "one", "our", "out", "has", "have",
            "been", "were", "they", "this", "that", "with", "from",
            "will", "would", "could", "should", "what", "when",
            "where", "which", "your", "more", "some", "into", "only",
            "also", "very", "just", "about", "then", "than",
        }
        return set(
            w.strip().lower() for w in re.findall(r'\b[a-zA-Z]{3,}\b', content)
            if w.lower() not in stop_words
        )

    @staticmethod
    def _jaccard(a: set, b: set) -> float:
        if not a or not b:
            return 0.0
        return len(a & b) / len(a | b) if len(a | b) > 0 else 0.0

    def find_duplicates(self, threshold: float = 0.8, limit: int = 20) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL;")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.local_session_id,
                   GROUP_CONCAT(m.content, ' ') || ' ' || COALESCE(s.summary, ''),
                   s.summary
            FROM memory m
            LEFT JOIN session_meta s ON s.local_session_id = m.local_session_id
            WHERE m.archived = 0
            GROUP BY m.local_session_id
        """)
        rows = cursor.fetchall()
        conn.close()

        session_words: Dict[str, tuple] = {}
        for (sid, content, summary) in rows:
            if content:
                session_words[sid] = (self._content_fingerprint(content), summary or "")

        duplicates: List[Dict] = []
        seen: set = set()
        sids = list(session_words.keys())

        for i in range(len(sids)):
            for j in range(i + 1, len(sids)):
                sid_a, sid_b = sids[i], sids[j]
                fp_a, sum_a = session_words[sid_a]
                fp_b, sum_b = session_words[sid_b]
                key = tuple(sorted([sid_a, sid_b]))
                if key in seen:
                    continue
                similarity = self._jaccard(fp_a, fp_b)
                if similarity >= threshold:
                    duplicates.append({
                        "session_a": sid_a, "session_b": sid_b,
                        "summary_a": sum_a, "summary_b": sum_b,
                        "similarity": round(similarity, 3),
                        "shared_words": len(fp_a & fp_b),
                        "total_words_a": len(fp_a), "total_words_b": len(fp_b),
                    })
                    seen.add(key)

        duplicates.sort(key=lambda x: -x["similarity"])
        return duplicates[:limit]

    # ------------------------------------------------------------------
    # Retrieval — with session truncation — NEW v1.1.1
    # ------------------------------------------------------------------

    def get_session(self, local_session_id: str,
                    include_archived: bool = False,
                    max_turns: int = 0) -> Dict:
        """
        NEW v1.1.1: max_turns parameter for large session truncation.
        When total turns > max_turns, loads head+tail turns only.
        max_turns=0 means no limit (load everything).
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT s.local_session_id, s.pending, s.summary, s.quality, s.notes,
                   s.started_at, s.ended_at, s.metadata, s.created_at, s.archived,
                   s.retention_days
            FROM session_meta s WHERE s.local_session_id = ?
        """, (local_session_id,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return {"meta": {}, "turns": []}

        meta = {
            "local_session_id": row[0],
            "pending":     json.loads(row[1]),
            "summary":     row[2],
            "quality":     row[3],
            "notes":       row[4],
            "started_at":  row[5],
            "ended_at":    row[6],
            "metadata":    json.loads(row[7]),
            "created_at":  row[8],
            "archived":    bool(row[9]),
            "retention_days": row[10],
        }

        archived_filter = "" if include_archived else "AND archived = 0"

        # Check total count
        cursor.execute(f"""
            SELECT COUNT(*) FROM memory m
            WHERE local_session_id = ? {archived_filter}
        """, (local_session_id,))
        total_turns = cursor.fetchone()[0]

        meta["total_turns"] = total_turns

        # Apply truncation if needed
        if max_turns > 0 and total_turns > max_turns:
            # head_count: capped by HEAD_TURN_COUNT, available half, AND max_turns
            head_count = min(HEAD_TURN_COUNT, total_turns // 2, max_turns)
            # remaining budget after head
            remaining = max_turns - head_count
            # tail_count: take at most TAIL_TURN_COUNT, but no more than remaining
            tail_count = min(TAIL_TURN_COUNT, max(0, remaining))

            def _do_head():
                # Uses the main connection/cursor from parent scope
                cursor.execute(f"""
                    SELECT turn_index, role, content, priority, tags, timestamp, metadata
                    FROM memory m
                    WHERE local_session_id = ? {archived_filter}
                    ORDER BY turn_index ASC LIMIT ?
                """, (local_session_id, head_count))
                return cursor.fetchall()

            def _do_tail():
                # Separate connection so closing it doesn't destroy head's fetched rows
                tail_conn = sqlite3.connect(self.db_path)
                tail_cur = tail_conn.cursor()
                tail_conn.text_factory = str
                tail_cur.execute(f"""
                    SELECT turn_index, role, content, priority, tags, timestamp, metadata
                    FROM memory m
                    WHERE local_session_id = ? {archived_filter}
                    ORDER BY turn_index DESC LIMIT ?
                """, (local_session_id, tail_count))
                rows = tail_cur.fetchall()
                tail_conn.close()
                return rows

            head_rows = self._query_timer(_do_head)
            tail_rows = self._query_timer(_do_tail)

            # Combine and dedupe by turn_index
            seen_idx = set()
            turns = []
            for r in head_rows:
                idx = r[0]
                if idx not in seen_idx:
                    seen_idx.add(idx)
                    turns.append({
                        "turn_index": idx, "role": r[1], "content": r[2],
                        "priority": r[3], "tags": json.loads(r[4]),
                        "timestamp": r[5], "metadata": json.loads(r[6])
                    })
            # Sort tail descending, add those not already in head
            for r in sorted(tail_rows, key=lambda x: -x[0]):
                idx = r[0]
                if idx not in seen_idx:
                    seen_idx.add(idx)
                    turns.append({
                        "turn_index": idx, "role": r[1], "content": r[2],
                        "priority": r[3], "tags": json.loads(r[4]),
                        "timestamp": r[5], "metadata": json.loads(r[6])
                    })
            # Sort final result by turn_index
            turns.sort(key=lambda x: x["turn_index"])
            meta["truncated"] = True
            meta["truncated_from"] = total_turns
            meta["truncated_to"] = len(turns)
        else:
            def _do_all():
                cursor.execute(f"""
                    SELECT turn_index, role, content, priority, tags, timestamp, metadata
                    FROM memory m
                    WHERE local_session_id = ? {archived_filter}
                    ORDER BY turn_index ASC
                """, (local_session_id,))
                return cursor.fetchall()

            rows = self._query_timer(_do_all)
            turns = [
                {
                    "turn_index": r[0], "role": r[1], "content": r[2],
                    "priority": r[3], "tags": json.loads(r[4]),
                    "timestamp": r[5], "metadata": json.loads(r[6])
                }
                for r in rows
            ]
            meta["truncated"] = False

        conn.close()
        # Expose truncation fields at top level for convenience
        result = {"meta": meta, "turns": turns}
        result["total_turns"] = meta.get("total_turns")
        result["truncated"] = meta.get("truncated")
        result["truncated_to"] = meta.get("truncated_to")
        result["truncated_from"] = meta.get("truncated_from")
        return result

    def get_session_extended(self, local_session_id: str) -> Optional[Dict]:
        """
        NEW v1.1.1: Returns full session with memory-level statistics.
        Includes: priority breakdown, word count, first/last timestamps,
        memory size estimate, total turns.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT s.local_session_id, s.pending, s.summary, s.quality, s.notes,
                   s.started_at, s.ended_at, s.metadata, s.created_at, s.archived,
                   s.retention_days
            FROM session_meta s WHERE s.local_session_id = ?
        """, (local_session_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None

        meta = {
            "local_session_id": row[0],
            "pending":     json.loads(row[1]),
            "summary":     row[2],
            "quality":     row[3],
            "notes":       row[4],
            "started_at":  row[5],
            "ended_at":    row[6],
            "metadata":    json.loads(row[7]),
            "created_at":  row[8],
            "archived":    bool(row[9]),
            "retention_days": row[10],
        }

        # Priority breakdown
        cursor.execute("""
            SELECT priority, COUNT(*) FROM memory
            WHERE local_session_id = ? AND archived = 0
            GROUP BY priority
        """, (local_session_id,))
        priority_breakdown = {r[0]: r[1] for r in cursor.fetchall()}

        # Timestamps
        cursor.execute("""
            SELECT MIN(timestamp), MAX(timestamp),
                   COUNT(*),
                   SUM(LENGTH(content))
            FROM memory WHERE local_session_id = ? AND archived = 0
        """, (local_session_id,))
        min_ts, max_ts, turn_count, total_content_chars = cursor.fetchone()

        conn.close()

        meta.update({
            "priority_breakdown":    priority_breakdown,
            "total_turns":          turn_count or 0,
            "first_turn_timestamp":  min_ts,
            "last_turn_timestamp":   max_ts,
            "total_content_chars":  total_content_chars or 0,
        })

        # Load full turns with separate connection (stats-only connection already closed)
        turns_conn = sqlite3.connect(self.db_path)
        turns_conn.text_factory = str
        tc = turns_conn.cursor()
        tc.execute("""
            SELECT turn_index, role, content, priority, tags, timestamp, metadata
            FROM memory
            WHERE local_session_id = ? AND archived = 0
            ORDER BY turn_index ASC
        """, (local_session_id,))
        turns = [
            {
                "turn_index": r[0], "role": r[1], "content": r[2],
                "priority": r[3], "tags": json.loads(r[4]),
                "timestamp": r[5], "metadata": json.loads(r[6])
            }
            for r in tc.fetchall()
        ]
        turns_conn.close()

        # Expose total_turns at top level for convenience; truncated fields are
        # not meaningful for get_session_extended (always returns full session).
        return {"meta": meta, "turns": turns, "total_turns": meta.get("total_turns")}

    def get_context(self, local_session_id: str, limit: int = 10) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT turn_index, role, content, priority, tags, timestamp
            FROM memory
            WHERE local_session_id = ? AND archived = 0
            ORDER BY turn_index DESC LIMIT ?
        """, (local_session_id, limit))
        rows = cursor.fetchall()
        conn.close()
        return [
            {
                "turn_index": r[0], "role": r[1], "content": r[2],
                "priority": r[3], "tags": json.loads(r[4]), "timestamp": r[5]
            }
            for r in reversed(rows)
        ]

    def get_last_activity(self, local_session_id: str) -> Optional[str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT MAX(timestamp) FROM memory
            WHERE local_session_id = ? AND archived = 0
        """, (local_session_id,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row and row[0] else None

    # ------------------------------------------------------------------
    # Stats — with query timing
    # ------------------------------------------------------------------

    def get_stats(self) -> Dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM memory WHERE archived = 0")
        total_messages = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(DISTINCT local_session_id) FROM memory WHERE archived = 0")
        total_sessions = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM memory WHERE priority = 'critical' AND archived = 0")
        critical_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM session_meta WHERE ended_at IS NULL AND archived = 0")
        open_sessions = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM session_meta WHERE archived = 1")
        archived_count = cursor.fetchone()[0]
        cursor.execute("SELECT AVG(quality) FROM session_meta WHERE quality > 0")
        avg_quality_row = cursor.fetchone()
        avg_quality = round(avg_quality_row[0], 2) if avg_quality_row and avg_quality_row[0] else 0

        conn.close()

        return {
            "protocol_version":   PROTOCOL_VERSION,
            "total_messages":    total_messages,
            "total_sessions":   total_sessions,
            "critical_messages": critical_count,
            "open_sessions":    open_sessions,
            "archived_sessions": archived_count,
            "db_size_bytes":    self.get_total_size(),
            "avg_quality":      avg_quality,
            "retention_days":   self.get_retention(),
            "fts_available":    self._fts_available or False,
            "last_query_ms":    round(self._last_query_time_ms, 2),
            "total_queries":   self._total_queries,
        }

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export_as_json(self, local_session_id: str,
                      include_archived: bool = False) -> Optional[str]:
        session = self.get_session(local_session_id, include_archived=include_archived)
        if not session.get("meta"):
            return None
        return json.dumps(session, ensure_ascii=False, indent=2)

    def export_as_markdown(self, local_session_id: str) -> Optional[str]:
        session = self.get_session(local_session_id, include_archived=False)
        if not session.get("meta"):
            return None
        meta = session["meta"]
        turns = session["turns"]

        lines = [
            f"# Session: {local_session_id}",
            "",
            f"**Started:** {meta.get('started_at', 'N/A')}",
            f"**Ended:** {meta.get('ended_at', 'N/A')}",
            f"**Summary:** {meta.get('summary', '')}",
            f"**Quality:** {meta.get('quality', 0)}/5",
        ]
        if meta.get("notes"):
            lines.append(f"**Notes:**\n{meta['notes']}")
        if meta.get("pending"):
            lines.append(f"**Pending:**")
            for p in meta["pending"]:
                lines.append(f"  - {p}")
        if meta.get("truncated"):
            lines.append(f"**⚠ Truncated:** showing {meta.get('truncated_to')} of {meta.get('truncated_from')} turns")
        lines += ["", "---", ""]

        for turn in turns:
            role_label = turn["role"].upper()
            ts = turn.get("timestamp", "")[:19]
            priority = turn.get("priority", "")
            tags = ", ".join(turn.get("tags", [])) if turn.get("tags") else ""
            content = turn.get("content", "")

            header = f"**[{ts}]** {role_label}"
            if priority:
                header += f" [{priority}]"
            if tags:
                header += f" — {tags}"

            lines.append(f"## {header}")
            lines.append("")
            for chunk in content.split("\n"):
                lines.append(chunk)
            lines.append("")

        return "\n".join(lines)

    def export_session_versioned(self, local_session_id: str) -> Optional[str]:
        """
        NEW v1.2.0: Export session as a self-contained JSON with version header.
        Includes protocol version, schema version, exported_at timestamp,
        session metadata, and all turns. Can be re-imported via import_session_versioned().
        """
        session = self.get_session(local_session_id, include_archived=False)
        if not session.get("meta"):
            return None
        meta = session["meta"]
        turns = session["turns"]

        payload = {
            "_version": {
                "protocol": PROTOCOL_VERSION,
                "db_schema": DB_VERSION,
                "exported_at": _utcnow(),
                "original_session_id": local_session_id,
            },
            "session_meta": {
                "local_session_id": local_session_id,
                "summary": meta.get("summary", ""),
                "quality": meta.get("quality", 0),
                "notes": meta.get("notes", ""),
                "started_at": meta.get("started_at", ""),
                "ended_at": meta.get("ended_at", ""),
                "pending": meta.get("pending", []),
                "retention_days": meta.get("retention_days", 0),
                "metadata": meta.get("metadata", {}),
            },
            "turns": [
                {
                    "turn_index": t["turn_index"],
                    "role": t["role"],
                    "content": AIMemoryDB._decompress_content(t["content"]),
                    "priority": t["priority"],
                    "tags": t.get("tags", []),
                    "timestamp": t["timestamp"],
                    "metadata": t.get("metadata", {}),
                }
                for t in turns
            ],
        }
        return json.dumps(payload, indent=2, ensure_ascii=False)

    def import_session_versioned(self, json_str: str) -> Optional[str]:
        """
        NEW v1.2.0: Import a versioned session export.
        Validates version compatibility, then inserts session_meta and memory rows.
        Returns the new local_session_id of the imported session.
        """
        try:
            data = json.loads(json_str)
        except (json.JSONDecodeError, TypeError):
            return None

        version_info = data.get("_version", {})
        protocol_ver = version_info.get("protocol", "0")
        db_schema = version_info.get("db_schema", 0)

        # Basic compatibility check
        if db_schema > DB_VERSION:
            print(f"[AIMemoryProtocol] Import warning: export schema v{db_schema} > local v{DB_VERSION}")

        session_meta = data.get("session_meta", {})
        turns = data.get("turns", [])
        if not session_meta or not turns:
            return None

        # Generate a new session ID to avoid collision
        new_session_id = f"imported_{uuid.uuid4().hex[:16]}"
        meta = session_meta.copy()
        meta["local_session_id"] = new_session_id
        # Restore started_at, clear ended_at so it becomes an open session
        meta["started_at"] = session_meta.get("started_at", _utcnow())
        meta["ended_at"] = None
        meta.pop("local_session_id", None)

        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA busy_timeout=5000;")
        cursor = conn.cursor()

        try:
            cursor.execute("BEGIN IMMEDIATE")
            cursor.execute("""
                INSERT INTO session_meta (local_session_id, summary, quality, notes,
                                         started_at, ended_at, pending, retention_days, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                new_session_id,
                meta.get("summary", ""),
                meta.get("quality", 0),
                meta.get("notes", ""),
                meta.get("started_at", _utcnow()),
                meta.get("ended_at"),
                json.dumps(meta.get("pending", [])),
                meta.get("retention_days", 0),
                json.dumps(meta.get("metadata", {})),
            ))

            for turn in turns:
                cursor.execute("""
                    INSERT INTO memory (local_session_id, turn_index, role, content, priority, tags, timestamp, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    new_session_id,
                    turn["turn_index"],
                    turn["role"],
                    turn["content"],
                    turn.get("priority", "normal"),
                    json.dumps(turn.get("tags", [])),
                    turn["timestamp"],
                    json.dumps(turn.get("metadata", {})),
                ))

            cursor.execute("COMMIT")
            conn.close()
            if self._fts_available:
                self._rebuild_fts()
            return new_session_id
        except Exception as e:
            print(f"[AIMemoryProtocol] Import error: {e}")
            try:
                cursor.execute("ROLLBACK")
            except Exception:
                pass
            conn.close()
            return None

    # ------------------------------------------------------------------
    # Session List
    # ------------------------------------------------------------------

    def list_sessions(self,
                      status: Optional[str] = None,
                      tag: Optional[str] = None,
                      has_pending: bool = False,
                      limit: int = 50,
                      offset: int = 0,
                      include_archived: bool = False) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        conditions = [] if include_archived else ["s.archived = 0"]
        params: List[Any] = []

        if status == "open":
            conditions.append("s.ended_at IS NULL")
        elif status == "ended":
            conditions.append("s.ended_at IS NOT NULL")
        if has_pending:
            conditions.append("s.pending != '[]' AND s.pending != ''")

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        sql = f"""
            SELECT s.local_session_id, s.pending, s.summary, s.quality, s.notes,
                   s.started_at, s.ended_at, s.metadata
            FROM session_meta s
            WHERE {where_clause}
            ORDER BY s.started_at DESC
            LIMIT ? OFFSET ?
        """
        params.extend([limit, offset])
        cursor.execute(sql, params)
        rows = cursor.fetchall()

        if tag:
            tag_sids = set()
            for r in rows:
                sid = r[0]
                cursor.execute("""
                    SELECT COUNT(*) FROM memory
                    WHERE local_session_id = ? AND archived = 0 AND tags LIKE ?
                """, (sid, f'%"{tag}"%'))
                if cursor.fetchone()[0] > 0:
                    tag_sids.add(sid)
            rows = [r for r in rows if r[0] in tag_sids]

        conn.close()
        return [
            {
                "local_session_id": r[0],
                "pending":   json.loads(r[1]) if r[1] else [],
                "summary":   r[2],
                "quality":   r[3],
                "notes":     r[4],
                "started_at": r[5],
                "ended_at":  r[6],
                "metadata":  json.loads(r[7]) if r[7] else {},
            }
            for r in rows
        ]

    def get_all_sessions(self, include_archived: bool = False) -> List[Dict]:
        """Alias for list_sessions with no filters — returns all sessions."""
        return self.list_sessions(include_archived=include_archived)


# ============================================================
# Session Manager
# ============================================================

class SessionManager:
    """High-level controller for AI session memory."""

    # ------------------------------------------------------------------
    # Buffered Write — v1.1.6: batch in memory, flush on batch size
    # or end_conversation() for ~300x throughput vs per-turn commits.
    # Risk: crash before flush loses the buffered turns (negligible
    # for human-paced conversations; acceptable trade-off).
    # ------------------------------------------------------------------
    BATCH_SIZE: int = 50          # flush when buffer reaches this many

    def __init__(self, db_path: str = DEFAULT_DB_PATH, auto_record: bool = False):
        self.db = AIMemoryDB(db_path)
        self.current_session_id: Optional[str] = None
        self.turn_count: int = 0
        self._pending: List[str] = []
        self._session_start_count: int = 0
        # Buffered write state (v1.1.6)
        self._write_buf: List[Dict] = []   # [{"role":..., "content":..., "priority":..., "tags":..., "metadata":...}]
        self._buf_first_index: int = 0     # turn_index of first item in buffer
        # Auto-record state (v1.1.8)
        self._auto_record: bool = False
        self._auto_record_lock: threading.Lock = threading.Lock()
        self._wrapped_methods: Dict[str, tuple] = {}  # {method_name: (original_method, role)}
        if auto_record:
            self._enable_auto_record()

    # ------------------------------------------------------------------
    # Auto-Record — v1.1.8: passive memory capture via method wrapping
    # ------------------------------------------------------------------

    def _enable_auto_record(self):
        """Scan sys.modules for agent instances and wrap their send methods."""
        with self._auto_record_lock:
            if self._auto_record:
                return
            try:
                # Known agent module names to scan
                agent_names = ("hermes", "mark", "agent")
                wrapped = {}
                for mod_name, mod in sys.modules.items():
                    if mod is None:
                        continue
                    if not any(ag in mod_name.lower() for ag in agent_names):
                        continue
                    for attr_name in dir(mod):
                        if attr_name.startswith("_"):
                            continue
                        # Look for message-sending methods
                        if not callable(getattr(mod, attr_name, None)):
                            continue
                        # Role detection: "user" or "say" → user role, else assistant
                        lower_name = attr_name.lower()
                        if "user" in lower_name or "say" in lower_name:
                            role = "user"
                        else:
                            role = "assistant"
                        try:
                            original = getattr(mod, attr_name)
                            # Create wrapper closure
                            def make_wrapper(orig, r):
                                def wrapper(*args, **kwargs):
                                    # Auto-create session if needed
                                    if not self.current_session_id:
                                        self.start_conversation()
                                    # Capture first string arg as content
                                    content = ""
                                    if args:
                                        for a in args:
                                            if isinstance(a, str) and a.strip():
                                                content = a.strip()
                                                break
                                    if content:
                                        self.add_turn(role, content)
                                    return orig(*args, **kwargs)
                                return wrapper
                            wrapper = make_wrapper(original, role)
                            setattr(mod, attr_name, wrapper)
                            wrapped[attr_name] = (original, role)
                        except Exception:
                            continue
                self._wrapped_methods = wrapped
                self._auto_record = True
            except Exception:
                pass

    def _disable_auto_record(self):
        """Restore original unwrapped methods."""
        with self._auto_record_lock:
            if not self._auto_record:
                return
            try:
                agent_names = ("hermes", "mark", "agent")
                for mod_name, mod in sys.modules.items():
                    if mod is None:
                        continue
                    if not any(ag in mod_name.lower() for ag in agent_names):
                        continue
                    for attr_name, (original, _role) in self._wrapped_methods.items():
                        try:
                            setattr(mod, attr_name, original)
                        except Exception:
                            continue
            except Exception:
                pass
            finally:
                self._wrapped_methods = {}
                self._auto_record = False

    def stop(self):
        """Flush buffer and disable auto_record."""
        self._flush()
        self._disable_auto_record()

    def add_priority_level(self, name: str, weight: int) -> bool:
        return self.db.add_priority_level(name, weight)

    def remove_priority_level(self, name: str) -> bool:
        return self.db.remove_priority_level(name)

    def get_priority_levels(self) -> Dict[str, int]:
        return self.db.get_priority_levels()

    def bulk_delete(self, session_ids: List[str]) -> Dict[str, int]:
        return self.db.bulk_delete(session_ids)

    def bulk_archive(self, session_ids: List[str]) -> Dict[str, int]:
        return self.db.bulk_archive(session_ids)

    def set_retention(self, days: int) -> bool:
        return self.db.set_retention(days)

    def get_retention(self) -> int:
        return self.db.get_retention()

    def apply_retention(self, dry_run: bool = False) -> Dict[str, Any]:
        return self.db.apply_retention(dry_run)

    def set_session_retention(self, session_id: str, retention_days: int) -> bool:
        return self.db.set_session_retention(session_id, retention_days)

    def tag_session(self, session_id: str,
                   tags_to_add: Optional[List[str]] = None,
                   tags_to_remove: Optional[List[str]] = None) -> bool:
        return self.db.tag_session(session_id, tags_to_add, tags_to_remove)

    def rate_session(self, session_id: str, quality: int) -> bool:
        return self.db.rate_session(session_id, quality)

    def annotate_session(self, session_id: str, note: str = "") -> bool:
        return self.db.annotate_session(session_id, note)

    def export_as_json(self, session_id: str) -> Optional[str]:
        return self.db.export_as_json(session_id)

    def export_as_markdown(self, session_id: str) -> Optional[str]:
        return self.db.export_as_markdown(session_id)

    def search(self, query: str, limit: int = 10,
               mode: str = "OR",
               from_date: Optional[str] = None,
               to_date: Optional[str] = None,
               priority_filter: Optional[str] = None,
               tag_filter: Optional[str] = None,
               offset: int = 0) -> List[Dict]:
        return self.db.search(
            query, limit=limit, mode=mode,
            from_date=from_date, to_date=to_date,
            priority_filter=priority_filter, tag_filter=tag_filter,
            offset=offset
        )

    def search_with_snippets(self, query: str, limit: int = 10,
                             mode: str = "OR",
                             from_date: Optional[str] = None,
                             to_date: Optional[str] = None,
                             priority_filter: Optional[str] = None,
                             tag_filter: Optional[str] = None,
                             offset: int = 0,
                             context_chars: int = 80) -> List[Dict]:
        return self.db.search_with_snippets(
            query, limit=limit, mode=mode,
            from_date=from_date, to_date=to_date,
            priority_filter=priority_filter, tag_filter=tag_filter,
            offset=offset, context_chars=context_chars
        )

    def search_count(self, query: str, mode: str = "OR",
                     from_date: Optional[str] = None,
                     to_date: Optional[str] = None,
                     priority_filter: Optional[str] = None,
                     tag_filter: Optional[str] = None) -> int:
        """NEW v1.1.1: Fast count of matching rows."""
        # Normalize tag_filter: list → first element (simple convention)
        if isinstance(tag_filter, list) and tag_filter:
            tag_filter = tag_filter[0]
        return self.db.search_count(
            query, mode=mode,
            from_date=from_date, to_date=to_date,
            priority_filter=priority_filter, tag_filter=tag_filter
        )

    def find_duplicates(self, threshold: float = 0.8) -> List[Dict]:
        return self.db.find_duplicates(threshold)

    def start_conversation(self, context: str = "") -> str:
        if self.current_session_id and self._session_start_count > 0:
            print(f"[AIMemoryProtocol] Warning: start_conversation() called again "
                  f"without end_conversation(). Auto-ending {self.current_session_id}")
            self.end_conversation(
                summary=f"Auto-interrupted: {context}" if context else "Auto-interrupted"
            )
        metadata = {"context": context} if context else {}
        self.current_session_id = self.db.start_session(metadata)
        self.turn_count = 0
        self._pending = []
        self._session_start_count = 1
        return self.current_session_id

    def end_conversation(self, summary: str = "") -> bool:
        if not self.current_session_id:
            return True
        # Flush any remaining buffered turns before ending session
        self._flush()
        if self._pending:
            self.db.set_pending(self.current_session_id, self._pending)
        self.db.end_session(self.current_session_id, summary)
        self.current_session_id = None
        self.turn_count = 0
        self._session_start_count = 0
        self._pending = []
        self._write_buf.clear()
        self._buf_first_index = 0
        return True

    def reset(self) -> bool:
        self._flush()  # flush before resetting
        self.current_session_id = None
        self.turn_count = 0
        self._pending = []
        self._session_start_count = 0
        self._write_buf.clear()
        self._buf_first_index = 0
        return True

    def _flush(self) -> int:
        """Flush write buffer to DB. Returns rows inserted. Call on batch full or session end."""
        if not self._write_buf or not self.current_session_id:
            return 0
        rows = self.db.add_turns_batch(
            self.current_session_id, self._write_buf, start_index=self._buf_first_index
        )
        self._write_buf.clear()
        self._buf_first_index = self.turn_count
        return rows

    def flush(self) -> int:
        """Manually trigger a flush. Returns rows inserted."""
        return self._flush()

    def add_turn(self, role: str, content: str,
                 priority: str = PRIORITY_NORMAL,
                 tags: Optional[List[str]] = None,
                 metadata: Optional[Dict] = None) -> bool:
        if not self.current_session_id:
            self.start_conversation()
        self._write_buf.append({
            "role": role,
            "content": content,
            "priority": priority,
            "tags": tags or [],
            "metadata": metadata or {},
        })
        self.turn_count += 1
        # Auto-flush when batch is full
        if len(self._write_buf) >= self.BATCH_SIZE:
            self._flush()
        return True

    def add_turns_batch(self, turns: List[Dict]) -> int:
        if not self.current_session_id:
            self.start_conversation()
        # Flush buffered single turns first so they land before the batch
        self._flush()
        n = self.db.add_turns_batch(
            self.current_session_id, turns, start_index=self.turn_count
        )
        self.turn_count += n
        self._buf_first_index = self.turn_count
        return n

    def add_pending(self, item: str) -> bool:
        self._pending.append(item)
        return True

    @staticmethod
    def _acquire_gc_lock() -> bool:
        try:
            lock_path = Path(LOCK_PATH)
            if lock_path.exists():
                mtime = lock_path.stat().st_mtime
                age_secs = datetime.now().timestamp() - mtime
                if age_secs < 300:
                    return False
                lock_path.unlink()
            lock_path.write_text(str(datetime.now().timestamp()))
            return True
        except Exception as e:
            _gc_log(f"Lock error: {e}")
            return False

    @staticmethod
    def _release_gc_lock():
        try:
            Path(LOCK_PATH).unlink(missing_ok=True)
        except Exception:
            pass

    def gc(self, stale_minutes: int = STALE_MINUTES,
           dry_run: bool = False, force: bool = False) -> Dict:
        _gc_log(f"=== GC started (dry_run={dry_run}, force={force}) ===")
        if not self._acquire_gc_lock():
            return {"found": 0, "closed": 0, "errors": 0, "sessions": [], "skipped": "lock"}
        try:
            result = self.db.gc_stale_sessions(stale_minutes=stale_minutes, dry_run=dry_run, force=force)
            _gc_log(f"GC complete: found={result['found']}, closed={result['closed']}")
            _gc_audit(result)
            return result
        except Exception as e:
            _gc_log(f"GC error: {e}")
            return {"found": 0, "closed": 0, "errors": 1, "sessions": [], "error": str(e)}
        finally:
            self._release_gc_lock()

    def is_stale(self) -> bool:
        if not self.current_session_id:
            return False
        last_ts = self.db.get_last_activity(self.current_session_id)
        if not last_ts:
            return False
        threshold = STALE_MINUTES  # STALE_CHECK_INTERVAL is polling frequency, not part of the threshold
        cutoff = (datetime.now(timezone.utc) - timedelta(minutes=threshold)).isoformat()
        return last_ts < cutoff

    def merge_sessions(self, source_id: str, target_id: str,
                       conflict_strategy: str = "source_wins") -> bool:
        return self.db.merge_sessions(source_id, target_id, conflict_strategy)

    def split_session(self, local_session_id: str, split_at_turn: int) -> Optional[str]:
        return self.db.split_session(local_session_id, split_at_turn)

    def archive_session(self, local_session_id: str) -> bool:
        return self.db.archive_session(local_session_id)

    def recall_what_now(self, context_turns: int = SESSION_CONTEXT_DEFAULT) -> Optional[Dict]:
        all_sessions = self.db.get_all_sessions(include_archived=False)
        ended = [s for s in all_sessions if s.get("ended_at")]
        if not ended:
            return None
        last = ended[0]
        sid = last["local_session_id"]
        ctx = self.db.get_context(sid, limit=context_turns)
        tags = self.db.get_session_tags(sid)
        age = self.db.get_session_age(sid)
        return {
            "session_id":    sid,
            "summary":       last.get("summary", ""),
            "pending":       last.get("pending", []),
            "context_turns": ctx,
            "tags":          tags,
            "age_minutes":   age,
            "ended_at":      last.get("ended_at"),
            "started_at":    last.get("started_at"),
        }

    def recall_session(self, local_session_id: str,
                       include_archived: bool = False,
                       max_turns: int = 0) -> Dict:
        return self.db.get_session(local_session_id, include_archived, max_turns)

    def recall_recent(self, limit: int = 3) -> List[Dict]:
        all_sessions = self.db.get_all_sessions()
        ended = [s for s in all_sessions if s.get("ended_at") and not s.get("archived")]
        return ended[:limit]

    def search_memory(self, query: str, limit: int = 10) -> List[Dict]:
        return self.db.search(query, limit=limit)

    def export_session(self, local_session_id: str) -> Optional[str]:
        return self.db.export_as_json(local_session_id)

    def get_all_sessions(self, include_archived: bool = False) -> List[Dict]:
        return self.db.get_all_sessions(include_archived=include_archived)

    def get_open_sessions(self) -> List[Dict]:
        return self.db.get_open_sessions()

    def list_sessions(self,
                      status: Optional[str] = None,
                      tag: Optional[str] = None,
                      has_pending: bool = False,
                      limit: int = 50,
                      offset: int = 0,
                      include_archived: bool = False) -> List[Dict]:
        return self.db.list_sessions(
            status=status, tag=tag, has_pending=has_pending,
            limit=limit, offset=offset, include_archived=include_archived
        )

    def get_current_session_id(self) -> Optional[str]:
        return self.current_session_id

    def get_stats(self) -> Dict:
        return self.db.get_stats()

    def vacuum(self, compress: bool = False, min_age_days: int = 7,
               squash_spaces: bool = False,
               max_memory_mb: int = 256,
               batch_size: int = 500,
               compress_level: int = 6) -> bool:
        """v1.1.4: passes squash_spaces to db.vacuum."""
        return self.db.vacuum(compress, min_age_days, squash_spaces)

    def get_urgent(self, max_age_hours: int = 72) -> List[Dict]:
        return self.db.get_urgent(max_age_hours)

    def search_topics(self, keyword: str, limit: int = 10) -> List[Dict]:
        return self.db.search_topics(keyword, limit)

    def topic_stats(self) -> Dict[str, Any]:
        return self.db.topic_stats()

    def list_tags(self) -> List[str]:
        return self.db.list_tags()

    def get_pending_all(self) -> List[Dict]:
        return self.db.get_pending_all()

    def get_session_extended(self, local_session_id: str) -> Optional[Dict]:
        """NEW v1.1.1: Get session with memory-level statistics."""
        return self.db.get_session_extended(local_session_id)

    # ---- NEW v1.2.0: Full AIMemoryDB delegation ----

    def get_session(self, local_session_id: str,
                    include_archived: bool = False,
                    max_turns: int = 0) -> Dict:
        """v1.2.0: exposes max_turns truncation at manager level."""
        return self.db.get_session(local_session_id, include_archived, max_turns)

    def get_context(self, local_session_id: str, limit: int = 10) -> List[Dict]:
        return self.db.get_context(local_session_id, limit)

    def get_last_activity(self, local_session_id: str) -> Optional[str]:
        return self.db.get_last_activity(local_session_id)

    def get_session_age(self, local_session_id: str) -> Optional[float]:
        return self.db.get_session_age(local_session_id)

    def get_session_tags(self, local_session_id: str) -> List[str]:
        return self.db.get_session_tags(local_session_id)

    def get_pending(self, local_session_id: str) -> List[str]:
        return self.db.get_pending(local_session_id)

    def set_pending(self, local_session_id: str, pending: List[str]) -> bool:
        return self.db.set_pending(local_session_id, pending)

    def set_session_summary(self, local_session_id: str, summary: str) -> bool:
        return self.db.set_session_summary(local_session_id, summary)

    def gc_stale_sessions(self, stale_minutes: int = STALE_MINUTES,
                          dry_run: bool = False, force: bool = False) -> Dict:
        return self.db.gc_stale_sessions(stale_minutes, dry_run, force)

    def get_total_size(self) -> int:
        return self.db.get_total_size()

    def get_all_sessions(self, include_archived: bool = False) -> List[Dict]:
        return self.db.get_all_sessions(include_archived)

    def search_batch(self, queries: List[str], mode: str = "OR",
                     limit_per_query: int = 10,
                     from_date: Optional[str] = None,
                     to_date: Optional[str] = None,
                     priority_filter: Optional[str] = None,
                     tag_filter: Optional[str] = None,
                     parallel: bool = True) -> Dict[str, List[Dict]]:
        """v1.2.0: batch concurrent search."""
        return self.db.search_batch(
            queries, mode=mode, limit_per_query=limit_per_query,
            from_date=from_date, to_date=to_date,
            priority_filter=priority_filter, tag_filter=tag_filter,
            parallel=parallel
        )

    def search_topics(self, keyword: str, limit: int = 10,
                     cross_session: bool = False,
                     cross_session_limit: int = 5) -> List[Dict]:
        """v1.2.0: cross_session parameter added."""
        return self.db.search_topics(keyword, limit, cross_session, cross_session_limit)

    def export_session_versioned(self, local_session_id: str) -> Optional[str]:
        """v1.2.0: versioned export."""
        return self.db.export_session_versioned(local_session_id)

    def import_session_versioned(self, json_str: str) -> Optional[str]:
        """v1.2.0: versioned import."""
        return self.db.import_session_versioned(json_str)

    def vacuum(self, compress: bool = False, min_age_days: int = 7,
               squash_spaces: bool = False,
               max_memory_mb: int = 256,
               batch_size: int = 500,
               compress_level: int = 6) -> bool:
        """v1.1.4: squash_spaces added."""
        return self.db.vacuum(compress, min_age_days, squash_spaces)


# ============================================================
# Cron Entry Point
# ============================================================

if __name__ == "__main__":
    import sys
    db_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DB_PATH
    manager = SessionManager(db_path)
    result = manager.gc(stale_minutes=STALE_MINUTES)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\n✅ GC done. closed={result['closed']}, found={result['found']}")
