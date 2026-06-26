#!/bin/bash
# KCC Office v2 AI Agent Setup Script
# Configures agent for autonomous operation

set -euo pipefail

AGENT_ROLE="${1:-unknown}"
AGENT_DIR="./agents/${AGENT_ROLE}"

echo "🔧 Setting up KCC Office v2 AI Agent: ${AGENT_ROLE}"

# Check if agent workspace exists
if [ ! -d "${AGENT_DIR}" ]; then
  echo "❌ Agent workspace not found. Run onboard-agent.sh first."
  exit 1
fi

# Create ONBOARDING.md to signal the agent to start onboarding
cat > "${AGENT_DIR}/ONBOARDING.md" << 'EOF'
# Agent Onboarding

Welcome to your KCC Office v2 AI Agent role!

Please answer the following questions to configure your workspace:

## Role Identity
- What are your primary responsibilities as the [ROLE]?
- What principles guide your decision-making?
- What boundaries should you not cross?

## Human Context
- Who do you primarily serve or report to?
- What are their goals and expectations?
- How do you prefer to communicate?

## Initial Tasks
- What are your first 3 tasks or objectives?
- What does success look like for each?

## Workflow Preferences
- How do you like to receive tasks?
- What information do you need to act?
- How do you report progress?

Answer in the relevant files:
- SOUL.md: Identity, principles, boundaries
- USER.md: Human context, goals, preferences
- AGENTS.md: Workflows, delegation, reporting

When complete, the ONBOARDING.md file will be removed and you'll begin autonomous operation.
EOF

echo "📝 ONBOARDING.md created at ${AGENT_DIR}/ONBOARDING.md"
echo "✏️ Please edit the files mentioned above to complete your onboarding"
echo "🚀 Once ONBOARDING.md is removed, you'll begin autonomous operation"