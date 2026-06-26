#!/bin/bash
# price.sh — Get real-time crypto prices from CoinGecko (free, no API key)
# Usage: bash price.sh BTC ETH SOL [--json]
# Compatible with macOS bash 3.2+

set -uo pipefail

JSON_MODE=false
TOKENS=""

for arg in "$@"; do
    if [ "$arg" = "--json" ]; then
        JSON_MODE=true
    else
        TOKENS="$TOKENS $arg"
    fi
done

TOKENS=$(echo "$TOKENS" | xargs)

if [ -z "$TOKENS" ]; then
    echo "Usage: bash price.sh BTC ETH SOL [--json]"
    exit 1
fi

# Use python for symbol→gecko mapping and output
python3 << PYEOF
import json, sys, urllib.request

GECKO_MAP = {
    'BTC': 'bitcoin', 'ETH': 'ethereum', 'SOL': 'solana',
    'MATIC': 'matic-network', 'AVAX': 'avalanche-2', 'ARB': 'arbitrum',
    'OP': 'optimism', 'USDC': 'usd-coin', 'USDT': 'tether', 'DAI': 'dai',
    'LINK': 'chainlink', 'UNI': 'uniswap', 'AAVE': 'aave', 'DOT': 'polkadot',
    'ADA': 'cardano', 'DOGE': 'dogecoin', 'SHIB': 'shiba-inu', 'ATOM': 'cosmos',
    'NEAR': 'near', 'FTM': 'fantom', 'PEPE': 'pepe', 'WIF': 'dogwifcoin',
    'RENDER': 'render-token', 'FET': 'fetch-ai', 'TAO': 'bittensor',
    'VIRTUAL': 'virtual-protocol', 'ONDO': 'ondo-finance',
}

tokens = "$TOKENS".upper().split()
ids = []
token_to_gecko = {}
for t in tokens:
    gid = GECKO_MAP.get(t, t.lower())
    ids.append(gid)
    token_to_gecko[t] = gid

url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(ids)}&vs_currencies=usd&include_24hr_change=true"

try:
    req = urllib.request.Request(url, headers={'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
except Exception as e:
    print(f"❌ Failed to fetch prices: {e}")
    sys.exit(1)

json_mode = $( [ "$JSON_MODE" = true ] && echo "True" || echo "False" )

if json_mode:
    print(json.dumps(data, indent=2))
    sys.exit(0)

from datetime import datetime
print(f"💰 Crypto Prices — {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}")
print("=" * 40)

for t in tokens:
    gid = token_to_gecko[t]
    info = data.get(gid, {})
    price = info.get('usd', 0)
    change = info.get('usd_24h_change', 0)
    
    if not price:
        print(f"⚪ {t:>6}: not found")
        continue
    
    arrow = '🟢' if change >= 0 else '🔴'
    if price >= 1:
        print(f"{arrow} {t:>6}: \${price:>12,.2f}  ({change:+.2f}%)")
    else:
        print(f"{arrow} {t:>6}: \${price:>12,.6f}  ({change:+.2f}%)")
PYEOF
