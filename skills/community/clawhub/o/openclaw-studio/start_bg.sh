#!/bin/zsh
set -euo pipefail
cd "$(dirname "$0")"

PORT="${MONITOR_PORT:-18991}"
HOST="${MONITOR_HOST:-127.0.0.1}"

if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  PID=$(lsof -nP -iTCP:"$PORT" -sTCP:LISTEN -t | head -n1)
  echo "$PID" > monitor.pid
  echo "Monitor already running on $HOST:$PORT (PID $PID)"
  exit 0
fi

MONITOR_HOST="$HOST" MONITOR_PORT="$PORT" /usr/bin/nohup /usr/bin/python3 -u server.py </dev/null >monitor.log 2>&1 &
PID=""
for _ in {1..10}; do
  sleep 1
  PID=$(lsof -nP -iTCP:"$PORT" -sTCP:LISTEN -t | head -n1 || true)
  if [[ -n "$PID" ]]; then
    break
  fi
done

if [[ -z "$PID" ]]; then
  echo "Monitor log:"
  tail -n 40 monitor.log || true
  echo "Failed to start monitor"
  exit 1
fi

echo "$PID" > monitor.pid
echo "Monitor started on $HOST:$PORT (PID $PID)"
