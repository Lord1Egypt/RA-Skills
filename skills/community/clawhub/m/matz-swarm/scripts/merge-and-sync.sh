#!/bin/bash
# merge-and-sync.sh - Merge MR/PR and sync local main
# Usage: ./merge-and-sync.sh <project-name> <mr-iid>

set -e
source "$(dirname "$0")/config.sh"

PROJECT="$1"
MR_IID="$2"

if [ -z "$PROJECT" ] || [ -z "$MR_IID" ]; then
  echo "Usage: $0 <project-name> <mr-iid>"
  exit 1
fi

LOCAL_REPO=$(jq -r --arg p "$PROJECT" '.projects[$p].local_repo // empty' "$REGISTRY")
if [ -z "$LOCAL_REPO" ] || [ ! -d "$LOCAL_REPO/.git" ]; then
  echo "❌ local_repo not found for project: $PROJECT"
  exit 1
fi

cd "$LOCAL_REPO"

echo "== merging MR !$MR_IID on $PROJECT =="
swarm_mr_merge "$MR_IID"

echo "== syncing main =="
"${SCRIPTS_DIR}/sync-project-main.sh" "$PROJECT"

echo "✅ merge + sync done"
