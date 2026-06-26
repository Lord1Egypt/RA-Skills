#!/usr/bin/env bash
set -euo pipefail

# Helper launcher for Playwright MCP. Override defaults via env vars or CLI flags.
# Env vars:
#   PWMCP_BROWSER   (default: chromium)
#   PWMCP_PORT      (default: 8931)
#   PWMCP_HOST      (default: 127.0.0.1)
#   PWMCP_PROFILE   (default: $HOME/.cache/ms-playwright/mcp-${PWMCP_BROWSER}-profile)
#   PWMCP_EXTRA     (default: empty)

BROWSER=${PWMCP_BROWSER:-chromium}
PORT=${PWMCP_PORT:-8931}
HOST=${PWMCP_HOST:-127.0.0.1}
PROFILE=${PWMCP_PROFILE:-$HOME/.cache/ms-playwright/mcp-${BROWSER}-profile}
EXTRA=${PWMCP_EXTRA:-}

set -x
exec npx @playwright/mcp@latest \
  --browser="${BROWSER}" \
  --host="${HOST}" \
  --port="${PORT}" \
  --user-data-dir="${PROFILE}" \
  --allowed-hosts=* \
  --snapshot-mode=incremental \
  --timeout-action=8000 \
  --timeout-navigation=60000 \
  ${EXTRA} "$@"
