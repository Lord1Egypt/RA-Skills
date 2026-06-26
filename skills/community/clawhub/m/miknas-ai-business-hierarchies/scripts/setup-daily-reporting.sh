#!/bin/bash

# AI Business Hierarchies - Daily Reporting Setup Script
# Configures cron jobs for automated agent reporting

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== AI Business Hierarchies - Daily Reporting Setup ===${NC}\n"

# Prompt for business name
if [ -z "$1" ]; then
    read -p "Business name (e.g., my-company): " BUSINESS_NAME
else
    BUSINESS_NAME="$1"
fi

BUSINESS_DIR="$HOME/business/$BUSINESS_NAME"

# Check if business exists
if [ ! -d "$BUSINESS_DIR" ]; then
    echo -e "${RED}Error: Business directory not found: $BUSINESS_DIR${NC}"
    echo "Run setup-business.sh first to create the business structure."
    exit 1
fi

echo -e "${YELLOW}Setting up automated reporting for: $BUSINESS_NAME${NC}\n"

# Create report generation script
REPORT_SCRIPT="$BUSINESS_DIR/scripts/generate-daily-reports.sh"
mkdir -p "$(dirname "$REPORT_SCRIPT")"

cat > "$REPORT_SCRIPT" << 'EOF'
#!/bin/bash

# Generate daily reports from all agents
# Run via cron job

BUSINESS_NAME="$(basename $(dirname $(dirname $0)))"
REPORT_DIR="$(dirname $0)/../reports/daily"
TODAY=$(date +%Y-%m-%d)
REPORT_FILE="$REPORT_DIR/daily-$TODAY.md"

mkdir -p "$REPORT_DIR"

echo "# Daily Agent Reports - $BUSINESS_NAME" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "**Date:** $TODAY" >> "$REPORT_FILE"
echo "**Generated:** $(date)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Get all active sessions for this business
SESSIONS=$(sessions_list --kinds agent | grep "$BUSINESS_NAME" | jq -r '.[] | select(.label | contains("'$BUSINESS_NAME'")) | .sessionKey' 2>/dev/null || echo "")

if [ -n "$SESSIONS" ]; then
    for SESSION in $SESSIONS; do
        SESSION_INFO=$(sessions_list --kinds agent | grep "$SESSION" | jq -r '.[] | select(.sessionKey == "'$SESSION'") | {label: .label, message: .lastMessage}')
        AGENT_LABEL=$(echo "$SESSION_INFO" | jq -r '.label')

        echo "## $AGENT_LABEL" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"

        # Get recent history
        HISTORY=$(sessions_history --sessionKey "$SESSION" --limit 5 2>/dev/null || echo "No recent activity")

        echo "**Last Activity:**" >> "$REPORT_FILE"
        echo "$HISTORY" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
        echo "---" >> "$REPORT_FILE"
        echo "" >> "$REPORT_FILE"
    done
else
    echo "No active sessions found for $BUSINESS_NAME" >> "$REPORT_FILE"
fi

echo "✓ Daily report generated: $REPORT_FILE"
EOF

chmod +x "$REPORT_SCRIPT"

echo -e "${GREEN}✓ Report generation script created${NC}\n"

# Setup cron jobs
CRON_FILE="$HOME/.business-cron-$BUSINESS_NAME"

cat > "$CRON_FILE" << EOF
# AI Business Hierarchies - Automated Reporting for $BUSINESS_NAME

# Daily Supervisor Reports (8 AM UTC)
0 8 * * * $REPORT_SCRIPT

# Weekly CEO Report (Monday 9 AM UTC)
0 9 * * 1 $BUSINESS_DIR/scripts/generate-weekly-report.sh

# Monthly Strategy Review (1st of month, 10 AM UTC)
0 10 1 * * $BUSINESS_DIR/scripts/generate-monthly-report.sh
EOF

echo -e "${YELLOW}Installing cron jobs...${NC}"
crontab -l > /tmp/current-cron 2>/dev/null || touch /tmp/current-cron
cat "$CRON_FILE" >> /tmp/current-cron
crontab /tmp/current-cron
rm /tmp/current-cron

echo -e "${GREEN}✓ Cron jobs installed${NC}\n"

# List scheduled jobs
echo -e "${BLUE}=== Scheduled Cron Jobs ===${NC}\n"
crontab -l | grep "$BUSINESS_NAME" | grep -v "^#" | sed 's/^/  /' || echo "No cron jobs found"

echo ""
echo -e "${YELLOW}=== Reporting Schedule ===${NC}\n"
echo "📅 Daily Reports: 8 AM UTC (Supervisor level)"
echo "📊 Weekly Reports: Monday 9 AM UTC (CEO level)"
echo "📈 Monthly Reports: 1st of month 10 AM UTC (Strategic)"
echo ""
echo -e "${GREEN}✓ Daily reporting setup complete!${NC}\n"
echo "Reports will be saved to: $BUSINESS_DIR/reports/"
echo ""
echo "To view current crontab: crontab -l"
echo "To remove jobs: crontab -e (delete lines for $BUSINESS_NAME)"
