#!/bin/bash
#
# GitLab Weekly Report Generator - Fixed Version
# 自动生成指定时间范围内团队成员的 GitLab 周报
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 默认配置
CONFIG_FILE=""
START_DATE=""
END_DATE=""
OUTPUT_DIR=""
FEISHU_UPLOAD=false
GENERATE_CHARTS=true

show_help() {
    cat << EOF
GitLab Weekly Report Generator

Usage:
    $0 [options]

Options:
    -c, --config FILE       Config file path
    -s, --start-date DATE   Start date (YYYY-MM-DD)
    -e, --end-date DATE     End date (YYYY-MM-DD)
    -o, --output DIR        Output directory
    -f, --feishu            Upload to Feishu
    --no-charts             Skip chart generation
    -h, --help              Show help
EOF
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -c|--config) CONFIG_FILE="$2"; shift 2 ;;
            -s|--start-date) START_DATE="$2"; shift 2 ;;
            -e|--end-date) END_DATE="$2"; shift 2 ;;
            -o|--output) OUTPUT_DIR="$2"; shift 2 ;;
            -f|--feishu) FEISHU_UPLOAD=true; shift ;;
            --no-charts) GENERATE_CHARTS=false; shift ;;
            -h|--help) show_help; exit 0 ;;
            *) echo -e "${RED}Unknown option: $1${NC}"; show_help; exit 1 ;;
        esac
    done
}

load_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        echo -e "${BLUE}Loading config: $CONFIG_FILE${NC}"
        GITLAB_URL=$(jq -r '.gitlab.url // "https://gitlab.example.com"' "$CONFIG_FILE")
        GITLAB_TOKEN=$(jq -r '.gitlab.token // ""' "$CONFIG_FILE")
        USERS_JSON=$(jq -c '.users // []' "$CONFIG_FILE")
        FEISHU_ENABLED=$(jq -r '.feishu.enabled // false' "$CONFIG_FILE")
        FEISHU_DOC_URL=$(jq -r '.feishu.doc_url // ""' "$CONFIG_FILE")
        FEISHU_APP_ID=$(jq -r '.feishu.app_id // ""' "$CONFIG_FILE")
        FEISHU_APP_SECRET=$(jq -r '.feishu.app_secret // ""' "$CONFIG_FILE")
        
        if [[ "$GENERATE_CHARTS" == true ]]; then
            GENERATE_CHARTS=$(jq -r '.visualization.enabled // true' "$CONFIG_FILE")
        fi
        
        if [[ -z "$OUTPUT_DIR" ]]; then
            OUTPUT_DIR=$(jq -r '.report.output_dir // "./reports"' "$CONFIG_FILE")
        fi
    else
        echo -e "${RED}Config file not found: $CONFIG_FILE${NC}"
        exit 1
    fi
}

validate() {
    [[ -z "$GITLAB_TOKEN" ]] && { echo -e "${RED}GitLab Token required${NC}"; exit 1; }
    [[ "$USERS_JSON" == "[]" ]] && { echo -e "${RED}No users configured${NC}"; exit 1; }
    
    if [[ -z "$START_DATE" ]]; then
        START_DATE=$(date -v-7d +%Y-%m-%d 2>/dev/null || date -d "7 days ago" +%Y-%m-%d)
    fi
    if [[ -z "$END_DATE" ]]; then
        END_DATE=$(date +%Y-%m-%d)
    fi
    
    REPORT_DIR="${OUTPUT_DIR}/${START_DATE}_to_${END_DATE}"
    mkdir -p "$REPORT_DIR"
    mkdir -p "$REPORT_DIR/charts"
    
    echo -e "${BLUE}Output: $REPORT_DIR${NC}"
}

get_user_events() {
    local user_id=$1
    curl -s "${GITLAB_URL}/api/v4/users/${user_id}/events?per_page=100" \
        -H "PRIVATE-TOKEN: ${GITLAB_TOKEN}" 2>/dev/null
}

