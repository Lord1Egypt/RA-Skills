"""Tests for mail module commands."""

import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import pytest
import mail


class TestResolveFolderId:
    """Tests for resolve_folder_id function."""

    def test_resolve_well_known_folder_inbox(self):
        """Test resolving well-known inbox folder."""
        result = mail.resolve_folder_id("inbox")
        assert result == "inbox"

    def test_resolve_well_known_folder_drafts(self):
        """Test resolving well-known drafts folder."""
        result = mail.resolve_folder_id("drafts")
        assert result == "drafts"

    def test_resolve_well_known_folder_case_insensitive(self):
        """Test well-known folder names are case-insensitive."""
        result = mail.resolve_folder_id("ARCHIVE")
        assert result == "archive"

    def test_resolve_well_known_folder_ignores_spaces(self):
        """Test spaces are ignored in well-known folder names."""
        result = mail.resolve_folder_id("deleted items")
        assert result == "deleteditems"

    def test_resolve_long_string_as_id(self):
        """Test that long strings are returned as-is (assumes they're IDs)."""
        long_id = "a" * 60
        result = mail.resolve_folder_id(long_id)
        assert result == long_id


class TestCmdInbox:
    """Tests for cmd_inbox command."""

    @patch("mail.graph_api.graph_get")
    def test_cmd_inbox_default_params(self, mock_get, capsys):
        """Test inbox command with default parameters."""
        mock_get.return_value = {
            "value": [
                {
                    "id": "msg-1",
                    "subject": "Test Email",
                    "from": {"emailAddress": {"name": "Sender", "address": "sender@example.com"}},
                    "receivedDateTime": "2026-03-03T10:30:00Z",
                    "isRead": False,
                    "hasAttachments": False,
                    "bodyPreview": "Test preview"
                }
            ]
        }

        mail.cmd_inbox([])
        
        captured = capsys.readouterr()
        assert "INBOX" in captured.out
        assert "Test Email" in captured.out
        assert "sender@example.com" in captured.out

    @patch("mail.graph_api.graph_get")
    def test_cmd_inbox_empty(self, mock_get, capsys):
        """Test inbox command with no messages."""
        mock_get.return_value = {"value": []}

        mail.cmd_inbox([])
        
        captured = capsys.readouterr()
        assert "No messages found" in captured.out

    @patch("mail.graph_api.graph_get")
    def test_cmd_inbox_with_count_param(self, mock_get, capsys):
        """Test inbox command with custom count."""
        mock_get.return_value = {"value": []}

        mail.cmd_inbox(["--count", "50"])
        
        # Check that the param was passed to graph_get
        call_args = mock_get.call_args
        params = call_args[0][1]
        assert params["$top"] == "50"

    @patch("mail.graph_api.graph_get")
    def test_cmd_inbox_with_folder(self, mock_get, capsys):
        """Test inbox command with custom folder."""
        mock_get.return_value = {"value": []}

        mail.cmd_inbox(["--folder", "sentitems"])
        
        # Check that correct folder path was used
        call_args = mock_get.call_args[0][0]
        assert "sentitems" in call_args


class TestCmdRead:
    """Tests for cmd_read command."""

    @patch("mail.graph_api.graph_patch")
    @patch("mail.graph_api.graph_get")
    def test_cmd_read_success(self, mock_get, mock_patch, capsys):
        """Test reading a message."""
        mock_get.return_value = {
            "id": "msg-123",
            "subject": "Important Email",
            "from": {"emailAddress": {"name": "John", "address": "john@example.com"}},
            "toRecipients": [
                {"emailAddress": {"name": "You", "address": "you@example.com"}}
            ],
            "receivedDateTime": "2026-03-03T10:30:00Z",
            "body": {
                "contentType": "text",
                "content": "Email body text"
            },
            "hasAttachments": False,
            "isRead": False
        }

        mail.cmd_read(["msg-123"])
        
        # Verify message was marked as read
        mock_patch.assert_called_once_with("/me/messages/msg-123", {"isRead": True})
        
        captured = capsys.readouterr()
        assert "Important Email" in captured.out
        assert "john@example.com" in captured.out

    @patch("mail.graph_api.graph_get")
    def test_cmd_read_no_id(self, mock_get, capsys):
        """Test read command without message ID fails."""
        with pytest.raises(SystemExit):
            mail.cmd_read([])


