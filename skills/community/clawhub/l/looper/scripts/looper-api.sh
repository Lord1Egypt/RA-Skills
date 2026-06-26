#!/usr/bin/env bash
# Looper API helper script (tenant-scoped operations only)
# Usage: looper-api.sh <command> [args]

set -euo pipefail

API_URL="${LOOPER_API_URL:-https://api.looper.bot}"
KEY="${LOOPER_ADMIN_KEY:-}"

if [ -z "$KEY" ]; then
  echo "Error: LOOPER_ADMIN_KEY not set. Sign up at POST $API_URL/api/signup" >&2
  exit 1
fi

case "${1:-help}" in
  loops)
    curl -s "$API_URL/api/loops" -H "Authorization: Bearer $KEY"
    ;;
  loop)
    # Usage: looper-api.sh loop <id>
    curl -s "$API_URL/api/loops/$2" -H "Authorization: Bearer $KEY"
    ;;
  runs)
    # Usage: looper-api.sh runs <loop-id>
    curl -s "$API_URL/api/loops/$2/runs" -H "Authorization: Bearer $KEY"
    ;;
  trigger)
    # Usage: looper-api.sh trigger <loop-id>
    curl -s -X POST "$API_URL/api/loops/$2/run" -H "Authorization: Bearer $KEY"
    ;;
  toggle)
    # Usage: looper-api.sh toggle <loop-id> true|false
    curl -s -X PATCH "$API_URL/api/loops/$2" \
      -H "Authorization: Bearer $KEY" \
      -H "Content-Type: application/json" \
      -d "{\"enabled\": $3}"
    ;;
  github)
    # Show GitHub connection status
    curl -s "$API_URL/api/github/status" -H "Authorization: Bearer $KEY"
    ;;
  tenant)
    # Show current tenant info
    curl -s "$API_URL/api/tenant" -H "Authorization: Bearer $KEY"
    ;;
  help|*)
    echo "Looper API Helper"
    echo ""
    echo "Commands:"
    echo "  loops                      - List your loops"
    echo "  loop <id>                  - Get loop details"
    echo "  runs <loop-id>             - View run history"
    echo "  trigger <loop-id>          - Run a loop now"
    echo "  toggle <loop-id> true|false - Enable/disable"
    echo "  github                     - GitHub connection status"
    echo "  tenant                     - Your account info"
    echo ""
    echo "Env vars:"
    echo "  LOOPER_ADMIN_KEY  - Your API key (required, starts with lp_)"
    echo "  LOOPER_API_URL    - API base URL (default: https://api.looper.bot)"
    ;;
esac
