#!/usr/bin/env python3
"""Shared OpenMath API helpers for theorem discovery and download workflows."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone

from openmath_env_config import (
    OpenMathEnvConfigError,
    normalize_api_language,
    normalize_preferred_language,
    resolve_openmath_api_host,
)


@dataclass
class TheoremRecord:
    theorem_id: int
    title: str
    description: str
    language: str
    reward: str
    status: str
    expire_time: str | None
    theorem_code: str
    proposer: str | None
    proposer_nickname: str | None
    raw: dict


def fetch_json(url: str, user_agent: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": user_agent,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code} {exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from exc

    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Received non-JSON response from OpenMath API") from exc


def fetch_open_theorems(language: str | None = None) -> list[dict]:
    try:
        api_host = resolve_openmath_api_host()
    except OpenMathEnvConfigError as exc:
        raise RuntimeError(str(exc)) from exc
    api_language = normalize_api_language(language)
    url = (
        f"{api_host}/api/v1/theorems/open/{api_language}"
        if api_language
        else f"{api_host}/api/v1/theorems/open"
    )
    result = fetch_json(url, "openmath-open-theorem/fetch_theorems.py")
    ensure_success(result)
    return result.get("data") or []


def fetch_theorem_detail(theorem_id: int) -> TheoremRecord:
    try:
        api_host = resolve_openmath_api_host()
    except OpenMathEnvConfigError as exc:
        raise RuntimeError(str(exc)) from exc
    url = f"{api_host}/api/v1/theorems/{theorem_id}"
    result = fetch_json(url, "openmath-open-theorem/fetch_theorem_detail.py")
    ensure_success(result)

    theorem = result.get("data")
    if not theorem:
        raise RuntimeError(f"Theorem with ID {theorem_id} not found.")

    return normalize_theorem_record(theorem, theorem_id)


def ensure_success(result: dict) -> None:
    if result.get("code") == 0:
        return

    message = result.get("message") or {}
    title = message.get("title", "Unknown")
    detail = message.get("detail", "No detail provided")
    raise RuntimeError(f"{title} - {detail}")


def normalize_theorem_record(theorem: dict, fallback_id: int | None = None) -> TheoremRecord:
    raw_id = theorem.get("id", fallback_id)
    theorem_id = int(raw_id) if raw_id is not None else 0
    raw_language = str(theorem.get("language") or "unknown")
    language = normalize_preferred_language(raw_language) or raw_language
    return TheoremRecord(
        theorem_id=theorem_id,
        title=theorem.get("title") or theorem.get("theorem_title") or f"Theorem {theorem_id}",
        description=theorem.get("desc") or theorem.get("theorem_desc") or "No description",
        language=language,
        reward=str(theorem.get("reward") or "N/A"),
        status=str(theorem.get("status") or "N/A"),
        expire_time=theorem.get("end_time") or theorem.get("expire_time"),
        theorem_code=theorem.get("theorem_code") or "",
        proposer=theorem.get("proposer"),
        proposer_nickname=theorem.get("proposer_nickname"),
        raw=theorem,
    )


def format_date(value: object) -> str:
    if not value:
        return "N/A"

    if isinstance(value, str) and value.endswith("Z"):
        value = value[:-1] + "+00:00"

    try:
        return datetime.fromisoformat(str(value)).astimezone(timezone.utc).date().isoformat()
    except ValueError:
        return "N/A"


def format_datetime(value: object) -> str:
    if not value:
        return "N/A"

    if isinstance(value, str) and value.endswith("Z"):
        value = value[:-1] + "+00:00"

    try:
        return datetime.fromisoformat(str(value)).astimezone(timezone.utc).isoformat()
    except ValueError:
        return "N/A"
