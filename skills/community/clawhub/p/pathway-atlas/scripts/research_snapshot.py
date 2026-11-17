"""Build a path-neutral runtime province dataset from authenticated evidence."""

from __future__ import annotations

from dataclasses import dataclass, fields
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

if __package__:
    from .adapters.admission_bridge import (
        AdmissionEvidenceBridge,
        validate_admission_evidence_bridge,
    )
    from .adapters.rank_bridge import (
        RankEvidenceBridge,
        _replay_rank_evidence_fact,
        validate_rank_evidence_bridge,
    )
    from .adapters.school_fit_bridge import (
        _PERSISTED_ORIGIN_KIND,
        _replay_persisted_school_fit_evidence_fact,
        SchoolFitEvidenceBridge,
        merge_school_fit_metadata,
        validate_school_fit_evidence_bridge,
    )
    from .contracts import EvidenceStatus
    from .decision_policy import DecisionPolicySnapshot
    from .planning_profile import PlanningProfile
    from .province_registry import ProvinceConfig, canonical_discovery_subject_key, discovery_subjects_33
    from .query_plan import QueryPlan, validate_query_plan_payload
    from .validate_data import (
        RuntimeCalculationPolicy,
        ValidatedAdmissionRow,
        ValidatedScoreRow,
        admission_row_hash,
        validate_runtime_admission_row,
        validate_runtime_score_row,
    )
    from .validate_evidence import (
        ValidatedEvidenceSnapshot,
        validate_bundle_snapshot,
    )
    from .year_fallback import year_window
else:  # pragma: no cover - flat scripts-path compatibility
    from adapters.admission_bridge import (  # type: ignore
        AdmissionEvidenceBridge,
        validate_admission_evidence_bridge,
    )
    from adapters.rank_bridge import (  # type: ignore
        RankEvidenceBridge,
        _replay_rank_evidence_fact,
        validate_rank_evidence_bridge,
    )
    from adapters.school_fit_bridge import (  # type: ignore
        _PERSISTED_ORIGIN_KIND,
        _replay_persisted_school_fit_evidence_fact,
        SchoolFitEvidenceBridge,
        merge_school_fit_metadata,
        validate_school_fit_evidence_bridge,
    )
    from contracts import EvidenceStatus  # type: ignore
    from decision_policy import DecisionPolicySnapshot  # type: ignore
    from planning_profile import PlanningProfile  # type: ignore
    from province_registry import ProvinceConfig, canonical_discovery_subject_key, discovery_subjects_33  # type: ignore
    from query_plan import QueryPlan, validate_query_plan_payload  # type: ignore
    from validate_data import (  # type: ignore
        RuntimeCalculationPolicy,
        ValidatedAdmissionRow,
        ValidatedScoreRow,
        admission_row_hash,
        validate_runtime_admission_row,
        validate_runtime_score_row,
    )
    from validate_evidence import (  # type: ignore
        ValidatedEvidenceSnapshot,
        validate_bundle_snapshot,
    )
    from year_fallback import year_window  # type: ignore


_ACCEPTED = frozenset(
    {EvidenceStatus.OFFICIAL, EvidenceStatus.CORROBORATED, EvidenceStatus.REFERENCE}
)
_SCORE_TABLE_KINDS = frozenset(
    {"official_score_table", "score_table_reference"}
)
_ADMISSION_COVERAGE = _ACCEPTED | frozenset({EvidenceStatus.PARTIAL})
_ADMISSION_COMPATIBILITY_FIELDS = (
    "year",
    "province",
    "subject_group",
    "school_code",
    "program_group",
    "remarks",
    "min_score",
    "min_rank",
)


class ResearchSnapshotError(ValueError):
    """Authenticated inputs cannot form one coherent province snapshot."""


def _digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _score_scale(profile: PlanningProfile) -> int:
    values = {
        item.max_score
        for item in profile.rank_observations
        if item.max_score is not None
    }
    if (
        len(values) != 1
        or not isinstance(next(iter(values)), int)
        or isinstance(next(iter(values)), bool)
    ):
        raise ResearchSnapshotError("profile does not provide one exact score scale")
    value = next(iter(values))
    if not 100 <= value <= 1000:
        raise ResearchSnapshotError("profile score scale is outside the supported range")
    return value


