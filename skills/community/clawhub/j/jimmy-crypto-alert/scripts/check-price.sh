#!/bin/bash
# Crypto Alert Monitor - Check price for token(s)
# Uses Binance public API (no key required)
# Usage: bash check-price.sh BTC ETH SOL

BINANCE_API="https://api.binance.com/api/v3"

check_token() {
    local symbol=$1
    # Map common symbols to Binance symbols
    case "$symbol" in
        btc|BTC) symbol="BTCUSDT" ;;
        eth|ETH) symbol="ETHUSDT" ;;
        sol|SOL) symbol="SOLUSDT" ;;
        ada|ADA) symbol="ADAUSDT" ;;
        dot|DOT) symbol="DOTUSDT" ;;
        matic|MATIC) symbol="MATICUSDT" ;;
        arb|ARB) symbol="ARBUSDT" ;;
        op|OP) symbol="OPUSDT" ;;
        base|BASE) symbol="BASEUSDT" ;;
        onto|ONTO) symbol="ONTOUSDT" ;;
        cake|CAKE) symbol="CAKEUSDT" ;;
        virtual|VIRTUAL) symbol="VIRTUALUSDT" ;;
        nerf|NERF) symbol="NERFUSDT" ;;
    esac
    
    local data=$(curl -s --max-time 10 "$BINANCE_API/ticker/price?symbol=$symbol")
    
    if echo "$data" | grep -q "price"; then
        local price=$(echo "$data" | python3 -c "import sys,json; d=json.load(sys.stdin); print(float(d['price']))")
        echo "🪙 $symbol: \$$price"
    else
        echo "❌ $symbol: not found"
    fi
}

if [ -z "$1" ]; then
    echo "Usage: bash check-price.sh <symbol> [symbol2] ..."
    echo "Examples: bash check-price.sh BTC ETH SOL"
    exit 1
fi

for symbol in "$@"; do
    check_token "$symbol"
done
