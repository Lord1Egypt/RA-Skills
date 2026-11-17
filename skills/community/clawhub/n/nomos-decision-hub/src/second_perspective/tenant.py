"""Tenant isolation context (v0.5 enterprise control plane).

NOMOS supports multi-tenant deployments. The active tenant identity is carried
in a :mod:`contextvars` contextvar so persistence layers can partition data
without threading ``tenant_id`` through every call signature. The API middleware
resolves the tenant from the ``X-Tenant-Id`` request header, or — when OIDC is
enabled and authorization is enforced — from the ``tid`` claim. When unset it
defaults to the global tenant ``""``.
"""

from __future__ import annotations

import contextvars

TENANT_HEADER = "X-Tenant-Id"

_active_tenant: contextvars.ContextVar[str] = contextvars.ContextVar(
    "nomos_tenant", default=""
)


def set_tenant(tenant_id: str | None) -> contextvars.Token:
    return _active_tenant.set(tenant_id or "")


def get_tenant() -> str:
    return _active_tenant.get()


def reset_tenant(token: contextvars.Token) -> None:
    _active_tenant.reset(token)


def resolve_tenant_from_claims(claims: dict | None) -> str:
    """Extract a tenant id from verified OIDC claims, if present."""
    if not claims:
        return ""
    for key in ("tid", "tenant_id", "https://nomos.ai/tenant"):
        value = claims.get(key)
        if value:
            return str(value)
    return ""
