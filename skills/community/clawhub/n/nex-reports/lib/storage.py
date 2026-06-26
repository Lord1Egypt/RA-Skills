"""
Nex Reports - Storage & Database
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from .config import DB_PATH, DB_SCHEMA, DATA_DIR, REPORTS_DIR, TEMPLATES_DIR


class ReportDatabase:
    """SQLite database interface for report configs and runs."""

    def __init__(self):
        self.db_path = DB_PATH
        self._ensure_initialized()

    def _ensure_initialized(self):
        """Create data directories and initialize database."""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

        if not self.db_path.exists():
            conn = sqlite3.connect(self.db_path)
            conn.executescript(DB_SCHEMA)
            conn.commit()
            conn.close()

    def _get_conn(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> bool:
        """Initialize database. Idempotent."""
        try:
            self._ensure_initialized()
            return True
        except Exception as e:
            print(f"Error initializing database: {e}")
            return False

    def save_config(
        self,
        name: str,
        schedule: str,
        modules: List[Dict[str, Any]],
        output_format: str,
        output_target: str,
        enabled: bool = True,
    ) -> Optional[int]:
        """Save report config. Returns config_id or None on error."""
        try:
            conn = self._get_conn()
            now = datetime.utcnow().isoformat()

            conn.execute(
                """
                INSERT INTO report_configs
                (name, schedule, modules, output_format, output_target, enabled, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    schedule,
                    json.dumps(modules),
                    output_format,
                    output_target,
                    1 if enabled else 0,
                    now,
                    now,
                ),
            )
            conn.commit()
            config_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            conn.close()
            return config_id
        except sqlite3.IntegrityError:
            return None  # Name already exists
        except Exception as e:
            print(f"Error saving config: {e}")
            return None

    def get_config(self, name: str) -> Optional[Dict[str, Any]]:
        """Get report config by name."""
        try:
            conn = self._get_conn()
            row = conn.execute(
                "SELECT * FROM report_configs WHERE name = ?", (name,)
            ).fetchone()
            conn.close()

            if not row:
                return None

            return {
                "id": row["id"],
                "name": row["name"],
                "schedule": row["schedule"],
                "modules": json.loads(row["modules"]),
                "output_format": row["output_format"],
                "output_target": row["output_target"],
                "enabled": bool(row["enabled"]),
                "last_run": row["last_run"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
        except Exception as e:
            print(f"Error getting config: {e}")
            return None

    def list_configs(self) -> List[Dict[str, Any]]:
        """List all report configs."""
        try:
            conn = self._get_conn()
            rows = conn.execute(
                "SELECT * FROM report_configs ORDER BY name"
            ).fetchall()
            conn.close()

            configs = []
            for row in rows:
                configs.append(
                    {
                        "id": row["id"],
                        "name": row["name"],
                        "schedule": row["schedule"],
                        "modules": json.loads(row["modules"]),
                        "output_format": row["output_format"],
                        "output_target": row["output_target"],
                        "enabled": bool(row["enabled"]),
                        "last_run": row["last_run"],
                        "created_at": row["created_at"],
                    }
                )
            return configs
        except Exception as e:
            print(f"Error listing configs: {e}")
            return []

    def update_config(
        self,
        name: str,
        schedule: Optional[str] = None,
        modules: Optional[List[Dict[str, Any]]] = None,
        output_format: Optional[str] = None,
        output_target: Optional[str] = None,
        enabled: Optional[bool] = None,
    ) -> bool:
        """Update report config. Returns True on success."""
        try:
            conn = self._get_conn()
            updates = []
            params = []

            if schedule is not None:
                updates.append("schedule = ?")
                params.append(schedule)
            if modules is not None:
                updates.append("modules = ?")
                params.append(json.dumps(modules))
            if output_format is not None:
                updates.append("output_format = ?")
                params.append(output_format)
            if output_target is not None:
                updates.append("output_target = ?")
                params.append(output_target)
            if enabled is not None:
                updates.append("enabled = ?")
                params.append(1 if enabled else 0)

            if updates:
                updates.append("updated_at = ?")
                params.append(datetime.utcnow().isoformat())
                params.append(name)

                sql = f"UPDATE report_configs SET {', '.join(updates)} WHERE name = ?"
                conn.execute(sql, params)
                conn.commit()

            conn.close()
            return True
        except Exception as e:
            print(f"Error updating config: {e}")
            return False

    def delete_config(self, name: str) -> bool:
        """Delete report config by name."""
        try:
            conn = self._get_conn()
            conn.execute("DELETE FROM report_configs WHERE name = ?", (name,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting config: {e}")
            return False

    def save_run(
        self,
        config_id: int,
        started_at: str,
        status: str,
        module_results: Dict[str, Any],
        errors: Optional[Dict[str, Any]] = None,
        output_path: Optional[str] = None,
        completed_at: Optional[str] = None,
    ) -> Optional[int]:
        """Save report run. Returns run_id or None on error."""
        try:
            conn = self._get_conn()
            completed_at = completed_at or datetime.utcnow().isoformat()

            conn.execute(
                """
                INSERT INTO report_runs
                (config_id, started_at, completed_at, status, output_path, module_results, errors)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    config_id,
                    started_at,
                    completed_at,
                    status,
                    output_path,
                    json.dumps(module_results),
                    json.dumps(errors) if errors else None,
                ),
            )
            conn.commit()
            run_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

            # Update last_run in config
            conn.execute(
                "UPDATE report_configs SET last_run = ? WHERE id = ?",
                (completed_at, config_id),
            )
            conn.commit()
            conn.close()

            return run_id
        except Exception as e:
            print(f"Error saving run: {e}")
            return None

    def get_runs(
        self, config_name: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get report runs for a config."""
        try:
            conn = self._get_conn()
            config = conn.execute(
                "SELECT id FROM report_configs WHERE name = ?", (config_name,)
            ).fetchone()

            if not config:
                return []

            rows = conn.execute(
                """
                SELECT * FROM report_runs
                WHERE config_id = ?
                ORDER BY started_at DESC
                LIMIT ?
                """,
                (config["id"], limit),
            ).fetchall()
            conn.close()

            runs = []
            for row in rows:
                runs.append(
                    {
                        "id": row["id"],
                        "config_id": row["config_id"],
                        "started_at": row["started_at"],
                        "completed_at": row["completed_at"],
                        "status": row["status"],
                        "output_path": row["output_path"],
                        "module_results": json.loads(row["module_results"]),
                        "errors": json.loads(row["errors"]) if row["errors"] else None,
                    }
                )
            return runs
        except Exception as e:
            print(f"Error getting runs: {e}")
            return []

    def get_latest_run(self, config_name: str) -> Optional[Dict[str, Any]]:
        """Get latest run for a config."""
        runs = self.get_runs(config_name, limit=1)
        return runs[0] if runs else None


# Global database instance
_db = None


def get_db() -> ReportDatabase:
    """Get global database instance."""
    global _db
    if _db is None:
        _db = ReportDatabase()
    return _db
