"""Shared helpers for linkfox-tiktok-shop-fulfillment (ERP developerProxy, token backendized)."""

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

API_BASE_URL = (
    os.environ.get("LINKFOX_TOOL_GATEWAY")
    or os.environ.get("TIKTOK_SHOP_API_BASE_URL")
    or "https://tool-gateway.linkfox.com"
).rstrip("/")
DEVELOPER_PROXY_ENDPOINT = f"{API_BASE_URL}/tiktokShop/developerProxy"

REQUIRED_SKILL = "linkfox-tiktok-shop-auth"
DEPENDENCY_EXIT_CODE = 42
ERP_APP_TYPE = "erp"

# ERP fulfillment skill path whitelist
ALLOWED_PATH_PREFIXES = ("fulfillment", "authorization")


def ensure_auth_skill_available(caller: str = "shop-fulfillment script") -> None:
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
    key = os.environ.get("LINKFOX_AGENT_API_KEY") or os.environ.get("LINKFOXAGENT_API_KEY")
    if not key:
        print("API Key 未配置", file=sys.stderr)
        sys.exit(1)
    return key


def call_api(endpoint: str, params: dict) -> dict:
    api_key = get_api_key()
    data = json.dumps(params).encode("utf-8")
    req = Request(
        endpoint,
        data=data,
        headers={
            "Authorization": api_key,
            "Content-Type": "application/json",
            "User-Agent": "LinkFox-Skill/1.0",
            "SESSION_ID": os.environ.get("SESSION_ID", ""),
            "MODE_ID": os.environ.get("MODE_ID", ""),
            "APP_NAME": os.environ.get("APP_NAME", ""),
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=150) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        return {"error": f"HTTP {e.code}: {e.reason}", "details": body}
    except URLError as e:
        return {"error": f"Connection failed: {e.reason}"}


def require_open_id(params: dict) -> str:
    """ACCESS_TOKEN is backendized: developerProxy resolves token by openId + appType=erp."""
    if params.get("ttsAccessToken") and not params.get("openId"):
        print(
            "Error: ttsAccessToken is deprecated (ignored by gateway). "
            "Pass openId only; token is resolved server-side.",
            file=sys.stderr,
        )
        sys.exit(1)

    open_id = params.get("openId")
    if not open_id or not str(open_id).strip():
        print("Missing required field: openId", file=sys.stderr)
        sys.exit(1)
    return str(open_id).strip()


def assert_path_allowed(path: str) -> None:
    normalized = path.lstrip("/").replace("\\", "/")
    if ".." in normalized or "//" in normalized:
        print(f"Error: invalid path {path!r}", file=sys.stderr)
        sys.exit(1)
    if not any(
        normalized == prefix or normalized.startswith(prefix + "/")
        for prefix in ALLOWED_PATH_PREFIXES
    ):
        print(
            f"Error: path must start with one of {ALLOWED_PATH_PREFIXES}, got {path!r}",
            file=sys.stderr,
        )
        sys.exit(1)


def developer_proxy_call(
    open_id: str,
    path: str,
    method: str,
    region: Optional[str] = None,
    query_string: Optional[str] = None,
    body: Optional[str] = None,
    content_type: str = "application/json",
) -> dict:
    assert_path_allowed(path)
    proxy: dict[str, Any] = {
        "path": path.lstrip("/"),
        "method": method,
        "openId": open_id,
        "appType": ERP_APP_TYPE,
    }
    if region:
        proxy["region"] = str(region)
    if query_string:
        proxy["queryString"] = query_string
    if body is not None:
        proxy["body"] = body
        proxy["contentType"] = content_type
    return call_api(DEVELOPER_PROXY_ENDPOINT, proxy)


def qs_add(parts: list[str], key: str, value: str) -> None:
    parts.append(f"{key}={quote(str(value), safe='')}")


def merge_upstream_body(out: dict, proxy: dict, key: str) -> None:
    body_raw = proxy.get("body")
    if body_raw is None or not str(body_raw).strip():
        out[key] = None
        return
    try:
        out[key] = json.loads(body_raw)
    except json.JSONDecodeError:
        out[key] = body_raw


def parse_proxy_business_json(proxy: dict) -> Optional[dict]:
    body_raw = proxy.get("body")
    if body_raw is None or not str(body_raw).strip():
        return None
    try:
        parsed = json.loads(body_raw)
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None
