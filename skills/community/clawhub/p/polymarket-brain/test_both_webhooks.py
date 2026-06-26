import requests

# Phase 1 webhook (CNBC fetcher)
webhook1 = "https://discord.com/api/webhooks/1482043765471445333/-cHOLCqBtvU_Wua8STfoINes7J0pFNFsXB27EJ3f8F7BklC5P_OkIGAx2HQLDPZe1bNJ"

# Phase 4 webhook (Polymarket analysis)
webhook2 = "https://discord.com/api/webhooks/1483478506070474922/ReIZsU3KTpXqNseTWFBNsuPJ-FbYgqEuCTELtMHRWw4ND8vVjMUr36b6LyusiOoJn66d"

print("Testing Phase 1 webhook (CNBC)...")
r1 = requests.post(webhook1, json={"content": "Test from CNBC fetcher"}, timeout=30)
print(f"Phase 1 Status: {r1.status_code}")
print(f"Phase 1 Response: {r1.text}")

print("\nTesting Phase 4 webhook (Analysis)...")
r2 = requests.post(webhook2, json={"content": "Test from Polymarket"}, timeout=30)
print(f"Phase 4 Status: {r2.status_code}")
print(f"Phase 4 Response: {r2.text}")
