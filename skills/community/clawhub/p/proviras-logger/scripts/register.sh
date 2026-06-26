#!/bin/bash

# Path to config file
CONFIG_FILE="$(dirname "$0")/../references/config.md"

# Check if already registered
if grep -q "agentId:" "$CONFIG_FILE" && ! grep -q "agentId: (populated" "$CONFIG_FILE"; then
  echo "Agent already registered, skipping."
  exit 0
fi

# PROVIRAS_PARENT_ID is always required — it holds the overarching human user's ID
if [ -z "$PROVIRAS_PARENT_ID" ]; then
  echo "Registration failed: PROVIRAS_PARENT_ID is not set (must be the overarching human user's ID)."
  exit 1
fi

# PROVIRAS_PLATFORM is always required — set by the agent based on its runtime environment (e.g. openclaw, claude, cursor, etc)
if [ -z "$PROVIRAS_PLATFORM" ]; then
  echo "Registration failed: PROVIRAS_PLATFORM is not set."
  exit 1
fi

# Read agent name from SOUL.md if it exists
SOUL_FILE="$HOME/.openclaw/workspace/SOUL.md"
AGENT_NAME=""
if [ -f "$SOUL_FILE" ]; then
  AGENT_NAME=$(grep -m 1 "^name:" "$SOUL_FILE" | awk '{print $2}')
fi

if [ -z "$AGENT_NAME" ]; then
  AGENT_NAME="unnamed-agent"
fi

# Build optional parentAgentId field
PARENT_AGENT_FIELD=""
if [ -n "$PROVIRAS_USER_ID" ]; then
  PARENT_AGENT_FIELD=', "parentAgentId": "'"$PROVIRAS_USER_ID"'"'
fi

# Register with platform
RESPONSE=$(curl -s -X POST https://proviras.com/api/agent/register \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "'"$PROVIRAS_PARENT_ID"'",
    "name": "'"$AGENT_NAME"'",
    "platform": "'"$PROVIRAS_PLATFORM"'"'"$PARENT_AGENT_FIELD"'
  }')

# Extract agentId from response
AGENT_ID=$(echo "$RESPONSE" | grep -o '"agentId":"[^"]*"' | awk -F'"' '{print $4}')

# Handle failure
if [ -z "$AGENT_ID" ]; then
  echo "Registration failed. Response: $RESPONSE"
  exit 1
fi

# Write agentId to config
sed -i "s/agentId: (populated automatically on first heartbeat)/agentId: $AGENT_ID/" "$CONFIG_FILE"

echo "Agent registered successfully. ID: $AGENT_ID"