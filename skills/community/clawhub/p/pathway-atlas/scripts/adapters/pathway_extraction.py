"""Authenticate pathway-policy fields extracted by public-source adapters.

This module is the single seam between host-selected HTML/XLSX/PDF/OCR
material and pathway evidence.  Callers select already-extracted fields; this
factory derives trust, coverage, source IDs, policy identity, and all digests.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any

if __package__ == "scripts.adapters":
    from . import (
        CellStatus,
        ExtractedRow,
        ExtractedTable,
        validate_public_locator,
    )
    from .ocr_rows import OcrExtractedRow
    from .pdf_text import PdfTextDocument
    from .public_text import (
        PublicTextAdapterError,
        PublicTextDocument,
        public_text_projection,
        validate_public_text_projection,
    )
    from ..contracts import EvidenceStatus, FactClaim, SourceCandidate, SourceTier
    from ..path_recommend import validate_public_output_text
    from ..planning_profile import PlanningProfile
    from ..query_plan import QueryPlan, QueryTask, validate_query_plan_payload
    from ..source_policy import (
        canonical_site_identity,
        canonicalize_provenance_url,
        evaluate_claims,
    )
else:  # ``sys.path`` rooted at ``scripts`` package compatibility.
    from adapters import (  # type: ignore
        CellStatus,
        ExtractedRow,
        ExtractedTable,
        validate_public_locator,
    )
    from adapters.ocr_rows import OcrExtractedRow  # type: ignore
    from adapters.pdf_text import PdfTextDocument  # type: ignore
    from adapters.public_text import (  # type: ignore
        PublicTextAdapterError,
        PublicTextDocument,
        public_text_projection,
        validate_public_text_projection,
    )
    from contracts import EvidenceStatus, FactClaim, SourceCandidate, SourceTier  # type: ignore
    from path_recommend import validate_public_output_text  # type: ignore
    from planning_profile import PlanningProfile  # type: ignore
    from query_plan import QueryPlan, QueryTask, validate_query_plan_payload  # type: ignore
    from source_policy import (  # type: ignore
        canonical_site_identity,
        canonicalize_provenance_url,
        evaluate_claims,
    )


_HASH = re.compile(r"sha256:[0-9a-f]{64}\Z")
_ACCEPTED = frozenset(
    {
        EvidenceStatus.OFFICIAL,
        EvidenceStatus.CORROBORATED,
        EvidenceStatus.REFERENCE,
    }
)
_COLLECTION_FIELDS = frozenset(
    {
        "eligibility_requirements",
        "grade_requirements",
        "subject_requirements",
        "award_requirements",
        "activity_requirements",
        "disqualifying_facts",
        "professional_options",
        "dates_and_deadlines",
        "application_materials",
        "preparation_actions",
    }
)
_FIELDS = (
    "institution",
    "province",
    "subject_mode",
    "year",
    "eligibility_requirements",
    "grade_requirements",
    "subject_requirements",
    "award_requirements",
    "activity_requirements",
    "disqualifying_facts",
    "professional_options",
    "training_arrangements",
    "transition_rules",
    "outcomes",
    "service_employment_obligations",
    "penalty_exit_rules",
    "fees_and_subsidies",
    "dates_and_deadlines",
    "application_materials",
    "preparation_actions",
)
_TARGETS = {
    "强基计划": ("strong_foundation", "strong_foundation"),
    "综合评价": ("comprehensive_evaluation", "comprehensive_evaluation"),
    "国家专项": ("special_program", "national_special"),
    "地方专项": ("special_program", "local_special"),
    "高校专项": ("special_program", "university_special"),
    "公费师范": ("service_oriented", "public_funded_teacher"),
    "优师计划": ("service_oriented", "excellent_teacher"),
    "定向医学生": ("service_oriented", "directed_medical"),
    "军校": ("uniformed_service", "military"),
    "公安司法消防": ("uniformed_service", "police_judicial_fire"),
    "航海航空": ("uniformed_service", "maritime_aviation"),
    "港澳招生": ("cross_border", "hong_kong_macao"),
    "中外合作办学": ("cross_border", "sino_foreign"),
    "艺体类": ("arts_sports", "arts_sports"),
}
_PATHWAY_IDS = (
    "strong_foundation",
    "comprehensive_evaluation",
    "special_program",
    "service_oriented",
    "uniformed_service",
    "cross_border",
    "arts_sports",
)
_TABLE_METHODS = frozenset({"html-table", "xlsx-worksheet", "xls-worksheet", "pdf-text-table", "host-ocr-rows"})
_PDF_METHODS = frozenset({"pdfplumber-text", "pypdf-text"})


class PathwayExtractionError(ValueError):
    """Adapter material cannot form one authenticated pathway projection."""


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def _digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _hash_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _profile_pathway_trace(profile: PlanningProfile) -> tuple[dict[str, str], ...]:
    records: list[dict[str, str]] = []
    for pathway_id in _PATHWAY_IDS:
        preference = profile.pathway_preferences[pathway_id]
        if (
            pathway_id in {"service_oriented", "uniformed_service"}
            and profile.constraints.service_commitment == "reject"
        ):
            decision, reason = "exclude", "service_commitment_rejected"
        elif preference == "interested":
            decision, reason = "include", "profile_interested"
        elif preference == "unknown":
            decision, reason = "discover", "preference_unknown_requires_discovery"
        elif preference == "not_interested":
            decision, reason = "exclude", "profile_not_interested"
        else:
            decision, reason = "exclude", "profile_not_applicable"
        records.append(
            {
                "pathway_id": pathway_id,
                "preference": preference,
                "decision": decision,
                "reason_code": reason,
            }
        )
    return tuple(records)


def _safe_text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise PathwayExtractionError(f"{name} must be nonempty exact public text")
    try:
        validate_public_output_text(value)
    except (TypeError, ValueError):
        raise PathwayExtractionError(f"{name} contains non-public text") from None
    return value


def _normalize_value(field: str, value: Any) -> Any:
    if value is None:
        return None
    if field == "year":
        if isinstance(value, bool):
            raise PathwayExtractionError("year must be an exact integer")
        if isinstance(value, str) and value.isascii() and value.isdigit():
            value = int(value)
        if not isinstance(value, int) or not 2000 <= value <= 2100:
            raise PathwayExtractionError("year must be an exact supported integer")
        return value
    if field in _COLLECTION_FIELDS:
        if isinstance(value, str):
            values = (value,)
        elif isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
            values = tuple(value)
        else:
            raise PathwayExtractionError(f"{field} must be public text or ordered text")
        normalized = tuple(_safe_text(item, field) for item in values)
        if len(normalized) != len(set(normalized)):
            raise PathwayExtractionError(f"{field} must contain unique public text")
        return list(normalized)
    return _safe_text(value, field)


def _candidate_projection(candidate: SourceCandidate) -> dict[str, str]:
    document_url = canonicalize_provenance_url(candidate.url)
    site = canonical_site_identity(candidate.url)
    citation_root = canonicalize_provenance_url(candidate.citation_root)
    publisher = (
        " ".join(candidate.publisher.casefold().split())
        if isinstance(candidate.publisher, str)
        else ""
    )
    if not document_url or not site or not citation_root or not publisher:
        raise PathwayExtractionError("candidate lacks a public source identity")
    try:
        validate_public_locator(candidate.source_id)
    except (TypeError, ValueError):
        raise PathwayExtractionError("candidate source ID is unsafe") from None
    if not isinstance(candidate.content_hash, str) or _HASH.fullmatch(candidate.content_hash) is None:
        raise PathwayExtractionError("candidate content hash is invalid")
    if type(candidate.tier) is not SourceTier:
        raise PathwayExtractionError("candidate source tier is invalid")
    return {
        "source_id": candidate.source_id,
        "tier": candidate.tier.value,
        "publisher_hash": _digest(publisher),
        "site_hash": _digest(site),
        "document_hash": _digest(document_url),
        "citation_root_hash": _digest(citation_root),
        "content_hash": candidate.content_hash,
    }


def _synthetic_document_url(value: Any) -> str:
    if not isinstance(value, Mapping):
        raise PathwayExtractionError("source projection is incomplete")
    site_hash = value.get("site_hash")
    document_hash = value.get("document_hash")
    if (
        not isinstance(site_hash, str)
        or _HASH.fullmatch(site_hash) is None
        or not isinstance(document_hash, str)
        or _HASH.fullmatch(document_hash) is None
    ):
        raise PathwayExtractionError("source projection hash is invalid")
    return (
        f"https://site-{site_hash[7:23]}.example.cn/"
        f"document/{document_hash[7:23]}"
    )


def _candidate_from_projection(
    value: Any,
    document_urls: Mapping[str, str],
) -> SourceCandidate:
    expected = {
        "source_id",
        "tier",
        "publisher_hash",
        "site_hash",
        "document_hash",
        "citation_root_hash",
        "content_hash",
    }
    if not isinstance(value, Mapping) or set(value) != expected:
        raise PathwayExtractionError("source projection is incomplete")
    for name in (
        "publisher_hash",
        "site_hash",
        "document_hash",
        "citation_root_hash",
        "content_hash",
    ):
        if not isinstance(value[name], str) or _HASH.fullmatch(value[name]) is None:
            raise PathwayExtractionError("source projection hash is invalid")
    try:
        source_id = validate_public_locator(value["source_id"])
    except (TypeError, ValueError):
        raise PathwayExtractionError("source projection source ID is invalid") from None
    try:
        tier = SourceTier(value["tier"])
    except (TypeError, ValueError):
        raise PathwayExtractionError("source projection tier is invalid") from None
    root_key = value["citation_root_hash"][7:23]
    publisher_key = value["publisher_hash"][7:23]
    return SourceCandidate(
        source_id=source_id,
        url=_synthetic_document_url(value),
        publisher=f"publisher-{publisher_key}",
        tier=tier,
        published_at=None,
        retrieved_at="2000-01-01T00:00:00Z",
        content_hash=value["content_hash"],
        citation_root=document_urls.get(
            value["citation_root_hash"],
            f"https://root-{root_key}.example.cn/",
        ),
        summary="authenticated-pathway-source",
    )


def _snapshot_candidates(values: Iterable[SourceCandidate]) -> tuple[SourceCandidate, ...]:
    if isinstance(values, (str, bytes, bytearray)):
        raise TypeError("candidates must contain SourceCandidate records")
    candidates = tuple(values)
    if not candidates or any(type(item) is not SourceCandidate for item in candidates):
        raise TypeError("candidates must contain SourceCandidate records")
    if len({item.source_id for item in candidates}) != len(candidates):
        raise PathwayExtractionError("candidate source IDs must be unique")
    snapshots = tuple(
        SourceCandidate(
            source_id=item.source_id,
            url=item.url,
            publisher=item.publisher,
            tier=item.tier,
            published_at=item.published_at,
            retrieved_at=item.retrieved_at,
            content_hash=item.content_hash,
            citation_root=item.citation_root,
            summary=item.summary,
        )
        for item in candidates
    )
    return tuple(sorted(snapshots, key=lambda item: item.source_id))


def _table_document(table: ExtractedTable, field_map: Any) -> dict[str, Any]:
    if table.extraction_method not in _TABLE_METHODS:
        raise PathwayExtractionError("table extraction method is unsupported")
    if len(table.rows) != 1:
        raise PathwayExtractionError("pathway table must select exactly one policy row")
    if not isinstance(field_map, Mapping) or set(field_map) != set(_FIELDS):
        raise PathwayExtractionError("pathway field map is incomplete")
    mapped = tuple(field_map[field] for field in _FIELDS)
    if any(not isinstance(item, str) for item in mapped) or len(set(mapped)) != len(mapped):
        raise PathwayExtractionError("table field map must use unique source fields")
    row = table.rows[0]
    fields: dict[str, Any] = {}
    for canonical in _FIELDS:
        source_field = field_map[canonical]
        if source_field not in row.values:
            raise PathwayExtractionError("mapped pathway source field is absent")
        status = row.cell_status[source_field]
        value = None
        warning = None
        if status is CellStatus.EXACT:
            try:
                value = _normalize_value(canonical, row.values[source_field])
            except PathwayExtractionError:
                if row.values[source_field] is not None:
                    raise
            if value is None:
                warning = f"{canonical}:missing"
        else:
            warning = f"{canonical}:{status.value}"
        locator = (
            row.cell_locations[source_field]
            if isinstance(row, OcrExtractedRow)
            else row.location
        )
        fields[canonical] = {
            "value": value,
            "cell_status": status.value,
            "locator": validate_public_locator(locator),
            "warning": warning,
        }
    body = {
        "adapter_kind": "ocr" if isinstance(row, OcrExtractedRow) else "table",
        "extraction_method": table.extraction_method,
        "fields": fields,
    }
    body["extraction_digest"] = _digest(body)
    return body


def _pdf_document(document: PdfTextDocument, field_map: Any) -> dict[str, Any]:
    if not isinstance(field_map, Mapping) or not set(field_map) <= set(_FIELDS):
        raise PathwayExtractionError("pathway PDF field map contains unknown fields")
    methods = {page.extraction_method for page in document.pages if page.text}
    if len(methods) != 1 or not methods <= _PDF_METHODS:
        raise PathwayExtractionError("PDF requires readable text from one supported parser")
    method = next(iter(methods))
    fields: dict[str, Any] = {}
    for canonical in _FIELDS:
        if canonical not in field_map:
            fields[canonical] = {
                "value": None,
                "cell_status": CellStatus.EMPTY.value,
                "locator": f"document/field[{canonical}]/missing",
                "warning": f"{canonical}:missing",
            }
            continue
        selection = field_map[canonical]
        if (
            not isinstance(selection, Sequence)
            or isinstance(selection, (str, bytes, bytearray))
            or len(selection) != 2
        ):
            raise PathwayExtractionError("PDF field selection must contain page and exact text")
        page_number, exact_text = selection
        if isinstance(page_number, bool) or not isinstance(page_number, int):
            raise PathwayExtractionError("PDF page selection must be an integer")
        if not isinstance(exact_text, str) or not exact_text:
            raise PathwayExtractionError("PDF field selection must contain exact text")
        page = next((item for item in document.pages if item.page_number == page_number), None)
        if page is None:
            raise PathwayExtractionError("PDF field selection references a missing page")
        occurrences = page.text.count(exact_text)
        status = CellStatus.EXACT if occurrences == 1 else CellStatus.UNCERTAIN
        value = _normalize_value(canonical, exact_text) if status is CellStatus.EXACT else None
        locator = f"page[{page_number}]/text[{_hash_text(exact_text)[:16]}]"
        fields[canonical] = {
            "value": value,
            "cell_status": status.value,
            "locator": validate_public_locator(locator),
            "warning": None if status is CellStatus.EXACT else f"{canonical}:ambiguous",
        }
    warnings = tuple(
        dict.fromkeys(
            (
                *document.warnings,
                *(warning for page in document.pages for warning in page.warnings),
            )
        )
    )
    body = {
        "adapter_kind": "pdf",
        "extraction_method": method,
        "document_id": document.document_id,
        "page_count": document.page_count,
        "coverage_status": "complete" if not warnings else "partial",
        "warnings": list(warnings),
        "fields": fields,
    }
    body["extraction_digest"] = _digest(body)
    return body


def _public_text_document(
    document: PublicTextDocument,
    field_map: Any,
) -> dict[str, Any]:
    try:
        return public_text_projection(
            document,
            required_fields=_FIELDS,
            field_map=field_map,
        )
    except (PublicTextAdapterError, TypeError, ValueError):
        raise PathwayExtractionError("public text pathway fields are invalid") from None


def _documents(extraction: Any, field_map: Any) -> tuple[dict[str, Any], ...]:
    if isinstance(extraction, (ExtractedTable, PdfTextDocument, PublicTextDocument)):
        extractions = (extraction,)
        maps = (field_map,)
    else:
        if isinstance(extraction, (str, bytes, bytearray)):
            raise TypeError("extraction must contain adapter outputs")
        try:
            extractions = tuple(extraction)
        except TypeError:
            raise TypeError("extraction must contain adapter outputs") from None
        if isinstance(field_map, Mapping):
            maps = (field_map,)
        else:
            try:
                maps = tuple(field_map)
            except TypeError:
                raise TypeError("field_map must match adapter outputs") from None
    if not extractions or len(extractions) != len(maps):
        raise PathwayExtractionError("field maps must match adapter outputs")
    documents: list[dict[str, Any]] = []
    for item, mapping in zip(extractions, maps):
        if isinstance(item, ExtractedTable):
            documents.append(_table_document(item, mapping))
        elif isinstance(item, PdfTextDocument):
            documents.append(_pdf_document(item, mapping))
        elif isinstance(item, PublicTextDocument):
            documents.append(_public_text_document(item, mapping))
        else:
            raise TypeError("extraction must contain typed adapter outputs")
    return tuple(documents)


@dataclass(frozen=True, init=False)
class FieldProvenance:
    field: str
    status: EvidenceStatus
    source_ids: tuple[str, ...]
    locators: tuple[str, ...]
    extraction_methods: tuple[str, ...]
    evidence_method: str
    warnings: tuple[str, ...]

    def __init__(self) -> None:
        raise TypeError("FieldProvenance is factory-only")

    @classmethod
    def _create(cls, **values: Any) -> "FieldProvenance":
        instance = object.__new__(cls)
        for name, value in values.items():
            object.__setattr__(instance, name, value)
        return instance

    def to_dict(self) -> dict[str, Any]:
        return {
            "field": self.field,
            "status": self.status.value,
            "source_ids": list(self.source_ids),
            "locators": list(self.locators),
            "extraction_methods": list(self.extraction_methods),
            "evidence_method": self.evidence_method,
            "warnings": list(self.warnings),
        }


@dataclass(frozen=True, init=False)
class PathwayPolicyProjection:
    policy_id: str
    pathway_family: str
    pathway_type: str
    title: str
    institution: str | None
    province: str
    subject_mode: str
    target_year: int
    data_year: int
    eligibility_requirements: tuple[str, ...] | None
    grade_requirements: tuple[str, ...] | None
    subject_requirements: tuple[str, ...] | None
    award_requirements: tuple[str, ...] | None
    activity_requirements: tuple[str, ...] | None
    disqualifying_facts: tuple[str, ...] | None
    professional_options: tuple[str, ...] | None
    training_arrangements: str | None
    transition_rules: str | None
    outcomes: str | None
    service_employment_obligations: str | None
    penalty_exit_rules: str | None
    fees_and_subsidies: str | None
    timeline: tuple[str, ...] | None
    application_materials: tuple[str, ...] | None
    preparation_actions: tuple[str, ...] | None
    evidence_status: EvidenceStatus
    source_ids: tuple[str, ...]
    evidence_method: str
    evidence_methods: tuple[str, ...]
    coverage_status: str
    warnings: tuple[str, ...]
    field_provenance: tuple[FieldProvenance, ...]
    profile_digest: str
    query_plan_digest: str
    query_task_id: str
    query_task_digest: str
    extraction_digest: str
    provenance_digest: str
    input_digest: str
    digest: str
    _input_projection_json: str

    def __init__(self) -> None:
        raise TypeError("PathwayPolicyProjection is factory-only")

    @classmethod
    def _create(cls, **values: Any) -> "PathwayPolicyProjection":
        instance = object.__new__(cls)
        for name, value in values.items():
            object.__setattr__(instance, name, value)
        return instance

    @property
    def input_projection(self) -> dict[str, Any]:
        value = json.loads(self._input_projection_json)
        if not isinstance(value, dict):  # pragma: no cover - factory invariant
            raise PathwayExtractionError("pathway input projection is invalid")
        return value

    def to_dict(self) -> dict[str, Any]:
        def items(value: tuple[str, ...] | None) -> list[str] | None:
            return None if value is None else list(value)

        return {
            "policy_id": self.policy_id,
            "pathway_family": self.pathway_family,
            "pathway_type": self.pathway_type,
            "title": self.title,
            "institution": self.institution,
            "province": self.province,
            "subject_mode": self.subject_mode,
            "target_year": self.target_year,
            "data_year": self.data_year,
            "eligibility_requirements": items(self.eligibility_requirements),
            "grade_requirements": items(self.grade_requirements),
            "subject_requirements": items(self.subject_requirements),
            "award_requirements": items(self.award_requirements),
            "activity_requirements": items(self.activity_requirements),
            "disqualifying_facts": items(self.disqualifying_facts),
            "professional_options": items(self.professional_options),
            "training_arrangements": self.training_arrangements,
            "transition_rules": self.transition_rules,
            "outcomes": self.outcomes,
            "service_employment_obligations": self.service_employment_obligations,
            "penalty_exit_rules": self.penalty_exit_rules,
            "fees_and_subsidies": self.fees_and_subsidies,
            "timeline": items(self.timeline),
            "application_materials": items(self.application_materials),
            "preparation_actions": items(self.preparation_actions),
            "evidence_status": self.evidence_status.value,
            "source_ids": list(self.source_ids),
            "evidence_method": self.evidence_method,
            "evidence_methods": list(self.evidence_methods),
            "coverage_status": self.coverage_status,
            "warnings": list(self.warnings),
            "field_provenance": [item.to_dict() for item in self.field_provenance],
            "profile_digest": self.profile_digest,
            "query_plan_digest": self.query_plan_digest,
            "query_task_id": self.query_task_id,
            "query_task_digest": self.query_task_digest,
            "extraction_digest": self.extraction_digest,
            "provenance_digest": self.provenance_digest,
            "input_digest": self.input_digest,
            "input_projection": self.input_projection,
            "digest": self.digest,
        }


def _field_value(facts: Mapping[str, Any], field: str) -> Any:
    fact = facts[field]
    return fact.value if fact.status in _ACCEPTED else None


def _project_from_input(value: Any) -> PathwayPolicyProjection:
    expected = {
        "schema_version",
        "profile_digest",
        "query_plan_digest",
        "task",
        "pathway_family",
        "pathway_type",
        "sources",
        "documents",
    }
    if not isinstance(value, Mapping) or set(value) != expected or value["schema_version"] != "1.0":
        raise PathwayExtractionError("pathway input projection is incomplete")
    task = value["task"]
    task_fields = {
        "task_id",
        "task_digest",
        "kind",
        "target_name",
        "province",
        "subject_group",
        "subject_mode",
        "year",
        "target_year",
        "source_policy_id",
        "source_policy_version",
    }
    if not isinstance(task, Mapping) or set(task) != task_fields:
        raise PathwayExtractionError("pathway task projection is incomplete")
    if task["target_name"] not in _TARGETS:
        raise PathwayExtractionError("pathway task target is unsupported")
    family, pathway_type = _TARGETS[task["target_name"]]
    if value["pathway_family"] != family or value["pathway_type"] != pathway_type:
        raise PathwayExtractionError("pathway family projection disagrees with its task")
    if task["task_digest"] != _digest({key: task[key] for key in task if key != "task_digest"}):
        raise PathwayExtractionError("pathway task digest disagrees")
    if not isinstance(value["profile_digest"], str) or _HASH.fullmatch(value["profile_digest"]) is None:
        raise PathwayExtractionError("profile digest is invalid")
    if not isinstance(value["query_plan_digest"], str) or _HASH.fullmatch(value["query_plan_digest"]) is None:
        raise PathwayExtractionError("query plan digest is invalid")
    source_values = value["sources"]
    document_values = value["documents"]
    if (
        not isinstance(source_values, list)
        or not isinstance(document_values, list)
        or not source_values
        or len(source_values) != len(document_values)
    ):
        raise PathwayExtractionError("pathway sources and documents disagree")
    document_urls: dict[str, str] = {}
    for item in source_values:
        synthetic_url = _synthetic_document_url(item)
        document_hash = item["document_hash"]
        previous = document_urls.setdefault(document_hash, synthetic_url)
        if previous != synthetic_url:
            raise PathwayExtractionError("source document identity disagrees")
    candidates = tuple(
        _candidate_from_projection(item, document_urls) for item in source_values
    )
    source_ids = tuple(item.source_id for item in candidates)
    if len(source_ids) != len(set(source_ids)):
        raise PathwayExtractionError("pathway source IDs repeat")

    observations: dict[
        str, list[tuple[str, Any, str, str, str | None, CellStatus]]
    ] = {
        field: [] for field in _FIELDS
    }
    document_digests: list[str] = []
    document_warnings: list[str] = []
    document_coverage_complete = True
    for candidate, source_value, document in zip(
        candidates, source_values, document_values
    ):
        if not isinstance(document, Mapping):
            raise PathwayExtractionError("pathway document projection is invalid")
        adapter_kind = document.get("adapter_kind")
        if adapter_kind == "public-text":
            try:
                validate_public_text_projection(document, required_fields=_FIELDS)
            except (PublicTextAdapterError, TypeError, ValueError):
                raise PathwayExtractionError(
                    "public text pathway projection does not replay"
                ) from None
            if (
                document["source_id"] != candidate.source_id
                or _digest(document["url"]) != source_value["document_hash"]
            ):
                raise PathwayExtractionError(
                    "public text source provenance disagrees with its candidate"
                )
        document_body = dict(document)
        claimed_digest = document_body.pop("extraction_digest", None)
        if claimed_digest != _digest(document_body):
            raise PathwayExtractionError("pathway extraction digest disagrees")
        fields = document.get("fields")
        if not isinstance(fields, Mapping) or set(fields) != set(_FIELDS):
            raise PathwayExtractionError("pathway document field coverage is incomplete")
        method = document.get("extraction_method")
        if method not in _TABLE_METHODS | _PDF_METHODS | {"host-public-text"}:
            raise PathwayExtractionError("pathway extraction method is unsupported")
        if (
            (method in _PDF_METHODS) != (adapter_kind == "pdf")
            or adapter_kind not in {"pdf", "table", "ocr", "public-text"}
            or (adapter_kind == "ocr") != (method == "host-ocr-rows")
            or (adapter_kind == "public-text") != (method == "host-public-text")
        ):
            raise PathwayExtractionError("pathway adapter kind and method disagree")
        if adapter_kind == "pdf":
            pdf_warnings = document.get("warnings")
            pdf_coverage = document.get("coverage_status")
            if (
                not isinstance(pdf_warnings, list)
                or any(not isinstance(item, str) or not item for item in pdf_warnings)
                or pdf_coverage not in {"complete", "partial"}
                or (pdf_coverage == "complete") != (not pdf_warnings)
            ):
                raise PathwayExtractionError("pathway PDF coverage projection is invalid")
            document_warnings.extend(
                item for item in pdf_warnings if item not in document_warnings
            )
            document_coverage_complete = document_coverage_complete and (
                pdf_coverage == "complete"
            )
        document_digests.append(claimed_digest)
        for field in _FIELDS:
            item = fields[field]
            expected_field_keys = {"value", "cell_status", "locator", "warning"}
            if adapter_kind == "public-text":
                expected_field_keys.update({"quote", "start", "end"})
            if not isinstance(item, Mapping) or set(item) != expected_field_keys:
                raise PathwayExtractionError("pathway field projection is incomplete")
            try:
                cell_status = CellStatus(item["cell_status"])
                locator = validate_public_locator(item["locator"])
            except (TypeError, ValueError):
                raise PathwayExtractionError("pathway field provenance is invalid") from None
            normalized = item["value"]
            if cell_status is CellStatus.EXACT:
                normalized = _normalize_value(field, normalized)
            elif normalized is not None:
                raise PathwayExtractionError("non-exact pathway field carries a value")
            warning = item["warning"]
            if warning is not None and (not isinstance(warning, str) or not warning):
                raise PathwayExtractionError("pathway field warning is invalid")
            observations[field].append(
                (candidate.source_id, normalized, method, locator, warning, cell_status)
            )

    facts: dict[str, Any] = {}
    provenance: list[FieldProvenance] = []
    warnings: list[str] = []
    for field in _FIELDS:
        claims = tuple(
            FactClaim(
                field=f"pathway_projection:{field}",
                value=observed,
                unit=None,
                source_id=source_id,
                method="pathway-adapter-field-v1",
            )
            for (
                source_id,
                observed,
                _method,
                _locator,
                _warning,
                _cell_status,
            ) in observations[field]
            if observed is not None
        )
        evaluated = evaluate_claims(
            f"pathway_projection:{field}",
            claims,
            candidates,
        )
        facts[field] = evaluated
        cell_statuses = tuple(item[5] for item in observations[field])
        has_field_value = any(item[1] is not None for item in observations[field])
        if evaluated.status in _ACCEPTED or evaluated.status is EvidenceStatus.CONFLICT:
            field_status = evaluated.status
            field_evidence_method = evaluated.method
        elif has_field_value:
            field_status = EvidenceStatus.PARTIAL
            field_evidence_method = "pathway-field-partial-v1"
        elif CellStatus.MASKED in cell_statuses:
            field_status = EvidenceStatus.MASKED
            field_evidence_method = "pathway-field-masked-v1"
        elif any(item not in {CellStatus.EXACT, CellStatus.EMPTY} for item in cell_statuses):
            field_status = EvidenceStatus.PARTIAL
            field_evidence_method = "pathway-field-partial-v1"
        else:
            field_status = EvidenceStatus.MISSING
            field_evidence_method = "pathway-field-missing-v1"
        field_warnings = tuple(
            item[4] for item in observations[field] if item[4] is not None
        )
        warnings.extend(item for item in field_warnings if item not in warnings)
        provenance.append(
            FieldProvenance._create(
                field=field,
                status=field_status,
                source_ids=(
                    tuple(evaluated.source_ids)
                    if evaluated.source_ids
                    else tuple(sorted({item[0] for item in observations[field]}))
                ),
                locators=tuple(sorted({item[3] for item in observations[field]})),
                extraction_methods=tuple(sorted({item[2] for item in observations[field]})),
                evidence_method=field_evidence_method,
                warnings=field_warnings,
            )
        )

    warnings.extend(item for item in document_warnings if item not in warnings)

    for field, expected_value in (
        ("province", task["province"]),
        ("subject_mode", task["subject_mode"]),
        ("year", task["year"]),
    ):
        exact_observed = {
            item[1] for item in observations[field] if item[1] is not None
        }
        if exact_observed and exact_observed != {expected_value}:
            raise PathwayExtractionError("adapter pathway context disagrees with query task")

    has_observed_value = any(
        observed is not None
        for field_observations in observations.values()
        for (
            _source_id,
            observed,
            _method,
            _locator,
            _warning,
            _cell_status,
        ) in field_observations
    )
    complete = document_coverage_complete and all(
        item.status in _ACCEPTED and facts[item.field].value is not None
        for item in provenance
    )
    if complete:
        status = max(
            (item.status for item in provenance),
            key={
                EvidenceStatus.OFFICIAL: 0,
                EvidenceStatus.CORROBORATED: 1,
                EvidenceStatus.REFERENCE: 2,
            }.__getitem__,
        )
        weakest = next(item for item in provenance if item.status is status)
        evidence_method = weakest.evidence_method
        coverage_status = "complete"
    elif any(item.status is EvidenceStatus.CONFLICT for item in provenance):
        status = EvidenceStatus.CONFLICT
        evidence_method = "pathway-projection-conflict-v1"
        coverage_status = "conflict"
    elif not has_observed_value and all(
        item.status is EvidenceStatus.MASKED for item in provenance
    ):
        status = EvidenceStatus.MASKED
        evidence_method = "pathway-projection-masked-v1"
        coverage_status = "missing"
    elif not has_observed_value:
        status = EvidenceStatus.MISSING
        evidence_method = "pathway-projection-missing-v1"
        coverage_status = "missing"
    else:
        status = EvidenceStatus.PARTIAL
        evidence_method = "pathway-projection-partial-v1"
        coverage_status = "partial"

    if complete:
        weakest = next(item for item in provenance if item.status is status)
        result_source_ids = weakest.source_ids
    else:
        result_source_ids = tuple(sorted(source_ids))
    evidence_methods = tuple(sorted({item.evidence_method for item in provenance}))
    collection_values = {
        field: (
            None
            if _field_value(facts, field) is None
            else tuple(_field_value(facts, field))
        )
        for field in _COLLECTION_FIELDS
    }
    eligibility_parts = (
        "eligibility_requirements",
        "grade_requirements",
        "subject_requirements",
        "award_requirements",
        "activity_requirements",
    )
    eligibility = (
        None
        if any(collection_values[field] is None for field in eligibility_parts)
        else tuple(
            item
            for field in eligibility_parts
            for item in collection_values[field] or ()
        )
    )
    institution = _field_value(facts, "institution")
    policy_seed = {
        "task_id": task["task_id"],
        "institution": institution,
        "pathway_type": pathway_type,
    }
    policy_id = "pathway-" + _hash_text(_canonical_json(policy_seed))[:24]
    provenance_value = [item.to_dict() for item in provenance]
    input_value = json.loads(_canonical_json(value))
    input_digest = _digest(input_value)
    query_task_digest = task["task_digest"]
    extraction_digest = _digest(document_digests)
    provenance_digest = _digest(provenance_value)
    projection_values: dict[str, Any] = {
        "policy_id": policy_id,
        "pathway_family": family,
        "pathway_type": pathway_type,
        "title": task["target_name"],
        "institution": institution,
        "province": task["province"],
        "subject_mode": task["subject_mode"],
        "target_year": task["target_year"],
        "data_year": task["year"],
        "eligibility_requirements": eligibility,
        "grade_requirements": collection_values["grade_requirements"],
        "subject_requirements": collection_values["subject_requirements"],
        "award_requirements": collection_values["award_requirements"],
        "activity_requirements": collection_values["activity_requirements"],
        "disqualifying_facts": collection_values["disqualifying_facts"],
        "professional_options": collection_values["professional_options"],
        "training_arrangements": _field_value(facts, "training_arrangements"),
        "transition_rules": _field_value(facts, "transition_rules"),
        "outcomes": _field_value(facts, "outcomes"),
        "service_employment_obligations": _field_value(
            facts, "service_employment_obligations"
        ),
        "penalty_exit_rules": _field_value(facts, "penalty_exit_rules"),
        "fees_and_subsidies": _field_value(facts, "fees_and_subsidies"),
        "timeline": collection_values["dates_and_deadlines"],
        "application_materials": collection_values["application_materials"],
        "preparation_actions": collection_values["preparation_actions"],
        "evidence_status": status,
        "source_ids": result_source_ids,
        "evidence_method": evidence_method,
        "evidence_methods": evidence_methods,
        "coverage_status": coverage_status,
        "warnings": tuple(warnings),
        "field_provenance": tuple(provenance),
        "profile_digest": value["profile_digest"],
        "query_plan_digest": value["query_plan_digest"],
        "query_task_id": task["task_id"],
        "query_task_digest": query_task_digest,
        "extraction_digest": extraction_digest,
        "provenance_digest": provenance_digest,
        "input_digest": input_digest,
        "_input_projection_json": _canonical_json(input_value),
    }
    digest_payload = {
        key: (
            value_item.value
            if isinstance(value_item, EvidenceStatus)
            else [item.to_dict() for item in value_item]
            if key == "field_provenance"
            else list(value_item)
            if isinstance(value_item, tuple)
            else value_item
        )
        for key, value_item in projection_values.items()
        if key != "_input_projection_json"
    }
    digest_payload["input_projection"] = input_value
    projection_values["digest"] = _digest(digest_payload)
    return PathwayPolicyProjection._create(**projection_values)


def extract_pathway_policy(
    *,
    profile: PlanningProfile,
    plan: QueryPlan,
    task: QueryTask,
    extraction: Any,
    field_map: Any,
    candidates: Iterable[SourceCandidate],
) -> PathwayPolicyProjection:
    """Build one immutable policy projection from typed adapter output only."""

    if type(profile) is not PlanningProfile:
        raise TypeError("profile must be a strict PlanningProfile")
    if type(plan) is not QueryPlan:
        raise TypeError("plan must be a canonical QueryPlan")
    try:
        validated_plan = validate_query_plan_payload(plan.to_dict())
    except (KeyError, TypeError, ValueError):
        raise PathwayExtractionError("plan is not a canonical validated query plan") from None
    if validated_plan.to_dict() != plan.to_dict():
        raise PathwayExtractionError("plan is not a canonical validated query plan")
    if type(task) is not QueryTask:
        raise TypeError("task must be a QueryTask")
    if sum(item is task for item in plan.tasks) != 1:
        raise PathwayExtractionError("query task is detached from its canonical plan")
    if task.target_name not in _TARGETS:
        raise PathwayExtractionError("query task is not a supported pathway task")
    family, pathway_type = _TARGETS[task.target_name]
    trace = next((item for item in plan.pathway_trace if item.pathway_id == family), None)
    if trace is None or trace.decision == "exclude":
        raise PathwayExtractionError("query task is detached from active profile trace")
    if tuple(item.to_dict() for item in plan.pathway_trace) != _profile_pathway_trace(
        profile
    ):
        raise PathwayExtractionError("profile pathway trace disagrees with query plan")
    if (
        plan.province != profile.province
        or plan.mode != profile.subject_mode
        or plan.exam_year != profile.exam_year
        or task.province != profile.province
        or not 0 <= plan.research_year - task.year <= 3
    ):
        raise PathwayExtractionError("profile, plan, and pathway task contexts disagree")
    if isinstance(candidates, (str, bytes, bytearray)):
        raise TypeError("candidates must contain SourceCandidate records")
    caller_candidates = tuple(candidates)
    normalized_candidates = _snapshot_candidates(caller_candidates)
    documents = _documents(extraction, field_map)
    if len(documents) != len(normalized_candidates):
        raise PathwayExtractionError("each pathway source requires one adapter output")
    source_by_id = {item.source_id: item for item in normalized_candidates}
    ordered_sources = sorted(source_by_id)
    # Candidate ordering is canonical; bind documents to caller order before sorting.
    document_by_id = {
        item.source_id: document for item, document in zip(caller_candidates, documents)
    }
    task_value = {
        "task_id": task.task_id,
        "kind": task.kind,
        "target_name": task.target_name,
        "province": task.province,
        "subject_group": task.subject_group,
        "subject_mode": profile.subject_mode,
        "year": task.year,
        "target_year": plan.research_year,
        "source_policy_id": task.source_policy_id,
        "source_policy_version": task.source_policy_version,
    }
    task_value["task_digest"] = _digest(task_value)
    input_projection = {
        "schema_version": "1.0",
        "profile_digest": profile.digest,
        "query_plan_digest": _digest(plan.to_dict()),
        "task": task_value,
        "pathway_family": family,
        "pathway_type": pathway_type,
        "sources": [_candidate_projection(source_by_id[item]) for item in ordered_sources],
        "documents": [document_by_id[item] for item in ordered_sources],
    }
    return _project_from_input(input_projection)


def validate_pathway_policy_projection(
    projection: PathwayPolicyProjection,
) -> PathwayPolicyProjection:
    """Rebuild a projection from its persisted typed inputs."""

    if type(projection) is not PathwayPolicyProjection:
        raise TypeError("projection must be a PathwayPolicyProjection")
    rebuilt = _project_from_input(projection.input_projection)
    if rebuilt.to_dict() != projection.to_dict():
        raise PathwayExtractionError("pathway projection no longer matches its inputs")
    return projection


def validate_pathway_policy_projection_sources(
    projection: PathwayPolicyProjection,
    candidates: Iterable[SourceCandidate],
) -> PathwayPolicyProjection:
    """Bind a replayed projection to freshly validated public candidates."""

    validate_pathway_policy_projection(projection)
    snapshots = _snapshot_candidates(candidates)
    expected = projection.input_projection["sources"]
    actual = [_candidate_projection(item) for item in snapshots]
    if actual != expected:
        raise PathwayExtractionError(
            "pathway projection source identities do not match validated candidates"
        )
    return projection


def replay_pathway_policy_projection(value: Any) -> PathwayPolicyProjection:
    """Rebuild a persisted projection value and verify every serialized field."""

    if not isinstance(value, Mapping):
        raise PathwayExtractionError("persisted pathway projection is invalid")
    input_projection = value.get("input_projection")
    rebuilt = _project_from_input(input_projection)
    if rebuilt.to_dict() != dict(value):
        raise PathwayExtractionError("persisted pathway projection does not replay")
    return rebuilt


__all__ = [
    "FieldProvenance",
    "PathwayExtractionError",
    "PathwayPolicyProjection",
    "extract_pathway_policy",
    "replay_pathway_policy_projection",
    "validate_pathway_policy_projection",
    "validate_pathway_policy_projection_sources",
]
