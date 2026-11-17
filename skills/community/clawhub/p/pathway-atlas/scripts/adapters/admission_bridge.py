"""Typed bridge from exact adapter rows to authenticated admission evidence.

The bridge owns no admission-row hashing or report thresholds.  It composes an
adapter result with a query task and the validator's immutable row snapshot,
then delegates the complete-row digest to :func:`admission_row_hash`.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any

if __package__ == "scripts.adapters":
    from . import (
        CellStatus,
        ExtractedCoverage,
        ExtractedRow,
        ExtractedTable,
        PublicLocatorError,
        validate_public_locator,
    )
    from ..contracts import (
        EvidenceFact,
        EvidenceStatus,
        FactClaim,
        SourceCandidate,
    )
    from ..evidence import EvidenceStore
    from ..query_plan import QueryTask
    from ..source_policy import evaluate_claims
    from ..validate_data import ValidatedAdmissionRow, admission_row_hash
else:  # ``sys.path`` rooted at ``scripts`` package compatibility.
    from adapters import (  # type: ignore
        CellStatus,
        ExtractedCoverage,
        ExtractedRow,
        ExtractedTable,
        PublicLocatorError,
        validate_public_locator,
    )
    from contracts import (  # type: ignore
        EvidenceFact,
        EvidenceStatus,
        FactClaim,
        SourceCandidate,
    )
    from evidence import EvidenceStore  # type: ignore
    from query_plan import QueryTask  # type: ignore
    from source_policy import evaluate_claims  # type: ignore
    from validate_data import ValidatedAdmissionRow, admission_row_hash  # type: ignore


_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_CONTEXT_FIELDS = frozenset({"year", "province", "subject_group"})
_OBSERVED_FIELDS = frozenset(
    {"school_code", "school_name", "program_group", "min_score", "min_rank"}
)
_OPTIONAL_DECISION_FIELDS = frozenset(
    {
        "city_location",
        "school_province",
        "majors_in_group",
        "institution_type",
        "affordable_for",
        "adjustment_required",
    }
)
_ADMISSION_METHODS = frozenset(
    {"html-table", "xlsx-worksheet", "xls-worksheet", "pdf-text-table", "host-ocr-rows"}
)
_EVIDENCE_STATUSES = frozenset(
    {
        EvidenceStatus.OFFICIAL,
        EvidenceStatus.CORROBORATED,
        EvidenceStatus.REFERENCE,
    }
)
_COVERAGE_STATUSES = _EVIDENCE_STATUSES | frozenset({EvidenceStatus.PARTIAL})


class AdmissionBridgeError(ValueError):
    """Inputs cannot form one exact, report-consumable admission fact."""


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def _canonical_digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(
        _canonical_json(value).encode("utf-8")
    ).hexdigest()


def _canonical_task_snapshot(task: QueryTask) -> QueryTask:
    """Replay every QueryTask field and detach it from caller-owned state."""

    if not isinstance(task, QueryTask):
        raise TypeError("task must be a QueryTask")
    payload = task.to_dict()
    try:
        snapshot = QueryTask(**payload)
    except (KeyError, TypeError, ValueError):
        raise AdmissionBridgeError("query task is not canonical") from None
    if snapshot.to_dict() != payload:
        raise AdmissionBridgeError("query task is not canonical")
    return snapshot


def _bridge_identity_digest(
    *,
    origin_digest: str,
    admission_row_hash: str,
    fact_id: str,
    evidence_status: EvidenceStatus,
    source_ids: tuple[str, ...],
    evidence_method: str,
    extraction_method: str,
    locator: str,
) -> str:
    return _canonical_digest(
        {
            "origin_digest": origin_digest,
            "admission_row_hash": admission_row_hash,
            "fact_id": fact_id,
            "evidence_status": evidence_status.value,
            "source_ids": list(source_ids),
            "evidence_method": evidence_method,
            "extraction_method": extraction_method,
            "locator": locator,
        }
    )


def _safe_id(value: Any, name: str) -> str:
    if not isinstance(value, str) or _SAFE_ID.fullmatch(value) is None:
        raise AdmissionBridgeError(f"{name} is unsafe")
    try:
        validate_public_locator(value)
    except PublicLocatorError:
        raise AdmissionBridgeError(f"{name} is unsafe") from None
    return value


def _source_ids(value: Any) -> tuple[str, ...]:
    if isinstance(value, (str, bytes, bytearray)):
        raise AdmissionBridgeError("source_ids must be an ordered collection")
    try:
        items = tuple(value)
    except TypeError:
        raise AdmissionBridgeError(
            "source_ids must be an ordered collection"
        ) from None
    if not items:
        raise AdmissionBridgeError("source_ids must not be empty")
    normalized = tuple(_safe_id(item, "source_id") for item in items)
    if len(normalized) != len(set(normalized)):
        raise AdmissionBridgeError("source_ids must be unique")
    return tuple(sorted(normalized))


def _source_candidates(value: Any) -> tuple[SourceCandidate, ...]:
    if isinstance(value, (str, bytes, bytearray)):
        raise AdmissionBridgeError("candidates must be an ordered collection")
    try:
        candidates = tuple(value)
    except TypeError:
        raise AdmissionBridgeError(
            "candidates must be an ordered collection"
        ) from None
    if not candidates or not all(
        isinstance(candidate, SourceCandidate) for candidate in candidates
    ):
        raise AdmissionBridgeError("candidates must contain source contracts")
    _source_ids(tuple(candidate.source_id for candidate in candidates))
    snapshots = tuple(
        SourceCandidate(
            source_id=candidate.source_id,
            url=candidate.url,
            publisher=candidate.publisher,
            tier=candidate.tier,
            published_at=candidate.published_at,
            retrieved_at=candidate.retrieved_at,
            content_hash=candidate.content_hash,
            citation_root=candidate.citation_root,
            summary=candidate.summary,
        )
        for candidate in candidates
    )
    return tuple(sorted(snapshots, key=lambda item: item.source_id))


def _table_snapshot(
    table: ExtractedTable, adapter_row: ExtractedRow
) -> tuple[ExtractedTable, ExtractedRow]:
    row_index = next(index for index, item in enumerate(table.rows) if item is adapter_row)
    rows = tuple(
        ExtractedRow(
            values=row.values,
            cell_status=row.cell_status,
            location=row.location,
            confidence=row.confidence,
            warnings=row.warnings,
        )
        for row in table.rows
    )
    snapshot = ExtractedTable(
        table_id=table.table_id,
        caption=table.caption,
        sheet=table.sheet,
        rows=rows,
        coverage=ExtractedCoverage(**table.coverage.to_dict()),
        warnings=table.warnings,
        extraction_method=table.extraction_method,
    )
    return snapshot, snapshot.rows[row_index]


def _fact_value(
    row: dict[str, str | int],
    coverage: ExtractedCoverage,
    coverage_status: EvidenceStatus,
    row_hash: str,
) -> dict[str, Any]:
    return {
        # This complete canonical projection is the sole replay source of
        # truth.  The compatibility fields below are checked against it by
        # research_snapshot before they can reach calculation.
        "dataset_row": dict(row),
        "year": row["year"],
        "province": row["province"],
        "subject_group": row["subject_group"],
        "school_code": row["school_code"],
        "program_group": row["program_group"],
        "remarks": row["remarks"],
        "min_score": row["min_score"],
        "min_rank": row["min_rank"],
        "coverage_min_rank": coverage.lower_rank,
        "coverage_max_rank": coverage.upper_rank,
        "coverage_status": coverage_status.value,
        "row_hash": row_hash,
    }


@dataclass(frozen=True, init=False)
class AdmissionEvidenceBridge:
    """Immutable composition result ready for EvidenceStore persistence."""

    task: QueryTask
    table: ExtractedTable
    adapter_row: ExtractedRow
    dataset_row: ValidatedAdmissionRow
    candidates: tuple[SourceCandidate, ...]
    extraction_coverage: ExtractedCoverage
    evidence_status: EvidenceStatus
    coverage_status: EvidenceStatus
    admission_row_hash: str
    fact_id: str
    source_ids: tuple[str, ...]
    evidence_method: str
    extraction_method: str
    locator: str
    origin_digest: str
    bridge_digest: str
    _origin_json: str

    def __init__(self) -> None:
        raise TypeError("AdmissionEvidenceBridge is factory-only")

    @classmethod
    def _create(
        cls,
        *,
        task: QueryTask,
        table: ExtractedTable,
        adapter_row: ExtractedRow,
        dataset_row: ValidatedAdmissionRow,
        candidates: tuple[SourceCandidate, ...],
        extraction_coverage: ExtractedCoverage,
        evidence_status: EvidenceStatus,
        coverage_status: EvidenceStatus,
        row_hash: str,
        fact_id: str,
        source_ids: tuple[str, ...],
        evidence_method: str,
        extraction_method: str,
        locator: str,
        origin_digest: str,
        bridge_digest: str,
        origin_json: str,
    ) -> "AdmissionEvidenceBridge":
        instance = object.__new__(cls)
        object.__setattr__(instance, "task", task)
        object.__setattr__(instance, "table", table)
        object.__setattr__(instance, "adapter_row", adapter_row)
        object.__setattr__(instance, "dataset_row", dataset_row)
        object.__setattr__(instance, "candidates", candidates)
        object.__setattr__(instance, "extraction_coverage", extraction_coverage)
        object.__setattr__(instance, "evidence_status", evidence_status)
        object.__setattr__(instance, "coverage_status", coverage_status)
        object.__setattr__(instance, "admission_row_hash", row_hash)
        object.__setattr__(instance, "fact_id", fact_id)
        object.__setattr__(instance, "source_ids", source_ids)
        object.__setattr__(instance, "evidence_method", evidence_method)
        object.__setattr__(instance, "extraction_method", extraction_method)
        object.__setattr__(instance, "locator", locator)
        object.__setattr__(instance, "origin_digest", origin_digest)
        object.__setattr__(instance, "bridge_digest", bridge_digest)
        object.__setattr__(instance, "_origin_json", origin_json)
        return instance

    @property
    def fact(self) -> EvidenceFact:
        row = self.dataset_row.to_dict()
        value = _fact_value(
            row,
            self.extraction_coverage,
            self.coverage_status,
            self.admission_row_hash,
        )
        return EvidenceFact(
            fact_id=self.fact_id,
            field=f"admission_record:{self.fact_id}",
            value=value,
            unit=None,
            status=self.evidence_status,
            source_ids=self.source_ids,
            method=self.evidence_method,
            notes=f"query_task:{self.task.task_id}",
        )

    def persist(self, store: EvidenceStore) -> None:
        """Persist through EvidenceStore's authenticated provenance boundary."""

        if not isinstance(store, EvidenceStore):
            raise TypeError("store must be an EvidenceStore")
        store.add_fact(
            self.fact,
            year=self.task.year,
            extraction_method=self.extraction_method,
            locator=self.locator,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task.task_id,
            "task": self.task.to_dict(),
            "table": self.table.to_dict(),
            "adapter_row": self.adapter_row.to_dict(),
            "dataset_row": self.dataset_row.to_dict(),
            "sources": [item.to_dict() for item in self.candidates],
            "extraction_coverage": self.extraction_coverage.to_dict(),
            "evidence_status": self.evidence_status.value,
            "coverage_status": self.coverage_status.value,
            "admission_row_hash": self.admission_row_hash,
            "fact": self.fact.to_dict(),
            "evidence_method": self.evidence_method,
            "extraction_method": self.extraction_method,
            "locator": self.locator,
            "origin_digest": self.origin_digest,
            "bridge_digest": self.bridge_digest,
        }


