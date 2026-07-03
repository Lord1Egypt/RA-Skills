from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

from config import load_settings
from db import Database, utc_now
from models import CandidateStatus


class InvalidTransition(RuntimeError):
    pass


@dataclass(frozen=True)
class ScreeningResult:
    status: CandidateStatus
    reason: str


@dataclass(frozen=True)
class RetentionReviewItem:
    candidate_id: str
    author_id: str
    status: str
    updated_at: str


ALLOWED_TRANSITIONS = {
    CandidateStatus.INVESTIGATE: {
        CandidateStatus.HUMAN_REVIEW,
        CandidateStatus.NOT_QUALIFIED,
        CandidateStatus.AWAITING_APPROVAL,
    },
    CandidateStatus.HUMAN_REVIEW: {
        CandidateStatus.INVESTIGATE,
        CandidateStatus.NOT_QUALIFIED,
        CandidateStatus.AWAITING_APPROVAL,
        CandidateStatus.CLOSED,
    },
    CandidateStatus.AWAITING_APPROVAL: {
        CandidateStatus.APPROVED,
        CandidateStatus.NOT_QUALIFIED,
        CandidateStatus.CLOSED,
    },
    CandidateStatus.APPROVED: {
        CandidateStatus.DRAFT_REVIEW,
        CandidateStatus.CLOSED,
    },
    CandidateStatus.DRAFT_REVIEW: {
        CandidateStatus.CONTACTED,
        CandidateStatus.CLOSED,
    },
    CandidateStatus.CONTACTED: {
        CandidateStatus.REPLIED,
        CandidateStatus.NOT_INTERESTED,
        CandidateStatus.UNSUBSCRIBED,
        CandidateStatus.CLOSED,
    },
    CandidateStatus.REPLIED: {
        CandidateStatus.ADVANCING,
        CandidateStatus.FOLLOW_UP_LATER,
        CandidateStatus.NOT_INTERESTED,
        CandidateStatus.UNSUBSCRIBED,
        CandidateStatus.HUMAN_REVIEW,
    },
    CandidateStatus.ADVANCING: {
        CandidateStatus.FOLLOW_UP_LATER,
        CandidateStatus.NOT_INTERESTED,
        CandidateStatus.CLOSED,
    },
    CandidateStatus.FOLLOW_UP_LATER: {
        CandidateStatus.ADVANCING,
        CandidateStatus.NOT_INTERESTED,
        CandidateStatus.UNSUBSCRIBED,
        CandidateStatus.CLOSED,
    },
    CandidateStatus.NOT_QUALIFIED: {CandidateStatus.CLOSED},
    CandidateStatus.NOT_INTERESTED: {CandidateStatus.CLOSED},
    CandidateStatus.CLOSED: set(),
    CandidateStatus.UNSUBSCRIBED: set(),
}


def screen_candidate(
    *,
    current_status: str | None,
    hard_allowed: list[str],
) -> ScreeningResult:
    if not current_status or current_status in {"无法确认", "其他"}:
        return ScreeningResult(
            CandidateStatus.HUMAN_REVIEW,
            "Education or current status evidence is insufficient",
        )
    if current_status not in hard_allowed:
        return ScreeningResult(
            CandidateStatus.NOT_QUALIFIED,
            f"{current_status} does not meet the hard education requirement",
        )
    return ScreeningResult(
        CandidateStatus.AWAITING_APPROVAL,
        f"{current_status} meets the hard education requirement",
    )


def transition_candidate(
    database: Database,
    candidate_id: str,
    new_status: CandidateStatus,
    *,
    reason: str | None = None,
) -> None:
    row = database.fetch_one(
        "SELECT status FROM candidates WHERE id = ?", (candidate_id,)
    )
    if row is None:
        raise KeyError(f"Candidate not found: {candidate_id}")
    current = CandidateStatus(row["status"])
    if new_status not in ALLOWED_TRANSITIONS[current]:
        raise InvalidTransition(f"Cannot transition {current.value} to {new_status.value}")
    if new_status == CandidateStatus.APPROVED:
        database.authorize_action("approve_candidate", "candidate", candidate_id)
    elif new_status == CandidateStatus.CLOSED:
        database.authorize_action("close_candidate", "candidate", candidate_id)
    now = utc_now()
    suppressed = int(new_status == CandidateStatus.UNSUBSCRIBED)
    database.execute(
        """
        UPDATE candidates
        SET status = ?,
            suppressed = CASE WHEN ? = 1 THEN 1 ELSE suppressed END,
            suppression_reason = CASE WHEN ? = 1 THEN ? ELSE suppression_reason END,
            updated_at = ?
        WHERE id = ?
        """,
        (
            new_status.value,
            suppressed,
            suppressed,
            reason or "Candidate unsubscribed",
            now,
            candidate_id,
        ),
    )
    database.execute(
        """
        INSERT INTO audit_logs (
            event_type, target_type, target_id, details_json, created_at
        ) VALUES ('candidate_transition', 'candidate', ?, ?, ?)
        """,
        (
            candidate_id,
            json.dumps(
                {
                    "from": current.value,
                    "to": new_status.value,
                    "reason": reason,
                },
                ensure_ascii=False,
            ),
            now,
        ),
    )