def _score_row_from_rank_fact(
    fact: dict[str, Any],
    *,
    evidence_status: EvidenceStatus,
    score_scale: int,
    subject_group: str,
    allowed_years: tuple[int, ...],
) -> ValidatedScoreRow | None:
    value = fact["value"]
    kind = value.get("kind")
    if kind not in _SCORE_TABLE_KINDS:
        return None
    try:
        coverage_status = EvidenceStatus(value["coverage_status"])
    except (KeyError, TypeError, ValueError):
        raise ResearchSnapshotError("score row coverage status is invalid") from None
    if coverage_status not in _ACCEPTED:
        raise ResearchSnapshotError("score rows require accepted extraction coverage")
    if kind == "official_score_table":
        if (
            evidence_status is not EvidenceStatus.OFFICIAL
            or coverage_status is not EvidenceStatus.OFFICIAL
        ):
            raise ResearchSnapshotError(
                "official score rows require official evidence and coverage"
            )
    elif evidence_status not in {
        EvidenceStatus.CORROBORATED,
        EvidenceStatus.REFERENCE,
    }:
        raise ResearchSnapshotError(
            "reference score rows require corroborated or reference evidence"
        )
    return validate_runtime_score_row(
        {
            "year": value["year"],
            "score": value["score"],
            "rank": value["rank"],
            "cumulative_count": value["cumulative_count"],
            "subject_group": value["subject_group"],
        },
        score_scale=score_scale,
        subject_group=subject_group,
        allowed_years=allowed_years,
    )


def _runtime_config(
    profile: PlanningProfile,
    plan: QueryPlan,
    policy: DecisionPolicySnapshot,
    score_scale: int,
) -> ProvinceConfig:
    if plan.mode == "3+1+2":
        primary = ("物理", "历史")
        secondary = ("化学", "生物", "政治", "地理")
    else:
        primary = discovery_subjects_33(province=plan.province)
        secondary = ()
    calculation = RuntimeCalculationPolicy(
        policy_id=policy.policy_id,
        basis_id=policy.basis.basis_id,
        tier_caps=policy.scenario.tier_caps,
    )
    # ProvinceConfig is the established downstream metadata interface.  Its
    # policy slot deliberately carries the explicit runtime "unavailable"
    # projection instead of fabricating ordinary-batch rank deltas.
    return ProvinceConfig(
        province=profile.province,
        mode=plan.mode,
        primary_subjects=primary,
        secondary_subjects=secondary,
        score_scale=score_scale,
        schema_version="1.0",
        ordinary_batch_policy=calculation,  # type: ignore[arg-type]
        directory=Path("."),
    )


def _config_dict(config: ProvinceConfig) -> dict[str, Any]:
    return {
        "province": config.province,
        "mode": config.mode,
        "primary_subjects": list(config.primary_subjects),
        "secondary_subjects": list(config.secondary_subjects),
        "score_scale": config.score_scale,
        "schema_version": config.schema_version,
        "calculation_policy": config.ordinary_batch_policy.to_dict(),
        "directory_identity": "in-memory",
    }


