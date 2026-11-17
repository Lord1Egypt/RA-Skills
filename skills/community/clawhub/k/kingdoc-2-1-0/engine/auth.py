"""KingDoc OAuth 鉴权模块"""
import json
import time
import sys
import argparse
import requests
from pathlib import Path
from typing import Optional, Dict

TOKEN_URL = "https://open.kdocs.cn/oauth/token"
API_BASE = "https://developer.kdocs.cn/api/v1/openapi"


class KingDocAuth:
    """金山文档 OAuth 2.0 鉴权"""
    
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self._access_token: Optional[str] = None
        self._token_expiry: float = 0
    
    @staticmethod
    def _load_config(path: str) -> Dict:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Config not found: {path}")
        return json.loads(p.read_text(encoding="utf-8"))
    
    @property
    def access_token(self) -> str:
        """获取有效 Token，自动刷新"""
        if self._access_token and time.time() < self._token_expiry:
            return self._access_token
        self._refresh_token()
        return self._access_token
    
    def _refresh_token(self):
        """使用 Client Credentials 获取 Token"""
        resp = requests.post(TOKEN_URL, data={
            "grant_type": "client_credentials",
            "client_id": self.config["appId"],
            "client_secret": self.config["appSecret"],
            "scope": self.config.get("scope", "user:file:write user:file:read")
        }, timeout=30)
        
        if resp.status_code != 200:
            raise AuthenticationError(f"Token refresh failed: {resp.status_code} {resp.text}")
        
        data = resp.json()
        self._access_token = data["access_token"]
        self._token_expiry = time.time() + data.get("expires_in", 7200) - 300
    
    @property
    def headers(self) -> Dict[str, str]:
        """获取带鉴权的请求头"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    @property
    def api_base(self) -> str:
        return API_BASE


class AuthenticationError(Exception):
    """鉴权失败异常"""
    pass


def main():
    """命令行测试入口"""
    parser = argparse.ArgumentParser(description="KingDoc Auth Test")
    parser.add_argument("--config", required=True, help="Config file path")
    parser.add_argument("--test", action="store_true", help="Test connection")
    args = parser.parse_args()
    
    try:
        auth = KingDocAuth(args.config)
        token = auth.access_token
        print(f"[OK] Auth successful, token: {token[:20]}...")
        print(f"[OK] API Base: {auth.api_base}")
        sys.exit(0)
    except Exception as e:
        print(f"[FAIL] Auth failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
