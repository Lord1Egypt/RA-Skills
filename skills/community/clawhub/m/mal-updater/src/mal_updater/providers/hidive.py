from __future__ import annotations

from pathlib import Path

from ..config import AppConfig
from ..contracts import ProviderSnapshot
from ..hidive_snapshot import fetch_snapshot as fetch_hidive_snapshot
from ..hidive_snapshot import write_snapshot_file as write_hidive_snapshot_file
from ..provider_registry import register_provider
from ..provider_types import ProviderCapabilities, ProviderFetchResult


class HidiveProvider:
    slug = "hidive"
    display_name = "HIDIVE"
    capabilities = ProviderCapabilities(
        history=True,
        continue_watching=True,
        watchlists=True,
        favourites=True,
        rich_progress=True,
        token_refresh=True,
    )

    def fetch_snapshot(
        self,
        config: AppConfig,
        *,
        profile: str = "default",
        full_refresh: bool = False,
    ) -> ProviderFetchResult:
        result = fetch_hidive_snapshot(
            config,
            profile=profile,
            use_incremental_boundary=not full_refresh,
        )
        return ProviderFetchResult(
            snapshot=result.snapshot,
            metadata={
                "provider": self.slug,
                "history_count": result.history_count,
                "continue_count": result.continue_count,
                "favourite_count": result.favourite_count,
                "full_refresh_requested": full_refresh,
            },
        )

    def write_snapshot_file(self, path: Path, snapshot: ProviderSnapshot) -> Path:
        return write_hidive_snapshot_file(path, snapshot)


provider = HidiveProvider()
register_provider(provider)
