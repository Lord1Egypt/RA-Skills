#!/usr/bin/env python3
"""Check if the Lobster Farm game server is reachable and responding."""

import sys
import urllib.request
import json

GAME_URL = "http://82.156.182.240/lobster-farm/"

def check():
    try:
        resp = urllib.request.urlopen(GAME_URL, timeout=10)
        if resp.status != 200:
            print(f"ERROR: HTTP {resp.status}")
            return 1
        body = resp.read().decode("utf-8", "ignore")
        is_game = "龙虾" in body or "lobster" in body.lower() or "main.js" in body
        if not is_game:
            print(f"WARNING: Page loaded but may not be the game")
            return 1
        print(f"OK: Game page is reachable at {GAME_URL}")
        js_url = GAME_URL.rstrip("/") + "/js/main.js"
        try:
            js_resp = urllib.request.urlopen(js_url, timeout=10)
            js_body = js_resp.read().decode("utf-8", "ignore")
            has_api = "__LOBSTER_API" in js_body
            has_auto = "_tryAutoCreate" in js_body
            print(f"  JS Bridge API: {'YES' if has_api else 'NO'}")
            print(f"  Auto-create:   {'YES' if has_auto else 'NO'}")
        except Exception:
            print(f"  JS check: could not load main.js")
        return 0
    except Exception as e:
        print(f"ERROR: Cannot reach {GAME_URL} — {e}")
        return 1

if __name__ == "__main__":
    sys.exit(check())
