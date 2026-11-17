"""Recoverable, host-neutral planning-session orchestration.

The immutable state machine is the only public seam.  Hosts execute declared
research work; this module performs no network operation and snapshots only
canonical machine state.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, fields
from enum import Enum
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from typing import Any, Mapping, Sequence

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from contracts import CapabilityReport
else:
    from .contracts import CapabilityReport


_SCHEMA_VERSION = "1.0"
_MAX_SNAPSHOT_BYTES = 1024 * 1024
_MAX_REPLAY_JOURNAL_BYTES = 16 * 1024 * 1024
_SESSION_ID = re.compile(r"[0-9a-f]{32}")
_DIGEST = re.compile(r"sha256:[0-9a-f]{64}")
_TASK_ID = re.compile(r"[a-z][a-z0-9-]*:[0-9a-f]{24}")
_UNAVAILABLE_REASONS = frozenset(
    {
        "current_year_not_published",
        "source_threshold_not_met",
        "source_conflict",
        "network_unavailable",
        "capability_unavailable",
        "newer_comparable_year_accepted",
    }
)
_CLI_UNAVAILABLE_REASONS = tuple(
    sorted(_UNAVAILABLE_REASONS - {"newer_comparable_year_accepted"})
)
_PREFLIGHT_DEGRADATION_MAP = {
    "browse": "missing_browse",
    "docx": "missing_docx",
    "openpyxl": "missing_openpyxl",
    "pdfplumber": "missing_pdfplumber",
    "python>=3.10": "unsupported_python",
    "search": "missing_search",
    "vision": "missing_vision",
}
_PREFLIGHT_DEGRADATION_CODES = frozenset(_PREFLIGHT_DEGRADATION_MAP.values())
_SNAPSHOT_NAME = re.compile(r"([0-9a-f]{32})\.([0-9]{8})\.json")
_REPLAY_JOURNAL_NAME = re.compile(
    r"([0-9a-f]{32})\.([0-9]{8})\.replay\.json"
)


class PlanningSessionInputError(ValueError):
    """A snapshot or transition value violates the public contract."""


class SessionTransitionError(PlanningSessionInputError):
    """A command is stale, replayed, forged, or out of order."""


class PlanningSessionStoreError(OSError):
    """Path-neutral persistence failure with a controlled reason code."""

    def __init__(self, reason_code: str) -> None:
        self.reason_code = reason_code
        super().__init__(f"planning-session storage error: {reason_code}")


class SessionStage(str, Enum):
    INTAKE = "intake"
    PROFILE_CONFIRMED = "profile_confirmed"
    PREFLIGHT_COMPLETE = "preflight_complete"
    QUERY_PLAN_READY = "query_plan_ready"
    RESEARCH_IN_PROGRESS = "research_in_progress"
    EVIDENCE_FINALIZED = "evidence_finalized"
    CALCULATION_COMPLETE = "calculation_complete"
    REPORT_PUBLISHED = "report_published"


_STAGE_ORDER = tuple(SessionStage)
_STATE_FIELDS = (
    "session_id",
    "revision",
    "stage",
    "profile_digest",
    "preflight_digest",
    "preflight_degradation_codes",
    "query_plan_digest",
    "expected_task_ids",
    "completed_task_ids",
    "completed_artifact_digests",
    "completed_provenance_digests",
    "completed_usable_flags",
    "completed_receipt_digests",
    "unavailable_task_ids",
    "unavailable_reason_codes",
    "evidence_manifest_hash",
    "evidence_receipt_digest",
    "calculation_digest",
    "calculation_receipt_digest",
    "report_digest",
    "publication_receipt_digest",
)
_SERIALIZED_FIELDS = frozenset(("schema_version", "session_digest", *_STATE_FIELDS))
PreflightReport = CapabilityReport


@dataclass(frozen=True, init=False)
class TaskEvidenceOutcome:
    """Factory-only completed-task result replayed from typed evidence bridges."""

    task_id: str
    profile_digest: str
    query_plan_digest: str
    kind: str
    target_name: str | None
    year: int
    artifact_digest: str
    provenance_digest: str
    evidence_statuses: tuple[str, ...]
    usable: bool
    receipt_digest: str
    _bridges: tuple[Any, ...]

    def __init__(self) -> None:
        raise TypeError("TaskEvidenceOutcome is factory-only")

    @classmethod
    def _create(cls, **values: Any) -> "TaskEvidenceOutcome":
        instance = object.__new__(cls)
        for name, value in values.items():
            object.__setattr__(instance, name, value)
        return instance

    def _payload(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "profile_digest": self.profile_digest,
            "query_plan_digest": self.query_plan_digest,
            "kind": self.kind,
            "target_name": self.target_name,
            "year": self.year,
            "artifact_digest": self.artifact_digest,
            "provenance_digest": self.provenance_digest,
            "evidence_statuses": list(self.evidence_statuses),
            "usable": self.usable,
        }

    def validate(self, profile: Any, query_plan: Any) -> "TaskEvidenceOutcome":
        if type(self) is not TaskEvidenceOutcome:
            raise TypeError("evidence_outcome must be a TaskEvidenceOutcome")
        if not isinstance(self.task_id, str) or _TASK_ID.fullmatch(self.task_id) is None:
            raise PlanningSessionInputError("evidence outcome task is invalid")
        _require_digest(self.query_plan_digest, "evidence outcome query plan")
        _require_digest(self.profile_digest, "evidence outcome profile")
        _require_digest(self.artifact_digest, "evidence outcome artifact")
        _require_digest(self.provenance_digest, "evidence outcome provenance")
        accepted = {"official", "corroborated", "reference"}
        if (
            not self.evidence_statuses
            or any(
                item not in accepted | {"conflict", "missing", "masked", "partial"}
                for item in self.evidence_statuses
            )
            or not isinstance(self.usable, bool)
            or self.receipt_digest != _digest_payload(self._payload())
        ):
            raise PlanningSessionInputError("evidence outcome is not canonical")
        canonical_profile = _validated_profile(profile)
        plan_identity, canonical_plan = _validated_query_plan(query_plan)
        _validate_profile_plan_context(canonical_profile, canonical_plan)
        task = next(
            (
                item
                for item in canonical_plan.tasks
                if item.task_id == self.task_id
            ),
            None,
        )
        if (
            canonical_profile.digest != self.profile_digest
            or plan_identity != self.query_plan_digest
            or task is None
            or (task.kind, task.target_name, task.year)
            != (self.kind, self.target_name, self.year)
        ):
            raise SessionTransitionError(
                "evidence receipt does not match the planning context"
        )
        rebuilt = build_task_evidence_outcome(
            canonical_profile,
            canonical_plan,
            task,
            self._bridges,
            _validating=True,
        )
        if rebuilt._payload() != self._payload() or rebuilt.receipt_digest != self.receipt_digest:
            raise PlanningSessionInputError("evidence receipt no longer replays")
        return self


@dataclass(frozen=True, init=False)
class EvidenceManifestOutcome:
    """Factory-only evidence partition bound to a freshly replayed bundle."""

    planning_session_id: str
    profile_digest: str
    query_plan_digest: str
    expected_task_ids: tuple[str, ...]
    completed_task_ids: tuple[str, ...]
    completed_receipt_digests: tuple[str, ...]
    usable_task_ids: tuple[str, ...]
    unavailable_task_ids: tuple[str, ...]
    unavailable_reason_codes: tuple[str, ...]
    manifest_session_id: str
    manifest_hash: str
    facts_digest: str
    receipt_digest: str
    _bundle_path: Path | None
    _task_outcomes: tuple[TaskEvidenceOutcome, ...]
    _capability: CapabilityReport
    _snapshot: Any | None

    def __init__(self) -> None:
        raise TypeError("EvidenceManifestOutcome is factory-only")

    @classmethod
    def _create(cls, **values: Any) -> "EvidenceManifestOutcome":
        instance = object.__new__(cls)
        for name, value in values.items():
            object.__setattr__(instance, name, value)
        return instance

    def _payload(self) -> dict[str, Any]:
        return {
            "planning_session_id": self.planning_session_id,
            "profile_digest": self.profile_digest,
            "query_plan_digest": self.query_plan_digest,
            "expected_task_ids": list(self.expected_task_ids),
            "completed_task_ids": list(self.completed_task_ids),
            "completed_receipt_digests": list(self.completed_receipt_digests),
            "usable_task_ids": list(self.usable_task_ids),
            "unavailable_task_ids": list(self.unavailable_task_ids),
            "unavailable_reason_codes": list(self.unavailable_reason_codes),
            "manifest_session_id": self.manifest_session_id,
            "manifest_hash": self.manifest_hash,
            "facts_digest": self.facts_digest,
        }

    def validate(
        self,
        session: Any,
        profile: Any,
        query_plan: Any,
    ) -> "EvidenceManifestOutcome":
        if type(self) is not EvidenceManifestOutcome:
            raise TypeError("evidence manifest must be an EvidenceManifestOutcome")
        if self.receipt_digest != _digest_payload(self._payload()):
            raise PlanningSessionInputError("evidence manifest receipt is not canonical")
        rebuilt = build_evidence_manifest_outcome(
            session,
            profile,
            query_plan,
            bundle_path=self._bundle_path,
            task_outcomes=self._task_outcomes,
            capability_report=self._capability,
            _validating=True,
        )
        if (
            rebuilt._payload() != self._payload()
            or rebuilt.receipt_digest != self.receipt_digest
        ):
            raise PlanningSessionInputError("evidence manifest no longer replays")
        return self


@dataclass(frozen=True, init=False)
class CalculationOutcome:
    """Factory-only replay of research, rank, school, pathway, and report logic."""

    evidence_receipt_digest: str
    research_snapshot_digest: str
    rank_scenario_digest: str
    recommendation_result_digest: str
    pathway_result_digest: str
    report_model_digest: str
    degraded: bool
    receipt_digest: str
    _evidence_outcome: EvidenceManifestOutcome
    _policy: Any
    _research_snapshot: Any
    _model: Any

    def __init__(self) -> None:
        raise TypeError("CalculationOutcome is factory-only")

    @classmethod
    def _create(cls, **values: Any) -> "CalculationOutcome":
        instance = object.__new__(cls)
        for name, value in values.items():
            object.__setattr__(instance, name, value)
        return instance

    @property
    def model(self) -> Any:
        return self._model

    @property
    def research_snapshot(self) -> Any:
        return self._research_snapshot

    def _payload(self) -> dict[str, Any]:
        return {
            "evidence_receipt_digest": self.evidence_receipt_digest,
            "research_snapshot_digest": self.research_snapshot_digest,
            "rank_scenario_digest": self.rank_scenario_digest,
            "recommendation_result_digest": self.recommendation_result_digest,
            "pathway_result_digest": self.pathway_result_digest,
            "report_model_digest": self.report_model_digest,
            "degraded": self.degraded,
        }

    def validate(
        self,
        session: Any,
        profile: Any,
        query_plan: Any,
    ) -> "CalculationOutcome":
        if type(self) is not CalculationOutcome:
            raise TypeError("calculation must be a CalculationOutcome")
        if self.receipt_digest != _digest_payload(self._payload()):
            raise PlanningSessionInputError("calculation receipt is not canonical")
        rebuilt = build_calculation_outcome(
            session,
            self._evidence_outcome,
            profile,
            query_plan,
            decision_policy=self._policy,
            _validating=True,
        )
        if (
            rebuilt._payload() != self._payload()
            or rebuilt.receipt_digest != self.receipt_digest
            or rebuilt.research_snapshot.to_dict()
            != self.research_snapshot.to_dict()
            or rebuilt.model.to_dict() != self.model.to_dict()
        ):
            raise PlanningSessionInputError("calculation outcome no longer replays")
        return self


@dataclass(frozen=True, init=False)
class ReportPublicationOutcome:
    """Factory-rendered immutable publication bytes bound to one calculation."""

    format: str
    calculation_receipt_digest: str
    report_model_digest: str
    rendered_digest: str
    receipt_digest: str
    _calculation_outcome: CalculationOutcome
    _rendered_bytes: bytes

    def __init__(self) -> None:
        raise TypeError("ReportPublicationOutcome is factory-only")

    @classmethod
    def _create(cls, **values: Any) -> "ReportPublicationOutcome":
        instance = object.__new__(cls)
        for name, value in values.items():
            object.__setattr__(instance, name, value)
        return instance

    @property
    def markdown(self) -> str:
        if self.format != "markdown":
            raise TypeError("publication is not Markdown")
        return self._rendered_bytes.decode("utf-8")

    @property
    def rendered_bytes(self) -> bytes:
        """Return the exact immutable artifact authenticated by this receipt."""

        return self._rendered_bytes

    def _payload(self) -> dict[str, Any]:
        return {
            "format": self.format,
            "calculation_receipt_digest": self.calculation_receipt_digest,
            "report_model_digest": self.report_model_digest,
            "rendered_digest": self.rendered_digest,
        }

    def validate(
        self,
        session: Any,
        profile: Any,
        query_plan: Any,
    ) -> "ReportPublicationOutcome":
        if type(self) is not ReportPublicationOutcome:
            raise TypeError("publication must be a ReportPublicationOutcome")
        self._calculation_outcome.validate(session, profile, query_plan)
        if self.receipt_digest != _digest_payload(self._payload()):
            raise PlanningSessionInputError("publication receipt is not canonical")
        rebuilt = build_report_publication_outcome(
            self._calculation_outcome,
            format=self.format,
            _validating=True,
        )
        if (
            rebuilt._payload() != self._payload()
            or rebuilt.receipt_digest != self.receipt_digest
            or rebuilt._rendered_bytes != self._rendered_bytes
        ):
            raise PlanningSessionInputError("publication outcome no longer replays")
        return self


@dataclass(frozen=True)
class PlanningSessionReplayContext:
    """Private typed context rebuilt from a replay journal.

    The journal is never calculation authority by itself.  Each operation
    replays the task bridges, the retained evidence bundle, and every stage
    receipt before advancing the immutable session.
    """

    session: Any
    profile: Any
    query_plan: Any | None
    capability_report: CapabilityReport | None
    bundle_path: Path | None
    task_outcomes: tuple[TaskEvidenceOutcome, ...]

    def _evidence(self) -> EvidenceManifestOutcome:
        if (
            self.query_plan is None
            or self.capability_report is None
            or self.bundle_path is None
        ):
            raise SessionTransitionError("evidence replay context is incomplete")
        return build_evidence_manifest_outcome(
            self.session,
            self.profile,
            self.query_plan,
            bundle_path=self.bundle_path,
            task_outcomes=self.task_outcomes,
            capability_report=self.capability_report,
        )

    def validate(self) -> "PlanningSessionReplayContext":
        if type(self) is not PlanningSessionReplayContext:
            raise TypeError("replay context must be a PlanningSessionReplayContext")
        if type(self.session) is not PlanningSession:
            raise TypeError("replay context session must be a PlanningSession")
        self.session._at(
            SessionStage.PROFILE_CONFIRMED,
            SessionStage.PREFLIGHT_COMPLETE,
            SessionStage.QUERY_PLAN_READY,
            SessionStage.RESEARCH_IN_PROGRESS,
            SessionStage.EVIDENCE_FINALIZED,
            SessionStage.CALCULATION_COMPLETE,
        )
        canonical_profile = _validated_profile(self.profile)
        self.session._bound("profile_digest", canonical_profile.digest)
        if self.session.stage is SessionStage.PROFILE_CONFIRMED:
            if (
                self.capability_report is not None
                or self.query_plan is not None
                or self.bundle_path is not None
                or self.task_outcomes
            ):
                raise PlanningSessionInputError(
                    "profile-confirmed replay carries future context"
                )
            return self
        if self.capability_report is None:
            raise PlanningSessionInputError("replay capability is missing")
        capability_identity, _codes = _preflight_identity(self.capability_report)
        self.session._bound("preflight_digest", capability_identity)
        if self.session.stage is SessionStage.PREFLIGHT_COMPLETE:
            if (
                self.query_plan is not None
                or self.bundle_path is not None
                or self.task_outcomes
            ):
                raise PlanningSessionInputError(
                    "preflight replay carries future context"
                )
            return self
        if self.query_plan is None:
            raise PlanningSessionInputError("replay query plan is missing")
        canonical_profile, _identity, canonical_plan = _validated_planning_context(
            self.session,
            canonical_profile,
            self.query_plan,
            require_bound_universe=True,
        )
        outcomes = _validate_replay_task_ledger(
            self.session,
            canonical_profile,
            canonical_plan,
            self.task_outcomes,
        )
        if outcomes != self.task_outcomes:
            raise PlanningSessionInputError("replay task ledger is not canonical")
        if self.session.stage is SessionStage.QUERY_PLAN_READY:
            if self.bundle_path is not None or outcomes:
                raise PlanningSessionInputError(
                    "query-ready replay carries research context"
                )
            return self
        if not isinstance(self.bundle_path, Path):
            raise TypeError("replay bundle path must be a Path")
        _validate_private_bundle_path(self.bundle_path)
        if self.session.stage in {
            SessionStage.EVIDENCE_FINALIZED,
            SessionStage.CALCULATION_COMPLETE,
            SessionStage.REPORT_PUBLISHED,
        }:
            evidence = self._evidence()
            if self.session.stage in {
                SessionStage.CALCULATION_COMPLETE,
                SessionStage.REPORT_PUBLISHED,
            }:
                build_calculation_outcome(
                    self.session,
                    evidence,
                    canonical_profile,
                    canonical_plan,
                )
        return self

    def finalize_evidence(
        self,
    ) -> tuple[Any, EvidenceManifestOutcome]:
        self.validate()
        self.session._at(SessionStage.RESEARCH_IN_PROGRESS)
        evidence = self._evidence()
        advanced = self.session.finalize_evidence(
            evidence,
            query_plan=self.query_plan,
            profile=self.profile,
        )
        return advanced, evidence

    def calculate(self) -> tuple[Any, CalculationOutcome]:
        self.validate()
        self.session._at(SessionStage.EVIDENCE_FINALIZED)
        evidence = self._evidence()
        calculation = build_calculation_outcome(
            self.session,
            evidence,
            self.profile,
            self.query_plan,
        )
        advanced = self.session.with_calculation(
            calculation,
            query_plan=self.query_plan,
            profile=self.profile,
        )
        return advanced, calculation

    def publish(
        self,
        *,
        format: str = "markdown",
    ) -> tuple[Any, ReportPublicationOutcome]:
        self.validate()
        self.session._at(SessionStage.CALCULATION_COMPLETE)
        evidence = self._evidence()
        calculation = build_calculation_outcome(
            self.session,
            evidence,
            self.profile,
            self.query_plan,
        )
        publication = build_report_publication_outcome(
            calculation,
            format=format,
        )
        advanced = self.session.publish_report(
            publication,
            query_plan=self.query_plan,
            profile=self.profile,
        )
        return advanced, publication


def build_task_evidence_outcome(
    profile: Any,
    query_plan: Any,
    task: Any,
    bridges: Any,
    *,
    _validating: bool = False,
) -> TaskEvidenceOutcome:
    """Replay typed evidence bridges and derive usability without host authority."""

    plan_identity, canonical_plan = _validated_query_plan(query_plan)
    canonical_profile = _validated_profile(profile)
    _validate_profile_plan_context(canonical_profile, canonical_plan)
    profile_digest = canonical_profile.digest
    canonical_task = next(
        (
            item
            for item in canonical_plan.tasks
            if getattr(item, "task_id", None) == getattr(task, "task_id", None)
        ),
        None,
    )
    if canonical_task is None or canonical_task.to_dict() != task.to_dict():
        raise PlanningSessionInputError("evidence outcome task is outside the query plan")
    if isinstance(bridges, (str, bytes, bytearray)):
        raise TypeError("bridges must be typed evidence bridge records")
    try:
        records = tuple(bridges)
    except TypeError as error:
        raise TypeError("bridges must be typed evidence bridge records") from error
    if not records:
        raise PlanningSessionInputError("completed evidence outcome is empty")

    if __package__ in (None, ""):
        from scripts.adapters.admission_bridge import (
            AdmissionEvidenceBridge,
            validate_admission_evidence_bridge,
        )
        from scripts.adapters.pathway_bridge import (
            PathwayPolicyEvidenceBridge,
            validate_pathway_policy_evidence_bridge,
        )
        from scripts.adapters.rank_bridge import (
            RankEvidenceBridge,
            validate_rank_evidence_bridge,
        )
        from scripts.adapters.school_fit_bridge import (
            SchoolFitEvidenceBridge,
            validate_school_fit_evidence_bridge,
        )
    else:
        from .adapters.admission_bridge import (
            AdmissionEvidenceBridge,
            validate_admission_evidence_bridge,
        )
        from .adapters.pathway_bridge import (
            PathwayPolicyEvidenceBridge,
            validate_pathway_policy_evidence_bridge,
        )
        from .adapters.rank_bridge import RankEvidenceBridge, validate_rank_evidence_bridge
        from .adapters.school_fit_bridge import (
            SchoolFitEvidenceBridge,
            validate_school_fit_evidence_bridge,
        )

    statuses: list[str] = []
    provenance: list[dict[str, Any]] = []
    artifacts: list[dict[str, Any]] = []
    for bridge in records:
        if type(bridge) is RankEvidenceBridge:
            try:
                validate_rank_evidence_bridge(
                    bridge, canonical_profile, canonical_plan
                )
            except (TypeError, ValueError) as error:
                raise PlanningSessionInputError(
                    "rank evidence bridge failed canonical replay"
                ) from error
            bridge_task_id = bridge.task.task_id
        elif type(bridge) is AdmissionEvidenceBridge:
            try:
                validate_admission_evidence_bridge(bridge)
            except (TypeError, ValueError) as error:
                raise PlanningSessionInputError(
                    "admission evidence bridge failed canonical replay"
                ) from error
            bridge_task_id = bridge.task.task_id
            if bridge.task.to_dict() != canonical_task.to_dict():
                raise PlanningSessionInputError(
                    "admission evidence task does not match the canonical query task"
                )
        elif type(bridge) is PathwayPolicyEvidenceBridge:
            try:
                validate_pathway_policy_evidence_bridge(bridge)
            except (TypeError, ValueError) as error:
                raise PlanningSessionInputError(
                    "pathway evidence bridge failed canonical replay"
                ) from error
            projection = bridge.projection
            bridge_task_id = projection.query_task_id
            if (
                projection.profile_digest != profile_digest
                or projection.query_plan_digest != plan_identity
            ):
                raise PlanningSessionInputError(
                    "pathway evidence outcome is outside the planning context"
                )
            expected_task_projection = {
                "task_id": canonical_task.task_id,
                "kind": canonical_task.kind,
                "target_name": canonical_task.target_name,
                "province": canonical_task.province,
                "subject_group": canonical_task.subject_group,
                "subject_mode": canonical_profile.subject_mode,
                "year": canonical_task.year,
                "target_year": canonical_plan.research_year,
                "source_policy_id": canonical_task.source_policy_id,
                "source_policy_version": canonical_task.source_policy_version,
            }
            expected_task_projection["task_digest"] = _digest_payload(
                expected_task_projection
            )
            if (
                projection.input_projection.get("task")
                != expected_task_projection
                or projection.query_task_digest
                != expected_task_projection["task_digest"]
            ):
                raise PlanningSessionInputError(
                    "pathway evidence task does not match the canonical query task"
                )
        elif type(bridge) is SchoolFitEvidenceBridge:
            try:
                validate_school_fit_evidence_bridge(
                    bridge, canonical_profile, canonical_plan
                )
            except (TypeError, ValueError) as error:
                raise PlanningSessionInputError(
                    "school-fit evidence bridge failed canonical replay"
                ) from error
            bridge_task_id = bridge.task.task_id
            if (
                bridge.task.to_dict() != canonical_task.to_dict()
                or bridge.profile_digest != profile_digest
                or bridge.query_plan_digest != plan_identity
            ):
                raise PlanningSessionInputError(
                    "school-fit evidence task does not match the planning context"
                )
        else:
            raise TypeError("bridges must be factory evidence bridge records")
        if bridge_task_id != canonical_task.task_id:
            raise PlanningSessionInputError("evidence bridges span multiple tasks")
        status = bridge.evidence_status.value
        statuses.append(status)
        artifacts.append(bridge.to_dict())
        provenance.append(
            {
                "type": type(bridge).__name__,
                "status": status,
                "source_ids": list(bridge.source_ids),
                "method": bridge.evidence_method,
                "locator": bridge.locator,
            }
        )
    usable = all(
        item in {"official", "corroborated", "reference"}
        for item in statuses
    )
    if records and type(records[0]) is AdmissionEvidenceBridge:
        if any(type(item) is not AdmissionEvidenceBridge for item in records):
            raise TypeError("admission evidence outcome cannot mix bridge types")
        accepted_coverage = {"official", "corroborated", "reference"}
        decisive_fields = {
            "dataset_row", "min_score", "min_rank", "coverage_min_rank",
            "coverage_max_rank", "coverage_status", "row_hash",
        }
        usable = usable and all(
            bridge.coverage_status.value in accepted_coverage
            and isinstance(bridge.fact.value, dict)
            and decisive_fields.issubset(bridge.fact.value)
            and bridge.fact.value["coverage_status"]
            == bridge.coverage_status.value
            and bridge.fact.value["row_hash"] == bridge.admission_row_hash
            for bridge in records
        )
    elif records and type(records[0]) is PathwayPolicyEvidenceBridge:
        if any(type(item) is not PathwayPolicyEvidenceBridge for item in records):
            raise TypeError("pathway evidence outcome cannot mix bridge types")
        try:
            from scripts.adapters.pathway_bridge import bridge_pathway_policies
        except ModuleNotFoundError:  # pragma: no cover - package fallback
            from .adapters.pathway_bridge import bridge_pathway_policies
        usable = usable and bool(
            bridge_pathway_policies(
                records,
                province=canonical_profile.province,
                subject_mode=canonical_profile.subject_mode,
                target_year=canonical_plan.research_year,
                expected_profile_digest=profile_digest,
                expected_query_plan_digest=plan_identity,
            )
        )
    elif records and type(records[0]) is SchoolFitEvidenceBridge:
        if any(type(item) is not SchoolFitEvidenceBridge for item in records):
            raise TypeError("school-fit evidence outcome cannot mix bridge types")
        usable = usable and all(
            isinstance(bridge.fact.value, dict)
            for bridge in records
        )
    values = {
        "task_id": canonical_task.task_id,
        "profile_digest": profile_digest,
        "query_plan_digest": plan_identity,
        "kind": canonical_task.kind,
        "target_name": canonical_task.target_name,
        "year": canonical_task.year,
        "artifact_digest": _digest_payload({"bridges": artifacts}),
        "provenance_digest": _digest_payload(
            {"task_id": canonical_task.task_id, "bridges": provenance}
        ),
        "evidence_statuses": tuple(statuses),
        "usable": usable,
    }
    result = TaskEvidenceOutcome._create(
        **values,
        receipt_digest=_digest_payload(
            {
                **values,
                "evidence_statuses": list(values["evidence_statuses"]),
            }
        ),
        _bridges=records,
    )
    if not _validating:
        return result.validate(canonical_profile, canonical_plan)
    return result


def _validate_profile_plan_context(profile: Any, plan: Any) -> None:
    """Reject individually canonical records that belong to different students."""

    try:
        validators: dict[type[Any], Any] = {}
        try:
            from scripts.query_plan import (
                QueryPlan as PackageQueryPlan,
                validate_query_plan_for_profile as validate_package_context,
            )
            validators[PackageQueryPlan] = validate_package_context
        except ModuleNotFoundError:  # pragma: no cover - flat install
            pass
        try:
            from query_plan import (
                QueryPlan as FlatQueryPlan,
                validate_query_plan_for_profile as validate_flat_context,
            )
            validators[FlatQueryPlan] = validate_flat_context
        except ModuleNotFoundError:  # pragma: no cover - package-only install
            pass
        validator = validators.get(type(plan))
        if validator is None:
            raise TypeError("plan is not a strict QueryPlan")
        validator(profile, plan)
        if __package__ in (None, ""):
            from province_registry import canonical_discovery_subject_key
        else:
            from .province_registry import canonical_discovery_subject_key
        expected_subject_group = canonical_discovery_subject_key(
            profile.subject_mode,
            profile.subject_group,
            profile.secondary_subjects,
            province=profile.province,
        )
    except (AttributeError, TypeError, ValueError):
        raise SessionTransitionError(
            "profile and query plan contexts cannot be compared"
        ) from None
    if (
        plan.province != profile.province
        or plan.mode != profile.subject_mode
        or plan.subject_group != expected_subject_group
        or plan.exam_year != profile.exam_year
        or plan.research_year > plan.exam_year
    ):
        raise SessionTransitionError(
            "profile and query plan contexts do not match"
        )


def _validated_planning_context(
    session: Any,
    profile: Any,
    query_plan: Any,
    *,
    require_bound_universe: bool,
) -> tuple[Any, str, Any]:
    """Replay the canonical profile, plan, and (when bound) exact task universe."""

    canonical_profile = _validated_profile(profile)
    identity, canonical_plan = _validated_query_plan(query_plan)
    if canonical_profile.digest != session.profile_digest:
        raise SessionTransitionError("profile does not match the planning session")
    _validate_profile_plan_context(canonical_profile, canonical_plan)
    expected = tuple(sorted(task.task_id for task in canonical_plan.tasks))
    if not expected:
        raise PlanningSessionInputError("query plan has no expected tasks")
    if require_bound_universe:
        session._bound("query_plan_digest", identity)
        if expected != session.expected_task_ids:
            raise SessionTransitionError(
                "profile and query plan task universe does not match the session"
            )
    return canonical_profile, identity, canonical_plan


def build_evidence_manifest_outcome(
    session: Any,
    profile: Any,
    query_plan: Any,
    *,
    bundle_path: Path | None,
    task_outcomes: Sequence[TaskEvidenceOutcome],
    capability_report: CapabilityReport | None = None,
    _validating: bool = False,
) -> EvidenceManifestOutcome:
    """Freshly bind the exact task partition to typed receipts and bundle facts."""

    if type(session) is not PlanningSession:
        raise TypeError("session must be a PlanningSession")
    session._at(
        SessionStage.RESEARCH_IN_PROGRESS,
        SessionStage.EVIDENCE_FINALIZED,
        SessionStage.CALCULATION_COMPLETE,
        SessionStage.REPORT_PUBLISHED,
    )
    canonical_profile, plan_identity, canonical_plan = _validated_planning_context(
        session,
        profile,
        query_plan,
        require_bound_universe=True,
    )
    actual_partition = tuple(
        sorted((*session.completed_task_ids, *session.unavailable_task_ids))
    )
    if actual_partition != session.expected_task_ids:
        raise SessionTransitionError("research coverage is incomplete")
    if isinstance(task_outcomes, (str, bytes, bytearray)):
        raise TypeError("task_outcomes must contain TaskEvidenceOutcome records")
    outcomes = tuple(task_outcomes)
    if any(type(item) is not TaskEvidenceOutcome for item in outcomes):
        raise TypeError("task_outcomes must contain TaskEvidenceOutcome records")
    if tuple(sorted(item.task_id for item in outcomes)) != session.completed_task_ids:
        raise SessionTransitionError(
            "completed tasks require their exact typed evidence receipts"
        )
    if len({item.task_id for item in outcomes}) != len(outcomes):
        raise PlanningSessionInputError("task evidence receipts contain duplicates")
    outcome_by_id = {item.task_id: item for item in outcomes}
    usable_ids: list[str] = []
    expected_facts: list[dict[str, Any]] = []
    expected_contexts: list[dict[str, Any]] = []
    expected_sources: set[str] = set()
    for index, task_id in enumerate(session.completed_task_ids):
        outcome = outcome_by_id[task_id]
        outcome.validate(canonical_profile, canonical_plan)
        stored = (
            session.completed_artifact_digests[index],
            session.completed_provenance_digests[index],
            session.completed_usable_flags[index],
            session.completed_receipt_digests[index],
        )
        if stored != (
            outcome.artifact_digest,
            outcome.provenance_digest,
            outcome.usable,
            outcome.receipt_digest,
        ):
            raise SessionTransitionError(
                "typed evidence receipt does not match completed session metadata"
            )
        if outcome.usable:
            usable_ids.append(task_id)
        for bridge in outcome._bridges:
            fact = getattr(bridge, "fact", None)
            if fact is None or not hasattr(fact, "to_dict"):
                raise PlanningSessionInputError(
                    "typed evidence receipt lacks a replayable fact"
                )
            expected_facts.append(fact.to_dict())
            expected_sources.update(getattr(bridge, "source_ids", ()))
            bridge_task = getattr(bridge, "task", None)
            bridge_projection = getattr(bridge, "projection", None)
            evidence_year = (
                bridge_task.year
                if bridge_task is not None
                else bridge_projection.data_year
            )
            expected_contexts.append(
                {
                    "kind": "fact-provenance",
                    "fact_id": fact.fact_id,
                    "source_ids": sorted(fact.source_ids),
                    "year": evidence_year,
                    "extraction_method": bridge.extraction_method,
                    "locator": bridge.locator,
                }
            )

    if not isinstance(bundle_path, Path):
        raise TypeError("evidence requires a host-internal bundle Path")
    try:
        if __package__ in (None, ""):
            from validate_evidence import validate_bundle_snapshot
        else:
            from .validate_evidence import validate_bundle_snapshot
        validation = validate_bundle_snapshot(
            bundle_path,
            _allow_empty=not session.completed_task_ids,
        )
    except (OSError, TypeError, ValueError) as error:
        raise PlanningSessionInputError("evidence bundle validation failed") from error
    if validation.snapshot is None or validation.issues:
        raise PlanningSessionInputError("evidence bundle validation failed")
    snapshot = validation.snapshot
    capability = snapshot.capability
    if (
        capability_report is not None
        and capability.to_dict() != capability_report.to_dict()
    ):
        raise SessionTransitionError(
            "evidence capability does not match the supplied preflight"
        )
    actual_facts = [item.to_dict() for item in snapshot.facts]
    canonical_fact = lambda value: json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    if sorted(map(canonical_fact, actual_facts)) != sorted(
        map(canonical_fact, expected_facts)
    ):
        raise SessionTransitionError(
            "bundle facts do not exactly match completed task receipts"
        )
    actual_contexts = [
        item.to_dict()
        for item in snapshot.contexts
        if item.to_dict().get("kind") == "fact-provenance"
    ]
    if sorted(map(canonical_fact, actual_contexts)) != sorted(
        map(canonical_fact, expected_contexts)
    ):
        raise SessionTransitionError(
            "bundle provenance contexts do not match completed task receipts"
        )
    candidate_source_ids = {
        item.to_dict().get("source_id") for item in snapshot.candidates
    }
    if not expected_sources <= candidate_source_ids:
        raise SessionTransitionError(
            "bundle candidates do not cover completed receipt sources"
        )
    manifest_session_id = snapshot.manifest.session_id
    manifest_hash = snapshot.manifest_hash
    facts_digest = snapshot.facts_digest
    retained_path = bundle_path
    capability_identity, _codes = _preflight_identity(capability)
    session._bound("preflight_digest", capability_identity)
    values = {
        "planning_session_id": session.session_id,
        "profile_digest": canonical_profile.digest,
        "query_plan_digest": plan_identity,
        "expected_task_ids": session.expected_task_ids,
        "completed_task_ids": session.completed_task_ids,
        "completed_receipt_digests": tuple(
            outcome_by_id[task_id].receipt_digest
            for task_id in session.completed_task_ids
        ),
        "usable_task_ids": tuple(sorted(usable_ids)),
        "unavailable_task_ids": session.unavailable_task_ids,
        "unavailable_reason_codes": session.unavailable_reason_codes,
        "manifest_session_id": manifest_session_id,
        "manifest_hash": manifest_hash,
        "facts_digest": facts_digest,
    }
    result = EvidenceManifestOutcome._create(
        **values,
        receipt_digest=_digest_payload(
            {
                **values,
                "expected_task_ids": list(values["expected_task_ids"]),
                "completed_task_ids": list(values["completed_task_ids"]),
                "completed_receipt_digests": list(
                    values["completed_receipt_digests"]
                ),
                "usable_task_ids": list(values["usable_task_ids"]),
                "unavailable_task_ids": list(values["unavailable_task_ids"]),
                "unavailable_reason_codes": list(
                    values["unavailable_reason_codes"]
                ),
            }
        ),
        _bundle_path=retained_path,
        _task_outcomes=tuple(
            outcome_by_id[task_id] for task_id in session.completed_task_ids
        ),
        _capability=capability,
        _snapshot=snapshot,
    )
    if session.stage is not SessionStage.RESEARCH_IN_PROGRESS:
        session._bound("evidence_manifest_hash", result.manifest_hash)
        session._bound("evidence_receipt_digest", result.receipt_digest)
    if not _validating:
        return result.validate(session, canonical_profile, canonical_plan)
    return result


def _matching_source_receipts_by_year(
    task_outcomes: Sequence[Any],
    source_id: str,
    *,
    kinds: set[str],
    years: set[int],
    require_usable: bool,
    allow_typed_partial: bool = False,
    policy_id: str | None = None,
) -> dict[int, tuple[Any, tuple[Any, ...]]] | None:
    """Resolve one source per declared year after semantic filtering.

    A public page may legitimately support multiple planned tasks.  It is an
    authority ambiguity only when more than one receipt still matches the same
    displayed kind/year/policy condition.
    """

    matches: dict[int, list[tuple[Any, tuple[Any, ...]]]] = {}
    for outcome in task_outcomes:
        if outcome.kind not in kinds or outcome.year not in years:
            continue
        bridges = tuple(
            bridge
            for bridge in outcome._bridges
            if source_id in bridge.source_ids
            and (
                policy_id is None
                or getattr(bridge, "policy_id", None) == policy_id
            )
        )
        if not bridges:
            continue
        if require_usable and not outcome.usable:
            continue
        if (
            not require_usable
            and not outcome.usable
            and not (
                allow_typed_partial
                and any(
                    getattr(
                        getattr(bridge, "coverage_status", None),
                        "value",
                        None,
                    )
                    == "partial"
                    for bridge in bridges
                )
            )
        ):
            continue
        matches.setdefault(outcome.year, []).append((outcome, bridges))
    if any(len(items) != 1 for items in matches.values()):
        return None
    return {year: items[0] for year, items in matches.items()}


def _matching_source_receipt(
    task_outcomes: Sequence[Any],
    source_id: str,
    *,
    kinds: set[str],
    years: set[int],
    require_usable: bool,
    allow_typed_partial: bool = False,
    policy_id: str | None = None,
) -> tuple[Any, tuple[Any, ...]] | None:
    matches = _matching_source_receipts_by_year(
        task_outcomes,
        source_id,
        kinds=kinds,
        years=years,
        require_usable=require_usable,
        allow_typed_partial=allow_typed_partial,
        policy_id=policy_id,
    )
    if matches is None or len(matches) != 1:
        return None
    return next(iter(matches.values()))


def _validate_displayed_school_sources(
    item: Any,
    task_outcomes: Sequence[Any],
) -> None:
    """Bind a displayed school to the exact authenticated admission rows.

    Task-level usability controls year fallback.  It must not let a partial
    sibling row taint—or authorize—a different complete row in the same task.
    """

    if not item.source_ids:
        raise SessionTransitionError(
            "displayed school requires authenticated sources"
        )
    years = set(item.supporting_years or (item.data_year,))
    if not years or item.data_year not in years:
        raise SessionTransitionError(
            "displayed school sources lack matching exact admission rows"
        )
    claim_status = getattr(item.evidence_status, "value", item.evidence_status)
    strengths = {"reference": 1, "corroborated": 2, "official": 3}
    if claim_status not in strengths:
        raise SessionTransitionError(
            "numeric school recommendations require exact accepted evidence"
        )
    covered_years: set[int] = set()
    for source_id in item.source_ids:
        source_years: set[int] = set()
        for year in years:
            matches: list[tuple[Any, Any]] = []
            for outcome in task_outcomes:
                if outcome.kind != "batch_admission" or outcome.year != year:
                    continue
                bridges = []
                for bridge in outcome._bridges:
                    if source_id not in bridge.source_ids:
                        continue
                    row = getattr(bridge, "dataset_row", None)
                    if (
                        row is None
                        or getattr(row, "year", None) != year
                        or getattr(row, "school_name", None) != item.school_name
                    ):
                        continue
                    selected_groups = getattr(item, "major_groups", ())
                    if selected_groups and getattr(row, "program_group", None) not in selected_groups:
                        continue
                    if year == item.data_year and (
                        getattr(row, "min_score", None) != item.min_score
                        or getattr(row, "min_rank", None) != item.min_rank
                    ):
                        continue
                    evidence = getattr(
                        getattr(bridge, "evidence_status", None),
                        "value",
                        None,
                    )
                    coverage = getattr(
                        getattr(bridge, "coverage_status", None),
                        "value",
                        None,
                    )
                    if (
                        evidence not in strengths
                        or coverage not in strengths
                        or strengths[evidence] < strengths[claim_status]
                        or strengths[coverage] < strengths[claim_status]
                    ):
                        continue
                    bridges.append(bridge)
                matches.extend((outcome, bridge) for bridge in bridges)
            if len(matches) > 1:
                raise SessionTransitionError(
                    "displayed school sources are ambiguous for one supporting year"
                )
            if matches:
                source_years.add(year)
        fit_matches: list[tuple[Any, Any]] = []
        for outcome in task_outcomes:
            if outcome.kind not in {
                "province_policy",
                "enrollment_plan",
                "admission_charter",
                "tuition_fee",
                "subject_requirement",
            }:
                continue
            for bridge in outcome._bridges:
                if source_id not in getattr(bridge, "source_ids", ()):
                    continue
                bridge_task = getattr(bridge, "task", None)
                if bridge_task is None or bridge_task.kind != outcome.kind:
                    continue
                if outcome.kind != "province_policy":
                    metadata = getattr(bridge, "metadata", None)
                    if isinstance(metadata, dict):
                        bound_school = metadata.get("school_name")
                    else:
                        bound_school = None
                    if bound_school != item.school_name:
                        adapter_rows = getattr(bridge, "adapter_rows", ())
                        if not any(
                            getattr(row, "values", {}).get("institution")
                            == item.school_name
                            for row in adapter_rows
                        ):
                            continue
                fit_matches.append((outcome, bridge))
        # One public document can support both roles; only exact admission
        # matches above authorize the displayed numbers and supporting years.
        if not source_years and not fit_matches:
            raise SessionTransitionError(
                "displayed school sources lack matching exact admission rows or typed fit receipts"
            )
        covered_years.update(source_years)
    if covered_years != years:
        raise SessionTransitionError(
            "displayed school supporting years lack matching admission receipts"
        )


def _validate_displayed_school_observation(
    item: Any,
    task_outcomes: Sequence[Any],
) -> None:
    """Bind one non-numeric school observation to exact partial bridge rows."""

    status = getattr(item.evidence_status, "value", item.evidence_status)
    if status != "partial":
        raise SessionTransitionError(
            "school observations must remain explicitly partial"
        )
    if not item.source_ids:
        raise SessionTransitionError(
            "school observation requires authenticated sources"
        )
    accepted = {"official", "corroborated", "reference"}
    for source_id in item.source_ids:
        matches: list[tuple[Any, Any]] = []
        for outcome in task_outcomes:
            if outcome.kind != "batch_admission" or outcome.year != item.data_year:
                continue
            bridges = tuple(
                bridge
                for bridge in outcome._bridges
                if source_id in bridge.source_ids
                and getattr(
                    getattr(bridge, "evidence_status", None),
                    "value",
                    None,
                )
                in accepted
                and getattr(
                    getattr(bridge, "coverage_status", None),
                    "value",
                    None,
                )
                == "partial"
                and getattr(getattr(bridge, "dataset_row", None), "year", None)
                == item.data_year
                and getattr(
                    getattr(bridge, "dataset_row", None),
                    "school_name",
                    None,
                )
                == item.school_name
            )
            matches.extend((outcome, bridge) for bridge in bridges)
        if len(matches) > 1:
            raise SessionTransitionError(
                "school observation sources are ambiguous for one year"
            )
        if not matches:
            raise SessionTransitionError(
                "school observation lacks a matching typed partial receipt"
            )


def build_calculation_outcome(
    session: Any,
    evidence_outcome: EvidenceManifestOutcome,
    profile: Any,
    query_plan: Any,
    *,
    decision_policy: Any | None = None,
    _validating: bool = False,
) -> CalculationOutcome:
    """Run the complete public calculation from the receipt-bound bundle."""

    if type(session) is not PlanningSession:
        raise TypeError("session must be a PlanningSession")
    session._at(
        SessionStage.EVIDENCE_FINALIZED,
        SessionStage.CALCULATION_COMPLETE,
        SessionStage.REPORT_PUBLISHED,
    )
    canonical_profile, _plan_identity, canonical_plan = _validated_planning_context(
        session,
        profile,
        query_plan,
        require_bound_universe=True,
    )
    if type(evidence_outcome) is not EvidenceManifestOutcome:
        raise TypeError("evidence_outcome must be an EvidenceManifestOutcome")
    evidence_outcome.validate(session, canonical_profile, canonical_plan)
    if evidence_outcome._bundle_path is None:
        raise PlanningSessionInputError("evidence outcome lacks its replayable bundle")
    if __package__ in (None, ""):
        from decision_policy import DecisionPolicySnapshot
        from generate_report import build_pathway_atlas_model
        from rank_locator import locate_rank
        from research_snapshot import build_research_snapshot
    else:
        from .decision_policy import DecisionPolicySnapshot
        from .generate_report import build_pathway_atlas_model
        from .rank_locator import locate_rank
        from .research_snapshot import build_research_snapshot
    policy = decision_policy or DecisionPolicySnapshot.load_default()
    if type(policy) is not DecisionPolicySnapshot:
        raise TypeError("decision_policy must be a strict DecisionPolicySnapshot")
    research = build_research_snapshot(
        canonical_profile,
        canonical_plan,
        evidence_outcome._bundle_path,
        policy,
    )
    model = build_pathway_atlas_model(
        canonical_profile,
        research,
        evidence_outcome._bundle_path,
        canonical_plan,
        decision_policy=policy,
    )
    model_payload = model.to_dict()
    if (
        model.manifest_hash != evidence_outcome.manifest_hash
        or model.manifest_session_id != evidence_outcome.manifest_session_id
    ):
        raise SessionTransitionError(
            "report model does not match the evidence manifest receipt"
        )
    task_by_id = {task.task_id: task for task in canonical_plan.tasks}
    usable_tasks = tuple(
        task_by_id[task_id] for task_id in evidence_outcome.usable_task_ids
    )
    completed_sources = {
        source_id
        for outcome in evidence_outcome._task_outcomes
        for bridge in outcome._bridges
        for source_id in bridge.source_ids
    }
    replayed_rank = locate_rank(
        canonical_profile,
        research_snapshot=research,
    )
    rank_exactly_replays = bool(
        model.rank is not None
        and model.rank.to_dict() == replayed_rank.to_dict()
    )
    profile_bound_sources: set[str] = set()
    if rank_exactly_replays and model.rank.basis == "profile_reported_province_rank":
        if (
            getattr(model.rank.status, "value", model.rank.status) != "inferred"
            or tuple(model.rank.source_ids) != ("profile-reported-rank",)
            or tuple(model.rank.channel_kinds) != ("profile_reported_rank",)
            or tuple(model.rank.channel_statuses) != ("inferred",)
        ):
            raise SessionTransitionError(
                "profile-reported rank does not match its canonical inference"
            )
        profile_bound_sources.add("profile-reported-rank")
    elif rank_exactly_replays and model.rank.basis == "profile_reported_score_table":
        if "profile-reported-score" not in model.rank.source_ids:
            raise SessionTransitionError(
                "profile-reported score does not match its canonical inference"
            )
        profile_bound_sources.add("profile-reported-score")
    if not set(model.source_ids) <= completed_sources | profile_bound_sources:
        raise SessionTransitionError(
            "report displays sources outside completed typed evidence"
        )
    profile_direct_rank = bool(
        rank_exactly_replays
        and model.rank is not None
        and model.rank.basis == "profile_reported_province_rank"
        and tuple(model.rank.source_ids) == ("profile-reported-rank",)
    )
    if (
        model.rank is not None
        and model.rank.central_rank is not None
        and not model.rank.source_ids
    ):
        raise SessionTransitionError(
            "displayed numeric rank requires authenticated sources"
        )
    if model.rank is not None and model.rank.source_ids and not profile_direct_rank:
        contributing_years = set(model.rank.contributing_years)
        channel_kinds = set(model.rank.channel_kinds)
        allowed_rank_task_kinds = set()
        if "official_score_table" in channel_kinds:
            allowed_rank_task_kinds.add("score_table")
        if channel_kinds - {"official_rank", "official_score_table"}:
            allowed_rank_task_kinds.add("joy_report")
        covered_rank_years: set[int] = set()
        rank_sources_valid = bool(contributing_years)
        for source_id in (
            item for item in model.rank.source_ids if item not in profile_bound_sources
        ):
            matches = _matching_source_receipts_by_year(
                evidence_outcome._task_outcomes,
                source_id,
                kinds=allowed_rank_task_kinds,
                years=contributing_years,
                require_usable=True,
            )
            if not matches:
                rank_sources_valid = False
                break
            covered_rank_years.update(matches)
        if not rank_sources_valid or covered_rank_years != contributing_years:
            raise SessionTransitionError(
                "displayed rank sources lack matching usable receipts"
            )

    for item in model.recommendations:
        _validate_displayed_school_sources(
            item,
            evidence_outcome._task_outcomes,
        )
    for item in model.school_observations:
        _validate_displayed_school_observation(
            item,
            evidence_outcome._task_outcomes,
        )

    pathway_kinds = {
        "strong_foundation",
        "comprehensive_evaluation",
        "hk_macao_admission",
        "special_pathway",
    }
    for item in model.pathways:
        item_evidence_status = getattr(
            item.evidence_status, "value", item.evidence_status
        )
        unverified_observation = (
            item.status == "pending_verification"
            and item.target_year is None
            and item.data_year is None
            and item.year_basis == "unverified"
        )
        if unverified_observation:
            if not any(
                task.kind in pathway_kinds and task.target_name == item.title
                for task in canonical_plan.tasks
            ):
                raise SessionTransitionError(
                    "displayed pathway observation is outside the active query plan"
                )
            if not item.source_ids:
                if item_evidence_status not in {"missing", "masked"}:
                    raise SessionTransitionError(
                        "source-free pathway observation must remain missing or masked"
                    )
                continue
            if item_evidence_status not in {
                "conflict",
                "partial",
                "missing",
                "masked",
            }:
                raise SessionTransitionError(
                    "unverified pathway observation has an unsupported evidence status"
                )
            for source_id in item.source_ids:
                if not any(
                    outcome.kind in pathway_kinds
                    and any(
                        source_id in bridge.source_ids
                        and getattr(
                            getattr(bridge, "evidence_status", None),
                            "value",
                            None,
                        )
                        in {"conflict", "partial", "missing", "masked"}
                        for bridge in outcome._bridges
                    )
                    for outcome in evidence_outcome._task_outcomes
                ):
                    raise SessionTransitionError(
                        "pathway observation sources lack matching typed receipts"
                    )
            continue
        if not item.source_ids:
            raise SessionTransitionError(
                "displayed pathway requires authenticated sources"
            )
        if item.data_year is None or any(
            _matching_source_receipt(
                evidence_outcome._task_outcomes,
                source_id,
                kinds=pathway_kinds,
                years={item.data_year},
                require_usable=item.status == "formal",
                policy_id=item.policy_id,
            )
            is None
            for source_id in item.source_ids
        ):
            raise SessionTransitionError(
                "displayed pathway sources lack matching typed receipts"
            )
    rank_status = (
        getattr(model.rank.status, "value", model.rank.status)
        if model.rank is not None
        else "missing"
    )
    if (
        model.rank is not None
        and model.rank.central_rank is not None
        and rank_status in {"official", "inferred"}
        and not (
            profile_direct_rank
        )
        and not any(
            task.kind in {"score_table", "joy_report"} for task in usable_tasks
        )
    ):
        raise SessionTransitionError(
            "numeric rank lacks a usable authenticated research receipt"
        )
    accepted_statuses = {"official", "corroborated", "reference", "inferred"}
    if any(item.status == "formal" for item in model.pathways) and not any(
        task.kind
        in {
            "strong_foundation",
            "comprehensive_evaluation",
            "hk_macao_admission",
            "special_pathway",
        }
        for task in usable_tasks
    ):
        raise SessionTransitionError(
            "formal pathways lack a usable pathway-policy receipt"
        )
    rank_payload = model_payload.get("rank")
    recommendation_payload = {
        key: model_payload[key]
        for key in (
            "recommendations",
            "school_observations",
            "school_decisions",
            "recommendation_policy_status",
            "recommendation_coverage_status",
            "verified_rank_coverage",
            "recommendation_empty_reason",
            "recommendation_warnings",
        )
    }
    pathway_payload = {
        key: model_payload[key]
        for key in (
            "pathways_available",
            "pathways",
            "pathway_warnings",
            "pathway_target_rank",
            "pathway_transformation",
            "pathway_policy_evidence_status",
            "pathway_target_evidence_status",
        )
    }
    usable_families = {
        (task.kind, task.target_name) for task in usable_tasks
    }
    unresolved_families = {
        (task_by_id[outcome.task_id].kind, task_by_id[outcome.task_id].target_name)
        for outcome in evidence_outcome._task_outcomes
        if not outcome.usable
        and (
            task_by_id[outcome.task_id].kind,
            task_by_id[outcome.task_id].target_name,
        )
        not in usable_families
    }
    unresolved_families.update(
        (task_by_id[task_id].kind, task_by_id[task_id].target_name)
        for task_id in session.unavailable_task_ids
        if (
            task_by_id[task_id].kind,
            task_by_id[task_id].target_name,
        )
        not in usable_families
    )
    model_status = getattr(model.evidence_status, "value", model.evidence_status)
    values = {
        "evidence_receipt_digest": evidence_outcome.receipt_digest,
        "research_snapshot_digest": research.digest,
        "rank_scenario_digest": _digest_payload({"rank": rank_payload}),
        "recommendation_result_digest": _digest_payload(recommendation_payload),
        "pathway_result_digest": _digest_payload(pathway_payload),
        "report_model_digest": _digest_payload(model_payload),
        "degraded": bool(
            unresolved_families
            or model_status not in accepted_statuses
        ),
    }
    result = CalculationOutcome._create(
        **values,
        receipt_digest=_digest_payload(values),
        _evidence_outcome=evidence_outcome,
        _policy=policy,
        _research_snapshot=research,
        _model=model,
    )
    if session.stage in {
        SessionStage.CALCULATION_COMPLETE,
        SessionStage.REPORT_PUBLISHED,
    }:
        session._bound("calculation_digest", result.report_model_digest)
        session._bound("calculation_receipt_digest", result.receipt_digest)
    if not _validating:
        return result.validate(session, canonical_profile, canonical_plan)
    return result


def build_report_publication_outcome(
    calculation_outcome: CalculationOutcome,
    *,
    format: str = "markdown",
    _validating: bool = False,
) -> ReportPublicationOutcome:
    """Render publication bytes internally; callers never supply their own digest."""

    if type(calculation_outcome) is not CalculationOutcome:
        raise TypeError("calculation_outcome must be a CalculationOutcome")
    if format not in {"markdown", "docx"}:
        raise PlanningSessionInputError(
            "publication format must be markdown or docx"
        )
    if format == "markdown":
        if __package__ in (None, ""):
            from report_model import render_markdown
        else:
            from .report_model import render_markdown
        rendered = render_markdown(calculation_outcome.model).encode("utf-8")
    else:
        if __package__ in (None, ""):
            from docx_export import export_docx
        else:
            from .docx_export import export_docx
        with tempfile.TemporaryDirectory() as temporary:
            output = export_docx(
                calculation_outcome.model,
                Path(temporary) / "pathway-atlas.docx",
            )
            rendered = output.read_bytes()
    values = {
        "format": format,
        "calculation_receipt_digest": calculation_outcome.receipt_digest,
        "report_model_digest": calculation_outcome.report_model_digest,
        "rendered_digest": "sha256:" + hashlib.sha256(rendered).hexdigest(),
    }
    result = ReportPublicationOutcome._create(
        **values,
        receipt_digest=_digest_payload(values),
        _calculation_outcome=calculation_outcome,
        _rendered_bytes=rendered,
    )
    if not _validating:
        rebuilt = build_report_publication_outcome(
            calculation_outcome,
            format=format,
            _validating=True,
        )
        if (
            rebuilt._payload() != result._payload()
            or rebuilt._rendered_bytes != result._rendered_bytes
        ):
            raise PlanningSessionInputError("publication did not replay")
    return result


def _require_digest(value: Any, name: str) -> str:
    if not isinstance(value, str) or _DIGEST.fullmatch(value) is None:
        raise PlanningSessionInputError(f"{name} must be a lower-case SHA-256 identity")
    return value


def _canonical_bytes(payload: Mapping[str, Any]) -> bytes:
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _digest_payload(payload: Mapping[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(_canonical_bytes(payload)).hexdigest()


def _preflight_identity(report: CapabilityReport) -> tuple[str, tuple[str, ...]]:
    if not isinstance(report, CapabilityReport):
        # Flat-script and package imports can load the same frozen contract
        # under two module names.  Admit only that exact serialized shape.
        if type(report).__name__ != "CapabilityReport" or not hasattr(report, "to_dict"):
            raise TypeError("preflight must be a strict CapabilityReport")
    payload = report.to_dict()
    if set(payload) != {
        "tier",
        "host_capabilities",
        "available_capabilities",
        "missing_capabilities",
        "degradations",
        "python_version",
        "optional_modules",
    }:
        raise TypeError("preflight must be a strict CapabilityReport")
    missing = payload["missing_capabilities"]
    if (
        not isinstance(missing, list)
        or any(
            not isinstance(item, str) or item not in _PREFLIGHT_DEGRADATION_MAP
            for item in missing
        )
    ):
        raise PlanningSessionInputError(
            "preflight missing capabilities are invalid"
        )
    codes = tuple(
        sorted({_PREFLIGHT_DEGRADATION_MAP[item] for item in missing})
    )
    return _digest_payload(payload), codes


def _validated_query_plan(value: Any) -> tuple[str, Any]:
    allowed: dict[type[Any], Any] = {}
    try:
        from scripts.query_plan import (
            QueryPlan as PackageQueryPlan,
            validate_query_plan_payload as validate_package_query_plan,
        )
        allowed[PackageQueryPlan] = validate_package_query_plan
    except ModuleNotFoundError:  # pragma: no cover - flat install
        pass
    try:
        from query_plan import (
            QueryPlan as FlatQueryPlan,
            validate_query_plan_payload as validate_flat_query_plan,
        )
        allowed[FlatQueryPlan] = validate_flat_query_plan
    except ModuleNotFoundError:  # pragma: no cover - package-only install
        pass
    validator = allowed.get(type(value))
    if validator is None:
        raise TypeError("query plan must be a validated QueryPlan")
    payload = value.to_dict()
    if not isinstance(payload, dict) or not isinstance(payload.get("tasks"), list):
        raise TypeError("query plan must be a validated QueryPlan")
    validated = validator(payload)
    if validated.to_dict() != payload:
        raise TypeError("query plan must be a canonical validated QueryPlan")
    return _digest_payload(payload), validated


def _query_plan_identity(value: Any) -> str:
    return _validated_query_plan(value)[0]


def _profile_identity(value: Any) -> str:
    if isinstance(value, str):
        return _require_digest(value, "profile_digest")
    if type(value).__name__ != "PlanningProfile" or not hasattr(value, "digest"):
        raise TypeError("profile must be a strict PlanningProfile or its digest")
    return _require_digest(value.digest, "profile_digest")


def _validated_profile(value: Any) -> Any:
    allowed: set[type[Any]] = set()
    try:
        from scripts.planning_profile import PlanningProfile as PackagePlanningProfile
        allowed.add(PackagePlanningProfile)
    except ModuleNotFoundError:  # pragma: no cover - flat install
        pass
    try:
        from planning_profile import PlanningProfile as FlatPlanningProfile
        allowed.add(FlatPlanningProfile)
    except ModuleNotFoundError:  # pragma: no cover - package-only install
        pass
    if type(value) not in allowed:
        raise TypeError("profile must be a strict PlanningProfile")
    payload = value.to_dict()
    if not isinstance(payload, dict):
        raise TypeError("profile must be a strict PlanningProfile")
    public_payload = {
        key: item
        for key, item in payload.items()
        if key not in {"mode", "digest"}
    }
    try:
        canonical = type(value).create(public_payload)
    except (TypeError, ValueError):
        raise TypeError("profile must be a canonical PlanningProfile") from None
    if canonical.to_dict() != payload:
        raise TypeError("profile must be a canonical PlanningProfile")
    return canonical


def _task_ids(values: Any, name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes, bytearray)):
        raise PlanningSessionInputError(f"{name} must be an array")
    try:
        result = tuple(values)
    except TypeError as error:
        raise PlanningSessionInputError(f"{name} must be an array") from error
    if any(not isinstance(item, str) or _TASK_ID.fullmatch(item) is None for item in result):
        raise PlanningSessionInputError(f"{name} contains an invalid machine ID")
    if result != tuple(sorted(result)) or len(result) != len(set(result)):
        raise PlanningSessionInputError(f"{name} must be unique and canonical")
    return result


def _string_tuple(values: Any, name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes, bytearray)):
        raise PlanningSessionInputError(f"{name} must be an array")
    try:
        result = tuple(values)
    except TypeError as error:
        raise PlanningSessionInputError(f"{name} must be an array") from error
    if any(not isinstance(item, str) for item in result):
        raise PlanningSessionInputError(f"{name} must contain strings")
    return result


def _bool_tuple(values: Any, name: str) -> tuple[bool, ...]:
    if isinstance(values, (str, bytes, bytearray)):
        raise PlanningSessionInputError(f"{name} must be an array")
    try:
        result = tuple(values)
    except TypeError as error:
        raise PlanningSessionInputError(f"{name} must be an array") from error
    if any(type(item) is not bool for item in result):
        raise PlanningSessionInputError(f"{name} must contain booleans")
    return result


def _optional_digest_tuple(
    values: Any, name: str
) -> tuple[str | None, ...]:
    if isinstance(values, (str, bytes, bytearray)):
        raise PlanningSessionInputError(f"{name} must be an array")
    try:
        result = tuple(values)
    except TypeError as error:
        raise PlanningSessionInputError(f"{name} must be an array") from error
    for item in result:
        if item is not None:
            _require_digest(item, name.removesuffix("s"))
    return result


def _validate_reachable_state(values: Mapping[str, Any]) -> None:
    """Reject any state that cannot be produced by the transition interface."""

    stage = values["stage"]
    revision = values["revision"]
    rank = _STAGE_ORDER.index(stage)
    minimum_revision = {
        SessionStage.INTAKE: 0,
        SessionStage.PROFILE_CONFIRMED: 1,
        SessionStage.PREFLIGHT_COMPLETE: 2,
        SessionStage.QUERY_PLAN_READY: 3,
        SessionStage.RESEARCH_IN_PROGRESS: 4,
        SessionStage.EVIDENCE_FINALIZED: 5,
        SessionStage.CALCULATION_COMPLETE: 6,
        SessionStage.REPORT_PUBLISHED: 7,
    }[stage]
    if revision < minimum_revision or (
        stage is SessionStage.INTAKE and revision != 0
    ):
        raise PlanningSessionInputError("stage revision is unreachable")

    required_at = {
        "preflight_digest": SessionStage.PREFLIGHT_COMPLETE,
        "query_plan_digest": SessionStage.QUERY_PLAN_READY,
        "evidence_manifest_hash": SessionStage.EVIDENCE_FINALIZED,
        "evidence_receipt_digest": SessionStage.EVIDENCE_FINALIZED,
        "calculation_digest": SessionStage.CALCULATION_COMPLETE,
        "calculation_receipt_digest": SessionStage.CALCULATION_COMPLETE,
        "report_digest": SessionStage.REPORT_PUBLISHED,
        "publication_receipt_digest": SessionStage.REPORT_PUBLISHED,
    }
    for name, first_stage in required_at.items():
        present = values[name] is not None
        expected = rank >= _STAGE_ORDER.index(first_stage)
        if present != expected:
            raise PlanningSessionInputError("stage dependency invariants are invalid")
    if (
        rank < _STAGE_ORDER.index(SessionStage.PREFLIGHT_COMPLETE)
        and values["preflight_degradation_codes"]
    ):
        raise PlanningSessionInputError(
            "preflight degradation precedes preflight"
        )

    expected_ids = values["expected_task_ids"]
    completed_ids = values["completed_task_ids"]
    unavailable_ids = values["unavailable_task_ids"]
    if (
        len(values["completed_artifact_digests"]) != len(completed_ids)
        or len(values["completed_provenance_digests"]) != len(completed_ids)
        or len(values["completed_usable_flags"]) != len(completed_ids)
        or len(values["completed_receipt_digests"]) != len(completed_ids)
    ):
        raise PlanningSessionInputError("completed outcome metadata is incomplete")
    if len(values["unavailable_reason_codes"]) != len(unavailable_ids):
        raise PlanningSessionInputError("unavailable outcome metadata is incomplete")
    if set(completed_ids) & set(unavailable_ids):
        raise PlanningSessionInputError("task outcomes overlap")
    if not set((*completed_ids, *unavailable_ids)) <= set(expected_ids):
        raise PlanningSessionInputError("task outcome is outside the query plan")

    outcome_count = len(completed_ids) + len(unavailable_ids)
    if rank >= _STAGE_ORDER.index(SessionStage.RESEARCH_IN_PROGRESS):
        # Each outcome is an immutable transition; later stages add one
        # transition apiece.  A rehashed snapshot cannot compress that history.
        transition_floor = rank + outcome_count - 1
        if revision < transition_floor:
            raise PlanningSessionInputError("stage revision is unreachable")

    query_ready = rank >= _STAGE_ORDER.index(SessionStage.QUERY_PLAN_READY)
    research_started = rank >= _STAGE_ORDER.index(SessionStage.RESEARCH_IN_PROGRESS)
    evidence_ready = rank >= _STAGE_ORDER.index(SessionStage.EVIDENCE_FINALIZED)
    if evidence_ready and any(
        receipt is None for receipt in values["completed_receipt_digests"]
    ):
        raise PlanningSessionInputError(
            "finalized completed tasks require typed evidence receipts"
        )
    if query_ready != bool(expected_ids):
        raise PlanningSessionInputError("query-plan task universe is unreachable")
    if not research_started and (completed_ids or unavailable_ids):
        raise PlanningSessionInputError("task outcomes precede research")
    if stage is SessionStage.RESEARCH_IN_PROGRESS and not (
        completed_ids or unavailable_ids
    ):
        raise PlanningSessionInputError("research must record a task outcome")
    if evidence_ready and (
        not (completed_ids or unavailable_ids)
        or tuple(sorted((*completed_ids, *unavailable_ids))) != expected_ids
    ):
        raise PlanningSessionInputError("evidence requires complete task coverage")


@dataclass(frozen=True, init=False)
class PlanningSession:
    session_id: str
    revision: int
    stage: SessionStage
    profile_digest: str
    preflight_digest: str | None
    preflight_degradation_codes: tuple[str, ...]
    query_plan_digest: str | None
    expected_task_ids: tuple[str, ...]
    completed_task_ids: tuple[str, ...]
    completed_artifact_digests: tuple[str, ...]
    completed_provenance_digests: tuple[str, ...]
    completed_usable_flags: tuple[bool, ...]
    completed_receipt_digests: tuple[str | None, ...]
    unavailable_task_ids: tuple[str, ...]
    unavailable_reason_codes: tuple[str, ...]
    evidence_manifest_hash: str | None
    evidence_receipt_digest: str | None
    calculation_digest: str | None
    calculation_receipt_digest: str | None
    report_digest: str | None
    publication_receipt_digest: str | None
    session_digest: str

    def __init__(self) -> None:
        raise TypeError("PlanningSession is factory-only")

    @classmethod
    def create(cls, session_id: str, profile_digest: Any) -> "PlanningSession":
        if not isinstance(session_id, str) or _SESSION_ID.fullmatch(session_id) is None:
            raise ValueError("session_id must be lower-case UUID hex")
        return cls._build(
            session_id=session_id,
            revision=0,
            stage=SessionStage.INTAKE,
            profile_digest=_profile_identity(profile_digest),
            preflight_digest=None,
            preflight_degradation_codes=(),
            query_plan_digest=None,
            expected_task_ids=(),
            completed_task_ids=(),
            completed_artifact_digests=(),
            completed_provenance_digests=(),
            completed_usable_flags=(),
            completed_receipt_digests=(),
            unavailable_task_ids=(),
            unavailable_reason_codes=(),
            evidence_manifest_hash=None,
            evidence_receipt_digest=None,
            calculation_digest=None,
            calculation_receipt_digest=None,
            report_digest=None,
            publication_receipt_digest=None,
        )

    @classmethod
    def _build(cls, **raw: Any) -> "PlanningSession":
        if set(raw) != set(_STATE_FIELDS):
            raise PlanningSessionInputError("session fields do not match the contract")
        session_id = raw["session_id"]
        if not isinstance(session_id, str) or _SESSION_ID.fullmatch(session_id) is None:
            raise PlanningSessionInputError("session_id is invalid")
        revision = raw["revision"]
        if (
            isinstance(revision, bool)
            or not isinstance(revision, int)
            or revision < 0
            or revision > 99_999_999
        ):
            raise PlanningSessionInputError("revision is invalid")
        try:
            stage = (
                raw["stage"]
                if isinstance(raw["stage"], SessionStage)
                else SessionStage(raw["stage"])
            )
        except (TypeError, ValueError) as error:
            raise PlanningSessionInputError("stage is invalid") from error
        profile_digest = _require_digest(raw["profile_digest"], "profile_digest")
        optional_digests: dict[str, str | None] = {}
        for name in (
            "preflight_digest",
            "query_plan_digest",
            "evidence_manifest_hash",
            "evidence_receipt_digest",
            "calculation_digest",
            "calculation_receipt_digest",
            "report_digest",
            "publication_receipt_digest",
        ):
            value = raw[name]
            optional_digests[name] = (
                None if value is None else _require_digest(value, name)
            )
        completed = _task_ids(raw["completed_task_ids"], "completed_task_ids")
        unavailable = _task_ids(raw["unavailable_task_ids"], "unavailable_task_ids")
        expected = _task_ids(raw["expected_task_ids"], "expected_task_ids")
        artifacts = _string_tuple(
            raw["completed_artifact_digests"], "completed_artifact_digests"
        )
        for item in artifacts:
            _require_digest(item, "completed artifact digest")
        provenance = _string_tuple(
            raw["completed_provenance_digests"], "completed_provenance_digests"
        )
        for item in provenance:
            _require_digest(item, "completed provenance digest")
        usable_flags = _bool_tuple(
            raw["completed_usable_flags"], "completed_usable_flags"
        )
        receipt_digests = _optional_digest_tuple(
            raw["completed_receipt_digests"], "completed_receipt_digests"
        )
        reasons = _string_tuple(
            raw["unavailable_reason_codes"], "unavailable_reason_codes"
        )
        if any(item not in _UNAVAILABLE_REASONS for item in reasons):
            raise PlanningSessionInputError("unavailable reason code is invalid")
        preflight_codes = _string_tuple(
            raw["preflight_degradation_codes"],
            "preflight_degradation_codes",
        )
        if (
            any(
                item not in _PREFLIGHT_DEGRADATION_CODES
                for item in preflight_codes
            )
            or preflight_codes != tuple(sorted(set(preflight_codes)))
        ):
            raise PlanningSessionInputError(
                "preflight degradation codes are invalid"
            )

        normalized: dict[str, Any] = {
            "session_id": session_id,
            "revision": revision,
            "stage": stage,
            "profile_digest": profile_digest,
            **optional_digests,
            "expected_task_ids": expected,
            "completed_task_ids": completed,
            "completed_artifact_digests": artifacts,
            "completed_provenance_digests": provenance,
            "completed_usable_flags": usable_flags,
            "completed_receipt_digests": receipt_digests,
            "unavailable_task_ids": unavailable,
            "unavailable_reason_codes": reasons,
            "preflight_degradation_codes": preflight_codes,
        }
        _validate_reachable_state(normalized)
        digest_source = cls._state_payload(normalized)
        instance = object.__new__(cls)
        for name in _STATE_FIELDS:
            object.__setattr__(instance, name, normalized[name])
        object.__setattr__(instance, "session_digest", _digest_payload(digest_source))
        return instance

    @staticmethod
    def _state_payload(values: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "schema_version": _SCHEMA_VERSION,
            "session_id": values["session_id"],
            "revision": values["revision"],
            "stage": (
                values["stage"].value
                if isinstance(values["stage"], SessionStage)
                else values["stage"]
            ),
            "profile_digest": values["profile_digest"],
            "preflight_digest": values["preflight_digest"],
            "preflight_degradation_codes": list(
                values["preflight_degradation_codes"]
            ),
            "query_plan_digest": values["query_plan_digest"],
            "expected_task_ids": list(values["expected_task_ids"]),
            "completed_task_ids": list(values["completed_task_ids"]),
            "completed_artifact_digests": list(
                values["completed_artifact_digests"]
            ),
            "completed_provenance_digests": list(
                values["completed_provenance_digests"]
            ),
            "completed_usable_flags": list(values["completed_usable_flags"]),
            "completed_receipt_digests": list(values["completed_receipt_digests"]),
            "unavailable_task_ids": list(values["unavailable_task_ids"]),
            "unavailable_reason_codes": list(values["unavailable_reason_codes"]),
            "evidence_manifest_hash": values["evidence_manifest_hash"],
            "evidence_receipt_digest": values["evidence_receipt_digest"],
            "calculation_digest": values["calculation_digest"],
            "calculation_receipt_digest": values["calculation_receipt_digest"],
            "report_digest": values["report_digest"],
            "publication_receipt_digest": values["publication_receipt_digest"],
        }

    def _values(self) -> dict[str, Any]:
        return {name: getattr(self, name) for name in _STATE_FIELDS}

    def _transition(self, stage: SessionStage, **changes: Any) -> "PlanningSession":
        values = self._values()
        values.update(changes)
        values["revision"] = self.revision + 1
        values["stage"] = stage
        return type(self)._build(**values)

    def _at(self, *stages: SessionStage) -> None:
        if self.stage not in stages:
            raise SessionTransitionError("command is out of order")

    def _bound(self, name: str, supplied: str) -> None:
        expected = getattr(self, name)
        if expected is None or supplied != expected:
            raise SessionTransitionError("dependency digest does not match the snapshot")

    def confirm_profile(self, profile_digest: str) -> "PlanningSession":
        self._at(SessionStage.INTAKE)
        if _require_digest(profile_digest, "profile_digest") != self.profile_digest:
            raise SessionTransitionError("profile digest does not match intake")
        return self._transition(SessionStage.PROFILE_CONFIRMED)

    def revise_profile(self, profile_digest: str) -> "PlanningSession":
        self._at(*tuple(stage for stage in SessionStage if stage is not SessionStage.INTAKE))
        value = _require_digest(profile_digest, "profile_digest")
        if value == self.profile_digest:
            raise SessionTransitionError("profile revision must change the digest")
        return self._transition(
            SessionStage.PROFILE_CONFIRMED,
            profile_digest=value,
            preflight_digest=None,
            preflight_degradation_codes=(),
            query_plan_digest=None,
            expected_task_ids=(),
            completed_task_ids=(),
            completed_artifact_digests=(),
            completed_provenance_digests=(),
            completed_usable_flags=(),
            completed_receipt_digests=(),
            unavailable_task_ids=(),
            unavailable_reason_codes=(),
            evidence_manifest_hash=None,
            evidence_receipt_digest=None,
            calculation_digest=None,
            calculation_receipt_digest=None,
            report_digest=None,
            publication_receipt_digest=None,
        )

    def with_preflight(self, report: CapabilityReport) -> "PlanningSession":
        self._at(SessionStage.PROFILE_CONFIRMED)
        identity, degradation_codes = _preflight_identity(report)
        return self._transition(
            SessionStage.PREFLIGHT_COMPLETE,
            preflight_digest=identity,
            preflight_degradation_codes=degradation_codes,
        )

    def with_query_plan(
        self,
        query_plan: Any,
        *,
        profile: Any,
    ) -> "PlanningSession":
        self._at(SessionStage.PREFLIGHT_COMPLETE)
        _canonical_profile, identity, validated = _validated_planning_context(
            self,
            profile,
            query_plan,
            require_bound_universe=False,
        )
        expected = tuple(sorted(task.task_id for task in validated.tasks))
        return self._transition(
            SessionStage.QUERY_PLAN_READY,
            query_plan_digest=identity,
            expected_task_ids=expected,
        )

    def next_tasks(self, query_plan: Any, *, profile: Any) -> tuple[Any, ...]:
        """Return unresolved typed QueryTask records without executing them."""

        self._at(SessionStage.QUERY_PLAN_READY, SessionStage.RESEARCH_IN_PROGRESS)
        _canonical_profile, _identity, validated = _validated_planning_context(
            self,
            profile,
            query_plan,
            require_bound_universe=True,
        )
        tasks = validated.tasks
        if not isinstance(tasks, tuple) or any(
            type(task).__name__ != "QueryTask" or not hasattr(task, "to_dict")
            for task in tasks
        ):
            raise TypeError("query plan must contain typed QueryTask records")
        resolved = set((*self.completed_task_ids, *self.unavailable_task_ids))
        return tuple(task for task in tasks if task.task_id not in resolved)

    def ingest_task(
        self,
        task_id: str,
        *,
        query_plan_digest: str,
        query_plan: Any,
        profile: Any,
        outcome: str,
        evidence_outcome: TaskEvidenceOutcome | None = None,
        newer_evidence_outcome: TaskEvidenceOutcome | None = None,
        artifact_digest: str | None = None,
        provenance_digest: str | None = None,
        unavailable_reason: str | None = None,
    ) -> "PlanningSession":
        self._at(SessionStage.QUERY_PLAN_READY, SessionStage.RESEARCH_IN_PROGRESS)
        canonical_profile, identity, validated = _validated_planning_context(
            self,
            profile,
            query_plan,
            require_bound_universe=True,
        )
        if _require_digest(query_plan_digest, "query_plan_digest") != identity:
            raise SessionTransitionError("query plan digest does not match input")
        if not isinstance(task_id, str) or _TASK_ID.fullmatch(task_id) is None:
            raise PlanningSessionInputError("task_id is invalid")
        if task_id not in self.expected_task_ids:
            raise PlanningSessionInputError("task_id is outside the query plan")
        if task_id in self.completed_task_ids or task_id in self.unavailable_task_ids:
            raise SessionTransitionError("task outcome was already ingested")
        if outcome not in {"completed", "unavailable"}:
            raise PlanningSessionInputError("task outcome is invalid")
        completed_records = list(
            zip(
                self.completed_task_ids,
                self.completed_artifact_digests,
                self.completed_provenance_digests,
                self.completed_usable_flags,
                self.completed_receipt_digests,
            )
        )
        unavailable_records = list(
            zip(self.unavailable_task_ids, self.unavailable_reason_codes)
        )
        if outcome == "completed":
            if unavailable_reason is not None:
                raise PlanningSessionInputError(
                    "completed task cannot carry an unavailable reason"
                )
            if evidence_outcome is None:
                artifact = _require_digest(artifact_digest, "artifact_digest")
                provenance = _require_digest(
                    provenance_digest, "provenance_digest"
                )
                usable = False
            else:
                if artifact_digest is not None or provenance_digest is not None:
                    raise PlanningSessionInputError(
                        "typed evidence outcome owns completed metadata"
                    )
                evidence_outcome.validate(canonical_profile, validated)
                if (
                    evidence_outcome.task_id != task_id
                    or evidence_outcome.profile_digest != self.profile_digest
                    or evidence_outcome.query_plan_digest != self.query_plan_digest
                ):
                    raise SessionTransitionError(
                        "evidence outcome does not match the session task"
                    )
                artifact = evidence_outcome.artifact_digest
                provenance = evidence_outcome.provenance_digest
                usable = evidence_outcome.usable
            receipt = (
                evidence_outcome.receipt_digest
                if evidence_outcome is not None
                else None
            )
            if newer_evidence_outcome is not None:
                raise PlanningSessionInputError(
                    "completed task cannot carry a newer evidence receipt"
                )
            completed_records.append((task_id, artifact, provenance, usable, receipt))
        else:
            if (
                artifact_digest is not None
                or provenance_digest is not None
                or evidence_outcome is not None
            ):
                raise PlanningSessionInputError(
                    "unavailable task cannot carry completed metadata"
                )
            if unavailable_reason not in _UNAVAILABLE_REASONS:
                raise PlanningSessionInputError("unavailable reason code is invalid")
            if unavailable_reason == "newer_comparable_year_accepted":
                if (
                    newer_evidence_outcome is None
                ):
                    raise SessionTransitionError(
                        "newer comparable resolution requires a replayable evidence receipt"
                    )
                newer_evidence_outcome.validate(canonical_profile, validated)
                current = next(
                    (item for item in validated.tasks if item.task_id == task_id),
                    None,
                )
                completed_by_id = dict(
                    zip(
                        self.completed_task_ids,
                        zip(
                            self.completed_artifact_digests,
                            self.completed_provenance_digests,
                            self.completed_usable_flags,
                            self.completed_receipt_digests,
                        ),
                    )
                )
                stored = completed_by_id.get(newer_evidence_outcome.task_id)
                if (
                    current is None
                    or stored is None
                    or stored
                    != (
                        newer_evidence_outcome.artifact_digest,
                        newer_evidence_outcome.provenance_digest,
                        True,
                        newer_evidence_outcome.receipt_digest,
                    )
                    or newer_evidence_outcome.kind != current.kind
                    or newer_evidence_outcome.target_name != current.target_name
                    or newer_evidence_outcome.year <= current.year
                    or "official" not in newer_evidence_outcome.evidence_statuses
                ):
                    raise SessionTransitionError(
                        "no official newer comparable task was accepted"
                    )
            elif newer_evidence_outcome is not None:
                raise PlanningSessionInputError(
                    "newer evidence receipt requires the comparable-year reason"
                )
            unavailable_records.append((task_id, unavailable_reason))
        completed_records.sort(key=lambda item: item[0])
        unavailable_records.sort(key=lambda item: item[0])
        return self._transition(
            SessionStage.RESEARCH_IN_PROGRESS,
            completed_task_ids=tuple(item[0] for item in completed_records),
            completed_artifact_digests=tuple(
                item[1] for item in completed_records
            ),
            completed_provenance_digests=tuple(
                item[2] for item in completed_records
            ),
            completed_usable_flags=tuple(item[3] for item in completed_records),
            completed_receipt_digests=tuple(item[4] for item in completed_records),
            unavailable_task_ids=tuple(item[0] for item in unavailable_records),
            unavailable_reason_codes=tuple(
                item[1] for item in unavailable_records
            ),
        )

    def finalize_evidence(
        self,
        evidence_outcome: EvidenceManifestOutcome,
        *,
        query_plan: Any,
        profile: Any,
    ) -> "PlanningSession":
        self._at(SessionStage.RESEARCH_IN_PROGRESS)
        canonical_profile, _identity, validated = _validated_planning_context(
            self,
            profile,
            query_plan,
            require_bound_universe=True,
        )
        actual = tuple(
            sorted((*self.completed_task_ids, *self.unavailable_task_ids))
        )
        if actual != self.expected_task_ids:
            raise SessionTransitionError("research coverage is incomplete")
        if type(evidence_outcome) is not EvidenceManifestOutcome:
            raise TypeError("evidence_outcome must be an EvidenceManifestOutcome")
        evidence_outcome.validate(self, canonical_profile, validated)
        return self._transition(
            SessionStage.EVIDENCE_FINALIZED,
            evidence_manifest_hash=evidence_outcome.manifest_hash,
            evidence_receipt_digest=evidence_outcome.receipt_digest,
        )

    def with_calculation(
        self,
        calculation_outcome: CalculationOutcome,
        *,
        query_plan: Any,
        profile: Any,
    ) -> "PlanningSession":
        self._at(SessionStage.EVIDENCE_FINALIZED)
        if type(calculation_outcome) is not CalculationOutcome:
            raise TypeError("calculation_outcome must be a CalculationOutcome")
        calculation_outcome.validate(self, profile, query_plan)
        return self._transition(
            SessionStage.CALCULATION_COMPLETE,
            calculation_digest=calculation_outcome.report_model_digest,
            calculation_receipt_digest=calculation_outcome.receipt_digest,
        )

    def publish_report(
        self,
        publication_outcome: ReportPublicationOutcome,
        *,
        query_plan: Any,
        profile: Any,
    ) -> "PlanningSession":
        self._at(SessionStage.CALCULATION_COMPLETE)
        if type(publication_outcome) is not ReportPublicationOutcome:
            raise TypeError(
                "publication_outcome must be a ReportPublicationOutcome"
            )
        publication_outcome.validate(self, profile, query_plan)
        return self._transition(
            SessionStage.REPORT_PUBLISHED,
            report_digest=publication_outcome.rendered_digest,
            publication_receipt_digest=publication_outcome.receipt_digest,
        )

    def to_dict(self) -> dict[str, Any]:
        payload = self._state_payload(self._values())
        payload["session_digest"] = self.session_digest
        return payload

    def to_json_bytes(self) -> bytes:
        return _canonical_bytes(self.to_dict())

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "PlanningSession":
        if not isinstance(payload, Mapping) or set(payload) != _SERIALIZED_FIELDS:
            raise PlanningSessionInputError("snapshot fields do not match the contract")
        if payload.get("schema_version") != _SCHEMA_VERSION:
            raise PlanningSessionInputError("snapshot schema version is unsupported")
        raw = {name: payload[name] for name in _STATE_FIELDS}
        candidate = cls._build(**raw)
        if payload["session_digest"] != candidate.session_digest:
            raise PlanningSessionInputError("snapshot digest is invalid")
        return candidate

    @property
    def coverage(self) -> dict[str, Any]:
        resolved = len(self.completed_task_ids) + len(self.unavailable_task_ids)
        resolved_ids = {*self.completed_task_ids, *self.unavailable_task_ids}
        return {
            "expected": len(self.expected_task_ids),
            "completed": len(self.completed_task_ids),
            "unavailable": len(self.unavailable_task_ids),
            "remaining": len(self.expected_task_ids) - resolved,
            "gap_task_ids": [
                task_id
                for task_id in self.expected_task_ids
                if task_id not in resolved_ids
            ],
        }

    def status(self) -> dict[str, Any]:
        """Project durable state into a deterministic, path-neutral control view."""

        coverage = self.coverage
        remaining = tuple(coverage["gap_task_ids"])
        if self.stage is SessionStage.INTAKE:
            actions = ({"type": "confirm_profile"},)
        elif self.stage is SessionStage.PROFILE_CONFIRMED:
            actions = ({"type": "run_preflight"},)
        elif self.stage is SessionStage.PREFLIGHT_COMPLETE:
            actions = ({"type": "build_query_plan"},)
        elif self.stage in (
            SessionStage.QUERY_PLAN_READY,
            SessionStage.RESEARCH_IN_PROGRESS,
        ):
            actions = (
                tuple(
                    {"type": "query_task", "task_id": task_id}
                    for task_id in remaining
                )
                if remaining
                else ({"type": "finalize_evidence"},)
            )
        elif self.stage is SessionStage.EVIDENCE_FINALIZED:
            actions = ({"type": "compute"},)
        elif self.stage is SessionStage.CALCULATION_COMPLETE:
            actions = ({"type": "publish_report"},)
        else:
            actions = ()
        return {
            "session_id": self.session_id,
            "revision": self.revision,
            "stage": self.stage.value,
            "coverage": coverage,
            "next_actions": list(actions),
            "degradations": sorted(
                {
                    *self.preflight_degradation_codes,
                    *self.unavailable_reason_codes,
                }
            ),
        }


def _file_identity(value: os.stat_result) -> tuple[int, int, int, int]:
    return value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns


def _stable_file_state(value: os.stat_result) -> tuple[int, int, int, int, int]:
    return (*_file_identity(value), value.st_ctime_ns)


def _same_file(left: os.stat_result, right: os.stat_result) -> bool:
    return left.st_dev == right.st_dev and left.st_ino == right.st_ino


def _run_cleanups(
    primary: BaseException | None,
    actions: Sequence[Any],
    *,
    reason_code: str,
) -> None:
    cleanup_error: BaseException | None = None
    for action in actions:
        try:
            action()
        except BaseException as error:
            if cleanup_error is None:
                cleanup_error = error
    if primary is None and cleanup_error is not None:
        raise PlanningSessionStoreError(reason_code) from cleanup_error


def _unlink_if_owned(path: Path, identity: os.stat_result) -> None:
    try:
        current = os.lstat(path)
    except FileNotFoundError:
        return
    if _same_file(current, identity):
        path.unlink()


def _lock_for_stable_read(descriptor: int, size: int) -> Any:
    """Lock reads where supported; POSIX flock remains advisory by design."""

    if os.name == "nt":
        import msvcrt

        length = max(size, 1)
        os.lseek(descriptor, 0, os.SEEK_SET)
        msvcrt.locking(descriptor, msvcrt.LK_NBRLCK, length)

        def unlock() -> None:
            os.lseek(descriptor, 0, os.SEEK_SET)
            msvcrt.locking(descriptor, msvcrt.LK_UNLCK, length)

        return unlock

    import fcntl

    fcntl.flock(descriptor, fcntl.LOCK_SH | fcntl.LOCK_NB)
    return lambda: fcntl.flock(descriptor, fcntl.LOCK_UN)


def _read_fd_once(
    descriptor: int,
    maximum_bytes: int = _MAX_SNAPSHOT_BYTES,
) -> bytes:
    os.lseek(descriptor, 0, os.SEEK_SET)
    chunks = []
    remaining = maximum_bytes + 1
    while remaining:
        chunk = os.read(descriptor, min(64 * 1024, remaining))
        if not chunk:
            break
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def _read_bound_file(
    path_value: Any,
    *,
    expected_identity: os.stat_result | None = None,
    maximum_bytes: int = _MAX_SNAPSHOT_BYTES,
) -> bytes:
    """Read one bounded regular file from one fd and recheck its path identity."""

    path = Path(path_value)
    descriptor: int | None = None
    unlock: Any | None = None
    primary: BaseException | None = None
    try:
        before_path = os.lstat(path)
        if (
            stat.S_ISLNK(before_path.st_mode)
            or not stat.S_ISREG(before_path.st_mode)
            or (
                expected_identity is not None
                and _file_identity(expected_identity) != _file_identity(before_path)
            )
        ):
            raise OSError("unsafe input")
        flags = (
            os.O_RDONLY
            | getattr(os, "O_BINARY", 0)
            | getattr(os, "O_NOFOLLOW", 0)
        )
        descriptor = os.open(path, flags)
        before_fd = os.fstat(descriptor)
        if (
            not stat.S_ISREG(before_fd.st_mode)
            or not _same_file(before_path, before_fd)
            or before_fd.st_size > maximum_bytes
        ):
            raise OSError("unsafe input")
        unlock = _lock_for_stable_read(descriptor, before_fd.st_size)
        first_before = os.fstat(descriptor)
        first = _read_fd_once(descriptor, maximum_bytes)
        first_after = os.fstat(descriptor)
        second_before = os.fstat(descriptor)
        second = _read_fd_once(descriptor, maximum_bytes)
        second_after = os.fstat(descriptor)
        after_fd = os.fstat(descriptor)
        after_path = os.lstat(path)
        if (
            len(first) > maximum_bytes
            or len(first) != before_fd.st_size
            or first != second
            or _stable_file_state(before_fd) != _stable_file_state(first_before)
            or _stable_file_state(first_before) != _stable_file_state(first_after)
            or _stable_file_state(first_after) != _stable_file_state(second_before)
            or _stable_file_state(second_before) != _stable_file_state(second_after)
            or _stable_file_state(before_fd) != _stable_file_state(after_fd)
            or _file_identity(before_fd) != _file_identity(after_path)
        ):
            raise OSError("input identity changed")
        return first
    except BaseException as error:
        primary = error
        if isinstance(error, (KeyboardInterrupt, SystemExit, GeneratorExit)):
            raise
        raise PlanningSessionInputError("unable to read bounded input") from error
    finally:
        actions = []
        if unlock is not None:
            actions.append(unlock)
        if descriptor is not None:
            actions.append(lambda: os.close(descriptor))
        _run_cleanups(primary, actions, reason_code="cleanup_failed")


class PlanningSessionStore:
    """Exclusive append-only snapshot storage in one private directory."""

    def __init__(self, root: str | os.PathLike[str]) -> None:
        self.root = Path(root)
        try:
            info = os.lstat(self.root)
            if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
                raise OSError("unsafe root")
        except OSError as error:
            raise PlanningSessionStoreError("unsafe_store") from error

    def _path(self, session_id: str, revision: int) -> Path:
        if _SESSION_ID.fullmatch(session_id) is None:
            raise PlanningSessionInputError("session_id is invalid")
        return self.root / f"{session_id}.{revision:08d}.json"

    def save(self, session: PlanningSession) -> Path:
        if type(session) is not PlanningSession:
            raise TypeError("session must be a strict PlanningSession")
        # Re-run the same parser used on recovery before touching storage so
        # an object assembled through private Python mechanics cannot publish.
        if PlanningSession.from_dict(session.to_dict()) != session:
            raise PlanningSessionInputError("session object is not canonical")
        destination = self._path(session.session_id, session.revision)
        payload = session.to_json_bytes()
        source_path: Path | None = None
        source_fd: int | None = None
        source_identity: os.stat_result | None = None
        published_identity: os.stat_result | None = None
        primary: BaseException | None = None
        try:
            source_fd, temporary_name = tempfile.mkstemp(
                dir=self.root, prefix=".planning-session-", suffix=".tmp"
            )
            source_path = Path(temporary_name)
            os.chmod(source_path, 0o600)
            source_identity = os.fstat(source_fd)
            offset = 0
            while offset < len(payload):
                written = os.write(source_fd, payload[offset:])
                if written <= 0:
                    raise OSError("partial snapshot write")
                offset += written
            os.fsync(source_fd)
            durable_identity = os.fstat(source_fd)
            visible_source = os.lstat(source_path)
            if (
                not _same_file(source_identity, durable_identity)
                or _file_identity(durable_identity) != _file_identity(visible_source)
                or durable_identity.st_size != len(payload)
            ):
                raise OSError("temporary identity changed")
            os.link(source_path, destination)
            destination_identity = os.lstat(destination)
            if not _same_file(durable_identity, destination_identity):
                raise OSError("published identity changed")
            published_identity = destination_identity
            if (
                _read_bound_file(
                    destination, expected_identity=durable_identity
                )
                != payload
            ):
                raise OSError("published content changed")
            return destination
        except BaseException as error:
            primary = error
            if isinstance(error, (KeyboardInterrupt, SystemExit, GeneratorExit)):
                raise
            reason = (
                "destination_owned"
                if isinstance(error, FileExistsError)
                else "publish_failed"
            )
            raise PlanningSessionStoreError(reason) from error
        finally:
            actions = []
            if source_fd is not None:
                actions.append(lambda: os.close(source_fd))
            if source_path is not None and source_identity is not None:
                actions.append(
                    lambda: _unlink_if_owned(source_path, source_identity)
                )
            if primary is not None and published_identity is not None:
                actions.append(
                    lambda: _unlink_if_owned(destination, published_identity)
                )
            _run_cleanups(primary, actions, reason_code="cleanup_failed")

    def _read(self, path: Path) -> PlanningSession:
        try:
            data = _read_bound_file(path)
            payload = _strict_json(data)
            session = PlanningSession.from_dict(payload)
            match = _SNAPSHOT_NAME.fullmatch(path.name)
            if (
                match is None
                or session.session_id != match.group(1)
                or session.revision != int(match.group(2))
            ):
                raise PlanningSessionInputError("snapshot identity is invalid")
            return session
        except (OSError, UnicodeError, ValueError, TypeError) as error:
            raise PlanningSessionStoreError("invalid_snapshot") from error

    def load(self, session_id: str, revision: int | None = None) -> PlanningSession:
        if not isinstance(session_id, str) or _SESSION_ID.fullmatch(session_id) is None:
            raise PlanningSessionInputError("session_id is invalid")
        if revision is None:
            candidates = []
            try:
                for item in self.root.iterdir():
                    match = _SNAPSHOT_NAME.fullmatch(item.name)
                    if match is not None and match.group(1) == session_id:
                        candidates.append((int(match.group(2)), item))
            except OSError as error:
                raise PlanningSessionStoreError("read_failed") from error
            if not candidates:
                raise PlanningSessionStoreError("session_missing")
            path = max(candidates, key=lambda item: item[0])[1]
        else:
            if (
                isinstance(revision, bool)
                or not isinstance(revision, int)
                or revision < 0
                or revision > 99_999_999
            ):
                raise PlanningSessionInputError("revision is invalid")
            path = self._path(session_id, revision)
        return self._read(path)


def _validate_private_bundle_path(value: Path) -> Path:
    if not isinstance(value, Path):
        raise TypeError("replay bundle path must be a Path")
    try:
        info = os.lstat(value)
        resolved = value.resolve(strict=True)
        if (
            stat.S_ISLNK(info.st_mode)
            or not stat.S_ISDIR(info.st_mode)
            or resolved != value
        ):
            raise OSError("unsafe bundle path")
    except OSError as error:
        raise PlanningSessionInputError("replay bundle path is unavailable") from error
    return resolved


def _validate_replay_task_ledger(
    session: PlanningSession,
    profile: Any,
    query_plan: Any,
    task_outcomes: Sequence[TaskEvidenceOutcome],
) -> tuple[TaskEvidenceOutcome, ...]:
    if isinstance(task_outcomes, (str, bytes, bytearray)):
        raise TypeError("replay task outcomes must be typed receipts")
    outcomes = tuple(sorted(tuple(task_outcomes), key=lambda item: item.task_id))
    if any(type(item) is not TaskEvidenceOutcome for item in outcomes):
        raise TypeError("replay task outcomes must be typed receipts")
    if tuple(item.task_id for item in outcomes) != session.completed_task_ids:
        raise PlanningSessionInputError(
            "replay task receipts do not match the completed ledger"
        )
    for index, outcome in enumerate(outcomes):
        outcome.validate(profile, query_plan)
        stored = (
            session.completed_artifact_digests[index],
            session.completed_provenance_digests[index],
            session.completed_usable_flags[index],
            session.completed_receipt_digests[index],
        )
        replayed = (
            outcome.artifact_digest,
            outcome.provenance_digest,
            outcome.usable,
            outcome.receipt_digest,
        )
        if stored != replayed:
            raise PlanningSessionInputError(
                "replay task receipt disagrees with the completed ledger"
            )
    return outcomes


def _replay_adapter_row(value: Any, row_type: Any) -> Any:
    expected = {
        "values",
        "cell_status",
        "location",
        "confidence",
        "warnings",
    }
    is_ocr = "cell_locations" in {item.name for item in fields(row_type)}
    if is_ocr:
        expected.add("cell_locations")
    if not isinstance(value, Mapping) or set(value) != expected:
        raise PlanningSessionInputError("replay adapter row is invalid")
    arguments = {
        "values": value["values"],
        "cell_status": value["cell_status"],
        "location": value["location"],
        "confidence": value["confidence"],
        "warnings": tuple(value["warnings"]),
    }
    if is_ocr:
        arguments["cell_locations"] = value["cell_locations"]
    return row_type(
        **arguments,
    )


def _replay_adapter_table(value: Any, contracts: Mapping[str, Any]) -> Any:
    expected = {
        "table_id",
        "caption",
        "sheet",
        "rows",
        "coverage",
        "warnings",
        "extraction_method",
    }
    if not isinstance(value, Mapping):
        raise PlanningSessionInputError("replay adapter table is invalid")
    is_ocr = value.get("extraction_method") == "host-ocr-rows"
    if is_ocr:
        expected.add("mapping_snapshot")
    if set(value) != expected:
        raise PlanningSessionInputError("replay adapter table is invalid")
    if not isinstance(value["rows"], list) or not isinstance(
        value["coverage"], Mapping
    ):
        raise PlanningSessionInputError("replay adapter table is invalid")
    table_type = contracts["ExtractedTable"]
    row_type = contracts["ExtractedRow"]
    arguments: dict[str, Any] = {}
    if is_ocr:
        if __package__ in (None, ""):
            from scripts.adapters import ColumnMapping
            from scripts.adapters.ocr_rows import OcrExtractedRow, OcrExtractedTable
        else:
            from .adapters import ColumnMapping
            from .adapters.ocr_rows import OcrExtractedRow, OcrExtractedTable
        snapshot = value["mapping_snapshot"]
        if not isinstance(snapshot, Mapping) or set(snapshot) != {
            "columns",
            "roles",
            "score_scale",
        }:
            raise PlanningSessionInputError("replay OCR mapping is invalid")
        mapping = ColumnMapping(
            snapshot["columns"],
            roles=snapshot["roles"],
            score_scale=snapshot["score_scale"],
        )
        canonical_snapshot = {
            "columns": {name: list(aliases) for name, aliases in mapping.items()},
            "roles": dict(mapping.roles),
            "score_scale": (
                None
                if mapping.score_scale is None
                else list(mapping.score_scale)
            ),
        }
        if canonical_snapshot != snapshot:
            raise PlanningSessionInputError("replay OCR mapping is invalid")
        table_type = OcrExtractedTable
        row_type = OcrExtractedRow
        arguments["mapping_snapshot"] = snapshot
    return table_type(
        table_id=value["table_id"],
        caption=value["caption"],
        sheet=value["sheet"],
        rows=tuple(
            _replay_adapter_row(item, row_type)
            for item in value["rows"]
        ),
        coverage=contracts["ExtractedCoverage"](**value["coverage"]),
        warnings=tuple(value["warnings"]),
        extraction_method=value["extraction_method"],
        **arguments,
    )


def _replay_candidate(value: Any, contracts: Mapping[str, Any]) -> Any:
    expected = {
        "source_id",
        "url",
        "publisher",
        "tier",
        "published_at",
        "retrieved_at",
        "content_hash",
        "citation_root",
        "summary",
    }
    if not isinstance(value, Mapping) or set(value) != expected:
        raise PlanningSessionInputError("replay source candidate is invalid")
    return contracts["SourceCandidate"](
        source_id=value["source_id"],
        url=value["url"],
        publisher=value["publisher"],
        tier=contracts["SourceTier"](value["tier"]),
        published_at=value["published_at"],
        retrieved_at=value["retrieved_at"],
        content_hash=value["content_hash"],
        citation_root=value["citation_root"],
        summary=value["summary"],
    )


def _replay_contracts() -> dict[str, Any]:
    if __package__ in (None, ""):
        from scripts.adapters import ExtractedCoverage, ExtractedRow, ExtractedTable
        from scripts.contracts import EvidenceStatus, SourceCandidate, SourceTier
        from scripts.validate_data import ValidatedAdmissionRow
    else:
        from .adapters import ExtractedCoverage, ExtractedRow, ExtractedTable
        from .contracts import EvidenceStatus, SourceCandidate, SourceTier
        from .validate_data import ValidatedAdmissionRow
    return {
        "ExtractedCoverage": ExtractedCoverage,
        "ExtractedRow": ExtractedRow,
        "ExtractedTable": ExtractedTable,
        "EvidenceStatus": EvidenceStatus,
        "SourceCandidate": SourceCandidate,
        "SourceTier": SourceTier,
        "ValidatedAdmissionRow": ValidatedAdmissionRow,
    }


def _bridge_journal_record(bridge: Any) -> dict[str, str]:
    if __package__ in (None, ""):
        from scripts.adapters.admission_bridge import AdmissionEvidenceBridge
        from scripts.adapters.pathway_bridge import PathwayPolicyEvidenceBridge
        from scripts.adapters.rank_bridge import RankEvidenceBridge
        from scripts.adapters.school_fit_bridge import SchoolFitEvidenceBridge
    else:
        from .adapters.admission_bridge import AdmissionEvidenceBridge
        from .adapters.pathway_bridge import PathwayPolicyEvidenceBridge
        from .adapters.rank_bridge import RankEvidenceBridge
        from .adapters.school_fit_bridge import SchoolFitEvidenceBridge
    if type(bridge) is AdmissionEvidenceBridge:
        return {"kind": "admission", "origin": bridge._origin_json}
    if type(bridge) is RankEvidenceBridge:
        return {"kind": "rank", "origin": bridge._origin_json}
    if type(bridge) is PathwayPolicyEvidenceBridge:
        return {"kind": "pathway", "origin": bridge._projection_json}
    if type(bridge) is SchoolFitEvidenceBridge:
        return {"kind": "school_fit", "origin": bridge._origin_json}
    raise TypeError("replay journal only accepts factory evidence bridges")


def _replay_bridge_journal_record(
    value: Any,
    profile: Any,
    query_plan: Any,
) -> Any:
    if (
        not isinstance(value, Mapping)
        or set(value) != {"kind", "origin"}
        or not isinstance(value["kind"], str)
        or not isinstance(value["origin"], str)
    ):
        raise PlanningSessionInputError("replay bridge record is invalid")
    try:
        origin = json.loads(value["origin"])
    except (TypeError, ValueError, json.JSONDecodeError):
        raise PlanningSessionInputError("replay bridge origin is invalid") from None
    if not isinstance(origin, dict) or _canonical_bytes(origin).decode("utf-8") != value["origin"]:
        raise PlanningSessionInputError("replay bridge origin is not canonical")
    contracts = _replay_contracts()
    task_payload = origin.get("task")
    task = next(
        (
            item
            for item in query_plan.tasks
            if isinstance(task_payload, Mapping)
            and item.task_id == task_payload.get("task_id")
        ),
        None,
    )
    if value["kind"] in {"admission", "rank", "school_fit"} and (
        task is None or task.to_dict() != task_payload
    ):
        raise PlanningSessionInputError("replay bridge task is outside the query plan")
    try:
        if value["kind"] == "admission":
            if __package__ in (None, ""):
                from scripts.adapters.admission_bridge import bridge_admission_evidence
            else:
                from .adapters.admission_bridge import bridge_admission_evidence
            table = _replay_adapter_table(origin.get("table"), contracts)
            adapter_payload = origin.get("adapter_row")
            matches = tuple(
                row for row in table.rows if row.to_dict() == adapter_payload
            )
            if len(matches) != 1:
                raise PlanningSessionInputError("replay admission row is ambiguous")
            candidates = tuple(
                _replay_candidate(item, contracts) for item in origin.get("sources", ())
            )
            return bridge_admission_evidence(
                table=table,
                adapter_row=matches[0],
                task=task,
                dataset_row=contracts["ValidatedAdmissionRow"].from_mapping(
                    origin.get("dataset_row")
                ),
                fact_id=origin.get("fact_id"),
                candidates=candidates,
                coverage_status=contracts["EvidenceStatus"](
                    origin.get("coverage_status")
                ),
            )
        if value["kind"] == "rank":
            if __package__ in (None, ""):
                from scripts.adapters.rank_bridge import bridge_rank_evidence
            else:
                from .adapters.rank_bridge import bridge_rank_evidence
            table = _replay_adapter_table(origin.get("table"), contracts)
            index = origin.get("adapter_row_index")
            if (
                not isinstance(index, int)
                or isinstance(index, bool)
                or index < 0
                or index >= len(table.rows)
                or table.rows[index].to_dict() != origin.get("adapter_row")
            ):
                raise PlanningSessionInputError("replay rank row is invalid")
            candidates = tuple(
                _replay_candidate(item, contracts) for item in origin.get("sources", ())
            )
            return bridge_rank_evidence(
                profile=profile,
                plan=query_plan,
                task=task,
                table=table,
                extracted_row=table.rows[index],
                candidates=candidates,
                coverage_status=contracts["EvidenceStatus"](
                    origin.get("coverage_status")
                ),
            )
        if value["kind"] == "pathway":
            if __package__ in (None, ""):
                from scripts.adapters.pathway_bridge import (
                    bridge_pathway_policy_evidence,
                )
                from scripts.adapters.pathway_extraction import (
                    replay_pathway_policy_projection,
                )
            else:
                from .adapters.pathway_bridge import bridge_pathway_policy_evidence
                from .adapters.pathway_extraction import (
                    replay_pathway_policy_projection,
                )
            return bridge_pathway_policy_evidence(
                replay_pathway_policy_projection(origin)
            )
        if value["kind"] == "school_fit":
            if __package__ in (None, ""):
                from scripts.adapters.school_fit_bridge import (
                    _replay_school_fit_public_text_origin,
                    bridge_school_fit_evidence,
                )
            else:
                from .adapters.school_fit_bridge import (
                    _replay_school_fit_public_text_origin,
                    bridge_school_fit_evidence,
                )
            if origin.get("adapter_kind") == "public-text":
                return _replay_school_fit_public_text_origin(
                    origin,
                    profile,
                    query_plan,
                )
            table_payloads = origin.get("tables")
            indexes = origin.get("adapter_row_indexes")
            source_payloads = origin.get("sources")
            if (
                not isinstance(table_payloads, list)
                or not isinstance(indexes, list)
                or not isinstance(source_payloads, list)
                or not table_payloads
                or not (
                    len(table_payloads) == len(indexes) == len(source_payloads)
                )
            ):
                raise PlanningSessionInputError(
                    "replay school-fit bridge origin is invalid"
                )
            tables = tuple(
                _replay_adapter_table(item, contracts) for item in table_payloads
            )
            rows = []
            for table, index in zip(tables, indexes):
                if (
                    not isinstance(index, int)
                    or isinstance(index, bool)
                    or index < 0
                    or index >= len(table.rows)
                ):
                    raise PlanningSessionInputError(
                        "replay school-fit row is invalid"
                    )
                rows.append(table.rows[index])
            return bridge_school_fit_evidence(
                profile=profile,
                plan=query_plan,
                task=task,
                tables=tables,
                adapter_rows=tuple(rows),
                candidates=tuple(
                    _replay_candidate(item, contracts)
                    for item in source_payloads
                ),
            )
    except PlanningSessionInputError:
        raise
    except (KeyError, TypeError, ValueError) as error:
        raise PlanningSessionInputError("replay bridge factory rejected its origin") from error
    raise PlanningSessionInputError("replay bridge kind is unsupported")


def _task_outcome_journal_record(outcome: TaskEvidenceOutcome) -> dict[str, Any]:
    return {
        "task_id": outcome.task_id,
        "receipt_digest": outcome.receipt_digest,
        "bridges": [_bridge_journal_record(item) for item in outcome._bridges],
    }


def _replay_task_outcome_journal_record(
    value: Any,
    profile: Any,
    query_plan: Any,
) -> TaskEvidenceOutcome:
    if not isinstance(value, Mapping) or set(value) != {
        "task_id",
        "receipt_digest",
        "bridges",
    }:
        raise PlanningSessionInputError("replay task receipt is invalid")
    task = next(
        (item for item in query_plan.tasks if item.task_id == value["task_id"]),
        None,
    )
    if task is None or not isinstance(value["bridges"], list):
        raise PlanningSessionInputError("replay task receipt is outside the query plan")
    bridges = tuple(
        _replay_bridge_journal_record(item, profile, query_plan)
        for item in value["bridges"]
    )
    outcome = build_task_evidence_outcome(profile, query_plan, task, bridges)
    if outcome.receipt_digest != value["receipt_digest"]:
        raise PlanningSessionInputError("replay task receipt digest disagrees")
    return outcome


def _replay_profile_payload(value: Any) -> Any:
    if not isinstance(value, dict):
        raise PlanningSessionInputError("replay profile is invalid")
    if __package__ in (None, ""):
        from planning_profile import PlanningProfile
    else:
        from .planning_profile import PlanningProfile
    try:
        return PlanningProfile.create(value)
    except (TypeError, ValueError) as error:
        raise PlanningSessionInputError("replay profile is invalid") from error


def _replay_query_plan_payload(value: Any) -> Any:
    if not isinstance(value, dict):
        raise PlanningSessionInputError("replay query plan is invalid")
    if __package__ in (None, ""):
        from query_plan import validate_query_plan_payload
    else:
        from .query_plan import validate_query_plan_payload
    try:
        return validate_query_plan_payload(value)
    except (KeyError, TypeError, ValueError) as error:
        raise PlanningSessionInputError("replay query plan is invalid") from error


def _replay_capability_payload(value: Any) -> CapabilityReport:
    expected = {
        "tier",
        "host_capabilities",
        "available_capabilities",
        "missing_capabilities",
        "degradations",
        "python_version",
        "optional_modules",
    }
    if not isinstance(value, Mapping) or set(value) != expected:
        raise PlanningSessionInputError("replay capability is invalid")
    if __package__ in (None, ""):
        from contracts import CapabilityTier
    else:
        from .contracts import CapabilityTier
    try:
        result = CapabilityReport(
            tier=CapabilityTier(value["tier"]),
            host_capabilities=tuple(value["host_capabilities"]),
            available_capabilities=tuple(value["available_capabilities"]),
            missing_capabilities=tuple(value["missing_capabilities"]),
            degradations=tuple(value["degradations"]),
            python_version=value["python_version"],
            optional_modules=tuple(value["optional_modules"]),
        )
        _preflight_identity(result)
        return result
    except (TypeError, ValueError) as error:
        raise PlanningSessionInputError("replay capability is invalid") from error


class PlanningSessionReplayJournal:
    """Private append-only journal that replays, rather than trusts, receipts."""

    _FIELDS = frozenset(
        {
            "schema_version",
            "session",
            "profile",
            "query_plan",
            "capability",
            "bundle_path",
            "task_receipts",
            "journal_digest",
        }
    )

    def __init__(self, root: str | os.PathLike[str]) -> None:
        self.root = Path(root)
        try:
            info = os.lstat(self.root)
            if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
                raise OSError("unsafe root")
        except OSError as error:
            raise PlanningSessionStoreError("unsafe_replay_store") from error

    def _path(self, session_id: str, revision: int) -> Path:
        if _SESSION_ID.fullmatch(session_id) is None:
            raise PlanningSessionInputError("session_id is invalid")
        if (
            isinstance(revision, bool)
            or not isinstance(revision, int)
            or not 0 <= revision <= 99_999_999
        ):
            raise PlanningSessionInputError("revision is invalid")
        return self.root / f"{session_id}.{revision:08d}.replay.json"

    def _context(
        self,
        session: PlanningSession,
        *,
        profile: Any,
        query_plan: Any | None = None,
        capability_report: CapabilityReport | None = None,
        bundle_path: Path | None = None,
        task_outcomes: Sequence[TaskEvidenceOutcome] = (),
    ) -> PlanningSessionReplayContext:
        if type(session) is not PlanningSession:
            raise TypeError("session must be a PlanningSession")
        session._at(
            SessionStage.PROFILE_CONFIRMED,
            SessionStage.PREFLIGHT_COMPLETE,
            SessionStage.QUERY_PLAN_READY,
            SessionStage.RESEARCH_IN_PROGRESS,
            SessionStage.EVIDENCE_FINALIZED,
            SessionStage.CALCULATION_COMPLETE,
        )
        canonical_profile = _validated_profile(profile)
        canonical_plan = None
        if query_plan is not None:
            _identity, canonical_plan = _validated_query_plan(query_plan)
        if isinstance(task_outcomes, (str, bytes, bytearray)):
            raise TypeError("replay task outcomes must be typed receipts")
        raw_outcomes = tuple(task_outcomes)
        if canonical_plan is None:
            if raw_outcomes:
                raise PlanningSessionInputError(
                    "replay task receipts require a query plan"
                )
            outcomes: tuple[TaskEvidenceOutcome, ...] = ()
        else:
            outcomes = _validate_replay_task_ledger(
                session,
                canonical_profile,
                canonical_plan,
                raw_outcomes,
            )
        retained_bundle = (
            None
            if bundle_path is None
            else _validate_private_bundle_path(bundle_path)
        )
        context = PlanningSessionReplayContext(
            session=session,
            profile=canonical_profile,
            query_plan=canonical_plan,
            capability_report=capability_report,
            bundle_path=retained_bundle,
            task_outcomes=outcomes,
        )
        return context.validate()

    def save(
        self,
        session: PlanningSession,
        *,
        profile: Any,
        query_plan: Any | None = None,
        capability_report: CapabilityReport | None = None,
        bundle_path: Path | None = None,
        task_outcomes: Sequence[TaskEvidenceOutcome] = (),
    ) -> Path:
        context = self._context(
            session,
            profile=profile,
            query_plan=query_plan,
            capability_report=capability_report,
            bundle_path=bundle_path,
            task_outcomes=task_outcomes,
        )
        profile_payload = {
            key: item
            for key, item in context.profile.to_dict().items()
            if key not in {"mode", "digest"}
        }
        body = {
            "schema_version": "1.0",
            "session": context.session.to_dict(),
            "profile": profile_payload,
            "query_plan": (
                None
                if context.query_plan is None
                else context.query_plan.to_dict()
            ),
            "capability": (
                None
                if context.capability_report is None
                else context.capability_report.to_dict()
            ),
            "bundle_path": (
                None if context.bundle_path is None else str(context.bundle_path)
            ),
            "task_receipts": [
                _task_outcome_journal_record(item) for item in context.task_outcomes
            ],
        }
        payload = _canonical_bytes(
            {**body, "journal_digest": _digest_payload(body)}
        )
        if len(payload) > _MAX_REPLAY_JOURNAL_BYTES:
            raise PlanningSessionInputError("replay journal exceeds the bounded size")
        destination = self._path(session.session_id, session.revision)
        source_path: Path | None = None
        source_fd: int | None = None
        source_identity: os.stat_result | None = None
        published_identity: os.stat_result | None = None
        primary: BaseException | None = None
        try:
            source_fd, temporary_name = tempfile.mkstemp(
                dir=self.root,
                prefix=".planning-replay-",
                suffix=".tmp",
            )
            source_path = Path(temporary_name)
            os.chmod(source_path, 0o600)
            source_identity = os.fstat(source_fd)
            offset = 0
            while offset < len(payload):
                written = os.write(source_fd, payload[offset:])
                if written <= 0:
                    raise OSError("partial replay journal write")
                offset += written
            os.fsync(source_fd)
            durable_identity = os.fstat(source_fd)
            visible_source = os.lstat(source_path)
            if (
                not _same_file(source_identity, durable_identity)
                or _file_identity(durable_identity) != _file_identity(visible_source)
                or durable_identity.st_size != len(payload)
            ):
                raise OSError("temporary replay identity changed")
            os.link(source_path, destination)
            destination_identity = os.lstat(destination)
            if not _same_file(durable_identity, destination_identity):
                raise OSError("published replay identity changed")
            published_identity = destination_identity
            if _read_bound_file(
                destination,
                expected_identity=durable_identity,
                maximum_bytes=_MAX_REPLAY_JOURNAL_BYTES,
            ) != payload:
                raise OSError("published replay content changed")
            return destination
        except BaseException as error:
            primary = error
            if isinstance(error, (KeyboardInterrupt, SystemExit, GeneratorExit)):
                raise
            reason = (
                "replay_destination_owned"
                if isinstance(error, FileExistsError)
                else "replay_publish_failed"
            )
            raise PlanningSessionStoreError(reason) from error
        finally:
            actions = []
            if source_fd is not None:
                actions.append(lambda: os.close(source_fd))
            if source_path is not None and source_identity is not None:
                actions.append(lambda: _unlink_if_owned(source_path, source_identity))
            if primary is not None and published_identity is not None:
                actions.append(
                    lambda: _unlink_if_owned(destination, published_identity)
                )
            _run_cleanups(primary, actions, reason_code="replay_cleanup_failed")

    def _load_path(self, path: Path) -> PlanningSessionReplayContext:
        data = _read_bound_file(
            path,
            maximum_bytes=_MAX_REPLAY_JOURNAL_BYTES,
        )
        payload = _strict_json(data, maximum_bytes=_MAX_REPLAY_JOURNAL_BYTES)
        if not isinstance(payload, dict) or set(payload) != self._FIELDS:
            raise PlanningSessionInputError("replay journal fields are invalid")
        body = {key: value for key, value in payload.items() if key != "journal_digest"}
        if (
            payload.get("schema_version") != "1.0"
            or payload.get("journal_digest") != _digest_payload(body)
        ):
            raise PlanningSessionInputError("replay journal digest is invalid")
        session = PlanningSession.from_dict(payload["session"])
        match = _REPLAY_JOURNAL_NAME.fullmatch(path.name)
        if (
            match is None
            or session.session_id != match.group(1)
            or session.revision != int(match.group(2))
        ):
            raise PlanningSessionInputError("replay journal identity is invalid")
        profile = _replay_profile_payload(payload["profile"])
        query_plan = (
            None
            if payload["query_plan"] is None
            else _replay_query_plan_payload(payload["query_plan"])
        )
        capability = (
            None
            if payload["capability"] is None
            else _replay_capability_payload(payload["capability"])
        )
        raw_receipts = payload["task_receipts"]
        if not isinstance(raw_receipts, list):
            raise PlanningSessionInputError("replay task receipts are invalid")
        if raw_receipts and query_plan is None:
            raise PlanningSessionInputError(
                "replay task receipts require a query plan"
            )
        outcomes = tuple(
            _replay_task_outcome_journal_record(item, profile, query_plan)
            for item in raw_receipts
        )
        raw_bundle_path = payload["bundle_path"]
        if raw_bundle_path is not None and not isinstance(raw_bundle_path, str):
            raise PlanningSessionInputError("replay bundle path is invalid")
        bundle_path = (
            None if raw_bundle_path is None else Path(raw_bundle_path)
        )
        return self._context(
            session,
            profile=profile,
            query_plan=query_plan,
            capability_report=capability,
            bundle_path=bundle_path,
            task_outcomes=outcomes,
        )

    def load(
        self,
        session_id: str,
        revision: int | None = None,
    ) -> PlanningSessionReplayContext:
        if not isinstance(session_id, str) or _SESSION_ID.fullmatch(session_id) is None:
            raise PlanningSessionInputError("session_id is invalid")
        if revision is None:
            candidates: list[tuple[int, Path]] = []
            try:
                for item in self.root.iterdir():
                    match = _REPLAY_JOURNAL_NAME.fullmatch(item.name)
                    if match is not None and match.group(1) == session_id:
                        candidates.append((int(match.group(2)), item))
            except OSError as error:
                raise PlanningSessionStoreError("replay_read_failed") from error
            if not candidates:
                raise PlanningSessionStoreError("replay_session_missing")
            path = max(candidates, key=lambda item: item[0])[1]
        else:
            path = self._path(session_id, revision)
        return self._load_path(path)


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise PlanningSessionInputError("duplicate JSON key")
        result[key] = value
    return result


def _strict_json(
    data: bytes,
    *,
    maximum_bytes: int = _MAX_SNAPSHOT_BYTES,
) -> Any:
    if len(data) > maximum_bytes:
        raise PlanningSessionInputError("JSON input exceeds the bounded size")
    try:
        return json.loads(
            data.decode("utf-8"),
            object_pairs_hook=_strict_object,
            parse_constant=lambda _value: (_ for _ in ()).throw(
                PlanningSessionInputError("non-finite JSON number")
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise PlanningSessionInputError("input is not strict UTF-8 JSON") from error


def _load_query_plan(path_value: str) -> Any:
    try:
        if path_value == "-":
            data = sys.stdin.buffer.read(_MAX_SNAPSHOT_BYTES + 1)
        else:
            data = _read_bound_file(path_value)
        payload = _strict_json(data)
        if __package__ in (None, ""):
            from query_plan import validate_query_plan_payload
        else:
            from .query_plan import validate_query_plan_payload
        return validate_query_plan_payload(payload)
    except (OSError, UnicodeError, TypeError, ValueError) as error:
        raise PlanningSessionInputError("query plan input is invalid") from error


def _load_profile(path_value: str) -> Any:
    try:
        if path_value == "-":
            data = sys.stdin.buffer.read(_MAX_SNAPSHOT_BYTES + 1)
        else:
            data = _read_bound_file(path_value)
        payload = _strict_json(data)
        if __package__ in (None, ""):
            from planning_profile import load_planning_profile
        else:
            from .planning_profile import load_planning_profile
        return load_planning_profile(payload)
    except (OSError, UnicodeError, TypeError, ValueError) as error:
        raise PlanningSessionInputError("profile input is invalid") from error


def _load_cli_context(profile_path: str, query_plan_path: str) -> tuple[Any, Any]:
    """Load and replay the typed planning context owned by the host process."""

    profile = _load_profile(profile_path)
    query_plan = _load_query_plan(query_plan_path)
    return profile, query_plan


def _build_cli_evidence_outcome(
    session: PlanningSession,
    profile: Any,
    query_plan: Any,
    bundle_value: str,
) -> EvidenceManifestOutcome:
    """Rebuild the only safely serializable CLI evidence partition.

    Completed tasks retain live factory-only bridge objects and therefore
    cannot cross a raw JSON/argv boundary.  An all-unavailable partition has
    no task receipts to deserialize and can be replayed from its validated
    empty evidence bundle.
    """

    if session.completed_task_ids:
        raise PlanningSessionInputError(
            "completed CLI tasks require live factory evidence receipts"
        )
    try:
        bundle_path = Path(bundle_value).resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise PlanningSessionInputError("evidence bundle input is invalid") from error
    return build_evidence_manifest_outcome(
        session,
        profile,
        query_plan,
        bundle_path=bundle_path,
        task_outcomes=(),
    )


class _SafeParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        del message
        raise PlanningSessionInputError("invalid command")


def _parser() -> argparse.ArgumentParser:
    parser = _SafeParser(description="Advance a recoverable planning session")
    parser.add_argument("--session-dir", required=True)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("--session-id", required=True)
    profile_input = init.add_mutually_exclusive_group(required=True)
    profile_input.add_argument("--profile-digest")
    profile_input.add_argument("--profile")
    confirm = commands.add_parser("confirm")
    confirm.add_argument("--session-id", required=True)
    confirm_input = confirm.add_mutually_exclusive_group(required=True)
    confirm_input.add_argument("--profile-digest")
    confirm_input.add_argument("--profile")
    next_command = commands.add_parser("next")
    next_command.add_argument("--session-id", required=True)
    next_command.add_argument("--profile", required=True)
    next_command.add_argument("--host-capability", action="append", default=[])
    next_command.add_argument("--query-plan")
    ingest = commands.add_parser("ingest")
    ingest.add_argument("--session-id", required=True)
    ingest.add_argument("--profile", required=True)
    ingest.add_argument("--query-plan", required=True)
    ingest.add_argument("--task-id", required=True)
    ingest.add_argument("--outcome", choices=("completed", "unavailable"), required=True)
    # Comparable-year skips are authorized only by a live, factory-only typed
    # receipt replay.  The raw JSON CLI deliberately cannot express one.
    ingest.add_argument("--unavailable-reason", choices=_CLI_UNAVAILABLE_REASONS)
    finalize = commands.add_parser("finalize")
    finalize.add_argument("--session-id", required=True)
    finalize.add_argument("--profile", required=True)
    finalize.add_argument("--query-plan", required=True)
    finalize.add_argument("--evidence-bundle", required=True)
    compute = commands.add_parser("compute")
    compute.add_argument("--session-id", required=True)
    compute.add_argument("--profile", required=True)
    compute.add_argument("--query-plan", required=True)
    compute.add_argument("--evidence-bundle", required=True)
    compute.add_argument("--format", choices=("markdown", "docx"), default="markdown")
    status = commands.add_parser("status")
    status.add_argument("--session-id", required=True)
    return parser


def _output(
    session: PlanningSession,
    next_actions: Sequence[Any] = (),
) -> None:
    payload = session.status()
    if next_actions:
        payload["next_actions"] = list(next_actions)
    sys.stdout.write(_canonical_bytes(payload).decode("utf-8") + "\n")


def main(argv: list[str] | None = None) -> int:
    if sys.version_info < (3, 10):
        sys.stderr.write("planning-session: missing capability\n")
        return 3
    try:
        args = _parser().parse_args(argv)
        store = PlanningSessionStore(args.session_dir)
        if args.command == "init":
            profile = (
                _load_profile(args.profile)
                if args.profile is not None
                else args.profile_digest
            )
            session = PlanningSession.create(args.session_id, profile)
            original_digest = None
        else:
            session = store.load(args.session_id)
            original_digest = session.session_digest
        next_actions: Sequence[Any] = ()
        if args.command == "confirm":
            if session.stage is SessionStage.INTAKE:
                profile_identity = (
                    _profile_identity(_load_profile(args.profile))
                    if args.profile is not None
                    else args.profile_digest
                )
                session = session.confirm_profile(profile_identity)
            else:
                if args.profile is None:
                    raise PlanningSessionInputError(
                        "later profile confirmation requires validated input"
                    )
                session = session.revise_profile(
                    _profile_identity(_load_profile(args.profile))
                )
        elif args.command == "next":
            profile = _load_profile(args.profile)
            if profile.digest != session.profile_digest:
                raise SessionTransitionError(
                    "profile does not match the planning session"
                )
            if session.stage is SessionStage.PROFILE_CONFIRMED:
                if __package__ in (None, ""):
                    from preflight import detect_capabilities
                else:
                    from .preflight import detect_capabilities

                preflight = detect_capabilities(set(args.host_capability))
                session = session.with_preflight(preflight)
            elif session.stage is SessionStage.PREFLIGHT_COMPLETE:
                if args.query_plan is None:
                    raise PlanningSessionInputError("typed query plan input is required")
                query_plan = _load_query_plan(args.query_plan)
                session = session.with_query_plan(query_plan, profile=profile)
                next_actions = tuple(
                    {"type": "query_task", "payload": task.to_dict()}
                    for task in session.next_tasks(query_plan, profile=profile)
                )
            elif session.stage in (
                SessionStage.QUERY_PLAN_READY,
                SessionStage.RESEARCH_IN_PROGRESS,
            ):
                if args.query_plan is None:
                    raise PlanningSessionInputError("typed query plan input is required")
                query_plan = _load_query_plan(args.query_plan)
                next_actions = tuple(
                    {"type": "query_task", "payload": task.to_dict()}
                    for task in session.next_tasks(query_plan, profile=profile)
                )
            else:
                raise SessionTransitionError("no research task is available at this stage")
        elif args.command == "ingest":
            if args.outcome == "completed":
                raise PlanningSessionInputError(
                    "completed CLI ingestion requires a live typed receipt"
                )
            profile, query_plan = _load_cli_context(
                args.profile, args.query_plan
            )
            session = session.ingest_task(
                args.task_id,
                query_plan_digest=_query_plan_identity(query_plan),
                query_plan=query_plan,
                profile=profile,
                outcome=args.outcome,
                unavailable_reason=args.unavailable_reason,
            )
        elif args.command == "finalize":
            profile, query_plan = _load_cli_context(
                args.profile, args.query_plan
            )
            evidence_outcome = _build_cli_evidence_outcome(
                session,
                profile,
                query_plan,
                args.evidence_bundle,
            )
            session = session.finalize_evidence(
                evidence_outcome,
                query_plan=query_plan,
                profile=profile,
            )
        elif args.command == "compute":
            if session.stage not in {
                SessionStage.EVIDENCE_FINALIZED,
                SessionStage.CALCULATION_COMPLETE,
            }:
                raise SessionTransitionError("compute command is out of order")
            profile, query_plan = _load_cli_context(
                args.profile, args.query_plan
            )
            evidence_outcome = _build_cli_evidence_outcome(
                session,
                profile,
                query_plan,
                args.evidence_bundle,
            )
            calculation_outcome = build_calculation_outcome(
                session,
                evidence_outcome,
                profile,
                query_plan,
            )
            if session.stage is SessionStage.EVIDENCE_FINALIZED:
                session = session.with_calculation(
                    calculation_outcome,
                    query_plan=query_plan,
                    profile=profile,
                )
                # Persist the authenticated calculation checkpoint before
                # rendering; a later missing capability or renderer failure is
                # recoverable without accepting a caller-authored digest.
                store.save(session)
                original_digest = session.session_digest
            publication_outcome = build_report_publication_outcome(
                calculation_outcome,
                format=args.format,
            )
            session = session.publish_report(
                publication_outcome,
                query_plan=query_plan,
                profile=profile,
            )
        elif args.command == "status":
            pass
        if original_digest != session.session_digest:
            store.save(session)
        _output(session, next_actions)
        return 0
    except ModuleNotFoundError:
        sys.stderr.write("planning-session: missing capability\n")
        return 3
    except (
        PlanningSessionInputError,
        PlanningSessionStoreError,
        TypeError,
        ValueError,
        OSError,
        UnicodeError,
    ):
        sys.stderr.write("planning-session: invalid session or evidence\n")
        return 2


def _reconfigure_utf8() -> None:
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


__all__ = [
    "PlanningSession",
    "PlanningSessionInputError",
    "PlanningSessionReplayContext",
    "PlanningSessionReplayJournal",
    "PlanningSessionStore",
    "PlanningSessionStoreError",
    "PreflightReport",
    "SessionStage",
    "SessionTransitionError",
    "build_calculation_outcome",
    "build_evidence_manifest_outcome",
    "build_report_publication_outcome",
    "build_task_evidence_outcome",
]


if __name__ == "__main__":
    _reconfigure_utf8()
    raise SystemExit(main())
