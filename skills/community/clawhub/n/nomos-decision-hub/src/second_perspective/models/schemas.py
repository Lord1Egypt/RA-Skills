from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .enums import (
    AlternativeStatus,
    AssumptionSource,
    AssumptionState,
    ConstraintKind,
    ConstraintOperator,
    ConvergenceKind,
    CounterfactualStatus,
    DecisionStatus,
    EvaluationMode,
    EvidenceStatus,
    InteractionEffectType,
    IssueSeverity,
    ReconstructionKind,
    ScoringRule,
    SessionStatus,
)


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class ResponsibilityRef(StrictModel):
    owner: str = Field(min_length=1, description="Smallest accountable person or organizational role.")
    role: str | None = None
    source: str = Field(min_length=1, description="Document, policy, instruction, or record assigning responsibility.")
    authorization_ref: str | None = None


class EvidenceQuality(StrictModel):
    """Explicit evidence-quality assessment; values are never inferred by the engine."""

    reliability: Decimal = Field(ge=Decimal("0"), le=Decimal("1"))
    relevance: Decimal = Field(ge=Decimal("0"), le=Decimal("1"))
    independence: Decimal = Field(ge=Decimal("0"), le=Decimal("1"))
    freshness: Decimal = Field(ge=Decimal("0"), le=Decimal("1"))
    assessed_by: ResponsibilityRef
    method: str = Field(min_length=1)

    @property
    def composite_score(self) -> Decimal:
        return (
            self.reliability
            + self.relevance
            + self.independence
            + self.freshness
        ) / Decimal("4")


class Evidence(StrictModel):
    id: str = Field(pattern=r"^E[0-9A-Za-z_-]+$")
    statement: str = Field(min_length=1)
    source: str = Field(min_length=1)
    status: EvidenceStatus = EvidenceStatus.SUPPLIED
    observed_at: datetime | None = None
    valid_until: datetime | None = None
    quality: EvidenceQuality | None = None
    content_hash: str | None = Field(default=None, pattern=r"^[0-9a-fA-F]{64}$")
    responsibility: ResponsibilityRef

    @model_validator(mode="after")
    def validate_timeline(self) -> "Evidence":
        for field_name in ("observed_at", "valid_until"):
            value = getattr(self, field_name)
            if value is not None and value.utcoffset() is None:
                raise ValueError(f"{field_name} must include a timezone offset")
        if (
            self.observed_at is not None
            and self.valid_until is not None
            and self.valid_until <= self.observed_at
        ):
            raise ValueError("valid_until must be later than observed_at")
        return self


class Criterion(StrictModel):
    id: str = Field(pattern=r"^K[0-9A-Za-z_-]+$")
    name: str = Field(min_length=1)
    metric: str = Field(min_length=1)
    weight: Decimal = Field(ge=Decimal("0"), le=Decimal("1"))
    scoring_rule: ScoringRule
    min_value: Decimal
    max_value: Decimal
    target_value: Decimal | None = None
    responsibility: ResponsibilityRef

    @model_validator(mode="after")
    def validate_range(self) -> "Criterion":
        if self.max_value <= self.min_value:
            raise ValueError("criterion max_value must be greater than min_value")
        if self.scoring_rule == ScoringRule.TARGET_IS_BETTER and self.target_value is None:
            raise ValueError("target_value is required for target_is_better")
        if self.target_value is not None and not (
            self.min_value <= self.target_value <= self.max_value
        ):
            raise ValueError("target_value must be inside the criterion range")
        return self


class Constraint(StrictModel):
    id: str = Field(pattern=r"^C[0-9A-Za-z_-]+$")
    name: str = Field(min_length=1)
    kind: ConstraintKind
    metric: str = Field(min_length=1)
    operator: ConstraintOperator
    expected: Any
    penalty: Decimal | None = Field(
        default=None,
        gt=Decimal("0"),
        le=Decimal("1"),
        description="Explicit score deduction for a failed soft constraint.",
    )
    responsibility: ResponsibilityRef

    @model_validator(mode="after")
    def validate_penalty(self) -> "Constraint":
        if self.kind == ConstraintKind.SOFT and self.penalty is None:
            raise ValueError("soft constraints require an explicit penalty")
        if self.kind == ConstraintKind.HARD and self.penalty is not None:
            raise ValueError("hard constraints must not define a penalty")
        return self


