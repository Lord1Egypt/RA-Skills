"""Runtime paths and profile loading with source precedence tracing."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import SecretStr

from hkipo_next.config.profile import LoadedProfile, ProfileRepository, StoredProfile


PROFILE_ENV_MAP = {
    "risk_profile": "HKIPO_RISK_PROFILE",
    "default_output_format": "HKIPO_DEFAULT_OUTPUT_FORMAT",
    "max_budget_hkd": "HKIPO_MAX_BUDGET_HKD",
    "financing_preference": "HKIPO_FINANCING_PREFERENCE",
}
SENSITIVE_ENV_MAP = {
    "api_token": "HKIPO_API_TOKEN",
}
PROFILE_FIELDS = tuple(PROFILE_ENV_MAP)


@dataclass(frozen=True)
class RuntimePaths:
    """Resolved runtime paths for config and state."""

    root: Path
    config_dir: Path
    data_dir: Path
    artifacts_dir: Path
    review_artifacts_dir: Path
    profile_file: Path
    watchlist_file: Path
    sqlite_file: Path


def resolve_runtime_paths(home: str | Path | None = None) -> RuntimePaths:
    root = Path(home or os.getenv("HKIPO_HOME") or (Path.home() / ".hkipo-next")).expanduser()
    config_dir = root / "config"
    data_dir = root / "data"
    artifacts_dir = root / "artifacts"
    return RuntimePaths(
        root=root,
        config_dir=config_dir,
        data_dir=data_dir,
        artifacts_dir=artifacts_dir,
        review_artifacts_dir=artifacts_dir / "review",
        profile_file=config_dir / "profile.json",
        watchlist_file=config_dir / "watchlist.json",
        sqlite_file=data_dir / "hkipo.db",
    )


class ProfileLoader:
    """Merge profile values from config, env, and CLI with traceability."""

    def __init__(self, *, runtime_paths: RuntimePaths | None = None):
        self.paths = runtime_paths or resolve_runtime_paths()
        self.repository = ProfileRepository(self.paths.profile_file)

    def load(self, *, cli_overrides: dict[str, Any] | None = None) -> LoadedProfile:
        values = StoredProfile().model_dump()
        sources = {field_name: "default" for field_name in PROFILE_FIELDS}
        cli_overrides = {
            field_name: value
            for field_name, value in (cli_overrides or {}).items()
            if value is not None and field_name in PROFILE_FIELDS
        }

        raw_config = self.repository.read_raw()
        if raw_config:
            stored_profile = StoredProfile.model_validate(raw_config)
            for field_name in PROFILE_FIELDS:
                if field_name in raw_config:
                    values[field_name] = getattr(stored_profile, field_name)
                    sources[field_name] = "config"

        for field_name, env_name in PROFILE_ENV_MAP.items():
            env_value = os.getenv(env_name)
            if env_value in (None, ""):
                continue
            parsed = StoredProfile.model_validate({field_name: env_value})
            values[field_name] = getattr(parsed, field_name)
            sources[field_name] = "env"

        for field_name, value in cli_overrides.items():
            parsed = StoredProfile.model_validate({field_name: value})
            values[field_name] = getattr(parsed, field_name)
            sources[field_name] = "cli"

        api_token_value = None
        if api_token := os.getenv(SENSITIVE_ENV_MAP["api_token"]):
            api_token_value = SecretStr(api_token)
            sources["api_token"] = "env"

        return LoadedProfile(
            **values,
            api_token=api_token_value,
            sources=sources,
            config_file=str(self.paths.profile_file),
        )
