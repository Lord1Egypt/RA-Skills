"""TikTok provider using TikTok-Api (Playwright-based non-official API)."""

from __future__ import annotations

import asyncio
import json
import logging
import os
from dataclasses import replace
from typing import Any

from src.errors import ErrorCode, ProviderError
from src.models import TrendItem, now_shanghai_iso
from src.providers.base import BaseProvider


class TikTokProvider(BaseProvider):
    """TikTok 热点抓取，基于 trend-stack/TikTok-Api。

    需要安装 playwright 并执行 ``playwright install`` 以获取浏览器二进制文件。
    """

    name = "tiktok"
    source_type = "unofficial_scraper"
    source_engine = "tiktok-api"
    trust_level = "B"
    content_type = "video"

    def __init__(self, config: dict | None = None):
        super().__init__(config)
        self._logger: logging.Logger | None = None

    @property
    def logger(self) -> logging.Logger:
        if self._logger is None:
            self._logger = logging.getLogger(f"providers.{self.name}")
        return self._logger

    def fetch_trends(self, region: str):
        if self.offline_mode:
            return self._offline_trends(region, ["trending video", "dance challenge", "short drama"], "https://www.tiktok.com/tag")
        return asyncio.run(self._fetch_trends_async(region))

    def search(self, region: str, keyword: str, time_range: str = "7d", limit: int = 10, filters: dict | None = None):
        if self.offline_mode:
            return self._offline_search(region, keyword, limit, "https://www.tiktok.com")
        self._validate_region(region)
        return asyncio.run(self._search_async(region, keyword, limit, filters))

    # ---- 异步内部实现 ----

    async def _fetch_trends_async(self, region: str) -> list[TrendItem]:
        """通过 TikTok-Api trending.videos 获取候选视频，并按点赞量重排。"""
        api = await self._make_api()
        items: list[TrendItem] = []
        fetched_at = now_shanghai_iso()
        candidate_count = self._config_int("trend_candidate_count", 30)
        limit = self._config_int("trend_limit", 10)
        try:
            async for video in api.trending.videos(count=candidate_count):
                item = self._video_to_item(video, region, fetched_at)
                if item:
                    items.append(item)
                if len(items) >= candidate_count:
                    break
        finally:
            await api.close_sessions()
        if not items:
            raise ProviderError(
                ErrorCode.PLATFORM_BLOCKED,
                "TikTok returned empty; configure ms_token/cookies in providers.yaml or set TIKTOK_MS_TOKEN env var",
            )
        return self._rank_by_likes(items)[:limit]

    async def _search_async(self, region: str, keyword: str, limit: int, filters: dict | None) -> list[TrendItem]:
        """通过 TikTok-Api search.search_type('item') 搜索视频。"""
        api = await self._make_api()
        items: list[TrendItem] = []
        fetched_at = now_shanghai_iso()
        try:
            async for video in api.search.search_type(keyword, "item", count=limit):
                item = self._video_to_item(video, region, fetched_at, keyword=keyword, rank=len(items) + 1)
                if item:
                    items.append(item)
                if len(items) >= limit:
                    break
        finally:
            await api.close_sessions()
        if not items:
            raise ProviderError(
                ErrorCode.PLATFORM_BLOCKED,
                f"TikTok search for '{keyword}' returned empty; configure ms_token/cookies in providers.yaml or set TIKTOK_MS_TOKEN env var",
            )
        return items

    # ---- 视频对象转换 ----

    def _video_to_item(self, video, region: str, fetched_at: str, keyword: str | None = None, rank: int | None = None) -> TrendItem | None:
        """将 TikTok-Api Video 对象转换为 TrendItem。"""
        try:
            video_data = getattr(video, "as_dict", {}) or {}
            video_id = getattr(video, "id", None) or video_data.get("id", "")
            if not video_id:
                return None

            # author — TikTok-Api 的 User 对象 unique_id 属性可能为 None，需从 as_dict 取
            author = getattr(video, "author", None)
            username = ""
            if author:
                username = getattr(author, "unique_id", None) or getattr(author, "username", None) or ""
                if not username and hasattr(author, "as_dict") and author.as_dict:
                    username = author.as_dict.get("uniqueId", "")
            if not username:
                username = video_data.get("author", {}).get("uniqueId", "")

            # title
            title = video_data.get("desc", "") or f"TikTok video {video_id}"

            # URL
            raw_url = f"https://www.tiktok.com/@{username}/video/{video_id}" if username else f"https://www.tiktok.com/video/{video_id}"

            # stats
            stats = getattr(video, "stats", None) or video_data.get("stats", {})

            return TrendItem(
                platform=self.name,
                region=region,
                title_original=self._clean_text(title),
                title_zh=None,
                summary_zh="",
                raw_url=raw_url,
                source_type=self.source_type,
                source_engine=self.source_engine,
                trust_level=self.trust_level,
                content_type=self.content_type,
                published_at=fetched_at,
                fetched_at=fetched_at,
                rank=rank,
                keyword=keyword,
                meta_json=self._safe_json({"region": region, "stats": stats}),
            )
        except Exception as exc:
            self.logger.warning(f"TikTok video conversion failed: {exc}")
            return None

    # ---- 辅助方法 ----

    @staticmethod
    def _safe_json(obj: Any) -> str:
        try:
            return json.dumps(obj, ensure_ascii=False, default=str)
        except (TypeError, ValueError):
            return "{}"

    def _config_int(self, key: str, default: int) -> int:
        try:
            value = int(self.config.get(key, default))
        except (TypeError, ValueError):
            return default
        return value if value > 0 else default

    @classmethod
    def _rank_by_likes(cls, items: list[TrendItem]) -> list[TrendItem]:
        sorted_items = sorted(
            enumerate(items),
            key=lambda entry: (-cls._item_stat_int(entry[1], "diggCount"), entry[0]),
        )
        return [replace(item, rank=rank) for rank, (_, item) in enumerate(sorted_items, start=1)]

    @staticmethod
    def _item_stat_int(item: TrendItem, key: str) -> int:
        if not item.meta_json:
            return 0
        try:
            payload = json.loads(item.meta_json)
        except (TypeError, ValueError):
            return 0
        stats = payload.get("stats") if isinstance(payload, dict) else None
        if not isinstance(stats, dict):
            return 0
        raw_value = stats.get(key, 0)
        try:
            return int(float(str(raw_value).replace(",", "").strip() or 0))
        except (TypeError, ValueError):
            return 0

    # ---- TikTok-Api 工厂 ----

    async def _make_api(self):
        """从 TikTokApi 包创建 TikTokApi 实例并初始化 session。"""
        from TikTokApi import TikTokApi
        from playwright.async_api import TimeoutError as PlaywrightTimeout

        api = TikTokApi(logging_level=30)  # WARNING level
        extra = self._get_provider_extra()
        proxy = extra.get("proxy")
        ms_token = extra.get("ms_token") or os.environ.get("TIKTOK_MS_TOKEN", "")
        cookies = extra.get("cookies")

        kwargs: dict[str, Any] = {
            "num_sessions": 1,
            "headless": True,
            "browser": "webkit",  # webkit 比 chromium 更难被检测
            "sleep_after": 3,  # 等 3 秒让 TikTok JS 写入 msToken cookie
        }
        if ms_token:
            kwargs["ms_tokens"] = [ms_token]
        if cookies:
            kwargs["cookies"] = cookies if isinstance(cookies, list) else [cookies]
        if proxy:
            proxy_str = str(proxy).replace("http://", "").replace("https://", "")
            proxy_parts = proxy_str.split("@")
            if len(proxy_parts) == 2:
                auth, host_port = proxy_parts
                host, port = host_port.split(":", 1)
                user, pwd = auth.split(":", 1)
                kwargs["proxies"] = [{"server": f"http://{host}:{port}", "username": user, "password": pwd}]
            else:
                host_port = proxy_parts[0]
                host, port = host_port.split(":", 1)
                kwargs["proxies"] = [{"server": f"http://{host}:{port}"}]
        try:
            # Monkey-patch page 方法和默认超时：跨境网络下 load/networkidle 事件太慢
            import playwright.async_api._generated as _pw_gen
            _orig_goto = _pw_gen.Page.goto  # type: ignore
            _orig_wait = _pw_gen.Page.wait_for_load_state  # type: ignore
            _orig_new_page = _pw_gen.BrowserContext.new_page  # type: ignore

            async def _fast_goto(self, url: str, **kw):
                kw["wait_until"] = kw.get("wait_until", "domcontentloaded")
                kw["timeout"] = kw.get("timeout", 90000)
                return await _orig_goto(self, url, **kw)

            async def _fast_wait(self, state: str = "load", **kw):
                # networkidle 在跨境网络下几乎不可能达成，改为 domcontentloaded
                if state == "networkidle":
                    state = "domcontentloaded"
                kw["timeout"] = kw.get("timeout", 90000)
                return await _orig_wait(self, state, **kw)

            async def _new_page_with_timeout(self):
                page = await _orig_new_page(self)
                page.set_default_timeout(90000)
                page.set_default_navigation_timeout(90000)
                return page

            _pw_gen.Page.goto = _fast_goto  # type: ignore
            _pw_gen.Page.wait_for_load_state = _fast_wait  # type: ignore
            _pw_gen.BrowserContext.new_page = _new_page_with_timeout  # type: ignore
            self.logger.info("TikTok monkey-patch applied: goto/wait_for_load_state + 90s timeout")
            try:
                await api.create_sessions(**kwargs)
            finally:
                _pw_gen.Page.goto = _orig_goto  # type: ignore
                _pw_gen.Page.wait_for_load_state = _orig_wait  # type: ignore
                _pw_gen.BrowserContext.new_page = _orig_new_page  # type: ignore

            # 验证 msToken 是否自动获取成功
            if api.sessions:
                session = api.sessions[0]
                if session.ms_token:
                    self.logger.info(f"TikTok msToken auto-acquired: {session.ms_token[:20]}...")
                else:
                    self.logger.warning("TikTok msToken not acquired from cookies, requests may fail")
        except PlaywrightTimeout as exc:
            await api.close_sessions()
            hint = "请在 providers.yaml 配置代理，或设置 TIKTOK_MS_TOKEN 环境变量"
            raise ProviderError(ErrorCode.TARGET_TIMEOUT, f"TikTok session creation timeout: {hint}") from exc
        except Exception as exc:
            try:
                await api.close_sessions()
            except Exception:
                pass
            hint = "请在 providers.yaml 配置代理，或设置 TIKTOK_MS_TOKEN 环境变量"
            raise ProviderError(ErrorCode.PLATFORM_BLOCKED, f"TikTok session error: {exc}. {hint}") from exc
        return api

    def _get_provider_extra(self) -> dict:
        """从 providers.yaml 读取 tiktok 配置段。"""
        from src.config import load_provider_config

        return load_provider_config().get("tiktok", {})
