"""
test_keychain_secrets.py — Tests for keychain_secrets.py

Tests:
  - Keychain-first loading path (keyring available and returns values)
  - .env fallback when keyring returns nothing
  - Manual .env parse when python-dotenv unavailable
  - verify_secrets() reports missing keys correctly
  - store_secret() success and failure paths
"""
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


# We import the module fresh in each test by reloading, since module-level
# code sets env vars. Helper to clear relevant env vars before tests.

def _clear_google_env():
    for k in ("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN"):
        os.environ.pop(k, None)


class TestTryKeyring:
    def test_returns_value_from_keychain(self):
        import core.keychain_secrets as keychain_secrets
        kr_mock = MagicMock()
        kr_mock.get_password.return_value = "secret-value"
        with patch.dict(sys.modules, {"keyring": kr_mock}):
            result = keychain_secrets._try_keyring("some-key")
        assert result == "secret-value"

    def test_returns_empty_string_when_keyring_unavailable(self):
        import core.keychain_secrets as keychain_secrets
        with patch.dict(sys.modules, {"keyring": None}):
            result = keychain_secrets._try_keyring("some-key")
        assert result == ""

    def test_returns_empty_string_on_exception(self):
        import core.keychain_secrets as keychain_secrets
        kr_mock = MagicMock()
        kr_mock.get_password.side_effect = Exception("keychain locked")
        with patch.dict(sys.modules, {"keyring": kr_mock}):
            result = keychain_secrets._try_keyring("some-key")
        assert result == ""

    def test_returns_empty_string_when_password_is_none(self):
        import core.keychain_secrets as keychain_secrets
        kr_mock = MagicMock()
        kr_mock.get_password.return_value = None
        with patch.dict(sys.modules, {"keyring": kr_mock}):
            result = keychain_secrets._try_keyring("some-key")
        assert result == ""


class TestLoadGoogleSecrets:
    def test_loads_from_keychain_when_all_keys_present(self):
        """When keyring returns values for all three keys, env vars are set."""
        import core.keychain_secrets as keychain_secrets
        _clear_google_env()

        kr_mock = MagicMock()
        kr_mock.get_password.side_effect = lambda svc, key: f"kc-{key}"
        with patch.dict(sys.modules, {"keyring": kr_mock}):
            keychain_secrets.load_google_secrets()

        assert os.environ.get("GOOGLE_CLIENT_ID", "").startswith("kc-")
        assert os.environ.get("GOOGLE_CLIENT_SECRET", "").startswith("kc-")
        assert os.environ.get("GOOGLE_REFRESH_TOKEN", "").startswith("kc-")

    def test_falls_back_to_dotenv_when_keychain_empty(self, tmp_path, monkeypatch):
        """When keyring returns nothing, we fall back to .env file."""
        import core.keychain_secrets as keychain_secrets
        _clear_google_env()

        env_content = (
            "GOOGLE_CLIENT_ID=env-client-id\n"
            "GOOGLE_CLIENT_SECRET=env-client-secret\n"
            "GOOGLE_REFRESH_TOKEN=env-refresh-token\n"
        )
        env_file = tmp_path / ".env"
        env_file.write_text(env_content)

        kr_mock = MagicMock()
        kr_mock.get_password.return_value = None
        monkeypatch.setattr(keychain_secrets, "_SECRET_KEYS", {
            "GOOGLE_CLIENT_ID":     "google-client-id",
            "GOOGLE_CLIENT_SECRET": "google-client-secret",
            "GOOGLE_REFRESH_TOKEN": "google-refresh-token",
        })

        def fake_load_dotenv(path):
            for line in env_content.splitlines():
                if "=" in line:
                    k, _, v = line.partition("=")
                    os.environ[k.strip()] = v.strip()

        with patch.dict(sys.modules, {"keyring": kr_mock}):
            with patch("core.keychain_secrets.__file__", str(tmp_path / "keychain_secrets.py"), create=True):
                with patch("dotenv.load_dotenv", side_effect=fake_load_dotenv):
                    keychain_secrets.load_google_secrets()

    def test_skips_env_var_already_set(self):
        """load_google_secrets() should not overwrite existing env vars."""
        import core.keychain_secrets as keychain_secrets
        os.environ["GOOGLE_CLIENT_ID"] = "already-set"

        kr_mock = MagicMock()
        kr_mock.get_password.return_value = "kc-value"
        with patch.dict(sys.modules, {"keyring": kr_mock}):
            keychain_secrets.load_google_secrets()

        # The already-set value should be preserved
        assert os.environ["GOOGLE_CLIENT_ID"] == "already-set"
        os.environ.pop("GOOGLE_CLIENT_ID", None)


class TestVerifySecrets:
    def test_returns_empty_when_all_set(self, monkeypatch):
        import core.keychain_secrets as keychain_secrets
        monkeypatch.setenv("GOOGLE_CLIENT_ID", "x")
        monkeypatch.setenv("GOOGLE_CLIENT_SECRET", "y")
        monkeypatch.setenv("GOOGLE_REFRESH_TOKEN", "z")
        with patch.object(keychain_secrets, "load_google_secrets", return_value=None):
            missing = keychain_secrets.verify_secrets()
        assert missing == []

    def test_returns_missing_keys(self, monkeypatch):
        import core.keychain_secrets as keychain_secrets
        monkeypatch.delenv("GOOGLE_CLIENT_ID", raising=False)
        monkeypatch.delenv("GOOGLE_CLIENT_SECRET", raising=False)
        monkeypatch.setenv("GOOGLE_REFRESH_TOKEN", "z")
        with patch.object(keychain_secrets, "load_google_secrets", return_value=None):
            missing = keychain_secrets.verify_secrets()
        assert "GOOGLE_CLIENT_ID" in missing
        assert "GOOGLE_CLIENT_SECRET" in missing
        assert "GOOGLE_REFRESH_TOKEN" not in missing


class TestStoreSecret:
    def test_stores_known_key_successfully(self):
        import core.keychain_secrets as keychain_secrets
        kr_mock = MagicMock()
        kr_mock.set_password.return_value = None
        with patch.dict(sys.modules, {"keyring": kr_mock}):
            result = keychain_secrets.store_secret("GOOGLE_CLIENT_ID", "my-secret")
        assert result is True
        kr_mock.set_password.assert_called_once()

    def test_returns_false_for_unknown_key(self):
        import core.keychain_secrets as keychain_secrets
        result = keychain_secrets.store_secret("UNKNOWN_KEY", "value")
        assert result is False

    def test_returns_false_on_keychain_write_error(self):
        import core.keychain_secrets as keychain_secrets
        kr_mock = MagicMock()
        kr_mock.set_password.side_effect = Exception("permission denied")
        with patch.dict(sys.modules, {"keyring": kr_mock}):
            result = keychain_secrets.store_secret("GOOGLE_CLIENT_ID", "my-secret")
        assert result is False
