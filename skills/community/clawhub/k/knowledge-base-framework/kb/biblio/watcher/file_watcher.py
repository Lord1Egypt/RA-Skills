#!/usr/bin/env python3
"""
FileWatcher - Monitor kb/library/ for new files and trigger essence generation.

Features:
- Scans kb/library/ for new .md and .pdf files
- Tracks processed files in SQLite DB (avoids reprocessing)
- Excludes kb/library/biblio/ (no recursive scanning into LLM output)
- Triggers EssenzGenerator on new files
- Async-first design
- Configurable scan interval and file filters
"""

import asyncio
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any, Set

from kb.biblio.config import LLMConfig, get_llm_config
from kb.base.config import KBConfig, get_config
from kb.base.logger import KBLogger, get_logger

logger = get_logger("kb.llm.watcher")


class FileWatcherError(Exception):
    """Error in file watcher operations."""
    pass


class WatchedFile:
    """
    Represents a file detected by the watcher.

    Attributes:
        path: Absolute path to the file
        relative_path: Path relative to library root
        file_hash: SHA256 hash of file content
        size: File size in bytes
        modified_at: Last modification timestamp
        extension: File extension (e.g. '.md', '.pdf')
    """

    def __init__(
        self,
        path: Path,
        relative_path: Path,
        file_hash: str,
        size: int,
        modified_at: datetime,
        extension: str,
    ):
        self.path = path
        self.relative_path = relative_path
        self.file_hash = file_hash
        self.size = size
        self.modified_at = modified_at
        self.extension = extension

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "path": str(self.path),
            "relative_path": str(self.relative_path),
            "file_hash": self.file_hash,
            "size": self.size,
            "modified_at": self.modified_at.isoformat(),
            "extension": self.extension,
        }


