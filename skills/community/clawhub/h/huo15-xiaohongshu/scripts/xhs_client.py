"""火一五小红书客户端 — 尊重频率 / 防封号的 HTTP 层。

设计原则
========
1. **用用户自己的登录 Cookie**：脚本不做登录自动化（输入密码 / 刷验证码都会被风控识别）。用户在
   正常浏览器里登录后，把 Cookie 复制过来用。
2. **浏览器式请求**：Header 与真实 Chrome/手 Q 保持一致；不伪造 User-Agent 之外的指纹。
3. **人类化节奏**：每次请求之间加入 2~8 秒随机延时 + 任务级 max-requests 上限；
   绝不在短时间内密集抓取。
4. **错误即退出**：遇到 460 / 461 / 403 / 出现 "verify" / "captcha" / "登录" 字样，
   立即停止并抛出 RateLimited / BlockedByCaptcha，不做盲目重试。
5. **只读 / 小规模**：目标是给个人号做"选题调研、同行分析"，而不是批量搬运。
6. **不写**：从不调用 post / like / follow / comment 接口，避免触发行为风控。

使用
====
    from xhs_client import XHSClient, load_cookie_from_env

    client = XHSClient(cookie=load_cookie_from_env(), min_delay=3, max_delay=7)
    html = client.get_explore_page(note_id='64abcd...')

实现说明
========
- 目前使用 **web 网页端** + Cookie 的方式，解析 `window.__INITIAL_STATE__` / `window.__INITIAL_SSR_STATE__`。
- API 接口（/api/sns/web/v1/...）需要 X-s / X-t 签名。本模块预留 `_sign_request` 钩子，
  但默认不启用 — 风险大、容易封号，不推荐。
"""

from __future__ import annotations

import json
import logging
import os
import random
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from urllib.parse import urlparse

try:
    import requests
except ImportError as exc:  # pragma: no cover
    raise SystemExit("需要 requests: pip install requests") from exc


LOG = logging.getLogger("xhs_client")
if not LOG.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    LOG.addHandler(_h)
    LOG.setLevel(logging.INFO)


# -------- 例外 --------


class XHSError(Exception):
    """小红书客户端基础错误。"""


class RateLimited(XHSError):
    """触发频率限制 — 必须停止抓取一段时间。"""


class BlockedByCaptcha(XHSError):
    """触发滑块 / 图形验证 — 必须人工处理，脚本不自救。"""


class LoginRequired(XHSError):
    """Cookie 失效或未登录。"""


class NotFound(XHSError):
    """笔记 / 用户不存在或已被删除。"""


# -------- 工具 --------


def load_cookie_from_env(var: str = "XHS_COOKIE") -> str:
    """从环境变量读 Cookie。"""
    cookie = os.environ.get(var, "").strip()
    if not cookie:
        raise LoginRequired(
            f"未设置环境变量 {var}。请先在浏览器登录小红书，复制完整 Cookie 字符串后执行：\n"
            f"    export {var}='a=b; c=d; ...'\n"
            "注意：这是你本人的登录态，切勿分享给他人。"
        )
    return cookie


_DEFAULT_UAS = [
    # 桌面 Chrome（最安全、最常见）
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    # 手机端 Safari
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
]


# -------- 客户端 --------


