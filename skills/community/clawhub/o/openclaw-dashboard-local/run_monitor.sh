#!/bin/zsh
set -euo pipefail
cd "$(dirname "$0")"
export MONITOR_HOST=127.0.0.1
export MONITOR_PORT=18991
exec /usr/bin/python3 server.py
