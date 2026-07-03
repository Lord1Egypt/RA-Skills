from __future__ import annotations

import argparse
import html
import json
import uuid
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

from config import load_settings
from db import ApprovalRequired, Database, utc_now


class OutreachBlocked(RuntimeError):
    pass


@dataclass(frozen=True)
class DraftPayload:
    mail_thread_id: str
    mailbox: str
    to: str
    subject: str
    html_body: str
    candidate_ids: tuple[str, ...]
    approval_action: str


def followup_dates(sent_at: datetime) -> list[date]:
    return [
        (sent_at + timedelta(days=7)).date(),
        (sent_at + timedelta(days=21)).date(),
    ]


def _candidate_rows(database: Database, candidate_id: str) -> list[Any]:
    return database.fetch_all(
        """
        SELECT c.id AS candidate_id, c.status, c.suppressed, c.suppression_reason,
               c.author_id, c.job_snapshot_id,
               a.display_name, a.public_email, a.mainland_china,
               a.contact_suppressed AS author_contact_suppressed,
               a.contact_suppression_reason AS author_contact_suppression_reason,
               js.config_json AS job_config_json,
               p.title AS paper_title, m.result_json AS match_result_json
        FROM candidates c
        JOIN authors a ON a.id = c.author_id
        JOIN job_snapshots js ON js.id = c.job_snapshot_id
        LEFT JOIN paper_job_matches m ON m.job_snapshot_id = c.job_snapshot_id
        LEFT JOIN paper_authors pa
          ON pa.paper_id = m.paper_id AND pa.author_id = c.author_id
        LEFT JOIN papers p ON p.id = m.paper_id
        WHERE c.id = ? AND (pa.author_id IS NOT NULL OR m.id IS NULL)
        ORDER BY CASE m.classification
                   WHEN '高度匹配' THEN 0
                   WHEN '可能匹配' THEN 1
                   ELSE 2
                 END,
                 p.publication_date DESC
        """,
        (candidate_id,),
    )


def _validate_candidate(row: Any) -> None:
    if row["author_contact_suppressed"]:
        raise OutreachBlocked(
            f"Candidate {row['candidate_id']} is globally suppressed: "
            f"{row['author_contact_suppression_reason'] or 'no contact'}"
        )
    if row["suppressed"] or row["status"] == "退订":
        raise OutreachBlocked(
            f"Candidate {row['candidate_id']} is suppressed: "
            f"{row['suppression_reason'] or 'no contact'}"
        )
    if row["status"] != "已批准":
        raise OutreachBlocked(
            f"Candidate {row['candidate_id']} is not in 已批准 status"
        )
    if row["mainland_china"] != 1:
        raise OutreachBlocked(
            f"Candidate {row['candidate_id']} lacks verified mainland-China affiliation"
        )
    email = str(row["public_email"] or "")
    if email.count("@") != 1 or "." not in email.rsplit("@", 1)[1]:
        raise OutreachBlocked(
            f"Candidate {row['candidate_id']} lacks a complete public professional email"
        )


def _render_initial(
    template_path: Path,
    *,
    candidate_name: str,
    paper_title: str,
    match_reason: str,
    job_titles: str,
    company_team_intro: str,
    sender_signature: str,
) -> str:
    template = template_path.read_text(encoding="utf-8")
    values = {
        "candidate_name": html.escape(candidate_name),
        "paper_title": html.escape(paper_title),
        "match_reason": html.escape(match_reason),
        "job_titles": html.escape(job_titles),
        "company_team_intro": html.escape(company_team_intro),
        "sender_signature": html.escape(sender_signature),
    }
    return template.format_map(values)


def _render_followup(
    template_path: Path,
    *,
    candidate_name: str,
    paper_title: str,
    job_titles: str,
    sender_signature: str,
) -> str:
    template = template_path.read_text(encoding="utf-8")
    values = {
        "candidate_name": html.escape(candidate_name),
        "paper_title": html.escape(paper_title),
        "job_titles": html.escape(job_titles),
        "sender_signature": html.escape(sender_signature),
    }
    return template.format_map(values)


