#!/bin/bash
# OpenClaw Self Guard - Cron Job Setup Script
# Registers a daily vulnerability check cron job

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CRON_SCRIPT="$SKILL_DIR/scripts/check_vulns.py"
CRON_ID="openclaw-self-guard"
CRON_NAME="OpenClaw安全漏洞巡检"
CRON_SCHEDULE="0 6 * * *"  # Daily at 06:00 AM Beijing time

# Config
OC_CONFIG_DIR="$HOME/.openclaw"
OC_JOBS_FILE="$OC_CONFIG_DIR/cron/jobs.json"
OC_BACKUP_DIR="$OC_CONFIG_DIR/backups/configs"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🔒 OpenClaw Self Guard - Cron Setup${NC}"
echo "================================"

# Get channel from args or use default (empty = no delivery)
CHANNEL="${1:-}"

# Create backup directory
mkdir -p "$OC_BACKUP_DIR"

# Backup existing jobs file
if [ -f "$OC_JOBS_FILE" ]; then
    cp "$OC_JOBS_FILE" "$OC_BACKUP_DIR/jobs.json.backup.$(date +%Y%m%d_%H%M%S)"
    echo -e "${YELLOW}✓ Backed up existing jobs.json${NC}"
fi

# Read existing jobs or create new
if [ -f "$OC_JOBS_FILE" ]; then
    JOBS=$(cat "$OC_JOBS_FILE")
else
    JOBS='{"version":1,"jobs":[]}'
fi

# Check if job already exists
if echo "$JOBS" | grep -q "\"$CRON_ID\""; then
    echo -e "${YELLOW}⚠ Cron job '$CRON_ID' already exists. Updating...${NC}"
    JOBS=$(echo "$JOBS" | python3 -c "
import json, sys
data = json.load(sys.stdin)
data['jobs'] = [j for j in data['jobs'] if j.get('id') != '$CRON_ID']
print(json.dumps(data, indent=2))
")
fi

# Build delivery config
DELIVERY_CONFIG='"mode": "announce"'
if [ -n "$CHANNEL" ]; then
    DELIVERY_CONFIG='"mode": "announce", "channel": "'"$CHANNEL"'"'
fi

# Create new job (no hard-coded channel)
NEW_JOB=$(cat <<EOFJOB
{
    "id": "$CRON_ID",
    "name": "$CRON_NAME",
    "enabled": true,
    "createdAtMs": $(date +%s000),
    "schedule": {
        "kind": "cron",
        "expr": "$CRON_SCHEDULE"
    },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
        "kind": "agentTurn",
        "message": "请运行 python3 $CRON_SCRIPT --json 生成安全漏洞报告。如果 has_vulnerabilities 为 true，则输出完整报告并告诉我补救步骤。否则回复 '✅ 安全检查完成，无漏洞'。"
    },
    "delivery": {
        $DELIVERY_CONFIG
    }
}
EOFJOB
)

# Add new job
JOBS=$(echo "$JOBS" | python3 -c "
import json, sys
data = json.load(sys.stdin)
new_job = json.loads('''$NEW_JOB''')
data['jobs'].append(new_job)
print(json.dumps(data, indent=2))
")

# Write back
echo "$JOBS" > "$OC_JOBS_FILE"

echo -e "${GREEN}✓${NC} Cron job registered successfully!"
echo ""
echo "Job Details:"
echo "  - ID: $CRON_ID"
echo "  - Name: $CRON_NAME"
echo "  - Schedule: $CRON_SCHEDULE (daily at 06:00)"
echo "  - Script: $CRON_SCRIPT"
if [ -n "$CHANNEL" ]; then
echo "  - Delivery Channel: $CHANNEL"
else
echo "  - Delivery: Console only (no external channel)"
fi
echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
