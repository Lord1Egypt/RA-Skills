from __future__ import annotations

import io
import stat
import tempfile
import textwrap
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from mal_updater.auth import format_auth_flow_prompt, persist_token_response, write_secret_file
from mal_updater.cli import _cmd_approve_mapping, _cmd_dry_run_sync, _cmd_review_mappings
from mal_updater.config import load_config, load_mal_secrets
from mal_updater.db import bootstrap_database, get_series_mapping
from mal_updater.ingestion import ingest_snapshot_payload
from tests.test_validation_ingestion import sample_snapshot
from mal_updater.mal_client import MalApiError, MalClient, TokenResponse


class ConfigTests(unittest.TestCase):
    def test_load_config_reads_bind_host_and_redirect_host_from_settings(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            (root / ".MAL-Updater" / "config" / "settings.toml").write_text(
                textwrap.dedent(
                    """
                    [mal]
                    bind_host = "127.0.0.50"
                    redirect_host = "animebox.local"
                    redirect_port = 9999
                    """
                ),
                encoding="utf-8",
            )

            config = load_config(root)

            self.assertEqual(config.mal.bind_host, "127.0.0.50")
            self.assertEqual(config.mal.redirect_host, "animebox.local")
            self.assertEqual(config.mal.redirect_uri, "http://animebox.local:9999/callback")

    def test_load_config_reads_request_timeout_seconds_from_settings(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            (root / ".MAL-Updater" / "config" / "settings.toml").write_text(
                textwrap.dedent(
                    """
                    request_timeout_seconds = 7.5
                    """
                ),
                encoding="utf-8",
            )

            config = load_config(root)

            self.assertEqual(config.request_timeout_seconds, 7.5)

    def test_load_config_reads_mal_request_spacing_and_jitter_seconds(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            (root / ".MAL-Updater" / "config" / "settings.toml").write_text(
                textwrap.dedent(
                    """
                    [mal]
                    request_spacing_seconds = 1.1
                    request_spacing_jitter_seconds = 0.15
                    """
                ),
                encoding="utf-8",
            )

            config = load_config(root)

            self.assertEqual(config.mal.request_spacing_seconds, 1.1)
            self.assertEqual(config.mal.request_spacing_jitter_seconds, 0.15)

    def test_load_mal_secrets_reads_secret_file_overrides_from_settings(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True)
            (root / ".MAL-Updater" / "config" / "settings.toml").write_text(
                textwrap.dedent(
                    """
                    [secret_files]
                    mal_client_id = "../secrets/custom_client_id.txt"
                    """
                ),
                encoding="utf-8",
            )
            (root / ".MAL-Updater" / "secrets" / "custom_client_id.txt").write_text("client-123\n", encoding="utf-8")

            secrets = load_mal_secrets(load_config(root))

            self.assertEqual(secrets.client_id, "client-123")
            self.assertEqual(secrets.client_id_path, (root / ".MAL-Updater" / "secrets" / "custom_client_id.txt").resolve())



    def test_load_config_reads_crunchyroll_request_spacing_and_jitter_seconds(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            (root / ".MAL-Updater" / "config" / "settings.toml").write_text(
                textwrap.dedent(
                    """
                    [crunchyroll]
                    request_spacing_seconds = 12.5
                    request_spacing_jitter_seconds = 2.25
                    """
                ),
                encoding="utf-8",
            )

            config = load_config(root)

            self.assertEqual(config.crunchyroll.request_spacing_seconds, 12.5)
            self.assertEqual(config.crunchyroll.request_spacing_jitter_seconds, 2.25)

class AuthHelperTests(unittest.TestCase):
    def test_format_auth_flow_prompt_includes_bind_host_and_redirect_uri(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            (root / ".MAL-Updater" / "config" / "settings.toml").write_text(
                textwrap.dedent(
                    """
                    [mal]
                    bind_host = "0.0.0.0"
                    redirect_host = "127.0.0.117"
                    redirect_port = 8765
                    """
                ),
                encoding="utf-8",
            )
            config = load_config(root)

            prompt = format_auth_flow_prompt(config, "https://example.test/auth", 300)

            self.assertIn("bind_host=0.0.0.0", prompt)
            self.assertIn("redirect_uri=http://127.0.0.117:8765/callback", prompt)
            self.assertIn("https://example.test/auth", prompt)

    def test_write_secret_file_sets_0600_permissions(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "secret.txt"

            write_secret_file(path, "top-secret")

            self.assertEqual(path.read_text(encoding="utf-8"), "top-secret\n")
            mode = stat.S_IMODE(path.stat().st_mode)
            self.assertEqual(mode, 0o600)

    def test_persist_token_response_writes_access_and_refresh_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            secrets = load_mal_secrets(config)
            token = TokenResponse(
                access_token="access-abc",
                token_type="Bearer",
                expires_in=3600,
                refresh_token="refresh-xyz",
                scope=None,
                raw={},
            )

            persisted = persist_token_response(token, secrets)

            self.assertEqual(persisted.access_token_path.read_text(encoding="utf-8"), "access-abc\n")
            self.assertEqual(persisted.refresh_token_path.read_text(encoding="utf-8"), "refresh-xyz\n")

    def test_mal_client_uses_configured_request_timeout_for_get_requests(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            (root / ".MAL-Updater" / "config" / "settings.toml").write_text("request_timeout_seconds = 7.5\n", encoding="utf-8")
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            config = load_config(root)
            client = MalClient(config, load_mal_secrets(config))

            class _Response:
                def __enter__(self):
                    return self

                def __exit__(self, exc_type, exc, tb):
                    return False

                def read(self):
                    return b'{"data": []}'

            with patch("mal_updater.mal_client.urlopen", return_value=_Response()) as urlopen_mock:
                client.search_anime("Example")

            self.assertEqual(urlopen_mock.call_args.kwargs["timeout"], 7.5)

    def test_mal_client_paces_requests_using_configured_spacing(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            (root / ".MAL-Updater" / "config" / "settings.toml").write_text(
                textwrap.dedent(
                    """
                    [mal]
                    request_spacing_seconds = 1.0
                    request_spacing_jitter_seconds = 0.0
                    """
                ),
                encoding="utf-8",
            )
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            config = load_config(root)
            client = MalClient(config, load_mal_secrets(config))

            class _Response:
                def __enter__(self):
                    return self

                def __exit__(self, exc_type, exc, tb):
                    return False

                def read(self):
                    return b'{"data": []}'

            with patch("mal_updater.mal_client.urlopen", return_value=_Response()), patch(
                "mal_updater.mal_client.time.monotonic",
                side_effect=[100.0, 100.0, 100.4, 100.4],
            ), patch("mal_updater.mal_client.time.sleep") as sleep_mock:
                client.search_anime("Example")
                client.search_anime("Example Again")

            sleep_mock.assert_called_once()
            self.assertAlmostEqual(sleep_mock.call_args.args[0], 0.6, places=6)

    def test_mal_client_retries_timeout_once_then_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            config = load_config(root)
            client = MalClient(config, load_mal_secrets(config))

            class _Response:
                def __enter__(self):
                    return self

                def __exit__(self, exc_type, exc, tb):
                    return False

                def read(self):
                    return b'{"data": []}'

            with patch(
                "mal_updater.mal_client.urlopen",
                side_effect=[TimeoutError("timed out"), _Response()],
            ) as urlopen_mock, patch("mal_updater.mal_client.time.sleep"):
                response = client.search_anime("Example")

            self.assertEqual(response, {"data": []})
            self.assertEqual(urlopen_mock.call_count, 2)

    def test_mal_client_wraps_timeout_errors_as_mal_api_errors(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            (root / ".MAL-Updater" / "secrets").mkdir(parents=True)
            (root / ".MAL-Updater" / "secrets" / "mal_client_id.txt").write_text("client-id\n", encoding="utf-8")
            config = load_config(root)
            client = MalClient(config, load_mal_secrets(config))

            with patch("mal_updater.mal_client.urlopen", side_effect=TimeoutError("timed out")), patch(
                "mal_updater.mal_client.time.sleep"
            ):
                with self.assertRaises(MalApiError) as exc:
                    client.search_anime("Example")

            self.assertIn("timeout after 2 attempts", str(exc.exception))
            self.assertIn("timed out", str(exc.exception))

    def test_review_mappings_rejects_partial_queue_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            stderr = io.StringIO()

            with redirect_stderr(stderr):
                code = _cmd_review_mappings(root, limit=20, mapping_limit=5, persist_queue=True)

            self.assertEqual(code, 2)
            self.assertIn("requires a full scan", stderr.getvalue())

    def test_dry_run_sync_rejects_partial_queue_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            stderr = io.StringIO()

            with redirect_stderr(stderr):
                code = _cmd_dry_run_sync(
                    root,
                    limit=20,
                    mapping_limit=5,
                    approved_mappings_only=False,
                    exact_approved_only=False,
                    persist_queue=True,
                )

            self.assertEqual(code, 2)
            self.assertIn("requires a full scan", stderr.getvalue())

    def test_approve_mapping_exact_flag_persists_user_exact_source(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            config = load_config(root)
            bootstrap_database(config.db_path)
            ingest_snapshot_payload(sample_snapshot(), config)
            stdout = io.StringIO()

            with redirect_stdout(stdout):
                code = _cmd_approve_mapping(
                    root,
                    provider_series_id="series-123",
                    mal_anime_id=123,
                    confidence=1.0,
                    notes="manual exact approval",
                    exact=True,
                )

            self.assertEqual(code, 0)
            mapping = get_series_mapping(config.db_path, "crunchyroll", "series-123")
            self.assertIsNotNone(mapping)
            assert mapping is not None
            self.assertEqual(mapping.mapping_source, "user_exact")
            self.assertTrue(mapping.approved_by_user)


if __name__ == "__main__":
    unittest.main()
