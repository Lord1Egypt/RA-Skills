#!/usr/bin/env python3
"""
Dream Consolidator
==================
Main orchestrator for nightly memory consolidation.

Coordinates pattern detection, insight generation, and narrative creation
by delegating to specialized modules while managing state persistence.

The DreamConsolidator class provides:
  - State management (loading/saving insights, patterns, dream log)
  - Orchestration of pattern detection and insight generation
  - Database persistence
  - Query helpers for historical data

Usage:
    dc = DreamConsolidator(db_path="~/.nima/memory/nima.sqlite", bot_name="mybot")
    result = dc.run(hours=24, verbose=True)
    print(result["summary"])

Environment:
    NIMA_DB_PATH         Path to SQLite database
    NIMA_DATA_DIR        Base data directory (default: ~/.nima)
    NIMA_BOT_NAME        Bot identity (default: bot)
    NIMA_DREAM_HOURS     Lookback window in hours (default: 24)
    NIMA_MAX_INSIGHTS    Max insights to keep in memory (default: 500)
    NIMA_MAX_PATTERNS    Max patterns to keep in memory (default: 200)
    NIMA_MAX_DREAM_LOG   Max dream sessions to keep in log (default: 100)

Author: Lilu / nima-core
"""

from __future__ import annotations

import os
import json
import hashlib
import sqlite3
import logging
import threading
from pathlib import Path
from datetime import datetime, timedelta, timezone
from collections import Counter, deque
from typing import Dict, List, Optional, Union

from .models import Insight, Pattern, DreamSession, _utcnow, _now_str, _atomic_write_json
from .domain_classifier import classify_domain, DOMAINS
from .pattern_detector import PatternDetector
from .insight_generator import InsightGenerator
from .narrative_generator import generate_dream_narrative, save_dream_markdown
from .db_operations import open_connection, ensure_tables, load_memories, load_sqlite_turns
from .vsa_blender import blend_dream_vector, has_numpy

__all__ = [
    "DreamConsolidator",
    "MAX_INSIGHTS",
    "MAX_PATTERNS",
    "MAX_DREAM_LOG",
    "DEFAULT_HOURS",
]

logger = logging.getLogger(__name__)


# ── Paths ─────────────────────────────────────────────────────────────────────

def _base_dir() -> Path:
    """Get base data directory from environment or default to ~/.nima"""
    return Path(os.environ.get("NIMA_DATA_DIR", Path.home() / ".nima"))


def _default_db() -> Path:
    """Get default database path from environment or default location"""
    return Path(os.environ.get("NIMA_DB_PATH",
                               _base_dir() / "memory" / "nima.sqlite"))


def _dreams_dir() -> Path:
    """Get dreams directory, creating it if needed"""
    d = _base_dir() / "dreams"
    d.mkdir(parents=True, exist_ok=True)
    return d


# ── Constants ─────────────────────────────────────────────────────────────────

MAX_INSIGHTS    = int(os.environ.get("NIMA_MAX_INSIGHTS", 500))
MAX_PATTERNS    = int(os.environ.get("NIMA_MAX_PATTERNS", 200))
MAX_DREAM_LOG   = int(os.environ.get("NIMA_MAX_DREAM_LOG", 100))
DEFAULT_HOURS   = int(os.environ.get("NIMA_DREAM_HOURS", 24))


# ── DreamConsolidator ─────────────────────────────────────────────────────────

