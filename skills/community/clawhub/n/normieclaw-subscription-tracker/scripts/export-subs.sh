#!/usr/bin/env bash
set -euo pipefail

# Subscription Tracker — Export Script
# Exports subscription list as CSV, markdown, or Budget Buddy Pro format

ST_DIR="$HOME/.normieclaw/subscription-tracker"
DB_FILE="$ST_DIR/subscriptions.json"
EXPORT_DIR="$ST_DIR/exports"
FORMAT="${1:---format}"
FORMAT_VALUE="${2:-markdown}"
DATE_STAMP=$(date +%Y-%m-%d)

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --format)
      FORMAT_VALUE="${2:-markdown}"
      shift 2
      ;;
    --output|-o)
      CUSTOM_OUTPUT="${2:-}"
      shift 2
      ;;
    --help|-h)
      echo "Usage: export-subs.sh [--format csv|markdown|budget-buddy] [--output path]"
      echo ""
      echo "Formats:"
      echo "  csv           Comma-separated values"
      echo "  markdown      Markdown table (default)"
      echo "  budget-buddy  JSON for Budget Buddy Pro import"
      echo ""
      echo "Output: Saved to ~/.normieclaw/subscription-tracker/exports/"
      exit 0
      ;;
    *)
      shift
      ;;
  esac
done

# Verify database exists
if [[ ! -f "$DB_FILE" ]]; then
  echo "❌ No subscription database found at $DB_FILE"
  echo "   Run setup.sh first, then scan a statement."
  exit 1
fi

mkdir -p "$EXPORT_DIR"

# Check if jq is available
if ! command -v jq &>/dev/null; then
  echo "❌ jq is required for export. Install with: brew install jq (macOS) or apt install jq (Linux)"
  exit 1
fi

# Count active subscriptions
SUB_COUNT=$(jq '.subscriptions | length' "$DB_FILE")
if [[ "$SUB_COUNT" -eq 0 ]]; then
  echo "📭 No active subscriptions to export. Scan a statement first."
  exit 0
fi

case "$FORMAT_VALUE" in
  csv)
    OUTPUT_FILE="${CUSTOM_OUTPUT:-$EXPORT_DIR/$DATE_STAMP-subscriptions.csv}"
    echo "Service,Amount,Frequency,Category,Next Renewal,Payment Method,Status" > "$OUTPUT_FILE"
    jq -r '.subscriptions[] | [.service, .amount, .frequency, .category, .next_renewal, .payment_method, .status] | @csv' "$DB_FILE" >> "$OUTPUT_FILE"
    echo "✅ Exported $SUB_COUNT subscriptions to: $OUTPUT_FILE"
    ;;

  markdown)
    OUTPUT_FILE="${CUSTOM_OUTPUT:-$EXPORT_DIR/$DATE_STAMP-subscriptions.md}"
    {
      echo "# Subscription Report — $DATE_STAMP"
      echo ""
      MONTHLY_TOTAL=$(jq '[.subscriptions[] | select(.status == "active" and .frequency == "monthly") | .amount] | add // 0' "$DB_FILE")
      ANNUAL_SUBS=$(jq '[.subscriptions[] | select(.status == "active" and .frequency == "annual") | .amount] | add // 0' "$DB_FILE")
      ANNUAL_TOTAL=$(echo "$MONTHLY_TOTAL * 12 + $ANNUAL_SUBS" | bc 2>/dev/null || echo "0")
      echo "**Monthly total:** \$$MONTHLY_TOTAL"
      echo "**Annual projected:** \$$ANNUAL_TOTAL"
      echo "**Active subscriptions:** $SUB_COUNT"
      echo ""
      echo "| Service | Amount | Frequency | Category | Next Renewal |"
      echo "|---------|--------|-----------|----------|--------------|"
      jq -r '.subscriptions[] | select(.status == "active") | "| \(.service) | $\(.amount) | \(.frequency) | \(.category) | \(.next_renewal // "—") |"' "$DB_FILE"
      echo ""

      CANCELLED_COUNT=$(jq '.cancelled | length' "$DB_FILE")
      if [[ "$CANCELLED_COUNT" -gt 0 ]]; then
        TOTAL_SAVINGS=$(jq '[.cancelled[].annual_savings] | add // 0' "$DB_FILE")
        echo "## Cancelled Subscriptions"
        echo ""
        echo "**Total annual savings:** \$$TOTAL_SAVINGS"
        echo ""
        jq -r '.cancelled[] | "- ~~\(.service)~~ — $\(.amount)/\(.frequency // "mo") — cancelled \(.cancelled_date) — saving $\(.annual_savings)/yr"' "$DB_FILE"
        echo ""
      fi

      TRIAL_COUNT=$(jq '.trials | length' "$DB_FILE")
      if [[ "$TRIAL_COUNT" -gt 0 ]]; then
        echo "## Active Trials"
        echo ""
        jq -r '.trials[] | select(.status == "active") | "- **\(.service)** — trial ends \(.end_date) — converts to $\(.converts_to_amount)/\(.frequency)"' "$DB_FILE"
      fi
    } > "$OUTPUT_FILE"
    echo "✅ Exported $SUB_COUNT subscriptions to: $OUTPUT_FILE"
    ;;

  budget-buddy)
    OUTPUT_FILE="${CUSTOM_OUTPUT:-$EXPORT_DIR/$DATE_STAMP-budget-buddy-import.json}"
    MONTHLY_TOTAL=$(jq '[.subscriptions[] | select(.status == "active" and .frequency == "monthly") | .amount] | add // 0' "$DB_FILE")
    ANNUAL_SUBS=$(jq '[.subscriptions[] | select(.status == "active" and .frequency == "annual") | .amount] | add // 0' "$DB_FILE")
    ANNUAL_TOTAL=$(echo "$MONTHLY_TOTAL * 12 + $ANNUAL_SUBS" | bc 2>/dev/null || echo "0")

    jq --arg date "$DATE_STAMP" --argjson mt "$MONTHLY_TOTAL" --argjson at "$ANNUAL_TOTAL" '{
      source: "subscription-tracker",
      version: "1.0.0",
      exported_at: ($date + "T00:00:00Z"),
      monthly_recurring: [.subscriptions[] | select(.status == "active") | {
        name: .service,
        amount: .amount,
        category: .category,
        frequency: .frequency,
        next_charge: .next_renewal
      }],
      annual_total: $at,
      monthly_total: $mt
    }' "$DB_FILE" > "$OUTPUT_FILE"
    echo "✅ Exported $SUB_COUNT subscriptions in Budget Buddy format: $OUTPUT_FILE"
    echo "   Import this file into Budget Buddy Pro to sync your subscription data."
    ;;

  *)
    echo "❌ Unknown format: $FORMAT_VALUE"
    echo "   Supported: csv, markdown, budget-buddy"
    exit 1
    ;;
esac