def bridge_admission_evidence(
    *,
    table: ExtractedTable,
    adapter_row: ExtractedRow,
    task: QueryTask,
    dataset_row: ValidatedAdmissionRow,
    fact_id: str,
    candidates: tuple[SourceCandidate, ...],
    coverage_status: EvidenceStatus,
) -> AdmissionEvidenceBridge:
    """Validate and compose one adapter row with its admission context."""

    if not isinstance(table, ExtractedTable) or not isinstance(
        adapter_row, ExtractedRow
    ):
        raise TypeError("table and adapter_row must be adapter contracts")
    canonical_task = _canonical_task_snapshot(task)
    if not isinstance(dataset_row, ValidatedAdmissionRow):
        raise TypeError("dataset_row must be a ValidatedAdmissionRow")
    if sum(item is adapter_row for item in table.rows) != 1:
        raise AdmissionBridgeError("adapter row is detached from its table")
    if (
        canonical_task.kind != "batch_admission"
        or canonical_task.target_name != "普通批"
    ):
        raise AdmissionBridgeError("query task is not ordinary-batch admission")
    if table.extraction_method not in _ADMISSION_METHODS:
        raise AdmissionBridgeError("adapter extraction method is unsupported")
    if (
        not isinstance(coverage_status, EvidenceStatus)
        or coverage_status not in _COVERAGE_STATUSES
    ):
        raise AdmissionBridgeError("coverage status is not report-consumable")

    row = dataset_row.to_dict()
    try:
        for item in row.values():
            if isinstance(item, str) and item:
                validate_public_locator(item)
    except PublicLocatorError:
        raise AdmissionBridgeError(
            "validated admission row contains non-public text"
        ) from None
    required_dataset_fields = _CONTEXT_FIELDS | _OBSERVED_FIELDS | {"remarks"}
    if not required_dataset_fields.issubset(row):
        raise AdmissionBridgeError("validated admission row lacks required fields")
    if (
        canonical_task.year != row["year"]
        or canonical_task.province != row["province"]
        or canonical_task.subject_group != row["subject_group"]
    ):
        raise AdmissionBridgeError("query task and admission row context disagree")

    observed = set(adapter_row.values)
    required_observed = set(_OBSERVED_FIELDS) | (
        set(row) & _OPTIONAL_DECISION_FIELDS
    )
    if row["remarks"]:
        required_observed.add("remarks")
    if not required_observed.issubset(observed) or not observed.issubset(row):
        raise AdmissionBridgeError("adapter row fields do not bind the admission row")
    if any(
        status is not CellStatus.EXACT
        for status in adapter_row.cell_status.values()
    ):
        raise AdmissionBridgeError("adapter row contains non-exact cells")
    if any(adapter_row.values[field] != row[field] for field in observed):
        raise AdmissionBridgeError("adapter row and validated admission row disagree")

    coverage = table.coverage
    bounds = (
        coverage.lower_score,
        coverage.upper_score,
        coverage.lower_rank,
        coverage.upper_rank,
    )
    if any(not isinstance(value, int) or isinstance(value, bool) for value in bounds):
        raise AdmissionBridgeError("adapter coverage lacks exact numeric bounds")
    if not coverage.lower_score <= row["min_score"] <= coverage.upper_score:
        raise AdmissionBridgeError("adapter score lies outside extraction coverage")
    if not coverage.lower_rank <= row["min_rank"] <= coverage.upper_rank:
        raise AdmissionBridgeError("adapter rank lies outside extraction coverage")

    normalized_fact_id = _safe_id(fact_id, "fact_id")
    normalized_candidates = _source_candidates(candidates)
    locator = validate_public_locator(adapter_row.location)
    dataset_snapshot = ValidatedAdmissionRow.from_mapping(row)
    table_snapshot, adapter_snapshot = _table_snapshot(table, adapter_row)
    row_hash = admission_row_hash(dataset_snapshot)
    field = f"admission_record:{normalized_fact_id}"
    value = _fact_value(row, coverage, coverage_status, row_hash)
    evaluated = evaluate_claims(
        field,
        tuple(
            FactClaim(
                field=field,
                value=value,
                unit=None,
                source_id=candidate.source_id,
                method="adapter-dataset-bridge-v1",
            )
            for candidate in normalized_candidates
        ),
        normalized_candidates,
    )
    if evaluated.status not in _EVIDENCE_STATUSES or evaluated.value != value:
        raise AdmissionBridgeError(
            "candidate policy does not support an exact admission fact"
        )
    origin_payload = {
        "schema_version": "1.0",
        "task": canonical_task.to_dict(),
        "source_policy": {
            "id": canonical_task.source_policy_id,
            "version": canonical_task.source_policy_version,
        },
        "table": table_snapshot.to_dict(),
        "adapter_row": adapter_snapshot.to_dict(),
        "dataset_row": dataset_snapshot.to_dict(),
        "sources": [item.to_dict() for item in normalized_candidates],
        "extraction_coverage": table_snapshot.coverage.to_dict(),
        "coverage_status": coverage_status.value,
        "fact_id": normalized_fact_id,
    }
    origin_json = _canonical_json(origin_payload)
    origin_digest = _canonical_digest(origin_payload)
    bridge_digest = _bridge_identity_digest(
        origin_digest=origin_digest,
        admission_row_hash=row_hash,
        fact_id=normalized_fact_id,
        evidence_status=evaluated.status,
        source_ids=evaluated.source_ids,
        evidence_method=evaluated.method,
        extraction_method=table_snapshot.extraction_method,
        locator=locator,
    )
    return AdmissionEvidenceBridge._create(
        task=task,
        table=table_snapshot,
        adapter_row=adapter_snapshot,
        dataset_row=dataset_snapshot,
        candidates=normalized_candidates,
        extraction_coverage=table_snapshot.coverage,
        evidence_status=evaluated.status,
        coverage_status=coverage_status,
        row_hash=row_hash,
        fact_id=normalized_fact_id,
        source_ids=evaluated.source_ids,
        evidence_method=evaluated.method,
        extraction_method=table.extraction_method,
        locator=locator,
        origin_digest=origin_digest,
        bridge_digest=bridge_digest,
        origin_json=origin_json,
    )


