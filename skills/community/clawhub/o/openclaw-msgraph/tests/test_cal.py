"""Tests for cal module calendar commands."""

import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import pytest
import cal


class TestCmdList:
    """Tests for cmd_list command."""

    @patch("cal.graph_api.graph_get")
    def test_cmd_list_default_days(self, mock_get, capsys):
        """Test listing events with default 7 days."""
        mock_get.return_value = {
            "value": [
                {
                    "id": "event-1",
                    "subject": "Team Meeting",
                    "start": {"dateTime": "2026-03-10T10:00:00", "timeZone": "America/New_York"},
                    "end": {"dateTime": "2026-03-10T11:00:00", "timeZone": "America/New_York"},
                    "location": {"displayName": "Conference Room A"},
                    "organizer": {"emailAddress": {"name": "John", "address": "john@example.com"}},
                    "attendees": [],
                    "isAllDay": False,
                    "onlineMeetingUrl": None,
                    "isCancelled": False,
                    "bodyPreview": ""
                }
            ]
        }

        cal.cmd_list([])
        
        captured = capsys.readouterr()
        assert "CALENDAR" in captured.out
        assert "Team Meeting" in captured.out
        assert "Conference Room A" in captured.out

    @patch("cal.graph_api.graph_get")
    def test_cmd_list_custom_days(self, mock_get, capsys):
        """Test listing events with custom day range."""
        mock_get.return_value = {"value": []}

        cal.cmd_list(["--days", "14"])
        
        # Verify correct parameters were passed
        call_args = mock_get.call_args[0]
        params = call_args[1]
        assert "startDateTime" in params
        assert "endDateTime" in params

    @patch("cal.graph_api.graph_get")
    def test_cmd_list_no_events(self, mock_get, capsys):
        """Test listing when no events exist."""
        mock_get.return_value = {"value": []}

        cal.cmd_list([])
        
        captured = capsys.readouterr()
        assert "No events" in captured.out

    @patch("cal.graph_api.graph_get")
    def test_cmd_list_all_day_event(self, mock_get, capsys):
        """Test that all-day events are displayed correctly."""
        mock_get.return_value = {
            "value": [
                {
                    "id": "event-1",
                    "subject": "Company Off-site",
                    "start": {"dateTime": "2026-03-15", "timeZone": "America/New_York"},
                    "end": {"dateTime": "2026-03-16", "timeZone": "America/New_York"},
                    "isAllDay": True,
                    "organizer": {"emailAddress": {}},
                    "attendees": [],
                    "location": {},
                    "onlineMeetingUrl": None,
                    "isCancelled": False,
                    "bodyPreview": ""
                }
            ]
        }

        cal.cmd_list([])
        
        captured = capsys.readouterr()
        assert "All day" in captured.out

    @patch("cal.graph_api.graph_get")
    def test_cmd_list_skips_cancelled(self, mock_get, capsys):
        """Test that cancelled events are skipped."""
        mock_get.return_value = {
            "value": [
                {
                    "id": "event-1",
                    "subject": "Cancelled Meeting",
                    "start": {"dateTime": "2026-03-10T10:00:00", "timeZone": "America/New_York"},
                    "end": {"dateTime": "2026-03-10T11:00:00", "timeZone": "America/New_York"},
                    "isAllDay": False,
                    "isCancelled": True,
                    "organizer": {"emailAddress": {}},
                    "attendees": [],
                    "location": {},
                    "onlineMeetingUrl": None,
                    "bodyPreview": ""
                }
            ]
        }

        cal.cmd_list([])
        
        captured = capsys.readouterr()
        assert "Cancelled Meeting" not in captured.out


class TestCmdGet:
    """Tests for cmd_get command."""

    @patch("cal.graph_api.graph_get")
    def test_cmd_get_event_details(self, mock_get, capsys, sample_event):
        """Test getting detailed event information."""
        mock_get.return_value = sample_event

        cal.cmd_get(["event-456"])
        
        captured = capsys.readouterr()
        assert "Team Sync" in captured.out
        assert "Conference Room A" in captured.out
        assert "organizer@example.com" in captured.out

    @patch("cal.graph_api.graph_get")
    def test_cmd_get_with_attendees(self, mock_get, capsys, sample_event):
        """Test event details with attendees."""
        mock_get.return_value = sample_event

        cal.cmd_get(["event-456"])
        
        captured = capsys.readouterr()
        assert "Attendees:" in captured.out
        assert "attendee1@example.com" in captured.out

    def test_cmd_get_no_event_id(self):
        """Test get command without event ID."""
        with pytest.raises(SystemExit):
            cal.cmd_get([])


