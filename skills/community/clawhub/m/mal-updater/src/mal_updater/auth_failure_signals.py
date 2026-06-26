from __future__ import annotations

from collections.abc import Mapping

AUTH_STYLE_FAILURE_MARKERS = (
    "http 401",
    "http 403",
    "unauthor",
    "forbidden",
    "auth_failed",
    "invalid_grant",
    "invalid token",
    "expired token",
    "token refresh",
    "refresh token",
    "missing mal refresh material",
    "missing crunchyroll refresh token",
    "missing hidive refresh token",
    "credential_rebootstrap",
    "login failed",
    "login did not return",
    "did not return a json object",
    "did not return both access_token and refresh_token",
    "did not return both authorisationtoken and refreshtoken",
    "did not return authorisationtoken",
    "did not return refreshtoken",
    "bearer",
)

AUTH_STYLE_SESSION_PHASES = {
    "auth_failed",
    "auth_retrying_with_refresh_token",
    "auth_retrying_with_credentials",
}


def looks_auth_style_failure(reason: str, *, session_residue: Mapping[str, object] | None = None) -> bool:
    lowered = reason.lower()
    if any(marker in lowered for marker in AUTH_STYLE_FAILURE_MARKERS):
        return True
    if isinstance(session_residue, Mapping):
        if isinstance(session_residue.get("session_phase"), str):
            return True
        session_last_error = session_residue.get("session_last_error")
        if isinstance(session_last_error, str):
            lowered_session_error = session_last_error.lower()
            if any(marker in lowered_session_error for marker in AUTH_STYLE_FAILURE_MARKERS):
                return True
    return False
