#!/usr/bin/env bash
# Security Audit Script for Proactive Agent Skill
# Scans workspace for potential security issues

set -e

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔒 Proactive Agent Security Audit"
echo "=================================="
echo "Workspace: $WORKSPACE"
echo ""

ISSUES=0
WARNINGS=0

# Function to report issues
report_issue() {
    echo -e "${RED}[ISSUE]${NC} $1"
    ((ISSUES++))
}

report_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
    ((WARNINGS++))
}

report_ok() {
    echo -e "${GREEN}[OK]${NC} $1"
}

# Check 1: Credential files should be in .gitignore
echo "Checking credential protection..."
if [ -f "$WORKSPACE/.gitignore" ]; then
    if grep -q "\.env" "$WORKSPACE/.gitignore" 2>/dev/null; then
        report_ok ".env files are gitignored"
    else
        report_warning ".env not in .gitignore"
    fi
else
    report_warning "No .gitignore found"
fi

# Check 2: Look for exposed API keys in workspace files
echo "Scanning for exposed credentials..."
if grep -r "sk-[a-zA-Z0-9]\{20,\}" "$WORKSPACE" --include="*.md" --include="*.txt" 2>/dev/null | grep -v ".env"; then
    report_issue "Potential API key found in workspace files"
else
    report_ok "No exposed API keys in workspace files"
fi

# Check 3: Check for curl/wget to unknown URLs in skills
echo "Checking skill scripts..."
if [ -d "$WORKSPACE/skills" ]; then
    for skill in "$WORKSPACE/skills"/*/; do
        if [ -f "${skill}*.py" ] || [ -f "${skill}*.sh" ]; then
            if grep -q "curl.*|" "${skill}"*.py "${skill}"*.sh 2>/dev/null; then
                report_warning "Skill $skill contains curl piped to shell"
            fi
        fi
    done
    report_ok "Skill scripts reviewed"
fi

# Check 4: Verify no external network calls in skills without approval
echo "Checking for unauthorized network calls..."
if grep -r "requests\.post\|urllib\.request" "$WORKSPACE/skills" --include="*.py" 2>/dev/null | grep -v "api\." | grep -v "localhost"; then
    report_warning "Found network calls to non-API endpoints"
else
    report_ok "Network calls appear to be to known APIs"
fi

# Check 5: Memory files should not contain sensitive data patterns
echo "Checking memory files for sensitive data..."
if [ -d "$WORKSPACE/memory" ]; then
    if grep -rE "(password|secret|token|key)\s*[=:]\s*['\"][^'\"]+['\"]" "$WORKSPACE/memory" 2>/dev/null; then
        report_issue "Potential credentials in memory files"
    else
        report_ok "Memory files clean"
    fi
fi

# Check 6: Verify AGENTS.md has security guidelines
echo "Checking security guidelines..."
if [ -f "$WORKSPACE/AGENTS.md" ]; then
    if grep -q "injection\|external content\|don't execute" "$WORKSPACE/AGENTS.md" 2>/dev/null; then
        report_ok "Security guidelines present in AGENTS.md"
    else
        report_warning "AGENTS.md may lack security guidelines"
    fi
else
    report_warning "AGENTS.md not found"
fi

# Summary
echo ""
echo "=================================="
echo "Audit Complete"
echo "=================================="
echo -e "Issues: ${RED}$ISSUES${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"

if [ $ISSUES -gt 0 ]; then
    echo ""
    echo -e "${RED}Action required: Please address the issues above.${NC}"
    exit 1
elif [ $WARNINGS -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}Recommendation: Review warnings when convenient.${NC}"
    exit 0
else
    echo ""
    echo -e "${GREEN}All checks passed! Workspace looks secure.${NC}"
    exit 0
fi
