#!/bin/bash
# paper.sh — Paper Design MCP bridge for OpenClaw
# Connects to Paper's local MCP server via HTTP and translates tool calls.
#
# Usage:
#   paper.sh <tool_name> [json_arguments]
#
# Examples:
#   paper.sh get_basic_info
#   paper.sh create_artboard '{"name":"Login Screen","styles":{"width":"390px","height":"844px"}}'
#   paper.sh write_html '{"html":"<div style=\"padding:20px\">Hello</div>","targetNodeId":"F4-0","mode":"insert-children"}'
#   paper.sh get_screenshot '{"nodeId":"K9-0"}'
#   paper.sh get_screenshot '{"nodeId":"K9-0"}' --save /tmp/screenshot.jpg
#
# Environment:
#   PAPER_MCP_URL    — MCP endpoint (default: http://127.0.0.1:29979/mcp)
#   PAPER_SESSION    — Path to session cache file (default: /tmp/paper-mcp-session)
#   PAPER_SCREENSHOT_DIR — Where to save screenshots (default: /tmp/paper-screenshots)

set -euo pipefail

# --- Config ---
PAPER_MCP_URL="${PAPER_MCP_URL:-http://127.0.0.1:29979/mcp}"
PAPER_SESSION_FILE="${PAPER_SESSION:-/tmp/paper-mcp-session}"
PAPER_SCREENSHOT_DIR="${PAPER_SCREENSHOT_DIR:-/tmp/paper-screenshots}"
ACCEPT_HEADER="application/json, text/event-stream"

# --- Helpers ---

die() { echo "ERROR: $*" >&2; exit 1; }

# Check if Paper is reachable
check_paper() {
  if ! curl -s --max-time 3 -o /dev/null -w "%{http_code}" "$PAPER_MCP_URL" -X POST \
    -H "Content-Type: application/json" \
    -H "Accept: $ACCEPT_HEADER" \
    -d '{"jsonrpc":"2.0","method":"ping","id":0}' 2>/dev/null | grep -q "200\|400\|405"; then
    # Try a simple HEAD/OPTIONS to check if server is up at all
    if ! curl -s --max-time 3 -o /dev/null "$PAPER_MCP_URL" 2>/dev/null; then
      die "Paper is not running. Open the Paper app first."
    fi
  fi
}

# Parse SSE response — extract JSON from "data: {...}" lines
parse_sse() {
  local input="$1"
  # If response starts with "event:", it's SSE format
  if echo "$input" | grep -q "^event:"; then
    echo "$input" | grep "^data: " | sed 's/^data: //' | head -1
  else
    # Might be direct JSON
    echo "$input"
  fi
}

# Get or create MCP session
get_session() {
  # Check if cached session is still valid (less than 30 min old)
  if [ -f "$PAPER_SESSION_FILE" ]; then
    local age=$(( $(date +%s) - $(stat -f %m "$PAPER_SESSION_FILE" 2>/dev/null || echo 0) ))
    if [ "$age" -lt 1800 ]; then
      cat "$PAPER_SESSION_FILE"
      return 0
    fi
  fi

  # Initialize new session
  local response
  response=$(curl -s -i -X POST "$PAPER_MCP_URL" \
    -H "Content-Type: application/json" \
    -H "Accept: $ACCEPT_HEADER" \
    -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"openclaw-paper-skill","version":"1.0.0"}},"id":1}' 2>&1)

  local session_id
  session_id=$(echo "$response" | grep -i "mcp-session-id" | tr -d '\r\n' | awk '{print $2}')

  if [ -z "$session_id" ]; then
    die "Failed to initialize MCP session. Is Paper open?"
  fi

  # Send initialized notification
  curl -s -X POST "$PAPER_MCP_URL" \
    -H "Content-Type: application/json" \
    -H "Accept: $ACCEPT_HEADER" \
    -H "Mcp-Session-Id: $session_id" \
    -d '{"jsonrpc":"2.0","method":"notifications/initialized"}' > /dev/null 2>&1

  # Cache session
  echo "$session_id" > "$PAPER_SESSION_FILE"
  echo "$session_id"
}