def build_initial_drafts(
    database: Database,
    candidate_ids: list[str],
    company_profile: dict[str, str],
    *,
    template_path: Path | None = None,
) -> list[DraftPayload]:
    required_profile = ("mailbox", "company_team_intro", "sender_signature")
    missing = [key for key in required_profile if not company_profile.get(key)]
    if missing:
        raise OutreachBlocked(f"Missing approved outreach fields: {', '.join(missing)}")
    template_path = template_path or (
        Path(__file__).resolve().parents[1] / "templates" / "email" / "initial.html"
    )
    grouped: dict[tuple[str, str], list[Any]] = {}
    for candidate_id in candidate_ids:
        rows = _candidate_rows(database, candidate_id)
        if not rows:
            raise KeyError(f"Candidate not found or has no matched paper: {candidate_id}")
        row = rows[0]
        _validate_candidate(row)
        grouped.setdefault(
            (str(row["author_id"]), str(row["public_email"]).casefold()), []
        ).append(row)

    drafts: list[DraftPayload] = []
    for (author_id, email), rows in grouped.items():
        for row in rows:
            database.authorize_action(
                "prepare_outreach", "candidate", str(row["candidate_id"])
            )
        prior = database.fetch_one(
            """
            SELECT id FROM mail_threads
            WHERE author_id = ? AND message_type = 'initial'
            LIMIT 1
            """,
            (author_id,),
        )
        if prior:
            raise OutreachBlocked(
                f"An initial outreach record already exists for author {author_id}"
            )
        job_configs = [json.loads(row["job_config_json"]) for row in rows]
        job_titles = "、".join(config["title"] for config in job_configs)
        summaries = []
        paper_titles = []
        for row in rows:
            if row["paper_title"] and row["paper_title"] not in paper_titles:
                paper_titles.append(str(row["paper_title"]))
            result = json.loads(row["match_result_json"] or "{}")
            summary = result.get("summary")
            if summary and summary not in summaries:
                summaries.append(str(summary))
        candidate_name = str(rows[0]["display_name"])
        paper_title = "；".join(paper_titles) or "相关研究工作"
        match_reason = "；".join(summaries) or "研究方向与岗位需求存在关联"
        body = _render_initial(
            template_path,
            candidate_name=candidate_name,
            paper_title=paper_title,
            match_reason=match_reason,
            job_titles=job_titles,
            company_team_intro=company_profile["company_team_intro"],
            sender_signature=company_profile["sender_signature"],
        )
        mail_thread_id = str(uuid.uuid4())
        ids = tuple(str(row["candidate_id"]) for row in rows)
        subject = f"关于{job_titles}方向的交流邀请"
        database.execute(
            """
            INSERT INTO mail_threads (
                id, author_id, candidate_id, candidate_ids_json, job_snapshot_id,
                message_type, mailbox, recipient, subject, body_html,
                delivery_status, last_synced_at
            ) VALUES (?, ?, ?, ?, ?, 'initial', ?, ?, ?, ?, 'draft_payload', ?)
            """,
            (
                mail_thread_id,
                author_id,
                ids[0],
                json.dumps(ids, ensure_ascii=False),
                rows[0]["job_snapshot_id"],
                company_profile["mailbox"],
                email,
                subject,
                body,
                utc_now(),
            ),
        )
        for candidate_id in ids:
            database.execute(
                """
                UPDATE candidates
                SET status = '草稿待审', updated_at = ?
                WHERE id = ?
                """,
                (utc_now(), candidate_id),
            )
        drafts.append(
            DraftPayload(
                mail_thread_id=mail_thread_id,
                mailbox=company_profile["mailbox"],
                to=email,
                subject=subject,
                html_body=body,
                candidate_ids=ids,
                approval_action="send_initial",
            )
        )
    return drafts


