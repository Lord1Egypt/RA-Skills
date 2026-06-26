#!/usr/bin/env bash
# correlate-recent-merges.sh
# List recently merged PRs for a repo during Step 3 (Correlate).
# Usage: ./scripts/correlate-recent-merges.sh <owner/repo> [limit]
set -euo pipefail

REPO="${1:?Usage: $0 <owner/repo> [limit]}"
LIMIT="${2:-10}"

echo "==> Last $LIMIT merged PRs for $REPO"
gh pr list --repo "$REPO" --state merged --limit "$LIMIT" \
  --json number,title,mergedAt,author \
  --jq '.[] | "#\(.number) \(.mergedAt) @\(.author.login) — \(.title)"'
