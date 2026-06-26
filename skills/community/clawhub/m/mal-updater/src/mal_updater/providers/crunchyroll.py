from __future__ import annotations

from pathlib import Path

from ..config import AppConfig
from ..contracts import ProviderSnapshot
from ..crunchyroll_snapshot import fetch_snapshot as fetch_crunchyroll_snapshot
from ..crunchyroll_snapshot import write_snapshot_file as write_crunchyroll_snapshot_file
from ..provider_registry import register_provider
from ..provider_types import ProviderCapabilities, ProviderFetchResult


class CrunchyrollProvider:
    slug = "crunchyroll"
    display_name = "Crunchyroll"
    capabilities = ProviderCapabilities(
        history=True,
        watchlists=True,
        rich_progress=True,
        incremental_boundaries=True,
        token_refresh=True,
    )

    def fetch_snapshot(
        self,
        config: AppConfig,
        *,
        profile: str = "default",
        full_refresh: bool = False,
    ) -> ProviderFetchResult:
        result = fetch_crunchyroll_snapshot(
            config,
            profile=profile,
            use_incremental_boundary=not full_refresh,
        )
        return ProviderFetchResult(
            snapshot=result.snapshot,
            metadata={
                "provider": self.slug,
                "used_incremental_boundary": not full_refresh,
                "account_email": result.account_email,
                "state_paths": {
                    "root": str(result.state_paths.root),
                    "refresh_token_path": str(result.state_paths.refresh_token_path),
                    "device_id_path": str(result.state_paths.device_id_path),
                    "session_state_path": str(result.state_paths.session_state_path),
                    "sync_boundary_path": str(result.state_paths.sync_boundary_path),
                },
            },
        )

    def write_snapshot_file(self, path: Path, snapshot: ProviderSnapshot) -> Path:
        return write_crunchyroll_snapshot_file(path, snapshot)


provider = CrunchyrollProvider()
register_provider(provider)