class Assumption(StrictModel):
    id: str = Field(pattern=r"^A[0-9A-Za-z_-]+$")
    statement: str = Field(min_length=1)
    source: AssumptionSource
    falsification_condition: str = Field(min_length=1)
    critical: bool = True
    dependencies: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    responsibility: ResponsibilityRef | None = None


class Alternative(StrictModel):
    id: str = Field(pattern=r"^S[0-9A-Za-z_-]+$")
    name: str = Field(min_length=1)
    description: str | None = None
    metrics: dict[str, Any] = Field(default_factory=dict)
    required_assumptions: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)


class InteractionDecl(StrictModel):
    """A single declared interaction between two or more assumptions.

    The interaction strength Δ is *always* explicitly declared — the engine
    never estimates or learns it.  A positive Δ means conjunctive amplification
    (joint failure is worse than the sum), a negative Δ means disjunctive
    redundancy (joint failure is less severe than the sum).
    """

    id: str = Field(pattern=r"^I[0-9A-Za-z_-]+$", description="交互声明 ID")
    member_ids: list[str] = Field(
        min_length=2,
        description="参与交互的假设 ID 列表（至少 2 个）",
    )
    interaction_strength: Decimal = Field(description="交互强度 Δ，由责任人显式声明")
    effect_type: InteractionEffectType = Field(
        default=InteractionEffectType.CONJUNCTIVE,
        description="交互效果类型：放大/冗余/退化",
    )
    responsibility: ResponsibilityRef | None = None

    @model_validator(mode="after")
    def _dedupe_members(self) -> "InteractionDecl":
        if len(self.member_ids) != len(set(self.member_ids)):
            raise ValueError(f"interaction {self.id} has duplicate member_ids")
        return self


class InteractionDeclaration(StrictModel):
    """Full interaction declaration block attached to a DecisionRequest.

    When absent, the engine behaves exactly like v0.3 (first-order only).
    """

    interactions: list[InteractionDecl] = Field(
        default_factory=list,
        description="已声明的假设间交互列表",
    )
    first_order_effects: dict[str, Decimal] = Field(
        default_factory=dict,
        description="每个假设的一阶失效效应 {assumption_id: effect}",
    )
    amplification_ceiling: Decimal = Field(
        default=Decimal("2.0"),
        gt=Decimal("0"),
        description="累计交互效应上限系数（相对于一阶效应绝对值之和的倍数）",
    )

    @model_validator(mode="after")
    def _validate_members_in_first_order(self) -> "InteractionDeclaration":
        fo_set = set(self.first_order_effects.keys())
        for inter in self.interactions:
            unknown = set(inter.member_ids) - fo_set
            if unknown:
                raise ValueError(
                    f"interaction {inter.id} references assumptions without "
                    f"declared first-order effects: {sorted(unknown)}"
                )
        # I-3 效应有界性预校验：所有交互强度之和不得超过 ceiling × Σ|一阶|
        total_fo_abs = sum((abs(v) for v in self.first_order_effects.values()), Decimal("0"))
        ceiling_total = self.amplification_ceiling * total_fo_abs
        total_inter = sum(abs(inter.interaction_strength) for inter in self.interactions)
        if total_inter > ceiling_total and self.interactions:
            raise ValueError(
                f"total interaction magnitude {total_inter} exceeds "
                f"amplification ceiling {ceiling_total} "
                f"(ceiling={self.amplification_ceiling})"
            )
        return self


class ResourceBudget(StrictModel):
    """单项资源预算：budget = 可用额度，used = 已承诺/已耗。

    对应 ⊙ORI 的「能量守恒」检查：gap = budget - used 为负即违反守恒。
    两者都为 None 时 ORI 会记「缺少可用/已承诺字段」而不做估算——
    缺就是缺，不补默认值。
    """

    name: str = Field(min_length=1)
    budget: float | None = None
    used: float | None = None
    unit: str | None = None


class DecisionOrigin(StrictModel):
    """本次决策的原点事件——「为什么是现在要决策」。

    企业语义：立项申请 / 预算请求 / 风险事件 / 董事会决议 / 客户投诉 / 系统告警。
    它是 ⊙ORI 的输入。不声明则 ORI 不参与审计（见 adapter 的条件注册），
    因为「NOMOS 无法表达原点」与「这次决策真的没有原点」是两件不同的事，
    不该由审计算子去猜。
    """

    trigger: str = Field(min_length=1, description="触发本次决策的具体事件")
    source: str | None = Field(default=None, description="触发来源：谁或哪个系统提出的")
    event_time: datetime | None = None
    resources: list[ResourceBudget] = Field(default_factory=list)


