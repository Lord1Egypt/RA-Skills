"""
Nex HealthCheck - SQLite storage layer
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import os
import stat
import sqlite3
import platform
import datetime as dt
import json
from pathlib import Path
from contextlib import contextmanager
from config import DB_PATH, DATA_DIR, StatusLevel, HISTORY_RETENTION_DAYS


def init_db():
    """Create database and tables if they don't exist. Sets secure file permissions."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if platform.system() != "Windows":
        os.chmod(str(DATA_DIR), stat.S_IRWXU)

    with _connect() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS services (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT UNIQUE NOT NULL,
                check_type      TEXT NOT NULL,
                target          TEXT NOT NULL,
                port            INTEGER,
                expected_status TEXT,
                enabled         BOOLEAN DEFAULT 1,
                check_interval  INTEGER DEFAULT 300,
                tags            TEXT,
                group_name      TEXT,
                notes           TEXT,
                created_at      TEXT DEFAULT (datetime('now')),
                updated_at      TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS check_results (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                service_id      INTEGER NOT NULL,
                status          TEXT NOT NULL,
                response_time_ms INTEGER,
                message         TEXT,
                details         TEXT,
                checked_at      TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS incidents (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                service_id      INTEGER NOT NULL,
                status          TEXT NOT NULL,
                started_at      TEXT DEFAULT (datetime('now')),
                resolved_at     TEXT,
                duration_seconds INTEGER,
                notification_sent BOOLEAN DEFAULT 0,
                notes           TEXT,
                FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS check_history (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                service_id      INTEGER NOT NULL,
                date            TEXT NOT NULL,
                uptime_pct      REAL,
                avg_response_ms INTEGER,
                checks_total    INTEGER,
                checks_failed   INTEGER,
                FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE,
                UNIQUE(service_id, date)
            );

            CREATE INDEX IF NOT EXISTS idx_check_results_service
                ON check_results(service_id);
            CREATE INDEX IF NOT EXISTS idx_check_results_checked
                ON check_results(checked_at);
            CREATE INDEX IF NOT EXISTS idx_incidents_service
                ON incidents(service_id);
            CREATE INDEX IF NOT EXISTS idx_incidents_resolved
                ON incidents(resolved_at);
            CREATE INDEX IF NOT EXISTS idx_history_service
                ON check_history(service_id);
        """)


@contextmanager
def _connect():
    """Context manager for database connections."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def save_service(name, check_type, target, expected_status="200", port=None,
                 enabled=True, check_interval=300, tags=None, group_name=None, notes=None):
    """Save a service to monitor. Returns service_id."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO services
            (name, check_type, target, port, expected_status, enabled, check_interval, tags, group_name, notes, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (name, check_type, target, port, expected_status, enabled, check_interval, tags, group_name, notes))
        conn.commit()
        cursor.execute("SELECT id FROM services WHERE name = ?", (name,))
        return cursor.fetchone()[0]


def get_service(service_id):
    """Get service by ID."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM services WHERE id = ?", (service_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def list_services(enabled_only=False, group_name=None, tag=None):
    """List all monitored services. Can filter by enabled, group, or tag."""
    with _connect() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM services WHERE 1=1"
        params = []

        if enabled_only:
            query += " AND enabled = 1"
        if group_name:
            query += " AND group_name = ?"
            params.append(group_name)
        if tag:
            query += " AND tags LIKE ?"
            params.append(f"%{tag}%")

        query += " ORDER BY group_name, name"
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


def delete_service(service_id):
    """Delete a service and all its data."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM services WHERE id = ?", (service_id,))
        conn.commit()


def save_check_result(service_id, status, response_time_ms=None, message=None, details=None):
    """Save a check result. Auto-detects and manages incidents."""
    with _connect() as conn:
        cursor = conn.cursor()

        # Save the result
        cursor.execute("""
            INSERT INTO check_results
            (service_id, status, response_time_ms, message, details)
            VALUES (?, ?, ?, ?, ?)
        """, (service_id, status, response_time_ms, message, json.dumps(details) if details else None))

        # Check for active incidents
        cursor.execute("""
            SELECT id FROM incidents
            WHERE service_id = ? AND resolved_at IS NULL
            ORDER BY started_at DESC LIMIT 1
        """, (service_id,))
        active_incident = cursor.fetchone()

        if status == StatusLevel.OK.value or status == "ok":
            # Service is OK - resolve any active incident
            if active_incident:
                incident_id = active_incident[0]
                now = dt.datetime.utcnow().isoformat()
                cursor.execute("""
                    SELECT started_at FROM incidents WHERE id = ?
                """, (incident_id,))
                start_row = cursor.fetchone()
                if start_row:
                    start_dt = dt.datetime.fromisoformat(start_row[0].replace('Z', '+00:00'))
                    now_dt = dt.datetime.utcnow().replace(tzinfo=None)
                    duration = int((now_dt - start_dt.replace(tzinfo=None)).total_seconds())
                else:
                    duration = 0

                cursor.execute("""
                    UPDATE incidents
                    SET resolved_at = datetime('now'), duration_seconds = ?
                    WHERE id = ?
                """, (duration, incident_id))
        else:
            # Service is down or warning - create incident if needed
            if not active_incident:
                cursor.execute("""
                    INSERT INTO incidents
                    (service_id, status)
                    VALUES (?, ?)
                """, (service_id, status))

        conn.commit()


def get_latest_results(limit=50):
    """Get the most recent check results."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cr.*, s.name, s.check_type FROM check_results cr
            JOIN services s ON cr.service_id = s.id
            ORDER BY cr.checked_at DESC
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]


def get_service_history(service_id, days=7):
    """Get check history for a service."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM check_history
            WHERE service_id = ? AND date >= date('now', '-' || ? || ' days')
            ORDER BY date DESC
        """, (service_id, days))
        return [dict(row) for row in cursor.fetchall()]


def get_incidents(since=None, service_id=None, active_only=False):
    """Get incidents. Can filter by time, service, and active status."""
    with _connect() as conn:
        cursor = conn.cursor()
        query = "SELECT i.*, s.name FROM incidents i JOIN services s ON i.service_id = s.id WHERE 1=1"
        params = []

        if since:
            query += " AND i.started_at >= ?"
            params.append(since)
        if service_id:
            query += " AND i.service_id = ?"
            params.append(service_id)
        if active_only:
            query += " AND i.resolved_at IS NULL"

        query += " ORDER BY i.started_at DESC"
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


def resolve_incident(incident_id, notes=None):
    """Manually resolve an incident."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE incidents
            SET resolved_at = datetime('now'), notes = ?
            WHERE id = ?
        """, (notes, incident_id))
        conn.commit()


