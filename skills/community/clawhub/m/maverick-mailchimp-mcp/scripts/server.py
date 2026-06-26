#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "mcp>=1.27.0",
#   "certifi>=2025.11.12",
# ]
# ///
"""Local Mailchimp Marketing API MCP server exposed over stdio."""

from __future__ import annotations

import hashlib
import json
import os
import ssl
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

import certifi
from mcp.server.fastmcp import Context, FastMCP

mcp = FastMCP("mailchimp")

_API_BASE = os.environ.get("MAVERICK_MAILCHIMP_MCP_API_BASE", "").rstrip("/")
_ACCESS_TOKEN_ENV = "MAVERICK_MAILCHIMP_MCP_ACCESS_TOKEN"


def _bearer_token(ctx: Context) -> str:
    _ = ctx
    token = os.environ.get(_ACCESS_TOKEN_ENV, "").strip()
    if not token:
        raise RuntimeError(f"{_ACCESS_TOKEN_ENV} is required")
    return token


def _api_base() -> str:
    if not _API_BASE:
        raise RuntimeError("MAVERICK_MAILCHIMP_MCP_API_BASE is required")
    return _API_BASE


def _bounded_limit(limit: int, *, default: int = 20, maximum: int = 100) -> int:
    try:
        value = int(limit or default)
    except (TypeError, ValueError):
        value = default
    return max(1, min(value, maximum))


def _clean_params(params: dict[str, object] | None) -> dict[str, object]:
    return {
        key: value
        for key, value in (params or {}).items()
        if value not in (None, "", False)
    }


def _subscriber_hash(email_or_hash: str) -> str:
    value = email_or_hash.strip()
    if "@" not in value:
        return value.lower()
    return hashlib.md5(value.lower().encode("utf-8")).hexdigest()


def _url(path: str, params: dict[str, object] | None = None) -> str:
    normalized_path = path if path.startswith("/") else f"/{path}"
    query = urllib.parse.urlencode(_clean_params(params))
    url = f"{_api_base()}{normalized_path}"
    return f"{url}?{query}" if query else url


def _request(
    access_token: str,
    method: str,
    path: str,
    *,
    params: dict[str, object] | None = None,
) -> dict[str, Any]:
    request = urllib.request.Request(
        _url(path, params),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        },
        method=method.upper(),
    )
    context = ssl.create_default_context(cafile=certifi.where())
    try:
        with urllib.request.urlopen(request, timeout=30, context=context) as response:
            raw = response.read().decode("utf-8")
            if not raw:
                return {"success": True, "data": None}
            parsed = json.loads(raw)
            return parsed if isinstance(parsed, dict) else {"success": True, "data": parsed}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(raw)
        except ValueError:
            parsed = {"message": raw[:500]}
        return {
            "success": False,
            "error": "mailchimp_http_error",
            "status": exc.code,
            "details": parsed,
        }


def _data_response(response: dict[str, Any]) -> dict[str, Any]:
    if response.get("success") is False:
        return response
    return response


@mcp.tool()
def get_account(ctx: Context) -> dict[str, Any]:
    """Get account details for the connected Mailchimp account."""
    return _data_response(_request(_bearer_token(ctx), "GET", "/"))


@mcp.tool()
def list_audiences(ctx: Context, limit: int = 20, offset: int = 0) -> dict[str, Any]:
    """List Mailchimp audiences."""
    return _data_response(
        _request(
            _bearer_token(ctx),
            "GET",
            "/lists",
            params={"count": _bounded_limit(limit), "offset": max(0, int(offset or 0))},
        )
    )


@mcp.tool()
def get_audience(ctx: Context, audience_id: str) -> dict[str, Any]:
    """Get details for one Mailchimp audience."""
    return _data_response(_request(_bearer_token(ctx), "GET", f"/lists/{audience_id}"))


@mcp.tool()
def list_members(
    ctx: Context,
    audience_id: str,
    limit: int = 20,
    offset: int = 0,
    status: str = "",
) -> dict[str, Any]:
    """List members in one Mailchimp audience."""
    return _data_response(
        _request(
            _bearer_token(ctx),
            "GET",
            f"/lists/{audience_id}/members",
            params={
                "count": _bounded_limit(limit),
                "offset": max(0, int(offset or 0)),
                "status": status,
            },
        )
    )


@mcp.tool()
def get_member(ctx: Context, audience_id: str, email_or_hash: str) -> dict[str, Any]:
    """Get one Mailchimp audience member by email address or subscriber hash."""
    return _data_response(
        _request(
            _bearer_token(ctx),
            "GET",
            f"/lists/{audience_id}/members/{_subscriber_hash(email_or_hash)}",
        )
    )


@mcp.tool()
def search_members(
    ctx: Context,
    query: str,
    audience_id: str = "",
    limit: int = 20,
    offset: int = 0,
) -> dict[str, Any]:
    """Search Mailchimp list members by text query."""
    return _data_response(
        _request(
            _bearer_token(ctx),
            "GET",
            "/search-members",
            params={
                "query": query,
                "list_id": audience_id,
                "count": _bounded_limit(limit),
                "offset": max(0, int(offset or 0)),
            },
        )
    )


@mcp.tool()
def list_campaigns(
    ctx: Context,
    limit: int = 20,
    offset: int = 0,
    status: str = "",
    audience_id: str = "",
    sort_field: str = "create_time",
    sort_dir: str = "DESC",
) -> dict[str, Any]:
    """List Mailchimp campaigns."""
    return _data_response(
        _request(
            _bearer_token(ctx),
            "GET",
            "/campaigns",
            params={
                "count": _bounded_limit(limit),
                "offset": max(0, int(offset or 0)),
                "status": status,
                "list_id": audience_id,
                "sort_field": sort_field,
                "sort_dir": sort_dir,
            },
        )
    )


@mcp.tool()
def get_campaign(ctx: Context, campaign_id: str) -> dict[str, Any]:
    """Get details for one Mailchimp campaign."""
    return _data_response(_request(_bearer_token(ctx), "GET", f"/campaigns/{campaign_id}"))


@mcp.tool()
def get_campaign_content(ctx: Context, campaign_id: str) -> dict[str, Any]:
    """Get rendered content for one Mailchimp campaign."""
    return _data_response(
        _request(_bearer_token(ctx), "GET", f"/campaigns/{campaign_id}/content")
    )


@mcp.tool()
def get_campaign_report(ctx: Context, campaign_id: str) -> dict[str, Any]:
    """Get report metrics for one Mailchimp campaign."""
    return _data_response(_request(_bearer_token(ctx), "GET", f"/reports/{campaign_id}"))


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
