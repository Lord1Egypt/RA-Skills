import urllib.request
import urllib.error
import json
import time

webhook = "https://discord.com/api/webhooks/1483478506070474922/ReIZsU3KTpXqNseTWFBNsuPJ-FbYgqEuCTELtMHRWw4ND8vVjMUr36b6LyusiOoJn66d"

# Test WITHOUT User-Agent
msg = {"content": "Test without User-Agent"}
req = urllib.request.Request(
    webhook,
    data=json.dumps(msg).encode(),
    headers={"Content-Type": "application/json"},
    method="POST"
)

print("Without User-Agent...")
try:
    resp = urllib.request.urlopen(req)
    print(f"Status: {resp.status}")
except urllib.error.HTTPError as e:
    print(f"Error: {e.code} {e.reason}")

time.sleep(1.2)

# Test WITH User-Agent
msg = {"content": "Test with User-Agent"}
req = urllib.request.Request(
    webhook,
    data=json.dumps(msg).encode(),
    headers={
        "Content-Type": "application/json",
        "User-Agent": "Polymarket-Brain/1.0"
    },
    method="POST"
)

print("With User-Agent...")
try:
    resp = urllib.request.urlopen(req)
    print(f"Status: {resp.status}")
except urllib.error.HTTPError as e:
    print(f"Error: {e.code} {e.reason}")
