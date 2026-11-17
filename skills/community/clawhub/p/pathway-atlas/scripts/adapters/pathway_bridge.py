"""Bridge authenticated pathway projections into evidence and domain policy."""

from __future__ import annotations

import base64
from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, fields
import hashlib
import json
from pathlib import Path
import re
from typing import Any

if __package__ == "scripts.adapters":
    from .pathway_extraction import (
        FieldProvenance,
        PathwayPolicyProjection,
        _TARGETS,
        replay_pathway_policy_projection,
        validate_pathway_policy_projection,
        validate_pathway_policy_projection_sources,
    )
    from . import validate_public_locator
    from ..contracts import EvidenceFact, EvidenceStatus, SourceCandidate, SourceTier
    from ..evidence import EvidenceStore
    from ..path_recommend import (
        PathwayFieldEvidenceOrigin,
        PathwayPolicy,
        _create_pathway_field_evidence,
        _pathway_field_context_binding,
        pathway_policy_field_values,
        pathway_policy_internal_payload,
    )
    from ..validate_evidence import FrozenJsonRecord, validate_bundle_snapshot
else:  # ``sys.path`` rooted at ``scripts`` package compatibility.
    from adapters.pathway_extraction import (  # type: ignore
        FieldProvenance,
        PathwayPolicyProjection,
        _TARGETS,
        replay_pathway_policy_projection,
        validate_pathway_policy_projection,
        validate_pathway_policy_projection_sources,
    )
    from adapters import validate_public_locator  # type: ignore
    from contracts import (  # type: ignore
        EvidenceFact,
        EvidenceStatus,
        SourceCandidate,
        SourceTier,
    )
    from evidence import EvidenceStore  # type: ignore
    from path_recommend import (  # type: ignore
        PathwayFieldEvidenceOrigin,
        PathwayPolicy,
        _create_pathway_field_evidence,
        _pathway_field_context_binding,
        pathway_policy_field_values,
        pathway_policy_internal_payload,
    )
    from validate_evidence import FrozenJsonRecord, validate_bundle_snapshot  # type: ignore


_FIELD = re.compile(r"pathway_policy:([A-Za-z0-9][A-Za-z0-9._:-]{0,127})\Z")
_HASH = re.compile(r"sha256:[0-9a-f]{64}\Z")
_ACCEPTED = frozenset(
    {
        EvidenceStatus.OFFICIAL,
        EvidenceStatus.CORROBORATED,
        EvidenceStatus.REFERENCE,
    }
)
_WRAPPER_FIELDS = frozenset(
    {"projection_hash", "provenance_count", "field_coverage"}
)
_PARTIAL_NOTES = "pathway-projection-v1:"
_RAW_TO_POLICY_FIELD = {
    "institution": "institution",
    "province": "province",
    "subject_mode": "subject_mode",
    "year": "data_year",
    "eligibility_requirements": "eligibility_requirements",
    "grade_requirements": "grade_requirements",
    "subject_requirements": "subject_requirements",
    "award_requirements": "award_requirements",
    "activity_requirements": "activity_requirements",
    "disqualifying_facts": "disqualifying_facts",
    "professional_options": "professional_options",
    "training_arrangements": "training_arrangements",
    "transition_rules": "transition_rules",
    "outcomes": "outcomes",
    "service_employment_obligations": "service_employment_obligations",
    "penalty_exit_rules": "penalty_exit_rules",
    "fees_and_subsidies": "fees_and_subsidies",
    "dates_and_deadlines": "timeline",
    "application_materials": "application_materials",
    "preparation_actions": "preparation_actions",
}


class PathwayBridgeError(ValueError):
    """Projection or persisted fact fails authenticated pathway replay."""


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def _fact_value(projection: PathwayPolicyProjection) -> dict[str, Any]:
    value = projection.to_dict()
    value.update(
        {
            "projection_hash": projection.digest,
            "provenance_count": len(projection.field_provenance),
            "field_coverage": {
                item.field: item.status.value for item in projection.field_provenance
            },
        }
    )
    return value


def _partial_notes(projection: PathwayPolicyProjection) -> str:
    encoded = base64.urlsafe_b64encode(
        _canonical_json(_fact_value(projection)).encode("utf-8")
    ).decode("ascii")
    return _PARTIAL_NOTES + encoded


def _projection_from_fact_value(value: Any) -> PathwayPolicyProjection:
    if not isinstance(value, Mapping):
        raise PathwayBridgeError("pathway fact does not contain a projection")
    if not _WRAPPER_FIELDS.issubset(value):
        raise PathwayBridgeError("pathway projection wrapper is incomplete")
    projection_value = {
        key: item for key, item in value.items() if key not in _WRAPPER_FIELDS
    }
    try:
        projection = replay_pathway_policy_projection(projection_value)
    except (TypeError, ValueError):
        raise PathwayBridgeError("pathway projection cannot be replayed") from None
    if value.get("projection_hash") != projection.digest:
        raise PathwayBridgeError("pathway projection hash disagrees")
    if value.get("provenance_count") != len(projection.field_provenance):
        raise PathwayBridgeError("pathway provenance count disagrees")
    expected_coverage = {
        item.field: item.status.value for item in projection.field_provenance
    }
    if value.get("field_coverage") != expected_coverage:
        raise PathwayBridgeError("pathway field coverage disagrees")
    return projection


def _validated_candidate(value: Mapping[str, Any]) -> SourceCandidate:
    try:
        return SourceCandidate(
            source_id=value["source_id"],
            url=value["url"],
            publisher=value["publisher"],
            tier=SourceTier(value["tier"]),
            published_at=value["published_at"],
            retrieved_at=value["retrieved_at"],
            content_hash=value["content_hash"],
            citation_root=value["citation_root"],
            summary=value["summary"],
        )
    except (KeyError, TypeError, ValueError):
        raise PathwayBridgeError("validated pathway candidate is invalid") from None


