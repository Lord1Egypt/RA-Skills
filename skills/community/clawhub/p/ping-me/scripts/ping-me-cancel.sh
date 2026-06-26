#!/bin/bash
# Cancel a ping-me reminder by job ID (full or partial).
# All data parsing uses stdin — no inline string embedding.
# Usage: ping-me-cancel.sh <job-id>
set -euo pipefail

JOB_ID="${1:-}"
if [ -z "$JOB_ID" ]; then
  echo "Usage: ping-me-cancel.sh <job-id>"
  echo "Use ping-me-list.sh to find job IDs."
  exit 1
fi

OPENCLAW=$(which openclaw 2>/dev/null || echo "openclaw")

# If partial ID (< 36 chars), try to resolve full ID via stdin parsing
if [ ${#JOB_ID} -lt 36 ]; then
  FULL_ID=$("$OPENCLAW" cron list --json 2>/dev/null | python3 -c '
import json, sys

partial = sys.argv[1]
try:
    data = json.load(sys.stdin)
    jobs = data.get("jobs", data) if isinstance(data, dict) else data
    if isinstance(jobs, list):
        for j in jobs:
            if isinstance(j, dict) and j.get("id", "").startswith(partial):
                print(j["id"])
                sys.exit(0)
except Exception:
    pass
print("")
' "$JOB_ID" 2>/dev/null) || FULL_ID=""

  if [ -n "$FULL_ID" ]; then
    JOB_ID="$FULL_ID"
  fi
fi

RESULT=$("$OPENCLAW" cron rm "$JOB_ID" 2>&1)

if echo "$RESULT" | grep -qi "removed\|deleted\|success"; then
  echo "✅ Reminder cancelled (ID: ${JOB_ID:0:8})"
else
  echo "❌ Failed to cancel reminder"
  echo "$RESULT"
  exit 1
fi
