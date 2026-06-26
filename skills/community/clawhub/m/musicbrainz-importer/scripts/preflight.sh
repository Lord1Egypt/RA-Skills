#!/usr/bin/env bash
# Preflight credential check for MusicBrainz skill.
# Checks credentials file first, then falls back to env vars.
# Exit 0 = good, exit 1 = missing creds, exit 2 = invalid creds.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CRED_FILE="$SKILL_DIR/.credentials.json"

# Load from credentials file if it exists
if [ -f "$CRED_FILE" ]; then
  FILE_USER=$(jq -r '.username // empty' "$CRED_FILE" 2>/dev/null || true)
  FILE_PASS=$(jq -r '.password // empty' "$CRED_FILE" 2>/dev/null || true)
  if [ -n "$FILE_USER" ] && [ -n "$FILE_PASS" ]; then
    export MB_USERNAME="$FILE_USER"
    export MB_PASSWORD="$FILE_PASS"
  fi
fi

# Check if we have credentials from either source
if [ -z "${MB_USERNAME:-}" ] || [ -z "${MB_PASSWORD:-}" ]; then
  echo "MISSING_CREDENTIALS"
  echo "No MusicBrainz credentials found."
  echo "Checked: $CRED_FILE and MB_USERNAME/MB_PASSWORD env vars."
  exit 1
fi

# Validate credentials by attempting login
echo "Checking MusicBrainz credentials for user: $MB_USERNAME"

COOKIE_JAR=$(mktemp)
trap "rm -f $COOKIE_JAR" EXIT

# Fetch login page to get session cookie
curl -s -c "$COOKIE_JAR" -o /dev/null "https://musicbrainz.org/login"

# Attempt login
RESPONSE=$(curl -s -w "\n%{http_code}" \
  -b "$COOKIE_JAR" -c "$COOKIE_JAR" \
  -X POST "https://musicbrainz.org/login" \
  -d "username=${MB_USERNAME}&password=${MB_PASSWORD}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -L --max-redirs 3)

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if echo "$BODY" | grep -q "Log Out" 2>/dev/null; then
  echo "CREDENTIALS_VALID"
  echo "Authenticated as: $MB_USERNAME"
  exit 0
fi

if echo "$BODY" | grep -qi "Incorrect username or password" 2>/dev/null; then
  echo "INVALID_CREDENTIALS"
  echo "The username/password combination is incorrect."
  exit 2
fi

echo "UNKNOWN_STATUS (HTTP $HTTP_CODE)"
echo "Could not confirm credentials. MusicBrainz may be rate-limiting or unavailable."
echo "Proceeding anyway — login will be attempted in the browser during editing."
exit 0
