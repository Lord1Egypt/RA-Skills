from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

from .auth import write_secret_file
from .config import AppConfig, _read_secret_file, _resolve_secret_path
from .request_tracking import record_api_request_event

HIDIVE_API_BASE_URL = "https://dce-frontoffice.imggaming.com/api/v2"
HIDIVE_REALM = "dce.hidive"
HIDIVE_APP = "dice"
HIDIVE_APP_VERSION = "6.60.0"
HIDIVE_API_KEY = "857a1e5d-e35e-4fdf-805b-a87b6f8364bf"
DEFAULT_HIDIVE_USERNAME_FILE = "hidive_username.txt"
DEFAULT_HIDIVE_PASSWORD_FILE = "hidive_password.txt"
HIDIVE_REFRESH_WINDOW_SECONDS = 90


class HidiveAuthError(RuntimeError):
    pass


@dataclass(slots=True)
class HidiveCredentials:
    username: str | None
    password: str | None
    username_path: Path
    password_path: Path


@dataclass(slots=True)
class HidiveStatePaths:
    root: Path
    access_token_path: Path
    refresh_token_path: Path
    session_state_path: Path
    sync_boundary_path: Path


@dataclass(slots=True)
class HidiveBootstrapResult:
    profile: str
    username_path: Path
    password_path: Path
    access_token_path: Path
    refresh_token_path: Path
    session_state_path: Path
    account_id: str | None
    account_name: str | None
    authorisation_token: str
    refresh_token: str


@dataclass(slots=True)
class HidiveTokenSet:
    authorisation_token: str
    refresh_token: str
    account_id: str | None = None
    account_name: str | None = None


@dataclass(slots=True)
class HidiveSession:
    config: AppConfig
    profile: str
    state_paths: HidiveStatePaths
    token: HidiveTokenSet
    credential_rebootstrap_attempted: bool = False

    def default_headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "x-api-key": HIDIVE_API_KEY,
            "app": HIDIVE_APP,
            "x-app-var": HIDIVE_APP_VERSION,
            "Realm": HIDIVE_REALM,
            "Origin": "https://www.hidive.com",
            "Referer": "https://www.hidive.com/",
            "Authorization": f"Bearer {self.token.authorisation_token}",
        }

    def ensure_fresh_tokens(self, *, timeout_seconds: float | None = None) -> None:
        seconds_remaining = _seconds_until_jwt_expiry(self.token.authorisation_token)
        if seconds_remaining is None:
            return
        if seconds_remaining <= HIDIVE_REFRESH_WINDOW_SECONDS:
            self.refresh_tokens(timeout_seconds=timeout_seconds)

    def json_get(self, path: str, *, params: dict[str, Any] | None = None, timeout_seconds: float | None = None) -> Any:
        self.ensure_fresh_tokens(timeout_seconds=timeout_seconds)
        try:
            return _hidive_json_request(
                self.config,
                "GET",
                path,
                headers=self.default_headers(),
                params=params,
                timeout_seconds=timeout_seconds,
            )
        except HidiveAuthError as exc:
            message = str(exc)
            if "HTTP 401" not in message:
                raise
            self.refresh_tokens(timeout_seconds=timeout_seconds)
            return _hidive_json_request(
                self.config,
                "GET",
                path,
                headers=self.default_headers(),
                params=params,
                timeout_seconds=timeout_seconds,
            )

    def refresh_tokens(self, *, timeout_seconds: float | None = None) -> None:
        try:
            payload = _hidive_json_request(
                self.config,
                "POST",
                "/token/refresh",
                headers=self.default_headers(),
                json_body={"refreshToken": self.token.refresh_token},
                timeout_seconds=timeout_seconds,
            )
            if not isinstance(payload, dict):
                raise HidiveAuthError("HIDIVE token refresh did not return a JSON object")
            authorisation_token = payload.get("authorisationToken")
            refresh_token = payload.get("refreshToken") or self.token.refresh_token
            if not isinstance(authorisation_token, str):
                raise HidiveAuthError("HIDIVE token refresh did not return authorisationToken")
            if not isinstance(refresh_token, str):
                raise HidiveAuthError("HIDIVE token refresh did not return refreshToken")
            self.token.authorisation_token = authorisation_token
            self.token.refresh_token = refresh_token
            write_secret_file(self.state_paths.access_token_path, authorisation_token)
            write_secret_file(self.state_paths.refresh_token_path, refresh_token)
            _write_session_state(
                state_paths=self.state_paths,
                profile=self.profile,
                account_id=self.token.account_id,
                account_name=self.token.account_name,
                last_error=None,
                success=True,
                phase="ready",
            )
            return
        except HidiveAuthError as refresh_exc:
            if self.credential_rebootstrap_attempted:
                raise
            bootstrap = hidive_login_with_credentials(
                self.config,
                profile=self.profile,
                timeout_seconds=timeout_seconds,
                verify_account=True,
            )
            self.token.authorisation_token = bootstrap.authorisation_token
            self.token.refresh_token = bootstrap.refresh_token
            self.token.account_id = bootstrap.account_id
            self.token.account_name = bootstrap.account_name
            self.credential_rebootstrap_attempted = True


