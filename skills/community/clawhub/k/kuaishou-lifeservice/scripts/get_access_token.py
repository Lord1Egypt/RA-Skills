#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kwai Life Service - Get access_token by app_key/merchant_id/app_secret.

Features:
- Call access_token API with app_key, merchant_id, app_secret
- Cache access_token to file
- Check expiry by access_token file mtime; refresh only when expired
- Support loading credentials from current context file

Default storage dir:
  ./.kuaishou-localife-token/{app_key}/{merchant_id}/access_token.txt

Notes:
- TTL defaults to 1.9 days. You can override by --access_token_ttl.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from typing import Dict, Optional
from dataclasses import dataclass

try:
    import requests
except ImportError:
    print("Error: requests module not found. Please install: pip3 install requests", file=sys.stderr)
    sys.exit(1)


@dataclass
class ApiKeyContext:
    """Represents the current API key context."""
    app_key: str
    merchant_id: str
    app_secret: str


def load_current_context() -> Optional[ApiKeyContext]:
    """Load current context from file."""
    DEFAULT_TOKEN_BASE_DIR = "./.kuaishou-localife-token/"
    context_file = os.path.join(DEFAULT_TOKEN_BASE_DIR, "current_context.txt")
    
    if not os.path.exists(context_file):
        return None
    
    try:
        with open(context_file, "r", encoding="utf-8") as f:
            line = f.readline().strip()
        parts = line.split('#')
        if len(parts) != 3:
            return None
        app_key, merchant_id, app_secret = parts
        if not all([app_key, merchant_id, app_secret]):
            return None
        return ApiKeyContext(app_key=app_key, merchant_id=merchant_id, app_secret=app_secret)
    except Exception:
        return None


class AccessTokenManager:
    # API endpoint based on doc: 4.1.3 获取accessToken
    # Interface domain: https://open.kwailocallife.com
    # Interface URL: /rest/open/platform/claw/app/accessToken
    # Method: POST
    API_URL = "https://open.kwailocallife.com/rest/open/platform/claw/app/accessToken"
    DEFAULT_TOKEN_BASE_DIR = "./.kuaishou-localife-token/"

    def __init__(
        self,
        app_key: str,
        merchant_id: str,
        app_secret: str,
        access_token_file: Optional[str] = None,
        access_token_ttl: int = int(1.9 * 24 * 60 * 60),
    ):
        self.app_key = app_key
        self.merchant_id = merchant_id
        self.app_secret = app_secret
        self.access_token_ttl = access_token_ttl

        if access_token_file is None:
            token_dir = os.path.join(self.DEFAULT_TOKEN_BASE_DIR, str(app_key), str(merchant_id))
            access_token_file = os.path.join(token_dir, "access_token.txt")

        self.access_token_file = access_token_file

    def is_token_expired(self) -> bool:
        if not os.path.exists(self.access_token_file):
            return True
        try:
            file_mtime = os.path.getmtime(self.access_token_file)
            return (time.time() - file_mtime) >= self.access_token_ttl
        except Exception:
            return True

    def read_token_from_file(self) -> Optional[str]:
        try:
            with open(self.access_token_file, "r", encoding="utf-8") as f:
                token = f.read().strip()
                return token or None
        except Exception:
            return None

    def save_token_to_file(self, token: str) -> None:
        token_dir = os.path.dirname(self.access_token_file)
        if token_dir and not os.path.exists(token_dir):
            os.makedirs(token_dir, exist_ok=True)
        with open(self.access_token_file, "w", encoding="utf-8") as f:
            f.write(token)

    def call_access_token_api(self) -> Dict:
        payload = {
            "app_key": self.app_key,
            "merchant_id": self.merchant_id,
            "app_secret": self.app_secret,
        }

        try:
            resp = requests.post(self.API_URL, json=payload, timeout=10)
            if resp.status_code != 200:
                return {"error": True, "message": f"HTTP {resp.status_code}", "response": resp.text}

            data = resp.json()
            # New protocol: status=200 means success
            status = data.get("status")
            if status != 200:
                message = data.get("message", "API returned error")
                return {"error": True, "message": f"API error (status={status}): {message}", "response": data}

            # Access token is now in data.access_token
            data_obj = data.get("data")
            if not data_obj:
                return {"error": True, "message": "Missing data object in response", "response": data}
            
            access_token = data_obj.get("access_token")
            if not access_token:
                return {"error": True, "message": "Missing access_token in response", "response": data}

            expires_in = data_obj.get("expires_in")
            return {
                "error": False, 
                "access_token": access_token, 
                "expires_in": expires_in,
                "raw_response": data
            }
        except requests.exceptions.RequestException as e:
            return {"error": True, "message": f"Network request failed: {str(e)}"}
        except json.JSONDecodeError as e:
            return {"error": True, "message": f"Failed to parse API response: {str(e)}"}
        except Exception as e:
            return {"error": True, "message": f"Unexpected error: {str(e)}"}

    def get_access_token(self) -> str:
        if not self.is_token_expired():
            token = self.read_token_from_file()
            if token:
                return token

        result = self.call_access_token_api()
        if result.get("error"):
            msg = result.get("message", "Unknown error")
            print(f"Error: API call failed: {msg}", file=sys.stderr)
            if "response" in result:
                try:
                    print(
                        f"API Response: {json.dumps(result['response'], indent=2, ensure_ascii=False)}",
                        file=sys.stderr,
                    )
                except Exception:
                    print(f"API Response: {result['response']}", file=sys.stderr)
            sys.exit(1)

        token = result["access_token"]
        self.save_token_to_file(token)
        return token


