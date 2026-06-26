#!/usr/bin/env bash
# pctx-skill.sh — OpenClaw skill wrapper for pctx MCP aggregation layer
# Usage: pctx-skill.sh <command> [args]
set -euo pipefail

PCTX_CONFIG="${PCTX_CONFIG:-$HOME/.config/pctx/pctx.json}"
PCTX_PLIST="$HOME/Library/LaunchAgents/ai.openclaw.pctx.plist"
PCTX_PORT="${PCTX_PORT:-8080}"
PCTX_HOST="${PCTX_HOST:-127.0.0.1}"
PCTX_BIN="${PCTX_BIN:-$(which pctx 2>/dev/null || echo '')}"

# ─── Helpers ──────────────────────────────────────────────────────────────────

die() { echo "❌ $*" >&2; exit 1; }
ok()  { echo "✅ $*"; }
info(){ echo "ℹ️  $*"; }

require_pctx() {
  [[ -n "$PCTX_BIN" ]] || die "pctx not found. Install with: brew install portofcontext/tap/pctx"
  [[ -f "$PCTX_CONFIG" ]] || die "pctx config not found at $PCTX_CONFIG. Run: pctx mcp init -c $PCTX_CONFIG"
}

mask_token() {
  local tok="$1"
  if [[ ${#tok} -gt 20 ]]; then
    echo "${tok:0:10}***${tok: -6}"
  else
    echo "***"
  fi
}

daemon_running() {
  # Check launchd has a running PID (not just loaded)
  local pid
  pid=$(launchctl list 2>/dev/null | grep ai.openclaw.pctx | awk '{print $1}')
  [[ -z "$pid" || "$pid" == "-" ]] && return 1
  # Verify /mcp endpoint is responding (requires both Accept types)
  curl -sf --max-time 3 \
    -X POST "http://${PCTX_HOST}:${PCTX_PORT}/mcp" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d '{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"healthcheck","version":"1"}}}' \
    -o /dev/null 2>/dev/null
}

wait_for_mcp() {
  local max=20 i=0
  while ! curl -sf --max-time 3 \
    -X POST "http://${PCTX_HOST}:${PCTX_PORT}/mcp" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d '{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"healthcheck","version":"1"}}}' \
    -o /dev/null 2>/dev/null; do
    ((i++))
    [[ $i -ge $max ]] && die "pctx didn't respond after ${max}s. Check /tmp/pctx.err"
    sleep 1
    echo -n "."
  done
  echo ""
}

# ─── Commands ─────────────────────────────────────────────────────────────────

cmd_status() {
  if daemon_running; then
    local pid
    pid=$(launchctl list 2>/dev/null | grep ai.openclaw.pctx | awk '{print $1}')
    local start_time=""
    if [[ -n "$pid" && "$pid" != "-" ]]; then
      start_time=$(ps -p "$pid" -o lstart= 2>/dev/null | xargs || echo "")
    fi
    echo "🟢 RUNNING — http://${PCTX_HOST}:${PCTX_PORT}/mcp"
    [[ -n "$start_time" ]] && echo "   Started: $start_time"
    echo "   Config:  $PCTX_CONFIG"
    echo "   Logs:    /tmp/pctx.log | /tmp/pctx.err"
  else
    echo "🔴 STOPPED"
    echo "   Run: pctx-skill start"
  fi
}

cmd_start() {
  require_pctx
  if daemon_running; then
    ok "pctx already running on http://${PCTX_HOST}:${PCTX_PORT}/mcp"
    return 0
  fi
  [[ ! -f "$PCTX_PLIST" ]] && die "launchd plist not found at $PCTX_PLIST. Was MJM-210 setup completed?"
  info "Starting pctx daemon..."
  launchctl load "$PCTX_PLIST" 2>&1 || true
  sleep 2
  echo -n "Waiting for /mcp endpoint"
  wait_for_mcp
  ok "pctx running on http://${PCTX_HOST}:${PCTX_PORT}/mcp"
  return 0
}

cmd_stop() {
  if ! launchctl list 2>/dev/null | grep -q "ai.openclaw.pctx"; then
    info "pctx daemon not loaded"
    return 0
  fi
  info "Stopping pctx daemon..."
  launchctl unload "$PCTX_PLIST" 2>/dev/null || true
  pkill -f "pctx mcp start" 2>/dev/null || true
  sleep 1
  ok "pctx stopped"
  return 0
}

cmd_restart() {
  # Full stop: unload launchd + kill any orphan processes
  launchctl unload "$PCTX_PLIST" 2>/dev/null || true
  pkill -f "pctx mcp start" 2>/dev/null || true
  sleep 2
  ok "pctx stopped"
  cmd_start
}

cmd_mcp_list() {
  require_pctx
  "$PCTX_BIN" mcp list -c "$PCTX_CONFIG" 2>&1
}

cmd_mcp_add() {
  require_pctx
  local name="${1:-}"
  [[ -n "$name" ]] || die "Usage: pctx-skill mcp-add <name> [--url <url> | --command <cmd>] [--arg arg ...] [--env KEY=VAL ...]"
  shift

  # Build pctx mcp add args, pass through remaining flags
  cmd_config_backup
  "$PCTX_BIN" mcp add "$name" -c "$PCTX_CONFIG" "$@" && ok "MCP '$name' added" || die "Failed to add MCP '$name'"

  if daemon_running; then
    info "Restarting daemon to pick up new MCP..."
    cmd_restart
  fi
}

cmd_mcp_remove() {
  require_pctx
  local name="${1:-}"
  [[ -n "$name" ]] || die "Usage: pctx-skill mcp-remove <name>"
  cmd_config_backup
  "$PCTX_BIN" mcp remove "$name" -c "$PCTX_CONFIG" 2>&1 && ok "MCP '$name' removed"
  if daemon_running; then
    info "Restarting daemon..."
    cmd_restart
  fi
}

cmd_config_backup() {
  local ts
  ts=$(date +%Y%m%d-%H%M%S)
  local dest="${PCTX_CONFIG}.backup.${ts}"
  cp "$PCTX_CONFIG" "$dest"
  chmod 600 "$dest"
  ok "Backup: $dest"
}

cmd_config_restore() {
  local ts="${1:-}"
  local backups=()
  while IFS= read -r f; do backups+=("$f"); done < <(ls "${PCTX_CONFIG}.backup."* 2>/dev/null | sort -r)

  [[ ${#backups[@]} -gt 0 ]] || die "No backups found at ${PCTX_CONFIG}.backup.*"

  local chosen=""
  if [[ -n "$ts" ]]; then
    chosen="${PCTX_CONFIG}.backup.${ts}"
    [[ ! -f "$chosen" ]] && die "Backup not found: $chosen"
  else
    echo "Available backups:"
    for i in "${!backups[@]}"; do
      echo "  [$i] ${backups[$i]}"
    done
    echo -n "Enter number to restore: "
    read -r idx
    chosen="${backups[$idx]}"
  fi

  info "Restoring from: $chosen"
  cp "$chosen" "$PCTX_CONFIG"
  chmod 600 "$PCTX_CONFIG"
  ok "Config restored from $chosen"

  if daemon_running; then
    info "Restarting daemon..."
    cmd_restart
  fi
}

cmd_test() {
  local server="${1:-}"
  local fn="${2:-}"
  [[ -n "$server" ]] || die "Usage: pctx-skill test <linear|github> [function-name]"

  daemon_running || die "pctx daemon not running. Run: pctx-skill start"

  # Resolve namespace capitalisation
  local ns
  case "$server" in
    linear) ns="Linear" ;;
    github) ns="Github" ;;
    *) ns="$server" ;;
  esac

  info "Testing pctx Code Mode for '$ns'..."

  if [[ -z "$fn" ]]; then
    # No function specified — list available functions for this namespace
    # Use a broad query and filter by namespace in post-processing
    local list_resp
    list_resp=$(curl -sf --max-time 15 -X POST "http://${PCTX_HOST}:${PCTX_PORT}/mcp" \
      -H "Content-Type: application/json" \
      -H "Accept: application/json, text/event-stream" \
      -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"list_functions","arguments":{"query":"*","limit":100}}}' \
      2>/dev/null | grep "^data:" | head -1 | sed 's/^data: //')
    echo "📚 Available functions in $ns:"
    echo "$list_resp" | python3 -c "
import sys, json, re
ns = '$ns'
d = json.load(sys.stdin)
text = d.get('result',{}).get('content',[{}])[0].get('text','')
# Find the specific namespace block
pattern = f'namespace {ns}'
idx = text.find(pattern)
if idx >= 0:
    block = text[idx:idx+5000]
    # Extract until next namespace or end
    next_ns = re.search(r'namespace \w+', block[len(pattern):])
    if next_ns:
        block = block[:len(pattern) + next_ns.start()]
    fns = re.findall(r'export async function (\w+)', block)
    for f in fns[:30]: print('  -', f)
else:
    print(f'  Namespace {ns} not found in pctx catalog')
" 2>/dev/null
    return
  fi

  # Function specified — call it via execute_typescript
  # pctx requires: field="code", wrapped in "async function run() { ... }"
  info "Calling ${ns}.${fn}({}) via execute_typescript..."
  local code="async function run() { const result = await ${ns}.${fn}({}); return JSON.stringify(result, null, 2); }"
  local call_payload
  call_payload=$(python3 -c "
import json
print(json.dumps({'jsonrpc':'2.0','id':2,'method':'tools/call','params':{
  'name':'execute_typescript',
  'arguments':{'code':'$code'}
}}))
" 2>/dev/null)

  local call_resp
  call_resp=$(curl -sf --max-time 30 -X POST "http://${PCTX_HOST}:${PCTX_PORT}/mcp" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d "$call_payload" \
    2>/dev/null | grep "^data:" | tail -1 | sed 's/^data: //')

  if [[ -z "$call_resp" ]]; then
    die "No response from pctx. Check /tmp/pctx.log"
  fi

  echo "📦 Result:"
  echo "$call_resp" | python3 -c "
import sys, json
d = json.load(sys.stdin)
if 'result' in d:
    content = d.get('result',{}).get('content',[])
    for c in content:
        txt = c.get('text','')
        print(txt[:800] + ('...' if len(txt) > 800 else ''))
elif 'error' in d:
    print('❌ Error:', json.dumps(d['error'], indent=2))
else:
    print(json.dumps(d, indent=2)[:800])
" 2>/dev/null || echo "$call_resp" | head -c 800
}

cmd_install() {
  info "Checking pctx installation..."

  # pctx
  if ! command -v pctx &>/dev/null; then
    info "Installing pctx..."
    brew install portofcontext/tap/pctx
  else
    ok "pctx $(pctx --version 2>/dev/null)"
  fi

  # Deno
  if ! command -v deno &>/dev/null; then
    info "Installing deno..."
    brew install deno
  else
    ok "deno $(deno --version 2>/dev/null | head -1)"
  fi

  # github-mcp-server
  if ! command -v github-mcp-server &>/dev/null; then
    info "Installing github-mcp-server..."
    brew install github-mcp-server
  else
    ok "github-mcp-server $(github-mcp-server --version 2>&1 | head -1)"
  fi

  # @tacticlaunch/mcp-linear
  if ! command -v mcp-linear &>/dev/null; then
    info "Installing @tacticlaunch/mcp-linear..."
    npm install -g @tacticlaunch/mcp-linear
  else
    ok "mcp-linear installed"
  fi

  ok "All dependencies installed"
}

# ─── Dispatch ─────────────────────────────────────────────────────────────────

CMD="${1:-help}"
shift 2>/dev/null || true

case "$CMD" in
  status)          cmd_status ;;
  start)           cmd_start "$@" ;;
  stop)            cmd_stop ;;
  restart)         cmd_restart ;;
  mcp-list)        cmd_mcp_list ;;
  mcp-add)         cmd_mcp_add "$@" ;;
  mcp-remove)      cmd_mcp_remove "$@" ;;
  config-backup)   cmd_config_backup ;;
  config-restore)  cmd_config_restore "$@" ;;
  test)            cmd_test "$@" ;;
  install)         cmd_install ;;
  help|--help|-h)
    cat <<'EOF'
pctx-skill — OpenClaw skill for pctx MCP aggregation

Usage: pctx-skill <command> [args]

Commands:
  status                        Check daemon status + port
  start                         Start pctx daemon (launchd)
  stop                          Stop pctx daemon
  restart                       Restart pctx daemon
  mcp-list                      List connected MCP servers + tool counts
  mcp-add <name> [flags]        Add an upstream MCP server
  mcp-remove <name>             Remove an upstream MCP server
  config-backup                 Backup pctx.json (timestamped)
  config-restore [timestamp]    Restore pctx.json from backup
  test <server> <tool>          Test a tool call through pctx
  install                       Idempotent install of all dependencies

Examples:
  pctx-skill status
  pctx-skill mcp-list
  pctx-skill test linear linear_getOrganization
  pctx-skill test github list_issues
  pctx-skill mcp-add memory --command "npx -y @modelcontextprotocol/server-memory"
  pctx-skill config-backup
  pctx-skill config-restore 20260422-092733

Config: ~/.config/pctx/pctx.json
Logs:   /tmp/pctx.log | /tmp/pctx.err
EOF
    ;;
  *)
    die "Unknown command: $CMD. Run 'pctx-skill help' for usage."
    ;;
esac