@dataclass(frozen=True, init=False)
class PathwayPolicyEvidenceBridge:
    """Factory-only evidence artifact over one replayable projection."""

    policy_id: str
    evidence_status: EvidenceStatus
    source_ids: tuple[str, ...]
    evidence_method: str
    extraction_method: str
    locator: str
    projection_digest: str
    bridge_digest: str
    _projection_json: str

    def __init__(self) -> None:
        raise TypeError("PathwayPolicyEvidenceBridge is factory-only")

    @classmethod
    def _create(cls, **values: Any) -> "PathwayPolicyEvidenceBridge":
        instance = object.__new__(cls)
        for name, value in values.items():
            object.__setattr__(instance, name, value)
        return instance

    @property
    def projection(self) -> PathwayPolicyProjection:
        value = json.loads(self._projection_json)
        if not isinstance(value, dict):  # pragma: no cover - factory invariant
            raise PathwayBridgeError("pathway bridge projection is invalid")
        try:
            return replay_pathway_policy_projection(value)
        except (TypeError, ValueError):
            raise PathwayBridgeError("pathway bridge projection cannot be replayed") from None

    @property
    def fact(self) -> EvidenceFact:
        projection = self.projection
        exact = projection.evidence_status in _ACCEPTED
        return EvidenceFact(
            fact_id=projection.policy_id,
            field=f"pathway_policy:{projection.policy_id}",
            value=_fact_value(projection) if exact else None,
            unit=None,
            status=projection.evidence_status,
            source_ids=projection.source_ids,
            method=projection.evidence_method,
            notes=(
                f"query_task:{projection.query_task_id}"
                if exact
                else _partial_notes(projection)
            ),
        )

    def persist(self, store: EvidenceStore) -> None:
        if not isinstance(store, EvidenceStore):
            raise TypeError("store must be an EvidenceStore")
        validate_pathway_policy_evidence_bridge(self)
        store.add_fact(
            self.fact,
            year=self.projection.data_year,
            extraction_method=self.extraction_method,
            locator=self.locator,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "evidence_status": self.evidence_status.value,
            "source_ids": list(self.source_ids),
            "evidence_method": self.evidence_method,
            "projection": self.projection.to_dict(),
            "fact": self.fact.to_dict(),
            "extraction_method": self.extraction_method,
            "locator": self.locator,
            "projection_digest": self.projection_digest,
            "bridge_digest": self.bridge_digest,
        }


@dataclass(frozen=True, init=False)
class PathwayEvidenceObservation:
    """Authenticated non-decisive projection for one planned pathway target."""

    observation_id: str
    pathway_family: str
    pathway_type: str
    title: str
    institution: str | None
    professional_options: tuple[str, ...]
    evidence_status: EvidenceStatus
    source_ids: tuple[str, ...]
    missing_constraints: tuple[str, ...]
    preparation_actions: tuple[str, ...]
    evidence_method: str
    locators: tuple[str, ...]
    extraction_methods: tuple[str, ...]
    profile_digest: str
    query_plan_digest: str
    query_task_ids: tuple[str, ...]
    projection_digests: tuple[str, ...]
    field_provenance: tuple[FieldProvenance, ...]
    digest: str
    _origin_json: str

    def __init__(self) -> None:
        raise TypeError("PathwayEvidenceObservation is factory-only")

    @classmethod
    def _create(cls, **values: Any) -> "PathwayEvidenceObservation":
        instance = object.__new__(cls)
        for name, value in values.items():
            object.__setattr__(instance, name, value)
        return instance

    def to_dict(self) -> dict[str, Any]:
        return {
            "observation_id": self.observation_id,
            "pathway_family": self.pathway_family,
            "pathway_type": self.pathway_type,
            "title": self.title,
            "institution": self.institution,
            "professional_options": list(self.professional_options),
            "evidence_status": self.evidence_status.value,
            "source_ids": list(self.source_ids),
            "missing_constraints": list(self.missing_constraints),
            "preparation_actions": list(self.preparation_actions),
            "evidence_method": self.evidence_method,
            "locators": list(self.locators),
            "extraction_methods": list(self.extraction_methods),
            "profile_digest": self.profile_digest,
            "query_plan_digest": self.query_plan_digest,
            "query_task_ids": list(self.query_task_ids),
            "projection_digests": list(self.projection_digests),
            "field_provenance": [
                item.to_dict() for item in self.field_provenance
            ],
            "digest": self.digest,
        }


def bridge_pathway_policy_evidence(
    projection: PathwayPolicyProjection,
) -> PathwayPolicyEvidenceBridge:
    """Create evidence without accepting caller-authored status or source IDs."""

    try:
        validate_pathway_policy_projection(projection)
    except (TypeError, ValueError):
        raise PathwayBridgeError("pathway projection is not authenticated") from None
    methods = tuple(
        sorted(
            {
                method
                for item in projection.field_provenance
                for method in item.extraction_methods
            }
        )
    )
    if not methods:
        raise PathwayBridgeError("pathway projection lacks extraction provenance")
    extraction_method = methods[0] if len(methods) == 1 else "manual-structured"
    locator = validate_public_locator(
        f"pathway-projection[{projection.provenance_digest[7:23]}]"
    )
    projection_json = _canonical_json(projection.to_dict())
    bridge_payload = {
        "projection_digest": projection.digest,
        "evidence_status": projection.evidence_status.value,
        "source_ids": list(projection.source_ids),
        "evidence_method": projection.evidence_method,
        "extraction_method": extraction_method,
        "locator": locator,
    }
    bridge_digest = "sha256:" + hashlib.sha256(
        _canonical_json(bridge_payload).encode("utf-8")
    ).hexdigest()
    return PathwayPolicyEvidenceBridge._create(
        policy_id=projection.policy_id,
        evidence_status=projection.evidence_status,
        source_ids=projection.source_ids,
        evidence_method=projection.evidence_method,
        extraction_method=extraction_method,
        locator=locator,
        projection_digest=projection.digest,
        bridge_digest=bridge_digest,
        _projection_json=projection_json,
    )


