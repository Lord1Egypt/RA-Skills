"""Profile storage and typed views."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, SecretStr

from hkipo_next.contracts.preferences import (
    ConfigSource,
    FinancingPreference,
    OutputFormat,
    ProfileView,
    RiskProfile,
)


class StoredProfile(BaseModel):
    """Persisted profile values stored on disk."""

    model_config = ConfigDict(extra="forbid")

    risk_profile: RiskProfile = "balanced"
    default_output_format: OutputFormat = "text"
    max_budget_hkd: float = Field(default=50000.0, gt=0)
    financing_preference: FinancingPreference = "auto"


class LoadedProfile(StoredProfile):
    """Effective profile after merging config, env, and CLI values."""

    api_token: SecretStr | None = Field(default=None, exclude=True)
    sources: dict[str, ConfigSource] = Field(default_factory=dict, exclude=True)
    config_file: str = Field(default="", exclude=True)

    def to_view(self) -> ProfileView:
        return ProfileView(
            risk_profile=self.risk_profile,
            default_output_format=self.default_output_format,
            max_budget_hkd=self.max_budget_hkd,
            financing_preference=self.financing_preference,
            api_token_configured=self.api_token is not None,
        )


class ProfileRepository:
    """Persist non-sensitive profile values to a JSON file."""

    def __init__(self, path: Path):
        self.path = path

    def read_raw(self) -> dict[str, object]:
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def read(self) -> StoredProfile:
        raw = self.read_raw()
        if not raw:
            return StoredProfile()
        return StoredProfile.model_validate(raw)

    def save(self, profile: StoredProfile) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(profile.model_dump(mode="json"), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def update(self, updates: dict[str, object]) -> StoredProfile:
        current = self.read()
        updated = current.model_copy(update=updates)
        profile = StoredProfile.model_validate(updated.model_dump())
        self.save(profile)
        return profile
