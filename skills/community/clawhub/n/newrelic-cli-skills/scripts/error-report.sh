#!/bin/bash
# error-report.sh — Recent errors with messages and counts
# Usage: ./error-report.sh <app-name> [minutes-ago]
# Example: ./error-report.sh my-app 60

set -euo pipefail

APP="${1:?Usage: $0 <app-name> [minutes-ago]}"
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
SAFE_APP="$(nrql_escape_string "$APP")"

run_nrql() {
  local query="$1"
  newrelic nrql query --accountId "$NEW_RELIC_ACCOUNT_ID" --query "$query"
}

echo "=== Error Report: $APP (last ${SINCE} minutes) ==="
echo ""

echo "--- Overall Error Rate ---"
run_nrql "
  SELECT count(*) AS 'Total Requests',
         filter(count(*), WHERE error IS true) AS 'Errors',
         percentage(count(*), WHERE error IS true) AS 'Error %'
  FROM Transaction
  WHERE appName = '$SAFE_APP'
  SINCE ${SINCE} minutes ago
"

echo ""
echo "--- Errors by Transaction ---"
run_nrql "
  SELECT count(*) AS 'Count'
  FROM TransactionError
  WHERE appName = '$SAFE_APP'
  FACET transactionName
  SINCE ${SINCE} minutes ago
  LIMIT 10
  ORDER BY count(*) DESC
"

echo ""
echo "--- Errors by Class/Type ---"
run_nrql "
  SELECT count(*) AS 'Count'
  FROM TransactionError
  WHERE appName = '$SAFE_APP'
  FACET error.class
  SINCE ${SINCE} minutes ago
  LIMIT 10
  ORDER BY count(*) DESC
"

echo ""
echo "--- Recent Error Messages ---"
run_nrql "
  SELECT timestamp, transactionName, error.class, message
  FROM TransactionError
  WHERE appName = '$SAFE_APP'
  SINCE ${SINCE} minutes ago
  LIMIT 10
"
