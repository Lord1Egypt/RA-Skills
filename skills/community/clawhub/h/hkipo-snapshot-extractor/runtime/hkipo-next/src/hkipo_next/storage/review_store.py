"""SQLite-backed persistence for review history records."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Sequence

from hkipo_next.contracts.review import (
    ReviewActualResult,
    ReviewRecord,
    ReviewRecordRevision,
    ReviewSuggestion,
    SuggestionAdoption,
)


class ReviewStore:
    """Persist and query review history records in SQLite."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS review_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    record_id TEXT NOT NULL UNIQUE,
                    command TEXT NOT NULL,
                    command_run_id TEXT NOT NULL,
                    batch_id TEXT,
                    symbol TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    parameter_version TEXT NOT NULL,
                    parameter_name TEXT,
                    risk_profile TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    score REAL NOT NULL,
                    data_status TEXT NOT NULL,
                    rule_version TEXT NOT NULL,
                    schema_version TEXT NOT NULL,
                    source_issue_count INTEGER NOT NULL DEFAULT 0,
                    prediction_payload_json TEXT NOT NULL,
                    actual_result_json TEXT,
                    actual_updated_at TEXT,
                    variance_note TEXT,
                    variance_updated_at TEXT
                );

                CREATE TABLE IF NOT EXISTS review_record_revisions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    revision_id TEXT NOT NULL UNIQUE,
                    record_id TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    actual_result_json TEXT,
                    variance_note TEXT,
                    FOREIGN KEY(record_id) REFERENCES review_records(record_id)
                );

                CREATE TABLE IF NOT EXISTS review_suggestions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    suggestion_id TEXT NOT NULL UNIQUE,
                    source TEXT NOT NULL,
                    record_id TEXT,
                    batch_id TEXT,
                    impact_scope TEXT NOT NULL,
                    title TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    rationale TEXT,
                    suggested_changes_json TEXT NOT NULL,
                    status TEXT NOT NULL,
                    imported_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS suggestion_adoptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    suggestion_id TEXT NOT NULL UNIQUE,
                    decision TEXT NOT NULL,
                    decided_at TEXT NOT NULL,
                    decision_note TEXT,
                    before_parameter_version TEXT,
                    after_parameter_version TEXT,
                    applied_changes_json TEXT NOT NULL,
                    FOREIGN KEY(suggestion_id) REFERENCES review_suggestions(suggestion_id)
                );

                CREATE INDEX IF NOT EXISTS idx_review_records_created_at
                ON review_records(created_at DESC);

                CREATE INDEX IF NOT EXISTS idx_review_records_symbol
                ON review_records(symbol);

                CREATE INDEX IF NOT EXISTS idx_review_records_run
                ON review_records(command_run_id);

                CREATE INDEX IF NOT EXISTS idx_review_record_revisions_record_id
                ON review_record_revisions(record_id, updated_at DESC);

                CREATE INDEX IF NOT EXISTS idx_review_suggestions_record_id
                ON review_suggestions(record_id);

                CREATE INDEX IF NOT EXISTS idx_review_suggestions_batch_id
                ON review_suggestions(batch_id);

                CREATE INDEX IF NOT EXISTS idx_suggestion_adoptions_suggestion_id
                ON suggestion_adoptions(suggestion_id);
                """
            )
            self._ensure_column(connection, "review_records", "actual_updated_at", "TEXT")

    def save_records(self, records: Sequence[ReviewRecord]) -> list[ReviewRecord]:
        self.initialize()
        with self._connect() as connection:
            connection.execute("BEGIN")
            for record in records:
                connection.execute(
                    """
                    INSERT INTO review_records (
                        record_id,
                        command,
                        command_run_id,
                        batch_id,
                        symbol,
                        created_at,
                        parameter_version,
                        parameter_name,
                        risk_profile,
                        decision,
                        score,
                        data_status,
                        rule_version,
                        schema_version,
                        source_issue_count,
                        prediction_payload_json,
                        actual_result_json,
                        actual_updated_at,
                        variance_note,
                        variance_updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        record.record_id,
                        record.command,
                        record.command_run_id,
                        record.batch_id,
                        record.symbol,
                        record.created_at.isoformat(),
                        record.parameter_version,
                        record.parameter_name,
                        record.risk_profile,
                        record.decision,
                        record.score,
                        record.data_status,
                        record.rule_version,
                        record.schema_version,
                        record.source_issue_count,
                        json.dumps(record.prediction_payload, ensure_ascii=False),
                        (
                            json.dumps(
                                record.actual_result.model_dump(mode="json"),
                                ensure_ascii=False,
                            )
                            if record.actual_result is not None
                            else None
                        ),
                        record.actual_updated_at.isoformat()
                        if record.actual_updated_at is not None
                        else None,
                        record.variance_note,
                        record.variance_updated_at.isoformat()
                        if record.variance_updated_at is not None
                        else None,
                    ),
                )
        return list(records)

    def list_records(
        self,
        *,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
        limit: int | None = None,
    ) -> list[ReviewRecord]:
        self.initialize()
        clauses: list[str] = []
        params: list[object] = []
        if from_date is not None:
            clauses.append("created_at >= ?")
            params.append(from_date.isoformat())
        if to_date is not None:
            clauses.append("created_at <= ?")
            params.append(to_date.isoformat())

        query = "SELECT * FROM review_records"
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY created_at DESC, id DESC"
        if limit is not None:
            query += " LIMIT ?"
            params.append(limit)

        with self._connect() as connection:
            rows = connection.execute(query, params).fetchall()
        return [self._row_to_record(row) for row in rows]

    def get_record(self, record_id: str) -> ReviewRecord | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM review_records WHERE record_id = ?",
                (record_id,),
            ).fetchone()
        return self._row_to_record(row) if row is not None else None

    def list_revisions(self, record_id: str) -> list[ReviewRecordRevision]:
        self.initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM review_record_revisions
                WHERE record_id = ?
                ORDER BY updated_at DESC, id DESC
                """,
                (record_id,),
            ).fetchall()
        return [self._row_to_revision(row) for row in rows]

    def update_record(
        self,
        *,
        record_id: str,
        actual_result: ReviewActualResult | None,
        variance_note: str | None,
        updated_at: datetime,
    ) -> ReviewRecord:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM review_records WHERE record_id = ?",
                (record_id,),
            ).fetchone()
            if row is None:
                raise KeyError(record_id)
            current = self._row_to_record(row)
            merged_actual = self._merge_actual_result(current.actual_result, actual_result)
            merged_variance_note = current.variance_note if variance_note is None else variance_note
            actual_updated_at = (
                updated_at
                if actual_result is not None and actual_result.model_dump(exclude_none=True)
                else current.actual_updated_at
            )
            variance_updated_at = updated_at if variance_note is not None else current.variance_updated_at
            connection.execute(
                """
                UPDATE review_records
                SET actual_result_json = ?, actual_updated_at = ?, variance_note = ?, variance_updated_at = ?
                WHERE record_id = ?
                """,
                (
                    json.dumps(merged_actual.model_dump(mode="json"), ensure_ascii=False)
                    if merged_actual is not None
                    else None,
                    actual_updated_at.isoformat() if actual_updated_at is not None else None,
                    merged_variance_note,
                    variance_updated_at.isoformat() if variance_updated_at is not None else None,
                    record_id,
                ),
            )
            revision_id = self._next_revision_id(connection, record_id)
            connection.execute(
                """
                INSERT INTO review_record_revisions (
                    revision_id,
                    record_id,
                    updated_at,
                    actual_result_json,
                    variance_note
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    revision_id,
                    record_id,
                    updated_at.isoformat(),
                    json.dumps(merged_actual.model_dump(mode="json"), ensure_ascii=False)
                    if merged_actual is not None
                    else None,
                    merged_variance_note,
                ),
            )
            row = connection.execute(
                "SELECT * FROM review_records WHERE record_id = ?",
                (record_id,),
            ).fetchone()
        return self._row_to_record(row)

    def save_suggestions(self, suggestions: Sequence[ReviewSuggestion]) -> list[ReviewSuggestion]:
        self.initialize()
        with self._connect() as connection:
            connection.execute("BEGIN")
            for suggestion in suggestions:
                connection.execute(
                    """
                    INSERT INTO review_suggestions (
                        suggestion_id,
                        source,
                        record_id,
                        batch_id,
                        impact_scope,
                        title,
                        summary,
                        rationale,
                        suggested_changes_json,
                        status,
                        imported_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(suggestion_id) DO UPDATE SET
                        source = excluded.source,
                        record_id = excluded.record_id,
                        batch_id = excluded.batch_id,
                        impact_scope = excluded.impact_scope,
                        title = excluded.title,
                        summary = excluded.summary,
                        rationale = excluded.rationale,
                        suggested_changes_json = excluded.suggested_changes_json
                    """,
                    (
                        suggestion.suggestion_id,
                        suggestion.source,
                        suggestion.record_id,
                        suggestion.batch_id,
                        suggestion.impact_scope,
                        suggestion.title,
                        suggestion.summary,
                        suggestion.rationale,
                        json.dumps(
                            [change.model_dump(mode="json") for change in suggestion.suggested_changes],
                            ensure_ascii=False,
                        ),
                        suggestion.status,
                        suggestion.imported_at.isoformat(),
                    ),
                )
        return list(suggestions)

    def list_suggestions(
        self,
        *,
        record_id: str | None = None,
        batch_id: str | None = None,
        status: str | None = None,
    ) -> list[ReviewSuggestion]:
        self.initialize()
        clauses: list[str] = []
        params: list[object] = []
        if record_id is not None:
            clauses.append("record_id = ?")
            params.append(record_id)
        if batch_id is not None:
            clauses.append("batch_id = ?")
            params.append(batch_id)
        if status is not None:
            clauses.append("status = ?")
            params.append(status)

        query = "SELECT * FROM review_suggestions"
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY imported_at DESC, id DESC"

        with self._connect() as connection:
            rows = connection.execute(query, params).fetchall()
        return [self._row_to_suggestion(row) for row in rows]

    def get_suggestion(self, suggestion_id: str) -> ReviewSuggestion | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM review_suggestions WHERE suggestion_id = ?",
                (suggestion_id,),
            ).fetchone()
        return self._row_to_suggestion(row) if row is not None else None

    def update_suggestion_status(self, suggestion_id: str, status: str) -> None:
        self.initialize()
        with self._connect() as connection:
            connection.execute(
                "UPDATE review_suggestions SET status = ? WHERE suggestion_id = ?",
                (status, suggestion_id),
            )

    def get_adoption(self, suggestion_id: str) -> SuggestionAdoption | None:
        self.initialize()
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM suggestion_adoptions WHERE suggestion_id = ?",
                (suggestion_id,),
            ).fetchone()
        return self._row_to_adoption(row) if row is not None else None

    def save_adoption(self, adoption: SuggestionAdoption) -> SuggestionAdoption:
        self.initialize()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO suggestion_adoptions (
                    suggestion_id,
                    decision,
                    decided_at,
                    decision_note,
                    before_parameter_version,
                    after_parameter_version,
                    applied_changes_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    adoption.suggestion_id,
                    adoption.decision,
                    adoption.decided_at.isoformat(),
                    adoption.decision_note,
                    adoption.before_parameter_version,
                    adoption.after_parameter_version,
                    json.dumps(
                        [change.model_dump(mode="json") for change in adoption.applied_changes],
                        ensure_ascii=False,
                    ),
                ),
            )
        return adoption

    def _connect(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    @staticmethod
    def _ensure_column(
        connection: sqlite3.Connection,
        table_name: str,
        column_name: str,
        column_definition: str,
    ) -> None:
        columns = {
            row["name"]
            for row in connection.execute(f"PRAGMA table_info({table_name})").fetchall()
        }
        if column_name not in columns:
            connection.execute(
                f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}"
            )

    @staticmethod
    def _row_to_record(row: sqlite3.Row) -> ReviewRecord:
        actual_result = None
        if row["actual_result_json"]:
            actual_result = ReviewActualResult.model_validate(json.loads(row["actual_result_json"]))
        return ReviewRecord(
            record_id=row["record_id"],
            command=row["command"],
            command_run_id=row["command_run_id"],
            batch_id=row["batch_id"],
            symbol=row["symbol"],
            created_at=datetime.fromisoformat(row["created_at"]),
            parameter_version=row["parameter_version"],
            parameter_name=row["parameter_name"],
            risk_profile=row["risk_profile"],
            decision=row["decision"],
            score=row["score"],
            data_status=row["data_status"],
            rule_version=row["rule_version"],
            schema_version=row["schema_version"],
            source_issue_count=row["source_issue_count"],
            prediction_payload=json.loads(row["prediction_payload_json"]),
            actual_result=actual_result,
            actual_updated_at=(
                datetime.fromisoformat(row["actual_updated_at"])
                if row["actual_updated_at"] is not None
                else None
            ),
            variance_note=row["variance_note"],
            variance_updated_at=(
                datetime.fromisoformat(row["variance_updated_at"])
                if row["variance_updated_at"] is not None
                else None
            ),
        )

    @staticmethod
    def _row_to_revision(row: sqlite3.Row) -> ReviewRecordRevision:
        actual_result = None
        if row["actual_result_json"]:
            actual_result = ReviewActualResult.model_validate(json.loads(row["actual_result_json"]))
        return ReviewRecordRevision(
            revision_id=row["revision_id"],
            record_id=row["record_id"],
            updated_at=datetime.fromisoformat(row["updated_at"]),
            actual_result=actual_result,
            variance_note=row["variance_note"],
        )

    @staticmethod
    def _merge_actual_result(
        current: ReviewActualResult | None,
        patch: ReviewActualResult | None,
    ) -> ReviewActualResult | None:
        if patch is None:
            return current
        if current is None:
            if not patch.model_dump(exclude_none=True):
                return None
            return patch
        merged = current.model_dump(mode="python")
        merged.update(patch.model_dump(mode="python", exclude_none=True))
        return ReviewActualResult.model_validate(merged)

    @staticmethod
    def _next_revision_id(connection: sqlite3.Connection, record_id: str) -> str:
        row = connection.execute(
            "SELECT COUNT(*) AS total FROM review_record_revisions WHERE record_id = ?",
            (record_id,),
        ).fetchone()
        next_number = int(row["total"]) + 1
        return f"{record_id}:rev{next_number:03d}"

    @staticmethod
    def _row_to_suggestion(row: sqlite3.Row) -> ReviewSuggestion:
        return ReviewSuggestion(
            suggestion_id=row["suggestion_id"],
            source=row["source"],
            record_id=row["record_id"],
            batch_id=row["batch_id"],
            impact_scope=row["impact_scope"],
            title=row["title"],
            summary=row["summary"],
            rationale=row["rationale"],
            suggested_changes=json.loads(row["suggested_changes_json"]),
            status=row["status"],
            imported_at=datetime.fromisoformat(row["imported_at"]),
        )

    @staticmethod
    def _row_to_adoption(row: sqlite3.Row) -> SuggestionAdoption:
        return SuggestionAdoption(
            suggestion_id=row["suggestion_id"],
            decision=row["decision"],
            decided_at=datetime.fromisoformat(row["decided_at"]),
            decision_note=row["decision_note"],
            before_parameter_version=row["before_parameter_version"],
            after_parameter_version=row["after_parameter_version"],
            applied_changes=json.loads(row["applied_changes_json"]),
        )
