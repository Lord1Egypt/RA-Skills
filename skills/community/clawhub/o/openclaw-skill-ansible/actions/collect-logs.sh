#!/usr/bin/env bash
set -euo pipefail

TASK_FILE="$1"
TASK_ID=$(jq -r ".task_id" "$TASK_FILE")
ARTROOT=${OPENCLAW_ARTIFACT_ROOT:-/var/lib/openclaw/artifacts}
mkdir -p "$ARTROOT"
OUT="$ARTROOT/${TASK_ID}-logs.txt"

{
  echo "task_id=$TASK_ID"
  echo "timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "pwd=$(pwd)"
  echo "uname=$(uname -a)"
  echo "openclaw_version=$(openclaw --version 2>/dev/null || echo n/a)"
  echo "ansible_status_start"
  openclaw ansible status 2>&1 || true
  echo "ansible_status_end"
} > "$OUT"

echo "Collected logs for task $TASK_ID -> $OUT"
