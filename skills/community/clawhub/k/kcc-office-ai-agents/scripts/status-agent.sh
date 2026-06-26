#!/bin/bash
# KCC Office v2 AI Agent Status Script
# Reports current state of an agent

set -euo pipefail

AGENT_ROLE="${1:-unknown}"
AGENT_DIR="./agents/${AGENT_ROLE}"

echo "📊 Status check for KCC Office v2 AI Agent: ${AGENT_ROLE}"

# Check if agent workspace exists
if [ ! -d "${AGENT_DIR}" ]; then
  echo "❌ Agent workspace not found"
  exit 1
fi

# Check onboarding status
if [ -f "${AGENT_DIR}/ONBOARDING.md" ]; then
  echo "📝 Status: ONBOARDING - Awaiting configuration"
  echo "📋 Please edit SOUL.md, USER.md, and AGENTS.md to complete setup"
elif [ -f "${AGENT_DIR}/SHUTDOWN.md" ]; then
  echo "🛑 Status: SHUTDOWN_INITIATED - Graceful termination in progress"
else
  echo "✅ Status: ACTIVE - Autonomous operation"
fi

# Report key files and their status
echo ""
echo "📁 Agent Workspace: ${AGENT_DIR}"
echo ""

# Count memory files
MEMORY_COUNT=$(find "${AGENT_DIR}/memory" -name "*.md" 2>/dev/null | wc -l)
echo "📓 Daily Memory Files: ${MEMORY_COUNT}"

# Check key files exist
for file in SOUL.md USER.md AGENTS.md MEMORY.md SESSION-STATE.md HEARTBEAT.md; do
  if [ -f "${AGENT_DIR}/${file}" ]; then
    echo "📄 ${file}: PRESENT"
  else
    echo "📄 ${file}: MISSING"
  fi
done

# Show brief status from key files if they exist
if [ -f "${AGENT_DIR}/SOUL.md" ]; then
  echo ""
  echo "👤 SOUL.md Preview:"
  head -5 "${AGENT_DIR}/SOUL.md"
fi

if [ -f "${AGENT_DIR}/USER.md" ]; then
  echo ""
  echo "👥 USER.md Preview:"
  head -5 "${AGENT_DIR}/USER.md"
fi

if [ -f "${AGENT_DIR}/AGENTS.md" ]; then
  echo ""
  echo "⚙️ AGENTS.md Preview:"
  head -5 "${AGENT_DIR}/AGENTS.md"
fi

if [ -f "${AGENT_DIR}/MEMORY.md" ]; then
  echo ""
  echo "🧠 MEMORY.md Preview:"
  head -5 "${AGENT_DIR}/MEMORY.md"
fi