class TestCmdCreate:
    """Tests for cmd_create command."""

    @patch("cal.graph_api.graph_post")
    def test_cmd_create_basic_event(self, mock_post, capsys):
        """Test creating a basic event."""
        mock_post.return_value = {
            "id": "new-event-123",
            "subject": "New Meeting",
            "start": {"dateTime": "2026-03-10T10:00:00"},
            "end": {"dateTime": "2026-03-10T11:00:00"},
            "webLink": "https://outlook.office365.com/..."
        }

        cal.cmd_create([
            "--subject", "New Meeting",
            "--start", "2026-03-10T10:00",
            "--end", "2026-03-10T11:00"
        ])
        
        captured = capsys.readouterr()
        assert "Event created" in captured.out
        assert "New Meeting" in captured.out

    @patch("cal.graph_api.graph_post")
    def test_cmd_create_with_attendees(self, mock_post, capsys):
        """Test creating event with attendees."""
        mock_post.return_value = {
            "id": "event-123",
            "subject": "Team Sync",
            "start": {"dateTime": "2026-03-10T10:00:00"},
            "end": {"dateTime": "2026-03-10T11:00:00"},
            "webLink": ""
        }

        cal.cmd_create([
            "--subject", "Team Sync",
            "--start", "2026-03-10T10:00",
            "--end", "2026-03-10T11:00",
            "--attendees", "alice@example.com,bob@example.com"
        ])
        
        # Verify attendees were included in payload
        call_args = mock_post.call_args
        payload = call_args[0][1]
        assert "attendees" in payload
        assert len(payload["attendees"]) == 2

    @patch("cal.graph_api.graph_post")
    def test_cmd_create_with_location(self, mock_post, capsys):
        """Test creating event with location."""
        mock_post.return_value = {
            "id": "event-123",
            "subject": "Meeting",
            "start": {"dateTime": ""},
            "end": {"dateTime": ""},
            "webLink": ""
        }

        cal.cmd_create([
            "--subject", "Meeting",
            "--start", "2026-03-10T10:00",
            "--end", "2026-03-10T11:00",
            "--location", "Conference Room B"
        ])
        
        call_args = mock_post.call_args
        payload = call_args[0][1]
        assert "location" in payload
        assert payload["location"]["displayName"] == "Conference Room B"

    @patch("cal.graph_api.graph_post")
    def test_cmd_create_missing_required_args(self, mock_post):
        """Test create command with missing required arguments."""
        with pytest.raises(SystemExit):
            cal.cmd_create(["--subject", "Meeting"])  # Missing start/end


class TestCmdDelete:
    """Tests for cmd_delete command."""

    @patch("builtins.input", return_value="y")
    @patch("cal.graph_api.graph_delete")
    def test_cmd_delete_with_confirmation(self, mock_delete, mock_input, capsys):
        """Test deleting event with confirmation."""
        cal.cmd_delete(["event-123"])
        
        mock_delete.assert_called_once_with("/me/events/event-123")
        captured = capsys.readouterr()
        assert "deleted" in captured.out.lower()

    @patch("builtins.input", return_value="n")
    @patch("cal.graph_api.graph_delete")
    def test_cmd_delete_decline_confirmation(self, mock_delete, mock_input, capsys):
        """Test declining deletion confirmation."""
        cal.cmd_delete(["event-123"])
        
        mock_delete.assert_not_called()
        captured = capsys.readouterr()
        assert "Cancelled" in captured.out

    @patch("cal.graph_api.graph_delete")
    def test_cmd_delete_with_confirm_flag(self, mock_delete, capsys):
        """Test deleting with --confirm flag skips prompt."""
        cal.cmd_delete(["event-123", "--confirm"])
        
        mock_delete.assert_called_once_with("/me/events/event-123")


class TestCmdCalendars:
    """Tests for cmd_calendars command."""

    @patch("cal.graph_api.graph_get")
    def test_cmd_calendars_list(self, mock_get, capsys):
        """Test listing available calendars."""
        mock_get.return_value = {
            "value": [
                {
                    "id": "cal-1",
                    "name": "Calendar",
                    "isDefaultCalendar": True,
                    "canEdit": True,
                    "color": "auto"
                },
                {
                    "id": "cal-2",
                    "name": "Shared Calendar",
                    "isDefaultCalendar": False,
                    "canEdit": False,
                    "color": "auto"
                }
            ]
        }

        cal.cmd_calendars([])
        
        captured = capsys.readouterr()
        assert "CALENDARS" in captured.out
        assert "Calendar" in captured.out
        assert "[default]" in captured.out
        assert "read-only" in captured.out


class TestCalIntegration:
    """Integration tests for cal module."""

    @patch("cal.graph_api.graph_get")
    def test_list_shows_meeting_url(self, mock_get, capsys):
        """Test that online meeting URLs are indicated."""
        mock_get.return_value = {
            "value": [
                {
                    "id": "event-1",
                    "subject": "Virtual Standup",
                    "start": {"dateTime": "2026-03-10T10:00:00", "timeZone": "America/New_York"},
                    "end": {"dateTime": "2026-03-10T10:30:00", "timeZone": "America/New_York"},
                    "isAllDay": False,
                    "onlineMeetingUrl": "https://teams.microsoft.com/...",
                    "organizer": {"emailAddress": {}},
                    "attendees": [],
                    "location": {},
                    "isCancelled": False,
                    "bodyPreview": ""
                }
            ]
        }

        cal.cmd_list([])
        
        captured = capsys.readouterr()
        assert "🔗" in captured.out  # Link indicator


class TestCalInputValidation:
    """Tests for cal module input validation."""

    @patch("cal.graph_api.graph_post")
    def test_create_parses_date_formats(self, mock_post):
        """Test that various date formats are accepted."""
        mock_post.return_value = {
            "id": "event-123",
            "subject": "Test",
            "start": {"dateTime": ""},
            "end": {"dateTime": ""}
        }

        # Should succeed with standard format
        cal.cmd_create([
            "--subject", "Meeting",
            "--start", "2026-03-10T10:00",
            "--end", "2026-03-10T11:00"
        ])
        
        mock_post.assert_called_once()