def _admission_row_from_fact(
    fact: dict[str, Any],
    *,
    tasks: dict[str, Any],
    province: str,
    subject_group: str,
    score_scale: int,
    allowed_years: tuple[int, ...],
) -> tuple[ValidatedAdmissionRow, EvidenceStatus, Any]:
    """Authenticate the canonical full-row projection used for replay."""

    fact_id = fact.get("fact_id")
    field = fact.get("field")
    value = fact.get("value")
    if (
        not isinstance(fact_id, str)
        or field != f"admission_record:{fact_id}"
        or not isinstance(value, dict)
    ):
        raise ResearchSnapshotError("admission fact shape is invalid")
    try:
        status = EvidenceStatus(fact["status"])
    except (KeyError, TypeError, ValueError):
        raise ResearchSnapshotError("admission fact evidence status is invalid") from None
    if status not in _ACCEPTED:
        raise ResearchSnapshotError("admission evidence status is not accepted")
    task_note = fact.get("notes")
    if not isinstance(task_note, str) or not task_note.startswith("query_task:"):
        raise ResearchSnapshotError("admission fact lacks its query task binding")
    task_id = task_note.removeprefix("query_task:")
    task = tasks.get(task_id)
    if (
        task is None
        or task.kind != "batch_admission"
        or task.target_name != "普通批"
        or task.year not in allowed_years
    ):
        raise ResearchSnapshotError("admission fact query task binding is invalid")

    projection = value.get("dataset_row")
    if not isinstance(projection, dict):
        raise ResearchSnapshotError("admission fact lacks its canonical dataset row")
    try:
        row = validate_runtime_admission_row(
            projection,
            province=province,
            subject_group=subject_group,
            score_scale=score_scale,
            allowed_years=allowed_years,
        )
    except (KeyError, TypeError, ValueError):
        raise ResearchSnapshotError("admission fact canonical row is invalid") from None
    if row.year != task.year or value.get("row_hash") != admission_row_hash(row):
        raise ResearchSnapshotError("admission fact row hash or year binding disagrees")
    if any(value.get(name) != projection.get(name) for name in _ADMISSION_COMPATIBILITY_FIELDS):
        raise ResearchSnapshotError("admission compatibility fields diverge from canonical row")
    try:
        coverage_status = EvidenceStatus(value["coverage_status"])
    except (KeyError, TypeError, ValueError):
        raise ResearchSnapshotError("admission coverage status is invalid") from None
    lower_rank = value.get("coverage_min_rank")
    upper_rank = value.get("coverage_max_rank")
    if (
        coverage_status not in _ADMISSION_COVERAGE
        or not isinstance(lower_rank, int)
        or isinstance(lower_rank, bool)
        or not isinstance(upper_rank, int)
        or isinstance(upper_rank, bool)
        or not 1 <= lower_rank <= row.min_rank <= upper_rank
    ):
        raise ResearchSnapshotError("admission fact coverage binding is invalid")
    return row, status, task


@dataclass(frozen=True, init=False)
class ProvinceResearchSnapshot:
    """Factory-only in-memory dataset bound to profile, plan, evidence and policy."""

    profile_digest: str
    query_plan_digest: str
    research_year: int
    evidence_digest: str
    policy_id: str
    policy_digest: str
    calculation_policy_status: str
    config: ProvinceConfig
    admission_rows: tuple[ValidatedAdmissionRow, ...]
    score_rows: tuple[ValidatedScoreRow, ...]
    _rank_fact_json: tuple[str, ...]
    _admission_fact_json: tuple[str, ...]
    _school_fit_fact_json: tuple[str, ...]
    digest: str

    def __init__(self) -> None:
        raise TypeError("ProvinceResearchSnapshot is factory-only")

    @classmethod
    def _create(cls, **values: Any) -> "ProvinceResearchSnapshot":
        if set(values) != {item.name for item in fields(cls)}:
            raise TypeError("research snapshot factory fields do not match the contract")
        instance = object.__new__(cls)
        for name, value in values.items():
            object.__setattr__(instance, name, value)
        return instance

    @property
    def rank_facts(self) -> tuple[dict[str, Any], ...]:
        return tuple(json.loads(item) for item in self._rank_fact_json)

    @property
    def admission_facts(self) -> tuple[dict[str, Any], ...]:
        return tuple(json.loads(item) for item in self._admission_fact_json)

    @property
    def school_fit_facts(self) -> tuple[dict[str, Any], ...]:
        return tuple(json.loads(item) for item in self._school_fit_fact_json)

    def to_dict(self) -> dict[str, Any]:
        return {
            "profile_digest": self.profile_digest,
            "query_plan_digest": self.query_plan_digest,
            "research_year": self.research_year,
            "evidence_digest": self.evidence_digest,
            "policy_id": self.policy_id,
            "policy_digest": self.policy_digest,
            "calculation_policy_status": self.calculation_policy_status,
            "config": _config_dict(self.config),
            "admission_rows": [item.to_dict() for item in self.admission_rows],
            "score_rows": [item.to_dict() for item in self.score_rows],
            "rank_facts": list(self.rank_facts),
            "admission_facts": list(self.admission_facts),
            "school_fit_facts": list(self.school_fit_facts),
            "digest": self.digest,
        }


