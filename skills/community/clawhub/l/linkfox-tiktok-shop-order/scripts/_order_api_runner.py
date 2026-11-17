"""Run registered TikTok Shop ERP order APIs via /tiktokShop/developerProxy."""

from __future__ import annotations

import json
import sys
from typing import Any, List, Optional
from urllib.parse import parse_qsl, urlencode

from _order_endpoints import ORDER_ENDPOINTS, RESERVED_PARAM_KEYS
from _shop_order_common import (
    developer_proxy_call,
    ensure_auth_skill_available,
    merge_upstream_body,
    parse_proxy_business_json,
    qs_add,
    require_open_id,
)


def _build_get_query(params: dict, spec: dict, shop_cipher: Optional[str]) -> str:
    parts: list[str] = []
    if shop_cipher:
        qs_add(parts, "shop_cipher", shop_cipher)
    # Allow raw queryString passthrough extras
    raw_qs = params.get("queryString")
    if isinstance(raw_qs, str) and raw_qs.strip():
        for k, v in parse_qsl(raw_qs.strip().lstrip("?"), keep_blank_values=True):
            if k == "shop_cipher" and shop_cipher:
                continue
            qs_add(parts, k, v)

    allowed = set(spec.get("query_fields") or [])
    path_params = set(spec.get("path_params") or [])
    for key, val in params.items():
        if key in RESERVED_PARAM_KEYS or key in path_params or val is None:
            continue
        if key in ("shop_cipher", "shopCipher"):
            continue
        if allowed and key not in allowed:
            continue
        if isinstance(val, bool):
            qs_add(parts, key, str(val).lower())
        elif isinstance(val, list):
            items = [str(x).strip() for x in val if str(x).strip()]
            if items:
                qs_add(parts, key, ",".join(items))
        elif isinstance(val, dict):
            continue
        else:
            qs_add(parts, key, str(val))
    return "&".join(parts)


def _build_post_query(params: dict, spec: dict, shop_cipher: Optional[str]) -> Optional[str]:
    """POST/PUT/DELETE may still need shop_cipher (+ optional query_fields) on query string."""
    parts: list[str] = []
    if shop_cipher:
        qs_add(parts, "shop_cipher", shop_cipher)
    allowed = set(spec.get("query_fields") or [])
    path_params = set(spec.get("path_params") or [])
    for key, val in params.items():
        if key in RESERVED_PARAM_KEYS or key in path_params or val is None:
            continue
        if key in ("shop_cipher", "shopCipher"):
            continue
        if key not in allowed:
            continue
        if isinstance(val, bool):
            qs_add(parts, key, str(val).lower())
        elif isinstance(val, list):
            items = [str(x).strip() for x in val if str(x).strip()]
            if items:
                qs_add(parts, key, ",".join(items))
        elif isinstance(val, dict):
            continue
        else:
            qs_add(parts, key, str(val))
    return "&".join(parts) if parts else None


