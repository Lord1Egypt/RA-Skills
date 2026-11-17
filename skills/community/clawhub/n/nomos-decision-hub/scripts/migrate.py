#!/usr/bin/env python
"""NOMOS schema migration runner (v0.5).

Idempotent DDL that ensures every required table/column exists for the v0.5
enterprise control plane (tenant columns + the append-only event store).

Usage:
    SP_DATABASE_DSN=postgresql://user:pass@host/db python scripts/migrate.py
"""

from __future__ import annotations

import os
import sys

import psycopg2
import psycopg2.extras

DDL = [
    # Forward-compatible tenant columns on legacy tables (default global tenant).
    "ALTER TABLE nomos_decisions ADD COLUMN IF NOT EXISTS tenant_id TEXT NOT NULL DEFAULT '';",
    "CREATE INDEX IF NOT EXISTS idx_decisions_tenant ON nomos_decisions (tenant_id, decision_id);",
    "ALTER TABLE nomos_hub_reports ADD COLUMN IF NOT EXISTS tenant_id TEXT NOT NULL DEFAULT '';",
    "ALTER TABLE nomos_sessions ADD COLUMN IF NOT EXISTS tenant_id TEXT NOT NULL DEFAULT '';",
    # Append-only event store.
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
    """,
    "CREATE INDEX IF NOT EXISTS idx_events_agg ON nomos_events (aggregate_id);",
    "CREATE INDEX IF NOT EXISTS idx_events_tenant ON nomos_events (tenant_id);",
]


def main() -> int:
    dsn = os.getenv("SP_DATABASE_DSN", "").strip()
    if not dsn:
        print("SP_DATABASE_DSN not set; nothing to migrate.", file=sys.stderr)
        return 1
    conn = psycopg2.connect(dsn, cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        with conn.cursor() as cur:
            for statement in DDL:
                cur.execute(statement)
        conn.commit()
        print("migration complete")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
