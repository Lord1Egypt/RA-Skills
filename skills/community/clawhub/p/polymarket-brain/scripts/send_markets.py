"""Send Polymarket markets to Discord one-by-one"""
import requests
import json
from pathlib import Path

# Load config
config_path = Path(__file__).parent.parent / "references" / "config.md"
webhook_url = None
for line in config_path.read_text().splitlines():
    if "discord.com" in line:
        webhook_url = line.strip()
        break

if not webhook_url:
    print("ERROR: No webhook URL found in config.md")
    exit(1)

# Sample markets (in production, these come from polymarket-analyst output)
markets = [
    {"title": "Fed Rate Decision", "odds": 51.0, "expert": 45, "rec": "HOLD", "url": "https://polymarket.com/market/fed"},
    {"title": "Inflation >3%", "odds": 36.5, "expert": 50, "rec": "BUY", "url": "https://polymarket.com/market/inflation"},
    {"title": "Treasury Yield", "odds": 58.5, "expert": 55, "rec": "HOLD", "url": "https://polymarket.com/market/treasury"},
    {"title": "Stagflation Risk", "odds": 52.5, "expert": 40, "rec": "SELL", "url": "https://polymarket.com/market/stagflation"},
    {"title": "Oil Price", "odds": 39.5, "expert": 60, "rec": "BUY", "url": "https://polymarket.com/market/oil"},
]

print(f"Sending {len(markets)} markets to Discord...")
print(f"Webhook: {webhook_url[:50]}...")

for i, market in enumerate(markets, 1):
    emoji = "✅" if market["rec"] == "BUY" else "❌" if market["rec"] == "SELL" else "⚠️"
    gap = abs(market["odds"] - market["expert"])
    rec_text = f"{emoji} **{market['rec']}** ({gap:.1f}% gap)"
    
    content = f"""**Polymarket Brain Analysis**
{emoji} **{market['title']}**
Odds: {market['odds']}% | Expert Prob: {market['expert']}%
{rec_text}
{market['url']}
"""
    
    response = requests.post(webhook_url, json={"content": content})
    if response.status_code == 204:
        print(f"[{i}/{len(markets)}] Sent: {market['title']}")
    else:
        print(f"[{i}/{len(markets)}] FAILED: {response.status_code}")

print(f"\n✅ Done! Sent {len(markets)} markets one-by-one.")
