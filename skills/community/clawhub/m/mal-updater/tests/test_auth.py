from __future__ import annotations

import stat
import tempfile
import threading
import time
import unittest
from pathlib import Path
from urllib.request import urlopen

from mal_updater.auth import OAuthCallbackError, persist_token_response, wait_for_oauth_callback, write_secret_file
from mal_updater.config import MalSecrets
from mal_updater.mal_client import TokenResponse


class AuthHelpersTests(unittest.TestCase):
    def test_wait_for_oauth_callback_captures_code_and_state(self) -> None:
        results: dict[str, object] = {}

        def runner() -> None:
            results["callback"] = wait_for_oauth_callback("127.0.0.1", 8876, expected_state="abc123", timeout_seconds=2.0)

        thread = threading.Thread(target=runner)
        thread.start()
        time.sleep(0.2)
        with urlopen("http://127.0.0.1:8876/callback?code=hello&state=abc123") as response:
            body = response.read().decode("utf-8")
        thread.join(timeout=2.0)

        callback = results["callback"]
        self.assertIn("MAL auth complete", body)
        self.assertEqual(callback.code, "hello")
        self.assertEqual(callback.state, "abc123")

    def test_wait_for_oauth_callback_rejects_state_mismatch(self) -> None:
        results: dict[str, object] = {}

        def runner() -> None:
            try:
                wait_for_oauth_callback("127.0.0.1", 8877, expected_state="good", timeout_seconds=2.0)
            except Exception as exc:  # pragma: no cover - exercised by assertion below
                results["error"] = exc

        thread = threading.Thread(target=runner)
        thread.start()
        time.sleep(0.2)
        with self.assertRaises(Exception):
            urlopen("http://127.0.0.1:8877/callback?code=hello&state=bad")
        thread.join(timeout=2.0)

        self.assertIsInstance(results.get("error"), OAuthCallbackError)
        self.assertIn("state mismatch", str(results["error"]).lower())

    def test_write_secret_file_uses_private_permissions(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "secret.txt"
            write_secret_file(path, " value-with-space \n")
            self.assertEqual(path.read_text(encoding="utf-8"), "value-with-space\n")
            mode = stat.S_IMODE(path.stat().st_mode)
            self.assertEqual(mode, 0o600)

    def test_persist_token_response_writes_expected_files(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            secrets = MalSecrets(
                client_id=None,
                client_secret=None,
                access_token=None,
                refresh_token=None,
                client_id_path=root / "mal_client_id.txt",
                client_secret_path=root / "mal_client_secret.txt",
                access_token_path=root / "mal_access_token.txt",
                refresh_token_path=root / "mal_refresh_token.txt",
            )
            token = TokenResponse(
                access_token="access-123",
                token_type="Bearer",
                expires_in=3600,
                refresh_token="refresh-456",
                scope=None,
                raw={"access_token": "access-123", "refresh_token": "refresh-456"},
            )

            persist_token_response(token, secrets)

            self.assertEqual(secrets.access_token_path.read_text(encoding="utf-8"), "access-123\n")
            self.assertEqual(secrets.refresh_token_path.read_text(encoding="utf-8"), "refresh-456\n")


if __name__ == "__main__":
    unittest.main()
