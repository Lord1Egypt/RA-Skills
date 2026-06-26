#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeChat API Proxy Server - Runs on a VPS with a fixed public IP.

Proxies WeChat API requests so the caller's dynamic home IP doesn't matter.
Only the VPS IP (whitelisted in WeChat) is seen by api.weixin.qq.com.

Usage:
    PROXY_TOKEN=your-secret python3 wechat_proxy_server.py

Then set in your local .env:
    WECHAT_PROXY_URL=http://43.156.101.197:9500
    WECHAT_PROXY_TOKEN=your-secret
"""

import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, urlencode, parse_qs
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")
PORT = int(os.environ.get("PORT", "9500"))

WECHAT_API_BASE = "https://api.weixin.qq.com/cgi-bin"

ROUTE_MAP = {
    "/token": "/token",
    "/uploadimg": "/media/uploadimg",
    "/add_material": "/material/add_material",
    "/draft/add": "/draft/add",
    "/freepublish": "/freepublish/submit",
}


class ProxyHandler(BaseHTTPRequestHandler):

    def _check_auth(self):
        token = self.headers.get("X-Proxy-Token", "")
        if not PROXY_TOKEN:
            self._send_json(500, {"error": "PROXY_TOKEN not configured on server"})
            return False
        if token != PROXY_TOKEN:
            self._send_json(403, {"error": "Invalid proxy token"})
            return False
        return True

    def _get_wechat_url(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        if path not in ROUTE_MAP:
            self._send_json(404, {"error": f"Unknown path: {path}", "available": list(ROUTE_MAP.keys())})
            return None, None
        wechat_path = WECHAT_API_BASE + ROUTE_MAP[path]
        qs = parsed.query
        if qs:
            wechat_path = f"{wechat_path}?{qs}"
        return wechat_path, parsed

    def do_GET(self):
        if not self._check_auth():
            return
        wechat_url, _ = self._get_wechat_url()
        if not wechat_url:
            return
        try:
            req = Request(wechat_url, method="GET")
            with urlopen(req, timeout=15) as resp:
                body = resp.read()
                self._send_json(resp.status, json.loads(body))
        except HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            self._send_json(e.code, {"error": f"WeChat API error: {e.code}", "detail": detail})
        except URLError as e:
            self._send_json(502, {"error": f"Network error: {str(e.reason)}"})
        except Exception as e:
            self._send_json(500, {"error": f"Proxy error: {str(e)}"})

    def do_POST(self):
        if not self._check_auth():
            return
        wechat_url, _ = self._get_wechat_url()
        if not wechat_url:
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length else b""
        content_type = self.headers.get("Content-Type", "application/json")

        try:
            req = Request(wechat_url, data=body, method="POST")
            req.add_header("Content-Type", content_type)
            timeout = 120 if "multipart" in content_type else 30
            with urlopen(req, timeout=timeout) as resp:
                resp_body = resp.read()
                self._send_json(resp.status, json.loads(resp_body))
        except HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")
            self._send_json(e.code, {"error": f"WeChat API error: {e.code}", "detail": detail})
        except URLError as e:
            self._send_json(502, {"error": f"Network error: {str(e.reason)}"})
        except Exception as e:
            self._send_json(500, {"error": f"Proxy error: {str(e)}"})

    def _send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"[proxy] {self.address_string()} - {fmt % args}")


def main():
    if not PROXY_TOKEN:
        print("ERROR: Set PROXY_TOKEN environment variable")
        print("  export PROXY_TOKEN=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')")
        sys.exit(1)

    server = HTTPServer(("0.0.0.0", PORT), ProxyHandler)
    print(f"WeChat API Proxy listening on 0.0.0.0:{PORT}")
    print(f"Routes: {list(ROUTE_MAP.keys())}")
    print(f"Auth: X-Proxy-Token header required")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.server_close()


if __name__ == "__main__":
    main()
