#!/bin/bash
# KCC Office v2 AI Agent Shutdown Script
# Gracefully stops agent operation

set -euo pipefail

AGENT_ROLE="${1:-unknown}"
AGENT_DIR="./agents/${AGENT_ROLE}"

echo "🛑 Initiating shutdown of KCC Office v2 AI Agent: ${AGENT_ROLE}"

# Check if agent workspace exists
if [ ! -d "${AGENT_DIR}" ]; then
  echo "❌ Agent workspace not found"
  exit 1
fi

# Check if agent is currently onboarded
if [ ! -f "${AGENT_DIR}/ONBOARDING.md" ]; then
  echo "ℹ️ Agent is not currently in onboarding state"
  # Still perform cleanup tasks
fi

# Create SHUTDOWN signal file
touch "${AGENT_DIR}/SHUTDOWN.md"

echo "📝 SHUTDOWN.md signal created at ${AGENT_DIR}/SHUTDOWN.md"
echo "🔄 Agent will check for this signal and begin graceful shutdown"
echo "💾 Current state will be preserved in MEMORY.md and session files"
echo "🧹 Cleanup tasks will be performed before termination"