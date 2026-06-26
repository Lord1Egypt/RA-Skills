import requests

# --- Config ---
BASE_URL = "https://ai-lead-intelligence-acet.onrender.com"
ACCESS_TOKEN = "your-access-token-here"  # ← replace with your actual ACCESS_TOKEN from Render

headers = {
    "Content-Type": "application/json",
    "X-Access-Token": ACCESS_TOKEN
}

# --- Test 1: Health check ---
print("Testing health check...")
r = requests.get(BASE_URL)
print(r.json())
print()

# --- Test 2: Lead intelligence ---
print("Testing lead intelligence...")
payload = {
    "company": "HubSpot",
    "persona": "Head of Sales"
}
r = requests.post(f"{BASE_URL}/analyze-lead", json=payload, headers=headers)
data = r.json()

print("Status:", r.status_code)
print()
print("Hunter Data:", data.get("hunter_data"))
print()
print("Report:")
print(data.get("report"))