def list_retention_review(
    database: Database,
    *,
    as_of: date,
    retention_days: int,
) -> list[RetentionReviewItem]:
    cutoff = as_of - timedelta(days=retention_days)
    rows = database.fetch_all(
        """
        SELECT id, author_id, status, updated_at
        FROM candidates
        WHERE substr(updated_at, 1, 10) <= ?
        ORDER BY updated_at, id
        """,
        (cutoff.isoformat(),),
    )
    return [
        RetentionReviewItem(
            candidate_id=str(row["id"]),
            author_id=str(row["author_id"]),
            status=str(row["status"]),
            updated_at=str(row["updated_at"]),
        )
        for row in rows
    ]


def _cancel_candidate_mail(database: Database, candidate_id: str, reason: str) -> None:
    rows = database.fetch_all(
        """
        SELECT id, candidate_ids_json
        FROM mail_threads
        WHERE sent_at IS NULL
          AND delivery_status NOT LIKE 'cancelled%'
        """
    )
    for row in rows:
        candidate_ids = json.loads(row["candidate_ids_json"] or "[]")
        if candidate_id in candidate_ids:
            database.execute(
                """
                UPDATE mail_threads
                SET delivery_status = ?, last_synced_at = ?
                WHERE id = ?
                """,
                (reason, utc_now(), row["id"]),
            )


def stop_processing_candidate(database: Database, candidate_id: str) -> None:
    database.authorize_action("stop_processing", "candidate", candidate_id)
    row = database.fetch_one(
        "SELECT status FROM candidates WHERE id = ?", (candidate_id,)
    )
    if row is None:
        raise KeyError(f"Candidate not found: {candidate_id}")
    now = utc_now()
    status = (
        CandidateStatus.UNSUBSCRIBED.value
        if row["status"] == CandidateStatus.UNSUBSCRIBED.value
        else CandidateStatus.CLOSED.value
    )
    database.execute(
        """
        UPDATE candidates
        SET status = ?, suppressed = 1, suppression_reason = '停止处理',
            updated_at = ?
        WHERE id = ?
        """,
        (status, now, candidate_id),
    )
    database.execute(
        """
        UPDATE followups
        SET status = 'cancelled_stop_processing'
        WHERE candidate_id = ? AND sent_at IS NULL
        """,
        (candidate_id,),
    )
    _cancel_candidate_mail(database, candidate_id, "cancelled_stop_processing")
    database.execute(
        """
        INSERT INTO audit_logs (
            event_type, target_type, target_id, details_json, created_at
        ) VALUES ('candidate_stop_processing', 'candidate', ?, '{}', ?)
        """,
        (candidate_id, now),
    )


