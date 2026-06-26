"""Contracts for parameter versions and scoring comparisons."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from hkipo_next.contracts.common import ResponseMeta
from hkipo_next.contracts.preferences import RiskProfile


ActionType = Literal["participate", "cautious", "pass"]
ParameterOperation = Literal["save", "list", "show", "use"]


class FactorWeights(BaseModel):
    model_config = ConfigDict(extra="forbid")

    snapshot_quality: float = Field(default=0.30, gt=0)
    affordability: float = Field(default=0.20, gt=0)
    pricing_stability: float = Field(default=0.15, gt=0)
    sponsor_support: float = Field(default=0.15, gt=0)
    cost_efficiency: float = Field(default=0.20, gt=0)


class DecisionThresholds(BaseModel):
    model_config = ConfigDict(extra="forbid")

    participate_min: float = Field(default=75.0, ge=0, le=100)
    cautious_min: float = Field(default=60.0, ge=0, le=100)

    @model_validator(mode="after")
    def validate_threshold_order(self) -> "DecisionThresholds":
        if self.cautious_min >= self.participate_min:
            raise ValueError("cautious_min must be lower than participate_min")
        return self


class CostModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    handling_fee_hkd: float = Field(default=100.0, ge=0)
    financing_rate_annual_pct: float = Field(default=5.5, ge=0)
    cash_opportunity_rate_annual_pct: float = Field(default=2.0, ge=0)
    lockup_days: int = Field(default=7, ge=1)


class ParameterSet(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    weights: FactorWeights = Field(default_factory=FactorWeights)
    thresholds: DecisionThresholds = Field(default_factory=DecisionThresholds)
    costs: CostModel = Field(default_factory=CostModel)
    notes: str | None = None


class ParameterVersion(ParameterSet):
    model_config = ConfigDict(extra="forbid")

    parameter_version: str
    created_at: datetime
    is_active: bool = False


class ScoreFactor(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    raw_score: float
    weight: float
    contribution: float
    reason: str


class ScoreCostBreakdown(BaseModel):
    model_config = ConfigDict(extra="forbid")

    handling_fee_hkd: float
    financing_cost_hkd: float
    opportunity_cost_hkd: float
    total_cost_hkd: float
    cost_ratio_pct: float


class ScoreSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str
    parameter_version: str
    parameter_name: str
    risk_profile: RiskProfile
    score: float
    action: ActionType
    factors: list[ScoreFactor] = Field(default_factory=list)
    cost_breakdown: ScoreCostBreakdown
    assumptions: list[str] = Field(default_factory=list)
    risk_disclosure: str
    source_issue_count: int = 0
    snapshot_overall_confidence: float | None = None
    notes: list[str] = Field(default_factory=list)


class ScoreResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: Literal[True] = True
    data: ScoreSummary
    meta: ResponseMeta


class ParametersData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    operation: ParameterOperation
    active_version: str | None = None
    parameter_set: ParameterVersion | None = None
    versions: list[ParameterVersion] = Field(default_factory=list)
    storage_path: str


class ParametersResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: Literal[True] = True
    data: ParametersData
    meta: ResponseMeta


class FactorDelta(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    baseline: float
    candidate: float
    delta: float


class ParameterComparisonData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    symbol: str
    baseline_version: str
    candidate_version: str
    baseline_score: float
    candidate_score: float
    score_delta: float
    baseline_action: ActionType
    candidate_action: ActionType
    action_changed: bool
    factor_deltas: list[FactorDelta] = Field(default_factory=list)
    active_version: str | None = None
    risk_profile: RiskProfile
    storage_path: str


class ParameterComparisonResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ok: Literal[True] = True
    data: ParameterComparisonData
    meta: ResponseMeta