class RolloutStage(StrictModel):
    """灰度阶梯中的一档。ratio 为该档的放量比例（0..1）。"""

    name: str = Field(min_length=1)
    ratio: float = Field(ge=0.0, le=1.0)
    gate: str | None = Field(default=None, description="进入下一档的前置条件")


class DecisionRollout(StrictModel):
    """放量阶梯与现实反馈——「怎么落地、落地后现实怎么说」。

    企业语义：试点 → 分批 → 全量。它是 ⇄GRF 的输入。
    注意并非所有决策都有阶梯：一次性决策（批准/否决一笔预算）本来就没有，
    此时不声明本字段，GRF 也就不会去报一个假阳性。
    """

    stages: list[RolloutStage] = Field(default_factory=list)
    current_ratio: float | None = Field(default=None, ge=0.0, le=1.0,
                                        description="当前放量比例")
    feedback: dict[str, str] = Field(
        default_factory=dict,
        description="现实反馈：假设（或前置因）-> 观测结论",
    )


class DecisionRequest(StrictModel):
    decision_id: str | None = Field(default=None, pattern=r"^DEC-[0-9A-Za-z_-]+$")
    objective: str = Field(min_length=1)
    decision_owner: ResponsibilityRef
    time_horizon: str | None = None
    evaluation_as_of: datetime | None = Field(
        default=None,
        description="Explicit replay time used for temporal evidence checks.",
    )
    evaluation_mode: EvaluationMode = EvaluationMode.CONSTRAINT_ONLY
    criteria: list[Criterion] = Field(default_factory=list)
    constraints: list[Constraint] = Field(default_factory=list)
    assumptions: list[Assumption] = Field(default_factory=list)
    alternatives: list[Alternative] = Field(min_length=1)
    evidence: list[Evidence] = Field(default_factory=list)
    interaction_declaration: InteractionDeclaration | None = Field(
        default=None,
        description="可选：假设交互声明。不传则为一阶失效（v0.3 行为）。",
    )
    origin: DecisionOrigin | None = Field(
        default=None,
        description="可选：本次决策的原点事件。声明后 ⊙ORI 算子参与审计；"
                    "不声明则 ORI 不注册（无法表达 ≠ 真的没有）。",
    )
    rollout: DecisionRollout | None = Field(
        default=None,
        description="可选：放量阶梯与现实反馈。声明后 ⇄GRF 算子参与审计；"
                    "一次性决策本就没有阶梯，不声明即不审。",
    )
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_references(self) -> "DecisionRequest":
        if self.evaluation_as_of is not None and self.evaluation_as_of.utcoffset() is None:
            raise ValueError("evaluation_as_of must include a timezone offset")

        collections = {
            "criteria": [item.id for item in self.criteria],
            "constraints": [item.id for item in self.constraints],
            "assumptions": [item.id for item in self.assumptions],
            "alternatives": [item.id for item in self.alternatives],
            "evidence": [item.id for item in self.evidence],
        }
        for name, ids in collections.items():
            if len(ids) != len(set(ids)):
                raise ValueError(f"duplicate IDs in {name}")

        assumption_ids = set(collections["assumptions"])
        evidence_ids = set(collections["evidence"])

        for assumption in self.assumptions:
            unknown_dependencies = set(assumption.dependencies) - assumption_ids
            if unknown_dependencies:
                raise ValueError(
                    f"assumption {assumption.id} references unknown dependencies: "
                    f"{sorted(unknown_dependencies)}"
                )
            unknown_evidence = set(assumption.evidence_ids) - evidence_ids
            if unknown_evidence:
                raise ValueError(
                    f"assumption {assumption.id} references unknown evidence: "
                    f"{sorted(unknown_evidence)}"
                )

        for alternative in self.alternatives:
            unknown_assumptions = set(alternative.required_assumptions) - assumption_ids
            if unknown_assumptions:
                raise ValueError(
                    f"alternative {alternative.id} references unknown assumptions: "
                    f"{sorted(unknown_assumptions)}"
                )
            unknown_evidence = set(alternative.evidence_ids) - evidence_ids
            if unknown_evidence:
                raise ValueError(
                    f"alternative {alternative.id} references unknown evidence: "
                    f"{sorted(unknown_evidence)}"
                )

        # Interaction member references must exist in assumptions
        if self.interaction_declaration is not None:
            for inter in self.interaction_declaration.interactions:
                unknown_members = set(inter.member_ids) - assumption_ids
                if unknown_members:
                    raise ValueError(
                        f"interaction {inter.id} references unknown assumptions: "
                        f"{sorted(unknown_members)}"
                    )

        if self.evaluation_mode == EvaluationMode.WEIGHTED:
            if not self.criteria:
                raise ValueError("weighted evaluation requires at least one criterion")
            total = sum((criterion.weight for criterion in self.criteria), Decimal("0"))
            if abs(total - Decimal("1")) > Decimal("0.000001"):
                raise ValueError(f"criterion weights must sum to 1; received {total}")
        return self


