#!/usr/bin/env bash
set -euo pipefail

TOOL_NAME="${1:-}"
ARGS_JSON="${2:-}"
if [[ -z "$ARGS_JSON" ]]; then
  ARGS_JSON='{}'
fi
BASE_URL="${3:-${BIL_CRAWL_URL:-http://127.0.0.1:39002}}"
MCP_URL="$BASE_URL/mcp"

if [[ -z "$TOOL_NAME" ]]; then
  echo "Usage: $0 <tool_name> [args_json] [base_url]" >&2
  echo "Example: $0 list_archives '{"\"platform\"":"\"bilibili\"","\"limit\"":10}'" >&2
  exit 2
fi

curl -fsS "$BASE_URL/" >/dev/null 2>&1 || {
  echo "Service not reachable at $BASE_URL" >&2
  exit 1
}

init_payload='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"media-crawler-local","version":"1.0.0"}}}'

tmp_args_file=$(mktemp)
trap 'rm -f "$tmp_args_file"' EXIT
printf '%s' "$ARGS_JSON" >"$tmp_args_file"

call_payload=$(TOOL_NAME_ENV="$TOOL_NAME" ARGS_FILE_ENV="$tmp_args_file" node -e '
const fs = require("node:fs");
const tool = process.env.TOOL_NAME_ENV || "";
const file = process.env.ARGS_FILE_ENV || "";
const raw = (file && fs.existsSync(file)) ? fs.readFileSync(file, "utf8") : "{}";
let args={};
try { args=JSON.parse(raw); } catch (e) {
  console.error("Invalid args_json, must be valid JSON object");
  process.exit(2);
}
if (typeof args !== "object" || Array.isArray(args) || args===null) {
  console.error("args_json must be a JSON object");
  process.exit(2);
}
process.stdout.write(JSON.stringify({jsonrpc:"2.0",id:2,method:"tools/call",params:{name:tool,arguments:args}}));
')

curl -sS -N "$MCP_URL" \
  -H 'Accept: application/json, text/event-stream' \
  -H 'Content-Type: application/json' \
  --data "$init_payload" >/dev/null

curl -sS -N "$MCP_URL" \
  -H 'Accept: application/json, text/event-stream' \
  -H 'Content-Type: application/json' \
  --data "$call_payload"

echo
