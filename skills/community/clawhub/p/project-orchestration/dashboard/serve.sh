#!/usr/bin/env bash
# serve.sh — Start the Orchestration Dashboard
# Usage: bash dashboard/serve.sh [port]
# Default port: 8766
# Data from: $ORCHESTRATOR_DATA_DIR (default: ../orchestrator-data/ from skill root)
# Open: http://localhost:8766

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${ORCHESTRATOR_DATA_DIR:-$(dirname "$(dirname "$SKILL_DIR")")/orchestrator-data}"
PORT="${1:-8766}"

echo "━━━ Orchestration Dashboard ━━━"
echo "Port: $PORT"
echo "Data: $DATA_DIR"
echo "Open: http://localhost:$PORT"
echo "Set ORCHESTRATOR_DATA_DIR to override data path"
echo ""

cd "$SCRIPT_DIR"
ORCHESTRATOR_DATA_DIR="$DATA_DIR" DASHBOARD_PORT="$PORT" python3 server.py