def main() -> None:
    parser = argparse.ArgumentParser(description="Kwai Life Service - get access_token")

    parser.add_argument("--app_key", required=False, help="app_key (if not provided, uses current context)")
    parser.add_argument("--merchant_id", required=False, help="merchant_id (if not provided, uses current context)")
    parser.add_argument("--app_secret", required=False, help="app_secret (if not provided, uses current context)")
    parser.add_argument(
        "--access_token_file",
        default=None,
        help=(
            "access_token save path "
            "(default: ./.kuaishou-localife-token/{app_key}/{merchant_id}/access_token.txt)"
        ),
    )
    parser.add_argument(
        "--access_token_ttl",
        type=int,
        default=int(1.9 * 24 * 60 * 60),
        help="access_token ttl seconds (default 1.9 days)",
    )
    parser.add_argument("--json", action="store_true", help="output json")

    args = parser.parse_args()

    # If any of the required args are provided, all must be provided
    has_any_arg = args.app_key or args.merchant_id or args.app_secret
    has_all_args = args.app_key and args.merchant_id and args.app_secret
    
    if has_any_arg and not has_all_args:
        print("Error: If any of --app_key, --merchant_id, --app_secret is provided, all must be provided.", file=sys.stderr)
        sys.exit(1)
    
    # Try to get credentials from args or current context
    app_key = args.app_key
    merchant_id = args.merchant_id
    app_secret = args.app_secret
    
    if not has_all_args:
        # Try to load from current context
        context = load_current_context()
        if not context:
            print("Error: No credentials provided and no current context found.", file=sys.stderr)
            print("Please either:", file=sys.stderr)
            print("  1. Provide --app_key, --merchant_id, --app_secret arguments", file=sys.stderr)
            print("  2. Or use api_key_manager.py to select a context:", file=sys.stderr)
            print('     python3 scripts/api_key_manager.py --add "app_key#merchant_id#app_secret"', file=sys.stderr)
            print("     python3 scripts/api_key_manager.py --select 1", file=sys.stderr)
            sys.exit(1)
        
        app_key = context.app_key
        merchant_id = context.merchant_id
        app_secret = context.app_secret
        print(f"Using current context: app_key={app_key}, merchant_id={merchant_id}", file=sys.stderr)

    mgr = AccessTokenManager(
        app_key=app_key,
        merchant_id=merchant_id,
        app_secret=app_secret,
        access_token_file=args.access_token_file,
        access_token_ttl=args.access_token_ttl,
    )

    token = mgr.get_access_token()

    if args.json:
        out = {
            "access_token": token,
            "timestamp": datetime.now().isoformat(),
            "token_file": mgr.access_token_file,
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(token)


if __name__ == "__main__":
    main()
