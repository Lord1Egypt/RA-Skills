"""API security — API key verification and OIDC token validation.

Supports two authentication modes:
  - API key (production default): Bearer token must match SP_API_KEY.
  - OIDC (optional): JWT bearer token verified against the configured issuer.
  - Development mode (SP_ENV=development): keyless access.
"""

from __future__ import annotations

import logging
import os

from fastapi import Header, HTTPException, status

logger = logging.getLogger(__name__)


def assert_auth_configured() -> None:
    """Fail fast if production mode has no authentication configured.

    Called at module import time.  Raises SystemExit if the production
    environment is not properly configured.
    """
    env = os.getenv("SP_ENV", "development").strip().lower()
    if env == "production":
        api_key = os.getenv("SP_API_KEY", "").strip()
        oidc_issuer = os.getenv("SP_OIDC_ISSUER", "").strip()
        if not api_key and not oidc_issuer:
            raise SystemExit(
                "FATAL: SP_ENV=production but neither SP_API_KEY nor SP_OIDC_ISSUER is set. "
                "Refusing to start without authentication."
            )
        if not api_key:
            logger.info("production mode: SP_API_KEY not set, OIDC-only auth will be enforced")
        else:
            logger.info("production mode: API key authentication configured")


def verify_api_key(authorization: str | None = Header(default=None)) -> None:
    """FastAPI dependency: verify the Bearer token.

    In development mode, any request (including unauthenticated) is allowed.
    In production mode, the Bearer token must match SP_API_KEY or be a valid
    OIDC JWT (if OIDC is configured).
    """
    env = os.getenv("SP_ENV", "development").strip().lower()
    if env == "development":
        return  # keyless access in development

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.casefold() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Expected: Bearer <token>",
        )

    # API key check
    api_key = os.getenv("SP_API_KEY", "").strip()
    if api_key and token == api_key:
        return

    # OIDC check (if configured)
    oidc_issuer = os.getenv("SP_OIDC_ISSUER", "").strip()
    if oidc_issuer:
        try:
            config = _get_oidc_config()
            if config is not None:
                claims = _verify_oidc_token(token, config)
                if claims is not None:
                    return
        except Exception:
            pass

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token",
    )


def _get_oidc_config() -> dict | None:
    """Fetch OIDC configuration from the configured issuer.

    Returns a dict with 'jwks_uri' and 'issuer' keys, or None on failure.
    """
    import requests

    issuer = os.getenv("SP_OIDC_ISSUER", "").strip()
    if not issuer:
        return None

    config_url = f"{issuer.rstrip('/')}/.well-known/openid-configuration"
    try:
        resp = requests.get(config_url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return {
            "issuer": data.get("issuer", issuer),
            "jwks_uri": data.get("jwks_uri", ""),
            "audience": os.getenv("SP_OIDC_AUDIENCE", ""),
        }
    except Exception as exc:
        logger.warning("failed to fetch OIDC config from %s: %s", config_url, exc)
        return None


def _verify_oidc_token(token: str, config: dict) -> dict | None:
    """Verify a JWT against the OIDC provider's JWKS.

    Returns the verified claims dict, or None if verification fails.
    """
    from jose import jwt as jose_jwt
    from jose.exceptions import JWTError

    try:
        jwks_uri = config.get("jwks_uri", "")
        if not jwks_uri:
            return None

        import requests

        resp = requests.get(jwks_uri, timeout=5)
        resp.raise_for_status()
        jwks = resp.json()

        audience = config.get("audience", "") or None
        claims = jose_jwt.decode(
            token,
            jwks,
            audience=audience,
            issuer=config.get("issuer"),
            options={"verify_at_hash": False},
        )
        return claims
    except (JWTError, requests.RequestException) as exc:
        logger.warning("OIDC token verification failed: %s", exc)
        return None