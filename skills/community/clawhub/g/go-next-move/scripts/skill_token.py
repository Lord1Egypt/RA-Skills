#!/usr/bin/env python3
"""Stateless signed tokens for the Go Next Move HTTP service.

A token is a short, URL-safe string that carries an expiry timestamp and an
HMAC signature. The server can validate a token without keeping any per-token
state: it only needs the shared secret. To revoke every outstanding link,
rotate the secret. A fresh link is just a fresh token signed with the same
secret.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from pathlib import Path

DEFAULT_TTL_SECONDS = 5 * 60 * 60  # 5 hours
DEFAULT_STATE_DIR = Path.home() / ".go-next-move"
DEFAULT_SECRET_PATH = DEFAULT_STATE_DIR / "secret"
SECRET_ENV = "GO_NEXT_MOVE_SECRET"


def _b64encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _b64decode(text: str) -> bytes:
    padding = "=" * (-len(text) % 4)
    return base64.urlsafe_b64decode(text + padding)


def load_or_create_secret(path: Path = DEFAULT_SECRET_PATH) -> str:
    """Return a stable secret, preferring the environment, then a secret file.

    The first run writes a freshly generated secret to ``path`` (chmod 600) so
    later launches reuse it and previously issued tokens keep validating.
    """
    env_secret = os.environ.get(SECRET_ENV)
    if env_secret:
        return env_secret

    path = Path(path)
    if path.exists():
        secret = path.read_text(encoding="utf-8").strip()
        if secret:
            return secret

    secret = secrets.token_urlsafe(32)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(secret, encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass
    return secret


def rotate_secret(path: Path = DEFAULT_SECRET_PATH) -> str:
    """Generate and persist a new secret, invalidating all existing tokens."""
    path = Path(path)
    secret = secrets.token_urlsafe(32)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(secret, encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass
    return secret


def _sign(secret: str, payload_b64: str) -> str:
    signature = hmac.new(
        secret.encode("utf-8"), payload_b64.encode("ascii"), hashlib.sha256
    ).digest()
    return _b64encode(signature)


def mint_token(secret: str, ttl_seconds: int = DEFAULT_TTL_SECONDS) -> str:
    """Create a signed token that expires ``ttl_seconds`` from now."""
    now = int(time.time())
    payload = {
        "iat": now,
        "exp": now + int(ttl_seconds),
        "nonce": secrets.token_hex(8),
    }
    payload_b64 = _b64encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signature_b64 = _sign(secret, payload_b64)
    return f"{payload_b64}.{signature_b64}"


def verify_token(secret: str, token: str) -> dict | None:
    """Return the decoded payload if the token is valid and unexpired, else None."""
    if not token or "." not in token:
        return None
    payload_b64, _, signature_b64 = token.partition(".")
    expected = _sign(secret, payload_b64)
    if not hmac.compare_digest(expected, signature_b64):
        return None
    try:
        payload = json.loads(_b64decode(payload_b64).decode("utf-8"))
    except (ValueError, json.JSONDecodeError):
        return None
    exp = payload.get("exp")
    if not isinstance(exp, int) or time.time() > exp:
        return None
    return payload


def token_remaining_seconds(payload: dict) -> int:
    return max(0, int(payload.get("exp", 0)) - int(time.time()))