def validate_pathway_policy_evidence_bridge(
    bridge: PathwayPolicyEvidenceBridge,
) -> PathwayPolicyEvidenceBridge:
    """Rebuild a bridge and reject direct or coordinated field mutation."""

    if type(bridge) is not PathwayPolicyEvidenceBridge:
        raise TypeError("bridge must be a PathwayPolicyEvidenceBridge")
    rebuilt = bridge_pathway_policy_evidence(bridge.projection)
    if rebuilt.to_dict() != bridge.to_dict():
        raise PathwayBridgeError("pathway bridge no longer matches its projection")
    return bridge


def _domain_policy(projection: PathwayPolicyProjection) -> PathwayPolicy:
    required = (
        projection.institution,
        projection.eligibility_requirements,
        projection.grade_requirements,
        projection.subject_requirements,
        projection.award_requirements,
        projection.activity_requirements,
        projection.disqualifying_facts,
        projection.professional_options,
        projection.training_arrangements,
        projection.transition_rules,
        projection.outcomes,
        projection.service_employment_obligations,
        projection.penalty_exit_rules,
        projection.fees_and_subsidies,
        projection.timeline,
        projection.application_materials,
        projection.preparation_actions,
    )
    if projection.coverage_status != "complete" or any(item is None for item in required):
        raise PathwayBridgeError("incomplete pathway projection is not decisive")
    distance = projection.target_year - projection.data_year
    if not 0 <= distance <= 3:
        raise PathwayBridgeError("pathway projection year fallback is invalid")
    context_payload = {
        "profile_digest": projection.profile_digest,
        "query_plan_digest": projection.query_plan_digest,
        "query_task_id": projection.query_task_id,
        "query_task_digest": projection.query_task_digest,
        "projection_digest": projection.digest,
        "policy_id": projection.policy_id,
        "target_year": projection.target_year,
        "data_year": projection.data_year,
    }
    context_binding = _pathway_field_context_binding(context_payload)
    specialized_requirements = {
        item
        for values in (
            projection.grade_requirements,
            projection.subject_requirements,
            projection.award_requirements,
            projection.activity_requirements,
        )
        for item in values or ()
    }
    eligibility_requirements = tuple(
        item
        for item in projection.eligibility_requirements
        if item not in specialized_requirements
    )
    policy = PathwayPolicy(
        policy_id=projection.policy_id,
        pathway_type=projection.pathway_type,
        title=projection.title,
        institution=projection.institution,
        province=projection.province,
        subject_mode=projection.subject_mode,
        valid_year=projection.data_year,
        eligibility_requirements=eligibility_requirements,
        disqualifying_facts=projection.disqualifying_facts,
        professional_options=projection.professional_options,
        training_arrangements=projection.training_arrangements,
        transition_rules=projection.transition_rules,
        outcomes=projection.outcomes,
        service_employment_obligations=projection.service_employment_obligations,
        penalty_exit_rules=projection.penalty_exit_rules,
        fees_and_subsidies=projection.fees_and_subsidies,
        policy_source_ids=projection.source_ids,
        evidence_status=projection.evidence_status,
        calculation_basis=(
            "经认证公开政策投影；当年资料"
            if distance == 0
            else f"经认证公开政策投影；历史回退 {projection.data_year}"
        ),
        target_year=projection.target_year,
        data_year=projection.data_year,
        fallback_distance=distance,
        year_basis="current_year" if distance == 0 else "historical_fallback",
        timeline=projection.timeline,
        preparation_actions=projection.preparation_actions,
        grade_requirements=projection.grade_requirements,
        subject_requirements=projection.subject_requirements,
        award_requirements=projection.award_requirements,
        activity_requirements=projection.activity_requirements,
        application_materials=projection.application_materials,
        profile_digest=projection.profile_digest,
        query_plan_digest=projection.query_plan_digest,
        field_evidence=(),
        _authenticated_projection=projection,
    )
    policy_values = pathway_policy_field_values(policy)
    evidence = tuple(
        _create_pathway_field_evidence(
            field=_RAW_TO_POLICY_FIELD[item.field],
            value=policy_values[_RAW_TO_POLICY_FIELD[item.field]],
            origin=PathwayFieldEvidenceOrigin.POLICY_SOURCE,
            context_binding=context_binding,
            origin_payload={
                "projection_digest": projection.digest,
                "provenance": item.to_dict(),
            },
            status=item.status,
            coverage=(
                "complete"
                if item.status in _ACCEPTED
                else projection.coverage_status
            ),
            source_ids=item.source_ids,
            locators=item.locators,
            extraction_methods=item.extraction_methods,
            evidence_method=item.evidence_method,
            upstream_fields=(item.field,),
            warnings=item.warnings,
        )
        for item in projection.field_provenance
    )
    return PathwayPolicy(
        **{
            item.name: getattr(policy, item.name)
            for item in fields(policy)
            if item.name not in {"field_evidence", "_authenticated_projection"}
        },
        field_evidence=evidence,
        _authenticated_projection=projection,
    )


