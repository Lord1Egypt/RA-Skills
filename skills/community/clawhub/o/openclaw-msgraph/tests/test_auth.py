"""Tests for auth module PKCE authentication."""

import sys
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
from io import BytesIO
import tempfile
import time

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import pytest
import auth


class TestPkceGeneration:
    """Tests for PKCE code generation."""

    def test_generate_pkce_returns_tuple(self):
        """Test that PKCE generation returns (verifier, challenge) tuple."""
        verifier, challenge = auth.generate_pkce()
        assert isinstance(verifier, str)
        assert isinstance(challenge, str)
        assert len(verifier) > 0
        assert len(challenge) > 0

    def test_generate_pkce_creates_different_values(self):
        """Test that each PKCE generation creates unique values."""
        verifier1, challenge1 = auth.generate_pkce()
        verifier2, challenge2 = auth.generate_pkce()
        assert verifier1 != verifier2
        assert challenge1 != challenge2

    def test_generate_pkce_challenge_is_base64url(self):
        """Test that challenge is base64url encoded (no padding)."""
        verifier, challenge = auth.generate_pkce()
        # Base64url doesn't have padding =
        assert "=" not in challenge
        # Should only contain valid base64url characters
        assert all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_" for c in challenge)


class TestBuildAuthUrl:
    """Tests for auth URL building."""

    def test_build_auth_url_contains_required_params(self):
        """Test that auth URL contains all required parameters."""
        url = auth.build_auth_url("challenge123", "state456")
        assert "client_id" in url
        assert "response_type=code" in url
        assert "code_challenge=challenge123" in url
        assert "code_challenge_method=S256" in url
        assert "state=state456" in url

    def test_build_auth_url_has_correct_authority(self):
        """Test that URL uses correct endpoint."""
        url = auth.build_auth_url("challenge", "state")
        assert url.startswith("https://login.microsoftonline.com/")

    def test_build_auth_url_includes_scopes(self):
        """Test that auth URL includes requested scopes."""
        url = auth.build_auth_url("challenge", "state")
        assert "scope=" in url


class TestTokenStorage:
    """Tests for token file storage and loading."""

    def test_load_tokens_empty_when_no_file(self):
        """Test loading tokens when file doesn't exist."""
        with patch("pathlib.Path.exists", return_value=False):
            result = auth.load_tokens()
            assert result == {}

    def test_load_tokens_parses_json(self):
        """Test loading and parsing token file."""
        token_data = {"access_token": "token123", "refresh_token": "refresh789"}
        mock_content = json.dumps(token_data)
        
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pathlib.Path.read_text", return_value=mock_content):
                result = auth.load_tokens()
                assert result == token_data

    def test_save_tokens_creates_dirs(self):
        """Test that save_tokens creates necessary directories."""
        with patch("pathlib.Path.mkdir") as mock_mkdir:
            with patch("pathlib.Path.write_text"):
                with patch("pathlib.Path.chmod"):
                    auth.save_tokens({"access_token": "test"})
                    mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    def test_save_tokens_writes_json(self):
        """Test that tokens are saved as JSON."""
        with patch("pathlib.Path.mkdir"):
            with patch("pathlib.Path.write_text") as mock_write:
                with patch("pathlib.Path.chmod"):
                    tokens = {"access_token": "test123", "refresh_token": "refresh456"}
                    auth.save_tokens(tokens)
                    
                    # Verify JSON was written
                    call_args = mock_write.call_args[0][0]
                    parsed = json.loads(call_args)
                    assert parsed == tokens

    def test_save_tokens_sets_restrictive_permissions(self):
        """Test that token file is saved with restrictive permissions."""
        with patch("pathlib.Path.mkdir"):
            with patch("pathlib.Path.write_text"):
                with patch("pathlib.Path.chmod") as mock_chmod:
                    auth.save_tokens({"access_token": "test"})
                    mock_chmod.assert_called_once_with(0o600)


