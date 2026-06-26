#!/usr/bin/env bash
set -euo pipefail

# Freelancer Toolkit — Export Timesheet as CSV
# Usage: export-timesheet.sh --start YYYY-MM-DD --end YYYY-MM-DD [--client "Client Name"]
# Output: ~/.freelancer-toolkit/exports/timesheet-YYYY-MM-DD.csv

DATA_DIR="$HOME/.freelancer-toolkit"
ENTRIES_FILE="$DATA_DIR/time-entries.json"
CLIENTS_FILE="$DATA_DIR/clients.json"
PROJECTS_FILE="$DATA_DIR/projects.json"
EXPORT_DIR="$DATA_DIR/exports"

START_DATE=""
END_DATE=""
CLIENT_FILTER=""

usage() {
    echo "Usage: export-timesheet.sh --start YYYY-MM-DD --end YYYY-MM-DD [--client \"Client Name\"]"
    echo ""
    echo "Options:"
    echo "  --start    Start date (inclusive)"
    echo "  --end      End date (inclusive)"
    echo "  --client   Filter by client name (optional, partial match)"
    echo ""
    echo "Examples:"
    echo "  export-timesheet.sh --start 2026-03-01 --end 2026-03-31"
    echo "  export-timesheet.sh --start 2026-03-01 --end 2026-03-31 --client \"Acme\""
    exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --start) START_DATE="$2"; shift 2 ;;
        --end) END_DATE="$2"; shift 2 ;;
        --client) CLIENT_FILTER="$2"; shift 2 ;;
        -h|--help) usage ;;
        *) echo "Unknown option: $1"; usage ;;
    esac
done

if [[ -z "$START_DATE" || -z "$END_DATE" ]]; then
    echo "❌ --start and --end are required."
    usage
fi

# Validate data files
if [[ ! -f "$ENTRIES_FILE" ]]; then
    echo "❌ No time entries found at $ENTRIES_FILE"
    echo "   Run setup.sh first."
    exit 1
fi

mkdir -p "$EXPORT_DIR"

OUTPUT_FILE="$EXPORT_DIR/timesheet-$(date +%Y-%m-%d-%H%M%S).csv"

# Build the CSV using jq
# Join entries with client names and project names
echo "date,client,project,hours,description,category,billable,rate,amount" > "$OUTPUT_FILE"

jq -r --arg start "$START_DATE" --arg end "$END_DATE" --arg client_filter "$CLIENT_FILTER" '
    # Load lookup data
    (input | map({(.id): .name}) | add // {}) as $clients |
    (input | map({(.id): {name: .name, rate: .hourly_rate}}) | add // {}) as $projects |
    
    # Filter and format entries
    map(
        select(.date >= $start and .date <= $end) |
        if $client_filter != "" then
            select(($clients[.client_id] // "Unknown") | ascii_downcase | contains($client_filter | ascii_downcase))
        else . end
    ) |
    sort_by(.date) |
    .[] |
    [
        .date,
        ($clients[.client_id] // "Unknown"),
        ($projects[.project_id] // {name: "General"}).name,
        (.hours | tostring),
        (.description // "" | gsub(","; ";")),
        (.category // ""),
        (if .billable then "yes" else "no" end),
        (($projects[.project_id] // {rate: 0}).rate | tostring),
        (if .billable then (.hours * (($projects[.project_id] // {rate: 0}).rate)) else 0 end | tostring)
    ] | @csv
' "$ENTRIES_FILE" "$CLIENTS_FILE" "$PROJECTS_FILE" >> "$OUTPUT_FILE"

LINE_COUNT=$(tail -n +2 "$OUTPUT_FILE" | wc -l | tr -d ' ')
TOTAL_HOURS=$(tail -n +2 "$OUTPUT_FILE" | awk -F',' '{sum += $4} END {printf "%.2f", sum}')

echo "✅ Exported $LINE_COUNT entries to: $OUTPUT_FILE"
echo "   Period: $START_DATE to $END_DATE"
if [[ -n "$CLIENT_FILTER" ]]; then
    echo "   Client filter: $CLIENT_FILTER"
fi
echo "   Total hours: $TOTAL_HOURS"
