#!/usr/bin/bash

# Council of Wisdom - Validation Script
# Validates the skill structure and verifies all required files exist

set -euo pipefail

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Counters
PASSED=0
FAILED=0
WARNINGS=0

# Functions
pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

# Main validation
echo "Council of Wisdom - Skill Validation"
echo "===================================="
echo ""

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Validating skill at: ${SCRIPT_DIR}"
echo ""

# Check required files
echo "Required Files:"
echo "---------------"

# SKILL.md
if [[ -f "${SCRIPT_DIR}/SKILL.md" ]]; then
    pass "SKILL.md exists"
    if grep -q "Council of Wisdom" "${SCRIPT_DIR}/SKILL.md"; then
        pass "SKILL.md contains correct title"
    else
        fail "SKILL.md title mismatch"
    fi
else
    fail "SKILL.md missing"
fi

# README.md
if [[ -f "${SCRIPT_DIR}/README.md" ]]; then
    pass "README.md exists"
else
    fail "README.md missing"
fi

# _meta.json
if [[ -f "${SCRIPT_DIR}/_meta.json" ]]; then
    pass "_meta.json exists"
else
    fail "_meta.json missing"
fi

# IMPLEMENTATION.md
if [[ -f "${SCRIPT_DIR}/IMPLEMENTATION.md" ]]; then
    pass "IMPLEMENTATION.md exists"
else
    fail "IMPLEMENTATION.md missing"
fi

# Check directory structure
echo ""
echo "Directory Structure:"
echo "--------------------"

# scripts/
if [[ -d "${SCRIPT_DIR}/scripts" ]]; then
    pass "scripts/ directory exists"
    if [[ -x "${SCRIPT_DIR}/scripts/council-of-wisdom.sh" ]]; then
        pass "council-of-wisdom.sh is executable"
    else
        fail "council-of-wisdom.sh is not executable"
    fi
else
    fail "scripts/ directory missing"
fi

# templates/
if [[ -d "${SCRIPT_DIR}/templates" ]]; then
    pass "templates/ directory exists"
else
    fail "templates/ directory missing"
fi

# .github/
if [[ -d "${SCRIPT_DIR}/.github" ]]; then
    pass ".github/ directory exists"
    if [[ -f "${SCRIPT_DIR}/.github/workflows/test.yml" ]]; then
        pass "GitHub Actions workflow exists"
    else
        warn "GitHub Actions workflow missing (optional)"
    fi
else
    warn ".github/ directory missing (optional)"
fi

# Check template files
echo ""
echo "Template Files:"
echo "---------------"

if [[ -f "${SCRIPT_DIR}/templates/referee-prompt.md" ]]; then
    pass "referee-prompt.md exists"
else
    fail "referee-prompt.md missing"
fi

if [[ -f "${SCRIPT_DIR}/templates/debater-prompt.md" ]]; then
    pass "debater-prompt.md exists"
else
    fail "debater-prompt.md missing"
fi

if [[ -f "${SCRIPT_DIR}/templates/council-prompts.md" ]]; then
    pass "council-prompts.md exists"
else
    fail "council-prompts.md missing"
fi

# Check content quality
echo ""
echo "Content Quality:"
echo "----------------"

# Check SKILL.md size
SKILL_SIZE=$(stat -c%s "${SCRIPT_DIR}/SKILL.md" 2>/dev/null || stat -f%z "${SCRIPT_DIR}/SKILL.md" 2>/dev/null)
if [[ $SKILL_SIZE -gt 10000 ]]; then
    pass "SKILL.md is comprehensive ($((SKILL_SIZE / 1024))KB)"
else
    warn "SKILL.md may be too short"
fi

# Check for key sections in SKILL.md
if grep -q "Architecture Overview" "${SCRIPT_DIR}/SKILL.md"; then
    pass "SKILL.md has architecture section"
else
    fail "SKILL.md missing architecture section"
fi

if grep -q "Council of 9" "${SCRIPT_DIR}/SKILL.md"; then
    pass "SKILL.md has council section"
else
    fail "SKILL.md missing council section"
fi

if grep -q "Monitoring & Metrics" "${SCRIPT_DIR}/SKILL.md"; then
    pass "SKILL.md has monitoring section"
else
    fail "SKILL.md missing monitoring section"
fi

# Check _meta.json structure
echo ""
echo "Metadata Validation:"
echo "--------------------"

if command -v jq &> /dev/null; then
    if jq empty "${SCRIPT_DIR}/_meta.json" 2>/dev/null; then
        pass "_meta.json is valid JSON"
    else
        fail "_meta.json is not valid JSON"
    fi

    if jq -e '.name' "${SCRIPT_DIR}/_meta.json" &> /dev/null; then
        NAME=$(jq -r '.name' "${SCRIPT_DIR}/_meta.json")
        if [[ "$NAME" == "council-of-wisdom" ]]; then
            pass "Skill name is correct: $NAME"
        else
            fail "Skill name incorrect: $NAME"
        fi
    else
        fail "_meta.json missing name field"
    fi

    VERSION=$(jq -r '.version' "${SCRIPT_DIR}/_meta.json")
    if [[ "$VERSION" != "null" ]]; then
        pass "Version defined: $VERSION"
    else
        warn "Version not defined"
    fi
else
    warn "jq not available, skipping JSON validation"
fi

# Summary
echo ""
echo "===================================="
echo "Validation Summary"
echo "===================================="
echo -e "${GREEN}Passed:${NC}  $PASSED"
echo -e "${RED}Failed:${NC}  $FAILED"
echo -e "${YELLOW}Warnings:${NC} $WARNINGS"
echo ""

if [[ $FAILED -eq 0 ]]; then
    echo -e "${GREEN}✓ All critical checks passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some checks failed. Please review and fix.${NC}"
    exit 1
fi
