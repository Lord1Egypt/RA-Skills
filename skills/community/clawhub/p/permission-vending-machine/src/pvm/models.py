"""Core data models for PVM."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional


class Decision(str, Enum):
    """Audit log decision types."""

    GRANTED = "GRANTED"
    DENIED = "DENIED"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    SUCCESS = "SUCCESS"


class AuditEntryType(str, Enum):
    """Types of audit log entries."""

    REQUEST = "REQUEST"
    APPROVAL = "APPROVAL"
    DENIAL = "DENIAL"
    GRANT_CHECK = "GRANT_CHECK"
    REVOCATION = "REVOCATION"
    EXECUTION = "EXECUTION"


@dataclass
class Grant:
    """A time-limited permission grant."""

    grant_id: str
    agent_id: str
    scope: str
    scope_type: str  # "path" | "repo"
    reason: str
    issued_at: datetime
    expires_at: datetime
    revoked: bool = False
    approved_by: Optional[str] = None

    @classmethod
    def create(
        cls,
        agent_id: str,
        scope: str,
        scope_type: str,
        reason: str,
        ttl_minutes: int,
        approved_by: Optional[str] = None,
    ) -> Grant:
        """Factory: create a new grant with auto-generated ID and timestamps."""
        now = datetime.now(timezone.utc)
        return cls(
            grant_id=f"grant_{uuid.uuid4().hex[:12]}",
            agent_id=agent_id,
            scope=scope,
            scope_type=scope_type,
            reason=reason,
            issued_at=now,
            expires_at=now + timedelta(minutes=ttl_minutes),
            approved_by=approved_by,
        )

    def is_active(self) -> bool:
        """Check if grant is currently valid (not revoked and not expired)."""
        if self.revoked:
            return False
        return datetime.now(timezone.utc) < self.expires_at

    def remaining_minutes(self) -> float:
        """Minutes until expiry (negative if already expired)."""
        delta = self.expires_at - datetime.now(timezone.utc)
        return delta.total_seconds() / 60.0

    def to_dict(self) -> dict:
        return {
            "grant_id": self.grant_id,
            "agent_id": self.agent_id,
            "scope": self.scope,
            "scope_type": self.scope_type,
            "reason": self.reason,
            "issued_at": self.issued_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "revoked": self.revoked,
            "approved_by": self.approved_by,
        }


@dataclass
class PermissionRequest:
    """A permission request from an agent."""

    request_id: str
    agent_id: str
    operation: str
    scope: str
    scope_type: str
    reason: str
    ttl_minutes: int
    approval_token: str
    status: str = "pending"  # pending | approved | denied | expired
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(
        cls,
        agent_id: str,
        operation: str,
        scope: str,
        scope_type: str,
        reason: str,
        ttl_minutes: int,
    ) -> PermissionRequest:
        """Factory: create a new permission request."""
        return cls(
            request_id=f"req_{uuid.uuid4().hex[:12]}",
            agent_id=agent_id,
            operation=operation,
            scope=scope,
            scope_type=scope_type,
            reason=reason,
            ttl_minutes=ttl_minutes,
            approval_token=f"tok_{uuid.uuid4().hex[:24]}",
        )


@dataclass
class AuditEntry:
    """A single audit log entry."""

    entry_id: str
    timestamp: datetime
    entry_type: AuditEntryType
    agent_id: Optional[str]
    scope: Optional[str]
    decision: Optional[Decision]
    details: str
    grant_id: Optional[str] = None

    @classmethod
    def create(
        cls,
        entry_type: AuditEntryType,
        details: str,
        agent_id: Optional[str] = None,
        scope: Optional[str] = None,
        decision: Optional[Decision] = None,
        grant_id: Optional[str] = None,
    ) -> AuditEntry:
        """Factory: create a new audit entry."""
        return cls(
            entry_id=f"audit_{uuid.uuid4().hex[:12]}",
            timestamp=datetime.now(timezone.utc),
            entry_type=entry_type,
            agent_id=agent_id,
            scope=scope,
            decision=decision,
            details=details,
            grant_id=grant_id,
        )

    def to_dict(self) -> dict:
        return {
            "entry_id": self.entry_id,
            "timestamp": self.timestamp.isoformat(),
            "entry_type": self.entry_type.value,
            "agent_id": self.agent_id,
            "scope": self.scope,
            "decision": self.decision.value if self.decision else None,
            "details": self.details,
            "grant_id": self.grant_id,
        }
