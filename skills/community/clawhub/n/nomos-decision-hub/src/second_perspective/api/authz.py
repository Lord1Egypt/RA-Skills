"""Authorization enforcement (v0.5).

Complements authentication (``api.security.verify_api_key`` / OIDC verify) with
*authorization*: which scopes a verified identity may exercise. Enforcement is
opt-in via ``SP_AUTHZ_ENFORCE=true`` so existing deployments that rely only on
API-key authentication keep working unchanged. When enabled, the API resolves
the verified OIDC identity and checks the required scope on write endpoints.
"""

from __future__ import annotations

import os

from fastapi import HTTPException, Request, status


def authz_enforced() -> bool:
    return os.getenv("SP_AUTHZ_ENFORCE", "").strip().lower() in ("1", "true", "yes")


def _scopes_for(request: Request) -> set[str]:
    claims = getattr(request.state, "oidc_claims", None)
    if not claims:
        return set()
    raw = claims.get("scope") or claims.get("scopes") or ""
    if isinstance(raw, str):
        return set(raw.split())
    if isinstance(raw, list):
        return set(raw)
    return set()


def require_scope(scope: str):
    """FastAPI dependency factory enforcing a required scope (opt-in)."""

    def dependency(request: Request) -> None:
        if not authz_enforced():
            return
        if scope not in _scopes_for(request):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required scope: {scope}",
            )

    return dependency
