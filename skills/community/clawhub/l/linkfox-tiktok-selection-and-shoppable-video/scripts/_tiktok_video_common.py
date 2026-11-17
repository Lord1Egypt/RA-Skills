"""Shared helpers for linkfox-tiktok-video (accountTokens + developerProxy)."""

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

API_BASE_URL = os.environ.get("LINKFOX_TOOL_GATEWAY") or "https://tool-gateway.linkfox.com"
ACCOUNT_TOKENS_ENDPOINT = f"{API_BASE_URL.rstrip('/')}/tiktokVideo/accountTokens"
DEVELOPER_PROXY_ENDPOINT = f"{API_BASE_URL.rstrip('/')}/tiktokVideo/developerProxy"

REQUIRED_SKILL = "linkfox-tiktok-video-auth"
DEPENDENCY_EXIT_CODE = 42

ALLOWED_PATH_PREFIXES = ("affiliate_creator", "video", "creator")


def ensure_auth_skill_available(caller: str = "video script") -> None:
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
    """
    获取配置在环境变量的API Key。
    如果获取不到，按 SKILL.md 的 **## 解决认证和积分问题** 处理。
    """
    key = os.environ.get("LINKFOXAGENT_API_KEY")
    if not key:
        print(
            "API Key 未配置",
            file=sys.stderr,
        )
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


def resolve_account_tokens(params: dict) -> dict:
    if params.get("ttsAccessToken"):
        return {"accessToken": str(params["ttsAccessToken"]).strip()}

    open_id = params.get("openId")
    if not open_id or not str(open_id).strip():
        print("Missing required field: openId OR ttsAccessToken", file=sys.stderr)
        sys.exit(1)

    result = call_api(ACCOUNT_TOKENS_ENDPOINT, {"openId": str(open_id).strip()})
    if result.get("errcode"):
        return result
    if "accessToken" not in result:
        return {"error": "accountTokens response missing accessToken", "details": result}
    return result


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
    tts_access_token: str,
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
        "ttsAccessToken": tts_access_token,
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
