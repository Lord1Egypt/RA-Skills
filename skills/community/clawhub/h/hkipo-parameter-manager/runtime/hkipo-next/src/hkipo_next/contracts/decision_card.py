"""Contracts for decision cards and batch output."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from hkipo_next.contracts.common import ResponseMeta
from hkipo_next.contracts.errors import AppError
from hkipo_next.contracts.preferences import RiskProfile
from hkipo_next.contracts.scoring import ActionType, ScoreCostBreakdown


BatchSource = Literal["symbols", "watchlist", "mixed"]
PositionMode = Literal["cash", "margin", "watch-only"]


class PositionSuggestion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    position_size_pct: float
    suggested_budget_hkd: float
    subscription_mode: PositionMode


class ExitPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    take_profit_pct: float
    stop_loss_pct: float
    max_holding_days: int
    note: str


class DecisionCardData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str
    decision: ActionType
    headline: str
    score: float
    parameter_version: str
    risk_profile: RiskProfile
    position_suggestion: PositionSuggestion
    exit_plan: ExitPlan
    top_reasons: list[str] = Field(default_factory=list)
    risk_disclosure: str
    cost_breakdown: ScoreCostBreakdown
    source_issue_count: int = 0


class DecisionCardResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: Literal[True] = True
    data: DecisionCardData
    meta: ResponseMeta


class BatchItemResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str
    ok: bool
    decision_card: DecisionCardData | None = None
    error: AppError | None = None
    data_status: Literal["complete", "partial", "error"] = "complete"


class BatchSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_items: int
    success_count: int
    partial_count: int
    failure_count: int


class BatchData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: BatchSource
    items: list[BatchItemResult] = Field(default_factory=list)
    summary: BatchSummary
    active_parameter_version: str | None = None
    risk_profile: RiskProfile


class BatchResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: Literal[True] = True
    data: BatchData
    meta: ResponseMeta