def validate_authenticated_domain_policy(
    policy: PathwayPolicy,
    profile: Any,
    plan: Any,
) -> PathwayPolicy:
    """Replay one full-profile policy from its typed projection and plan context."""

    if type(policy) is not PathwayPolicy:
        raise TypeError("authenticated projection replay requires a strict PathwayPolicy")
    if __package__ == "scripts.adapters":
        from ..planning_profile import PlanningProfile
        from ..query_plan import validate_query_plan_payload
    else:  # pragma: no cover - flat scripts-path compatibility
        from planning_profile import PlanningProfile  # type: ignore
        from query_plan import validate_query_plan_payload  # type: ignore
    if type(profile) is not PlanningProfile:
        raise TypeError("authenticated projection replay requires a strict PlanningProfile")
    try:
        profile_payload = profile.to_dict()
        profile_payload.pop("mode")
        profile_payload.pop("digest")
        canonical_profile = PlanningProfile.create(profile_payload)
        canonical_plan = validate_query_plan_payload(plan.to_dict())
    except (AttributeError, KeyError, TypeError, ValueError):
        raise PathwayBridgeError(
            "authenticated projection context cannot be replayed"
        ) from None
    if (
        canonical_profile.to_dict() != profile.to_dict()
        or canonical_plan.to_dict() != plan.to_dict()
    ):
        raise PathwayBridgeError(
            "authenticated projection context cannot be replayed"
        )
    projection = policy._authenticated_projection
    if type(projection) is not PathwayPolicyProjection:
        raise PathwayBridgeError("pathway policy lacks an authenticated projection")
    try:
        validate_pathway_policy_projection(projection)
    except (TypeError, ValueError):
        raise PathwayBridgeError("pathway policy authenticated projection is invalid") from None
    query_plan_digest = "sha256:" + hashlib.sha256(
        _canonical_json(canonical_plan.to_dict()).encode("utf-8")
    ).hexdigest()
    matching_tasks = tuple(
        item
        for item in canonical_plan.tasks
        if item.task_id == projection.query_task_id
    )
    if len(matching_tasks) != 1:
        raise PathwayBridgeError(
            "pathway policy authenticated projection task is detached"
        )
    task = matching_tasks[0]
    expected_task = {
        "task_id": task.task_id,
        "kind": task.kind,
        "target_name": task.target_name,
        "province": task.province,
        "subject_group": task.subject_group,
        "subject_mode": canonical_profile.subject_mode,
        "year": task.year,
        "target_year": canonical_plan.research_year,
        "source_policy_id": task.source_policy_id,
        "source_policy_version": task.source_policy_version,
    }
    expected_task["task_digest"] = "sha256:" + hashlib.sha256(
        _canonical_json(expected_task).encode("utf-8")
    ).hexdigest()
    input_projection = projection.input_projection
    if (
        input_projection.get("task") != expected_task
        or projection.profile_digest != canonical_profile.digest
        or projection.query_plan_digest != query_plan_digest
        or projection.target_year != canonical_plan.research_year
        or projection.province != canonical_profile.province
        or projection.subject_mode != canonical_profile.subject_mode
    ):
        raise PathwayBridgeError(
            "pathway policy authenticated projection disagrees with its planning context"
        )
    rebuilt = _domain_policy(projection)
    if pathway_policy_internal_payload(rebuilt) != pathway_policy_internal_payload(policy):
        raise PathwayBridgeError(
            "pathway policy no longer matches its authenticated projection"
        )
    return rebuilt


