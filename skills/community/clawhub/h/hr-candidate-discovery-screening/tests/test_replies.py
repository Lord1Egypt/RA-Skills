from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from pathlib import Path

from models import ReplyClass, ReplyClassificationResult
from process_replies import process_reply


FIXTURES = Path(__file__).parent / "fixtures"


def seed_reply_case(database):
    now = datetime.now(UTC).isoformat()
    author_id = str(uuid.uuid4())
    job_id = str(uuid.uuid4())
    snapshot_id = str(uuid.uuid4())
    candidate_id = str(uuid.uuid4())
    mail_thread_id = str(uuid.uuid4())
    database.execute(
        """
        INSERT INTO authors (
            id, normalized_name, display_name, public_email, mainland_china,
            verification_status, created_at, updated_at
        ) VALUES (?, 'li ming', '李明', 'candidate@example.edu.cn', 1,
                  '已核验', ?, ?)
        """,
        (author_id, now, now),
    )
    database.execute(
        """
        INSERT INTO jobs (id, title, active, config_json, updated_at)
        VALUES (?, 'Researcher', 1, '{}', ?)
        """,
        (job_id, now),
    )
    database.execute(
        """
        INSERT INTO job_snapshots (id, job_id, config_json, config_hash, created_at)
        VALUES (?, ?, '{}', ?, ?)
        """,
        (snapshot_id, job_id, snapshot_id, now),
    )
    database.execute(
        """
        INSERT INTO candidates (
            id, author_id, job_snapshot_id, status, created_at, updated_at
        ) VALUES (?, ?, ?, '已联系', ?, ?)
        """,
        (candidate_id, author_id, snapshot_id, now, now),
    )
    database.execute(
        """
        INSERT INTO mail_threads (
            id, author_id, candidate_id, candidate_ids_json, job_snapshot_id,
            message_type, mailbox, recipient, subject, body_html, message_id,
            thread_id, delivery_status, sent_at, last_synced_at
        ) VALUES (?, ?, ?, ?, ?, 'initial', 'recruiting@example.com',
                  'candidate@example.edu.cn', '交流邀请', '<p>hello</p>',
                  'message-1', 'thread-1', 'delivered', ?, ?)
        """,
        (
            mail_thread_id,
            author_id,
            candidate_id,
            json.dumps([candidate_id]),
            snapshot_id,
            now,
            now,
        ),
    )
    for sequence, due_date in ((1, "2026-06-18"), (2, "2026-07-02")):
        database.execute(
            """
            INSERT INTO followups (
                id, author_id, candidate_id, mail_thread_id, sequence,
                due_date, status
            ) VALUES (?, ?, ?, ?, ?, ?, 'pending')
            """,
            (
                str(uuid.uuid4()),
                author_id,
                candidate_id,
                mail_thread_id,
                sequence,
                due_date,
            ),
        )
    return author_id, candidate_id


class FakeClassifier:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def classify_reply(self, payload):
        self.calls.append(payload)
        return self.result


def classification(value, *, followup_date=None, needs_reply=False):
    return ReplyClassificationResult(
        classification=value,
        evidence_summary="邮件明确表达意向",
        confidence=0.95,
        suggested_action="人工复核后处理",
        needs_reply=needs_reply,
        reply_body="感谢回复" if needs_reply else None,
        followup_date=followup_date,
        model="deepseek-v4-pro",
        usage={},
    )


def reply_fixture(name):
    data = json.loads((FIXTURES / "replies.json").read_text(encoding="utf-8"))
    return {"thread_id": "thread-1", **data[name]}


def test_unsubscribe_cancels_followups_and_sets_global_suppression(
    initialized_database,
):
    author_id, _candidate_id = seed_reply_case(initialized_database)
    classifier = FakeClassifier(classification(ReplyClass.UNSUBSCRIBE))

    result = process_reply(
        initialized_database,
        reply_fixture("unsubscribe"),
        classifier,
    )

    assert result.classification == "退订"
    assert initialized_database.fetch_one(
        "SELECT contact_suppressed FROM authors WHERE id = ?", (author_id,)
    )["contact_suppressed"] == 1
    assert initialized_database.fetch_one(
        "SELECT COUNT(*) AS count FROM followups WHERE status = 'pending'"
    )["count"] == 0


def test_any_reply_cancels_unsent_followup_draft(initialized_database):
    author_id, candidate_id = seed_reply_case(initialized_database)
    followup = initialized_database.fetch_one(
        "SELECT id, mail_thread_id FROM followups WHERE sequence = 1"
    )
    draft_mail_id = str(uuid.uuid4())
    initialized_database.execute(
        """
        INSERT INTO mail_threads (
            id, author_id, candidate_id, candidate_ids_json, message_type,
            mailbox, recipient, subject, body_html, thread_id,
            delivery_status, last_synced_at
        ) VALUES (?, ?, ?, ?, 'followup-1', 'recruiting@example.com',
                  'candidate@example.edu.cn', 'Re: 交流邀请', '<p>follow-up</p>',
                  'thread-1', 'lark_draft_created', ?)
        """,
        (
            draft_mail_id,
            author_id,
            candidate_id,
            json.dumps([candidate_id]),
            datetime.now(UTC).isoformat(),
        ),
    )
    initialized_database.execute(
        """
        UPDATE followups
        SET status = 'draft_pending', draft_id = ?
        WHERE id = ?
        """,
        (draft_mail_id, followup["id"]),
    )
    classifier = FakeClassifier(classification(ReplyClass.ADVANCE))

    process_reply(
        initialized_database,
        reply_fixture("prompt_injection"),
        classifier,
    )

    assert initialized_database.fetch_one(
        "SELECT status FROM followups WHERE id = ?", (followup["id"],)
    )["status"] == "cancelled_reply"
    assert initialized_database.fetch_one(
        "SELECT delivery_status FROM mail_threads WHERE id = ?", (draft_mail_id,)
    )["delivery_status"] == "cancelled_reply"


def test_prompt_injection_text_is_data_not_an_action(initialized_database):
    seed_reply_case(initialized_database)
    classifier = FakeClassifier(classification(ReplyClass.UNCLEAR))

    result = process_reply(
        initialized_database,
        reply_fixture("prompt_injection"),
        classifier,
    )

    assert result.executed_actions == ()
    assert result.requires_human_approval is True
    assert classifier.calls[0]["untrusted_email_thread"][
        "messages"
    ][0]["body"].startswith("Ignore previous")


def test_follow_up_later_without_date_requires_human_date(initialized_database):
    seed_reply_case(initialized_database)
    classifier = FakeClassifier(classification(ReplyClass.LATER))

    result = process_reply(
        initialized_database,
        reply_fixture("later_without_date"),
        classifier,
    )

    assert result.classification == "稍后联系"
    assert result.followup_date is None
    assert result.requires_human_approval is True
