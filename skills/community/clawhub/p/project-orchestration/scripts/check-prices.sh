#!/usr/bin/env bash
# check-prices.sh — Check cloud model prices from provider sites
# Usage: bash scripts/check-prices.sh [--report] [--providers openrouter,opencode]
#
# Probes provider pricing pages and logs changes.
# Data stored in $ORCHESTRATOR_DATA_DIR (default: ../../orchestrator-data/ from skill root)
#
# --report    Print prices without logging
# --providers Comma-separated list of providers to check (default: all known)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${ORCHESTRATOR_DATA_DIR:-$(dirname "$(dirname "$SKILL_DIR")")/orchestrator-data}"
LOG_FILE="$DATA_DIR/price_changes.log"
MODELS_FILE="$DATA_DIR/models.json"

REPORT_MODE=false
PROVIDER_FILTER=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --report) REPORT_MODE=true; shift ;;
        --providers) PROVIDER_FILTER="$2"; shift 2 ;;
        *) echo "Usage: $0 [--report] [--providers openrouter,opencode,cursor]"; exit 1 ;;
    esac
done

echo "━━━ Price Check — $(date '+%Y-%m-%d %H:%M') ━━━"

if [ ! -f "$MODELS_FILE" ]; then
    echo "No models.json — run onboarding first"
    exit 1
fi

# Extract unique providers from models.json
KNOWN_PROVIDERS=$(grep -o '"provider"[[:space:]]*:[[:space:]]*"[^"]*"' "$MODELS_FILE" 2>/dev/null | sed 's/"provider"://;s/"//g;s/ //g' | sort -u || echo "")

if [ -z "$KNOWN_PROVIDERS" ]; then
    echo "No providers found in models.json"
    echo "Using default provider list"
    KNOWN_PROVIDERS="openrouter opencode cursor"
fi

# Apply filter if specified
if [ -n "$PROVIDER_FILTER" ]; then
    FILTERED=""
    IFS=',' read -ra FILTER_LIST <<< "$PROVIDER_FILTER"
    for f in "${FILTER_LIST[@]}"; do
        if echo "$KNOWN_PROVIDERS" | grep -qi "$f"; then
            FILTERED="$FILTERED $f"
        fi
    done
    KNOWN_PROVIDERS="$FILTERED"
fi

fetch_page() {
    local url="$1" label="$2"
    echo "  $label..."
    local result
    result=$(curl -sL --max-time 15 "$url" 2>/dev/null || echo "FETCH_FAILED")
    if [ "$result" = "FETCH_FAILED" ]; then
        echo "    ❌ Failed to fetch"
        return 1
    fi
    # Extract pricing info: look for $ signs and numbers near them
    local prices
    prices=$(echo "$result" | grep -oiP '\$\d+\.?\d*[^.]{0,40}(per|/|million|token|month|input|output)' 2>/dev/null | head -5 || true)
    if [ -n "$prices" ]; then
        echo "$prices" | sed 's/^/    /'
    else
        echo "    ℹ️  Page fetched but no pricing pattern detected"
        echo "       (pricing may be JS-rendered or behind login)"
    fi
}

echo ""
echo "Checking provider pricing pages..."
echo ""

# Provider pricing URLs (well-known, not model-specific)
fetch_page "https://openrouter.ai/pricing" "OpenRouter"
fetch_page "https://opencode.ai/pricing" "OpenCode"
fetch_page "https://cursor.com/pricing" "Cursor"

echo ""
echo "━━━ Complete ━━━"

if $REPORT_MODE; then
    echo "Report mode: no changes saved"
else
    # Log the check
    mkdir -p "$DATA_DIR"
    if [ ! -f "$LOG_FILE" ]; then
        echo "# Price Change Log" > "$LOG_FILE"
        echo "# Created $(date '+%Y-%m-%d')" >> "$LOG_FILE"
    fi
    echo "$(date '+%Y-%m-%d %H:%M'): Price check completed" >> "$LOG_FILE"
    echo "Logged to $LOG_FILE"
fi