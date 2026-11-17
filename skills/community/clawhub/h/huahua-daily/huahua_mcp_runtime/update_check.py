"""Best-effort, bounded update detection for the public MCP runtime."""

from __future__ import annotations

import asyncio
import logging
import os
import re
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any

import httpx

from .version import (
    PUBLIC_REPOSITORY_URL,
    PUBLIC_VERSION_SOURCE_URL,
    UPDATE_INSTRUCTIONS,
    __version__,
)


UPDATE_CHECK_TIMEOUT_SECONDS = 2.0
UPDATE_CHECK_TTL_SECONDS = 6 * 60 * 60
UPDATE_CHECK_FAILURE_TTL_SECONDS = 15 * 60
MAX_VERSION_SOURCE_BYTES = 4096
logger = logging.getLogger("huahua-daily.update-check")

_VERSION_ASSIGNMENT = re.compile(
    r'^__version__\s*=\s*["\'](\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?)["\']\s*$',
    re.MULTILINE,
)
_SEMVER = re.compile(
    r"^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?(?:\+[0-9A-Za-z.-]+)?$"
)

_update_cache: dict[str, Any] = {"result": None, "expires_at": 0.0}
_update_lock: asyncio.Lock | None = None
_update_lock_loop: asyncio.AbstractEventLoop | None = None


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _enabled() -> bool:
    value = os.environ.get("HUAHUA_MCP_UPDATE_CHECK", "1").strip().lower()
    return value not in {"0", "false", "no", "off"}


def _version_parts(value: str) -> tuple[tuple[int, int, int], tuple[str, ...] | None]:
    match = _SEMVER.fullmatch(value.strip())
    if not match:
        raise ValueError("invalid semantic version")
    major, minor, patch, prerelease = match.groups()
    return (
        (int(major), int(minor), int(patch)),
        tuple(prerelease.split(".")) if prerelease is not None else None,
    )


def _prerelease_is_newer(latest: tuple[str, ...], current: tuple[str, ...]) -> bool:
    for latest_part, current_part in zip(latest, current, strict=False):
        if latest_part == current_part:
            continue
        latest_numeric = latest_part.isdigit()
        current_numeric = current_part.isdigit()
        if latest_numeric and current_numeric:
            return int(latest_part) > int(current_part)
        if latest_numeric != current_numeric:
            # SemVer numeric identifiers have lower precedence than text.
            return not latest_numeric
        return latest_part > current_part
    return len(latest) > len(current)


def _is_newer(latest: str, current: str) -> bool:
    latest_main, latest_pre = _version_parts(latest)
    current_main, current_pre = _version_parts(current)
    if latest_main != current_main:
        return latest_main > current_main
    if latest_pre is None:
        return current_pre is not None
    if current_pre is None:
        return False
    return _prerelease_is_newer(latest_pre, current_pre)


def _get_update_lock() -> asyncio.Lock:
    global _update_lock, _update_lock_loop
    loop = asyncio.get_running_loop()
    if _update_lock is None or _update_lock_loop is not loop:
        _update_lock = asyncio.Lock()
        _update_lock_loop = loop
    return _update_lock


def _base_result(
    status: str,
    *,
    checked_at: str | None = None,
    cache_ttl_seconds: int = UPDATE_CHECK_TTL_SECONDS,
) -> dict[str, Any]:
    return {
        "status": status,
        "currentVersion": __version__,
        "latestVersion": None,
        "updateAvailable": None,
        "checkedAt": checked_at,
        "cacheTtlSeconds": cache_ttl_seconds,
        "repositoryUrl": PUBLIC_REPOSITORY_URL,
        "updateInstructions": dict(UPDATE_INSTRUCTIONS),
    }


async def _fetch_latest_version() -> str:
    source_url = os.environ.get(
        "HUAHUA_MCP_VERSION_SOURCE_URL",
        PUBLIC_VERSION_SOURCE_URL,
    ).strip()
    timeout = httpx.Timeout(UPDATE_CHECK_TIMEOUT_SECONDS, connect=1.0)
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        async with client.stream(
            "GET",
            source_url,
            headers={"Accept": "text/plain", "User-Agent": f"huahua-daily/{__version__}"},
        ) as response:
            response.raise_for_status()
            chunks: list[bytes] = []
            size = 0
            async for chunk in response.aiter_bytes():
                size += len(chunk)
                if size > MAX_VERSION_SOURCE_BYTES:
                    raise ValueError("version source is too large")
                chunks.append(chunk)
    return _extract_latest_version(b"".join(chunks))


def _extract_latest_version(content: bytes) -> str:
    if len(content) > MAX_VERSION_SOURCE_BYTES:
        raise ValueError("version source is too large")
    match = _VERSION_ASSIGNMENT.search(content.decode("utf-8", errors="strict"))
    if not match:
        raise ValueError("version source has no valid version")
    latest = match.group(1)
    _version_parts(latest)
    return latest


async def get_mcp_update_status(*, force: bool = False) -> dict[str, Any]:
    """Return update status without ever making manifest discovery fail."""
    if not _enabled():
        return _base_result("disabled", cache_ttl_seconds=0)

    now = time.monotonic()
    cached = _update_cache.get("result")
    if not force and isinstance(cached, dict) and now < float(_update_cache["expires_at"]):
        result = dict(cached)
        result["cached"] = True
        return result

    async with _get_update_lock():
        now = time.monotonic()
        cached = _update_cache.get("result")
        if not force and isinstance(cached, dict) and now < float(_update_cache["expires_at"]):
            result = dict(cached)
            result["cached"] = True
            return result

        checked_at = _iso_now()
        try:
            latest = await asyncio.wait_for(
                _fetch_latest_version(),
                timeout=UPDATE_CHECK_TIMEOUT_SECONDS,
            )
            result = _base_result("ok", checked_at=checked_at)
            result.update({
                "latestVersion": latest,
                "updateAvailable": _is_newer(latest, __version__),
                "cached": False,
            })
            ttl = UPDATE_CHECK_TTL_SECONDS
        except Exception:
            # Update discovery is advisory. Network, proxy, GitHub, or parsing
            # failures must never block the MCP capability manifest.
            result = _base_result(
                "unavailable",
                checked_at=checked_at,
                cache_ttl_seconds=UPDATE_CHECK_FAILURE_TTL_SECONDS,
            )
            result["cached"] = False
            ttl = UPDATE_CHECK_FAILURE_TTL_SECONDS

        _update_cache["result"] = result
        _update_cache["expires_at"] = time.monotonic() + ttl
        return dict(result)


def reset_update_check_cache() -> None:
    """Clear process-local state for tests and explicit runtime reconfiguration."""
    _update_cache["result"] = None
    _update_cache["expires_at"] = 0.0


async def _run_startup_update_check() -> dict[str, Any]:
    result = await get_mcp_update_status()
    if result.get("updateAvailable") is True:
        logger.warning(
            "HuahuaDaily MCP update available: current=%s latest=%s; "
            "call get_tool_manifest for update instructions",
            result.get("currentVersion"),
            result.get("latestVersion"),
        )
    return result


@asynccontextmanager
async def mcp_lifespan(_server):
    """Preflight update state at startup without delaying MCP initialization."""
    task = asyncio.create_task(
        _run_startup_update_check(),
        name="huahua-mcp-update-check",
    )
    try:
        yield {"updateCheckTask": task}
    finally:
        if not task.done():
            task.cancel()
        await asyncio.gather(task, return_exceptions=True)
