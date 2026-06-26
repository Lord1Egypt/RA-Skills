from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

try:
    from curl_cffi import requests as curl_requests
except ModuleNotFoundError:  # pragma: no cover - optional runtime dependency
    curl_requests = None

from .auth import write_secret_file
from .config import AppConfig, _read_secret_file, _resolve_secret_path
from .request_tracking import record_api_request_event

CRUNCHYROLL_TOKEN_URL = "https://www.crunchyroll.com/auth/v1/token"
CRUNCHYROLL_ME_URL = "https://www.crunchyroll.com/accounts/v1/me"
CRUNCHYROLL_BASIC_AUTH_TOKEN = "dC1rZGdwMmg4YzNqdWI4Zm4wZnE6eWZMRGZNZnJZdktYaDRKWFMxTEVJMmNDcXUxdjVXYW4="
DEFAULT_CRUNCHYROLL_USERNAME_FILE = "crunchyroll_username.txt"
DEFAULT_CRUNCHYROLL_PASSWORD_FILE = "crunchyroll_password.txt"
DEFAULT_CRUNCHYROLL_DEVICE_TYPE = "ANDROIDTV"


class CrunchyrollAuthError(RuntimeError):
    pass


@dataclass(slots=True)
class CrunchyrollCredentials:
    username: str | None
    password: str | None
    username_path: Path
    password_path: Path


@dataclass(slots=True)
class CrunchyrollStatePaths:
    root: Path
    refresh_token_path: Path
    device_id_path: Path
    session_state_path: Path
    sync_boundary_path: Path


@dataclass(slots=True)
class CrunchyrollBootstrapResult:
    profile: str
    locale: str
    username_path: Path
    password_path: Path
    refresh_token_path: Path
    device_id_path: Path
    session_state_path: Path
    account_id: str | None
    account_email: str | None
    access_token: str
    refresh_token: str
    device_id: str
    device_type: str


def _now_string() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_crunchyroll_state_paths(config: AppConfig, profile: str = "default") -> CrunchyrollStatePaths:
    root = config.state_dir / "crunchyroll" / profile
    return CrunchyrollStatePaths(
        root=root,
        refresh_token_path=root / "refresh_token.txt",
        device_id_path=root / "device_id.txt",
        session_state_path=root / "session.json",
        sync_boundary_path=root / "sync_boundary.json",
    )


def load_crunchyroll_credentials(config: AppConfig) -> CrunchyrollCredentials:
    secret_files = config.secret_files
    username_path = _resolve_secret_path(
        "MAL_UPDATER_CRUNCHYROLL_USERNAME_FILE",
        secret_files,
        "crunchyroll_username",
        secrets_dir=config.secrets_dir,
        default_file=DEFAULT_CRUNCHYROLL_USERNAME_FILE,
    )
    password_path = _resolve_secret_path(
        "MAL_UPDATER_CRUNCHYROLL_PASSWORD_FILE",
        secret_files,
        "crunchyroll_password",
        secrets_dir=config.secrets_dir,
        default_file=DEFAULT_CRUNCHYROLL_PASSWORD_FILE,
    )
    return CrunchyrollCredentials(
        username=os.getenv("MAL_UPDATER_CRUNCHYROLL_USERNAME") or _read_secret_file(username_path),
        password=os.getenv("MAL_UPDATER_CRUNCHYROLL_PASSWORD") or _read_secret_file(password_path),
        username_path=username_path,
        password_path=password_path,
    )


def _write_session_state(
    *,
    state_paths: CrunchyrollStatePaths,
    profile: str,
    locale: str,
    device_type: str,
    account_id: str | None,
    last_error: str | None,
    success: bool,
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
        "crunchyroll_phase": "ready" if success else "auth_failed",
    }
    state_paths.session_state_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    os.chmod(state_paths.session_state_path, 0o600)


def _http_post(url: str, *, data: dict[str, str], headers: dict[str, str], timeout_seconds: float):
    if curl_requests is not None:
        return curl_requests.post(url, data=data, headers=headers, timeout=timeout_seconds, impersonate="chrome124")
    return requests.post(url, data=data, headers=headers, timeout=timeout_seconds)



