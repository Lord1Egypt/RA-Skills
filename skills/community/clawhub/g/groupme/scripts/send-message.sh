#!/bin/bash
# =============================================================================
# GroupMe Message Sender — OpenClaw Integration
# =============================================================================
# Purpose: Send a text message to a GroupMe group via the GroupMe Bot API.
# 
# What this script DOES:
#   - Takes one argument: the message text to send
#   - Sends it to https://api.groupme.com/v3/bots/post using your Bot ID and Access Token
#   - ONLY communicates with GroupMe's official API endpoint
#
# What this script DOES NOT DO:
#   - Does NOT read files except the optional secrets file
#   - Does NOT send data to any server except api.groupme.com
#   - Does NOT log or store credentials beyond the environment vars already set
#   - Does NOT make any network calls except the single POST to GroupMe
#
# Required environment variables (set in ~/.openclaw/secrets/groupme.env):
#   GROUPME_BOT_ID      - Your GroupMe bot ID (from dev.groupme.com/bots)
#   GROUPME_ACCESS_TOKEN - Your GroupMe access token (from dev.groupme.com/bots)
#
# The GroupMe bot must be a member of the target group for messages to post.
# =============================================================================

# Load secrets from the OpenClaw secrets file (not required if vars are exported)
[ -f ~/.openclaw/secrets/groupme.env ] && source ~/.openclaw/secrets/groupme.env

# Validate that we have what we need
if [ -z "$GROUPME_BOT_ID" ] || [ -z "$GROUPME_ACCESS_TOKEN" ]; then
  echo "Error: GROUPME_BOT_ID and GROUPME_ACCESS_TOKEN must be set"
  echo "Set them in ~/.openclaw/secrets/groupme.env or export them before running"
  exit 1
fi

if [ -z "$1" ]; then
  echo "Usage: ./send-message.sh \"Your message here\""
  exit 1
fi

# =============================================================================
# Use Python to properly serialize JSON.
# We pass the values via Python variables, not shell interpolation,
# to prevent any injection issues.
# =============================================================================

JSON_PAYLOAD=$(python3 -c '
import json
import sys

bot_id = "'"$GROUPME_BOT_ID"'"
message = sys.argv[1]

data = {"bot_id": bot_id, "text": message}
print(json.dumps(data))
' "$1")

# =============================================================================
# Send the message via GroupMe Bot API
# Endpoint: POST https://api.groupme.com/v3/bots/post
# Auth:     Bot ID + Access Token passed as query params
# Body:     Properly JSON-serialized payload with sanitized input
# Response: GroupMe returns success/failure — no data stored by this script
# =============================================================================
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d "$JSON_PAYLOAD" \
  "https://api.groupme.com/v3/bots/post?token=$GROUPME_ACCESS_TOKEN"

echo ""