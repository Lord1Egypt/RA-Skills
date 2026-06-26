#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "usage: $0 <AppName>" >&2
  exit 2
fi

APP_NAME="$1"

peekaboo app switch --to "$APP_NAME"
sleep 1
peekaboo see --app "$APP_NAME" --json
