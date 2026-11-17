from __future__ import annotations

import json
from threading import RLock

import psycopg2
import psycopg2.extras
from psycopg2 import sql

from ..decision.integrity import verify_chain, verify_record
from ..hub.integrity import verify_hub_report
from ..models.hub import HubReport
from ..models.schemas import DecisionRecord, ReconstructionSession

psycopg2.extras.register_uuid()


class PostgresDecisionRepository:
    """PostgreSQL-backed decision repository.

    Stores DecisionRecord bodies as JSONB with indexed metadata columns for
    decision_id, revision, and record_hash. Integrity verification (hash-chain)
    is enforced on read to catch tampering at the storage layer.
    """

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._lock = RLock()
        self._ensure_tables()

    def _conn(self):
        return psycopg2.connect(self._dsn, cursor_factory=psycopg2.extras.RealDictCursor)

    def _ensure_tables(self) -> None:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS nomos_decisions (
                    decision_id   TEXT        NOT NULL,
                    revision      INTEGER     NOT NULL,
                    record_hash   TEXT        NOT NULL,
                    body          JSONB       NOT NULL,
                    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    PRIMARY KEY (decision_id, revision)
                );
                CREATE INDEX IF NOT EXISTS idx_decisions_id
                    ON nomos_decisions (decision_id, revision DESC);
                """
            )
            conn.commit()

    def put(self, record: DecisionRecord) -> None:
        with self._lock:
            if not verify_record(record):
                raise ValueError("record_hash does not match the decision record payload")
            with self._conn() as conn, conn.cursor() as cur:
                cur.execute(
                    "SELECT revision FROM nomos_decisions WHERE decision_id = %s ORDER BY revision DESC LIMIT 1",
                    (record.result.decision_id,),
                )
                row = cur.fetchone()
                expected_revision = (row["revision"] + 1) if row else 1
                if record.revision != expected_revision:
                    raise ValueError(
                        f"revision must be {expected_revision} for {record.result.decision_id}; "
                        f"received {record.revision}"
                    )
                if row and record.parent_record_hash:
                    cur.execute(
                        "SELECT record_hash FROM nomos_decisions WHERE decision_id = %s AND revision = %s",
                        (record.result.decision_id, record.revision - 1),
                    )
                    parent = cur.fetchone()
                    if parent and parent["record_hash"] != record.parent_record_hash:
                        raise ValueError("parent_record_hash does not match the latest revision")
                cur.execute(
                    sql.SQL(
                        "INSERT INTO nomos_decisions (decision_id, revision, record_hash, body) "
                        "VALUES (%s, %s, %s, %s::jsonb)"
                    ),
                    (
                        record.result.decision_id,
                        record.revision,
                        record.record_hash,
                        record.model_dump_json(),
                    ),
                )
                conn.commit()

    def get(self, decision_id: str) -> DecisionRecord | None:
        with self._lock:
            with self._conn() as conn, conn.cursor() as cur:
                cur.execute(
                    "SELECT body FROM nomos_decisions WHERE decision_id = %s ORDER BY revision DESC LIMIT 1",
                    (decision_id,),
                )
                row = cur.fetchone()
                if row is None:
                    return None
                record = DecisionRecord.model_validate(json.loads(row["body"]))
                history = self.history(decision_id)
                if history and not verify_chain(history):
                    raise ValueError(f"integrity verification failed for {decision_id}")
                return record

    def history(self, decision_id: str) -> list[DecisionRecord]:
        with self._lock:
            with self._conn() as conn, conn.cursor() as cur:
                cur.execute(
                    "SELECT body FROM nomos_decisions WHERE decision_id = %s ORDER BY revision ASC",
                    (decision_id,),
                )
                rows = cur.fetchall()
                records = [DecisionRecord.model_validate(json.loads(r["body"])) for r in rows]
                if records and not verify_chain(records):
                    raise ValueError(f"integrity verification failed for {decision_id}")
                return records


class PostgresHubReportRepository:
    """PostgreSQL-backed immutable store for sealed Hub reports."""

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._lock = RLock()
        self._ensure_tables()

    def _conn(self):
        return psycopg2.connect(self._dsn, cursor_factory=psycopg2.extras.RealDictCursor)

    def _ensure_tables(self) -> None:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS nomos_hub_reports (
                    hub_run_id  TEXT        PRIMARY KEY,
                    body        JSONB       NOT NULL,
                    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
                """
            )
            conn.commit()

    def put(self, report: HubReport) -> None:
        with self._lock:
            if not verify_hub_report(report):
                raise ValueError("Hub report fails integrity verification")
            with self._conn() as conn, conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM nomos_hub_reports WHERE hub_run_id = %s",
                    (report.hub_run_id,),
                )
                if cur.fetchone():
                    raise ValueError(f"Hub report {report.hub_run_id} already exists")
                cur.execute(
                    sql.SQL(
                        "INSERT INTO nomos_hub_reports (hub_run_id, body) VALUES (%s, %s::jsonb)"
                    ),
                    (report.hub_run_id, report.model_dump_json()),
                )
                conn.commit()

    def get(self, hub_run_id: str) -> HubReport | None:
        with self._lock:
            with self._conn() as conn, conn.cursor() as cur:
                cur.execute(
                    "SELECT body FROM nomos_hub_reports WHERE hub_run_id = %s",
                    (hub_run_id,),
                )
                row = cur.fetchone()
                if row is None:
                    return None
                report = HubReport.model_validate(json.loads(row["body"]))
                if not verify_hub_report(report):
                    raise ValueError(f"integrity verification failed for {hub_run_id}")
                return report


class PostgresSessionRepository:
    """PostgreSQL-backed store for reconstruction sessions."""

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._lock = RLock()
        self._ensure_tables()

    def _conn(self):
        return psycopg2.connect(self._dsn, cursor_factory=psycopg2.extras.RealDictCursor)

    def _ensure_tables(self) -> None:
        with self._conn() as conn, conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS nomos_sessions (
                    session_id  TEXT        PRIMARY KEY,
                    body        JSONB       NOT NULL,
                    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
                """
            )
            conn.commit()

    def put(self, session: ReconstructionSession) -> None:
        with self._lock:
            with self._conn() as conn, conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM nomos_sessions WHERE session_id = %s",
                    (session.session_id,),
                )
                if cur.fetchone():
                    raise ValueError(f"Session {session.session_id} already exists")
                cur.execute(
                    sql.SQL(
                        "INSERT INTO nomos_sessions (session_id, body) VALUES (%s, %s::jsonb)"
                    ),
                    (session.session_id, session.model_dump_json()),
                )
                conn.commit()

    def update(self, session: ReconstructionSession) -> None:
        with self._lock:
            with self._conn() as conn, conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM nomos_sessions WHERE session_id = %s",
                    (session.session_id,),
                )
                if not cur.fetchone():
                    raise ValueError(f"Session {session.session_id} does not exist")
                cur.execute(
                    sql.SQL(
                        "UPDATE nomos_sessions SET body = %s::jsonb WHERE session_id = %s"
                    ),
                    (session.model_dump_json(), session.session_id),
                )
                conn.commit()

    def get(self, session_id: str) -> ReconstructionSession | None:
        with self._lock:
            with self._conn() as conn, conn.cursor() as cur:
                cur.execute(
                    "SELECT body FROM nomos_sessions WHERE session_id = %s",
                    (session_id,),
                )
                row = cur.fetchone()
                if row is None:
                    return None
                return ReconstructionSession.model_validate(json.loads(row["body"]))