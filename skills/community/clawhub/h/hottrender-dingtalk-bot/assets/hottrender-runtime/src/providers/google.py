"""Google Trends / News provider."""

from __future__ import annotations

from email.utils import parsedate_to_datetime
from urllib.parse import quote_plus
import xml.etree.ElementTree as ET

from src.errors import ErrorCode, ProviderError
from src.models import TrendItem, now_shanghai_iso
from src.providers.base import BaseProvider


class GoogleProvider(BaseProvider):
    name = "google"
    source_type = "official_rss"
    source_engine = "google-news-rss"
    trust_level = "A"
    content_type = "text"

    def fetch_trends(self, region: str):
        if not self.offline_mode:
            return self.search(region, "trending", "24h", 10)
        topics = ["breaking news", "entertainment", "game industry", "ai products", "culture"]
        return self._offline_trends(region, topics, "https://news.google.com/rss")

    def search(self, region: str, keyword: str, time_range: str = "7d", limit: int = 10, filters: dict | None = None):
        if self.offline_mode:
            return self._offline_search(region, keyword, limit, "https://news.google.com")
        self._validate_region(region)
        if not keyword.strip():
            raise ProviderError(ErrorCode.NO_RESULT, "keyword is required")
        locale = {
            "jp": ("ja", "JP"),
            "us": ("en-US", "US"),
            "tw": ("zh-TW", "TW"),
            "kr": ("ko", "KR"),
        }[region]
        url = "https://news.google.com/rss/search"
        query = keyword if keyword != "trending" else "ニュース OR trending"
        xml_text = self._get_text(url, {"q": query, "hl": locale[0], "gl": locale[1], "ceid": f"{locale[1]}:{locale[0].split('-')[0]}"})
        root = ET.fromstring(xml_text)
        items = []
        fetched_at = now_shanghai_iso()
        for idx, node in enumerate(root.findall("./channel/item")[:limit], start=1):
            title = self._clean_text(node.findtext("title") or "")
            link = self._clean_text(node.findtext("link") or f"https://news.google.com/search?q={quote_plus(keyword)}")
            published_raw = node.findtext("pubDate") or ""
            try:
                published_at = parsedate_to_datetime(published_raw).astimezone().replace(microsecond=0).isoformat()
            except Exception:
                published_at = fetched_at
            if not title:
                continue
            items.append(
                TrendItem(
                    platform=self.name,
                    region=region,
                    title_original=title,
                    title_zh=None,
                    summary_zh=title,
                    raw_url=link,
                    source_type=self.source_type,
                    source_engine=self.source_engine,
                    trust_level=self.trust_level,
                    content_type=self.content_type,
                    published_at=published_at,
                    fetched_at=fetched_at,
                    rank=idx,
                    keyword=None if keyword == "trending" else keyword,
                )
            )
        if not items:
            raise ProviderError(ErrorCode.NO_RESULT, f"no google news result for {keyword}")
        return items