def _build_body(params: dict, spec: dict) -> Optional[str]:
    method = spec["method"]
    if method == "GET":
        return None

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
        if spec.get("allow_empty_body"):
            return "{}"
        print(
            "POST/PUT/DELETE requires 'body' / 'requestBody' or documented body_fields in params",
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


def _extract_cipher_from_shops(data: Any, shop_id: Optional[str] = None) -> Optional[str]:
    if not isinstance(data, dict):
        return None
    shops = data.get("shops")
    if not isinstance(shops, list) or not shops:
        return None
    if shop_id:
        for s in shops:
            if isinstance(s, dict) and str(s.get("id")) == str(shop_id):
                cipher = s.get("cipher")
                return str(cipher) if cipher else None
        return None
    if len(shops) == 1 and isinstance(shops[0], dict) and shops[0].get("cipher"):
        return str(shops[0]["cipher"])
    return None


def resolve_shop_cipher(params: dict, open_id: str) -> str:
    """Resolve shop_cipher from params or Get Authorized Shops."""
    for key in ("shop_cipher", "shopCipher"):
        val = params.get(key)
        if val is not None and str(val).strip():
            return str(val).strip()

    # Prefer cipher already obtained in-session via nested call
    shop_id = params.get("shop_id") or params.get("shopId")
    proxy = developer_proxy_call(
        open_id,
        "authorization/202309/shops",
        "GET",
        region=params.get("region"),
    )
    business = parse_proxy_business_json(proxy)
    cipher = None
    if business and business.get("code") == 0:
        cipher = _extract_cipher_from_shops(business.get("data"), shop_id=str(shop_id) if shop_id else None)

    if cipher:
        return cipher

    shops = []
    if business and isinstance(business.get("data"), dict):
        shops = business["data"].get("shops") or []
    print(
        "Missing shop_cipher. Pass shop_cipher explicitly, or shop_id when multiple shops exist.\n"
        f"  Get Authorized Shops returned {len(shops) if isinstance(shops, list) else 0} shop(s).\n"
        "  Example: {\"api\":\"get_order_list\",\"openId\":\"...\",\"shop_cipher\":\"GCP_...\"}",
        file=sys.stderr,
    )
    sys.exit(1)


def run_order_api(api_name: str, params: dict, caller: Optional[str] = None) -> dict:
    if api_name not in ORDER_ENDPOINTS:
        print(
            f"Unknown api: {api_name}. Valid: {', '.join(sorted(ORDER_ENDPOINTS))}",
            file=sys.stderr,
        )
        sys.exit(1)

    spec = ORDER_ENDPOINTS[api_name]

    for key, val in (spec.get("defaults") or {}).items():
        if key not in params or params[key] is None:
            params[key] = val

    for field in spec.get("required") or []:
        if field not in params or params[field] is None or params[field] == "":
            print(f"Missing required field: {field}", file=sys.stderr)
            sys.exit(1)

    if not params.get("skipDepCheck"):
        ensure_auth_skill_available(caller or f"{api_name}.py")

    open_id = require_open_id(params)

    shop_cipher: Optional[str] = None
    if spec.get("needs_shop_cipher"):
        if params.get("skipShopCipherResolve") and not (
            params.get("shop_cipher") or params.get("shopCipher")
        ):
            print("needs_shop_cipher=true but shop_cipher missing", file=sys.stderr)
            sys.exit(1)
        shop_cipher = resolve_shop_cipher(params, open_id)

    method = spec["method"]
    path = _resolve_path(spec["path"], params, spec.get("path_params") or [])
    response_key = spec.get("response_key") or "data"

    query_string: Optional[str] = None
    body: Optional[str] = None
    content_type = str(params.get("contentType") or "application/json")

    if method == "GET":
        query_string = _build_get_query(params, spec, shop_cipher) or None
    else:
        query_string = _build_post_query(params, spec, shop_cipher)
        body = _build_body(params, spec)

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
        "appType": "erp",
        "developerProxy": proxy,
        "resolvedPath": path,
    }
    if shop_cipher:
        out["shop_cipher"] = shop_cipher
    if query_string:
        out["queryString"] = query_string
    if body is not None:
        try:
            out["requestBody"] = json.loads(body) if body else None
        except json.JSONDecodeError:
            out["requestBody"] = body

    merge_upstream_body(out, proxy, response_key)
    return out


def run_order_proxy(params: dict, caller: str = "order_proxy.py") -> dict:
    """Generic proxy: path + method + openId (+ optional shop_cipher)."""
    if not params.get("skipDepCheck"):
        ensure_auth_skill_available(caller)

    path = params.get("path")
    method = params.get("method")
    if not path or not method:
        print("Missing required fields: path, method", file=sys.stderr)
        sys.exit(1)

    open_id = require_open_id(params)

    shop_cipher = None
    needs_cipher = str(path).lstrip("/").startswith("order/")
    if needs_cipher:
        shop_cipher = resolve_shop_cipher(params, open_id)

    query_string = params.get("queryString")
    if shop_cipher:
        # ensure shop_cipher present
        pairs = dict(parse_qsl(str(query_string or "").lstrip("?"), keep_blank_values=True))
        pairs["shop_cipher"] = shop_cipher
        query_string = urlencode(pairs)

    body = params.get("body")
    if body is not None and not isinstance(body, str):
        body = json.dumps(body, ensure_ascii=False, separators=(",", ":"))
    if "requestBody" in params and body is None:
        rb = params["requestBody"]
        body = rb if isinstance(rb, str) else json.dumps(rb, ensure_ascii=False, separators=(",", ":"))

    proxy = developer_proxy_call(
        open_id,
        str(path),
        str(method).upper(),
        region=params.get("region"),
        query_string=query_string,
        body=body,
        content_type=str(params.get("contentType") or "application/json"),
    )
    out = {
        "developerProxy": proxy,
        "resolvedPath": str(path).lstrip("/"),
        "appType": "erp",
    }
    if shop_cipher:
        out["shop_cipher"] = shop_cipher
    if query_string:
        out["queryString"] = query_string
    merge_upstream_body(out, proxy, "data")
    return out
