"""Run registered TikTok Video Products APIs via /tiktokVideo/developerProxy."""

from __future__ import annotations

import json
import sys
from typing import Any, List, Optional

from _products_endpoints import LIST_QUERY_FIELDS, PRODUCTS_ENDPOINTS, RESERVED_PARAM_KEYS
from _tiktok_video_products_common import (
    developer_proxy_call,
    ensure_auth_skill_available,
    merge_upstream_body,
    qs_add,
    require_open_id,
)


def _comma_join_list(val: object, field: str, max_items: int) -> str:
    items: List[str] = []
    if isinstance(val, str):
        items = [x.strip() for x in val.split(",") if x.strip()]
    elif isinstance(val, list):
        items = [str(x).strip() for x in val if str(x).strip()]
    else:
        print(f"{field} must be string or string[]", file=sys.stderr)
        sys.exit(1)
    if not items:
        print(f"{field} cannot be empty", file=sys.stderr)
        sys.exit(1)
    if len(items) > max_items:
        print(f"{field} supports at most {max_items} values", file=sys.stderr)
        sys.exit(1)
    return ",".join(items)


def _normalize_list_fields(params: dict) -> None:
    for field in LIST_QUERY_FIELDS:
        if field in params:
            params[field] = _comma_join_list(params[field], field, 50)


def _build_get_query(params: dict, spec: dict) -> str:
    _normalize_list_fields(params)
    parts: list[str] = []
    allowed = set(spec.get("query_fields") or [])
    path_params = set(spec.get("path_params") or [])
    for key, val in params.items():
        if key in RESERVED_PARAM_KEYS or key in path_params or val is None:
            continue
        if allowed and key not in allowed:
            continue
        if isinstance(val, bool):
            qs_add(parts, key, str(val).lower())
        elif isinstance(val, (dict, list)):
            continue
        else:
            qs_add(parts, key, str(val))
    return "&".join(parts)


def _build_post_body(params: dict, spec: dict) -> str:
    if "body" in params:
        body = params["body"]
        if isinstance(body, str):
            return body
        return json.dumps(body, ensure_ascii=False, separators=(",", ":"))

    if "requestBody" in params:
        rb = params["requestBody"]
        if isinstance(rb, str):
            return rb
        return json.dumps(rb, ensure_ascii=False, separators=(",", ":"))

    body_obj: dict[str, Any] = {}
    for key in spec.get("body_fields") or []:
        if key in params and params[key] is not None:
            body_obj[key] = params[key]

    if not body_obj:
        print(
            "POST/PUT requires 'body' / 'requestBody' or documented body_fields in params",
            file=sys.stderr,
        )
        sys.exit(1)
    return json.dumps(body_obj, ensure_ascii=False, separators=(",", ":"))


def _resolve_path(path_template: str, params: dict, path_params: List[str]) -> str:
    path = path_template
    for key in path_params:
        val = params.get(key)
        if val is None or val == "":
            print(f"Missing required path param: {key}", file=sys.stderr)
            sys.exit(1)
        path = path.replace(f"{{{key}}}", str(val))
    if "{" in path and "}" in path:
        print(f"Unresolved path template placeholders in: {path}", file=sys.stderr)
        sys.exit(1)
    return path


def run_products_api(api_name: str, params: dict, caller: Optional[str] = None) -> dict:
    if api_name not in PRODUCTS_ENDPOINTS:
        print(
            f"Unknown api: {api_name}. Valid: {', '.join(sorted(PRODUCTS_ENDPOINTS))}",
            file=sys.stderr,
        )
        sys.exit(1)

    spec = PRODUCTS_ENDPOINTS[api_name]

    for key, val in (spec.get("defaults") or {}).items():
        if key not in params or params[key] is None:
            params[key] = val

    for field in spec.get("required") or []:
        if field == "ttsAccessToken":
            continue
        if field not in params or params[field] is None or params[field] == "":
            print(f"Missing required field: {field}", file=sys.stderr)
            sys.exit(1)

    if not params.get("skipDepCheck"):
        ensure_auth_skill_available(caller or f"{api_name}.py")

    method = spec["method"]
    path = _resolve_path(spec["path"], params, spec.get("path_params") or [])
    response_key = spec.get("response_key") or "data"

    query_string: Optional[str] = None
    body: Optional[str] = None
    content_type = str(params.get("contentType") or "application/json")

    if method == "GET":
        query_string = _build_get_query(params, spec) or None
    else:
        body = _build_post_body(params, spec)

    open_id = require_open_id(params)

    proxy = developer_proxy_call(
        open_id,
        path,
        method,
        region=params.get("region"),
        query_string=query_string,
        body=body,
        content_type=content_type,
    )

    out: dict = {
        "api": api_name,
        "developerProxy": proxy,
        "resolvedPath": path,
    }
    if query_string:
        out["queryString"] = query_string
    if body is not None:
        try:
            out["requestBody"] = json.loads(body) if body else None
        except json.JSONDecodeError:
            out["requestBody"] = body

    merge_upstream_body(out, proxy, response_key)
    return out