def validate_admission_evidence_bridge(
    bridge: AdmissionEvidenceBridge,
) -> AdmissionEvidenceBridge:
    """Replay the admission factory and reject coordinated bridge mutation."""

    if type(bridge) is not AdmissionEvidenceBridge:
        raise TypeError("bridge must be an AdmissionEvidenceBridge")
    try:
        origin = json.loads(bridge._origin_json)
    except (AttributeError, TypeError, ValueError, json.JSONDecodeError):
        raise AdmissionBridgeError("admission bridge factory origin is invalid") from None
    expected_origin_fields = {
        "schema_version",
        "task",
        "source_policy",
        "table",
        "adapter_row",
        "dataset_row",
        "sources",
        "extraction_coverage",
        "coverage_status",
        "fact_id",
    }
    if (
        not isinstance(origin, dict)
        or set(origin) != expected_origin_fields
        or origin.get("schema_version") != "1.0"
        or _canonical_json(origin) != bridge._origin_json
        or _canonical_digest(origin) != bridge.origin_digest
    ):
        raise AdmissionBridgeError("admission bridge factory origin is invalid")
    raw_task = origin.get("task")
    if not isinstance(raw_task, dict):
        raise AdmissionBridgeError("admission bridge task origin is invalid")
    try:
        origin_task = QueryTask(**raw_task)
    except (KeyError, TypeError, ValueError):
        raise AdmissionBridgeError("admission bridge task origin is invalid") from None
    if origin_task.to_dict() != raw_task:
        raise AdmissionBridgeError("admission bridge task origin is invalid")
    try:
        visible_origin = {
            "schema_version": "1.0",
            "task": bridge.task.to_dict(),
            "source_policy": {
                "id": bridge.task.source_policy_id,
                "version": bridge.task.source_policy_version,
            },
            "table": bridge.table.to_dict(),
            "adapter_row": bridge.adapter_row.to_dict(),
            "dataset_row": bridge.dataset_row.to_dict(),
            "sources": [item.to_dict() for item in bridge.candidates],
            "extraction_coverage": bridge.extraction_coverage.to_dict(),
            "coverage_status": bridge.coverage_status.value,
            "fact_id": bridge.fact_id,
        }
    except (AttributeError, TypeError, ValueError):
        raise AdmissionBridgeError("admission bridge visible origin is invalid") from None
    if _canonical_json(visible_origin) != bridge._origin_json:
        raise AdmissionBridgeError(
            "admission bridge no longer matches its factory-owned origin"
        )
    expected_bridge_digest = _bridge_identity_digest(
        origin_digest=bridge.origin_digest,
        admission_row_hash=bridge.admission_row_hash,
        fact_id=bridge.fact_id,
        evidence_status=bridge.evidence_status,
        source_ids=bridge.source_ids,
        evidence_method=bridge.evidence_method,
        extraction_method=bridge.extraction_method,
        locator=bridge.locator,
    )
    if bridge.bridge_digest != expected_bridge_digest:
        raise AdmissionBridgeError("admission bridge identity digest disagrees")
    rebuilt = bridge_admission_evidence(
        table=bridge.table,
        adapter_row=bridge.adapter_row,
        task=bridge.task,
        dataset_row=bridge.dataset_row,
        fact_id=bridge.fact_id,
        candidates=bridge.candidates,
        coverage_status=bridge.coverage_status,
    )
    if rebuilt.to_dict() != bridge.to_dict():
        raise AdmissionBridgeError(
            "admission bridge no longer matches its authenticated inputs"
        )
    return bridge


__all__ = [
    "AdmissionBridgeError",
    "AdmissionEvidenceBridge",
    "bridge_admission_evidence",
    "validate_admission_evidence_bridge",
]
