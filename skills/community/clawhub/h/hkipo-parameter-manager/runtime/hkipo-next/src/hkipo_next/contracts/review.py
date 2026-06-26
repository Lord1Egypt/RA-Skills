"""Contracts for review history and export datasets."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from hkipo_next.contracts.common import ResponseMeta
from hkipo_next.contracts.preferences import RiskProfile
from hkipo_next.contracts.scoring import ActionType


ReviewCommand = Literal["score", "decision-card", "batch"]
SuggestionStatus = Literal["pending", "accepted", "rejected", "applied"]
SuggestionScope = Literal["record", "batch", "parameter-set", "rule"]


class ReviewActualResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    allocated_lots: int | None = Field(default=None, ge=0)
    listing_return_pct: float | None = None
    exit_return_pct: float | None = None
    realized_pnl_hkd: float | None = None
    exited_at: datetime | None = None
    notes: str | None = None


class ReviewRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    record_id: str
    command: ReviewCommand
    command_run_id: str
    batch_id: str | None = None
    symbol: str
    created_at: datetime
    parameter_version: str
    parameter_name: str | None = None
    risk_profile: RiskProfile
    decision: ActionType
    score: float
    data_status: Literal["complete", "partial"] = "complete"
    rule_version: str
    schema_version: str
    source_issue_count: int = 0
    prediction_payload: dict[str, Any] = Field(default_factory=dict)
    actual_result: ReviewActualResult | None = None
    actual_updated_at: datetime | None = None
    variance_note: str | None = None
    variance_updated_at: datetime | None = None


class ReviewRecordRevision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    revision_id: str
    record_id: str
    updated_at: datetime
    actual_result: ReviewActualResult | None = None
    variance_note: str | None = None


class ReviewListData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_items: int
    items: list[ReviewRecord] = Field(default_factory=list)
    storage_path: str


class ReviewListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: Literal[True] = True
    data: ReviewListData
    meta: ResponseMeta


class ReviewDetailData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    record: ReviewRecord
    revisions: list[ReviewRecordRevision] = Field(default_factory=list)
    storage_path: str


class ReviewDetailResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: Literal[True] = True
    data: ReviewDetailData
    meta: ResponseMeta


class ReviewExportFilters(BaseModel):
    model_config = ConfigDict(extra="forbid")

    from_date: datetime | None = None
    to_date: datetime | None = None
    limit: int | None = Field(default=None, ge=1)


class ReviewExportData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    generated_at: datetime
    export_path: str
    filters: ReviewExportFilters
    total_items: int
    records: list[ReviewRecord] = Field(default_factory=list)
    storage_path: str


class ReviewExportResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: Literal[True] = True
    data: ReviewExportData
    meta: ResponseMeta


class SuggestionChange(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field_path: str
    current_value: Any | None = None
    suggested_value: Any
    reason: str | None = None


class ImportedSuggestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    suggestion_id: str
    record_id: str | None = None
    batch_id: str | None = None
    impact_scope: SuggestionScope
    title: str
    summary: str
    rationale: str | None = None
    suggested_changes: list[SuggestionChange] = Field(default_factory=list)


class OpenClawSuggestionFile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str = "openclaw"
    batch_id: str | None = None
    suggestions: list[ImportedSuggestion] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_targets(self) -> "OpenClawSuggestionFile":
        for suggestion in self.suggestions:
            if suggestion.record_id is None and suggestion.batch_id is None and self.batch_id is None:
                raise ValueError("suggestion must include record_id or batch_id")
        return self


class ReviewSuggestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    suggestion_id: str
    source: str
    record_id: str | None = None
    batch_id: str | None = None
    impact_scope: SuggestionScope
    title: str
    summary: str
    rationale: str | None = None
    suggested_changes: list[SuggestionChange] = Field(default_factory=list)
    status: SuggestionStatus = "pending"
    imported_at: datetime


class ResolvedSuggestionChange(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field_path: str
    current_value: Any | None = None
    suggested_value: Any
    will_change: bool
    reason: str | None = None


class SuggestionAdoption(BaseModel):
    model_config = ConfigDict(extra="forbid")

    suggestion_id: str
    decision: Literal["accepted", "rejected"]
    decided_at: datetime
    decision_note: str | None = None
    before_parameter_version: str | None = None
    after_parameter_version: str | None = None
    applied_changes: list[ResolvedSuggestionChange] = Field(default_factory=list)


class SuggestionListData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_items: int
    items: list[ReviewSuggestion] = Field(default_factory=list)
    storage_path: str


class SuggestionListResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: Literal[True] = True
    data: SuggestionListData
    meta: ResponseMeta


class SuggestionImportData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_file: str
    imported_count: int
    items: list[ReviewSuggestion] = Field(default_factory=list)
    storage_path: str


class SuggestionImportResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: Literal[True] = True
    data: SuggestionImportData
    meta: ResponseMeta


class SuggestionDetailData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    suggestion: ReviewSuggestion
    current_parameter_version: str | None = None
    preview_changes: list[ResolvedSuggestionChange] = Field(default_factory=list)
    adoption: SuggestionAdoption | None = None
    storage_path: str


class SuggestionDetailResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: Literal[True] = True
    data: SuggestionDetailData
    meta: ResponseMeta
