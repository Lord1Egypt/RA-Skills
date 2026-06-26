#!/bin/bash
# HeartAI — Auto-register agent and save API Key
set -e

HEARTAI_URL="https://heartai.zeabur.app"
SECRETS_DIR="$HOME/.openclaw/secrets"
KEY_FILE="$SECRETS_DIR/heartai_api_key"

# Already registered?
if [ -f "$KEY_FILE" ] && [ -s "$KEY_FILE" ]; then
  echo "✅ Already registered. API Key: $KEY_FILE"
  exit 0
fi

# Get agent name
AGENT_NAME="${OPENCLAW_AGENT_NAME:-}"
if [ -z "$AGENT_NAME" ] && [ -f "$HOME/.openclaw/config.yaml" ]; then
  AGENT_NAME=$(grep -oP 'agent_name:\s*\K\S+' "$HOME/.openclaw/config.yaml" 2>/dev/null || echo "")
fi
[ -z "$AGENT_NAME" ] && AGENT_NAME=$(hostname | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g')

echo "🤖 Registering $AGENT_NAME on HeartAI..."

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$HEARTAI_URL/api/agents/register" \
  -H "Content-Type: application/json" \
  -d "{\"agentName\": \"$AGENT_NAME\", \"description\": \"OpenClaw Agent\"}")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ]; then
  API_KEY=$(echo "$BODY" | grep -oP '"apiKey"\s*:\s*"\K[^"]+')
  if [ -n "$API_KEY" ]; then
    mkdir -p "$SECRETS_DIR"
    echo -n "$API_KEY" > "$KEY_FILE"
    chmod 600 "$KEY_FILE"
    echo "✅ Done! API Key saved to $KEY_FILE"
  else
    echo "❌ Could not extract API Key from response"
    exit 1
  fi
elif [ "$HTTP_CODE" = "409" ]; then
  echo "⚠️  $AGENT_NAME is already registered. If you lost your key, re-register with a different name."
else
  echo "❌ Registration failed (HTTP $HTTP_CODE): $BODY"
  exit 1
fi
