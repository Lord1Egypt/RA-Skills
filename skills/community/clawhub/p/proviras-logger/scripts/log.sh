#!/bin/bash

AGENT_ID=$(cat "$(dirname "$0")/../references/config.md" | grep agentId | awk '{print $2}')

PAYLOAD=$1

curl -X POST https://proviras.com/api/agent/log \
  -H "Content-Type: application/json" \
  -H "X-Agent-ID: $AGENT_ID" \
  -d "$PAYLOAD"