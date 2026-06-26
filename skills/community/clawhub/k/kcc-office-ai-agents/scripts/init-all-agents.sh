#!/bin/bash
# KCC Office v2 - Initialize All Agent Roles
# Sets up workspaces for all office agents: Komi, CEO, CFO, CTO, COO, EDN

set -euo pipefail

echo "🏢 Initializing all KCC Office v2 AI Agent roles"
echo ""

AGENTS=("komi" "ceo" "cfo" "cto" "coo" "edn")

for AGENT in "${AGENTS[@]}"; do
  echo "📋 Processing agent: ${AGENT}"
  
  # Run onboarding script for each agent
  ./scripts/onboard-agent.sh "${AGENT}"
  
  echo "✅ Completed onboarding for ${AGENT}"
  echo ""
done

echo "🎉 All agent roles have been initialized!"
echo ""
echo "📝 Next steps:"
echo "   1. Each agent should complete their ONBOARDING.md file"
echo "   2. Run ./scripts/setup-agent.sh for each agent to begin autonomous operation"
echo "   3. Set up inter-agent communication and shared resources"
echo ""
echo "💡 Tip: You can check status with ./scripts/status-agent.sh <role>"