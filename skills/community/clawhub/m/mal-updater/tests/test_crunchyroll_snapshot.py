from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from mal_updater.config import load_config
from mal_updater.crunchyroll_auth import resolve_crunchyroll_state_paths
from mal_updater.crunchyroll_auth import CrunchyrollAuthError, CrunchyrollBootstrapResult
from mal_updater.crunchyroll_snapshot import (
    CRUNCHYROLL_ME_URL,
    CrunchyrollAccessToken,
    CrunchyrollUnauthorizedError,
    _CrunchyrollAuthSession,
    _CrunchyrollRequestPacer,
    _fetch_snapshot_once,
    _write_sync_boundary,
)


class CrunchyrollAuthRecoveryTests(unittest.TestCase):
    def _build_session(self, root: Path) -> _CrunchyrollAuthSession:
        config = load_config(root)
        state_paths = resolve_crunchyroll_state_paths(config)
        return _CrunchyrollAuthSession(
            config=config,
            profile="default",
            timeout_seconds=5.0,
            pacer=_CrunchyrollRequestPacer(0.0, 0.0),
            state_paths=state_paths,
            token=CrunchyrollAccessToken(
                access_token="access-token",
                refresh_token="refresh-token",
                account_id="acct-123",
                device_id="device-123",
                device_type="ANDROIDTV",
            ),
            auth_source="refresh_token",
        )

    def test_authorized_json_get_recovers_401_by_refreshing_access_token(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            session = self._build_session(root)
            calls: list[str] = []

            def fake_authorized_get(url: str, *, access_token: str, timeout_seconds: float, params=None, pacer=None):
                calls.append(access_token)
                if len(calls) == 1:
                    raise CrunchyrollUnauthorizedError(url, 401)
                return {"ok": True, "token_used": access_token}

            with patch("mal_updater.crunchyroll_snapshot._authorized_json_get", side_effect=fake_authorized_get), patch(
                "mal_updater.crunchyroll_snapshot.refresh_access_token"
            ) as mock_refresh, patch("mal_updater.crunchyroll_snapshot.crunchyroll_login_with_credentials") as mock_login:
                mock_refresh.return_value = (
                    CrunchyrollAccessToken(
                        access_token="refreshed-access-token",
                        refresh_token="refreshed-refresh-token",
                        account_id="acct-123",
                        device_id="device-123",
                        device_type="ANDROIDTV",
                    ),
                    session.state_paths,
                )

                payload = session.authorized_json_get("https://example.invalid/history")

            self.assertEqual(payload["token_used"], "refreshed-access-token")
            self.assertEqual(calls, ["access-token", "refreshed-access-token"])
            self.assertEqual(session.auth_source, "refresh_token_recovery")
            self.assertFalse(session.credential_rebootstrap_attempted)
            mock_refresh.assert_called_once()
            mock_login.assert_not_called()

    def test_authorized_json_get_falls_back_to_credentials_when_refresh_recovery_fails(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            session = self._build_session(root)
            calls: list[str] = []

            def fake_authorized_get(url: str, *, access_token: str, timeout_seconds: float, params=None, pacer=None):
                calls.append(access_token)
                if len(calls) == 1:
                    raise CrunchyrollUnauthorizedError(url, 401)
                return {"ok": True, "token_used": access_token}

            with patch("mal_updater.crunchyroll_snapshot._authorized_json_get", side_effect=fake_authorized_get), patch(
                "mal_updater.crunchyroll_snapshot.refresh_access_token",
                side_effect=CrunchyrollAuthError("refresh failed"),
            ) as mock_refresh, patch(
                "mal_updater.crunchyroll_snapshot.crunchyroll_login_with_credentials"
            ) as mock_login:
                mock_login.return_value = CrunchyrollBootstrapResult(
                    profile="default",
                    locale="en-US",
                    username_path=root / ".MAL-Updater" / "secrets" / "crunchyroll_username.txt",
                    password_path=root / ".MAL-Updater" / "secrets" / "crunchyroll_password.txt",
                    refresh_token_path=session.state_paths.refresh_token_path,
                    device_id_path=session.state_paths.device_id_path,
                    session_state_path=session.state_paths.session_state_path,
                    account_id="acct-123",
                    account_email="user@example.com",
                    access_token="credential-access-token",
                    refresh_token="credential-refresh-token",
                    device_id="device-123",
                    device_type="ANDROIDTV",
                )

                payload = session.authorized_json_get("https://example.invalid/history")

            self.assertEqual(payload["token_used"], "credential-access-token")
            self.assertEqual(calls, ["access-token", "credential-access-token"])
            self.assertEqual(session.auth_source, "credential_rebootstrap")
            self.assertTrue(session.credential_rebootstrap_attempted)
            mock_refresh.assert_called_once()
            mock_login.assert_called_once()

    def test_authorized_json_get_stops_cleanly_after_refresh_and_credential_retry_are_exhausted(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            session = self._build_session(root)
            calls: list[tuple[str, dict[str, object] | None]] = []

            def fake_authorized_get(url: str, *, access_token: str, timeout_seconds: float, params=None, pacer=None):
                calls.append((access_token, params))
                raise CrunchyrollUnauthorizedError(url, 401)

            with patch("mal_updater.crunchyroll_snapshot._authorized_json_get", side_effect=fake_authorized_get), patch(
                "mal_updater.crunchyroll_snapshot.refresh_access_token"
            ) as mock_refresh, patch("mal_updater.crunchyroll_snapshot.crunchyroll_login_with_credentials") as mock_login:
                mock_refresh.return_value = (
                    CrunchyrollAccessToken(
                        access_token="refreshed-access-token",
                        refresh_token="refreshed-refresh-token",
                        account_id="acct-123",
                        device_id="device-123",
                        device_type="ANDROIDTV",
                    ),
                    session.state_paths,
                )
                mock_login.return_value = CrunchyrollBootstrapResult(
                    profile="default",
                    locale="en-US",
                    username_path=root / ".MAL-Updater" / "secrets" / "crunchyroll_username.txt",
                    password_path=root / ".MAL-Updater" / "secrets" / "crunchyroll_password.txt",
                    refresh_token_path=session.state_paths.refresh_token_path,
                    device_id_path=session.state_paths.device_id_path,
                    session_state_path=session.state_paths.session_state_path,
                    account_id="acct-123",
                    account_email="user@example.com",
                    access_token="credential-access-token",
                    refresh_token="credential-refresh-token",
                    device_id="device-123",
                    device_type="ANDROIDTV",
                )

                with self.assertRaises(CrunchyrollUnauthorizedError):
                    session.authorized_json_get(
                        "https://example.invalid/history",
                        params={"page": 7, "page_size": 100},
                    )

            self.assertEqual(
                calls,
                [
                    ("access-token", {"page": 7, "page_size": 100}),
                    ("refreshed-access-token", {"page": 7, "page_size": 100}),
                    ("credential-access-token", {"page": 7, "page_size": 100}),
                ],
            )
            self.assertEqual(session.auth_source, "credential_rebootstrap")
            self.assertTrue(session.credential_rebootstrap_attempted)
            mock_refresh.assert_called_once()
            mock_login.assert_called_once()

            session_state = json.loads(session.state_paths.session_state_path.read_text(encoding="utf-8"))
            self.assertEqual(session_state["crunchyroll_phase"], "auth_failed")
            self.assertIn("credential rebootstrap already used", session_state["last_error"])


class CrunchyrollSnapshotBoundaryTests(unittest.TestCase):
    def _build_session(self, root: Path) -> _CrunchyrollAuthSession:
        config = load_config(root)
        state_paths = resolve_crunchyroll_state_paths(config)
        return _CrunchyrollAuthSession(
            config=config,
            profile="default",
            timeout_seconds=5.0,
            pacer=_CrunchyrollRequestPacer(0.0, 0.0),
            state_paths=state_paths,
            token=CrunchyrollAccessToken(
                access_token="access-token",
                refresh_token="refresh-token",
                account_id="acct-123",
                device_id="device-123",
                device_type="ANDROIDTV",
            ),
            auth_source="refresh_token",
        )

    def _history_entry(self, idx: int, *, played_at: str | None = None) -> dict[str, object]:
        return {
            "date_played": played_at or f"2026-03-14T20:{idx % 60:02d}:00Z",
            "playhead": 1_440_000,
            "fully_watched": True,
            "panel": {
                "type": "episode",
                "id": f"episode-{idx}",
                "title": f"Episode {idx}",
                "episode_metadata": {
                    "series_id": "series-123",
                    "series_title": "Example Show",
                    "season_title": "Example Show",
                    "season_number": 1,
                    "episode_number": idx,
                    "duration_ms": 1_440_000,
                    "audio_locale": "en-US",
                    "subtitle_locales": ["en-US"],
                },
            },
        }

    def _watchlist_entry(self, idx: int, *, added_at: str | None = None) -> dict[str, object]:
        return {
            "date_added": added_at or f"2026-03-14T18:{idx % 60:02d}:00Z",
            "never_watched": idx % 2 == 0,
            "fully_watched": False,
            "panel": {
                "type": "series",
                "id": f"watch-{idx}",
                "title": f"Watchlist Show {idx}",
            },
        }

    def test_fetch_snapshot_recovers_watch_history_401_via_refresh_then_completes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            session = self._build_session(root)
            calls: list[tuple[str, str, dict[str, object] | None]] = []
            history_page = [self._history_entry(1)]
            watchlist_page = [self._watchlist_entry(1)]

            def fake_authorized_get(
                url: str,
                *,
                access_token: str,
                timeout_seconds: float,
                params=None,
                pacer=None,
            ):
                calls.append((url, access_token, params))
                if url == CRUNCHYROLL_ME_URL:
                    self.assertEqual(access_token, "access-token")
                    return {"account_id": "acct-123", "email": "user@example.com"}
                if url.endswith("/watch-history"):
                    if access_token == "access-token":
                        raise CrunchyrollUnauthorizedError(url, 401)
                    self.assertEqual(access_token, "refreshed-access-token")
                    return {"total": 1, "data": history_page}
                if url.endswith("/watchlist"):
                    self.assertEqual(access_token, "refreshed-access-token")
                    return {"total": 1, "data": watchlist_page}
                raise AssertionError(url)

            with patch("mal_updater.crunchyroll_snapshot._authorized_json_get", side_effect=fake_authorized_get), patch(
                "mal_updater.crunchyroll_snapshot.refresh_access_token"
            ) as mock_refresh, patch("mal_updater.crunchyroll_snapshot.crunchyroll_login_with_credentials") as mock_login:
                mock_refresh.return_value = (
                    CrunchyrollAccessToken(
                        access_token="refreshed-access-token",
                        refresh_token="refreshed-refresh-token",
                        account_id="acct-123",
                        device_id="device-123",
                        device_type="ANDROIDTV",
                    ),
                    session.state_paths,
                )

                result = _fetch_snapshot_once(session, use_incremental_boundary=True)

            self.assertEqual(
                calls,
                [
                    (CRUNCHYROLL_ME_URL, "access-token", None),
                    (
                        "https://www.crunchyroll.com/content/v2/acct-123/watch-history",
                        "access-token",
                        {"page": 1, "page_size": 100, "locale": "en-US"},
                    ),
                    (
                        "https://www.crunchyroll.com/content/v2/acct-123/watch-history",
                        "refreshed-access-token",
                        {"page": 1, "page_size": 100, "locale": "en-US"},
                    ),
                    (
                        "https://www.crunchyroll.com/content/v2/discover/acct-123/watchlist",
                        "refreshed-access-token",
                        {"locale": "en-US", "n": 100, "start": 0},
                    ),
                ],
            )
            self.assertEqual(session.auth_source, "refresh_token_recovery")
            self.assertEqual(session.token.access_token, "refreshed-access-token")
            self.assertEqual(session.token.refresh_token, "refreshed-refresh-token")
            self.assertEqual(session.account_email, "user@example.com")
            self.assertFalse(session.credential_rebootstrap_attempted)
            self.assertEqual(result.account_email, "user@example.com")
            self.assertEqual(result.snapshot.account_id_hint, "acct-123")
            self.assertEqual(result.snapshot.raw["auth_source"], "refresh_token_recovery")
            self.assertEqual(result.snapshot.raw["history_count"], 1)
            self.assertEqual(result.snapshot.raw["watchlist_count"], 1)
            self.assertFalse(result.snapshot.raw["history_stopped_early"])
            self.assertFalse(result.snapshot.raw["watchlist_stopped_early"])
            mock_refresh.assert_called_once()
            mock_login.assert_not_called()

            session_state = json.loads(session.state_paths.session_state_path.read_text(encoding="utf-8"))
            self.assertEqual(session_state["crunchyroll_phase"], "python_live_snapshot")
            self.assertIsNone(session_state["last_error"])
            self.assertEqual(session_state["last_account_id_hint"], "acct-123")

    def test_fetch_snapshot_uses_incremental_boundary_to_stop_history_and_watchlist_early(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            session = self._build_session(root)

            previous_history = [self._history_entry(500), self._history_entry(499)]
            previous_watchlist = [self._watchlist_entry(700), self._watchlist_entry(699)]
            _write_sync_boundary(
                state_paths=session.state_paths,
                generated_at="2026-03-14T19:00:00Z",
                account_id_hint="acct-123",
                history_entries=previous_history,
                watchlist_entries=previous_watchlist,
            )

            history_page = [self._history_entry(idx) for idx in range(1, 100)] + [previous_history[0]]
            watchlist_page = [self._watchlist_entry(idx) for idx in range(1, 100)] + [previous_watchlist[0]]
            calls: list[tuple[str, dict[str, object] | None]] = []

            def fake_get(url: str, *, params: dict[str, object] | None = None):
                calls.append((url, params))
                if url == CRUNCHYROLL_ME_URL:
                    return {"account_id": "acct-123", "email": "user@example.com"}
                if url.endswith("/watch-history"):
                    return {"total": 350, "data": history_page}
                if url.endswith("/watchlist"):
                    return {"total": 250, "data": watchlist_page}
                raise AssertionError(url)

            with patch.object(_CrunchyrollAuthSession, "authorized_json_get", side_effect=fake_get):
                result = _fetch_snapshot_once(session, use_incremental_boundary=True)

            watch_history_calls = [item for item in calls if item[0].endswith("/watch-history")]
            watchlist_calls = [item for item in calls if item[0].endswith("/watchlist")]
            self.assertEqual(len(watch_history_calls), 1)
            self.assertEqual(len(watchlist_calls), 1)
            self.assertTrue(result.snapshot.raw["history_stopped_early"])
            self.assertTrue(result.snapshot.raw["watchlist_stopped_early"])
            self.assertEqual(result.snapshot.raw["sync_boundary_mode"], "incremental")
            self.assertTrue(result.state_paths.sync_boundary_path.exists())
            saved = json.loads(result.state_paths.sync_boundary_path.read_text(encoding="utf-8"))
            self.assertEqual(saved["account_id_hint"], "acct-123")
            self.assertGreaterEqual(saved["history"]["retained_count"], 1)
            self.assertGreaterEqual(saved["watchlist"]["retained_count"], 1)

    def test_fetch_snapshot_full_refresh_ignores_existing_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            session = self._build_session(root)

            previous_history = [self._history_entry(500)]
            previous_watchlist = [self._watchlist_entry(700)]
            _write_sync_boundary(
                state_paths=session.state_paths,
                generated_at="2026-03-14T19:00:00Z",
                account_id_hint="acct-123",
                history_entries=previous_history,
                watchlist_entries=previous_watchlist,
            )

            history_page_1 = [self._history_entry(idx) for idx in range(1, 100)] + [previous_history[0]]
            history_page_2 = [self._history_entry(idx) for idx in range(101, 151)]
            watchlist_page_1 = [self._watchlist_entry(idx) for idx in range(1, 100)] + [previous_watchlist[0]]
            watchlist_page_2 = [self._watchlist_entry(idx) for idx in range(101, 121)]
            calls: list[tuple[str, dict[str, object] | None]] = []

            def fake_get(url: str, *, params: dict[str, object] | None = None):
                calls.append((url, params))
                if url == CRUNCHYROLL_ME_URL:
                    return {"account_id": "acct-123", "email": "user@example.com"}
                if url.endswith("/watch-history"):
                    if params and params.get("page") == 1:
                        return {"total": 150, "data": history_page_1}
                    if params and params.get("page") == 2:
                        return {"total": 150, "data": history_page_2}
                if url.endswith("/watchlist"):
                    if params and params.get("start") == 0:
                        return {"total": 120, "data": watchlist_page_1}
                    if params and params.get("start") == 100:
                        return {"total": 120, "data": watchlist_page_2}
                raise AssertionError((url, params))

            with patch.object(_CrunchyrollAuthSession, "authorized_json_get", side_effect=fake_get):
                result = _fetch_snapshot_once(session, use_incremental_boundary=False)

            watch_history_calls = [item for item in calls if item[0].endswith("/watch-history")]
            watchlist_calls = [item for item in calls if item[0].endswith("/watchlist")]
            self.assertEqual(len(watch_history_calls), 2)
            self.assertEqual(len(watchlist_calls), 2)
            self.assertFalse(result.snapshot.raw["history_stopped_early"])
            self.assertFalse(result.snapshot.raw["watchlist_stopped_early"])
            self.assertEqual(result.snapshot.raw["sync_boundary_mode"], "full_refresh")


if __name__ == "__main__":
    unittest.main()
