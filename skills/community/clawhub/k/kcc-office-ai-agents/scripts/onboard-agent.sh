#!/bin/bash
# KCC Office v2 AI Agent Onboarding Script
# Initializes agent workspace and defines responsibilities

set -euo pipefail

# Get the agent role from the first argument or directory name
AGENT_ROLE="${1:-unknown}"
AGENT_DIR="./agents/${AGENT_ROLE}"

echo "🤖 Initializing KCC Office v2 AI Agent: ${AGENT_ROLE}"

# Create agent workspace if it doesn't exist
mkdir -p "${AGENT_DIR}"

# Copy base files to agent workspace
cp -r ../{SKILL.md,SESSION-STATE.md,HEARTBEAT.md} "${AGENT_DIR}/" 2>/dev/null || true

# Copy role-specific files if they exist
if [ -d "../${AGENT_ROLE}" ]; then
  cp -r "../${AGENT_ROLE}/"* "${AGENT_DIR}/" 2>/dev/null || true
fi

# Initialize memory directory
mkdir -p "${AGENT_DIR}/memory"

echo "📋 Agent workspace initialized at: ${AGENT_DIR}"
echo "📝 Edit ${AGENT_DIR}/SOUL.md to define your role identity"
echo "👤 Edit ${AGENT_DIR}/USER.md to define your human context"
echo "⚙️ Edit ${AGENT_DIR}/AGENTS.md to define your workflows"
echo "💾 The agent will use ${AGENT_DIR}/memory/ for daily logs"
echo "🎯 Ready to receive tasks and begin autonomous operation"