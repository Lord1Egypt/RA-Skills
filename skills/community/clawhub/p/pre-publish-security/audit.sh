#!/bin/bash
# Pre-Publish Security Audit Orchestrator

set -e

TARGET_PATH="${1:-.}"
REPORT_DIR="/tmp/openclaw-security-audit-$(date +%s)"
mkdir -p "$REPORT_DIR"

echo "=== Pre-Publish Security Audit ==="
echo "Target: $TARGET_PATH"
echo "Report: $REPORT_DIR"
echo ""

CRITICAL_FOUND=0
HIGH_FOUND=0

# Spawn Security Auditor
echo "🔒 Launching Security Auditor..."
openclaw sessions spawn \
  --runtime subagent \
  --mode run \
  --label "security-auditor" \
  --task "$(cat ~/.openclaw/workspace/skills/pre-publish-security/agents/security-auditor.md | sed "s|{{TARGET}}|$TARGET_PATH|g")" \
  > "$REPORT_DIR/security.txt" 2>&1 &
SEC_PID=$!

# Spawn Code Quality Reviewer
echo "🔍 Launching Code Quality Reviewer..."
openclaw sessions spawn \
  --runtime subagent \
  --mode run \
  --label "code-quality" \
  --task "$(cat ~/.openclaw/workspace/skills/pre-publish-security/agents/code-quality.md | sed "s|{{TARGET}}|$TARGET_PATH|g")" \
  > "$REPORT_DIR/quality.txt" 2>&1 &
QUAL_PID=$!

# Spawn Documentation Validator
echo "📝 Launching Documentation Validator..."
openclaw sessions spawn \
  --runtime subagent \
  --mode run \
  --label "docs-validator" \
  --task "$(cat ~/.openclaw/workspace/skills/pre-publish-security/agents/docs-validator.md | sed "s|{{TARGET}}|$TARGET_PATH|g")" \
  > "$REPORT_DIR/docs.txt" 2>&1 &
DOCS_PID=$!

# Spawn License Checker
echo "⚖️  Launching License Compliance Checker..."
openclaw sessions spawn \
  --runtime subagent \
  --mode run \
  --label "license-checker" \
  --task "$(cat ~/.openclaw/workspace/skills/pre-publish-security/agents/license-checker.md | sed "s|{{TARGET}}|$TARGET_PATH|g")" \
  > "$REPORT_DIR/license.txt" 2>&1 &
LIC_PID=$!

# Wait for all agents
echo ""
echo "⏳ Waiting for agents to complete..."
wait $SEC_PID $QUAL_PID $DOCS_PID $LIC_PID

# Parse results
echo ""
echo "=== AUDIT RESULTS ==="
for report in "$REPORT_DIR"/*.txt; do
    cat "$report"
    if grep -q "CRITICAL" "$report"; then
        CRITICAL_FOUND=1
    fi
    if grep -q "HIGH" "$report"; then
        HIGH_FOUND=1
    fi
done

echo ""
echo "Report saved to: $REPORT_DIR"

if [ $CRITICAL_FOUND -eq 1 ]; then
    echo ""
    echo "❌ CRITICAL ISSUES FOUND - PUSH BLOCKED"
    exit 1
elif [ $HIGH_FOUND -eq 1 ]; then
    echo ""
    echo "⚠️  HIGH SEVERITY ISSUES FOUND - REVIEW REQUIRED"
    echo "Continue? (y/n)"
    read -r response
    if [ "$response" != "y" ]; then
        exit 1
    fi
fi

echo ""
echo "✅ Security audit passed"
exit 0
