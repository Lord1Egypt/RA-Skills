#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeChat API Proxy - Tencent Cloud SCF Function

Proxies WeChat API requests through a Tencent Cloud Function with a fixed
public egress IP. This allows the SCF's static IP to be whitelisted in the
WeChat Official Account IP whitelist, solving the dynamic home IP problem.

Supported endpoints:
  - POST /token         -> WeChat access_token
  - POST /uploadimg     -> Upload content image
  - POST /add_material  -> Upload material (cover image)
  - POST /draft/add     -> Create draft article
  - POST /freepublish   -> Submit for publishing

All requests must include the header:
  X-Proxy-Token: <shared secret>
"""

import json
import os
import urllib.request
import urllib.parse
import urllib.error

# Shared secret for authenticating callers
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")

# WeChat API base
WECHAT_API_BASE = "https://api.weixin.qq.com/cgi-bin"

# Route map: proxy path -> WeChat API path
ROUTE_MAP = {
    "/token": "/token",
    "/uploadimg": "/media/uploadimg",
    "/add_material": "/material/add_material",
    "/draft/add": "/draft/add",
    "/freepublish": "/freepublish/submit",
}


def main_handler(event, context):
    """SCF entry point (API Gateway trigger)."""

    # --- Auth check ---
    headers = event.get("headers", {})
    # API Gateway may lowercase header keys
    token = headers.get("x-proxy-token") or headers.get("X-Proxy-Token", "")

    if not PROXY_TOKEN:
        return _resp(500, {"error": "PROXY_TOKEN not configured on server"})

    if token != PROXY_TOKEN:
        return _resp(403, {"error": "Invalid proxy token"})

    # --- Routing ---
    path = event.get("path", "")
    http_method = event.get("httpMethod", "GET").upper()

    if path not in ROUTE_MAP:
        return _resp(404, {"error": f"Unknown path: {path}", "available": list(ROUTE_MAP.keys())})

    wechat_path = WECHAT_API_BASE + ROUTE_MAP[path]

    # --- Forward query string params (e.g. access_token, grant_type, appid, secret, type) ---
    query = event.get("queryString", {}) or event.get("queryStringParameters", {}) or {}
    if query:
        qs = urllib.parse.urlencode(query, doseq=True)
        wechat_path = f"{wechat_path}?{qs}"

    # --- Forward request ---
    try:
        if http_method == "GET":
            req = urllib.request.Request(wechat_path, method="GET")
            with urllib.request.urlopen(req, timeout=15) as resp:
                body = resp.read()
                return _resp(resp.status, json.loads(body))

        elif http_method == "POST":
            content_type = headers.get("content-type") or headers.get("Content-Type", "")

            if "multipart/form-data" in content_type:
                # For file uploads, reconstruct the multipart body
                # SCF API Gateway passes base64-encoded body for binary content
                is_base64 = event.get("isBase64Encoded", False)
                raw_body = event.get("body", "")

                if is_base64:
                    import base64
                    body_bytes = base64.b64decode(raw_body)
                else:
                    body_bytes = raw_body.encode("utf-8") if isinstance(raw_body, str) else raw_body

                req = urllib.request.Request(
                    wechat_path,
                    data=body_bytes,
                    method="POST",
                    headers={"Content-Type": content_type},
                )
                with urllib.request.urlopen(req, timeout=120) as resp:
                    resp_body = resp.read()
                    return _resp(resp.status, json.loads(resp_body))

            else:
                # JSON body
                raw_body = event.get("body", "{}")
                if isinstance(raw_body, str):
                    body_bytes = raw_body.encode("utf-8")
                else:
                    body_bytes = raw_body

                req = urllib.request.Request(
                    wechat_path,
                    data=body_bytes,
                    method="POST",
                    headers={"Content-Type": "application/json; charset=utf-8"},
                )
                with urllib.request.urlopen(req, timeout=30) as resp:
                    resp_body = resp.read()
                    return _resp(resp.status, json.loads(resp_body))

        else:
            return _resp(405, {"error": f"Method {http_method} not supported"})

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        return _resp(e.code, {"error": f"WeChat API error: {e.code}", "detail": error_body})
    except urllib.error.URLError as e:
        return _resp(502, {"error": f"Network error: {str(e.reason)}"})
    except Exception as e:
        return _resp(500, {"error": f"Proxy error: {str(e)}"})


def _resp(status_code, body):
    """Format API Gateway response."""
    return {
        "isBase64Encoded": False,
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, ensure_ascii=False),
    }
