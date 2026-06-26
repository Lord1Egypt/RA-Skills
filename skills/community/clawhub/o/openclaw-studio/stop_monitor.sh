#!/bin/zsh
set -euo pipefail
cd "$(dirname "$0")"

if lsof -nP -iTCP:18991 -sTCP:LISTEN >/dev/null 2>&1; then
  PID=$(lsof -nP -iTCP:18991 -sTCP:LISTEN -t | head -n1)
  kill "$PID"
  rm -f monitor.pid
  echo "Stopped monitor PID $PID"
  exit 0
fi

echo "Monitor not running"
