#!/usr/bin/env bash
#
# Log Analyzer
# Analyzes server logs for error patterns, IP frequency, time-based analysis, alert generation
#

set -euo pipefail

# ── Colors ──────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# ── Defaults ────────────────────────────────────────────
ERROR_PATTERN="error|fail|warn|critical|exception|fatal|denied|timeout|refused"
FILE=""
TIME_WINDOW=24
MODE="all"

# ── Help ────────────────────────────────────────────────
usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS] [--all | --errors | --time-analysis | --ips | --spikes]

Analyze log files for error patterns, IP frequency, time-based analysis, and spikes.

Options:
  -f <file>         Log file to analyze (use '-' for stdin)
  -p <pattern>      Custom error pattern regex (default: $ERROR_PATTERN)
  -t <hours>        Time window in hours (default: 24)
  --errors          Find top error messages and their frequency
  --time-analysis   Group errors by time period (hourly/daily)
  --ips             Analyze IP frequency from log entries
  --spikes          Identify unusual patterns and spikes
  --all             Run all analyses (default)
  --help            Show this help message

Examples:
  $(basename "$0") -f /var/log/syslog --all
  journalctl -u nginx --since "24 hours ago" | $(basename "$0") -f - --all
  $(basename "$0") -f /var/log/auth.log --ips --spikes
EOF
    exit 0
}

# ── Parse Args ──────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        -f) FILE="$2"; shift 2 ;;
        -p) ERROR_PATTERN="$2"; shift 2 ;;
        -t) TIME_WINDOW="$2"; shift 2 ;;
        --errors) MODE="errors" ; shift ;;
        --time-analysis) MODE="time" ; shift ;;
        --ips) MODE="ips" ; shift ;;
        --spikes) MODE="spikes" ; shift ;;
        --all) MODE="all" ; shift ;;
        --help|-h) usage ;;
        *) echo -e "${RED}Unknown option: $1${NC}" >&2; usage ;;
    esac
done

# ── Read Input ──────────────────────────────────────────
TEMP_FILE=$(mktemp)
trap 'rm -f "$TEMP_FILE"' EXIT

if [[ -z "$FILE" || "$FILE" == "-" ]]; then
    cat > "$TEMP_FILE"
elif [[ -f "$FILE" ]]; then
    cat "$FILE" > "$TEMP_FILE"
else
    echo -e "${RED}Error: File '$FILE' not found or not readable.${NC}" >&2
    exit 1
fi

# Check if we got any data
if [[ ! -s "$TEMP_FILE" ]]; then
    echo -e "${YELLOW}No log data to analyze.${NC}" >&2
    exit 0
fi

# ── Section Header ──────────────────────────────────────
header() {
    echo -e "\n${CYAN}══════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}$1${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════${NC}\n"
}

# ── 1. Error Patterns ───────────────────────────────────
analyze_errors() {
    header "Error Pattern Analysis (pattern: $ERROR_PATTERN)"

    # Extract error lines, normalize whitespace, get top 20 messages
    local total_errors
    total_errors=$(grep -ciE "$ERROR_PATTERN" "$TEMP_FILE" 2>/dev/null || echo 0)
    local total_lines
    total_lines=$(wc -l < "$TEMP_FILE")

    echo -e "Total log lines: ${BOLD}$total_lines${NC}"
    echo -e "Lines matching pattern: ${BOLD}$total_errors${NC}"

    if [[ "$total_errors" -eq 0 ]]; then
        echo -e "\n${GREEN}✓ No error patterns detected.${NC}"
        return
    fi

    local pct
    pct=$(echo "scale=1; $total_errors * 100 / $total_lines" | bc 2>/dev/null || echo "0")
    echo -e "Error rate: ${BOLD}${pct}%${NC}"

    echo -e "\n${BOLD}Top Error Messages:${NC}"
    printf "${BOLD}%-5s %-10s %s${NC}\n" "#" "COUNT" "MESSAGE"
    printf "%-5s %-10s %s\n" "-----" "----------" "-------"

    # Extract unique error patterns grouped by common prefix
    grep -ioE "($ERROR_PATTERN)[^.!?]*[.!?]" "$TEMP_FILE" 2>/dev/null \
        | tr '[:upper:]' '[:lower:]' \
        | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' \
        | sort | uniq -c | sort -rn \
        | head -20 \
        | awk '{printf "%-5s %-10s %s\n", NR, $1, substr($0, index($0,$2))}'
}

