from __future__ import annotations

import json
import random
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

try:
    from curl_cffi import requests as curl_requests
except ModuleNotFoundError:  # pragma: no cover - optional runtime dependency
    curl_requests = None

from .auth import write_secret_file
from .config import AppConfig, _read_secret_file
from .request_tracking import record_api_request_event
from .contracts import CrunchyrollSnapshot, EpisodeProgress, SeriesRef, WatchlistEntry
from .crunchyroll_auth import (
    CRUNCHYROLL_BASIC_AUTH_TOKEN,
    CRUNCHYROLL_ME_URL,
    CRUNCHYROLL_TOKEN_URL,
    CrunchyrollAuthError,
    CrunchyrollBootstrapResult,
    CrunchyrollStatePaths,
    crunchyroll_login_with_credentials,
    resolve_crunchyroll_state_paths,
)


class CrunchyrollSnapshotError(RuntimeError):
    pass


class CrunchyrollUnauthorizedError(CrunchyrollSnapshotError):
    def __init__(self, url: str, status_code: int):
        super().__init__(f"Crunchyroll GET failed for {url}: HTTP {status_code}")
        self.url = url
        self.status_code = status_code


DEFAULT_CRUNCHYROLL_DEVICE_TYPE = "ANDROIDTV"
SYNC_BOUNDARY_SCHEMA_VERSION = 1
HISTORY_BOUNDARY_MARKER_LIMIT = 200
WATCHLIST_BOUNDARY_MARKER_LIMIT = 200


@dataclass(slots=True)
class CrunchyrollAccessToken:
    access_token: str
    refresh_token: str
    account_id: str | None
    device_id: str
    device_type: str


@dataclass(slots=True)
class CrunchyrollFetchResult:
    snapshot: CrunchyrollSnapshot
    state_paths: CrunchyrollStatePaths
    account_email: str | None


@dataclass(slots=True)
class _SyncBoundary:
    generated_at: str | None
    account_id_hint: str | None
    history_markers: list[str]
    watchlist_markers: list[str]


@dataclass(slots=True)
class _CrunchyrollRequestPacer:
    spacing_seconds: float
    jitter_seconds: float = 0.0
    last_request_started_at: float | None = None

    def _target_spacing_seconds(self) -> float:
        if self.spacing_seconds <= 0:
            return 0.0
        if self.jitter_seconds <= 0:
            return self.spacing_seconds
        lower = max(0.0, self.spacing_seconds - self.jitter_seconds)
        upper = self.spacing_seconds + self.jitter_seconds
        return random.uniform(lower, upper)

    def wait_turn(self) -> None:
        target_spacing_seconds = self._target_spacing_seconds()
        if target_spacing_seconds <= 0:
            self.last_request_started_at = time.monotonic()
            return
        now = time.monotonic()
        if self.last_request_started_at is not None:
            remaining = target_spacing_seconds - (now - self.last_request_started_at)
            if remaining > 0:
                time.sleep(remaining)
                now = time.monotonic()
        self.last_request_started_at = now


