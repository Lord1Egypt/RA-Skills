from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from typing import Any, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from scripts.config import settings, get_api_key


@dataclass
class HttpResult:
    status_code: int
    json: Any
    elapsed_ms: int
    url: str


class UpstreamError(RuntimeError):
    def __init__(self, message: str, *, status_code: Optional[int] = None, payload: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload


class XiaoBenYangClient:
    """小笨羊MCP API客户端"""

    def __init__(self) -> None:
        self._session = requests.Session()
        retry_strategy = Retry(
            total=settings.max_retries,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self._session.mount("http://", adapter)
        self._session.mount("https://", adapter)
        self._log = logging.getLogger("scripts.xiaobenyang")

    def close(self) -> None:
        self._session.close()

    def call_tool(
        self,
        mcp_id: str,
        tool_name: str,
        params: dict[str, Any],
    ) -> HttpResult:
        """调用小笨羊MCP工具"""
        url = f"{settings.base_url}/api"
        mcp_id = mcp_id or settings.mcp_id

        api_key = get_api_key()
        if not api_key:
            raise UpstreamError("API密钥未设置，请先调用 set_api_key()")
        
        headers = {
            "XBY-APIKEY": api_key,
            "func": tool_name,
            "mcpid": mcp_id,
            "Content-Type": "application/json",
        }

        # data = {k: str(v) if v is not None else "" for k, v in params.items()}

        t0 = time.time()
        try:
            resp = self._session.post(
                url=url,
                headers=headers,
                data=json.dumps(params),
                timeout=settings.timeout_seconds,
            )
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            self._log.warning("upstream_http_error url=%s tool=%s error=%s", url, tool_name, str(e))
            raise UpstreamError(
                f"Upstream HTTP error: {e}",
                status_code=getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None,
                payload=str(e),
            )

        elapsed_ms = int((time.time() - t0) * 1000)

        try:
            payload = resp.json()
        except json.JSONDecodeError:
            payload = resp.text

        self._log.info("upstream_ok url=%s tool=%s status=%s elapsed_ms=%s", url, tool_name, resp.status_code, elapsed_ms)

        return HttpResult(
            status_code=resp.status_code,
            json=payload,
            elapsed_ms=elapsed_ms,
            url=url,
        )


def call_api(mcp_id: str, tool_name: str, params: dict[str, Any]) -> dict[str, Any]:
    """调用小笨羊MCP API，返回统一格式"""
    client = XiaoBenYangClient()
    try:
        res = client.call_tool(mcp_id, tool_name, params)
        return {"success": True, "raw": res.json, "message": "success"}
    except UpstreamError as e:
        return {"success": False, "raw": getattr(e, "payload", None), "message": f"API调用失败: {e}"}
    finally:
        client.close()