# ── 2. Time-Based Analysis ──────────────────────────────
analyze_time() {
    header "Time-Based Analysis (last ${TIME_WINDOW}h)"

    # ── Hourly breakdown ──
    echo -e "${BOLD}Errors by Hour (top 24h):${NC}"
    printf "${BOLD}%-15s %-8s %s${NC}\n" "HOUR" "COUNT" "BAR"
    printf "%-15s %-8s %s\n" "---------------" "--------" "---"

    # Extract hours from syslog format (e.g., "May 12 06:59:45") or RFC 5424 (e.g., "2025-05-12T06:59:45")
    local max_count hourly_data
    hourly_data=$(grep -iE "$ERROR_PATTERN" "$TEMP_FILE" 2>/dev/null \
        | sed -n 's/^[A-Za-z]\+  *\([0-9]\+\) \([0-9]\{2\}\):[0-9]\{2\}:[0-9]\{2\}.*/\1-\2/p' \
        | sort | uniq -c | sort -rn -k2,2 | head -24)
    max_count=$(echo "$hourly_data" | awk '{print $1}' | sort -rn | head -1)
    max_count="${max_count:-1}"

    if [[ -z "$hourly_data" ]]; then
        echo -e "${YELLOW}Could not parse time-based data (unexpected log format).${NC}"
    else
        echo "$hourly_data" | while read -r count hour_label; do
            [[ -z "$count" || -z "$hour_label" ]] && continue
            local bar_len=$(( count * 40 / max_count ))
            [[ "$bar_len" -gt 40 ]] && bar_len=40
            [[ "$bar_len" -lt 1 ]] && bar_len=1
            local bar
            bar=$(printf "%${bar_len}s" | tr ' ' '█')
            printf "%-15s %-8s %s\n" "$hour_label" "$count" "$bar"
        done
    fi

    # ── Daily breakdown ──
    echo -e "\n${BOLD}Errors by Day (last 7 days):${NC}"
    printf "${BOLD}%-12s %-8s %s${NC}\n" "DATE" "COUNT" "BAR"
    printf "%-12s %-8s %s\n" "------------" "--------" "---"

    local daily_data
    daily_data=$(grep -iE "$ERROR_PATTERN" "$TEMP_FILE" 2>/dev/null \
        | sed -n 's/^[A-Za-z]\+  *\([0-9]\{1,2\}\) \([0-9]\{2\}\):[0-9]\{2\}:[0-9]\{2\}.*/\1/p' \
        | sort -n | uniq -c | sort -rn -k2,2 | head -7)
    max_count=$(echo "$daily_data" | awk '{print $1}' | sort -rn | head -1)
    max_count="${max_count:-1}"

    if [[ -z "$daily_data" ]]; then
        echo -e "${YELLOW}Could not parse daily data (unexpected log format).${NC}"
    else
        echo "$daily_data" | while read -r count day_label; do
            [[ -z "$count" || -z "$day_label" ]] && continue
            local bar_len=$(( count * 40 / max_count ))
            [[ "$bar_len" -gt 40 ]] && bar_len=40
            [[ "$bar_len" -lt 1 ]] && bar_len=1
            local bar
            bar=$(printf "%${bar_len}s" | tr ' ' '█')
            printf "%-12s %-8s %s\n" "Day $day_label" "$count" "$bar"
        done
    fi
}