def delete_candidate_data(database: Database, candidate_id: str) -> None:
    database.authorize_action("delete_candidate_data", "candidate", candidate_id)
    row = database.fetch_one(
        "SELECT author_id FROM candidates WHERE id = ?", (candidate_id,)
    )
    if row is None:
        raise KeyError(f"Candidate not found: {candidate_id}")
    author_id = str(row["author_id"])
    now = utc_now()
    with database.connection() as connection:
        candidate_rows = connection.execute(
            "SELECT id FROM candidates WHERE author_id = ?", (author_id,)
        ).fetchall()
        candidate_ids = [str(item["id"]) for item in candidate_rows]
        mail_rows = connection.execute(
            "SELECT id FROM mail_threads WHERE author_id = ?", (author_id,)
        ).fetchall()
        mail_ids = [str(item["id"]) for item in mail_rows]

        connection.execute("DELETE FROM followups WHERE author_id = ?", (author_id,))
        connection.execute("DELETE FROM mail_threads WHERE author_id = ?", (author_id,))
        connection.execute("DELETE FROM author_evidence WHERE author_id = ?", (author_id,))
        for target_id in candidate_ids:
            connection.execute(
                "DELETE FROM approvals WHERE target_type = 'candidate' AND target_id = ?",
                (target_id,),
            )
            connection.execute(
                "DELETE FROM audit_logs WHERE target_type = 'candidate' AND target_id = ?",
                (target_id,),
            )
        for target_id in mail_ids:
            connection.execute(
                "DELETE FROM approvals WHERE target_type = 'mail_thread' AND target_id = ?",
                (target_id,),
            )
            connection.execute(
                "DELETE FROM audit_logs WHERE target_type = 'mail_thread' AND target_id = ?",
                (target_id,),
            )
        connection.execute(
            """
            UPDATE candidates
            SET status = '关闭', education_result = NULL, recommendation = NULL,
                suppressed = 1, suppression_reason = '资料已删除',
                updated_at = ?
            WHERE author_id = ?
            """,
            (now, author_id),
        )
        connection.execute(
            """
            UPDATE authors
            SET normalized_name = ?, display_name = '已删除候选人',
                orcid = NULL, openalex_id = NULL, dblp_id = NULL,
                current_institution = NULL, current_status = NULL,
                public_email = NULL, homepage_url = NULL, mainland_china = NULL,
                contact_suppressed = 1,
                contact_suppression_reason = '资料已删除',
                confidence = NULL, verification_status = '资料已删除',
                updated_at = ?
            WHERE id = ?
            """,
            (f"deleted:{author_id}", now, author_id),
        )
        connection.execute(
            "DELETE FROM audit_logs WHERE target_type = 'author' AND target_id = ?",
            (author_id,),
        )
        connection.execute(
            """
            INSERT INTO audit_logs (
                event_type, target_type, target_id, details_json, created_at
            ) VALUES ('candidate_data_deleted', 'author', ?, ?, ?)
            """,
            (
                author_id,
                json.dumps(
                    {"candidate_count": len(candidate_ids)},
                    ensure_ascii=True,
                    sort_keys=True,
                ),
                now,
            ),
        )


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Screen and transition candidates.")
    parser.add_argument(
        "command",
        choices=(
            "screen",
            "transition",
            "retention-review",
            "stop-processing",
            "delete-data",
        ),
    )
    parser.add_argument("--candidate-id")
    parser.add_argument("--current-status")
    parser.add_argument("--hard-allowed", nargs="*")
    parser.add_argument("--new-status")
    parser.add_argument("--reason")
    parser.add_argument("--as-of")
    parser.add_argument(
        "--settings-config", default=str(root / "config" / "settings.yaml")
    )
    args = parser.parse_args()
    settings = load_settings(args.settings_config)
    database = Database(settings.database_path)
    database.initialize()
    if args.command == "screen":
        result = screen_candidate(
            current_status=args.current_status,
            hard_allowed=args.hard_allowed or [],
        )
        print(json.dumps(result.__dict__, ensure_ascii=False, default=str))
        return 0
    if args.command == "retention-review":
        as_of = date.fromisoformat(args.as_of) if args.as_of else date.today()
        result = list_retention_review(
            database,
            as_of=as_of,
            retention_days=settings.retention_days,
        )
        print(
            json.dumps(
                [item.__dict__ for item in result],
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    if not args.candidate_id:
        parser.error(f"{args.command} requires --candidate-id")
    if args.command == "stop-processing":
        stop_processing_candidate(database, args.candidate_id)
        print(
            json.dumps(
                {"candidate_id": args.candidate_id, "status": "停止处理"},
                ensure_ascii=False,
            )
        )
        return 0
    if args.command == "delete-data":
        delete_candidate_data(database, args.candidate_id)
        print(
            json.dumps(
                {"candidate_id": args.candidate_id, "status": "资料已删除"},
                ensure_ascii=False,
            )
        )
        return 0
    if not args.new_status:
        parser.error("transition requires --new-status")
    transition_candidate(
        database,
        args.candidate_id,
        CandidateStatus(args.new_status),
        reason=args.reason,
    )
    print(json.dumps({"candidate_id": args.candidate_id, "status": args.new_status}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
