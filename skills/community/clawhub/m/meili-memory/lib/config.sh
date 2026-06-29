#!/bin/bash
# Shared MeiliSearch configuration loader
# Source this script in other scripts: source "$(dirname "$0")/../lib/config.sh"
# or: source /root/.openclaw/workspace/skills/lib/config.sh

# Determine workspace root
if [ -z "$WORKSPACE" ]; then
  WORKSPACE="/root/.openclaw/workspace"
fi

# Load .env if it exists
ENV_FILE="${WORKSPACE}/.env"
if [ -f "$ENV_FILE" ]; then
  set -a
  source "$ENV_FILE"
  set +a
fi

# Defaults if not set
MEILI_HOST="${MEILI_HOST:-http://127.0.0.1:7700}"
MEILI_KEY="${MEILI_KEY:-}"

if [ -z "$MEILI_KEY" ]; then
  echo "ERROR: MEILI_KEY not set. Create ${ENV_FILE} with your MeiliSearch master key." >&2
  exit 1
fi

export MEILI_HOST MEILI_KEY