generate_weekly_report() {
    echo -e "${BLUE}Generating report...${NC}"
    echo -e "${BLUE}Period: ${START_DATE} to ${END_DATE}${NC}"
    echo ""
    
    local report_file="${REPORT_DIR}/weekly_report.md"
    
    # Header
    cat > "$report_file" << EOF
# Agent Dev Weekly Report

Period: \`${START_DATE}\` to \`${END_DATE}\`

Team members:

EOF

    # User list
    local user_count=$(echo "$USERS_JSON" | jq 'length')
    for ((i=0; i<user_count; i++)); do
        local name=$(echo "$USERS_JSON" | jq -r ".[$i].name")
        local username=$(echo "$USERS_JSON" | jq -r ".[$i].username")
        echo "- $name (\`$username\`)" >> "$report_file"
    done
    
    echo "" >> "$report_file"
    echo "---" >> "$report_file"
    echo "" >> "$report_file"
    
    # User details
    for ((i=0; i<user_count; i++)); do
        local username=$(echo "$USERS_JSON" | jq -r ".[$i].username")
        local user_id=$(echo "$USERS_JSON" | jq -r ".[$i].id")
        local user_name=$(echo "$USERS_JSON" | jq -r ".[$i].name")
        
        echo -e "${YELLOW}Processing: $user_name${NC}"
        
        echo "### $user_name ($username)" >> "$report_file"
        echo "" >> "$report_file"
        
        local events=$(get_user_events "$user_id")
        local filtered=$(echo "$events" | jq --arg s "$START_DATE" --arg e "$END_DATE" '
            map(select(.created_at >= ($s + "T00:00:00Z") and .created_at <= ($e + "T23:59:59Z")))
        ')
        local count=$(echo "$filtered" | jq 'length')
        
        if [[ "$count" -eq 0 ]]; then
            echo "No activity in this period." >> "$report_file"
            echo "" >> "$report_file"
            continue
        fi
        
        echo "**Activity count**: $count" >> "$report_file"
        echo "" >> "$report_file"
        
        # MRs
        local mrs=$(echo "$filtered" | jq '[map(select(.target_type == "merge_request")) | group_by(.target_iid) | map(.[0])]')
        local mr_count=$(echo "$mrs" | jq 'length')
        if [[ "$mr_count" -gt 0 ]]; then
            echo "#### Merge Requests ($mr_count)" >> "$report_file"
            echo "" >> "$report_file"
            echo "$mrs" | jq -r '.[] | "- **!\(.target_iid)** \(.target_title)\n  - Action: \(.action_name) | Date: \(.created_at[:10])"' >> "$report_file"
            echo "" >> "$report_file"
        fi
        
        # Commits
        local pushes=$(echo "$filtered" | jq '[map(select(.action_name | contains("pushed"))) | .[:10]]')
        local push_count=$(echo "$pushes" | jq 'length')
        if [[ "$push_count" -gt 0 ]]; then
            echo "#### Commits ($push_count)" >> "$report_file"
            echo "" >> "$report_file"
            echo "$pushes" | jq -r '.[] | select(.push_data) | "- `\(.push_data.commit_title[:60])`\n  - Branch: \(.push_data.ref) | Date: \(.created_at[:10])"' >> "$report_file"
            echo "" >> "$report_file"
        fi
    done
    
    # Summary
    cat >> "$report_file" << EOF
## Summary

Period: ${START_DATE} to ${END_DATE}

### Overview

| User | Activities |
|------|------------|

EOF

    for ((i=0; i<user_count; i++)); do
        local name=$(echo "$USERS_JSON" | jq -r ".[$i].name")
        local uid=$(echo "$USERS_JSON" | jq -r ".[$i].id")
        local events=$(get_user_events "$uid")
        local filtered=$(echo "$events" | jq --arg s "$START_DATE" --arg e "$END_DATE" 'map(select(.created_at >= ($s + "T00:00:00Z") and .created_at <= ($e + "T23:59:59Z"))) | length')
        echo "| $name | $filtered |" >> "$report_file"
    done
    
    echo "" >> "$report_file"
    echo "---" >> "$report_file"
    echo "" >> "$report_file"
    echo "*Generated: $(date '+%Y-%m-%d %H:%M:%S')*" >> "$report_file"
    
    echo ""
    echo -e "${GREEN}Report generated: $report_file${NC}"
    
    # Create symlink
    ln -sfn "$REPORT_DIR" "${OUTPUT_DIR}/latest"
    
    echo -e "${GREEN}Done!${NC}"
}

main() {
    parse_args "$@"
    [[ -z "$CONFIG_FILE" ]] && { echo -e "${RED}Config file required (-c)${NC}"; exit 1; }
    load_config
    validate
    generate_weekly_report
}

main "$@"
