#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "mcp>=1.27.0",
#   "certifi>=2025.11.12",
# ]
# ///
"""Local Trello MCP server exposed over stdio."""

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

mcp = FastMCP("trello")

_API_KEY = os.environ.get("MAVERICK_TRELLO_MCP_API_KEY", "")
_API_BASE = "https://api.trello.com/1"
_ACCESS_TOKEN_ENV = "MAVERICK_TRELLO_MCP_ACCESS_TOKEN"


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


def _clean_params(access_token: str, params: dict[str, object] | None) -> dict[str, object]:
    if not _API_KEY:
        raise RuntimeError("MAVERICK_TRELLO_MCP_API_KEY is required")
    cleaned = {key: value for key, value in (params or {}).items() if value not in (None, "", 0, False)}
    cleaned["key"] = _API_KEY
    cleaned["token"] = access_token
    return cleaned


def _clean_body(body: dict[str, Any] | None) -> dict[str, Any]:
    return {key: value for key, value in (body or {}).items() if value not in (None, "")}


def _url(access_token: str, path: str, params: dict[str, object] | None = None) -> str:
    normalized_path = path if path.startswith("/") else f"/{path}"
    query = urllib.parse.urlencode(_clean_params(access_token, params))
    return f"{_API_BASE}{normalized_path}?{query}"


def _request(
    access_token: str,
    method: str,
    path: str,
    *,
    params: dict[str, object] | None = None,
    body: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = None
    headers = {"Accept": "application/json"}
    if body is not None:
        payload = urllib.parse.urlencode(_clean_body(body)).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    request = urllib.request.Request(
        _url(access_token, path, params),
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
            return {"success": True, "data": parsed}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            details = json.loads(raw)
        except ValueError:
            details = {"message": raw[:500]}
        return {"success": False, "error": "trello_http_error", "status": exc.code, "details": details}


def _data_response(response: dict[str, Any]) -> dict[str, Any]:
    if response.get("success") is False:
        return response
    return {"data": response.get("data")}


def _limited_data_response(response: dict[str, Any], limit: int) -> dict[str, Any]:
    if response.get("success") is False:
        return response
    data = response.get("data")
    if isinstance(data, list):
        return {"data": data[: _bounded_limit(limit)]}
    return {"data": data}


@mcp.tool()
def list_boards(ctx: Context, filter: str = "open", limit: int = 50) -> dict[str, Any]:
    """List Trello boards the connected member can access."""
    token = _bearer_token(ctx)
    response = _request(
        token,
        "GET",
        "/members/me/boards",
        params={
            "filter": filter,
            "fields": "id,name,desc,url,closed,dateLastActivity",
            "lists": "open",
            "list_fields": "id,name,closed,pos",
        },
    )
    return _limited_data_response(response, limit)


@mcp.tool()
def get_board(ctx: Context, board_id: str) -> dict[str, Any]:
    """Get Trello board details, including open lists."""
    token = _bearer_token(ctx)
    return _data_response(
        _request(
            token,
            "GET",
            f"/boards/{board_id}",
            params={
                "fields": "id,name,desc,url,closed,dateLastActivity",
                "lists": "open",
                "list_fields": "id,name,closed,pos",
            },
        )
    )


@mcp.tool()
def list_lists(ctx: Context, board_id: str, filter: str = "open") -> dict[str, Any]:
    """List Trello lists on a board."""
    return _data_response(
        _request(
            _bearer_token(ctx),
            "GET",
            f"/boards/{board_id}/lists",
            params={"filter": filter, "fields": "id,name,closed,pos"},
        )
    )


@mcp.tool()
def list_cards(ctx: Context, board_id: str, filter: str = "open", limit: int = 50) -> dict[str, Any]:
    """List Trello cards on a board."""
    token = _bearer_token(ctx)
    response = _request(
        token,
        "GET",
        f"/boards/{board_id}/cards/{filter}",
        params={"fields": "id,name,desc,url,closed,due,idList,labels,dateLastActivity"},
    )
    return _limited_data_response(response, limit)


@mcp.tool()
def list_cards_in_list(ctx: Context, list_id: str, limit: int = 50) -> dict[str, Any]:
    """List Trello cards in a specific list."""
    token = _bearer_token(ctx)
    response = _request(
        token,
        "GET",
        f"/lists/{list_id}/cards",
        params={"fields": "id,name,desc,url,closed,due,idList,labels,dateLastActivity"},
    )
    return _limited_data_response(response, limit)


@mcp.tool()
def get_card(ctx: Context, card_id: str) -> dict[str, Any]:
    """Get details for one Trello card."""
    token = _bearer_token(ctx)
    return _data_response(
        _request(
            token,
            "GET",
            f"/cards/{card_id}",
            params={
                "fields": "id,name,desc,url,closed,due,idBoard,idList,labels,dateLastActivity",
                "members": "true",
                "member_fields": "id,fullName,username",
                "actions": "commentCard,updateCard:idList",
                "actions_limit": 20,
            },
        )
    )


@mcp.tool()
def search_cards(ctx: Context, query: str, board_id: str = "", limit: int = 20) -> dict[str, Any]:
    """Search Trello cards by text, optionally within one board."""
    token = _bearer_token(ctx)
    response = _request(
        token,
        "GET",
        "/search",
        params={
            "query": query,
            "modelTypes": "cards",
            "card_fields": "id,name,desc,url,closed,due,idBoard,idList,labels,dateLastActivity",
            "cards_limit": _bounded_limit(limit, default=20, maximum=100),
            "idBoards": board_id,
        },
    )
    return _data_response(response)


@mcp.tool()
def create_card(ctx: Context, list_id: str, name: str, desc: str = "", due: str = "", pos: str = "bottom") -> dict[str, Any]:
    """Create a Trello card in a list."""
    return _data_response(
        _request(
            _bearer_token(ctx),
            "POST",
            "/cards",
            body={"idList": list_id, "name": name, "desc": desc, "due": due, "pos": pos},
        )
    )


@mcp.tool()
def update_card(ctx: Context, card_id: str, fields: dict[str, Any]) -> dict[str, Any]:
    """Update a Trello card."""
    return _data_response(_request(_bearer_token(ctx), "PUT", f"/cards/{card_id}", body=fields))


@mcp.tool()
def move_card(ctx: Context, card_id: str, list_id: str, pos: str = "bottom") -> dict[str, Any]:
    """Move a Trello card to another list."""
    return _data_response(
        _request(_bearer_token(ctx), "PUT", f"/cards/{card_id}", body={"idList": list_id, "pos": pos})
    )


@mcp.tool()
def add_comment(ctx: Context, card_id: str, text: str) -> dict[str, Any]:
    """Add a comment to a Trello card."""
    return _data_response(
        _request(_bearer_token(ctx), "POST", f"/cards/{card_id}/actions/comments", body={"text": text})
    )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
