"""Snapshot-specific contracts."""

from __future__ import annotations

from datetime import date
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from hkipo_next.contracts.common import ResponseMeta


SnapshotSeverity = Literal["warning", "error"]


class SnapshotIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str
    source: str
    message: str
    severity: SnapshotSeverity = "warning"
    details: dict[str, Any] = Field(default_factory=dict)


class SnapshotFieldSource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field_name: str
    source: str


class SnapshotConflictValue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str
    value: str


class SnapshotConflict(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field_name: str
    selected_source: str
    selected_value: str
    alternatives: list[SnapshotConflictValue] = Field(default_factory=list)


class SnapshotFieldConfidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field_name: str
    confidence: float


class SnapshotQuality(BaseModel):
    model_config = ConfigDict(extra="forbid")

    missing_fields: list[str] = Field(default_factory=list)
    conflicts: list[SnapshotConflict] = Field(default_factory=list)
    field_confidence: list[SnapshotFieldConfidence] = Field(default_factory=list)
    overall_confidence: float


class SnapshotData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str
    company_name: str | None = None
    industry: str | None = None
    sponsors: list[str] = Field(default_factory=list)
    offer_price_floor: float | None = None
    offer_price_ceiling: float | None = None
    lot_size: int | None = None
    entry_fee_hkd: float | None = None
    deadline_date: date | None = None
    listing_date: date | None = None
    source_priority: list[str] = Field(default_factory=list)
    field_sources: list[SnapshotFieldSource] = Field(default_factory=list)
    issues: list[SnapshotIssue] = Field(default_factory=list)
    quality: SnapshotQuality | None = None


class SnapshotResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: Literal[True] = True
    data: SnapshotData
    meta: ResponseMeta
