"""YouTube search provider."""

from __future__ import annotations

import json
import re
from urllib.parse import quote_plus

from src.errors import ErrorCode, ProviderError
from src.models import TrendItem, now_shanghai_iso
from src.providers.base import BaseProvider


class YouTubeProvider(BaseProvider):
    name = "youtube"
    source_type = "official_open_page"
    source_engine = "youtube-search-python"
    trust_level = "B"
    content_type = "video"

    def fetch_trends(self, region: str):
        if not self.offline_mode:
            return self.search(region, "trending", "24h", 10)
        topics = ["music video", "vtuber clip", "game trailer", "variety cut", "anime review"]
        return self._offline_trends(region, topics, "https://www.youtube.com/feed/trending")

    def search(self, region: str, keyword: str, time_range: str = "7d", limit: int = 10, filters: dict | None = None):
        if self.offline_mode:
            return self._offline_search(region, keyword, limit, "https://www.youtube.com")
        self._validate_region(region)
        html = self._get_text("https://www.youtube.com/results", {"search_query": keyword})
        video_ids = re.findall(r'"videoId":"([^"]+)"', html)
        titles = re.findall(r'"title":\{"runs":\[\{"text":"((?:[^"\\]|\\.)+)"', html)
        seen = set()
        items = []
        fetched_at = now_shanghai_iso()
        title_idx = 0
        for video_id in video_ids:
            if video_id in seen:
                continue
            seen.add(video_id)
            title = ""
            while title_idx < len(titles) and not title:
                try:
                    title = json.loads(f'"{titles[title_idx]}"')
                except json.JSONDecodeError:
                    title = titles[title_idx]
                title_idx += 1
            if not title:
                title = f"YouTube video {video_id}"
            items.append(
                TrendItem(
                    platform=self.name,
                    region=region,
                    title_original=self._clean_text(title),
                    title_zh=None,
                    summary_zh=title,
                    raw_url=f"https://www.youtube.com/watch?v={video_id}",
                    source_type=self.source_type,
                    source_engine=self.source_engine,
                    trust_level=self.trust_level,
                    content_type=self.content_type,
                    published_at=fetched_at,
                    fetched_at=fetched_at,
                    rank=len(items) + 1,
                    keyword=None if keyword == "trending" else keyword,
                )
            )
            if len(items) >= limit:
                break
        if not items:
            raise ProviderError(ErrorCode.PARSING_FAILED, f"no youtube result parsed for {quote_plus(keyword)}")
        return items
