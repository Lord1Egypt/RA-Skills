# -*- coding: utf-8 -*-
"""Province-neutral, evidence-aware ordinary-batch school matching.

The public API accepts normalized rows plus an explicit profile and always
returns an immutable recommendation result. Evidence coverage and provenance
must already be present on the rows; this module never fabricates either.
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from typing import Any, Optional

if __package__:
    from .contracts import (
        EvidenceStatus,
        OrdinaryBatchPolicy,
        RecommendationItem,
        RecommendationMajorGroup,
        RecommendationProfile,
        RecommendationResult,
        SchoolObservation,
    )
    from .rank_locator import RankScenario
    from .decision_policy import (
        DecisionPolicySnapshot,
        DecisionReason,
        risk_tier_caps,
    )
    from .planning_profile import PlanningProfile
else:
    from contracts import (
        EvidenceStatus,
        OrdinaryBatchPolicy,
        RecommendationItem,
        RecommendationMajorGroup,
        RecommendationProfile,
        RecommendationResult,
        SchoolObservation,
    )
    from rank_locator import RankScenario
    from decision_policy import DecisionPolicySnapshot, DecisionReason, risk_tier_caps
    from planning_profile import PlanningProfile


LEVEL_ORDER = {"985": 0, "211": 1, "双一流": 2}

_ACCEPTED_EXACT_STATUSES = {
    EvidenceStatus.OFFICIAL,
    EvidenceStatus.CORROBORATED,
    EvidenceStatus.REFERENCE,
}
_USABLE_COVERAGE_STATUSES = _ACCEPTED_EXACT_STATUSES
_ISSUE_PRECEDENCE = (
    EvidenceStatus.CONFLICT,
    EvidenceStatus.MASKED,
    EvidenceStatus.PARTIAL,
    EvidenceStatus.MISSING,
)
_ACCEPTED_PRECEDENCE = (
    EvidenceStatus.REFERENCE,
    EvidenceStatus.CORROBORATED,
    EvidenceStatus.OFFICIAL,
)

_PROVINCE_ALIASES = {
    "北京": "北京", "北京市": "北京", "天津": "天津", "天津市": "天津",
    "上海": "上海", "上海市": "上海", "重庆": "重庆", "重庆市": "重庆",
    "河北": "河北", "河北省": "河北", "山西": "山西", "山西省": "山西",
    "辽宁": "辽宁", "辽宁省": "辽宁", "吉林": "吉林", "吉林省": "吉林",
    "黑龙江": "黑龙江", "黑龙江省": "黑龙江", "江苏": "江苏", "江苏省": "江苏",
    "浙江": "浙江", "浙江省": "浙江", "安徽": "安徽", "安徽省": "安徽",
    "福建": "福建", "福建省": "福建", "江西": "江西", "江西省": "江西",
    "山东": "山东", "山东省": "山东", "河南": "河南", "河南省": "河南",
    "湖北": "湖北", "湖北省": "湖北", "湖南": "湖南", "湖南省": "湖南",
    "广东": "广东", "广东省": "广东", "海南": "海南", "海南省": "海南",
    "四川": "四川", "四川省": "四川", "贵州": "贵州", "贵州省": "贵州",
    "云南": "云南", "云南省": "云南", "陕西": "陕西", "陕西省": "陕西",
    "甘肃": "甘肃", "甘肃省": "甘肃", "青海": "青海", "青海省": "青海",
    "内蒙古": "内蒙古", "内蒙古自治区": "内蒙古",
    "广西": "广西", "广西壮族自治区": "广西",
    "西藏": "西藏", "西藏自治区": "西藏",
    "宁夏": "宁夏", "宁夏回族自治区": "宁夏",
    "新疆": "新疆", "新疆维吾尔自治区": "新疆",
    "香港": "香港", "香港特别行政区": "香港",
    "澳门": "澳门", "澳门特别行政区": "澳门",
    "台湾": "台湾", "台湾省": "台湾",
}
_OFFICIAL_PROVINCE_NAMES = frozenset(_PROVINCE_ALIASES) | frozenset(
    _PROVINCE_ALIASES.values()
)

_SUBJECT_REQ_RE = re.compile(r"再选科目：([^；]+)")
_SUBJECT_SPLIT_RE = re.compile(r"(?:和|、|/|，|,|\s)+")
_SELECTION_SPLIT_RE = re.compile(r"(?:和|或|、|/|，|,|\s)+")


class SchoolRecommendError(Exception):
    """Controlled recommendation error carrying a stable public code."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True)
class SchoolDecision:
    """Parallel audit record that leaves RecommendationItem compatibility intact."""

    school_name: str
    outcome: str
    order: int | None
    stable_key: tuple[str, ...]
    reasons: tuple[DecisionReason, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.school_name, str) or not self.school_name.strip():
            raise ValueError("school decision requires a school name")
        if self.outcome not in {"included", "excluded"}:
            raise ValueError("school decision outcome is unsupported")
        if self.outcome == "included":
            if not isinstance(self.order, int) or isinstance(self.order, bool) or self.order < 1:
                raise ValueError("included school decisions require a positive order")
        elif self.order is not None:
            raise ValueError("excluded school decisions cannot carry an order")
        if not self.stable_key or not all(isinstance(item, str) for item in self.stable_key):
            raise ValueError("school decision requires a stable key")
        if not self.reasons or not all(isinstance(item, DecisionReason) for item in self.reasons):
            raise ValueError("school decision requires finite decision reasons")

    def to_dict(self) -> dict[str, Any]:
        return {
            "school_name": self.school_name,
            "outcome": self.outcome,
            "order": self.order,
            "stable_key": list(self.stable_key),
            "reasons": [item.to_dict() for item in self.reasons],
        }


@dataclass(frozen=True)
class SchoolDecisionResult:
    """Full-profile result independent of the legacy batch-policy contract."""

    items: tuple[RecommendationItem, ...]
    decisions: tuple[SchoolDecision, ...]
    rank_scenario: RankScenario
    policy_status: str
    ordinary_batch_policy: OrdinaryBatchPolicy | None = None
    warnings: tuple[str, ...] = ()
    compatibility_result: RecommendationResult | None = None
    observations: tuple[SchoolObservation, ...] = ()

    def __post_init__(self) -> None:
        items = tuple(self.items)
        if not all(isinstance(item, RecommendationItem) for item in items):
            raise TypeError("items must contain RecommendationItem records")
        if not isinstance(self.rank_scenario, RankScenario):
            raise TypeError("rank_scenario must be an authenticated RankScenario")
        if self.policy_status not in {
            "ordinary_batch_policy_available",
            "rank_delta_policy_unavailable",
        }:
            raise ValueError("school policy status is unsupported")
        ordinary_policy = self.ordinary_batch_policy
        if self.policy_status == "ordinary_batch_policy_available":
            if not isinstance(ordinary_policy, OrdinaryBatchPolicy):
                raise TypeError("available ordinary-batch policy must be explicit")
            ordinary_policy = OrdinaryBatchPolicy(**ordinary_policy.to_dict())
        elif ordinary_policy is not None:
            raise ValueError("unavailable rank-delta policy cannot carry a policy")
        warnings = tuple(self.warnings)
        if any(not isinstance(item, str) or not item.strip() for item in warnings):
            raise ValueError("school decision warnings must be public text")
        compatibility = self.compatibility_result
        if compatibility is not None:
            if not isinstance(compatibility, RecommendationResult):
                raise TypeError("compatibility_result must be a RecommendationResult")
            if self.policy_status != "ordinary_batch_policy_available":
                raise ValueError("legacy results require an available ordinary-batch policy")
            if tuple(compatibility.items) != items:
                raise ValueError("legacy result items must match school decision items")
            if compatibility.ordinary_batch_policy != ordinary_policy:
                raise ValueError("legacy result and wrapper policies must match")
            if tuple(compatibility.observations) != tuple(self.observations):
                raise ValueError("legacy result observations must match school decisions")
        elif self.policy_status != "rank_delta_policy_unavailable":
            raise ValueError("available ordinary-batch policy requires its compatibility result")
        decisions = tuple(self.decisions)
        if not all(isinstance(item, SchoolDecision) for item in decisions):
            raise TypeError("decisions must contain SchoolDecision records")
        names = tuple(item.school_name for item in decisions)
        if len(names) != len(set(names)):
            raise ValueError("school decisions must have unique school names")
        included = tuple(
            item.school_name for item in sorted(
                (item for item in decisions if item.outcome == "included"),
                key=lambda item: item.order,
            )
        )
        if included != tuple(item.school_name for item in items):
            raise ValueError("school decisions do not match recommendation ordering")
        observations = tuple(self.observations)
        if not all(isinstance(item, SchoolObservation) for item in observations):
            raise TypeError("observations must contain SchoolObservation records")
        object.__setattr__(self, "items", items)
        object.__setattr__(self, "decisions", decisions)
        object.__setattr__(self, "ordinary_batch_policy", ordinary_policy)
        object.__setattr__(self, "warnings", warnings)
        object.__setattr__(self, "observations", observations)

    @property
    def recommendations(self) -> RecommendationResult:
        """Compatibility projection for callers that supplied a real policy."""

        if self.compatibility_result is None:
            raise AttributeError("rank-delta policy is unavailable for this result")
        return self.compatibility_result

    def decision(self, school_name: str) -> SchoolDecision:
        matches = tuple(item for item in self.decisions if item.school_name == school_name)
        if len(matches) != 1:
            raise KeyError("school decision is unavailable")
        return matches[0]

    def to_dict(self) -> dict[str, Any]:
        return {
            "items": [item.to_dict() for item in self.items],
            "decisions": [item.to_dict() for item in self.decisions],
            "rank_scenario": self.rank_scenario.to_dict(),
            "policy_status": self.policy_status,
            "ordinary_batch_policy": (
                self.ordinary_batch_policy.to_dict()
                if self.ordinary_batch_policy is not None
                else None
            ),
            "warnings": list(self.warnings),
            "observations": [item.to_dict() for item in self.observations],
            "compatibility_result": (
                self.compatibility_result.to_dict()
                if self.compatibility_result is not None
                else None
            ),
        }


def _tier(delta: int, challenge_delta_lt: int, stable_delta_le: int) -> str:
    if delta < challenge_delta_lt:
        return "冲"
    return "稳" if delta <= stable_delta_le else "保"