@dataclass(slots=True)
class _CrunchyrollAuthSession:
    config: AppConfig
    profile: str
    timeout_seconds: float
    pacer: _CrunchyrollRequestPacer
    state_paths: CrunchyrollStatePaths
    token: CrunchyrollAccessToken
    auth_source: str
    account_email: str | None = None
    credential_rebootstrap_attempted: bool = False

    def authorized_json_get(self, url: str, *, params: dict[str, Any] | None = None) -> Any:
        last_unauthorized: CrunchyrollUnauthorizedError | None = None
        refresh_error: CrunchyrollAuthError | None = None
        for attempt in range(3):
            try:
                return _authorized_json_get(
                    url,
                    access_token=self.token.access_token,
                    timeout_seconds=self.timeout_seconds,
                    params=params,
                    pacer=self.pacer,
                )
            except CrunchyrollUnauthorizedError as exc:
                last_unauthorized = exc
                if attempt == 0:
                    try:
                        self._refresh_with_refresh_token(exc)
                        continue
                    except CrunchyrollAuthError as refresh_exc:
                        refresh_error = refresh_exc
                if not self.credential_rebootstrap_attempted:
                    self._rebootstrap_with_credentials(exc, refresh_error=refresh_error)
                    continue
                detail = f"{exc}; refresh-token recovery failed"
                if refresh_error is not None:
                    detail += f" ({refresh_error})"
                detail += "; credential rebootstrap already used for this run"
                _write_session_state(
                    state_paths=self.state_paths,
                    profile=self.profile,
                    locale=self.config.crunchyroll.locale,
                    device_type=self.token.device_type,
                    account_id=self.token.account_id,
                    last_error=detail,
                    success=False,
                    phase="auth_failed",
                )
                raise
        raise last_unauthorized or CrunchyrollSnapshotError(f"Crunchyroll authorization failed for {url}")

    def _refresh_with_refresh_token(self, exc: CrunchyrollUnauthorizedError) -> None:
        _write_session_state(
            state_paths=self.state_paths,
            profile=self.profile,
            locale=self.config.crunchyroll.locale,
            device_type=self.token.device_type,
            account_id=self.token.account_id,
            last_error=f"{exc}; retrying with refresh-token renewal",
            success=False,
            phase="auth_retrying_with_refresh_token",
        )
        token, state_paths = refresh_access_token(
            self.config,
            profile=self.profile,
            timeout_seconds=self.timeout_seconds,
            pacer=self.pacer,
        )
        self.token = token
        self.state_paths = state_paths
        self.auth_source = "refresh_token_recovery"

    def _rebootstrap_with_credentials(
        self,
        exc: CrunchyrollUnauthorizedError,
        *,
        refresh_error: CrunchyrollAuthError | None = None,
    ) -> None:
        message = f"{exc}; retrying once with credential rebootstrap"
        if refresh_error is not None:
            message += f" after refresh-token recovery failed ({refresh_error})"
        _write_session_state(
            state_paths=self.state_paths,
            profile=self.profile,
            locale=self.config.crunchyroll.locale,
            device_type=self.token.device_type,
            account_id=self.token.account_id,
            last_error=message,
            success=False,
            phase="auth_retrying_with_credentials",
        )
        bootstrap = crunchyroll_login_with_credentials(
            self.config,
            profile=self.profile,
            timeout_seconds=self.timeout_seconds,
            verify_account=True,
        )
        self.token = _token_from_bootstrap(bootstrap)
        self.state_paths = resolve_crunchyroll_state_paths(self.config, profile=self.profile)
        self.auth_source = "credential_rebootstrap"
        self.account_email = bootstrap.account_email
        self.credential_rebootstrap_attempted = True



def _now_string() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _http_post(url: str, *, data: dict[str, str], headers: dict[str, str], timeout_seconds: float):
    try:
        if curl_requests is not None:
            response = curl_requests.post(url, data=data, headers=headers, timeout=timeout_seconds, impersonate="chrome124")
        else:
            response = requests.post(url, data=data, headers=headers, timeout=timeout_seconds)
        record_api_request_event("crunchyroll", "http_post", url=url, method="POST", outcome="ok" if response.status_code < 400 else "http_error", status_code=response.status_code)
        return response
    except requests.RequestException as exc:
        record_api_request_event("crunchyroll", "http_post", url=url, method="POST", outcome="request_error", error=str(exc))
        raise


def _http_get(url: str, *, headers: dict[str, str], timeout_seconds: float, params: dict[str, Any] | None = None):
    try:
        if curl_requests is not None:
            response = curl_requests.get(url, headers=headers, timeout=timeout_seconds, params=params, impersonate="chrome124")
        else:
            response = requests.get(url, headers=headers, timeout=timeout_seconds, params=params)
        record_api_request_event("crunchyroll", "http_get", url=url, method="GET", outcome="ok" if response.status_code < 400 else "http_error", status_code=response.status_code)
        return response
    except requests.RequestException as exc:
        record_api_request_event("crunchyroll", "http_get", url=url, method="GET", outcome="request_error", error=str(exc))
        raise


