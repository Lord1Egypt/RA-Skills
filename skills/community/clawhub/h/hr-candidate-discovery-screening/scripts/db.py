from __future__ import annotations

import argparse
import json
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable, Iterator

if TYPE_CHECKING:
    from models import PaperRecord


class ApprovalRequired(RuntimeError):
    pass


SCHEMA = """
CREATE TABLE IF NOT EXISTS papers (
    id TEXT PRIMARY KEY,
    source_key TEXT NOT NULL,
    source_type TEXT NOT NULL,
    source_record_id TEXT NOT NULL,
    doi TEXT,
    title TEXT NOT NULL,
    normalized_title TEXT NOT NULL,
    abstract TEXT,
    original_keywords_json TEXT NOT NULL DEFAULT '[]',
    generated_keywords_json TEXT NOT NULL DEFAULT '[]',
    keyword_model TEXT,
    keyword_prompt_version TEXT,
    keywords_generated_at TEXT,
    official_url TEXT,
    acceptance_evidence_url TEXT,
    publication_date TEXT NOT NULL,
    publication_date_precision TEXT NOT NULL DEFAULT 'day',
    is_retracted INTEGER NOT NULL DEFAULT 0,
    collected_at TEXT NOT NULL,
    UNIQUE(source_key, source_record_id)
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_papers_doi
    ON papers(doi) WHERE doi IS NOT NULL AND doi != '';
CREATE INDEX IF NOT EXISTS idx_papers_normalized_title ON papers(normalized_title);

CREATE TABLE IF NOT EXISTS authors (
    id TEXT PRIMARY KEY,
    normalized_name TEXT NOT NULL,
    display_name TEXT NOT NULL,
    orcid TEXT,
    openalex_id TEXT,
    dblp_id TEXT,
    current_institution TEXT,
    current_status TEXT,
    public_email TEXT,
    homepage_url TEXT,
    mainland_china INTEGER,
    contact_suppressed INTEGER NOT NULL DEFAULT 0,
    contact_suppression_reason TEXT,
    confidence REAL,
    verification_status TEXT NOT NULL DEFAULT '待调查',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS paper_authors (
    paper_id TEXT NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    author_id TEXT NOT NULL REFERENCES authors(id) ON DELETE CASCADE,
    author_order INTEGER NOT NULL,
    role TEXT NOT NULL,
    role_evidence_url TEXT,
    PRIMARY KEY (paper_id, author_id, role)
);

CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    active INTEGER NOT NULL,
    config_json TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS job_snapshots (
    id TEXT PRIMARY KEY,
    job_id TEXT NOT NULL REFERENCES jobs(id),
    config_json TEXT NOT NULL,
    config_hash TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS paper_job_matches (
    id TEXT PRIMARY KEY,
    paper_id TEXT NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    job_snapshot_id TEXT NOT NULL REFERENCES job_snapshots(id),
    classification TEXT NOT NULL,
    result_json TEXT NOT NULL,
    model TEXT NOT NULL,
    prompt_version TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(paper_id, job_snapshot_id)
);

CREATE TABLE IF NOT EXISTS candidates (
    id TEXT PRIMARY KEY,
    author_id TEXT NOT NULL REFERENCES authors(id),
    job_snapshot_id TEXT NOT NULL REFERENCES job_snapshots(id),
    status TEXT NOT NULL,
    education_result TEXT,
    recommendation TEXT,
    suppressed INTEGER NOT NULL DEFAULT 0,
    suppression_reason TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(author_id, job_snapshot_id)
);

CREATE TABLE IF NOT EXISTS approvals (
    id TEXT PRIMARY KEY,
    action TEXT NOT NULL,
    target_type TEXT NOT NULL,
    target_id TEXT NOT NULL,
    decision TEXT NOT NULL,
    preview_json TEXT NOT NULL,
    decided_by TEXT NOT NULL,
    decided_at TEXT NOT NULL,
    consumed_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_approvals_lookup
    ON approvals(action, target_type, target_id, decision, consumed_at);

CREATE TABLE IF NOT EXISTS mail_threads (
    id TEXT PRIMARY KEY,
    author_id TEXT REFERENCES authors(id),
    candidate_id TEXT REFERENCES candidates(id),
    candidate_ids_json TEXT NOT NULL DEFAULT '[]',
    job_snapshot_id TEXT REFERENCES job_snapshots(id),
    message_type TEXT NOT NULL,
    mailbox TEXT,
    recipient TEXT NOT NULL,
    subject TEXT NOT NULL,
    body_html TEXT NOT NULL DEFAULT '',
    draft_id TEXT,
    message_id TEXT,
    thread_id TEXT,
    delivery_status TEXT,
    sent_at TEXT,
    last_synced_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS followups (
    id TEXT PRIMARY KEY,
    author_id TEXT NOT NULL REFERENCES authors(id),
    candidate_id TEXT NOT NULL REFERENCES candidates(id),
    mail_thread_id TEXT REFERENCES mail_threads(id),
    sequence INTEGER NOT NULL,
    due_date TEXT NOT NULL,
    status TEXT NOT NULL,
    draft_id TEXT,
    approved_at TEXT,
    sent_at TEXT,
    UNIQUE(candidate_id, sequence)
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    target_type TEXT,
    target_id TEXT,
    details_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS source_runs (
    id TEXT PRIMARY KEY,
    source_key TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    status TEXT NOT NULL,
    cursor TEXT,
    saved_count INTEGER NOT NULL DEFAULT 0,
    error TEXT,
    started_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(source_key, start_date, end_date)
);

CREATE TABLE IF NOT EXISTS author_evidence (
    id TEXT PRIMARY KEY,
    author_id TEXT NOT NULL REFERENCES authors(id) ON DELETE CASCADE,
    source_type TEXT NOT NULL,
    source_url TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    page_date TEXT,
    summary TEXT NOT NULL,
    institution TEXT,
    role TEXT,
    email TEXT,
    orcid TEXT,
    openalex_id TEXT,
    dblp_id TEXT,
    google_scholar_url TEXT,
    mainland_china INTEGER,
    confidence REAL NOT NULL,
    created_at TEXT NOT NULL
);
"""


