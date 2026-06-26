#!/usr/bin/env bash
set -euo pipefail

# iHRFlow MCP Client wrapper
# Encapsulates JSON-RPC 2.0 over Streamable HTTP (FastMCP)
#
# Usage:
#   mcp-call.sh init                              # initialize session
#   mcp-call.sh login                             # authenticate with env credentials
#   mcp-call.sh call <tool> '<json_args>'         # invoke a tool
#   mcp-call.sh resource <uri>                    # read an MCP resource
#
# Required env: IHRFLOW_MCP_URL, IHRFLOW_USERNAME, IHRFLOW_PASSWORD
# Optional env: IHRFLOW_TENANT_ID, IHRFLOW_API_KEY

readonly SESSION_FILE="/tmp/ihrflow-mcp-session-${USER:-unknown}"
readonly MCP_URL="${IHRFLOW_MCP_URL:?IHRFLOW_MCP_URL is not set}"

_request_id=0
_next_id() { _request_id=$((_request_id + 1)); echo "$_request_id"; }

_common_headers() {
  local -a h=(
    -H "Content-Type: application/json"
    -H "Accept: application/json, text/event-stream"
  )
  if [[ -n "${IHRFLOW_API_KEY:-}" ]]; then
    h+=(-H "X-API-Key: ${IHRFLOW_API_KEY}")
  fi
  if [[ -f "$SESSION_FILE" ]]; then
    h+=(-H "Mcp-Session-Id: $(cat "$SESSION_FILE")")
  fi
  printf '%s\n' "${h[@]}"
}

_parse_sse() {
  # Reads curl output (SSE or plain JSON), extracts the last JSON-RPC data payload.
  local raw="$1"
  # If the response contains SSE framing, extract last data: line
  if printf '%s' "$raw" | grep -q '^data: '; then
    printf '%s' "$raw" | grep '^data: ' | tail -1 | sed 's/^data: //'
  else
    # Plain JSON response (some endpoints return JSON directly)
    printf '%s' "$raw"
  fi
}

_check_error() {
  local json="$1"
  if printf '%s' "$json" | jq -e '.error' >/dev/null 2>&1; then
    printf '%s' "$json" | jq -r '.error'
    return 1
  fi
  return 0
}

cmd_init() {
  # Remove stale session
  rm -f "$SESSION_FILE"

  local id
  id=$(_next_id)
  local body
  body=$(jq -n --argjson id "$id" '{
    jsonrpc: "2.0",
    id: $id,
    method: "initialize",
    params: {
      protocolVersion: "2025-03-26",
      capabilities: {},
      clientInfo: { name: "ihrflow-skill", version: "1.0.0" }
    }
  }')

  local bodyfile headerfile
  bodyfile=$(mktemp)
  headerfile=$(mktemp)

  local headers_arr=()
  while IFS= read -r line; do headers_arr+=("$line"); done < <(_common_headers)

  curl -s -o "$bodyfile" -D "$headerfile" \
    -X POST "$MCP_URL" \
    "${headers_arr[@]}" \
    -d "$body" 2>/dev/null

  # Extract session ID from response headers
  local session_id
  session_id=$(grep -i '^mcp-session-id:' "$headerfile" | tr -d '\r' | awk '{print $2}' | head -1)
  rm -f "$headerfile"

  if [[ -n "$session_id" ]]; then
    printf '%s' "$session_id" > "$SESSION_FILE"
  fi

  local raw
  raw=$(cat "$bodyfile")
  rm -f "$bodyfile"

  local result
  result=$(_parse_sse "$raw")

  # Send initialized notification (reload headers to include new session)
  local notify_headers=()
  while IFS= read -r line; do notify_headers+=("$line"); done < <(_common_headers)
  curl -s -X POST "$MCP_URL" \
    "${notify_headers[@]}" \
    -d "$(jq -n '{jsonrpc:"2.0",method:"notifications/initialized"}')" \
    >/dev/null 2>&1 || true

  printf '%s' "$result" | jq -r '.result // .' 2>/dev/null || printf '%s' "$result"
}

cmd_login() {
  local username="${IHRFLOW_USERNAME:?IHRFLOW_USERNAME is not set}"
  local password="${IHRFLOW_PASSWORD:?IHRFLOW_PASSWORD is not set}"
  local tenant_id="${IHRFLOW_TENANT_ID:-}"

  if [[ ! -f "$SESSION_FILE" ]]; then
    cmd_init >/dev/null
  fi

  local args
  args=$(jq -n \
    --arg u "$username" \
    --arg p "$password" \
    --arg t "$tenant_id" \
    'if $t == "" then {username:$u, password:$p} else {username:$u, password:$p, tenant_id:$t} end')

  _call_tool "login" "$args"
}

