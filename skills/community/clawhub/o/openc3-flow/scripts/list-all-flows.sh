#!/bin/bash
# Get all flows from Open-C3 platform
# Usage: ./list-all-flows.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Load configuration
if [ -f "$SKILL_DIR/config.env" ]; then
    source "$SKILL_DIR/config.env"
else
    echo "Error: config.env not found in $SKILL_DIR"
    exit 1
fi

# Validate configuration
if [ -z "$OPEN_C3_URL" ] || [ -z "$APP_NAME" ] || [ -z "$APP_KEY" ]; then
    echo "Error: Missing required configuration. Please check config.env"
    exit 1
fi

# Get all flows and format as table
response=$(curl -s -X GET "${OPEN_C3_URL}/api/ci/group/ci/dump" \
    -H "appname: ${APP_NAME}" \
    -H "appkey: ${APP_KEY}" \
    -H "Content-Type: application/json")

# Check if response is valid
stat=$(echo "$response" | jq -r '.stat')
if [ "$stat" != "true" ]; then
    echo "Error: API returned stat=false"
    echo "$response" | jq .
    exit 1
fi

# Count total flows
total=$(echo "$response" | jq '.data | length')

echo "✅ **系统共有 ${total} 条流水线：**"
echo ""
echo "| ID | 名称 | 服务树 ID | 服务树名称 | 源码地址 |"
echo "|----|------|----------|-----------|---------|"

# Format each flow as a table row
echo "$response" | jq -r '.data[] | "| \(.id) | \(.name) | \(.treeid) | \(.treename) | \(.addr // "null") |"'

echo ""
echo "**统计信息：**"
echo "- **总计**: ${total} 条流水线"

# Count by service tree
echo "$response" | jq -r '.data | group_by(.treename) | map("- **\(.[0].treename)** (ID:\(.[0].treeid)): \(length) 条") | .[]'
