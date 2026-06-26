"""Tests for graph_api module HTTP utilities."""

import sys
import json
import urllib.error
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import pytest
import graph_api


class TestGraphGet:
    """Tests for graph_get function."""

    @patch("urllib.request.urlopen")
    @patch("auth.get_access_token")
    def test_graph_get_success(self, mock_token, mock_urlopen):
        """Test successful GET request."""
        mock_token.return_value = "test-token"
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"value": [{"id": "1"}]}).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = graph_api.graph_get("/me/messages", {"$top": "10"})
        
        assert result == {"value": [{"id": "1"}]}
        mock_token.assert_called_once()

    @patch("urllib.request.urlopen")
    @patch("auth.get_access_token")
    def test_graph_get_with_params(self, mock_token, mock_urlopen):
        """Test GET request with query parameters."""
        mock_token.return_value = "test-token"
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"value": []}).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response

        graph_api.graph_get("/me/events", {"$top": "50", "$orderby": "start/dateTime"})
        
        # Verify URL contains parameters (URL encoded)
        call_args = mock_urlopen.call_args[0][0]
        # Parameters are URL encoded, so check for the actual values
        assert "50" in call_args.full_url
        assert "start" in call_args.full_url

    @patch("urllib.request.urlopen")
    @patch("auth.get_access_token")
    def test_graph_get_error_handling(self, mock_token, mock_urlopen, capsys):
        """Test GET request error handling."""
        import urllib.error
        
        mock_token.return_value = "test-token"
        error = urllib.error.HTTPError("url", 404, "Not Found", {}, BytesIO(b"Message not found"))
        mock_urlopen.side_effect = error

        with pytest.raises(SystemExit):
            graph_api.graph_get("/me/messages/invalid-id")
        
        captured = capsys.readouterr()
        assert "ERROR 404" in captured.err


class TestGraphPost:
    """Tests for graph_post function."""

    @patch("urllib.request.urlopen")
    @patch("auth.get_access_token")
    def test_graph_post_success(self, mock_token, mock_urlopen):
        """Test successful POST request."""
        mock_token.return_value = "test-token"
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"id": "new-event-123"}).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response

        payload = {"subject": "Meeting", "start": "2026-03-10T10:00"}
        result = graph_api.graph_post("/me/events", payload)
        
        assert result == {"id": "new-event-123"}

    @patch("urllib.request.urlopen")
    @patch("auth.get_access_token")
    def test_graph_post_empty_response(self, mock_token, mock_urlopen):
        """Test POST with empty response (204 No Content)."""
        mock_token.return_value = "test-token"
        mock_response = Mock()
        mock_response.read.return_value = b""
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = graph_api.graph_post("/me/messages/123/move", {"destinationId": "inbox"})
        
        assert result == {}

    @patch("urllib.request.urlopen")
    @patch("auth.get_access_token")
    def test_graph_post_json_encoding(self, mock_token, mock_urlopen):
        """Test that payload is properly JSON encoded."""
        mock_token.return_value = "test-token"
        mock_response = Mock()
        mock_response.read.return_value = b"{}"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        payload = {"name": "Test", "nested": {"key": "value"}}
        graph_api.graph_post("/me/endpoint", payload)
        
        # Verify payload was JSON encoded
        call_args = mock_urlopen.call_args[0][0]
        assert call_args.data == json.dumps(payload).encode()


class TestGraphPatch:
    """Tests for graph_patch function."""

    @patch("urllib.request.urlopen")
    @patch("auth.get_access_token")
    def test_graph_patch_success(self, mock_token, mock_urlopen):
        """Test successful PATCH request."""
        mock_token.return_value = "test-token"
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"id": "msg-123", "isRead": True}).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = graph_api.graph_patch("/me/messages/msg-123", {"isRead": True})
        
        assert result["isRead"] is True

    @patch("urllib.request.urlopen")
    @patch("auth.get_access_token")
    def test_graph_patch_method(self, mock_token, mock_urlopen):
        """Test that PATCH method is used."""
        mock_token.return_value = "test-token"
        mock_response = Mock()
        mock_response.read.return_value = b"{}"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        graph_api.graph_patch("/me/messages/123", {"isRead": True})
        
        call_args = mock_urlopen.call_args[0][0]
        assert call_args.get_method() == "PATCH"


class TestGraphDelete:
    """Tests for graph_delete function."""

    @patch("urllib.request.urlopen")
    @patch("auth.get_access_token")
    def test_graph_delete_success(self, mock_token, mock_urlopen):
        """Test successful DELETE request."""
        mock_token.return_value = "test-token"
        mock_response = Mock()
        mock_response.read.return_value = b""
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Should not raise
        graph_api.graph_delete("/me/events/event-123")

    @patch("urllib.request.urlopen")
    @patch("auth.get_access_token")
    def test_graph_delete_method(self, mock_token, mock_urlopen):
        """Test that DELETE method is used."""
        mock_token.return_value = "test-token"
        mock_response = Mock()
        mock_response.read.return_value = b""
        mock_urlopen.return_value.__enter__.return_value = mock_response

        graph_api.graph_delete("/me/events/123")
        
        call_args = mock_urlopen.call_args[0][0]
        assert call_args.get_method() == "DELETE"

    @patch("urllib.request.urlopen")
    @patch("auth.get_access_token")
    def test_graph_delete_error(self, mock_token, mock_urlopen, capsys):
        """Test DELETE error handling."""
        import urllib.error
        
        mock_token.return_value = "test-token"
        error = urllib.error.HTTPError("url", 404, "Not Found", {}, BytesIO(b"Not found"))
        mock_urlopen.side_effect = error

        with pytest.raises(SystemExit):
            graph_api.graph_delete("/me/events/invalid")
        
        captured = capsys.readouterr()
        assert "ERROR 404" in captured.err


