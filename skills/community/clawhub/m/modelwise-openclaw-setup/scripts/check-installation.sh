#!/bin/bash
# OpenClaw Installation Checker - Cross Platform (macOS/Linux/Windows Git Bash)

# Colors (disable on Windows if not supported)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    GREEN=""
    YELLOW=""
    RED=""
    NC=""
else
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    RED='\033[0;31m'
    NC='\033[0m'
fi

echo "🦞 OpenClaw Installation Checker"
echo "================================="
echo ""

# Detect OS
detect_os() {
    case "$OSTYPE" in
        darwin*)  echo "macOS" ;;
        linux*)   echo "Linux" ;;
        msys*)    echo "Windows (Git Bash)" ;;
        cygwin*)  echo "Windows (Cygwin)" ;;
        win32*)   echo "Windows" ;;
        *)        echo "Unknown ($OSTYPE)" ;;
    esac
}

echo "📋 System: $(detect_os)"
echo ""

# Check Node.js
echo "📋 Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version 2>/dev/null)
    NODE_MAJOR=$(echo "$NODE_VERSION" | cut -d'.' -f1 | tr -d 'v')

    if [ "$NODE_MAJOR" -ge 22 ]; then
        echo -e "  ${GREEN}✓${NC} Node.js version: $NODE_VERSION"
    else
        echo -e "  ${YELLOW}!${NC} Node.js version: $NODE_VERSION (need >= 22)"
        echo "    Upgrade: nvm install 22 && nvm use 22"
    fi
else
    echo -e "  ${RED}✗${NC} Node.js not installed"
    echo "    Install: https://nodejs.org/ or use nvm"
fi

# Check npm
echo ""
echo "📋 Checking npm..."
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version 2>/dev/null)
    echo -e "  ${GREEN}✓${NC} npm version: $NPM_VERSION"
else
    echo -e "  ${RED}✗${NC} npm not installed"
fi

# Check OpenClaw
echo ""
echo "📋 Checking OpenClaw..."
if command -v openclaw &> /dev/null; then
    OPENCLAW_VERSION=$(openclaw --version 2>/dev/null || echo "unknown")
    echo -e "  ${GREEN}✓${NC} OpenClaw CLI installed: $OPENCLAW_VERSION"
else
    echo -e "  ${RED}✗${NC} OpenClaw not installed"
    echo "    Install: npm install -g openclaw@latest"
fi

# Check config directory
echo ""
echo "📋 Checking configuration..."

# Cross-platform home directory
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    # Windows: use USERPROFILE or HOME
    if [ -n "$USERPROFILE" ]; then
        CONFIG_DIR="$USERPROFILE/.openclaw"
    else
        CONFIG_DIR="$HOME/.openclaw"
    fi
else
    # macOS/Linux
    CONFIG_DIR="$HOME/.openclaw"
fi

if [ -d "$CONFIG_DIR" ]; then
    echo -e "  ${GREEN}✓${NC} Config directory: $CONFIG_DIR"

    # Check config file
    if [ -f "$CONFIG_DIR/openclaw.json" ]; then
        echo -e "  ${GREEN}✓${NC} Configuration file exists"

        # Check model config (cross-platform grep)
        if grep -q "model" "$CONFIG_DIR/openclaw.json" 2>/dev/null; then
            echo -e "  ${GREEN}✓${NC} Model configured"
        else
            echo -e "  ${YELLOW}!${NC} Model not configured"
        fi
    else
        echo -e "  ${YELLOW}!${NC} Configuration file missing"
        echo "    Run: openclaw onboard"
    fi
else
    echo -e "  ${YELLOW}!${NC} Config directory missing: $CONFIG_DIR"
    echo "    Run: openclaw onboard"
fi

# Check Gateway
echo ""
echo "📋 Checking Gateway..."

# Cross-platform process check
check_gateway_process() {
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
        # Windows: use tasklist
        tasklist //FI "IMAGENAME eq node.exe" 2>/dev/null | grep -q "node.exe" && return 0
        return 1
    else
        # macOS/Linux: use pgrep
        pgrep -f "openclaw gateway" > /dev/null 2>&1 && return 0
        return 1
    fi
}

if check_gateway_process; then
    echo -e "  ${GREEN}✓${NC} Gateway is running"
else
    echo -e "  ${YELLOW}!${NC} Gateway is not running"
    echo "    Start with: openclaw gateway"
fi

# Check port 18789 (cross-platform)
check_port() {
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
        # Windows: use netstat
        netstat -an 2>/dev/null | grep -q ":18789.*LISTENING" && return 0
        return 1
    else
        # macOS/Linux: use lsof
        lsof -i :18789 > /dev/null 2>&1 && return 0
        return 1
    fi
}

if check_port; then
    echo -e "  ${GREEN}✓${NC} Port 18789 is in use"
else
    echo -e "  ${YELLOW}!${NC} Port 18789 is not in use"
fi

# Summary
echo ""
echo "================================="
echo "📊 Summary"

# Count issues
ISSUES=0

if ! command -v node &> /dev/null; then ((ISSUES++)); fi
if [ "$NODE_MAJOR" -lt 22 ] 2>/dev/null; then ((ISSUES++)); fi
if ! command -v openclaw &> /dev/null; then ((ISSUES++)); fi
if [ ! -d "$CONFIG_DIR" ]; then ((ISSUES++)); fi
if [ ! -f "$CONFIG_DIR/openclaw.json" ]; then ((ISSUES++)); fi

if [ "$ISSUES" -eq 0 ]; then
    echo -e "${GREEN}✓ OpenClaw is properly installed!${NC}"
    echo ""
    echo "Quick commands:"
    echo "  openclaw doctor      - Run diagnostics"
    echo "  openclaw gateway     - Start gateway"
    echo "  openclaw skills list - List installed skills"
else
    echo -e "${YELLOW}! Found $ISSUES issue(s)${NC}"
    echo ""
    echo "Installation steps:"
    echo ""
    echo "  Windows (PowerShell):"
    echo "    1. Install Node.js 22+: winget install OpenJS.NodeJS.LTS"
    echo "    2. Or download from: https://nodejs.org/"
    echo "    3. Install openclaw: npm install -g openclaw@latest"
    echo "    4. Run setup wizard: openclaw onboard"
    echo ""
    echo "  macOS/Linux:"
    echo "    1. Install Node.js 22+: nvm install 22"
    echo "    2. Install openclaw: npm install -g openclaw@latest"
    echo "    3. Run setup wizard: openclaw onboard"
fi

echo ""