class AuditIssue(StrictModel):
    code: str
    severity: IssueSeverity
    path: str
    message: str
    blocking: bool = False


class ConstraintCheck(StrictModel):
    constraint_id: str
    passed: bool | None
    actual: Any = None
    expected: Any = None
    reason: str


class CriterionScore(StrictModel):
    criterion_id: str
    actual: Decimal
    normalized_score: Decimal
    weighted_score: Decimal


class AlternativeEvaluation(StrictModel):
    alternative_id: str
    status: AlternativeStatus
    hard_constraints_passed: bool
    constraint_checks: list[ConstraintCheck]
    criterion_scores: list[CriterionScore] = Field(default_factory=list)
    base_score: Decimal | None = None
    soft_constraint_penalty: Decimal = Decimal("0")
    total_score: Decimal | None = None
    missing_metrics: list[str] = Field(default_factory=list)
    unavailable_evidence_ids: list[str] = Field(default_factory=list)


class FailureBranch(StrictModel):
    assumption_id: str
    expression: str
    invalidated_assumption_ids: list[str] = Field(default_factory=list)
    affected_alternative_ids: list[str]
    affected_leading_candidate_ids: list[str]
    candidate_exposure_ratio: Decimal
    structural_effect: str
    triggered_interaction_ids: list[str] = Field(
        default_factory=list,
        description="该失效分支触发的交互声明 ID 列表",
    )
    interaction_contribution: Decimal | None = Field(
        default=None,
        description="交互效应对该分支的额外贡献量（Δ），None 表示未启用交互层",
    )


class ResponsibilityEntry(StrictModel):
    element_type: str
    element_id: str
    owner: str | None
    source: str | None
    status: str


class SensitivityCase(StrictModel):
    criterion_id: str
    direction: str
    adjusted_weight: Decimal
    adjusted_weights: dict[str, Decimal] = Field(default_factory=dict)
    alternative_scores: dict[str, Decimal] = Field(default_factory=dict)
    leading_candidate_ids: list[str]


class RobustnessReport(StrictModel):
    pareto_frontier_ids: list[str] = Field(default_factory=list)
    sensitivity_cases: list[SensitivityCase] = Field(default_factory=list)
    fragile_criterion_ids: list[str] = Field(default_factory=list)
    stable_leader_ids: list[str] = Field(default_factory=list)
    ranking_stability: Decimal | None = None


class TraceEntry(StrictModel):
    stage: str
    rule_id: str
    message: str
    references: list[str] = Field(default_factory=list)


class AlgorithmAuditEvent(StrictModel):
    sequence: int = Field(ge=1)
    stage: str = Field(min_length=1)
    rule_id: str = Field(min_length=1)
    operation: str = Field(min_length=1)
    inputs: dict[str, Any] = Field(default_factory=dict)
    output: Any = None
    references: list[str] = Field(default_factory=list)
    previous_event_hash: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    event_hash: str = Field(pattern=r"^[0-9a-f]{64}$")


class CounterfactualResult(StrictModel):
    trigger_assumption_id: str
    status: CounterfactualStatus
    invalidated_assumption_ids: list[str]
    removed_alternative_ids: list[str]
    remaining_eligible_alternative_ids: list[str]
    baseline_leading_candidate_ids: list[str]
    counterfactual_leading_candidate_ids: list[str]
    counterfactual_pareto_frontier_ids: list[str]
    decision_changed: bool


class PolicySnapshot(StrictModel):
    policy_id: str
    version: str
    require_all_alternatives_complete: bool
    require_critical_evidence_quality: bool
    critical_evidence_quality_threshold: Decimal
    sensitivity_delta: Decimal


