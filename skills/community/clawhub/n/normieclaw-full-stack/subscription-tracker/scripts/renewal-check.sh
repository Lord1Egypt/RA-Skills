#!/usr/bin/env bash
set -euo pipefail

# Subscription Tracker — Renewal Check
# Shows upcoming renewals within N days

ST_DIR="$HOME/.normieclaw/subscription-tracker"
DB_FILE="$ST_DIR/subscriptions.json"
DAYS="${1:-7}"

# Help
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  echo "Usage: renewal-check.sh [days]"
  echo ""
  echo "Check for subscription renewals within the next N days (default: 7)."
  echo ""
  echo "Examples:"
  echo "  renewal-check.sh        # Next 7 days"
  echo "  renewal-check.sh 3      # Next 3 days"
  echo "  renewal-check.sh 30     # Next 30 days"
  exit 0
fi

# Verify database
if [[ ! -f "$DB_FILE" ]]; then
  echo "❌ No subscription database found at $DB_FILE"
  echo "   Run setup.sh first, then scan a statement."
  exit 1
fi

# Check jq
if ! command -v jq &>/dev/null; then
  echo "❌ jq is required. Install with: brew install jq (macOS) or apt install jq (Linux)"
  exit 1
fi

# Get today and target date
TODAY=$(date +%Y-%m-%d)

# macOS and GNU date handle differently
if date -v+1d &>/dev/null 2>&1; then
  # macOS
  TARGET=$(date -v+"${DAYS}d" +%Y-%m-%d)
else
  # GNU/Linux
  TARGET=$(date -d "+${DAYS} days" +%Y-%m-%d)
fi

echo "📅 Upcoming Renewals — Next $DAYS Days ($TODAY → $TARGET)"
echo ""

# Find renewals in range
RENEWALS=$(jq -r --arg today "$TODAY" --arg target "$TARGET" '
  .subscriptions[]
  | select(.status == "active" and .next_renewal != null)
  | select(.next_renewal >= $today and .next_renewal <= $target)
  | "\(.next_renewal)|\(.service)|\(.amount)|\(.payment_method // "—")"
' "$DB_FILE" | sort)

if [[ -z "$RENEWALS" ]]; then
  echo "  ✅ No renewals in the next $DAYS days. You're clear!"
  exit 0
fi

TOTAL=0
COUNT=0

while IFS='|' read -r date service amount payment; do
  printf "  %s — %-30s \$%-8s (%s)\n" "$date" "$service" "$amount" "$payment"
  TOTAL=$(echo "$TOTAL + $amount" | bc 2>/dev/null || echo "$TOTAL")
  COUNT=$((COUNT + 1))
done <<< "$RENEWALS"

echo ""
echo "  📊 $COUNT renewals totaling \$$TOTAL"

# Also check trials expiring in range
TRIALS=$(jq -r --arg today "$TODAY" --arg target "$TARGET" '
  .trials[]
  | select(.status == "active")
  | select(.end_date >= $today and .end_date <= $target)
  | "\(.end_date)|\(.service)|\(.converts_to_amount)"
' "$DB_FILE" 2>/dev/null | sort)

if [[ -n "$TRIALS" ]]; then
  echo ""
  echo "⚠️  Free Trials Expiring:"
  echo ""
  while IFS='|' read -r date service amount; do
    echo "  🔔 $date — $service trial ends (converts to \$$amount/mo)"
  done <<< "$TRIALS"
fi
