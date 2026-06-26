#!/usr/bin/env python3
"""ESPN provider adapter for NBA_TR."""

from __future__ import annotations

import json
import os
import socket
import shutil
import ssl
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from cache_store import cached_json_fetch
from nba_common import NBAReportError

DEFAULT_BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba"
USER_AGENT = "nba-tr-openclaw/2.0"


def resolve_base_url(base_url: str | None = None) -> str:
    return (base_url or os.environ.get("NBA_TR_ESPN_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")


def _cache_identity(resolved_base: str, key: str) -> str:
    if os.environ.get("NBA_PULSE_CACHE_DIR", "").strip():
        return key
    return f"{resolved_base}|{key}"


def _request_json(url: str, timeout_seconds: int) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="GET",
    )
    context = ssl.create_default_context()
    with urllib.request.urlopen(request, timeout=timeout_seconds, context=context) as response:
        return json.loads(response.read().decode("utf-8"))


def _request_json_with_curl(url: str, timeout_seconds: int) -> dict[str, Any]:
    curl_bin = shutil.which("curl")
    if not curl_bin:
        raise NBAReportError("curl 不可用，且 ESPN 请求失败。", kind="connection_failed")
    completed = subprocess.run(
        [
            curl_bin,
            "-L",
            "--silent",
            "--fail",
            "--max-time",
            str(timeout_seconds),
            "-H",
            f"User-Agent: {USER_AGENT}",
            "-H",
            "Accept: application/json",
            url,
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        message = (completed.stderr or completed.stdout or "curl request failed").strip()
        raise NBAReportError(message, kind="connection_failed")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise NBAReportError("ESPN 返回不是合法 JSON。", kind="invalid_json") from exc


def _fetch_json(url: str, timeout_seconds: int = 20) -> dict[str, Any]:
    last_error: Exception | None = None
    for _ in range(2):
        try:
            return _request_json(url, timeout_seconds)
        except urllib.error.HTTPError as exc:
            body_text = exc.read().decode("utf-8", errors="replace")
            message = parse_error_message(body_text) or f"HTTP {exc.code}"
            raise NBAReportError(message, status=exc.code, kind=classify_http_status(exc.code)) from exc
        except (urllib.error.URLError, TimeoutError, socket.timeout, ssl.SSLError, json.JSONDecodeError) as exc:
            last_error = exc
    try:
        return _request_json_with_curl(url, timeout_seconds)
    except NBAReportError:
        pass
    detail = str(last_error) if last_error else "unknown error"
    raise NBAReportError(f"无法连接 ESPN 数据源: {detail}", kind="connection_failed")


def build_url(base_url: str, endpoint: str, params: dict[str, str]) -> str:
    query = urllib.parse.urlencode(params)
    return f"{base_url}/{endpoint}?{query}" if query else f"{base_url}/{endpoint}"


def _cached_response(
    *,
    namespace: str,
    cache_key: str,
    base_url: str,
    endpoint: str,
    params: dict[str, str],
    timeout_seconds: int,
    ttl_seconds: int,
    use_disk: bool | None = None,
) -> dict[str, Any]:
    url = build_url(base_url, endpoint, params)
    payload, freshness = cached_json_fetch(
        namespace=namespace,
        key=cache_key,
        ttl_seconds=ttl_seconds,
        fetcher=lambda: _fetch_json(url, timeout_seconds=timeout_seconds),
        use_disk=use_disk,
    )
    return {
        "baseUrl": base_url,
        "endpoint": endpoint,
        "request": params,
        "data": payload,
        "dataFreshness": freshness,
    }


def fetch_scoreboard(
    date_text: str,
    *,
    base_url: str | None = None,
    timeout_seconds: int = 20,
    persistent_cache: bool = False,
) -> dict[str, Any]:
    resolved_base = resolve_base_url(base_url)
    return _cached_response(
        namespace="espn:scoreboard",
        cache_key=_cache_identity(resolved_base, date_text),
        base_url=resolved_base,
        endpoint="scoreboard",
        params={"dates": date_text},
        timeout_seconds=timeout_seconds,
        ttl_seconds=120,
        use_disk=True if persistent_cache else None,
    )


def fetch_summary(
    event_id: str,
    *,
    base_url: str | None = None,
    timeout_seconds: int = 20,
    persistent_cache: bool = False,
) -> dict[str, Any]:
    resolved_base = resolve_base_url(base_url)
    return _cached_response(
        namespace="espn:summary",
        cache_key=_cache_identity(resolved_base, event_id),
        base_url=resolved_base,
        endpoint="summary",
        params={"event": event_id},
        timeout_seconds=timeout_seconds,
        ttl_seconds=45,
        use_disk=True if persistent_cache else None,
    )


def fetch_team_statistics(team_id: str, *, base_url: str | None = None, timeout_seconds: int = 20) -> dict[str, Any]:
    resolved_base = resolve_base_url(base_url)
    return _cached_response(
        namespace="espn:team_statistics",
        cache_key=_cache_identity(resolved_base, team_id),
        base_url=resolved_base,
        endpoint=f"teams/{team_id}/statistics",
        params={},
        timeout_seconds=timeout_seconds,
        ttl_seconds=1800,
    )


def fetch_team_schedule(team_id: str, *, base_url: str | None = None, timeout_seconds: int = 20) -> dict[str, Any]:
    resolved_base = resolve_base_url(base_url)
    return _cached_response(
        namespace="espn:team_schedule",
        cache_key=_cache_identity(resolved_base, team_id),
        base_url=resolved_base,
        endpoint=f"teams/{team_id}/schedule",
        params={},
        timeout_seconds=timeout_seconds,
        ttl_seconds=600,
    )


def fetch_news(*, base_url: str | None = None, timeout_seconds: int = 20) -> dict[str, Any]:
    resolved_base = resolve_base_url(base_url)
    return _cached_response(
        namespace="espn:news",
        cache_key=_cache_identity(resolved_base, "latest"),
        base_url=resolved_base,
        endpoint="news",
        params={},
        timeout_seconds=timeout_seconds,
        ttl_seconds=600,
    )


def fetch_teams(*, base_url: str | None = None, timeout_seconds: int = 20) -> dict[str, Any]:
    resolved_base = resolve_base_url(base_url)
    return _cached_response(
        namespace="espn:teams",
        cache_key=_cache_identity(resolved_base, "teams"),
        base_url=resolved_base,
        endpoint="teams",
        params={},
        timeout_seconds=timeout_seconds,
        ttl_seconds=3600,
    )


def fetch_team_roster(team_id: str, *, base_url: str | None = None, timeout_seconds: int = 20) -> dict[str, Any]:
    resolved_base = resolve_base_url(base_url)
    return _cached_response(
        namespace="espn:team_roster",
        cache_key=_cache_identity(resolved_base, team_id),
        base_url=resolved_base,
        endpoint=f"teams/{team_id}/roster",
        params={},
        timeout_seconds=timeout_seconds,
        ttl_seconds=3600,
    )


def fetch_team_injuries(team_id: str, *, base_url: str | None = None, timeout_seconds: int = 20) -> dict[str, Any]:
    resolved_base = resolve_base_url(base_url)
    return _cached_response(
        namespace="espn:team_injuries",
        cache_key=_cache_identity(resolved_base, team_id),
        base_url=resolved_base,
        endpoint=f"teams/{team_id}/injuries",
        params={},
        timeout_seconds=timeout_seconds,
        ttl_seconds=900,
    )


def extract_roster_players(payload: dict[str, Any]) -> list[dict[str, str]]:
    players: list[dict[str, str]] = []
    for athlete in payload.get("athletes") or []:
        name = athlete.get("displayName") or athlete.get("fullName") or athlete.get("shortName")
        if not name:
            continue
        players.append(
            {
                "id": str(athlete.get("id") or ""),
                "displayName": str(name),
                "shortName": str(athlete.get("shortName") or name),
                "jersey": str(athlete.get("jersey") or ""),
                "position": str(((athlete.get("position") or {}).get("abbreviation")) or ""),
            }
        )
    return players


def classify_http_status(status: int) -> str:
    if status == 404:
        return "not_found"
    if status == 429:
        return "rate_limited"
    if 400 <= status < 500:
        return "client_error"
    return "server_error"


def parse_error_message(body_text: str) -> str | None:
    try:
        payload = json.loads(body_text)
    except json.JSONDecodeError:
        return None
    if isinstance(payload, dict):
        for key in ("message", "error", "detail"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None