def _now_string() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _decode_jwt_payload(token: str) -> dict[str, Any] | None:
    parts = token.split('.')
    if len(parts) < 2:
        return None
    payload_part = parts[1] + ('=' * ((4 - len(parts[1]) % 4) % 4))
    try:
        decoded = base64.urlsafe_b64decode(payload_part.encode()).decode()
        payload = json.loads(decoded)
    except Exception:
        return None
    return payload if isinstance(payload, dict) else None


def _jwt_expiry_epoch(token: str) -> int | None:
    payload = _decode_jwt_payload(token)
    exp = payload.get('exp') if isinstance(payload, dict) else None
    return int(exp) if isinstance(exp, (int, float)) else None


def _seconds_until_jwt_expiry(token: str, *, now_epoch: int | None = None) -> int | None:
    exp = _jwt_expiry_epoch(token)
    if exp is None:
        return None
    current = now_epoch if now_epoch is not None else int(datetime.now(timezone.utc).timestamp())
    return exp - current


def resolve_hidive_state_paths(config: AppConfig, profile: str = "default") -> HidiveStatePaths:
    root = config.state_dir / "hidive" / profile
    return HidiveStatePaths(
        root=root,
        access_token_path=root / "authorisation_token.txt",
        refresh_token_path=root / "refresh_token.txt",
        session_state_path=root / "session.json",
        sync_boundary_path=root / "sync_boundary.json",
    )


def load_hidive_credentials(config: AppConfig) -> HidiveCredentials:
    secret_files = config.secret_files
    username_path = _resolve_secret_path(
        "MAL_UPDATER_HIDIVE_USERNAME_FILE",
        secret_files,
        "hidive_username",
        secrets_dir=config.secrets_dir,
        default_file=DEFAULT_HIDIVE_USERNAME_FILE,
    )
    password_path = _resolve_secret_path(
        "MAL_UPDATER_HIDIVE_PASSWORD_FILE",
        secret_files,
        "hidive_password",
        secrets_dir=config.secrets_dir,
        default_file=DEFAULT_HIDIVE_PASSWORD_FILE,
    )
    return HidiveCredentials(
        username=os.getenv("MAL_UPDATER_HIDIVE_USERNAME") or _read_secret_file(username_path),
        password=os.getenv("MAL_UPDATER_HIDIVE_PASSWORD") or _read_secret_file(password_path),
        username_path=username_path,
        password_path=password_path,
    )


def _write_session_state(
    *,
    state_paths: HidiveStatePaths,
    profile: str,
    account_id: str | None,
    account_name: str | None,
    last_error: str | None,
    success: bool,
    phase: str,
) -> None:
    state_paths.root.mkdir(parents=True, exist_ok=True)
    payload = {
        "profile": profile,
        "authorisation_token_present": state_paths.access_token_path.exists(),
        "refresh_token_present": state_paths.refresh_token_path.exists(),
        "last_login_attempt_at": _now_string(),
        "last_login_success_at": _now_string() if success else None,
        "last_account_id_hint": account_id,
        "last_account_name_hint": account_name,
        "last_error": last_error,
        "hidive_phase": phase,
    }
    state_paths.session_state_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    os.chmod(state_paths.session_state_path, 0o600)


def _hidive_json_request(
    config: AppConfig,
    method: str,
    path: str,
    *,
    headers: dict[str, str],
    params: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
    timeout_seconds: float | None = None,
) -> Any:
    url = f"{HIDIVE_API_BASE_URL}{path}"
    timeout = timeout_seconds or config.request_timeout_seconds
    try:
        response = requests.request(method, url, headers=headers, params=params, json=json_body, timeout=timeout)
        record_api_request_event(
            "hidive",
            f"http_{method.lower()}",
            url=url,
            method=method,
            outcome="ok" if response.status_code < 400 else "http_error",
            status_code=response.status_code,
            config=config,
        )
    except requests.RequestException as exc:
        record_api_request_event(
            "hidive",
            f"http_{method.lower()}",
            url=url,
            method=method,
            outcome="request_error",
            error=str(exc),
            config=config,
        )
        raise HidiveAuthError(f"HIDIVE {method} {path} request failed: {exc}") from exc

    if response.status_code >= 400:
        detail = response.text.strip()[:800]
        raise HidiveAuthError(f"HIDIVE {method} {path} failed: HTTP {response.status_code}: {detail}")
    try:
        return response.json()
    except ValueError as exc:
        raise HidiveAuthError(f"HIDIVE {method} {path} did not return JSON") from exc


