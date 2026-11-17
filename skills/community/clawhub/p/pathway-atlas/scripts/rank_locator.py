"""Deterministic multi-evidence provincial-rank location."""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
import json
import math
import re
from statistics import median
from typing import Any, Iterable, Mapping

if __package__:
    from .contracts import EvidenceStatus
    from .planning_profile import PlanningProfile
    from .rank_calc import RankAnchor, RankEstimate, RankScope, estimate_rank_from_anchors
    from .validate_data import ValidatedScoreRow
    from .year_fallback import year_window
else:  # pragma: no cover - flat scripts-path compatibility
    from contracts import EvidenceStatus
    from planning_profile import PlanningProfile
    from rank_calc import RankAnchor, RankEstimate, RankScope, estimate_rank_from_anchors
    from validate_data import ValidatedScoreRow
    from year_fallback import year_window


_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_CHANNEL_KINDS = frozenset(
    {"joint_exam", "school_anchor", "score_distribution", "group_prior"}
)
_ACCEPTED = frozenset(
    {EvidenceStatus.OFFICIAL, EvidenceStatus.CORROBORATED, EvidenceStatus.REFERENCE}
)
_SOURCE_MINIMUM = {
    EvidenceStatus.OFFICIAL: 1,
    EvidenceStatus.CORROBORATED: 2,
    EvidenceStatus.REFERENCE: 3,
}
_PROFILE_SOURCE_UNCERTAINTY = {
    "official_score": (0.02, "high"),
    "joint_exam_report": (0.04, "medium"),
    "school_report": (0.07, "low"),
    "user_reported": (0.10, "low"),
}
_PROFILE_SCOPE_UNCERTAINTY = {
    "province_official": (0.00, "high"),
    "province_joint": (0.03, "medium"),
    "city_joint": (0.06, "low"),
}
_CONFIDENCE_LEVEL = {"low": 0, "medium": 1, "high": 2}
_PROFILE_SCORE_BASIS_UNCERTAINTY = {
    "赋分": (0.00, "assigned"),
    "原始分与赋分": (0.03, "mixed"),
    "原始分": (0.08, "raw"),
    "不确定": (0.12, "uncertain"),
    None: (0.12, "unknown"),
}
_SCORE_TABLE_STATUS_UNCERTAINTY = {
    EvidenceStatus.OFFICIAL: 0.00,
    EvidenceStatus.CORROBORATED: 0.03,
    EvidenceStatus.REFERENCE: 0.06,
}
_STATUS_RELIABILITY = {
    EvidenceStatus.REFERENCE: 1,
    EvidenceStatus.CORROBORATED: 2,
    EvidenceStatus.OFFICIAL: 3,
}
_CHANNEL_VALUE_FIELDS = frozenset(
    {
        "schema_version",
        "channel_id",
        "kind",
        "profile_digest",
        "province",
        "subject_group",
        "high_school",
        "class_level",
        "year",
        "lower_percentile",
        "central_percentile",
        "upper_percentile",
        "coverage",
        "comparability",
        "backtest_error",
    }
)
_ANCHOR_VALUE_FIELDS = frozenset(
    {
        "schema_version",
        "profile_digest",
        "province",
        "subject_group",
        "class_level",
        "anchor_id",
        "year",
        "school_name",
        "scope_type",
        "scope_value",
        "school_rank",
        "province_rank",
        "school_score",
        "source_ids",
        "evidence_status",
        "coverage_status",
        "coverage_min_school_rank",
        "coverage_max_school_rank",
    }
)
_ANCHOR_COMPARABILITY_FIELDS = frozenset(
    {"comparability_tier", "comparability_basis"}
)
_SCHOOL_FALLBACK_UNCERTAINTY = {
    "exact_class": 0.00,
    "same_school": 0.05,
    "regional_similar": 0.10,
}
_SCHOOL_FALLBACK_REASON = {
    "exact_class": "school_anchor_fallback_exact_class",
    "same_school": "school_anchor_fallback_same_school",
    "regional_similar": "school_anchor_fallback_regional_similar",
}
_SCHOOL_FALLBACK_CONFIDENCE_CAP = {
    "exact_class": 2,
    "same_school": 1,
    "regional_similar": 0,
}


