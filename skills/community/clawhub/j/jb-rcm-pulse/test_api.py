#!/usr/bin/env python3
import urllib.request, json

API = "https://www.moltbook.com/api/v1"
TOKEN = "moltbook_sk_h_WdHz8lcsCi_-tUAgZtMZEAVcg22chm"

def auth():
    return {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def get(path):
    req = urllib.request.Request(f"{API}{path}", headers=auth())
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())

# Get recent posts to understand format
data = get("/posts?author=jbsclaw&limit=3")
print(json.dumps(data, indent=2)[:2000])