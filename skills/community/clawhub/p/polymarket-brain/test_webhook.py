import requests

webhook = "https://discord.com/api/webhooks/1483478506070474922/ReIZsU3KTpXqNseTWFBNsuPJ-FbYgqEuCTELtMHRWw4ND8vVjMUr36b6LyusiOoJn66d"

response = requests.post(webhook, json={"content": "Test from polymarket-brain"}, timeout=30)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
