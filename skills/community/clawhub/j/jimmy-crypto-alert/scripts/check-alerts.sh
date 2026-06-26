#!/bin/bash
# Check all active alerts

STATE_FILE="$HOME/.crypto-alert-state.json"
COINGECKO_API="https://api.coingecko.com/api/v3"

if [ ! -f "$STATE_FILE" ]; then
    echo "No alerts configured. Use set-alert.sh first."
    exit 0
fi

python3 << 'PYEOF'
import json, urllib.request, os

STATE_FILE = os.path.expanduser("~/.crypto-alert-state.json")
COINGECKO_API = "https://api.coingecko.com/api/v3"

with open(STATE_FILE) as f:
    state = json.load(f)

alerts = state.get("alerts", [])
active = [a for a in alerts if a.get("active")]

print(f"📊 Active alerts: {len(active)}")
print()

if not active:
    print("No active alerts.")
    exit(0)

# Get unique tokens
tokens = list(set(a["token"] for a in active))
ids = ",".join(tokens)

try:
    url = f"{COINGECKO_API}/simple/price?ids={ids}&vs_currencies=usd"
    with urllib.request.urlopen(url, timeout=10) as r:
        prices = json.loads(r.read())
except Exception as e:
    print(f"⚠️ Failed to fetch prices: {e}")
    exit(1)

for alert in active:
    token = alert["token"]
    threshold = alert["threshold"]
    msg = alert["message"]
    
    if token in prices:
        price = prices[token]["usd"]
        status = "🔔" if price >= threshold else "✅"
        print(f"{status} {msg}: ${price:,.2f} (threshold: ${threshold:,})")
    else:
        print(f"⚠️ {msg}: price data unavailable")
PYEOF
