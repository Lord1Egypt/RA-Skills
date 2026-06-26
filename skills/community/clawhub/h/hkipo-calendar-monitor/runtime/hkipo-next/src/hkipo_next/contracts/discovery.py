"""Discovery-specific contracts."""

from __future__ import annotations

from datetime import date
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from hkipo_next.contracts.common import ResponseMeta


WindowType = Literal["deadline", "listing"]
DiscoverySeverity = Literal["warning", "error"]
DataStatus = Literal["complete", "partial"]


class DiscoveryFilter(BaseModel):
    model_config = ConfigDict(extra="forbid")

    window: WindowType
    days: int


class DiscoveryIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str
    source: str
    message: str
    severity: DiscoverySeverity = "warning"
    details: dict[str, Any] = Field(default_factory=dict)


class DiscoveryItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str | None = None
    name: str
    deadline_date: date | None = None
    listing_date: date | None = None
    entry_fee_hkd: float | None = None
    total_margin_hkd_100m: float | None = None
    source_tags: list[str] = Field(default_factory=list)
    data_status: DataStatus = "complete"
    degradation_reason: str | None = None


class DiscoveryData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    filter: DiscoveryFilter
    items: list[DiscoveryItem]
    issues: list[DiscoveryIssue] = Field(default_factory=list)
    total_items: int


class DiscoveryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: Literal[True] = True
    data: DiscoveryData
    meta: ResponseMeta
