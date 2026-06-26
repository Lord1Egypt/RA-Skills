#!/bin/bash
# Expiry Arbitrage Scanner
# Finds monotonicity violations in same-event different-expiry markets
# Usage: ./expiry-arb.sh "US strikes Iran" [threshold_cents]
#
# If P(earlier_expiry) > P(later_expiry), that's free money.

source "$HOME/.cargo/env" 2>/dev/null

QUERY="${1:-US strikes Iran}"
THRESHOLD="${2:-0.5}"  # minimum spread in cents to flag

echo "🔍 Scanning: \"$QUERY\""
echo "   Threshold: ${THRESHOLD}¢"
echo ""

polymarket -o json markets search "$QUERY" --limit 200 2>/dev/null
