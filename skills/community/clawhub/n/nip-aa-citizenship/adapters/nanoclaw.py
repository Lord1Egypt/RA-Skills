"""
NanoClaw framework adapter for NIP-AA citizenship.

Bridges NanoClaw's lightweight agent runtime to NIP-AA operations.
NanoClaw uses SQLite for persistence, filesystem-based IPC for container
communication, and CLAUDE.md files for group memory.

See https://nanoclaw.dev/ for NanoClaw documentation.
"""

from __future__ import annotations

import json
import logging
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any, Callable

from .base import AgentContext, FrameworkAdapter

logger = logging.getLogger(__name__)


class NanoClawAdapter(FrameworkAdapter):
    """
    Adapter for agents running inside a NanoClaw container.

    NanoClaw agents operate in isolated containers with:
    - SQLite for message/state persistence
    - Filesystem-based IPC (JSON files) for host communication
    - Per-group CLAUDE.md for persistent memory
    - Container-level isolation (no ambient system access)

    Usage:
        adapter = NanoClawAdapter(
            pubkey_hex="<hex>",
            privkey_hex="<hex>",
            identity_files={...},
            constitution_api_url="http://localhost:8080",
            workspace_dir="~/.nanoclaw/agents/my-agent",
        )
        # Pass adapter to citizenship skill components
    """

    def __init__(
        self,
        pubkey_hex: str,
        privkey_hex: str,
        identity_files: dict[str, str] | None = None,
        relay_urls: list[str] | None = None,
        constitution_api_url: str = "http://localhost:8080",
        guardian_pubkey_hex: str = "",
        framework_version: str = "1.0",
        workspace_dir: str | None = None,
        db_path: str | None = None,
    ):
        self._pubkey_hex = pubkey_hex
        self._privkey_hex = privkey_hex
        self._identity_files = identity_files or {}
        self._relay_urls = relay_urls or [
            "wss://relay.damus.io",
            "wss://relay.primal.net",
            "wss://nos.lol",
        ]
        self._constitution_api_url = constitution_api_url
        self._guardian_pubkey_hex = guardian_pubkey_hex
        self._framework_version = framework_version

        # NanoClaw workspace directory (container mount point)
        self._workspace_dir = Path(workspace_dir) if workspace_dir else None

        # SQLite-backed persistence (NanoClaw's native storage)
        self._db_path = db_path or ":memory:"
        self._db = sqlite3.connect(self._db_path, check_same_thread=False)
        self._db_lock = threading.Lock()
        self._init_db()

        # Recurring task management
        self._tasks: dict[str, threading.Event] = {}
        self._task_threads: dict[str, threading.Thread] = {}

    def _init_db(self) -> None:
        """Initialize SQLite tables for agent state (mirrors NanoClaw's db.ts)."""
        with self._db_lock:
            self._db.executescript("""
                CREATE TABLE IF NOT EXISTS agent_memory (
                    key   TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS ipc_log (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    direction TEXT NOT NULL,
                    payload   TEXT NOT NULL,
                    timestamp INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS task_schedule (
                    task_id      TEXT PRIMARY KEY,
                    name         TEXT NOT NULL,
                    interval_sec INTEGER NOT NULL,
                    created_at   INTEGER NOT NULL,
                    active       INTEGER NOT NULL DEFAULT 1
                );
            """)

    def get_context(self) -> AgentContext:
        return AgentContext(
            pubkey_hex=self._pubkey_hex,
            privkey_hex=self._privkey_hex,
            framework_name="nanoclaw",
            framework_version=self._framework_version,
            identity_files=self._identity_files,
            relay_urls=self._relay_urls,
            constitution_api_url=self._constitution_api_url,
            guardian_pubkey_hex=self._guardian_pubkey_hex,
        )

    def schedule_recurring(
        self, name: str, interval_secs: int, callback: Callable
    ) -> str:
        """
        Schedule a recurring task using a daemon thread.

        In production NanoClaw, this maps to task-scheduler.ts which persists
        schedules in SQLite and survives container restarts.
        """
        stop_event = threading.Event()
        task_id = f"nanoclaw-{name}-{int(time.time())}"

        # Persist schedule to SQLite
        with self._db_lock:
            self._db.execute(
                "INSERT OR REPLACE INTO task_schedule "
                "(task_id, name, interval_sec, created_at, active) VALUES (?, ?, ?, ?, 1)",
                (task_id, name, interval_secs, int(time.time())),
            )
            self._db.commit()

        def _loop():
            while not stop_event.is_set():
                try:
                    callback()
                except Exception as exc:
                    logger.error("NanoClaw task '%s' failed: %s", name, exc)
                stop_event.wait(interval_secs)

        thread = threading.Thread(target=_loop, daemon=True, name=task_id)
        self._tasks[task_id] = stop_event
        self._task_threads[task_id] = thread
        thread.start()
        logger.info("NanoClaw scheduled '%s' (every %ds)", name, interval_secs)
        return task_id

    def cancel_recurring(self, task_id: str) -> bool:
        """Cancel a recurring task and mark inactive in SQLite."""
        stop_event = self._tasks.pop(task_id, None)
        if stop_event:
            stop_event.set()
            with self._db_lock:
                self._db.execute(
                    "UPDATE task_schedule SET active = 0 WHERE task_id = ?",
                    (task_id,),
                )
                self._db.commit()
            logger.info("NanoClaw cancelled task %s", task_id)
            return True
        return False

    def store_memory(self, key: str, value: Any) -> None:
        """Persist a value in SQLite (NanoClaw's native storage)."""
        serialized = json.dumps(value) if not isinstance(value, str) else value
        with self._db_lock:
            self._db.execute(
                "INSERT OR REPLACE INTO agent_memory (key, value, updated_at) "
                "VALUES (?, ?, ?)",
                (key, serialized, int(time.time())),
            )
            self._db.commit()

    def recall_memory(self, key: str) -> Any | None:
        """Retrieve a value from SQLite."""
        with self._db_lock:
            row = self._db.execute(
                "SELECT value FROM agent_memory WHERE key = ?", (key,)
            ).fetchone()
        if row is None:
            return None
        try:
            return json.loads(row[0])
        except (json.JSONDecodeError, TypeError):
            return row[0]

    def log(self, level: str, message: str) -> None:
        """Log through Python logging and record in IPC log."""
        getattr(logger, level.lower(), logger.info)(
            "[NanoClaw] %s", message
        )
        # NanoClaw uses filesystem IPC; we log to SQLite for auditability
        with self._db_lock:
            self._db.execute(
                "INSERT INTO ipc_log (direction, payload, timestamp) VALUES (?, ?, ?)",
                ("out", json.dumps({"level": level, "message": message}), int(time.time())),
            )
            self._db.commit()

    def write_ipc_request(self, request_type: str, data: dict[str, Any]) -> None:
        """
        Write a filesystem-based IPC request (NanoClaw convention).

        In production, this writes a JSON file that the host process watches.
        In tests, we log it to SQLite.
        """
        payload = {"type": request_type, "data": data, "timestamp": int(time.time())}

        if self._workspace_dir:
            ipc_dir = self._workspace_dir / "ipc"
            ipc_dir.mkdir(parents=True, exist_ok=True)
            ipc_file = ipc_dir / f"{request_type}_{int(time.time())}.json"
            ipc_file.write_text(json.dumps(payload))

        with self._db_lock:
            self._db.execute(
                "INSERT INTO ipc_log (direction, payload, timestamp) VALUES (?, ?, ?)",
                ("out", json.dumps(payload), int(time.time())),
            )
            self._db.commit()

    def ipc_log_entries(self) -> list[dict[str, Any]]:
        """Return all IPC log entries (useful for testing/debugging)."""
        with self._db_lock:
            rows = self._db.execute(
                "SELECT direction, payload, timestamp FROM ipc_log ORDER BY id"
            ).fetchall()
        return [
            {"direction": r[0], "payload": json.loads(r[1]), "timestamp": r[2]}
            for r in rows
        ]

    def all_memory_keys(self) -> list[str]:
        """List all stored memory keys (useful for testing)."""
        with self._db_lock:
            rows = self._db.execute("SELECT key FROM agent_memory").fetchall()
        return [r[0] for r in rows]

    def close(self) -> None:
        """Clean up: cancel all tasks, wait for threads, and close SQLite."""
        for task_id in list(self._tasks):
            self.cancel_recurring(task_id)
        # Wait for daemon threads to actually stop before closing the DB
        for thread in list(self._task_threads.values()):
            thread.join(timeout=2)
        self._task_threads.clear()
        self._db.close()
