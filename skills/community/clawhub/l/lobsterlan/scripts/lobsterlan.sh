#!/usr/bin/env bash
# lobsterlan.sh — Agent-to-agent communication for OpenClaw on LAN
# Usage:
#   lobsterlan.sh ask <peer> <message>           # Sync ask via chat completions
#   lobsterlan.sh delegate <peer> <message>      # Async task via webhooks
#   lobsterlan.sh status <peer>                  # Check if peer is reachable
#   lobsterlan.sh peers                          # List configured peers

set -euo pipefail

# --- Config ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${LOBSTERLAN_CONFIG:-$SCRIPT_DIR/../config/peers.json}"

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "Error: Config file not found: $CONFIG_FILE" >&2
  echo "Copy peers.example.json to peers.json and configure your peers." >&2
  exit 1
fi

# --- Validation ---
validate_peer_name() {
  local peer="$1"
  if [[ ! "$peer" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    echo "Error: Invalid peer name '$peer' — must match [a-zA-Z0-9_-]+" >&2
    exit 1
  fi
}

validate_host_port() {
  local host="$1" port="$2"
  if [[ ! "$host" =~ ^[a-zA-Z0-9._-]+$ ]]; then
    echo "Error: Invalid host '$host' — must match [a-zA-Z0-9._-]+" >&2
    exit 1
  fi
  if [[ ! "$port" =~ ^[0-9]+$ ]]; then
    echo "Error: Invalid port '$port' — must be numeric" >&2
    exit 1
  fi
}

warn_if_not_localhost() {
  local host="$1"
  if [[ "$host" != "localhost" && "$host" != "127.0.0.1" && "$host" != "::1" ]]; then
    echo "Warning: Connecting to non-localhost address '$host' over plaintext HTTP" >&2
  fi
}

# --- Helpers ---
get_peer_field() {
  local peer="$1" field="$2"
  LOBSTERLAN_CF="$CONFIG_FILE" LOBSTERLAN_PEER="$peer" LOBSTERLAN_FIELD="$field" \
  python3 -c "
import json, sys, os
with open(os.environ['LOBSTERLAN_CF']) as f:
    cfg = json.load(f)
p = cfg.get('peers', {}).get(os.environ['LOBSTERLAN_PEER'])
if not p:
    print('ERROR: Unknown peer: ' + os.environ['LOBSTERLAN_PEER'], file=sys.stderr)
    sys.exit(1)
print(p.get(os.environ['LOBSTERLAN_FIELD'], ''))
"
}

get_self_id() {
  LOBSTERLAN_CF="$CONFIG_FILE" \
  python3 -c "
import json, os
with open(os.environ['LOBSTERLAN_CF']) as f:
    cfg = json.load(f)
print(cfg.get('self', {}).get('id', 'unknown'))
"
}

# --- Commands ---
cmd_ask() {
  local peer="$1"
  shift
  local message="$*"

  validate_peer_name "$peer"

  local host; host=$(get_peer_field "$peer" "host")
  local port; port=$(get_peer_field "$peer" "port")
  local token; token=$(get_peer_field "$peer" "gateway_token")
  local self_id; self_id=$(get_self_id)

  if [[ -z "$host" || -z "$port" || -z "$token" ]]; then
    echo "Error: Incomplete config for peer '$peer'" >&2
    exit 1
  fi

  validate_host_port "$host" "$port"

  local url="http://${host}:${port}/v1/chat/completions"

  warn_if_not_localhost "$host"

  local response
  response=$(curl -sS --max-time 120 "$url" \
    -H "Authorization: Bearer ${token}" \
    -H "Content-Type: application/json" \
    -H "X-LobsterLAN-Agent: ${self_id}" \
    -d "$(LOBSTERLAN_SELF="$self_id" python3 -c "
import json, sys, os
msg = sys.stdin.read()
print(json.dumps({
    'model': 'openclaw:main',
    'user': os.environ['LOBSTERLAN_SELF'],
    'messages': [{'role': 'user', 'content': msg}]
}))
" <<< "$message")" 2>&1)

  local exit_code=$?
  if [[ $exit_code -ne 0 ]]; then
    echo "Error: Failed to reach $peer at $url" >&2
    echo "$response" >&2
    exit 1
  fi

  # Extract the reply text
  echo "$response" | python3 -c "
import json, sys
try:
    data = json.loads(sys.stdin.read())
    choices = data.get('choices', [])
    if choices:
        print(choices[0].get('message', {}).get('content', '(no content)'))
    else:
        print('(no response)')
except Exception as e:
    print(f'Error parsing response: {e}', file=sys.stderr)
    sys.stdin.seek(0)
    print(sys.stdin.read())
"
}

cmd_delegate() {
  local peer="$1"
  shift
  local message="$*"

  validate_peer_name "$peer"

  local host; host=$(get_peer_field "$peer" "host")
  local port; port=$(get_peer_field "$peer" "port")
  local token; token=$(get_peer_field "$peer" "hooks_token")
  local self_id; self_id=$(get_self_id)

  if [[ -z "$host" || -z "$port" || -z "$token" ]]; then
    echo "Error: Incomplete config for peer '$peer'" >&2
    exit 1
  fi

  validate_host_port "$host" "$port"

  local url="http://${host}:${port}/hooks/agent"

  warn_if_not_localhost "$host"

  local response
  response=$(curl -sS --max-time 10 "$url" \
    -H "Authorization: Bearer ${token}" \
    -H "Content-Type: application/json" \
    -H "X-LobsterLAN-Agent: ${self_id}" \
    -d "$(LOBSTERLAN_SELF="$self_id" python3 -c "
import json, sys, os
msg = sys.stdin.read()
print(json.dumps({
    'message': msg,
    'name': os.environ['LOBSTERLAN_SELF'],
    'wakeMode': 'now',
    'deliver': False
}))
" <<< "$message")" 2>&1)

  local exit_code=$?
  if [[ $exit_code -ne 0 ]]; then
    echo "Error: Failed to reach $peer at $url" >&2
    echo "$response" >&2
    exit 1
  fi

  echo "Task delegated to $peer (async)"
  echo "$response"
}

cmd_status() {
  local peer="$1"

  validate_peer_name "$peer"

  local host; host=$(get_peer_field "$peer" "host")
  local port; port=$(get_peer_field "$peer" "port")
  local token; token=$(get_peer_field "$peer" "gateway_token")

  validate_host_port "$host" "$port"

  local url="http://${host}:${port}/health"

  warn_if_not_localhost "$host"

  local http_code
  http_code=$(curl -sS --max-time 5 -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")

  if [[ "$http_code" == "200" ]]; then
    echo "✅ $peer is reachable at ${host}:${port}"
  else
    echo "❌ $peer is unreachable at ${host}:${port} (HTTP $http_code)"
  fi
}

cmd_peers() {
  LOBSTERLAN_CF="$CONFIG_FILE" \
  python3 -c "
import json, os
with open(os.environ['LOBSTERLAN_CF']) as f:
    cfg = json.load(f)
self_info = cfg.get('self', {})
print(f\"Self: {self_info.get('id', '?')} ({self_info.get('name', '?')}) @ {self_info.get('host', '?')}:{self_info.get('port', '?')}\")
print()
for pid, p in cfg.get('peers', {}).items():
    cc = '✅' if p.get('chat_completions') else '❌'
    wh = '✅' if p.get('webhooks') else '❌'
    print(f\"{pid}: {p.get('name', '?')} @ {p.get('host', '?')}:{p.get('port', '?')} [completions:{cc} hooks:{wh}]\")
"
}

# --- Main ---
case "${1:-help}" in
  ask)
    shift
    if [[ $# -lt 2 ]]; then
      echo "Usage: lobsterlan.sh ask <peer> <message>" >&2
      exit 1
    fi
    cmd_ask "$@"
    ;;
  delegate)
    shift
    if [[ $# -lt 2 ]]; then
      echo "Usage: lobsterlan.sh delegate <peer> <message>" >&2
      exit 1
    fi
    cmd_delegate "$@"
    ;;
  status)
    shift
    cmd_status "${1:?Usage: lobsterlan.sh status <peer>}"
    ;;
  peers)
    cmd_peers
    ;;
  help|--help|-h)
    echo "🦞 LobsterLAN — Agent-to-agent communication"
    echo ""
    echo "Commands:"
    echo "  ask <peer> <message>        Synchronous ask (chat completions)"
    echo "  delegate <peer> <message>   Async task delegation (webhooks)"
    echo "  status <peer>               Check peer reachability"
    echo "  peers                       List configured peers"
    echo ""
    echo "Config: \$LOBSTERLAN_CONFIG or ./config/peers.json"
    ;;
  *)
    echo "Unknown command: $1 (try 'help')" >&2
    exit 1
    ;;
esac
