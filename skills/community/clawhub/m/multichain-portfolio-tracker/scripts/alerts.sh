#!/bin/bash
# alerts.sh — Check price alerts from portfolio.json
# Usage: bash alerts.sh [config_path]
# Exit 0 = no alerts triggered, Exit 1 = alerts triggered

set -uo pipefail

CONFIG="${1:-}"
if [ -z "$CONFIG" ]; then
    for p in "./portfolio.json" "$HOME/clawd/portfolio.json" "$HOME/.openclaw/portfolio.json"; do
        if [ -f "$p" ]; then CONFIG="$p"; break; fi
    done
fi

if [ -z "$CONFIG" ] || [ ! -f "$CONFIG" ]; then
    echo "No portfolio.json found"
    exit 0
fi

# Extract alert tokens
ALERT_TOKENS=$(python3 -c "
import json
with open('$CONFIG') as f:
    config = json.load(f)
alerts = config.get('alerts', [])
tokens = set()
for a in alerts:
    tokens.add(a['token'].upper())
print(','.join(tokens))
" 2>/dev/null)

if [ -z "$ALERT_TOKENS" ]; then
    echo "No alerts configured"
    exit 0
fi

# Get script directory for price.sh
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Fetch prices
PRICES_JSON=$(bash "$SCRIPT_DIR/price.sh" $ALERT_TOKENS --json 2>/dev/null)
TRIGGERED=0

python3 -c "
import json, sys

with open('$CONFIG') as f:
    config = json.load(f)

prices_raw = '''$PRICES_JSON'''
try:
    prices = json.loads(prices_raw)
except:
    prices = {}

# Map symbols to gecko IDs (simplified)
GECKO = {
    'BTC': 'bitcoin', 'ETH': 'ethereum', 'SOL': 'solana',
    'MATIC': 'matic-network', 'AVAX': 'avalanche-2',
    'LINK': 'chainlink', 'UNI': 'uniswap', 'AAVE': 'aave',
    'DOT': 'polkadot', 'ADA': 'cardano', 'DOGE': 'dogecoin',
    'NEAR': 'near', 'ARB': 'arbitrum', 'OP': 'optimism',
}

triggered = 0
for alert in config.get('alerts', []):
    token = alert['token'].upper()
    gecko_id = GECKO.get(token, token.lower())
    price_data = prices.get(gecko_id, {})
    current = price_data.get('usd', 0)
    
    if not current:
        continue
    
    msg = alert.get('message', f'{token} alert triggered')
    
    if 'above' in alert and current >= alert['above']:
        print(f'🚨 {msg} (current: \${current:,.2f}, threshold: \${alert[\"above\"]:,.2f})')
        triggered += 1
    
    if 'below' in alert and current <= alert['below']:
        print(f'🚨 {msg} (current: \${current:,.2f}, threshold: \${alert[\"below\"]:,.2f})')
        triggered += 1

if triggered == 0:
    print('✅ No alerts triggered')
    sys.exit(0)
else:
    sys.exit(1)
" 2>/dev/null

exit $?
