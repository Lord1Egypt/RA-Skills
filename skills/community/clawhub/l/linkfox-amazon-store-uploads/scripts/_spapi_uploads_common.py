"""Shared helpers for linkfox-amazon-store-uploads (Uploads API v2020-11-01)."""

from __future__ import annotations

import base64
import hashlib
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

UPLOADS_API_VERSION = "2020-11-01"
UPLOADS_PATH_PREFIX = f"uploads/{UPLOADS_API_VERSION}"

API_BASE_URL = os.environ.get("STORE_API_BASE_URL") or os.environ.get(
    "SPAPI_BASE_URL", "https://tool-gateway.linkfox.com"
)
STORE_TOKENS_ENDPOINT = f"{API_BASE_URL.rstrip('/')}/spApi/storeTokens"
DEVELOPER_PROXY_ENDPOINT = f"{API_BASE_URL.rstrip('/')}/spApi/developerProxy"

SUCCESS_HTTP_STATUSES = frozenset({200, 201})


def ensure_auth_skill_available(caller: str = "uploads script") -> None:
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


def developer_proxy_post(
    region: str,
    path: str,
    access_token: str,
    *,
    query_string: Optional[str] = None,
    timeout: int = 120,
) -> dict:
    params: dict = {
        "region": region,
        "path": path,
        "method": "POST",
        "amzAccessToken": access_token,
        "contentType": "application/json",
    }
    if query_string:
        params["queryString"] = query_string
    return call_api(DEVELOPER_PROXY_ENDPOINT, params, timeout=timeout)


def path_for_upload_destination(resource: str) -> str:
    """resource 为下游 API 资源路径，如 aplus/2020-11-01/contentDocuments（勿带前导 /）。"""
    res = str(resource).strip().lstrip("/")
    enc = quote(res, safe="")
    return f"{UPLOADS_PATH_PREFIX}/uploadDestinations/{enc}"


def content_md5_base64(data: bytes) -> str:
    return base64.b64encode(hashlib.md5(data).digest()).decode("ascii")


def load_file_bytes(params: dict) -> bytes:
    if params.get("filePath"):
        p = Path(str(params["filePath"]).expanduser())
        if not p.is_file():
            print(f"filePath not found: {p}", file=sys.stderr)
            sys.exit(1)
        return p.read_bytes()
    if params.get("contentBase64"):
        try:
            return base64.b64decode(str(params["contentBase64"]))
        except Exception as e:
            print(f"Invalid contentBase64: {e}", file=sys.stderr)
            sys.exit(1)
    if "content" in params:
        raw = params["content"]
        if isinstance(raw, str):
            return raw.encode("utf-8")
        print("content must be a string", file=sys.stderr)
        sys.exit(1)
    return b""


def resolve_content_md5(params: dict) -> str:
    if params.get("contentMD5"):
        return str(params["contentMD5"]).strip()
    data = load_file_bytes(params)
    if not data:
        print(
            "Missing contentMD5, or provide filePath/content/contentBase64 to auto-compute.",
            file=sys.stderr,
        )
        sys.exit(1)
    return content_md5_base64(data)


def resolve_marketplace_id(params: dict) -> str:
    mid = params.get("marketplaceId")
    if mid is None and params.get("marketplaceIds") is not None:
        mids = params["marketplaceIds"]
        if isinstance(mids, list) and mids:
            mid = mids[0]
            if len(mids) > 1:
                print(
                    "Warning: createUploadDestinationForResource uses one marketplaceId; using first.",
                    file=sys.stderr,
                )
        elif isinstance(mids, str) and mids.strip():
            mid = mids.strip()
    if mid is None or not str(mid).strip():
        print("Missing marketplaceId (or marketplaceIds).", file=sys.stderr)
        sys.exit(1)
    return str(mid).strip()


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
