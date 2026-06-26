#!/bin/bash
# OpenCLI Environment Setup Check Script
# Verifies that all prerequisites for opencli are met.

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS=0
FAIL=0
WARN=0

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    PASS=$((PASS + 1))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    echo -e "  ${YELLOW}→ Fix: $2${NC}"
    FAIL=$((FAIL + 1))
}

check_warn() {
    echo -e "${YELLOW}!${NC} $1"
    echo -e "  ${YELLOW}→ Note: $2${NC}"
    WARN=$((WARN + 1))
}

echo "============================================"
echo "  OpenCLI Environment Setup Check"
echo "============================================"
echo ""

# 1. Check Node.js
echo "--- Runtime ---"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node -v | sed 's/v//')
    NODE_MAJOR=$(echo "$NODE_VERSION" | cut -d. -f1)
    if [ "$NODE_MAJOR" -ge 20 ]; then
        check_pass "Node.js v${NODE_VERSION} (>= 20.0.0 required)"
    else
        check_fail "Node.js v${NODE_VERSION} is too old (>= 20.0.0 required)" "Run: brew install node  OR  nvm install 20"
    fi
else
    check_fail "Node.js not found" "Run: brew install node  OR visit https://nodejs.org"
fi

# 2. Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm -v)
    check_pass "npm v${NPM_VERSION}"
else
    check_fail "npm not found" "npm is usually installed with Node.js"
fi

echo ""

# 3. Check opencli installation
echo "--- OpenCLI ---"
if command -v opencli &> /dev/null; then
    OPENCLI_VERSION=$(opencli --version 2>/dev/null || echo "unknown")
    check_pass "opencli installed (${OPENCLI_VERSION})"
else
    check_fail "opencli not found" "Run: npm install -g @jackwener/opencli"
fi

echo ""

# 4. Check opencli doctor (extension + daemon connectivity)
echo "--- Connectivity ---"
if command -v opencli &> /dev/null; then
    DOCTOR_OUTPUT=$(opencli doctor 2>&1 || true)
    if echo "$DOCTOR_OUTPUT" | grep -qi "connected\|ok\|healthy\|ready"; then
        check_pass "opencli doctor: Extension and daemon connected"
    elif echo "$DOCTOR_OUTPUT" | grep -qi "not connected\|error\|fail"; then
        check_fail "opencli doctor: Connection issue detected" "Ensure Chrome is running with the opencli extension enabled. Details: ${DOCTOR_OUTPUT}"
    else
        check_warn "opencli doctor: Could not determine status" "Run 'opencli doctor' manually to check. Output: ${DOCTOR_OUTPUT}"
    fi
else
    check_fail "Cannot run opencli doctor (opencli not installed)" "Install opencli first: npm install -g @jackwener/opencli"
fi

echo ""

# 5. Check Chrome browser
echo "--- Browser ---"
if [[ "$OSTYPE" == "darwin"* ]]; then
    if [ -d "/Applications/Google Chrome.app" ]; then
        check_pass "Google Chrome found"
    else
        check_fail "Google Chrome not found" "Download from https://www.google.com/chrome/"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v google-chrome &> /dev/null || command -v google-chrome-stable &> /dev/null; then
        check_pass "Google Chrome found"
    else
        check_fail "Google Chrome not found" "Download from https://www.google.com/chrome/"
    fi
else
    check_warn "Cannot detect Chrome on this OS" "Ensure Google Chrome is installed"
fi

echo ""

# 6. Check optional dependencies
echo "--- Optional ---"
if command -v yt-dlp &> /dev/null; then
    check_pass "yt-dlp installed (for video downloads)"
else
    check_warn "yt-dlp not installed" "Only needed for video downloads. Install: brew install yt-dlp"
fi

echo ""
echo "============================================"
echo "  Results: ${GREEN}${PASS} passed${NC}, ${RED}${FAIL} failed${NC}, ${YELLOW}${WARN} warnings${NC}"
echo "============================================"

if [ "$FAIL" -gt 0 ]; then
    echo ""
    echo -e "${RED}Some checks failed. Please fix the issues above before using opencli.${NC}"
    exit 1
else
    echo ""
    echo -e "${GREEN}Environment is ready for opencli!${NC}"
    exit 0
fi
