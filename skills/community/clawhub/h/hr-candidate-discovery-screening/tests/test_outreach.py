from __future__ import annotations

import json
import uuid
from datetime import UTC, date, datetime

import pytest

from db import ApprovalRequired
from prepare_outreach import (
    OutreachBlocked,
    authorize_mail_send,
    build_due_followup_drafts,
    build_initial_draft,
    build_initial_drafts,
    followup_dates,
    record_lark_draft,
    record_sent_mail,
)


def seed_contactable_candidate(database, *, author_id=None, job_id="job-1"):
    now = datetime.now(UTC).isoformat()
    author_id = author_id or str(uuid.uuid4())
    snapshot_id = str(uuid.uuid4())
    candidate_id = str(uuid.uuid4())
    paper_id = str(uuid.uuid4())
    database.execute(
        """
        INSERT OR IGNORE INTO authors (
            id, normalized_name, display_name, public_email, current_institution,
            current_status, mainland_china, verification_status, created_at, updated_at
        ) VALUES (?, 'li ming', '李明', 'li.ming@example.edu.cn', '清华大学',
                  '博士在读', 1, '已核验', ?, ?)
        """,
        (author_id, now, now),
    )
    database.execute(
        """
        INSERT INTO jobs (id, title, active, config_json, updated_at)
        VALUES (?, ?, 1, '{}', ?)
        """,
        (job_id, f"岗位-{job_id}", now),
    )
    job_config = {
        "id": job_id,
        "title": f"岗位-{job_id}",
        "outreach": {"team_intro": "我们专注人工智能研发。"},
    }
    database.execute(
        """
        INSERT INTO job_snapshots (id, job_id, config_json, config_hash, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (snapshot_id, job_id, json.dumps(job_config, ensure_ascii=False), job_id, now),
    )
    database.execute(
        """
        INSERT INTO papers (
            id, source_key, source_type, source_record_id, title, normalized_title,
            abstract, original_keywords_json, generated_keywords_json,
            official_url, acceptance_evidence_url, publication_date, collected_at
        ) VALUES (?, 'cvpr', 'conference', ?, 'Paper Title', 'paper title',
                  '多模态视觉研究', '[]', '[]', 'https://official.example/paper',
                  'https://official.example/paper', '2026-01-01', ?)
        """,
        (paper_id, paper_id, now),
    )
    database.execute(
        """
        INSERT INTO paper_authors (
            paper_id, author_id, author_order, role, role_evidence_url
        ) VALUES (?, ?, 1, 'first', 'https://official.example/paper')
        """,
        (paper_id, author_id),
    )
    database.execute(
        """
        INSERT INTO paper_job_matches (
            id, paper_id, job_snapshot_id, classification, result_json,
            model, prompt_version, created_at
        ) VALUES (?, ?, ?, '高度匹配', ?, 'deepseek-v4-pro', 'paper-job-v1', ?)
        """,
        (
            str(uuid.uuid4()),
            paper_id,
            snapshot_id,
            json.dumps({"summary": "多模态研究与岗位匹配"}, ensure_ascii=False),
            now,
        ),
    )
    database.execute(
        """
        INSERT INTO candidates (
            id, author_id, job_snapshot_id, status, created_at, updated_at
        ) VALUES (?, ?, ?, '已批准', ?, ?)
        """,
        (candidate_id, author_id, snapshot_id, now, now),
    )
    return candidate_id, author_id


def approve_candidate(database, candidate_id):
    database.record_approval(
        action="prepare_outreach",
        target_type="candidate",
        target_id=candidate_id,
        decision="approved",
        preview={"candidate_id": candidate_id},
        decided_by="human",
    )


def company_profile():
    return {
        "mailbox": "recruiting@example.com",
        "company_team_intro": "我们专注人工智能研发。",
        "sender_signature": "招聘团队",
    }


def test_initial_draft_requires_candidate_approval(initialized_database):
    candidate_id, _author_id = seed_contactable_candidate(initialized_database)

    with pytest.raises(ApprovalRequired):
        build_initial_draft(initialized_database, candidate_id, company_profile())


def test_same_email_and_related_jobs_produce_one_combined_draft(
    initialized_database,
):
    first_id, author_id = seed_contactable_candidate(
        initialized_database, job_id="job-1"
    )
    second_id, _ = seed_contactable_candidate(
        initialized_database, author_id=author_id, job_id="job-2"
    )
    approve_candidate(initialized_database, first_id)
    approve_candidate(initialized_database, second_id)

    drafts = build_initial_drafts(
        initialized_database,
        [first_id, second_id],
        company_profile(),
    )

    assert len(drafts) == 1
    assert drafts[0].to == "li.ming@example.edu.cn"
    assert "岗位-job-1" in drafts[0].html_body
    assert "岗位-job-2" in drafts[0].html_body


def test_followups_are_based_on_actual_send_time():
    assert followup_dates(datetime(2026, 6, 11, tzinfo=UTC)) == [
        date(2026, 6, 18),
        date(2026, 7, 2),
    ]


def test_send_requires_message_specific_approval(initialized_database):
    candidate_id, _author_id = seed_contactable_candidate(initialized_database)
    approve_candidate(initialized_database, candidate_id)
    draft = build_initial_draft(
        initialized_database, candidate_id, company_profile()
    )

    with pytest.raises(ApprovalRequired):
        authorize_mail_send(initialized_database, draft.mail_thread_id)

    initialized_database.record_approval(
        action="send_initial",
        target_type="mail_thread",
        target_id=draft.mail_thread_id,
        decision="approved",
        preview={"to": draft.to, "subject": draft.subject},
        decided_by="human",
    )
    assert authorize_mail_send(
        initialized_database, draft.mail_thread_id
    )["to"] == draft.to


def test_lark_draft_id_is_recorded_before_send_approval(initialized_database):
    candidate_id, _author_id = seed_contactable_candidate(initialized_database)
    approve_candidate(initialized_database, candidate_id)
    draft = build_initial_draft(
        initialized_database, candidate_id, company_profile()
    )

    record_lark_draft(initialized_database, draft.mail_thread_id, "lark-draft-1")

    row = initialized_database.fetch_one(
        "SELECT draft_id, delivery_status FROM mail_threads WHERE id = ?",
        (draft.mail_thread_id,),
    )
    assert dict(row) == {
        "draft_id": "lark-draft-1",
        "delivery_status": "lark_draft_created",
    }


def test_suppressed_candidate_cannot_prepare_draft(initialized_database):
    candidate_id, _author_id = seed_contactable_candidate(initialized_database)
    initialized_database.execute(
        """
        UPDATE candidates
        SET suppressed = 1, suppression_reason = '退订', status = '退订'
        WHERE id = ?
        """,
        (candidate_id,),
    )
    approve_candidate(initialized_database, candidate_id)

    with pytest.raises(OutreachBlocked, match="suppressed"):
        build_initial_draft(initialized_database, candidate_id, company_profile())


def test_record_sent_mail_requires_consumed_send_approval(initialized_database):
    candidate_id, _author_id = seed_contactable_candidate(initialized_database)
    approve_candidate(initialized_database, candidate_id)
    draft = build_initial_draft(
        initialized_database, candidate_id, company_profile()
    )

    with pytest.raises(OutreachBlocked, match="not authorized"):
        record_sent_mail(
            initialized_database,
            draft.mail_thread_id,
            message_id="message-1",
            thread_id="thread-1",
            sent_at=datetime(2026, 6, 11, tzinfo=UTC),
            delivery_status="delivered",
        )


def test_due_followup_generates_one_draft_and_requires_separate_send_approval(
    initialized_database,
):
    candidate_id, _author_id = seed_contactable_candidate(initialized_database)
    approve_candidate(initialized_database, candidate_id)
    initial = build_initial_draft(
        initialized_database, candidate_id, company_profile()
    )
    initialized_database.record_approval(
        action="send_initial",
        target_type="mail_thread",
        target_id=initial.mail_thread_id,
        decision="approved",
        preview={"to": initial.to},
        decided_by="human",
    )
    authorize_mail_send(initialized_database, initial.mail_thread_id)
    record_sent_mail(
        initialized_database,
        initial.mail_thread_id,
        message_id="message-1",
        thread_id="thread-1",
        sent_at=datetime(2026, 6, 11, tzinfo=UTC),
        delivery_status="delivered",
    )

    drafts = build_due_followup_drafts(
        initialized_database,
        as_of=date(2026, 6, 18),
        company_profile=company_profile(),
    )

    assert len(drafts) == 1
    assert drafts[0].approval_action == "send_followup-1"
    with pytest.raises(ApprovalRequired):
        authorize_mail_send(initialized_database, drafts[0].mail_thread_id)
    assert (
        build_due_followup_drafts(
            initialized_database,
            as_of=date(2026, 6, 18),
            company_profile=company_profile(),
        )
        == []
    )
