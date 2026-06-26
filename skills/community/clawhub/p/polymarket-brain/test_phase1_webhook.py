import requests

# Phase 1 webhook (CNBC fetcher)
webhook1 = "https://discord.com/api/webhooks/1482043765471445333/-cHOLCqBtvU_Wua8STfoINes7J0pFNFsXB27EJ3f8F7BklC5P_OkIGAx2HQLDPZe1bNJ"

print("Testing Phase 1 webhook (CNBC News)...")
r1 = requests.post(webhook1, json={"content": "Test from CNBC fetcher - checking if webhook works"}, timeout=30)
print(f"Phase 1 Status: {r1.status_code}")
if r1.status_code == 204:
    print("✓ Webhook is working!")
else:
    print(f"✗ Webhook error: {r1.text}")
