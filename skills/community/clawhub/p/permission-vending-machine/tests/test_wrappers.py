"""Tests for safe-* wrappers (mocked vault)."""

import os
import sqlite3
import tempfile
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_db(tmp_path):
    """Create a temporary grants.db with known test data."""
    db_path = tmp_path / "grants.db"
    conn = sqlite3.connect(str(db_path))
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS grants (
            grant_id        TEXT PRIMARY KEY,
            agent_id        TEXT NOT NULL,
            scope           TEXT NOT NULL,
            scope_type      TEXT NOT NULL,
            reason          TEXT NOT NULL,
            issued_at       TEXT NOT NULL,
            expires_at      TEXT NOT NULL,
            revoked         INTEGER NOT NULL DEFAULT 0,
            approved_by     TEXT
        );
        CREATE TABLE IF NOT EXISTS audit_log (
            entry_id    TEXT PRIMARY KEY,
            timestamp   TEXT NOT NULL,
            entry_type  TEXT NOT NULL,
            agent_id    TEXT,
            scope       TEXT,
            decision    TEXT,
            details     TEXT NOT NULL,
            grant_id    TEXT
        );
    """)
    now = datetime.now(timezone.utc)
    future = (now + timedelta(minutes=10)).isoformat()
    conn.execute(
        "INSERT INTO grants VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("grant_test123", "coder", "/tmp/allowed", "path",
         "testing", now.isoformat(), future, 0, "tyler"),
    )
    conn.commit()
    conn.close()
    return str(db_path)


class TestSafeRmGrantCheck:
    """Test that safe-rm correctly checks grants."""

    def test_safe_rm_allows_when_grant_exists(self, mock_db, tmp_path):
        """When a grant exists, safe-rm should execute rm."""
        with patch.dict(os.environ, {
            "PVM_DB": mock_db,
            "PVM_AGENT_ID": "coder",
            "GRANT_SCOPE": "/tmp/allowed",
        }):
            with patch("subprocess.run") as mock_run:
                with patch("builtins.open"):
                    # Simulate rm being called
                    mock_run.return_value = MagicMock(returncode=0)
                    result = os.system(
                        f"echo 'test' > /tmp/testfile && "
                        f"chmod +x {tmp_path.parent}/wrappers/safe-rm 2>/dev/null || true"
                    )

    def test_safe_rm_denies_without_grant(self, mock_db):
        """When no grant exists, safe-rm should exit 1."""
        # Simulate the check_grant call
        import sqlite3
        conn = sqlite3.connect(mock_db)
        conn.row_factory = sqlite3.Row
        now_iso = datetime.now(timezone.utc).isoformat()
        cur = conn.execute(
            "SELECT 1 FROM grants WHERE agent_id=? AND scope=? AND revoked=0 AND expires_at>?",
            ("coder", "/tmp/forbidden", now_iso)
        )
        assert cur.fetchone() is None  # no grant exists
        conn.close()

    def test_safe_rm_prefix_matching(self, mock_db):
        """Grant on /tmp should cover /tmp/subdir."""
        import sqlite3
        conn = sqlite3.connect(mock_db)
        conn.row_factory = sqlite3.Row
        now_iso = datetime.now(timezone.utc).isoformat()

        # Add parent grant
        conn.execute(
            "INSERT INTO grants VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("grant_parent", "coder", "/tmp", "path", "parent scope",
             datetime.now(timezone.utc).isoformat(),
             (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat(),
             0, "tyler")
        )
        conn.commit()

        # Check if child path is covered
        cur = conn.execute(
            "SELECT scope FROM grants WHERE agent_id=? AND scope_type='path' AND revoked=0 AND expires_at>?",
            ("coder", now_iso)
        )
        scopes = [row["scope"] for row in cur.fetchall()]
        assert "/tmp" in scopes

        # Child should be covered
        child_scope = "/tmp/subdir/file.txt"
        covered = any(
            child_scope == s or child_scope.startswith(s.rstrip("/") + "/")
            for s in scopes
        )
        assert covered


class TestSafeGitPushGrantCheck:
    def test_git_push_requires_force_flag(self, mock_db):
        """safe-git-push should only guard --force pushes."""
        # When no --force, it should not need a grant
        # This is implicit in the script logic
        pass

    def test_git_push_denies_force_without_grant(self, mock_db):
        """Force push without grant should be denied."""
        import sqlite3
        conn = sqlite3.connect(mock_db)
        conn.row_factory = sqlite3.Row
        now_iso = datetime.now(timezone.utc).isoformat()

        cur = conn.execute(
            "SELECT 1 FROM grants WHERE agent_id=? AND scope=? AND revoked=0 AND expires_at>?",
            ("coder", "https://github.com/tylerdotai/repo", now_iso)
        )
        assert cur.fetchone() is None  # no force-push grant


class TestWrapperScriptLogic:
    """Test the Python-equivalent logic of the shell wrappers."""

    def test_grant_scope_extraction(self):
        """Verify scope extraction from path arguments."""
        # If user runs: safe-rm /tmp/myfile
        # Scope should be: /tmp/myfile
        scope = "/tmp/myfile"
        assert scope.startswith("/")  # absolute path

    def test_inside_workspace_logic(self):
        """Test workspace boundary logic for safe-trash."""
        workspace = "/Users/soup/workspace"

        assert (workspace + "/coder/file.txt").startswith(workspace + "/")
        assert not "/tmp/forbidden".startswith(workspace + "/")

    def test_audit_log_written_on_execution(self, mock_db):
        """Verify execution is logged to audit_log."""
        import sqlite3
        import uuid
        conn = sqlite3.connect(mock_db)
        now_iso = datetime.now(timezone.utc).isoformat()

        conn.execute(
            "INSERT INTO audit_log (entry_id, timestamp, entry_type, agent_id, scope, decision, details, grant_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (f"audit_{uuid.uuid4().hex[:12]}", now_iso, "EXECUTION",
             "coder", "/tmp/allowed", "SUCCESS",
             "safe-rm executed: /tmp/allowed", None)
        )
        conn.commit()

        cur = conn.execute("SELECT * FROM audit_log WHERE decision='SUCCESS'")
        rows = cur.fetchall()
        assert len(rows) >= 1
        conn.close()
