#!/usr/bin/env bash
set -euo pipefail

JOB_ID="${1:-}"
if [[ -z "$JOB_ID" ]]; then
  echo "Usage: $0 <job-id>"
  exit 1
fi

openclaw cron run "$JOB_ID"
openclaw cron runs --id "$JOB_ID" --limit 1
