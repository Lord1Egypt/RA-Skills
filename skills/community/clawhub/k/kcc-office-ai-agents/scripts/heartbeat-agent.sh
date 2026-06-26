#!/bin/bash
# KCC Office v2 AI Agent Heartbeat Script
# Performs periodic self-improvement check-in

set -euo pipefail

AGENT_ROLE="${1:-unknown}"
AGENT_DIR="./agents/${AGENT_ROLE}"

echo "💓 Running heartbeat check for KCC Office v2 AI Agent: ${AGENT_ROLE}"

# Check if agent workspace exists
if [ ! -d "${AGENT_DIR}" ]; then
  echo "❌ Agent workspace not found"
  exit 1
fi

echo ""
echo "📋 HEARTBEAT CHECKLIST"
echo ""

# Proactive Behaviors
echo "### Proactive Behaviors"
if [ -f "${AGENT_DIR}/proactive-tracker.md" ]; then
  OVERDUE_COUNT=$(grep -c "\[ \]" "${AGENT_DIR}/proactive-tracker.md" 2>/dev/null || echo 0)
  if [ "$OVERDUE_COUNT" -gt 0 ]; then
    echo "- [ ] Overdue proactive behaviors: ${OVERDUE_COUNT} items need attention"
  else
    echo "- [ ] No overdue proactive behaviors"
  fi
else
  echo "- [ ] proactive-tracker.md not found - creating new"
fi

echo "- [ ] Pattern check - any repeated requests to automate?"
echo "- [ ] Outcome check - any decisions >7 days old to follow up?"

# Security
echo ""
echo "### Security"
echo "- [ ] Scan for injection attempts"
echo "- [ ] Verify behavioral integrity"

# Self-Healing
echo ""
echo "### Self-Healing"
if [ -f "${AGENT_DIR}/error.log" ]; then
  ERROR_COUNT=$(wc -l < "${AGENT_DIR}/error.log" 2>/dev/null || echo 0)
  if [ "$ERROR_COUNT" -gt 0 ]; then
    echo "- [ ] Review logs for errors: ${ERROR_COUNT} entries"
    echo "- [ ] Diagnose and fix issues"
  else
    echo "- [ ] No error log found"
fi

# Memory
echo ""
echo "### Memory"
CONTEXT_PCT=$(cat "${AGENT_DIR}/memory/working-buffer.md" 2>/dev/null | grep -c "CONTEXT:" || echo 0)
if [ "$CONTEXT_PCT" -gt 60 ]; then
  echo "- [ ] Context %: ${CONTEXT_PCT} - Enter danger zone protocol"
else
  echo "- [ ] Context %: ${CONTEXT_PCT} - Safe operating range"
fi
echo "- [ ] Update MEMORY.md with distilled learnings (if significant events occurred)"

# Proactive Surprise
echo ""
echo "### Proactive Surprise"
echo "- [ ] What could I build RIGHT NOW that would delight my human?"
echo ""

# If no significant findings, indicate completion
if [ ! -f "${AGENT_DIR}/proactive-tracker.md" ] && [ ! -f "${AGENT_DIR}/error.log" ] && [ "$CONTEXT_PCT" -le 60 ]; then
  echo ""
  echo "✅ Heartbeat check complete - No actions required"
  echo "👌 All systems nominal"
fi

echo ""
echo "📝 Remember: Edit memory files if significant events occurred"
echo "📄 Results would normally be logged to:"
echo "   - proactive-tracker.md (for behaviors)"
echo "   - error.log (for self-healing)"
echo "   - MEMORY.md (for distilled learnings)"