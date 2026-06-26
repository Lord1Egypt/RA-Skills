from __future__ import annotations

from typing import Any, Protocol

from .models import PreflightReport


class PropertyListingClient(Protocol):
    source_name: str
    runtime_mode: str
    detail_supported: bool

    def doctor(self, *, run_browser_smoke: bool = True) -> PreflightReport:
        ...

    def search_property(
        self,
        *,
        keyword: str,
        country: str,
        city: str,
        lang: str,
        max_results: int,
        query_text: str = "",
        search_location: str = "",
    ) -> list[dict[str, Any]]:
        ...

    def browse_property(
        self,
        *,
        country: str,
        city: str,
        lang: str,
        max_results: int,
        query_text: str = "",
        search_location: str = "",
    ) -> list[dict[str, Any]]:
        ...

    def get_listing_detail(self, *, url: str) -> dict[str, Any]:
        ...

    def drain_warnings(self) -> list[str]:
        ...