class DecisionResult(StrictModel):
    decision_id: str
    status: DecisionStatus
    objective: str
    evaluation_mode: EvaluationMode
    audit_passed: bool
    issues: list[AuditIssue]
    alternatives: list[AlternativeEvaluation]
    eligible_alternative_ids: list[str]
    leading_candidate_ids: list[str]
    failure_branches: list[FailureBranch]
    responsibility_map: list[ResponsibilityEntry]
    unresolved_variables: list[str]
    robustness: RobustnessReport = Field(default_factory=RobustnessReport)
    counterfactuals: list[CounterfactualResult] = Field(default_factory=list)
    trace: list[TraceEntry] = Field(default_factory=list)
    algorithm_audit: list[AlgorithmAuditEvent] = Field(default_factory=list)
    algorithm_audit_root_hash: str | None = Field(
        default=None,
        pattern=r"^[0-9a-f]{64}$",
    )
    policy: PolicySnapshot
    engine_version: str
    input_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    evaluation_as_of: datetime
    human_approval_required: bool = True
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ApprovalRequest(StrictModel):
    approved: bool
    approver: str = Field(min_length=1)
    authorization_ref: str = Field(min_length=1)
    note: str | None = None


class ApprovalRecord(StrictModel):
    approved: bool
    approver: str
    authorization_ref: str
    note: str | None = None
    approved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DecisionRecord(StrictModel):
    request: DecisionRequest
    result: DecisionResult
    approval: ApprovalRecord | None = None
    revision: int = Field(default=1, ge=1)
    parent_record_hash: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    record_hash: str = Field(default="", pattern=r"^$|^[0-9a-f]{64}$")


# ── Causal Reconstruction Models ──────────────────────────────────────


class DeviationSignal(StrictModel):
    """经营变量偏差信号，由感知层推送至决策层。

    代表一个可观测的指标偏离，携带来源管道标识符以便审计追溯。
    """

    metric: str = Field(min_length=1, description="偏离指标名，对应 Criterion.metric 或 Alternative.metrics 的 key")
    observed: Any = Field(description="观测值")
    baseline: Any = Field(description="基线/预期值，用于判定偏离方向")
    direction: str = Field(pattern=r"^(above|below|anomaly)$", description="偏离方向")
    observed_at: datetime = Field(description="观测时间点，必须带时区")
    source: str = Field(min_length=1, description="感知管道标识符，用于审计追溯")

    @model_validator(mode="after")
    def validate_timezone(self) -> "DeviationSignal":
        if self.observed_at.utcoffset() is None:
            raise ValueError("observed_at must include a timezone offset")
        return self


class RootCauseHypothesis(StrictModel):
    """候选根因假设。

    每条假设声明一个可能的根因假设节点，附带追溯出的因果链、
    可解释的偏差信号、缺失信息以及推荐验证动作。
    引擎不判定哪条假设"正确"——这是人类审批者的权力。
    """

    id: str = Field(pattern=r"^RH-[0-9A-Za-z_-]+$")
    root_assumption_id: str = Field(description="候选根因——依赖图中最上游的失效假设 ID")
    causal_chain: list[str] = Field(
        description="从根因到观测信号的节点序列 root -> ... -> observed-effect"
    )
    explained_signals: list[str] = Field(
        description="该假设可解释的偏差信号的 metric 名"
    )
    missing_evidence_ids: list[str] = Field(
        default_factory=list,
        description="确认或排除该假设所需的、当前缺失的证据 ID",
    )
    verification_action: str = Field(
        min_length=1, description="推荐的人类验证动作"
    )
    dependency_depth: int = Field(ge=0, description="依赖链深度（根因到最远观测的距离）")
    severity: IssueSeverity = Field(description="根因影响严重度")


class CausalReconstructionReport(StrictModel):
    """因果重构推演报告。

    包含一组候选根因假设和追溯过程的审计信息。
    报告本身不声称确定性结论——它是一份结构化的诊断输入，
    供决策者验证后使用。
    """

    reconstruction_id: str = Field(pattern=r"^REC-[0-9A-Za-z_-]+$")
    hypotheses: list[RootCauseHypothesis] = Field(default_factory=list)
    signal_count: int = Field(ge=0, description="输入的偏差信号总数")
    root_candidate_count: int = Field(ge=0, description="去重后的根因候选数")
    unresolved_branches: list[str] = Field(
        default_factory=list,
        description="因信息真空无法继续追溯的假设 ID",
    )
    algorithm_audit: list[AlgorithmAuditEvent] = Field(default_factory=list)
    algorithm_audit_root_hash: str | None = Field(
        default=None, pattern=r"^[0-9a-f]{64}$"
    )
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ── Three-Layer Reconstruction Session Models ──────────────────────────