def get_uptime_stats(service_id, days=30):
    """Get uptime statistics for a service."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                SUM(checks_total) as total_checks,
                SUM(checks_failed) as failed_checks,
                AVG(uptime_pct) as avg_uptime,
                AVG(avg_response_ms) as avg_response_ms
            FROM check_history
            WHERE service_id = ? AND date >= date('now', '-' || ? || ' days')
        """, (service_id, days))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return {"total_checks": 0, "failed_checks": 0, "avg_uptime": 100, "avg_response_ms": 0}


def get_dashboard_summary():
    """Get summary stats for the dashboard."""
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                COUNT(DISTINCT s.id) as total_services,
                SUM(CASE WHEN cr.status = 'ok' THEN 1 ELSE 0 END) as healthy_services,
                SUM(CASE WHEN cr.status = 'warning' THEN 1 ELSE 0 END) as warning_services,
                SUM(CASE WHEN cr.status = 'critical' THEN 1 ELSE 0 END) as critical_services
            FROM services s
            LEFT JOIN (
                SELECT DISTINCT ON (service_id) * FROM check_results
                ORDER BY service_id, checked_at DESC
            ) cr ON s.id = cr.service_id
            WHERE s.enabled = 1
        """)
        row = cursor.fetchone()
        return dict(row) if row else {
            "total_services": 0,
            "healthy_services": 0,
            "warning_services": 0,
            "critical_services": 0
        }


def search_services(query):
    """Search services by name, notes, or tags."""
    with _connect() as conn:
        cursor = conn.cursor()
        search_term = f"%{query}%"
        cursor.execute("""
            SELECT * FROM services
            WHERE name LIKE ? OR notes LIKE ? OR tags LIKE ?
            ORDER BY name
        """, (search_term, search_term, search_term))
        return [dict(row) for row in cursor.fetchall()]