def build_initial_draft(
    database: Database,
    candidate_id: str,
    company_profile: dict[str, str],
    *,
    template_path: Path | None = None,
) -> DraftPayload:
    return build_initial_drafts(
        database,
        [candidate_id],
        company_profile,
        template_path=template_path,
    )[0]


def build_due_followup_drafts(
    database: Database,
    *,
    as_of: date,
    company_profile: dict[str, str],
    template_dir: Path | None = None,
) -> list[DraftPayload]:
    required_profile = ("mailbox", "sender_signature")
    missing = [key for key in required_profile if not company_profile.get(key)]
    if missing:
        raise OutreachBlocked(f"Missing approved outreach fields: {', '.join(missing)}")
    template_dir = template_dir or (
        Path(__file__).resolve().parents[1] / "templates" / "email"
    )
    due_rows = database.fetch_all(
        """
        SELECT f.id AS followup_id, f.sequence, f.candidate_id,
               f.mail_thread_id AS initial_mail_thread_id,
               c.status, c.suppressed, c.suppression_reason,
               a.contact_suppressed AS author_contact_suppressed,
               a.contact_suppression_reason AS author_contact_suppression_reason,
               mt.author_id, mt.job_snapshot_id, mt.mailbox, mt.recipient,
               mt.subject, mt.thread_id
        FROM followups f
        JOIN candidates c ON c.id = f.candidate_id
        JOIN authors a ON a.id = f.author_id
        JOIN mail_threads mt ON mt.id = f.mail_thread_id
        WHERE f.status = 'pending'
          AND f.draft_id IS NULL
          AND f.due_date <= ?
        ORDER BY f.due_date, f.sequence, f.mail_thread_id
        """,
        (as_of.isoformat(),),
    )
    grouped: dict[tuple[str, int], list[Any]] = {}
    for row in due_rows:
        if row["author_contact_suppressed"] or row["suppressed"]:
            continue
        if row["status"] in {"退订", "无意向", "已回复"}:
            continue
        grouped.setdefault(
            (str(row["initial_mail_thread_id"]), int(row["sequence"])), []
        ).append(row)

    drafts: list[DraftPayload] = []
    for (_initial_id, sequence), rows in grouped.items():
        candidate_rows = []
        for row in rows:
            matches = _candidate_rows(database, str(row["candidate_id"]))
            if matches:
                candidate_rows.append(matches[0])
        if not candidate_rows:
            continue
        job_configs = [json.loads(row["job_config_json"]) for row in candidate_rows]
        job_titles = "、".join(
            dict.fromkeys(str(config["title"]) for config in job_configs)
        )
        paper_titles = [
            str(row["paper_title"])
            for row in candidate_rows
            if row["paper_title"]
        ]
        paper_title = "；".join(dict.fromkeys(paper_titles)) or "相关研究工作"
        template_path = template_dir / f"followup-{sequence}.html"
        if not template_path.exists():
            raise OutreachBlocked(f"Missing follow-up template: {template_path}")
        first = rows[0]
        body = _render_followup(
            template_path,
            candidate_name=str(candidate_rows[0]["display_name"]),
            paper_title=paper_title,
            job_titles=job_titles,
            sender_signature=company_profile["sender_signature"],
        )
        mail_thread_id = str(uuid.uuid4())
        candidate_ids = tuple(str(row["candidate_id"]) for row in rows)
        subject = f"Re: {first['subject']}"
        database.execute(
            """
            INSERT INTO mail_threads (
                id, author_id, candidate_id, candidate_ids_json, job_snapshot_id,
                message_type, mailbox, recipient, subject, body_html, thread_id,
                delivery_status, last_synced_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'draft_payload', ?)
            """,
            (
                mail_thread_id,
                first["author_id"],
                candidate_ids[0],
                json.dumps(candidate_ids, ensure_ascii=False),
                first["job_snapshot_id"],
                f"followup-{sequence}",
                company_profile["mailbox"],
                first["recipient"],
                subject,
                body,
                first["thread_id"],
                utc_now(),
            ),
        )
        for row in rows:
            database.execute(
                """
                UPDATE followups
                SET status = 'draft_pending', draft_id = ?
                WHERE id = ? AND status = 'pending' AND draft_id IS NULL
                """,
                (mail_thread_id, row["followup_id"]),
            )
        drafts.append(
            DraftPayload(
                mail_thread_id=mail_thread_id,
                mailbox=company_profile["mailbox"],
                to=str(first["recipient"]),
                subject=subject,
                html_body=body,
                candidate_ids=candidate_ids,
                approval_action=f"send_followup-{sequence}",
            )
        )
    return drafts


