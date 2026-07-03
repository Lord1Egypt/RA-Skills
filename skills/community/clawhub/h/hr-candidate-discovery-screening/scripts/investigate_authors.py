from __future__ import annotations

import argparse
import json
import uuid
from dataclasses import dataclass
from email.utils import parseaddr
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from config import load_settings
from db import Database, utc_now
from models import CandidateStatus


TARGET_ROLES = {"first", "cofirst", "corresponding"}
INVESTIGATED_MATCHES = {"高度匹配", "可能匹配"}


class EvidenceError(ValueError):
    pass


@dataclass(frozen=True)
class InvestigationQueueItem:
    candidate_id: str
    author_id: str
    paper_id: str
    job_snapshot_id: str
    role: str


@dataclass(frozen=True)
class ReconcileResult:
    status: CandidateStatus
    merged: bool
    reason: str


def queue_target_authors(database: Database) -> list[InvestigationQueueItem]:
    rows = database.fetch_all(
        """
        SELECT pa.paper_id, pa.author_id, pa.role, m.job_snapshot_id
        FROM paper_authors pa
        JOIN paper_job_matches m ON m.paper_id = pa.paper_id
        WHERE pa.role IN ('first', 'cofirst', 'corresponding')
          AND m.classification IN ('高度匹配', '可能匹配')
        ORDER BY pa.paper_id, pa.author_order
        """
    )
    queued: list[InvestigationQueueItem] = []
    now = utc_now()
    for row in rows:
        candidate_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                f"candidate:{row['author_id']}:{row['job_snapshot_id']}",
            )
        )
        database.execute(
            """
            INSERT OR IGNORE INTO candidates (
                id, author_id, job_snapshot_id, status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                candidate_id,
                row["author_id"],
                row["job_snapshot_id"],
                CandidateStatus.INVESTIGATE.value,
                now,
                now,
            ),
        )
        queued.append(
            InvestigationQueueItem(
                candidate_id=candidate_id,
                author_id=str(row["author_id"]),
                paper_id=str(row["paper_id"]),
                job_snapshot_id=str(row["job_snapshot_id"]),
                role=str(row["role"]),
            )
        )
    return queued


def _strong_identifiers(evidence: dict[str, Any]) -> set[str]:
    identifiers = set()
    for key in ("orcid", "openalex_id", "dblp_id", "email"):
        value = evidence.get(key)
        if value:
            identifiers.add(f"{key}:{str(value).strip().casefold()}")
    return identifiers


def reconcile_author(
    database: Database, evidence_records: list[dict[str, Any]]
) -> ReconcileResult:
    del database
    if not evidence_records:
        return ReconcileResult(
            CandidateStatus.HUMAN_REVIEW, False, "No evidence records"
        )
    strong_sets = [_strong_identifiers(item) for item in evidence_records]
    common = set.intersection(*strong_sets) if all(strong_sets) else set()
    institutions = {
        str(item.get("institution")).strip().casefold()
        for item in evidence_records
        if item.get("institution")
    }
    if common:
        return ReconcileResult(
            CandidateStatus.INVESTIGATE, True, "Shared strong identifier"
        )
    if len(evidence_records) > 1 and len(institutions) > 1:
        return ReconcileResult(
            CandidateStatus.HUMAN_REVIEW,
            False,
            "Same name has conflicting institutions and no shared strong identifier",
        )
    return ReconcileResult(
        CandidateStatus.HUMAN_REVIEW,
        False,
        "Insufficient strong identity evidence",
    )


def _validate_public_email(value: str | None) -> str | None:
    if value in (None, ""):
        return None
    _name, address = parseaddr(value)
    if (
        address != value.strip()
        or address.startswith("@")
        or address.count("@") != 1
        or "." not in address.rsplit("@", 1)[1]
    ):
        raise EvidenceError("email must be a complete public professional email")
    return address.casefold()


def _validate_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise EvidenceError("source_url must be an absolute HTTP(S) URL")
    return value


def record_author_evidence(
    database: Database,
    author_id: str,
    evidence: dict[str, Any],
) -> str:
    required = ("source_type", "source_url", "observed_at", "summary", "confidence")
    missing = [key for key in required if evidence.get(key) in (None, "")]
    if missing:
        raise EvidenceError(f"missing evidence fields: {', '.join(missing)}")
    source_url = _validate_url(str(evidence["source_url"]))
    email = _validate_public_email(evidence.get("email"))
    confidence = float(evidence["confidence"])
    if not 0 <= confidence <= 1:
        raise EvidenceError("confidence must be between 0 and 1")
    evidence_id = str(uuid.uuid4())
    now = utc_now()
    database.execute(
        """
        INSERT INTO author_evidence (
            id, author_id, source_type, source_url, observed_at, page_date,
            summary, institution, role, email, orcid, openalex_id, dblp_id,
            google_scholar_url, mainland_china, confidence, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            evidence_id,
            author_id,
            evidence["source_type"],
            source_url,
            evidence["observed_at"],
            evidence.get("page_date"),
            evidence["summary"],
            evidence.get("institution"),
            evidence.get("role"),
            email,
            evidence.get("orcid"),
            evidence.get("openalex_id"),
            evidence.get("dblp_id"),
            evidence.get("google_scholar_url"),
            (
                None
                if evidence.get("mainland_china") is None
                else int(bool(evidence["mainland_china"]))
            ),
            confidence,
            now,
        ),
    )
    updates = {
        "current_institution": evidence.get("institution"),
        "current_status": evidence.get("role"),
        "public_email": email,
        "orcid": evidence.get("orcid"),
        "openalex_id": evidence.get("openalex_id"),
        "dblp_id": evidence.get("dblp_id"),
        "homepage_url": evidence.get("homepage_url"),
        "mainland_china": (
            None
            if evidence.get("mainland_china") is None
            else int(bool(evidence["mainland_china"]))
        ),
        "confidence": confidence,
    }
    for column, value in updates.items():
        if value is not None:
            database.execute(
                f"UPDATE authors SET {column} = ?, updated_at = ? WHERE id = ?",
                (value, now, author_id),
            )
    return evidence_id


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Manage author investigation evidence.")
    parser.add_argument("command", choices=("queue", "add-evidence"))
    parser.add_argument("--author-id")
    parser.add_argument("--evidence-file")
    parser.add_argument(
        "--settings-config", default=str(root / "config" / "settings.yaml")
    )
    args = parser.parse_args()
    settings = load_settings(args.settings_config)
    database = Database(settings.database_path)
    database.initialize()
    if args.command == "queue":
        result = [item.__dict__ for item in queue_target_authors(database)]
    else:
        if not args.author_id or not args.evidence_file:
            parser.error("add-evidence requires --author-id and --evidence-file")
        evidence = json.loads(Path(args.evidence_file).read_text(encoding="utf-8"))
        result = {
            "evidence_id": record_author_evidence(database, args.author_id, evidence)
        }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
