#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

if [ -f .env ]; then
  # shellcheck disable=SC1091
  source .env
fi

mkdir -p logs

exec python3 openclaw_autopilot.py --config openclaw_config.json >> logs/runner.stdout.log 2>&1
