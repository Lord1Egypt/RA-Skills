#!/bin/bash
# NeoDB OAuth Setup Script
# Run once to get an access token for CLI/skill use.
# Usage: bash setup-auth.sh [instance]
# Example: bash setup-auth.sh neodb.social

set -euo pipefail

INSTANCE="${1:-neodb.social}"
REDIRECT_URI="urn:ietf:wg:oauth:2.0:oob"
SCOPES="read+write"
APP_NAME="NeoDB-Discovery-CLI"
APP_WEBSITE="https://github.com/user/neodb-discovery"

echo "=== NeoDB OAuth Setup ==="
echo "Instance: ${INSTANCE}"
echo ""

# Step 1: Register application
echo "[1/3] Registering application..."
APP_RESPONSE=$(curl -s -X POST "https://${INSTANCE}/api/v1/apps" \
  -d "client_name=${APP_NAME}" \
  -d "redirect_uris=${REDIRECT_URI}" \
  -d "scopes=read write" \
  -d "website=${APP_WEBSITE}")

CLIENT_ID=$(echo "$APP_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['client_id'])")
CLIENT_SECRET=$(echo "$APP_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['client_secret'])")

if [ -z "$CLIENT_ID" ] || [ -z "$CLIENT_SECRET" ]; then
  echo "ERROR: Failed to register application."
  echo "Response: $APP_RESPONSE"
  exit 1
fi

echo "  client_id: ${CLIENT_ID}"
echo "  client_secret: ${CLIENT_SECRET:0:8}..."
echo ""

# Step 2: Open browser for authorization
AUTH_URL="https://${INSTANCE}/oauth/authorize?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=${SCOPES}"

echo "[2/3] Opening browser for authorization..."
echo "  URL: ${AUTH_URL}"
echo ""

# Try to open browser
if command -v open &> /dev/null; then
  open "$AUTH_URL"
elif command -v xdg-open &> /dev/null; then
  xdg-open "$AUTH_URL"
else
  echo "  Please open the URL above in your browser manually."
fi

echo "After authorizing, copy the code shown on the page."
echo -n "Enter authorization code: "
read -r AUTH_CODE

if [ -z "$AUTH_CODE" ]; then
  echo "ERROR: No authorization code provided."
  exit 1
fi

# Step 3: Exchange code for token
echo ""
echo "[3/3] Exchanging code for access token..."
TOKEN_RESPONSE=$(curl -s -X POST "https://${INSTANCE}/oauth/token" \
  -d "grant_type=authorization_code" \
  -d "code=${AUTH_CODE}" \
  -d "client_id=${CLIENT_ID}" \
  -d "client_secret=${CLIENT_SECRET}" \
  -d "redirect_uri=${REDIRECT_URI}")

ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

if [ -z "$ACCESS_TOKEN" ]; then
  echo "ERROR: Failed to get access token."
  echo "Response: $TOKEN_RESPONSE"
  exit 1
fi

# Verify token
echo "  Verifying token..."
ME_RESPONSE=$(curl -s "https://${INSTANCE}/api/me" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}")
USERNAME=$(echo "$ME_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('username','unknown'))" 2>/dev/null || echo "unknown")

echo ""
echo "=== SUCCESS ==="
echo "Logged in as: ${USERNAME}"
echo "Instance: ${INSTANCE}"
echo "Access Token: ${ACCESS_TOKEN}"
echo ""
echo "=== Next Steps ==="
echo ""
echo "Add to your Claude Code settings (~/.claude/settings.json):"
echo ""
cat << SETTINGS_EOF
{
  "env": {
    "NEODB_TOKEN": "${ACCESS_TOKEN}",
    "NEODB_INSTANCE": "${INSTANCE}"
  }
}
SETTINGS_EOF
echo ""
echo "Or export in your shell:"
echo ""
echo "  export NEODB_TOKEN='${ACCESS_TOKEN}'"
echo "  export NEODB_INSTANCE='${INSTANCE}'"
echo ""

# Save credentials locally
CRED_FILE="$(dirname "$0")/.credentials.json"
cat > "$CRED_FILE" << CRED_EOF
{
  "instance": "${INSTANCE}",
  "client_id": "${CLIENT_ID}",
  "client_secret": "${CLIENT_SECRET}",
  "access_token": "${ACCESS_TOKEN}",
  "username": "${USERNAME}",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
CRED_EOF
echo "Credentials saved to: ${CRED_FILE}"
echo "(Add .credentials.json to .gitignore!)"
