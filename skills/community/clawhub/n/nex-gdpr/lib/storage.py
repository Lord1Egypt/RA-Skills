#!/usr/bin/env python3
# Nex GDPR - Storage & Database
# MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Any
import json

from .config import DB_PATH, REQUEST_TYPES, REQUEST_STATUSES, RESPONSE_DEADLINE_DAYS


class GDPRStorage:
    """SQLite storage for GDPR requests, findings, and audit trail."""

    def __init__(self):
        self.db_path = DB_PATH
        self.init_db()

    def init_db(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Requests table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_type TEXT NOT NULL,
                data_subject_name TEXT NOT NULL,
                data_subject_email TEXT NOT NULL,
                data_subject_id TEXT,
                received_date TEXT NOT NULL,
                deadline_date TEXT NOT NULL,
                extended_deadline TEXT,
                status TEXT NOT NULL,
                assigned_to TEXT,
                verified INTEGER NOT NULL DEFAULT 0,
                verification_method TEXT,
                response_summary TEXT,
                completed_at TEXT,
                denied_reason TEXT,
                notes TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """
        )

        # Data findings table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS data_findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id INTEGER NOT NULL,
                data_source TEXT NOT NULL,
                file_path TEXT NOT NULL,
                data_type TEXT NOT NULL,
                description TEXT,
                size_bytes INTEGER,
                contains_pii INTEGER NOT NULL DEFAULT 0,
                action_taken TEXT,
                action_date TEXT,
                notes TEXT,
                FOREIGN KEY (request_id) REFERENCES requests(id)
            )
        """
        )

        # Audit trail table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_trail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                actor TEXT NOT NULL,
                details TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (request_id) REFERENCES requests(id)
            )
        """
        )

        # Retention policies table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS retention_policies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_type TEXT NOT NULL UNIQUE,
                retention_days INTEGER NOT NULL,
                auto_delete INTEGER NOT NULL DEFAULT 0,
                last_cleanup TEXT,
                created_at TEXT NOT NULL
            )
        """
        )

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_request_status ON requests(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_request_type ON requests(request_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_request_deadline ON requests(deadline_date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_finding_request ON data_findings(request_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_request ON audit_trail(request_id)")

        conn.commit()
        conn.close()

    def save_request(self, request_type: str, name: str, email: str,
                     data_subject_id: Optional[str] = None, notes: str = "") -> int:
        """Save a new GDPR request. Returns request ID."""
        now = datetime.now().isoformat()
        deadline = (datetime.now() + timedelta(days=RESPONSE_DEADLINE_DAYS)).isoformat()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO requests
            (request_type, data_subject_name, data_subject_email, data_subject_id,
             received_date, deadline_date, status, verified, created_at, updated_at, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                request_type,
                name,
                email,
                data_subject_id,
                now,
                deadline,
                "RECEIVED",
                0,
                now,
                now,
                notes,
            ),
        )
        conn.commit()
        request_id = cursor.lastrowid
        conn.close()

        self.save_audit_entry(
            request_id, "request_created", "system", f"New {request_type} request created"
        )
        return request_id

    def get_request(self, request_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a request by ID."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM requests WHERE id = ?", (request_id,))
        row = cursor.fetchone()
        conn.close()

        return dict(row) if row else None

    def list_requests(
        self, status: Optional[str] = None, request_type: Optional[str] = None,
        overdue: bool = False
    ) -> List[Dict[str, Any]]:
        """List requests with optional filters."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = "SELECT * FROM requests WHERE 1=1"
        params = []

        if status:
            query += " AND status = ?"
            params.append(status)

        if request_type:
            query += " AND request_type = ?"
            params.append(request_type)

        if overdue:
            now = datetime.now().isoformat()
            query += " AND deadline_date < ? AND status NOT IN ('COMPLETED', 'DENIED')"
            params.append(now)

        query += " ORDER BY received_date DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def update_request_status(self, request_id: int, new_status: str,
                             actor: str = "system", details: str = "") -> bool:
        """Update request status."""
        now = datetime.now().isoformat()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE requests SET status = ?, updated_at = ? WHERE id = ?",
            (new_status, now, request_id),
        )

        if new_status == "COMPLETED":
            cursor.execute("UPDATE requests SET completed_at = ? WHERE id = ?", (now, request_id))

        conn.commit()
        conn.close()

        self.save_audit_entry(request_id, "status_changed", actor,
                             f"Status changed to {new_status}. {details}")
        return True

    def save_finding(self, request_id: int, data_source: str, file_path: str,
                    data_type: str, description: str = "", size_bytes: int = 0,
                    contains_pii: bool = False, action_taken: str = "",
                    notes: str = "") -> int:
        """Save a data finding."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO data_findings
            (request_id, data_source, file_path, data_type, description, size_bytes,
             contains_pii, action_taken, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                request_id,
                data_source,
                file_path,
                data_type,
                description,
                size_bytes,
                1 if contains_pii else 0,
                action_taken,
                notes,
            ),
        )
        conn.commit()
        finding_id = cursor.lastrowid
        conn.close()

        return finding_id

    def list_findings(self, request_id: int) -> List[Dict[str, Any]]:
        """List findings for a request."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM data_findings WHERE request_id = ? ORDER BY id DESC",
            (request_id,),
        )
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def save_audit_entry(self, request_id: int, action: str, actor: str,
                        details: str = "") -> int:
        """Save audit trail entry."""
        now = datetime.now().isoformat()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO audit_trail (request_id, action, actor, details, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """,
            (request_id, action, actor, details, now),
        )
        conn.commit()
        entry_id = cursor.lastrowid
        conn.close()

        return entry_id

    def get_audit_trail(self, request_id: int) -> List[Dict[str, Any]]:
        """Get audit trail for a request."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM audit_trail WHERE request_id = ? ORDER BY timestamp DESC",
            (request_id,),
        )
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_overdue_requests(self) -> List[Dict[str, Any]]:
        """Get requests past deadline that are not completed/denied."""
        return self.list_requests(overdue=True)

    def get_request_stats(self) -> Dict[str, Any]:
        """Get GDPR request statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        stats = {}

        # Count by status
        for status in REQUEST_STATUSES.keys():
            cursor.execute("SELECT COUNT(*) FROM requests WHERE status = ?", (status,))
            stats[f"count_{status}"] = cursor.fetchone()[0]

        # Count by type
        for req_type in REQUEST_TYPES.keys():
            cursor.execute("SELECT COUNT(*) FROM requests WHERE request_type = ?", (req_type,))
            stats[f"count_{req_type}"] = cursor.fetchone()[0]

        # Overdue
        cursor.execute(
            "SELECT COUNT(*) FROM requests WHERE deadline_date < ? AND status NOT IN ('COMPLETED', 'DENIED')",
            (datetime.now().isoformat(),),
        )
        stats["overdue"] = cursor.fetchone()[0]

        # Total findings
        cursor.execute("SELECT COUNT(*) FROM data_findings")
        stats["total_findings"] = cursor.fetchone()[0]

        # PII findings
        cursor.execute("SELECT COUNT(*) FROM data_findings WHERE contains_pii = 1")
        stats["pii_findings"] = cursor.fetchone()[0]

        # Total data size
        cursor.execute("SELECT SUM(size_bytes) FROM data_findings")
        result = cursor.fetchone()[0]
        stats["total_size_bytes"] = result if result else 0

        conn.close()
        return stats

    def get_retention_policies(self) -> List[Dict[str, Any]]:
        """Get all retention policies."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM retention_policies ORDER BY data_type")
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def save_retention_policy(self, data_type: str, retention_days: int,
                             auto_delete: bool = False) -> int:
        """Save or update retention policy."""
        now = datetime.now().isoformat()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO retention_policies
            (data_type, retention_days, auto_delete, created_at)
            VALUES (?, ?, ?, ?)
        """,
            (data_type, retention_days, 1 if auto_delete else 0, now),
        )
        conn.commit()
        policy_id = cursor.lastrowid
        conn.close()

        return policy_id

    def export_request_report(self, request_id: int) -> Dict[str, Any]:
        """Export complete request report for compliance documentation."""
        request = self.get_request(request_id)
        findings = self.list_findings(request_id)
        audit = self.get_audit_trail(request_id)

        if not request:
            return {}

        return {
            "request": dict(request),
            "findings": findings,
            "audit_trail": audit,
            "exported_at": datetime.now().isoformat(),
        }