def _write_session_state(
    *,
    state_paths: CrunchyrollStatePaths,
    profile: str,
    locale: str,
    device_type: str,
    account_id: str | None,
    last_error: str | None,
    success: bool,
    phase: str,
) -> None:
    state_paths.root.mkdir(parents=True, exist_ok=True)
    payload = {
        "profile": profile,
        "locale": locale,
        "refresh_token_present": state_paths.refresh_token_path.exists(),
        "device_id_present": state_paths.device_id_path.exists(),
        "device_type_hint": device_type,
        "last_login_attempt_at": _now_string(),
        "last_login_success_at": _now_string() if success else None,
        "last_account_id_hint": account_id,
        "last_error": last_error,
        "crunchyroll_phase": phase,
    }
    state_paths.session_state_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    state_paths.session_state_path.chmod(0o600)


def _read_device_id(state_paths: CrunchyrollStatePaths) -> str:
    return _read_secret_file(state_paths.device_id_path) or str(uuid.uuid4())


def refresh_access_token(
    config: AppConfig,
    *,
    profile: str = "default",
    timeout_seconds: float = 30.0,
    pacer: _CrunchyrollRequestPacer | None = None,
) -> tuple[CrunchyrollAccessToken, CrunchyrollStatePaths]:
    state_paths = resolve_crunchyroll_state_paths(config, profile=profile)
    refresh_token = _read_secret_file(state_paths.refresh_token_path)
    if not refresh_token:
        raise CrunchyrollAuthError(f"Missing Crunchyroll refresh token at {state_paths.refresh_token_path}")

    device_id = _read_device_id(state_paths)
    device_type = DEFAULT_CRUNCHYROLL_DEVICE_TYPE
    body = {
        "grant_type": "refresh_token",
        "scope": "offline_access",
        "refresh_token": refresh_token,
        "device_id": device_id,
        "device_type": device_type,
    }
    headers = {
        "Authorization": f"Basic {CRUNCHYROLL_BASIC_AUTH_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded",
        "ETP-Anonymous-ID": device_id,
    }
    if pacer is not None:
        pacer.wait_turn()
    response = _http_post(CRUNCHYROLL_TOKEN_URL, data=body, headers=headers, timeout_seconds=timeout_seconds)
    if response.status_code >= 400:
        message = f"Crunchyroll refresh-token login failed: HTTP {response.status_code}"
        if response.status_code == 403 and curl_requests is None:
            message += " (likely blocked by Cloudflare; install optional curl_cffi support for browser-TLS impersonation)"
        try:
            payload = response.json()
        except ValueError:
            payload = None
        if isinstance(payload, dict):
            error = payload.get("error")
            error_description = payload.get("error_description")
            if error or error_description:
                message = f"Crunchyroll refresh-token login failed: {error or 'unknown_error'} - {error_description or 'no description'}"
        _write_session_state(
            state_paths=state_paths,
            profile=profile,
            locale=config.crunchyroll.locale,
            device_type=device_type,
            account_id=None,
            last_error=message,
            success=False,
            phase="auth_failed",
        )
        raise CrunchyrollAuthError(message)

    token_payload = response.json()
    access_token = token_payload.get("access_token")
    new_refresh_token = token_payload.get("refresh_token")
    account_id = token_payload.get("account_id")
    if not access_token or not new_refresh_token:
        message = "Crunchyroll refresh-token login succeeded but did not return both access_token and refresh_token"
        _write_session_state(
            state_paths=state_paths,
            profile=profile,
            locale=config.crunchyroll.locale,
            device_type=device_type,
            account_id=account_id,
            last_error=message,
            success=False,
            phase="auth_failed",
        )
        raise CrunchyrollAuthError(message)

    write_secret_file(state_paths.refresh_token_path, new_refresh_token)
    write_secret_file(state_paths.device_id_path, device_id)
    return (
        CrunchyrollAccessToken(
            access_token=access_token,
            refresh_token=new_refresh_token,
            account_id=str(account_id) if account_id else None,
            device_id=device_id,
            device_type=device_type,
        ),
        state_paths,
    )


