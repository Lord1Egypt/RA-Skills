#!/usr/bin/env python3
"""
TikTok Video API 通用代理 - LinkFox Skill
经 LinkFox 网关 /tiktokVideo/developerProxy 转发至紫鸟 tiktok-proxy/creator/{region}/{path}。

Usage:
  python video_proxy.py '{"path": "video/upload/...", "method": "POST", "ttsAccessToken": "TTP_xxx", "body": "{...}"}'

参数（JSON）：
  path           必填，TikTok Creator API 相对路径（不含 tiktok-proxy 前缀）
  method         必填，GET / POST / PUT / DELETE
  ttsAccessToken 必填，creator access_token（由 linkfox-tiktok-video-auth 授权获得）
  queryString    可选，查询字符串（不含 ?）
  body           可选，POST/PUT 请求体（JSON 字符串）
  region         可选，默认 global
  contentType    可选，默认 application/json

环境变量：
  LINKFOXAGENT_API_KEY        必填，网关鉴权
  TIKTOK_VIDEO_API_BASE_URL   可选，覆盖网关根 URL
"""

import json
import os
import sys
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


API_BASE_URL = os.environ.get(
    "TIKTOK_VIDEO_API_BASE_URL", "https://tool-gateway.linkfox.com"
)
API_ENDPOINT = f"{API_BASE_URL.rstrip('/')}/tiktokVideo/developerProxy"

ALLOWED_PATH_PREFIXES = ("affiliate_creator", "video", "creator")


def get_api_key():
    key = os.environ.get("LINKFOXAGENT_API_KEY")
    if not key:
        print(
            "API Key not configured. Please set the environment variable:\n"
            "  export LINKFOXAGENT_API_KEY=your-key-here",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


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


def call_api(params: dict) -> dict:
    api_key = get_api_key()
    data = json.dumps(params).encode("utf-8")
    req = Request(
        API_ENDPOINT,
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


def main():
    if len(sys.argv) < 2:
        print("Usage: video_proxy.py '<JSON parameters>'", file=sys.stderr)
        print(
            'Example: video_proxy.py \'{"path": "video/...", "method": "GET", '
            '"ttsAccessToken": "TTP_xxx"}\'',
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        params = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"Invalid parameter format: {e}", file=sys.stderr)
        sys.exit(1)

    for field in ("path", "method", "ttsAccessToken"):
        val = params.get(field)
        if not isinstance(val, str) or not val.strip():
            print(f"Error: '{field}' parameter is required", file=sys.stderr)
            sys.exit(1)

    params["path"] = params["path"].strip().lstrip("/")
    assert_path_allowed(params["path"])
    params.setdefault("region", "global")

    result = call_api(params)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
