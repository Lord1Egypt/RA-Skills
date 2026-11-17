"""
Stockpile Market API Client for MCP Server.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional


class StockpileAPIError(RuntimeError):
    """Exception raised when a Stockpile API call fails."""

    def __init__(self, message: str, status_code: Optional[int] = None, detail: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.detail = detail


class StockpileClient:
    """Client for interacting with Stockpile Market REST API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        jwt_token: Optional[str] = None,
        timeout: float = 20.0,
    ):
        self.base_url = (
            base_url
            or os.getenv("STOCKPILE_API_URL")
            or "https://stockpile.market/api"
        ).rstrip("/")
        self.api_key = api_key or os.getenv("STOCKPILE_API_KEY", "")
        self.jwt_token = jwt_token or os.getenv("STOCKPILE_JWT_TOKEN", "")
        self.timeout = timeout

    def request(
        self,
        endpoint: str,
        method: str = "GET",
        payload: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        api_key_override: Optional[str] = None,
        jwt_token_override: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Make an authenticated HTTP request to the Stockpile API."""
        clean_endpoint = endpoint.lstrip("/")
        url = f"{self.base_url}/{clean_endpoint}"
        if params:
            query_string = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
            if query_string:
                url = f"{url}?{query_string}"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "mcp-stockpile/1.0.0 (Model Context Protocol Client)",
        }

        key = api_key_override or self.api_key
        token = jwt_token_override or self.jwt_token

        if key:
            headers["X-API-Key"] = key
        elif token:
            headers["Authorization"] = f"Bearer {token}"

        data = json.dumps(payload).encode("utf-8") if payload is not None else None
        req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw_body = resp.read().decode("utf-8")
                if not raw_body:
                    return {"success": True}
                try:
                    return json.loads(raw_body)
                except json.JSONDecodeError:
                    return {"raw": raw_body}
        except urllib.error.HTTPError as e:
            raw_err = e.read().decode("utf-8")
            try:
                err_data = json.loads(raw_err)
                detail = err_data.get("detail", raw_err)
            except Exception:
                detail = raw_err
            raise StockpileAPIError(f"HTTP {e.code}: {detail}", status_code=e.code, detail=detail) from e
        except urllib.error.URLError as e:
            raise StockpileAPIError(f"Network error connecting to Stockpile API: {e.reason}") from e
        except Exception as e:
            raise StockpileAPIError(f"Request failed: {str(e)}") from e
