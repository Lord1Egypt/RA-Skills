"""Append-only, hash-linked event store (v0.5 enterprise control-plane primitive).

Every state transition produced by the decision service (evaluate / approve)
emits a domain event. Events are immutable and chained by ``prev_hash`` so the
event log itself is independently auditable. The default in-process store is
suitable for development; the Postgres store provides durable, cross-process
persistence and per-tenant partitioning.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from threading import RLock
from typing import Protocol

from ..tenant import get_tenant


class DomainEvent:
    """An immutable, hash-chained record of a single state transition."""

    __slots__ = (
        "event_id",
        "event_type",
        "tenant_id",
        "aggregate_id",
        "payload",
        "created_at",
        "prev_hash",
        "event_hash",
    )

    def __init__(
        self,
        event_id: str,
        event_type: str,
        tenant_id: str,
        aggregate_id: str,
        payload: dict,
        created_at: float,
        prev_hash: str,
        event_hash: str,
    ) -> None:
        self.event_id = event_id
        self.event_type = event_type
        self.tenant_id = tenant_id
        self.aggregate_id = aggregate_id
        self.payload = payload
        self.created_at = created_at
        self.prev_hash = prev_hash
        self.event_hash = event_hash

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "tenant_id": self.tenant_id,
            "aggregate_id": self.aggregate_id,
            "payload": self.payload,
            "created_at": self.created_at,
            "prev_hash": self.prev_hash,
            "event_hash": self.event_hash,
        }

    @classmethod
    def create(
        cls,
        event_type: str,
        aggregate_id: str,
        payload: dict,
        prev_hash: str,
        tenant_id: str | None = None,
    ) -> "DomainEvent":
        created_at = time.time()
        event_id = uuid.uuid4().hex
        digest_source = json.dumps(
            {
                "event_id": event_id,
                "event_type": event_type,
                "tenant_id": tenant_id or "",
                "aggregate_id": aggregate_id,
                "payload": payload,
                "created_at": created_at,
                "prev_hash": prev_hash,
            },
            sort_keys=True,
            default=str,
        )
        event_hash = hashlib.sha256(digest_source.encode("utf-8")).hexdigest()
        return cls(
            event_id=event_id,
            event_type=event_type,
            tenant_id=tenant_id or "",
            aggregate_id=aggregate_id,
            payload=payload,
            created_at=created_at,
            prev_hash=prev_hash,
            event_hash=event_hash,
        )


class EventStore(Protocol):
    def append(self, event: DomainEvent) -> None: ...

    def stream(
        self, aggregate_id: str | None = None, tenant_id: str | None = None
    ) -> list[DomainEvent]: ...

    def last_hash(self, tenant_id: str = "") -> str: ...


class InMemoryEventStore:
    """Thread-safe in-process event store for development."""

    def __init__(self) -> None:
        self._events: list[DomainEvent] = []
        self._lock = RLock()

    def append(self, event: DomainEvent) -> None:
        with self._lock:
            self._events.append(event)

    def stream(
        self, aggregate_id: str | None = None, tenant_id: str | None = None
    ) -> list[DomainEvent]:
        with self._lock:
            result = self._events
            if aggregate_id is not None:
                result = [e for e in result if e.aggregate_id == aggregate_id]
            if tenant_id is not None:
                result = [e for e in result if e.tenant_id == tenant_id]
            return list(result)

    def last_hash(self, tenant_id: str = "") -> str:
        with self._lock:
            events = [e for e in self._events if e.tenant_id == tenant_id]
            return events[-1].event_hash if events else ""


class PostgresEventStore:
    """Durable Postgres-backed event store with per-tenant partitioning."""

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._lock = RLock()
        self._ensure_table()

    def _conn(self):
        import psycopg2
        import psycopg2.extras

        psycopg2.extras.register_uuid()
        return psycopg2.connect(self._dsn, cursor_factory=psycopg2.extras.RealDictCursor)

    def _ensure_table(self) -> None:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS nomos_events (
                    event_id     TEXT             PRIMARY KEY,
                    event_type   TEXT             NOT NULL,
                    tenant_id    TEXT             NOT NULL DEFAULT '',
                    aggregate_id TEXT             NOT NULL,
                    payload      JSONB            NOT NULL,
                    created_at   DOUBLE PRECISION NOT NULL,
                    prev_hash    TEXT             NOT NULL,
                    event_hash   TEXT             NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_events_agg
                    ON nomos_events (aggregate_id);
                CREATE INDEX IF NOT EXISTS idx_events_tenant
                    ON nomos_events (tenant_id);
                """
            )
            conn.commit()

    def append(self, event: DomainEvent) -> None:
        with self._lock:
            with self._conn() as conn, conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO nomos_events
                        (event_id, event_type, tenant_id, aggregate_id,
                         payload, created_at, prev_hash, event_hash)
                    VALUES (%s, %s, %s, %s, %s::jsonb, %s, %s, %s)
                    ON CONFLICT (event_id) DO NOTHING
                    """,
                    (
                        event.event_id,
                        event.event_type,
                        event.tenant_id,
                        event.aggregate_id,
                        json.dumps(event.payload, default=str),
                        event.created_at,
                        event.prev_hash,
                        event.event_hash,
                    ),
                )
                conn.commit()

    def stream(
        self, aggregate_id: str | None = None, tenant_id: str | None = None
    ) -> list[DomainEvent]:
        with self._lock:
            with self._conn() as conn, conn.cursor() as cur:
                clauses: list[str] = []
                params: list[object] = []
                if aggregate_id is not None:
                    clauses.append("aggregate_id = %s")
                    params.append(aggregate_id)
                if tenant_id is not None:
                    clauses.append("tenant_id = %s")
                    params.append(tenant_id)
                where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
                cur.execute(
                    f"SELECT * FROM nomos_events {where} ORDER BY created_at ASC",
                    params,
                )
                rows = cur.fetchall()
                return [
                    DomainEvent(
                        event_id=r["event_id"],
                        event_type=r["event_type"],
                        tenant_id=r["tenant_id"],
                        aggregate_id=r["aggregate_id"],
                        payload=r["payload"],
                        created_at=r["created_at"],
                        prev_hash=r["prev_hash"],
                        event_hash=r["event_hash"],
                    )
                    for r in rows
                ]

    def last_hash(self, tenant_id: str = "") -> str:
        with self._lock:
            with self._conn() as conn, conn.cursor() as cur:
                cur.execute(
                    "SELECT event_hash FROM nomos_events "
                    "WHERE tenant_id = %s ORDER BY created_at DESC LIMIT 1",
                    (tenant_id,),
                )
                row = cur.fetchone()
                return row["event_hash"] if row else ""
