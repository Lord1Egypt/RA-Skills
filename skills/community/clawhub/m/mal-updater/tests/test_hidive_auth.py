from __future__ import annotations

import json
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

from mal_updater.config import load_config
from mal_updater.hidive_auth import (
    HIDIVE_REFRESH_WINDOW_SECONDS,
    HidiveAuthError,
    HidiveSession,
    HidiveStatePaths,
    HidiveTokenSet,
    _seconds_until_jwt_expiry,
    hidive_login_with_credentials,
    load_hidive_credentials,
    resolve_hidive_state_paths,
)


class _FakeResponse:
    def __init__(self, status_code: int, payload: dict[str, object]) -> None:
        self.status_code = status_code
        self._payload = payload
        self.text = json.dumps(payload)

    def json(self) -> dict[str, object]:
        return self._payload


class HidiveAuthTests(unittest.TestCase):
    def _build_session(self, root: Path) -> HidiveSession:
        config = load_config(root)
        state_paths = HidiveStatePaths(
            root=root / ".MAL-Updater" / "state" / "hidive" / "default",
            access_token_path=root / ".MAL-Updater" / "state" / "hidive" / "default" / "authorisation_token.txt",
            refresh_token_path=root / ".MAL-Updater" / "state" / "hidive" / "default" / "refresh_token.txt",
            session_state_path=root / ".MAL-Updater" / "state" / "hidive" / "default" / "session.json",
            sync_boundary_path=root / ".MAL-Updater" / "state" / "hidive" / "default" / "sync_boundary.json",
        )
        state_paths.root.mkdir(parents=True, exist_ok=True)
        return HidiveSession(
            config=config,
            profile="default",
            state_paths=state_paths,
            token=HidiveTokenSet(authorisation_token="access-token", refresh_token="refresh-token", account_id="acct-123"),
        )

    def test_load_hidive_credentials_reads_secret_file_overrides(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True)
            (root / ".MAL-Updater" / "config" / "settings.toml").write_text(
                textwrap.dedent(
                    """
                    [secret_files]
                    hidive_username = "../secrets/custom_hidive_username.txt"
                    hidive_password = "../secrets/custom_hidive_password.txt"
                    """
                ),
                encoding="utf-8",
            )
            (root / ".MAL-Updater" / "secrets" / "custom_hidive_username.txt").write_text("user@example.com\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "custom_hidive_password.txt").write_text("hunter2\n", encoding="utf-8")

            credentials = load_hidive_credentials(load_config(root))

            self.assertEqual(credentials.username, "user@example.com")
            self.assertEqual(credentials.password, "hunter2")

    def test_seconds_until_jwt_expiry_decodes_exp_claim(self) -> None:
        token = (
            "eyJhbGciOiJIUzI1NiJ9."
            "eyJleHAiOjE3NzQwNjkyMzYsInN1YiI6IjU3MjQ2MnxkY2UuaGlkaXZlIn0."
            "signature"
        )
        self.assertEqual(1774069236 - 1774068636, _seconds_until_jwt_expiry(token, now_epoch=1774068636))

    def test_hidive_login_with_credentials_persists_tokens_and_session_state(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True)
            (root / ".MAL-Updater" / "secrets" / "hidive_username.txt").write_text("user@example.com\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "hidive_password.txt").write_text("pw-123\n", encoding="utf-8")
            config = load_config(root)

            with patch("mal_updater.hidive_auth.requests.request") as mock_request:
                mock_request.side_effect = [
                    _FakeResponse(
                        200,
                        {
                            "authorisationToken": "access-abc",
                            "refreshToken": "refresh-xyz",
                            "missingInformationStatus": "NONE",
                        },
                    ),
                    _FakeResponse(
                        200,
                        {
                            "id": "acct-42",
                            "displayName": "example-user",
                        },
                    ),
                ]

                result = hidive_login_with_credentials(config)

            state_paths = resolve_hidive_state_paths(config)
            self.assertEqual(state_paths.access_token_path.read_text(encoding="utf-8"), "access-abc\n")
            self.assertEqual(state_paths.refresh_token_path.read_text(encoding="utf-8"), "refresh-xyz\n")
            session_payload = json.loads(state_paths.session_state_path.read_text(encoding="utf-8"))
            self.assertEqual(session_payload["hidive_phase"], "ready")
            self.assertEqual(session_payload["last_account_id_hint"], "acct-42")
            self.assertEqual(result.account_name, "example-user")

    def test_hidive_login_with_credentials_records_failure_state(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True)
            (root / ".MAL-Updater" / "secrets" / "hidive_username.txt").write_text("user@example.com\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "hidive_password.txt").write_text("pw-123\n", encoding="utf-8")
            config = load_config(root)

            with patch("mal_updater.hidive_auth.requests.request") as mock_request:
                mock_request.return_value = _FakeResponse(
                    401,
                    {
                        "status": 401,
                        "code": "UNAUTHORIZED",
                        "messages": ["bad credentials"],
                    },
                )
                with self.assertRaises(HidiveAuthError):
                    hidive_login_with_credentials(config)

            state_paths = resolve_hidive_state_paths(config)
            session_payload = json.loads(state_paths.session_state_path.read_text(encoding="utf-8"))
            self.assertEqual(session_payload["hidive_phase"], "auth_failed")
            self.assertIn("HTTP 401", session_payload["last_error"])

    def test_hidive_session_refreshes_proactively_when_near_expiry(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            session = self._build_session(Path(td))
            session.token.authorisation_token = (
                "eyJhbGciOiJIUzI1NiJ9."
                "eyJleHAiOjEwMCwic3ViIjoiNTcyNDYyfGRjZS5oaWRpdmUifQ."
                "signature"
            )
            with patch("mal_updater.hidive_auth._seconds_until_jwt_expiry", return_value=HIDIVE_REFRESH_WINDOW_SECONDS), patch.object(
                HidiveSession, "refresh_tokens"
            ) as refresh_mock:
                session.ensure_fresh_tokens()
            refresh_mock.assert_called_once()

    def test_hidive_session_retries_401_via_refresh(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            session = self._build_session(Path(td))
            calls = []

            def fake_request(config, method, path, *, headers, params=None, json_body=None, timeout_seconds=None):
                calls.append((method, path, json_body, headers.get("Authorization")))
                if len(calls) == 1:
                    raise HidiveAuthError("HIDIVE GET /content/home failed: HTTP 401: expired")
                if path == "/token/refresh":
                    return {"authorisationToken": "refreshed-access", "refreshToken": "refreshed-refresh"}
                return {"ok": True}

            with patch("mal_updater.hidive_auth._hidive_json_request", side_effect=fake_request):
                payload = session.json_get("/content/home")

            self.assertEqual(payload, {"ok": True})
            self.assertEqual(session.token.authorisation_token, "refreshed-access")
            self.assertEqual(session.token.refresh_token, "refreshed-refresh")
            self.assertEqual([item[1] for item in calls], ["/content/home", "/token/refresh", "/content/home"])

    def test_hidive_session_falls_back_to_credentials_after_refresh_failure(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            session = self._build_session(Path(td))
            calls = []

            def fake_request(config, method, path, *, headers, params=None, json_body=None, timeout_seconds=None):
                calls.append((method, path))
                if path == "/content/home" and len(calls) == 1:
                    raise HidiveAuthError("HIDIVE GET /content/home failed: HTTP 401: expired")
                if path == "/token/refresh":
                    raise HidiveAuthError("refresh blocked")
                return {"ok": True}

            with patch("mal_updater.hidive_auth._hidive_json_request", side_effect=fake_request), patch(
                "mal_updater.hidive_auth.hidive_login_with_credentials"
            ) as mock_login:
                mock_login.return_value = type("Bootstrap", (), {
                    "authorisation_token": "credential-access",
                    "refresh_token": "credential-refresh",
                    "account_id": "acct-123",
                    "account_name": "example-user",
                })()
                payload = session.json_get("/content/home")

            self.assertEqual(payload, {"ok": True})
            self.assertEqual(session.token.authorisation_token, "credential-access")
            self.assertEqual(session.token.refresh_token, "credential-refresh")
            self.assertTrue(session.credential_rebootstrap_attempted)


if __name__ == "__main__":
    unittest.main()
