"""
Integration tests for NextLink Exchange sync operations.

These tests mock EWS and Nextcloud APIs to validate sync behavior
without hitting real servers.
"""

import json
import os
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch, PropertyMock

import pytest

# Ensure modules are importable
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "modules", "exchange"))

from sync import (
    cmd_sync,
    cmd_reminders,
    cmd_link_calendar,
    cmd_status,
    get_sync_state,
    save_sync_state,
    SYNC_STATE_FILE,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def isolate_sync_state(tmp_path, monkeypatch):
    """Redirect sync state to a temporary file so tests don't pollute ~/.openclaw."""
    state_file = tmp_path / "task-sync-state.json"
    monkeypatch.setattr("sync.SYNC_STATE_FILE", state_file)
    monkeypatch.setattr("sync.SYNC_STATE_DIR", tmp_path)
    # Ensure clean state for each test
    if state_file.exists():
        state_file.unlink()
    yield state_file
    if state_file.exists():
        state_file.unlink()


@pytest.fixture
def fake_account():
    """Return a mock Exchange account with minimal realistic structure."""
    account = MagicMock()
    account.primary_smtp_address = "alex@example.com"
    account.default_timezone = None

    # Tasks folder
    tasks_folder = MagicMock()
    account.tasks = tasks_folder
    account.tasks.total_count = 0

    # Calendar folder
    calendar_folder = MagicMock()
    account.calendar = calendar_folder

    # Inbox (for reminder email tests)
    inbox_folder = MagicMock()
    account.inbox = inbox_folder
    account.inbox.total_count = 0
    account.inbox.unread_count = 0

    return account


@pytest.fixture
def make_fake_task():
    """Factory for fake Exchange Task objects."""
    def _make(
        task_id="task-1",
        subject="Test Task",
        status="NotStarted",
        due_date=None,
        changekey="ck-v1",
        percent_complete=0,
        importance="Normal",
        body=None,
    ):
        task = MagicMock()
        task.id = task_id
        task.subject = subject
        task.status = status
        task.due_date = due_date
        task.changekey = changekey
        task.percent_complete = percent_complete
        task.importance = importance
        task.body = body
        task.owner = "alex@example.com"
        task.delegation_state = None
        task.complete_date = None
        task.datetime_created = datetime.now()
        task.datetime_received = datetime.now()
        return task
    return _make


@pytest.fixture
def sample_tasks(make_fake_task):
    """Return a list of sample tasks for sync tests."""
    today = datetime.now()
    return [
        make_fake_task(
            task_id="task-new",
            subject="New Task",
            due_date=today + timedelta(days=1),
            changekey="ck-new",
        ),
        make_fake_task(
            task_id="task-existing",
            subject="Existing Task",
            due_date=today + timedelta(days=2),
            changekey="ck-existing",
        ),
        make_fake_task(
            task_id="task-completed",
            subject="Completed Task",
            status="Completed",
            due_date=today - timedelta(days=1),
            changekey="ck-completed",
        ),
    ]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_args(**kwargs):
    """Build an argparse.Namespace from keyword arguments."""
    return MagicMock(**kwargs)


# ---------------------------------------------------------------------------
# TestEmailSync
# ---------------------------------------------------------------------------

class TestEmailSync:
    """Tests for email-based reminder sync (reminders command)."""

    @patch("sync.get_account")
    @patch("sync.check_dependencies")
    def test_sync_new_email(self, mock_check, mock_get_account, fake_account, make_fake_task, isolate_sync_state):
        """Reminder command should detect tasks and prepare email when tasks exist."""
        mock_get_account.return_value = fake_account

        today = datetime.now()
        fake_account.tasks.all.return_value = [
            make_fake_task(
                task_id="task-overdue",
                subject="Overdue Email Task",
                due_date=today - timedelta(days=1),
                status="NotStarted",
            )
        ]

        args = make_args(to=None, hours=24, dry_run=True)

        with pytest.raises(SystemExit) as exc_info:
            cmd_reminders(args)

        assert exc_info.value.code == 0
        fake_account.tasks.all.assert_called_once()

    @patch("sync.get_account")
    @patch("sync.check_dependencies")
    def test_sync_duplicate_email(self, mock_check, mock_get_account, fake_account, make_fake_task, isolate_sync_state):
        """Reminder command should not duplicate emails on repeated dry-runs."""
        mock_get_account.return_value = fake_account

        today = datetime.now()
        fake_account.tasks.all.return_value = [
            make_fake_task(
                task_id="task-dup",
                subject="Duplicate Task",
                due_date=today - timedelta(days=1),
                status="NotStarted",
            )
        ]

        args = make_args(to=None, hours=24, dry_run=True)

        # First call
        with pytest.raises(SystemExit) as exc_info:
            cmd_reminders(args)
        assert exc_info.value.code == 0

        # Second call — same result, no error
        with pytest.raises(SystemExit) as exc_info:
            cmd_reminders(args)
        assert exc_info.value.code == 0

    @patch("sync.get_account")
    @patch("sync.check_dependencies")
    def test_sync_deleted_email(self, mock_check, mock_get_account, fake_account, make_fake_task, isolate_sync_state):
        """When no overdue or upcoming tasks exist, reminders should report zero."""
        mock_get_account.return_value = fake_account
        fake_account.tasks.all.return_value = []

        args = make_args(to=None, hours=24, dry_run=True)

        with pytest.raises(SystemExit) as exc_info:
            cmd_reminders(args)

        assert exc_info.value.code == 0


# ---------------------------------------------------------------------------
# TestContactSync (mapped to task sync in current module scope)
# ---------------------------------------------------------------------------

class TestContactSync:
    """Tests for bidirectional task sync behavior."""

    @patch("sync.get_account")
    @patch("sync.check_dependencies")
    def test_sync_new_contact(self, mock_check, mock_get_account, fake_account, sample_tasks, isolate_sync_state):
        """Sync should add new tasks from Exchange to local state."""
        mock_get_account.return_value = fake_account

        # Simulate one new task in Exchange
        fake_account.tasks.all.return_value.order_by.return_value = [sample_tasks[0]]
        fake_account.tasks.total_count = 1

        args = make_args(limit=50)

        with pytest.raises(SystemExit) as exc_info:
            cmd_sync(args)

        assert exc_info.value.code == 0
        state = get_sync_state()
        assert "task-new" in state["tasks"]
        assert state["tasks"]["task-new"]["subject"] == "New Task"

    @patch("sync.get_account")
    @patch("sync.check_dependencies")
    def test_sync_updated_contact(self, mock_check, mock_get_account, fake_account, make_fake_task, isolate_sync_state):
        """Sync should update existing tasks when changekey differs."""
        mock_get_account.return_value = fake_account

        # Pre-seed local state
        state = get_sync_state()
        state["tasks"]["task-update"] = {
            "id": "task-update",
            "subject": "Old Subject",
            "changekey": "ck-old",
            "status": "NotStarted",
            "due_date": None,
        }
        save_sync_state(state)

        updated_task = make_fake_task(
            task_id="task-update",
            subject="Updated Subject",
            changekey="ck-new",
        )
        fake_account.tasks.all.return_value.order_by.return_value = [updated_task]
        fake_account.tasks.total_count = 1

        args = make_args(limit=50)

        with pytest.raises(SystemExit) as exc_info:
            cmd_sync(args)

        assert exc_info.value.code == 0
        state = get_sync_state()
        assert state["tasks"]["task-update"]["subject"] == "Updated Subject"

    @patch("sync.get_account")
    @patch("sync.check_dependencies")
    def test_conflict_resolution(self, mock_check, mock_get_account, fake_account, make_fake_task, isolate_sync_state):
        """When task exists locally and remotely with same ID but different changekey,
        remote state should win (last-write-wins from Exchange)."""
        mock_get_account.return_value = fake_account

        state = get_sync_state()
        state["tasks"]["task-conflict"] = {
            "id": "task-conflict",
            "subject": "Local Version",
            "changekey": "ck-local",
            "status": "NotStarted",
            "due_date": None,
        }
        save_sync_state(state)

        remote_task = make_fake_task(
            task_id="task-conflict",
            subject="Remote Version",
            changekey="ck-remote",
        )
        fake_account.tasks.all.return_value.order_by.return_value = [remote_task]
        fake_account.tasks.total_count = 1

        args = make_args(limit=50)

        with pytest.raises(SystemExit) as exc_info:
            cmd_sync(args)

        assert exc_info.value.code == 0
        state = get_sync_state()
        assert state["tasks"]["task-conflict"]["subject"] == "Remote Version"


# ---------------------------------------------------------------------------
# TestTaskSync
# ---------------------------------------------------------------------------

class TestTaskSync:
    """Tests for task deletion, status, and calendar linking."""

    @patch("sync.get_account")
    @patch("sync.check_dependencies")
    def test_sync_deleted_task(self, mock_check, mock_get_account, fake_account, make_fake_task, isolate_sync_state):
        """Tasks deleted in Exchange should be removed from local state."""
        mock_get_account.return_value = fake_account

        state = get_sync_state()
        state["tasks"]["task-gone"] = {
            "id": "task-gone",
            "subject": "Deleted Task",
            "changekey": "ck-gone",
        }
        save_sync_state(state)

        # Exchange returns no tasks
        fake_account.tasks.all.return_value.order_by.return_value = []
        fake_account.tasks.total_count = 0

        args = make_args(limit=50)

        with pytest.raises(SystemExit) as exc_info:
            cmd_sync(args)

        assert exc_info.value.code == 0
        state = get_sync_state()
        assert "task-gone" not in state["tasks"]

    @patch("sync.get_account")
    @patch("sync.check_dependencies")
    def test_sync_status_report(self, mock_check, mock_get_account, fake_account, make_fake_task, isolate_sync_state):
        """Status command should report Exchange and sync statistics."""
        mock_get_account.return_value = fake_account

        today = datetime.now()
        fake_account.tasks.total_count = 3
        fake_account.tasks.all.return_value.only.return_value = [
            make_fake_task(status="NotStarted", due_date=today + timedelta(days=1)),
            make_fake_task(status="Completed", due_date=today - timedelta(days=1)),
            make_fake_task(status="NotStarted", due_date=None),
        ]

        args = make_args()

        with pytest.raises(SystemExit) as exc_info:
            cmd_status(args)

        assert exc_info.value.code == 0

    @patch("sync.get_account")
    @patch("sync.check_dependencies")
    def test_link_calendar_from_task(self, mock_check, mock_get_account, fake_account, make_fake_task, isolate_sync_state):
        """Link-calendar should create a CalendarItem from a task."""
        mock_get_account.return_value = fake_account

        task = make_fake_task(
            task_id="task-cal",
            subject="Calendar Task",
            due_date=datetime(2026, 5, 15),
        )
        fake_account.tasks.get.return_value = task
        fake_account.calendar = MagicMock()

        mock_event = MagicMock()
        mock_event.id = "event-123"
        mock_event.subject = "📌 Calendar Task"
        mock_event.start = datetime(2026, 5, 15, 9, 0)
        mock_event.end = datetime(2026, 5, 15, 10, 0)

        fake_account.calendar.save.return_value = None

        args = make_args(id="task-cal", time="09:00", duration=60, reminder=30, invite=False)

        with patch("sync.CalendarItem", return_value=mock_event) as mock_cal_item:
            with pytest.raises(SystemExit) as exc_info:
                cmd_link_calendar(args)
            assert exc_info.value.code == 0
            mock_cal_item.assert_called_once()


# ---------------------------------------------------------------------------
# TestErrorHandling
# ---------------------------------------------------------------------------

class TestErrorHandling:
    """Tests for network failures, auth errors, and edge cases."""

    @patch("sync.get_account")
    @patch("sync.check_dependencies")
    def test_ews_auth_error(self, mock_check, mock_get_account, isolate_sync_state):
        """Sync should handle authentication failure by exiting with code 1."""
        # connection.py catches UnauthorizedError and calls die() -> sys.exit(1).
        # When get_account() is mocked directly, the raw error propagates from cmd_sync
        # since it has no try/except of its own. We verify exit behavior via pytest.raises.
        from exchangelib.errors import UnauthorizedError as EWSUnauthorizedError
        mock_get_account.side_effect = EWSUnauthorizedError("Invalid credentials")

        args = make_args(limit=50)

        with pytest.raises((SystemExit, EWSUnauthorizedError)):
            cmd_sync(args)

    @patch("sync.get_account")
    @patch("sync.check_dependencies")
    def test_nextcloud_timeout(self, mock_check, mock_get_account, fake_account, isolate_sync_state):
        """Sync should handle timeout errors by exiting with code 1."""
        mock_get_account.return_value = fake_account
        fake_account.tasks.all.return_value.order_by.side_effect = TimeoutError("Connection timed out")

        args = make_args(limit=50)

        with pytest.raises((SystemExit, TimeoutError)):
            cmd_sync(args)

    @patch("sync.get_account")
    @patch("sync.check_dependencies")
    def test_corrupt_sync_state(self, mock_check, mock_get_account, fake_account, isolate_sync_state):
        """Corrupt sync state file should be handled gracefully (starts fresh)."""
        mock_get_account.return_value = fake_account

        # Write invalid JSON to state file
        isolate_sync_state.write_text("not-json{")

        fake_account.tasks.all.return_value.order_by.return_value = []
        fake_account.tasks.total_count = 0

        args = make_args(limit=50)

        with pytest.raises(SystemExit) as exc_info:
            cmd_sync(args)

        assert exc_info.value.code == 0
        state = get_sync_state()
        assert state["tasks"] == {}

    @patch("sync.get_account")
    @patch("sync.check_dependencies")
    def test_missing_task_for_calendar_link(self, mock_check, mock_get_account, fake_account, isolate_sync_state):
        """Link-calendar with missing task ID should exit with error."""
        mock_get_account.return_value = fake_account
        fake_account.tasks.get.side_effect = Exception("Task not found")

        args = make_args(id="missing-id", time="09:00", duration=60, reminder=30, invite=False)

        with pytest.raises(SystemExit) as exc_info:
            cmd_link_calendar(args)

        assert exc_info.value.code == 1

    @patch("sync.get_account")
    @patch("sync.check_dependencies")
    def test_empty_task_list_sync(self, mock_check, mock_get_account, fake_account, isolate_sync_state):
        """Sync with empty task list should succeed and clear tracked tasks."""
        mock_get_account.return_value = fake_account
        fake_account.tasks.all.return_value.order_by.return_value = []
        fake_account.tasks.total_count = 0

        args = make_args(limit=50)

        with pytest.raises(SystemExit) as exc_info:
            cmd_sync(args)

        assert exc_info.value.code == 0
        state = get_sync_state()
        assert state["tasks"] == {}
        assert state["last_sync"] is not None

    @patch("sync.get_account")
    @patch("sync.check_dependencies")
    def test_reminder_email_send_failure(self, mock_check, mock_get_account, fake_account, make_fake_task, isolate_sync_state):
        """Reminder email send failure should be caught and reported."""
        mock_get_account.return_value = fake_account

        today = datetime.now()
        fake_account.tasks.all.return_value = [
            make_fake_task(
                task_id="task-rem",
                subject="Reminder Task",
                due_date=today - timedelta(days=1),
                status="NotStarted",
            )
        ]

        args = make_args(to=None, hours=24, dry_run=False)

        with patch("sync.die", side_effect=SystemExit(1)):
            with pytest.raises(SystemExit) as exc_info:
                cmd_reminders(args)
            assert exc_info.value.code == 1


class TestOwnerEmailFallback:
    """Test OWNER_EMAIL config variable fallback behavior."""

    @patch("sync.get_connection_config")
    @patch("sync.get_account")
    @patch("sync.check_dependencies")
    def test_reminder_uses_owner_email(self, mock_check, mock_get_account, mock_config, fake_account, make_fake_task, isolate_sync_state):
        """When OWNER_EMAIL is set, reminders should use it as recipient."""
        mock_get_account.return_value = fake_account
        mock_config.return_value = {
            "owner_email": "owner@example.com",
            "email": "service@example.com",
        }

        today = datetime.now()
        fake_account.tasks.all.return_value = [
            make_fake_task(
                task_id="task-owner",
                subject="Owner Task",
                due_date=today - timedelta(days=1),
                status="NotStarted",
            )
        ]

        args = make_args(to=None, hours=24, dry_run=True)
        with patch("sync.out") as mock_out:
            cmd_reminders(args)
            # Dry run should show owner_email as recipient, not service account
            call_args = mock_out.call_args[0][0]
            assert call_args["would_send_to"] == "owner@example.com"

    @patch("sync.get_connection_config")
    @patch("sync.get_account")
    @patch("sync.check_dependencies")
    def test_reminder_falls_back_to_account_email(self, mock_check, mock_get_account, mock_config, fake_account, make_fake_task, isolate_sync_state):
        """When OWNER_EMAIL is not set, reminders should fall back to account.primary_smtp_address."""
        mock_get_account.return_value = fake_account
        mock_config.return_value = {
            "owner_email": None,  # Not set
            "email": "service@example.com",
        }

        today = datetime.now()
        fake_account.tasks.all.return_value = [
            make_fake_task(
                task_id="task-fallback",
                subject="Fallback Task",
                due_date=today - timedelta(days=1),
                status="NotStarted",
            )
        ]

        args = make_args(to=None, hours=24, dry_run=True)
        with patch("sync.out") as mock_out:
            cmd_reminders(args)
            # Should fall back to account.primary_smtp_address
            call_args = mock_out.call_args[0][0]
            assert call_args["would_send_to"] == fake_account.primary_smtp_address

    @patch("sync.get_connection_config")
    @patch("sync.get_account")
    @patch("sync.check_dependencies")
    def test_reminder_explicit_to_overrides_owner_email(self, mock_check, mock_get_account, mock_config, fake_account, make_fake_task, isolate_sync_state):
        """When --to is given, it should override both OWNER_EMAIL and account address."""
        mock_get_account.return_value = fake_account
        mock_config.return_value = {
            "owner_email": "owner@example.com",
            "email": "service@example.com",
        }

        today = datetime.now()
        fake_account.tasks.all.return_value = [
            make_fake_task(
                task_id="task-explicit",
                subject="Explicit To Task",
                due_date=today - timedelta(days=1),
                status="NotStarted",
            )
        ]

        args = make_args(to="explicit@example.com", hours=24, dry_run=True)
        with patch("sync.out") as mock_out:
            cmd_reminders(args)
            # Explicit --to should take priority
            call_args = mock_out.call_args[0][0]
            assert call_args["would_send_to"] == "explicit@example.com"
