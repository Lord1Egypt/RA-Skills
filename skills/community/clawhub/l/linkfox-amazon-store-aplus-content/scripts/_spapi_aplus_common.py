"""Shared helpers for linkfox-amazon-store-aplus-content (A+ Content Management v2020-11-01)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

REQUIRED_SKILL = "linkfox-amazon-store-auth"
DEPENDENCY_EXIT_CODE = 42

APLUS_API_VERSION = "2020-11-01"
APLUS_PATH_PREFIX = f"aplus/{APLUS_API_VERSION}"

API_BASE_URL = os.environ.get("STORE_API_BASE_URL") or os.environ.get(
    "SPAPI_BASE_URL", "https://tool-gateway.linkfox.com"
)
STORE_TOKENS_ENDPOINT = f"{API_BASE_URL.rstrip('/')}/spApi/storeTokens"
DEVELOPER_PROXY_ENDPOINT = f"{API_BASE_URL.rstrip('/')}/spApi/developerProxy"


def ensure_auth_skill_available(caller_script: str) -> None:
    here = Path(__file__).resolve().parent
    checker = here / "check_auth_dependency.py"
    if not checker.exists():
        payload = {
            "missingSkill": REQUIRED_SKILL,
            "reason": f"check_auth_dependency.py not found next to {caller_script}",
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
    params: dict[str, Any] = {
        "region": region,
        "path": path,
        "method": "GET",
        "amzAccessToken": access_token,
    }
    if query_string:
        params["queryString"] = query_string
    return call_api(DEVELOPER_PROXY_ENDPOINT, params, timeout=timeout)


def developer_proxy_post(
    region: str,
    path: str,
    access_token: str,
    *,
    query_string: Optional[str] = None,
    body_obj: Optional[dict[str, Any]] = None,
    timeout: int = 120,
) -> dict:
    params: dict[str, Any] = {
        "region": region,
        "path": path,
        "method": "POST",
        "amzAccessToken": access_token,
        "contentType": "application/json",
    }
    if query_string:
        params["queryString"] = query_string
    if body_obj is not None:
        params["body"] = json.dumps(body_obj, ensure_ascii=False)
    return call_api(DEVELOPER_PROXY_ENDPOINT, params, timeout=timeout)


def resolve_marketplace_id(params: dict, api_name: str) -> str:
    mid = params.get("marketplaceId")
    if mid is None and params.get("marketplaceIds") is not None:
        mids = params["marketplaceIds"]
        if isinstance(mids, list) and mids:
            mid = mids[0]
            if len(mids) > 1:
                print(
                    f"⚠️  Warning: {api_name} uses a single marketplaceId; using first marketplaceIds only.",
                    file=sys.stderr,
                )
        elif isinstance(mids, str) and mids.strip():
            mid = mids.strip()
    if mid is None or (isinstance(mid, str) and not mid.strip()):
        raise ValueError("Missing marketplaceId (or non-empty marketplaceIds)")
    return str(mid).strip()


def encode_path_segment(value: str) -> str:
    return quote(value, safe="")


def merge_success_json(out: dict, proxy: dict, result_key: str) -> None:
    if proxy.get("errcode") == 200 and proxy.get("httpStatus") == 200:
        body_raw = proxy.get("body") or "{}"
        try:
            out[result_key] = json.loads(body_raw)
        except json.JSONDecodeError:
            out[result_key] = None
            out[f"{result_key}Raw"] = body_raw