def record_lark_draft(
    database: Database,
    mail_thread_id: str,
    draft_id: str,
) -> None:
    row = database.fetch_one(
        "SELECT sent_at FROM mail_threads WHERE id = ?",
        (mail_thread_id,),
    )
    if row is None:
        raise KeyError(f"Mail thread not found: {mail_thread_id}")
    if row["sent_at"]:
        raise OutreachBlocked(f"Mail thread {mail_thread_id} was already sent")
    database.execute(
        """
        UPDATE mail_threads
        SET draft_id = ?, delivery_status = 'lark_draft_created',
            last_synced_at = ?
        WHERE id = ?
        """,
        (draft_id, utc_now(), mail_thread_id),
    )


def authorize_mail_send(database: Database, mail_thread_id: str) -> dict[str, Any]:
    row = database.fetch_one(
        """
        SELECT id, message_type, mailbox, recipient, subject, body_html, draft_id,
               candidate_ids_json, sent_at
        FROM mail_threads WHERE id = ?
        """,
        (mail_thread_id,),
    )
    if row is None:
        raise KeyError(f"Mail thread not found: {mail_thread_id}")
    if row["sent_at"]:
        raise OutreachBlocked(f"Mail thread {mail_thread_id} was already sent")
    candidate_ids = json.loads(row["candidate_ids_json"])
    for candidate_id in candidate_ids:
        candidate = database.fetch_one(
            """
            SELECT c.suppressed, c.status, a.contact_suppressed
            FROM candidates c
            JOIN authors a ON a.id = c.author_id
            WHERE c.id = ?
            """,
            (candidate_id,),
        )
        if (
            candidate is None
            or candidate["suppressed"]
            or candidate["contact_suppressed"]
            or candidate["status"] in {"退订", "无意向"}
        ):
            raise OutreachBlocked(f"Candidate {candidate_id} is suppressed")
    action = f"send_{row['message_type']}"
    approval_id = database.authorize_action(action, "mail_thread", mail_thread_id)
    database.execute(
        """
        UPDATE mail_threads
        SET delivery_status = 'send_authorized', last_synced_at = ?
        WHERE id = ?
        """,
        (utc_now(), mail_thread_id),
    )
    return {
        "approval_id": approval_id,
        "mail_thread_id": mail_thread_id,
        "mailbox": row["mailbox"],
        "to": row["recipient"],
        "subject": row["subject"],
        "html_body": row["body_html"],
        "draft_id": row["draft_id"],
        "candidate_ids": candidate_ids,
    }