class DeltaVar(StrictModel):
    """A declared correction variable injected into delta reconstruction.

    `path` targets an element of the decision structure (e.g. an assumption
    falsification, a criterion weight, an alternative metric). The engine
    applies it verbatim — it never invents corrections itself.
    """

    path: str = Field(min_length=1, description="修正路径，如 'A2'、'criteria.K1.weight'、'alternatives.S1.metrics.cost'")
    value: Any = Field(description="修正后的值")
    reason: str = Field(min_length=1, description="修正理由（由人类声明，引擎不推断）")
    responsibility: ResponsibilityRef | None = None


class ConvergenceReport(StrictModel):
    """Third-layer result: what changes when declared delta_vars are applied."""

    kind: ConvergenceKind = Field(description="收敛类型：fixed_point / no_gain / budget")
    reconstruction_id: str = Field(pattern=r"^REC-[0-9A-Za-z_-]+$")
    delta_vars: list[DeltaVar] = Field(default_factory=list)
    before_leading_candidate_ids: list[str] = Field(default_factory=list)
    after_leading_candidate_ids: list[str] = Field(default_factory=list)
    candidate_set_changed: bool = Field(description="应用 delta 后领先候选集合是否变化")
    invalidated_assumption_ids: list[str] = Field(default_factory=list)
    is_converged: bool = Field(description="是否已到达收敛点")
    reason: str = Field(min_length=1, description="人类可读的收敛/停止说明")
    algorithm_audit: list[AlgorithmAuditEvent] = Field(default_factory=list)
    algorithm_audit_root_hash: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")


class SessionRound(StrictModel):
    """One iteration of a reconstruction session (all three layers executed)."""

    round_index: int = Field(ge=0)
    kind: ReconstructionKind = Field(description="本轮主导的重构层")
    invalidated_assumption_ids: list[str] = Field(default_factory=list)
    hypotheses: list[RootCauseHypothesis] = Field(default_factory=list)
    unresolved_branches: list[str] = Field(default_factory=list)
    convergence: ConvergenceReport | None = None
    applied_delta_vars: list[DeltaVar] = Field(default_factory=list)
    assumption_states: dict[str, AssumptionState] = Field(default_factory=dict)
    round_root_hash: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    previous_round_hash: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    requires_human_decision: bool = True


# ── Cognitive Audit Models ────────────────────────────────────────────


class CognitiveRiskFinding(StrictModel):
    """A single structural cognitive risk finding."""

    code: str = Field(min_length=1, description="风险代码，如 ANCHORING、CONFIRMATION_BIAS")
    severity: IssueSeverity
    description: str = Field(min_length=1, description="风险描述")
    affected_elements: list[str] = Field(default_factory=list, description="受影响的结构元素路径")
    recommendation: str = Field(default="", description="推荐缓解措施")


class CognitiveAuditReport(StrictModel):
    """Structured cognitive audit report."""

    findings: list[CognitiveRiskFinding] = Field(default_factory=list)
    total_findings: int = Field(ge=0)
    scanner_version: str = Field(min_length=1)


# ── Scenario Models ────────────────────────────────────────────────────


class ScenarioDefinition(StrictModel):
    """A declared stress scenario for re-running the evaluation."""

    id: str = Field(min_length=1, description="场景标识符")
    name: str = Field(min_length=1, description="场景名称")
    description: str | None = None
    failed_assumption_ids: list[str] = Field(default_factory=list)
    metric_overrides: dict[str, dict[str, object]] = Field(
        default_factory=dict,
        description="{alternative_id: {metric_name: value}}",
    )


class ReconstructionSession(StrictModel):
    """A bounded, hash-chained, human-gated reconstruction session.

    Replaces single-shot reconstruction with an iterative process: each round
    runs forward propagation → backward tracing → delta reconstruction, records
    all events into a session-level hash chain, and pauses for a human decision.
    The session converges when no new information is produced, or stops when an
    explicit budget is exhausted.
    """

    session_id: str = Field(pattern=r"^SESS-[0-9A-Za-z_-]+$")
    request: DecisionRequest
    deviation_signals: list[DeviationSignal] = Field(default_factory=list)
    rounds: list[SessionRound] = Field(default_factory=list)
    assumption_states: dict[str, AssumptionState] = Field(default_factory=dict)
    status: SessionStatus = SessionStatus.ACTIVE
    convergence_kind: ConvergenceKind | None = None
    max_iterations: int = Field(default=5, ge=1, description="最大推演轮次预算")
    max_evidence_requests: int = Field(default=20, ge=1, description="最大证据请求预算")
    session_root_hash: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sealed_at: datetime | None = None
