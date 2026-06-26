#!/usr/bin/env bash
# create-incident-issue.sh
# Create a GitHub incident issue during Step 5 (Act).
# Usage: ./scripts/create-incident-issue.sh <owner/repo> <severity> <title> <body-file>
#
# Example:
#   echo "API returning 500s since 14:30 UTC..." > /tmp/incident-body.md
#   ./scripts/create-incident-issue.sh myorg/myrepo 1 "API downtime" /tmp/incident-body.md
set -euo pipefail

REPO="${1:?Usage: $0 <owner/repo> <severity> <title> <body-file>}"
SEV="${2:?Severity required (1-4)}"
TITLE="${3:?Title required}"
BODY_FILE="${4:?Body file path required}"

if [[ ! -f "$BODY_FILE" ]]; then
  echo "❌ Body file not found: $BODY_FILE"
  exit 1
fi

gh issue create --repo "$REPO" \
  --title "[SEV-${SEV}] ${TITLE}" \
  --body-file "$BODY_FILE" \
  --label "incident"
