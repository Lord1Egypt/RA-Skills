#!/usr/bin/env python3
"""Shared utilities for LMail ops scripts."""

from __future__ import annotations

import base64
import hashlib
import json
import os
from pathlib import Path
from typing import Any
from urllib import error, request


class LMailHttpError(RuntimeError):
    """Raised for request, envelope, or workflow errors."""


def mask_secret(value: str | None, left: int = 6, right: int = 4) -> str:
    if not value:
        return ""
    if len(value) <= left + right:
        return "*" * len(value)
    return f"{value[:left]}...{value[-right:]}"


def load_json_file(path: str) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def save_json_file(path: str, payload: dict[str, Any]) -> None:
    p = Path(path)
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    try:
        os.chmod(p, 0o600)
    except OSError:
        pass


def _b64url_decode(segment: str) -> bytes:
    padded = segment + "=" * ((4 - len(segment) % 4) % 4)
    return base64.urlsafe_b64decode(padded.encode("ascii"))


def decode_jwt_payload(token: str) -> dict[str, Any]:
    parts = token.split(".")
    if len(parts) != 3:
        raise LMailHttpError("Invalid JWT format")
    try:
        return json.loads(_b64url_decode(parts[1]).decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise LMailHttpError(f"Failed to decode JWT payload: {exc}") from exc


def request_json(
    url: str,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
    timeout: int = 20,
) -> tuple[int, dict[str, Any]]:
    req_headers = dict(headers or {})
    body = None

    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        req_headers.setdefault("Content-Type", "application/json")

    req = request.Request(url=url, data=body, method=method, headers=req_headers)

    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            status = resp.status
    except error.HTTPError as http_err:
        status = http_err.code
        raw = http_err.read().decode("utf-8")
    except error.URLError as url_err:
        raise LMailHttpError(f"Network error for {method} {url}: {url_err}") from url_err

    try:
        parsed = json.loads(raw) if raw else {}
    except json.JSONDecodeError:
        parsed = {"raw": raw}

    return status, parsed


def expect_success(response: dict[str, Any], context: str) -> dict[str, Any]:
    if not isinstance(response, dict):
        raise LMailHttpError(f"{context}: non-JSON response")

    if response.get("success") is True:
        return response.get("data") or {}

    error_obj = response.get("error") or {}
    code = error_obj.get("code", "UNKNOWN_ERROR")
    message = error_obj.get("message", "Unknown API error")
    details = error_obj.get("details")
    if details:
        raise LMailHttpError(f"{context}: {code} - {message} ({details})")
    raise LMailHttpError(f"{context}: {code} - {message}")


def auth_headers(token: str | None = None, api_key: str | None = None) -> dict[str, str]:
    if token:
        return {"Authorization": f"Bearer {token}"}
    if api_key:
        return {"Authorization": f"ApiKey {api_key}"}
    raise LMailHttpError("Missing auth: provide token or api key")


def solve_pow(
    jti: str,
    salt: str,
    difficulty: int,
    max_iterations: int,
    start_nonce: int = 0,
) -> dict[str, Any]:
    if difficulty < 1:
        raise LMailHttpError("difficulty must be >= 1")

    prefix = "0" * difficulty
    nonce = start_nonce

    for attempt in range(1, max_iterations + 1):
        material = f"{jti}:{salt}:{nonce}"
        digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
        if digest.startswith(prefix):
            return {
                "nonce": nonce,
                "hash": digest,
                "attempts": attempt,
                "difficulty": difficulty,
            }
        nonce += 1

    raise LMailHttpError(
        f"PoW solution not found after {max_iterations} attempts; increase max_iterations"
    )


def json_pretty(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=True)
