#!/usr/bin/env bash
# ────────────────────────────────────────────────────────
# Kannaka Eye — Glyph Viewer CLI wrapper
# ────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
SERVER="$PROJECT_ROOT/server.js"

PORT="${EYE_PORT:-3333}"

usage() {
  cat <<EOF
Usage: eye.sh <command> [options]

Commands:
  start [--port N]   Start the glyph viewer server
  stop               Stop the server
  restart            Restart the server
  status             Check if server is running

Options:
  --port N           HTTP port (default: $PORT, env: EYE_PORT)

Examples:
  eye.sh start
  eye.sh start --port 4444
  eye.sh status
  eye.sh stop
EOF
}

find_pid() {
  # Find node process running server.js on the configured port
  if command -v lsof &>/dev/null; then
    lsof -ti "tcp:$PORT" 2>/dev/null || true
  elif command -v netstat &>/dev/null; then
    netstat -tlnp 2>/dev/null | grep ":$PORT " | awk '{print $NF}' | cut -d/ -f1 || true
  else
    ps aux 2>/dev/null | grep "node.*server.js" | grep -v grep | awk '{print $2}' || true
  fi
}

cmd_start() {
  # Parse args
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --port) PORT="$2"; shift 2 ;;
      *) shift ;;
    esac
  done

  PID=$(find_pid)
  if [[ -n "$PID" ]]; then
    echo "[eye] Already running on port $PORT (pid $PID)"
    return 0
  fi

  echo "[eye] Starting glyph viewer on port $PORT..."
  node "$SERVER" --port "$PORT" &
  disown
  sleep 1

  PID=$(find_pid)
  if [[ -n "$PID" ]]; then
    echo "[eye] Running at http://localhost:$PORT (pid $PID)"
  else
    echo "[eye] Started — open http://localhost:$PORT"
  fi
}

cmd_stop() {
  PID=$(find_pid)
  if [[ -z "$PID" ]]; then
    echo "[eye] Not running on port $PORT"
    return 0
  fi
  echo "[eye] Stopping (pid $PID)..."
  kill "$PID" 2>/dev/null || true
  echo "[eye] Stopped"
}

cmd_restart() {
  cmd_stop
  sleep 1
  cmd_start "$@"
}

cmd_status() {
  PID=$(find_pid)
  if [[ -n "$PID" ]]; then
    echo "[eye] Running on port $PORT (pid $PID)"
    echo "      http://localhost:$PORT"
  else
    echo "[eye] Not running"
  fi
}

# ── Main ───────────────────────────────────────────────
CMD="${1:-}"
shift || true

case "$CMD" in
  start)   cmd_start "$@" ;;
  stop)    cmd_stop ;;
  restart) cmd_restart "$@" ;;
  status)  cmd_status ;;
  -h|--help|help|"") usage ;;
  *) echo "[eye] Unknown command: $CMD"; usage; exit 1 ;;
esac
