"""SQLite-backed grant registry and audit log for PVM."""

from __future__ import annotations

import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Generator, List, Optional

from .models import AuditEntry, AuditEntryType, Decision, Grant, PermissionRequest


class Vault:
    """Thread-safe SQLite vault for grants and audit logs."""

    def __init__(self, db_path: str = "./grants.db", uri: bool = False):
        self.db_path = db_path
        self._local = threading.local()
        self._uri = uri
        self._init_db()

    # ── Connection management ────────────────────────────────────────────────

    def _get_conn(self) -> sqlite3.Connection:
        """Get a thread-local DB connection, creating if needed."""
        if not hasattr(self._local, "conn") or self._local.conn is None:
            kw = {"check_same_thread": False}
            if self._uri:
                kw["uri"] = True
            self._local.conn = sqlite3.connect(self.db_path, **kw)
            self._local.conn.row_factory = sqlite3.Row
        return self._local.conn

    @contextmanager
    def _tx(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager for a transaction."""
        conn = self._get_conn()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    # ── Schema init ─────────────────────────────────────────────────────────

    def _init_db(self) -> None:
        """Create tables if they don't exist."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with self._tx() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS grants (
                    grant_id        TEXT PRIMARY KEY,
                    agent_id        TEXT NOT NULL,
                    scope           TEXT NOT NULL,
                    scope_type      TEXT NOT NULL,
                    reason          TEXT NOT NULL,
                    issued_at       TEXT NOT NULL,
                    expires_at      TEXT NOT NULL,
                    revoked         INTEGER NOT NULL DEFAULT 0,
                    approved_by     TEXT,
                    approval_token  TEXT
                );

                CREATE INDEX IF NOT EXISTS idx_grants_agent
                    ON grants(agent_id);
                CREATE INDEX IF NOT EXISTS idx_grants_scope
                    ON grants(scope);
                CREATE INDEX IF NOT EXISTS idx_grants_expires
                    ON grants(expires_at);
                CREATE INDEX IF NOT EXISTS idx_grants_token
                    ON grants(approval_token);

                CREATE TABLE IF NOT EXISTS permission_requests (
                    request_id      TEXT PRIMARY KEY,
                    agent_id        TEXT NOT NULL,
                    operation       TEXT NOT NULL,
                    scope           TEXT NOT NULL,
                    scope_type      TEXT NOT NULL,
                    reason          TEXT NOT NULL,
                    ttl_minutes     INTEGER NOT NULL,
                    approval_token  TEXT NOT NULL,
                    status          TEXT NOT NULL DEFAULT 'pending',
                    created_at      TEXT NOT NULL,
                    decided_by      TEXT,
                    decided_at      TEXT
                );

                CREATE INDEX IF NOT EXISTS idx_requests_token
                    ON permission_requests(approval_token);
                CREATE INDEX IF NOT EXISTS idx_requests_agent
                    ON permission_requests(agent_id);
                CREATE INDEX IF NOT EXISTS idx_requests_status
                    ON permission_requests(status);

                CREATE TABLE IF NOT EXISTS audit_log (
                    entry_id    TEXT PRIMARY KEY,
                    timestamp   TEXT NOT NULL,
                    entry_type  TEXT NOT NULL,
                    agent_id    TEXT,
                    scope       TEXT,
                    decision    TEXT,
                    details     TEXT NOT NULL,
                    grant_id    TEXT
                );

                CREATE INDEX IF NOT EXISTS idx_audit_agent
                    ON audit_log(agent_id);
                CREATE INDEX IF NOT EXISTS idx_audit_timestamp
                    ON audit_log(timestamp);
                CREATE INDEX IF NOT EXISTS idx_audit_decision
                    ON audit_log(decision);
            """)

    # ── Grant operations ─────────────────────────────────────────────────────

    def create_grant(
        self,
        agent_id: str,
        scope: str,
        scope_type: str,
        reason: str,
        ttl_minutes: int,
        approved_by: Optional[str] = None,
        approval_token: Optional[str] = None,
    ) -> Grant:
        """Create and persist a new grant."""
        grant = Grant.create(
            agent_id=agent_id,
            scope=scope,
            scope_type=scope_type,
            reason=reason,
            ttl_minutes=ttl_minutes,
            approved_by=approved_by,
        )
        with self._tx() as conn:
            conn.execute(
                """
                INSERT INTO grants
                    (grant_id, agent_id, scope, scope_type, reason,
                     issued_at, expires_at, revoked, approved_by, approval_token)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    grant.grant_id,
                    grant.agent_id,
                    grant.scope,
                    grant.scope_type,
                    grant.reason,
                    grant.issued_at.isoformat(),
                    grant.expires_at.isoformat(),
                    0,
                    grant.approved_by,
                    approval_token,
                ),
            )
        # Update the permission request status if a token was provided
        if approval_token:
            conn.execute(
                """
                UPDATE permission_requests
                SET status = 'approved', decided_by = ?, decided_at = ?
                WHERE approval_token = ? AND status = 'pending'
                """,
                (approved_by, datetime.now(timezone.utc).isoformat(), approval_token),
            )
        self.log_audit(
            entry_type=AuditEntryType.APPROVAL,
            agent_id=agent_id,
            scope=scope,
            decision=Decision.GRANTED,
            details=f"Grant {grant.grant_id} issued for {ttl_minutes}min to {agent_id}: {scope} (token={approval_token})",
            grant_id=grant.grant_id,
        )
        return grant

    def create_request(
        self,
        agent_id: str,
        operation: str,
        scope: str,
        scope_type: str,
        reason: str,
        ttl_minutes: int,
        approval_token: str,
    ) -> str:
        """Create a pending permission request. Returns request_id."""
        req = PermissionRequest.create(
            agent_id=agent_id,
            operation=operation,
            scope=scope,
            scope_type=scope_type,
            reason=reason,
            ttl_minutes=ttl_minutes,
        )
        req.approval_token = approval_token  # use the token we already have
        with self._tx() as conn:
            conn.execute(
                """
                INSERT INTO permission_requests
                    (request_id, agent_id, operation, scope, scope_type,
                     reason, ttl_minutes, approval_token, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?)
                """,
                (
                    req.request_id,
                    req.agent_id,
                    req.operation,
                    req.scope,
                    req.scope_type,
                    req.reason,
                    req.ttl_minutes,
                    req.approval_token,
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
        self.log_audit(
            entry_type=AuditEntryType.REQUEST,
            agent_id=agent_id,
            scope=scope,
            decision=None,
            details=f"Permission request {req.request_id} created: {operation} on {scope} (token={approval_token})",
        )
        return req.request_id

    def get_request_by_token(self, approval_token: str) -> Optional[dict]:
        """Get a pending permission request by its approval token."""
        with self._tx() as conn:
            row = conn.execute(
                """
                SELECT * FROM permission_requests
                WHERE approval_token = ? AND status = 'pending'
                """,
                (approval_token,),
            ).fetchone()
        if not row:
            return None
        return dict(row)

    def get_most_recent_pending_request(self) -> Optional[dict]:
        """Get the most recently created pending request."""
        with self._tx() as conn:
            row = conn.execute(
                """
                SELECT * FROM permission_requests
                WHERE status = 'pending'
                ORDER BY created_at DESC
                LIMIT 1
                """,
            ).fetchone()
        if not row:
            return None
        return dict(row)

    def deny_request(self, approval_token: str, denied_by: str) -> None:
        """Mark a permission request as denied."""
        with self._tx() as conn:
            conn.execute(
                """
                UPDATE permission_requests
                SET status = 'denied', decided_by = ?, decided_at = ?
                WHERE approval_token = ? AND status = 'pending'
                """,
                (denied_by, datetime.now(timezone.utc).isoformat(), approval_token),
            )
        entries = self.get_audit_log(limit=1000)
        matching = [e for e in entries if approval_token in (e.details or "")]
        latest = matching[0] if matching else None
        self.log_audit(
            entry_type=AuditEntryType.DENIAL,
            agent_id=latest.agent_id if latest else None,
            scope=latest.scope if latest else None,
            decision=Decision.DENIED,
            details=f"Request {approval_token} denied by {denied_by}",
        )

    def check_grant(self, agent_id: str, scope: str) -> bool:
        """
        Check if an active (non-revoked, non-expired) grant exists
        for the given agent+scope.
        """
        self._purge_expired()
        now_iso = datetime.now(timezone.utc).isoformat()
        with self._tx() as conn:
            row = conn.execute(
                """
                SELECT 1 FROM grants
                WHERE agent_id   = ?
                  AND scope      = ?
                  AND revoked    = 0
                  AND expires_at > ?
                LIMIT 1
                """,
                (agent_id, scope, now_iso),
            ).fetchone()
        return row is not None

    def check_grant_glob(self, agent_id: str, scope: str, scope_type: str) -> bool:
        """
        Check grant with glob-style path matching.
        For 'path' scope_type: checks if scope is a sub-path of any active grant scope.
        For 'repo' scope_type: exact match.
        """
        self._purge_expired()
        now_iso = datetime.now(timezone.utc).isoformat()
        with self._tx() as conn:
            if scope_type == "path":
                rows = conn.execute(
                    """
                    SELECT scope FROM grants
                    WHERE agent_id    = ?
                      AND scope_type  = 'path'
                      AND revoked     = 0
                      AND expires_at  > ?
                    """,
                    (agent_id, now_iso),
                ).fetchall()
            else:
                rows = conn.execute(
                    """
                    SELECT scope FROM grants
                    WHERE agent_id    = ?
                      AND scope       = ?
                      AND scope_type  = ?
                      AND revoked     = 0
                      AND expires_at  > ?
                    """,
                    (agent_id, scope, scope_type, now_iso),
                ).fetchall()

        if scope_type == "path":
            for row in rows:
                grant_scope = row["scope"]
                if scope == grant_scope or scope.startswith(grant_scope.rstrip("/") + "/"):
                    return True
            return False
        return len(rows) > 0

    def revoke_grant(self, grant_id: str) -> None:
        """Mark a grant as revoked."""
        with self._tx() as conn:
            conn.execute(
                "UPDATE grants SET revoked = 1 WHERE grant_id = ?",
                (grant_id,),
            )
            row = conn.execute(
                "SELECT agent_id, scope FROM grants WHERE grant_id = ?",
                (grant_id,),
            ).fetchone()
        if row:
            self.log_audit(
                entry_type=AuditEntryType.REVOCATION,
                agent_id=row["agent_id"],
                scope=row["scope"],
                decision=Decision.REVOKED,
                details=f"Grant {grant_id} revoked",
                grant_id=grant_id,
            )

    def get_grant(self, grant_id: str) -> Optional[Grant]:
        """Fetch a grant by ID, or None if not found."""
        with self._tx() as conn:
            row = conn.execute(
                "SELECT * FROM grants WHERE grant_id = ?", (grant_id,)
            ).fetchone()
        if not row:
            return None
        return self._row_to_grant(row)

    def get_active_grants(self, agent_id: Optional[str] = None) -> List[Grant]:
        """List all active (non-revoked, non-expired) grants, optionally filtered."""
        self._purge_expired()
        now_iso = datetime.now(timezone.utc).isoformat()
        with self._tx() as conn:
            if agent_id:
                rows = conn.execute(
                    """
                    SELECT * FROM grants
                    WHERE agent_id   = ?
                      AND revoked    = 0
                      AND expires_at > ?
                    ORDER BY issued_at DESC
                    """,
                    (agent_id, now_iso),
                ).fetchall()
            else:
                rows = conn.execute(
                    """
                    SELECT * FROM grants
                    WHERE revoked    = 0
                      AND expires_at > ?
                    ORDER BY issued_at DESC
                    """,
                    (now_iso,),
                ).fetchall()
        return [self._row_to_grant(row) for row in rows]

    def _purge_expired(self) -> None:
        """Mark expired grants as revoked (idempotent)."""
        now_iso = datetime.now(timezone.utc).isoformat()
        with self._tx() as conn:
            # Log expirations before marking
            rows = conn.execute(
                """
                SELECT grant_id, agent_id, scope FROM grants
                WHERE revoked = 0 AND expires_at <= ?
                """,
                (now_iso,),
            ).fetchall()
            for row in rows:
                self.log_audit(
                    entry_type=AuditEntryType.REVOCATION,
                    agent_id=row["agent_id"],
                    scope=row["scope"],
                    decision=Decision.EXPIRED,
                    details=f"Grant {row['grant_id']} expired",
                    grant_id=row["grant_id"],
                )
            conn.execute(
                "UPDATE grants SET revoked = 1 WHERE revoked = 0 AND expires_at <= ?",
                (now_iso,),
            )

    def _row_to_grant(self, row: sqlite3.Row) -> Grant:
        return Grant(
            grant_id=row["grant_id"],
            agent_id=row["agent_id"],
            scope=row["scope"],
            scope_type=row["scope_type"],
            reason=row["reason"],
            issued_at=datetime.fromisoformat(row["issued_at"]),
            expires_at=datetime.fromisoformat(row["expires_at"]),
            revoked=bool(row["revoked"]),
            approved_by=row["approved_by"],
        )

    # ── Audit log ────────────────────────────────────────────────────────────

    def log_audit(
        self,
        entry_type: AuditEntryType,
        details: str,
        agent_id: Optional[str] = None,
        scope: Optional[str] = None,
        decision: Optional[Decision] = None,
        grant_id: Optional[str] = None,
    ) -> None:
        """Append an audit entry."""
        entry = AuditEntry.create(
            entry_type=entry_type,
            details=details,
            agent_id=agent_id,
            scope=scope,
            decision=decision,
            grant_id=grant_id,
        )
        with self._tx() as conn:
            conn.execute(
                """
                INSERT INTO audit_log
                    (entry_id, timestamp, entry_type, agent_id,
                     scope, decision, details, grant_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entry.entry_id,
                    entry.timestamp.isoformat(),
                    entry.entry_type.value,
                    entry.agent_id,
                    entry.scope,
                    entry.decision.value if entry.decision else None,
                    entry.details,
                    entry.grant_id,
                ),
            )

    def get_audit_log(
        self,
        agent_id: Optional[str] = None,
        decision: Optional[Decision] = None,
        limit: int = 100,
    ) -> List[AuditEntry]:
        """Query audit log with optional filters."""
        with self._tx() as conn:
            query = "SELECT * FROM audit_log WHERE 1=1"
            params: list = []
            if agent_id:
                query += " AND agent_id = ?"
                params.append(agent_id)
            if decision:
                query += " AND decision = ?"
                params.append(decision.value)
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            rows = conn.execute(query, params).fetchall()
        return [self._row_to_audit(row) for row in rows]

    def _row_to_audit(self, row: sqlite3.Row) -> AuditEntry:
        return AuditEntry(
            entry_id=row["entry_id"],
            timestamp=datetime.fromisoformat(row["timestamp"]),
            entry_type=AuditEntryType(row["entry_type"]),
            agent_id=row["agent_id"],
            scope=row["scope"],
            decision=Decision(row["decision"]) if row["decision"] else None,
            details=row["details"],
            grant_id=row["grant_id"],
        )