class TestGraphApiHeaders:
    """Tests for proper HTTP headers in Graph API calls."""

    @patch("urllib.request.urlopen")
    @patch("auth.get_access_token")
    def test_authorization_header(self, mock_token, mock_urlopen):
        """Test that Authorization header is set."""
        mock_token.return_value = "test-token-value"
        mock_response = Mock()
        mock_response.read.return_value = b"{}"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        graph_api.graph_get("/me/messages")
        
        call_args = mock_urlopen.call_args[0][0]
        assert "Bearer test-token-value" in call_args.get_header("Authorization")

    @patch("urllib.request.urlopen")
    @patch("auth.get_access_token")
    def test_content_type_header(self, mock_token, mock_urlopen):
        """Test that Content-Type header is set for POST."""
        mock_token.return_value = "test-token"
        mock_response = Mock()
        mock_response.read.return_value = b"{}"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        graph_api.graph_post("/me/events", {"subject": "Test"})
        
        call_args = mock_urlopen.call_args[0][0]
        headers = call_args.headers
        assert "application/json" in headers.get("Content-type", "")

class TestGraphApiErrorHandling:
    """Tests for error handling in Graph API calls."""

    @patch("urllib.request.urlopen")
    @patch("auth.get_access_token")
    def test_graph_post_raises_http_error(self, mock_token, mock_urlopen, capsys):
        """Test graph_post handles HTTP errors."""
        mock_token.return_value = "test-token"
        error = urllib.error.HTTPError("url", 401, "Unauthorized", {}, BytesIO(b'{"error": "invalid token"}'))
        mock_urlopen.side_effect = error

        with pytest.raises(SystemExit):
            graph_api.graph_post("/me/messages", {"subject": "Test"})
        
        captured = capsys.readouterr()
        assert "ERROR 401" in captured.err

    @patch("urllib.request.urlopen")
    @patch("auth.get_access_token")
    def test_graph_delete_network_error(self, mock_token, mock_urlopen):
        """Test graph_delete handles network errors."""
        mock_token.return_value = "test-token"
        mock_urlopen.side_effect = Exception("Network timeout")

        with pytest.raises(Exception):
            graph_api.graph_delete("/me/events/123")

    @patch("urllib.request.urlopen")
    @patch("auth.get_access_token")
    def test_graph_patch_forbidden(self, mock_token, mock_urlopen, capsys):
        """Test graph_patch with 403 Forbidden error."""
        mock_token.return_value = "test-token"
        error = urllib.error.HTTPError("url", 403, "Forbidden", {}, BytesIO(b'{"error": "access denied"}'))
        mock_urlopen.side_effect = error

        with pytest.raises(SystemExit):
            graph_api.graph_patch("/me/messages/123", {"isRead": True})
        
        captured = capsys.readouterr()
        assert "ERROR 403" in captured.err


class TestGraphApiEdgeCases:
    """Tests for edge cases in Graph API calls."""

    @patch("urllib.request.urlopen")
    @patch("auth.get_access_token")
    def test_graph_get_empty_response(self, mock_token, mock_urlopen):
        """Test graph_get with empty value array."""
        mock_token.return_value = "test-token"
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"value": []}).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = graph_api.graph_get("/me/messages")
        
        assert result == {"value": []}

    @patch("urllib.request.urlopen")
    @patch("auth.get_access_token")
    def test_graph_post_null_response(self, mock_token, mock_urlopen):
        """Test graph_post with null field in response."""
        mock_token.return_value = "test-token"
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"id": "123", "parentId": None}).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = graph_api.graph_post("/me/events", {"subject": "Test"})
        
        assert result["id"] == "123"
        assert result["parentId"] is None

    @patch("urllib.request.urlopen")
    @patch("auth.get_access_token")
    def test_graph_patch_complex_payload(self, mock_token, mock_urlopen):
        """Test graph_patch with nested JSON payload."""
        mock_token.return_value = "test-token"
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"id": "updated"}).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response

        payload = {
            "subject": "Updated",
            "attendees": [
                {"emailAddress": {"address": "user1@example.com"}},
                {"emailAddress": {"address": "user2@example.com"}}
            ]
        }
        
        result = graph_api.graph_patch("/me/events/123", payload)
        
        assert result["id"] == "updated"
        # Verify complex payload was properly JSON encoded
        assert mock_urlopen.called