def bridge_pathway_policies(
    evidence: Path | Iterable[PathwayPolicyEvidenceBridge],
    *,
    province: str,
    subject_mode: str,
    target_year: int,
    expected_profile_digest: str | None = None,
    expected_query_plan_digest: str | None = None,
) -> tuple[PathwayPolicy, ...]:
    """Return only persisted projections that pass complete replay validation."""

    if (
        not isinstance(expected_profile_digest, str)
        or _HASH.fullmatch(expected_profile_digest) is None
        or not isinstance(expected_query_plan_digest, str)
        or _HASH.fullmatch(expected_query_plan_digest) is None
    ):
        raise PathwayBridgeError(
            "pathway replay requires expected profile and query-plan digests"
        )
    if isinstance(evidence, Path):
        validation = validate_bundle_snapshot(evidence, _allow_empty=True)
        if validation.snapshot is None or validation.issues:
            raise PathwayBridgeError("host-internal evidence bundle validation failed")
        persisted_facts = validation.snapshot.facts
        persisted_candidates = tuple(
            _validated_candidate(item.to_dict())
            for item in validation.snapshot.candidates
        )
        persisted_contexts = tuple(
            item.to_dict() for item in validation.snapshot.contexts
        )
        direct_bridges: tuple[PathwayPolicyEvidenceBridge, ...] = ()
    else:
        if isinstance(evidence, (str, bytes, bytearray)):
            raise TypeError(
                "pathway evidence must be a host-internal bundle Path or factory bridges"
            )
        try:
            direct_bridges = tuple(evidence)
        except TypeError:
            raise TypeError(
                "persisted pathway evidence requires a host-internal bundle Path"
            ) from None
        if any(type(item) is not PathwayPolicyEvidenceBridge for item in direct_bridges):
            raise TypeError("direct pathway evidence accepts only factory bridges")
        persisted_facts = ()
        persisted_candidates = ()
        persisted_contexts = ()
    if not isinstance(province, str) or not province.strip():
        raise TypeError("province must be non-empty text")
    province = province.strip()
    if subject_mode not in {"3+1+2", "3+3"}:
        raise ValueError("subject_mode must be 3+1+2 or 3+3")
    if (
        not isinstance(target_year, int)
        or isinstance(target_year, bool)
        or not 2000 <= target_year <= 2100
    ):
        raise TypeError("target_year must be a supported integer year")

    projected: list[tuple[str, PathwayPolicy]] = []
    for bridge in direct_bridges:
        validate_pathway_policy_evidence_bridge(bridge)
        projection = bridge.projection
        if (
            projection.profile_digest != expected_profile_digest
            or projection.query_plan_digest != expected_query_plan_digest
        ):
            raise PathwayBridgeError(
                "direct pathway projection does not match the expected planning context"
            )
        if (
            projection.evidence_status not in _ACCEPTED
            or projection.province != province
            or projection.subject_mode != subject_mode
            or projection.target_year != target_year
        ):
            continue
        try:
            policy = _domain_policy(projection)
        except (TypeError, ValueError):
            continue
        projected.append((projection.digest, policy))

    for frozen in persisted_facts:
        if type(frozen) is not FrozenJsonRecord:
            raise TypeError("snapshot facts must be frozen JSON records")
        fact = frozen.to_dict()
        field = fact.get("field")
        match = _FIELD.fullmatch(field) if isinstance(field, str) else None
        if match is None:
            continue
        try:
            status = EvidenceStatus(fact.get("status"))
        except (TypeError, ValueError):
            continue
        if status not in _ACCEPTED:
            continue
        try:
            projection = _projection_from_fact_value(fact.get("value"))
        except (TypeError, ValueError):
            raise PathwayBridgeError(
                "persisted pathway projection does not replay"
            ) from None
        projection_candidate_ids = {
            item["source_id"] for item in projection.input_projection["sources"]
        }
        projection_candidates = tuple(
            item
            for item in persisted_candidates
            if item.source_id in projection_candidate_ids
        )
        if len(projection_candidates) != len(projection_candidate_ids):
            raise PathwayBridgeError(
                "persisted pathway projection lacks validated candidates"
            )
        try:
            validate_pathway_policy_projection_sources(
                projection, projection_candidates
            )
        except (TypeError, ValueError):
            raise PathwayBridgeError(
                "persisted pathway candidate identities do not replay"
            ) from None
        contexts = tuple(
            item
            for item in persisted_contexts
            if item.get("kind") == "fact-provenance"
            and item.get("fact_id") == projection.policy_id
        )
        rebuilt_bridge = bridge_pathway_policy_evidence(projection)
        if len(contexts) != 1 or rebuilt_bridge.fact.to_dict() != fact:
            raise PathwayBridgeError(
                "persisted pathway fact does not match its typed bridge"
            )
        context = contexts[0]
        if (
            context.get("source_ids") != list(projection.source_ids)
            or context.get("year") != projection.data_year
            or context.get("extraction_method") != rebuilt_bridge.extraction_method
            or context.get("locator") != rebuilt_bridge.locator
        ):
            raise PathwayBridgeError(
                "persisted pathway provenance does not match its typed bridge"
            )
        if (
            projection.policy_id != match.group(1)
            or fact.get("fact_id") != projection.policy_id
            or projection.evidence_status is not status
            or fact.get("source_ids") != list(projection.source_ids)
            or fact.get("method") != projection.evidence_method
            or fact.get("notes") != f"query_task:{projection.query_task_id}"
        ):
            raise PathwayBridgeError(
                "persisted pathway fact identity does not match its projection"
            )
        if (
            projection.profile_digest != expected_profile_digest
            or projection.query_plan_digest != expected_query_plan_digest
            or projection.province != province
            or projection.subject_mode != subject_mode
            or projection.target_year != target_year
        ):
            raise PathwayBridgeError(
                "persisted pathway projection does not match the expected planning context"
            )
        try:
            policy = _domain_policy(projection)
        except (TypeError, ValueError):
            continue
        projected.append((projection.digest, policy))

    hash_counts = Counter(item[0] for item in projected)
    id_counts = Counter(item[1].policy_id for item in projected)
    return tuple(
        sorted(
            (
                policy
                for projection_hash, policy in projected
                if hash_counts[projection_hash] == 1
                and id_counts[policy.policy_id] == 1
            ),
            key=lambda policy: policy.policy_id,
        )
    )


def _canonical_observation_context(profile: Any, plan: Any) -> tuple[Any, Any, str]:
    if __package__ == "scripts.adapters":
        from ..planning_profile import PlanningProfile
        from ..query_plan import validate_query_plan_payload
    else:  # pragma: no cover - flat scripts-path compatibility
        from planning_profile import PlanningProfile  # type: ignore
        from query_plan import validate_query_plan_payload  # type: ignore
    if type(profile) is not PlanningProfile:
        raise TypeError("pathway observations require a strict PlanningProfile")
    try:
        profile_payload = profile.to_dict()
        profile_payload.pop("mode")
        profile_payload.pop("digest")
        canonical_profile = PlanningProfile.create(profile_payload)
        canonical_plan = validate_query_plan_payload(plan.to_dict())
    except (AttributeError, KeyError, TypeError, ValueError):
        raise PathwayBridgeError(
            "pathway observation context cannot be replayed"
        ) from None
    if (
        canonical_profile.to_dict() != profile.to_dict()
        or canonical_plan.to_dict() != plan.to_dict()
    ):
        raise PathwayBridgeError(
            "pathway observation context cannot be replayed"
        )
    plan_digest = "sha256:" + hashlib.sha256(
        _canonical_json(canonical_plan.to_dict()).encode("utf-8")
    ).hexdigest()
    return canonical_profile, canonical_plan, plan_digest


