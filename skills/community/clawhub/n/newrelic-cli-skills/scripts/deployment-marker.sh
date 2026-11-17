#!/bin/bash
# deployment-marker.sh — Record a deployment event in New Relic
# Usage: ./deployment-marker.sh <app_id> <revision> [description] [user]
# Example: ./deployment-marker.sh 12345678 "v2.1.0" "MR !193: Svelte 5 migration" "steven-openclaw"

set -euo pipefail

APP_ID="${1:?Usage: $0 <app_id> <revision> [description] [user]}"
REVISION="${2:?revision required (e.g. git SHA, semver, MR number)}"
DESCRIPTION="${3:-Automated deployment}"
USER="${4:-deploy-bot}"

if [[ ! "$APP_ID" =~ ^[0-9]+$ ]]; then
  echo "ERROR: app_id must contain decimal digits only" >&2
  exit 2
fi

normalize_common_whitespace() {
  local value=$1

  value=${value//$'\r'/ }
  value=${value//$'\n'/ }
  value=${value//$'\t'/ }
  printf '%s' "$value"
}

reject_unsafe_control_characters() {
  local label=$1
  local value=$2

  if [[ "$value" =~ [[:cntrl:]] ]]; then
    echo "ERROR: $label must not contain non-whitespace control characters" >&2
    exit 2
  fi
}

REVISION=$(normalize_common_whitespace "$REVISION")
DESCRIPTION=$(normalize_common_whitespace "$DESCRIPTION")
USER=$(normalize_common_whitespace "$USER")

reject_unsafe_control_characters "revision" "$REVISION"
reject_unsafe_control_characters "description" "$DESCRIPTION"
reject_unsafe_control_characters "user" "$USER"

if [[ -z "${NEW_RELIC_API_KEY:-}" ]]; then
  echo "ERROR: NEW_RELIC_API_KEY must be set"
  exit 1
fi

echo "Recording deployment marker..."
echo "  App ID:      $APP_ID"
echo "  Revision:    $REVISION"
echo "  Description: $DESCRIPTION"
echo "  User:        $USER"

newrelic apm deployment create \
  --applicationId "$APP_ID" \
  --revision "$REVISION" \
  --description "$DESCRIPTION" \
  --user "$USER"

echo "Done. Deployment marker recorded in New Relic."