def _authorized_json_get(
    url: str,
    *,
    access_token: str,
    timeout_seconds: float,
    params: dict[str, Any] | None = None,
    pacer: _CrunchyrollRequestPacer | None = None,
) -> Any:
    if pacer is not None:
        pacer.wait_turn()
    response = _http_get(
        url,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout_seconds=timeout_seconds,
        params=params,
    )
    if response.status_code == 401:
        raise CrunchyrollUnauthorizedError(url, response.status_code)
    if response.status_code >= 400:
        raise CrunchyrollSnapshotError(f"Crunchyroll GET failed for {url}: HTTP {response.status_code}")
    return response.json()


def _panel_metadata(panel: dict[str, Any]) -> dict[str, Any]:
    if isinstance(panel.get("episode_metadata"), dict):
        return panel["episode_metadata"]
    if isinstance(panel.get("movie_metadata"), dict):
        return panel["movie_metadata"]
    return panel


def _pick_subtitle_locale(panel: dict[str, Any]) -> str | None:
    metadata = _panel_metadata(panel)
    locales = metadata.get("subtitle_locales")
    if isinstance(locales, list) and locales:
        first = locales[0]
        return str(first) if first else None
    return None


def _series_from_panel(panel: dict[str, Any]) -> SeriesRef | None:
    panel_type = panel.get("type")
    metadata = _panel_metadata(panel)
    if panel_type == "episode":
        provider_series_id = metadata.get("series_id")
        title = metadata.get("series_title") or provider_series_id
        season_title = metadata.get("season_title")
        season_number = metadata.get("season_number")
    elif panel_type == "movie":
        provider_series_id = metadata.get("movie_listing_id")
        title = metadata.get("movie_listing_title") or panel.get("title") or provider_series_id
        season_title = None
        season_number = None
    elif panel_type == "series":
        provider_series_id = panel.get("id")
        title = panel.get("title") or provider_series_id
        season_title = None
        season_number = None
    elif panel_type == "movie_listing":
        provider_series_id = panel.get("id")
        title = panel.get("title") or provider_series_id
        season_title = None
        season_number = None
    else:
        return None

    if not provider_series_id:
        return None
    return SeriesRef(
        provider_series_id=str(provider_series_id),
        title=str(title or provider_series_id),
        season_title=str(season_title) if season_title not in (None, "") else None,
        season_number=int(season_number) if isinstance(season_number, int) else None,
    )


