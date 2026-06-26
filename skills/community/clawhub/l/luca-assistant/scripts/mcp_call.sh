#!/usr/bin/env bash
# Generic MCP tool caller for luca-assistant.
# Spawns luca-mcp as a subprocess, sends JSON-RPC initialize + tools/call,
# and prints the result.
#
# Usage: mcp_call.sh <tool_name> '<json_args>'
# Example: mcp_call.sh luca_query_card_details '{"card_name":"Chase Sapphire Preferred"}'
set -euo pipefail

# Ensure uv-installed binaries are on PATH
export PATH="$HOME/.local/bin:$PATH"

TOOL_NAME="${1:?Usage: mcp_call.sh <tool_name> '<json_args>'}"
TOOL_ARGS="${2:-\{\}}"

# Default DB location if not set
export DB_PATH="${DB_PATH:-${HOME}/.local/share/luca/luca.db}"

python3 - "$TOOL_NAME" "$TOOL_ARGS" <<'PY'
import json
import subprocess
import sys

tool_name = sys.argv[1]
tool_args = json.loads(sys.argv[2])

proc = subprocess.Popen(
    ["luca-mcp"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

# JSON-RPC: initialize
init_req = json.dumps({
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "luca-skill", "version": "1.0.0"},
    },
})

# JSON-RPC: tools/call
call_req = json.dumps({
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {"name": tool_name, "arguments": tool_args},
})

# Send both requests, close stdin to signal EOF
stdin_payload = init_req + "\n" + call_req + "\n"
stdout, stderr = proc.communicate(input=stdin_payload, timeout=60)

# Parse responses — look for the tools/call result (id=2)
for line in stdout.strip().split("\n"):
    line = line.strip()
    if not line:
        continue
    try:
        msg = json.loads(line)
        if msg.get("id") == 2:
            result = msg.get("result", {})
            content = result.get("content", [])
            for item in content:
                if item.get("type") == "text":
                    # Pretty-print if it's JSON
                    try:
                        parsed = json.loads(item["text"])
                        print(json.dumps(parsed, indent=2, ensure_ascii=False))
                    except (json.JSONDecodeError, TypeError):
                        print(item["text"])
            sys.exit(0)
    except json.JSONDecodeError:
        continue

print(f"Error: no response for tool '{tool_name}'", file=sys.stderr)
if stderr.strip():
    print(f"stderr: {stderr.strip()}", file=sys.stderr)
sys.exit(1)
PY
