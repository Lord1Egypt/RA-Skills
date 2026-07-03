from __future__ import annotations

import sqlite3
import subprocess
import sys
import json
from pathlib import Path

import pytest

from db import ApprovalRequired, Database


REQUIRED_TABLES = {
    "papers",
    "authors",
    "paper_authors",
    "jobs",
    "job_snapshots",
    "paper_job_matches",
    "candidates",
    "approvals",
    "mail_threads",
    "followups",
    "audit_logs",
    "source_runs",
    "author_evidence",
}


def test_database_initializes_all_required_tables(tmp_path):
    database = Database(tmp_path / "recruitment.db")

    database.initialize()

    assert REQUIRED_TABLES <= set(database.table_names())


def test_send_authorization_requires_matching_approval(initialized_database):
    with pytest.raises(ApprovalRequired, match="send_initial"):
        initialized_database.authorize_action(
            "send_initial",
            "candidate",
            "candidate-1",
        )


def test_approval_is_scoped_and_consumed_once(initialized_database):
    approval_id = initialized_database.record_approval(
        action="send_initial",
        target_type="candidate",
        target_id="candidate-1",
        decision="approved",
        preview={"to": "candidate@example.edu"},
        decided_by="human",
    )

    authorized = initialized_database.authorize_action(
        "send_initial",
        "candidate",
        "candidate-1",
    )

    assert authorized == approval_id
    with pytest.raises(ApprovalRequired):
        initialized_database.authorize_action(
            "send_initial",
            "candidate",
            "candidate-1",
        )
    with pytest.raises(ApprovalRequired):
        initialized_database.authorize_action(
            "send_reply",
            "candidate",
            "candidate-1",
        )


def test_database_status_returns_zero_counts_for_fresh_database(initialized_database):
    status = initialized_database.status()

    assert status["papers"] == 0
    assert status["authors"] == 0
    assert status["candidates"] == 0
    assert status["approvals"] == 0
    assert status["mail_threads"] == 0


def test_initialize_adds_new_columns_to_existing_database(tmp_path):
    path = tmp_path / "old.db"
    connection = sqlite3.connect(path)
    connection.executescript(
        """
        CREATE TABLE papers (
            id TEXT PRIMARY KEY,
            doi TEXT,
            normalized_title TEXT
        );
        CREATE TABLE authors (id TEXT PRIMARY KEY);
        CREATE TABLE mail_threads (id TEXT PRIMARY KEY);
        CREATE TABLE author_evidence (id TEXT PRIMARY KEY);
        """
    )
    connection.close()

    database = Database(path)
    database.initialize()

    assert {
        "publication_date_precision",
        "keyword_model",
        "keyword_prompt_version",
        "keywords_generated_at",
    } <= set(database.column_names("papers"))
    assert {"contact_suppressed", "contact_suppression_reason"} <= set(
        database.column_names("authors")
    )
    assert {"candidate_ids_json", "body_html"} <= set(
        database.column_names("mail_threads")
    )
    assert "mainland_china" in database.column_names("author_evidence")


def test_db_cli_records_human_approval(tmp_path):
    database_path = tmp_path / "recruitment.db"
    script = Path(__file__).resolve().parents[1] / "scripts" / "db.py"
    subprocess.run(
        [
            sys.executable,
            str(script),
            "init",
            "--database",
            str(database_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(script),
            "approve",
            "--database",
            str(database_path),
            "--action",
            "send_initial",
            "--target-type",
            "mail_thread",
            "--target-id",
            "mail-1",
            "--preview-json",
            '{"to":"candidate@example.edu.cn"}',
            "--decided-by",
            "user",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    result = json.loads(completed.stdout)
    database = Database(database_path)
    assert result["approval_id"]
    assert database.fetch_one(
        "SELECT decision FROM approvals WHERE id = ?", (result["approval_id"],)
    )["decision"] == "approved"
