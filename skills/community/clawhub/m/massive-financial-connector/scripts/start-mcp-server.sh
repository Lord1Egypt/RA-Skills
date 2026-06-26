#!/usr/bin/env bash
set -euo pipefail

source "$HOME/.zshrc" >/dev/null 2>&1 || true
KEY="${MASSIVE_API_KEY:-}"
KEY="${KEY#\"}"; KEY="${KEY%\"}"; KEY="${KEY#\'}"; KEY="${KEY%\'}"

if [ -z "$KEY" ]; then
  echo "ERROR: MASSIVE_API_KEY not set" >&2
  exit 1
fi

export MASSIVE_API_KEY="$KEY"
exec "$HOME/.local/bin/uvx" --from git+https://github.com/massive-com/mcp_massive@v0.4.0 mcp_polygon