def _projection_from_persisted_pathway_fact(
    fact: Mapping[str, Any],
) -> PathwayPolicyProjection:
    try:
        status = EvidenceStatus(fact.get("status"))
    except (TypeError, ValueError):
        raise PathwayBridgeError("persisted pathway fact status is invalid") from None
    if status in _ACCEPTED:
        value = fact.get("value")
    else:
        notes = fact.get("notes")
        if not isinstance(notes, str) or not notes.startswith(_PARTIAL_NOTES):
            raise PathwayBridgeError(
                "non-decisive pathway fact lacks its replayable projection"
            )
        try:
            value = json.loads(
                base64.urlsafe_b64decode(
                    notes.removeprefix(_PARTIAL_NOTES).encode("ascii")
                ).decode("utf-8")
            )
        except (UnicodeDecodeError, ValueError):
            raise PathwayBridgeError(
                "non-decisive pathway projection cannot be decoded"
            ) from None
    return _projection_from_fact_value(value)


def _pathway_projections(
    evidence: Path | tuple[PathwayPolicyEvidenceBridge, ...],
    *,
    profile_digest: str,
    query_plan_digest: str,
    province: str,
    subject_mode: str,
    target_year: int,
) -> tuple[PathwayPolicyProjection, ...]:
    if isinstance(evidence, Path):
        validation = validate_bundle_snapshot(evidence, _allow_empty=True)
        if validation.snapshot is None or validation.issues:
            raise PathwayBridgeError("host-internal evidence bundle validation failed")
        persisted_facts = validation.snapshot.facts
        persisted_candidates = tuple(
            _validated_candidate(item.to_dict())
            for item in validation.snapshot.candidates
        )
        persisted_contexts = tuple(
            item.to_dict() for item in validation.snapshot.contexts
        )
        direct_bridges: tuple[PathwayPolicyEvidenceBridge, ...] = ()
    else:
        persisted_facts = ()
        persisted_candidates = ()
        persisted_contexts = ()
        direct_bridges = evidence

    projections: list[PathwayPolicyProjection] = []
    for bridge in direct_bridges:
        validate_pathway_policy_evidence_bridge(bridge)
        projection = bridge.projection
        if (
            projection.profile_digest != profile_digest
            or projection.query_plan_digest != query_plan_digest
            or projection.province != province
            or projection.subject_mode != subject_mode
            or projection.target_year != target_year
        ):
            raise PathwayBridgeError(
                "direct pathway projection does not match the observation context"
            )
        projections.append(projection)

    for frozen in persisted_facts:
        if type(frozen) is not FrozenJsonRecord:
            raise TypeError("snapshot facts must be frozen JSON records")
        fact = frozen.to_dict()
        field = fact.get("field")
        match = _FIELD.fullmatch(field) if isinstance(field, str) else None
        if match is None:
            continue
        projection = _projection_from_persisted_pathway_fact(fact)
        projection_candidate_ids = {
            item["source_id"] for item in projection.input_projection["sources"]
        }
        projection_candidates = tuple(
            item
            for item in persisted_candidates
            if item.source_id in projection_candidate_ids
        )
        if len(projection_candidates) != len(projection_candidate_ids):
            raise PathwayBridgeError(
                "persisted pathway projection lacks validated candidates"
            )
        try:
            validate_pathway_policy_projection_sources(
                projection, projection_candidates
            )
        except (TypeError, ValueError):
            raise PathwayBridgeError(
                "persisted pathway candidate identities do not replay"
            ) from None
        rebuilt = bridge_pathway_policy_evidence(projection)
        contexts = tuple(
            item
            for item in persisted_contexts
            if item.get("kind") == "fact-provenance"
            and item.get("fact_id") == projection.policy_id
        )
        if len(contexts) != 1 or rebuilt.fact.to_dict() != fact:
            raise PathwayBridgeError(
                "persisted pathway fact does not match its typed bridge"
            )
        context = contexts[0]
        if (
            context.get("source_ids") != list(projection.source_ids)
            or context.get("year") != projection.data_year
            or context.get("extraction_method") != rebuilt.extraction_method
            or context.get("locator") != rebuilt.locator
        ):
            raise PathwayBridgeError(
                "persisted pathway provenance does not match its typed bridge"
            )
        try:
            fact_status = EvidenceStatus(fact.get("status"))
        except (TypeError, ValueError):  # pragma: no cover - rebuilt fact guards this
            raise PathwayBridgeError("persisted pathway fact status is invalid") from None
        if (
            projection.policy_id != match.group(1)
            or fact.get("fact_id") != projection.policy_id
            or projection.evidence_status is not fact_status
            or fact.get("source_ids") != list(projection.source_ids)
            or fact.get("method") != projection.evidence_method
            or projection.profile_digest != profile_digest
            or projection.query_plan_digest != query_plan_digest
            or projection.province != province
            or projection.subject_mode != subject_mode
            or projection.target_year != target_year
        ):
            raise PathwayBridgeError(
                "persisted pathway projection does not match the observation context"
            )
        projections.append(projection)

    unique = {item.digest: item for item in projections}
    return tuple(sorted(unique.values(), key=lambda item: item.digest))


def _observation_status(
    projections: tuple[PathwayPolicyProjection, ...],
) -> EvidenceStatus:
    for status in (
        EvidenceStatus.CONFLICT,
        EvidenceStatus.PARTIAL,
        EvidenceStatus.MASKED,
        EvidenceStatus.MISSING,
    ):
        if any(item.evidence_status is status for item in projections):
            return status
    return EvidenceStatus.MISSING


