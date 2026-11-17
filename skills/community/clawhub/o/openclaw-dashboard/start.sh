#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

NODE_ARGS=()
if [[ -f .env ]]; then
  NODE_ARGS+=(--env-file=.env)
fi

exec node "${NODE_ARGS[@]}" backend/server.js