def _progress_from_history_entry(entry: dict[str, Any]) -> EpisodeProgress | None:
    panel = entry.get("panel")
    if not isinstance(panel, dict):
        return None

    panel_type = panel.get("type")
    metadata = _panel_metadata(panel)
    playhead = entry.get("playhead")
    fully_watched = bool(entry.get("fully_watched"))
    last_watched_at = entry.get("date_played")

    if panel_type == "episode":
        duration_ms = int(metadata.get("duration_ms")) if isinstance(metadata.get("duration_ms"), int) else None
        playback_position_ms = int(playhead) if isinstance(playhead, int) else None
        if playback_position_ms is not None and duration_ms and playback_position_ms <= max(60000, duration_ms // 100):
            playback_position_ms *= 1000

        provider_series_id = metadata.get("series_id")
        provider_episode_id = panel.get("id")
        if not provider_series_id or not provider_episode_id:
            return None
        completion_ratio = None
        if duration_ms and playback_position_ms is not None and duration_ms > 0:
            completion_ratio = max(0.0, min(1.0, playback_position_ms / duration_ms))
        elif fully_watched:
            completion_ratio = 1.0
        episode_number = metadata.get("episode_number")
        return EpisodeProgress(
            provider_episode_id=str(provider_episode_id),
            provider_series_id=str(provider_series_id),
            episode_number=int(episode_number) if isinstance(episode_number, int) else None,
            episode_title=str(panel.get("title")) if panel.get("title") else None,
            playback_position_ms=playback_position_ms,
            duration_ms=duration_ms,
            completion_ratio=completion_ratio,
            last_watched_at=str(last_watched_at) if last_watched_at else None,
            audio_locale=str(metadata.get("audio_locale")) if metadata.get("audio_locale") else None,
            subtitle_locale=_pick_subtitle_locale(panel),
            rating=None,
        )

    if panel_type == "movie":
        duration_ms = int(metadata.get("duration_ms")) if isinstance(metadata.get("duration_ms"), int) else None
        playback_position_ms = int(playhead) if isinstance(playhead, int) else None
        if playback_position_ms is not None and duration_ms and playback_position_ms <= max(60000, duration_ms // 100):
            playback_position_ms *= 1000
        provider_series_id = metadata.get("movie_listing_id")
        provider_episode_id = panel.get("id")
        if not provider_series_id or not provider_episode_id:
            return None
        completion_ratio = None
        if duration_ms and playback_position_ms is not None and duration_ms > 0:
            completion_ratio = max(0.0, min(1.0, playback_position_ms / duration_ms))
        elif fully_watched:
            completion_ratio = 1.0
        return EpisodeProgress(
            provider_episode_id=str(provider_episode_id),
            provider_series_id=str(provider_series_id),
            episode_number=None,
            episode_title=str(panel.get("title")) if panel.get("title") else None,
            playback_position_ms=playback_position_ms,
            duration_ms=duration_ms,
            completion_ratio=completion_ratio,
            last_watched_at=str(last_watched_at) if last_watched_at else None,
            audio_locale=None,
            subtitle_locale=None,
            rating="movie",
        )

    return None


def _watchlist_from_entry(entry: dict[str, Any]) -> tuple[SeriesRef | None, WatchlistEntry | None]:
    panel = entry.get("panel")
    if not isinstance(panel, dict):
        return None, None
    series_ref = _series_from_panel(panel)
    if series_ref is None:
        return None, None
    if entry.get("fully_watched") is True:
        status = "fully_watched"
    elif entry.get("never_watched") is True:
        status = "never_watched"
    else:
        status = "in_progress"
    added_at = entry.get("date_added")
    return (
        series_ref,
        WatchlistEntry(
            provider_series_id=series_ref.provider_series_id,
            added_at=str(added_at) if added_at else None,
            status=status,
        ),
    )


def _dedupe_series(series_items: list[SeriesRef]) -> list[SeriesRef]:
    by_id: dict[str, SeriesRef] = {}
    for item in series_items:
        by_id.setdefault(item.provider_series_id, item)
    return list(by_id.values())


def _history_entry_fingerprint(entry: dict[str, Any]) -> str | None:
    panel = entry.get("panel")
    if not isinstance(panel, dict):
        return None
    metadata = _panel_metadata(panel)
    provider_episode_id = panel.get("id")
    provider_series_id = metadata.get("series_id") or metadata.get("movie_listing_id")
    panel_type = panel.get("type")
    last_watched_at = entry.get("date_played")
    playhead = entry.get("playhead")
    fully_watched = entry.get("fully_watched")
    if not provider_episode_id or not provider_series_id or not panel_type:
        return None
    return "|".join(
        [
            str(panel_type),
            str(provider_series_id),
            str(provider_episode_id),
            str(last_watched_at or ""),
            str(playhead if playhead is not None else ""),
            str(bool(fully_watched)),
        ]
    )


def _watchlist_entry_fingerprint(entry: dict[str, Any]) -> str | None:
    series_ref, watchlist_entry = _watchlist_from_entry(entry)
    if series_ref is None or watchlist_entry is None:
        return None
    return "|".join(
        [
            str(series_ref.provider_series_id),
            str(watchlist_entry.status),
            str(watchlist_entry.added_at or ""),
        ]
    )


def _load_sync_boundary(state_paths: CrunchyrollStatePaths) -> _SyncBoundary | None:
    path = state_paths.sync_boundary_path
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return None
    if not isinstance(payload, dict):
        return None
    if int(payload.get("schema_version") or 0) != SYNC_BOUNDARY_SCHEMA_VERSION:
        return None
    history = payload.get("history") if isinstance(payload.get("history"), dict) else {}
    watchlist = payload.get("watchlist") if isinstance(payload.get("watchlist"), dict) else {}
    return _SyncBoundary(
        generated_at=str(payload.get("generated_at")) if payload.get("generated_at") else None,
        account_id_hint=str(payload.get("account_id_hint")) if payload.get("account_id_hint") else None,
        history_markers=[str(item) for item in history.get("first_seen", []) if item],
        watchlist_markers=[str(item) for item in watchlist.get("first_seen", []) if item],
    )


def _write_sync_boundary(
    *,
    state_paths: CrunchyrollStatePaths,
    generated_at: str,
    account_id_hint: str | None,
    history_entries: list[dict[str, Any]],
    watchlist_entries: list[dict[str, Any]],
) -> None:
    state_paths.root.mkdir(parents=True, exist_ok=True)
    history_markers = []
    for entry in history_entries:
        fingerprint = _history_entry_fingerprint(entry)
        if fingerprint and fingerprint not in history_markers:
            history_markers.append(fingerprint)
        if len(history_markers) >= HISTORY_BOUNDARY_MARKER_LIMIT:
            break
    watchlist_markers = []
    for entry in watchlist_entries:
        fingerprint = _watchlist_entry_fingerprint(entry)
        if fingerprint and fingerprint not in watchlist_markers:
            watchlist_markers.append(fingerprint)
        if len(watchlist_markers) >= WATCHLIST_BOUNDARY_MARKER_LIMIT:
            break
    payload = {
        "schema_version": SYNC_BOUNDARY_SCHEMA_VERSION,
        "generated_at": generated_at,
        "account_id_hint": account_id_hint,
        "history": {
            "marker_limit": HISTORY_BOUNDARY_MARKER_LIMIT,
            "retained_count": len(history_markers),
            "first_seen": history_markers,
        },
        "watchlist": {
            "marker_limit": WATCHLIST_BOUNDARY_MARKER_LIMIT,
            "retained_count": len(watchlist_markers),
            "first_seen": watchlist_markers,
        },
    }
    state_paths.sync_boundary_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    state_paths.sync_boundary_path.chmod(0o600)


def _token_from_bootstrap(result: CrunchyrollBootstrapResult) -> CrunchyrollAccessToken:
    return CrunchyrollAccessToken(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        account_id=result.account_id,
        device_id=result.device_id,
        device_type=result.device_type,
    )


def _start_auth_session(
    config: AppConfig,
    *,
    profile: str,
    timeout_seconds: float,
    pacer: _CrunchyrollRequestPacer,
) -> _CrunchyrollAuthSession:
    state_paths = resolve_crunchyroll_state_paths(config, profile=profile)
    try:
        token, state_paths = refresh_access_token(config, profile=profile, timeout_seconds=timeout_seconds, pacer=pacer)
        return _CrunchyrollAuthSession(
            config=config,
            profile=profile,
            timeout_seconds=timeout_seconds,
            pacer=pacer,
            state_paths=state_paths,
            token=token,
            auth_source="refresh_token",
        )
    except CrunchyrollAuthError:
        bootstrap = crunchyroll_login_with_credentials(
            config,
            profile=profile,
            timeout_seconds=timeout_seconds,
            verify_account=True,
        )
        return _CrunchyrollAuthSession(
            config=config,
            profile=profile,
            timeout_seconds=timeout_seconds,
            pacer=pacer,
            state_paths=resolve_crunchyroll_state_paths(config, profile=profile),
            token=_token_from_bootstrap(bootstrap),
            auth_source="credential_rebootstrap",
            account_email=bootstrap.account_email,
            credential_rebootstrap_attempted=True,
        )


def _fetch_snapshot_once(
    session: _CrunchyrollAuthSession,
    *,
    use_incremental_boundary: bool = True,
) -> CrunchyrollFetchResult:
    config = session.config
    account_payload = session.authorized_json_get(CRUNCHYROLL_ME_URL)
    if not isinstance(account_payload, dict):
        raise CrunchyrollSnapshotError("Crunchyroll account response was not a JSON object")
    account_id = str(account_payload.get("account_id") or session.token.account_id or "") or None
    if not account_id:
        raise CrunchyrollSnapshotError("Crunchyroll account response did not include account_id")
    session.token.account_id = account_id
    if account_payload.get("email"):
        session.account_email = str(account_payload.get("email"))

    boundary = _load_sync_boundary(session.state_paths) if use_incremental_boundary else None
    if boundary and boundary.account_id_hint and boundary.account_id_hint != account_id:
        boundary = None
    history_markers = set(boundary.history_markers) if boundary else set()
    watchlist_markers = set(boundary.watchlist_markers) if boundary else set()

    history_entries: list[dict[str, Any]] = []
    history_pages_fetched = 0
    history_stopped_early = False
    page = 1
    while True:
        history_payload = session.authorized_json_get(
            f"https://www.crunchyroll.com/content/v2/{account_id}/watch-history",
            params={"page": page, "page_size": 100, "locale": config.crunchyroll.locale},
        )
        history_pages_fetched += 1
        if not isinstance(history_payload, dict):
            raise CrunchyrollSnapshotError("Crunchyroll watch-history response was not a JSON object")
        data = history_payload.get("data")
        if not isinstance(data, list):
            raise CrunchyrollSnapshotError("Crunchyroll watch-history response did not include a data list")
        batch = [item for item in data if isinstance(item, dict)]
        history_entries.extend(batch)
        if history_markers and any((_history_entry_fingerprint(item) in history_markers) for item in batch):
            history_stopped_early = True
            break
        total = history_payload.get("total")
        if len(batch) < 100:
            break
        if isinstance(total, int) and len(history_entries) >= total:
            break
        page += 1

    watchlist_data: list[dict[str, Any]] = []
    watchlist_total: int | None = None
    watchlist_pages_fetched = 0
    watchlist_stopped_early = False
    watchlist_start = 0
    while True:
        watchlist_payload = session.authorized_json_get(
            f"https://www.crunchyroll.com/content/v2/discover/{account_id}/watchlist",
            params={"locale": config.crunchyroll.locale, "n": 100, "start": watchlist_start},
        )
        watchlist_pages_fetched += 1
        if not isinstance(watchlist_payload, dict):
            raise CrunchyrollSnapshotError("Crunchyroll watchlist response was not a JSON object")
        data = watchlist_payload.get("data")
        if not isinstance(data, list):
            raise CrunchyrollSnapshotError("Crunchyroll watchlist response did not include a data list")
        batch = [item for item in data if isinstance(item, dict)]
        watchlist_data.extend(batch)
        if watchlist_markers and any((_watchlist_entry_fingerprint(item) in watchlist_markers) for item in batch):
            watchlist_stopped_early = True
            break
        total = watchlist_payload.get("total")
        if isinstance(total, int):
            watchlist_total = total
        if not batch:
            break
        watchlist_start += len(batch)
        if len(batch) < 100:
            break
        if watchlist_total is not None and len(watchlist_data) >= watchlist_total:
            break

    progress = [item for item in (_progress_from_history_entry(entry) for entry in history_entries) if item is not None]
    history_series = [item for item in (_series_from_panel(entry.get("panel")) for entry in history_entries if isinstance(entry.get("panel"), dict)) if item is not None]

    watchlist_series: list[SeriesRef] = []
    watchlist_entries: list[WatchlistEntry] = []
    for entry in watchlist_data:
        if not isinstance(entry, dict):
            continue
        series_ref, watchlist_entry = _watchlist_from_entry(entry)
        if series_ref is not None:
            watchlist_series.append(series_ref)
        if watchlist_entry is not None:
            watchlist_entries.append(watchlist_entry)

    generated_at = _now_string()
    snapshot = CrunchyrollSnapshot(
        contract_version=config.contract_version,
        generated_at=generated_at,
        provider="crunchyroll",
        account_id_hint=account_id,
        series=_dedupe_series(history_series + watchlist_series),
        progress=progress,
        watchlist=watchlist_entries,
        raw={
            "status": "ok",
            "profile": session.profile,
            "state_root": str(session.state_paths.root),
            "session_state_path": str(session.state_paths.session_state_path),
            "sync_boundary_path": str(session.state_paths.sync_boundary_path),
            "sync_boundary_present": boundary is not None,
            "sync_boundary_mode": "incremental" if use_incremental_boundary else "full_refresh",
            "sync_boundary_schema_version": SYNC_BOUNDARY_SCHEMA_VERSION,
            "sync_boundary_account_match": None if boundary is None else boundary.account_id_hint == account_id,
            "refresh_token_present": session.state_paths.refresh_token_path.exists(),
            "device_id_present": session.state_paths.device_id_path.exists(),
            "device_type_hint": session.token.device_type,
            "history_count": len(history_entries),
            "history_pages_fetched": history_pages_fetched,
            "history_stopped_early": history_stopped_early,
            "history_boundary_marker_count": len(history_markers),
            "watchlist_count": len(watchlist_entries),
            "watchlist_pages_fetched": watchlist_pages_fetched,
            "watchlist_stopped_early": watchlist_stopped_early,
            "watchlist_boundary_marker_count": len(watchlist_markers),
            "transport": "curl_cffi:chrome124" if curl_requests is not None else "requests",
            "request_spacing_seconds": config.crunchyroll.request_spacing_seconds,
            "request_spacing_jitter_seconds": config.crunchyroll.request_spacing_jitter_seconds,
            "auth_source": session.auth_source,
        },
    )
    _write_sync_boundary(
        state_paths=session.state_paths,
        generated_at=generated_at,
        account_id_hint=account_id,
        history_entries=history_entries,
        watchlist_entries=watchlist_data,
    )
    _write_session_state(
        state_paths=session.state_paths,
        profile=session.profile,
        locale=config.crunchyroll.locale,
        device_type=session.token.device_type,
        account_id=account_id,
        last_error=None,
        success=True,
        phase="python_live_snapshot",
    )
    return CrunchyrollFetchResult(
        snapshot=snapshot,
        state_paths=session.state_paths,
        account_email=session.account_email,
    )


def fetch_snapshot(
    config: AppConfig,
    *,
    profile: str = "default",
    timeout_seconds: float = 30.0,
    use_incremental_boundary: bool = True,
) -> CrunchyrollFetchResult:
    pacer = _CrunchyrollRequestPacer(
        config.crunchyroll.request_spacing_seconds,
        jitter_seconds=config.crunchyroll.request_spacing_jitter_seconds,
    )
    session = _start_auth_session(
        config,
        profile=profile,
        timeout_seconds=timeout_seconds,
        pacer=pacer,
    )
    return _fetch_snapshot_once(session, use_incremental_boundary=use_incremental_boundary)


def snapshot_to_dict(snapshot: CrunchyrollSnapshot) -> dict[str, Any]:
    return {
        "contract_version": snapshot.contract_version,
        "generated_at": snapshot.generated_at,
        "provider": snapshot.provider,
        "account_id_hint": snapshot.account_id_hint,
        "series": [asdict(item) for item in snapshot.series],
        "progress": [asdict(item) for item in snapshot.progress],
        "watchlist": [asdict(item) for item in snapshot.watchlist],
        "raw": snapshot.raw,
    }


def write_snapshot_file(path: Path, snapshot: CrunchyrollSnapshot) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(snapshot_to_dict(snapshot), indent=2) + "\n", encoding="utf-8")
    return path
