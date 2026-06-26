#!/usr/bin/env python3
"""
TaskScheduler - Cron-like job scheduler for LLM maintenance tasks.

Features:
- Cron-like scheduling syntax for jobs
- Persistent state in SQLite (survives restarts)
- Manual trigger via CLI/method call
- Logging of all job executions
- Async/await for all jobs
- Graceful shutdown on SIGTERM
- Retry with exponential backoff on failures
- Four built-in jobs:
  1. File-Watcher Job — every 20 minutes
  2. KB-Validator Job — every 12 hours
  3. Graph-Rebuild Job — Sundays at 04:00
  4. Essenz-GC Job — daily at 03:00

Usage:
    scheduler = TaskScheduler()

    # Start all scheduled jobs
    await scheduler.start()

    # Manual trigger
    result = await scheduler.run_job("file-watcher")

    # Graceful shutdown
    await scheduler.shutdown()
"""

import asyncio
import json
import signal
import sqlite3
import time
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable, Awaitable
from functools import partial

from kb.biblio.config import LLMConfig, get_llm_config
from kb.base.config import KBConfig, get_config
from kb.base.logger import KBLogger, get_logger

logger = get_logger("kb.llm.scheduler")


# --- Async DB Helper ---
# sqlite3 is synchronous; calling it directly in async methods
# blocks the event loop. These helpers run DB operations in
# a thread pool via asyncio.to_thread().

def _db_connect(db_path: Path) -> sqlite3.Connection:
    """Create a new sqlite3 connection with row factory."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


async def _db_execute(db_path: Path, sql: str, params: tuple = (), commit: bool = True) -> None:
    """Execute a write statement in a background thread."""
    def _exec():
        with sqlite3.connect(str(db_path)) as conn:
            conn.execute(sql, params)
            if commit:
                conn.commit()
    await asyncio.to_thread(_exec)


async def _db_fetch_one(db_path: Path, sql: str, params: tuple = ()) -> Optional[tuple]:
    """Fetch one row in a background thread."""
    def _fetch():
        with sqlite3.connect(str(db_path)) as conn:
            return conn.execute(sql, params).fetchone()
    return await asyncio.to_thread(_fetch)


async def _db_fetch_all(db_path: Path, sql: str, params: tuple = ()) -> List[tuple]:
    """Fetch all rows in a background thread."""
    def _fetch():
        with sqlite3.connect(str(db_path)) as conn:
            conn.row_factory = sqlite3.Row
            return [dict(r) for r in conn.execute(sql, params).fetchall()]
    return await asyncio.to_thread(_fetch)


async def _db_execute_many(db_path: Path, sql: str, params_seq: list, commit: bool = True) -> None:
    """Execute many statements in a background thread."""
    def _exec():
        with sqlite3.connect(str(db_path)) as conn:
            conn.executemany(sql, params_seq)
            if commit:
                conn.commit()
    await asyncio.to_thread(_exec)


class TaskSchedulerError(Exception):
    """Error in task scheduler operations."""
    pass


class JobStatus(str, Enum):
    """Status of a scheduled job."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    DISABLED = "disabled"


class JobResult:
    """
    Result of a job execution.

    Attributes:
        job_id: Unique job identifier
        status: Final job status
        started_at: When the job started
        completed_at: When the job completed
        duration_ms: Execution time in milliseconds
        message: Human-readable result message
        error: Error message if failed
        data: Additional result data
    """

    def __init__(
        self,
        job_id: str,
        status: JobStatus,
        *,
        started_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
        duration_ms: int = 0,
        message: str = "",
        error: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None,
    ):
        self.job_id = job_id
        self.status = status
        self.started_at = started_at or datetime.now(timezone.utc)
        self.completed_at = completed_at
        self.duration_ms = duration_ms
        self.message = message
        self.error = error
        self.data = data or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "job_id": self.job_id,
            "status": self.status.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_ms": self.duration_ms,
            "message": self.message,
            "error": self.error,
            "data": self.data,
        }