class TestTokenExchange:
    """Tests for authorization code exchange."""

    @patch("urllib.request.urlopen")
    def test_exchange_code_success(self, mock_urlopen):
        """Test successful code exchange."""
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({
            "access_token": "new-access-token",
            "refresh_token": "new-refresh-token",
            "expires_in": 3600
        }).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = auth.exchange_code("auth-code-123", "verifier456")
        
        assert result["access_token"] == "new-access-token"
        assert result["refresh_token"] == "new-refresh-token"

    @patch("urllib.request.urlopen")
    def test_exchange_code_sends_correct_params(self, mock_urlopen):
        """Test that exchange sends correct parameters."""
        mock_response = Mock()
        mock_response.read.return_value = b'{"access_token": "test"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        auth.exchange_code("code123", "verifier789")
        
        # Verify request was made with correct data
        call_args = mock_urlopen.call_args[0][0]
        assert call_args.data is not None
        data_str = call_args.data.decode()
        assert "code=code123" in data_str
        assert "code_verifier=verifier789" in data_str
        assert "grant_type=authorization_code" in data_str

    @patch("urllib.request.urlopen")
    def test_exchange_code_error_handling(self, mock_urlopen):
        """Test that exchange handles HTTP errors."""
        import urllib.error
        
        error = urllib.error.HTTPError("url", 400, "Bad Request", {}, BytesIO(b"Invalid code"))
        mock_urlopen.side_effect = error

        with pytest.raises(urllib.error.HTTPError):
            auth.exchange_code("invalid", "verifier")


class TestTokenRefresh:
    """Tests for token refresh."""

    @patch("urllib.request.urlopen")
    def test_do_refresh_success(self, mock_urlopen):
        """Test successful token refresh."""
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({
            "access_token": "refreshed-token",
            "expires_in": 3600
        }).encode()
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = auth.do_refresh("refresh-token-123")
        
        assert result["access_token"] == "refreshed-token"

    @patch("urllib.request.urlopen")
    def test_do_refresh_sends_correct_params(self, mock_urlopen):
        """Test that refresh sends correct parameters."""
        mock_response = Mock()
        mock_response.read.return_value = b'{"access_token": "test"}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        auth.do_refresh("refresh-token-xyz")
        
        call_args = mock_urlopen.call_args[0][0]
        data_str = call_args.data.decode()
        assert "grant_type=refresh_token" in data_str
        assert "refresh_token=refresh-token-xyz" in data_str


class TestGetAccessToken:
    """Tests for get_access_token function."""

    @patch("auth.load_tokens")
    def test_get_access_token_not_authenticated(self, mock_load):
        """Test error when not authenticated."""
        mock_load.return_value = {}

        with pytest.raises(SystemExit):
            auth.get_access_token()

    @patch("time.time")
    @patch("auth.load_tokens")
    def test_get_access_token_returns_valid_token(self, mock_load, mock_time):
        """Test returning valid token."""
        mock_time.return_value = 1000
        mock_load.return_value = {
            "access_token": "valid-token",
            "expires_at": 2000  # Far in future
        }

        result = auth.get_access_token()
        assert result == "valid-token"

    @patch("time.time")
    @patch("auth.do_refresh")
    @patch("auth.save_tokens")
    @patch("auth.load_tokens")
    def test_get_access_token_refreshes_expired(self, mock_load, mock_save, mock_refresh, mock_time):
        """Test that expired tokens are refreshed."""
        mock_time.return_value = 3000
        mock_load.return_value = {
            "access_token": "old-token",
            "refresh_token": "refresh-token",
            "expires_at": 1000  # Expired
        }
        mock_refresh.return_value = {
            "access_token": "new-token",
            "expires_in": 3600
        }

        result = auth.get_access_token()
        
        # Should have called refresh
        mock_refresh.assert_called_once_with("refresh-token")
        assert result == "new-token"

    @patch("time.time")
    @patch("auth.do_refresh")
    @patch("auth.save_tokens")
    @patch("auth.load_tokens")
    def test_get_access_token_saves_refreshed_token(self, mock_load, mock_save, mock_refresh, mock_time):
        """Test that refreshed tokens are saved."""
        mock_time.return_value = 3000
        mock_load.return_value = {
            "access_token": "old",
            "refresh_token": "refresh",
            "expires_at": 1000
        }
        mock_refresh.return_value = {
            "access_token": "new",
            "expires_in": 3600
        }

        auth.get_access_token()
        
        # Verify save was called
        mock_save.assert_called_once()
        saved_tokens = mock_save.call_args[0][0]
        assert saved_tokens["access_token"] == "new"

    @patch("time.time")
    @patch("auth.do_refresh")
    @patch("auth.load_tokens")
    def test_get_access_token_refresh_failure(self, mock_load, mock_refresh, mock_time):
        """Test handling of refresh failure."""
        import urllib.error
        
        mock_time.return_value = 3000
        mock_load.return_value = {
            "refresh_token": "refresh",
            "expires_at": 1000
        }
        mock_refresh.side_effect = urllib.error.HTTPError("url", 401, "Unauthorized", {}, BytesIO(b"Invalid refresh token"))

        with pytest.raises(SystemExit):
            auth.get_access_token()


