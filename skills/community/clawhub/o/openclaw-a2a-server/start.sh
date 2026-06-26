#!/usr/bin/env bash
# a2a-server start.sh — Start the A2A inbound task listener in the background
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="${SCRIPT_DIR}/a2a-listener.pid"
LOG_FILE="${SCRIPT_DIR}/a2a-listener.log"
LISTENER="${SCRIPT_DIR}/a2a-listener.py"
CONF_FILE="${SCRIPT_DIR}/a2a.conf"

# Also check shared config in a2a-client skill directory
CLIENT_CONF="${SCRIPT_DIR}/../a2a-client/a2a.conf"

# --- Source config file if it exists (prefer local, fall back to shared) ---
if [[ -f "$CONF_FILE" ]]; then
  # shellcheck source=a2a.conf
  source "$CONF_FILE"
elif [[ -f "$CLIENT_CONF" ]]; then
  # shellcheck source=a2a.conf
  source "$CLIENT_CONF"
fi

# --- Auto-detect local bind address (this is the agent's own IP, NOT the gateway) ---
_auto_ip() { tailscale ip -4 2>/dev/null || hostname -I | awk '{print $1}'; }
_auto_port="${LISTENER_PORT:-8100}"
_auto_bind="${BIND_ADDR:-$(_auto_ip)}"

# --- Parse args (CLI flags override everything) ---
PORT=""
BIND_ADDR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --port) PORT="$2"; shift 2 ;;
    --bind) BIND_ADDR="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

# Apply priority: CLI > env vars > config > auto-detected
PORT="${PORT:-${LISTENER_PORT:-$_auto_port}}"
BIND_ADDR="${BIND_ADDR:-${BIND_ADDR:-$_auto_bind}}"

# --- Check if already running ---
if [[ -f "$PID_FILE" ]]; then
  OLD_PID=$(cat "$PID_FILE" 2>/dev/null || true)
  if [[ -n "$OLD_PID" ]] && kill -0 "$OLD_PID" 2>/dev/null; then
    echo "⚠ A2A listener already running (PID: ${OLD_PID})"
    echo "  Stop it first: ./stop.sh"
    exit 0
  else
    echo "Cleaning stale PID file..."
    rm -f "$PID_FILE"
  fi
fi

# --- Check that the listener script exists ---
if [[ ! -f "$LISTENER" ]]; then
  echo "Error: Listener script not found at ${LISTENER}" >&2
  exit 1
fi

# --- Start the listener, passing all config via environment ---
echo "Starting A2A listener on ${BIND_ADDR}:${PORT}..."

PORT="$PORT" \
BIND_ADDR="$BIND_ADDR" \
A2A_GATEWAY_API_KEY="${A2A_GATEWAY_API_KEY:-}" \
A2A_OPENCLAW_COMMAND="${A2A_OPENCLAW_COMMAND:-}" \
A2A_OPENCLAW_URL="${A2A_OPENCLAW_URL:-}" \
A2A_OPENCLAW_TIMEOUT="${A2A_OPENCLAW_TIMEOUT:-}" \
A2A_OPENCLAW_URL_API_KEY="${A2A_OPENCLAW_URL_API_KEY:-}" \
AGENT_SLUG="${AGENT_SLUG:-}" \
AGENT_NAME="${AGENT_NAME:-}" \
AGENT_URL="${AGENT_URL:-}" \
AGENT_CAPABILITIES="${AGENT_CAPABILITIES:-}" \
AGENT_AUTH_TYPE="${AGENT_AUTH_TYPE:-}" \
nohup python3 "$LISTENER" >> "$LOG_FILE" 2>&1 &
LISTENER_PID=$!

# Give it a moment to start (or fail fast)
sleep 1

if kill -0 "$LISTENER_PID" 2>/dev/null; then
  echo "$LISTENER_PID" > "$PID_FILE"
  echo "✅ A2A listener started (PID: ${LISTENER_PID})"
  echo "  Port: ${PORT}"
  echo "  Bind: ${BIND_ADDR}"
  echo "  Log:  ${LOG_FILE}"
  echo "  PID:  ${PID_FILE}"
  echo ""
  echo "Verify: curl -s http://${BIND_ADDR}:${PORT}/health"
else
  echo "Error: Listener process exited immediately" >&2
  echo "Check the log: ${LOG_FILE}" >&2
  rm -f "$PID_FILE"
  exit 1
fi
