from __future__ import annotations

import json
import uuid
from datetime import UTC, date, datetime

import pytest

from db import ApprovalRequired
from investigate_authors import (
    EvidenceError,
    queue_target_authors,
    reconcile_author,
    record_author_evidence,
)
from manage_candidates import (
    InvalidTransition,
    delete_candidate_data,
    list_retention_review,
    screen_candidate,
    stop_processing_candidate,
    transition_candidate,
)
from models import CandidateStatus


def seed_authorships(database, roles):
    now = datetime.now(UTC).isoformat()
    paper_id = str(uuid.uuid4())
    job_id = "job-1"
    snapshot_id = str(uuid.uuid4())
    database.execute(
        """
        INSERT INTO papers (
            id, source_key, source_type, source_record_id, title, normalized_title,
            original_keywords_json, generated_keywords_json, publication_date, collected_at
        ) VALUES (?, 'cvpr', 'conference', ?, 'Paper', 'paper', '[]', '[]',
                  '2026-01-01', ?)
        """,
        (paper_id, paper_id, now),
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
        VALUES (?, ?, '{}', 'hash', ?)
        """,
        (snapshot_id, job_id, now),
    )
    database.execute(
        """
        INSERT INTO paper_job_matches (
            id, paper_id, job_snapshot_id, classification, result_json,
            model, prompt_version, created_at
        ) VALUES (?, ?, ?, '高度匹配', '{}', 'deepseek-v4-pro', 'paper-job-v1', ?)
        """,
        (str(uuid.uuid4()), paper_id, snapshot_id, now),
    )
    for order, role in enumerate(roles, start=1):
        author_id = str(uuid.uuid4())
        database.execute(
            """
            INSERT INTO authors (
                id, normalized_name, display_name, verification_status,
                created_at, updated_at
            ) VALUES (?, ?, ?, '待调查', ?, ?)
            """,
            (author_id, f"author {order}", f"Author {order}", now, now),
        )
        database.execute(
            """
            INSERT INTO paper_authors (
                paper_id, author_id, author_order, role, role_evidence_url
            ) VALUES (?, ?, ?, ?, 'https://official.example/paper')
            """,
            (paper_id, author_id, order, role),
        )
    return snapshot_id


def test_only_target_author_roles_enter_investigation(initialized_database):
    seed_authorships(
        initialized_database, ["first", "middle", "cofirst", "corresponding"]
    )

    queued = queue_target_authors(initialized_database)

    assert {item.role for item in queued} == {"first", "cofirst", "corresponding"}
    assert initialized_database.fetch_one(
        "SELECT COUNT(*) AS count FROM candidates"
    )["count"] == 3


def test_same_name_without_strong_identifier_requires_human_review(
    initialized_database,
):
    result = reconcile_author(
        initialized_database,
        [
            {
                "name": "Li Ming",
                "institution": "Tsinghua University",
                "source_url": "https://example.edu/li",
            },
            {
                "name": "Li Ming",
                "institution": "Peking University",
                "source_url": "https://example.edu.cn/li",
            },
        ],
    )

    assert result.status == CandidateStatus.HUMAN_REVIEW
    assert result.merged is False


def test_evidence_rejects_incomplete_or_inferred_email(initialized_database):
    now = datetime.now(UTC).isoformat()
    author_id = str(uuid.uuid4())
    initialized_database.execute(
        """
        INSERT INTO authors (
            id, normalized_name, display_name, verification_status,
            created_at, updated_at
        ) VALUES (?, 'li ming', 'Li Ming', '待调查', ?, ?)
        """,
        (author_id, now, now),
    )

    with pytest.raises(EvidenceError, match="complete public professional email"):
        record_author_evidence(
            initialized_database,
            author_id,
            {
                "source_type": "google_scholar",
                "source_url": "https://scholar.google.com/profile",
                "observed_at": now,
                "summary": "Verified email at tsinghua.edu.cn",
                "email": "@tsinghua.edu.cn",
                "confidence": 0.8,
            },
        )


def test_explicit_hard_requirement_failure_is_not_qualified():
    result = screen_candidate(
        current_status="本科在读",
        hard_allowed=["博士在读", "博士后"],
    )

    assert result.status == CandidateStatus.NOT_QUALIFIED


def test_unknown_education_routes_to_human_review():
    result = screen_candidate(
        current_status="无法确认",
        hard_allowed=["博士在读"],
    )

    assert result.status == CandidateStatus.HUMAN_REVIEW


def test_unsubscribed_state_cannot_transition_back_to_contacted(
    initialized_database,
):
    snapshot_id = seed_authorships(initialized_database, ["first"])
    queued = queue_target_authors(initialized_database)
    candidate_id = queued[0].candidate_id
    initialized_database.execute(
        "UPDATE candidates SET status = '退订', suppressed = 1 WHERE id = ?",
        (candidate_id,),
    )

    with pytest.raises(InvalidTransition):
        transition_candidate(
            initialized_database,
            candidate_id,
            CandidateStatus.CONTACTED,
        )

    row = initialized_database.fetch_one(
        "SELECT status, suppressed FROM candidates WHERE id = ?", (candidate_id,)
    )
    assert dict(row) == {"status": "退订", "suppressed": 1}


def test_retention_review_lists_due_candidates_without_mutating_them(
    initialized_database,
):
    seed_authorships(initialized_database, ["first"])
    candidate = queue_target_authors(initialized_database)[0]
    initialized_database.execute(
        "UPDATE candidates SET updated_at = '2025-12-01T00:00:00+00:00' WHERE id = ?",
        (candidate.candidate_id,),
    )

    due = list_retention_review(
        initialized_database,
        as_of=date(2026, 6, 11),
        retention_days=180,
    )

    assert [item.candidate_id for item in due] == [candidate.candidate_id]
    assert initialized_database.fetch_one(
        "SELECT status FROM candidates WHERE id = ?", (candidate.candidate_id,)
    )["status"] == CandidateStatus.INVESTIGATE.value


def test_stop_processing_requires_exact_approval(initialized_database):
    seed_authorships(initialized_database, ["first"])
    candidate = queue_target_authors(initialized_database)[0]

    with pytest.raises(ApprovalRequired):
        stop_processing_candidate(initialized_database, candidate.candidate_id)

    initialized_database.record_approval(
        action="stop_processing",
        target_type="candidate",
        target_id=candidate.candidate_id,
        decision="approved",
        preview={"candidate_id": candidate.candidate_id},
        decided_by="human",
    )
    stop_processing_candidate(initialized_database, candidate.candidate_id)

    row = initialized_database.fetch_one(
        "SELECT status, suppressed FROM candidates WHERE id = ?",
        (candidate.candidate_id,),
    )
    assert dict(row) == {"status": CandidateStatus.CLOSED.value, "suppressed": 1}


def test_candidate_cannot_enter_approved_state_without_human_approval(
    initialized_database,
):
    seed_authorships(initialized_database, ["first"])
    candidate = queue_target_authors(initialized_database)[0]
    initialized_database.execute(
        "UPDATE candidates SET status = '待候选确认' WHERE id = ?",
        (candidate.candidate_id,),
    )

    with pytest.raises(ApprovalRequired):
        transition_candidate(
            initialized_database,
            candidate.candidate_id,
            CandidateStatus.APPROVED,
        )

    initialized_database.record_approval(
        action="approve_candidate",
        target_type="candidate",
        target_id=candidate.candidate_id,
        decision="approved",
        preview={"candidate_id": candidate.candidate_id},
        decided_by="human",
    )
    transition_candidate(
        initialized_database,
        candidate.candidate_id,
        CandidateStatus.APPROVED,
    )

    assert initialized_database.fetch_one(
        "SELECT status FROM candidates WHERE id = ?", (candidate.candidate_id,)
    )["status"] == CandidateStatus.APPROVED.value


def test_delete_candidate_data_keeps_only_suppressed_anonymous_tombstone(
    initialized_database,
):
    seed_authorships(initialized_database, ["first"])
    candidate = queue_target_authors(initialized_database)[0]
    row = initialized_database.fetch_one(
        "SELECT author_id FROM candidates WHERE id = ?", (candidate.candidate_id,)
    )
    author_id = str(row["author_id"])
    initialized_database.execute(
        """
        UPDATE authors
        SET public_email = 'candidate@example.edu.cn',
            current_institution = '清华大学',
            current_status = '博士在读',
            homepage_url = 'https://example.edu/candidate'
        WHERE id = ?
        """,
        (author_id,),
    )

    with pytest.raises(ApprovalRequired):
        delete_candidate_data(initialized_database, candidate.candidate_id)

    initialized_database.record_approval(
        action="delete_candidate_data",
        target_type="candidate",
        target_id=candidate.candidate_id,
        decision="approved",
        preview={"candidate_id": candidate.candidate_id},
        decided_by="human",
    )
    delete_candidate_data(initialized_database, candidate.candidate_id)

    author = initialized_database.fetch_one(
        """
        SELECT normalized_name, display_name, public_email, current_institution,
               current_status, homepage_url, contact_suppressed
        FROM authors WHERE id = ?
        """,
        (author_id,),
    )
    assert dict(author) == {
        "normalized_name": f"deleted:{author_id}",
        "display_name": "已删除候选人",
        "public_email": None,
        "current_institution": None,
        "current_status": None,
        "homepage_url": None,
        "contact_suppressed": 1,
    }
    candidate_row = initialized_database.fetch_one(
        """
        SELECT status, suppressed, education_result, recommendation
        FROM candidates WHERE id = ?
        """,
        (candidate.candidate_id,),
    )
    assert dict(candidate_row) == {
        "status": CandidateStatus.CLOSED.value,
        "suppressed": 1,
        "education_result": None,
        "recommendation": None,
    }
