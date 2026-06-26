"""initial schema

Revision ID: 001
Revises: None
Create Date: 2026-06-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS commits (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            commit_hash     TEXT NOT NULL UNIQUE,
            short_hash      TEXT NOT NULL,
            author_name     TEXT NOT NULL,
            author_email    TEXT NOT NULL,
            author_ts       TEXT NOT NULL,
            committer_name  TEXT,
            committer_email TEXT,
            commit_subject  TEXT NOT NULL,
            commit_body     TEXT,
            branch          TEXT,
            repo_path       TEXT NOT NULL,
            repo_name       TEXT NOT NULL,
            parent_hashes   TEXT,
            recorded_at     TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    op.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_commit_hash ON commits(commit_hash)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_repo_path ON commits(repo_path)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_author_email ON commits(author_email)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_recorded_at ON commits(recorded_at)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS idx_recorded_at")
    op.execute("DROP INDEX IF EXISTS idx_author_email")
    op.execute("DROP INDEX IF EXISTS idx_repo_path")
    op.execute("DROP INDEX IF EXISTS idx_commit_hash")
    op.execute("DROP TABLE IF EXISTS commits")
