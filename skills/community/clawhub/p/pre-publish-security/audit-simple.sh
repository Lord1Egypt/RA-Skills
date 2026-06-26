#!/bin/bash
# Simplified Pre-Publish Security Audit (no sub-agents)

set -e

TARGET_PATH="${1:-.}"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

echo "=== Pre-Publish Security Audit ==="
echo "Target: $TARGET_PATH"
echo "Time: $TIMESTAMP"
echo ""

CRITICAL_COUNT=0
HIGH_COUNT=0
MEDIUM_COUNT=0

### SECURITY SCAN ###
echo "🔒 Security Auditor"
echo "-------------------"

# Secret patterns
cd "$TARGET_PATH"
SECRETS=$(grep -r -E "(github_pat_|ghp_|AKIA|api_key|apikey|Bearer [A-Za-z0-9_-]+|password\s*=|pwd\s*=)" . \
  --exclude-dir=node_modules \
  --exclude-dir=.git \
  --exclude="*.tar.gz" \
  2>/dev/null || true)

if [ -n "$SECRETS" ]; then
    echo "❌ CRITICAL: Secrets detected:"
    echo "$SECRETS" | head -5
    ((CRITICAL_COUNT++))
else
    echo "✅ No secrets detected"
fi

# Check git config
if grep -q "github_pat_\|ghp_" .git/config 2>/dev/null; then
    echo "❌ CRITICAL: GitHub PAT in .git/config"
    ((CRITICAL_COUNT++))
fi

echo ""

### CODE QUALITY ###
echo "🔍 Code Quality Reviewer"
echo "------------------------"

# Shellcheck
if command -v shellcheck >/dev/null 2>&1; then
    SHELL_ISSUES=$(find . -name "*.sh" -exec shellcheck -f gcc {} \; 2>&1 | grep -E "error|warning" || true)
    if [ -n "$SHELL_ISSUES" ]; then
        echo "⚠️  HIGH: Shellcheck issues found"
        echo "$SHELL_ISSUES" | head -5
        ((HIGH_COUNT++))
    else
        echo "✅ Shell scripts passed"
    fi
else
    echo "ℹ️  Shellcheck not installed (skipping)"
fi

# Unsafe patterns
UNSAFE=$(grep -r -E "eval\(|os\.system\(|subprocess\.call" . \
  --exclude-dir=node_modules \
  2>/dev/null || true)
if [ -n "$UNSAFE" ]; then
    echo "⚠️  HIGH: Unsafe code patterns detected"
    echo "$UNSAFE" | head -3
    ((HIGH_COUNT++))
fi

echo ""

### DOCUMENTATION ###
echo "📝 Documentation Validator"
echo "--------------------------"

# Placeholders
PLACEHOLDERS=$(grep -r -E "\[ORG\]|\[TODO\]|\[USERNAME\]|example\.com" . \
  --include="*.md" \
  --include="*.json" \
  2>/dev/null || true)

if [ -n "$PLACEHOLDERS" ]; then
    echo "❌ CRITICAL: Placeholders found:"
    echo "$PLACEHOLDERS"
    ((CRITICAL_COUNT++))
else
    echo "✅ No placeholders detected"
fi

# Required files
[ -f README.md ] || { echo "⚠️  MEDIUM: Missing README.md"; ((MEDIUM_COUNT++)); }
[ -f LICENSE ] || { echo "⚠️  HIGH: Missing LICENSE file"; ((HIGH_COUNT++)); }

echo ""

### LICENSE ###
echo "⚖️  License Compliance Checker"
echo "-------------------------------"

if [ -f LICENSE ]; then
    echo "✅ LICENSE file exists"
else
    echo "⚠️  HIGH: Missing LICENSE file"
    ((HIGH_COUNT++))
fi

echo ""
echo "==========================="
echo "Summary:"
echo "  CRITICAL: $CRITICAL_COUNT"
echo "  HIGH: $HIGH_COUNT"
echo "  MEDIUM: $MEDIUM_COUNT"
echo "==========================="

if [ $CRITICAL_COUNT -gt 0 ]; then
    echo ""
    echo "❌ CRITICAL ISSUES FOUND - PUSH BLOCKED"
    exit 1
elif [ $HIGH_COUNT -gt 0 ]; then
    echo ""
    echo "⚠️  HIGH SEVERITY ISSUES FOUND - REVIEW REQUIRED"
    echo "Continue anyway? (y/n)"
    read -r response
    if [ "$response" != "y" ]; then
        exit 1
    fi
fi

echo ""
echo "✅ Security audit passed"
exit 0
