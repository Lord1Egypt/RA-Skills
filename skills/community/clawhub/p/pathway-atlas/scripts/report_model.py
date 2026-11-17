"""Immutable evidence-aware report model and pure Markdown renderer.

This module is deliberately file- and network-free.  It snapshots only the
privacy-minimal public contracts emitted by the deterministic engine; report
renderers project those decisions and never recalculate them.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from datetime import date
from enum import Enum
import hashlib
import json
import re
from typing import Any, Iterable

if __package__:
    from .contracts import (
        CapabilityReport,
        CapabilityTier,
        EvidenceManifest,
        EvidenceStatus,
        OrdinaryBatchPolicy,
        RecommendationItem,
        RecommendationResult,
        SchoolObservation,
    )
    from .action_plan import ActionItem, build_action_plan
    from .planning_profile import PlanningProfile
    from .path_recommend import (
        PATHWAY_DISPLAY_EVIDENCE_FIELDS,
        PathwayFieldEvidence,
        PathwayItem,
        PathwayResult,
        validate_pathway_display_evidence,
        validate_pathway_field_evidence,
        validate_public_output_text,
    )
    from .rank_calc import RankEstimate
    from .rank_locator import RankScenario
    from .school_recommend import SchoolDecisionResult
    from .validate_evidence import ValidatedEvidenceSnapshot
else:  # pragma: no cover - direct scripts-path compatibility
    from contracts import (
        CapabilityReport,
        CapabilityTier,
        EvidenceManifest,
        EvidenceStatus,
        OrdinaryBatchPolicy,
        RecommendationItem,
        RecommendationResult,
        SchoolObservation,
    )
    from action_plan import ActionItem, build_action_plan
    from planning_profile import PlanningProfile
    from path_recommend import (
        PATHWAY_DISPLAY_EVIDENCE_FIELDS,
        PathwayFieldEvidence,
        PathwayItem,
        PathwayResult,
        validate_pathway_display_evidence,
        validate_pathway_field_evidence,
        validate_public_output_text,
    )
    from rank_calc import RankEstimate
    from rank_locator import RankScenario
    from school_recommend import SchoolDecisionResult
    from validate_evidence import ValidatedEvidenceSnapshot


_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_SESSION_ID = re.compile(r"^[0-9a-f]{32}$")
_HASH = re.compile(r"^sha256:[0-9a-f]{64}$")
_REASON = re.compile(r"^[a-z][a-z0-9_-]{0,127}$")
_TRACE_FIELD = re.compile(r"^[a-z][a-z0-9_.]{0,127}$")
_SUBJECT_MODES = frozenset({"3+1+2", "3+3"})
_GRADES = frozenset({"高一", "高二", "高三"})
_ACCEPTED_EXACT = frozenset(
    {
        EvidenceStatus.OFFICIAL,
        EvidenceStatus.CORROBORATED,
        EvidenceStatus.REFERENCE,
    }
)
_ACCEPTED_STRENGTH = {
    EvidenceStatus.REFERENCE: 1,
    EvidenceStatus.CORROBORATED: 2,
    EvidenceStatus.OFFICIAL: 3,
}
_STATUS_PRECEDENCE = (
    EvidenceStatus.CONFLICT,
    EvidenceStatus.MASKED,
    EvidenceStatus.PARTIAL,
    EvidenceStatus.MISSING,
    EvidenceStatus.INFERRED,
    EvidenceStatus.REFERENCE,
    EvidenceStatus.CORROBORATED,
    EvidenceStatus.OFFICIAL,
)
_STATUS_LABEL = {
    EvidenceStatus.OFFICIAL: "官方",
    EvidenceStatus.CORROBORATED: "多源核验",
    EvidenceStatus.REFERENCE: "多源参考",
    EvidenceStatus.INFERRED: "推断",
    EvidenceStatus.CONFLICT: "冲突",
    EvidenceStatus.MISSING: "缺失",
    EvidenceStatus.MASKED: "屏蔽",
    EvidenceStatus.PARTIAL: "部分覆盖",
}
_TIER_LABEL = {
    CapabilityTier.FULL: "完整档",
    CapabilityTier.STANDARD: "标准档",
    CapabilityTier.OFFLINE: "离线档",
}
_CONFIDENCE_LABEL = {
    EvidenceStatus.OFFICIAL: "高",
    EvidenceStatus.CORROBORATED: "高",
    EvidenceStatus.REFERENCE: "中",
    EvidenceStatus.INFERRED: "中",
    EvidenceStatus.PARTIAL: "低",
    EvidenceStatus.MISSING: "无",
    EvidenceStatus.MASKED: "无",
    EvidenceStatus.CONFLICT: "无",
}
_COVERAGE_LABEL = {
    "complete": "完整",
    "partial": "部分覆盖",
    "missing": "缺失",
    "conflict": "冲突",
}
_PATHWAY_FIELD_LABEL = {
    "title": "路径",
    "institution": "院校",
    "status": "运行状态",
    "eligibility": "资格代码",
    "investment_decision": "投入结论",
    "qualification_status": "资格状态",
    "evidence_status": "政策证据状态",
    "policy_source_ids": "政策来源编号",
    "source_ids": "政策来源编号",
    "professional_options": "专业选项",
    "training_arrangements": "培养安排",
    "transition_rules": "转段规则",
    "outcomes": "毕业/升学出口",
    "service_employment_obligations": "服务/就业义务",
    "penalty_exit_rules": "退出/违约规则",
    "fees_and_subsidies": "费用/补助",
    "satisfied_conditions": "已满足条件",
    "missing_constraints": "待核实约束",
    "timeline": "时间线",
    "preparation_actions": "当前行动",
    "decision_reasons": "决策理由",
    "calculation_basis": "计算依据",
    "target_rank": "路径目标位次",
    "target_year": "目标年份",
    "data_year": "数据年份",
    "fallback_distance": "回溯年距",
    "year_basis": "年份依据",
}
_QUERY_COVERAGE = {
    CapabilityTier.FULL: "联网检索、网页读取与视觉识别能力可用",
    CapabilityTier.STANDARD: "联网文本与结构化附件可用，图片表格可能未覆盖",
    CapabilityTier.OFFLINE: "仅使用本地或用户提供的已验证证据包",
}
_HOST_CAPABILITIES = frozenset({"search", "browse", "vision"})
_OPTIONAL_MODULES = frozenset({"docx", "openpyxl", "pdfplumber"})


def _json_safe(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if is_dataclass(value) and hasattr(value, "to_dict"):
        return value.to_dict()
    raise TypeError(f"unsupported report value: {type(value).__name__}")


class _Serializable:
    def to_dict(self) -> dict[str, Any]:
        return {
            item.name: _json_safe(getattr(self, item.name))
            for item in fields(self)
        }


def _positive_int(value: Any, name: str, *, minimum: int = 1) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} is below its minimum")
    return value


def _nonnegative_int(value: Any, name: str) -> int:
    return _positive_int(value, name, minimum=0)


def _privacy_safe(value: str, *, profile_text: bool = False) -> bool:
    try:
        validate_public_output_text(value)
    except ValueError:
        return False
    return True


def _text(
    value: Any,
    name: str,
    *,
    optional: bool = False,
    profile_text: bool = False,
) -> str | None:
    if value is None and optional:
        return None
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value or value != value.strip():
        raise ValueError(f"{name} must be a non-empty trimmed string")
    if len(value) > 2048 or any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ValueError(f"{name} must be a bounded single-line string")
    if not _privacy_safe(value, profile_text=profile_text):
        raise ValueError(f"{name} contains private or non-public content")
    return value


def validate_profile_text(value: Any, name: str = "profile_text") -> str:
    """Validate one caller-provided profile string without retaining PII."""

    result = _text(value, name, profile_text=True)
    assert result is not None
    return result


def _text_tuple(
    value: Any,
    name: str,
    *,
    safe_ids: bool = False,
    unique: bool = False,
    sort: bool = False,
    profile_text: bool = False,
) -> tuple[str, ...]:
    if isinstance(value, (str, bytes, bytearray)):
        raise TypeError(f"{name} must be a collection of strings")
    try:
        items = tuple(value)
    except TypeError as error:
        raise TypeError(f"{name} must be a collection of strings") from error
    normalized: list[str] = []
    for item in items:
        text = _text(item, f"{name} item", profile_text=profile_text)
        assert text is not None
        if safe_ids and _SAFE_ID.fullmatch(text) is None:
            raise ValueError(f"{name} contains an unsafe ID")
        normalized.append(text)
    if unique and len(normalized) != len(set(normalized)):
        raise ValueError(f"{name} must contain unique values")
    if sort:
        normalized.sort()
    return tuple(normalized)


def _year_tuple(value: Any, name: str) -> tuple[int, ...]:
    if isinstance(value, (str, bytes, bytearray)):
        raise TypeError(f"{name} must be a collection of years")
    try:
        years = tuple(value)
    except TypeError as error:
        raise TypeError(f"{name} must be a collection of years") from error
    for year in years:
        _positive_int(year, f"{name} item", minimum=2000)
        if year > 2100:
            raise ValueError(f"{name} item exceeds 2100")
    if len(years) != len(set(years)):
        raise ValueError(f"{name} must contain unique years")
    return tuple(sorted(years))


def _date_tuple(
    value: Any,
    name: str,
    *,
    allow_empty: bool = False,
) -> tuple[str, ...]:
    values = _text_tuple(value, name, unique=True, sort=True)
    if not values and not allow_empty:
        raise ValueError(f"{name} must not be empty")
    for item in values:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", item) is None:
            raise ValueError(f"{name} must contain ISO calendar dates")
        try:
            date.fromisoformat(item)
        except ValueError as error:
            raise ValueError(f"{name} contains an invalid calendar date") from error
    return values


def _status(value: Any, name: str = "status") -> EvidenceStatus:
    if isinstance(value, EvidenceStatus):
        return value
    if not isinstance(value, str):
        raise TypeError(f"{name} must be an EvidenceStatus")
    try:
        return EvidenceStatus(value)
    except ValueError as error:
        raise ValueError(f"{name} is unsupported") from error


def _capability_tier(value: Any) -> CapabilityTier:
    if isinstance(value, CapabilityTier):
        return value
    if not isinstance(value, str):
        raise TypeError("capability tier must be a CapabilityTier")
    try:
        return CapabilityTier(value)
    except ValueError as error:
        raise ValueError("unsupported capability tier") from error


def _aggregate_status(values: Iterable[EvidenceStatus]) -> EvidenceStatus:
    present = set(values)
    for item in _STATUS_PRECEDENCE:
        if item in present:
            return item
    return EvidenceStatus.MISSING


def _recommendation_basis(data_year: int, min_rank: int, profile_rank: int) -> str:
    delta = min_rank - profile_rank
    return f"{data_year} 年已验证投档记录；最低位次与用户位次差 Δ={delta:+d}"


def _action_digest(actions: tuple[ActionItem, ...]) -> str:
    payload = [item.to_dict() for item in actions]
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


@dataclass(frozen=True)
class ActionTimelinePhase(_Serializable):
    """One phase of the non-priority remainder of an action plan."""

    phase: str
    actions: tuple[ActionItem, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "phase", _text(self.phase, "timeline phase"))
        actions = tuple(self.actions)
        if not actions or not all(isinstance(item, ActionItem) for item in actions):
            raise TypeError("timeline actions must contain ActionItem values")
        if any(item.phase != self.phase for item in actions):
            raise ValueError("timeline actions must match their phase")
        object.__setattr__(self, "actions", actions)


def _timeline(actions: tuple[ActionItem, ...]) -> tuple[ActionTimelinePhase, ...]:
    phases: list[ActionTimelinePhase] = []
    for phase in ("现在", "本学期", "下一阶段", "报名前", "出分后"):
        grouped = tuple(item for item in actions if item.phase == phase)
        if grouped:
            phases.append(ActionTimelinePhase(phase=phase, actions=grouped))
    return tuple(phases)


@dataclass(frozen=True)
class StudentProfile(_Serializable):
    """Privacy-minimal report profile; no name, contact, school, or class."""

    province: str
    subject_mode: str
    subject_group: str
    secondary_subjects: tuple[str, ...]
    rank: int | None
    grade: str
    current_year: int
    subject_selection_key: str = ""

    def __post_init__(self) -> None:
        for name in ("province", "subject_mode", "subject_group", "grade"):
            object.__setattr__(
                self,
                name,
                _text(getattr(self, name), name, profile_text=True),
            )
        if self.subject_mode not in _SUBJECT_MODES:
            raise ValueError("subject_mode must be 3+1+2 or 3+3")
        if self.grade not in _GRADES:
            raise ValueError("grade must be 高一, 高二, or 高三")
        key = self.subject_selection_key or self.subject_group
        object.__setattr__(
            self,
            "subject_selection_key",
            _text(key, "subject_selection_key", profile_text=True),
        )
        object.__setattr__(
            self,
            "secondary_subjects",
            _text_tuple(
                self.secondary_subjects,
                "secondary_subjects",
                unique=True,
                sort=True,
                profile_text=True,
            ),
        )
        if self.rank is not None:
            object.__setattr__(self, "rank", _positive_int(self.rank, "rank"))
        year = _positive_int(self.current_year, "current_year", minimum=2000)
        if year > 2100:
            raise ValueError("current_year must not exceed 2100")
        object.__setattr__(self, "current_year", year)


@dataclass(frozen=True)
class ReportRecommendation(_Serializable):
    strategy: str
    school_name: str
    school_level: str
    city: str
    min_score: int
    min_rank: int
    delta: int
    remarks: str
    match_reason: str
    data_year: int
    source_ids: tuple[str, ...]
    evidence_status: EvidenceStatus
    calculation_basis: str
    supporting_years: tuple[int, ...] = ()
    required_year_majority: int = 1
    scenario_reach_counts: tuple[int, int, int] = (0, 0, 0)
    scenario_confidence: str = "official"
    fit_evidence_statuses: tuple[EvidenceStatus, ...] = ()

    def __post_init__(self) -> None:
        if self.strategy not in {"冲", "稳", "保", "观察"}:
            raise ValueError("strategy must be 冲, 稳, 保, or 观察")
        for name in (
            "school_name",
            "school_level",
            "city",
            "remarks",
            "match_reason",
            "calculation_basis",
        ):
            value = getattr(self, name)
            if value == "" and name in {"school_level", "city", "remarks"}:
                continue
            object.__setattr__(self, name, _text(value, name))
        object.__setattr__(self, "min_score", _positive_int(self.min_score, "min_score"))
        object.__setattr__(self, "min_rank", _positive_int(self.min_rank, "min_rank"))
        if not isinstance(self.delta, int) or isinstance(self.delta, bool):
            raise TypeError("delta must be an integer")
        object.__setattr__(self, "data_year", _positive_int(self.data_year, "data_year", minimum=2000))
        if self.data_year > 2100:
            raise ValueError("data_year must not exceed 2100")
        object.__setattr__(
            self,
            "source_ids",
            _text_tuple(self.source_ids, "source_ids", safe_ids=True, unique=True, sort=True),
        )
        if not self.source_ids:
            raise ValueError("report recommendations require source IDs")
        object.__setattr__(self, "evidence_status", _status(self.evidence_status))
        if self.evidence_status not in _ACCEPTED_EXACT:
            raise ValueError("numeric recommendations require accepted exact evidence")
        object.__setattr__(
            self,
            "supporting_years",
            _year_tuple(self.supporting_years, "supporting_years"),
        )
        object.__setattr__(
            self,
            "required_year_majority",
            _positive_int(self.required_year_majority, "required_year_majority"),
        )
        if (
            not isinstance(self.scenario_reach_counts, (tuple, list))
            or len(self.scenario_reach_counts) != 3
        ):
            raise TypeError("scenario_reach_counts must contain three counts")
        counts = tuple(
            _nonnegative_int(value, "scenario_reach_count")
            for value in self.scenario_reach_counts
        )
        if any(value > len(self.supporting_years) for value in counts):
            raise ValueError("scenario reach count exceeds supporting years")
        object.__setattr__(self, "scenario_reach_counts", counts)
        if self.scenario_confidence not in {"official", "high", "medium", "low"}:
            raise ValueError("unsupported scenario confidence")
        try:
            fit_statuses = tuple(
                EvidenceStatus(value) for value in self.fit_evidence_statuses
            )
        except (TypeError, ValueError):
            raise ValueError("fit_evidence_statuses contains an invalid status") from None
        if len(fit_statuses) != len(set(fit_statuses)):
            raise ValueError("fit_evidence_statuses must be unique")
        object.__setattr__(self, "fit_evidence_statuses", fit_statuses)


@dataclass(frozen=True)
class ReportSchoolObservation(_Serializable):
    """Non-numeric report projection of a partial-coverage school row."""

    school_name: str
    school_level: str
    city: str
    data_year: int
    source_ids: tuple[str, ...]
    evidence_status: EvidenceStatus
    reason_code: str

    def __post_init__(self) -> None:
        for name in ("school_name", "school_level", "city"):
            value = getattr(self, name)
            if value == "" and name in {"school_level", "city"}:
                continue
            object.__setattr__(self, name, _text(value, name))
        object.__setattr__(
            self,
            "data_year",
            _positive_int(self.data_year, "data_year", minimum=2000),
        )
        if self.data_year > 2100:
            raise ValueError("data_year must not exceed 2100")
        object.__setattr__(
            self,
            "source_ids",
            _text_tuple(
                self.source_ids,
                "source_ids",
                safe_ids=True,
                unique=True,
                sort=True,
            ),
        )
        if not self.source_ids:
            raise ValueError("school observations require source IDs")
        if _status(self.evidence_status) is not EvidenceStatus.PARTIAL:
            raise ValueError("school observations must remain partial")
        object.__setattr__(self, "evidence_status", EvidenceStatus.PARTIAL)
        reason = _text(self.reason_code, "reason_code")
        assert reason is not None
        if _REASON.fullmatch(reason) is None:
            raise ValueError("school observation reason_code is invalid")
        object.__setattr__(self, "reason_code", reason)


@dataclass(frozen=True)
class ReportPathway(_Serializable):
    policy_id: str
    pathway_type: str
    title: str
    institution: str
    status: str
    eligibility: str
    missing_constraints: tuple[str, ...]
    professional_options: tuple[str, ...]
    training_arrangements: str | None
    transition_rules: str | None
    outcomes: str | None
    service_employment_obligations: str | None
    penalty_exit_rules: str | None
    fees_and_subsidies: str | None
    source_ids: tuple[str, ...]
    evidence_status: EvidenceStatus
    calculation_basis: str
    field_evidence: tuple[PathwayFieldEvidence, ...]
    field_evidence_context: str
    target_rank: int | None
    investment_decision: str = "观察"
    qualification_status: str = "待核验"
    satisfied_conditions: tuple[str, ...] = ()
    timeline: tuple[str, ...] = ()
    preparation_actions: tuple[str, ...] = ()
    target_year: int | None = None
    data_year: int | None = None
    fallback_distance: int = 0
    year_basis: str = "unverified"
    decision_reasons: tuple["ReportDecisionReason", ...] = ()

    def __post_init__(self) -> None:
        for name in ("policy_id", "pathway_type", "title", "institution", "status", "eligibility", "calculation_basis"):
            object.__setattr__(self, name, _text(getattr(self, name), name))
        if _SAFE_ID.fullmatch(self.policy_id) is None:
            raise ValueError("policy_id must use safe-ID syntax")
        if self.status not in {"formal", "pending_verification", "excluded"}:
            raise ValueError("unsupported pathway status")
        expected_eligibility = {
            "formal": "eligible",
            "pending_verification": "pending_verification",
            "excluded": "ineligible",
        }[self.status]
        if self.eligibility != expected_eligibility:
            raise ValueError("pathway status and eligibility are inconsistent")
        object.__setattr__(
            self,
            "missing_constraints",
            _text_tuple(self.missing_constraints, "missing_constraints"),
        )
        object.__setattr__(
            self,
            "professional_options",
            _text_tuple(self.professional_options, "professional_options", unique=True, sort=True),
        )
        for name in (
            "training_arrangements",
            "transition_rules",
            "outcomes",
            "service_employment_obligations",
            "penalty_exit_rules",
            "fees_and_subsidies",
        ):
            object.__setattr__(
                self,
                name,
                _text(getattr(self, name), name, optional=True),
            )
        if self.status == "formal" and self.missing_constraints:
            raise ValueError("formal pathways cannot carry missing constraints")
        if self.status != "formal" and not self.missing_constraints:
            raise ValueError("non-formal pathways require an explicit reason")
        complete_details = bool(self.professional_options) and all(
            getattr(self, name) is not None
            for name in (
                "training_arrangements",
                "transition_rules",
                "outcomes",
                "service_employment_obligations",
                "penalty_exit_rules",
                "fees_and_subsidies",
            )
        )
        if self.status == "formal" and not complete_details:
            raise ValueError("formal pathways require complete policy details")
        object.__setattr__(
            self,
            "source_ids",
            _text_tuple(self.source_ids, "source_ids", safe_ids=True, unique=True, sort=True),
        )
        object.__setattr__(self, "evidence_status", _status(self.evidence_status))
        if not self.source_ids and not (
            self.status == "pending_verification"
            and self.evidence_status
            in {EvidenceStatus.MISSING, EvidenceStatus.MASKED}
        ):
            raise ValueError("pathways require policy source IDs")
        minimum_sources = {
            EvidenceStatus.OFFICIAL: 1,
            EvidenceStatus.CORROBORATED: 2,
            EvidenceStatus.REFERENCE: 3,
        }.get(self.evidence_status)
        if self.status == "formal" and (
            minimum_sources is None or len(self.source_ids) < minimum_sources
        ):
            raise ValueError("formal pathways require accepted exact evidence")
        if self.target_rank is not None:
            object.__setattr__(self, "target_rank", _positive_int(self.target_rank, "target_rank"))
            if self.status != "formal":
                raise ValueError("only formal pathways may carry a target rank")
        if self.investment_decision not in {"主攻", "重点准备", "备选", "观察", "不建议"}:
            raise ValueError("unsupported pathway investment decision")
        if self.qualification_status not in {"已满足", "部分满足", "暂未满足", "待核验", "不适用"}:
            raise ValueError("unsupported pathway qualification status")
        for name in ("satisfied_conditions", "timeline", "preparation_actions"):
            object.__setattr__(
                self,
                name,
                _text_tuple(getattr(self, name), name),
            )
        if self.target_year is None or self.data_year is None:
            if self.target_year is not None or self.data_year is not None:
                raise ValueError("incomplete pathway year metadata")
            if self.fallback_distance != 0 or self.year_basis != "unverified":
                raise ValueError("unverified pathway year metadata is inconsistent")
        else:
            target = _positive_int(self.target_year, "target_year", minimum=2000)
            data = _positive_int(self.data_year, "data_year", minimum=2000)
            distance = _nonnegative_int(self.fallback_distance, "fallback_distance")
            if target - data != distance or distance > 3:
                raise ValueError("pathway fallback metadata is inconsistent")
            expected_basis = "current_year" if distance == 0 else "historical_fallback"
            if self.year_basis != expected_basis:
                raise ValueError("pathway year basis is inconsistent")
        reasons = tuple(self.decision_reasons)
        if reasons and (
            len(reasons) != 8
            or not all(isinstance(item, ReportDecisionReason) for item in reasons)
        ):
            raise ValueError("pathway decision trace must contain all eight reasons")
        object.__setattr__(self, "decision_reasons", reasons)
        object.__setattr__(
            self,
            "field_evidence",
            validate_pathway_display_evidence(self, owner="report pathway"),
        )


def pathway_field_evidence_lines(item: ReportPathway) -> tuple[str, ...]:
    """Return a renderer-neutral, exact-order audit for every displayed field."""

    if not isinstance(item, ReportPathway):
        raise TypeError("pathway evidence audit requires a ReportPathway")
    records = validate_pathway_display_evidence(
        item, owner="report pathway renderer"
    )
    return tuple(
        "；".join(
            (
                f"字段：{record.field}（{_PATHWAY_FIELD_LABEL.get(record.field, record.field)}）",
                f"证据状态：{_STATUS_LABEL[record.status]}",
                f"覆盖：{_COVERAGE_LABEL[record.coverage]}",
                f"来源编号：{'、'.join(record.source_ids) or '无'}",
                f"证据定位：{'、'.join(record.locators) or '无'}",
                f"抽取方式：{'、'.join(record.extraction_methods) or '无'}",
                f"证据方法：{record.evidence_method}",
                f"上游字段：{'、'.join(record.upstream_fields) or '无'}",
                f"画像字段：{'、'.join(record.profile_fields) or '无'}",
                f"提示：{'；'.join(record.warnings) or '无'}",
                f"来源类型：{record.origin.value}",
                f"值绑定：{record.value_digest}",
                f"上下文绑定：{record.context_binding}",
                f"记录摘要：{record.digest}",
            )
        )
        for record in records
    )


@dataclass(frozen=True)
class ReportDecisionReason(_Serializable):
    dimension: str
    code: str
    effect: str
    explanation: str
    input_fields: tuple[str, ...]
    source_ids: tuple[str, ...]
    evidence_status: EvidenceStatus | None = None

    def __post_init__(self) -> None:
        for name in ("dimension", "code", "effect", "explanation"):
            object.__setattr__(self, name, _text(getattr(self, name), name))
        if self.effect not in {"supports", "blocks", "uncertain"}:
            raise ValueError("school reason effect is unsupported")
        if _SAFE_ID.fullmatch(self.code) is None:
            raise ValueError("school reason code must use the safe-ID syntax")
        input_fields = tuple(self.input_fields)
        if (
            len(input_fields) != len(set(input_fields))
            or any(
                not isinstance(item, str) or _TRACE_FIELD.fullmatch(item) is None
                for item in input_fields
            )
        ):
            raise ValueError(
                "input_fields must contain only unique decision-trace fields"
            )
        object.__setattr__(self, "input_fields", input_fields)
        object.__setattr__(
            self,
            "source_ids",
            _text_tuple(self.source_ids, "source_ids", safe_ids=True, unique=True, sort=True),
        )
        if self.evidence_status is not None:
            object.__setattr__(
                self, "evidence_status", _status(self.evidence_status)
            )
            if self.evidence_status in {
                EvidenceStatus.OFFICIAL,
                EvidenceStatus.CORROBORATED,
                EvidenceStatus.REFERENCE,
                EvidenceStatus.CONFLICT,
                EvidenceStatus.PARTIAL,
                EvidenceStatus.INFERRED,
            } and not self.source_ids:
                raise ValueError(
                    "decision reason evidence status requires source IDs"
                )


@dataclass(frozen=True)
class ReportSchoolDecision(_Serializable):
    school_name: str
    outcome: str
    order: int | None
    reasons: tuple[ReportDecisionReason, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "school_name", _text(self.school_name, "school_name"))
        if self.outcome not in {"included", "excluded"}:
            raise ValueError("school decision outcome is unsupported")
        if self.outcome == "included":
            object.__setattr__(self, "order", _positive_int(self.order, "order"))
        elif self.order is not None:
            raise ValueError("excluded school decisions cannot have an order")
        reasons = tuple(self.reasons)
        if not reasons or not all(isinstance(item, ReportDecisionReason) for item in reasons):
            raise TypeError("school decisions require projected reason records")
        object.__setattr__(self, "reasons", reasons)


@dataclass(frozen=True, init=False)
class ReportModel(_Serializable):
    profile: StudentProfile
    capability_tier: CapabilityTier
    query_coverage: str
    host_capabilities: tuple[str, ...]
    available_capabilities: tuple[str, ...]
    missing_capabilities: tuple[str, ...]
    degradations: tuple[str, ...]
    python_version: str
    optional_modules: tuple[str, ...]
    recommendations: tuple[ReportRecommendation, ...]
    school_observations: tuple[ReportSchoolObservation, ...]
    ordinary_batch_policy: OrdinaryBatchPolicy | None
    recommendation_policy_status: str
    school_decisions: tuple[ReportSchoolDecision, ...]
    recommendation_coverage_status: EvidenceStatus
    verified_rank_coverage: tuple[int, int] | None
    recommendation_empty_reason: str | None
    recommendation_warnings: tuple[str, ...]
    excluded_by_subject_count: int
    zero_score_excluded_count: int
    input_years: tuple[int, ...]
    usable_years: tuple[int, ...]
    rank: RankEstimate | RankScenario | None
    pathways_available: bool
    pathways: tuple[ReportPathway, ...]
    pathway_warnings: tuple[str, ...]
    pathway_target_rank: int | None
    pathway_transformation: str | None
    model_source_ids: tuple[str, ...]
    model_id: str | None
    model_method: str | None
    pathway_policy_evidence_status: EvidenceStatus | None
    pathway_target_evidence_status: EvidenceStatus | None
    manifest_session_id: str
    manifest_hash: str
    retrieval_dates: tuple[str, ...]
    source_ids: tuple[str, ...]
    evidence_status: EvidenceStatus
    warnings: tuple[str, ...]
    action_items: tuple[ActionItem, ...]
    action_plan_digest: str
    priority_actions: tuple[ActionItem, ...]
    action_timeline: tuple[ActionTimelinePhase, ...]

    def __init__(self) -> None:
        raise TypeError("ReportModel is factory-only")

    @classmethod
    def _create(cls, **values: Any) -> "ReportModel":
        expected = {item.name for item in fields(cls)}
        if set(values) != expected:
            raise TypeError("ReportModel factory fields do not match the contract")
        instance = object.__new__(cls)
        for name, value in values.items():
            object.__setattr__(instance, name, value)
        instance.__post_init__()
        return instance

    def __post_init__(self) -> None:
        if not isinstance(self.profile, StudentProfile):
            raise TypeError("profile must be a StudentProfile")
        object.__setattr__(self, "profile", StudentProfile(**self.profile.to_dict()))
        tier = _capability_tier(self.capability_tier)
        object.__setattr__(self, "capability_tier", tier)
        expected_query = _QUERY_COVERAGE[tier]
        if self.query_coverage != expected_query:
            raise ValueError("query coverage must be derived from capability tier")
        object.__setattr__(self, "query_coverage", _text(self.query_coverage, "query_coverage"))
        for name in (
            "host_capabilities",
            "available_capabilities",
            "missing_capabilities",
            "degradations",
            "optional_modules",
        ):
            object.__setattr__(
                self,
                name,
                _text_tuple(getattr(self, name), name, unique=True, sort=True),
            )
        version = _text(self.python_version, "python_version")
        assert version is not None
        object.__setattr__(self, "python_version", version)
        _validate_capability_snapshot(
            tier,
            self.host_capabilities,
            self.available_capabilities,
            self.missing_capabilities,
            self.degradations,
            self.python_version,
            self.optional_modules,
        )

        if self.recommendation_policy_status not in {
            "ordinary_batch_policy_available",
            "rank_delta_policy_unavailable",
        }:
            raise ValueError("recommendation policy status is unsupported")
        ordinary_batch_policy = self.ordinary_batch_policy
        if self.recommendation_policy_status == "ordinary_batch_policy_available":
            if not isinstance(ordinary_batch_policy, OrdinaryBatchPolicy):
                raise TypeError("available ordinary-batch policy must be explicit")
            ordinary_batch_policy = OrdinaryBatchPolicy(
                **ordinary_batch_policy.to_dict()
            )
        elif ordinary_batch_policy is not None:
            raise ValueError("unavailable rank-delta policy cannot carry placeholder values")
        object.__setattr__(self, "ordinary_batch_policy", ordinary_batch_policy)

        school_decisions = tuple(self.school_decisions)
        if not all(isinstance(item, ReportSchoolDecision) for item in school_decisions):
            raise TypeError("school_decisions must contain report decision records")
        if len({item.school_name for item in school_decisions}) != len(school_decisions):
            raise ValueError("school decisions must be unique by school")
        object.__setattr__(self, "school_decisions", school_decisions)

        if isinstance(self.recommendations, (str, bytes, bytearray)):
            raise TypeError("recommendations must be a collection")
        try:
            recommendations = tuple(self.recommendations)
        except TypeError as error:
            raise TypeError("recommendations must be a collection") from error
        if not all(isinstance(item, ReportRecommendation) for item in recommendations):
            raise TypeError("recommendations must contain report recommendation records")
        if len({(item.school_name, item.strategy) for item in recommendations}) != len(recommendations):
            raise ValueError("recommendations must be unique by school and strategy")
        object.__setattr__(self, "recommendations", recommendations)
        school_observations = tuple(self.school_observations)
        if not all(
            isinstance(item, ReportSchoolObservation)
            for item in school_observations
        ):
            raise TypeError(
                "school_observations must contain report observation records"
            )
        observation_keys = tuple(
            (item.school_name, item.data_year, item.source_ids)
            for item in school_observations
        )
        if len(observation_keys) != len(set(observation_keys)):
            raise ValueError("school observations must be unique")
        object.__setattr__(self, "school_observations", school_observations)
        coverage_status = _status(self.recommendation_coverage_status)
        object.__setattr__(self, "recommendation_coverage_status", coverage_status)
        if self.verified_rank_coverage is not None:
            if not isinstance(self.verified_rank_coverage, (tuple, list)) or len(self.verified_rank_coverage) != 2:
                raise TypeError("verified_rank_coverage must be a pair")
            lower = _positive_int(self.verified_rank_coverage[0], "coverage lower")
            upper = _positive_int(self.verified_rank_coverage[1], "coverage upper")
            if lower > upper:
                raise ValueError("verified rank coverage is reversed")
            object.__setattr__(self, "verified_rank_coverage", (lower, upper))
        if self.recommendation_empty_reason is not None:
            reason = _text(self.recommendation_empty_reason, "recommendation_empty_reason")
            assert reason is not None
            if _REASON.fullmatch(reason) is None:
                raise ValueError("recommendation_empty_reason must be a stable code")
            object.__setattr__(self, "recommendation_empty_reason", reason)
        object.__setattr__(
            self,
            "recommendation_warnings",
            _text_tuple(self.recommendation_warnings, "recommendation_warnings"),
        )
        for name in ("excluded_by_subject_count", "zero_score_excluded_count"):
            object.__setattr__(self, name, _nonnegative_int(getattr(self, name), name))
        object.__setattr__(self, "input_years", _year_tuple(self.input_years, "input_years"))
        object.__setattr__(self, "usable_years", _year_tuple(self.usable_years, "usable_years"))
        if set(self.usable_years).difference(self.input_years):
            raise ValueError("usable years must be a subset of input years")
        scenario_rank = self.rank if isinstance(self.rank, RankScenario) else None
        if (
            self.recommendation_policy_status == "rank_delta_policy_unavailable"
            and scenario_rank is None
        ):
            raise ValueError("rank-delta-free recommendations require a rank scenario")
        if recommendations:
            if self.profile.rank is None:
                raise ValueError("numeric recommendations require a profile rank")
            if self.verified_rank_coverage is None:
                raise ValueError("numeric recommendations require verified rank coverage")
            lower, upper = self.verified_rank_coverage
            if not lower <= self.profile.rank <= upper:
                raise ValueError("profile rank must be inside recommendation coverage")
            if self.recommendation_empty_reason is not None:
                raise ValueError("non-empty recommendations cannot carry an empty reason")
            if coverage_status not in _ACCEPTED_EXACT | {EvidenceStatus.PARTIAL}:
                raise ValueError("numeric recommendations require usable aggregate evidence")
            if any(
                item.evidence_status not in _ACCEPTED_EXACT
                for item in recommendations
            ):
                raise ValueError(
                    "numeric recommendations require accepted exact evidence"
                )
            aggregate_strength = _ACCEPTED_STRENGTH.get(coverage_status)
            if aggregate_strength is not None and any(
                _ACCEPTED_STRENGTH[item.evidence_status] < aggregate_strength
                for item in recommendations
            ):
                raise ValueError("recommendation aggregate status overstates item evidence")
            if scenario_rank is not None:
                if (
                    scenario_rank.central_rank != self.profile.rank
                    or not lower <= scenario_rank.optimistic_rank
                    or not scenario_rank.conservative_rank <= upper
                ):
                    raise ValueError("rank scenario does not match report profile or coverage")
                for item in recommendations:
                    if not item.supporting_years:
                        raise ValueError("scenario recommendation requires supporting years")
                    if item.data_year != max(item.supporting_years):
                        raise ValueError("scenario recommendation year is not the latest support")
                    if set(item.supporting_years).difference(self.usable_years):
                        raise ValueError("scenario recommendation years must be usable")
                    counts = item.scenario_reach_counts
                    majority = item.required_year_majority
                    expected_strategy = (
                        "保" if counts[2] >= majority else
                        "稳" if counts[1] >= majority else
                        "冲" if counts[0] >= 1 else "观察"
                    )
                    if item.strategy != expected_strategy:
                        raise ValueError("scenario recommendation classification is inconsistent")
                    years = "、".join(str(year) for year in item.supporting_years)
                    expected_basis = (
                        f"{years} 年同省同选科可比投档记录；多数门槛 "
                        f"{majority}；乐观、中性、保守触达 "
                        f"{counts[0]}、{counts[1]}、{counts[2]}"
                    )
                    if item.calculation_basis != expected_basis:
                        raise ValueError("scenario recommendation basis is not canonical")
            else:
                for item in recommendations:
                    if not lower <= item.min_rank <= upper:
                        raise ValueError("recommendation rank must be inside verified coverage")
                    expected_delta = item.min_rank - self.profile.rank
                    if item.delta != expected_delta:
                        raise ValueError("recommendation delta must derive from profile rank")
                    expected_strategy = (
                        "冲"
                        if item.delta < ordinary_batch_policy.challenge_delta_lt
                        else (
                            "稳"
                            if item.delta <= ordinary_batch_policy.stable_delta_le
                            else "保"
                        )
                    )
                    if item.strategy != expected_strategy:
                        raise ValueError("recommendation strategy contradicts ordinary batch policy")
                    expected_basis = _recommendation_basis(
                        item.data_year,
                        item.min_rank,
                        self.profile.rank,
                    )
                    if item.calculation_basis != expected_basis:
                        raise ValueError("recommendation calculation basis is not canonical")
                    if item.data_year not in self.usable_years:
                        raise ValueError("recommendation year must be usable")
            if ordinary_batch_policy is not None:
                for strategy, cap in ordinary_batch_policy.tier_caps.items():
                    if sum(item.strategy == strategy for item in recommendations) > cap:
                        raise ValueError("recommendation tier exceeds ordinary batch policy cap")
        elif self.recommendation_empty_reason is None:
            raise ValueError("empty recommendations require an explicit stable reason")
        if school_observations and not recommendations:
            if self.recommendation_empty_reason not in {
                "partial_observations_only",
                "rank_outside_verified_coverage",
            }:
                raise ValueError(
                    "observation-only school output requires its stable empty reason"
                )
        elif self.recommendation_empty_reason == "partial_observations_only":
            raise ValueError(
                "partial observation empty reason requires school observations"
            )

        included_decisions = tuple(
            item.school_name
            for item in sorted(
                (item for item in school_decisions if item.outcome == "included"),
                key=lambda item: item.order,
            )
        )
        if school_decisions and included_decisions != tuple(
            item.school_name for item in recommendations
        ):
            raise ValueError("school decision trace does not match recommendations")
        if coverage_status not in _ACCEPTED_EXACT and not self.recommendation_warnings:
            raise ValueError("degraded recommendation coverage requires a warning")
        if self.recommendation_empty_reason == "missing_verified_coverage" and self.verified_rank_coverage is not None:
            raise ValueError("missing coverage reason cannot carry a coverage interval")
        if self.recommendation_empty_reason == "rank_outside_verified_coverage":
            if self.verified_rank_coverage is None:
                raise ValueError("outside-coverage reason requires a known interval")
            lower, upper = self.verified_rank_coverage
            if scenario_rank is not None:
                if (
                    lower <= scenario_rank.optimistic_rank
                    and scenario_rank.conservative_rank <= upper
                ):
                    raise ValueError("outside-coverage reason contradicts rank scenario")
            elif self.profile.rank is not None and lower <= self.profile.rank <= upper:
                raise ValueError("outside-coverage reason contradicts profile rank")
        if self.recommendation_empty_reason == "no_match_within_verified_coverage":
            if self.verified_rank_coverage is None:
                raise ValueError("verified empty result requires a coverage interval")
            lower, upper = self.verified_rank_coverage
            if self.profile.rank is None or not lower <= self.profile.rank <= upper:
                raise ValueError("verified empty result requires rank inside coverage")

        if self.rank is not None:
            if isinstance(self.rank, RankEstimate):
                object.__setattr__(self, "rank", RankEstimate(**self.rank.to_dict()))
            elif isinstance(self.rank, RankScenario):
                object.__setattr__(self, "rank", RankScenario._create(**self.rank.to_dict()))
            else:
                raise TypeError("rank must be a RankEstimate, RankScenario, or None")
        if not isinstance(self.pathways_available, bool):
            raise TypeError("pathways_available must be boolean")
        if isinstance(self.pathways, (str, bytes, bytearray)):
            raise TypeError("pathways must be a collection")
        try:
            pathways = tuple(self.pathways)
        except TypeError as error:
            raise TypeError("pathways must be a collection") from error
        if not all(isinstance(item, ReportPathway) for item in pathways):
            raise TypeError("pathways must contain report pathway records")
        if len({item.policy_id for item in pathways}) != len(pathways):
            raise ValueError("pathways must have unique policy IDs")
        if not self.pathways_available and pathways:
            raise ValueError("unavailable pathways cannot contain items")
        object.__setattr__(self, "pathways", pathways)
        object.__setattr__(self, "pathway_warnings", _text_tuple(self.pathway_warnings, "pathway_warnings"))
        if self.pathway_target_rank is not None:
            object.__setattr__(self, "pathway_target_rank", _positive_int(self.pathway_target_rank, "pathway_target_rank"))
        if self.pathway_transformation is not None:
            object.__setattr__(self, "pathway_transformation", _text(self.pathway_transformation, "pathway_transformation"))
            if self.pathway_target_rank is None:
                raise ValueError("pathway transformation requires a target rank")
        object.__setattr__(
            self,
            "model_source_ids",
            _text_tuple(self.model_source_ids, "model_source_ids", safe_ids=True, unique=True, sort=True),
        )
        if self.pathway_target_rank is not None and not self.model_source_ids:
            raise ValueError("pathway target rank requires model sources")
        formal_pathways = tuple(item for item in pathways if item.status == "formal")
        if self.pathway_target_rank is None:
            if (
                self.pathway_transformation is not None
                or self.model_source_ids
                or self.model_id is not None
                or self.model_method is not None
                or self.pathway_target_evidence_status is not None
            ):
                raise ValueError("pathway model output requires a target rank")
            if any(item.target_rank is not None for item in pathways):
                raise ValueError("pathway item targets require a result target rank")
        else:
            if self.pathway_transformation is None or not formal_pathways:
                raise ValueError("pathway target rank requires a documented formal pathway")
            if any(item.target_rank != self.pathway_target_rank for item in formal_pathways):
                raise ValueError("formal pathway targets must match the result target")
            model_id = _text(self.model_id, "model_id")
            model_method = _text(self.model_method, "model_method")
            assert model_id is not None and model_method is not None
            if _SAFE_ID.fullmatch(model_id) is None or _SAFE_ID.fullmatch(model_method) is None:
                raise ValueError("pathway model identity and method must use safe-ID syntax")
            object.__setattr__(self, "model_id", model_id)
            object.__setattr__(self, "model_method", model_method)
        expected_policy_status = (
            _aggregate_status(item.evidence_status for item in formal_pathways)
            if self.pathway_target_rank is not None
            else None
        )
        if self.pathway_policy_evidence_status is None:
            policy_status = None
        else:
            policy_status = _status(
                self.pathway_policy_evidence_status,
                "pathway_policy_evidence_status",
            )
        if policy_status != expected_policy_status:
            raise ValueError("pathway policy evidence status must derive from formal pathways")
        object.__setattr__(self, "pathway_policy_evidence_status", policy_status)
        if self.pathway_target_rank is None:
            target_status = None
        else:
            target_status = _status(
                self.pathway_target_evidence_status,
                "pathway_target_evidence_status",
            )
            minimum = {
                EvidenceStatus.OFFICIAL: 1,
                EvidenceStatus.CORROBORATED: 2,
                EvidenceStatus.REFERENCE: 3,
            }.get(target_status)
            if minimum is None or len(self.model_source_ids) < minimum:
                raise ValueError("pathway target requires sufficient exact model evidence")
        object.__setattr__(self, "pathway_target_evidence_status", target_status)
        if not self.pathways_available and (
            self.pathway_warnings
            or self.pathway_target_rank is not None
            or self.pathway_transformation is not None
            or self.model_source_ids
        ):
            raise ValueError("unavailable pathways cannot carry pathway output")

        session = self.manifest_session_id
        if not isinstance(session, str) or _SESSION_ID.fullmatch(session) is None:
            raise ValueError("manifest session id is invalid")
        object.__setattr__(self, "manifest_session_id", session)
        manifest_hash = self.manifest_hash
        if not isinstance(manifest_hash, str) or _HASH.fullmatch(manifest_hash) is None:
            raise ValueError("manifest hash is invalid")
        object.__setattr__(self, "manifest_hash", manifest_hash)
        pathways_with_retrieved_evidence = tuple(
            item
            for item in pathways
            if item.source_ids or item.data_year is not None
        )
        allow_empty_dates = (
            not recommendations
            and not school_observations
            and not pathways_with_retrieved_evidence
            and not self.source_ids
            and (
                self.rank is None
                or self.rank.status in {EvidenceStatus.MISSING, EvidenceStatus.CONFLICT}
            )
        )
        retrieval_dates = _date_tuple(
            self.retrieval_dates,
            "retrieval_dates",
            allow_empty=allow_empty_dates,
        )
        if any(int(item[:4]) != self.profile.current_year for item in retrieval_dates):
            raise ValueError("retrieval dates must match the profile current year")
        object.__setattr__(self, "retrieval_dates", retrieval_dates)

        source_ids = _text_tuple(self.source_ids, "source_ids", safe_ids=True, unique=True, sort=True)
        expected_sources = {
            source_id
            for item in recommendations
            for source_id in item.source_ids
        }
        expected_sources.update(
            source_id
            for item in school_observations
            for source_id in item.source_ids
        )
        expected_sources.update(
            source_id
            for decision in school_decisions
            for reason in decision.reasons
            for source_id in reason.source_ids
        )
        if self.rank is not None:
            expected_sources.update(
                self.rank.source_ids
                if isinstance(self.rank, RankScenario)
                else self.rank.contributing_source_ids
            )
        for item in pathways:
            expected_sources.update(item.source_ids)
        expected_sources.update(self.model_source_ids)
        if source_ids != tuple(sorted(expected_sources)):
            raise ValueError("source_ids must be the exact cross-result source union")
        object.__setattr__(self, "source_ids", source_ids)

        statuses = [coverage_status]
        statuses.extend(
            status
            for item in recommendations
            for status in item.fit_evidence_statuses
        )
        statuses.extend(
            reason.evidence_status
            for decision in school_decisions
            for reason in decision.reasons
            if reason.evidence_status is not None
        )
        statuses.append(self.rank.status if self.rank is not None else EvidenceStatus.MISSING)
        if pathways:
            statuses.extend(item.evidence_status for item in pathways)
        else:
            statuses.append(EvidenceStatus.MISSING)
        if self.pathway_target_evidence_status is not None:
            statuses.append(self.pathway_target_evidence_status)
        expected_status = _aggregate_status(statuses)
        if _status(self.evidence_status) != expected_status:
            raise ValueError("evidence_status must follow conservative precedence")
        object.__setattr__(self, "evidence_status", expected_status)
        warnings = _text_tuple(self.warnings, "warnings")
        required_warnings = tuple(
            dict.fromkeys(
                (
                    *self.degradations,
                    *self.recommendation_warnings,
                    *self.pathway_warnings,
                    *(
                        ("喜报位次证据不足：模型未提供；不执行校排名折算",)
                        if self.rank is None
                        else ()
                    ),
                    *(
                        ("多元升学结果未提供，本章节降级",)
                        if not self.pathways_available
                        else ()
                    ),
                )
            )
        )
        if warnings != required_warnings:
            raise ValueError("warnings must be the exact required degradation union")
        object.__setattr__(self, "warnings", warnings)
        actions = tuple(self.action_items)
        if not actions or not all(isinstance(item, ActionItem) for item in actions):
            raise TypeError("action_items must contain factory-built ActionItem values")
        if len({item.action_id for item in actions}) != len(actions):
            raise ValueError("action_items must have unique action IDs")
        if self.action_plan_digest != _action_digest(actions):
            raise ValueError("action_plan_digest must bind the complete deterministic action plan")
        priority = tuple(self.priority_actions)
        if not 3 <= len(priority) <= 7 or priority != actions[: len(priority)]:
            raise ValueError("priority_actions must be the first three to seven actions")
        if not all(isinstance(item, ActionItem) for item in priority):
            raise TypeError("priority_actions must contain ActionItem values")
        timeline = tuple(self.action_timeline)
        if not all(isinstance(item, ActionTimelinePhase) for item in timeline):
            raise TypeError("action_timeline must contain phase groups")
        expected_timeline = _timeline(actions[len(priority) :])
        if timeline != expected_timeline:
            raise ValueError("action_timeline must group the action-plan remainder by phase")
        object.__setattr__(self, "action_items", actions)
        object.__setattr__(self, "priority_actions", priority)
        object.__setattr__(self, "action_timeline", timeline)


def _validate_capability_snapshot(
    tier: CapabilityTier,
    host: tuple[str, ...],
    available: tuple[str, ...],
    missing: tuple[str, ...],
    degradations: tuple[str, ...],
    version: str,
    optional: tuple[str, ...],
) -> None:
    known_missing = _HOST_CAPABILITIES | _OPTIONAL_MODULES | {"python>=3.10"}
    if set(host).difference(_HOST_CAPABILITIES) or available != host:
        raise ValueError("capability host declarations are inconsistent")
    if set(available).intersection(missing):
        raise ValueError("available and missing capabilities must be disjoint")
    if set(missing).difference(known_missing):
        raise ValueError("capability missing declaration is unsupported")
    if not (_HOST_CAPABILITIES - set(host)).issubset(missing):
        raise ValueError("missing host capabilities cannot be hidden")
    if set(optional).difference(_OPTIONAL_MODULES):
        raise ValueError("capability optional-module declaration is unsupported")
    if set(optional).intersection(missing):
        raise ValueError("available optional modules cannot also be missing")
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version)
    if match is None:
        raise ValueError("capability python version is invalid")
    supported_python = (int(match.group(1)), int(match.group(2))) >= (3, 10)
    if supported_python == ("python>=3.10" in missing):
        raise ValueError("python capability declaration is inconsistent")
    has_network = {"search", "browse"}.issubset(host)
    is_full = (
        has_network
        and "vision" in host
        and set(optional) == _OPTIONAL_MODULES
        and supported_python
    )
    expected_tier = (
        CapabilityTier.FULL
        if is_full
        else CapabilityTier.STANDARD
        if has_network and supported_python
        else CapabilityTier.OFFLINE
    )
    if tier is not expected_tier:
        raise ValueError("capability tier does not match the declared capabilities")
    degraded = tier is not CapabilityTier.FULL
    if degraded and not degradations:
        raise ValueError("degraded capability tiers require explicit degradations")
    if not degraded and (missing or degradations):
        raise ValueError("full capability tier cannot carry missing or degradation output")


def _snapshot_capability(capability: CapabilityReport) -> tuple[
    CapabilityTier,
    tuple[str, ...],
    tuple[str, ...],
    tuple[str, ...],
    tuple[str, ...],
    str,
    tuple[str, ...],
]:
    tier = _capability_tier(capability.tier)
    host = _text_tuple(capability.host_capabilities, "host_capabilities", unique=True, sort=True)
    available = _text_tuple(capability.available_capabilities, "available_capabilities", unique=True, sort=True)
    missing = _text_tuple(capability.missing_capabilities, "missing_capabilities", unique=True, sort=True)
    degradations = _text_tuple(capability.degradations, "degradations", unique=True, sort=True)
    optional = _text_tuple(capability.optional_modules, "optional_modules", unique=True, sort=True)
    version = _text(capability.python_version, "python_version")
    assert version is not None
    _validate_capability_snapshot(
        tier,
        host,
        available,
        missing,
        degradations,
        version,
        optional,
    )
    return tier, host, available, missing, degradations, version, optional


def _snapshot_manifest(manifest: EvidenceManifest, tier: CapabilityTier) -> tuple[str, str]:
    if manifest.schema_version != "1.0":
        raise ValueError("only evidence manifest schema 1.0 is supported")
    if _capability_tier(manifest.capability_tier) != tier:
        raise ValueError("manifest and capability tiers disagree")
    if manifest.candidates_filename != "candidates.jsonl" or manifest.facts_filename != "normalized/facts.jsonl":
        raise ValueError("manifest artifact names are not canonical")
    _nonnegative_int(manifest.rejected_count, "manifest rejected_count")
    session = manifest.session_id
    digest = manifest.manifest_hash
    if (
        not isinstance(session, str)
        or _SESSION_ID.fullmatch(session) is None
        or not isinstance(digest, str)
        or _HASH.fullmatch(digest) is None
    ):
        raise ValueError("manifest public identity is invalid")
    return session, digest


def _project_recommendation(
    item: RecommendationItem,
    profile_rank: int | None,
    rank: RankEstimate | RankScenario | None,
) -> ReportRecommendation:
    if not isinstance(item, RecommendationItem):
        raise TypeError("recommendation items must be RecommendationItem records")
    if not isinstance(item.province_match, bool) or not isinstance(item.subject_match, bool):
        raise TypeError("recommendation match flags must be boolean")
    if not item.subject_match:
        raise ValueError("rendered recommendations must pass subject filters")
    if profile_rank is None:
        raise ValueError("numeric recommendations require a profile rank")
    if isinstance(rank, RankScenario):
        years = "、".join(str(year) for year in item.supporting_years)
        counts = item.scenario_reach_counts
        calculation_basis = (
            f"{years} 年同省同选科可比投档记录；多数门槛 "
            f"{item.required_year_majority}；乐观、中性、保守触达 "
            f"{counts[0]}、{counts[1]}、{counts[2]}"
        )
    else:
        calculation_basis = _recommendation_basis(
            item.data_year,
            item.min_rank,
            profile_rank,
        )
    return ReportRecommendation(
        strategy=item.strategy,
        school_name=item.school_name,
        school_level=item.school_level,
        city=item.city,
        min_score=item.min_score,
        min_rank=item.min_rank,
        delta=item.delta,
        remarks=item.remarks,
        match_reason=item.match_reason,
        data_year=item.data_year,
        source_ids=item.source_ids,
        evidence_status=item.evidence_status,
        calculation_basis=calculation_basis,
        supporting_years=item.supporting_years,
        required_year_majority=item.required_year_majority,
        scenario_reach_counts=item.scenario_reach_counts,
        scenario_confidence=item.scenario_confidence,
        fit_evidence_statuses=item.fit_evidence_statuses,
    )


def _project_school_observation(item: SchoolObservation) -> ReportSchoolObservation:
    if not isinstance(item, SchoolObservation):
        raise TypeError("school observations must use the typed contract")
    return ReportSchoolObservation(
        school_name=item.school_name,
        school_level=item.school_level,
        city=item.city,
        data_year=item.data_year,
        source_ids=item.source_ids,
        evidence_status=item.evidence_status,
        reason_code=item.reason_code,
    )


def _project_pathway(item: PathwayItem) -> ReportPathway:
    if not isinstance(item, PathwayItem):
        raise TypeError("pathway items must be PathwayItem records")
    validate_pathway_display_evidence(item, owner="pathway report projection")
    return ReportPathway(
        policy_id=item.policy_id,
        pathway_type=item.pathway_type,
        title=item.title,
        institution=item.institution,
        status=item.status,
        eligibility=item.eligibility,
        missing_constraints=item.missing_constraints,
        professional_options=item.professional_options,
        training_arrangements=item.training_arrangements,
        transition_rules=item.transition_rules,
        outcomes=item.outcomes,
        service_employment_obligations=item.service_employment_obligations,
        penalty_exit_rules=item.penalty_exit_rules,
        fees_and_subsidies=item.fees_and_subsidies,
        source_ids=item.policy_source_ids,
        evidence_status=item.evidence_status,
        calculation_basis=item.calculation_basis,
        field_evidence=item.field_evidence,
        field_evidence_context=item.field_evidence_context,
        target_rank=item.target_rank,
        investment_decision=item.investment_decision,
        qualification_status=item.qualification_status,
        satisfied_conditions=item.satisfied_conditions,
        timeline=item.timeline,
        preparation_actions=item.preparation_actions,
        target_year=item.target_year,
        data_year=item.data_year,
        fallback_distance=item.fallback_distance,
        year_basis=item.year_basis,
        decision_reasons=tuple(
            ReportDecisionReason(
                dimension=reason.dimension,
                code=reason.code,
                effect=reason.effect,
                explanation=reason.explanation,
                input_fields=reason.input_fields,
                source_ids=reason.source_ids,
                evidence_status=reason.evidence_status,
            )
            for reason in item.decision_reasons
        ),
    )


def _project_school_decision(item: Any) -> ReportSchoolDecision:
    reasons = tuple(
        ReportDecisionReason(
            dimension=reason.dimension,
            code=reason.code,
            effect=reason.effect,
            explanation=reason.explanation,
            input_fields=reason.input_fields,
            source_ids=reason.source_ids,
            evidence_status=reason.evidence_status,
        )
        for reason in item.reasons
    )
    return ReportSchoolDecision(
        school_name=item.school_name,
        outcome=item.outcome,
        order=item.order,
        reasons=reasons,
    )


def build_report_model(
    profile: StudentProfile,
    recommendations: RecommendationResult | SchoolDecisionResult,
    rank: RankEstimate | RankScenario | None,
    pathways: PathwayResult | None,
    evidence: ValidatedEvidenceSnapshot,
    *,
    planning_profile: PlanningProfile | None = None,
) -> ReportModel:
    """Snapshot validated engine decisions into one renderer-neutral model."""

    if not isinstance(profile, StudentProfile):
        raise TypeError("profile must be a StudentProfile")
    if not isinstance(evidence, ValidatedEvidenceSnapshot):
        raise TypeError("evidence must be a ValidatedEvidenceSnapshot")
    profile_snapshot = StudentProfile(**profile.to_dict())
    if planning_profile is not None:
        if not isinstance(planning_profile, PlanningProfile):
            raise TypeError("planning_profile must be a PlanningProfile or None")
        if (
            planning_profile.province != profile_snapshot.province
            or planning_profile.subject_mode != profile_snapshot.subject_mode
            or planning_profile.subject_group != profile_snapshot.subject_group
            or frozenset(planning_profile.secondary_subjects) != frozenset(profile_snapshot.secondary_subjects)
            or planning_profile.grade != profile_snapshot.grade
        ):
            raise ValueError("planning_profile and report profile must describe one student context")
    capability = evidence.capability
    manifest = evidence.manifest
    tier, host, available, missing, degradations, python_version, optional = (
        _snapshot_capability(capability)
    )
    session_id, manifest_hash = _snapshot_manifest(manifest, tier)
    retrieval_date_snapshot = _date_tuple(
        evidence.retrieval_dates,
        "retrieval_dates",
        allow_empty=not evidence.candidates and not evidence.facts,
    )
    if not isinstance(recommendations, (RecommendationResult, SchoolDecisionResult)):
        raise TypeError(
            "recommendations must be a RecommendationResult or SchoolDecisionResult"
        )
    if rank is not None and not isinstance(rank, (RankEstimate, RankScenario)):
        raise TypeError("rank must be a RankEstimate, RankScenario, or None")
    if isinstance(recommendations, SchoolDecisionResult):
        if not isinstance(rank, RankScenario) or (
            rank.to_dict() != recommendations.rank_scenario.to_dict()
        ):
            raise ValueError("school decision result must share the report rank scenario")
        recommendation_items = recommendations.items
        recommendation_observations = recommendations.observations
        ordinary_batch_policy = (
            OrdinaryBatchPolicy(**recommendations.ordinary_batch_policy.to_dict())
            if recommendations.ordinary_batch_policy is not None
            else None
        )
        recommendation_policy_status = recommendations.policy_status
        school_decisions = tuple(
            _project_school_decision(item) for item in recommendations.decisions
        )
        recommendation_status = _aggregate_status(
            (
                *(item.evidence_status for item in recommendation_items),
                *(item.evidence_status for item in recommendation_observations),
            )
        )
        recommendation_warnings = _text_tuple(
            recommendations.warnings, "recommendation warnings"
        )
        compatibility = recommendations.compatibility_result
        if compatibility is not None:
            recommendation_status = _status(
                compatibility.coverage_status,
                "recommendation coverage status",
            )
            input_years = _year_tuple(
                compatibility.input_years,
                "recommendation input years",
            )
            usable_years = _year_tuple(
                compatibility.usable_years,
                "recommendation usable years",
            )
            verified_rank_coverage = compatibility.verified_rank_coverage
            recommendation_empty_reason = compatibility.empty_reason
        else:
            input_years = _year_tuple(
                sorted(
                    {
                        year
                        for item in recommendation_items
                        for year in item.supporting_years
                    }
                    | {item.data_year for item in recommendation_observations}
                ),
                "recommendation input years",
            )
            usable_years = _year_tuple(
                sorted(
                    {
                        year
                        for item in recommendation_items
                        for year in item.supporting_years
                    }
                ),
                "recommendation usable years",
            )
            verified_rank_coverage = (
                (
                    recommendations.rank_scenario.optimistic_rank,
                    recommendations.rank_scenario.conservative_rank,
                )
                if recommendation_items
                else None
            )
            recommendation_empty_reason = (
                None
                if recommendation_items
                else "partial_observations_only"
                if recommendation_observations
                else "profile_constraints"
            )
        excluded_by_subject_count = sum(
            decision.outcome == "excluded"
            and any(reason.code == "SCHOOL_SUBJECT_MISMATCH" for reason in decision.reasons)
            for decision in recommendations.decisions
        )
        zero_score_excluded_count = 0
    else:
        recommendation_items = recommendations.items
        recommendation_observations = recommendations.observations
        ordinary_batch_policy = OrdinaryBatchPolicy(
            **recommendations.ordinary_batch_policy.to_dict()
        )
        recommendation_policy_status = "ordinary_batch_policy_available"
        school_decisions = ()
        recommendation_status = _status(
            recommendations.coverage_status, "recommendation coverage status"
        )
        recommendation_warnings = _text_tuple(
            recommendations.warnings, "recommendation warnings"
        )
        input_years = _year_tuple(
            recommendations.input_years, "recommendation input years"
        )
        usable_years = _year_tuple(
            recommendations.usable_years, "recommendation usable years"
        )
        verified_rank_coverage = recommendations.verified_rank_coverage
        recommendation_empty_reason = recommendations.empty_reason
        excluded_by_subject_count = recommendations.excluded_by_subject_count
        zero_score_excluded_count = recommendations.zero_score_excluded_count
    projected_recommendations = tuple(
        _project_recommendation(item, profile_snapshot.rank, rank)
        for item in tuple(recommendation_items)
    )
    projected_school_observations = tuple(
        _project_school_observation(item)
        for item in tuple(recommendation_observations)
    )
    if isinstance(rank, RankEstimate):
        rank_snapshot = RankEstimate(**rank.to_dict())
    elif isinstance(rank, RankScenario):
        rank_snapshot = RankScenario._create(**rank.to_dict())
    else:
        rank_snapshot = None

    if pathways is None:
        pathways_available = False
        projected_pathways: tuple[ReportPathway, ...] = ()
        pathway_warnings: tuple[str, ...] = ()
        pathway_target_rank = None
        pathway_transformation = None
        model_source_ids: tuple[str, ...] = ()
        model_id = None
        model_method = None
        pathway_policy_evidence_status = None
        pathway_target_evidence_status = None
    else:
        if not isinstance(pathways, PathwayResult):
            raise TypeError("pathways must be a PathwayResult or None")
        pathways_available = True
        projected_pathways = tuple(_project_pathway(item) for item in tuple(pathways.items))
        pathway_warnings = _text_tuple(pathways.warnings, "pathway warnings")
        pathway_target_rank = pathways.target_rank
        pathway_transformation = pathways.transformation
        model_source_ids = _text_tuple(pathways.model_source_ids, "model source IDs", safe_ids=True, unique=True, sort=True)
        model_id = pathways.model_id
        model_method = pathways.model_method
        formal_statuses = tuple(
            item.evidence_status
            for item in projected_pathways
            if item.status == "formal"
        )
        pathway_policy_evidence_status = (
            _aggregate_status(formal_statuses)
            if pathway_target_rank is not None
            else None
        )
        pathway_target_evidence_status = pathways.model_evidence_status

    source_ids = {
        source_id
        for item in projected_recommendations
        for source_id in item.source_ids
    }
    source_ids.update(
        source_id
        for item in projected_school_observations
        for source_id in item.source_ids
    )
    source_ids.update(
        source_id
        for decision in school_decisions
        for reason in decision.reasons
        for source_id in reason.source_ids
    )
    if rank_snapshot is not None:
        source_ids.update(
            rank_snapshot.source_ids
            if isinstance(rank_snapshot, RankScenario)
            else rank_snapshot.contributing_source_ids
        )
    for item in projected_pathways:
        source_ids.update(item.source_ids)
    source_ids.update(model_source_ids)
    statuses = [recommendation_status]
    statuses.extend(
        status
        for item in projected_recommendations
        for status in item.fit_evidence_statuses
    )
    statuses.extend(
        reason.evidence_status
        for decision in school_decisions
        for reason in decision.reasons
        if reason.evidence_status is not None
    )
    statuses.append(rank_snapshot.status if rank_snapshot is not None else EvidenceStatus.MISSING)
    if projected_pathways:
        statuses.extend(item.evidence_status for item in projected_pathways)
    else:
        statuses.append(EvidenceStatus.MISSING)
    if pathway_target_evidence_status is not None:
        statuses.append(_status(pathway_target_evidence_status))
    warnings = tuple(
        dict.fromkeys(
            (
                *degradations,
                *recommendation_warnings,
                *pathway_warnings,
                *(("喜报位次证据不足：模型未提供；不执行校排名折算",) if rank_snapshot is None else ()),
                *(("多元升学结果未提供，本章节降级",) if not pathways_available else ()),
            )
        )
    )
    action_items = build_action_plan(
        planning_profile,
        rank_snapshot,
        projected_recommendations,
        projected_pathways,
        recommendation_status,
    )
    if len(action_items) < 3:
        raise ValueError("action plan must provide at least three priority actions")
    priority_count = 3
    priority_actions = action_items[:priority_count]
    action_timeline = _timeline(action_items[priority_count:])
    return ReportModel._create(
        profile=profile_snapshot,
        capability_tier=tier,
        query_coverage=_QUERY_COVERAGE[tier],
        host_capabilities=host,
        available_capabilities=available,
        missing_capabilities=missing,
        degradations=degradations,
        python_version=python_version,
        optional_modules=optional,
        recommendations=projected_recommendations,
        school_observations=projected_school_observations,
        ordinary_batch_policy=ordinary_batch_policy,
        recommendation_policy_status=recommendation_policy_status,
        school_decisions=school_decisions,
        recommendation_coverage_status=recommendation_status,
        verified_rank_coverage=verified_rank_coverage,
        recommendation_empty_reason=recommendation_empty_reason,
        recommendation_warnings=recommendation_warnings,
        excluded_by_subject_count=excluded_by_subject_count,
        zero_score_excluded_count=zero_score_excluded_count,
        input_years=input_years,
        usable_years=usable_years,
        rank=rank_snapshot,
        pathways_available=pathways_available,
        pathways=projected_pathways,
        pathway_warnings=pathway_warnings,
        pathway_target_rank=pathway_target_rank,
        pathway_transformation=pathway_transformation,
        model_source_ids=model_source_ids,
        model_id=model_id,
        model_method=model_method,
        pathway_policy_evidence_status=pathway_policy_evidence_status,
        pathway_target_evidence_status=pathway_target_evidence_status,
        manifest_session_id=session_id,
        manifest_hash=manifest_hash,
        retrieval_dates=retrieval_date_snapshot,
        source_ids=tuple(sorted(source_ids)),
        evidence_status=_aggregate_status(statuses),
        warnings=warnings,
        action_items=action_items,
        action_plan_digest=_action_digest(action_items),
        priority_actions=priority_actions,
        action_timeline=action_timeline,
    )


def _md(value: Any) -> str:
    text = str(value)
    replacements = (
        ("\\", "\\\\"),
        ("|", "\\|"),
        ("`", "\\`"),
        ("*", "\\*"),
        ("_", "\\_"),
        ("[", "\\["),
        ("]", "\\]"),
        ("<", "&lt;"),
        (">", "&gt;"),
    )
    for original, escaped in replacements:
        text = text.replace(original, escaped)
    return text


def _ids(values: tuple[str, ...]) -> str:
    return "、".join(_md(item) for item in values) if values else "无可公开来源编号"


def _table(headers: tuple[str, ...], rows: Iterable[tuple[Any, ...]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(_md(cell) for cell in row) + " |" for row in rows)
    return lines


def _empty_recommendation_text(model: ReportModel) -> str:
    reason = model.recommendation_empty_reason
    status = model.recommendation_coverage_status
    if reason == "partial_observations_only":
        return "仅发现部分覆盖的院校线索；这些学校仅作方向性观察，不进入冲稳保。"
    if reason == "no_match_within_verified_coverage" and status in _ACCEPTED_EXACT:
        return "经验证覆盖范围内未找到匹配院校；未硬凑冲稳保数量。"
    if reason == "no_match_within_verified_coverage":
        return "数据仅部分覆盖：当前已验证覆盖范围内未找到匹配院校，不能解释为没有符合院校。"
    if reason == "rank_outside_verified_coverage":
        return "用户位次超出已验证数据覆盖范围，未生成精确推荐。"
    if reason == "unusable_evidence":
        return "输入包含屏蔽、冲突或不可精确使用的证据，未生成数值边界。"
    if reason == "missing_verified_coverage":
        return "缺少可验证覆盖范围，未生成精确推荐。"
    return "当前证据未形成可展示的普通批推荐。"


def action_linkage_lines(
    model: ReportModel,
    item: ActionItem,
) -> tuple[str, str, str]:
    """Project action dependencies and machine targets into human labels."""

    if not isinstance(model, ReportModel) or not isinstance(item, ActionItem):
        raise TypeError("action linkage requires a ReportModel ActionItem pair")
    if item not in model.action_items:
        raise ValueError("action linkage item is outside the report action plan")
    action_titles = {
        action.action_id: action.title for action in model.action_items
    }
    school_titles = {
        f"school:{index}": recommendation.school_name
        for index, recommendation in enumerate(model.recommendations, 1)
    }
    pathway_titles = {
        pathway.policy_id: pathway.title for pathway in model.pathways
    }

    dependencies = "、".join(
        f"{action_titles.get(action_id, action_id)}（{action_id}）"
        for action_id in item.depends_on
    ) or "无"
    schools = "、".join(
        school_titles.get(school_id, school_id) for school_id in item.school_ids
    ) or "无"
    pathways = "、".join(
        pathway_titles.get(pathway_id, pathway_id)
        for pathway_id in item.pathway_ids
    ) or "无"
    return (
        f"依赖行动：{dependencies}",
        f"关联院校：{schools}",
        f"关联路径：{pathways}",
    )


def render_markdown(model: ReportModel) -> str:
    """Pure projection of a :class:`ReportModel`; no decision is recomputed."""

    if not isinstance(model, ReportModel):
        raise TypeError("model must be a ReportModel")
    profile = model.profile
    reminder = (
        "> ⚠️ 基于公开数据由 AI 整理，仅供参考；不构成升学建议或录取承诺，"
        "最终以当年官方发布为准。"
    )
    def action_lines(item: ActionItem) -> list[str]:
        linkage = action_linkage_lines(model, item)
        return [
            f"- **{_md(item.title)}**（{_md(item.phase)}；{_md(item.urgency)}）",
            f"  - 战略价值：{_md(item.strategic_value)}；投入：{_md(item.effort)}",
            f"  - 完成标准：{'；'.join(_md(value) for value in item.completion_criteria)}",
            f"  - 原因：{_md(item.reason)}；未完成后果：{_md(item.consequence)}",
            f"  - 截止：{_md(item.deadline) if item.deadline else '未提供具体日期'}；证据：{_STATUS_LABEL[item.evidence_status]}；来源：{_ids(item.source_ids)}",
            *(f"  - {_md(value)}" for value in linkage),
        ]

    lines = [
        f"# 匿名升学规划报告（{_md(profile.province)}）", "", reminder, "",
        "## 一、结论摘要与免责声明", "",
        f"- 年级：{_md(profile.grade)}；选科：{_md(profile.subject_mode)} / {_md(profile.subject_selection_key)}",
        f"- 当前定位位次：{profile.rank if profile.rank is not None else '暂无可靠位次'}；整份报告最低证据状态：{_STATUS_LABEL[model.evidence_status]}",
        f"- 能力档位：{_TIER_LABEL[model.capability_tier]}；证据置信度：{_CONFIDENCE_LABEL[model.evidence_status]}；查询覆盖：{_md(model.query_coverage)}",
        f"- 来源编号：{_ids(model.source_ids)}",
        "- 本报告是已认证材料的行动投影，不构成录取或资格承诺。", "",
    ]
    lines.extend(f"- 风险与缺失：{_md(item)}" for item in model.warnings)
    lines.extend([
        "", "## 二、当前最需要做的事", "",
        "- 以下行动按时间与价值排序。",
    ])
    for item in model.priority_actions:
        lines.extend(action_lines(item))
    lines.extend(["", "## 三、位次情景与置信度", ""])
    if isinstance(model.rank, RankScenario):
        rank = model.rank
        if rank.status in {EvidenceStatus.OFFICIAL, EvidenceStatus.INFERRED}:
            lines.extend(
                [
                    f"- 乐观位次：{rank.optimistic_rank}",
                    f"- 中性位次：{rank.central_rank}",
                    f"- 保守位次：{rank.conservative_rank}",
                    f"- 位次性质：{'官方' if rank.status is EvidenceStatus.OFFICIAL else '推断参考'}",
                    f"- 置信度：{_md(rank.confidence)}",
                    f"- 计算依据：{_md(rank.basis)}",
                    f"- 依据年份：{'、'.join(str(year) for year in rank.contributing_years) or '无'}",
                    f"- 位次来源编号：{_ids(rank.source_ids)}",
                ]
            )
        else:
            lines.append("当前没有可校准的位次依据；不制造数字，先保留路径判断并补充最小考试信息。")
    elif model.rank is None:
        lines.append("当前没有可校准的位次依据；不制造数字，先保留路径判断并补充最小考试信息。")
    elif model.rank.status is EvidenceStatus.INFERRED:
        rank = model.rank
        lines.extend(
            [
                f"- 推断位次区间：{rank.lower_rank}–{rank.upper_rank}",
                f"- 区间中位描述：{rank.median_rank} 位（推断，不是官方位次）",
                f"- 容差：±{rank.tolerance_rank} 位",
                f"- 置信度：{_md(rank.confidence)}",
                f"- 计算依据：{_md(rank.method)}",
                f"- 贡献年份：{'、'.join(str(year) for year in rank.contributing_years)}",
                f"- 贡献锚点：{_ids(rank.contributing_anchor_ids)}",
                f"- 锚点来源编号：{_ids(rank.contributing_source_ids)}",
            ]
        )
    else:
        lines.append(
            f"喜报位次证据{_STATUS_LABEL[model.rank.status]}：{_md(model.rank.reason_code or '未形成可用区间')}；未输出代理数值。"
        )

    lines.extend(["", "## 四、普通批代表院校", ""])
    if model.recommendations:
        lines.extend(
            _table(
                (
                    "档位", "院校", "最低分", "最低位次", "证据状态",
                    "来源编号", "决策理由", "计算依据",
                ),
                (
                    (
                        item.strategy,
                        item.school_name,
                        item.min_score,
                        item.min_rank,
                        _STATUS_LABEL[item.evidence_status],
                        "、".join(item.source_ids),
                        item.match_reason,
                        item.calculation_basis,
                    )
                    for item in model.recommendations
                ),
            )
        )
    else:
        lines.append(_empty_recommendation_text(model))
    if model.school_observations:
        lines.extend(["", "### 观察学校（部分覆盖，不进入冲稳保）", ""])
        lines.append(
            "以下院校仅作方向性观察；部分覆盖证据不能支持最低分、最低位次或冲稳保判断。"
        )
        lines.extend(
            _table(
                (
                    "院校",
                    "层次",
                    "城市",
                    "数据年份",
                    "证据状态",
                    "来源编号",
                    "处理结论",
                ),
                (
                    (
                        item.school_name,
                        item.school_level or "当前证据未提供",
                        item.city or "当前证据未提供",
                        item.data_year,
                        _STATUS_LABEL[item.evidence_status],
                        "、".join(item.source_ids),
                        "仅作方向性观察，不进入冲稳保",
                    )
                    for item in model.school_observations
                ),
            )
        )
    for warning in model.recommendation_warnings:
        lines.append(f"- 风险提示：{_md(warning)}")
    if model.school_decisions:
        lines.extend(["", "### 普通批逐维判断证据", ""])
        for decision in model.school_decisions:
            outcome_label = "纳入" if decision.outcome == "included" else "排除"
            for reason in decision.reasons:
                status_label = (
                    _STATUS_LABEL[reason.evidence_status]
                    if reason.evidence_status is not None
                    else "未单列"
                )
                lines.append(
                    f"- {_md(decision.school_name)}（{outcome_label}） · "
                    f"{_md(reason.dimension)}/[{reason.code}]："
                    f"{_md(reason.explanation)}；证据等级：{status_label}；"
                    f"来源编号：{_ids(reason.source_ids)}"
                )
    excluded_school_decisions = tuple(
        item for item in model.school_decisions if item.outcome == "excluded"
    )
    if excluded_school_decisions:
        lines.extend(["", "### 普通批排除审计", ""])
        for decision in excluded_school_decisions:
            reasons = "；".join(
                f"[{reason.code}] {reason.explanation}"
                for reason in decision.reasons
            )
            lines.append(f"- {_md(decision.school_name)}：{_md(reasons)}")
    lines.extend(["", reminder])
    lines.extend(["", "## 五、多元升学路径矩阵", ""])
    if not model.pathways_available:
        lines.append("多元升学数据不足：未提供经验证的政策结果，本章节不作正式推荐。")
    elif not model.pathways:
        lines.append("多元升学数据不足：未形成正式或待核实路径；不套用无依据的位次修正。")
    else:
        lines.extend(
            _table(
                (
                    "路径", "院校", "投入结论", "资格状态", "政策证据状态", "政策来源编号",
                    "专业选项", "培养安排", "转段规则", "毕业/升学出口",
                    "服务/就业义务", "退出/违约规则", "费用/补助",
                    "已满足条件", "待核实约束", "时间线", "当前行动", "决策理由", "计算依据",
                ),
                (
                    (
                        item.title,
                        item.institution,
                        item.investment_decision,
                        item.qualification_status,
                        _STATUS_LABEL[item.evidence_status],
                        "、".join(item.source_ids),
                        "、".join(item.professional_options) or "当前证据未提供",
                        item.training_arrangements or "当前证据未提供",
                        item.transition_rules or "当前证据未提供",
                        item.outcomes or "当前证据未提供",
                        item.service_employment_obligations or "当前证据未提供",
                        item.penalty_exit_rules or "当前证据未提供",
                        item.fees_and_subsidies or "当前证据未提供",
                        "；".join(item.satisfied_conditions) or "无",
                        "；".join(item.missing_constraints) or "无",
                        "；".join(item.timeline) or "待当年政策确认",
                        "；".join(item.preparation_actions) or "待补充可执行动作",
                        (
                            "；".join(
                                f"[{reason.code}] {reason.explanation}"
                                for reason in item.decision_reasons
                            )
                            or "未提供画像决策审计"
                        ),
                        item.calculation_basis,
                    )
                    for item in model.pathways
                ),
            )
        )
        for item in model.pathways:
            lines.extend(
                [
                    "",
                    f"### 逐字段证据审计：{_md(item.title)} · {_md(item.institution)}",
                    "",
                    *(f"- {line}" for line in pathway_field_evidence_lines(item)),
                ]
            )
    if model.pathway_target_rank is not None:
        assert model.pathway_policy_evidence_status is not None
        assert model.pathway_target_evidence_status is not None
        lines.extend(
            [
                f"- 有依据的路径目标位次：{model.pathway_target_rank}；位次模型证据状态：{_STATUS_LABEL[model.pathway_target_evidence_status]}",
                f"- 正式路径政策证据状态：{_STATUS_LABEL[model.pathway_policy_evidence_status]}",
                f"- 位次模型标识：{_md(model.model_id)}；方法：{_md(model.model_method)}",
                f"- 转换过程：{_md(model.pathway_transformation)}",
                f"- 模型来源编号：{_ids(model.model_source_ids)}",
            ]
        )
    for warning in model.pathway_warnings:
        lines.append(f"- 风险提示：{_md(warning)}")

    lines.extend(["", "## 六、详细路径缺口", ""])
    if model.pathways:
        for item in model.pathways:
            lines.append(f"- {_md(item.title)}：{'；'.join(_md(value) for value in item.missing_constraints) or '当前无已知缺口'}")
    else:
        lines.append("- 当前没有可展开的路径缺口。")

    lines.extend(["", "## 七、分阶段时间表", ""])
    if model.action_timeline:
        for group in model.action_timeline:
            lines.extend([f"### {_md(group.phase)}", ""])
            for item in group.actions:
                lines.extend(action_lines(item))
    else:
        lines.append("- 当前优先行动已覆盖完整行动计划。")

    lines.extend(
        [
            "",
            "## 八、证据披露",
            "",
            f"- 查询覆盖：{_md(model.query_coverage)}；检索日期："
            + (
                "、".join(model.retrieval_dates)
                if model.retrieval_dates
                else "无可验证检索日期"
            ),
            f"- 数据覆盖：{_STATUS_LABEL[model.recommendation_coverage_status]}；普通批输入年份：{'、'.join(str(year) for year in model.input_years) or '无'}",
            f"- 普通批可用年份：{'、'.join(str(year) for year in model.usable_years) or '无'}",
            *(
                (f"- 普通批已验证位次覆盖：{model.verified_rank_coverage[0]}–{model.verified_rank_coverage[1]}",)
                if model.verified_rank_coverage is not None else ()
            ),
            *(
                (
                    f"- 普通批策略：{_md(model.ordinary_batch_policy.policy_id)}；依据：{_md(model.ordinary_batch_policy.basis_id)}",
                    f"- 普通批位次差策略：检索Δ[{model.ordinary_batch_policy.search_delta_min},{model.ordinary_batch_policy.search_delta_max}]；冲< {model.ordinary_batch_policy.challenge_delta_lt}；稳≤ {model.ordinary_batch_policy.stable_delta_le}；上限冲={model.ordinary_batch_policy.tier_caps['冲']}、稳={model.ordinary_batch_policy.tier_caps['稳']}、保={model.ordinary_batch_policy.tier_caps['保']}",
                )
                if model.ordinary_batch_policy is not None
                else ("- 普通批位次差策略：不可用；未使用位次差阈值。",)
            ),
            f"- 来源编号：{_ids(model.source_ids)}",
            f"- 证据包清单哈希：{_md(model.manifest_hash)}",
            "- 报告只展示安全来源编号，不展示原始 URL 或本机路径。",
            "",
            reminder,
            "> 屏蔽值、冲突、部分覆盖与缺失数据均未被补成精确边界；请以省教育考试院和高校当年正式信息为准。",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


__all__ = [
    "ActionTimelinePhase",
    "ReportModel",
    "ReportPathway",
    "ReportRecommendation",
    "ReportSchoolObservation",
    "StudentProfile",
    "action_linkage_lines",
    "build_report_model",
    "pathway_field_evidence_lines",
    "render_markdown",
    "validate_profile_text",
]
