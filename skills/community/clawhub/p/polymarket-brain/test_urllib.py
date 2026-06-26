import urllib.request
import urllib.error
import json
import time

webhook = "https://discord.com/api/webhooks/1483478506070474922/ReIZsU3KTpXqNseTWFBNsuPJ-FbYgqEuCTELtMHRWw4ND8vVjMUr36b6LyusiOoJn66d"

# Test header
header = {"content": "Test header message"}
req = urllib.request.Request(
    webhook,
    data=json.dumps(header).encode(),
    headers={"Content-Type": "application/json"},
    method="POST"
)

print("Sending header...")
try:
    urllib.request.urlopen(req)
    print("Header: 204 OK")
    time.sleep(1.2)
except urllib.error.HTTPError as e:
    print(f"Header: {e.code} {e.reason}")

# Test market messages
for i in range(3):
    msg = {"content": f"Test market {i+1}"}
    req = urllib.request.Request(
        webhook,
        data=json.dumps(msg).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    print(f"Sending market {i+1}...")
    try:
        urllib.request.urlopen(req)
        print(f"Market {i+1}: 204 OK")
        time.sleep(1.2)
    except urllib.error.HTTPError as e:
        print(f"Market {i+1}: {e.code} {e.reason}")

print("Done!")