def _http_get(url: str, *, headers: dict[str, str], timeout_seconds: float):
    if curl_requests is not None:
        return curl_requests.get(url, headers=headers, timeout=timeout_seconds, impersonate="chrome124")
    return requests.get(url, headers=headers, timeout=timeout_seconds)



def crunchyroll_login_with_credentials(
    config: AppConfig,
    *,
    profile: str = "default",
    timeout_seconds: float = 30.0,
    verify_account: bool = True,
) -> CrunchyrollBootstrapResult:
    credentials = load_crunchyroll_credentials(config)
    if not credentials.username:
        raise CrunchyrollAuthError(f"Missing Crunchyroll username/email at {credentials.username_path}")
    if not credentials.password:
        raise CrunchyrollAuthError(f"Missing Crunchyroll password at {credentials.password_path}")

    state_paths = resolve_crunchyroll_state_paths(config, profile=profile)
    existing_device_id = _read_secret_file(state_paths.device_id_path)
    device_id = existing_device_id or str(uuid.uuid4())
    device_type = DEFAULT_CRUNCHYROLL_DEVICE_TYPE

    body = {
        "username": credentials.username,
        "password": credentials.password,
        "grant_type": "password",
        "scope": "offline_access",
        "device_id": device_id,
        "device_type": device_type,
    }
    headers = {
        "Authorization": f"Basic {CRUNCHYROLL_BASIC_AUTH_TOKEN}",
        "Content-Type": "application/x-www-form-urlencoded",
        "ETP-Anonymous-ID": device_id,
    }

    response = _http_post(CRUNCHYROLL_TOKEN_URL, data=body, headers=headers, timeout_seconds=timeout_seconds)
    if response.status_code >= 400:
        message = f"Crunchyroll credential login failed: HTTP {response.status_code}"
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
                message = f"Crunchyroll credential login failed: {error or 'unknown_error'} - {error_description or 'no description'}"
        _write_session_state(
            state_paths=state_paths,
            profile=profile,
            locale=config.crunchyroll.locale,
            device_type=device_type,
            account_id=None,
            last_error=message,
            success=False,
        )
        raise CrunchyrollAuthError(message)

    token_payload = response.json()
    access_token = token_payload.get("access_token")
    refresh_token = token_payload.get("refresh_token")
    account_id = token_payload.get("account_id")
    if not access_token or not refresh_token:
        message = "Crunchyroll credential login succeeded but did not return both access_token and refresh_token"
        _write_session_state(
            state_paths=state_paths,
            profile=profile,
            locale=config.crunchyroll.locale,
            device_type=device_type,
            account_id=account_id,
            last_error=message,
            success=False,
        )
        raise CrunchyrollAuthError(message)

    account_email = None
    if verify_account:
        me_response = _http_get(
            CRUNCHYROLL_ME_URL,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout_seconds=timeout_seconds,
        )
        if me_response.status_code >= 400:
            message = f"Crunchyroll /accounts/v1/me verification failed: HTTP {me_response.status_code}"
            _write_session_state(
                state_paths=state_paths,
                profile=profile,
                locale=config.crunchyroll.locale,
                device_type=device_type,
                account_id=account_id,
                last_error=message,
                success=False,
            )
            raise CrunchyrollAuthError(message)
        me_payload = me_response.json()
        if isinstance(me_payload, dict):
            account_id = str(me_payload.get("account_id") or account_id or "") or None
            account_email = me_payload.get("email")

    write_secret_file(state_paths.refresh_token_path, refresh_token)
    write_secret_file(state_paths.device_id_path, device_id)
    _write_session_state(
        state_paths=state_paths,
        profile=profile,
        locale=config.crunchyroll.locale,
        device_type=device_type,
        account_id=account_id,
        last_error=None,
        success=True,
    )

    return CrunchyrollBootstrapResult(
        profile=profile,
        locale=config.crunchyroll.locale,
        username_path=credentials.username_path,
        password_path=credentials.password_path,
        refresh_token_path=state_paths.refresh_token_path,
        device_id_path=state_paths.device_id_path,
        session_state_path=state_paths.session_state_path,
        account_id=account_id,
        account_email=account_email,
        access_token=str(access_token),
        refresh_token=str(refresh_token),
        device_id=device_id,
        device_type=device_type,
    )
