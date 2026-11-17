"""Versioned, non-official project planning rules.

This module owns calculation choices only.  Evidence admission remains solely
in :mod:`scripts.source_policy`; the snapshot carries a reference, never a
copy of A/B/C thresholds or conflict arithmetic.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
import re
from types import MappingProxyType
from typing import Any

if __package__:
    from .contracts import DecisionRuleBasis, EvidenceStatus, SourcePolicyReference
else:  # pragma: no cover - flat import compatibility
    from contracts import DecisionRuleBasis, EvidenceStatus, SourcePolicyReference


_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_SCHEMA_VERSION = "1.0"
_PATHWAY_REASON_ORDER = (
    "eligibility",
    "academic_fit",
    "interest_fit",
    "readiness",
    "urgency",
    "burden",
    "strategic_value",
    "evidence_quality",
)
_ACTION_PRIORITY_ORDER = (
    "known_deadline",
    "blocking_dependency",
    "long_lead_strategic_value",
    "uncertainty_reduction",
    "phase_effort_stable_id",
)
_DECISION_DIMENSIONS = frozenset(_PATHWAY_REASON_ORDER)
_DECISION_EFFECTS = frozenset({"supports", "blocks", "uncertain"})
_DECISION_REASON_DEFINITIONS = MappingProxyType(
    {
        "SCHOOL_RANK_CHALLENGE": (
            "academic_fit",
            "supports",
            ("province",),
        ),
        "SCHOOL_RANK_STABLE": (
            "academic_fit",
            "supports",
            ("province",),
        ),
        "SCHOOL_RANK_SAFE": (
            "academic_fit",
            "supports",
            ("province",),
        ),
        "SCHOOL_RANK_OBSERVE": (
            "academic_fit",
            "uncertain",
            ("province",),
        ),
        "SCHOOL_RANK_OUTSIDE_INTERVAL": (
            "academic_fit",
            "blocks",
            ("province",),
        ),
        "SCHOOL_SUBJECT_MATCH": (
            "academic_fit",
            "supports",
            ("subject_group", "secondary_subjects"),
        ),
        "SCHOOL_SUBJECT_MISMATCH": (
            "academic_fit",
            "blocks",
            ("subject_group", "secondary_subjects"),
        ),
        "SCHOOL_SUBJECT_UNVERIFIED": (
            "academic_fit",
            "uncertain",
            ("subject_group", "secondary_subjects"),
        ),
        "SCHOOL_PROVINCE_POLICY_MATCH": (
            "academic_fit",
            "supports",
            ("province", "subject_mode", "subject_group"),
        ),
        "SCHOOL_PROVINCE_POLICY_MISMATCH": (
            "academic_fit",
            "uncertain",
            ("province", "subject_mode", "subject_group"),
        ),
        "SCHOOL_PROVINCE_POLICY_UNVERIFIED": (
            "academic_fit",
            "uncertain",
            ("province", "subject_mode", "subject_group"),
        ),
        "SCHOOL_TARGET_SCHOOL_MATCH": (
            "interest_fit",
            "supports",
            ("priorities.target_schools", "target_school_reasons"),
        ),
        "SCHOOL_TARGET_SCHOOL_COMMITTED": (
            "interest_fit",
            "supports",
            ("priorities.target_schools", "target_school_reasons"),
        ),
        "SCHOOL_TARGET_MAJOR_MATCH": (
            "interest_fit",
            "supports",
            ("priorities.target_majors", "target_major_reasons"),
        ),
        "SCHOOL_TARGET_MAJOR_COMMITTED": (
            "interest_fit",
            "supports",
            ("priorities.target_majors", "target_major_reasons"),
        ),
        "SCHOOL_TARGET_MAJOR_UNVERIFIED": (
            "interest_fit",
            "uncertain",
            ("priorities.target_majors", "target_major_reasons"),
        ),
        "SCHOOL_TARGET_REGION_MATCH": (
            "interest_fit",
            "supports",
            ("priorities.target_regions",),
        ),
        "SCHOOL_LOCAL_CITY_MATCH": (
            "interest_fit",
            "supports",
            ("city",),
        ),
        "SCHOOL_REGION_UNVERIFIED": (
            "interest_fit",
            "uncertain",
            ("priorities.target_regions", "constraints.excluded_regions", "city"),
        ),
        "SCHOOL_EXCLUDED_REGION": (
            "eligibility",
            "blocks",
            ("constraints.excluded_regions",),
        ),
        "SCHOOL_INSTITUTION_TYPE_BLOCKED": (
            "eligibility",
            "blocks",
            ("constraints.institution_types",),
        ),
        "SCHOOL_INSTITUTION_TYPE_UNVERIFIED": (
            "eligibility",
            "uncertain",
            ("constraints.institution_types",),
        ),
        "SCHOOL_INSTITUTION_TYPE_MATCH": (
            "eligibility",
            "supports",
            ("constraints.institution_types",),
        ),
        "SCHOOL_AFFORDABILITY_BLOCKED": (
            "burden",
            "blocks",
            ("constraints.budget_level",),
        ),
        "SCHOOL_AFFORDABILITY_MATCH": (
            "burden",
            "supports",
            ("constraints.budget_level",),
        ),
        "SCHOOL_AFFORDABILITY_UNVERIFIED": (
            "burden",
            "uncertain",
            ("constraints.budget_level",),
        ),
        "SCHOOL_ADJUSTMENT_BLOCKED": (
            "burden",
            "blocks",
            ("constraints.adjustment_preference",),
        ),
        "SCHOOL_ADJUSTMENT_MATCH": (
            "burden",
            "supports",
            ("constraints.adjustment_preference",),
        ),
        "SCHOOL_ADJUSTMENT_UNVERIFIED": (
            "burden",
            "uncertain",
            ("constraints.adjustment_preference",),
        ),
        "SCHOOL_CHARTER_HEALTH_REVIEW_REQUIRED": (
            "eligibility",
            "uncertain",
            ("constraints.health_constraints",),
        ),
        "SCHOOL_CHARTER_HEALTH_UNVERIFIED": (
            "eligibility",
            "uncertain",
            ("constraints.health_constraints",),
        ),
        "SCHOOL_CHARTER_RESTRICTIONS_REVIEW_REQUIRED": (
            "eligibility",
            "uncertain",
            (
                "rank_observations.score",
                "rank_observations.max_score",
                "preparation_assets.english_readiness",
            ),
        ),
        "SCHOOL_CHARTER_RESTRICTIONS_UNVERIFIED": (
            "eligibility",
            "uncertain",
            (
                "rank_observations.score",
                "rank_observations.max_score",
                "preparation_assets.english_readiness",
            ),
        ),
        "SCHOOL_RISK_CAP_EXCLUDED": (
            "strategic_value",
            "blocks",
            ("constraints.risk_preference",),
        ),
        "SCHOOL_EVIDENCE_OFFICIAL": (
            "evidence_quality", "supports", (),
        ),
        "SCHOOL_EVIDENCE_CORROBORATED": (
            "evidence_quality", "supports", (),
        ),
        "SCHOOL_EVIDENCE_REFERENCE": (
            "evidence_quality", "uncertain", (),
        ),
        "SCHOOL_EVIDENCE_PARTIAL": (
            "evidence_quality", "uncertain", (),
        ),
        "SCHOOL_EVIDENCE_UNUSABLE": (
            "evidence_quality", "blocks", (),
        ),
        "PATH_ELIGIBILITY_SATISFIED": (
            "eligibility", "supports", ("gender", "eligibility_facts", "constraints.health_constraints"),
        ),
        "PATH_ELIGIBILITY_REQUIREMENT_MISSING": (
            "eligibility", "uncertain", ("gender", "eligibility_facts", "constraints.health_constraints"),
        ),
        "PATH_ELIGIBILITY_BLOCKED": (
            "eligibility", "blocks", ("gender", "eligibility_facts", "constraints.health_constraints"),
        ),
        "PATH_ACADEMIC_MATCH": (
            "academic_fit",
            "supports",
            ("grade", "subject_group", "secondary_subjects", "preparation_assets.subject_strengths"),
        ),
        "PATH_ACADEMIC_UNVERIFIED": (
            "academic_fit",
            "uncertain",
            ("grade", "subject_group", "secondary_subjects", "preparation_assets.subject_strengths"),
        ),
        "PATH_ACADEMIC_SUBJECT_BLOCKED": (
            "academic_fit",
            "blocks",
            ("grade", "subject_group", "secondary_subjects", "preparation_assets.subject_strengths"),
        ),
        "PATH_ACADEMIC_SUBJECT_UNCERTAIN": (
            "academic_fit",
            "uncertain",
            ("grade", "subject_group", "secondary_subjects", "preparation_assets.subject_strengths"),
        ),
        "PATH_ACADEMIC_GRADE_BLOCKED": (
            "academic_fit",
            "blocks",
            ("grade", "subject_group", "secondary_subjects", "preparation_assets.subject_strengths"),
        ),
        "PATH_INTEREST_DECLARED": (
            "interest_fit",
            "supports",
            ("priorities.target_majors", "priorities.future_plan", "pathway_preferences.strong_foundation", "pathway_preferences.comprehensive_evaluation", "pathway_preferences.special_program", "pathway_preferences.service_oriented", "pathway_preferences.uniformed_service", "pathway_preferences.cross_border", "pathway_preferences.arts_sports"),
        ),
        "PATH_INTEREST_REJECTED": (
            "interest_fit",
            "blocks",
            ("priorities.target_majors", "priorities.future_plan", "pathway_preferences.strong_foundation", "pathway_preferences.comprehensive_evaluation", "pathway_preferences.special_program", "pathway_preferences.service_oriented", "pathway_preferences.uniformed_service", "pathway_preferences.cross_border", "pathway_preferences.arts_sports"),
        ),
        "PATH_INTEREST_UNVERIFIED": (
            "interest_fit",
            "uncertain",
            ("priorities.target_majors", "priorities.future_plan", "pathway_preferences.strong_foundation", "pathway_preferences.comprehensive_evaluation", "pathway_preferences.special_program", "pathway_preferences.service_oriented", "pathway_preferences.uniformed_service", "pathway_preferences.cross_border", "pathway_preferences.arts_sports"),
        ),
        "PATH_READINESS_READY": (
            "readiness",
            "supports",
            ("preparation_assets.awards", "preparation_assets.research_experiences", "preparation_assets.activities", "preparation_assets.english_readiness", "preparation_assets.interview_readiness", "preparation_assets.physical_readiness"),
        ),
        "PATH_READINESS_GAP": (
            "readiness",
            "uncertain",
            ("preparation_assets.awards", "preparation_assets.research_experiences", "preparation_assets.activities", "preparation_assets.english_readiness", "preparation_assets.interview_readiness", "preparation_assets.physical_readiness"),
        ),
        "PATH_READINESS_UNVERIFIED": (
            "readiness",
            "uncertain",
            ("preparation_assets.awards", "preparation_assets.research_experiences", "preparation_assets.activities", "preparation_assets.english_readiness", "preparation_assets.interview_readiness", "preparation_assets.physical_readiness"),
        ),
        "PATH_URGENCY_CURRENT": (
            "urgency", "supports", ("grade",),
        ),
        "PATH_URGENCY_EARLY": (
            "urgency", "uncertain", ("grade",),
        ),
        "PATH_URGENCY_UNVERIFIED": (
            "urgency", "uncertain", ("grade",),
        ),
        "PATH_SERVICE_ACCEPTED": (
            "burden", "supports", ("constraints.service_commitment",),
        ),
        "PATH_SERVICE_REJECTED": (
            "burden", "blocks", ("constraints.service_commitment",),
        ),
        "PATH_AFFORDABILITY_UNVERIFIED": (
            "burden", "uncertain", ("constraints.budget_level",),
        ),
        "PATH_EFFORT_GAP": (
            "burden",
            "uncertain",
            ("preparation_assets.awards", "preparation_assets.research_experiences", "preparation_assets.activities", "preparation_assets.english_readiness", "preparation_assets.interview_readiness", "preparation_assets.physical_readiness"),
        ),
        "PATH_BURDEN_ACCEPTABLE": (
            "burden", "supports", ("constraints.budget_level", "constraints.service_commitment"),
        ),
        "PATH_BURDEN_UNVERIFIED": (
            "burden",
            "uncertain",
            (
                "constraints.budget_level",
                "constraints.service_commitment",
                "priorities.concerns",
                "preparation_assets.awards",
                "preparation_assets.research_experiences",
                "preparation_assets.activities",
                "preparation_assets.english_readiness",
                "preparation_assets.interview_readiness",
                "preparation_assets.physical_readiness",
            ),
        ),
        "PATH_STRATEGIC_MATCH": (
            "strategic_value",
            "supports",
            ("priorities.target_schools", "target_school_reasons", "priorities.target_majors", "target_major_reasons", "priorities.future_plan", "priorities.desired_outcomes"),
        ),
        "PATH_STRATEGIC_COMMITTED": (
            "strategic_value",
            "supports",
            ("priorities.target_schools", "target_school_reasons", "priorities.target_majors", "target_major_reasons", "priorities.future_plan", "priorities.desired_outcomes"),
        ),
        "PATH_STRATEGIC_UNVERIFIED": (
            "strategic_value",
            "uncertain",
            ("priorities.target_schools", "target_school_reasons", "priorities.target_majors", "target_major_reasons", "priorities.future_plan", "priorities.desired_outcomes"),
        ),
        "PATH_EVIDENCE_OFFICIAL": (
            "evidence_quality", "supports", (),
        ),
        "PATH_EVIDENCE_CORROBORATED": (
            "evidence_quality", "supports", (),
        ),
        "PATH_EVIDENCE_REFERENCE": (
            "evidence_quality", "uncertain", (),
        ),
        "PATH_EVIDENCE_HISTORICAL": (
            "evidence_quality", "uncertain", (),
        ),
        "PATH_EVIDENCE_UNRESOLVED": (
            "evidence_quality", "blocks", (),
        ),
    }
)
_RISK_TIER_CAPS = MappingProxyType(
    {
        "unknown": MappingProxyType({"冲": 3, "稳": 4, "保": 5}),
        "balanced": MappingProxyType({"冲": 3, "稳": 4, "保": 5}),
        "conservative": MappingProxyType({"冲": 1, "稳": 4, "保": 5}),
        "aggressive": MappingProxyType({"冲": 5, "稳": 4, "保": 3}),
    }
)


def _positive_int(value: Any, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


@dataclass(frozen=True, init=False)
class DecisionReason:
    """One finite, profile-trace-bound explanation for a decision."""

    dimension: str
    code: str
    effect: str
    explanation: str
    input_fields: tuple[str, ...]
    source_ids: tuple[str, ...]
    evidence_status: EvidenceStatus | None

    def __init__(self) -> None:
        raise TypeError("DecisionReason is factory-only")

    @classmethod
    def create(
        cls,
        profile: Any,
        *,
        code: str,
        explanation: str,
        input_fields: tuple[str, ...],
        source_ids: tuple[str, ...] = (),
        evidence_status: EvidenceStatus | str | None = None,
    ) -> "DecisionReason":
        definition = _DECISION_REASON_DEFINITIONS.get(code)
        if definition is None:
            raise ValueError("decision reason code is not in the finite vocabulary")
        dimension, effect, allowed_input_fields = definition
        if dimension not in _DECISION_DIMENSIONS or effect not in _DECISION_EFFECTS:
            raise ValueError("decision reason definition is invalid")
        if not isinstance(explanation, str) or not explanation.strip():
            raise ValueError("decision reason explanation must be non-empty")
        if explanation != explanation.strip() or any(
            ord(char) < 32 or ord(char) == 127 for char in explanation
        ):
            raise ValueError("decision reason explanation is not public text")
        try:
            trace = {item.field: item for item in profile.to_decision_trace()}
        except (AttributeError, TypeError, ValueError):
            raise TypeError("profile must provide the canonical decision trace") from None
        if (
            not isinstance(input_fields, tuple)
            or len(input_fields) != len(set(input_fields))
            or any(not isinstance(field, str) for field in input_fields)
            or any(field not in allowed_input_fields for field in input_fields)
        ):
            raise ValueError(
                "decision reason input fields must be an evaluator-owned subset"
            )
        requested_input_fields = frozenset(input_fields)
        input_fields = tuple(
            field for field in allowed_input_fields if field in requested_input_fields
        )
        if any(field not in trace for field in input_fields):
            raise ValueError("decision reason fields are not in the profile trace")
        if isinstance(source_ids, (str, bytes, bytearray)):
            raise TypeError("source_ids must be a collection of safe IDs")
        sources = tuple(sorted(source_ids))
        if len(sources) != len(set(sources)) or any(
            not isinstance(source, str) or _SAFE_ID.fullmatch(source) is None
            for source in sources
        ):
            raise ValueError("source_ids must contain unique safe IDs")
        if evidence_status is not None:
            try:
                evidence_status = EvidenceStatus(evidence_status)
            except (TypeError, ValueError):
                raise ValueError("decision reason evidence_status is invalid") from None
            if evidence_status in {
                EvidenceStatus.OFFICIAL,
                EvidenceStatus.CORROBORATED,
                EvidenceStatus.REFERENCE,
                EvidenceStatus.CONFLICT,
                EvidenceStatus.PARTIAL,
                EvidenceStatus.INFERRED,
            } and not sources:
                raise ValueError(
                    "decision reason evidence_status requires supporting source IDs"
                )
        instance = object.__new__(cls)
        for name, value in (
            ("dimension", dimension),
            ("code", code),
            ("effect", effect),
            ("explanation", explanation),
            ("input_fields", input_fields),
            ("source_ids", sources),
            ("evidence_status", evidence_status),
        ):
            object.__setattr__(instance, name, value)
        return instance

    def to_dict(self) -> dict[str, Any]:
        return {
            "dimension": self.dimension,
            "code": self.code,
            "effect": self.effect,
            "explanation": self.explanation,
            "input_fields": list(self.input_fields),
            "source_ids": list(self.source_ids),
            "evidence_status": (
                None if self.evidence_status is None else self.evidence_status.value
            ),
        }


def risk_tier_caps(
    policy: "DecisionPolicySnapshot", risk_preference: str
) -> dict[str, int]:
    """Resolve profile risk into the reviewed project-rule tier caps."""

    if type(policy) is not DecisionPolicySnapshot:
        raise TypeError("policy must be a strict DecisionPolicySnapshot")
    caps = _RISK_TIER_CAPS.get(risk_preference)
    if caps is None:
        raise ValueError("risk preference is unsupported")
    return dict(caps)


@dataclass(frozen=True, init=False)
class ScenarioSelectionPolicy:
    tier_caps: Mapping[str, int]
    min_supporting_years_for_medium_confidence: int
    required_year_majority: str

    def __init__(self) -> None:
        raise TypeError("ScenarioSelectionPolicy is factory-only")

    @classmethod
    def _create(
        cls,
        *,
        tier_caps: Mapping[str, Any],
        min_supporting_years_for_medium_confidence: Any,
        required_year_majority: str,
    ) -> "ScenarioSelectionPolicy":
        if not isinstance(tier_caps, Mapping) or set(tier_caps) != {"冲", "稳", "保"}:
            raise ValueError("tier_caps must contain exactly 冲, 稳, 保")
        caps = {
            tier: _positive_int(tier_caps[tier], f"tier_caps.{tier}")
            for tier in ("冲", "稳", "保")
        }
        minimum = _positive_int(
            min_supporting_years_for_medium_confidence,
            "min_supporting_years_for_medium_confidence",
        )
        if required_year_majority not in {"strict_majority"}:
            raise ValueError("required_year_majority is unsupported")
        instance = object.__new__(cls)
        object.__setattr__(instance, "tier_caps", MappingProxyType(caps))
        object.__setattr__(
            instance,
            "min_supporting_years_for_medium_confidence",
            minimum,
        )
        object.__setattr__(instance, "required_year_majority", required_year_majority)
        return instance

    def to_dict(self) -> dict[str, Any]:
        return {
            "tier_caps": dict(self.tier_caps),
            "min_supporting_years_for_medium_confidence": self.min_supporting_years_for_medium_confidence,
            "required_year_majority": self.required_year_majority,
        }


@dataclass(frozen=True, init=False)
class DecisionPolicySnapshot:
    schema_version: str
    policy_id: str
    policy_kind: str
    reviewed_at: str
    basis: DecisionRuleBasis
    source_policy: SourcePolicyReference
    scenario: ScenarioSelectionPolicy
    pathway_reason_order: tuple[str, ...]
    action_priority_order: tuple[str, ...]

    def __init__(self) -> None:
        raise TypeError("DecisionPolicySnapshot is factory-only")

    @classmethod
    def load_default(cls) -> "DecisionPolicySnapshot":
        """Return the reviewed project rule without loading dynamic data."""

        basis = DecisionRuleBasis.create(
            basis_id="approved-end-to-end-design-2026-08-29",
            source_id="pathway-atlas-project-design",
            source_version="1.0",
        )
        source_policy = SourcePolicyReference.create(
            policy_id="pathway-atlas-source-policy",
            version="1.0",
        )
        scenario = ScenarioSelectionPolicy._create(
            tier_caps={"冲": 3, "稳": 4, "保": 5},
            min_supporting_years_for_medium_confidence=2,
            required_year_majority="strict_majority",
        )
        return cls._create(
            schema_version=_SCHEMA_VERSION,
            policy_id="pathway-atlas-planning-2026-08",
            policy_kind="project_planning_rule",
            reviewed_at="2026-08-29",
            basis=basis,
            source_policy=source_policy,
            scenario=scenario,
            pathway_reason_order=_PATHWAY_REASON_ORDER,
            action_priority_order=_ACTION_PRIORITY_ORDER,
        )

    @classmethod
    def _create(
        cls,
        *,
        schema_version: str,
        policy_id: str,
        policy_kind: str,
        reviewed_at: str,
        basis: DecisionRuleBasis,
        source_policy: SourcePolicyReference,
        scenario: ScenarioSelectionPolicy,
        pathway_reason_order: tuple[str, ...],
        action_priority_order: tuple[str, ...],
    ) -> "DecisionPolicySnapshot":
        if schema_version != _SCHEMA_VERSION:
            raise ValueError("unsupported decision-policy schema version")
        if not isinstance(policy_id, str) or _SAFE_ID.fullmatch(policy_id) is None:
            raise ValueError("policy_id must use the public safe-ID syntax")
        if policy_kind != "project_planning_rule":
            raise ValueError("decision policy must be labeled as a project planning rule")
        try:
            parsed_date = date.fromisoformat(reviewed_at)
        except (TypeError, ValueError):
            raise ValueError("reviewed_at must be a real ISO calendar date") from None
        if parsed_date.isoformat() != reviewed_at:
            raise ValueError("reviewed_at must be a real ISO calendar date")
        if not isinstance(basis, DecisionRuleBasis):
            raise TypeError("basis must be a DecisionRuleBasis")
        if not isinstance(source_policy, SourcePolicyReference):
            raise TypeError("source_policy must be a SourcePolicyReference")
        if not isinstance(scenario, ScenarioSelectionPolicy):
            raise TypeError("scenario must be a ScenarioSelectionPolicy")
        if tuple(pathway_reason_order) != _PATHWAY_REASON_ORDER:
            raise ValueError("pathway reason order must use the reviewed vocabulary")
        if tuple(action_priority_order) != _ACTION_PRIORITY_ORDER:
            raise ValueError("action priority order must use the reviewed vocabulary")
        instance = object.__new__(cls)
        for name, value in (
            ("schema_version", schema_version),
            ("policy_id", policy_id),
            ("policy_kind", policy_kind),
            ("reviewed_at", reviewed_at),
            ("basis", basis),
            ("source_policy", source_policy),
            ("scenario", scenario),
            ("pathway_reason_order", tuple(pathway_reason_order)),
            ("action_priority_order", tuple(action_priority_order)),
        ):
            object.__setattr__(instance, name, value)
        return instance

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "policy_id": self.policy_id,
            "policy_kind": self.policy_kind,
            "reviewed_at": self.reviewed_at,
            "basis": self.basis.to_dict(),
            "source_policy": self.source_policy.to_dict(),
            "scenario": self.scenario.to_dict(),
            "pathway_reason_order": list(self.pathway_reason_order),
            "action_priority_order": list(self.action_priority_order),
        }


__all__ = [
    "DecisionPolicySnapshot",
    "DecisionReason",
    "ScenarioSelectionPolicy",
    "risk_tier_caps",
]