def _accepted_observation_field(
    projections: tuple[PathwayPolicyProjection, ...],
    field: str,
) -> tuple[Any, FieldProvenance] | None:
    """Retain one accepted field only when every accepted value agrees."""

    accepted: list[tuple[Any, FieldProvenance]] = []
    for projection in projections:
        provenance = next(
            (item for item in projection.field_provenance if item.field == field),
            None,
        )
        if provenance is None:
            continue
        if provenance.status is EvidenceStatus.CONFLICT:
            return None
        value = getattr(projection, field)
        if provenance.status in _ACCEPTED and value is not None:
            accepted.append((value, provenance))
    if not accepted:
        return None
    canonical_values = {_canonical_json(value) for value, _item in accepted}
    if len(canonical_values) != 1:
        return None
    value = accepted[0][0]
    provenance_items = tuple(item for _value, item in accepted)
    status = max(
        (item.status for item in provenance_items),
        key={
            EvidenceStatus.OFFICIAL: 0,
            EvidenceStatus.CORROBORATED: 1,
            EvidenceStatus.REFERENCE: 2,
        }.__getitem__,
    )
    evidence_methods = tuple(
        sorted({item.evidence_method for item in provenance_items})
    )
    return value, FieldProvenance._create(
        field=field,
        status=status,
        source_ids=tuple(
            sorted(
                {
                    source
                    for item in provenance_items
                    for source in item.source_ids
                }
            )
        ),
        locators=tuple(
            sorted(
                {
                    locator
                    for item in provenance_items
                    for locator in item.locators
                }
            )
        ),
        extraction_methods=tuple(
            sorted(
                {
                    method
                    for item in provenance_items
                    for method in item.extraction_methods
                }
            )
        ),
        evidence_method=(
            evidence_methods[0]
            if len(evidence_methods) == 1
            else "pathway-observation-field-consensus-v1"
        ),
        warnings=tuple(
            dict.fromkeys(
                warning
                for item in provenance_items
                for warning in item.warnings
            )
        ),
    )


def _build_pathway_observation(
    *,
    profile: Any,
    plan: Any,
    query_plan_digest: str,
    kind: str,
    title: str,
    tasks: tuple[Any, ...],
    projections: tuple[PathwayPolicyProjection, ...],
) -> PathwayEvidenceObservation:
    pathway_family, pathway_type = _TARGETS[title]
    status = _observation_status(projections)
    known_fields = {
        field: accepted
        for field in ("institution", "professional_options")
        if (accepted := _accepted_observation_field(projections, field))
        is not None
    }
    institution = (
        known_fields["institution"][0]
        if "institution" in known_fields
        else None
    )
    professional_options = (
        known_fields["professional_options"][0]
        if "professional_options" in known_fields
        else ()
    )
    field_provenance = tuple(
        known_fields[field][1]
        for field in ("institution", "professional_options")
        if field in known_fields
    )
    sources = tuple(
        sorted({source for item in projections for source in item.source_ids})
    )
    bridges = tuple(bridge_pathway_policy_evidence(item) for item in projections)
    if status is EvidenceStatus.CONFLICT:
        gap = f"{title}政策关键字段存在冲突，冲突值未用于判断"
        method = "pathway-observation-conflict-v1"
    elif status is EvidenceStatus.PARTIAL:
        gap = f"{title}政策关键字段证据不完整"
        method = "pathway-observation-partial-v1"
    elif status is EvidenceStatus.MASKED:
        gap = f"{title}政策关键字段无法可靠读取"
        method = "pathway-observation-masked-v1"
    else:
        gap = f"尚未取得可核验的{title}政策证据"
        method = "query-plan-pathway-missing-v1"
    identity_payload = {
        "profile_digest": profile.digest,
        "query_plan_digest": query_plan_digest,
        "kind": kind,
        "title": title,
    }
    identity_hash = hashlib.sha256(
        _canonical_json(identity_payload).encode("utf-8")
    ).hexdigest()
    origin = {
        "identity": identity_payload,
        "projections": [item.to_dict() for item in projections],
    }
    values = {
        "observation_id": "pathway-observation-" + identity_hash[:24],
        "pathway_family": pathway_family,
        "pathway_type": pathway_type,
        "title": title,
        "institution": institution,
        "professional_options": professional_options,
        "evidence_status": status,
        "source_ids": sources,
        "missing_constraints": (
            gap,
            f"{title}报考资格尚未完成政策证据核验",
        ),
        "preparation_actions": (
            f"检索并核验{title}当年官方政策原文",
            f"对照已确认画像逐项核验{title}报考资格",
        ),
        "evidence_method": method,
        "locators": (
            tuple(sorted({item.locator for item in bridges}))
            if bridges
            else (f"query-plan-pathway[{identity_hash[:16]}]",)
        ),
        "extraction_methods": (
            tuple(sorted({item.extraction_method for item in bridges}))
            if bridges
            else ("authenticated-query-plan",)
        ),
        "profile_digest": profile.digest,
        "query_plan_digest": query_plan_digest,
        "query_task_ids": tuple(sorted(item.task_id for item in tasks)),
        "projection_digests": tuple(sorted(item.digest for item in projections)),
        "field_provenance": field_provenance,
    }
    public_payload = {
        key: (
            value.value
            if isinstance(value, EvidenceStatus)
            else [item.to_dict() for item in value]
            if key == "field_provenance"
            else list(value)
            if isinstance(value, tuple)
            else value
        )
        for key, value in values.items()
    }
    return PathwayEvidenceObservation._create(
        **values,
        digest="sha256:" + hashlib.sha256(
            _canonical_json(public_payload).encode("utf-8")
        ).hexdigest(),
        _origin_json=_canonical_json(origin),
    )


