#!/usr/bin/env bash
set -euo pipefail

JOB='*/30 * * * * openclaw sessions prune >/dev/null 2>&1'

if crontab -l >/tmp/openclaw-current-crontab 2>/dev/null; then
  :
else
  : >/tmp/openclaw-current-crontab
fi

if grep -Fqx "$JOB" /tmp/openclaw-current-crontab; then
  echo "Cron prune job already present."
  exit 0
fi

printf '%s\n' "$JOB" >> /tmp/openclaw-current-crontab
crontab /tmp/openclaw-current-crontab
rm -f /tmp/openclaw-current-crontab

echo "Installed cron prune job:"
echo "$JOB"
