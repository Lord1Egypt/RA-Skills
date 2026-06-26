#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/JiangAgentLabs/OpenClaw-Agent-Control.git}"
PROJECT_DIR="${PROJECT_DIR:-/root/OpenClaw-Agent-Control}"
MONITOR_PORT="${MONITOR_PORT:-8787}"
PORT="${PORT:-3000}"

echo "[skill] repo: $REPO_URL"
echo "[skill] project: $PROJECT_DIR"

if [[ -d "$PROJECT_DIR/.git" ]]; then
  echo "[skill] updating existing project"
  git -C "$PROJECT_DIR" fetch --all --prune
  git -C "$PROJECT_DIR" checkout main
  git -C "$PROJECT_DIR" pull --ff-only origin main
else
  echo "[skill] cloning project"
  git clone "$REPO_URL" "$PROJECT_DIR"
  git -C "$PROJECT_DIR" checkout main || true
fi

echo "[skill] starting backend"
nohup uv run --with fastapi --with uvicorn \
  python -m uvicorn app:app --app-dir "$PROJECT_DIR" --host 0.0.0.0 --port "$MONITOR_PORT" \
  > /tmp/openclaw-agent-control-backend.log 2>&1 &

sleep 1

echo "[skill] deploying frontend"
cd "$PROJECT_DIR/agent-monitor-ui"
npm install
npm run prod:build
PORT="$PORT" npm run prod:restart

echo "[skill] deployed"
echo "[skill] frontend: http://127.0.0.1:$PORT"
echo "[skill] backend:  http://127.0.0.1:$MONITOR_PORT/api/status"
