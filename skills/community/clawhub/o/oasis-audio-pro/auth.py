#!/usr/bin/env python3

import http.client
import json
import sys
from pathlib import Path

# 配置路径
CONFIG_DIR = Path.home() / ".oasis_audio"
CONFIG_FILE = CONFIG_DIR / "oasis_config.json"
VISITOR_LOGIN_URL = "/api/user/login/visitor"
API_HOST = "eagle-api.xplai.ai"


def load_token():
    """从配置文件加载 jwt_token"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                return config.get("jwt_token", "")
        except (json.JSONDecodeError, IOError):
            return ""
    return ""


def save_token(token):
    """保存 jwt_token 到配置文件"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    config = {"jwt_token": token}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def get_or_refresh_token():
    """获取或刷新 token"""
    token = load_token()
    if token:
        return token
    
    # 调用 visitor 接口获取 token
    payload = {"scene": "oasis"}
    try:
        conn = http.client.HTTPSConnection(API_HOST, timeout=30)
        headers = {"Content-Type": "application/json"}
        conn.request("POST", VISITOR_LOGIN_URL, json.dumps(payload), headers)
        response = conn.getresponse()
        response_body = response.read().decode("utf-8")
        conn.close()
        
        if response.status >= 400:
            print(f"Failed to get token: HTTP {response.status}", file=sys.stderr)
            return None
        
        result = json.loads(response_body)
        if result.get("code") == 0:
            new_token = result.get("data", {}).get("jwt_token", "")
            if new_token:
                save_token(new_token)
                return new_token
        
        print(f"Failed to get token: {result.get('msg')}", file=sys.stderr)
        return None
    except (http.client.HTTPException, OSError) as e:
        print(f"Failed to get token: {e}", file=sys.stderr)
        return None


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Manage authentication token")
    parser.add_argument("--refresh", action="store_true", help="Force refresh token (ignore cached)")
    parser.add_argument("--set-token", type=str, metavar="TOKEN",
                        help="Set token directly (bypasses API call)")
    args = parser.parse_args()

    if args.set_token:
        save_token(args.set_token)
        print(f"Token saved to {CONFIG_FILE}")
        return

    if args.refresh:
        token = get_or_refresh_token()
    else:
        token = load_token()
        if not token:
            print("No cached token found, fetching new one...")
            token = get_or_refresh_token()

    if token:
        print(token)
    else:
        print("Failed to get token", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