class ScheduledJob:
    """
    Definition of a scheduled job.

    Attributes:
        job_id: Unique identifier (e.g. "file-watcher")
        name: Human-readable name
        description: What this job does
        cron_expression: Cron-like expression (minute hour day month weekday)
        handler: Async callable that executes the job
        enabled: Whether the job is active
        max_retries: Maximum retry attempts on failure
        retry_delay: Base delay in seconds for exponential backoff
        timeout: Maximum execution time in seconds
    """

    def __init__(
        self,
        job_id: str,
        name: str,
        description: str,
        cron_expression: str,
        handler: Callable[[], Awaitable[Dict[str, Any]]],
        *,
        enabled: bool = True,
        max_retries: int = 3,
        retry_delay: float = 5.0,
        timeout: int = 600,
    ):
        self.job_id = job_id
        self.name = name
        self.description = description
        self.cron_expression = cron_expression
        self.handler = handler
        self.enabled = enabled
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout

        # Parse cron expression
        self._cron = self._parse_cron(cron_expression)

    @staticmethod
    def _parse_cron(expression: str) -> Dict[str, Any]:
        """
        Parse a cron-like expression into components.

        Format: minute hour day month weekday

        Examples:
            "*/20 * * * *" — every 20 minutes
            "0 */12 * * *" — every 12 hours
            "0 4 * * 0"    — Sundays at 04:00
            "0 3 * * *"    — daily at 03:00

        Returns:
            Dictionary with parsed cron fields
        """
        parts = expression.strip().split()
        if len(parts) != 5:
            raise TaskSchedulerError(
                f"Invalid cron expression: '{expression}'. "
                f"Expected 5 fields: minute hour day month weekday"
            )

        def parse_field(field: str, min_val: int, max_val: int) -> Optional[set]:
            """Parse a single cron field into a set of valid values."""
            if field == "*":
                return None  # Any value

            values = set()

            for part in field.split(","):
                if "/" in part:
                    base, step = part.split("/", 1)
                    step = int(step)
                    if base == "*":
                        start = min_val
                    else:
                        start = int(base)
                    values.update(range(start, max_val + 1, step))
                elif "-" in part:
                    start, end = part.split("-", 1)
                    values.update(range(int(start), int(end) + 1))
                else:
                    values.add(int(part))

            return values

        return {
            "minute": parse_field(parts[0], 0, 59),
            "hour": parse_field(parts[1], 0, 23),
            "day": parse_field(parts[2], 1, 31),
            "month": parse_field(parts[3], 1, 12),
            "weekday": parse_field(parts[4], 0, 6),
        }

    def should_run(self, dt: Optional[datetime] = None) -> bool:
        """
        Check if this job should run at the given datetime.

        Args:
            dt: Datetime to check (defaults to now UTC)

        Returns:
            True if the cron expression matches
        """
        if not self.enabled:
            return False

        now = dt or datetime.now(timezone.utc)

        cron = self._cron

        def matches(field: Optional[set], value: int) -> bool:
            return field is None or value in field

        return (
            matches(cron["minute"], now.minute)
            and matches(cron["hour"], now.hour)
            and matches(cron["day"], now.day)
            and matches(cron["month"], now.month)
            and matches(cron["weekday"], now.weekday())  # 0=Monday
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "job_id": self.job_id,
            "name": self.name,
            "description": self.description,
            "cron_expression": self.cron_expression,
            "enabled": self.enabled,
            "max_retries": self.max_retries,
            "retry_delay": self.retry_delay,
            "timeout": self.timeout,
        }