class DreamConsolidator:
    """
    Full-featured nightly memory consolidation.

    Orchestrates pattern detection, insight generation, and narrative creation
    by delegating to specialized modules. Manages state persistence and provides
    query helpers for historical data.

    Example::

        dc = DreamConsolidator(db_path="~/.nima/memory/nima.sqlite", bot_name="mybot")
        result = dc.run(hours=24, verbose=True)
        print(result["summary"])
    """

    # DOMAINS exposed as class attr so subclasses can extend them
    DOMAINS: Dict[str, List[str]] = DOMAINS

    def __init__(
        self,
        db_path: Optional[Union[str, Path]] = None,
        bot_name: str = "bot",
        dry_run: bool = False,
        data_dir: Optional[Union[str, Path]] = None,
    ):
        """
        Initialize the DreamConsolidator.

        Args:
            db_path: Path to SQLite database (default: from env or ~/.nima/memory/nima.sqlite)
            bot_name: Bot identity for multi-bot environments (default: "bot")
            dry_run: If True, skip database writes and external API calls
            data_dir: Base data directory (default: from env or ~/.nima)
        """
        self.db_path  = Path(db_path or _default_db()).expanduser()
        self.bot_name = bot_name or os.environ.get("NIMA_BOT_NAME", "bot")
        self.dry_run  = dry_run
        self.data_dir = Path(data_dir or _base_dir()).expanduser()

        # State files
        self._dreams_dir   = self.data_dir / "dreams"
        self._insights_f   = self._dreams_dir / "insights.json"
        self._patterns_f   = self._dreams_dir / "patterns.json"
        self._dream_log_f  = self._dreams_dir / "dream_log.json"
        self._dreams_dir.mkdir(parents=True, exist_ok=True)

        # Bounded in-memory state (deques auto-prune oldest)
        self.insights:   deque = deque(maxlen=MAX_INSIGHTS)
        self.patterns:   deque = deque(maxlen=MAX_PATTERNS)
        self.dream_log:  deque = deque(maxlen=MAX_DREAM_LOG)

        self._lock = threading.Lock()
        self._load_state()

    # ── State persistence ─────────────────────────────────────────────────────

    def _load_json_deque(self, attr: str, filepath: "Path", cls) -> None:
        """Load a JSON-persisted deque of *cls* objects into ``self.<attr>``."""
        if not filepath.exists():
            return
        try:
            data = json.loads(filepath.read_text())
            for item in data.get(attr, []):
                try:
                    getattr(self, attr).append(cls.from_dict(item))
                except (TypeError, KeyError):
                    pass
            logger.debug(f"Loaded {len(getattr(self, attr))} {attr}")
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Could not load {attr}: {e}")

    def _load_dream_log_state(self) -> None:
        """Load persisted DreamSession records from the dream-log JSON file."""
        if not self._dream_log_f.exists():
            return
        try:
            data = json.loads(self._dream_log_f.read_text())
            for s in data.get("sessions", []):
                try:
                    self.dream_log.append(DreamSession.from_dict(s))
                except (TypeError, KeyError):
                    pass
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Could not load dream log: {e}")

    def _load_state(self) -> None:
        """Load persisted insights, patterns, and dream log from JSON files."""
        self._load_json_deque("insights", self._insights_f,  Insight)
        self._load_json_deque("patterns", self._patterns_f,  Pattern)
        self._load_dream_log_state()

    def _save_state(self) -> None:
        """Persist insights, patterns, and dream log to JSON files atomically."""
        if self.dry_run:
            return
        with self._lock:
            _atomic_write_json(self._insights_f,  {"insights":  [i.to_dict() for i in self.insights],  "updated": _now_str()})
            _atomic_write_json(self._patterns_f,  {"patterns":  [p.to_dict() for p in self.patterns],  "updated": _now_str()})
            _atomic_write_json(self._dream_log_f, {"sessions":  [s.to_dict() for s in self.dream_log], "updated": _now_str()})

    # ── DB persistence ────────────────────────────────────────────────────────

    def _save_to_db(
        self,
        conn: sqlite3.Connection,
        insights: List[Insight],
        patterns: List[Pattern],
        session: DreamSession,
    ) -> None:
        """Persist insights, patterns, and session to database."""
        for ins in insights:
            conn.execute("""
                INSERT OR REPLACE INTO nima_insights
                (id, type, content, confidence, sources, domains,
                 timestamp, importance, bot_name)
                VALUES (?,?,?,?,?,?,?,?,?)
            """, (ins.id, ins.type, ins.content, ins.confidence,
                  json.dumps(ins.sources), json.dumps(ins.domains),
                  ins.timestamp, ins.importance, self.bot_name))

        for p in patterns:
            conn.execute("""
                INSERT OR REPLACE INTO nima_patterns
                (id, name, description, occurrences, domains, examples,
                 first_seen, last_seen, strength, bot_name)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """, (p.id, p.name, p.description, p.occurrences,
                  json.dumps(p.domains), json.dumps(p.examples),
                  p.first_seen, p.last_seen, p.strength, self.bot_name))

        conn.execute("""
            INSERT INTO nima_dream_runs
            (session_id, started_at, ended_at, hours, memories_processed,
             patterns_found, insights_generated, top_domains,
             dominant_emotion, narrative, bot_name)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (session.id, session.started_at, session.ended_at,
              session.hours, session.memories_processed,
              session.patterns_found, session.insights_generated,
              json.dumps(session.top_domains), session.dominant_emotion,
              session.narrative, self.bot_name))

        conn.commit()

    # ── Internal helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _compute_top_domains(memories: list) -> list:
        """Return the top 3 domain labels across all memories."""
        domain_counter: Counter = Counter()
        for m in memories:
            text = (m.get("text") or m.get("summary") or "")
            for d in classify_domain(text):
                domain_counter[d] += 1
        return [d for d, _ in domain_counter.most_common(3)]

    @staticmethod
    def _compute_dominant_emotion(memories: list):
        """Return the most frequent dominant_emotion across memories, or None."""
        emotion_counter: Counter = Counter()
        for m in memories:
            e = m.get("dominant_emotion")
            if e:
                emotion_counter[e] += 1
        return emotion_counter.most_common(1)[0][0] if emotion_counter else None

    def _build_run_result(
        self,
        session_id: str,
        memories: list,
        new_patterns: list,
        new_insights: list,
        top_domains: list,
        dominant_emotion,
        narrative,
        darwin_stats: dict,
        summary: str,
    ) -> Dict:
        """Assemble and return the result dict from a completed run."""
        return {
            "session_id":       session_id,
            "memories_in":      len(memories),
            "patterns":         len(new_patterns),
            "insights":         len(new_insights),
            "top_domains":      top_domains,
            "dominant_emotion": dominant_emotion,
            "narrative":        narrative,
            "vsa_available":    has_numpy(),
            "insight_details": [
                {"type": i.type, "domain": i.domains, "content": i.content[:120]}
                for i in new_insights
            ],
            "pattern_details": [
                {"name": p.name, "strength": p.strength, "occurrences": p.occurrences}
                for p in new_patterns[:10]
            ],
            "summary":   summary,
            "dry_run":   self.dry_run,
            "darwinism": darwin_stats,
        }

    def _persist_run(
        self,
        conn: sqlite3.Connection,
        new_insights: List[Insight],
        new_patterns: List[Pattern],
        session: DreamSession,
        narrative: Optional[str],
        verbose: bool,
    ) -> None:
        """Write run results to DB, state files, markdown journal, and optional DB sync."""
        self._save_to_db(conn, new_insights, new_patterns, session)
        self._save_state()
        if narrative:
            save_dream_markdown(narrative, session, self._dreams_dir)
        try:
            from nima_core.dream_db_sync import sync_all as dream_sync
            sync_results = dream_sync(verbose=verbose)
            if verbose:
                logger.info(f"Dream DB sync: {sync_results}")
        except Exception as sync_err:
            logger.warning(f"Dream DB sync failed (non-fatal): {sync_err}")

    def _run_darwinism(self, verbose: bool) -> Dict:
        """Run Darwinian memory consolidation; return stats dict."""
        stats = {"clusters_found": 0, "ghosted": 0}
        try:
            from nima_core.darwinism import DarwinianEngine
            if str(self.db_path).endswith(".lbug"):
                darwin = DarwinianEngine(
                    db_path=str(self.db_path),
                    skip_llm=False,
                    dry_run=False,
                )
                stats = darwin.run_cycle(seeds=5)
            elif verbose:
                logger.info("Darwinism skipped: non-Ladybug DB path")
            if verbose:
                logger.info(
                    f"Darwinism: {stats['clusters_found']} clusters, "
                    f"{stats['ghosted']} memories ghosted."
                )
        except Exception as e:
            logger.warning(f"Darwinian cycle skipped: {e}")
        return stats

    # ── Main run ──────────────────────────────────────────────────────────────

    def _load_memories_from_conn(self, conn, hours: int, verbose: bool) -> list:
        """Load memories from *conn* using both table schemas.

        Returns the memory list, or an empty list if nothing is found.
        Logs the count when *verbose* is True.
        """
        memories = load_memories(conn, hours)
        if not memories:
            memories = load_sqlite_turns(conn, hours)
        if memories and verbose:
            logger.info(f"Loaded {len(memories)} memories ({hours}h window).")
        return memories

    def _blend_vsa_vector(self, memories: list, verbose: bool):
        """Blend a VSA dream vector from available embeddings (requires numpy).

        Returns the blended vector, or None when numpy is unavailable or no
        embeddings are present.  The return value is reserved for future use
        (pattern anchoring, etc.).
        """
        if not has_numpy():
            return None
        embeddings = [m.get("embedding") for m in memories if m.get("embedding")]
        if not embeddings:
            return None
        vector = blend_dream_vector(embeddings)
        if verbose:
            logger.info(f"VSA dream vector blended from {len(embeddings)} embeddings.")
        return vector

    def _detect_patterns_and_insights(self, memories: list, verbose: bool):
        """Run pattern detection and insight generation on *memories*.

        Syncs the updated pattern deque back to *self.patterns* and extends
        *self.insights* with the new insights.

        Returns ``(new_patterns, new_insights)``.
        """
        detector = PatternDetector(list(self.patterns))
        new_patterns = detector.detect_patterns(memories)
        self.patterns = deque(detector.patterns, maxlen=MAX_PATTERNS)
        if verbose:
            logger.info(f"Found {len(new_patterns)} new patterns.")

        generator = InsightGenerator()
        new_insights = generator.generate_insights(memories, new_patterns)
        new_insights += generator.generate_connections(memories)
        self.insights.extend(new_insights)
        if verbose:
            logger.info(f"Generated {len(new_insights)} insights.")

        return new_patterns, new_insights

    def _build_session_and_persist(
        self, conn, memories, new_patterns, new_insights,
        session_id: str, started_at: str,
        top_domains, dominant_emotion, narrative, hours: int, verbose: bool,
    ) -> "DreamSession":
        """Construct a DreamSession record, append it to the log, and persist it.

        Returns the created :class:`DreamSession`.
        """
        ended_at = _now_str()
        session = DreamSession(
            id=session_id,
            started_at=started_at,
            ended_at=ended_at,
            hours=hours,
            memories_processed=len(memories),
            patterns_found=len(new_patterns),
            insights_generated=len(new_insights),
            top_domains=top_domains,
            dominant_emotion=dominant_emotion,
            narrative=narrative,
            bot_name=self.bot_name,
        )
        self.dream_log.append(session)
        if not self.dry_run:
            self._persist_run(conn, new_insights, new_patterns, session, narrative, verbose)
        return session

    def _build_run_summary(
        self, memories, new_patterns, new_insights,
        top_domains, dominant_emotion, hours: int, verbose: bool,
    ) -> str:
        """Build the human-readable consolidation summary string."""
        summary = (
            f"Consolidated {len(memories)} memories over {hours}h. "
            f"Found {len(new_patterns)} patterns, {len(new_insights)} insights. "
            f"Top domains: {', '.join(top_domains)}. "
            f"Dominant emotion: {dominant_emotion or 'neutral'}."
        )
        if self.dry_run:
            summary = "[DRY RUN] " + summary
        if verbose:
            logger.info(summary)
        return summary

    def run(self, hours: int = DEFAULT_HOURS, verbose: bool = False) -> Dict:
        """
        Run a full dream consolidation cycle.

        This orchestrates the entire consolidation pipeline:
          1. Load memories from database
          2. (Optional) Blend VSA dream vector from embeddings
          3. Detect patterns using PatternDetector
          4. Generate insights using InsightGenerator
          5. Calculate top domains and dominant emotion
          6. (Optional) Generate LLM dream narrative
          7. Persist to database and JSON files
          8. (Optional) Sync to LadybugDB
          9. (Optional) Run Darwinian memory consolidation

        Args:
            hours: Lookback window in hours (default: from env or 24)
            verbose: If True, log progress messages

        Returns:
            Dict with: memories_in, patterns, insights, session_id,
                       summary, top_domains, dominant_emotion, narrative,
                       vsa_available, insight_details, pattern_details,
                       dry_run, darwinism
        """
        if not self.db_path.exists():
            summary = f"Database not found: {self.db_path}"
            if self.dry_run:
                summary = "[DRY RUN] " + summary
            return {
                "memories_in": 0,
                "patterns": 0,
                "insights": 0,
                "summary": summary,
                "dry_run": self.dry_run,
            }

        session_id  = hashlib.sha256(f"{self.bot_name}{_utcnow()}".encode()).hexdigest()[:12]
        started_at  = _now_str()

        conn = open_connection(self.db_path)
        try:
            ensure_tables(conn)

            # 1. Load memories from both table schemas
            memories = self._load_memories_from_conn(conn, hours, verbose)
            if not memories:
                return {
                    "memories_in": 0, "patterns": 0, "insights": 0,
                    "summary": "No memories to consolidate.",
                    "dry_run": self.dry_run,
                }

            # 2. VSA dream vector (optional, requires numpy)
            # NOTE: dream_vector is computed for future use (pattern anchoring, etc.)
            _dream_vector = self._blend_vsa_vector(memories, verbose)

            # 3–4. Pattern detection + insight generation
            new_patterns, new_insights = self._detect_patterns_and_insights(memories, verbose)

            # 5. Top domains / dominant emotion
            top_domains = self._compute_top_domains(memories)
            dominant_emotion = self._compute_dominant_emotion(memories)

            # 6. Dream narrative (optional LLM)
            narrative = None
            if not self.dry_run:
                theme     = top_domains[0] if top_domains else "memory"
                narrative = generate_dream_narrative(memories, theme)
                if narrative and verbose:
                    logger.info("Dream narrative generated.")

            # 7–8. Build session record and persist
            self._build_session_and_persist(
                conn, memories, new_patterns, new_insights,
                session_id, started_at,
                top_domains, dominant_emotion, narrative, hours, verbose,
            )

            # 9. Darwinian selection — merge near-duplicate memories
            darwin_stats = {"clusters_found": 0, "ghosted": 0}
            if not self.dry_run:
                darwin_stats = self._run_darwinism(verbose)

            # 10. Summary
            summary = self._build_run_summary(
                memories, new_patterns, new_insights,
                top_domains, dominant_emotion, hours, verbose,
            )

            return self._build_run_result(
                session_id, memories, new_patterns, new_insights,
                top_domains, dominant_emotion, narrative, darwin_stats, summary,
            )
        finally:
            conn.close()

    # ── Query helpers ─────────────────────────────────────────────────────────

    def last_runs(self, limit: int = 5) -> List[Dict]:
        """Return last N consolidation sessions."""
        if not self.db_path.exists():
            return []
        conn = open_connection(self.db_path)
        try:
            ensure_tables(conn)
            rows = conn.execute("""
                SELECT * FROM nima_dream_runs
                ORDER BY started_at DESC LIMIT ?
            """, (limit,)).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def recent_insights(self, hours: int = 48, limit: int = 20) -> List[Dict]:
        """Return recently generated insights ordered by importance."""
        if not self.db_path.exists():
            return []
        since = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
        conn  = open_connection(self.db_path)
        try:
            ensure_tables(conn)
            rows = conn.execute("""
                SELECT * FROM nima_insights
                WHERE timestamp >= ?
                ORDER BY importance DESC, confidence DESC
                LIMIT ?
            """, (since, limit)).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def active_patterns(self, min_strength: float = 0.4, limit: int = 20) -> List[Dict]:
        """Return patterns above a strength threshold."""
        if not self.db_path.exists():
            return []
        conn = open_connection(self.db_path)
        try:
            ensure_tables(conn)
            rows = conn.execute("""
                SELECT * FROM nima_patterns
                WHERE strength >= ?
                ORDER BY strength DESC, occurrences DESC
                LIMIT ?
            """, (min_strength, limit)).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def today_journal(self) -> Optional[str]:
        """Return today's dream journal markdown, if it exists."""
        date_str = datetime.now().strftime("%Y-%m-%d")
        filepath  = self._dreams_dir / f"{date_str}.md"
        return filepath.read_text() if filepath.exists() else None