class TestCmdMove:
    """Tests for cmd_move command."""

    @patch("mail.graph_api.graph_post")
    def test_cmd_move_success(self, mock_post, capsys):
        """Test moving a message to a folder."""
        mock_post.return_value = {"id": "msg-123-new"}

        mail.cmd_move(["msg-123", "archive"])
        
        captured = capsys.readouterr()
        assert "moved" in captured.out.lower()
        assert "archive" in captured.out.lower()

    @patch("mail.graph_api.graph_post")
    def test_cmd_move_insufficient_args(self, mock_post):
        """Test move command without all required args."""
        with pytest.raises(SystemExit):
            mail.cmd_move(["msg-123"])


class TestGetFoldersRecursive:
    """Tests for get_folders_recursive function."""

    @patch("mail.graph_api.graph_get")
    def test_get_folders_recursive_single_level(self, mock_get, capsys):
        """Test getting folders one level deep."""
        # First call returns root, second returns empty (no children)
        mock_get.side_effect = [
            {
                "value": [
                    {
                        "id": "folder-1",
                        "displayName": "Inbox",
                        "totalItemCount": 42,
                        "unreadItemCount": 5
                    }
                ]
            },
            {"value": []}  # No children
        ]

        mail.get_folders_recursive()
        captured = capsys.readouterr()
        assert "Inbox" in captured.out


class TestCmdFolders:
    """Tests for cmd_folders command."""

    @patch("mail.get_folders_recursive")
    def test_cmd_folders_calls_helper(self, mock_recursive, capsys):
        """Test that cmd_folders calls get_folders_recursive."""
        mail.cmd_folders([])
        
        mock_recursive.assert_called_once()
        captured = capsys.readouterr()
        assert "MAIL FOLDERS" in captured.out


class TestCmdSearch:
    """Tests for cmd_search command."""

    @patch("mail.graph_api.graph_get")
    def test_cmd_search_with_results(self, mock_get, capsys):
        """Test searching for messages with results."""
        mock_get.return_value = {
            "value": [
                {
                    "id": "msg-1",
                    "subject": "Project Update",
                    "from": {"emailAddress": {"name": "Boss", "address": "boss@example.com"}},
                    "receivedDateTime": "2026-03-03T10:30:00Z",
                    "isRead": True,
                    "bodyPreview": "Project is on track"
                }
            ]
        }

        mail.cmd_search(["project"])
        
        captured = capsys.readouterr()
        assert "Search results" in captured.out
        assert "project" in captured.out.lower()
        assert "Project Update" in captured.out

    @patch("mail.graph_api.graph_get")
    def test_cmd_search_no_results(self, mock_get, capsys):
        """Test searching with no results."""
        mock_get.return_value = {"value": []}

        mail.cmd_search(["nonexistent"])
        
        captured = capsys.readouterr()
        assert "No results" in captured.out

    def test_cmd_search_no_query(self):
        """Test search command without query."""
        with pytest.raises(SystemExit):
            mail.cmd_search([])


class TestMailIntegration:
    """Integration tests for mail module."""

    @patch("mail.graph_api.graph_get")
    def test_folder_resolution_with_recursive_search(self, mock_get):
        """Test folder resolution with recursive folder structure."""
        # First call returns child folders, second call returns matching folder
        mock_get.side_effect = [
            {
                "value": [
                    {"id": "folder-child-1", "displayName": "Projects"},
                    {"id": "folder-child-2", "displayName": "Work"}
                ]
            },
            {
                "value": [
                    {"id": "folder-sub-1", "displayName": "MyProject"}
                ]
            }
        ]

        # Would need to test actual recursive behavior
        # This is a basic integration test structure

    @patch("mail.graph_api.graph_get")
    def test_inbox_displays_unread_indicator(self, mock_get, capsys):
        """Test that inbox shows unread indicator."""
        mock_get.return_value = {
            "value": [
                {
                    "id": "msg-1",
                    "subject": "Unread Email",
                    "from": {"emailAddress": {"name": "Sender", "address": "s@example.com"}},
                    "receivedDateTime": "2026-03-03T10:30:00Z",
                    "isRead": False,
                    "hasAttachments": False,
                    "bodyPreview": ""
                }
            ]
        }

        mail.cmd_inbox([])
        
        captured = capsys.readouterr()
        assert "●" in captured.out  # Unread indicator


