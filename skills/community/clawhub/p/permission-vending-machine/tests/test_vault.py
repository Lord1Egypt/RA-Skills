"""Tests for vault.py."""

import threading
from datetime import datetime, timedelta, timezone

import pytest

from pvm.models import AuditEntryType, Decision, Grant
from pvm.vault import Vault


# vault fixture is defined in conftest.py (uses UUID in-memory SQLite, isolated per test)


class TestVaultGrantLifecycle:
    def test_create_grant(self, vault):
        grant = vault.create_grant(
            agent_id="test-agent",
            scope="/tmp/test",
            scope_type="path",
            reason="testing",
            ttl_minutes=10,
            approved_by="tyler",
        )
        assert grant.grant_id.startswith("grant_")
        assert grant.agent_id == "test-agent"
        assert grant.scope == "/tmp/test"
        assert grant.scope_type == "path"
        assert grant.approved_by == "tyler"
        assert not grant.revoked
        assert grant.expires_at > grant.issued_at

    def test_check_grant_active(self, vault):
        vault.create_grant(
            agent_id="test-agent",
            scope="/tmp/test",
            scope_type="path",
            reason="testing",
            ttl_minutes=10,
        )
        assert vault.check_grant("test-agent", "/tmp/test") is True

    def test_check_grant_not_found(self, vault):
        assert vault.check_grant("nobody", "/tmp/test") is False

    def test_check_grant_wrong_agent(self, vault):
        vault.create_grant(
            agent_id="test-agent",
            scope="/tmp/test",
            scope_type="path",
            reason="testing",
            ttl_minutes=10,
        )
        assert vault.check_grant("other-agent", "/tmp/test") is False

    def test_check_grant_wrong_scope(self, vault):
        vault.create_grant(
            agent_id="test-agent",
            scope="/tmp/test",
            scope_type="path",
            reason="testing",
            ttl_minutes=10,
        )
        assert vault.check_grant("test-agent", "/tmp/other") is False

    def test_check_grant_expired(self, vault):
        """Grant is denied once its TTL has passed."""
        grant = vault.create_grant(
            agent_id="test-agent",
            scope="/tmp/test",
            scope_type="path",
            reason="testing",
            ttl_minutes=1,
        )
        # Backdate expires_at to 5 minutes in the past via the vault's own tx
        past = (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat()
        with vault._tx() as conn:
            conn.execute(
                "UPDATE grants SET expires_at = ? WHERE grant_id = ?",
                (past, grant.grant_id),
            )
        # check_grant calls _purge_expired first, which marks expired → revoked
        assert vault.check_grant("test-agent", "/tmp/test") is False

    def test_revoke_grant(self, vault):
        grant = vault.create_grant(
            agent_id="test-agent",
            scope="/tmp/test",
            scope_type="path",
            reason="testing",
            ttl_minutes=10,
        )
        vault.revoke_grant(grant.grant_id)
        # Revoked grants are not active
        assert vault.check_grant("test-agent", "/tmp/test") is False
        # Can still fetch the grant record itself
        fetched = vault.get_grant(grant.grant_id)
        assert fetched is not None
        assert fetched.revoked is True

    def test_get_active_grants(self, vault):
        vault.create_grant(
            agent_id="test-agent",
            scope="/tmp/test1",
            scope_type="path",
            reason="r1",
            ttl_minutes=10,
        )
        vault.create_grant(
            agent_id="test-agent",
            scope="/tmp/test2",
            scope_type="path",
            reason="r2",
            ttl_minutes=10,
        )
        grants = vault.get_active_grants(agent_id="test-agent")
        assert len(grants) == 2

    def test_get_active_grants_filtered_by_agent(self, vault):
        vault.create_grant(
            agent_id="agent-a",
            scope="/tmp/a",
            scope_type="path",
            reason="r",
            ttl_minutes=10,
        )
        vault.create_grant(
            agent_id="agent-b",
            scope="/tmp/b",
            scope_type="path",
            reason="r",
            ttl_minutes=10,
        )
        grants = vault.get_active_grants(agent_id="agent-a")
        assert len(grants) == 1
        assert grants[0].agent_id == "agent-a"

    def test_get_grant_by_id(self, vault):
        created = vault.create_grant(
            agent_id="test-agent",
            scope="/tmp/test",
            scope_type="path",
            reason="testing",
            ttl_minutes=10,
        )
        fetched = vault.get_grant(created.grant_id)
        assert fetched is not None
        assert fetched.grant_id == created.grant_id

    def test_get_grant_not_found(self, vault):
        assert vault.get_grant("grant_nonexistent") is None


class TestVaultPathMatching:
    def test_check_grant_glob_exact(self, vault):
        vault.create_grant(
            agent_id="test-agent",
            scope="/tmp/parent",
            scope_type="path",
            reason="testing",
            ttl_minutes=10,
        )
        assert vault.check_grant_glob("test-agent", "/tmp/parent", "path") is True

    def test_check_grant_glob_subpath(self, vault):
        vault.create_grant(
            agent_id="test-agent",
            scope="/tmp/parent",
            scope_type="path",
            reason="testing",
            ttl_minutes=10,
        )
        assert vault.check_grant_glob("test-agent", "/tmp/parent/child/file.txt", "path") is True

    def test_check_grant_glob_sibling(self, vault):
        vault.create_grant(
            agent_id="test-agent",
            scope="/tmp/parent",
            scope_type="path",
            reason="testing",
            ttl_minutes=10,
        )
        assert vault.check_grant_glob("test-agent", "/tmp/other", "path") is False

    def test_check_grant_glob_repo_exact(self, vault):
        vault.create_grant(
            agent_id="test-agent",
            scope="https://github.com/tylerdotai/repo",
            scope_type="repo",
            reason="testing",
            ttl_minutes=10,
        )
        assert vault.check_grant_glob("test-agent", "https://github.com/tylerdotai/repo", "repo") is True


class TestVaultAuditLog:
    def test_audit_log_written_on_create(self, vault):
        vault.create_grant(
            agent_id="test-agent",
            scope="/tmp/test",
            scope_type="path",
            reason="testing",
            ttl_minutes=10,
        )
        entries = vault.get_audit_log(agent_id="test-agent")
        assert len(entries) >= 1
        approval_entries = [e for e in entries if e.decision == Decision.GRANTED]
        assert len(approval_entries) >= 1

    def test_audit_log_written_on_revoke(self, vault):
        grant = vault.create_grant(
            agent_id="test-agent",
            scope="/tmp/test",
            scope_type="path",
            reason="testing",
            ttl_minutes=10,
        )
        vault.revoke_grant(grant.grant_id)
        entries = vault.get_audit_log(agent_id="test-agent", decision=Decision.REVOKED)
        assert len(entries) >= 1

    def test_audit_log_log_audit(self, vault):
        vault.log_audit(
            entry_type=AuditEntryType.REQUEST,
            agent_id="test-agent",
            scope="/tmp/test",
            decision=Decision.DENIED,
            details="Test log entry",
        )
        entries = vault.get_audit_log(agent_id="test-agent", decision=Decision.DENIED)
        assert len(entries) >= 1
        assert entries[0].details == "Test log entry"

    def test_audit_log_limit(self, vault):
        for i in range(10):
            vault.log_audit(
                entry_type=AuditEntryType.REQUEST,
                details=f"Entry {i}",
            )
        entries = vault.get_audit_log(limit=5)
        assert len(entries) == 5


class TestVaultThreadSafety:
    def test_concurrent_grants(self, tmp_path):
        """Multiple threads writing to the same vault simultaneously — no data loss."""
        # Use a file-based DB for this test: in-memory SQLite doesn't handle
        # concurrent writes well even with cache=shared due to locking.
        db_path = str(tmp_path / "concurrent.db")
        shared_vault = Vault(db_path)

        errors = []

        def writer(agent_id: str):
            try:
                for i in range(10):
                    shared_vault.create_grant(
                        agent_id=agent_id,
                        scope=f"/tmp/{agent_id}/{i}",
                        scope_type="path",
                        reason="concurrent test",
                        ttl_minutes=5,
                    )
            except Exception as e:
                errors.append(e)

        t1 = threading.Thread(target=writer, args=("agent-a",))
        t2 = threading.Thread(target=writer, args=("agent-b",))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        assert not errors, f"Thread errors: {errors}"
        grants = shared_vault.get_active_grants()
        assert len(grants) == 20
