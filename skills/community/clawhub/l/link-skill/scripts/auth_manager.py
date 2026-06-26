#!/usr/bin/env python3
"""
auth_manager.py - Generic authentication manager.
Supports multi-platform token retrieval, cache reuse, and automatic refresh.
Auth types: bearer_token / api_key / basic / none
"""
import argparse
import json
import os
import sys
import time
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_CACHE = os.path.join(SCRIPT_DIR, ".token_cache.json")
TIMEOUT = 15


def load_config(config_path, platform_id=None):
    if not os.path.exists(config_path):
        sys.exit(f"[ERROR] Config file does not exist: {config_path}")
    with open(config_path, "r", encoding="utf-8-sig") as f:
        cfg = json.load(f)
    pid = platform_id or cfg.get("active_platform")
    if not pid or pid not in cfg.get("platforms", {}):
        sys.exit(f"[ERROR] Platform '{pid}' is not defined in config. Available: {list(cfg.get('platforms', {}).keys())}")
    p = cfg["platforms"][pid]
    p["_id"] = pid
    return p


def load_cache():
    if not os.path.exists(TOKEN_CACHE):
        return {}
    with open(TOKEN_CACHE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_cache(cache):
    with open(TOKEN_CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def extract_nested(data, field_path):
    """Extract a value from nested dict using dot path, for example: 'data.token'."""
    keys = field_path.split(".")
    val = data
    for k in keys:
        if isinstance(val, dict):
            val = val.get(k)
        else:
            return None
    return val


def do_login(plat):
    auth = plat.get("auth", {})
    auth_type = auth.get("type", "none")

    if auth_type == "none":
        print(f"[INFO] Platform '{plat['name']}' does not require authentication.")
        return None

    if auth_type == "api_key":
        key = auth.get("api_key", "")
        if key:
            print(f"[OK] Platform '{plat['name']}' uses static API Key.")
            return key
        sys.exit("[ERROR] auth.api_key is not configured.")

    if auth_type == "basic":
        print(f"[INFO] Platform '{plat['name']}' uses Basic Auth; pre-login is not required.")
        import base64
        body = auth.get("login_body", {})
        cred = base64.b64encode(f"{body.get('username', body.get('account', ''))}:{body.get('password', '')}".encode()).decode()
        return f"Basic {cred}"

    gateway = plat.get("gateway", "").rstrip("/")
    endpoint = auth.get("login_endpoint", "")
    if not gateway or not endpoint:
        sys.exit("[ERROR] Login requires both gateway and auth.login_endpoint.")

    url = f"{gateway}{endpoint}"
    body = auth.get("login_body", {})

    print(f"[LOGIN] {url}")
    try:
        resp = requests.post(url, json=body, headers={"Content-Type": "application/json"}, timeout=TIMEOUT)
    except requests.RequestException as e:
        sys.exit(f"[ERROR] Login request failed: {e}")

    if resp.status_code != 200:
        sys.exit(f"[ERROR] Login returned HTTP {resp.status_code}: {resp.text[:500]}")

    try:
        data = resp.json()
    except ValueError:
        sys.exit(f"[ERROR] Login response is not JSON: {resp.text[:500]}")

    token_field = auth.get("token_field", "data.token")
    token = extract_nested(data, token_field)
    if not token:
        print(f"[WARN] Cannot extract '{token_field}' from response. Full response:")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        sys.exit("[ERROR] Token extraction failed.")

    print(f"[OK] Login successful, first 16 chars of token: {str(token)[:16]}...")
    return token


def get_or_refresh_token(plat, force=False):
    pid = plat["_id"]
    cache = load_cache()

    if not force and pid in cache:
        entry = cache[pid]
        age_min = (time.time() - entry.get("timestamp", 0)) / 60
        if age_min < entry.get("ttl_minutes", 120):
            print(f"[CACHE] Using cached token (cached for {age_min:.0f} minutes)")
            print(entry["token"])
            return entry["token"]
        print(f"[CACHE] Token expired ({age_min:.0f} minutes), re-login...")

    token = do_login(plat)
    if token:
        cache[pid] = {
            "token": token,
            "timestamp": time.time(),
            "ttl_minutes": 120,
            "platform_name": plat.get("name", pid),
        }
        save_cache(cache)
    return token


def main():
    parser = argparse.ArgumentParser(description="Generic authentication manager")
    parser.add_argument("--config", required=True, help="Platform config file path")
    parser.add_argument("--platform", help="Specify platform ID")
    parser.add_argument("--force-login", action="store_true", help="Force re-login")
    parser.add_argument("--show-cache", action="store_true", help="Show current token cache")
    args = parser.parse_args()

    if args.show_cache:
        cache = load_cache()
        print(json.dumps(cache, ensure_ascii=False, indent=2))
        return

    plat = load_config(args.config, args.platform)
    get_or_refresh_token(plat, force=args.force_login)


if __name__ == "__main__":
    main()