_call_tool() {
  local tool_name="$1"
  local tool_args="${2:-{\}}"
  local id
  id=$(_next_id)

  local body
  body=$(jq -n \
    --argjson id "$id" \
    --arg name "$tool_name" \
    --argjson args "$tool_args" \
    '{jsonrpc:"2.0", id:$id, method:"tools/call", params:{name:$name, arguments:$args}}')

  local headers_arr=()
  while IFS= read -r line; do headers_arr+=("$line"); done < <(_common_headers)

  local raw
  raw=$(curl -s -X POST "$MCP_URL" \
    "${headers_arr[@]}" \
    -d "$body" 2>/dev/null)

  local result
  result=$(_parse_sse "$raw")

  # Extract text content from MCP tool result
  local content
  if printf '%s' "$result" | jq -e '.result.content' >/dev/null 2>&1; then
    content=$(printf '%s' "$result" | jq -r '.result.content[0].text // empty' 2>/dev/null)
    if [[ -n "$content" ]]; then
      # Try to parse as JSON for pretty output
      printf '%s' "$content" | jq . 2>/dev/null || printf '%s\n' "$content"
      return 0
    fi
  fi

  # Check for JSON-RPC error
  if printf '%s' "$result" | jq -e '.error' >/dev/null 2>&1; then
    printf '%s' "$result" | jq '{error: .error}' 2>/dev/null || printf '%s\n' "$result"
    return 1
  fi

  # Fallback: print raw result
  printf '%s' "$result" | jq . 2>/dev/null || printf '%s\n' "$result"
}

cmd_call() {
  local tool_name="${1:?Usage: mcp-call.sh call <tool_name> [json_args]}"
  local tool_args="${2:-{\}}"

  if [[ ! -f "$SESSION_FILE" ]]; then
    cmd_init >/dev/null
    cmd_login >/dev/null
  fi

  _call_tool "$tool_name" "$tool_args"
}

cmd_resource() {
  local uri="${1:?Usage: mcp-call.sh resource <uri>}"
  local id
  id=$(_next_id)

  if [[ ! -f "$SESSION_FILE" ]]; then
    cmd_init >/dev/null
    cmd_login >/dev/null
  fi

  local body
  body=$(jq -n \
    --argjson id "$id" \
    --arg uri "$uri" \
    '{jsonrpc:"2.0", id:$id, method:"resources/read", params:{uri:$uri}}')

  local headers_arr=()
  while IFS= read -r line; do headers_arr+=("$line"); done < <(_common_headers)

  local raw
  raw=$(curl -s -X POST "$MCP_URL" \
    "${headers_arr[@]}" \
    -d "$body" 2>/dev/null)

  local result
  result=$(_parse_sse "$raw")

  local content
  if printf '%s' "$result" | jq -e '.result.contents' >/dev/null 2>&1; then
    content=$(printf '%s' "$result" | jq -r '.result.contents[0].text // empty' 2>/dev/null)
    if [[ -n "$content" ]]; then
      printf '%s' "$content" | jq . 2>/dev/null || printf '%s\n' "$content"
      return 0
    fi
  fi

  printf '%s' "$result" | jq . 2>/dev/null || printf '%s\n' "$result"
}

case "${1:-help}" in
  init)     cmd_init ;;
  login)    cmd_login ;;
  call)     shift; cmd_call "$@" ;;
  resource) shift; cmd_resource "$@" ;;
  *)
    cat >&2 <<'USAGE'
iHRFlow MCP Client

Commands:
  init                          Initialize MCP session
  login                         Authenticate with env credentials
  call <tool> [json_args]       Invoke an MCP tool
  resource <uri>                Read an MCP resource

Environment:
  IHRFLOW_MCP_URL   (required)  MCP endpoint URL
  IHRFLOW_USERNAME  (required)  iHRFlow username
  IHRFLOW_PASSWORD  (required)  iHRFlow password
  IHRFLOW_TENANT_ID (optional)  Tenant ID
  IHRFLOW_API_KEY   (optional)  Transport API key
USAGE
    exit 1
    ;;
esac
