"""Provider interface and shared helpers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from html import unescape
from urllib.parse import quote_plus

import requests

from src.errors import ErrorCode, ProviderError
from src.models import TrendItem, now_shanghai_iso


SUPPORTED_REGIONS = {"jp", "us", "tw", "kr"}


class BaseProvider(ABC):
    name: str
    source_type: str
    source_engine: str
    trust_level: str
    content_type: str

    def __init__(self, config: dict | None = None):
        self.config = config or {}

    @property
    def offline_mode(self) -> bool:
        return str(self.config.get("mode", "real")).lower() == "offline"

    @property
    def timeout_seconds(self) -> float:
        try:
            return float(self.config.get("timeout_seconds", 20))
        except (TypeError, ValueError):
            return 20.0

    @abstractmethod
    def fetch_trends(self, region: str) -> list[TrendItem]:
        """Fetch trend inventory for one region."""

    @abstractmethod
    def search(
        self,
        region: str,
        keyword: str,
        time_range: str = "7d",
        limit: int = 10,
        filters: dict | None = None,
    ) -> list[TrendItem]:
        """Search platform content by keyword."""

    def healthcheck(self) -> dict:
        return {"status": "ok", "message": f"{self.name} provider ready"}

    def _validate_region(self, region: str) -> None:
        if region not in SUPPORTED_REGIONS:
            raise ProviderError(ErrorCode.NO_RESULT, f"unsupported region: {region}")

    def _build_item(
        self,
        region: str,
        title: str,
        url: str,
        rank: int | None = None,
        keyword: str | None = None,
        content_type: str | None = None,
    ) -> TrendItem:
        timestamp = now_shanghai_iso()
        return TrendItem(
            platform=self.name,
            region=region,
            title_original=title,
            title_zh=None,
            summary_zh=title,
            raw_url=url,
            source_type=self.source_type,
            source_engine=self.source_engine,
            trust_level=self.trust_level,
            content_type=content_type or self.content_type,
            published_at=timestamp,
            fetched_at=timestamp,
            rank=rank,
            keyword=keyword,
        )

    def _get_text(self, url: str, params: dict | None = None) -> str:
        try:
            response = requests.get(
                url,
                params=params,
                headers={
                    "User-Agent": self.config.get(
                        "user_agent",
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/122.0 Safari/537.36",
                    ),
                    "Accept-Language": self.config.get("accept_language", "ja,en-US;q=0.9,en;q=0.8"),
                },
                timeout=self.timeout_seconds,
            )
        except requests.Timeout as exc:
            raise ProviderError(ErrorCode.TARGET_TIMEOUT, f"{self.name} request timeout") from exc
        except requests.RequestException as exc:
            raise ProviderError(ErrorCode.PROXY_UNREACHABLE, str(exc)) from exc
        if response.status_code in {401, 403}:
            raise ProviderError(ErrorCode.PLATFORM_BLOCKED, f"{self.name} returned {response.status_code}")
        if response.status_code == 429:
            raise ProviderError(ErrorCode.RATE_LIMITED, f"{self.name} returned 429")
        if not 200 <= response.status_code < 300:
            raise ProviderError(ErrorCode.PARSING_FAILED, f"{self.name} returned {response.status_code}")
        configured_encoding = str(self.config.get("encoding", "")).strip()
        if configured_encoding:
            response.encoding = configured_encoding
        elif not response.encoding or response.encoding.lower() in {"iso-8859-1", "windows-1252"}:
            response.encoding = "utf-8"
        return response.text

    @staticmethod
    def _clean_text(value: str) -> str:
        return " ".join(unescape(value).replace("\\u0026", "&").split())

    def _offline_trends(self, region: str, topics: list[str], base_url: str) -> list[TrendItem]:
        self._validate_region(region)
        return [
            self._build_item(region, f"{region.upper()} {topic}", f"{base_url}/{region}/{quote_plus(topic)}", idx)
            for idx, topic in enumerate(topics, start=1)
        ]

    def _offline_search(self, region: str, keyword: str, limit: int, base_url: str) -> list[TrendItem]:
        self._validate_region(region)
        if not keyword.strip():
            raise ProviderError(ErrorCode.NO_RESULT, "keyword is required")
        return [
            self._build_item(
                region,
                f"{keyword} related {self.name} result {idx}",
                f"{base_url}/search/{region}/{quote_plus(keyword)}/{idx}",
                idx,
                keyword=keyword,
            )
            for idx in range(1, limit + 1)
        ]
