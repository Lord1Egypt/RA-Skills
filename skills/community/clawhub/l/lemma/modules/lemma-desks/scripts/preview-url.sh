#!/bin/bash

set -euo pipefail

PORT="${LEMMA_DESK_DEV_PORT:-5173}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Agent local preview:"
echo "http://127.0.0.1:$PORT/"

if [ -n "${LEMMA_WORKSPACE_URL:-}" ] && [[ "${LEMMA_WORKSPACE_URL}" == https://* ]]; then
  echo ""
  echo "User-facing public preview:"
  echo "https://port-$PORT-${LEMMA_WORKSPACE_URL#https://}"
fi

echo ""
echo "Optional manual browser auth helper:"
echo "bash $SCRIPT_DIR/print-browser-auth-setup.sh"
