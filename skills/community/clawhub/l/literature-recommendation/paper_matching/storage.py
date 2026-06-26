"""PostgreSQL storage layer for profiles, papers, and recommendations."""

from __future__ import annotations

import json
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Iterator

import psycopg
from psycopg.rows import dict_row

from .models import MemberProfile, Paper, Recommendation


SCHEMA_POSTGRES = """
CREATE TABLE IF NOT EXISTS member_profiles (
    record_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    team_name TEXT,
    primary_direction TEXT,
    secondary_directions JSONB DEFAULT '[]'::jsonb,
    keywords JSONB DEFAULT '[]'::jsonb,
    excluded_topics JSONB DEFAULT '[]'::jsonb,
    feishu_user_id TEXT,
    source TEXT DEFAULT 'manual',
    confidence REAL DEFAULT 1.0,
    version INTEGER DEFAULT 1,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS papers (
    paper_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    abstract TEXT NOT NULL,
    authors JSONB NOT NULL DEFAULT '[]'::jsonb,
    published_at TIMESTAMPTZ,
    source TEXT NOT NULL,
    url TEXT NOT NULL,
    tags JSONB NOT NULL DEFAULT '[]'::jsonb,
    raw_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS recommendations (
    run_id TEXT NOT NULL,
    record_id TEXT NOT NULL,
    paper_id TEXT NOT NULL,
    score DOUBLE PRECISION NOT NULL,
    rank INTEGER NOT NULL,
    reason TEXT NOT NULL,
    channel TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (run_id, record_id, paper_id, channel)
);

CREATE TABLE IF NOT EXISTS run_history (
    run_id TEXT PRIMARY KEY,
    started_at TIMESTAMPTZ NOT NULL,
    finished_at TIMESTAMPTZ,
    status TEXT NOT NULL,
    notes TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS behavior_events (
    event_id TEXT PRIMARY KEY,
    record_id TEXT NOT NULL,
    paper_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_value TEXT DEFAULT '',
    channel TEXT DEFAULT '',
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def _as_json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def _load_json_field(value: Any, fallback: Any) -> Any:
    if value is None:
        return fallback
    if isinstance(value, (list, dict)):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return fallback
        return json.loads(text)
    return fallback


def _to_iso(value: Any) -> str:
    if value is None:
        return datetime.now(timezone.utc).isoformat()
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc).isoformat()
        return value.isoformat()
    return str(value)


class Storage:
    def __init__(self, db_dsn: str):
        self.db_dsn = db_dsn.strip()
        if not self.db_dsn:
            raise RuntimeError("OPENCLAW_DB_DSN is required.")
        self._init_schema()

    @contextmanager
    def connection(self) -> Iterator[Any]:
        conn = psycopg.connect(self.db_dsn, row_factory=dict_row)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_schema(self) -> None:
        with self.connection() as conn:
            conn.execute(SCHEMA_POSTGRES)

    def load_profiles(self) -> list[MemberProfile]:
        with self.connection() as conn:
            rows = conn.execute("SELECT * FROM member_profiles ORDER BY display_name").fetchall()

        return [
            MemberProfile.from_dict(
                {
                    "record_id": row["record_id"],
                    "display_name": row["display_name"],
                    "team_name": row.get("team_name") or "",
                    "primary_direction": row.get("primary_direction") or "",
                    "secondary_directions": _load_json_field(row.get("secondary_directions"), []),
                    "keywords": _load_json_field(row.get("keywords"), []),
                    "excluded_topics": _load_json_field(row.get("excluded_topics"), []),
                    "feishu_user_id": row.get("feishu_user_id") or "",
                    "source": row.get("source") or "manual",
                    "confidence": row.get("confidence") if row.get("confidence") is not None else 1.0,
                    "version": row.get("version") if row.get("version") is not None else 1,
                    "updated_at": _to_iso(row.get("updated_at")),
                }
            )
            for row in rows
        ]

    def upsert_paper(self, paper: Paper) -> None:
        fetched_at = datetime.now(timezone.utc).isoformat()
        with self.connection() as conn:
            conn.execute(
                """
                INSERT INTO papers (
                    paper_id, title, abstract, authors, published_at,
                    source, url, tags, raw_json, fetched_at
                ) VALUES (%s, %s, %s, %s::jsonb, %s, %s, %s, %s::jsonb, %s::jsonb, %s)
                ON CONFLICT(paper_id) DO UPDATE SET
                    title=EXCLUDED.title,
                    abstract=EXCLUDED.abstract,
                    authors=EXCLUDED.authors,
                    published_at=EXCLUDED.published_at,
                    source=EXCLUDED.source,
                    url=EXCLUDED.url,
                    tags=EXCLUDED.tags,
                    raw_json=EXCLUDED.raw_json,
                    fetched_at=EXCLUDED.fetched_at
                """,
                (
                    paper.paper_id,
                    paper.title,
                    paper.abstract,
                    _as_json_text(paper.authors),
                    paper.published_at,
                    paper.source,
                    paper.url,
                    _as_json_text(paper.tags),
                    _as_json_text(paper.raw),
                    fetched_at,
                ),
            )

    def save_papers(self, papers: list[Paper]) -> None:
        for paper in papers:
            self.upsert_paper(paper)

    def load_recent_papers(self, limit: int = 500) -> list[Paper]:
        with self.connection() as conn:
            rows = conn.execute(
                "SELECT * FROM papers ORDER BY published_at DESC NULLS LAST LIMIT %s",
                (limit,),
            ).fetchall()

        return [
            Paper.from_dict(
                {
                    "paper_id": row["paper_id"],
                    "title": row["title"],
                    "abstract": row["abstract"],
                    "authors": _load_json_field(row.get("authors"), []),
                    "published_at": _to_iso(row.get("published_at")),
                    "source": row["source"],
                    "url": row["url"],
                    "tags": _load_json_field(row.get("tags"), []),
                    "raw": _load_json_field(row.get("raw_json"), {}),
                }
            )
            for row in rows
        ]

    def save_recommendations(self, run_id: str, recommendations: list[Recommendation]) -> None:
        with self.connection() as conn:
            for rec in recommendations:
                conn.execute(
                    """
                    INSERT INTO recommendations (
                        run_id, record_id, paper_id, score, rank, reason, channel, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (run_id, record_id, paper_id, channel) DO UPDATE SET
                        score=EXCLUDED.score,
                        rank=EXCLUDED.rank,
                        reason=EXCLUDED.reason,
                        created_at=EXCLUDED.created_at
                    """,
                    (
                        run_id,
                        rec.record_id,
                        rec.paper_id,
                        rec.score,
                        rec.rank,
                        rec.reason,
                        rec.channel,
                        rec.created_at,
                    ),
                )

    def save_run_status(self, run_id: str, status: str, started_at: str, finished_at: str | None = None, notes: str = "") -> None:
        with self.connection() as conn:
            conn.execute(
                """
                INSERT INTO run_history (run_id, started_at, finished_at, status, notes)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT(run_id) DO UPDATE SET
                    started_at=EXCLUDED.started_at,
                    finished_at=EXCLUDED.finished_at,
                    status=EXCLUDED.status,
                    notes=EXCLUDED.notes
                """,
                (run_id, started_at, finished_at, status, notes),
            )
