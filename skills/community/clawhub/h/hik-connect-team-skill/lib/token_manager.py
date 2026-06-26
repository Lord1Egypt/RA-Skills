#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HCTOpen Global Token Manager & Base Client

Provides global Token cache management and base API request encapsulation.
"""

import os
import sys
import time
import json
import hashlib
import tempfile
import requests
from typing import Dict, Any, Optional, List, Union
from pathlib import Path


def _get_openclaw_config_paths():
    """Get list of OpenClaw config file paths to search"""
    home = Path.home()
    return [
        home / ".openclaw" / "config.json",
        home / ".openclaw" / "gateway" / "config.json",
        home / ".openclaw" / "channels.json",
    ]


def _load_openclaw_config():
    """Load Hik-Connect Team credentials from OpenClaw config files

    Searches for config in the following order:
    1. ~/.openclaw/config.json
    2. ~/.openclaw/gateway/config.json
    3. ~/.openclaw/channels.json

    Config format:
    {
      "channels": {
        "hik_connect_team_openapi": {
          "appKey": "your_app_key",
          "secretKey": "your_secret_key",
          "enabled": true
        }
      }
    }
    """
    for config_path in _get_openclaw_config_paths():
        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    content = f.read().strip()
                    if not content:
                        continue
                    data = json.loads(content)

                hct_config = data.get("channels", {}).get("hik_connect_team_openapi", {})
                if hct_config.get("enabled", False) and hct_config.get("appKey") and hct_config.get("secretKey"):
                    return hct_config.get("appKey"), hct_config.get("secretKey")
            except (json.JSONDecodeError, OSError):
                continue
    return None, None

class TokenManager:
    """Manage HCTOpen AccessToken acquisition and caching"""

    CACHE_DIR_NAME = "hctopen_global_token_cache"
    CACHE_FILE_NAME = "global_token_cache.json"
    TOKEN_BUFFER_TIME = 5 * 60 * 1000  # 5-minute buffer
    TOKEN_URL = "https://ieu-team.hikcentralconnect.com/api/hccgw/platform/v1/token/get"

    def __init__(self):
        self.token_url = self.TOKEN_URL
        self.cache_file = os.path.join(tempfile.gettempdir(), self.CACHE_DIR_NAME, self.CACHE_FILE_NAME)
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)

    def _get_cache_key(self, app_key: str, secret_key: str) -> str:
        return hashlib.md5(f"{app_key}:{secret_key}".encode()).hexdigest()

    def _load_cache(self) -> Dict[str, Any]:
        if not os.path.exists(self.cache_file):
            return {}
        try:
            with open(self.cache_file, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARNING] Failed to load Token cache: {e}", file=sys.stderr)
            return {}

    def _save_cache(self, cache_data: Dict[str, Any]):
        try:
            temp_file = self.cache_file + ".tmp"
            with open(temp_file, "w") as f:
                json.dump(cache_data, f, indent=2)
            os.replace(temp_file, self.cache_file)
            # Only apply permission on Unix systems (os.chmod has no effect on Windows)
            if os.name != 'nt':
                os.chmod(self.cache_file, 0o600)
        except Exception as e:
            print(f"[WARNING] Failed to save Token cache: {e}", file=sys.stderr)

    def get_token(self, app_key: str, secret_key: str, force_refresh: bool = False) -> Dict[str, Any]:
        """Get Token, prefer using cache"""
        use_cache = os.environ.get("HIK_CONNECT_TEAM_TOKEN_CACHE", "1") == "1" and not force_refresh
        cache_key = self._get_cache_key(app_key, secret_key)

        if use_cache:
            cache = self._load_cache()
            if cache_key in cache:
                token_data = cache[cache_key]
                # Handle expire_time in seconds or milliseconds
                # HCT API returns expireTime in seconds (e.g., 3600),
                # but cache stores it as-is. Convert to milliseconds for comparison.
                # If value > 10^11, it's already in milliseconds (e.g., 1774419637518)
                expire_time = token_data.get("expire_time", 0)
                if expire_time < 10**11:
                    expire_time *= 1000

                if time.time() * 1000 + self.TOKEN_BUFFER_TIME < expire_time:
                    return {"success": True, "access_token": token_data["access_token"], "area_domain": token_data.get("area_domain"), "from_cache": True}

        # Request new Token
        try:
            resp = requests.post(self.token_url, json={"appKey": app_key, "secretKey": secret_key}, timeout=10)
            result = resp.json()
            if result.get("errorCode") == "0":
                data = result.get("data", {})
                access_token = data.get("accessToken")
                expire_time = data.get("expireTime") # API usually returns seconds
                area_domain = data.get("areaDomain", "").rstrip("/")

                # Update cache
                cache = self._load_cache()
                cache[cache_key] = {
                    "access_token": access_token,
                    "expire_time": expire_time,
                    "area_domain": area_domain,
                    "app_key_prefix": app_key[:8]
                }
                self._save_cache(cache)
                return {"success": True, "access_token": access_token, "area_domain": area_domain, "from_cache": False}
            # Unify error field as message
            return {"success": False, "message": result.get("message", "Unknown error"), "errorCode": result.get("errorCode")}
        except Exception as e:
            return {"success": False, "message": f"Request exception: {str(e)}"}

# Robust lib directory import logic: search upward until lib directory is found
def setup_lib_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Search upward 3 levels for root directory containing lib
    root_dir = current_dir
    for _ in range(3):
        root_dir = os.path.dirname(root_dir)
        potential_lib = os.path.join(root_dir, "lib")
        if os.path.exists(potential_lib):
            if potential_lib not in sys.path:
                sys.path.insert(0, potential_lib)
            return True
    return False

if not setup_lib_path():
    print("[ERROR] Cannot find lib directory, please ensure script is located in Hik-Connect_Team Skills directory structure")
    sys.exit(1)

class HCTOpenClient:
    """HCTOpen API Base Client"""

    def __init__(self):
        # Priority 1: Environment variables (highest)
        self.app_key = os.environ.get("HIK_CONNECT_TEAM_OPENAPI_APP_KEY")
        self.secret_key = os.environ.get("HIK_CONNECT_TEAM_OPENAPI_SECRET_KEY")
        self._config_source = "environment variables"

        # Priority 2: OpenClaw config files (only if env vars not set)
        if not all([self.app_key, self.secret_key]):
            config_app_key, config_secret_key = _load_openclaw_config()
            if config_app_key and config_secret_key:
                self.app_key = config_app_key
                self.secret_key = config_secret_key
                self._config_source = "OpenClaw config file"

        if not all([self.app_key, self.secret_key]):
            print("[ERROR] Credentials not found. Please set either:")
            print("  1. Environment variables: HIK_CONNECT_TEAM_OPENAPI_APP_KEY and HIK_CONNECT_TEAM_OPENAPI_SECRET_KEY")
            print("  2. OpenClaw config file: ~/.openclaw/config.json with channels.hik_connect_team_openapi section")
            sys.exit(1)

        print(f"[INFO] Using credentials from: {self._config_source}")

        self.token_manager = TokenManager()
        self._access_token = None
        self._area_domain = None

    def get_access_token(self, force_refresh: bool = False) -> str:
        if not self._access_token or force_refresh:
            res = self.token_manager.get_token(self.app_key, self.secret_key, force_refresh)
            if res["success"]:
                self._access_token = res["access_token"]
                self._area_domain = res.get("area_domain", "")
            else:
                # Unify error field as message
                print(f"[ERROR] Failed to get Token: {res.get('message')}")
                sys.exit(1)
        return self._access_token

    def get_area_domain(self) -> str:
        """Get the area domain from token response, must call get_access_token first"""
        if not self._area_domain:
            self.get_access_token()
        return self._area_domain

    def request(self, method: str, endpoint: str, json_data: Optional[Dict] = None, params: Optional[Dict] = None, token_header_key: str = "Token") -> Dict[str, Any]:
        """Send request with Token, supports auto retry (when Token expired)"""
        # Use areaDomain from token response as the domain
        area_domain = self.get_area_domain()
        if not area_domain:
            return {"errorCode": "-1", "message": "areaDomain not found in token response"}
        url = f"{area_domain}{endpoint}"
        
        for attempt in range(2):
            headers = {
                "Content-Type": "application/json",
                token_header_key: self.get_access_token(force_refresh=(attempt > 0))
            }
            try:
                response = requests.request(method, url, headers=headers, json=json_data, params=params, timeout=30)
                result = response.json()
                
                # Token invalid error codes - retry once with fresh token
                # Common token error codes in Hikvision APIs: 10002 (token expired/invalid), 20004 (token malformed)
                error_code = result.get("errorCode")
                if error_code in ["10002", "20004"] and attempt == 0:
                    print("[INFO] Token may be invalid, trying to refresh Token and retry...")
                    continue
                
                # Unify error field as message
                if result.get("errorCode") != "0" and "errorMsg" in result:
                    result["message"] = result.pop("errorMsg")
                
                return result
            except requests.exceptions.RequestException as e:
                # Unify error field as message
                return {"errorCode": "-1", "message": f"Request exception: {str(e)}"}
            except json.JSONDecodeError:
                # Unify error field as message
                return {"errorCode": "-1", "message": f"JSON parsing failed: {response.text}"}
            except Exception as e:
                # Unify error field as message
                return {"errorCode": "-1", "message": f"Unknown error: {str(e)}"}
        # Both attempts failed
        return {"errorCode": "-1", "message": "Request failed, Token refresh still invalid or other issue encountered"}

    @staticmethod
    def print_table(title: str, headers: List[str], rows: List[List[Any]]):
        """Generic table printing utility"""
        print("=" * 70)
        print(title)
        print("=" * 70)
        if not rows:
            print("No data found")
            return
            
        # Calculate max width for each column
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, val in enumerate(row):
                # Ensure val is string, avoid len() error
                col_widths[i] = max(col_widths[i], len(str(val)))
        
        # Print header
        header_line = "  ".join(f"{headers[i]:<{col_widths[i]}}" for i in range(len(headers)))
        print(header_line)
        print("-" * len(header_line))
        
        # Print rows
        for row in rows:
            row_line = "  ".join(f"{str(val):<{col_widths[i]}}" for i, val in enumerate(row))
            print(f"{row_line}")
        print("=" * 70)

    @staticmethod
    def exit_with_json(data: Dict[str, Any]):
        """Output in JSON format and exit"""
        print("\n[JSON Output]")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        print("=" * 70)
        print("Done")
        print("=" * 70)
        sys.exit(0 if data.get("success", True) else 1)

# Backward compatibility (if external code calls get_cached_token directly)
def get_cached_token(app_key, secret_key, use_cache=True):
    tm = TokenManager()
    return tm.get_token(app_key, secret_key, force_refresh=not use_cache)

if __name__ == "__main__":
    # Simple CLI test
    # Ensure HIK_CONNECT_TEAM_OPENAPI_APP_KEY, HIK_CONNECT_TEAM_OPENAPI_SECRET_KEY environment variables are set
    try:
        client = HCTOpenClient()
        token = client.get_access_token()
        print(f"Test Token: {token[:10]}...")
        # Simulate a request
        test_endpoint = "/api/hccgw/resource/v1/devices/get" # Hypothetical test endpoint
        test_result = client.request("POST", test_endpoint, json_data={"pageIndex":1, "pageSize":1}, token_header_key="Token")
        print("Test request result:")
        print(json.dumps(test_result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Test failed: {e}")
