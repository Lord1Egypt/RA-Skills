#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "mcp>=1.27.0",
#   "certifi>=2025.11.12",
# ]
# ///
"""Local Pipedrive MCP server exposed over stdio."""

from __future__ import annotations

import json
import os
import ssl
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

import certifi
from mcp.server.fastmcp import Context, FastMCP

mcp = FastMCP("pipedrive")

_API_BASE = os.environ.get("MAVERICK_PIPEDRIVE_MCP_API_BASE", "https://api.pipedrive.com/api").rstrip("/")
_ACCESS_TOKEN_ENV = "MAVERICK_PIPEDRIVE_MCP_ACCESS_TOKEN"


def _bearer_token(ctx: Context) -> str:
    _ = ctx
    token = os.environ.get(_ACCESS_TOKEN_ENV, "").strip()
    if not token:
        raise RuntimeError(f"{_ACCESS_TOKEN_ENV} is required")
    return token


def _bounded_limit(limit: int, *, default: int = 20, maximum: int = 100) -> int:
    try:
        value = int(limit or default)
    except (TypeError, ValueError):
        value = default
    return max(1, min(value, maximum))


def _clean_params(params: dict[str, object] | None) -> dict[str, object]:
    return {key: value for key, value in (params or {}).items() if value not in (None, "", 0, False)}


def _clean_body(body: dict[str, Any] | None) -> dict[str, Any]:
    cleaned: dict[str, Any] = {}
    for key, value in (body or {}).items():
        if value in (None, ""):
            continue
        if isinstance(value, dict) and not value:
            continue
        cleaned[key] = value
    return cleaned


def _merge_custom_fields(body: dict[str, Any], custom_fields: dict[str, Any] | None) -> dict[str, Any]:
    merged = dict(body)
    for key, value in (custom_fields or {}).items():
        if value not in (None, ""):
            merged[str(key)] = value
    return merged


def _url(version: str, path: str, params: dict[str, object] | None = None) -> str:
    normalized_path = path if path.startswith("/") else f"/{path}"
    query = urllib.parse.urlencode(_clean_params(params))
    url = f"{_API_BASE}/{version.strip('/')}{normalized_path}"
    return f"{url}?{query}" if query else url