def _json_safe(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    raise TypeError(f"unsupported rank-scenario value: {type(value).__name__}")


def _status(value: Any) -> EvidenceStatus:
    if isinstance(value, EvidenceStatus):
        return value
    if not isinstance(value, str):
        raise TypeError("evidence status must be text")
    return EvidenceStatus(value)


def _bounded_number(
    value: Any,
    name: str,
    *,
    minimum: float,
    maximum: float,
    optional: bool = False,
) -> float | None:
    if value is None and optional:
        return None
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(f"{name} must be a finite number")
    result = float(value)
    if not math.isfinite(result) or result < minimum or result > maximum:
        raise ValueError(f"{name} is outside its supported range")
    return result


def _safe_ids(value: Any, name: str) -> tuple[str, ...]:
    if isinstance(value, (str, bytes, bytearray)):
        raise TypeError(f"{name} must be an ID collection")
    items = tuple(value)
    if not items or len(items) != len(set(items)):
        raise ValueError(f"{name} must contain unique IDs")
    if any(not isinstance(item, str) or _SAFE_ID.fullmatch(item) is None for item in items):
        raise ValueError(f"{name} contains an unsafe ID")
    return tuple(sorted(items))


@dataclass(frozen=True)
class _Channel:
    channel_id: str
    kind: str
    year: int
    lower_percentile: float
    central_percentile: float
    upper_percentile: float
    coverage: float
    comparability: float
    backtest_error: float | None
    source_ids: tuple[str, ...]
    status: EvidenceStatus
    cohort_size: int | None = None
    lower_rank: int | None = None
    central_rank: int | None = None
    upper_rank: int | None = None
    rank_scope: str | None = None
    exam_date: str | None = None


@dataclass(frozen=True)
class _RankInterval:
    kind: str
    year: int
    lower_rank: int
    central_rank: int
    upper_rank: int
    source_ids: tuple[str, ...]
    status: EvidenceStatus
    event_key: str | None = None


@dataclass(frozen=True)
class _ScoreTableEvidence:
    source_ids: tuple[str, ...]
    status: EvidenceStatus
    kind: str


@dataclass(frozen=True)
class _ProvincialCohortEvidence:
    cohort: int
    year: int
    source_ids: tuple[str, ...]
    status: EvidenceStatus
    kind: str


@dataclass(frozen=True)
class _SchoolAnchorEvidence:
    anchor: RankAnchor
    comparability_tier: str
    comparability_basis: str


@dataclass(frozen=True, init=False)
class RankScenario:
    status: EvidenceStatus
    basis: str
    optimistic_rank: int | None
    central_rank: int | None
    conservative_rank: int | None
    confidence: str
    source_ids: tuple[str, ...]
    contributing_years: tuple[int, ...]
    backtest_error: float | None
    reasons: tuple[str, ...]
    channel_kinds: tuple[str, ...]
    channel_statuses: tuple[str, ...]
    rejected_channel_count: int

    def __init__(self) -> None:
        raise TypeError("RankScenario is factory-only")

    @classmethod
    def _create(cls, **values: Any) -> "RankScenario":
        if set(values) != {item.name for item in fields(cls)}:
            raise TypeError("RankScenario factory fields do not match the contract")
        status = _status(values["status"])
        if status not in {
            EvidenceStatus.OFFICIAL,
            EvidenceStatus.INFERRED,
            EvidenceStatus.MISSING,
            EvidenceStatus.CONFLICT,
        }:
            raise ValueError("unsupported rank scenario status")
        values["status"] = status
        ranks = (
            values["optimistic_rank"],
            values["central_rank"],
            values["conservative_rank"],
        )
        if status in {EvidenceStatus.OFFICIAL, EvidenceStatus.INFERRED}:
            if any(
                not isinstance(rank, int) or isinstance(rank, bool) or rank < 1
                for rank in ranks
            ):
                raise TypeError("numeric rank scenarios require positive integer bounds")
            if not ranks[0] <= ranks[1] <= ranks[2]:
                raise ValueError("rank scenario bounds must be ordered")
        elif any(rank is not None for rank in ranks):
            raise ValueError("non-numeric rank scenarios cannot contain bounds")
        confidence = values["confidence"]
        if confidence not in {"high", "medium", "low", "none"}:
            raise ValueError("unsupported rank scenario confidence")
        if status in {EvidenceStatus.MISSING, EvidenceStatus.CONFLICT} and confidence != "none":
            raise ValueError("non-numeric scenarios require no confidence")
        values["source_ids"] = (
            _safe_ids(values["source_ids"], "source_ids")
            if values["source_ids"]
            else ()
        )
        years = tuple(values["contributing_years"])
        if len(years) != len(set(years)) or any(
            not isinstance(year, int)
            or isinstance(year, bool)
            or year < 2000
            or year > 2100
            for year in years
        ):
            raise ValueError("contributing_years must be unique supported years")
        values["contributing_years"] = tuple(sorted(years))
        for name in ("reasons", "channel_kinds", "channel_statuses"):
            items = tuple(values[name])
            if len(items) != len(set(items)) or any(
                not isinstance(item, str) or _SAFE_ID.fullmatch(item) is None
                for item in items
            ):
                raise ValueError(f"{name} must contain unique safe identifiers")
            values[name] = tuple(sorted(items))
        rejected = values["rejected_channel_count"]
        if not isinstance(rejected, int) or isinstance(rejected, bool) or rejected < 0:
            raise TypeError("rejected_channel_count must be a non-negative integer")
        error = values["backtest_error"]
        if error is not None:
            values["backtest_error"] = _bounded_number(
                error, "backtest_error", minimum=0, maximum=1
            )
        instance = object.__new__(cls)
        for name, value in values.items():
            object.__setattr__(instance, name, value)
        return instance

    def to_dict(self) -> dict[str, Any]:
        return {item.name: _json_safe(getattr(self, item.name)) for item in fields(self)}


def _missing(reasons: Iterable[str], rejected: int = 0) -> RankScenario:
    return RankScenario._create(
        status=EvidenceStatus.MISSING,
        basis="unavailable",
        optimistic_rank=None,
        central_rank=None,
        conservative_rank=None,
        confidence="none",
        source_ids=(),
        contributing_years=(),
        backtest_error=None,
        reasons=tuple(sorted(set(reasons))),
        channel_kinds=(),
        channel_statuses=(),
        rejected_channel_count=rejected,
    )


def unavailable_rank_scenario(reason: str) -> RankScenario:
    """Create the public fail-closed scenario for a verified empty evidence bundle."""

    if not isinstance(reason, str) or _SAFE_ID.fullmatch(reason) is None:
        raise ValueError("missing-rank reason must be a safe identifier")
    return _missing((reason,))


def _conflict(channels: tuple[_Channel, ...], rejected: int) -> RankScenario:
    return RankScenario._create(
        status=EvidenceStatus.CONFLICT,
        basis="conflicting_authenticated_channels",
        optimistic_rank=None,
        central_rank=None,
        conservative_rank=None,
        confidence="none",
        source_ids=tuple(sorted({source for item in channels for source in item.source_ids})),
        contributing_years=tuple(sorted({item.year for item in channels})),
        backtest_error=None,
        reasons=("authenticated_channel_interval_conflict",),
        channel_kinds=tuple(sorted({item.kind for item in channels})),
        channel_statuses=tuple(sorted({item.status.value for item in channels})),
        rejected_channel_count=rejected,
    )


def _score_payload(row: ValidatedScoreRow) -> dict[str, str | int]:
    if not isinstance(row, ValidatedScoreRow):
        raise TypeError("score_rows must contain ValidatedScoreRow records")
    return row.to_dict()


def _matching_score_rows(
    profile: PlanningProfile,
    score_rows: Iterable[ValidatedScoreRow],
    subject_group: str | None = None,
    research_year: int | None = None,
) -> tuple[dict[str, str | int], ...]:
    expected_subject_group = subject_group or profile.subject_group
    if not isinstance(expected_subject_group, str) or not expected_subject_group.strip():
        raise TypeError("score subject group must be non-empty text")
    window = set(year_window(profile.exam_year if research_year is None else research_year))
    rows = tuple(_score_payload(row) for row in score_rows)
    return tuple(
        sorted(
            (
                row
                for row in rows
                if row["subject_group"] == expected_subject_group and row["year"] in window
            ),
            key=lambda row: (-int(row["year"]), -int(row["score"])),
        )
    )


def _cohort_context(
    profile: PlanningProfile,
    score_rows: Iterable[ValidatedScoreRow],
    subject_group: str | None = None,
    research_year: int | None = None,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    rows = _matching_score_rows(profile, score_rows, subject_group, research_year)
    by_year: dict[int, int] = {}
    for row in rows:
        year = int(row["year"])
        by_year[year] = max(by_year.get(year, 0), int(row["cumulative_count"]))
    years = tuple(sorted(by_year, reverse=True)[:3])
    cohorts = tuple(by_year[year] for year in years)
    return years, cohorts


def _profile_reported_bounds(
    rank: int,
    observation: Any,
    *,
    score_basis: str | None = None,
    include_score_basis: bool = False,
    table_status: EvidenceStatus | None = None,
    cohort_bound: int | None = None,
) -> tuple[int, int, str, tuple[str, ...], float]:
    source_ratio, confidence = _PROFILE_SOURCE_UNCERTAINTY[observation.source]
    ratio = source_ratio
    reasons = [f"profile_source_{observation.source}"]
    if observation.scope in _PROFILE_SCOPE_UNCERTAINTY:
        scope_ratio, scope_confidence = _PROFILE_SCOPE_UNCERTAINTY[
            observation.scope
        ]
        ratio += scope_ratio
        reasons.append(f"profile_scope_{observation.scope}")
        if _CONFIDENCE_LEVEL[scope_confidence] < _CONFIDENCE_LEVEL[confidence]:
            confidence = scope_confidence
    if include_score_basis:
        basis_ratio, basis_code = _PROFILE_SCORE_BASIS_UNCERTAINTY[score_basis]
        ratio += basis_ratio
        reasons.append(f"profile_score_basis_{basis_code}")
        if basis_ratio >= 0.08:
            confidence = "low"
    if table_status is not None:
        ratio += _SCORE_TABLE_STATUS_UNCERTAINTY[table_status]
        reasons.append(f"score_table_evidence_{table_status.value}")
        if table_status is EvidenceStatus.REFERENCE:
            confidence = "low"
    ratio = min(0.35, ratio)
    spread = max(1, math.ceil(rank * ratio))
    lower = max(1, rank - spread)
    upper = rank + spread
    effective_cohort = (
        cohort_bound if cohort_bound is not None else observation.cohort_size
    )
    if effective_cohort is not None:
        upper = min(effective_cohort, upper)
    upper = max(rank, upper)
    return lower, upper, confidence, tuple(reasons), ratio


def _joint_event_key(exam_date: str, scope: str) -> str:
    return f"joint_exam:{exam_date}:{scope}"


def _project_joint_rank(observation: Any, provincial_cohort: int | None) -> int | None:
    if observation.scope not in {"province_joint", "city_joint"}:
        return observation.rank
    if (
        observation.rank is None
        or observation.cohort_size is None
        or provincial_cohort is None
    ):
        return None
    return max(
        1,
        math.ceil(observation.rank * provincial_cohort / observation.cohort_size),
    )


def _direct_rank_observation(profile: PlanningProfile) -> Any | None:
    official = tuple(
        item
        for item in profile.rank_observations
        if item.scope == "province_official" and item.rank is not None
    )
    if official:
        return max(official, key=lambda item: item.exam_date)
    joint = tuple(
        item
        for item in profile.rank_observations
        if item.scope in {"province_joint", "city_joint"}
        and item.source == "joint_exam_report"
        and item.rank is not None
    )
    if not joint:
        return None
    scope_priority = {"city_joint": 0, "province_joint": 1}
    return max(
        joint,
        key=lambda item: (item.exam_date, scope_priority[item.scope]),
    )


def _profile_reported_scenario(
    profile: PlanningProfile,
    rows: tuple[dict[str, str | int], ...],
    score_evidence: Mapping[tuple[int, int], _ScoreTableEvidence] | None = None,
    research_year: int | None = None,
    provincial_cohort: int | None = None,
    cohort_evidence: _ProvincialCohortEvidence | None = None,
) -> RankScenario | None:
    direct = _direct_rank_observation(profile)
    if direct is not None:
        projected_rank = _project_joint_rank(direct, provincial_cohort)
        if projected_rank is None:
            return None
        lower, upper, confidence, reasons, uncertainty = _profile_reported_bounds(
            projected_rank,
            direct,
            cohort_bound=(
                provincial_cohort
                if direct.scope in {"province_joint", "city_joint"}
                else None
            ),
        )
        if direct.scope in {"province_joint", "city_joint"}:
            reasons = (*reasons, "joint_exam_cohort_projected_to_province")
        cohort_sources = (
            cohort_evidence.source_ids
            if direct.scope in {"province_joint", "city_joint"}
            and cohort_evidence is not None
            else ()
        )
        cohort_years = (
            (cohort_evidence.year,)
            if direct.scope in {"province_joint", "city_joint"}
            and cohort_evidence is not None
            else ()
        )
        cohort_kinds = (
            (cohort_evidence.kind,)
            if direct.scope in {"province_joint", "city_joint"}
            and cohort_evidence is not None
            else ()
        )
        cohort_statuses = (
            (cohort_evidence.status.value,)
            if direct.scope in {"province_joint", "city_joint"}
            and cohort_evidence is not None
            else ()
        )
        return RankScenario._create(
            status=EvidenceStatus.INFERRED,
            basis="profile_reported_province_rank",
            optimistic_rank=lower,
            central_rank=projected_rank,
            conservative_rank=upper,
            confidence=confidence,
            source_ids=tuple(sorted({"profile-reported-rank", *cohort_sources})),
            contributing_years=tuple(
                sorted({int(direct.exam_date[:4]), *cohort_years})
            ),
            backtest_error=uncertainty,
            reasons=reasons,
            channel_kinds=tuple(
                sorted({"profile_reported_rank", *cohort_kinds})
            ),
            channel_statuses=tuple(sorted({"inferred", *cohort_statuses})),
            rejected_channel_count=0,
        )
    reported = tuple(
        item for item in profile.rank_observations if item.scope == "province_official"
    )
    if not reported:
        return None
    latest = max(reported, key=lambda item: item.exam_date)
    if latest.score is None:
        return None
    candidates = tuple(
        row
        for row in rows
        if int(row["score"]) == latest.score
        and (
            score_evidence is None
            or (int(row["year"]), int(row["score"])) in score_evidence
        )
    )
    if not candidates:
        return None
    selected = candidates[0]
    selected_year = int(selected["year"])
    rank = int(selected["rank"])
    fallback = (research_year if research_year is not None else selected_year) - selected_year
    table_evidence = (
        score_evidence.get((selected_year, int(selected["score"])))
        if score_evidence is not None
        else None
    )
    lower, upper, confidence, reasons, uncertainty = _profile_reported_bounds(
        rank,
        latest,
        score_basis=profile.score_basis,
        include_score_basis=True,
        table_status=(table_evidence.status if table_evidence is not None else None),
    )
    table_sources = (
        table_evidence.source_ids
        if table_evidence is not None
        else (f"score-table:{selected_year}",)
    )
    return RankScenario._create(
        status=EvidenceStatus.INFERRED,
        basis="profile_reported_score_table",
        optimistic_rank=lower,
        central_rank=rank,
        conservative_rank=upper,
        confidence=confidence,
        source_ids=tuple(sorted({"profile-reported-score", *table_sources})),
        contributing_years=(selected_year,),
        backtest_error=uncertainty,
        reasons=(*reasons, f"year_fallback:{fallback}"),
        channel_kinds=tuple(
            sorted(
                {
                    "profile_reported_score",
                    (
                        table_evidence.kind
                        if table_evidence is not None
                        else "profile_reported_score"
                    ),
                }
            )
        ),
        channel_statuses=(
            ("inferred", table_evidence.status.value)
            if table_evidence is not None
            else ("inferred",)
        ),
        rejected_channel_count=0,
    )


def _profile_reported_intervals(
    profile: PlanningProfile,
    rows: tuple[dict[str, str | int], ...],
    score_evidence: Mapping[tuple[int, int], _ScoreTableEvidence] | None,
    scenario: RankScenario | None,
) -> tuple[_RankInterval, ...]:
    if scenario is None:
        return ()
    assert scenario.optimistic_rank is not None
    assert scenario.central_rank is not None
    assert scenario.conservative_rank is not None
    direct = _direct_rank_observation(profile)
    if direct is not None:
        return (
            _RankInterval(
                kind=scenario.channel_kinds[0],
                year=int(direct.exam_date[:4]),
                lower_rank=scenario.optimistic_rank,
                central_rank=scenario.central_rank,
                upper_rank=scenario.conservative_rank,
                source_ids=scenario.source_ids,
                status=EvidenceStatus.INFERRED,
                event_key=(
                    _joint_event_key(direct.exam_date, direct.scope)
                    if direct.scope in {"province_joint", "city_joint"}
                    else None
                ),
            ),
        )
    reported = tuple(
        item for item in profile.rank_observations if item.scope == "province_official"
    )
    if not reported:
        return ()
    latest = max(reported, key=lambda item: item.exam_date)
    if latest.score is None:
        return ()
    intervals: list[_RankInterval] = []
    for row in rows:
        if int(row["score"]) != latest.score:
            continue
        year = int(row["year"])
        rank = int(row["rank"])
        table_evidence = (
            score_evidence.get((year, int(row["score"])))
            if score_evidence is not None
            else None
        )
        if score_evidence is not None and table_evidence is None:
            continue
        lower, upper, _confidence, _reasons, _uncertainty = (
            _profile_reported_bounds(
                rank,
                latest,
                score_basis=profile.score_basis,
                include_score_basis=True,
                table_status=(
                    table_evidence.status if table_evidence is not None else None
                ),
            )
        )
        table_sources = (
            table_evidence.source_ids
            if table_evidence is not None
            else (f"score-table:{year}",)
        )
        intervals.append(
            _RankInterval(
                kind=(
                    table_evidence.kind
                    if table_evidence is not None
                    else "profile_reported_score"
                ),
                year=year,
                lower_rank=lower,
                central_rank=rank,
                upper_rank=upper,
                source_ids=tuple(
                    sorted({"profile-reported-score", *table_sources})
                ),
                status=(
                    table_evidence.status
                    if table_evidence is not None
                    else EvidenceStatus.INFERRED
                ),
            )
        )
    return tuple(intervals)


def _fact_mapping(value: Any) -> Mapping[str, Any]:
    if hasattr(value, "to_dict"):
        value = value.to_dict()
    if not isinstance(value, Mapping):
        raise TypeError("evidence facts must be mappings")
    return value


def _fact_channel(
    profile: PlanningProfile,
    raw: Any,
    *,
    subject_group: str | None = None,
    authenticated: bool = False,
    research_year: int | None = None,
) -> _Channel:
    fact = _fact_mapping(raw)
    field = fact.get("field")
    value = fact.get("value")
    if not isinstance(field, str) or not field.startswith("rank_channel:"):
        raise ValueError("fact is not a rank channel")
    if not isinstance(value, Mapping):
        raise ValueError("rank channel value fields do not match the contract")
    if authenticated:
        required_auth = {
            "query_plan_digest", "query_task_id", "row_hash", "artifact_digest",
            "provenance_digest", "bridge_digest", "coverage_status",
            "coverage_min_rank", "coverage_max_rank", "cohort_size",
            "rank_scope", "exam_date",
        }
        if not _CHANNEL_VALUE_FIELDS.issubset(value) or not required_auth.issubset(value):
            raise ValueError("authenticated rank channel fields do not match the contract")
    elif set(value) != _CHANNEL_VALUE_FIELDS:
        raise ValueError("rank channel value fields do not match the contract")
    channel_id = value["channel_id"]
    if field != f"rank_channel:{channel_id}":
        raise ValueError("rank channel field does not match its ID")
    if not isinstance(channel_id, str) or _SAFE_ID.fullmatch(channel_id) is None:
        raise ValueError("rank channel ID is unsafe")
    kind = value["kind"]
    if kind not in _CHANNEL_KINDS - {"school_anchor"}:
        raise ValueError("unsupported authenticated rank channel kind")
    if value["schema_version"] != "1.0" or value["profile_digest"] != profile.digest:
        raise ValueError("rank channel is not bound to this profile")
    for field_name, expected in (
        ("province", profile.province),
        ("subject_group", subject_group or profile.subject_group),
        ("high_school", profile.high_school),
        ("class_level", profile.class_level),
    ):
        if value[field_name] != expected:
            raise ValueError("rank channel context does not match the profile")
    year = value["year"]
    if (
        not isinstance(year, int)
        or isinstance(year, bool)
        or year
        not in year_window(
            research_year
            if authenticated and research_year is not None
            else profile.exam_year
        )
    ):
        raise ValueError("rank channel year is outside the fallback window")
    lower = _bounded_number(
        value["lower_percentile"], "lower_percentile", minimum=0, maximum=1
    )
    central = _bounded_number(
        value["central_percentile"], "central_percentile", minimum=0, maximum=1
    )
    upper = _bounded_number(
        value["upper_percentile"], "upper_percentile", minimum=0, maximum=1
    )
    assert lower is not None and central is not None and upper is not None
    if not lower <= central <= upper:
        raise ValueError("rank channel percentile bounds must be ordered")
    coverage = _bounded_number(value["coverage"], "coverage", minimum=0.01, maximum=1)
    comparability = _bounded_number(
        value["comparability"], "comparability", minimum=0.01, maximum=1
    )
    error = _bounded_number(
        value["backtest_error"], "backtest_error", minimum=0, maximum=1, optional=True
    )
    sources = _safe_ids(fact.get("source_ids"), "rank channel source_ids")
    status = _status(fact.get("status"))
    if status not in _ACCEPTED or len(sources) < _SOURCE_MINIMUM[status]:
        raise ValueError("rank channel does not meet the evidence threshold")
    cohort_size = value.get("cohort_size") if authenticated else None
    if cohort_size is not None and (
        not isinstance(cohort_size, int) or isinstance(cohort_size, bool) or cohort_size < 1
    ):
        raise ValueError("authenticated rank channel cohort is invalid")
    absolute_ranks: tuple[int | None, int | None, int | None] = (None, None, None)
    if authenticated and kind == "joint_exam":
        absolute_ranks = (
            value.get("lower_rank"),
            value.get("central_rank"),
            value.get("upper_rank"),
        )
        if (
            cohort_size is None
            or any(
                not isinstance(item, int) or isinstance(item, bool) or item < 1
                for item in absolute_ranks
            )
            or not absolute_ranks[0] <= absolute_ranks[1] <= absolute_ranks[2]
            or absolute_ranks[2] > cohort_size
        ):
            raise ValueError("authenticated joint rank interval is invalid")
        rank_scope = value.get("rank_scope")
        exam_date = value.get("exam_date")
        if rank_scope not in {"province_joint", "city_joint"}:
            raise ValueError("authenticated joint rank scope is invalid")
        if (
            not isinstance(exam_date, str)
            or len(exam_date) != 10
            or not exam_date.startswith(f"{year:04d}-")
        ):
            raise ValueError("authenticated joint exam date is invalid")
    else:
        rank_scope = None
        exam_date = None
    return _Channel(
        channel_id=channel_id,
        kind=kind,
        year=year,
        lower_percentile=lower,
        central_percentile=central,
        upper_percentile=upper,
        coverage=coverage,
        comparability=comparability,
        backtest_error=error,
        source_ids=sources,
        status=status,
        cohort_size=cohort_size,
        lower_rank=absolute_ranks[0],
        central_rank=absolute_ranks[1],
        upper_rank=absolute_ranks[2],
        rank_scope=rank_scope,
        exam_date=exam_date,
    )


def _fact_anchor(
    profile: PlanningProfile,
    raw: Any,
    *,
    subject_group: str | None = None,
    authenticated: bool = False,
) -> RankAnchor | _SchoolAnchorEvidence:
    fact = _fact_mapping(raw)
    field = fact.get("field")
    value = fact.get("value")
    if not isinstance(field, str) or not field.startswith("rank_anchor:"):
        raise ValueError("fact is not a rank anchor")
    if not isinstance(value, Mapping):
        raise ValueError("rank anchor value fields do not match the contract")
    if authenticated:
        required_auth = {
            "query_plan_digest", "query_task_id", "row_hash", "artifact_digest",
            "provenance_digest", "bridge_digest", "cohort_size",
        }
        if (
            not (_ANCHOR_VALUE_FIELDS | _ANCHOR_COMPARABILITY_FIELDS).issubset(value)
            or not required_auth.issubset(value)
        ):
            raise ValueError("authenticated rank anchor fields do not match the contract")
    elif set(value) != _ANCHOR_VALUE_FIELDS:
        raise ValueError("rank anchor value fields do not match the contract")
    anchor_id = value["anchor_id"]
    if field != f"rank_anchor:{anchor_id}":
        raise ValueError("rank anchor field does not match its ID")
    if value["schema_version"] != "1.0" or value["profile_digest"] != profile.digest:
        raise ValueError("rank anchor is not bound to this profile")
    if (
        value["province"] != profile.province
        or value["subject_group"] != (subject_group or profile.subject_group)
        or value["class_level"] != profile.class_level
    ):
        raise ValueError("rank anchor context does not match the profile")
    if not authenticated and value["year"] not in year_window(profile.exam_year):
        raise ValueError("rank anchor year is outside the fallback window")
    outer_sources = _safe_ids(fact.get("source_ids"), "rank anchor source_ids")
    inner_sources = _safe_ids(value["source_ids"], "rank anchor value source_ids")
    outer_status = _status(fact.get("status"))
    inner_status = _status(value["evidence_status"])
    if outer_sources != inner_sources or outer_status != inner_status:
        raise ValueError("rank anchor projection conflicts with its evidence fact")
    if outer_status not in _ACCEPTED or len(outer_sources) < _SOURCE_MINIMUM[outer_status]:
        raise ValueError("rank anchor does not meet the evidence threshold")
    anchor = RankAnchor(
        anchor_id=anchor_id,
        year=value["year"],
        school_name=value["school_name"],
        scope_type=value["scope_type"],
        scope_value=value["scope_value"],
        school_rank=value["school_rank"],
        province_rank=value["province_rank"],
        school_score=value["school_score"],
        source_ids=inner_sources,
        evidence_status=inner_status,
        coverage_status=value["coverage_status"],
        coverage_min_school_rank=value["coverage_min_school_rank"],
        coverage_max_school_rank=value["coverage_max_school_rank"],
    )
    if not authenticated:
        return anchor
    tier = value["comparability_tier"]
    basis = value["comparability_basis"]
    if tier not in _SCHOOL_FALLBACK_UNCERTAINTY or not isinstance(basis, str):
        raise ValueError("rank anchor comparability metadata is invalid")
    exact_class = (
        anchor.school_name == profile.high_school
        and anchor.scope_type is RankScope.NAMED_PROGRAM
        and anchor.scope_value == profile.class_level
    )
    same_school = anchor.school_name == profile.high_school
    if tier == "exact_class" and (
        not exact_class or basis != "same_school_exact_class"
    ):
        raise ValueError("exact-class rank anchor comparability is inconsistent")
    if tier == "same_school" and (
        not same_school
        or exact_class
        or basis
        not in {
            "authenticated_same_school_other_class_cohort",
            "authenticated_same_school_whole_school_cohort",
        }
    ):
        raise ValueError("same-school rank anchor comparability is inconsistent")
    if tier == "regional_similar" and (
        same_school
        or basis
        not in {
            "authenticated_similar_school_cohort",
            "authenticated_regional_cohort",
        }
    ):
        raise ValueError("regional rank anchor comparability is inconsistent")
    return _SchoolAnchorEvidence(
        anchor=anchor,
        comparability_tier=tier,
        comparability_basis=basis,
    )


def _integer_median(values: tuple[int, ...]) -> int:
    return int(median(values))


def _school_channel(
    profile: PlanningProfile,
    anchors: Iterable[RankAnchor],
    cohorts: tuple[int, ...],
) -> tuple[_Channel | None, tuple[int, ...], tuple[str, ...]]:
    if not cohorts:
        return None, (), ()
    estimate, usable = _school_estimate(profile, anchors)
    if estimate is None:
        return None, (), ()
    cohort = _integer_median(cohorts)
    offsets = tuple(item.province_rank - item.school_rank for item in usable)
    errors: list[int] = []
    for index, item in enumerate(usable):
        other = offsets[:index] + offsets[index + 1 :]
        if other:
            errors.append(abs(item.school_rank + _integer_median(other) - item.province_rank))
    backtest = (float(median(errors)) / cohort) if errors else None
    status_order = {
        EvidenceStatus.REFERENCE: 1,
        EvidenceStatus.CORROBORATED: 2,
        EvidenceStatus.OFFICIAL: 3,
    }
    anchor_status = min(
        (item.evidence_status for item in usable),
        key=lambda item: status_order[item],
    )
    return (
        _Channel(
            channel_id="school-anchor",
            kind="school_anchor",
            year=max(estimate.contributing_years),
            lower_percentile=max(0.0, estimate.lower_rank / cohort),
            central_percentile=min(1.0, estimate.median_rank / cohort),
            upper_percentile=min(1.0, estimate.upper_rank / cohort),
            coverage=min(1.0, estimate.usable_anchor_count / 3),
            comparability=1.0,
            backtest_error=backtest,
            source_ids=estimate.contributing_source_ids,
            status=anchor_status,
        ),
        estimate.contributing_years,
        estimate.reasons,
    )


def _school_anchor_evidence(
    profile: PlanningProfile,
    item: RankAnchor | _SchoolAnchorEvidence,
) -> _SchoolAnchorEvidence | None:
    if isinstance(item, _SchoolAnchorEvidence):
        return item
    if not isinstance(item, RankAnchor):
        return None
    exact_class = (
        item.school_name == profile.high_school
        and item.scope_type is RankScope.NAMED_PROGRAM
        and item.scope_value == profile.class_level
    )
    if exact_class:
        return _SchoolAnchorEvidence(
            anchor=item,
            comparability_tier="exact_class",
            comparability_basis="same_school_exact_class",
        )
    # Every broadened anchor (other class, whole school, or regional school)
    # must arrive through an authenticated fact with explicit comparability.
    return None


def _school_estimate(
    profile: PlanningProfile,
    anchors: Iterable[RankAnchor | _SchoolAnchorEvidence],
    research_year: int | None = None,
) -> tuple[RankEstimate | None, tuple[RankAnchor, ...]]:
    if profile.high_school is None or profile.class_level is None:
        return None, ()
    observations = tuple(
        item
        for item in profile.rank_observations
        if item.scope == "school" and item.rank is not None
    )
    if not observations:
        return None, ()
    latest = max(observations, key=lambda item: item.exam_date)
    window = set(year_window(profile.exam_year if research_year is None else research_year))
    evidence = tuple(
        record
        for item in anchors
        if (record := _school_anchor_evidence(profile, item)) is not None
        and record.anchor.year in window
        and record.anchor.evidence_status in _ACCEPTED
        and record.anchor.coverage_status in _ACCEPTED
    )
    grouped: dict[
        tuple[str, str, str, str, str], list[_SchoolAnchorEvidence]
    ] = {}
    for record in evidence:
        anchor = record.anchor
        grouped.setdefault(
            (
                record.comparability_tier,
                anchor.school_name,
                anchor.scope_type.value,
                anchor.scope_value,
                record.comparability_basis,
            ),
            [],
        ).append(record)
    selected_estimate: RankEstimate | None = None
    selected_records: tuple[_SchoolAnchorEvidence, ...] = ()
    for tier in ("exact_class", "same_school", "regional_similar"):
        tier_groups = tuple(
            records for key, records in grouped.items() if key[0] == tier
        )
        ordered_groups = sorted(
            tier_groups,
            key=lambda records: (
                -len({item.anchor.year for item in records}),
                -len(records),
                records[0].anchor.school_name,
                records[0].anchor.scope_type.value,
                records[0].anchor.scope_value,
                records[0].comparability_basis,
            ),
        )
        for records in ordered_groups:
            anchors_in_group = tuple(item.anchor for item in records)
            candidate = estimate_rank_from_anchors(
                anchors_in_group, latest.score, latest.rank
            )
            if candidate.status is EvidenceStatus.CONFLICT:
                return None, anchors_in_group
            if candidate.status is EvidenceStatus.INFERRED:
                selected_estimate = candidate
                selected_records = tuple(records)
                break
        if selected_estimate is not None:
            break
    if selected_estimate is None:
        return None, tuple(item.anchor for item in evidence)
    estimate = selected_estimate
    usable = tuple(item.anchor for item in selected_records)
    fallback_tier = selected_records[0].comparability_tier
    comparability_basis = selected_records[0].comparability_basis
    best_estimate = (
        estimate_rank_from_anchors(usable, None, profile.best_rank)
        if profile.best_rank is not None
        else None
    )
    usual_estimate = (
        estimate_rank_from_anchors(usable, None, profile.usual_rank)
        if profile.usual_rank is not None
        else None
    )
    reasons = set(estimate.reasons)
    reasons.add(_SCHOOL_FALLBACK_REASON[fallback_tier])
    reasons.add(f"school_anchor_comparability_{comparability_basis}")
    lower_candidates = [estimate.lower_rank]
    upper_candidates = [estimate.upper_rank]
    central = estimate.median_rank
    if best_estimate is not None and best_estimate.status is EvidenceStatus.INFERRED:
        lower_candidates.append(best_estimate.lower_rank)
        reasons.add("profile_best_rank_bound")
    if usual_estimate is not None and usual_estimate.status is EvidenceStatus.INFERRED:
        central = usual_estimate.median_rank
        upper_candidates.append(usual_estimate.upper_rank)
        reasons.add("profile_usual_rank_anchor")
    assert central is not None
    source_ratio, source_confidence = _PROFILE_SOURCE_UNCERTAINTY[latest.source]
    source_spread = max(1, math.ceil(central * source_ratio))
    lower = max(
        1,
        min(value for value in lower_candidates if value is not None)
        - source_spread,
    )
    upper = max(
        central,
        max(value for value in upper_candidates if value is not None) + source_spread,
    )
    fallback_spread = math.ceil(
        central * _SCHOOL_FALLBACK_UNCERTAINTY[fallback_tier]
    )
    lower = max(1, lower - fallback_spread)
    upper += fallback_spread
    central = max(lower, min(central, upper))
    reasons.add(f"profile_source_{latest.source}")
    estimate_confidence = {
        "high": 2,
        "moderate": 1,
        "corroborated": 1,
    }.get(estimate.confidence, 0)
    confidence_level = min(
        estimate_confidence,
        _CONFIDENCE_LEVEL[source_confidence],
        _SCHOOL_FALLBACK_CONFIDENCE_CAP[fallback_tier],
    )
    confidence = ("low", "medium", "high")[confidence_level]
    return (
        RankEstimate(
            status=EvidenceStatus.INFERRED,
            lower_rank=lower,
            upper_rank=upper,
            median_rank=central,
            method=f"{estimate.method}_profile_calibrated_{fallback_tier}",
            confidence=confidence,
            input_anchor_count=estimate.input_anchor_count,
            usable_anchor_count=estimate.usable_anchor_count,
            rejected_anchor_count=estimate.rejected_anchor_count,
            rejection_reasons=estimate.rejection_reasons,
            reason_code=None,
            reasons=tuple(sorted(reasons)),
            contributing_anchor_ids=estimate.contributing_anchor_ids,
            contributing_years=estimate.contributing_years,
            contributing_source_ids=estimate.contributing_source_ids,
            tolerance_rank=max(central - lower, upper - central),
        ),
        usable,
    )


def _absolute_school_scenario(
    profile: PlanningProfile,
    anchors: Iterable[RankAnchor],
    rejected: int,
) -> RankScenario | None:
    estimate, usable = _school_estimate(profile, anchors)
    if estimate is None:
        return None
    confidence = (
        estimate.confidence
        if estimate.confidence in {"high", "medium", "low"}
        else "medium"
    )
    return RankScenario._create(
        status=EvidenceStatus.INFERRED,
        basis="school_anchor_interval",
        optimistic_rank=estimate.lower_rank,
        central_rank=estimate.median_rank,
        conservative_rank=estimate.upper_rank,
        confidence=confidence,
        source_ids=estimate.contributing_source_ids,
        contributing_years=estimate.contributing_years,
        backtest_error=None,
        reasons=tuple(
            sorted({"provincial_anchor_interval_preserved", *estimate.reasons})
        ),
        channel_kinds=("school_anchor",),
        channel_statuses=tuple(
            sorted({item.evidence_status.value for item in usable})
        ),
        rejected_channel_count=rejected,
    )


def _authenticated_interval_scenario(
    profile_reported: RankScenario | None,
    official_intervals: Iterable[_RankInterval],
    channels: Iterable[_Channel],
    profile: PlanningProfile,
    anchors: Iterable[RankAnchor],
    rejected: int,
    research_year: int | None = None,
    provincial_cohort: int | None = None,
    cohort_evidence: _ProvincialCohortEvidence | None = None,
) -> RankScenario | None:
    """Intersect every authenticated absolute rank interval before returning."""

    profile_intervals = list(official_intervals)
    channel_intervals: list[_RankInterval] = []
    joint_scopes: set[str] = set()
    for channel in channels:
        if (
            channel.lower_rank is None
            or channel.central_rank is None
            or channel.upper_rank is None
        ):
            continue
        lower_rank = channel.lower_rank
        central_rank = channel.central_rank
        upper_rank = channel.upper_rank
        event_key = None
        if channel.kind == "joint_exam":
            if provincial_cohort is None:
                continue
            lower_rank = max(1, math.ceil(channel.lower_percentile * provincial_cohort))
            central_rank = max(
                1, math.ceil(channel.central_percentile * provincial_cohort)
            )
            upper_rank = max(1, math.ceil(channel.upper_percentile * provincial_cohort))
            assert channel.rank_scope is not None and channel.exam_date is not None
            event_key = _joint_event_key(channel.exam_date, channel.rank_scope)
            joint_scopes.add(channel.rank_scope)
        channel_intervals.append(
            _RankInterval(
                kind=channel.kind,
                year=channel.year,
                lower_rank=lower_rank,
                central_rank=central_rank,
                upper_rank=upper_rank,
                source_ids=channel.source_ids,
                status=channel.status,
                event_key=event_key,
            )
        )
    authenticated_event_keys = {
        item.event_key for item in channel_intervals if item.event_key is not None
    }
    profile_intervals = [
        item
        for item in profile_intervals
        if item.event_key is None or item.event_key not in authenticated_event_keys
    ]
    profile_included = bool(profile_intervals)
    intervals = [*profile_intervals, *channel_intervals]
    profile_reasons = (
        profile_reported.reasons
        if profile_reported is not None and profile_included
        else ()
    )
    if channel_intervals and joint_scopes:
        profile_reasons = (
            *profile_reasons,
            "joint_exam_cohort_projected_to_province",
        )
    cohort_sources = (
        set(cohort_evidence.source_ids)
        if joint_scopes and cohort_evidence is not None
        else set()
    )
    cohort_kinds = (
        {cohort_evidence.kind}
        if joint_scopes and cohort_evidence is not None
        else set()
    )
    cohort_statuses = (
        {cohort_evidence.status.value}
        if joint_scopes and cohort_evidence is not None
        else set()
    )
    cohort_years = (
        {cohort_evidence.year}
        if joint_scopes and cohort_evidence is not None
        else set()
    )
    estimate, usable = _school_estimate(profile, anchors, research_year)
    school_years: tuple[int, ...] = ()
    school_reasons: tuple[str, ...] = ()
    school_confidence: str | None = None
    if estimate is not None:
        school_years = estimate.contributing_years
        school_reasons = estimate.reasons
        school_confidence = (
            estimate.confidence
            if estimate.confidence in {"high", "medium", "low"}
            else "medium"
        )
        status_order = {
            EvidenceStatus.REFERENCE: 1,
            EvidenceStatus.CORROBORATED: 2,
            EvidenceStatus.OFFICIAL: 3,
        }
        anchor_status = min(
            (item.evidence_status for item in usable),
            key=lambda item: status_order[item],
        )
        intervals.append(
            _RankInterval(
                kind="school_anchor",
                year=max(estimate.contributing_years),
                lower_rank=estimate.lower_rank,
                central_rank=estimate.median_rank,
                upper_rank=estimate.upper_rank,
                source_ids=estimate.contributing_source_ids,
                status=anchor_status,
            )
        )
    if not intervals:
        return None
    ordered = tuple(sorted(intervals, key=lambda item: (item.kind, item.year)))
    lower = max(item.lower_rank for item in ordered)
    upper = min(item.upper_rank for item in ordered)
    if lower > upper:
        profile_kinds = (
            set(profile_reported.channel_kinds)
            if profile_reported is not None and profile_included
            else set()
        )
        profile_statuses = (
            set(profile_reported.channel_statuses)
            if profile_reported is not None and profile_included
            else set()
        )
        return RankScenario._create(
            status=EvidenceStatus.CONFLICT,
            basis="conflicting_authenticated_channels",
            optimistic_rank=None,
            central_rank=None,
            conservative_rank=None,
            confidence="none",
            source_ids=tuple(
                sorted(
                    {
                        source
                        for item in ordered
                        for source in item.source_ids
                    }
                    | cohort_sources
                )
            ),
            contributing_years=tuple(
                sorted(
                    {item.year for item in ordered}
                    | set(school_years)
                    | cohort_years
                )
            ),
            backtest_error=None,
            reasons=tuple(
                sorted({
                    "authenticated_channel_interval_conflict",
                    *profile_reasons,
                    *school_reasons,
                })
            ),
            channel_kinds=tuple(
                sorted(
                    {item.kind for item in ordered}
                    | profile_kinds
                    | cohort_kinds
                )
            ),
            channel_statuses=tuple(
                sorted(
                    {item.status.value for item in ordered}
                    | profile_statuses
                    | cohort_statuses
                )
            ),
            rejected_channel_count=rejected,
        )
    central = int(median(item.central_rank for item in ordered))
    central = min(upper, max(lower, central))
    exact_official = any(
        item.status is EvidenceStatus.OFFICIAL
        and item.kind == "official_score_table"
        and item.lower_rank == item.central_rank == item.upper_rank == central
        for item in ordered
    )
    profile_only = bool(
        profile_reported is not None
        and all(
            item.kind
            in {
                "profile_reported_rank",
                "profile_reported_score",
                "official_score_table",
                "score_table_reference",
            }
            for item in ordered
        )
    )
    profile_kinds = (
        set(profile_reported.channel_kinds)
        if profile_reported is not None and profile_included
        else set()
    )
    profile_statuses = (
        set(profile_reported.channel_statuses)
        if profile_reported is not None and profile_included
        else set()
    )
    confidence = "high" if lower == upper else "medium"
    if profile_reported is not None and profile_reported.confidence == "low":
        confidence = "low"
    if "city_joint" in joint_scopes:
        confidence = "low"
    elif "province_joint" in joint_scopes and confidence == "high":
        confidence = "medium"
    if school_confidence is not None:
        if len(ordered) == 1 and ordered[0].kind == "school_anchor":
            confidence = school_confidence
        elif school_confidence == "low":
            confidence = "low"
    return RankScenario._create(
        status=(
            EvidenceStatus.OFFICIAL
            if lower == upper == central and exact_official
            else EvidenceStatus.INFERRED
        ),
        basis=(
            profile_reported.basis
            if profile_only
            else "authenticated_interval_intersection"
        ),
        optimistic_rank=lower,
        central_rank=central,
        conservative_rank=upper,
        confidence=confidence,
        source_ids=tuple(
            sorted(
                {source for item in ordered for source in item.source_ids}
                | cohort_sources
            )
        ),
        contributing_years=tuple(
            sorted(
                {item.year for item in ordered}
                | set(school_years)
                | cohort_years
            )
        ),
        backtest_error=(
            profile_reported.backtest_error
            if profile_reported is not None and profile_included
            else None
        ),
        reasons=tuple(
            sorted({
                "authenticated_interval_intersection",
                *profile_reasons,
                *school_reasons,
            })
        ),
        channel_kinds=tuple(
            sorted(
                {item.kind for item in ordered}
                | profile_kinds
                | cohort_kinds
            )
        ),
        channel_statuses=tuple(
            sorted(
                {item.status.value for item in ordered}
                | profile_statuses
                | cohort_statuses
            )
        ),
        rejected_channel_count=rejected,
    )


def _weighted_median(
    channels: tuple[_Channel, ...],
    weights: tuple[float, ...],
    name: str,
) -> float:
    ordered = sorted(
        zip(channels, weights),
        key=lambda pair: (getattr(pair[0], name), pair[0].channel_id),
    )
    threshold = sum(weights) / 2
    running = 0.0
    for channel, weight in ordered:
        running += weight
        if running >= threshold:
            return float(getattr(channel, name))
    return float(getattr(ordered[-1][0], name))


def _weights(
    channels: tuple[_Channel, ...],
    target_year: int,
    cohort: int,
) -> tuple[tuple[float, ...], bool]:
    tested_errors = tuple(
        item.backtest_error
        for item in channels
        if item.backtest_error is not None
    )
    floor = max(1 / cohort, float(median(tested_errors)) if tested_errors else 0.02)
    tested: list[float] = []
    untested: list[float] = []
    for item in channels:
        recency = 0.5 ** (max(0, target_year - item.year) / 2)
        error = max(item.backtest_error if item.backtest_error is not None else floor, floor)
        weight = item.coverage * item.comparability * recency / (error * error)
        (untested if item.backtest_error is None else tested).append(weight)
    if not untested:
        return tuple(tested), False
    # Rebuild in original order after capping all untested channels to at most
    # one quarter of the final combined weight.
    tested_total = sum(tested)
    untested_total = sum(untested)
    cap_total = tested_total / 3 if tested_total > 0 else untested_total
    scale = min(1.0, cap_total / untested_total) if untested_total else 1.0
    result: list[float] = []
    for item in channels:
        recency = 0.5 ** (max(0, target_year - item.year) / 2)
        error = max(item.backtest_error if item.backtest_error is not None else floor, floor)
        weight = item.coverage * item.comparability * recency / (error * error)
        result.append(weight if item.backtest_error is not None else weight * scale)
    return tuple(result), True


def _volatility(profile: PlanningProfile) -> float:
    percentiles = tuple(
        item.rank / item.cohort_size
        for item in profile.rank_observations
        if item.rank is not None and item.cohort_size is not None
    )
    if len(percentiles) < 2:
        return 0.0
    return (max(percentiles) - min(percentiles)) / 2


def _locate_rank_core(
    profile: PlanningProfile,
    *,
    evidence_facts: Iterable[Any] = (),
    score_rows: Iterable[ValidatedScoreRow] = (),
    anchors: Iterable[RankAnchor] = (),
    score_subject_group: str | None = None,
    research_snapshot: Any = None,
) -> RankScenario:
    """Return an official or explicitly inferred rank scenario."""

    if not isinstance(profile, PlanningProfile):
        raise TypeError("profile must be a PlanningProfile")
    authenticated = False
    research_year = profile.exam_year
    provincial_cohorts: tuple[int, ...] = ()
    provincial_cohort_years: tuple[int, ...] = ()
    provincial_cohort_by_year: dict[int, int] = {}
    cohort_evidence_by_year: dict[int, _ProvincialCohortEvidence] = {}
    if research_snapshot is not None:
        if tuple(evidence_facts) or tuple(score_rows) or tuple(anchors):
            raise ValueError("research_snapshot cannot be mixed with legacy rank inputs")
        if score_subject_group is not None:
            raise ValueError("research_snapshot owns the canonical score subject")
        if __package__:
            from .research_snapshot import validate_research_snapshot
        else:  # pragma: no cover
            from research_snapshot import validate_research_snapshot  # type: ignore
        snapshot = validate_research_snapshot(research_snapshot, profile)
        research_year = snapshot.research_year
        evidence_facts = snapshot.rank_facts
        score_rows = snapshot.score_rows
        anchors = ()
        if snapshot.score_rows:
            score_subject_group = snapshot.score_rows[0].to_dict()["subject_group"]
        elif snapshot.rank_facts:
            score_subject_group = snapshot.rank_facts[0]["value"].get("subject_group")
        for fact in snapshot.rank_facts:
            value = fact["value"]
            if value.get("kind") not in {
                "official_score_table",
                "score_table_reference",
            }:
                continue
            # The PDF text-table adapter selects an explicit page/line region.
            # Its last cumulative count is a regional coverage boundary, not
            # evidence of the total number of provincial candidates. The same
            # exact row remains available below for an official score lookup.
            if value["input_projection"]["extraction_method"] == "pdf-text-table":
                continue
            fact_status = EvidenceStatus(fact["status"])
            coverage_status = EvidenceStatus(value["coverage_status"])
            if fact_status not in _ACCEPTED or coverage_status not in _ACCEPTED:
                continue
            year = int(value["year"])
            effective_status = min(
                (fact_status, coverage_status),
                key=lambda item: _STATUS_RELIABILITY[item],
            )
            candidate_cohort = _ProvincialCohortEvidence(
                cohort=int(value["coverage_max_rank"]),
                year=year,
                source_ids=tuple(fact["source_ids"]),
                status=effective_status,
                kind=str(value["kind"]),
            )
            previous_cohort = cohort_evidence_by_year.get(year)
            if previous_cohort is None or (
                candidate_cohort.cohort,
                _STATUS_RELIABILITY[candidate_cohort.status],
                candidate_cohort.source_ids,
            ) > (
                previous_cohort.cohort,
                _STATUS_RELIABILITY[previous_cohort.status],
                previous_cohort.source_ids,
            ):
                cohort_evidence_by_year[year] = candidate_cohort
        provincial_cohort_by_year = {
            year: item.cohort for year, item in cohort_evidence_by_year.items()
        }
        provincial_cohort_years = tuple(
            sorted(provincial_cohort_by_year, reverse=True)
        )
        provincial_cohorts = tuple(
            provincial_cohort_by_year[year] for year in provincial_cohort_years
        )
        authenticated = True
    rows = _matching_score_rows(
        profile, score_rows, score_subject_group, research_year
    )
    score_evidence: dict[tuple[int, int], _ScoreTableEvidence] | None = None
    if authenticated:
        score_evidence = {}
        for fact in snapshot.rank_facts:
            value = fact["value"]
            if value.get("kind") not in {
                "official_score_table",
                "score_table_reference",
            }:
                continue
            fact_status = EvidenceStatus(fact["status"])
            coverage_status = EvidenceStatus(value["coverage_status"])
            if fact_status not in _ACCEPTED or coverage_status not in _ACCEPTED:
                continue
            effective_status = min(
                (fact_status, coverage_status),
                key=lambda item: _STATUS_RELIABILITY[item],
            )
            score_evidence[(int(value["year"]), int(value["score"]))] = (
                _ScoreTableEvidence(
                    source_ids=tuple(fact["source_ids"]),
                    status=effective_status,
                    kind=str(value["kind"]),
                )
            )
    cohort_years, cohorts = _cohort_context(
        profile, score_rows, score_subject_group, research_year
    )
    provincial_cohort = (
        provincial_cohort_by_year.get(research_year)
        or (
            provincial_cohort_by_year[provincial_cohort_years[0]]
            if provincial_cohort_years
            else None
        )
        if authenticated
        else (cohorts[0] if cohorts else None)
    )
    cohort_evidence = (
        cohort_evidence_by_year.get(research_year)
        or (
            cohort_evidence_by_year[provincial_cohort_years[0]]
            if provincial_cohort_years
            else None
        )
        if authenticated
        else None
    )
    profile_reported = _profile_reported_scenario(
        profile,
        rows,
        score_evidence,
        research_year if authenticated else None,
        provincial_cohort,
        cohort_evidence,
    )
    if profile_reported is not None and not authenticated:
        return profile_reported
    channels: list[_Channel] = []
    authenticated_anchors: list[RankAnchor] = []
    for anchor in anchors:
        if not isinstance(anchor, RankAnchor):
            raise TypeError("anchors must contain RankAnchor records")
        authenticated_anchors.append(anchor)
    rejected = 0
    for fact in evidence_facts:
        try:
            raw = _fact_mapping(fact)
            field = raw.get("field")
            value = raw.get("value")
            if (
                authenticated
                and isinstance(value, Mapping)
                and value.get("kind")
                in {"official_score_table", "score_table_reference"}
            ):
                continue
            if isinstance(field, str) and field.startswith("rank_anchor:"):
                authenticated_anchors.append(
                    _fact_anchor(
                        profile,
                        raw,
                        subject_group=score_subject_group,
                        authenticated=authenticated,
                    )
                )
            else:
                channels.append(
                    _fact_channel(
                        profile,
                        raw,
                        subject_group=score_subject_group,
                        authenticated=authenticated,
                        research_year=research_year,
                    )
                )
        except (TypeError, ValueError):
            rejected += 1
    if authenticated:
        bounded = _authenticated_interval_scenario(
            profile_reported,
            _profile_reported_intervals(
                profile,
                rows,
                score_evidence or {},
                profile_reported,
            ),
            channels,
            profile,
            authenticated_anchors,
            rejected,
            research_year,
            provincial_cohort,
            cohort_evidence,
        )
        if bounded is not None:
            return bounded
    if authenticated:
        # Never reconstruct an excluded cohort from the snapshot's individual
        # score rows: that would reintroduce a partial PDF's last row as a total.
        cohorts = provincial_cohorts
        cohort_years = provincial_cohort_years
    if authenticated and not provincial_cohorts:
        absolute_school = _absolute_school_scenario(
            profile, authenticated_anchors, rejected
        )
        if absolute_school is not None:
            return absolute_school
    if not cohorts:
        return _missing(("official_cohort_size_missing",), rejected)
    school, school_years, school_reasons = _school_channel(
        profile,
        authenticated_anchors,
        provincial_cohorts if authenticated else cohorts,
    )
    if school is not None:
        channels.append(school)
    if not channels:
        return _missing(("calibration_evidence_missing",), rejected)
    ordered = tuple(sorted(channels, key=lambda item: item.channel_id))
    if authenticated and any(
        left.upper_percentile < right.lower_percentile
        or right.upper_percentile < left.lower_percentile
        for index, left in enumerate(ordered)
        for right in ordered[index + 1 :]
    ):
        return _conflict(ordered, rejected)
    central_cohort = _integer_median(cohorts)
    weights, capped = _weights(ordered, research_year, central_cohort)
    lower = _weighted_median(ordered, weights, "lower_percentile")
    central = _weighted_median(ordered, weights, "central_percentile")
    upper = _weighted_median(ordered, weights, "upper_percentile")
    volatility = _volatility(profile)
    lower = max(0.0, lower - volatility)
    upper = min(1.0, upper + volatility)
    if lower > central:
        lower = central
    if upper < central:
        upper = central
    optimistic = max(1, math.ceil(lower * min(cohorts)))
    central_rank = max(1, math.ceil(central * central_cohort))
    conservative = max(1, math.ceil(upper * max(cohorts)))
    optimistic = min(optimistic, central_rank)
    conservative = max(conservative, central_rank)
    errors = tuple(
        item.backtest_error
        for item in ordered
        if item.backtest_error is not None
    )
    reasons = ["deterministic_weighted_median"]
    reasons.extend(school_reasons)
    if capped:
        reasons.append("untested_weight_capped")
    if volatility:
        reasons.append("recent_exam_volatility_applied")
    confidence = "low" if capped or len(ordered) == 1 else "medium"
    basis = (
        "school_anchor_ensemble"
        if len(ordered) == 1 and school is not None
        else "multi_channel_ensemble"
    )
    return RankScenario._create(
        status=EvidenceStatus.INFERRED,
        basis=basis,
        optimistic_rank=optimistic,
        central_rank=central_rank,
        conservative_rank=conservative,
        confidence=confidence,
        source_ids=tuple(sorted({source for item in ordered for source in item.source_ids})),
        contributing_years=tuple(
            sorted({item.year for item in ordered} | set(school_years))
        ),
        backtest_error=float(median(errors)) if errors else None,
        reasons=tuple(sorted(reasons)),
        channel_kinds=tuple(sorted({item.kind for item in ordered})),
        channel_statuses=tuple(sorted({item.status.value for item in ordered})),
        rejected_channel_count=rejected,
    )


def _locate_rank_legacy(
    profile: PlanningProfile,
    *,
    evidence_facts: Iterable[Any],
    score_rows: Iterable[ValidatedScoreRow],
    anchors: Iterable[RankAnchor] = (),
    score_subject_group: str | None = None,
) -> RankScenario:
    """Private compatibility seam for the pre-snapshot report pipeline."""

    return _locate_rank_core(
        profile,
        evidence_facts=evidence_facts,
        score_rows=score_rows,
        anchors=anchors,
        score_subject_group=score_subject_group,
    )


def locate_rank(
    profile: PlanningProfile,
    *,
    research_snapshot: Any,
) -> RankScenario:
    """Locate rank only from an authenticated province research snapshot."""

    return _locate_rank_core(profile, research_snapshot=research_snapshot)


__all__ = ["RankScenario", "locate_rank", "unavailable_rank_scenario"]
