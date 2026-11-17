#!/usr/bin/env python3
"""HeyRepli CLI helper. Stdlib only (Python 3.8+).

Reads API key from env HEYREPLI_API_KEY (or --api-key).

Usage:
  python heyrepli.py list-tools
  python heyrepli.py usage
  python heyrepli.py call <tool_name> --args '{"videoId":"dQw4w9WgXcQ"}'
  python heyrepli.py rest <posts|replies|schedule|mentions|analytics> [--params k=v ...] [--body '<json>']
  python heyrepli.py health
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = os.environ.get("HEYREPLI_BASE_URL", "https://api.heyrepli.com")
MCP_URL = BASE + "/api/v1/mcp"
OPEN_URL = BASE + "/api/v1/open"

REST_METHODS = {
    "posts": "GET",
    "replies": "POST",
    "schedule": "POST",
    "mentions": "GET",
    "analytics": "GET",
}


def _request(url, method="GET", headers=None, body=None, timeout=60):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    # Cloudflare bot protection blocks default Python-urllib UA (error 1010)
    req.add_header("User-Agent", os.environ.get("HEYREPLI_UA", "heyrepli-skill/1.0 (+https://heyrepli.com)"))
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            out = json.loads(raw)
        except Exception:
            out = {"ok": False, "error": {"code": str(e.code), "message": raw[:500]}}
        _emit(out)
        sys.exit(1)
    except urllib.error.URLError as e:
        _emit({"ok": False, "error": {"code": "NETWORK", "message": str(e.reason)}})
        sys.exit(1)
    try:
        _emit(json.loads(raw))
    except Exception:
        print(raw)


def _emit(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def _auth_headers(args):
    key = args.api_key or os.environ.get("HEYREPLI_API_KEY")
    if not key:
        print("ERROR: set HEYREPLI_API_KEY env var or pass --api-key. "
              "Get one at https://app.heyrepli.com/dashboard/settings/account", file=sys.stderr)
        sys.exit(2)
    return {"X-API-Key": key}


def cmd_mcp(args, tool=None, arguments=None, method="tools/call"):
    payload = {"jsonrpc": "2.0", "id": 1, "method": method}
    if tool is not None:
        payload["params"] = {"name": tool, "arguments": arguments or {}}
    _request(MCP_URL, "POST", _auth_headers(args), payload)


def main():
    p = argparse.ArgumentParser(description="HeyRepli API helper")
    p.add_argument("--api-key", default=None)
    p.add_argument("--base-url", default=None)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("health")
    sub.add_parser("list-tools")
    sub.add_parser("usage")

    pc = sub.add_parser("call", help="call an MCP tool")
    pc.add_argument("tool")
    pc.add_argument("--args", default="{}", help="JSON object of arguments")

    pr = sub.add_parser("rest", help="call Open REST endpoint")
    pr.add_argument("endpoint", choices=list(REST_METHODS))
    pr.add_argument("--params", nargs="*", default=[], help="k=v query params")
    pr.add_argument("--body", default=None, help="JSON body for POST endpoints")

    args = p.parse_args()
    if args.base_url:
        global BASE, MCP_URL, OPEN_URL
        BASE = args.base_url.rstrip("/")
        MCP_URL = BASE + "/api/v1/mcp"
        OPEN_URL = BASE + "/api/v1/open"

    if args.cmd == "health":
        _request(BASE + "/health")
    elif args.cmd == "list-tools":
        cmd_mcp(args, method="tools/list")
    elif args.cmd == "usage":
        cmd_mcp(args, tool="get_usage", arguments={})
    elif args.cmd == "call":
        try:
            tool_args = json.loads(args.args)
        except json.JSONDecodeError as e:
            print(f"ERROR: --args is not valid JSON: {e}", file=sys.stderr)
            sys.exit(2)
        cmd_mcp(args, tool=args.tool, arguments=tool_args)
    elif args.cmd == "rest":
        qs = {}
        for kv in args.params:
            if "=" not in kv:
                print(f"ERROR: --params expects k=v, got {kv!r}", file=sys.stderr)
                sys.exit(2)
            k, v = kv.split("=", 1)
            qs[k] = v
        url = OPEN_URL + "/" + args.endpoint
        if qs:
            url += "?" + urllib.parse.urlencode(qs)
        method = REST_METHODS[args.endpoint]
        body = None
        if args.body:
            try:
                body = json.loads(args.body)
            except json.JSONDecodeError as e:
                print(f"ERROR: --body is not valid JSON: {e}", file=sys.stderr)
                sys.exit(2)
        if method == "POST" and body is None:
            print("ERROR: POST endpoints require --body '<json>'", file=sys.stderr)
            sys.exit(2)
        _request(url, method, _auth_headers(args), body)


if __name__ == "__main__":
    main()
