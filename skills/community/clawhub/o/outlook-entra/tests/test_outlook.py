"""Tests unitaires pour outlook_entra — skill Microsoft Outlook via OAuth Entra."""

import json
import os
import sys
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import pytest

# ── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture
def token_file_valid(tmp_path):
    """Fichier token temporaire avec expiration future (valide)."""
    f = tmp_path / "tokens.json"
    data = {
        "access_token":  "eyJhbGciOiJSUzI1NiJ9.fake_valid",
        "refresh_token": "0-AQB fake_refresh",
        "expires_in":    3600,
        "expires_at":    time.time() + 3600,
        "token_type":    "Bearer",
        "scope":         "Mail.Read Mail.Send",
    }
    f.write_text(json.dumps(data))
    return f

@pytest.fixture
def token_file_expired(tmp_path):
    """Fichier token expiré."""
    f = tmp_path / "tokens.json"
    data = {
        "access_token":  "eyJhbGciOiJSUzI1NiJ9.fake_expired",
        "refresh_token": "0-AQB fake_refresh",
        "expires_in":    3600,
        "expires_at":    time.time() - 600,
        "token_type":    "Bearer",
        "scope":         "Mail.Read Mail.Send",
    }
    f.write_text(json.dumps(data))
    return f

@pytest.fixture
def mock_env(monkeypatch):
    """Mock os.getenv avec variables de test (TOKEN_FILE à charge du testeur)."""
    env = {
        "AZURE_TENANT_ID":      "test-tenant-id",
        "AZURE_CLIENT_ID":      "test-client-id",
        "AZURE_CLIENT_SECRET":  "test-secret",
        "AZURE_REDIRECT_URI":   "http://localhost",
        "OAUTH_TOKEN_URL":      "https://login.microsoftonline.com/test-tenant-id/oauth2/v2.0/token",
        "OAUTH_DEVICE_CODE_URL":
            "https://login.microsoftonline.com/test-tenant-id/oauth2/v2.0/devicecode",
        "MS_GRAPH_BASE_URL":   "https://graph.microsoft.com/v1.0",
        "SCOPES":               "Mail.Read Mail.Send Calendars.Read Contacts.Read",
        "TOKEN_FILE_KEY":       "",
        "REQUEST_TIMEOUT":     "30",
    }
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    return env

# ── Tests outlook_token ─────────────────────────────────────────────────────────

def test_is_token_expired_valid(token_file_valid, mock_env):
    import outlook_token as ot
    ot.TOKEN_FILE = str(token_file_valid)
    ot.load_env = lambda: None
    token = ot.get_token()
    assert not ot.is_token_expired(token)
    assert ot.is_token_expired(token, margin_seconds=4000)

def test_is_token_expired_expired(token_file_expired, mock_env):
    import outlook_token as ot
    ot.TOKEN_FILE = str(token_file_expired)
    ot.load_env = lambda: None
    token = ot.get_token()
    assert ot.is_token_expired(token)

def test_get_token_ok(token_file_valid, mock_env):
    import outlook_token as ot
    ot.TOKEN_FILE = str(token_file_valid)
    ot.load_env = lambda: None
    token = ot.get_token()
    assert token is not None
    assert "access_token" in token
    assert token["access_token"] == "eyJhbGciOiJSUzI1NiJ9.fake_valid"

def test_get_token_missing():
    import outlook_token as ot
    ot.TOKEN_FILE = "/tmp/this_file_does_not_exist_12345.json"
    assert ot.get_token() is None

def test_save_and_retrieve_token(tmp_path, mock_env):
    import outlook_token as ot
    tf = tmp_path / "new_tokens.json"
    ot.TOKEN_FILE = str(tf)
    ot.load_env = lambda: None
    data = {
        "access_token":  "new_access",
        "refresh_token": "new_refresh",
        "expires_in":    7200,
        "expires_at":    time.time() + 7200,
    }
    ot.save_token(data)
    loaded = ot.get_token()
    assert loaded["access_token"] == "new_access"
    assert loaded["refresh_token"] == "new_refresh"

def test_ensure_valid_token_fresh(token_file_valid, mock_env):
    import outlook_token as ot
    ot.TOKEN_FILE = str(token_file_valid)
    ot.load_env = lambda: None
    mock_req = MagicMock()
    token = ot.ensure_valid_token(mock_req)
    assert token == "eyJhbGciOiJSUzI1NiJ9.fake_valid"
    mock_req.post.assert_not_called()

def test_ensure_valid_token_refresh(token_file_expired, mock_env):
    import outlook_token as ot
    ot.TOKEN_FILE = str(token_file_expired)
    ot.load_env = lambda: None
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "access_token":  "refreshed_access",
        "refresh_token": "refreshed_refresh",
        "expires_in":    3600,
    }
    mock_req = MagicMock()
    mock_req.post.return_value = mock_resp
    token = ot.ensure_valid_token(mock_req)
    assert token == "refreshed_access"
    mock_req.post.assert_called_once()

def test_ensure_valid_token_no_token(mock_env, monkeypatch):
    import outlook_token as ot
    ot.TOKEN_FILE = "/tmp/no_token_here_123.json"
    ot.load_env = lambda: None
    with pytest.raises(RuntimeError, match="Aucun token trouvé"):
        ot.ensure_valid_token(MagicMock())

# ── Tests outlook_graph helpers ────────────────────────────────────────────────

def test_handle_error_raises():
    from outlook_graph import _handle_error
    resp = MagicMock()
    resp.status_code = 401
    resp.json.return_value = {"error": {"message": "Token expired"}}
    with pytest.raises(RuntimeError, match="Graph API 401"):
        _handle_error(resp)

def test_fmt_message():
    from outlook_graph import fmt_message
    m = {
        "id": "abc123",
        "subject": "Test email",
        "from": {"emailAddress": {"name": "Alice", "address": "alice@example.com"}},
        "receivedDateTime": "2026-04-27T10:00:00Z",
        "isRead": False,
        "hasAttachments": True,
    }
    out = fmt_message(m)
    assert "Test email" in out
    assert "Alice" in out
    assert "abc123" in out

def test_fmt_event():
    from outlook_graph import fmt_event
    e = {
        "id": "evt1",
        "subject": "Réunion",
        "start": {"dateTime": "2026-04-27T14:00:00"},
        "end":   {"dateTime": "2026-04-27T15:00:00"},
        "location": {"displayName": "Salle 42"},
        "attendees": [{"emailAddress": {"address": "bob@example.com"}}],
    }
    out = fmt_event(e)
    assert "Réunion" in out
    assert "Salle 42" in out
    assert "evt1" in out

def test_fmt_contact():
    from outlook_graph import fmt_contact
    c = {
        "id": "c1",
        "givenName": "Jean",
        "surname": "Dupont",
        "emailAddresses": [{"address": "jean@example.com"}],
    }
    out = fmt_contact(c)
    assert "Jean" in out
    assert "jean@example.com" in out