def _canonical_province(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = value.strip()
    if not normalized:
        return None
    known = _PROVINCE_ALIASES.get(normalized)
    if known is not None:
        return known
    if not re.fullmatch(r"[A-Za-z0-9一-鿿]{2,20}", normalized):
        return None
    for suffix in ("特别行政区", "自治区", "省", "市"):
        if normalized.endswith(suffix) and len(normalized) > len(suffix):
            base = normalized[:-len(suffix)]
            if base in _OFFICIAL_PROVINCE_NAMES:
                return None
            return base
    return normalized


def is_in_province(school_province: object, target_province: object) -> bool:
    """Compare exact canonical administrative names without fuzzy matching."""

    school = _canonical_province(school_province)
    target = _canonical_province(target_province)
    return school is not None and target is not None and school == target


def parse_secondary_subjects(text: object) -> frozenset[str]:
    """Parse an explicit selection from a string or a sequence of strings."""

    if text is None:
        return frozenset()
    if isinstance(text, str):
        values = _SELECTION_SPLIT_RE.split(text.strip()) if text.strip() else []
    elif isinstance(text, Sequence) and not isinstance(text, (bytes, bytearray)):
        if not all(isinstance(value, str) for value in text):
            return frozenset()
        values = [part for value in text for part in _SELECTION_SPLIT_RE.split(value.strip())]
    elif isinstance(text, frozenset):
        if not all(isinstance(value, str) for value in text):
            return frozenset()
        values = list(text)
    else:
        return frozenset()
    return frozenset(value for value in values if value)


def _subject_required(remarks: str) -> Optional[list[set[str]]]:
    """One-release parser for legacy ``再选科目：`` remarks."""

    match = _SUBJECT_REQ_RE.search(remarks or "")
    if not match:
        return None
    text = match.group(1).strip()
    if text in ("不限", "", "无"):
        return []
    return [
        {token for token in _SUBJECT_SPLIT_RE.split(alternative) if token}
        for alternative in re.split(r"或", text)
        if alternative.strip()
    ]


def _subject_match(row: Mapping[str, Any], selected: frozenset[str]) -> bool:
    if "required_secondary_subjects" in row or "secondary_subject_rule" in row:
        rule = row.get("secondary_subject_rule")
        required = parse_secondary_subjects(row.get("required_secondary_subjects"))
        if rule not in {"any", "all"}:
            return False
        if not required:
            return True
        if not selected:
            return False
        return bool(required & selected) if rule == "any" else required <= selected

    legacy = _subject_required(str(row.get("remarks") or row.get("remark") or ""))
    if legacy is None or not legacy:
        return True
    if not selected:
        return True  # Legacy omission meant "do not filter" for one release.
    return any(requirement <= selected for requirement in legacy)


def _strict_int(value: object) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _status(value: object) -> EvidenceStatus | None:
    if isinstance(value, EvidenceStatus):
        return value
    if isinstance(value, str):
        try:
            return EvidenceStatus(value)
        except ValueError:
            return None
    return None


def _source_ids(row: Mapping[str, Any]) -> tuple[str, ...]:
    raw = row.get("source_ids")
    if raw is None and isinstance(row.get("source_id"), str):
        raw = (row["source_id"],)
    if isinstance(raw, str):
        raw = (raw,)
    if not isinstance(raw, (tuple, list)):
        return ()
    values = {value.strip() for value in raw if isinstance(value, str) and value.strip()}
    return tuple(sorted(values))


def _fit_source_ids(
    rows: Sequence[Mapping[str, Any]], kind: str | None = None
) -> tuple[str, ...]:
    field = {
        "enrollment_plan": "school_fit_enrollment_source_ids",
        "admission_charter": "school_fit_charter_source_ids",
        "tuition_fee": "school_fit_tuition_source_ids",
        "subject_requirement": "school_fit_subject_source_ids",
        "province_policy": "school_fit_province_policy_source_ids",
        None: "school_fit_source_ids",
    }[kind]
    values: set[str] = set()
    for row in rows:
        raw = row.get(field)
        if isinstance(raw, str):
            raw = (raw,)
        if isinstance(raw, (tuple, list)):
            values.update(
                item.strip()
                for item in raw
                if isinstance(item, str) and item.strip()
            )
    if not values and kind is not None and any(
        kind in tuple(row.get("school_fit_conflict_kinds") or ())
        for row in rows
    ):
        return _fit_source_ids(rows)
    return tuple(sorted(values))


def _fit_evidence_status(
    rows: Sequence[Mapping[str, Any]], kind: str
) -> EvidenceStatus:
    """Return the conservative authenticated status for one fit dimension."""

    status_field = {
        "enrollment_plan": "school_fit_enrollment_status",
        "admission_charter": "school_fit_charter_status",
        "tuition_fee": "school_fit_tuition_status",
        "subject_requirement": "school_fit_subject_status",
        "province_policy": "school_fit_province_policy_status",
    }[kind]
    if any(
        kind in tuple(row.get("school_fit_conflict_kinds") or ())
        for row in rows
    ):
        return EvidenceStatus.CONFLICT
    statuses = {
        status
        for row in rows
        if (status := _status(row.get(status_field))) is not None
    }
    for candidate in (
        EvidenceStatus.CONFLICT,
        EvidenceStatus.PARTIAL,
        EvidenceStatus.MISSING,
        EvidenceStatus.REFERENCE,
        EvidenceStatus.CORROBORATED,
        EvidenceStatus.OFFICIAL,
    ):
        if candidate in statuses:
            return candidate
    return EvidenceStatus.MISSING


def _usable_fit_dimension(
    rows: Sequence[Mapping[str, Any]], kind: str
) -> bool:
    return bool(_fit_source_ids(rows, kind)) and _fit_evidence_status(
        rows, kind
    ) in {
        EvidenceStatus.OFFICIAL,
        EvidenceStatus.CORROBORATED,
        EvidenceStatus.REFERENCE,
    }


def _major_tokens(categories: Iterable[str]) -> list[str]:
    tokens: list[str] = []
    for category in categories:
        tokens.extend(
            token for token in re.split(r"[^一-鿿A-Za-z0-9]+", category or "")
            if len(token) >= 2
        )
    return tokens


def _matched_tokens(majors_text: str, tokens: list[str]) -> list[str]:
    return [token for token in tokens if token and token in majors_text]


def _majors_text(raw: object) -> str:
    if raw in (None, ""):
        return ""
    try:
        items = json.loads(raw) if isinstance(raw, str) else raw
        if isinstance(items, list):
            return "、".join(str(item) for item in items)
    except (ValueError, TypeError):
        pass
    return str(raw)


def _program_group_name(row: Mapping[str, Any]) -> str:
    return str(row.get("major_group_name") or row.get("program_group") or "")


def _program_group_identity(row: Mapping[str, Any]) -> str:
    return str(row.get("major_group_code") or _program_group_name(row))


def _is_intent(school_name: str, preferences: Iterable[str]) -> bool:
    for preference in preferences:
        value = (preference or "").strip()
        if value == school_name or (
            len(value) >= 4 and (value in school_name or school_name in value)
        ):
            return True
    return False


def _profile(value: RecommendationProfile | Mapping[str, Any]) -> RecommendationProfile:
    if isinstance(value, RecommendationProfile):
        return RecommendationProfile(
            rank=value.rank,
            target_province=value.target_province,
            subject_group=value.subject_group,
            secondary_subjects=frozenset(value.secondary_subjects),
            target_major_categories=tuple(value.target_major_categories),
            target_cities=tuple(value.target_cities),
            target_schools=tuple(value.target_schools),
            rank_basis=value.rank_basis,
            optimistic_rank=value.optimistic_rank,
            conservative_rank=value.conservative_rank,
            rank_confidence=value.rank_confidence,
            rank_source_ids=value.rank_source_ids,
        )
    if not isinstance(value, Mapping):
        raise SchoolRecommendError("REC_001", "推荐输入缺少有效参考位次")
    try:
        raw_secondary = value.get("secondary_subjects", ())
        return RecommendationProfile(
            rank=value.get("rank"),
            target_province=value.get("target_province", ""),
            subject_group=value.get("subject_group", ""),
            secondary_subjects=(
                parse_secondary_subjects(raw_secondary)
                if isinstance(raw_secondary, str)
                else raw_secondary
            ),
            target_major_categories=value.get("target_major_categories", ()),
            target_cities=value.get("target_cities", ()),
            target_schools=value.get("target_schools", ()),
            rank_basis=value.get("rank_basis", "official"),
            optimistic_rank=value.get("optimistic_rank"),
            conservative_rank=value.get("conservative_rank"),
            rank_confidence=value.get("rank_confidence", "official"),
            rank_source_ids=value.get("rank_source_ids", ()),
        )
    except (TypeError, ValueError) as error:
        raise SchoolRecommendError("REC_001", "推荐输入格式无效") from error


def _coverage_status(statuses: set[EvidenceStatus]) -> EvidenceStatus:
    for status in _ISSUE_PRECEDENCE:
        if status in statuses:
            return status
    for status in _ACCEPTED_PRECEDENCE:
        if status in statuses:
            return status
    return EvidenceStatus.MISSING


def _warning_for_status(status: EvidenceStatus) -> str | None:
    return {
        EvidenceStatus.CONFLICT: "证据存在冲突，冲突行未进入精确推荐。",
        EvidenceStatus.MASKED: "数据包含屏蔽值、OCR 不确定值或非严格整数，相关行未进入精确推荐。",
        EvidenceStatus.PARTIAL: "数据覆盖不完整；结论仅适用于当前已验证覆盖范围内。",
        EvidenceStatus.MISSING: "部分数据缺少可验证状态、来源或覆盖元数据。",
    }.get(status)


def _partial_school_observations(
    rows: Sequence[Mapping[str, Any]],
) -> tuple[SchoolObservation, ...]:
    """Project authenticated partial rows without retaining numeric fields."""

    grouped: dict[tuple[str, int], list[SchoolObservation]] = {}
    for row in rows:
        status = _status(row.get("evidence_status"))
        coverage_status = _status(row.get("coverage_status"))
        if EvidenceStatus.PARTIAL not in {status, coverage_status}:
            continue
        if status not in _ACCEPTED_EXACT_STATUSES | {EvidenceStatus.PARTIAL}:
            continue
        if coverage_status not in _ACCEPTED_EXACT_STATUSES | {EvidenceStatus.PARTIAL}:
            continue
        school_name = str(row.get("school_name") or "").strip()
        year = _strict_int(row.get("year"))
        sources = _source_ids(row)
        if not school_name or year is None or not 2000 <= year <= 2100 or not sources:
            continue
        try:
            observation = SchoolObservation(
                school_name=school_name,
                school_level=str(row.get("school_level") or ""),
                city=str(row.get("city_location") or ""),
                data_year=year,
                source_ids=sources,
                evidence_status=EvidenceStatus.PARTIAL,
                reason_code="partial_coverage_not_used_for_exact_calculation",
            )
        except (TypeError, ValueError):
            continue
        grouped.setdefault((school_name, year), []).append(observation)
    observations: list[SchoolObservation] = []
    for (school_name, year), values in grouped.items():
        levels = {item.school_level for item in values if item.school_level}
        cities = {item.city for item in values if item.city}
        observations.append(
            SchoolObservation(
                school_name=school_name,
                school_level=next(iter(levels)) if len(levels) == 1 else "",
                city=next(iter(cities)) if len(cities) == 1 else "",
                data_year=year,
                source_ids=tuple(
                    sorted(
                        {
                            source_id
                            for item in values
                            for source_id in item.source_ids
                        }
                    )
                ),
                evidence_status=EvidenceStatus.PARTIAL,
                reason_code="partial_coverage_not_used_for_exact_calculation",
            )
        )
    return tuple(
        sorted(
            observations,
            key=lambda item: (item.school_name, -item.data_year, item.source_ids),
        )
    )


def _verified_coverage_for_rows(
    rows: Sequence[Mapping[str, Any]],
) -> tuple[tuple[int, int] | None, bool]:
    """Return the conservative intersection of source-bound coverage ranges."""

    ranges: list[tuple[int, int]] = []
    for row in rows:
        status = _status(row.get("evidence_status"))
        coverage_status = _status(row.get("coverage_status"))
        coverage_min = _strict_int(row.get("coverage_min_rank"))
        coverage_max = _strict_int(row.get("coverage_max_rank"))
        if (
            status not in _ACCEPTED_EXACT_STATUSES
            or coverage_status not in _USABLE_COVERAGE_STATUSES
            or not _source_ids(row)
            or coverage_min is None
            or coverage_max is None
            or coverage_min < 1
            or coverage_max < coverage_min
        ):
            continue
        ranges.append((coverage_min, coverage_max))
    if not ranges:
        return None, False
    intersection = (
        max(value[0] for value in ranges),
        min(value[1] for value in ranges),
    )
    if intersection[0] > intersection[1]:
        return None, True
    return intersection, False


def _recommend_core(
    rows: Sequence[Mapping[str, Any]],
    profile: RecommendationProfile,
    policy: OrdinaryBatchPolicy,
) -> RecommendationResult:
    rank = _strict_int(profile.rank)
    if rank is None or rank < 1:
        raise SchoolRecommendError("REC_001", "参考位次缺失或超出合理范围，请先完成折算")
    target = _canonical_province(profile.target_province)
    if target is None:
        raise SchoolRecommendError("REC_002", "目标省份缺失或不是受支持的行政区名称")

    selected = frozenset(profile.secondary_subjects)
    context_rows: list[dict[str, Any]] = []
    for original in rows:
        if not isinstance(original, Mapping):
            continue
        row = dict(original)
        admission_province = row.get("province")
        if not is_in_province(admission_province, target):
            continue
        row_group = row.get("subject_group")
        if profile.subject_group and row_group and row_group != profile.subject_group:
            continue
        context_rows.append(row)

    input_years = tuple(sorted({
        year for row in context_rows
        if (year := _strict_int(row.get("year"))) is not None
    }))
    excluded_by_subject = 0
    subject_rows: list[dict[str, Any]] = []
    for row in context_rows:
        if _subject_match(row, selected):
            subject_rows.append(row)
        else:
            excluded_by_subject += 1

    statuses: set[EvidenceStatus] = set()
    verified_ranges: list[tuple[int, int]] = []
    usable: list[dict[str, Any]] = []
    zero_score_excluded = 0
    for row in subject_rows:
        status = _status(row.get("evidence_status"))
        statuses.add(status or EvidenceStatus.MISSING)
        coverage_status = _status(row.get("coverage_status"))
        statuses.add(coverage_status or EvidenceStatus.MISSING)

        coverage_min = _strict_int(row.get("coverage_min_rank"))
        coverage_max = _strict_int(row.get("coverage_max_rank"))
        if coverage_min is None or coverage_max is None:
            statuses.add(EvidenceStatus.MISSING)
        elif coverage_min < 1 or coverage_max < coverage_min:
            statuses.add(EvidenceStatus.CONFLICT)
        elif (
            status in _ACCEPTED_EXACT_STATUSES
            and coverage_status in _USABLE_COVERAGE_STATUSES
        ):
            verified_ranges.append((coverage_min, coverage_max))

        min_score = _strict_int(row.get("min_score"))
        zero_score = min_score is not None and min_score <= 0
        if zero_score:
            zero_score_excluded += 1
            statuses.add(EvidenceStatus.PARTIAL)

        if any(bool(row.get(flag)) for flag in (
            "masked", "is_masked", "ocr_uncertain", "value_uncertain",
        )):
            statuses.add(EvidenceStatus.MASKED)
            continue
        min_rank = _strict_int(row.get("min_rank"))
        year = _strict_int(row.get("year"))
        if min_rank is None or min_score is None:
            statuses.add(EvidenceStatus.MASKED)
            continue
        if zero_score:
            if min_rank < 1 or year is None:
                statuses.add(EvidenceStatus.MISSING)
            continue
        if min_rank < 1 or year is None:
            statuses.add(EvidenceStatus.MISSING)
            continue
        sources = _source_ids(row)
        if not sources:
            statuses.add(EvidenceStatus.MISSING)
            continue
        if status not in _ACCEPTED_EXACT_STATUSES:
            continue
        if coverage_status not in _USABLE_COVERAGE_STATUSES:
            continue
        if coverage_min is None or coverage_max is None or coverage_max < coverage_min:
            continue
        if not coverage_min <= rank <= coverage_max:
            continue
        if (
            coverage_status is EvidenceStatus.PARTIAL
            and not coverage_min <= min_rank <= coverage_max
        ):
            statuses.add(EvidenceStatus.CONFLICT)
            continue
        snapshot = dict(row)
        snapshot.update({
            "min_rank": min_rank,
            "min_score": min_score,
            "year": year,
            "_status": _coverage_status({status, coverage_status}),
            "_source_ids": sources,
        })
        usable.append(snapshot)

    observations = _partial_school_observations(subject_rows)
    verified_coverage: tuple[int, int] | None = None
    if verified_ranges:
        intersection = (
            max(value[0] for value in verified_ranges),
            min(value[1] for value in verified_ranges),
        )
        if intersection[0] <= intersection[1]:
            verified_coverage = intersection
        else:
            statuses.add(EvidenceStatus.CONFLICT)
    else:
        statuses.add(EvidenceStatus.MISSING)

    usable_years = tuple(sorted({row["year"] for row in usable}))
    empty_reason: str | None = None
    candidate_rows: list[dict[str, Any]] = []
    if verified_coverage is None:
        empty_reason = "missing_verified_coverage"
    elif not (verified_coverage[0] <= rank <= verified_coverage[1]):
        empty_reason = "rank_outside_verified_coverage"
    elif usable:
        latest_year = max(row["year"] for row in usable)
        lo = max(1, rank + policy.search_delta_min)
        hi = rank + policy.search_delta_max
        candidate_rows = [
            row for row in usable
            if row["year"] == latest_year and lo <= row["min_rank"] <= hi
        ]

    tokens = _major_tokens(profile.target_major_categories)
    by_school: dict[str, list[dict[str, Any]]] = {}
    for row in sorted(candidate_rows, key=lambda value: (
        value["min_rank"], str(value.get("school_name") or ""),
        _program_group_identity(value),
    )):
        school_name = str(row.get("school_name") or "").strip()
        if not school_name:
            statuses.add(EvidenceStatus.MISSING)
            continue
        by_school.setdefault(school_name, []).append(row)

    sortable: list[tuple[tuple[Any, ...], RecommendationItem]] = []
    for school_name, groups in by_school.items():
        representative = min(groups, key=lambda group: (
            group["min_score"], group["min_rank"],
            _program_group_identity(group),
        ))
        representative_text = _majors_text(representative.get("majors_in_group"))
        representative_matches = _matched_tokens(representative_text, tokens)
        shown = [representative]
        extra_matches: list[str] = []
        for group in groups:
            if group is representative:
                continue
            matches = _matched_tokens(_majors_text(group.get("majors_in_group")), tokens)
            if matches:
                shown.append(group)
                extra_matches.extend(matches)
        matched = list(dict.fromkeys(representative_matches + extra_matches))
        intent = _is_intent(school_name, profile.target_schools)
        city = str(representative.get("city_location") or "")
        city_match = bool(city and city in profile.target_cities)
        delta = representative["min_rank"] - rank
        reasons: list[str] = []
        if intent:
            reasons.append("用户意向院校")
        if city_match:
            reasons.append("用户意向城市")
        if matched:
            reasons.append(f"专业倾向匹配：{'、'.join(matched)}")
        if not reasons:
            reasons.append(
                f"{representative.get('school_level') or '普通高校'}，位次差Δ{delta:+d}"
            )
        school_province = str(
            representative.get("school_province")
            or representative.get("province_location")
            or ""
        )
        province_match = is_in_province(school_province, target)
        item_status = _coverage_status({group["_status"] for group in shown})
        item_sources = tuple(sorted({
            source for group in shown for source in group["_source_ids"]
        }))
        major_groups = tuple(
            RecommendationMajorGroup(
                major_group_name=_program_group_name(group),
                major_group_code=str(group.get("major_group_code") or ""),
                min_score=group["min_score"],
                min_rank=group["min_rank"],
                majors=_majors_text(group.get("majors_in_group")),
            )
            for group in shown
        )
        item = RecommendationItem(
            school_name=school_name,
            school_level=str(representative.get("school_level") or ""),
            city=city,
            school_province=school_province,
            province_match=province_match,
            subject_match=True,
            min_score=representative["min_score"],
            min_rank=representative["min_rank"],
            delta=delta,
            related_majors=representative_text,
            remarks=str(representative.get("remarks") or ""),
            major_groups=major_groups,
            match_reason="；".join(reasons),
            recommend_level="★★★" if (intent or city_match or matched) else "★★",
            strategy=_tier(delta, policy.challenge_delta_lt, policy.stable_delta_le),
            data_year=representative["year"],
            source_ids=item_sources,
            evidence_status=item_status,
        )
        sort_key = (
            0 if intent else 1,
            0 if city_match else 1,
            LEVEL_ORDER.get(item.school_level, 9),
            0 if province_match else 1,
            item.min_rank,
            item.school_name,
        )
        sortable.append((sort_key, item))

    all_items = tuple(item for _key, item in sorted(sortable, key=lambda value: value[0]))
    capped: list[RecommendationItem] = []
    for tier in ("冲", "稳", "保"):
        tier_items = [item for item in all_items if item.strategy == tier]
        capped.extend(tier_items[:policy.tier_caps[tier]])
    items = tuple(capped)
    final_status = _coverage_status(statuses)
    if final_status is not EvidenceStatus.PARTIAL:
        items = tuple(
            item
            for item in items
            if item.evidence_status is not EvidenceStatus.PARTIAL
        )
    recommended_schools = {item.school_name for item in items}
    observations = tuple(
        item for item in observations if item.school_name not in recommended_schools
    )
    if verified_coverage is not None and verified_coverage[0] <= rank <= verified_coverage[1] and not items:
        empty_reason = (
            "unusable_evidence"
            if subject_rows and not usable
            else "no_match_within_verified_coverage"
        )
    if (
        observations
        and not items
        and empty_reason != "rank_outside_verified_coverage"
    ):
        empty_reason = "partial_observations_only"

    warnings = [
        warning
        for status in _ISSUE_PRECEDENCE
        if status in statuses
        if (warning := _warning_for_status(status)) is not None
    ]
    if len(input_years) == 1:
        warnings.append(f"仅覆盖 {input_years[0]}")
    if zero_score_excluded:
        warnings.append(f"0分占位已剔除：{zero_score_excluded} 行")
    if observations:
        warnings.append("部分覆盖院校仅作方向性观察，不进入精确冲稳保。")
    result = RecommendationResult(
        ordinary_batch_policy=policy,
        items=items,
        observations=observations,
        excluded_by_subject_count=excluded_by_subject,
        zero_score_excluded_count=zero_score_excluded,
        input_years=input_years,
        usable_years=usable_years,
        verified_rank_coverage=verified_coverage,
        coverage_status=final_status,
        empty_reason=empty_reason,
        warnings=tuple(dict.fromkeys(warnings)),
        rank_basis=profile.rank_basis,
        rank_bounds=(profile.optimistic_rank, profile.rank, profile.conservative_rank),
        rank_confidence=profile.rank_confidence,
        rank_source_ids=profile.rank_source_ids,
    )
    return result


def _scenario_item(
    group: list[dict[str, Any]],
    profile: RecommendationProfile,
    scenario: RankScenario,
) -> RecommendationItem | None:
    by_year: dict[int, dict[str, Any]] = {}
    for row in group:
        year = _strict_int(row.get("year"))
        min_rank = _strict_int(row.get("min_rank"))
        min_score = _strict_int(row.get("min_score"))
        status = _status(row.get("evidence_status"))
        coverage_status = _status(row.get("coverage_status"))
        coverage_min = _strict_int(row.get("coverage_min_rank"))
        coverage_max = _strict_int(row.get("coverage_max_rank"))
        sources = _source_ids(row)
        if (
            year is None
            or min_rank is None
            or min_rank < 1
            or min_score is None
            or min_score <= 0
            or status not in _ACCEPTED_EXACT_STATUSES
            or coverage_status not in _USABLE_COVERAGE_STATUSES
            or not sources
            or coverage_min is None
            or coverage_max is None
            or coverage_min > coverage_max
            or not coverage_min <= min_rank <= coverage_max
            or not coverage_min <= scenario.optimistic_rank
            or not scenario.conservative_rank <= coverage_max
        ):
            continue
        existing = by_year.get(year)
        if existing is not None and existing["min_rank"] != min_rank:
            return None
        snapshot = dict(row)
        snapshot["_status"] = _coverage_status({status, coverage_status})
        snapshot["_sources"] = sources
        by_year[year] = snapshot
    years = tuple(sorted(by_year, reverse=True)[:3])
    if not years:
        return None
    selected = tuple(by_year[year] for year in years)
    majority = math.ceil(2 * len(selected) / 3)
    bounds = (
        scenario.optimistic_rank,
        scenario.central_rank,
        scenario.conservative_rank,
    )
    counts = tuple(
        sum(1 for row in selected if rank <= row["min_rank"])
        for rank in bounds
    )
    if counts[2] >= majority:
        strategy = "保"
    elif counts[1] >= majority:
        strategy = "稳"
    elif counts[0] >= 1:
        strategy = "冲"
    else:
        strategy = "观察"
    representative = selected[0]
    school_name = str(representative.get("school_name") or "").strip()
    if not school_name:
        return None
    majors = _majors_text(representative.get("majors_in_group"))
    city = str(representative.get("city_location") or "")
    school_province = str(
        representative.get("school_province")
        or representative.get("province_location")
        or ""
    )
    statuses = {row["_status"] for row in selected}
    source_ids = tuple(
        sorted({source for row in selected for source in row["_sources"]})
    )
    major_group = RecommendationMajorGroup(
        major_group_name=_program_group_name(representative),
        major_group_code=str(representative.get("major_group_code") or ""),
        min_score=representative["min_score"],
        min_rank=representative["min_rank"],
        majors=majors,
    )
    reasons = [
        f"近{len(years)}年情景覆盖：乐观{counts[0]}、中性{counts[1]}、保守{counts[2]}"
    ]
    intent = _is_intent(school_name, profile.target_schools)
    city_match = bool(city and city in profile.target_cities)
    matched = _matched_tokens(majors, _major_tokens(profile.target_major_categories))
    if intent:
        reasons.append("用户意向院校")
    if city_match:
        reasons.append("用户意向城市")
    if matched:
        reasons.append(f"专业倾向匹配：{'、'.join(matched)}")

    scenario_fully_covered = all(
        row["coverage_min_rank"] <= scenario.optimistic_rank
        and scenario.conservative_rank <= row["coverage_max_rank"]
        for row in selected
    )
    scenario_confidence = (
        profile.rank_confidence
        if len(years) >= 2 and scenario_fully_covered
        else "low"
    )
    if not scenario_fully_covered:
        reasons.append("投档表验证范围未完整覆盖位次情景，结论按低置信度处理")
    plan_counts = tuple(
        _strict_int(row.get("plan_count")) for row in selected
    )
    known_plans = tuple(value for value in plan_counts if value is not None and value > 0)
    if len(known_plans) >= 2:
        latest_plan = _strict_int(representative.get("plan_count"))
        previous_plans = tuple(
            _strict_int(row.get("plan_count"))
            for row in selected[1:]
            if _strict_int(row.get("plan_count")) is not None
        )
        if (
            latest_plan is not None
            and latest_plan > 0
            and previous_plans
            and latest_plan * 5 < max(previous_plans) * 4
        ):
            scenario_confidence = "low"
            reasons.append("招生计划明显缩减")
    return RecommendationItem(
        school_name=school_name,
        school_level=str(representative.get("school_level") or ""),
        city=city,
        school_province=school_province,
        province_match=is_in_province(school_province, profile.target_province),
        subject_match=True,
        min_score=representative["min_score"],
        min_rank=representative["min_rank"],
        delta=representative["min_rank"] - profile.rank,
        related_majors=majors,
        remarks=str(representative.get("remarks") or ""),
        major_groups=(major_group,),
        match_reason="；".join(reasons),
        recommend_level=(
            "★★★" if len(years) >= 2 and (intent or city_match or matched) else "★★"
        ),
        strategy=strategy,
        data_year=max(years),
        source_ids=source_ids,
        evidence_status=_coverage_status(statuses),
        supporting_years=tuple(sorted(years)),
        required_year_majority=majority,
        scenario_reach_counts=counts,
        scenario_confidence=scenario_confidence,
    )


def _recommend_scenarios(
    rows: Sequence[Mapping[str, Any]],
    profile: RecommendationProfile,
    policy: OrdinaryBatchPolicy,
    scenario: RankScenario,
) -> RecommendationResult:
    if scenario.status not in {EvidenceStatus.OFFICIAL, EvidenceStatus.INFERRED}:
        raise SchoolRecommendError("REC_001", "位次情景缺少可计算边界")
    expected_basis = scenario.status.value
    if (
        profile.rank_basis != expected_basis
        or profile.rank != scenario.central_rank
        or profile.optimistic_rank != scenario.optimistic_rank
        or profile.conservative_rank != scenario.conservative_rank
        or profile.rank_confidence != scenario.confidence
        or tuple(profile.rank_source_ids) != tuple(scenario.source_ids)
    ):
        raise SchoolRecommendError("REC_001", "推荐画像与位次情景不一致")
    target = _canonical_province(profile.target_province)
    if target is None:
        raise SchoolRecommendError("REC_002", "目标省份无效")
    selected_subjects = frozenset(profile.secondary_subjects)
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    input_years: set[int] = set()
    excluded = 0
    for original in rows:
        if not isinstance(original, Mapping):
            continue
        row = dict(original)
        if not is_in_province(row.get("province"), target):
            continue
        if profile.subject_group and row.get("subject_group") != profile.subject_group:
            continue
        year = _strict_int(row.get("year"))
        if year is not None:
            input_years.add(year)
        if not _subject_match(row, selected_subjects):
            excluded += 1
            continue
        key = (
            str(row.get("school_code") or row.get("school_name") or ""),
            _program_group_identity(row),
            str(row.get("remarks") or ""),
        )
        groups.setdefault(key, []).append(row)
    subject_rows = tuple(row for group in groups.values() for row in group)
    observations = _partial_school_observations(subject_rows)
    items = tuple(
        item
        for key in sorted(groups)
        if (item := _scenario_item(groups[key], profile, scenario)) is not None
    )
    search_min = max(1, profile.rank + policy.search_delta_min)
    search_max = profile.rank + policy.search_delta_max
    items = tuple(
        item for item in items if search_min <= item.min_rank <= search_max
    )
    strategy_order = {"冲": 0, "稳": 1, "保": 2, "观察": 3}

    def preference_key(item: RecommendationItem) -> tuple[Any, ...]:
        intent = _is_intent(item.school_name, profile.target_schools)
        city_match = bool(item.city and item.city in profile.target_cities)
        major_match = bool(
            _matched_tokens(
                item.related_majors,
                _major_tokens(profile.target_major_categories),
            )
        )
        return (
            strategy_order[item.strategy],
            0 if intent else 1,
            0 if city_match else 1,
            0 if major_match else 1,
            LEVEL_ORDER.get(item.school_level, 9),
            item.school_name,
        )

    ordered = tuple(
        sorted(items, key=preference_key)
    )
    capped: list[RecommendationItem] = []
    for strategy in ("冲", "稳", "保"):
        matches = [item for item in ordered if item.strategy == strategy]
        capped.extend(matches[: policy.tier_caps[strategy]])
    capped.extend(item for item in ordered if item.strategy == "观察")
    recommended_schools = {item.school_name for item in capped}
    observations = tuple(
        item for item in observations if item.school_name not in recommended_schools
    )
    warnings: list[str] = []
    if any(len(item.supporting_years) == 1 for item in capped):
        one_years = sorted(
            {item.supporting_years[0] for item in capped if len(item.supporting_years) == 1}
        )
        warnings.extend(f"仅覆盖 {year}" for year in one_years)
    selected_coverage_rows: list[dict[str, Any]] = []
    if capped:
        selected_keys = {
            (
                item.school_name,
                group.major_group_code or group.major_group_name,
                year,
            )
            for item in capped
            for group in item.major_groups
            for year in item.supporting_years
        }
        selected_coverage_rows = [
            row
            for row in subject_rows
            if (
                str(row.get("school_name") or ""),
                _program_group_identity(row),
                _strict_int(row.get("year")),
            )
            in selected_keys
        ]
    verified_coverage, coverage_conflict = _verified_coverage_for_rows(
        selected_coverage_rows if capped else subject_rows
    )
    statuses = {item.evidence_status for item in capped}
    if observations:
        statuses.add(EvidenceStatus.PARTIAL)
    if coverage_conflict:
        statuses.add(EvidenceStatus.CONFLICT)
    elif verified_coverage is None:
        statuses.add(EvidenceStatus.MISSING)
    for status in _ISSUE_PRECEDENCE:
        if status in statuses:
            warning = _warning_for_status(status)
            if warning is not None:
                warnings.append(warning)
    if observations:
        warnings.append("部分覆盖院校仅作方向性观察，不进入精确冲稳保。")
    return RecommendationResult(
        ordinary_batch_policy=policy,
        items=tuple(capped),
        observations=observations,
        excluded_by_subject_count=excluded,
        zero_score_excluded_count=0,
        input_years=tuple(sorted(input_years)),
        usable_years=tuple(sorted({year for item in capped for year in item.supporting_years})),
        verified_rank_coverage=verified_coverage,
        coverage_status=_coverage_status(statuses),
        empty_reason=(
            None
            if capped
            else "rank_outside_verified_coverage"
            if (
                observations
                and verified_coverage is not None
                and not (
                    verified_coverage[0] <= scenario.optimistic_rank
                    and scenario.conservative_rank <= verified_coverage[1]
                )
            )
            else "partial_observations_only"
            if observations
            else "no_match_within_rank_scenarios"
        ),
        warnings=tuple(warnings),
        rank_basis=expected_basis,
        rank_bounds=(
            scenario.optimistic_rank,
            scenario.central_rank,
            scenario.conservative_rank,
        ),
        rank_confidence=scenario.confidence,
        rank_source_ids=scenario.source_ids,
    )


def recommend_schools(
    rows: Sequence[Mapping[str, Any]],
    profile: RecommendationProfile | Mapping[str, Any],
    policy: OrdinaryBatchPolicy,
    *,
    rank_scenario: RankScenario | None = None,
) -> RecommendationResult:
    """Return recommendations using one explicit authenticated province policy."""

    if not isinstance(policy, OrdinaryBatchPolicy):
        raise SchoolRecommendError("REC_003", "普通批策略缺失或无效")
    policy_snapshot = OrdinaryBatchPolicy(**policy.to_dict())
    profile_snapshot = _profile(profile)
    if rank_scenario is not None:
        if not isinstance(rank_scenario, RankScenario):
            raise TypeError("rank_scenario must be a RankScenario")
        return _recommend_scenarios(
            rows, profile_snapshot, policy_snapshot, rank_scenario
        )
    return _recommend_core(rows, profile_snapshot, policy_snapshot)


def _same_region(value: object, expected: str) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    return value.strip() == expected or is_in_province(value, expected)


def _school_reason(
    profile: PlanningProfile,
    code: str,
    explanation: str,
    source_ids: tuple[str, ...] = (),
    *,
    input_fields: tuple[str, ...],
    evidence_status: EvidenceStatus | None = None,
) -> DecisionReason:
    return DecisionReason.create(
        profile,
        code=code,
        explanation=explanation,
        input_fields=input_fields,
        source_ids=source_ids,
        evidence_status=evidence_status,
    )


def _school_subject_input_fields(
    rows: Sequence[Mapping[str, Any]], *, include_subject_group: bool
) -> tuple[str, ...]:
    fields: list[str] = []
    if include_subject_group and any(row.get("subject_group") for row in rows):
        fields.append("subject_group")
    profile_relevant_secondary = any(
        (
            row.get("secondary_subject_rule") in {"any", "all"}
            and bool(parse_secondary_subjects(row.get("required_secondary_subjects")))
        )
        or bool(
            _subject_required(str(row.get("remarks") or row.get("remark") or ""))
        )
        for row in rows
    )
    if profile_relevant_secondary:
        fields.append("secondary_subjects")
    return tuple(fields)


def _province_policy_reason(
    profile: PlanningProfile, rows: Sequence[Mapping[str, Any]]
) -> DecisionReason:
    sources = _fit_source_ids(rows, "province_policy")
    status = _fit_evidence_status(rows, "province_policy")
    modes = {
        str(row.get("province_policy_exam_mode")).strip()
        for row in rows
        if isinstance(row.get("province_policy_exam_mode"), str)
        and str(row.get("province_policy_exam_mode")).strip()
    }
    if _usable_fit_dimension(rows, "province_policy") and modes == {
        profile.subject_mode
    }:
        return _school_reason(
            profile,
            "SCHOOL_PROVINCE_POLICY_MATCH",
            "认证省级招考政策与已确认高考模式及选科上下文一致",
            sources,
            input_fields=("province", "subject_mode", "subject_group"),
            evidence_status=status,
        )
    if _usable_fit_dimension(rows, "province_policy") and modes:
        return _school_reason(
            profile,
            "SCHOOL_PROVINCE_POLICY_MISMATCH",
            "认证省级招考政策与已确认高考模式不一致，学校判断需复核",
            sources,
            input_fields=("province", "subject_mode", "subject_group"),
            evidence_status=status,
        )
    return _school_reason(
        profile,
        "SCHOOL_PROVINCE_POLICY_UNVERIFIED",
        (
            "省级招考政策证据存在冲突，学校判断需复核"
            if status is EvidenceStatus.CONFLICT
            else "未取得可回放的省级招考政策证据，学校判断按未核验标注"
        ),
        sources,
        input_fields=(),
        evidence_status=status,
    )


def _decision_reason_order(reason: DecisionReason) -> tuple[int, str]:
    dimensions = {
        name: index
        for index, name in enumerate(DecisionPolicySnapshot.load_default().pathway_reason_order)
    }
    return dimensions[reason.dimension], reason.code


def _scenario_items_without_delta_policy(
    rows: Sequence[Mapping[str, Any]],
    profile: RecommendationProfile,
    scenario: RankScenario,
) -> tuple[
    tuple[RecommendationItem, ...],
    tuple[SchoolObservation, ...],
    tuple[str, ...],
]:
    """Classify only by authenticated scenario reach; apply no rank deltas."""

    if scenario.status not in {EvidenceStatus.OFFICIAL, EvidenceStatus.INFERRED}:
        raise SchoolRecommendError("REC_001", "位次情景缺少可计算边界")
    if (
        profile.rank_basis != scenario.status.value
        or profile.rank != scenario.central_rank
        or profile.optimistic_rank != scenario.optimistic_rank
        or profile.conservative_rank != scenario.conservative_rank
        or profile.rank_confidence != scenario.confidence
        or tuple(profile.rank_source_ids) != tuple(scenario.source_ids)
    ):
        raise SchoolRecommendError("REC_001", "推荐画像与位次情景不一致")
    target = _canonical_province(profile.target_province)
    if target is None:
        raise SchoolRecommendError("REC_002", "目标省份无效")
    selected_subjects = frozenset(profile.secondary_subjects)
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    for original in rows:
        if not isinstance(original, Mapping):
            continue
        row = dict(original)
        if not is_in_province(row.get("province"), target):
            continue
        if profile.subject_group and row.get("subject_group") != profile.subject_group:
            continue
        if not _subject_match(row, selected_subjects):
            continue
        key = (
            str(row.get("school_code") or row.get("school_name") or ""),
            _program_group_identity(row),
            str(row.get("remarks") or ""),
        )
        groups.setdefault(key, []).append(row)
    items = tuple(
        item
        for key in sorted(groups)
        if (item := _scenario_item(groups[key], profile, scenario)) is not None
    )
    warnings = [
        "普通批位次差策略不可用；院校分档仅按认证位次情景与实际投档区间判定。"
    ]
    observations = _partial_school_observations(
        tuple(row for group in groups.values() for row in group)
    )
    recommended_schools = {item.school_name for item in items}
    observations = tuple(
        item for item in observations if item.school_name not in recommended_schools
    )
    for year in sorted(
        {item.supporting_years[0] for item in items if len(item.supporting_years) == 1}
    ):
        warnings.append(f"仅覆盖 {year}")
    if observations:
        warnings.append("部分覆盖院校仅作方向性观察，不进入精确冲稳保。")
    return items, observations, tuple(warnings)


def personalize_school_recommendations(
    rows: Sequence[Mapping[str, Any]],
    profile: PlanningProfile,
    policy: OrdinaryBatchPolicy | None = None,
    *,
    rank_scenario: RankScenario,
    decision_policy: DecisionPolicySnapshot | None = None,
    subject_selection_key: str | None = None,
) -> SchoolDecisionResult:
    """Apply full-profile school constraints around the compatible result seam."""

    if not isinstance(profile, PlanningProfile):
        raise TypeError("profile must be a PlanningProfile")
    if not isinstance(rank_scenario, RankScenario):
        raise TypeError("rank_scenario must be a RankScenario")
    if rank_scenario.status not in {EvidenceStatus.OFFICIAL, EvidenceStatus.INFERRED}:
        raise SchoolRecommendError("REC_001", "位次情景缺少可计算边界")
    reviewed = decision_policy or DecisionPolicySnapshot.load_default()
    if type(reviewed) is not DecisionPolicySnapshot:
        raise TypeError("decision_policy must be a strict DecisionPolicySnapshot")
    if policy is not None and not isinstance(policy, OrdinaryBatchPolicy):
        raise SchoolRecommendError("REC_003", "普通批策略缺失或无效")

    row_snapshots = tuple(dict(item) for item in rows if isinstance(item, Mapping))
    by_school: dict[str, list[dict[str, Any]]] = {}
    for row in row_snapshots:
        school_name = str(row.get("school_name") or "").strip()
        if school_name:
            by_school.setdefault(school_name, []).append(row)

    excluded: dict[str, tuple[DecisionReason, ...]] = {}
    eligible_rows: list[dict[str, Any]] = []
    selected_subjects = frozenset(profile.secondary_subjects)
    if profile.subject_mode == "3+3":
        # The first serialized subject has no special status in 3+3.
        selected_subjects |= {profile.subject_group}
    allowed_institution_types = set(profile.constraints.institution_types)
    for school_name in sorted(by_school):
        school_rows = by_school[school_name]
        sources = tuple(sorted({
            source for row in school_rows for source in _source_ids(row)
        }))
        fit_sources = _fit_source_ids(school_rows)
        enrollment_sources = _fit_source_ids(school_rows, "enrollment_plan")
        charter_sources = _fit_source_ids(school_rows, "admission_charter")
        tuition_sources = _fit_source_ids(school_rows, "tuition_fee")
        subject_sources = _fit_source_ids(school_rows, "subject_requirement")
        enrollment_status = _fit_evidence_status(school_rows, "enrollment_plan")
        charter_status = _fit_evidence_status(school_rows, "admission_charter")
        tuition_status = _fit_evidence_status(school_rows, "tuition_fee")
        subject_status = _fit_evidence_status(school_rows, "subject_requirement")
        enrollment_usable = _usable_fit_dimension(school_rows, "enrollment_plan")
        charter_usable = _usable_fit_dimension(school_rows, "admission_charter")
        tuition_usable = _usable_fit_dimension(school_rows, "tuition_fee")
        subject_usable = _usable_fit_dimension(school_rows, "subject_requirement")
        school_regions = tuple(
            str(value).strip()
            for row in school_rows
            for value in (row.get("city_location"), row.get("school_province"))
            if isinstance(value, str) and value.strip()
        ) if enrollment_usable else ()
        if any(
            _same_region(region, excluded_region)
            for region in school_regions
            for excluded_region in profile.constraints.excluded_regions
        ):
            excluded[school_name] = (
                _school_reason(
                    profile,
                    "SCHOOL_EXCLUDED_REGION",
                    "院校所在地命中已确认排除地区",
                    enrollment_sources,
                    input_fields=("constraints.excluded_regions",),
                    evidence_status=enrollment_status,
                ),
                _province_policy_reason(profile, school_rows),
            )
            continue

        known_types = {
            str(row.get("institution_type")).strip()
            for row in school_rows
            if isinstance(row.get("institution_type"), str)
            and str(row.get("institution_type")).strip()
        } if enrollment_usable else set()
        if (
            allowed_institution_types
            and known_types
            and not known_types & allowed_institution_types
        ):
            excluded[school_name] = (
                _school_reason(
                    profile,
                    "SCHOOL_INSTITUTION_TYPE_BLOCKED",
                    "认证院校类型不在已接受类型中",
                    enrollment_sources,
                    input_fields=("constraints.institution_types",),
                    evidence_status=enrollment_status,
                ),
                _province_policy_reason(profile, school_rows),
            )
            continue

        subject_rows = (
            [row for row in school_rows if _subject_match(row, selected_subjects)]
            if subject_usable
            else list(school_rows)
        )
        if not subject_rows:
            excluded[school_name] = (
                _school_reason(
                    profile,
                    "SCHOOL_SUBJECT_MISMATCH",
                    "认证选科要求与已确认选科不相符",
                    subject_sources,
                    input_fields=_school_subject_input_fields(
                        school_rows, include_subject_group=profile.subject_mode == "3+3"
                    ),
                    evidence_status=subject_status,
                ),
                _province_policy_reason(profile, school_rows),
            )
            continue

        if (
            profile.constraints.adjustment_preference == "reject"
            and charter_usable
        ):
            subject_rows = [
                row for row in subject_rows
                if row.get("charter_adjustment_required") is not True
            ]
            if not subject_rows:
                excluded[school_name] = (
                    _school_reason(
                        profile,
                        "SCHOOL_ADJUSTMENT_BLOCKED",
                        "认证专业组选项要求接受调剂但画像明确拒绝",
                        charter_sources,
                        input_fields=("constraints.adjustment_preference",),
                        evidence_status=charter_status,
                    ),
                    _province_policy_reason(profile, school_rows),
                )
                continue

        if (
            profile.constraints.budget_level != "unknown"
            and tuition_usable
        ):
            budget = profile.constraints.budget_level
            compatible_rows = []
            for row in subject_rows:
                raw_affordability = row.get("tuition_affordable_for")
                known_affordability = (
                    tuple(raw_affordability)
                    if isinstance(raw_affordability, (tuple, list, set, frozenset))
                    else ()
                )
                if not known_affordability or budget in known_affordability:
                    compatible_rows.append(row)
            if not compatible_rows:
                excluded[school_name] = (
                    _school_reason(
                        profile,
                        "SCHOOL_AFFORDABILITY_BLOCKED",
                        "认证费用适配范围不覆盖已确认预算档位",
                        tuition_sources,
                        input_fields=("constraints.budget_level",),
                        evidence_status=tuition_status,
                    ),
                    _province_policy_reason(profile, school_rows),
                )
                continue
            subject_rows = compatible_rows
        eligible_rows.extend(subject_rows)

    central_rank = rank_scenario.central_rank
    assert central_rank is not None
    recommendation_profile = RecommendationProfile(
        rank=central_rank,
        target_province=profile.province,
        subject_group=subject_selection_key or profile.subject_group,
        secondary_subjects=selected_subjects,
        target_major_categories=profile.target_majors,
        target_cities=profile.target_regions,
        target_schools=profile.target_schools,
        rank_basis=rank_scenario.status.value,
        optimistic_rank=rank_scenario.optimistic_rank,
        conservative_rank=rank_scenario.conservative_rank,
        rank_confidence=rank_scenario.confidence,
        rank_source_ids=rank_scenario.source_ids,
    )
    effective_caps = risk_tier_caps(reviewed, profile.constraints.risk_preference)
    if policy is None:
        base_items, base_observations, decision_warnings = _scenario_items_without_delta_policy(
            eligible_rows,
            recommendation_profile,
            rank_scenario,
        )
        base = None
    else:
        analysis_policy = OrdinaryBatchPolicy(
            schema_version=policy.schema_version,
            policy_id=policy.policy_id,
            basis_id=policy.basis_id,
            search_delta_min=policy.search_delta_min,
            search_delta_max=policy.search_delta_max,
            challenge_delta_lt=policy.challenge_delta_lt,
            stable_delta_le=policy.stable_delta_le,
            tier_caps={tier: max(len(by_school), cap) for tier, cap in effective_caps.items()},
        )
        base = recommend_schools(
            eligible_rows,
            recommendation_profile,
            analysis_policy,
            rank_scenario=rank_scenario,
        )
        base_items = base.items
        base_observations = base.observations
        decision_warnings = base.warnings

    fit_warnings: list[str] = []
    family_labels = {
        "province_policy": "省级招考政策",
        "enrollment_plan": "招生计划/院校属性",
        "admission_charter": "招生章程/录取与调剂规则",
        "tuition_fee": "学费/必要费用",
        "subject_requirement": "专业组选科要求",
    }
    for kind, label in family_labels.items():
        status = _fit_evidence_status(row_snapshots, kind)
        if status is EvidenceStatus.CONFLICT:
            fit_warnings.append(f"{label}证据冲突；相关维度不作确定匹配。")
        elif status is EvidenceStatus.MISSING:
            fit_warnings.append(f"{label}缺少可回放 receipt；相关维度按未核验展示。")
        current_status_field = {
            "province_policy": "school_fit_province_policy_current_status",
            "enrollment_plan": "school_fit_enrollment_current_status",
            "admission_charter": "school_fit_charter_current_status",
            "tuition_fee": "school_fit_tuition_current_status",
            "subject_requirement": "school_fit_subject_current_status",
        }[kind]
        unresolved_current = {
            item
            for row in row_snapshots
            if (item := _status(row.get(current_status_field))) is not None
        }
        if unresolved_current:
            fit_warnings.append(
                f"{label}当年证据状态为"
                f"{'/'.join(sorted(item.value for item in unresolved_current))}；"
                "当前使用的是更早年度参考，必须复核当年更新。"
            )
    charter_unverified_fields = {
        field
        for row in row_snapshots
        for field in (
            row.get("charter_unverified_fields")
            if isinstance(row.get("charter_unverified_fields"), (tuple, list))
            else ()
        )
        if isinstance(field, str)
    }
    if charter_unverified_fields:
        fit_warnings.append(
            "招生章程未披露的语种、单科、体检或特殊条件须列入逐校人工核对清单；"
            "不得解释为“无限制”。"
        )
    elif _usable_fit_dimension(row_snapshots, "admission_charter"):
        fit_warnings.append(
            "招生章程的体检、语种、单科和特殊条件已取得来源，仍须结合学生画像逐校人工核对。"
        )
    province_modes = {
        str(row.get("province_policy_exam_mode")).strip()
        for row in row_snapshots
        if isinstance(row.get("province_policy_exam_mode"), str)
        and str(row.get("province_policy_exam_mode")).strip()
    }
    if province_modes and province_modes != {profile.subject_mode}:
        fit_warnings.append(
            "省级招考政策中的高考模式与学生画像不一致；普通批学校判断需复核。"
        )
    decision_warnings = tuple(
        dict.fromkeys((*decision_warnings, *fit_warnings))
    )

    strategy_order = {"冲": 0, "稳": 1, "保": 2, "观察": 3}

    def item_flags(item: RecommendationItem) -> tuple[bool, bool, bool, bool]:
        rows_for_item = item_rows(item)
        enrollment_usable = _usable_fit_dimension(
            rows_for_item, "enrollment_plan"
        )
        school_match = _is_intent(item.school_name, profile.target_schools)
        major_match = enrollment_usable and bool(
            _matched_tokens(item.related_majors, _major_tokens(profile.target_majors))
        )
        target_region_match = enrollment_usable and any(
            _same_region(region, target)
            for region in (item.city, item.school_province)
            for target in profile.target_regions
        )
        local_match = enrollment_usable and bool(profile.city) and any(
            _same_region(region, profile.city)
            for region in (item.city, item.school_province)
        )
        return school_match, major_match, target_region_match, local_match

    def item_rows(item: RecommendationItem) -> tuple[dict[str, Any], ...]:
        codes = {
            group.major_group_code for group in item.major_groups
            if group.major_group_code
        }
        names = {
            group.major_group_name for group in item.major_groups
            if group.major_group_name
        }
        matched = tuple(
            row for row in by_school[item.school_name]
            if (
                (codes and str(row.get("major_group_code") or "") in codes)
                or (not codes and names and _program_group_name(row) in names)
            )
        )
        return matched or tuple(by_school[item.school_name])

    def adjustment_key(item: RecommendationItem) -> int:
        preference = profile.constraints.adjustment_preference
        if preference == "unknown":
            return 0
        rows_for_item = item_rows(item)
        if not _usable_fit_dimension(rows_for_item, "admission_charter"):
            return 2
        values = {
            row.get("charter_adjustment_required")
            for row in rows_for_item
            if isinstance(row.get("charter_adjustment_required"), bool)
        }
        if preference == "accept":
            return 0 if True in values else 1 if False in values else 2
        if preference == "reject":
            return 0 if False in values else 1
        return 0 if values else 1

    def preference_key(item: RecommendationItem) -> tuple[Any, ...]:
        school_match, major_match, region_match, local_match = item_flags(item)
        if profile.priorities.school_vs_major == "school_first":
            fit_key = (0 if school_match else 1, 0 if major_match else 1)
        elif profile.priorities.school_vs_major == "major_first":
            fit_key = (0 if major_match else 1, 0 if school_match else 1)
        else:
            fit_key = (
                0
                if major_match and school_match
                else 1
                if major_match
                else 2
                if school_match
                else 3,
                0,
            )
        return (
            strategy_order[item.strategy],
            *fit_key,
            0 if region_match else 1,
            0 if local_match else 1,
            adjustment_key(item),
            {
                EvidenceStatus.OFFICIAL: 0,
                EvidenceStatus.CORROBORATED: 1,
                EvidenceStatus.REFERENCE: 2,
            }.get(item.evidence_status, 3),
            LEVEL_ORDER.get(item.school_level, 9),
            item.school_name,
            tuple(
                (group.major_group_code, group.major_group_name)
                for group in item.major_groups
            ),
            tuple(item.source_ids),
        )

    ordered_candidates: list[RecommendationItem] = []
    seen_schools: set[str] = set()
    for item in sorted(base_items, key=preference_key):
        if item.school_name not in seen_schools:
            ordered_candidates.append(item)
            seen_schools.add(item.school_name)

    included: list[RecommendationItem] = []
    cap_excluded: set[str] = set()
    for strategy in ("冲", "稳", "保"):
        candidates = [item for item in ordered_candidates if item.strategy == strategy]
        included.extend(candidates[: effective_caps[strategy]])
        cap_excluded.update(item.school_name for item in candidates[effective_caps[strategy] :])
    included.extend(item for item in ordered_candidates if item.strategy == "观察")

    included_decisions: list[SchoolDecision] = []
    decorated_items: list[RecommendationItem] = []
    evidence_codes = {
        EvidenceStatus.OFFICIAL: "SCHOOL_EVIDENCE_OFFICIAL",
        EvidenceStatus.CORROBORATED: "SCHOOL_EVIDENCE_CORROBORATED",
        EvidenceStatus.REFERENCE: "SCHOOL_EVIDENCE_REFERENCE",
        EvidenceStatus.PARTIAL: "SCHOOL_EVIDENCE_PARTIAL",
    }
    rank_codes = {
        "冲": "SCHOOL_RANK_CHALLENGE",
        "稳": "SCHOOL_RANK_STABLE",
        "保": "SCHOOL_RANK_SAFE",
        "观察": "SCHOOL_RANK_OBSERVE",
    }
    for order, item in enumerate(included, start=1):
        source_ids = tuple(item.source_ids)
        school_rows = item_rows(item)
        fit_sources = _fit_source_ids(school_rows)
        enrollment_sources = _fit_source_ids(school_rows, "enrollment_plan")
        charter_sources = _fit_source_ids(school_rows, "admission_charter")
        tuition_sources = _fit_source_ids(school_rows, "tuition_fee")
        subject_sources = _fit_source_ids(school_rows, "subject_requirement")
        province_sources = _fit_source_ids(school_rows, "province_policy")
        enrollment_status = _fit_evidence_status(school_rows, "enrollment_plan")
        charter_status = _fit_evidence_status(school_rows, "admission_charter")
        tuition_status = _fit_evidence_status(school_rows, "tuition_fee")
        subject_status = _fit_evidence_status(school_rows, "subject_requirement")
        province_status = _fit_evidence_status(school_rows, "province_policy")
        enrollment_usable = _usable_fit_dimension(school_rows, "enrollment_plan")
        charter_usable = _usable_fit_dimension(school_rows, "admission_charter")
        tuition_usable = _usable_fit_dimension(school_rows, "tuition_fee")
        subject_usable = _usable_fit_dimension(school_rows, "subject_requirement")
        subject_metadata_known = subject_usable and any(
            (
                row.get("secondary_subject_rule") in {"any", "all"}
                and "required_secondary_subjects" in row
            )
            or _subject_required(str(row.get("remarks") or row.get("remark") or ""))
            is not None
            for row in school_rows
        )
        subject_code = (
            "SCHOOL_SUBJECT_MATCH"
            if subject_metadata_known
            else "SCHOOL_SUBJECT_UNVERIFIED"
        )
        reasons: list[DecisionReason] = [
            _school_reason(
                profile,
                rank_codes[item.strategy],
                f"认证位次区间将该院校归入{item.strategy}档",
                tuple(sorted(set(source_ids) | set(rank_scenario.source_ids))),
                input_fields=("province",),
                evidence_status=item.evidence_status,
            ),
            _school_reason(
                profile,
                subject_code,
                (
                    "认证专业组选科要求与已确认选科相符"
                    if subject_metadata_known
                    else "当前认证投档行未包含可判定的再选科目要求，需逐校复核"
                ),
                subject_sources,
                input_fields=_school_subject_input_fields(
                    school_rows, include_subject_group=True
                ),
                evidence_status=subject_status,
            ),
            _province_policy_reason(profile, school_rows),
        ]
        school_match, major_match, region_match, local_match = item_flags(item)
        for matched, code, explanation, input_fields in (
            (
                school_match,
                (
                    "SCHOOL_TARGET_SCHOOL_COMMITTED"
                    if profile.target_school_reasons
                    else "SCHOOL_TARGET_SCHOOL_MATCH"
                ),
                (
                    "院校命中已确认目标院校，且画像记录了目标承诺理由"
                    if profile.target_school_reasons
                    else "院校命中已确认目标院校"
                ),
                (
                    "priorities.target_schools",
                    "target_school_reasons",
                ),
            ),
            (
                major_match,
                (
                    "SCHOOL_TARGET_MAJOR_COMMITTED"
                    if profile.target_major_reasons
                    else "SCHOOL_TARGET_MAJOR_MATCH"
                ),
                (
                    "认证招生专业命中已确认目标专业，且画像记录了目标承诺理由"
                    if profile.target_major_reasons
                    else "认证招生专业命中已确认目标专业"
                ),
                (
                    "priorities.target_majors",
                    "target_major_reasons",
                ),
            ),
            (
                region_match,
                "SCHOOL_TARGET_REGION_MATCH",
                "院校所在地命中已确认目标地区",
                ("priorities.target_regions",),
            ),
            (
                local_match,
                "SCHOOL_LOCAL_CITY_MATCH",
                "院校所在地命中当前城市偏好",
                ("city",),
            ),
        ):
            if matched:
                reason_sources = source_ids
                reason_status = item.evidence_status
                if code.startswith("SCHOOL_TARGET_MAJOR"):
                    reason_sources = enrollment_sources
                    reason_status = enrollment_status
                elif code in {"SCHOOL_TARGET_REGION_MATCH", "SCHOOL_LOCAL_CITY_MATCH"}:
                    reason_sources = enrollment_sources
                    reason_status = enrollment_status
                reasons.append(
                    _school_reason(
                        profile,
                        code,
                        explanation,
                        reason_sources,
                        input_fields=input_fields,
                        evidence_status=reason_status,
                    )
                )
        known_majors = enrollment_usable and any(
            bool(_majors_text(row.get("majors_in_group"))) for row in school_rows
        )
        if profile.target_majors and not known_majors:
            reasons.append(
                _school_reason(
                    profile,
                    "SCHOOL_TARGET_MAJOR_UNVERIFIED",
                    "当前认证投档行未包含可判定的招生专业，需逐校复核",
                    enrollment_sources,
                    input_fields=(
                        "priorities.target_majors",
                        "target_major_reasons",
                    ),
                    evidence_status=enrollment_status,
                )
            )
        known_regions = {
            str(value).strip()
            for row in school_rows
            for value in (row.get("city_location"), row.get("school_province"))
            if isinstance(value, str) and value.strip()
        } if enrollment_usable else set()
        if (
            profile.target_regions or profile.constraints.excluded_regions or profile.city
        ) and not known_regions:
            region_fields = ["city"]
            if profile.target_regions:
                region_fields.append("priorities.target_regions")
            if profile.constraints.excluded_regions:
                region_fields.append("constraints.excluded_regions")
            reasons.append(
                _school_reason(
                    profile,
                    "SCHOOL_REGION_UNVERIFIED",
                    "当前认证投档行未包含可判定的院校所在地，需逐校复核",
                    enrollment_sources,
                    input_fields=tuple(region_fields),
                    evidence_status=enrollment_status,
                )
            )
        known_types = {
            str(row.get("institution_type")).strip()
            for row in school_rows
            if isinstance(row.get("institution_type"), str)
            and str(row.get("institution_type")).strip()
        } if enrollment_usable else set()
        if profile.constraints.institution_types:
            reasons.append(
                _school_reason(
                    profile,
                    (
                        "SCHOOL_INSTITUTION_TYPE_MATCH"
                        if known_types
                        else "SCHOOL_INSTITUTION_TYPE_UNVERIFIED"
                    ),
                    (
                        "认证院校类型在已接受类型中"
                        if known_types
                        else "当前认证投档行未包含院校类型，需逐校复核"
                    ),
                    enrollment_sources,
                    input_fields=("constraints.institution_types",),
                    evidence_status=enrollment_status,
                )
            )
        affordable_for = {
            budget
            for row in school_rows
            for budget in (
                row.get("tuition_affordable_for")
                if isinstance(row.get("tuition_affordable_for"), (tuple, list, set, frozenset))
                else ()
            )
            if isinstance(budget, str)
        } if tuition_usable else set()
        if profile.constraints.budget_level != "unknown":
            reasons.append(
                _school_reason(
                    profile,
                    (
                        "SCHOOL_AFFORDABILITY_MATCH"
                        if profile.constraints.budget_level in affordable_for
                        else "SCHOOL_AFFORDABILITY_UNVERIFIED"
                    ),
                    (
                        "认证费用适配范围覆盖已确认预算档位"
                        if profile.constraints.budget_level in affordable_for
                        else "当前认证投档行未提供可判定费用，需逐校复核"
                    ),
                    tuition_sources,
                    input_fields=("constraints.budget_level",),
                    evidence_status=tuition_status,
                )
            )
        adjustment_values = {
            row.get("charter_adjustment_required")
            for row in school_rows
            if isinstance(row.get("charter_adjustment_required"), bool)
        } if charter_usable else set()
        if profile.constraints.adjustment_preference != "unknown":
            reasons.append(
                _school_reason(
                    profile,
                    (
                        "SCHOOL_ADJUSTMENT_MATCH"
                        if adjustment_values
                        else "SCHOOL_ADJUSTMENT_UNVERIFIED"
                    ),
                    (
                        "认证专业组调剂信息与已确认偏好可继续比较"
                        if adjustment_values
                        else "当前认证投档行未提供调剂要求，需逐校复核"
                    ),
                    charter_sources,
                    input_fields=("constraints.adjustment_preference",),
                    evidence_status=charter_status,
                )
            )
        charter_health_known = charter_usable and any(
            isinstance(row.get("charter_health_restrictions"), str)
            and bool(str(row.get("charter_health_restrictions")).strip())
            for row in school_rows
        )
        if profile.constraints.health_constraints:
            health_status = (
                charter_status
                if charter_health_known
                else charter_status
                if charter_status in {
                    EvidenceStatus.CONFLICT,
                    EvidenceStatus.PARTIAL,
                    EvidenceStatus.MASKED,
                }
                else EvidenceStatus.MISSING
            )
            reasons.append(
                _school_reason(
                    profile,
                    (
                        "SCHOOL_CHARTER_HEALTH_REVIEW_REQUIRED"
                        if charter_health_known
                        else "SCHOOL_CHARTER_HEALTH_UNVERIFIED"
                    ),
                    (
                        "招生章程体检条件已有认证来源，须与已确认健康约束逐项人工核对"
                        if charter_health_known
                        else "招生章程未提供可判定体检条件，不能按无限制处理，须逐校人工核对"
                    ),
                    charter_sources,
                    input_fields=(),
                    evidence_status=health_status,
                )
            )
        restriction_fields = (
            "charter_language_restrictions",
            "charter_single_subject_restrictions",
            "charter_special_conditions",
        )
        charter_restrictions_known = charter_usable and all(
            any(
                isinstance(row.get(field), str)
                and bool(str(row.get(field)).strip())
                for row in school_rows
            )
            for field in restriction_fields
        )
        restrictions_status = (
            charter_status
            if charter_restrictions_known
            else charter_status
            if charter_status in {
                EvidenceStatus.CONFLICT,
                EvidenceStatus.PARTIAL,
                EvidenceStatus.MASKED,
            }
            else EvidenceStatus.MISSING
        )
        reasons.append(
            _school_reason(
                profile,
                (
                    "SCHOOL_CHARTER_RESTRICTIONS_REVIEW_REQUIRED"
                    if charter_restrictions_known
                    else "SCHOOL_CHARTER_RESTRICTIONS_UNVERIFIED"
                ),
                (
                    "招生章程语种、单科和特殊条件已有认证来源，须结合成绩与语言准备逐项人工核对"
                    if charter_restrictions_known
                    else "招生章程语种、单科或特殊条件未披露，不能按无限制处理，须逐校人工核对"
                ),
                charter_sources,
                input_fields=(),
                evidence_status=restrictions_status,
            )
        )
        evidence_code = evidence_codes.get(
            item.evidence_status, "SCHOOL_EVIDENCE_UNUSABLE"
        )
        reasons.append(
            _school_reason(
                profile,
                evidence_code,
                {
                    "SCHOOL_EVIDENCE_OFFICIAL": "院校行由官方证据支持",
                    "SCHOOL_EVIDENCE_CORROBORATED": "院校行由独立第三方交叉印证",
                    "SCHOOL_EVIDENCE_REFERENCE": "院校行仅作多源参考，需复核当年专业数据",
                    "SCHOOL_EVIDENCE_PARTIAL": "院校行仅在已验证覆盖范围内可用，不能外推为完整结论",
                    "SCHOOL_EVIDENCE_UNUSABLE": "院校行证据不足，不能形成确定判断",
                }[evidence_code],
                source_ids,
                input_fields=(),
                evidence_status=item.evidence_status,
            )
        )
        ordered_reasons = tuple(sorted(reasons, key=_decision_reason_order))
        decorated_items.append(
            replace(
                item,
                source_ids=tuple(
                    sorted(
                        set(source_ids)
                        | set(fit_sources)
                        | set(province_sources)
                    )
                ),
                fit_evidence_statuses=tuple(
                    dict.fromkeys(
                        (
                            enrollment_status,
                            charter_status,
                            tuition_status,
                            subject_status,
                            province_status,
                        )
                    )
                ),
                match_reason="；".join(
                    f"[{reason.code}] {reason.explanation}" for reason in ordered_reasons
                ),
            )
        )
        included_decisions.append(
            SchoolDecision(
                school_name=item.school_name,
                outcome="included",
                order=order,
                stable_key=(
                    item.strategy,
                    item.school_name,
                    *(group.major_group_code for group in item.major_groups),
                    *(group.major_group_name for group in item.major_groups),
                    *item.source_ids,
                ),
                reasons=ordered_reasons,
            )
        )

    for school_name in sorted(cap_excluded):
        sources = tuple(sorted({
            source for row in by_school[school_name] for source in _source_ids(row)
        }))
        excluded[school_name] = (
            _school_reason(
                profile,
                "SCHOOL_RISK_CAP_EXCLUDED",
                "该档院校超过已确认风险偏好对应的项目规则上限",
                sources,
                input_fields=("constraints.risk_preference",),
            ),
        )
    observed_schools = {item.school_name for item in base_observations}
    for school_name in sorted(
        set(by_school) - seen_schools - observed_schools - set(excluded)
    ):
        sources = tuple(sorted({
            source for row in by_school[school_name] for source in _source_ids(row)
        }))
        excluded[school_name] = (
            _school_reason(
                profile,
                "SCHOOL_RANK_OUTSIDE_INTERVAL",
                "认证投档位次未进入当前可计算区间",
                tuple(sorted(set(sources) | set(rank_scenario.source_ids))),
                input_fields=("province",),
            ),
        )
    excluded_decisions = tuple(
        SchoolDecision(
            school_name=name,
            outcome="excluded",
            order=None,
            stable_key=("excluded", name),
            reasons=tuple(sorted(reasons, key=_decision_reason_order)),
        )
        for name, reasons in sorted(excluded.items())
    )
    result = None
    if policy is not None:
        assert base is not None
        effective_policy = OrdinaryBatchPolicy(
            schema_version=policy.schema_version,
            policy_id=policy.policy_id,
            basis_id=policy.basis_id,
            search_delta_min=policy.search_delta_min,
            search_delta_max=policy.search_delta_max,
            challenge_delta_lt=policy.challenge_delta_lt,
            stable_delta_le=policy.stable_delta_le,
            tier_caps=effective_caps,
        )
        result = replace(
            base,
            ordinary_batch_policy=effective_policy,
            items=tuple(decorated_items),
            empty_reason=(
                base.empty_reason
                if decorated_items
                else base.empty_reason or "profile_constraints"
            ),
        )
    return SchoolDecisionResult(
        items=tuple(decorated_items),
        decisions=tuple(included_decisions) + excluded_decisions,
        rank_scenario=rank_scenario,
        policy_status=(
            "ordinary_batch_policy_available"
            if policy is not None
            else "rank_delta_policy_unavailable"
        ),
        ordinary_batch_policy=(
            result.ordinary_batch_policy if result is not None else None
        ),
        warnings=decision_warnings,
        compatibility_result=result,
        observations=base_observations,
    )


__all__ = [
    "SchoolRecommendError",
    "is_in_province",
    "parse_secondary_subjects",
    "personalize_school_recommendations",
    "recommend_schools",
    "SchoolDecision",
    "SchoolDecisionResult",
]