def _load_profile(config: AppConfig, authorisation_token: str, *, timeout_seconds: float) -> tuple[str | None, str | None]:
    payload = _hidive_json_request(
        config,
        "GET",
        "/user/profile",
        headers={
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "x-api-key": HIDIVE_API_KEY,
            "app": HIDIVE_APP,
            "x-app-var": HIDIVE_APP_VERSION,
            "Realm": HIDIVE_REALM,
            "Origin": "https://www.hidive.com",
            "Referer": "https://www.hidive.com/",
            "Authorization": f"Bearer {authorisation_token}",
        },
        timeout_seconds=timeout_seconds,
    )
    if not isinstance(payload, dict):
        return None, None
    account_id = payload.get("id")
    account_name = payload.get("displayName") or payload.get("username") or payload.get("email")
    return str(account_id) if account_id is not None else None, str(account_name) if account_name is not None else None


def hidive_login_with_credentials(
    config: AppConfig,
    *,
    profile: str = "default",
    timeout_seconds: float | None = None,
    verify_account: bool = True,
) -> HidiveBootstrapResult:
    credentials = load_hidive_credentials(config)
    if not credentials.username:
        raise HidiveAuthError(f"Missing HIDIVE username/email at {credentials.username_path}")
    if not credentials.password:
        raise HidiveAuthError(f"Missing HIDIVE password at {credentials.password_path}")

    state_paths = resolve_hidive_state_paths(config, profile=profile)
    try:
        token_payload = _hidive_json_request(
            config,
            "POST",
            "/login",
            headers={
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json",
                "x-api-key": HIDIVE_API_KEY,
                "app": HIDIVE_APP,
                "x-app-var": HIDIVE_APP_VERSION,
                "Realm": HIDIVE_REALM,
                "Origin": "https://www.hidive.com",
                "Referer": "https://www.hidive.com/login",
            },
            json_body={"id": credentials.username, "secret": credentials.password},
            timeout_seconds=timeout_seconds,
        )
    except HidiveAuthError as exc:
        _write_session_state(
            state_paths=state_paths,
            profile=profile,
            account_id=None,
            account_name=None,
            last_error=str(exc),
            success=False,
            phase="auth_failed",
        )
        raise

    if not isinstance(token_payload, dict):
        raise HidiveAuthError("HIDIVE login did not return a JSON object")
    authorisation_token = token_payload.get("authorisationToken")
    refresh_token = token_payload.get("refreshToken")
    if not isinstance(authorisation_token, str) or not isinstance(refresh_token, str):
        message = "HIDIVE login succeeded but did not return both authorisationToken and refreshToken"
        _write_session_state(
            state_paths=state_paths,
            profile=profile,
            account_id=None,
            account_name=None,
            last_error=message,
            success=False,
            phase="auth_failed",
        )
        raise HidiveAuthError(message)

    account_id = None
    account_name = None
    if verify_account:
        try:
            account_id, account_name = _load_profile(config, authorisation_token, timeout_seconds=timeout_seconds or config.request_timeout_seconds)
        except HidiveAuthError as exc:
            _write_session_state(
                state_paths=state_paths,
                profile=profile,
                account_id=None,
                account_name=None,
                last_error=str(exc),
                success=False,
                phase="auth_failed",
            )
            raise

    write_secret_file(state_paths.access_token_path, authorisation_token)
    write_secret_file(state_paths.refresh_token_path, refresh_token)
    _write_session_state(
        state_paths=state_paths,
        profile=profile,
        account_id=account_id,
        account_name=account_name,
        last_error=None,
        success=True,
        phase="ready",
    )
    return HidiveBootstrapResult(
        profile=profile,
        username_path=credentials.username_path,
        password_path=credentials.password_path,
        access_token_path=state_paths.access_token_path,
        refresh_token_path=state_paths.refresh_token_path,
        session_state_path=state_paths.session_state_path,
        account_id=account_id,
        account_name=account_name,
        authorisation_token=authorisation_token,
        refresh_token=refresh_token,
    )


def start_hidive_session(
    config: AppConfig,
    *,
    profile: str = "default",
    timeout_seconds: float | None = None,
) -> HidiveSession:
    state_paths = resolve_hidive_state_paths(config, profile=profile)
    authorisation_token = _read_secret_file(state_paths.access_token_path)
    refresh_token = _read_secret_file(state_paths.refresh_token_path)
    if not authorisation_token or not refresh_token:
        bootstrap = hidive_login_with_credentials(
            config,
            profile=profile,
            timeout_seconds=timeout_seconds,
            verify_account=True,
        )
        authorisation_token = bootstrap.authorisation_token
        refresh_token = bootstrap.refresh_token
        account_id = bootstrap.account_id
        account_name = bootstrap.account_name
    else:
        account_id = None
        account_name = None
    return HidiveSession(
        config=config,
        profile=profile,
        state_paths=state_paths,
        token=HidiveTokenSet(
            authorisation_token=authorisation_token,
            refresh_token=refresh_token,
            account_id=account_id,
            account_name=account_name,
        ),
    )
