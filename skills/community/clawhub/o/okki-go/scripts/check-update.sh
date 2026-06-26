#!/bin/bash
# Okki Go version check script (macOS/Linux)
# Usage: bash scripts/check-update.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
SKILL_NAME="okki-go"

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}🔍 Checking for okki-go updates...${NC}"
echo ""

# Get current version
CURRENT=$(cat "$SKILL_DIR/VERSION" 2>/dev/null)
if [ -z "$CURRENT" ]; then
    CURRENT=$(grep "^version:" "$SKILL_DIR/SKILL.md" 2>/dev/null | awk '{print $2}')
fi
if [ -z "$CURRENT" ]; then
    CURRENT="unknown"
fi

# Get latest version
LATEST=$(clawhub search "$SKILL_NAME" --limit 1 2>/dev/null | jq -r 'if .[0] then .[0].version else "unknown" end')

echo "Current version: $CURRENT"
echo "Latest version:  $LATEST"
echo ""

if [ "$CURRENT" = "$LATEST" ]; then
    echo -e "${GREEN}✅ Already up to date ($CURRENT)${NC}"
    exit 0
fi

if [ "$LATEST" = "unknown" ]; then
    echo -e "${YELLOW}⚠️ Unable to fetch latest version info${NC}"
    echo ""
    echo "Please check your network connection or try again later"
    exit 1
fi

# New version available
echo -e "${YELLOW}📦 New version available: $CURRENT → $LATEST${NC}"
echo ""

# Show changelog
echo "What's new:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
clawhub show "${SKILL_NAME}@${LATEST}" --changelog 2>/dev/null | head -20
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Ask what to do
echo "Options:"
echo "  1. Update now"
echo "  2. Remind me later"
echo "  3. Don't remind again (disable notifications)"
echo ""

read -p "Choose [1-3]: " choice

case $choice in
    1)
        echo ""
        echo "🔄 Updating..."
        if openclaw skills update "$SKILL_NAME"; then
            echo -e "${GREEN}✅ Update complete!${NC}"
            echo ""
            echo "New version features are ready"
        else
            echo -e "${RED}❌ Update failed${NC}"
            echo ""
            echo "Please check your network or update manually:"
            echo "  openclaw skills update $SKILL_NAME"
        fi
        ;;
    2)
        echo ""
        echo -e "${YELLOW}⏭️ Skipped${NC}"
        echo ""
        echo "You will be reminded again when a new version is available"
        echo "Update command: openclaw skills update $SKILL_NAME"
        ;;
    3)
        echo ""
        CRON_NAME="${SKILL_NAME}-update-reminder"
        JOB_ID=$(openclaw cron list 2>/dev/null | grep "$CRON_NAME" | awk '{print $1}')
        if [ -n "$JOB_ID" ]; then
            openclaw cron remove --jobId "$JOB_ID"
            echo -e "${GREEN}✅ Update notifications disabled${NC}"
        else
            echo "No notification job found"
        fi
        ;;
    *)
        echo "Invalid choice"
        ;;
esac