MIGRATION_COLUMNS = {
    "papers": {
        "keyword_model": "TEXT",
        "keyword_prompt_version": "TEXT",
        "keywords_generated_at": "TEXT",
        "publication_date_precision": "TEXT NOT NULL DEFAULT 'day'",
    },
    "authors": {
        "contact_suppressed": "INTEGER NOT NULL DEFAULT 0",
        "contact_suppression_reason": "TEXT",
    },
    "mail_threads": {
        "candidate_ids_json": "TEXT NOT NULL DEFAULT '[]'",
        "body_html": "TEXT NOT NULL DEFAULT ''",
    },
    "author_evidence": {
        "mainland_china": "INTEGER",
    },
}


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


class Database:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self) -> None:
        with self.connection() as connection:
            connection.executescript(SCHEMA)
            for table, columns in MIGRATION_COLUMNS.items():
                existing = {
                    str(row["name"])
                    for row in connection.execute(f"PRAGMA table_info({table})")
                }
                for column, definition in columns.items():
                    if column not in existing:
                        connection.execute(
                            f"ALTER TABLE {table} ADD COLUMN {column} {definition}"
                        )

    def table_names(self) -> list[str]:
        with self.connection() as connection:
            rows = connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
            ).fetchall()
        return [str(row["name"]) for row in rows]

    def column_names(self, table: str) -> list[str]:
        if table not in MIGRATION_COLUMNS and table not in self.table_names():
            raise ValueError(f"Unknown table: {table}")
        with self.connection() as connection:
            rows = connection.execute(f"PRAGMA table_info({table})").fetchall()
        return [str(row["name"]) for row in rows]

    def execute(self, sql: str, parameters: tuple[Any, ...] = ()) -> None:
        with self.connection() as connection:
            connection.execute(sql, parameters)

    def fetch_one(
        self, sql: str, parameters: tuple[Any, ...] = ()
    ) -> sqlite3.Row | None:
        with self.connection() as connection:
            return connection.execute(sql, parameters).fetchone()

    def fetch_all(
        self, sql: str, parameters: tuple[Any, ...] = ()
    ) -> list[sqlite3.Row]:
        with self.connection() as connection:
            return connection.execute(sql, parameters).fetchall()

    def record_approval(
        self,
        *,
        action: str,
        target_type: str,
        target_id: str,
        decision: str,
        preview: dict[str, Any],
        decided_by: str,
    ) -> str:
        approval_id = str(uuid.uuid4())
        self.execute(
            """
            INSERT INTO approvals (
                id, action, target_type, target_id, decision, preview_json,
                decided_by, decided_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                approval_id,
                action,
                target_type,
                target_id,
                decision,
                json.dumps(preview, ensure_ascii=False, sort_keys=True),
                decided_by,
                utc_now(),
            ),
        )
        return approval_id

    def authorize_action(
        self, action: str, target_type: str, target_id: str
    ) -> str:
        with self.connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                """
                SELECT id FROM approvals
                WHERE action = ?
                  AND target_type = ?
                  AND target_id = ?
                  AND decision = 'approved'
                  AND consumed_at IS NULL
                ORDER BY decided_at
                LIMIT 1
                """,
                (action, target_type, target_id),
            ).fetchone()
            if row is None:
                raise ApprovalRequired(
                    f"Approval required for {action} on {target_type}:{target_id}"
                )
            approval_id = str(row["id"])
            connection.execute(
                "UPDATE approvals SET consumed_at = ? WHERE id = ?",
                (utc_now(), approval_id),
            )
            return approval_id

    def status(self) -> dict[str, int]:
        names = ("papers", "authors", "candidates", "approvals", "mail_threads")
        result: dict[str, int] = {}
        with self.connection() as connection:
            for name in names:
                row = connection.execute(f"SELECT COUNT(*) AS count FROM {name}").fetchone()
                result[name] = int(row["count"])
        return result

    def save_page_and_checkpoint(
        self,
        *,
        records: Iterable["PaperRecord"],
        source_key: str,
        start_date: str,
        end_date: str,
        next_cursor: str | None,
        completed: bool = False,
    ) -> int:
        now = utc_now()
        run_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                f"source-run:{source_key}:{start_date}:{end_date}",
            )
        )
        saved = 0
        with self.connection() as connection:
            for record in records:
                paper_id = str(
                    uuid.uuid5(
                        uuid.NAMESPACE_URL,
                        f"paper:{record.doi or f'{record.source_key}:{record.source_record_id}'}",
                    )
                )
                cursor = connection.execute(
                    """
                    INSERT OR IGNORE INTO papers (
                        id, source_key, source_type, source_record_id, doi, title,
                        normalized_title, abstract, original_keywords_json,
                        official_url, acceptance_evidence_url, publication_date,
                        publication_date_precision, is_retracted, collected_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        paper_id,
                        record.source_key,
                        record.source_type,
                        record.source_record_id,
                        record.doi,
                        record.title,
                        record.normalized_title,
                        record.abstract,
                        json.dumps(record.original_keywords, ensure_ascii=False),
                        record.official_url,
                        record.acceptance_evidence_url,
                        record.publication_date.isoformat(),
                        record.publication_date_precision,
                        int(record.is_retracted),
                        now,
                    ),
                )
                saved += int(cursor.rowcount > 0)
                for author in record.authors:
                    author_key = (
                        author.get("openalex_id")
                        or f"{author.get('name')}:{'|'.join(author.get('affiliations') or [])}"
                    )
                    author_id = str(
                        uuid.uuid5(uuid.NAMESPACE_URL, f"author:{author_key}")
                    )
                    display_name = str(author.get("name") or "").strip()
                    if not display_name:
                        continue
                    connection.execute(
                        """
                        INSERT OR IGNORE INTO authors (
                            id, normalized_name, display_name, orcid, openalex_id,
                            verification_status, created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, '待调查', ?, ?)
                        """,
                        (
                            author_id,
                            " ".join(display_name.casefold().split()),
                            display_name,
                            author.get("orcid"),
                            author.get("openalex_id"),
                            now,
                            now,
                        ),
                    )
                    role = "first" if int(author.get("order", 0)) == 1 else "middle"
                    connection.execute(
                        """
                        INSERT OR IGNORE INTO paper_authors (
                            paper_id, author_id, author_order, role, role_evidence_url
                        ) VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            paper_id,
                            author_id,
                            int(author.get("order", 0)),
                            role,
                            record.acceptance_evidence_url,
                        ),
                    )
            previous = connection.execute(
                """
                SELECT saved_count FROM source_runs
                WHERE source_key = ? AND start_date = ? AND end_date = ?
                """,
                (source_key, start_date, end_date),
            ).fetchone()
            total_saved = int(previous["saved_count"]) + saved if previous else saved
            connection.execute(
                """
                INSERT INTO source_runs (
                    id, source_key, start_date, end_date, status, cursor,
                    saved_count, error, started_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, NULL, ?, ?)
                ON CONFLICT(source_key, start_date, end_date) DO UPDATE SET
                    status = excluded.status,
                    cursor = excluded.cursor,
                    saved_count = excluded.saved_count,
                    error = NULL,
                    updated_at = excluded.updated_at
                """,
                (
                    run_id,
                    source_key,
                    start_date,
                    end_date,
                    "completed" if completed else "running",
                    next_cursor,
                    total_saved,
                    now,
                    now,
                ),
            )
        return saved

    def mark_source_error(
        self,
        source_key: str,
        start_date: str,
        end_date: str,
        error: str,
    ) -> None:
        self.execute(
            """
            UPDATE source_runs
            SET status = 'failed', error = ?, updated_at = ?
            WHERE source_key = ? AND start_date = ? AND end_date = ?
            """,
            (error, utc_now(), source_key, start_date, end_date),
        )

    def get_source_checkpoint(
        self, source_key: str, start_date: str, end_date: str
    ) -> str | None:
        row = self.fetch_one(
            """
            SELECT cursor FROM source_runs
            WHERE source_key = ? AND start_date = ? AND end_date = ?
            """,
            (source_key, start_date, end_date),
        )
        return None if row is None else row["cursor"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage the recruitment SQLite database.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("init", "status"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--database", required=True)
    approve = subparsers.add_parser("approve")
    approve.add_argument("--database", required=True)
    approve.add_argument("--action", required=True)
    approve.add_argument("--target-type", required=True)
    approve.add_argument("--target-id", required=True)
    approve.add_argument("--preview-json", required=True)
    approve.add_argument("--decided-by", required=True)
    approve.add_argument("--decision", default="approved")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    database = Database(args.database)
    if args.command == "init":
        database.initialize()
        print(json.dumps({"database": str(database.path), "initialized": True}))
        return 0
    database.initialize()
    if args.command == "approve":
        preview = json.loads(args.preview_json)
        if not isinstance(preview, dict):
            raise ValueError("--preview-json must decode to a JSON object")
        approval_id = database.record_approval(
            action=args.action,
            target_type=args.target_type,
            target_id=args.target_id,
            decision=args.decision,
            preview=preview,
            decided_by=args.decided_by,
        )
        print(
            json.dumps(
                {"approval_id": approval_id, "decision": args.decision},
                ensure_ascii=False,
            )
        )
        return 0
    print(json.dumps(database.status(), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
