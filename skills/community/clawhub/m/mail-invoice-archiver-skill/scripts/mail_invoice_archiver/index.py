from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from .models import InvoiceMetadata


def _canonical_score(row: sqlite3.Row) -> tuple[int, int, int, int]:
    status_score = 2 if row["status"] == "saved" and row["duplicate_of_id"] is None else 1 if row["status"] in {"saved", "conflict"} else 0
    extension = (row["extension"] or "").lower()
    extension_score = {
        "png": 5,
        "jpg": 5,
        "jpeg": 5,
        "pdf": 4,
        "xml": 3,
        "ofd": 2,
        "zip": 1,
    }.get(extension, 0)
    metadata_score = sum(1 for key in ["invoice_number", "amount_cents", "invoice_date", "vendor"] if row[key] not in (None, ""))
    return (status_score, extension_score, metadata_score, -int(row["id"]))


class ArchiveIndex:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._ensure_schema()

    def close(self) -> None:
        self.conn.close()

    def _ensure_schema(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS artifacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account TEXT NOT NULL,
                folder TEXT NOT NULL,
                message_uid TEXT NOT NULL,
                part_ref TEXT NOT NULL,
                source_kind TEXT NOT NULL,
                source_ref TEXT NOT NULL,
                received_at TEXT,
                sender TEXT,
                subject TEXT,
                preview TEXT,
                local_path TEXT,
                sha256 TEXT NOT NULL,
                mime_type TEXT,
                extension TEXT,
                invoice_number TEXT,
                invoice_code TEXT,
                amount_cents INTEGER,
                currency TEXT,
                invoice_date TEXT,
                vendor TEXT,
                business_key TEXT NOT NULL,
                status TEXT NOT NULL,
                duplicate_of_id INTEGER,
                extraction_sources TEXT,
                failure_reason TEXT,
                created_at TEXT NOT NULL,
                UNIQUE(account, folder, message_uid, source_kind, part_ref)
            );
            CREATE INDEX IF NOT EXISTS idx_artifacts_business_key ON artifacts (business_key);
            CREATE INDEX IF NOT EXISTS idx_artifacts_invoice_number ON artifacts (invoice_number);
            """
        )
        self.conn.commit()

    def find_canonical(self, business_key: str) -> sqlite3.Row | None:
        rows = list(
            self.conn.execute(
                """
                SELECT * FROM artifacts
                WHERE business_key = ? AND status IN ('saved', 'conflict') AND duplicate_of_id IS NULL
                ORDER BY id ASC
                """,
                (business_key,),
            ).fetchall()
        )
        if not rows:
            return None
        best = rows[0]
        for row in rows[1:]:
            if _canonical_score(row) > _canonical_score(best):
                best = row
        return best

    def find_same_invoice_number(self, invoice_number: str) -> list[sqlite3.Row]:
        return list(
            self.conn.execute(
                """
                SELECT * FROM artifacts
                WHERE invoice_number = ? AND status IN ('saved', 'conflict') AND duplicate_of_id IS NULL
                ORDER BY id ASC
                """,
                (invoice_number,),
            ).fetchall()
        )

    def demote_artifact_to_duplicate(self, artifact_id: int, duplicate_of_id: int) -> None:
        self.conn.execute(
            """
            UPDATE artifacts
            SET status = 'duplicate', duplicate_of_id = ?, local_path = NULL
            WHERE id = ?
            """,
            (duplicate_of_id, artifact_id),
        )
        self.conn.commit()

    def update_artifact_path_and_extension(self, artifact_id: int, local_path: str, extension: str, mime_type: str, sha256: str) -> None:
        self.conn.execute(
            """
            UPDATE artifacts
            SET local_path = ?, extension = ?, mime_type = ?, sha256 = ?, status = 'saved', duplicate_of_id = NULL
            WHERE id = ?
            """,
            (local_path, extension, mime_type, sha256, artifact_id),
        )
        self.conn.commit()

    def insert_artifact(
        self,
        *,
        account: str,
        folder: str,
        message_uid: str,
        part_ref: str,
        source_kind: str,
        source_ref: str,
        received_at: str | None,
        sender: str,
        subject: str,
        preview: str,
        local_path: str | None,
        sha256: str,
        mime_type: str,
        extension: str,
        metadata: InvoiceMetadata,
        business_key: str,
        status: str,
        duplicate_of_id: int | None,
        failure_reason: str | None = None,
    ) -> int:
        cursor = self.conn.execute(
            """
            INSERT OR REPLACE INTO artifacts (
                account, folder, message_uid, part_ref, source_kind, source_ref,
                received_at, sender, subject, preview, local_path, sha256, mime_type,
                extension, invoice_number, invoice_code, amount_cents, currency,
                invoice_date, vendor, business_key, status, duplicate_of_id,
                extraction_sources, failure_reason, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                account,
                folder,
                message_uid,
                part_ref,
                source_kind,
                source_ref,
                received_at,
                sender,
                subject,
                preview,
                local_path,
                sha256,
                mime_type,
                extension,
                metadata.invoice_number,
                metadata.invoice_code,
                metadata.amount_cents,
                metadata.currency,
                metadata.invoice_date,
                metadata.vendor,
                business_key,
                status,
                duplicate_of_id,
                json.dumps(metadata.extraction_sources, ensure_ascii=False),
                failure_reason,
                datetime.utcnow().isoformat(timespec="seconds"),
            ),
        )
        self.conn.commit()
        return int(cursor.lastrowid)

    def month_rows(self, month: str) -> list[sqlite3.Row]:
        return list(
            self.conn.execute(
                """
                SELECT * FROM artifacts
                WHERE substr(received_at, 1, 7) = ?
                ORDER BY received_at ASC, id ASC
                """,
                (month,),
            ).fetchall()
        )

    def month_summary(self, month: str, high_value_threshold: int) -> dict[str, object]:
        rows = self.month_rows(month)
        duplicates = [row for row in rows if row["status"] == "duplicate"]
        failures = [row for row in rows if row["status"] == "failed"]
        conflicts = [row for row in rows if row["status"] == "conflict"]

        canonical_by_business_key: dict[str, sqlite3.Row] = {}
        for row in rows:
            if row["status"] == "failed":
                continue
            business_key = row["business_key"]
            current = canonical_by_business_key.get(business_key)
            if current is None:
                canonical_by_business_key[business_key] = row
                continue
            current_score = _canonical_score(current)
            row_score = _canonical_score(row)
            if row_score > current_score or (row_score == current_score and row["id"] < current["id"]):
                canonical_by_business_key[business_key] = row

        canonical = list(canonical_by_business_key.values())
        canonical.sort(key=lambda row: ((row["received_at"] or ""), row["id"]))
        unknown_amount = [row for row in canonical if row["amount_cents"] is None]
        total_amount_cents = sum(row["amount_cents"] or 0 for row in canonical)
        high_value = [row for row in canonical if (row["amount_cents"] or 0) >= high_value_threshold * 100]
        return {
            "month": month,
            "canonical_count": len(canonical),
            "duplicate_count": len(duplicates),
            "failure_count": len(failures),
            "conflict_count": len(conflicts),
            "unknown_amount_count": len(unknown_amount),
            "total_amount_cents": total_amount_cents,
            "high_value_threshold": high_value_threshold,
            "high_value": [dict(row) for row in high_value],
            "failures": [dict(row) for row in failures],
            "conflicts": [dict(row) for row in conflicts],
            "canonical_rows": [dict(row) for row in canonical],
        }