def record_sent_mail(
    database: Database,
    mail_thread_id: str,
    *,
    message_id: str,
    thread_id: str,
    sent_at: datetime,
    delivery_status: str,
) -> None:
    row = database.fetch_one(
        """
        SELECT author_id, candidate_ids_json, message_type, delivery_status
        FROM mail_threads WHERE id = ?
        """,
        (mail_thread_id,),
    )
    if row is None:
        raise KeyError(f"Mail thread not found: {mail_thread_id}")
    if row["delivery_status"] != "send_authorized":
        raise OutreachBlocked(f"Mail thread {mail_thread_id} is not authorized to send")
    database.execute(
        """
        UPDATE mail_threads
        SET message_id = ?, thread_id = ?, sent_at = ?, delivery_status = ?,
            last_synced_at = ?
        WHERE id = ?
        """,
        (
            message_id,
            thread_id,
            sent_at.isoformat(),
            delivery_status,
            utc_now(),
            mail_thread_id,
        ),
    )
    for candidate_id in json.loads(row["candidate_ids_json"]):
        database.execute(
            "UPDATE candidates SET status = '已联系', updated_at = ? WHERE id = ?",
            (utc_now(), candidate_id),
        )
        if row["message_type"] == "initial":
            for sequence, due_date in enumerate(followup_dates(sent_at), start=1):
                database.execute(
                    """
                    INSERT OR IGNORE INTO followups (
                        id, author_id, candidate_id, mail_thread_id, sequence,
                        due_date, status
                    ) VALUES (?, ?, ?, ?, ?, ?, 'pending')
                    """,
                    (
                        str(uuid.uuid4()),
                        row["author_id"],
                        candidate_id,
                        mail_thread_id,
                        sequence,
                        due_date.isoformat(),
                    ),
                )
        else:
            database.execute(
                """
                UPDATE followups
                SET status = 'sent', approved_at = COALESCE(approved_at, ?),
                    sent_at = ?
                WHERE draft_id = ? AND candidate_id = ?
                """,
                (
                    sent_at.isoformat(),
                    sent_at.isoformat(),
                    mail_thread_id,
                    candidate_id,
                ),
            )


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Prepare approval-gated outreach.")
    parser.add_argument(
        "command",
        choices=(
            "initial",
            "due-followups",
            "record-draft",
            "authorize-send",
            "record-sent",
        ),
    )
    parser.add_argument("--candidate-id", action="append")
    parser.add_argument("--mail-thread-id")
    parser.add_argument("--company-profile")
    parser.add_argument("--as-of")
    parser.add_argument("--draft-id")
    parser.add_argument("--message-id")
    parser.add_argument("--thread-id")
    parser.add_argument("--sent-at")
    parser.add_argument("--delivery-status", default="sent")
    parser.add_argument(
        "--settings-config", default=str(root / "config" / "settings.yaml")
    )
    args = parser.parse_args()
    settings = load_settings(args.settings_config)
    database = Database(settings.database_path)
    database.initialize()
    profile = (
        json.loads(Path(args.company_profile).read_text(encoding="utf-8"))
        if args.company_profile
        else settings.outreach_profile
    )
    if args.command == "record-draft":
        if not args.mail_thread_id or not args.draft_id:
            parser.error("record-draft requires --mail-thread-id and --draft-id")
        record_lark_draft(database, args.mail_thread_id, args.draft_id)
        result = {
            "mail_thread_id": args.mail_thread_id,
            "draft_id": args.draft_id,
            "status": "lark_draft_created",
        }
    elif args.command == "authorize-send":
        if not args.mail_thread_id:
            parser.error("authorize-send requires --mail-thread-id")
        result = authorize_mail_send(database, args.mail_thread_id)
    elif args.command == "record-sent":
        required = {
            "--mail-thread-id": args.mail_thread_id,
            "--message-id": args.message_id,
            "--thread-id": args.thread_id,
            "--sent-at": args.sent_at,
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            parser.error(f"record-sent requires {', '.join(missing)}")
        record_sent_mail(
            database,
            args.mail_thread_id,
            message_id=args.message_id,
            thread_id=args.thread_id,
            sent_at=datetime.fromisoformat(args.sent_at),
            delivery_status=args.delivery_status,
        )
        result = {
            "mail_thread_id": args.mail_thread_id,
            "message_id": args.message_id,
            "thread_id": args.thread_id,
            "status": args.delivery_status,
        }
    elif args.command == "initial":
        if not args.candidate_id:
            parser.error("initial requires --candidate-id")
        result = [
            draft.__dict__
            for draft in build_initial_drafts(database, args.candidate_id, profile)
        ]
    else:
        if not args.as_of:
            parser.error("due-followups requires --as-of")
        result = [
            draft.__dict__
            for draft in build_due_followup_drafts(
                database,
                as_of=date.fromisoformat(args.as_of),
                company_profile=profile,
            )
        ]
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
