#!/usr/bin/env python3
"""Minimal McDonald's MCP JSON-RPC client.

Examples:
  python3 scripts/mcd_rpc.py tools/list
  python3 scripts/mcd_rpc.py tools/call '{"name":"delivery-query-addresses","arguments":{}}'
"""

import json
import os
import sys
import urllib.request

URL = os.getenv("MCD_MCP_URL", "https://mcp.mcd.cn")
TOKEN = os.getenv("MCD_MCP_TOKEN", "")


def rpc(method: str, params=None, req_id: int = 1):
    payload = {
        "jsonrpc": "2.0",
        "id": req_id,
        "method": method,
        "params": params or {},
    }
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(), method="POST")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def notify_initialized():
    payload = {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(), method="POST")
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    with urllib.request.urlopen(req, timeout=60):
        return None


def initialize():
    return rpc(
        "initialize",
        {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "mcd-rpc-script", "version": "0.1.0"},
        },
        1,
    )


def main():
    if not TOKEN:
        print("Set MCD_MCP_TOKEN first", file=sys.stderr)
        sys.exit(2)
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(2)

    method = sys.argv[1]
    params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    init_res = initialize()
    notify_initialized()
    res = rpc(method, params, 2)
    print(json.dumps({"initialize": init_res, "result": res}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
