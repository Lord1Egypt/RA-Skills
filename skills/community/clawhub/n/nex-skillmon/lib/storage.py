#!/usr/bin/env python3
# Nex SkillMon - Storage Module
# MIT-0 License - Copyright 2026 Nex AI

import sqlite3
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import List, Dict, Optional, Any
from contextlib import contextmanager

from .config import DB_PATH, DATA_DIR

logger = logging.getLogger(__name__)


class Storage:
    """Database storage layer for skill monitoring."""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()

    def init_db(self):
        """Initialize database schema."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Skills table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    version TEXT,
                    install_date TEXT,
                    last_updated TEXT,
                    last_triggered TEXT,
                    trigger_count INTEGER DEFAULT 0,
                    skill_path TEXT,
                    file_hash TEXT,
                    description TEXT,
                    author TEXT,
                    homepage TEXT,
                    status TEXT DEFAULT 'active',
                    tags TEXT,
                    notes TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Usage log table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usage_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_id INTEGER NOT NULL,
                    triggered_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    duration_ms INTEGER,
                    tokens_used INTEGER,
                    model_used TEXT,
                    estimated_cost REAL,
                    success BOOLEAN DEFAULT 1,
                    error_message TEXT,
                    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
                )
            """)

            # Cost summary table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cost_summary (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_id INTEGER NOT NULL,
                    period TEXT,
                    period_start TEXT,
                    total_triggers INTEGER DEFAULT 0,
                    total_tokens INTEGER DEFAULT 0,
                    total_cost REAL DEFAULT 0,
                    avg_duration_ms INTEGER DEFAULT 0,
                    success_rate REAL DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
                )
            """)

            # Security checks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS security_checks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_id INTEGER NOT NULL,
                    check_type TEXT,
                    severity TEXT,
                    details TEXT,
                    checked_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    acknowledged BOOLEAN DEFAULT 0,
                    FOREIGN KEY (skill_id) REFERENCES skills(id) ON DELETE CASCADE
                )
            """)

            # Configuration table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS config (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create indices for performance
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_skills_status ON skills(status)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_usage_skill_id ON usage_log(skill_id)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_usage_triggered_at ON usage_log(triggered_at)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_security_skill_id ON security_checks(skill_id)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_security_acknowledged ON security_checks(acknowledged)"
            )

            logger.info("Database initialized")

    def save_skill(self, skill_data: Dict[str, Any]) -> int:
        """Save or update a skill."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()

            # Check if skill exists
            cursor.execute("SELECT id FROM skills WHERE name = ?", (skill_data["name"],))
            existing = cursor.fetchone()

            if existing:
                skill_id = existing["id"]
                cursor.execute(
                    """
                    UPDATE skills SET
                        version = ?, install_date = ?, last_updated = ?,
                        skill_path = ?, file_hash = ?, description = ?,
                        author = ?, homepage = ?, status = ?, tags = ?, notes = ?
                    WHERE id = ?
                    """,
                    (
                        skill_data.get("version"),
                        skill_data.get("install_date"),
                        skill_data.get("last_updated", now),
                        skill_data.get("skill_path"),
                        skill_data.get("file_hash"),
                        skill_data.get("description"),
                        skill_data.get("author"),
                        skill_data.get("homepage"),
                        skill_data.get("status", "active"),
                        skill_data.get("tags"),
                        skill_data.get("notes"),
                        skill_id,
                    ),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO skills
                    (name, version, install_date, last_updated, skill_path,
                     file_hash, description, author, homepage, status, tags, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        skill_data["name"],
                        skill_data.get("version"),
                        skill_data.get("install_date", now),
                        skill_data.get("last_updated", now),
                        skill_data.get("skill_path"),
                        skill_data.get("file_hash"),
                        skill_data.get("description"),
                        skill_data.get("author"),
                        skill_data.get("homepage"),
                        skill_data.get("status", "active"),
                        skill_data.get("tags"),
                        skill_data.get("notes"),
                    ),
                )
                skill_id = cursor.lastrowid

            logger.info(f"Saved skill: {skill_data['name']} (id={skill_id})")
            return skill_id

    def get_skill(self, skill_id: int) -> Optional[Dict[str, Any]]:
        """Get skill by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM skills WHERE id = ?", (skill_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_skill_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get skill by name."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM skills WHERE name = ?", (name,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def list_skills(
        self,
        status: Optional[str] = None,
        stale: bool = False,
        flagged: bool = False,
        stale_days: int = 30,
    ) -> List[Dict[str, Any]]:
        """List skills with optional filters."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM skills WHERE 1=1"
            params = []

            if status:
                query += " AND status = ?"
                params.append(status)

            if flagged:
                query += """
                    AND id IN (
                        SELECT DISTINCT skill_id FROM security_checks
                        WHERE severity = 'critical' AND acknowledged = 0
                    )
                """

            if stale:
                threshold = (
                    datetime.now() - timedelta(days=stale_days)
                ).isoformat()
                query += " AND (last_triggered IS NULL OR last_triggered < ?)"
                params.append(threshold)

            query += " ORDER BY last_triggered DESC NULLS LAST"
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def update_skill(self, skill_id: int, updates: Dict[str, Any]):
        """Update a skill."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            updates["last_updated"] = datetime.now().isoformat()

            set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
            values = list(updates.values()) + [skill_id]

            cursor.execute(
                f"UPDATE skills SET {set_clause} WHERE id = ?", values
            )
            logger.info(f"Updated skill id={skill_id}")

    def log_usage(
        self,
        skill_name: str,
        tokens_used: int,
        model_used: str,
        duration_ms: int,
        success: bool = True,
        error_message: Optional[str] = None,
    ) -> int:
        """Log skill usage."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Get skill ID
            cursor.execute("SELECT id FROM skills WHERE name = ?", (skill_name,))
            skill = cursor.fetchone()
            if not skill:
                raise ValueError(f"Skill not found: {skill_name}")

            skill_id = skill["id"]

            # Estimate cost
            from .cost_tracker import CostTracker

            tracker = CostTracker()
            estimated_cost = float(tracker.estimate_cost(tokens_used, model_used))

            # Insert usage log
            cursor.execute(
                """
                INSERT INTO usage_log
                (skill_id, tokens_used, model_used, duration_ms, estimated_cost, success, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (skill_id, tokens_used, model_used, duration_ms, estimated_cost, success, error_message),
            )

            # Update skill stats
            cursor.execute(
                """
                UPDATE skills SET
                    trigger_count = trigger_count + 1,
                    last_triggered = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (skill_id,),
            )

            logger.info(f"Logged usage for {skill_name}: {tokens_used} tokens")
            return cursor.lastrowid

    def get_skill_usage(
        self, skill_id: int, since: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Get usage logs for a skill."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM usage_log WHERE skill_id = ?"
            params = [skill_id]

            if since:
                query += " AND triggered_at >= ?"
                params.append(since.isoformat())

            query += " ORDER BY triggered_at DESC"
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_cost_summary(
        self, period: str = "monthly", since: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Get cost summaries."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM cost_summary WHERE period = ?"
            params = [period]

            if since:
                query += " AND created_at >= ?"
                params.append(since.isoformat())

            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_stale_skills(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get skills not used in N days."""
        return self.list_skills(stale=True, stale_days=days)

    def get_top_skills_by_cost(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top skills by cost."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT s.*, COALESCE(SUM(ul.estimated_cost), 0) as total_cost
                FROM skills s
                LEFT JOIN usage_log ul ON s.id = ul.skill_id
                GROUP BY s.id
                ORDER BY total_cost DESC
                LIMIT ?
                """,
                (limit,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_top_skills_by_usage(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top skills by usage count."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM skills
                ORDER BY trigger_count DESC
                LIMIT ?
                """,
                (limit,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def save_security_check(
        self,
        skill_id: int,
        check_type: str,
        severity: str,
        details: str,
    ) -> int:
        """Save a security check result."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO security_checks
                (skill_id, check_type, severity, details)
                VALUES (?, ?, ?, ?)
                """,
                (skill_id, check_type, severity, details),
            )
            logger.info(f"Saved security check for skill_id={skill_id}: {check_type}")
            return cursor.lastrowid

    def get_security_alerts(self, unacknowledged: bool = True) -> List[Dict[str, Any]]:
        """Get security alerts."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = """
                SELECT sc.*, s.name as skill_name
                FROM security_checks sc
                JOIN skills s ON sc.skill_id = s.id
            """
            params = []

            if unacknowledged:
                query += " WHERE sc.acknowledged = 0"

            query += " ORDER BY sc.severity DESC, sc.checked_at DESC"
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def acknowledge_alert(self, alert_id: int):
        """Acknowledge an alert."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE security_checks SET acknowledged = 1 WHERE id = ?",
                (alert_id,),
            )
            logger.info(f"Acknowledged alert id={alert_id}")

    def get_skill_health_score(self, skill_id: int) -> int:
        """Calculate skill health score (0-100)."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            skill = self.get_skill(skill_id)
            if not skill:
                return 0

            score = 100
            now = datetime.now()

            # Staleness check
            if skill["last_triggered"]:
                last_triggered = datetime.fromisoformat(skill["last_triggered"])
                days_unused = (now - last_triggered).days
                if days_unused > 30:
                    score -= min(days_unused - 30, 40)
            else:
                score -= 30

            # Error rate check
            usage_logs = self.get_skill_usage(skill_id)
            if usage_logs:
                failures = sum(1 for log in usage_logs if not log["success"])
                error_rate = failures / len(usage_logs)
                score -= int(error_rate * 20)

            # Flagged check
            cursor.execute(
                """
                SELECT COUNT(*) as count FROM security_checks
                WHERE skill_id = ? AND severity = 'critical' AND acknowledged = 0
                """,
                (skill_id,),
            )
            flags = cursor.fetchone()
            if flags["count"] > 0:
                score -= 25

            return max(0, min(100, score))

    def set_config(self, key: str, value: str):
        """Set configuration value."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)",
                (key, value),
            )
            logger.info(f"Set config: {key} = {value}")

    def get_config(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get configuration value."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM config WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row["value"] if row else default

    def export_report(
        self, period: str = "monthly", format: str = "json"
    ) -> Dict[str, Any]:
        """Export comprehensive report."""
        with self.get_connection() as conn:
            skills = self.list_skills()
            usage_logs = []
            security_alerts = self.get_security_alerts(unacknowledged=False)

            for skill in skills:
                usage_logs.extend(self.get_skill_usage(skill["id"]))

            return {
                "period": period,
                "generated_at": datetime.now().isoformat(),
                "skills": [dict(s) for s in skills],
                "usage_logs": usage_logs,
                "security_alerts": security_alerts,
                "format": format,
            }


# Global instance
_storage = None


def get_storage() -> Storage:
    """Get global storage instance."""
    global _storage
    if _storage is None:
        _storage = Storage()
    return _storage