def build_research_snapshot(
    profile: PlanningProfile,
    plan: QueryPlan,
    evidence: Iterable[
        RankEvidenceBridge | AdmissionEvidenceBridge | SchoolFitEvidenceBridge
    ] | Path,
    policy: DecisionPolicySnapshot,
) -> ProvinceResearchSnapshot:
    """Build from factory bridges or a host-internal bundle artifact reference.

    A path is an internal Task-4 handoff. It is never a user- or Skill-supplied
    value, and its bundle is freshly validated and consumed within this call.
    """

    if not isinstance(profile, PlanningProfile):
        raise TypeError("profile must be a PlanningProfile")
    if type(plan) is not QueryPlan:
        raise TypeError("plan must be a canonical QueryPlan")
    if type(policy) is not DecisionPolicySnapshot:
        raise TypeError("policy must be a strict DecisionPolicySnapshot")
    validated_evidence: ValidatedEvidenceSnapshot | None = None
    if isinstance(evidence, Path):
        validation = validate_bundle_snapshot(evidence, _allow_empty=True)
        if validation.snapshot is None or validation.issues:
            raise ResearchSnapshotError(
                "host-internal evidence bundle validation failed"
            )
        validated_evidence = validation.snapshot
        items: tuple[
            RankEvidenceBridge | AdmissionEvidenceBridge | SchoolFitEvidenceBridge,
            ...,
        ] = ()
        persisted_facts = tuple(
            item.to_dict() for item in validated_evidence.facts
        )
    elif type(evidence) is ValidatedEvidenceSnapshot:
        raise TypeError(
            "evidence snapshots are not accepted; use a host-internal bundle reference"
        )
    else:
        if isinstance(evidence, (str, bytes, bytearray)):
            raise TypeError("evidence must contain authenticated bridges")
        items = tuple(evidence)
        if not items:
            raise ResearchSnapshotError("authenticated research evidence is empty")
        if any(
            type(item)
            not in {
                RankEvidenceBridge,
                AdmissionEvidenceBridge,
                SchoolFitEvidenceBridge,
            }
            for item in items
        ):
            raise TypeError("evidence accepts only factory evidence bridges")
        persisted_facts = ()
    try:
        canonical_plan = validate_query_plan_payload(plan.to_dict())
    except (KeyError, TypeError, ValueError):
        raise ResearchSnapshotError("plan is not a canonical validated query plan") from None
    if canonical_plan.to_dict() != plan.to_dict():
        raise ResearchSnapshotError("plan is not a canonical validated query plan")
    expected_subject = canonical_discovery_subject_key(
        profile.subject_mode,
        profile.subject_group,
        profile.secondary_subjects,
        province=profile.province,
    )
    if (
        profile.province != plan.province
        or profile.exam_year != plan.exam_year
        or expected_subject != plan.subject_group
    ):
        raise ResearchSnapshotError("profile and query plan contexts disagree")
    plan_digest = _digest(plan.to_dict())
    policy_digest = _digest(policy.to_dict())
    if (
        plan.decision_policy_id != policy.policy_id
        or plan.decision_policy_digest != policy_digest
        or plan.decision_basis_id != policy.basis.basis_id
        or plan.decision_source_id != policy.basis.source_id
        or plan.decision_source_version != policy.basis.source_version
        or plan.source_policy_id != policy.source_policy.policy_id
        or plan.source_policy_version != policy.source_policy.version
    ):
        raise ResearchSnapshotError("decision policy does not match the query plan")
    score_scale = _score_scale(profile)
    allowed_years = year_window(plan.research_year)
    score_rows: list[ValidatedScoreRow] = []
    admission_rows: list[ValidatedAdmissionRow] = []
    rank_facts: list[dict[str, Any]] = []
    admission_facts: list[dict[str, Any]] = []
    school_fit_facts: list[dict[str, Any]] = []
    evidence_payload: list[dict[str, Any]] = []
    task_by_id = {task.task_id: task for task in plan.tasks}
    persisted_school_fit_origins: dict[str, list[dict[str, Any]]] = {}
    if validated_evidence is not None:
        for frozen_context in validated_evidence.contexts:
            context = frozen_context.to_dict()
            if context.get("kind") != _PERSISTED_ORIGIN_KIND:
                continue
            fact_id = context.get("fact_id")
            if not isinstance(fact_id, str):
                raise ResearchSnapshotError(
                    "persisted school-fit factory origin is invalid"
                )
            persisted_school_fit_origins.setdefault(fact_id, []).append(context)
    for item in items:
        if type(item) is RankEvidenceBridge:
            validate_rank_evidence_bridge(item, profile, plan)
            if item.query_plan_digest != plan_digest or item.profile_digest != profile.digest:
                raise ResearchSnapshotError("rank bridge dependency digests disagree")
            fact = item.fact.to_dict()
            rank_facts.append(fact)
            evidence_payload.append(item.to_dict())
            score_row = _score_row_from_rank_fact(
                fact,
                evidence_status=item.evidence_status,
                score_scale=score_scale,
                subject_group=plan.subject_group,
                allowed_years=allowed_years,
            )
            if score_row is not None:
                score_rows.append(score_row)
            continue

        if type(item) is SchoolFitEvidenceBridge:
            try:
                validate_school_fit_evidence_bridge(item, profile, plan)
            except (TypeError, ValueError):
                raise ResearchSnapshotError(
                    "school-fit bridge does not replay from its authenticated inputs"
                ) from None
            bound_task = task_by_id.get(item.task.task_id)
            if (
                item.profile_digest != profile.digest
                or item.query_plan_digest != plan_digest
                or bound_task is None
                or bound_task.to_dict() != item.task.to_dict()
            ):
                raise ResearchSnapshotError(
                    "school-fit bridge dependency bindings disagree"
                )
            school_fit_facts.append(item.fact.to_dict())
            evidence_payload.append(item.to_dict())
            continue

        try:
            validate_admission_evidence_bridge(item)
        except (TypeError, ValueError):
            raise ResearchSnapshotError(
                "admission bridge does not replay from its authenticated inputs"
            ) from None
        fact = item.fact
        fact_dict = fact.to_dict()
        row, status, task = _admission_row_from_fact(
            fact_dict,
            tasks=task_by_id,
            province=plan.province,
            subject_group=plan.subject_group,
            score_scale=score_scale,
            allowed_years=allowed_years,
        )
        if (
            task is not item.task
            or row.to_dict() != item.dataset_row.to_dict()
            or status is not item.evidence_status
            or fact.value["row_hash"] != item.admission_row_hash
            or fact.notes != f"query_task:{item.task.task_id}"
            or fact.status is not item.evidence_status
            or tuple(fact.source_ids) != item.source_ids
            or fact.value["coverage_status"] != item.coverage_status.value
            or fact.value["coverage_min_rank"] != item.extraction_coverage.lower_rank
            or fact.value["coverage_max_rank"] != item.extraction_coverage.upper_rank
        ):
            raise ResearchSnapshotError("admission bridge projection was mutated")
        admission_rows.append(row)
        admission_facts.append(fact_dict)
        evidence_payload.append(item.to_dict())

    for fact in persisted_facts:
        field = fact.get("field")
        value = fact.get("value")
        if not isinstance(field, str):
            raise ResearchSnapshotError("validated evidence fact shape is invalid")
        if field.startswith("school_fit:"):
            origins = persisted_school_fit_origins.get(str(fact.get("fact_id")), ())
            if len(origins) != 1:
                raise ResearchSnapshotError(
                    "school-fit fact lacks exactly one factory origin receipt"
                )
            try:
                rebuilt = _replay_persisted_school_fit_evidence_fact(
                    fact, origins[0], profile, plan
                )
            except (KeyError, TypeError, ValueError):
                raise ResearchSnapshotError(
                    "school-fit fact does not replay from its authenticated typed bridge"
                ) from None
            school_fit_facts.append(rebuilt.fact.to_dict())
            continue
        if not field.startswith(("admission_record:", "rank_channel:", "rank_anchor:")):
            continue
        if not isinstance(value, dict):
            raise ResearchSnapshotError("validated evidence fact shape is invalid")
        if field.startswith("admission_record:"):
            row, _status, _task = _admission_row_from_fact(
                fact,
                tasks=task_by_id,
                province=plan.province,
                subject_group=plan.subject_group,
                score_scale=score_scale,
                allowed_years=allowed_years,
            )
            admission_rows.append(row)
            admission_facts.append(fact)
            continue
        try:
            rebuilt = _replay_rank_evidence_fact(fact, profile, plan)
        except (KeyError, TypeError, ValueError):
            raise ResearchSnapshotError(
                "rank fact does not replay from its authenticated typed input"
            ) from None
        fact = rebuilt.fact.to_dict()
        status = rebuilt.evidence_status
        rank_facts.append(fact)
        score_row = _score_row_from_rank_fact(
            fact,
            evidence_status=status,
            score_scale=score_scale,
            subject_group=plan.subject_group,
            allowed_years=allowed_years,
        )
        if score_row is not None:
            score_rows.append(score_row)

    admission_rows = list(
        merge_school_fit_metadata(
            tuple(admission_rows),
            tuple(school_fit_facts),
            profile=profile,
            plan=plan,
        )
    )

    score_keys = [
        (row.to_dict()["year"], row.to_dict()["score"], row.to_dict()["subject_group"])
        for row in score_rows
    ]
    if len(score_keys) != len(set(score_keys)):
        raise ResearchSnapshotError("research evidence contains duplicate score rows")
    admission_hashes = [admission_row_hash(row) for row in admission_rows]
    if len(admission_hashes) != len(set(admission_hashes)):
        raise ResearchSnapshotError("research evidence contains duplicate admission rows")
    score_rows.sort(key=lambda row: (-int(row.to_dict()["year"]), -int(row.to_dict()["score"])))
    admission_rows.sort(
        key=lambda row: (
            -int(row.to_dict()["year"]),
            str(row.to_dict()["school_code"]),
            str(row.to_dict()["program_group"]),
        )
    )
    rank_facts.sort(key=lambda fact: str(fact["fact_id"]))
    admission_facts.sort(key=lambda fact: str(fact["fact_id"]))
    school_fit_facts.sort(key=lambda fact: str(fact["fact_id"]))
    config = _runtime_config(profile, plan, policy, score_scale)
    evidence_digest = (
        validated_evidence.manifest_hash
        if validated_evidence is not None
        else _digest(evidence_payload)
    )
    rank_fact_json = tuple(
        json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
        for item in rank_facts
    )
    admission_fact_json = tuple(
        json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
        for item in admission_facts
    )
    school_fit_fact_json = tuple(
        json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
        for item in school_fit_facts
    )
    core = {
        "profile_digest": profile.digest,
        "query_plan_digest": plan_digest,
        "research_year": plan.research_year,
        "evidence_digest": evidence_digest,
        "policy_id": policy.policy_id,
        "policy_digest": policy_digest,
        "calculation_policy_status": "rank_delta_policy_unavailable",
        "config": _config_dict(config),
        "admission_rows": [item.to_dict() for item in admission_rows],
        "score_rows": [item.to_dict() for item in score_rows],
        "rank_facts": rank_facts,
        "admission_facts": admission_facts,
        "school_fit_facts": school_fit_facts,
    }
    return ProvinceResearchSnapshot._create(
        profile_digest=profile.digest,
        query_plan_digest=plan_digest,
        research_year=plan.research_year,
        evidence_digest=evidence_digest,
        policy_id=policy.policy_id,
        policy_digest=policy_digest,
        calculation_policy_status="rank_delta_policy_unavailable",
        config=config,
        admission_rows=tuple(admission_rows),
        score_rows=tuple(score_rows),
        _rank_fact_json=rank_fact_json,
        _admission_fact_json=admission_fact_json,
        _school_fit_fact_json=school_fit_fact_json,
        digest=_digest(core),
    )


def validate_research_snapshot(
    snapshot: ProvinceResearchSnapshot,
    profile: PlanningProfile,
) -> ProvinceResearchSnapshot:
    """Verify the immutable calculation handoff before a consumer uses it."""

    if type(snapshot) is not ProvinceResearchSnapshot:
        raise TypeError("research_snapshot must be a ProvinceResearchSnapshot")
    if not isinstance(profile, PlanningProfile) or snapshot.profile_digest != profile.digest:
        raise ResearchSnapshotError("research snapshot is not bound to this profile")
    if snapshot.config.directory != Path("."):
        raise ResearchSnapshotError("research snapshot directory identity is not in-memory")
    payload = snapshot.to_dict()
    supplied = payload.pop("digest")
    if supplied != _digest(payload):
        raise ResearchSnapshotError("research snapshot digest does not match its content")
    if snapshot.calculation_policy_status != "rank_delta_policy_unavailable":
        raise ResearchSnapshotError("research snapshot calculation policy status is invalid")
    return snapshot


__all__ = [
    "ProvinceResearchSnapshot",
    "ResearchSnapshotError",
    "build_research_snapshot",
    "validate_research_snapshot",
]