# ── 3. IP Frequency ─────────────────────────────────────
analyze_ips() {
    header "IP Frequency Analysis"

    local ip_data
    ip_data=$(grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' "$TEMP_FILE" 2>/dev/null \
        | sort | uniq -c | sort -rn | head -20)

    if [[ -z "$ip_data" ]]; then
        echo -e "${YELLOW}No IP addresses found in the log.${NC}"
        return
    fi

    local total_unique total_all
    total_unique=$(grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' "$TEMP_FILE" 2>/dev/null | sort -u | wc -l)
    total_all=$(grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' "$TEMP_FILE" 2>/dev/null | wc -l)

    echo -e "Total unique IPs: ${BOLD}$total_unique${NC}"
    echo -e "Total IP occurrences: ${BOLD}$total_all${NC}"

    echo -e "\n${BOLD}Top IPs by Frequency:${NC}"
    printf "${BOLD}%-5s %-12s %-10s %s${NC}\n" "#" "IP" "COUNT" "PERCENT"
    printf "%-5s %-12s %-10s %s\n" "-----" "------------" "----------" "-------"

    echo "$ip_data" | while read -r count ip; do
        [[ -z "$count" || -z "$ip" ]] && continue
        local pct
        pct=$(echo "scale=1; $count * 100 / $total_all" | bc 2>/dev/null || echo "0")
        printf "%-5s %-12s %-10s %s%%\n" "$((++i))" "$ip" "$count" "$pct"
    done
}

# ── 4. Spike Detection ──────────────────────────────────
analyze_spikes() {
    header "Spike & Anomaly Detection"

    local spike_data
    spike_data=$(grep -iE "$ERROR_PATTERN" "$TEMP_FILE" 2>/dev/null \
        | sed -n 's/^[A-Za-z]\+  *\([0-9]\+\) \([0-9]\{2\}\):[0-9]\{2\}:[0-9]\{2\}.*/\1-\2/p' \
        | sort | uniq -c | awk '{print $2, $1}')

    if [[ -z "$spike_data" ]]; then
        echo -e "${YELLOW}Cannot detect spikes — insufficient time-parsed data.${NC}"
        return
    fi

    # Calculate average and standard deviation
    local avg std dev count_values
    count_values=$(echo "$spike_data" | awk '{print $2}')
    avg=$(echo "$count_values" | awk '{s+=$1; n++} END {printf "%.1f", s/n}')
    std=$(echo "$count_values" \
        | awk -v avg="$avg" '{sum+=($1-avg)^2} END {printf "%.1f", sqrt(sum/NR)}')

    echo -e "Average errors per time bucket: ${BOLD}$avg${NC}"
    echo -e "Standard deviation: ${BOLD}$std${NC}"
    echo -e "Spike threshold (2x average): ${BOLD}$(echo "$avg * 2" | bc)${NC}"

    local spike_found=0
    echo -e "\n${BOLD}Anomalies Detected:${NC}"
    printf "${BOLD}%-15s %-10s %-15s %s${NC}\n" "BUCKET" "COUNT" "VS AVG" "SEVERITY"
    printf "%-15s %-10s %-15s %s\n" "---------------" "----------" "---------------" "--------"

    echo "$spike_data" | while read -r bucket count; do
        [[ -z "$bucket" || -z "$count" ]] && continue
        local vs_avg
        vs_avg=$(echo "scale=1; $count / $avg" | bc 2>/dev/null || echo "0")

        # Compare with float (using awk for proper comparison)
        if echo "$vs_avg > 2.0" | bc -l | grep -q 1; then
            if echo "$vs_avg > 3.0" | bc -l | grep -q 1; then
                echo -e "  ${RED}⚠ $bucket  ${count}      ${vs_avg}x      CRITICAL${NC}"
            else
                echo -e "  ${YELLOW}⚠ $bucket  ${count}      ${vs_avg}x      WARNING${NC}"
            fi
            spike_found=1
        fi
    done

    if [[ "$spike_found" -eq 0 ]]; then
        echo -e "  ${GREEN}No significant spikes detected.${NC}"
    fi
}

# ── Main ─────────────────────────────────────────────────
main() {
    echo -e "${BOLD}Log Analyzer${NC} — Pattern: \"$ERROR_PATTERN\" | Window: ${TIME_WINDOW}h\n"

    local total_lines
    total_lines=$(wc -l < "$TEMP_FILE")
    echo -e "Input: ${BOLD}$FILE${NC} | ${BOLD}$total_lines${NC} lines\n"

    case "$MODE" in
        errors)
            analyze_errors
            ;;
        time)
            analyze_time
            ;;
        ips)
            analyze_ips
            ;;
        spikes)
            analyze_spikes
            ;;
        all)
            analyze_errors
            analyze_time
            analyze_ips
            analyze_spikes
            ;;
    esac

    echo -e "\n${GREEN}${BOLD}✓ Analysis complete.${NC}\n"
}

main
