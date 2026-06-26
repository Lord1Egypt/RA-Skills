"""Contracts for profile and watchlist management."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from hkipo_next.contracts.common import ResponseMeta


ConfigSource = Literal["default", "config", "env", "cli"]
RiskProfile = Literal["conservative", "balanced", "aggressive"]
OutputFormat = Literal["json", "text", "markdown"]
FinancingPreference = Literal["cash", "margin", "auto"]
WatchlistOperation = Literal["list", "add", "remove"]


class ProfileView(BaseModel):
    model_config = ConfigDict(extra="forbid")

    risk_profile: RiskProfile = "balanced"
    default_output_format: OutputFormat = "text"
    max_budget_hkd: float = Field(default=50000.0, gt=0)
    financing_preference: FinancingPreference = "auto"
    api_token_configured: bool = False


class ProfileData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile: ProfileView
    sources: dict[str, ConfigSource] = Field(default_factory=dict)
    config_file: str
    notes: list[str] = Field(default_factory=list)


class ProfileResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: Literal[True] = True
    data: ProfileData
    meta: ResponseMeta


class WatchlistData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation: WatchlistOperation
    symbols: list[str] = Field(default_factory=list)
    changed_symbols: list[str] = Field(default_factory=list)
    total_items: int
    storage_path: str


class WatchlistResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: Literal[True] = True
    data: WatchlistData
    meta: ResponseMeta
