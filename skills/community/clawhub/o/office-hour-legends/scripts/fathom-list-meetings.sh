#!/usr/bin/env bash
# List recent Fathom meetings (title, date, id) as JSON.
# Usage: fathom-list-meetings.sh [limit]
# Requires: FATHOM_API_KEY environment variable

set -euo pipefail

LIMIT="${1:-20}"
API_KEY="${FATHOM_API_KEY:?Missing FATHOM_API_KEY environment variable}"

curl -sS "https://api.fathom.ai/external/v1/meetings?limit=${LIMIT}&include_summary=true&include_transcript=false" \
  -H "X-Api-Key: ${API_KEY}"
