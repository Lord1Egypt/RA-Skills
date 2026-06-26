#!/usr/bin/env bash
set -euo pipefail

MAX_SESSIONS="${MAX_SESSIONS:-5}"
SESSION_TTL="${SESSION_TTL:-30m}"
MAX_AGENTS="${MAX_AGENTS:-3}"
MAX_BROWSERS="${MAX_BROWSERS:-1}"

cat <<EOF
{
  "runtime": {
    "maxSessions": ${MAX_SESSIONS},
    "sessionTTL": "${SESSION_TTL}",
    "maxAgents": ${MAX_AGENTS},
    "maxBrowsers": ${MAX_BROWSERS}
  }
}
EOF
