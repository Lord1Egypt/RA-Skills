"""Shared helpers for linkfox-amazon-store-customer-feedback (Customer Feedback API v2024-06-01)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Optional

from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

REQUIRED_SKILL = "linkfox-amazon-store-auth"
DEPENDENCY_EXIT_CODE = 42

CUSTOMER_FEEDBACK_VERSION = "2024-06-01"
API_PREFIX = f"customerFeedback/{CUSTOMER_FEEDBACK_VERSION}"

SORT_BY_ENUM = frozenset({"MENTIONS", "STAR_RATING_IMPACT"})

API_BASE_URL = os.environ.get("STORE_API_BASE_URL") or os.environ.get(
    "SPAPI_BASE_URL", "https://tool-gateway.linkfox.com"
)
STORE_TOKENS_ENDPOINT = f"{API_BASE_URL.rstrip('/')}/spApi/storeTokens"
DEVELOPER_PROXY_ENDPOINT = f"{API_BASE_URL.rstrip('/')}/spApi/developerProxy"

SUCCESS_HTTP_STATUSES = frozenset({200})


def ensure_auth_skill_available(caller: str = "customer-feedback script") -> None:
    here = Path(__file__).resolve().parent
    checker = here / "check_auth_dependency.py"
    if not checker.exists():
        payload = {
            "missingSkill": REQUIRED_SKILL,
            "reason": f"check_auth_dependency.py not found next to {caller}",
        }
        print(f"DEPENDENCY_MISSING: {json.dumps(payload, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(DEPENDENCY_EXIT_CODE)
    try:
        result = subprocess.run(
            [sys.executable, str(checker)],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception as exc:  # pragma: no cover
        payload = {"missingSkill": REQUIRED_SKILL, "reason": str(exc)}
        print(f"DEPENDENCY_MISSING: {json.dumps(payload, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(DEPENDENCY_EXIT_CODE)
    if result.stderr:
        sys.stderr.write(result.stderr)
        if not result.stderr.endswith("\n"):
            sys.stderr.write("\n")
    if result.returncode != 0:
        sys.exit(DEPENDENCY_EXIT_CODE)


def get_api_key() -> str:
    key = os.environ.get("LINKFOXAGENT_API_KEY")
    if not key:
        print(
            "API Key not configured. Set:\n  export LINKFOXAGENT_API_KEY=<your-key>",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def call_api(endpoint: str, params: dict, timeout: int = 120) -> dict:
    api_key = get_api_key()
    data = json.dumps(params).encode("utf-8")
    req = Request(
        endpoint,
        data=data,
        headers={
            "Authorization": api_key,
            "Content-Type": "application/json",
            "User-Agent": "LinkFox-Skill/1.0",
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        return {"error": f"HTTP {e.code}: {e.reason}", "details": body}
    except URLError as e:
        return {"error": f"Connection failed: {e.reason}"}


def get_store_tokens(seller_id: str, region: str) -> dict:
    return call_api(STORE_TOKENS_ENDPOINT, {"sellerId": seller_id, "region": region})


def developer_proxy_get(
    region: str,
    path: str,
    access_token: str,
    query_string: Optional[str] = None,
    timeout: int = 120,
) -> dict:
    params: dict = {
        "region": region,
        "path": path,
        "method": "GET",
        "amzAccessToken": access_token,
    }
    if query_string:
        params["queryString"] = query_string
    return call_api(DEVELOPER_PROXY_ENDPOINT, params, timeout=timeout)


def encode_path_segment(value: str) -> str:
    return quote(str(value).strip(), safe="")


def resolve_marketplace_id(params: dict) -> str:
    mid = params.get("marketplaceId")
    if mid is None and params.get("marketplaceIds") is not None:
        mids = params["marketplaceIds"]
        if isinstance(mids, list) and mids:
            mid = mids[0]
            if len(mids) > 1:
                print(
                    "Warning: Customer Feedback uses a single marketplaceId; using first only.",
                    file=sys.stderr,
                )
        elif isinstance(mids, str) and mids.strip():
            mid = mids.strip()
    if mid is None or not str(mid).strip():
        print("Missing marketplaceId (or marketplaceIds with at least one id).", file=sys.stderr)
        sys.exit(1)
    return str(mid).strip()


def query_marketplace_only(params: dict) -> str:
    mid = resolve_marketplace_id(params)
    return f"marketplaceId={quote(mid, safe='')}"


def query_marketplace_and_sort_by(params: dict) -> str:
    mid = resolve_marketplace_id(params)
    sort_by = params.get("sortBy")
    if not sort_by:
        print("Missing required field: sortBy (MENTIONS | STAR_RATING_IMPACT).", file=sys.stderr)
        sys.exit(1)
    sort_s = str(sort_by).strip().upper()
    if sort_s not in SORT_BY_ENUM:
        print(f"sortBy must be one of: {sorted(SORT_BY_ENUM)}", file=sys.stderr)
        sys.exit(1)
    return (
        f"marketplaceId={quote(mid, safe='')}"
        f"&sortBy={quote(sort_s, safe='')}"
    )


def merge_success_json(
    out: dict,
    proxy: dict,
    result_key: str,
    *,
    success_http: Iterable[int] = SUCCESS_HTTP_STATUSES,
) -> None:
    if proxy.get("errcode") != 200:
        return
    try:
        status = int(proxy.get("httpStatus") or 0)
    except (TypeError, ValueError):
        return
    if status not in success_http:
        return
    body_raw = proxy.get("body")
    if body_raw is None or not str(body_raw).strip():
        out[result_key] = None
        return
    try:
        out[result_key] = json.loads(str(body_raw))
    except json.JSONDecodeError:
        out[result_key] = None
        out[f"{result_key}Raw"] = body_raw


def load_cli_params() -> dict:
    if len(sys.argv) < 2:
        return {}
    try:
        return json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)


def require_seller_region(params: dict) -> tuple[str, str]:
    for f in ("sellerId", "region"):
        if f not in params:
            print(f"Missing required field: {f}", file=sys.stderr)
            sys.exit(1)
    return str(params["sellerId"]), str(params["region"])


def run_item_get(
    params: dict,
    *,
    path_suffix: str,
    result_key: str,
    query_builder,
    caller: str,
) -> None:
    if not params:
        print(f"Usage: {caller} '<JSON>' — see SKILL.md", file=sys.stderr)
        sys.exit(1)
    if not params.get("skipDepCheck"):
        ensure_auth_skill_available(caller)
    if "asin" not in params:
        print("Missing required field: asin", file=sys.stderr)
        sys.exit(1)

    seller_id, region = require_seller_region(params)
    asin = encode_path_segment(params["asin"])
    path = f"{API_PREFIX}/items/{asin}/{path_suffix}"
    qs = query_builder(params)

    tokens = get_store_tokens(seller_id, region)
    if "error" in tokens or "accessToken" not in tokens:
        print(json.dumps(tokens, indent=2, ensure_ascii=False))
        sys.exit(1)

    proxy = developer_proxy_get(region, path, tokens["accessToken"], query_string=qs)
    out: dict = {"developerProxy": proxy, "resolvedPath": path, "queryString": qs}
    merge_success_json(out, proxy, result_key)
    print(json.dumps(out, indent=2, ensure_ascii=False))


def run_browse_node_get(
    params: dict,
    *,
    path_suffix: str,
    result_key: str,
    query_builder,
    caller: str,
) -> None:
    if not params:
        print(f"Usage: {caller} '<JSON>' — see SKILL.md", file=sys.stderr)
        sys.exit(1)
    if not params.get("skipDepCheck"):
        ensure_auth_skill_available(caller)
    if "browseNodeId" not in params:
        print("Missing required field: browseNodeId", file=sys.stderr)
        sys.exit(1)

    seller_id, region = require_seller_region(params)
    bn = encode_path_segment(params["browseNodeId"])
    path = f"{API_PREFIX}/browseNodes/{bn}/{path_suffix}"
    qs = query_builder(params)

    tokens = get_store_tokens(seller_id, region)
    if "error" in tokens or "accessToken" not in tokens:
        print(json.dumps(tokens, indent=2, ensure_ascii=False))
        sys.exit(1)

    proxy = developer_proxy_get(region, path, tokens["accessToken"], query_string=qs)
    out: dict = {"developerProxy": proxy, "resolvedPath": path, "queryString": qs}
    merge_success_json(out, proxy, result_key)
    print(json.dumps(out, indent=2, ensure_ascii=False))
