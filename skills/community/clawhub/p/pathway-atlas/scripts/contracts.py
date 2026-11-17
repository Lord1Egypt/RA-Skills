"""Host-neutral contracts shared by retrieval and deterministic processing.

The contracts deliberately use only Python 3.10 standard-library features.  A
dataclass's ``to_dict`` method is the serialization seam used by the JSON
schemas and by evidence-bundle writers.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass
from enum import Enum
import re
from collections.abc import Mapping
from types import MappingProxyType
from typing import Any
from uuid import uuid4


class SourceTier(str, Enum):
    """Reliability tier of a source publisher."""

    A = "A"
    B = "B"
    C = "C"


class EvidenceStatus(str, Enum):
    """Status assigned to a normalized fact."""

    OFFICIAL = "official"
    CORROBORATED = "corroborated"
    REFERENCE = "reference"
    INFERRED = "inferred"
    CONFLICT = "conflict"
    MISSING = "missing"
    MASKED = "masked"
    PARTIAL = "partial"


class CapabilityTier(str, Enum):
    """Execution tier selected by the environment preflight."""

    FULL = "full"
    STANDARD = "standard"
    OFFLINE = "offline"


def _json_safe(value: Any) -> Any:
    """Recursively convert contract values to values accepted by ``json``."""

    if isinstance(value, Enum):
        return value.value
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, frozenset):
        if not all(isinstance(item, str) for item in value):
            raise TypeError("frozenset contract values must contain only strings")
        return sorted(value)
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        converted = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError(
                    "Value of type "
                    f"{type(key).__name__} is not a JSON object key"
                )
            converted[key] = _json_safe(item)
        return converted
    if is_dataclass(value) and hasattr(value, "to_dict"):
        return _json_safe(value.to_dict())
    raise TypeError(
        f"Value of type {type(value).__name__} is not JSON serializable"
    )


class _Serializable:
    """Mixin implementing stable recursive dataclass serialization."""

    def to_dict(self) -> dict[str, Any]:
        return {
            item.name: _json_safe(getattr(self, item.name))
            for item in fields(self)
        }


@dataclass(frozen=True)
class SourceCandidate(_Serializable):
    source_id: str
    url: str
    publisher: str
    tier: SourceTier
    published_at: str | None
    retrieved_at: str
    content_hash: str
    citation_root: str
    summary: str


@dataclass(frozen=True)
class FactClaim(_Serializable):
    field: str
    value: Any
    unit: str | None
    source_id: str
    method: str


@dataclass(frozen=True)
class EvidenceFact(_Serializable):
    fact_id: str
    field: str
    value: Any
    unit: str | None
    status: EvidenceStatus
    source_ids: tuple[str, ...]
    method: str
    notes: str


@dataclass(frozen=True)
class CapabilityReport(_Serializable):
    """Machine-readable result of host capability preflight.

    The optional tuple fields intentionally default to empty tuples so a
    caller can construct a minimal report for an offline run while preserving
    one stable serialized shape for all tiers.
    """

    tier: CapabilityTier
    host_capabilities: tuple[str, ...] = ()
    available_capabilities: tuple[str, ...] = ()
    missing_capabilities: tuple[str, ...] = ()
    degradations: tuple[str, ...] = ()
    python_version: str = ""
    optional_modules: tuple[str, ...] = ()


@dataclass(frozen=True)
class EvidenceManifest(_Serializable):
    """Index for one reproducible evidence bundle."""

    schema_version: str = "1.0"
    session_id: str = field(default_factory=lambda: uuid4().hex)
    capability_tier: CapabilityTier = CapabilityTier.OFFLINE
    candidates_filename: str = "candidates.jsonl"
    facts_filename: str = "facts.jsonl"
    rejected_count: int = 0
    manifest_hash: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.session_id, str) or re.fullmatch(
            r"[0-9a-f]{32}", self.session_id
        ) is None:
            raise ValueError("session_id must be lower-case UUID hex")
        if self.manifest_hash != "" and (
            not isinstance(self.manifest_hash, str)
            or re.fullmatch(r"sha256:[0-9a-f]{64}", self.manifest_hash) is None
        ):
            raise ValueError("manifest_hash must be a lower-case SHA-256 identifier")


@dataclass(frozen=True)
class RecommendationProfile(_Serializable):
    """Normalized, privacy-minimal inputs for ordinary-batch matching."""

    rank: int
    target_province: str
    subject_group: str = ""
    secondary_subjects: frozenset[str] = field(default_factory=frozenset)
    target_major_categories: tuple[str, ...] = ()
    target_cities: tuple[str, ...] = ()
    target_schools: tuple[str, ...] = ()
    rank_basis: str = "official"
    optimistic_rank: int | None = None
    conservative_rank: int | None = None
    rank_confidence: str = "official"
    rank_source_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.rank, int) or isinstance(self.rank, bool):
            raise TypeError("rank must be a positive integer")
        if self.rank < 1:
            raise ValueError("rank must be a positive integer")
        optimistic = self.rank if self.optimistic_rank is None else self.optimistic_rank
        conservative = (
            self.rank if self.conservative_rank is None else self.conservative_rank
        )
        for name, value in (
            ("optimistic_rank", optimistic),
            ("conservative_rank", conservative),
        ):
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                raise TypeError(f"{name} must be a positive integer")
        if not optimistic <= self.rank <= conservative:
            raise ValueError("rank scenario bounds must contain rank")
        object.__setattr__(self, "optimistic_rank", optimistic)
        object.__setattr__(self, "conservative_rank", conservative)
        if self.rank_basis not in {"official", "inferred"}:
            raise ValueError("rank_basis must be official or inferred")
        allowed_confidence = (
            {"official", "high"}
            if self.rank_basis == "official"
            else {"high", "medium", "low"}
        )
        if self.rank_confidence not in allowed_confidence:
            raise ValueError("rank_confidence does not match rank_basis")
        sources = self._normalize_collection(self.rank_source_ids, "rank_source_ids")
        if len(sources) != len(set(sources)) or any(
            _SAFE_ID.fullmatch(source) is None for source in sources
        ):
            raise ValueError("rank_source_ids must contain unique safe IDs")
        if self.rank_basis == "inferred" and not sources:
            raise ValueError("inferred ranks require source IDs")
        object.__setattr__(self, "rank_source_ids", tuple(sorted(sources)))
        for name in ("target_province", "subject_group"):
            value = getattr(self, name)
            if not isinstance(value, str):
                raise TypeError(f"{name} must be a non-empty string")
            normalized = value.strip()
            if not normalized:
                raise ValueError(f"{name} must be a non-empty string")
            object.__setattr__(self, name, normalized)

        subjects = self._normalize_collection(
            self.secondary_subjects, "secondary_subjects"
        )
        object.__setattr__(self, "secondary_subjects", frozenset(subjects))
        for name in ("target_major_categories", "target_cities", "target_schools"):
            object.__setattr__(
                self, name, self._normalize_collection(getattr(self, name), name)
            )

    @staticmethod
    def _normalize_collection(value: Any, name: str) -> tuple[str, ...]:
        if isinstance(value, (str, bytes, bytearray)):
            raise TypeError(f"{name} must be a collection of strings")
        try:
            items = tuple(value)
        except TypeError as error:
            raise TypeError(f"{name} must be a collection of strings") from error
        normalized: list[str] = []
        for item in items:
            if not isinstance(item, str):
                raise TypeError(f"{name} must contain only strings")
            stripped = item.strip()
            if not stripped:
                raise ValueError(f"{name} must not contain empty strings")
            normalized.append(stripped)
        return tuple(normalized)


_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_PUBLIC_VERSION = re.compile(r"^[0-9]+\.[0-9]+(?:\.[0-9]+)?$")


@dataclass(frozen=True, init=False)
class DecisionRuleBasis(_Serializable):
    """Auditable origin for project decision parameters."""

    basis_id: str
    source_id: str
    source_version: str

    def __init__(self) -> None:
        raise TypeError("DecisionRuleBasis is factory-only")

    @classmethod
    def create(
        cls, *, basis_id: str, source_id: str, source_version: str
    ) -> "DecisionRuleBasis":
        for name, value in (("basis_id", basis_id), ("source_id", source_id)):
            if not isinstance(value, str) or _SAFE_ID.fullmatch(value) is None:
                raise ValueError(f"{name} must use the public safe-ID syntax")
        if not isinstance(source_version, str) or _PUBLIC_VERSION.fullmatch(source_version) is None:
            raise ValueError("source_version must be a public numeric version")
        instance = object.__new__(cls)
        object.__setattr__(instance, "basis_id", basis_id)
        object.__setattr__(instance, "source_id", source_id)
        object.__setattr__(instance, "source_version", source_version)
        return instance


@dataclass(frozen=True, init=False)
class SourcePolicyReference(_Serializable):
    """Pointer to the one executable source-admission policy.

    Thresholds deliberately do not live in this record.  Query consumers must
    call ``scripts.source_policy`` so A/B/C admission and conflicts cannot
    drift into a second implementation.
    """

    policy_id: str
    version: str

    def __init__(self) -> None:
        raise TypeError("SourcePolicyReference is factory-only")

    @classmethod
    def create(cls, *, policy_id: str, version: str) -> "SourcePolicyReference":
        if not isinstance(policy_id, str) or _SAFE_ID.fullmatch(policy_id) is None:
            raise ValueError("policy_id must use the public safe-ID syntax")
        if not isinstance(version, str) or _PUBLIC_VERSION.fullmatch(version) is None:
            raise ValueError("version must be a public numeric version")
        instance = object.__new__(cls)
        object.__setattr__(instance, "policy_id", policy_id)
        object.__setattr__(instance, "version", version)
        return instance


@dataclass(frozen=True)
class OrdinaryBatchPolicy(_Serializable):
    """Immutable, versioned parameters for one province ordinary-batch run."""

    schema_version: str
    policy_id: str
    basis_id: str
    search_delta_min: int
    search_delta_max: int
    challenge_delta_lt: int
    stable_delta_le: int
    tier_caps: Mapping[str, int]

    def __post_init__(self) -> None:
        if self.schema_version != "1.0":
            raise ValueError("ordinary batch policy schema_version must be 1.0")
        for name in ("policy_id", "basis_id"):
            value = getattr(self, name)
            if not isinstance(value, str) or _SAFE_ID.fullmatch(value) is None:
                raise ValueError(f"{name} must use the public safe-ID syntax")
        for name in (
            "search_delta_min",
            "search_delta_max",
            "challenge_delta_lt",
            "stable_delta_le",
        ):
            value = getattr(self, name)
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError(f"{name} must be an integer")
        if not (
            self.search_delta_min
            <= self.challenge_delta_lt
            <= self.stable_delta_le
            <= self.search_delta_max
        ):
            raise ValueError("ordinary batch policy thresholds are out of order")
        if not isinstance(self.tier_caps, Mapping) or set(self.tier_caps) != {"冲", "稳", "保"}:
            raise ValueError("tier_caps must contain exactly 冲, 稳, 保")
        caps: dict[str, int] = {}
        for tier in ("冲", "稳", "保"):
            cap = self.tier_caps[tier]
            if not isinstance(cap, int) or isinstance(cap, bool) or cap <= 0:
                raise ValueError("tier caps must be positive integers")
            caps[tier] = cap
        object.__setattr__(self, "tier_caps", MappingProxyType(caps))

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "policy_id": self.policy_id,
            "basis_id": self.basis_id,
            "search_delta_min": self.search_delta_min,
            "search_delta_max": self.search_delta_max,
            "challenge_delta_lt": self.challenge_delta_lt,
            "stable_delta_le": self.stable_delta_le,
            "tier_caps": dict(self.tier_caps),
        }


@dataclass(frozen=True)
class RecommendationMajorGroup(_Serializable):
    major_group_name: str
    major_group_code: str
    min_score: int
    min_rank: int
    majors: str


@dataclass(frozen=True)
class RecommendationItem(_Serializable):
    """One deterministic school recommendation with field-level provenance."""

    school_name: str
    school_level: str
    city: str
    school_province: str
    province_match: bool
    subject_match: bool
    min_score: int
    min_rank: int
    delta: int
    related_majors: str
    remarks: str
    major_groups: tuple[RecommendationMajorGroup, ...]
    match_reason: str
    recommend_level: str
    strategy: str
    data_year: int
    source_ids: tuple[str, ...]
    evidence_status: EvidenceStatus
    supporting_years: tuple[int, ...] = ()
    required_year_majority: int = 1
    scenario_reach_counts: tuple[int, int, int] = (0, 0, 0)
    scenario_confidence: str = "official"
    fit_evidence_statuses: tuple[EvidenceStatus, ...] = ()


@dataclass(frozen=True)
class SchoolObservation(_Serializable):
    """A source-bound school lead that is intentionally non-numeric.

    Partial admission rows remain observations even when their declared range
    includes the student's rank. The separate contract prevents partial-row
    numbers from leaking into a 冲稳保 label.
    """

    school_name: str
    school_level: str
    city: str
    data_year: int
    source_ids: tuple[str, ...]
    evidence_status: EvidenceStatus
    reason_code: str

    def __post_init__(self) -> None:
        if not isinstance(self.school_name, str) or not self.school_name.strip():
            raise ValueError("school observations require a school name")
        object.__setattr__(self, "school_name", self.school_name.strip())
        for name in ("school_level", "city"):
            value = getattr(self, name)
            if not isinstance(value, str):
                raise TypeError(f"{name} must be text")
            object.__setattr__(self, name, value.strip())
        if (
            not isinstance(self.data_year, int)
            or isinstance(self.data_year, bool)
            or not 2000 <= self.data_year <= 2100
        ):
            raise ValueError("school observation data_year is invalid")
        sources = tuple(self.source_ids)
        if not sources or len(sources) != len(set(sources)) or any(
            not isinstance(source, str) or _SAFE_ID.fullmatch(source) is None
            for source in sources
        ):
            raise ValueError("school observations require unique public source IDs")
        object.__setattr__(self, "source_ids", tuple(sorted(sources)))
        try:
            status = EvidenceStatus(self.evidence_status)
        except (TypeError, ValueError) as error:
            raise ValueError("school observation evidence status is invalid") from error
        if status is not EvidenceStatus.PARTIAL:
            raise ValueError("school observations must be explicitly partial")
        object.__setattr__(self, "evidence_status", status)
        if (
            not isinstance(self.reason_code, str)
            or _SAFE_ID.fullmatch(self.reason_code) is None
        ):
            raise ValueError("school observation reason_code must be a public safe ID")


@dataclass(frozen=True)
class RecommendationResult(_Serializable):
    """Immutable school-matching result with explicit evidence coverage."""

    ordinary_batch_policy: OrdinaryBatchPolicy
    items: tuple[RecommendationItem, ...] = ()
    observations: tuple[SchoolObservation, ...] = ()
    excluded_by_subject_count: int = 0
    zero_score_excluded_count: int = 0
    input_years: tuple[int, ...] = ()
    usable_years: tuple[int, ...] = ()
    verified_rank_coverage: tuple[int, int] | None = None
    coverage_status: EvidenceStatus = EvidenceStatus.MISSING
    empty_reason: str | None = None
    warnings: tuple[str, ...] = ()
    rank_basis: str = "official"
    rank_bounds: tuple[int, int, int] | None = None
    rank_confidence: str = "official"
    rank_source_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.ordinary_batch_policy, OrdinaryBatchPolicy):
            raise TypeError("ordinary_batch_policy must be an OrdinaryBatchPolicy")
        if self.rank_basis not in {"official", "inferred"}:
            raise ValueError("rank_basis must be official or inferred")
        allowed_confidence = (
            {"official", "high"}
            if self.rank_basis == "official"
            else {"high", "medium", "low"}
        )
        if self.rank_confidence not in allowed_confidence:
            raise ValueError("rank_confidence does not match rank_basis")
        if self.rank_bounds is not None:
            if (
                not isinstance(self.rank_bounds, tuple)
                or len(self.rank_bounds) != 3
                or any(
                    not isinstance(rank, int)
                    or isinstance(rank, bool)
                    or rank < 1
                    for rank in self.rank_bounds
                )
                or not self.rank_bounds[0] <= self.rank_bounds[1] <= self.rank_bounds[2]
            ):
                raise ValueError("rank_bounds must be three ordered positive integers")
        sources = tuple(self.rank_source_ids)
        if len(sources) != len(set(sources)) or any(
            not isinstance(source, str) or _SAFE_ID.fullmatch(source) is None
            for source in sources
        ):
            raise ValueError("rank_source_ids must contain unique safe IDs")
        if self.rank_basis == "inferred" and not sources:
            raise ValueError("inferred ranks require source IDs")
        object.__setattr__(
            self,
            "ordinary_batch_policy",
            OrdinaryBatchPolicy(**self.ordinary_batch_policy.to_dict()),
        )
        items = tuple(self.items)
        if not all(isinstance(item, RecommendationItem) for item in items):
            raise TypeError("items must contain RecommendationItem records")
        allowed_numeric_statuses = {
            EvidenceStatus.OFFICIAL,
            EvidenceStatus.CORROBORATED,
            EvidenceStatus.REFERENCE,
        }
        if any(item.evidence_status not in allowed_numeric_statuses for item in items):
            raise ValueError("numeric recommendations require accepted exact evidence")
        observations = tuple(self.observations)
        if not all(isinstance(item, SchoolObservation) for item in observations):
            raise TypeError("observations must contain SchoolObservation records")
        observation_keys = tuple(
            (item.school_name, item.data_year, item.source_ids)
            for item in observations
        )
        if len(observation_keys) != len(set(observation_keys)):
            raise ValueError("school observations must be unique")
        try:
            coverage_status = EvidenceStatus(self.coverage_status)
        except (TypeError, ValueError) as error:
            raise ValueError("coverage_status is invalid") from error
        verified_coverage = self.verified_rank_coverage
        if verified_coverage is not None:
            if (
                not isinstance(verified_coverage, (tuple, list))
                or len(verified_coverage) != 2
                or any(
                    not isinstance(value, int)
                    or isinstance(value, bool)
                    or value < 1
                    for value in verified_coverage
                )
                or verified_coverage[0] > verified_coverage[1]
            ):
                raise ValueError("verified_rank_coverage must be an ordered positive pair")
            verified_coverage = tuple(verified_coverage)
            object.__setattr__(self, "verified_rank_coverage", verified_coverage)
        if observations and coverage_status in {
            EvidenceStatus.OFFICIAL,
            EvidenceStatus.CORROBORATED,
            EvidenceStatus.REFERENCE,
        }:
            raise ValueError("partial observations require degraded aggregate coverage")
        if observations and not items and self.empty_reason not in {
            "partial_observations_only",
            "rank_outside_verified_coverage",
        }:
            raise ValueError("observation-only results require a stable empty reason")
        if self.empty_reason == "partial_observations_only" and not observations:
            raise ValueError("partial observation reason requires observations")
        if self.empty_reason == "rank_outside_verified_coverage":
            if verified_coverage is None or self.rank_bounds is None:
                raise ValueError("outside-coverage reason requires rank bounds and coverage")
            lower, upper = verified_coverage
            if lower <= self.rank_bounds[0] and self.rank_bounds[2] <= upper:
                raise ValueError("outside-coverage reason contradicts rank bounds")
        object.__setattr__(self, "items", items)
        object.__setattr__(self, "observations", observations)
        object.__setattr__(self, "coverage_status", coverage_status)
        object.__setattr__(self, "warnings", tuple(self.warnings))
        object.__setattr__(self, "rank_source_ids", tuple(sorted(sources)))


__all__ = [
    "CapabilityReport",
    "CapabilityTier",
    "DecisionRuleBasis",
    "EvidenceFact",
    "EvidenceManifest",
    "EvidenceStatus",
    "FactClaim",
    "OrdinaryBatchPolicy",
    "RecommendationItem",
    "RecommendationMajorGroup",
    "RecommendationProfile",
    "RecommendationResult",
    "SchoolObservation",
    "SourceCandidate",
    "SourcePolicyReference",
    "SourceTier",
]
