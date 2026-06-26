"""
Nex Keyring - Storage Module
Database management for secrets, rotation history, and audit logging.
"""

import sqlite3
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Any
from contextlib import contextmanager

from .config import DB_PATH, DATA_DIR, SERVICE_PRESETS, ENCRYPTION_AVAILABLE, ENCRYPTION_METHOD


class Storage:
    """Handle all database operations for Nex Keyring."""

    def __init__(self, db_path: Optional[Path] = None):
        """Initialize storage with database path."""
        self.db_path = db_path or DB_PATH
        self._ensure_db_dir()
        self.init_db()

    def _ensure_db_dir(self):
        """Ensure data directory exists."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if self.db_path.parent != Path.home():
            self.db_path.parent.chmod(0o700)

    @contextmanager
    def _get_connection(self):
        """Get database connection."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_db(self):
        """Initialize database schema."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Secrets table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS secrets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    service TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT,
                    key_prefix TEXT,
                    key_hash TEXT UNIQUE,
                    created_date TEXT NOT NULL,
                    last_rotated TEXT,
                    rotation_policy_days INTEGER DEFAULT 90,
                    auto_check_env_var TEXT,
                    env_file_path TEXT,
                    status TEXT DEFAULT 'active',
                    used_in TEXT,
                    tags TEXT,
                    notes TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)

            # Rotation history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rotation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    secret_id INTEGER NOT NULL,
                    rotated_at TEXT NOT NULL,
                    old_key_hash TEXT,
                    new_key_hash TEXT,
                    rotated_by TEXT DEFAULT 'manual',
                    notes TEXT,
                    FOREIGN KEY (secret_id) REFERENCES secrets(id) ON DELETE CASCADE
                )
            """)

            # Audit log table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    secret_id INTEGER,
                    action TEXT NOT NULL,
                    details TEXT,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (secret_id) REFERENCES secrets(id) ON DELETE SET NULL
                )
            """)

            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_secrets_service ON secrets(service)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_secrets_category ON secrets(category)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_secrets_status ON secrets(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_rotation_history_secret ON rotation_history(secret_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_log_secret ON audit_log(secret_id)")

    def save_secret(self, secret_data: Dict[str, Any]) -> int:
        """Save or update a secret."""
        now = datetime.now().isoformat()

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Check if secret exists
            cursor.execute("SELECT id FROM secrets WHERE name = ?", (secret_data["name"],))
            existing = cursor.fetchone()

            if existing:
                secret_id = existing[0]
                # Update existing secret
                cursor.execute("""
                    UPDATE secrets SET
                        service = ?,
                        category = ?,
                        description = ?,
                        key_prefix = ?,
                        key_hash = ?,
                        rotation_policy_days = ?,
                        auto_check_env_var = ?,
                        env_file_path = ?,
                        status = ?,
                        used_in = ?,
                        tags = ?,
                        notes = ?,
                        updated_at = ?
                    WHERE id = ?
                """, (
                    secret_data.get("service", ""),
                    secret_data.get("category", "OTHER"),
                    secret_data.get("description"),
                    secret_data.get("key_prefix"),
                    secret_data.get("key_hash"),
                    secret_data.get("rotation_policy_days", 90),
                    secret_data.get("auto_check_env_var"),
                    secret_data.get("env_file_path"),
                    secret_data.get("status", "active"),
                    secret_data.get("used_in"),
                    secret_data.get("tags"),
                    secret_data.get("notes"),
                    now,
                    secret_id
                ))
            else:
                # Insert new secret
                cursor.execute("""
                    INSERT INTO secrets (
                        name, service, category, description, key_prefix, key_hash,
                        created_date, last_rotated, rotation_policy_days,
                        auto_check_env_var, env_file_path, status, used_in, tags, notes,
                        created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    secret_data["name"],
                    secret_data.get("service", ""),
                    secret_data.get("category", "OTHER"),
                    secret_data.get("description"),
                    secret_data.get("key_prefix"),
                    secret_data.get("key_hash"),
                    secret_data.get("created_date", now),
                    secret_data.get("last_rotated"),
                    secret_data.get("rotation_policy_days", 90),
                    secret_data.get("auto_check_env_var"),
                    secret_data.get("env_file_path"),
                    secret_data.get("status", "active"),
                    secret_data.get("used_in"),
                    secret_data.get("tags"),
                    secret_data.get("notes"),
                    now,
                    now
                ))
                secret_id = cursor.lastrowid

            # Add audit log entry in same transaction
            self._audit_log_entry_internal(cursor, secret_id, "added", json.dumps(secret_data))
            return secret_id

    def _audit_log_entry_internal(self, cursor, secret_id: Optional[int], action: str, details: Optional[str] = None):
        """Add audit log entry (internal, uses existing cursor)."""
        now = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO audit_log (secret_id, action, details, timestamp)
            VALUES (?, ?, ?, ?)
        """, (secret_id, action, details, now))

    def get_secret(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a secret by name."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM secrets WHERE name = ?", (name,))
            row = cursor.fetchone()

            if row:
                cursor.execute("""
                    INSERT INTO audit_log (secret_id, action, details, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (row["id"], "viewed", None, datetime.now().isoformat()))
                return dict(row)
            return None

    def list_secrets(
        self,
        service: Optional[str] = None,
        category: Optional[str] = None,
        stale: bool = False,
        overdue: bool = False,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List secrets with optional filters."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM secrets WHERE 1=1"
            params = []

            if service:
                query += " AND service = ?"
                params.append(service)

            if category:
                query += " AND category = ?"
                params.append(category)

            if status:
                query += " AND status = ?"
                params.append(status)
            else:
                query += " AND status = 'active'"

            query += " ORDER BY name ASC"

            cursor.execute(query, params)
            secrets = [dict(row) for row in cursor.fetchall()]

            # Post-filter for stale/overdue if needed
            if stale or overdue:
                now = datetime.now()
                filtered = []

                for secret in secrets:
                    if secret["last_rotated"]:
                        last_rotated = datetime.fromisoformat(secret["last_rotated"])
                        days_since = (now - last_rotated).days
                        policy_days = secret["rotation_policy_days"]

                        if stale and days_since > 90:
                            filtered.append(secret)
                        elif overdue and days_since > policy_days:
                            filtered.append(secret)
                    elif overdue:
                        # No rotation record = potentially overdue
                        created = datetime.fromisoformat(secret["created_date"])
                        days_since = (now - created).days
                        if days_since > secret["rotation_policy_days"]:
                            filtered.append(secret)

                secrets = filtered

            return secrets

    def update_secret(self, name: str, updates: Dict[str, Any]) -> bool:
        """Update a secret."""
        secret = self.get_secret(name)
        if not secret:
            return False

        secret_id = secret["id"]
        now = datetime.now().isoformat()

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Build dynamic update
            set_clause = []
            params = []

            for key, value in updates.items():
                if key in ["service", "category", "description", "status", "tags", "notes", "used_in"]:
                    set_clause.append(f"{key} = ?")
                    params.append(value)

            set_clause.append("updated_at = ?")
            params.append(now)
            params.append(secret_id)

            if set_clause:
                query = f"UPDATE secrets SET {', '.join(set_clause)} WHERE id = ?"
                cursor.execute(query, params)
                self._audit_log_entry_internal(cursor, secret_id, "updated", json.dumps(updates))
                return True

        return False

    def delete_secret(self, name: str) -> bool:
        """Delete a secret."""
        secret = self.get_secret(name)
        if not secret:
            return False

        secret_id = secret["id"]

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM secrets WHERE id = ?", (secret_id,))
            self._audit_log_entry_internal(cursor, secret_id, "removed", "Secret deleted")
            return True

    def record_rotation(self, secret_id: int, old_hash: Optional[str] = None,
                       new_hash: Optional[str] = None, notes: Optional[str] = None) -> int:
        """Record a rotation event."""
        now = datetime.now().isoformat()

        with self._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO rotation_history (secret_id, rotated_at, old_key_hash, new_key_hash, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (secret_id, now, old_hash, new_hash, notes))

            # Update last_rotated
            cursor.execute("UPDATE secrets SET last_rotated = ? WHERE id = ?", (now, secret_id))

            self._audit_log_entry_internal(cursor, secret_id, "rotated", f"Hash: {new_hash}")
            return cursor.lastrowid

    def get_rotation_history(self, secret_id: int) -> List[Dict[str, Any]]:
        """Get rotation history for a secret."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM rotation_history WHERE secret_id = ?
                ORDER BY rotated_at DESC
            """, (secret_id,))
            return [dict(row) for row in cursor.fetchall()]

    def get_stale_secrets(self, days: int = 90) -> List[Dict[str, Any]]:
        """Get secrets not rotated in specified days."""
        now = datetime.now()
        threshold = now - timedelta(days=days)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM secrets
                WHERE status = 'active' AND (
                    last_rotated IS NULL OR
                    datetime(last_rotated) < datetime(?)
                )
                ORDER BY last_rotated ASC
            """, (threshold.isoformat(),))
            return [dict(row) for row in cursor.fetchall()]

    def get_overdue_secrets(self) -> List[Dict[str, Any]]:
        """Get secrets overdue for rotation based on their policy."""
        now = datetime.now()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM secrets
                WHERE status = 'active'
                ORDER BY last_rotated ASC, created_date ASC
            """)

            overdue = []
            for row in cursor.fetchall():
                secret = dict(row)
                policy_days = secret["rotation_policy_days"]

                if secret["last_rotated"]:
                    last_rotated = datetime.fromisoformat(secret["last_rotated"])
                    days_since = (now - last_rotated).days
                    if days_since > policy_days:
                        overdue.append(secret)
                else:
                    # No rotation recorded
                    created = datetime.fromisoformat(secret["created_date"])
                    days_since = (now - created).days
                    if days_since > policy_days:
                        overdue.append(secret)

            return overdue

    def get_secret_stats(self) -> Dict[str, Any]:
        """Get statistics about tracked secrets."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Total count
            cursor.execute("SELECT COUNT(*) as count FROM secrets WHERE status = 'active'")
            total = cursor.fetchone()["count"]

            # By category
            cursor.execute("""
                SELECT category, COUNT(*) as count
                FROM secrets WHERE status = 'active'
                GROUP BY category
                ORDER BY count DESC
            """)
            by_category = {row["category"]: row["count"] for row in cursor.fetchall()}

            # By service
            cursor.execute("""
                SELECT service, COUNT(*) as count
                FROM secrets WHERE status = 'active'
                GROUP BY service
                ORDER BY count DESC
            """)
            by_service = {row["service"]: row["count"] for row in cursor.fetchall()}

            # Risk levels
            stale = len(self.get_stale_secrets(90))
            overdue = len(self.get_overdue_secrets())

            return {
                "total": total,
                "by_category": by_category,
                "by_service": by_service,
                "stale_count": stale,
                "overdue_count": overdue,
            }

    def search_secrets(self, query: str) -> List[Dict[str, Any]]:
        """Search secrets by name, service, or description."""
        search_term = f"%{query}%"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM secrets
                WHERE status = 'active' AND (
                    name LIKE ? OR
                    service LIKE ? OR
                    description LIKE ? OR
                    tags LIKE ?
                )
                ORDER BY name ASC
            """, (search_term, search_term, search_term, search_term))
            return [dict(row) for row in cursor.fetchall()]

    def audit_log_entry(self, secret_id: Optional[int], action: str, details: Optional[str] = None):
        """Add audit log entry."""
        now = datetime.now().isoformat()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO audit_log (secret_id, action, details, timestamp)
                VALUES (?, ?, ?, ?)
            """, (secret_id, action, details, now))

    def get_audit_log(self, limit: int = 100, secret_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get audit log entries."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            if secret_id:
                cursor.execute("""
                    SELECT * FROM audit_log
                    WHERE secret_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (secret_id, limit))
            else:
                cursor.execute("""
                    SELECT * FROM audit_log
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (limit,))

            return [dict(row) for row in cursor.fetchall()]

    def export_secrets(self, format: str = "json", exclude_sensitive: bool = True) -> str:
        """Export secrets in specified format."""
        secrets = self.list_secrets()

        if format == "json":
            return json.dumps([
                {k: v for k, v in dict(s).items() if k not in ["key_hash"] or not exclude_sensitive}
                for s in secrets
            ], indent=2)

        elif format == "csv":
            import csv
            from io import StringIO

            output = StringIO()
            if secrets:
                fieldnames = [k for k in secrets[0].keys() if k not in ["key_hash"] or not exclude_sensitive]
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                for secret in secrets:
                    writer.writerow({k: v for k, v in dict(secret).items() if k in fieldnames})

            return output.getvalue()

        elif format == "markdown":
            lines = ["# Nex Keyring Export\n"]
            lines.append(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            lines.append("## Tracked Secrets\n")

            for secret in secrets:
                lines.append(f"### {secret['name']}\n")
                lines.append(f"- Service: {secret['service']}\n")
                lines.append(f"- Category: {secret['category']}\n")
                lines.append(f"- Created: {secret['created_date']}\n")
                lines.append(f"- Last Rotated: {secret['last_rotated'] or 'Never'}\n")
                lines.append(f"- Status: {secret['status']}\n")
                if secret['description']:
                    lines.append(f"- Description: {secret['description']}\n")
                lines.append("")

            return "\n".join(lines)

        return ""