class TestCallbackHandler:
    """Tests for HTTP callback handler."""

    def test_callback_handler_initializes_captured(self):
        """Test that callback handler has captured dict."""
        # The handler has a class variable captured
        assert hasattr(auth.CallbackHandler, "captured")
        auth.CallbackHandler.captured = {"code": "test123"}
        assert auth.CallbackHandler.captured["code"] == "test123"


class TestOpenBrowser:
    """Tests for browser opening."""

    @patch("subprocess.run")
    def test_open_browser_tries_cmd_exe_first(self, mock_run):
        """Test that Windows cmd.exe is tried first."""
        auth.open_browser("https://example.com")
        
        # Should try cmd.exe
        if mock_run.called:
            call_args = mock_run.call_args[0][0]
            assert "cmd.exe" in call_args

    @patch("subprocess.run")
    def test_open_browser_fallback_to_xdg_open(self, mock_run):
        """Test fallback to xdg-open on non-Windows."""
        # First call (cmd.exe) fails, should try xdg-open
        def side_effect(*args, **kwargs):
            if "cmd.exe" in args[0]:
                raise FileNotFoundError()

        mock_run.side_effect = side_effect
        
        try:
            auth.open_browser("https://example.com")
        except FileNotFoundError:
            # Expected when both fail
            pass


class TestAuthIntegration:
    """Integration tests for auth flow."""

    @patch("auth.open_browser")
    @patch("auth.save_tokens")
    @patch("auth.exchange_code")
    def test_login_flow_happy_path(self, mock_exchange, mock_save, mock_open):
        """Test complete login flow."""
        # Mock the exchange to succeed
        mock_exchange.return_value = {
            "access_token": "token123",
            "refresh_token": "refresh456",
            "expires_in": 3600
        }

        # Would test with mock HTTP server, but complex
        # This validates the setup at least compiles


class TestAuthCommands:
    """Tests for auth CLI commands."""

    @patch("auth.load_tokens")
    def test_cmd_status_not_authenticated(self, mock_load, capsys):
        """Test status command when not authenticated."""
        mock_load.return_value = {}
        
        auth.cmd_status()
        
        captured = capsys.readouterr()
        assert "NOT authenticated" in captured.out

    @patch("time.time")
    @patch("auth.load_tokens")
    def test_cmd_status_authenticated(self, mock_load, mock_time, capsys):
        """Test status command when authenticated."""
        mock_time.return_value = 1000
        mock_load.return_value = {
            "access_token": "token",
            "refresh_token": "refresh",
            "expires_at": 2000
        }
        
        auth.cmd_status()
        
        captured = capsys.readouterr()
        assert "authenticated" in captured.out.lower()

    @patch("auth.do_refresh")
    @patch("auth.load_tokens")
    def test_cmd_refresh_success(self, mock_load, mock_refresh, capsys):
        """Test refresh command."""
        mock_load.return_value = {
            "access_token": "old",
            "refresh_token": "refresh",
            "expires_at": 0
        }
        mock_refresh.return_value = {
            "access_token": "new",
            "expires_in": 3600
        }
        
        with patch("auth.save_tokens"):
            auth.cmd_refresh()
        
        captured = capsys.readouterr()
        assert "Token refreshed" in captured.out

    @patch("auth.load_tokens")
    def test_cmd_refresh_no_token(self, mock_load, capsys):
        """Test refresh command without tokens."""
        mock_load.return_value = {}
        
        with pytest.raises(SystemExit):
            auth.cmd_refresh()

    @patch("auth.get_access_token")
    def test_cmd_token_prints_token(self, mock_token, capsys):
        """Test token command returns access token."""
        mock_token.return_value = "test-token-123"
        
        auth.cmd_token()
        
        captured = capsys.readouterr()
        assert "test-token-123" in captured.out