class FileWatcherState:
    """
    Persistent state tracker for the file watcher.

    Uses SQLite to track which files have been processed.
    Stores file hashes to detect content changes.
    """

    def __init__(self, db_path: Optional[Path] = None):
        self._db_path = db_path or self._default_db_path()
        self._init_db()

    @staticmethod
    def _default_db_path() -> Path:
        """Default path for watcher state database."""
        config = get_config()
        return config.base_path / "watcher_state.db"

    def _init_db(self) -> None:
        """Initialize the tracking database."""
        self._db_path.parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(str(self._db_path)) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS watched_files (
                    path TEXT PRIMARY KEY,
                    file_hash TEXT NOT NULL,
                    size INTEGER NOT NULL,
                    modified_at TEXT NOT NULL,
                    processed_at TEXT,
                    status TEXT NOT NULL DEFAULT 'pending',
                    error_message TEXT,
                    essence_hash TEXT,
                    scan_count INTEGER NOT NULL DEFAULT 0,
                    last_scanned_at TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_watched_status
                ON watched_files(status)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_watched_hash
                ON watched_files(file_hash)
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS scan_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scan_at TEXT NOT NULL,
                    files_found INTEGER NOT NULL DEFAULT 0,
                    files_new INTEGER NOT NULL DEFAULT 0,
                    files_changed INTEGER NOT NULL DEFAULT 0,
                    files_processed INTEGER NOT NULL DEFAULT 0,
                    errors INTEGER NOT NULL DEFAULT 0,
                    duration_ms INTEGER NOT NULL DEFAULT 0
                )
            """)
            conn.commit()

    async def is_processed(self, file_path: Path) -> bool:
        """Check if a file has already been processed."""
        def _check():
            with sqlite3.connect(str(self._db_path)) as conn:
                row = conn.execute(
                    "SELECT status FROM watched_files WHERE path = ?",
                    (str(file_path),)
                ).fetchone()
                return row is not None and row[0] in ("processed", "skipped")
        return await asyncio.to_thread(_check)

    async def get_file_state(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Get stored state for a file."""
        def _get():
            with sqlite3.connect(str(self._db_path)) as conn:
                conn.row_factory = sqlite3.Row
                row = conn.execute(
                    "SELECT * FROM watched_files WHERE path = ?",
                    (str(file_path),)
                ).fetchone()
                if row:
                    return dict(row)
            return None
        return await asyncio.to_thread(_get)

    async def has_changed(self, file_path: Path, current_hash: str) -> bool:
        """Check if a file has changed since last processing."""
        state = await self.get_file_state(file_path)
        if state is None:
            return True
        return state["file_hash"] != current_hash

    async def mark_scanned(self, watched_file: WatchedFile) -> None:
        """Mark a file as scanned (seen but not necessarily processed)."""
        now = datetime.now(timezone.utc).isoformat()

        def _mark():
            with sqlite3.connect(str(self._db_path)) as conn:
                conn.execute("""
                    INSERT INTO watched_files
                        (path, file_hash, size, modified_at, last_scanned_at, scan_count)
                    VALUES (?, ?, ?, ?, ?, 1)
                    ON CONFLICT(path) DO UPDATE SET
                        file_hash = excluded.file_hash,
                        size = excluded.size,
                        modified_at = excluded.modified_at,
                        last_scanned_at = excluded.last_scanned_at,
                        scan_count = scan_count + 1
                """, (
                    str(watched_file.path),
                    watched_file.file_hash,
                    watched_file.size,
                    watched_file.modified_at.isoformat(),
                    now,
                ))
                conn.commit()

        await asyncio.to_thread(_mark)

    async def mark_processing(self, file_path: Path) -> None:
        """Mark a file as currently being processed."""
        now = datetime.now(timezone.utc).isoformat()
        def _mark():
            with sqlite3.connect(str(self._db_path)) as conn:
                conn.execute(
                    "UPDATE watched_files SET status = 'processing', last_scanned_at = ? WHERE path = ?",
                    (now, str(file_path))
                )
                conn.commit()
        await asyncio.to_thread(_mark)

    async def mark_processed(
        self,
        file_path: Path,
        essence_hash: Optional[str] = None,
    ) -> None:
        """Mark a file as successfully processed."""
        now = datetime.now(timezone.utc).isoformat()
        def _mark():
            with sqlite3.connect(str(self._db_path)) as conn:
                conn.execute("""
                    UPDATE watched_files
                    SET status = 'processed',
                        processed_at = ?,
                        essence_hash = ?,
                        error_message = NULL
                    WHERE path = ?
                """, (now, essence_hash, str(file_path)))
                conn.commit()
        await asyncio.to_thread(_mark)

    async def mark_skipped(self, file_path: Path, reason: str = "") -> None:
        """Mark a file as skipped."""
        now = datetime.now(timezone.utc).isoformat()
        def _mark():
            with sqlite3.connect(str(self._db_path)) as conn:
                conn.execute("""
                    UPDATE watched_files
                    SET status = 'skipped',
                        processed_at = ?,
                        error_message = ?
                    WHERE path = ?
                """, (now, reason, str(file_path)))
                conn.commit()
        await asyncio.to_thread(_mark)

    async def mark_error(self, file_path: Path, error: str) -> None:
        """Mark a file as errored during processing."""
        def _mark():
            with sqlite3.connect(str(self._db_path)) as conn:
                conn.execute("""
                    UPDATE watched_files
                    SET status = 'error',
                        error_message = ?,
                        processed_at = NULL
                    WHERE path = ?
                """, (error[:500], str(file_path)))
                conn.commit()
        await asyncio.to_thread(_mark)

    async def log_scan(
        self,
        files_found: int,
        files_new: int,
        files_changed: int,
        files_processed: int,
        errors: int,
        duration_ms: int,
    ) -> None:
        """Log scan results for tracking."""
        now = datetime.now(timezone.utc).isoformat()
        def _log():
            with sqlite3.connect(str(self._db_path)) as conn:
                conn.execute("""
                    INSERT INTO scan_log
                        (scan_at, files_found, files_new, files_changed,
                         files_processed, errors, duration_ms)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (now, files_found, files_new, files_changed,
                      files_processed, errors, duration_ms))
                conn.commit()
        await asyncio.to_thread(_log)

    def get_stats(self) -> Dict[str, Any]:
        """Get watcher statistics."""
        with sqlite3.connect(str(self._db_path)) as conn:
            stats = {}
            stats["total_tracked"] = conn.execute(
                "SELECT COUNT(*) FROM watched_files"
            ).fetchone()[0]

            status_counts = {}
            for row in conn.execute(
                "SELECT status, COUNT(*) FROM watched_files GROUP BY status"
            ):
                status_counts[row[0]] = row[1]
            stats["by_status"] = status_counts

            last_scan = conn.execute(
                "SELECT scan_at FROM scan_log ORDER BY id DESC LIMIT 1"
            ).fetchone()
            stats["last_scan_at"] = last_scan[0] if last_scan else None

            recent_scans = []
            for row in conn.execute(
                "SELECT * FROM scan_log ORDER BY id DESC LIMIT 10"
            ):
                recent_scans.append({
                    "scan_at": row[1],
                    "files_found": row[2],
                    "files_new": row[3],
                    "files_changed": row[4],
                    "files_processed": row[5],
                    "errors": row[6],
                    "duration_ms": row[7],
                })
            stats["recent_scans"] = recent_scans

            return stats

    def reset_file(self, file_path: Path) -> None:
        """Reset a file's processing state (for re-processing)."""
        with sqlite3.connect(str(self._db_path)) as conn:
            conn.execute("""
                UPDATE watched_files
                SET status = 'pending',
                    processed_at = NULL,
                    essence_hash = NULL,
                    error_message = NULL
                WHERE path = ?
            """, (str(file_path),))
            conn.commit()

    def get_pending_files(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get list of files pending processing."""
        with sqlite3.connect(str(self._db_path)) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT * FROM watched_files
                WHERE status IN ('pending', 'error')
                ORDER BY last_scanned_at ASC
                LIMIT ?
            """, (limit,)).fetchall()
            return [dict(r) for r in rows]


class FileWatcher:
    """
    Monitors kb/library/ for new files and triggers essence generation.

    Features:
    - Scans kb/library/ recursively for .md and .pdf files
    - Excludes kb/library/biblio/ (LLM-generated output)
    - Tracks processed files in SQLite DB
    - Detects changes via SHA256 content hash
    - Triggers EssenzGenerator for new/changed files
    - Async scan and processing

    Usage:
        watcher = FileWatcher()

        # Run a single scan
        result = await watcher.scan()

        # Start continuous watching
        await watcher.run(interval_minutes=20)

        # Get stats
        stats = watcher.get_stats()
    """

    # File extensions to watch
    DEFAULT_EXTENSIONS: Set[str] = {".md", ".pdf"}

    # Directories to exclude (relative to library root)
    DEFAULT_EXCLUDE_DIRS: Set[str] = {"llm"}

    # Max file size to process (50MB)
    MAX_FILE_SIZE: int = 50 * 1024 * 1024

    def __init__(
        self,
        llm_config: Optional[LLMConfig] = None,
        kb_config: Optional[KBConfig] = None,
        state: Optional[FileWatcherState] = None,
        extensions: Optional[Set[str]] = None,
        exclude_dirs: Optional[Set[str]] = None,
    ):
        self._llm_config = llm_config or get_llm_config()
        self._kb_config = kb_config or get_config()
        self._state = state or FileWatcherState()
        self._extensions = extensions or self.DEFAULT_EXTENSIONS
        self._exclude_dirs = exclude_dirs or self.DEFAULT_EXCLUDE_DIRS
        self._running = False
        self._cancel_event: Optional[asyncio.Event] = None

        logger.info(
            "FileWatcher initialized",
            extra={
                "library_path": str(self._kb_config.library_path),
                "extensions": list(self._extensions),
                "exclude_dirs": list(self._exclude_dirs),
            }
        )

    # --- File Discovery ---

    def _compute_file_hash(self, file_path: Path) -> str:
        """Compute SHA256 hash of file content."""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return f"sha256:{sha256.hexdigest()[:16]}"

    def _should_exclude(self, path: Path, library_root: Path) -> bool:
        """Check if a path should be excluded from scanning."""
        try:
            relative = path.relative_to(library_root)
            parts = relative.parts
            # Exclude if any part of the path is in exclude_dirs
            for part in parts:
                if part in self._exclude_dirs:
                    return True
        except ValueError:
            return True

        return False

    def _is_valid_file(self, path: Path) -> bool:
        """Check if a file matches our criteria."""
        if not path.is_file():
            return False

        if path.suffix.lower() not in self._extensions:
            return False

        # Skip hidden files
        if path.name.startswith("."):
            return False

        # Skip very large files
        try:
            if path.stat().st_size > self.MAX_FILE_SIZE:
                logger.warning(
                    f"Skipping large file: {path}",
                    extra={"size": path.stat().st_size}
                )
                return False
        except OSError:
            return False

        return True

    def discover_files(self, library_root: Optional[Path] = None) -> List[WatchedFile]:
        """
        Discover all watchable files in the library directory.

        Args:
            library_root: Override library root path

        Returns:
            List of WatchedFile objects
        """
        root = library_root or self._kb_config.library_path

        if not root.exists():
            logger.warning(f"Library root does not exist: {root}")
            return []

        if not root.is_dir():
            logger.warning(f"Library root is not a directory: {root}")
            return []

        watched_files: List[WatchedFile] = []

        for file_path in root.rglob("*"):
            # Skip excluded directories
            if self._should_exclude(file_path, root):
                continue

            if not self._is_valid_file(file_path):
                continue

            try:
                stat = file_path.stat()
                file_hash = self._compute_file_hash(file_path)
                relative_path = file_path.relative_to(root)

                watched_files.append(WatchedFile(
                    path=file_path,
                    relative_path=relative_path,
                    file_hash=file_hash,
                    size=stat.st_size,
                    modified_at=datetime.fromtimestamp(
                        stat.st_mtime, tz=timezone.utc
                    ),
                    extension=file_path.suffix.lower(),
                ))

            except (OSError, PermissionError) as e:
                logger.warning(
                    f"Cannot access file: {file_path}",
                    extra={"error": str(e)}
                )
                continue

        logger.info(
            f"Discovered {len(watched_files)} watchable files",
            extra={"library_root": str(root)}
        )

        return watched_files

    # --- Scan and Process ---

    async def scan(self) -> Dict[str, Any]:
        """
        Perform a single scan of the library directory.

        Discovers files, identifies new/changed ones, and processes them.

        Returns:
            Scan result dictionary with stats
        """
        import time
        start = time.time()

        logger.info("Starting file scan")

        # 1. Discover files
        watched_files = self.discover_files()

        # 2. Categorize files
        new_files: List[WatchedFile] = []
        changed_files: List[WatchedFile] = []
        unchanged_count = 0

        for wf in watched_files:
            # Track in DB
            await self._state.mark_scanned(wf)

            if not await self._state.is_processed(wf.path):
                new_files.append(wf)
            elif await self._state.has_changed(wf.path, wf.file_hash):
                changed_files.append(wf)
            else:
                unchanged_count += 1

        # 3. Process new and changed files
        to_process = new_files + changed_files
        processed_count = 0
        error_count = 0

        for wf in to_process:
            try:
                result = await self._process_file(wf)
                if result:
                    processed_count += 1
                else:
                    # Skipped
                    pass
            except Exception as e:
                error_count += 1
                logger.error(
                    f"Error processing file: {wf.path}",
                    extra={"error": str(e)}
                )

        duration_ms = int((time.time() - start) * 1000)

        # 4. Log scan results
        await self._state.log_scan(
            files_found=len(watched_files),
            files_new=len(new_files),
            files_changed=len(changed_files),
            files_processed=processed_count,
            errors=error_count,
            duration_ms=duration_ms,
        )

        result = {
            "files_found": len(watched_files),
            "files_new": len(new_files),
            "files_changed": len(changed_files),
            "files_unchanged": unchanged_count,
            "files_processed": processed_count,
            "errors": error_count,
            "duration_ms": duration_ms,
        }

        logger.info(
            "File scan completed",
            extra=result
        )

        return result

    async def _process_file(self, watched_file: WatchedFile) -> bool:
        """
        Process a single file: generate essence.

        Args:
            watched_file: The file to process

        Returns:
            True if processed, False if skipped

        Raises:
            FileWatcherError: On processing failure
        """
        await self._state.mark_processing(watched_file.path)

        try:
            # Import here to avoid circular imports
            from kb.biblio.generator import EssenzGenerator

            generator = EssenzGenerator()

            # Use filename without extension as topic
            topic = watched_file.path.stem
            if len(topic) > 100:
                topic = topic[:100]

            result = await generator.generate_essence(
                topic=topic,
                source_files=[str(watched_file.path)],
            )

            if result.success:
                await self._state.mark_processed(
                    watched_file.path,
                    essence_hash=result.essence_hash,
                )
                logger.info(
                    f"Processed file: {watched_file.relative_path}",
                    extra={
                        "essence_hash": result.essence_hash,
                        "duration_ms": result.duration_ms,
                    }
                )
                return True
            else:
                await self._state.mark_error(
                    watched_file.path,
                    error=result.error or "Unknown error"
                )
                raise FileWatcherError(
                    f"Essence generation failed for {watched_file.path}: {result.error}"
                )

        except ImportError:
            # EssenzGenerator not available — mark as skipped
            await self._state.mark_skipped(
                watched_file.path,
                reason="EssenzGenerator not available"
            )
            logger.warning(
                f"Skipping file (EssenzGenerator unavailable): {watched_file.path}"
            )
            return False

        except Exception as e:
            await self._state.mark_error(watched_file.path, str(e))
            raise

    # --- Continuous Watching ---

    async def run(self, interval_minutes: int = 20) -> None:
        """
        Run the watcher continuously.

        Scans at the specified interval until cancelled.

        Args:
            interval_minutes: Minutes between scans (default: 20)
        """
        self._running = True
        self._cancel_event = asyncio.Event()

        logger.info(
            f"FileWatcher started (interval: {interval_minutes}min)"
        )

        while self._running and not self._cancel_event.is_set():
            try:
                await self.scan()
            except Exception as e:
                logger.error(
                    f"Scan failed",
                    extra={"error": str(e)}
                )

            # Wait for interval or cancellation
            try:
                await asyncio.wait_for(
                    self._cancel_event.wait(),
                    timeout=interval_minutes * 60,
                )
                # If we get here, the event was set — stop
                break
            except asyncio.TimeoutError:
                # Normal — interval elapsed, continue
                pass

        self._running = False
        logger.info("FileWatcher stopped")

    def stop(self) -> None:
        """Stop the continuous watcher."""
        self._running = False
        if self._cancel_event:
            self._cancel_event.set()
        logger.info("FileWatcher stop requested")

    @property
    def is_running(self) -> bool:
        """Whether the watcher is currently running."""
        return self._running

    # --- Stats and Debugging ---

    def get_stats(self) -> Dict[str, Any]:
        """Get watcher statistics."""
        return {
            "is_running": self._running,
            "library_path": str(self._kb_config.library_path),
            "extensions": list(self._extensions),
            "exclude_dirs": list(self._exclude_dirs),
            **self._state.get_stats(),
        }

    def get_pending(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get files pending processing."""
        return self._state.get_pending_files(limit)

    def reprocess_file(self, file_path: Path) -> None:
        """Mark a file for re-processing."""
        self._state.reset_file(file_path)
        logger.info(f"File marked for re-processing: {file_path}")