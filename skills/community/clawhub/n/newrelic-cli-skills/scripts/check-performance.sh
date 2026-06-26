#!/bin/bash
# check-performance.sh — Quick performance health check across all monitored apps
# Usage: ./check-performance.sh [app-name] [minutes-ago]
# Example: ./check-performance.sh my-app 60

set -euo pipefail

APP="${1:-}"
SINCE="${2:-60}"

if [[ -z "${NEW_RELIC_API_KEY:-}" || -z "${NEW_RELIC_ACCOUNT_ID:-}" ]]; then
  echo "ERROR: NEW_RELIC_API_KEY and NEW_RELIC_ACCOUNT_ID must be set"
  exit 1
fi

require_positive_integer() {
  local value="$1"
  local name="$2"

  if [[ ! "$value" =~ ^[1-9][0-9]*$ ]]; then
    echo "ERROR: ${name} must be a positive integer" >&2
    exit 1
  fi
}

nrql_escape_string() {
  local input="$1"
  local output=""
  local char
  local i

  for ((i = 0; i < ${#input}; i++)); do
    char="${input:i:1}"
    case "$char" in
      "\\") output+="\\\\" ;;
      "'") output+="''" ;;
      *) output+="$char" ;;
    esac
  done

  printf '%s' "$output"
}

require_positive_integer "$SINCE" "minutes-ago"

WHERE=""
if [[ -n "$APP" ]]; then
  SAFE_APP="$(nrql_escape_string "$APP")"
  WHERE="WHERE appName = '$SAFE_APP'"
fi

run_nrql() {
  local query="$1"
  newrelic nrql query --accountId "$NEW_RELIC_ACCOUNT_ID" --query "$query"
}

echo "=== Performance Health Check (last ${SINCE} minutes) ==="
echo ""

echo "--- Response Time (avg + P95) ---"
run_nrql "
  SELECT average(duration) AS 'Avg (s)', percentile(duration, 95) AS 'P95 (s)'
  FROM Transaction
  $WHERE
  FACET appName
  SINCE ${SINCE} minutes ago
  LIMIT 20
  ORDER BY average(duration) DESC
"

echo ""
echo "--- Error Rate ---"
run_nrql "
  SELECT percentage(count(*), WHERE error IS true) AS 'Error %', count(*) AS 'Total Requests'
  FROM Transaction
  $WHERE
  FACET appName
  SINCE ${SINCE} minutes ago
  LIMIT 20
"

echo ""
echo "--- Throughput (RPM) ---"
run_nrql "
  SELECT rate(count(*), 1 minute) AS 'RPM'
  FROM Transaction
  $WHERE
  FACET appName
  SINCE ${SINCE} minutes ago
  LIMIT 20
"

echo ""
echo "--- Top 5 Slowest Transactions ---"
run_nrql "
  SELECT average(duration) AS 'Avg (s)', count(*) AS 'Calls'
  FROM Transaction
  $WHERE
  FACET appName, name
  SINCE ${SINCE} minutes ago
  LIMIT 5
  ORDER BY average(duration) DESC
"
