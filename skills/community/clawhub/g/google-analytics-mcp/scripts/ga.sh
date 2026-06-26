#!/usr/bin/env bash
# ga.sh — call Google Analytics MCP tools using per-workspace credentials
# Usage: ga.sh <workspace_dir> <tool> [key=value ...]
# Example: ga.sh ~/.openclaw/workspace-relayter get_account_summaries
# Example: ga.sh ~/.openclaw/workspace-relayter run_report property=properties/123 'dateRanges=[{"startDate":"7daysAgo","endDate":"today"}]' 'metrics=[{"name":"sessions"}]'

set -euo pipefail

WORKSPACE="${1:?Usage: ga.sh <workspace_dir> <tool> [args...]}"
TOOL="${2:?Missing tool name}"
shift 2

CREDS_DIR="$WORKSPACE/credentials"
CREDS_FILE="$CREDS_DIR/ga-service-account.json"
CONFIG_FILE="$CREDS_DIR/ga-config.json"

# --- Validate credentials ---
if [[ ! -f "$CREDS_FILE" ]]; then
  echo "ERROR: Service account credentials not found at: $CREDS_FILE" >&2
  echo "See skill references/setup.md for setup instructions." >&2
  exit 1
fi

# --- Load optional config ---
PROJECT_ID=""
if [[ -f "$CONFIG_FILE" ]]; then
  PROJECT_ID="$(python3 -c "import json,sys; d=json.load(open('$CONFIG_FILE')); print(d.get('projectId',''))" 2>/dev/null || true)"
fi

# --- Build env flags ---
ENV_FLAGS=(--env "GOOGLE_APPLICATION_CREDENTIALS=$CREDS_FILE")
if [[ -n "$PROJECT_ID" ]]; then
  ENV_FLAGS+=(--env "GOOGLE_CLOUD_PROJECT=$PROJECT_ID")
fi

# --- Call via mcporter ---
exec npx --yes mcporter call \
  --stdio uvx \
  --stdio-arg analytics-mcp \
  "${ENV_FLAGS[@]}" \
  "analytics-mcp.$TOOL" \
  "$@"
