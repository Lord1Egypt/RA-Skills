"""KingDoc HTTP Client"""
import time
import random
import requests
from typing import Dict, Optional, Any

from .auth import KingDocAuth
from .exceptions import (
    KingDocError, AuthError, PermissionError, QuotaError,
    DocTypeError, DocNotFoundError, RateLimitError,
    VersionConflictError, FileTooLargeError, FileTypeBlockedError,
    ServiceUnavailableError, ParamError, ERROR_MAP
)


class KingDocClient:
    """金山文档 HTTP 客户端"""
    
    def __init__(self, config_path: str):
        self.auth = KingDocAuth(config_path)
        self.session = requests.Session()
        self._max_retries = 5
        self._base_delay = 1.0
    
    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict] = None,
        json: Optional[Dict] = None,
        retries: int = 0
    ) -> Dict[str, Any]:
        """发送 HTTP 请求（含自动重试和限流退避）"""
        url = f"{self.auth.API_BASE}{path}"
        headers = self.auth.headers
        
        try:
            resp = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                headers=headers,
                timeout=30
            )
        except requests.exceptions.Timeout:
            if retries < self._max_retries:
                time.sleep(self._base_delay * (2 ** retries))
                return self.request(method, path, params, json, retries + 1)
            raise ServiceUnavailableError()
        
        # 处理限流 429
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 60))
            if retries < self._max_retries:
                delay = min(retry_after * (2 ** retries) + random.uniform(0, 1), 300)
                time.sleep(delay)
                return self.request(method, path, params, json, retries + 1)
            raise RateLimitError(retry_after)
        
        # 处理其他错误
        if resp.status_code >= 400:
            error_class = ERROR_MAP.get(resp.status_code, KingDocError)
            try:
                body = resp.json()
                message = body.get("message", body.get("error", ""))
            except:
                message = resp.text[:200]
            raise error_class(message) if error_class != RateLimitError else error_class()
        
        try:
            return resp.json()
        except:
            return {"code": 0, "message": "OK"}
    
    def get(self, path: str, params: Optional[Dict] = None) -> Dict:
        return self.request("GET", path, params=params)
    
    def post(self, path: str, json: Optional[Dict] = None) -> Dict:
        return self.request("POST", path, json=json)
    
    def put(self, path: str, json: Optional[Dict] = None) -> Dict:
        return self.request("PUT", path, json=json)
    
    def delete(self, path: str) -> Dict:
        return self.request("DELETE", path)