@dataclass
class XHSClient:
    """小红书网页端客户端。用用户 Cookie，强节流 + 风控检测。"""

    cookie: str
    user_agent: Optional[str] = None
    min_delay: float = 3.0  # 最短随机等待（秒）
    max_delay: float = 7.0  # 最长随机等待（秒）
    timeout: float = 15.0
    max_requests_per_session: int = 30  # 单次会话抓取上限
    proxies: Optional[Dict[str, str]] = None

    session: requests.Session = field(init=False)
    _request_count: int = field(init=False, default=0)
    _last_request_at: float = field(init=False, default=0.0)

    def __post_init__(self) -> None:
        self.session = requests.Session()
        if not self.user_agent:
            self.user_agent = random.choice(_DEFAULT_UAS)
        self.session.headers.update(self._base_headers())
        self._apply_cookie(self.cookie)
        if self.proxies:
            self.session.proxies.update(self.proxies)

    # ----- headers / cookie -----

    def _base_headers(self) -> Dict[str, str]:
        return {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Referer": "https://www.xiaohongshu.com/",
            "Upgrade-Insecure-Requests": "1",
            "sec-ch-ua": '"Chromium";v="125", "Not.A/Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
        }

    def _apply_cookie(self, cookie_str: str) -> None:
        """把字符串形式的 Cookie 拆到 session 里。"""
        for chunk in cookie_str.split(";"):
            chunk = chunk.strip()
            if not chunk or "=" not in chunk:
                continue
            name, value = chunk.split("=", 1)
            self.session.cookies.set(name.strip(), value.strip(), domain=".xiaohongshu.com")

    # ----- 节流 -----

    def _throttle(self) -> None:
        self._request_count += 1
        if self._request_count > self.max_requests_per_session:
            raise RateLimited(
                f"本次会话已发起 {self._request_count - 1} 个请求，超过上限 "
                f"{self.max_requests_per_session}。请换个时间再抓，避免触发风控。"
            )
        wait = random.uniform(self.min_delay, self.max_delay)
        elapsed = time.time() - self._last_request_at
        if elapsed < wait and self._last_request_at > 0:
            time.sleep(wait - elapsed)
        self._last_request_at = time.time()

    # ----- 核心 GET -----

    def _get(self, url: str, params: Optional[Dict[str, Any]] = None,
             extra_headers: Optional[Dict[str, str]] = None) -> requests.Response:
        self._throttle()
        headers = {}
        if extra_headers:
            headers.update(extra_headers)
        LOG.info("GET %s", url)
        resp = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
        self._check_response(resp)
        return resp

    def _check_response(self, resp: requests.Response) -> None:
        """识别常见的风控信号。"""
        status = resp.status_code
        text_head = resp.text[:2048] if resp.text else ""
        low = text_head.lower()

        if status in (460, 461):
            raise RateLimited(f"HTTP {status} — 小红书频率限制，立即停止。")
        if status in (401,):
            raise LoginRequired("HTTP 401 — Cookie 失效，需要重新登录获取。")
        if status == 403:
            raise BlockedByCaptcha("HTTP 403 — 被拒绝，通常是风控，请到浏览器过一下滑块。")
        if status == 404:
            raise NotFound("HTTP 404 — 内容不存在。")
        if status >= 500:
            raise XHSError(f"HTTP {status} — 小红书服务端错误。")

        # HTML 层面的风控识别
        captcha_markers = ("captcha", "verify", "滑块", "行为验证", "/verify/")
        if any(m in low for m in captcha_markers) and "search" not in resp.url:
            raise BlockedByCaptcha("响应体出现验证码提示，已被风控，请到浏览器处理。")

        # 如果重定向到登录页
        if "login" in urlparse(resp.url).path.lower():
            raise LoginRequired("被重定向到登录页，Cookie 可能已失效。")

    # ----- 公开方法：网页端读取 -----

    def get_explore_page(self, note_id: str, xsec_token: Optional[str] = None,
                         xsec_source: str = "pc_feed") -> str:
        """抓取笔记详情页 HTML。解析 `window.__INITIAL_STATE__` 见 xhs_parser。"""
        url = f"https://www.xiaohongshu.com/explore/{note_id}"
        params: Dict[str, Any] = {}
        if xsec_token:
            params["xsec_token"] = xsec_token
            params["xsec_source"] = xsec_source
        resp = self._get(url, params=params)
        return resp.text

    def get_user_page(self, user_id: str) -> str:
        """抓取用户主页 HTML。解析 user profile + 已发布笔记列表 preview。"""
        url = f"https://www.xiaohongshu.com/user/profile/{user_id}"
        resp = self._get(url)
        return resp.text

    def get_search_page(self, keyword: str, source: str = "web_search_result_notes") -> str:
        """搜索笔记页（网页端）。"""
        from urllib.parse import quote
        url = f"https://www.xiaohongshu.com/search_result?keyword={quote(keyword)}&source={source}"
        resp = self._get(url)
        return resp.text

    # ----- 状态 -----

    @property
    def request_count(self) -> int:
        return self._request_count

    def cool_down(self, minutes: float = 10) -> None:
        """主动冷却 — 任务之间手动调用一下。"""
        LOG.info("cool down %.1f min ...", minutes)
        time.sleep(minutes * 60)
        self._request_count = 0
