#!/bin/bash
set -euo pipefail

# PixelDojo job status helper
# Usage: status.sh <job_id>

API_BASE="${PIXELDOJO_API_BASE:-https://pixeldojo.ai/api/v1}"
API_KEY="${PIXELDOJO_API_KEY:-}"

if [[ -z "$API_KEY" ]]; then
    echo "Error: PIXELDOJO_API_KEY is not set"
    exit 1
fi

JOB_ID="${1:-}"

if [[ -z "$JOB_ID" ]]; then
    echo "Usage: status.sh <job_id>"
    exit 1
fi

curl -sS "${API_BASE}/jobs/${JOB_ID}" \
    -H "Authorization: Bearer ${API_KEY}" | jq .
