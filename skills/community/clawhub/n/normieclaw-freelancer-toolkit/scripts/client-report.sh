#!/usr/bin/env bash
set -euo pipefail

# Freelancer Toolkit — Client Billing Summary Report
# Usage: client-report.sh --client "Client Name" [--start YYYY-MM-DD] [--end YYYY-MM-DD]
# Generates a markdown billing summary for a specific client.

DATA_DIR="$HOME/.freelancer-toolkit"
ENTRIES_FILE="$DATA_DIR/time-entries.json"
CLIENTS_FILE="$DATA_DIR/clients.json"
PROJECTS_FILE="$DATA_DIR/projects.json"
SETTINGS_FILE="$DATA_DIR/settings.json"
EXPORT_DIR="$DATA_DIR/exports"

CLIENT_FILTER=""
START_DATE=""
END_DATE=""

usage() {
    echo "Usage: client-report.sh --client \"Client Name\" [--start YYYY-MM-DD] [--end YYYY-MM-DD]"
    echo ""
    echo "Options:"
    echo "  --client   Client name (required, partial match)"
    echo "  --start    Start date (default: first of current month)"
    echo "  --end      End date (default: today)"
    echo ""
    echo "Examples:"
    echo "  client-report.sh --client \"Acme\""
    echo "  client-report.sh --client \"Acme\" --start 2026-03-01 --end 2026-03-31"
    exit 1
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --client) CLIENT_FILTER="$2"; shift 2 ;;
        --start) START_DATE="$2"; shift 2 ;;
        --end) END_DATE="$2"; shift 2 ;;
        -h|--help) usage ;;
        *) echo "Unknown option: $1"; usage ;;
    esac
done

if [[ -z "$CLIENT_FILTER" ]]; then
    echo "❌ --client is required."
    usage
fi

# Default date range: current month
if [[ -z "$START_DATE" ]]; then
    START_DATE=$(date +%Y-%m-01)
fi
if [[ -z "$END_DATE" ]]; then
    END_DATE=$(date +%Y-%m-%d)
fi

if [[ ! -f "$ENTRIES_FILE" || ! -f "$CLIENTS_FILE" || ! -f "$PROJECTS_FILE" ]]; then
    echo "❌ Data files not found. Run setup.sh first."
    exit 1
fi

mkdir -p "$EXPORT_DIR"

CURRENCY_SYMBOL=$(jq -r '.currency_symbol // "$"' "$SETTINGS_FILE" 2>/dev/null || echo '$')

# Generate the report
REPORT=$(jq -r --arg start "$START_DATE" --arg end "$END_DATE" \
    --arg client_filter "$CLIENT_FILTER" --arg cs "$CURRENCY_SYMBOL" '
    # Find matching client
    (input | map(select(.name | ascii_downcase | contains($client_filter | ascii_downcase)))) as $matched_clients |
    (input) as $projects |
    
    if ($matched_clients | length) == 0 then
        "❌ No client found matching: \($client_filter)"
    else
        $matched_clients[0] as $client |
        ($projects | map(select(.client_id == $client.id))) as $client_projects |
        
        # Filter entries for this client and date range
        map(select(
            .client_id == $client.id and
            .date >= $start and
            .date <= $end
        )) as $entries |
        
        ($entries | map(select(.billable)) | map(.hours) | add // 0) as $billable_hours |
        ($entries | map(select(.billable | not)) | map(.hours) | add // 0) as $nonbillable_hours |
        ($entries | map(.hours) | add // 0) as $total_hours |
        
        # Group by project
        ($entries | group_by(.project_id) | map({
            project_id: .[0].project_id,
            hours: (map(.hours) | add),
            entries: .
        })) as $by_project |
        
        "# Billing Summary: \($client.name)\n" +
        "**Company:** \($client.company // "—")\n" +
        "**Contact:** \($client.email // "—")\n" +
        "**Default Rate:** \($cs)\($client.default_rate // 0)/hr\n" +
        "**Payment Terms:** \($client.payment_terms // "—")\n" +
        "**Period:** \($start) to \($end)\n\n" +
        "---\n\n" +
        "## Hours Summary\n\n" +
        "- **Total hours:** \($total_hours)\n" +
        "- **Billable:** \($billable_hours) hrs\n" +
        "- **Non-billable:** \($nonbillable_hours) hrs\n\n" +
        "## By Project\n\n" +
        ($by_project | map(
            ($projects | map(select(.id == .project_id)) | .[0] // {name: "General", hourly_rate: ($client.default_rate // 0)}) as $proj |
            "### \($proj.name)\n" +
            "- Hours: \(.hours)\n" +
            "- Rate: \($cs)\($proj.hourly_rate // $client.default_rate // 0)/hr\n" +
            "- Amount: \($cs)\(.hours * ($proj.hourly_rate // $client.default_rate // 0))\n" +
            (if $proj.billing_type == "fixed" then
                "- Quoted: \($cs)\($proj.quoted_price // 0) | Budget used: \((($proj.hours_logged // 0) / ($proj.estimated_hours // 1) * 100) | floor)%\n"
            else "" end) +
            "\n**Entries:**\n" +
            (.entries | sort_by(.date) | map(
                "- \(.date) — \(.hours) hrs — \(.description // "(no description)")"
            ) | join("\n")) +
            "\n"
        ) | join("\n")) +
        "\n---\n\n" +
        "## Totals\n\n" +
        "- **Billable amount:** \($cs)\($billable_hours * ($client.default_rate // 0))\n" +
        "- **Outstanding (all time):** \($cs)\(($client.total_billed // 0) - ($client.total_paid // 0))\n" +
        "\n*Generated: \(now | strftime("%Y-%m-%d %H:%M UTC"))*\n"
    end
' "$ENTRIES_FILE" "$CLIENTS_FILE" "$PROJECTS_FILE")

# Save report
SAFE_NAME=$(echo "$CLIENT_FILTER" | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
REPORT_FILE="$EXPORT_DIR/client-report-${SAFE_NAME}-$(date +%Y-%m-%d).md"
echo "$REPORT" > "$REPORT_FILE"

echo "$REPORT"
echo ""
echo "📄 Report saved to: $REPORT_FILE"
