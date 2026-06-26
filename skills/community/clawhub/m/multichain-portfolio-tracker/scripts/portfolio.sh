#!/bin/bash
# portfolio.sh — Full portfolio scan across all configured wallets
# Usage: bash portfolio.sh [--json] [config_path]

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
JSON_MODE=false
CONFIG=""

for arg in "$@"; do
    case "$arg" in
        --json) JSON_MODE=true ;;
        *) CONFIG="$arg" ;;
    esac
done

# Find config
if [ -z "$CONFIG" ]; then
    for p in "./portfolio.json" "$HOME/clawd/portfolio.json" "$HOME/.openclaw/portfolio.json"; do
        if [ -f "$p" ]; then CONFIG="$p"; break; fi
    done
fi

if [ -z "$CONFIG" ] || [ ! -f "$CONFIG" ]; then
    echo "❌ No portfolio.json found. Create one with your wallet addresses."
    echo "   See SKILL.md for format."
    exit 1
fi

TOTAL=0
RESULTS="[]"
DATE=$(date '+%Y-%m-%d %H:%M %Z')

echo "📊 Portfolio — $DATE"
echo "================================"

# Get prices for native tokens
PRICES=$(curl -s "https://api.coingecko.com/api/v3/simple/price?ids=ethereum,solana,matic-network&vs_currencies=usd" 2>/dev/null)
ETH_PRICE=$(echo "$PRICES" | python3 -c "import sys,json; print(json.load(sys.stdin).get('ethereum',{}).get('usd',0))" 2>/dev/null)
SOL_PRICE=$(echo "$PRICES" | python3 -c "import sys,json; print(json.load(sys.stdin).get('solana',{}).get('usd',0))" 2>/dev/null)
MATIC_PRICE=$(echo "$PRICES" | python3 -c "import sys,json; print(json.load(sys.stdin).get('matic-network',{}).get('usd',0))" 2>/dev/null)

# Scan each wallet
python3 -c "
import json, sys

with open('$CONFIG') as f:
    config = json.load(f)

wallets = config.get('wallets', [])
for w in wallets:
    print(json.dumps(w))
" 2>/dev/null | while read -r WALLET_JSON; do
    ADDRESS=$(echo "$WALLET_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['address'])")
    CHAIN=$(echo "$WALLET_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['chain'])")
    LABEL=$(echo "$WALLET_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('label',''))")
    
    # Get balance
    BALANCE_JSON=$(bash "$SCRIPT_DIR/check-wallet.sh" "$ADDRESS" "$CHAIN" --json 2>/dev/null)
    BALANCE=$(echo "$BALANCE_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('balance',0))" 2>/dev/null)
    SYMBOL=$(echo "$BALANCE_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin).get('symbol','?'))" 2>/dev/null)
    
    # Calculate USD value
    case "$SYMBOL" in
        ETH) USD_VALUE=$(python3 -c "print(round($BALANCE * $ETH_PRICE, 2))") ;;
        SOL) USD_VALUE=$(python3 -c "print(round($BALANCE * $SOL_PRICE, 2))") ;;
        MATIC) USD_VALUE=$(python3 -c "print(round($BALANCE * $MATIC_PRICE, 2))") ;;
        *) USD_VALUE="0.00" ;;
    esac
    
    if [ -n "$LABEL" ]; then
        echo ""
        echo "📁 $LABEL ($CHAIN)"
    else
        echo ""
        echo "📁 ${ADDRESS:0:6}...${ADDRESS: -4} ($CHAIN)"
    fi
    echo "   $BALANCE $SYMBOL ≈ \$$USD_VALUE"
done

# Manual entries
python3 -c "
import json
with open('$CONFIG') as f:
    config = json.load(f)
manual = config.get('manual', [])
if manual:
    print('MANUAL_ENTRIES')
    for m in manual:
        print(json.dumps(m))
" 2>/dev/null | while read -r line; do
    if [ "$line" = "MANUAL_ENTRIES" ]; then
        echo ""
        echo "📝 Manual Entries"
        continue
    fi
    TOKEN=$(echo "$line" | python3 -c "import sys,json; print(json.load(sys.stdin).get('token','?'))")
    AMOUNT=$(echo "$line" | python3 -c "import sys,json; print(json.load(sys.stdin).get('amount',0))")
    COST=$(echo "$line" | python3 -c "import sys,json; print(json.load(sys.stdin).get('cost_basis',0))")
    echo "   $AMOUNT $TOKEN (cost basis: \$$COST)"
done

echo ""
echo "================================"
echo "⏰ Updated: $DATE"
