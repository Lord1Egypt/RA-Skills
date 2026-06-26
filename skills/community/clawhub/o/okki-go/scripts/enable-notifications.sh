#!/bin/bash
# Okki Go update notification setup script (macOS/Linux)
# Usage: bash scripts/enable-notifications.sh

set -e

SKILL_NAME="okki-go"
CRON_NAME="${SKILL_NAME}-update-reminder"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${CYAN}🌐 Okki Go skill update notification setup${NC}"
echo "━━━━━━━━━━━━━��━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if openclaw command exists
if ! command -v openclaw &> /dev/null; then
    echo -e "${RED}❌ Error: openclaw command not found${NC}"
    echo ""
    echo "Please install OpenClaw first:"
    echo "  npm install -g openclaw"
    exit 1
fi

# Check if a notification job already exists
if openclaw cron list 2>/dev/null | grep -q "$CRON_NAME"; then
    echo -e "${GREEN}✅ Update notifications are already enabled${NC}"
    echo ""
    echo "Current setting: check for new versions every Monday at 10:00 AM"
    echo ""
    echo -e "${YELLOW}Management options:${NC}"
    echo "  1. Disable notifications"
    echo "  2. Change check frequency"
    echo "  3. Check for updates now"
    echo "  4. Exit"
    echo ""
    read -p "Choose [1-4]: " choice

    case $choice in
        1)
            JOB_ID=$(openclaw cron list | grep "$CRON_NAME" | awk '{print $1}')
            if [ -n "$JOB_ID" ]; then
                openclaw cron remove --jobId "$JOB_ID"
                echo -e "${GREEN}✅ Update notifications disabled${NC}"
            fi
            ;;
        2)
            echo ""
            echo "Select check frequency:"
            echo "  1. Daily"
            echo "  2. Weekly (current)"
            echo "  3. Monthly"
            read -p "Choose [1-3]: " freq
            case $freq in
                1) SCHEDULE="0 10 * * *" ;;
                2) SCHEDULE="0 10 * * 1" ;;
                3) SCHEDULE="0 10 1 * *" ;;
                *) echo "Invalid choice"; exit 1 ;;
            esac
            JOB_ID=$(openclaw cron list | grep "$CRON_NAME" | awk '{print $1}')
            if [ -n "$JOB_ID" ]; then
                openclaw cron update --jobId "$JOB_ID" --schedule "$SCHEDULE"
                echo -e "${GREEN}✅ Check frequency updated${NC}"
            fi
            ;;
        3)
            echo ""
            echo "🔍 Checking for updates manually..."
            bash "$SCRIPT_DIR/check-update.sh"
            ;;
        *)
            echo "Exited"
            ;;
    esac
    exit 0
fi

# Welcome message
echo -e "${CYAN}📬 Would you like to enable Okki Go update notifications?${NC}"
echo ""
echo "Once enabled, you will receive:"
echo "  • New version release alerts"
echo "  • Changelog previews"
echo "  • One-command update instructions"
echo ""
echo "Check frequency: Every Monday at 10:00 AM (customizable)"
echo ""

read -p "Enable? [Y/n] " confirm

if [[ "$confirm" =~ ^[Nn]$ ]]; then
    echo ""
    echo -e "${YELLOW}⏭️ Skipped${NC}"
    echo ""
    echo "You can enable it later by running:"
    echo "  bash scripts/enable-notifications.sh"
    exit 0
fi

# Create cron job
PAYLOAD='CURRENT=$(cat ~/.openclaw/workspace/skills/okki-go/VERSION 2>/dev/null); if [ -z "$CURRENT" ]; then CURRENT=$(grep "^version:" ~/.openclaw/workspace/skills/okki-go/SKILL.md 2>/dev/null | awk '\''{print $2}'\''); fi; if [ -z "$CURRENT" ]; then CURRENT="unknown"; fi; LATEST=$(clawhub search okki go --limit 1 2>/dev/null | jq -r '\''if .[0] then .[0].version else "unknown" end'\''); if [ -n "$LATEST" ] && [ "$CURRENT" != "$LATEST" ] && [ "$LATEST" != "unknown" ]; then CHANGELOG=$(clawhub show okki-go@$LATEST --changelog 2>/dev/null | head -15); echo "📦 Okki Go new version available"; echo ""; echo "Current version: $CURRENT"; echo "Latest version:  $LATEST"; echo ""; echo "What'\''s new:"; echo "$CHANGELOG"; echo ""; echo "Update command: openclaw skills update okki-go"; echo "Skip: dismiss this notification, remind again next week"; elif [ "$CURRENT" = "$LATEST" ]; then echo "✅ Okki Go is already up to date ($CURRENT)"; fi'

echo ""
echo "📝 Configuring update notifications..."

if openclaw cron add \
  --name "$CRON_NAME" \
  --schedule "0 10 * * 1" \
  --payload "$PAYLOAD" \
  --delivery "announce" 2>/dev/null; then

    echo ""
    echo -e "${GREEN}✅ Update notifications enabled!${NC}"
    echo ""
    echo "Configuration details:"
    echo "  Skill name:      $SKILL_NAME"
    echo "  Check frequency: Every Monday at 10:00 AM"
    echo "  Delivery:        OpenClaw message"
    echo ""
    echo -e "${CYAN}Management commands:${NC}"
    echo "  View status:     bash scripts/enable-notifications.sh"
    echo "  Manual check:    bash scripts/check-update.sh"
    echo "  Disable:         run the script and choose option 1"
    echo ""
    echo -e "${YELLOW}Note:${NC} When a new version is available, you can choose to update immediately or later"
else
    echo ""
    echo -e "${RED}❌ Configuration failed${NC}"
    echo ""
    echo "Please check:"
    echo "  1. OpenClaw gateway is running (openclaw gateway status)"
    echo "  2. You have sufficient permissions"
    echo ""
    echo "Or create the notification job manually:"
    echo "  openclaw cron add --name \"$CRON_NAME\" --schedule \"0 10 * * 1\" --delivery \"announce\""
    exit 1
fi
