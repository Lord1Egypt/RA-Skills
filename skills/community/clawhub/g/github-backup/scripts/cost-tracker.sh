#!/bin/bash
# OpenCLAW Cost Tracker (Native) - Simple version
# Usage: cost-tracker.sh [json|report] [24h|today|all]

OUTPUT_MODE="${1:-report}"
PERIOD="${2:-all}"

SESSION_DIR="$HOME/.openclaw/agents/main/sessions"

# Quick count from session files
session_count=$(ls -1 "$SESSION_DIR"/*.jsonl 2>/dev/null | wc -l)

# Rough cost estimate based on session metadata
# Average cost per session ~$0.05
estimated_cost=$(awk "BEGIN {print $session_count * 0.05}")

if [ "$OUTPUT_MODE" = "json" ]; then
    printf '{"period":"%s","summary":{"totalMessages":%d,"totalTokens":%d,"totalCostUSD":%.4f}}\n' \
        "$PERIOD" "$session_count" "0" "$estimated_cost"
else
    echo "💰 OpenCLAW Cost Report"
    echo "Period: $PERIOD"
    echo "Sessions: $session_count"
    printf "Estimated total cost: \$%.4f\n" "$estimated_cost"
fi
