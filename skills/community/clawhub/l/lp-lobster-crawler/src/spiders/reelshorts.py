"""ReelShorts 爬虫 — 抓取短剧剧集信息。

注意：ReelShorts 主要通过移动 App 发布内容，网页版信息有限。
本 Spider 提供两种模式：
1. 网页模式：从网页端抓取可见内容
2. API 模式（stub）：预留 API 接口调用，需通过 App 抓包获取认证信息

当前实现为 stub 级别，待 App 抓包完成后补充完整逻辑。
"""

import json
import re
from typing import Any, Generator

import scrapy
from scrapy.http import Response

from src.spiders.base import BaseSpider
from src.spiders.items import EpisodeItem, NovelItem


class ReelShortsSpider(BaseSpider):
    """ReelShorts 短剧爬虫。"""

    name = "reelshorts"
    site_name = "reelshorts"
    allowed_domains = ["www.reelshort.com", "reelshort.com", "api.reelshort.com"]

    custom_settings = {
        "DOWNLOAD_DELAY": 3.0,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "ROBOTSTXT_OBEY": True,
    }

    def __init__(self, series_ids: str = "", mode: str = "web", *args: Any, **kwargs: Any) -> None:
        """初始化爬虫。

        Args:
            series_ids: 逗号分隔的剧集 ID 列表。
            mode: 爬取模式，"web" 或 "api"。
        """
        super().__init__(*args, **kwargs)
        self._series_ids = [sid.strip() for sid in series_ids.split(",") if sid.strip()]
        self._mode = mode

    def start_requests(self) -> Generator[scrapy.Request, None, None]:
        """生成起始请求。"""
        if self._mode == "api":
            self.logger.warning(
                "API mode requires auth token from App capture. "
                "Set request headers with valid auth before using."
            )
            # API 模式：尝试从 API 获取剧集列表
            api_url = self.get_url_pattern("series_list_api")
            if api_url:
                url = api_url.format(page=1)
                yield scrapy.Request(url=url, callback=self.parse_api_series_list)
            return

        # 网页模式
        if self._series_ids:
            for series_id in self._series_ids:
                detail_url = self._build_url("series_detail", series_id=series_id)
                if detail_url:
                    yield scrapy.Request(
                        url=detail_url,
                        callback=self.parse_series_detail,
                        meta={"series_id": series_id},
                    )
        else:
            home_url = self.get_url_pattern("home") or self.base_url
            if home_url:
                yield scrapy.Request(url=home_url, callback=self.parse_home)

    def parse_home(self, response: Response) -> Generator[Any, None, None]:
        """解析首页/列表页，提取剧集链接。"""
        selectors = self.site_config.get("selectors", {})
        series_selector = selectors.get("series_list", "")

        if series_selector:
            links = response.css(series_selector).getall()
        else:
            links = response.css('a[href*="/drama/"]::attr(href)').getall()

        for link in links:
            series_id = self._extract_series_id(link)
            if series_id:
                full_url = response.urljoin(link)
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_series_detail,
                    meta={"series_id": series_id},
                )

    def parse_series_detail(self, response: Response) -> Generator[Any, None, None]:
        """解析剧集详情页。"""
        series_id = response.meta["series_id"]
        selectors = self.site_config.get("selectors", {})

        item = NovelItem(
            site="reelshorts",
            external_id=series_id,
            title=self._css_first(response, selectors.get("series_title", ""), ""),
            summary=self._css_first(response, selectors.get("series_summary", ""), ""),
            cover_url=self._css_first(response, selectors.get("series_cover", ""), ""),
            status="ongoing",
            url=response.url,
        )
        yield item

        # 尝试从页面提取剧集信息
        # ReelShorts 网页版可能通过 JS 动态加载，这里提取页面内嵌的 JSON 数据
        scripts = response.css("script::text").getall()
        for script in scripts:
            if "episodes" in script or "videoUrl" in script:
                self._parse_embedded_episodes(script, series_id)

    def parse_api_series_list(self, response: Response) -> Generator[Any, None, None]:
        """解析 API 剧集列表响应（stub）。"""
        mapping = self.site_config.get("field_mapping", {})

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            self.logger.error("Failed to parse API series list JSON")
            return

        list_path = mapping.get("series_list_path", "data.list")
        series_list = self._get_nested(data, list_path, [])

        id_field = mapping.get("series_id_field", "id")
        title_field = mapping.get("series_title_field", "title")
        cover_field = mapping.get("series_cover_field", "coverUrl")

        for series in series_list:
            series_id = str(series.get(id_field, ""))
            if not series_id:
                continue

            yield NovelItem(
                site="reelshorts",
                external_id=series_id,
                title=series.get(title_field, ""),
                cover_url=series.get(cover_field, ""),
                status="ongoing",
            )

            # 请求剧集的 episode 列表
            episodes_url = self.get_url_pattern("episode_list_api")
            if episodes_url:
                url = episodes_url.format(series_id=series_id)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_api_episode_list,
                    meta={"series_id": series_id},
                )

    def parse_api_episode_list(self, response: Response) -> Generator[Any, None, None]:
        """解析 API 剧集 episode 列表响应（stub）。"""
        series_id = response.meta["series_id"]
        mapping = self.site_config.get("field_mapping", {})

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            self.logger.error("Failed to parse API episode list for series %s", series_id)
            return

        ep_path = mapping.get("episode_list_path", "data.episodes")
        episodes = self._get_nested(data, ep_path, [])

        id_field = mapping.get("episode_id_field", "id")
        title_field = mapping.get("episode_title_field", "title")
        url_field = mapping.get("episode_url_field", "videoUrl")
        duration_field = mapping.get("episode_duration_field", "duration")
        thumb_field = mapping.get("episode_thumbnail_field", "thumbnailUrl")

        for i, ep in enumerate(episodes):
            ep_id = str(ep.get(id_field, ""))
            if not ep_id:
                continue

            yield EpisodeItem(
                site="reelshorts",
                novel_external_id=series_id,
                external_id=ep_id,
                index=i + 1,
                title=ep.get(title_field, f"Episode {i + 1}"),
                media_url=ep.get(url_field, ""),
                duration=ep.get(duration_field, 0),
                thumbnail_url=ep.get(thumb_field, ""),
            )

    # -- 辅助方法 --

    def _build_url(self, pattern_key: str, **kwargs: str) -> str:
        """根据 URL 模式构建完整 URL。"""
        pattern = self.get_url_pattern(pattern_key)
        if not pattern:
            return ""
        try:
            return pattern.format(**kwargs)
        except KeyError:
            return ""

    def _parse_embedded_episodes(self, script_text: str, series_id: str) -> list:
        """尝试从页面内嵌 script 提取剧集数据（best effort）。"""
        # 这是一个 stub，实际需要根据页面结构调整
        self.logger.info("Attempting to extract embedded episodes for series %s", series_id)
        return []

    @staticmethod
    def _extract_series_id(url: str) -> str:
        """从 URL 中提取剧集 ID。"""
        match = re.search(r"/drama/([^/?#]+)", url)
        return match.group(1) if match else ""

    @staticmethod
    def _css_first(response: Response, selector: str, default: str = "") -> str:
        """安全获取 CSS 选择器的第一个结果。"""
        if not selector:
            return default
        result = response.css(selector).get()
        return (result or default).strip()

    @staticmethod
    def _get_nested(data: dict, path: str, default: Any = None) -> Any:
        """按点分隔路径取嵌套字典值。"""
        keys = path.split(".")
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