# Make a tool call
call_tool() {
  local tool_name="$1"
  local _default_args='{}'
  local arguments="${2:-$_default_args}"
  local session_id
  session_id=$(get_session)

  local payload
  payload=$(python3 -c "
import json, sys
tool = sys.argv[1]
args = json.loads(sys.argv[2])
print(json.dumps({
    'jsonrpc': '2.0',
    'method': 'tools/call',
    'params': {'name': tool, 'arguments': args},
    'id': 2
}))
" "$tool_name" "$arguments" 2>/dev/null) || die "Invalid JSON arguments: $arguments"

  local response
  response=$(curl -s -X POST "$PAPER_MCP_URL" \
    -H "Content-Type: application/json" \
    -H "Accept: $ACCEPT_HEADER" \
    -H "Mcp-Session-Id: $session_id" \
    -d "$payload" 2>&1)

  # Check for session expired (re-init and retry once)
  if echo "$response" | grep -q '"code":-32001\|"code":-32600\|Session.*not found\|session.*expired'; then
    rm -f "$PAPER_SESSION_FILE"
    session_id=$(get_session)
    response=$(curl -s -X POST "$PAPER_MCP_URL" \
      -H "Content-Type: application/json" \
      -H "Accept: $ACCEPT_HEADER" \
      -H "Mcp-Session-Id: $session_id" \
      -d "$payload" 2>&1)
  fi

  # Parse SSE
  local json_response
  json_response=$(parse_sse "$response")

  echo "$json_response"
}

# Handle screenshot: extract base64 image, save to file, return path
handle_screenshot() {
  local json_response="$1"
  local save_path="${2:-}"

  mkdir -p "$PAPER_SCREENSHOT_DIR"

  if [ -z "$save_path" ]; then
    save_path="$PAPER_SCREENSHOT_DIR/screenshot-$(date +%s).jpg"
  fi

  # Extract base64 image data and save
  python3 -c "
import json, base64, sys

data = json.loads(sys.stdin.read())
result = data.get('result', {})
content = result.get('content', [])

for item in content:
    if item.get('type') == 'image':
        img_data = base64.b64decode(item['data'])
        with open(sys.argv[1], 'wb') as f:
            f.write(img_data)
        print(f'Screenshot saved: {sys.argv[1]}')
        print(f'Size: {len(img_data)} bytes')
        print(f'Format: {item.get(\"mimeType\", \"unknown\")}')
        sys.exit(0)

print('No image in response')
sys.exit(1)
" "$save_path" <<< "$json_response"
}

# Extract text content from tool response
extract_text() {
  local json_response="$1"
  python3 -c "
import json, sys

data = json.loads(sys.stdin.read())

# Check for errors
if 'error' in data:
    err = data['error']
    print(f'Error ({err.get(\"code\", \"?\")}): {err.get(\"message\", \"unknown\")}')
    sys.exit(1)

result = data.get('result', {})
content = result.get('content', [])

for item in content:
    if item.get('type') == 'text':
        print(item['text'])
" <<< "$json_response"
}

# --- Main ---

if [ $# -lt 1 ]; then
  echo "Usage: paper.sh <tool_name> [json_arguments] [--save path]"
  echo ""
  echo "Tools:"
  echo "  get_basic_info                    — File info, artboards, fonts"
  echo "  get_selection                     — Currently selected nodes"
  echo "  get_node_info '{\"nodeId\":\"X\"}'   — Node details"
  echo "  get_children '{\"nodeId\":\"X\"}'    — Child nodes"
  echo "  get_screenshot '{\"nodeId\":\"X\"}'  — Screenshot (saves to file)"
  echo "  get_tree_summary '{\"nodeId\":\"X\"}' — Hierarchy overview"
  echo "  get_computed_styles '{\"nodeIds\":[\"X\"]}' — CSS styles"
  echo "  get_jsx '{\"nodeId\":\"X\"}'         — JSX code"
  echo "  get_font_family_info '{\"familyNames\":[\"Inter\"]}' — Font info"
  echo "  create_artboard '{\"name\":\"...\",\"styles\":{...}}' — New artboard"
  echo "  write_html '{\"html\":\"...\",\"targetNodeId\":\"X\",\"mode\":\"insert-children\"}'"
  echo "  update_styles '{\"updates\":[{\"nodeIds\":[\"X\"],\"styles\":{...}}]}'"
  echo "  set_text_content '{\"updates\":[{\"nodeId\":\"X\",\"textContent\":\"...\"}]}'"
  echo "  duplicate_nodes '{\"nodes\":[{\"id\":\"X\"}]}'"
  echo "  delete_nodes '{\"nodeIds\":[\"X\"]}'"
  echo "  rename_nodes '{\"updates\":[{\"nodeId\":\"X\",\"name\":\"...\"}]}'"
  echo "  finish_working_on_nodes           — Release working indicators"
  echo ""
  echo "Options:"
  echo "  --save <path>    Save screenshot to specific path"
  echo "  --raw            Output raw JSON (no extraction)"
  exit 0
fi

TOOL_NAME="$1"
shift
ARGUMENTS="{}"
SAVE_PATH=""
RAW_OUTPUT=false

# Parse positional + flags
if [ $# -gt 0 ] && [[ "${1:-}" == "{"* ]]; then
  ARGUMENTS="$1"
  shift
fi
while [ $# -gt 0 ]; do
  case "$1" in
    --save) SAVE_PATH="$2"; shift 2 ;;
    --raw) RAW_OUTPUT=true; shift ;;
    *) shift ;;
  esac
done

# Preflight
check_paper

# Make the call
RESPONSE=$(call_tool "$TOOL_NAME" "$ARGUMENTS")

if [ -z "$RESPONSE" ] || [ "$RESPONSE" = "null" ]; then
  die "Empty response from Paper. The tool call may have failed."
fi

# Handle output based on tool type
if $RAW_OUTPUT; then
  echo "$RESPONSE"
elif [ "$TOOL_NAME" = "get_screenshot" ]; then
  handle_screenshot "$RESPONSE" "$SAVE_PATH"
else
  extract_text "$RESPONSE"
fi
