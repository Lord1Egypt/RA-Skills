import urllib.request
import urllib.error
import json
import time
from datetime import datetime

webhook = "https://discord.com/api/webhooks/1483478506070474922/ReIZsU3KTpXqNseTWFBNsuPJ-FbYgqEuCTELtMHRWw4ND8vVjMUr36b6LyusiOoJn66d"

# Exact copy from orchestrator
header = {
    "content": "🧠 **Polymarket-Brain Analysis**\n"
               "📊 **5 Markets Analyzed** | Mode: PROD\n"
               f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n"
               "━" * 50
}

print(f"Header content length: {len(header['content'])}")
print(f"Header: {repr(header['content'][:100])}")

req = urllib.request.Request(
    webhook,
    data=json.dumps(header).encode('utf-8'),
    headers={
        "Content-Type": "application/json",
        "User-Agent": "Polymarket-Brain/1.0"
    },
    method="POST"
)

print("Sending header...")
try:
    resp = urllib.request.urlopen(req)
    print(f"Status: {resp.status}")
except urllib.error.HTTPError as e:
    print(f"Error: {e.code} {e.reason}")
    print(f"Response: {e.read().decode()}")
