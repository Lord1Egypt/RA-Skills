#!/usr/bin/env python3
import json
import os
import requests

QBIT_URL      = os.environ.get("QBIT_URL", "http://localhost:8080")
QBIT_USERNAME = os.environ.get("QBIT_USERNAME", "admin")
QBIT_PASSWORD = os.environ.get("QBIT_PASSWORD", "")

def login(session: requests.Session):
    resp = session.post(
        f"{QBIT_URL}/api/v2/auth/login",
        data={"username": QBIT_USERNAME, "password": QBIT_PASSWORD},
        timeout=5,
    )
    if resp.text.strip() != "Ok.":
        raise RuntimeError(f"qBittorrent login failed: {resp.text}")

def get_torrents(session: requests.Session):
    resp = session.get(f"{QBIT_URL}/api/v2/torrents/info", timeout=5)
    resp.raise_for_status()
    return resp.json()

def main():
    try:
        session = requests.Session()
        login(session)
        torrents = get_torrents(session)
        
        output = []
        for t in torrents:
            output.append({
                "name": t["name"],
                "progress": round(t["progress"] * 100, 1),
                "ratio": round(t["ratio"], 2),
                "state": t["state"]
            })
        print(json.dumps(output))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
