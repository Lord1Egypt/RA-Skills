#!/usr/bin/env bash
# a2a-server stop.sh — Stop the A2A inbound task listener
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="${SCRIPT_DIR}/a2a-listener.pid"

if [[ ! -f "$PID_FILE" ]]; then
  echo "⚠ No PID file found — listener may not be running"
  echo "  PID file: ${PID_FILE}"
  exit 0
fi

PID=$(cat "$PID_FILE" 2>/dev/null || true)

if [[ -z "$PID" ]]; then
  echo "⚠ PID file is empty — cleaning up"
  rm -f "$PID_FILE"
  exit 0
fi

if ! kill -0 "$PID" 2>/dev/null; then
  echo "⚠ Process ${PID} is not running — cleaning stale PID file"
  rm -f "$PID_FILE"
  exit 0
fi

echo "Stopping A2A listener (PID: ${PID})..."
kill "$PID" 2>/dev/null || true

# Wait up to 5 seconds for graceful shutdown
for i in $(seq 1 5); do
  if ! kill -0 "$PID" 2>/dev/null; then
    echo "✅ A2A listener stopped"
    rm -f "$PID_FILE"
    exit 0
  fi
  sleep 1
done

# Force kill if still running
if kill -0 "$PID" 2>/dev/null; then
  echo "Force killing listener..."
  kill -9 "$PID" 2>/dev/null || true
  sleep 1
fi

if kill -0 "$PID" 2>/dev/null; then
  echo "Error: Could not stop process ${PID}" >&2
  exit 1
else
  echo "✅ A2A listener stopped (force killed)"
  rm -f "$PID_FILE"
fi
