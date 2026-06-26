"""Webnovel 爬虫 — 抓取小说书籍/章节内容。

工作流程：
1. 从书城列表页（/stories/novel）抓取书籍链接
2. 解析书籍详情页获取元信息
3. 从 catalog 页面解析章节目录
"""

import re
from typing import Any, Generator

import scrapy
from scrapy.http import Response

from src.spiders.base import BaseSpider
from src.spiders.items import ChapterItem, NovelItem


class WebnovelSpider(BaseSpider):
    """Webnovel 小说爬虫。"""

    name = "webnovel"
    site_name = "webnovel"
    allowed_domains = ["www.webnovel.com", "webnovel.com"]

    custom_settings = {
        "DOWNLOAD_DELAY": 2.0,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 4,
    }

    def __init__(self, book_ids: str = "", *args: Any, **kwargs: Any) -> None:
        """初始化爬虫。

        Args:
            book_ids: 逗号分隔的书籍 ID 列表。为空则从排行榜爬取。
        """
        super().__init__(*args, **kwargs)
        self._book_ids = [bid.strip() for bid in book_ids.split(",") if bid.strip()]

    def start_requests(self) -> Generator[scrapy.Request, None, None]:
        """生成起始请求。"""
        if self._book_ids:
            # 指定书籍 ID 模式：直接抓取章节列表
            for book_id in self._book_ids:
                detail_url = self._build_url("book_detail", book_id=book_id)
                yield scrapy.Request(
                    url=detail_url,
                    callback=self.parse_book_detail,
                    meta={"book_id": book_id, "use_impersonate": True},
                )
        else:
            # 排行榜模式：从排行榜页面开始
            ranking_url = self.get_url_pattern("ranking")
            if ranking_url:
                yield scrapy.Request(
                    url=ranking_url,
                    callback=self.parse_ranking,
                    meta={"use_impersonate": True},
                )

    def parse_ranking(self, response: Response) -> Generator[Any, None, None]:
        """解析书城列表页，提取书籍链接。"""
        selectors = self.site_config.get("selectors", {})
        book_selector = selectors.get("book_list", "")

        if book_selector:
            book_links = response.css(book_selector).getall()
        else:
            # 回退：匹配 /book/ 或 /zh/book/ 模式的链接
            book_links = response.css(
                'a[href*="/book/"]::attr(href)'
            ).getall()

        # 去重（页面上同一本书可能出现多个链接）
        seen_ids: set[str] = set()
        for link in book_links:
            book_id = self._extract_book_id(link)
            if book_id and book_id not in seen_ids:
                seen_ids.add(book_id)
                full_url = response.urljoin(link)
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_book_detail,
                    meta={"book_id": book_id, "use_impersonate": True},
                )

    def parse_book_detail(self, response: Response) -> Generator[Any, None, None]:
        """解析书籍详情页，产出 NovelItem 并发起章节目录请求。"""
        book_id = response.meta["book_id"]
        selectors = self.site_config.get("selectors", {})

        item = NovelItem(
            site="webnovel",
            external_id=book_id,
            title=self._css_first(response, selectors.get("book_title", ""), ""),
            author=self._css_first(response, selectors.get("book_author", ""), ""),
            category=self._css_first(response, selectors.get("book_category", ""), ""),
            summary=self._css_first(response, selectors.get("book_summary", ""), ""),
            cover_url=self._css_first(response, selectors.get("book_cover", ""), ""),
            status=self._css_first(response, selectors.get("book_status", ""), "ongoing"),
            url=response.url,
        )
        yield item

        # 请求章节目录页（旧 API 已失效，改用 catalog HTML 页面）
        catalog_url = self._build_url("catalog", book_id=book_id)
        if catalog_url:
            yield scrapy.Request(
                url=catalog_url,
                callback=self.parse_catalog,
                meta={"book_id": book_id, "use_impersonate": True},
            )

    def parse_catalog(self, response: Response) -> Generator[Any, None, None]:
        """解析章节目录页，提取章节列表。

        Webnovel 的 catalog 页面以 volume-item 分卷，每卷内有章节链接。
        链接格式：/zh/book/{slug}_{bookId}/{chapterSlug}_{chapterId}
        """
        book_id = response.meta["book_id"]
        chapter_links = response.css("div.volume-item a[href*='/book/']")

        seen_ids: set[str] = set()
        index = 0
        for link in chapter_links:
            href = link.attrib.get("href", "")
            chapter_id = self._extract_chapter_id(href)
            if not chapter_id or chapter_id in seen_ids:
                continue

            seen_ids.add(chapter_id)
            index += 1

            # 章节标题：取链接文本，清理序号和时间后缀
            raw_texts = link.css("::text").getall()
            title = " ".join(t.strip() for t in raw_texts if t.strip())
            title = self._clean_chapter_title(title)

            yield ChapterItem(
                site="webnovel",
                novel_external_id=book_id,
                external_id=chapter_id,
                index=index,
                title=title or f"Chapter {index}",
            )

        self.logger.info(
            "Parsed %d chapters from catalog for book %s", len(seen_ids), book_id
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

    @staticmethod
    def _extract_book_id(url: str) -> str:
        """从 URL 中提取书籍 ID。

        支持格式：
        - /book/{slug}_{id}  (英文版)
        - /zh/book/{slug}_{id}  (中文版)
        - /book/{id}  (旧格式，兼容)
        """
        # 新格式：slug_数字ID
        match = re.search(r"/book/[^/]*?_(\d+)", url)
        if match:
            return match.group(1)
        # 旧格式：纯数字 ID
        match = re.search(r"/book/(\d+)", url)
        return match.group(1) if match else ""

    @staticmethod
    def _extract_chapter_id(url: str) -> str:
        """从章节 URL 中提取章节 ID。

        格式：/zh/book/{slug}_{bookId}/{chapterSlug}_{chapterId}
        """
        match = re.search(r"_(\d+)$", url)
        return match.group(1) if match else ""

    @staticmethod
    def _clean_chapter_title(title: str) -> str:
        """清理章节标题中的序号前缀和时间后缀。

        输入示例：'1 第一章 绯红 7 years ago'
        输出：'第一章 绯红'
        """
        # 移除开头的纯数字序号
        title = re.sub(r"^\d+\s+", "", title)
        # 移除末尾的时间标记（如 "7 years ago", "3 months ago"）
        title = re.sub(r"\s+\d+\s+(?:year|month|week|day|hour|minute)s?\s+ago\s*$", "", title)
        return title.strip()

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
