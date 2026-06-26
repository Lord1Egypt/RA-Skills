#!/usr/bin/env bash
# correlate-recent-deploys.sh
# Check recent CI/CD runs for a repo during Step 3 (Correlate).
# Usage: ./scripts/correlate-recent-deploys.sh <owner/repo> [hours-back]
set -euo pipefail

REPO="${1:?Usage: $0 <owner/repo> [hours-back]}"
HOURS="${2:-2}"

# Use Z-suffix format on both GNU (Linux) and BSD (macOS) so jq string
# comparison against GitHub's createdAt (which uses Z, not +00:00) works correctly.
SINCE=$(date -u -d "${HOURS} hours ago" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null \
  || date -u -v-${HOURS}H +%Y-%m-%dT%H:%M:%SZ)

echo "==> Recent CI runs for $REPO (last ${HOURS}h, since $SINCE)"
gh run list --repo "$REPO" --limit 20 \
  --json conclusion,createdAt,name,headBranch,event,url \
  --jq --arg since "$SINCE" \
  '.[] | select(.createdAt > $since) | "\(.createdAt) [\(.conclusion // "in_progress")] \(.name) (\(.headBranch)) \(.url)"'
