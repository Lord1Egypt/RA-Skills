import urllib.request
import urllib.error
import json
import time

webhook = "https://discord.com/api/webhooks/1483478506070474922/ReIZsU3KTpXqNseTWFBNsuPJ-FbYgqEuCTELtMHRWw4ND8vVjMUr36b6LyusiOoJn66d"

# Test short message
short_msg = {"content": "Short test"}
req = urllib.request.Request(
    webhook,
    data=json.dumps(short_msg).encode(),
    headers={
        "Content-Type": "application/json",
        "User-Agent": "Polymarket-Brain/1.0"
    },
    method="POST"
)

print("Short message...")
try:
    resp = urllib.request.urlopen(req)
    print(f"Status: {resp.status}")
except urllib.error.HTTPError as e:
    print(f"Error: {e.code} {e.reason} - {e.read()}")

time.sleep(1.2)

# Test long message (like orchestrator)
long_msg = {
    "content": "🧠 **Polymarket-Brain Analysis: Market 1/5**\n\n"
               "**📰 Will Iranian regime fall by June 30?**\n\n"
               "📅 **Resolution Date:** June 30, 2026\n"
               "📊 **Market Odds:** 28% Yes\n"
               "🎯 **Expert Probability:** 60%\n"
               "💡 **Recommendation:** ✅ Strong Yes\n\n"
               "📝 **Reasoning:** Expert analysis indicates market mispricing. "
               "See full analysis in output files.\n\n"
               "🔗 **Link:** https://polymarket.com/event/will-the-iranian-regime-fall-by-june-30\n"
               "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

req2 = urllib.request.Request(
    webhook,
    data=json.dumps(long_msg).encode(),
    headers={
        "Content-Type": "application/json",
        "User-Agent": "Polymarket-Brain/1.0"
    },
    method="POST"
)

print(f"Long message ({len(long_msg['content'])} chars)...")
try:
    resp = urllib.request.urlopen(req2)
    print(f"Status: {resp.status}")
except urllib.error.HTTPError as e:
    print(f"Error: {e.code} {e.reason}")
    print(f"Response: {e.read().decode()}")
