"""Scrapy Middleware — 反爬增强。"""

from __future__ import annotations

import logging
import os
import random
from typing import Any, Optional

import requests as http_requests
from curl_cffi import requests as cffi_requests
from scrapy import Request, signals
from scrapy.http import HtmlResponse, Response

logger = logging.getLogger(__name__)

# 常见 User-Agent 池
_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
]


class RandomUserAgentMiddleware:
    """随机 User-Agent 中间件。"""

    def process_request(self, request: Request, spider: Any) -> None:
        request.headers["User-Agent"] = random.choice(_USER_AGENTS)


class ProxyMiddleware:
    """代理池中间件。

    从代理池服务获取代理 IP，环境变量 PROXY_POOL_URL 配置代理池地址。
    代理池 API 需返回格式：{"proxy": "http://ip:port"} 或纯文本 ip:port。
    """

    def __init__(self) -> None:
        self._proxy_pool_url = os.environ.get("PROXY_POOL_URL", "")

    def process_request(self, request: Request, spider: Any) -> None:
        if not self._proxy_pool_url:
            return

        proxy = self._fetch_proxy()
        if proxy:
            request.meta["proxy"] = proxy

    def _fetch_proxy(self) -> str:
        """从代理池获取代理地址。"""
        try:
            resp = http_requests.get(self._proxy_pool_url, timeout=5)
            text = resp.text.strip()
            # 支持 JSON 或纯文本
            if text.startswith("{"):
                import json
                data = json.loads(text)
                return data.get("proxy", "")
            # 纯文本 ip:port
            if ":" in text:
                return f"http://{text}" if not text.startswith("http") else text
        except Exception as e:
            logger.debug("Failed to fetch proxy: %s", e)
        return ""


class TlsImpersonateMiddleware:
    """用 curl_cffi TLS 指纹伪装绕过 Cloudflare 反爬。

    无需启动浏览器，通过模拟 Chrome 的 TLS 握手特征直接发送 HTTP 请求。
    资源占用极低，适合容器/沙盒等受限环境。

    用法：在 Request.meta 中设置 use_impersonate=True 即可启用。
    """

    def process_request(
        self, request: Request, spider: Any
    ) -> Optional[HtmlResponse]:
        if not request.meta.get("use_impersonate"):
            return None  # 不拦截，走默认下载器

        resp = cffi_requests.get(
            request.url,
            impersonate="chrome",
            timeout=30,
            allow_redirects=True,
        )

        return HtmlResponse(
            url=request.url,
            body=resp.content,
            encoding="utf-8",
            request=request,
            status=resp.status_code,
        )


class RetryOnErrorMiddleware:
    """下载错误重试中间件（增强版）。

    对 403/429/503 等反爬响应进行标记，配合 Scrapy 内置 RetryMiddleware 工作。
    """

    def process_response(self, request: Request, response: Response, spider: Any) -> Response:
        if response.status in (403, 429, 503):
            spider.logger.warning(
                "Anti-crawl response: status=%d url=%s",
                response.status,
                request.url,
            )
            # 对于 429 (Too Many Requests)，标记需要降速
            if response.status == 429:
                spider.logger.info("Rate limited, consider increasing DOWNLOAD_DELAY")
        return response
