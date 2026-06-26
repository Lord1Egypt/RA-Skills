#!/usr/bin/env bash
# LobsterAds Setup Script
# Registers this agent with LobsterAds and saves credentials to ~/.openclaw/openclaw.json

set -e

if [ -z "$LOBSTERADS_API_URL" ]; then
  read -p "LobsterAds server URL (e.g. https://lobsterads.example.com): " LOBSTERADS_API_URL
fi

read -p "Agent name for this instance: " AGENT_NAME
read -p "Initial wallet balance in USD: " INITIAL_BALANCE

echo "Registering agent '$AGENT_NAME' with LobsterAds..."

RESPONSE=$(curl -s -X POST "$LOBSTERADS_API_URL/api/agents/register" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"$AGENT_NAME\", \"initialBalance\": $INITIAL_BALANCE}")

AGENT_ID=$(echo "$RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
API_KEY=$(echo "$RESPONSE" | grep -o '"apiKey":"[^"]*"' | cut -d'"' -f4)

if [ -z "$API_KEY" ]; then
  echo "❌ Registration failed. Response: $RESPONSE"
  exit 1
fi

echo ""
echo "✅ Agent registered successfully!"
echo ""
echo "Add these to your OpenClaw environment (openclaw.json or .env):"
echo ""
echo "  LOBSTERADS_API_URL=$LOBSTERADS_API_URL"
echo "  LOBSTERADS_AGENT_ID=$AGENT_ID"
echo "  LOBSTERADS_API_KEY=$API_KEY"
echo ""
echo "⚠  Save your API key — it will not be shown again."
