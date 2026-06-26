"""X/Twitter provider."""

from __future__ import annotations

from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from src.errors import ErrorCode, ProviderError
from src.providers.base import BaseProvider


class XProvider(BaseProvider):
    name = "x"
    source_type = "unofficial_scraper"
    source_engine = "trends24"
    trust_level = "B"
    content_type = "text"

    _REGION_PATHS = {
        "jp": "japan",
        "us": "united-states",
        "kr": "korea",
    }

    def fetch_trends(self, region: str):
        if not self.offline_mode:
            self._validate_region(region)
            region_path = self._REGION_PATHS.get(region)
            if region_path is None:
                raise ProviderError(ErrorCode.NO_RESULT, f"X trends via trends24 not available for region '{region}'; use a different platform or region")
            html = self._get_text(f"https://trends24.in/{region_path}/")
            soup = BeautifulSoup(html, "html.parser")
            topics = [item.get_text(strip=True) for item in soup.select("ol.trend-card__list li a")]
            topics = [topic for topic in dict.fromkeys(topics) if topic]
            if not topics:
                raise ProviderError(ErrorCode.PARSING_FAILED, f"no X trends parsed for {region}")
            return [
                self._build_item(region, topic, f"https://x.com/search?q={quote_plus(topic)}&src=trend_click&f=live", idx)
                for idx, topic in enumerate(topics[:20], start=1)
            ]
        topics = ["anime trend", "game release", "idol news", "ai boyfriend", "drama talk"]
        return self._offline_trends(region, topics, "https://x.com/i/trends")

    def search(self, region: str, keyword: str, time_range: str = "7d", limit: int = 10, filters: dict | None = None):
        if self.offline_mode:
            return self._offline_search(region, keyword, limit, "https://x.com")
        self._validate_region(region)
        # Public X search is client-rendered and often unavailable without auth. Return a hard error
        # instead of fabricating results so channel validation can fail honestly.
        raise ProviderError(ErrorCode.PLATFORM_BLOCKED, "X search requires an authenticated scraper or snscrape-compatible backend")


if __name__ == "__main__":
    for item in XProvider().fetch_trends("jp"):
        print(item.to_dict())
