#!/usr/bin/env python3
"""Minimal JSON-RPC client for the Podcast Robot MCP server.

Usage:
    mcp_robot.py call <tool> '<json-args>'
    mcp_robot.py tools

Written by Adam Curry's Muse agent; fixes by Podcast Robot. Guide: https://podcastindexrobot.com/llms.txt
The server is open: no key, no OAuth. Streamable HTTP, stateless.
"""
import json
import subprocess
import sys

URL = "https://podcastindexrobot.com/mcp"
_next_id = [1]


def rpc(method, params=None):
    """Call via curl: the server sometimes closes connections early and
    urllib raises IncompleteRead; curl -i lets us parse what arrived."""
    body = {"jsonrpc": "2.0", "id": _next_id[0], "method": method}
    _next_id[0] += 1
    if params is not None:
        body["params"] = params
    p = subprocess.run(
        ["curl", "-s", "--max-time", "40", "-X", "POST", URL,
         "-H", "Content-Type: application/json",
         "-H", "Accept: application/json, text/event-stream",
         "-H", "User-Agent: PodcastRobotSkill/0.2",
         "-d", json.dumps(body)],
        capture_output=True, text=True, timeout=60,
    )
    raw = p.stdout
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("data:"):
            line = line[5:].strip()
        if line.startswith("{"):
            return json.loads(line)
    raise RuntimeError("no JSON payload in response: " + raw[:200])


def call(tool, args):
    out = rpc("tools/call", {"name": tool, "arguments": args})
    if "error" in out:
        raise RuntimeError(out["error"])
    return out["result"]["content"]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    cmd = sys.argv[1]
    if cmd == "tools":
        out = rpc("tools/list", {})
        for t in out["result"]["tools"]:
            print(t["name"])
    elif cmd == "call":
        tool = sys.argv[2]
        args = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        for block in call(tool, args):
            if block.get("type") == "text":
                print(block["text"])
            else:
                print(json.dumps(block)[:500])
    else:
        print("unknown command", cmd)
        sys.exit(2)


if __name__ == "__main__":
    main()