class TestMailInputValidation:
    """Tests for mail module input validation."""

    @patch("mail._find_folder_recursive")
    def test_resolve_folder_handles_empty_string(self, mock_recursive):
        """Test that empty folder name calls recursive search."""
        mock_recursive.return_value = None
        result = mail.resolve_folder_id("")
        # Should have attempted recursive search
        mock_recursive.assert_called_once_with("")

    @patch("mail.graph_api.graph_post")
    def test_cmd_move_to_existing_folder(self, mock_post, capsys):
        """Test moving message to an existing folder."""
        mock_post.return_value = {}
        
        mail.cmd_move(["msg-123", "inbox"])
        
        captured = capsys.readouterr()
        assert "moved" in captured.out.lower()

    @patch("mail.graph_api.graph_patch")
    @patch("mail.graph_api.graph_get")
    def test_cmd_read_with_html_content(self, mock_get, mock_patch, capsys):
        """Test reading message with HTML content."""
        mock_get.return_value = {
            "subject": "HTML Message",
            "from": {"emailAddress": {"name": "Sender", "address": "test@example.com"}},
            "receivedDateTime": "2026-03-03T10:00:00Z",
            "body": {
                "contentType": "html",
                "content": "<html><body><p>Test message</p></body></html>"
            },
            "isRead": False
        }
        mock_patch.return_value = {}

        mail.cmd_read(["msg-123"])
        
        captured = capsys.readouterr()
        assert "Test message" in captured.out
        assert "<html>" not in captured.out

    @patch("mail.graph_api.graph_patch")
    @patch("mail.graph_api.graph_get")
    def test_cmd_read_marks_as_read(self, mock_get, mock_patch, capsys):
        """Test that reading a message marks it as read."""
        mock_get.return_value = {
            "subject": "Test",
            "from": {"emailAddress": {"name": "Sender", "address": "s@example.com"}},
            "receivedDateTime": "2026-03-03T10:00:00Z",
            "body": {"contentType": "text", "content": "Test"},
            "isRead": False
        }
        mock_patch.return_value = {}

        mail.cmd_read(["msg-123"])
        
        # Verify PATCH was called to mark as read
        assert mock_patch.called
        call_args = mock_patch.call_args
        payload = call_args[0][1]
        assert payload.get("isRead") == True

    @patch("mail.auth.get_access_token")
    @patch("mail._find_folder_recursive")
    @patch("mail.graph_api.graph_post")
    def test_cmd_move_simple_case(self, mock_post, mock_find, mock_token):
        """Test moving message to inbox folder."""
        mock_token.return_value = "fake-token"
        mock_find.return_value = "inbox"
        mock_post.return_value = {}

        mail.cmd_move(["msg-123", "inbox"])
        
        # Verify POST was called
        assert mock_post.called

    @patch("mail.auth.get_access_token")
    @patch("mail.graph_api.graph_patch")
    @patch("mail.graph_api.graph_get")
    def test_cmd_read_plain_text_message(self, mock_get, mock_patch, mock_token, capsys):
        """Test reading a plain text message."""
        mock_token.return_value = "fake-token"
        mock_get.return_value = {
            "subject": "Text Message",
            "from": {"emailAddress": {"name": "Sender", "address": "s@example.com"}},
            "receivedDateTime": "2026-03-03T10:00:00Z",
            "body": {"contentType": "text", "content": "Simple plain text message"},
            "isRead": True
        }
        mock_patch.return_value = {}