def _request(
    access_token: str,
    method: str,
    version: str,
    path: str,
    *,
    params: dict[str, object] | None = None,
    body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = None
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    if body is not None:
        payload = json.dumps(_clean_body(body)).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(
        _url(version, path, params),
        data=payload,
        headers=headers,
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
        return {"success": False, "error": "pipedrive_http_error", "status": exc.code, "details": parsed}


def _data_response(response: dict[str, Any]) -> dict[str, Any]:
    if response.get("success") is False:
        return response
    return {
        "data": response.get("data"),
        "additional_data": response.get("additional_data"),
        "related_objects": response.get("related_objects"),
    }


@mcp.tool()
def search_items(ctx: Context, term: str, item_types: str = "deal,person,organization", limit: int = 10, exact_match: bool = False) -> dict[str, Any]:
    """Search deals, persons, organizations, leads, products, files, or mail attachments."""
    token = _bearer_token(ctx)
    return _data_response(
        _request(
            token,
            "GET",
            "v2",
            "/itemSearch",
            params={
                "term": term,
                "item_types": item_types,
                "limit": _bounded_limit(limit, default=10, maximum=100),
                "exact_match": "true" if exact_match else "",
            },
        )
    )


@mcp.tool()
def search_deals(ctx: Context, term: str, limit: int = 10, exact_match: bool = False) -> dict[str, Any]:
    """Search Pipedrive deals by title, notes, custom fields, person, or organization."""
    token = _bearer_token(ctx)
    return _data_response(
        _request(
            token,
            "GET",
            "v2",
            "/deals/search",
            params={"term": term, "limit": _bounded_limit(limit, default=10, maximum=100), "exact_match": "true" if exact_match else ""},
        )
    )


@mcp.tool()
def list_deals(
    ctx: Context,
    limit: int = 20,
    cursor: str = "",
    status: str = "",
    owner_id: int = 0,
    person_id: int = 0,
    org_id: int = 0,
    pipeline_id: int = 0,
    stage_id: int = 0,
) -> dict[str, Any]:
    """List deals, optionally filtered by status, owner, person, organization, pipeline, or stage."""
    token = _bearer_token(ctx)
    return _data_response(
        _request(
            token,
            "GET",
            "v2",
            "/deals",
            params={
                "limit": _bounded_limit(limit),
                "cursor": cursor,
                "status": status,
                "owner_id": owner_id,
                "person_id": person_id,
                "org_id": org_id,
                "pipeline_id": pipeline_id,
                "stage_id": stage_id,
            },
        )
    )


@mcp.tool()
def get_deal(ctx: Context, deal_id: int) -> dict[str, Any]:
    """Get details for one Pipedrive deal."""
    return _data_response(_request(_bearer_token(ctx), "GET", "v2", f"/deals/{deal_id}"))


@mcp.tool()
def create_deal(
    ctx: Context,
    title: str,
    value: float = 0,
    currency: str = "",
    person_id: int = 0,
    org_id: int = 0,
    pipeline_id: int = 0,
    stage_id: int = 0,
    owner_id: int = 0,
    expected_close_date: str = "",
    custom_fields: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a Pipedrive deal. Put account-specific custom field keys in custom_fields."""
    body = _merge_custom_fields(
        {
            "title": title,
            "value": value,
            "currency": currency,
            "person_id": person_id,
            "org_id": org_id,
            "pipeline_id": pipeline_id,
            "stage_id": stage_id,
            "owner_id": owner_id,
            "expected_close_date": expected_close_date,
        },
        custom_fields,
    )
    return _data_response(_request(_bearer_token(ctx), "POST", "v2", "/deals", body=body))


@mcp.tool()
def update_deal(ctx: Context, deal_id: int, fields: dict[str, Any]) -> dict[str, Any]:
    """Update a Pipedrive deal. Pass Pipedrive field names, including custom field keys, in fields."""
    return _data_response(_request(_bearer_token(ctx), "PATCH", "v2", f"/deals/{deal_id}", body=fields))


@mcp.tool()
def search_persons(ctx: Context, term: str, limit: int = 10, exact_match: bool = False, organization_id: int = 0) -> dict[str, Any]:
    """Search Pipedrive persons by name, email, phone, notes, or custom fields."""
    token = _bearer_token(ctx)
    return _data_response(
        _request(
            token,
            "GET",
            "v2",
            "/persons/search",
            params={
                "term": term,
                "limit": _bounded_limit(limit, default=10, maximum=100),
                "exact_match": "true" if exact_match else "",
                "organization_id": organization_id,
            },
        )
    )


@mcp.tool()
def get_person(ctx: Context, person_id: int) -> dict[str, Any]:
    """Get details for one Pipedrive person/contact."""
    return _data_response(_request(_bearer_token(ctx), "GET", "v2", f"/persons/{person_id}"))


@mcp.tool()
def create_person(
    ctx: Context,
    name: str,
    email: str = "",
    phone: str = "",
    org_id: int = 0,
    owner_id: int = 0,
    custom_fields: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a Pipedrive person/contact."""
    body = _merge_custom_fields(
        {"name": name, "email": email, "phone": phone, "org_id": org_id, "owner_id": owner_id},
        custom_fields,
    )
    return _data_response(_request(_bearer_token(ctx), "POST", "v2", "/persons", body=body))


@mcp.tool()
def update_person(ctx: Context, person_id: int, fields: dict[str, Any]) -> dict[str, Any]:
    """Update a Pipedrive person/contact."""
    return _data_response(_request(_bearer_token(ctx), "PATCH", "v2", f"/persons/{person_id}", body=fields))


@mcp.tool()
def search_organizations(ctx: Context, term: str, limit: int = 10, exact_match: bool = False) -> dict[str, Any]:
    """Search Pipedrive organizations by name, address, notes, or custom fields."""
    token = _bearer_token(ctx)
    return _data_response(
        _request(
            token,
            "GET",
            "v2",
            "/organizations/search",
            params={"term": term, "limit": _bounded_limit(limit, default=10, maximum=100), "exact_match": "true" if exact_match else ""},
        )
    )


@mcp.tool()
def get_organization(ctx: Context, org_id: int) -> dict[str, Any]:
    """Get details for one Pipedrive organization."""
    return _data_response(_request(_bearer_token(ctx), "GET", "v2", f"/organizations/{org_id}"))


@mcp.tool()
def create_organization(
    ctx: Context,
    name: str,
    owner_id: int = 0,
    address: str = "",
    custom_fields: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a Pipedrive organization/company."""
    body = _merge_custom_fields({"name": name, "owner_id": owner_id, "address": address}, custom_fields)
    return _data_response(_request(_bearer_token(ctx), "POST", "v2", "/organizations", body=body))


@mcp.tool()
def update_organization(ctx: Context, org_id: int, fields: dict[str, Any]) -> dict[str, Any]:
    """Update a Pipedrive organization/company."""
    return _data_response(_request(_bearer_token(ctx), "PATCH", "v2", f"/organizations/{org_id}", body=fields))


@mcp.tool()
def list_activities(
    ctx: Context,
    limit: int = 20,
    cursor: str = "",
    done: bool = False,
    deal_id: int = 0,
    person_id: int = 0,
    org_id: int = 0,
) -> dict[str, Any]:
    """List Pipedrive activities, optionally filtered by linked deal, person, or organization."""
    token = _bearer_token(ctx)
    return _data_response(
        _request(
            token,
            "GET",
            "v2",
            "/activities",
            params={
                "limit": _bounded_limit(limit),
                "cursor": cursor,
                "done": "true" if done else "",
                "deal_id": deal_id,
                "person_id": person_id,
                "org_id": org_id,
            },
        )
    )


@mcp.tool()
def get_activity(ctx: Context, activity_id: int) -> dict[str, Any]:
    """Get details for one Pipedrive activity."""
    return _data_response(_request(_bearer_token(ctx), "GET", "v2", f"/activities/{activity_id}"))


@mcp.tool()
def create_activity(
    ctx: Context,
    subject: str,
    type: str = "",
    due_date: str = "",
    due_time: str = "",
    duration: str = "",
    note: str = "",
    deal_id: int = 0,
    person_id: int = 0,
    org_id: int = 0,
    owner_id: int = 0,
) -> dict[str, Any]:
    """Create a Pipedrive activity linked to a deal, person, or organization."""
    body = {
        "subject": subject,
        "type": type,
        "due_date": due_date,
        "due_time": due_time,
        "duration": duration,
        "note": note,
        "deal_id": deal_id,
        "person_id": person_id,
        "org_id": org_id,
        "owner_id": owner_id,
    }
    return _data_response(_request(_bearer_token(ctx), "POST", "v2", "/activities", body=body))


@mcp.tool()
def update_activity(ctx: Context, activity_id: int, fields: dict[str, Any]) -> dict[str, Any]:
    """Update a Pipedrive activity."""
    return _data_response(_request(_bearer_token(ctx), "PATCH", "v2", f"/activities/{activity_id}", body=fields))


@mcp.tool()
def add_note(
    ctx: Context,
    content: str,
    deal_id: int = 0,
    person_id: int = 0,
    org_id: int = 0,
    pinned_to_deal: bool = False,
    pinned_to_person: bool = False,
    pinned_to_organization: bool = False,
) -> dict[str, Any]:
    """Add a note to a deal, person, or organization."""
    body = {
        "content": content,
        "deal_id": deal_id,
        "person_id": person_id,
        "org_id": org_id,
        "pinned_to_deal_flag": pinned_to_deal,
        "pinned_to_person_flag": pinned_to_person,
        "pinned_to_organization_flag": pinned_to_organization,
    }
    return _data_response(_request(_bearer_token(ctx), "POST", "v1", "/notes", body=body))


@mcp.tool()
def list_pipelines(ctx: Context, limit: int = 100, cursor: str = "") -> dict[str, Any]:
    """List Pipedrive pipelines for choosing valid pipeline IDs."""
    return _data_response(
        _request(
            _bearer_token(ctx),
            "GET",
            "v2",
            "/pipelines",
            params={"limit": _bounded_limit(limit, default=100, maximum=500), "cursor": cursor},
        )
    )


@mcp.tool()
def list_stages(
    ctx: Context,
    pipeline_id: int = 0,
    limit: int = 100,
    cursor: str = "",
) -> dict[str, Any]:
    """List Pipedrive stages for choosing valid stage IDs."""
    return _data_response(
        _request(
            _bearer_token(ctx),
            "GET",
            "v2",
            "/stages",
            params={
                "pipeline_id": pipeline_id,
                "limit": _bounded_limit(limit, default=100, maximum=500),
                "cursor": cursor,
            },
        )
    )


@mcp.tool()
def list_users(ctx: Context, limit: int = 100, start: int = 0) -> dict[str, Any]:
    """List Pipedrive users for choosing valid owner/user IDs."""
    return _data_response(
        _request(
            _bearer_token(ctx),
            "GET",
            "v1",
            "/users",
            params={"limit": _bounded_limit(limit, default=100, maximum=500), "start": start},
        )
    )


@mcp.tool()
def list_activity_types(ctx: Context) -> dict[str, Any]:
    """List Pipedrive activity types for choosing valid activity type keys."""
    return _data_response(_request(_bearer_token(ctx), "GET", "v1", "/activityTypes"))


@mcp.tool()
def list_deal_fields(ctx: Context, limit: int = 100, cursor: str = "") -> dict[str, Any]:
    """List deal fields and custom field keys."""
    return _data_response(
        _request(
            _bearer_token(ctx),
            "GET",
            "v2",
            "/dealFields",
            params={"limit": _bounded_limit(limit, default=100, maximum=500), "cursor": cursor},
        )
    )


@mcp.tool()
def list_person_fields(ctx: Context, limit: int = 100, cursor: str = "") -> dict[str, Any]:
    """List person fields and custom field keys."""
    return _data_response(
        _request(
            _bearer_token(ctx),
            "GET",
            "v2",
            "/personFields",
            params={"limit": _bounded_limit(limit, default=100, maximum=500), "cursor": cursor},
        )
    )


@mcp.tool()
def list_organization_fields(ctx: Context, limit: int = 100, cursor: str = "") -> dict[str, Any]:
    """List organization fields and custom field keys."""
    return _data_response(
        _request(
            _bearer_token(ctx),
            "GET",
            "v2",
            "/organizationFields",
            params={"limit": _bounded_limit(limit, default=100, maximum=500), "cursor": cursor},
        )
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
