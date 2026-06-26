from __future__ import annotations

import json
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

from mal_updater.config import load_config
from mal_updater.crunchyroll_auth import (
    CrunchyrollAuthError,
    crunchyroll_login_with_credentials,
    load_crunchyroll_credentials,
    resolve_crunchyroll_state_paths,
)


class _FakeResponse:
    def __init__(self, status_code: int, payload: dict[str, object]) -> None:
        self.status_code = status_code
        self._payload = payload

    def json(self) -> dict[str, object]:
        return self._payload


class CrunchyrollAuthTests(unittest.TestCase):
    def test_load_crunchyroll_credentials_reads_secret_file_overrides(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True)
            (root / ".MAL-Updater" / "config" / "settings.toml").write_text(
                textwrap.dedent(
                    """
                    [secret_files]
                    crunchyroll_username = "../secrets/custom_username.txt"
                    crunchyroll_password = "../secrets/custom_password.txt"
                    """
                ),
                encoding="utf-8",
            )
            (root / ".MAL-Updater" / "secrets" / "custom_username.txt").write_text("user@example.com\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "custom_password.txt").write_text("hunter2\n", encoding="utf-8")

            credentials = load_crunchyroll_credentials(load_config(root))

            self.assertEqual(credentials.username, "user@example.com")
            self.assertEqual(credentials.password, "hunter2")
            self.assertEqual(credentials.username_path, (root / ".MAL-Updater" / "secrets" / "custom_username.txt").resolve())
            self.assertEqual(credentials.password_path, (root / ".MAL-Updater" / "secrets" / "custom_password.txt").resolve())

    def test_crunchyroll_login_with_credentials_persists_refresh_token_and_session_state(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True)
            (root / ".MAL-Updater" / "secrets" / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "crunchyroll_password.txt").write_text("pw-123\n", encoding="utf-8")
            config = load_config(root)

            with patch("mal_updater.crunchyroll_auth._http_post") as mock_post, patch(
                "mal_updater.crunchyroll_auth._http_get"
            ) as mock_get:
                mock_post.return_value = _FakeResponse(
                    200,
                    {
                        "access_token": "access-abc",
                        "refresh_token": "refresh-xyz",
                        "account_id": "acct-42",
                    },
                )
                mock_get.return_value = _FakeResponse(
                    200,
                    {
                        "account_id": "acct-42",
                        "email": "user@example.com",
                    },
                )

                result = crunchyroll_login_with_credentials(config)

            state_paths = resolve_crunchyroll_state_paths(config)
            self.assertEqual(state_paths.refresh_token_path.read_text(encoding="utf-8"), "refresh-xyz\n")
            self.assertEqual(state_paths.device_id_path.read_text(encoding="utf-8").strip(), result.device_id)
            session_payload = json.loads(state_paths.session_state_path.read_text(encoding="utf-8"))
            self.assertEqual(session_payload["crunchyroll_phase"], "ready")
            self.assertEqual(session_payload["last_account_id_hint"], "acct-42")
            self.assertIsNone(session_payload["last_error"])
            self.assertEqual(result.account_email, "user@example.com")

            request_body = mock_post.call_args.kwargs["data"]
            self.assertEqual(request_body["grant_type"], "password")
            self.assertEqual(request_body["scope"], "offline_access")
            self.assertEqual(request_body["device_type"], "ANDROIDTV")

    def test_crunchyroll_login_with_credentials_records_failure_state(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True)
            (root / ".MAL-Updater" / "secrets" / "crunchyroll_username.txt").write_text("user@example.com\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets" / "crunchyroll_password.txt").write_text("pw-123\n", encoding="utf-8")
            config = load_config(root)

            with patch("mal_updater.crunchyroll_auth._http_post") as mock_post:
                mock_post.return_value = _FakeResponse(
                    400,
                    {
                        "error": "invalid_grant",
                        "error_description": "bad credentials",
                    },
                )

                with self.assertRaises(CrunchyrollAuthError):
                    crunchyroll_login_with_credentials(config)

            state_paths = resolve_crunchyroll_state_paths(config)
            session_payload = json.loads(state_paths.session_state_path.read_text(encoding="utf-8"))
            self.assertEqual(session_payload["crunchyroll_phase"], "auth_failed")
            self.assertIn("invalid_grant", session_payload["last_error"])


if __name__ == "__main__":
    unittest.main()