class TaskScheduler:
    """
    Cron-like task scheduler for LLM maintenance jobs.

    Features:
    - Persistent state in SQLite
    - Manual trigger via run_job()
    - Graceful shutdown on SIGTERM/SIGINT
    - Retry with exponential backoff
    - Job execution logging

    Built-in Jobs:
    1. file-watcher: Scan library every 20 minutes
    2. kb-validator: Validate index integrity every 12 hours
    3. graph-rebuild: Rebuild knowledge graph Sundays at 04:00
    4. essenz-gc: Archive old essences daily at 03:00

    Usage:
        scheduler = TaskScheduler()
        await scheduler.start()

        # Manual trigger
        result = await scheduler.run_job("file-watcher")

        # Graceful shutdown
        await scheduler.shutdown()
    """

    def __init__(
        self,
        llm_config: Optional[LLMConfig] = None,
        kb_config: Optional[KBConfig] = None,
        db_path: Optional[Path] = None,
    ):
        self._llm_config = llm_config or get_llm_config()
        self._kb_config = kb_config or get_config()
        self._db_path = db_path or self._kb_config.base_path / "scheduler_state.db"
        self._jobs: Dict[str, ScheduledJob] = {}
        self._running = False
        self._shutdown_event = asyncio.Event()
        self._task: Optional[asyncio.Task] = None

        # Initialize DB
        self._init_db()

        # Register built-in jobs
        self._register_builtin_jobs()

        # Register signal handlers
        self._register_signals()

        logger.info("TaskScheduler initialized")

    def _init_db(self) -> None:
        """Initialize the scheduler state database."""
        self._db_path.parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(str(self._db_path)) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS job_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    completed_at TEXT,
                    duration_ms INTEGER DEFAULT 0,
                    message TEXT,
                    error TEXT,
                    result_data TEXT,
                    triggered_by TEXT NOT NULL DEFAULT 'scheduled',
                    retry_count INTEGER DEFAULT 0
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_job_log_job
                ON job_log(job_id)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_job_log_time
                ON job_log(started_at)
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS job_state (
                    job_id TEXT PRIMARY KEY,
                    last_run TEXT,
                    last_status TEXT,
                    last_duration_ms INTEGER DEFAULT 0,
                    run_count INTEGER DEFAULT 0,
                    error_count INTEGER DEFAULT 0,
                    enabled INTEGER DEFAULT 1,
                    next_run TEXT
                )
            """)
            conn.commit()

    def _register_signals(self) -> None:
        """Register signal handlers for graceful shutdown."""
        loop = asyncio.get_event_loop()
        try:
            for sig in (signal.SIGTERM, signal.SIGINT):
                loop.add_signal_handler(
                    sig,
                    lambda s=sig: asyncio.create_task(self._handle_signal(s))
                )
        except (RuntimeError, OSError):
            # Signal handlers can't be set in non-main thread or on Windows
            logger.debug("Could not register signal handlers (non-main thread or unsupported)")

    async def _handle_signal(self, sig: signal.Signals) -> None:
        """Handle shutdown signals gracefully."""
        logger.info(
            f"Received signal {sig.name}, initiating graceful shutdown"
        )
        await self.shutdown()

    # --- Built-in Jobs ---

    def _register_builtin_jobs(self) -> None:
        """Register the four built-in maintenance jobs."""
        # 1. File-Watcher Job — every 20 minutes
        self.register_job(ScheduledJob(
            job_id="file-watcher",
            name="File Watcher",
            description="Scan kb/library/ for new files and trigger essence generation",
            cron_expression="*/20 * * * *",
            handler=self._job_file_watcher,
            max_retries=3,
            retry_delay=10.0,
            timeout=300,
        ))

        # 2. KB-Validator Job — every 12 hours
        self.register_job(ScheduledJob(
            job_id="kb-validator",
            name="KB Validator",
            description="Validate knowledge base index integrity",
            cron_expression="0 */12 * * *",
            handler=self._job_kb_validator,
            max_retries=2,
            retry_delay=30.0,
            timeout=600,
        ))

        # 3. Graph-Rebuild Job — Sundays at 04:00
        self.register_job(ScheduledJob(
            job_id="graph-rebuild",
            name="Graph Rebuild",
            description="Rebuild knowledge graph from all essences",
            cron_expression="0 4 * * 6",  # 6 = Sunday (0=Mon convention)
            handler=self._job_graph_rebuild,
            max_retries=2,
            retry_delay=60.0,
            timeout=1800,
        ))

        # 4. Essenz-GC Job — daily at 03:00
        self.register_job(ScheduledJob(
            job_id="essenz-gc",
            name="Essenz GC",
            description="Archive old essences and cleanup stale data",
            cron_expression="0 3 * * *",
            handler=self._job_essenz_gc,
            max_retries=2,
            retry_delay=30.0,
            timeout=600,
        ))

    # --- Job Handlers ---

    async def _job_file_watcher(self) -> Dict[str, Any]:
        """Execute the file-watcher job."""
        from kb.biblio.watcher import FileWatcher

        watcher = FileWatcher(
            llm_config=self._llm_config,
            kb_config=self._kb_config,
        )
        result = await watcher.scan()
        return {
            "files_found": result.get("files_found", 0),
            "files_new": result.get("files_new", 0),
            "files_processed": result.get("files_processed", 0),
            "errors": result.get("errors", 0),
        }

    async def _job_kb_validator(self) -> Dict[str, Any]:
        """Execute the KB-validator job: check index integrity."""
        issues = []

        # Check essences directory consistency
        essences_path = self._llm_config.essences_path
        if essences_path.exists():
            for essence_dir in essences_path.iterdir():
                if not essence_dir.is_dir():
                    continue
                json_file = essence_dir / "essence.json"
                md_file = essence_dir / "essence.md"

                if not json_file.exists():
                    issues.append({
                        "type": "missing_json",
                        "path": str(essence_dir),
                        "message": f"Missing essence.json in {essence_dir.name}",
                    })
                    continue

                try:
                    data = json.loads(json_file.read_text(encoding="utf-8"))
                    # Validate required fields
                    essence = data.get("essence", {})
                    if not essence.get("title"):
                        issues.append({
                            "type": "missing_title",
                            "path": str(json_file),
                            "message": "Essence missing title",
                        })
                    if not essence.get("summary"):
                        issues.append({
                            "type": "missing_summary",
                            "path": str(json_file),
                            "message": "Essence missing summary",
                        })
                except json.JSONDecodeError as e:
                    issues.append({
                        "type": "invalid_json",
                        "path": str(json_file),
                        "message": f"Invalid JSON: {e}",
                    })

        # Check reports directory
        reports_path = self._llm_config.reports_path
        if reports_path.exists():
            for report_file in reports_path.rglob("*_report.md"):
                content = report_file.read_text(encoding="utf-8", errors="replace")
                if not content.strip().startswith("---"):
                    issues.append({
                        "type": "missing_frontmatter",
                        "path": str(report_file),
                        "message": "Report missing YAML frontmatter",
                    })

        # Check graph file
        graph_path = self._llm_config.graph_path / "knowledge_graph.json"
        if graph_path.exists():
            try:
                graph_data = json.loads(graph_path.read_text(encoding="utf-8"))
                if "nodes" not in graph_data or "edges" not in graph_data:
                    issues.append({
                        "type": "invalid_graph",
                        "path": str(graph_path),
                        "message": "Knowledge graph missing nodes or edges",
                    })
            except json.JSONDecodeError as e:
                issues.append({
                    "type": "invalid_graph_json",
                    "path": str(graph_path),
                    "message": f"Invalid graph JSON: {e}",
                })

        logger.info(
            "KB validation complete",
            extra={"issues_found": len(issues)}
        )

        return {
            "issues_found": len(issues),
            "issues": issues[:20],  # Cap for storage
            "status": "healthy" if not issues else "issues_found",
        }

    async def _job_graph_rebuild(self) -> Dict[str, Any]:
        """Execute the graph-rebuild job: rebuild knowledge graph from essences."""
        import shutil

        essences_path = self._llm_config.essences_path
        graph_path = self._llm_config.graph_path

        nodes = []
        edges = []

        # Collect all entities and relationships from essences
        if essences_path.exists():
            for essence_dir in essences_path.iterdir():
                if not essence_dir.is_dir():
                    continue

                json_file = essence_dir / "essence.json"
                if not json_file.exists():
                    continue

                try:
                    data = json.loads(json_file.read_text(encoding="utf-8"))
                    essence = data.get("essence", {})
                    essence_hash = essence_dir.name

                    # Add essence as node
                    nodes.append({
                        "id": essence_hash,
                        "type": "essence",
                        "label": essence.get("title", essence_hash),
                        "properties": {
                            "summary": essence.get("summary", "")[:200],
                            "keywords": essence.get("keywords", []),
                            "confidence": essence.get("confidence", 0),
                        }
                    })

                    # Add entities as nodes
                    for entity in essence.get("entities", []):
                        entity_id = f"entity:{entity}"
                        # Deduplicate: only add if not already present
                        if not any(n["id"] == entity_id for n in nodes):
                            nodes.append({
                                "id": entity_id,
                                "type": "entity",
                                "label": entity,
                            })

                    # Add relationships as edges
                    for rel in essence.get("relationships", []):
                        edges.append({
                            "source": f"entity:{rel.get('from', '')}",
                            "target": f"entity:{rel.get('to', '')}",
                            "type": rel.get("type", "related_to"),
                            "essence": essence_hash,
                        })

                    # Connect essence to its entities
                    for entity in essence.get("entities", []):
                        edges.append({
                            "source": essence_hash,
                            "target": f"entity:{entity}",
                            "type": "mentions",
                        })

                except (json.JSONDecodeError, IOError) as e:
                    logger.warning(
                        f"Failed to process essence for graph: {essence_dir.name}",
                        extra={"error": str(e)}
                    )
                    continue

        # Build final graph
        graph_data = {
            "version": "1.0",
            "rebuild_at": datetime.now(timezone.utc).isoformat(),
            "stats": {
                "nodes": len(nodes),
                "edges": len(edges),
            },
            "nodes": nodes,
            "edges": edges,
        }

        # Save graph
        graph_path.mkdir(parents=True, exist_ok=True)
        graph_file = graph_path / "knowledge_graph.json"

        # Backup existing graph
        if graph_file.exists():
            backup_file = graph_path / f"knowledge_graph_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json.bak"
            shutil.move(str(graph_file), str(backup_file))

        graph_file.write_text(
            json.dumps(graph_data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        logger.info(
            "Knowledge graph rebuilt",
            extra={"nodes": len(nodes), "edges": len(edges)}
        )

        return {
            "nodes": len(nodes),
            "edges": len(edges),
        }

    async def _job_essenz_gc(self) -> Dict[str, Any]:
        """Execute the essenz-GC job: archive old essences."""
        import shutil

        essences_path = self._llm_config.essences_path
        archive_path = essences_path.parent / "essences_archive"

        archived_count = 0
        removed_count = 0

        # Threshold: essences older than 90 days with no recent access
        threshold = datetime.now(timezone.utc) - timedelta(days=90)

        if essences_path.exists():
            for essence_dir in essences_path.iterdir():
                if not essence_dir.is_dir():
                    continue

                json_file = essence_dir / "essence.json"
                if not json_file.exists():
                    # Stale directory with no JSON — remove
                    try:
                        shutil.rmtree(essence_dir)
                        removed_count += 1
                    except OSError:
                        pass
                    continue

                try:
                    data = json.loads(json_file.read_text(encoding="utf-8"))
                    extracted_at = data.get("extracted_at")

                    if extracted_at:
                        # Parse ISO datetime
                        dt_str = extracted_at.replace("Z", "+00:00")
                        try:
                            extracted_dt = datetime.fromisoformat(dt_str)
                            if extracted_dt.tzinfo is None:
                                extracted_dt = extracted_dt.replace(tzinfo=timezone.utc)
                        except (ValueError, TypeError):
                            continue

                        if extracted_dt < threshold:
                            # Archive: move to archive directory
                            archive_path.mkdir(parents=True, exist_ok=True)
                            dest = archive_path / essence_dir.name

                            try:
                                shutil.move(str(essence_dir), str(dest))
                                archived_count += 1
                            except OSError as e:
                                logger.warning(
                                    f"Failed to archive essence {essence_dir.name}: {e}"
                                )

                except (json.JSONDecodeError, IOError) as e:
                    logger.warning(
                        f"Failed to process essence for GC: {essence_dir.name}",
                        extra={"error": str(e)}
                    )
                    continue

        # Clean up incoming queue
        incoming_path = self._llm_config.incoming_path
        cleaned_incoming = 0
        if incoming_path.exists():
            for f in incoming_path.iterdir():
                if f.is_file():
                    try:
                        mtime = datetime.fromtimestamp(
                            f.stat().st_mtime, tz=timezone.utc
                        )
                        if mtime < threshold:
                            f.unlink()
                            cleaned_incoming += 1
                    except OSError:
                        pass

        logger.info(
            "Essenz GC complete",
            extra={
                "archived": archived_count,
                "removed": removed_count,
                "cleaned_incoming": cleaned_incoming,
            }
        )

        return {
            "archived": archived_count,
            "removed": removed_count,
            "cleaned_incoming": cleaned_incoming,
        }

    # --- Job Registration ---

    def register_job(self, job: ScheduledJob) -> None:
        """Register a new job."""
        if job.job_id in self._jobs:
            logger.warning(
                f"Overwriting existing job: {job.job_id}"
            )
        self._jobs[job.job_id] = job
        logger.info(
            f"Registered job: {job.job_id}",
            extra={
                "name": job.name,
                "cron": job.cron_expression,
                "enabled": job.enabled,
            }
        )

    def unregister_job(self, job_id: str) -> bool:
        """Unregister a job by ID."""
        if job_id in self._jobs:
            del self._jobs[job_id]
            logger.info(f"Unregistered job: {job_id}")
            return True
        return False

    # --- Job Execution ---

    async def run_job(
        self,
        job_id: str,
        *,
        triggered_by: str = "manual",
    ) -> JobResult:
        """
        Execute a specific job by ID.

        Includes retry logic with exponential backoff.

        Args:
            job_id: ID of the job to execute
            triggered_by: Source of the trigger (manual, scheduled)

        Returns:
            JobResult with execution details
        """
        job = self._jobs.get(job_id)
        if job is None:
            raise TaskSchedulerError(f"Unknown job: {job_id}")

        if not job.enabled:
            return JobResult(
                job_id=job_id,
                status=JobStatus.SKIPPED,
                message=f"Job '{job.name}' is disabled",
            )

        logger.info(
            f"Starting job: {job.name}",
            extra={"job_id": job_id, "triggered_by": triggered_by}
        )

        started_at = datetime.now(timezone.utc)
        last_error = None
        retry_count = 0

        for attempt in range(job.max_retries):
            try:
                # Execute with timeout
                result_data = await asyncio.wait_for(
                    job.handler(),
                    timeout=job.timeout,
                )

                completed_at = datetime.now(timezone.utc)
                duration_ms = int((completed_at - started_at).total_seconds() * 1000)

                # Log success
                await self._log_execution(
                    job_id=job_id,
                    status=JobStatus.SUCCESS,
                    started_at=started_at,
                    completed_at=completed_at,
                    duration_ms=duration_ms,
                    message=f"Job completed successfully",
                    result_data=result_data,
                    triggered_by=triggered_by,
                    retry_count=retry_count,
                )

                await self._update_job_state(
                    job_id=job_id,
                    last_run=started_at,
                    last_status="success",
                    duration_ms=duration_ms,
                )

                return JobResult(
                    job_id=job_id,
                    status=JobStatus.SUCCESS,
                    started_at=started_at,
                    completed_at=completed_at,
                    duration_ms=duration_ms,
                    message="Job completed successfully",
                    data=result_data,
                )

            except asyncio.TimeoutError:
                last_error = f"Job timed out after {job.timeout}s"
                retry_count += 1
                logger.warning(
                    f"Job timed out: {job.name}",
                    extra={
                        "job_id": job_id,
                        "attempt": attempt + 1,
                        "timeout": job.timeout,
                    }
                )

            except asyncio.CancelledError:
                # Job was cancelled (shutdown) — don't retry
                logger.info(f"Job cancelled: {job.name}")
                raise

            except Exception as e:
                last_error = str(e)
                retry_count += 1
                logger.warning(
                    f"Job failed: {job.name}",
                    extra={
                        "job_id": job_id,
                        "attempt": attempt + 1,
                        "error": str(e),
                    }
                )

            # Retry with exponential backoff (except on last attempt)
            if attempt < job.max_retries - 1:
                delay = job.retry_delay * (2 ** attempt)
                logger.info(
                    f"Retrying job in {delay:.1f}s",
                    extra={"job_id": job_id, "attempt": attempt + 1}
                )
                await asyncio.sleep(delay)

        # All retries exhausted
        completed_at = datetime.now(timezone.utc)
        duration_ms = int((completed_at - started_at).total_seconds() * 1000)

        await self._log_execution(
            job_id=job_id,
            status=JobStatus.FAILED,
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=duration_ms,
            error=last_error,
            triggered_by=triggered_by,
            retry_count=retry_count,
        )

        await self._update_job_state(
            job_id=job_id,
            last_run=started_at,
            last_status="failed",
            duration_ms=duration_ms,
        )

        return JobResult(
            job_id=job_id,
            status=JobStatus.FAILED,
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=duration_ms,
            error=last_error,
            message=f"Job failed after {retry_count} retries",
        )

    # --- Scheduler Loop ---

    async def start(self) -> None:
        """
        Start the scheduler loop.

        Runs continuously, checking for due jobs every minute.
        Gracefully handles shutdown via SIGTERM or shutdown() call.
        """
        self._running = True
        self._shutdown_event.clear()

        logger.info("TaskScheduler started")

        while self._running and not self._shutdown_event.is_set():
            now = datetime.now(timezone.utc)

            # Check each job
            for job_id, job in self._jobs.items():
                if not job.enabled:
                    continue

                if job.should_run(now):
                    # Check if already ran recently (avoid double-runs)
                    if await self._ran_recently(job_id, within_minutes=2):
                        continue

                    # Run the job (fire-and-forget for scheduled runs)
                    asyncio.create_task(
                        self._safe_run_job(job_id, triggered_by="scheduled")
                    )

            # Wait 60 seconds or until shutdown
            try:
                await asyncio.wait_for(
                    self._shutdown_event.wait(),
                    timeout=60,
                )
                # Event was set — shutdown
                break
            except asyncio.TimeoutError:
                # Normal tick
                pass

        self._running = False
        logger.info("TaskScheduler stopped")

    async def _safe_run_job(self, job_id: str, triggered_by: str = "scheduled") -> None:
        """Run a job safely, catching all exceptions."""
        try:
            await self.run_job(job_id, triggered_by=triggered_by)
        except Exception as e:
            logger.error(
                f"Unexpected error running job: {job_id}",
                extra={"error": str(e)}
            )

    async def shutdown(self) -> None:
        """Gracefully shut down the scheduler."""
        logger.info("TaskScheduler shutdown initiated")
        self._running = False
        self._shutdown_event.set()

        # Give running jobs a moment to complete
        await asyncio.sleep(1)

        logger.info("TaskScheduler shutdown complete")

    @property
    def is_running(self) -> bool:
        """Whether the scheduler is currently running."""
        return self._running

    # --- State Management ---

    async def _ran_recently(self, job_id: str, within_minutes: int = 2) -> bool:
        """Check if a job ran within the last N minutes."""
        def _check():
            with sqlite3.connect(str(self._db_path)) as conn:
                row = conn.execute(
                    "SELECT last_run FROM job_state WHERE job_id = ?",
                    (job_id,)
                ).fetchone()

                if row is None or row[0] is None:
                    return False

                try:
                    last_run = datetime.fromisoformat(row[0].replace("Z", "+00:00"))
                    if last_run.tzinfo is None:
                        last_run = last_run.replace(tzinfo=timezone.utc)
                except (ValueError, TypeError):
                    return False

                cutoff = datetime.now(timezone.utc) - timedelta(minutes=within_minutes)
                return last_run > cutoff

        return await asyncio.to_thread(_check)

    async def _log_execution(
        self,
        job_id: str,
        status: JobStatus,
        started_at: datetime,
        completed_at: Optional[datetime] = None,
        duration_ms: int = 0,
        message: Optional[str] = None,
        error: Optional[str] = None,
        result_data: Optional[Dict[str, Any]] = None,
        triggered_by: str = "scheduled",
        retry_count: int = 0,
    ) -> None:
        """Log a job execution to the database."""
        def _log():
            with sqlite3.connect(str(self._db_path)) as conn:
                conn.execute("""
                    INSERT INTO job_log
                        (job_id, status, started_at, completed_at, duration_ms,
                         message, error, result_data, triggered_by, retry_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    job_id,
                    status.value,
                    started_at.isoformat(),
                    completed_at.isoformat() if completed_at else None,
                    duration_ms,
                    message,
                    error[:500] if error else None,
                    json.dumps(result_data, ensure_ascii=False) if result_data else None,
                    triggered_by,
                    retry_count,
                ))
                conn.commit()

        await asyncio.to_thread(_log)

    async def _update_job_state(
        self,
        job_id: str,
        last_run: datetime,
        last_status: str,
        duration_ms: int,
    ) -> None:
        """Update the persistent state of a job."""
        def _update():
            with sqlite3.connect(str(self._db_path)) as conn:
                conn.execute("""
                    INSERT INTO job_state
                        (job_id, last_run, last_status, last_duration_ms, run_count)
                    VALUES (?, ?, ?, ?, 1)
                    ON CONFLICT(job_id) DO UPDATE SET
                        last_run = excluded.last_run,
                        last_status = excluded.last_status,
                        last_duration_ms = excluded.last_duration_ms,
                        run_count = run_count + 1
                """, (
                    job_id,
                    last_run.isoformat(),
                    last_status,
                    duration_ms,
                ))
                conn.commit()

        await asyncio.to_thread(_update)

    async def enable_job(self, job_id: str) -> None:
        """Enable a job."""
        job = self._jobs.get(job_id)
        if job:
            job.enabled = True
            def _db_enable():
                with sqlite3.connect(str(self._db_path)) as conn:
                    conn.execute(
                        "UPDATE job_state SET enabled = 1 WHERE job_id = ?",
                        (job_id,)
                    )
                    conn.commit()
            await asyncio.to_thread(_db_enable)
            logger.info(f"Enabled job: {job_id}")

    async def disable_job(self, job_id: str) -> None:
        """Disable a job."""
        job = self._jobs.get(job_id)
        if job:
            job.enabled = False
            def _db_disable():
                with sqlite3.connect(str(self._db_path)) as conn:
                    conn.execute(
                        "UPDATE job_state SET enabled = 0 WHERE job_id = ?",
                        (job_id,)
                    )
                    conn.commit()
            await asyncio.to_thread(_db_disable)
            logger.info(f"Disabled job: {job_id}")

    # --- Query Methods ---

    def list_jobs(self) -> List[Dict[str, Any]]:
        """List all registered jobs with their state."""
        result = []
        for job_id, job in self._jobs.items():
            state = self._get_job_state(job_id)
            result.append({
                **job.to_dict(),
                "state": state,
            })
        return result

    def _get_job_state(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get state for a job from the database."""
        with sqlite3.connect(str(self._db_path)) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM job_state WHERE job_id = ?",
                (job_id,)
            ).fetchone()
            if row:
                return dict(row)
        return None

    def get_job_history(
        self,
        job_id: str,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """Get execution history for a job."""
        with sqlite3.connect(str(self._db_path)) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT * FROM job_log
                WHERE job_id = ?
                ORDER BY id DESC
                LIMIT ?
            """, (job_id, limit)).fetchall()
            return [dict(r) for r in rows]

    def get_stats(self) -> Dict[str, Any]:
        """Get scheduler statistics."""
        with sqlite3.connect(str(self._db_path)) as conn:
            total_runs = conn.execute(
                "SELECT COUNT(*) FROM job_log"
            ).fetchone()[0]

            success_count = conn.execute(
                "SELECT COUNT(*) FROM job_log WHERE status = 'success'"
            ).fetchone()[0]

            failure_count = conn.execute(
                "SELECT COUNT(*) FROM job_log WHERE status = 'failed'"
            ).fetchone()[0]

            recent_errors = []
            for row in conn.execute("""
                SELECT job_id, error, started_at
                FROM job_log
                WHERE status = 'failed'
                ORDER BY id DESC
                LIMIT 5
            """):
                recent_errors.append({
                    "job_id": row[0],
                    "error": row[1],
                    "started_at": row[2],
                })

        return {
            "is_running": self._running,
            "registered_jobs": len(self._jobs),
            "total_runs": total_runs,
            "success_count": success_count,
            "failure_count": failure_count,
            "recent_errors": recent_errors,
        }