def bridge_pathway_observations(
    evidence: Path | Iterable[PathwayPolicyEvidenceBridge],
    *,
    profile: Any,
    plan: Any,
) -> tuple[PathwayEvidenceObservation, ...]:
    """Keep every active path visible when its policy is not decisive."""

    canonical_profile, canonical_plan, plan_digest = _canonical_observation_context(
        profile, plan
    )
    if isinstance(evidence, Path):
        normalized_evidence: Path | tuple[PathwayPolicyEvidenceBridge, ...] = evidence
    else:
        if isinstance(evidence, (str, bytes, bytearray)):
            raise TypeError(
                "pathway evidence must be a host-internal bundle Path or factory bridges"
            )
        try:
            normalized_evidence = tuple(evidence)
        except TypeError:
            raise TypeError("pathway evidence must be iterable") from None
        if any(
            type(item) is not PathwayPolicyEvidenceBridge
            for item in normalized_evidence
        ):
            raise TypeError("pathway observations accept only factory bridges")
    projections = _pathway_projections(
        normalized_evidence,
        profile_digest=canonical_profile.digest,
        query_plan_digest=plan_digest,
        province=canonical_profile.province,
        subject_mode=canonical_profile.subject_mode,
        target_year=canonical_plan.research_year,
    )
    policies = bridge_pathway_policies(
        normalized_evidence,
        province=canonical_profile.province,
        subject_mode=canonical_profile.subject_mode,
        target_year=canonical_plan.research_year,
        expected_profile_digest=canonical_profile.digest,
        expected_query_plan_digest=plan_digest,
    )
    task_by_id = {item.task_id: item for item in canonical_plan.tasks}
    accepted_identities = {
        (
            task_by_id[item._authenticated_projection.query_task_id].kind,
            task_by_id[item._authenticated_projection.query_task_id].target_name,
        )
        for item in policies
    }
    tasks_by_identity: dict[tuple[str, str], list[Any]] = {}
    for task in canonical_plan.tasks:
        if task.target_name in _TARGETS:
            tasks_by_identity.setdefault((task.kind, task.target_name), []).append(task)
    projections_by_identity: dict[
        tuple[str, str], list[PathwayPolicyProjection]
    ] = {}
    for projection in projections:
        task = task_by_id.get(projection.query_task_id)
        if task is None or task.target_name not in _TARGETS:
            raise PathwayBridgeError(
                "pathway projection is detached from its planned target"
            )
        projections_by_identity.setdefault((task.kind, task.target_name), []).append(
            projection
        )
    return tuple(
        _build_pathway_observation(
            profile=canonical_profile,
            plan=canonical_plan,
            query_plan_digest=plan_digest,
            kind=kind,
            title=title,
            tasks=tuple(tasks_by_identity[(kind, title)]),
            projections=tuple(projections_by_identity.get((kind, title), ())),
        )
        for kind, title in sorted(tasks_by_identity)
        if (kind, title) not in accepted_identities
    )


def validate_pathway_evidence_observation(
    observation: PathwayEvidenceObservation,
    profile: Any,
    plan: Any,
) -> PathwayEvidenceObservation:
    """Replay the sealed projection set and reject caller-authored observations."""

    if type(observation) is not PathwayEvidenceObservation:
        raise TypeError("observation must be a PathwayEvidenceObservation")
    canonical_profile, canonical_plan, plan_digest = _canonical_observation_context(
        profile, plan
    )
    try:
        origin = json.loads(observation._origin_json)
        identity = origin["identity"]
        raw_projections = origin["projections"]
    except (AttributeError, KeyError, TypeError, ValueError):
        raise PathwayBridgeError("pathway observation origin is invalid") from None
    if (
        not isinstance(identity, dict)
        or identity.get("profile_digest") != canonical_profile.digest
        or identity.get("query_plan_digest") != plan_digest
        or identity.get("kind") is None
        or identity.get("title") not in _TARGETS
        or not isinstance(raw_projections, list)
    ):
        raise PathwayBridgeError("pathway observation origin is detached")
    tasks = tuple(
        item
        for item in canonical_plan.tasks
        if (item.kind, item.target_name)
        == (identity["kind"], identity["title"])
    )
    if not tasks:
        raise PathwayBridgeError("pathway observation target is not active")
    try:
        projections = tuple(
            replay_pathway_policy_projection(item) for item in raw_projections
        )
    except (TypeError, ValueError):
        raise PathwayBridgeError(
            "pathway observation projections cannot be replayed"
        ) from None
    if any(
        item.profile_digest != canonical_profile.digest
        or item.query_plan_digest != plan_digest
        or item.query_task_id not in {task.task_id for task in tasks}
        for item in projections
    ):
        raise PathwayBridgeError("pathway observation projection context disagrees")
    rebuilt = _build_pathway_observation(
        profile=canonical_profile,
        plan=canonical_plan,
        query_plan_digest=plan_digest,
        kind=identity["kind"],
        title=identity["title"],
        tasks=tasks,
        projections=projections,
    )
    if (
        rebuilt.to_dict() != observation.to_dict()
        or rebuilt._origin_json != observation._origin_json
    ):
        raise PathwayBridgeError("pathway observation no longer matches its origin")
    if observation.evidence_status in _ACCEPTED:
        raise PathwayBridgeError("accepted policy cannot be an observation")
    if (
        observation.evidence_status is EvidenceStatus.CONFLICT
        and not observation.source_ids
    ):
        raise PathwayBridgeError("conflict observation requires real sources")
    if not observation.projection_digests and (
        observation.evidence_status is not EvidenceStatus.MISSING
        or observation.source_ids
    ):
        raise PathwayBridgeError("empty observation must remain source-free missing evidence")
    return rebuilt


__all__ = [
    "PathwayBridgeError",
    "PathwayEvidenceObservation",
    "PathwayPolicyEvidenceBridge",
    "bridge_pathway_observations",
    "bridge_pathway_policies",
    "bridge_pathway_policy_evidence",
    "validate_authenticated_domain_policy",
    "validate_pathway_evidence_observation",
    "validate_pathway_policy_evidence_bridge",
]
