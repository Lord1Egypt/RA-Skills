"""Authenticated school/program metadata used by personalized recommendations.

The module is the sole seam between host-normalized plan/policy/subject rows
and admission-row personalization.  Hosts may report exact fees, but only the
versioned project policy below may derive affordability labels.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
import unicodedata
from typing import Any, Iterable, Mapping

if __package__ == "scripts.adapters":
    from . import (
        CellStatus,
        ExtractedCoverage,
        ExtractedRow,
        ExtractedTable,
        validate_public_locator,
    )
    from .public_text import (
        PublicTextAdapterError,
        PublicTextDocument,
        PublicTextField,
        bind_public_text,
        public_text_projection,
        validate_public_text_projection,
    )
    from ..contracts import (
        EvidenceFact,
        EvidenceStatus,
        FactClaim,
        SourceCandidate,
        SourceTier,
    )
    from ..evidence import EvidenceStore
    from ..planning_profile import PlanningProfile
    from ..query_plan import QueryPlan, QueryTask, validate_query_plan_payload
    from ..source_policy import canonicalize_provenance_url, evaluate_claims
    from ..validate_data import ValidatedAdmissionRow, admission_row_hash
else:  # ``sys.path`` rooted at ``scripts`` package compatibility.
    from adapters import (  # type: ignore
        CellStatus,
        ExtractedCoverage,
        ExtractedRow,
        ExtractedTable,
        validate_public_locator,
    )
    from adapters.public_text import (  # type: ignore
        PublicTextAdapterError,
        PublicTextDocument,
        PublicTextField,
        bind_public_text,
        public_text_projection,
        validate_public_text_projection,
    )
    from contracts import (  # type: ignore
        EvidenceFact,
        EvidenceStatus,
        FactClaim,
        SourceCandidate,
        SourceTier,
    )
    from evidence import EvidenceStore  # type: ignore
    from planning_profile import PlanningProfile  # type: ignore
    from query_plan import QueryPlan, QueryTask, validate_query_plan_payload  # type: ignore
    from source_policy import canonicalize_provenance_url, evaluate_claims  # type: ignore
    from validate_data import ValidatedAdmissionRow, admission_row_hash  # type: ignore


AFFORDABILITY_POLICY_ID = "pathway-atlas-school-fee-affordability"
AFFORDABILITY_POLICY_VERSION = "1.0"
_AFFORDABILITY_POLICY_CORE = {
    "policy_id": AFFORDABILITY_POLICY_ID,
    "version": AFFORDABILITY_POLICY_VERSION,
    "currency": "CNY",
    "period": "academic_year",
    "limited_max": 10000,
    "moderate_max": 50000,
}
_SAFE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")
_DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")
_FIELD = re.compile(
    r"school_fit:(province_policy|enrollment_plan|admission_charter|tuition_fee|subject_requirement):"
    r"(20[0-9]{2}):([0-9a-f]{64})\Z"
)
_ACCEPTED = frozenset(
    {
        EvidenceStatus.OFFICIAL,
        EvidenceStatus.CORROBORATED,
        EvidenceStatus.REFERENCE,
    }
)
_KINDS = frozenset(
    {
        "province_policy",
        "enrollment_plan",
        "admission_charter",
        "tuition_fee",
        "subject_requirement",
    }
)
_METHODS = frozenset({"html-table", "xlsx-worksheet", "xls-worksheet", "pdf-text-table", "host-ocr-rows"})
_PUBLIC_TEXT_METHOD = "host-public-text"
_INSTITUTION_TYPES = frozenset({"public", "private", "cooperative"})
_PERSISTED_ORIGIN_KIND = "school-fit-bridge-origin-v1"

_PROVINCE_FIELDS = frozenset(
    {
        "province",
        "year",
        "exam_mode",
        "subject_structure",
        "batch_structure",
        "effective_date",
    }
)
_ENROLLMENT_FIELDS = frozenset(
    {
        "province",
        "year",
        "subject_group",
        "institution",
        "institution_code",
        "program_group",
        "majors",
        "school_province",
        "school_city",
        "institution_type",
    }
)
_SUBJECT_FIELDS = frozenset(
    {
        "province",
        "year",
        "subject_group",
        "institution",
        "institution_code",
        "program_group",
        "required_secondary_subjects",
        "secondary_subject_rule",
        "special_conditions",
    }
)
_CHARTER_FIELDS = frozenset(
    {
        "province",
        "year",
        "institution",
        "institution_code",
        "admission_rules",
        "adjustment_rules",
        "adjustment_required",
        "health_restrictions",
        "language_restrictions",
        "single_subject_restrictions",
        "special_conditions",
    }
)
_TUITION_FIELDS = frozenset(
    {
        "province",
        "year",
        "institution",
        "institution_code",
        "program_group",
        "majors",
        "annual_fee_amount",
        "fee_currency",
        "fee_period",
        "accommodation_fee",
        "other_required_fees",
        "financial_aid",
    }
)
_OPTIONAL_EMPTY_FIELDS = {
    "admission_charter": frozenset(
        {
            "health_restrictions",
            "language_restrictions",
            "single_subject_restrictions",
            "special_conditions",
        }
    ),
    "tuition_fee": frozenset(
        {"accommodation_fee", "other_required_fees", "financial_aid"}
    ),
}
_FIELDS_BY_KIND = {
    "province_policy": _PROVINCE_FIELDS,
    "enrollment_plan": _ENROLLMENT_FIELDS,
    "admission_charter": _CHARTER_FIELDS,
    "tuition_fee": _TUITION_FIELDS,
    "subject_requirement": _SUBJECT_FIELDS,
}
_BASE_VALUE_FIELDS = frozenset(
    {
        "schema_version",
        "profile_digest",
        "query_plan_digest",
        "task_id",
        "kind",
        "province",
        "year",
        "subject_group",
    }
)
_ENROLLMENT_VALUE_FIELDS = _BASE_VALUE_FIELDS | frozenset(
    {
        "school_code",
        "school_name",
        "program_group",
        "majors_in_group",
        "school_province",
        "city_location",
        "institution_type",
    }
)
_SUBJECT_VALUE_FIELDS = _BASE_VALUE_FIELDS | frozenset(
    {
        "school_code",
        "school_name",
        "program_group",
        "required_secondary_subjects",
        "secondary_subject_rule",
        "special_conditions",
    }
)
_CHARTER_VALUE_FIELDS = _BASE_VALUE_FIELDS | frozenset(
    {
        "school_code",
        "school_name",
        "admission_rules",
        "adjustment_rules",
        "adjustment_required",
        "health_restrictions",
        "language_restrictions",
        "single_subject_restrictions",
        "special_conditions",
        "unverified_fields",
    }
)
_TUITION_VALUE_FIELDS = _BASE_VALUE_FIELDS | frozenset(
    {
        "school_code",
        "school_name",
        "program_group",
        "majors",
        "annual_fee_amount",
        "fee_currency",
        "fee_period",
        "accommodation_fee",
        "other_required_fees",
        "financial_aid",
        "affordable_for",
        "affordability_policy",
        "unverified_fields",
    }
)
_PROVINCE_VALUE_FIELDS = _BASE_VALUE_FIELDS | frozenset(
    {"exam_mode", "subject_structure", "batch_structure", "effective_date"}
)
_MERGED_ADMISSION_FIELDS = frozenset(
    {
        "admission_evidence_row_hash",
        "majors_in_group",
        "school_province",
        "city_location",
        "institution_type",
        "adjustment_required",
        "annual_fee_amount",
        "fee_currency",
        "fee_period",
        "affordable_for",
        "affordability_policy_id",
        "affordability_policy_version",
        "affordability_policy_digest",
        "required_secondary_subjects",
        "secondary_subject_rule",
        "subject_special_conditions",
        "school_fit_source_ids",
        "school_fit_enrollment_source_ids",
        "school_fit_subject_source_ids",
        "school_fit_province_policy_source_ids",
        "school_fit_charter_source_ids",
        "school_fit_tuition_source_ids",
        "school_fit_enrollment_status",
        "school_fit_subject_status",
        "school_fit_province_policy_status",
        "school_fit_charter_status",
        "school_fit_tuition_status",
        "school_fit_enrollment_year",
        "school_fit_subject_year",
        "school_fit_province_policy_year",
        "school_fit_charter_year",
        "school_fit_tuition_year",
        "school_fit_enrollment_current_status",
        "school_fit_subject_current_status",
        "school_fit_province_policy_current_status",
        "school_fit_charter_current_status",
        "school_fit_tuition_current_status",
        "school_fit_enrollment_current_year",
        "school_fit_subject_current_year",
        "school_fit_province_policy_current_year",
        "school_fit_charter_current_year",
        "school_fit_tuition_current_year",
        "school_fit_enrollment_current_source_ids",
        "school_fit_subject_current_source_ids",
        "school_fit_province_policy_current_source_ids",
        "school_fit_charter_current_source_ids",
        "school_fit_tuition_current_source_ids",
        "school_fit_statuses",
        "school_fit_conflict_kinds",
        "province_policy_exam_mode",
        "province_policy_subject_structure",
        "province_policy_batch_structure",
        "province_policy_effective_date",
        "charter_admission_rules",
        "charter_adjustment_rules",
        "charter_adjustment_required",
        "charter_health_restrictions",
        "charter_language_restrictions",
        "charter_single_subject_restrictions",
        "charter_special_conditions",
        "charter_unverified_fields",
        "tuition_majors",
        "tuition_annual_fee_amount",
        "tuition_fee_currency",
        "tuition_fee_period",
        "tuition_accommodation_fee",
        "tuition_other_required_fees",
        "tuition_financial_aid",
        "tuition_affordable_for",
        "tuition_affordability_policy_id",
        "tuition_affordability_policy_version",
        "tuition_affordability_policy_digest",
        "tuition_unverified_fields",
    }
)


class SchoolFitBridgeError(ValueError):
    """School-fit evidence cannot be authenticated or safely joined."""


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


def _policy() -> dict[str, Any]:
    return {
        **_AFFORDABILITY_POLICY_CORE,
        "policy_digest": _digest(_AFFORDABILITY_POLICY_CORE),
    }


def _text(value: Any, name: str) -> str:
    if (
        not isinstance(value, str)
        or not value
        or value != value.strip()
        or value != unicodedata.normalize("NFKC", value)
        or len(value) > 512
        or any(ord(char) < 32 or ord(char) == 127 for char in value)
    ):
        raise SchoolFitBridgeError(f"{name} must be canonical exact text")
    try:
        validate_public_locator(value)
    except (TypeError, ValueError):
        raise SchoolFitBridgeError(f"{name} is not public-safe") from None
    return value


def _strings(
    value: Any,
    name: str,
    *,
    allow_empty: bool = False,
) -> tuple[str, ...]:
    if isinstance(value, (str, bytes, bytearray)):
        raise SchoolFitBridgeError(f"{name} must be an ordered collection")
    try:
        values = tuple(_text(item, name) for item in value)
    except TypeError:
        raise SchoolFitBridgeError(f"{name} must be an ordered collection") from None
    if (not values and not allow_empty) or len(values) != len(set(values)):
        raise SchoolFitBridgeError(f"{name} must contain unique exact values")
    return tuple(sorted(values))


def _positive_integer(value: Any, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise SchoolFitBridgeError(f"{name} must be a non-negative integer")
    return value


def _optional_text(value: Any, name: str) -> str | None:
    return None if value is None else _text(value, name)


def _optional_integer(value: Any, name: str) -> int | None:
    return None if value is None else _positive_integer(value, name)


def _plan_context(
    profile: Any, plan: Any, task: Any
) -> tuple[PlanningProfile, QueryPlan, QueryTask, str]:
    if not isinstance(profile, PlanningProfile):
        raise TypeError("profile must be a PlanningProfile")
    if type(plan) is not QueryPlan:
        raise TypeError("plan must be a QueryPlan")
    try:
        canonical_plan = validate_query_plan_payload(plan.to_dict())
    except (KeyError, TypeError, ValueError):
        raise SchoolFitBridgeError("query plan is not canonical") from None
    if canonical_plan.to_dict() != plan.to_dict():
        raise SchoolFitBridgeError("query plan is not canonical")
    if not isinstance(task, QueryTask):
        raise TypeError("task must be a QueryTask")
    matches = tuple(item for item in canonical_plan.tasks if item.task_id == task.task_id)
    if len(matches) != 1 or matches[0].to_dict() != task.to_dict():
        raise SchoolFitBridgeError("query task is outside the plan")
    canonical_task = matches[0]
    if canonical_task.kind not in _KINDS:
        raise SchoolFitBridgeError("query task is not a school-fit evidence task")
    if (
        profile.province != canonical_plan.province
        or profile.exam_year != canonical_plan.exam_year
        or canonical_task.province != profile.province
        or canonical_task.subject_group != canonical_plan.subject_group
    ):
        raise SchoolFitBridgeError("profile, plan and task contexts disagree")
    return profile, canonical_plan, canonical_task, _digest(canonical_plan.to_dict())


def _affordable_for(amount: int, currency: str, period: str) -> tuple[str, ...]:
    policy = _policy()
    if currency != policy["currency"] or period != policy["period"]:
        raise SchoolFitBridgeError(
            "fee cannot be mapped by the current affordability policy"
        )
    if amount <= policy["limited_max"]:
        return ("limited", "moderate", "flexible")
    if amount <= policy["moderate_max"]:
        return ("moderate", "flexible")
    return ("flexible",)


def _key(kind: str, values: Mapping[str, Any]) -> dict[str, str]:
    if kind == "province_policy":
        return {
            "province": _text(values["province"], "province"),
            "year": str(values["year"]),
        }
    school = {
        "school_code": _text(values["institution_code"], "institution_code"),
        "school_name": _text(values["institution"], "institution"),
    }
    if kind == "admission_charter":
        return school
    return {
        **school,
        "program_group": _text(values["program_group"], "program_group"),
    }


def _normalize_projection(
    kind: str,
    raw: Mapping[str, Any],
    *,
    profile_digest: str,
    query_plan_digest: str,
    task: QueryTask,
) -> dict[str, Any]:
    if not isinstance(raw, Mapping) or set(raw) != set(_FIELDS_BY_KIND[kind]):
        if isinstance(raw, Mapping) and "affordable_for" in raw:
            raise SchoolFitBridgeError(
                "affordability labels must be derived by the project policy"
            )
        raise SchoolFitBridgeError("school-fit extraction fields do not match the task")
    province = _text(raw["province"], "province")
    year = _positive_integer(raw["year"], "year")
    if province != task.province or year != task.year:
        raise SchoolFitBridgeError("school-fit row context disagrees with the task")
    subject_group = (
        _text(raw["subject_group"], "subject_group")
        if kind in {"enrollment_plan", "subject_requirement"}
        else task.subject_group
    )
    if subject_group != task.subject_group:
        raise SchoolFitBridgeError("school-fit subject group disagrees with the task")
    base: dict[str, Any] = {
        "schema_version": "1.0",
        "profile_digest": profile_digest,
        "query_plan_digest": query_plan_digest,
        "task_id": task.task_id,
        "kind": kind,
        "province": province,
        "year": year,
        "subject_group": subject_group,
    }
    if kind == "province_policy":
        base.update(
            {
                name: _text(raw[name], name)
                for name in (
                    "exam_mode",
                    "subject_structure",
                    "batch_structure",
                    "effective_date",
                )
            }
        )
        return base

    school_code = _text(raw["institution_code"], "institution_code")
    school_name = _text(raw["institution"], "institution")
    base.update(
        {
            "school_code": school_code,
            "school_name": school_name,
        }
    )
    if kind == "admission_charter":
        adjustment = raw["adjustment_required"]
        if not isinstance(adjustment, bool):
            raise SchoolFitBridgeError("adjustment_required must be boolean")
        base.update(
            {
                "admission_rules": _text(raw["admission_rules"], "admission_rules"),
                "adjustment_rules": _text(raw["adjustment_rules"], "adjustment_rules"),
                "adjustment_required": adjustment,
                "health_restrictions": _optional_text(
                    raw["health_restrictions"], "health_restrictions"
                ),
                "language_restrictions": _optional_text(
                    raw["language_restrictions"], "language_restrictions"
                ),
                "single_subject_restrictions": _optional_text(
                    raw["single_subject_restrictions"],
                    "single_subject_restrictions",
                ),
                "special_conditions": _optional_text(
                    raw["special_conditions"], "special_conditions"
                ),
                "unverified_fields": sorted(
                    name
                    for name in _OPTIONAL_EMPTY_FIELDS["admission_charter"]
                    if raw[name] is None
                ),
            }
        )
        return base

    program_group = _text(raw["program_group"], "program_group")
    base["program_group"] = program_group
    if kind == "subject_requirement":
        rule = _text(raw["secondary_subject_rule"], "secondary_subject_rule")
        if rule not in {"any", "all"}:
            raise SchoolFitBridgeError("secondary subject rule is unsupported")
        base.update(
            {
                "required_secondary_subjects": list(
                    _strings(
                        raw["required_secondary_subjects"],
                        "required_secondary_subjects",
                        allow_empty=True,
                    )
                ),
                "secondary_subject_rule": rule,
                "special_conditions": _text(
                    raw["special_conditions"], "special_conditions"
                ),
            }
        )
        return base

    if kind == "tuition_fee":
        amount = _positive_integer(raw["annual_fee_amount"], "annual_fee_amount")
        currency = _text(raw["fee_currency"], "fee_currency")
        period = _text(raw["fee_period"], "fee_period")
        base.update(
            {
                "majors": list(_strings(raw["majors"], "majors")),
                "annual_fee_amount": amount,
                "fee_currency": currency,
                "fee_period": period,
                "accommodation_fee": _optional_integer(
                    raw["accommodation_fee"], "accommodation_fee"
                ),
                "other_required_fees": _optional_text(
                    raw["other_required_fees"], "other_required_fees"
                ),
                "financial_aid": _optional_text(
                    raw["financial_aid"], "financial_aid"
                ),
                "affordable_for": list(_affordable_for(amount, currency, period)),
                "affordability_policy": _policy(),
                "unverified_fields": sorted(
                    name
                    for name in _OPTIONAL_EMPTY_FIELDS["tuition_fee"]
                    if raw[name] is None
                ),
            }
        )
        return base

    institution_type = _text(raw["institution_type"], "institution_type")
    if institution_type not in _INSTITUTION_TYPES:
        raise SchoolFitBridgeError("institution type is unsupported")
    base.update(
        {
            "majors_in_group": list(_strings(raw["majors"], "majors")),
            "school_province": _text(raw["school_province"], "school_province"),
            "city_location": _text(raw["school_city"], "school_city"),
            "institution_type": institution_type,
        }
    )
    return base


def _fact_id(kind: str, year: int, key_digest: str) -> str:
    return f"school-fit-{kind}-{year}-{key_digest.removeprefix('sha256:')[:16]}"


def _public_text_table(
    document: PublicTextDocument,
    *,
    kind: str,
) -> tuple[dict[str, Any], ExtractedTable, ExtractedRow]:
    try:
        projection = public_text_projection(
            document,
            required_fields=sorted(_FIELDS_BY_KIND[kind]),
        )
        validate_public_text_projection(
            projection,
            required_fields=sorted(_FIELDS_BY_KIND[kind]),
        )
    except (PublicTextAdapterError, TypeError, ValueError):
        raise SchoolFitBridgeError("public text school-fit fields are invalid") from None
    values: dict[str, Any] = {}
    statuses: dict[str, CellStatus] = {}
    warnings: list[str] = []
    for name, field in projection["fields"].items():
        values[name] = field["value"]
        status = CellStatus(field["cell_status"])
        if (
            field["value"] is None
            and field["quote"] is None
            and status is CellStatus.EXACT
        ):
            status = CellStatus.EMPTY
        statuses[name] = status
        if field["warning"] is not None:
            warnings.append(field["warning"])
    text_identity = projection["text_hash"].removeprefix("sha256:")[:16]
    row = ExtractedRow(
        values=values,
        cell_status=statuses,
        location=f"text[{text_identity}]/fields[{kind}]",
        confidence=1,
        warnings=tuple(sorted(warnings)),
    )
    table = ExtractedTable(
        table_id=f"public-text[{text_identity}]",
        caption=None,
        sheet=None,
        rows=(row,),
        coverage=ExtractedCoverage(),
        warnings=tuple(sorted(warnings)),
        extraction_method=_PUBLIC_TEXT_METHOD,
    )
    return projection, table, row


def _public_text_document_from_projection(
    value: Any,
    *,
    kind: str,
) -> PublicTextDocument:
    required_fields = sorted(_FIELDS_BY_KIND[kind])
    try:
        projection = validate_public_text_projection(
            value,
            required_fields=required_fields,
        )
        fields = {
            name: PublicTextField(
                value=item["value"],
                quote=item["quote"],
                start=item["start"],
                end=item["end"],
                status=item["cell_status"],
            )
            for name, item in projection["fields"].items()
        }
        return bind_public_text(
            source_id=projection["source_id"],
            url=projection["url"],
            text=projection["text"],
            fields=fields,
        )
    except (PublicTextAdapterError, KeyError, TypeError, ValueError):
        raise SchoolFitBridgeError(
            "public text school-fit projection does not replay"
        ) from None


def _candidate_from_origin(value: Any) -> SourceCandidate:
    if not isinstance(value, Mapping):
        raise SchoolFitBridgeError("school-fit source origin is invalid")
    try:
        candidate = SourceCandidate(
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
        raise SchoolFitBridgeError("school-fit source origin is invalid") from None
    if candidate.to_dict() != dict(value):
        raise SchoolFitBridgeError("school-fit source origin is not canonical")
    return candidate


@dataclass(frozen=True, init=False)
class SchoolFitEvidenceBridge:
    """Factory-only typed receipt for one school/program key and query task."""

    task: QueryTask
    profile_digest: str
    query_plan_digest: str
    tables: tuple[ExtractedTable, ...]
    adapter_rows: tuple[ExtractedRow, ...]
    candidates: tuple[SourceCandidate, ...]
    evidence_status: EvidenceStatus
    source_ids: tuple[str, ...]
    evidence_method: str
    extraction_method: str
    locator: str
    key_digest: str
    bridge_digest: str
    _metadata_json: str | None
    _fact_json: str
    _origin_json: str

    def __init__(self) -> None:
        raise TypeError("SchoolFitEvidenceBridge is factory-only")

    @classmethod
    def _create(cls, **values: Any) -> "SchoolFitEvidenceBridge":
        instance = object.__new__(cls)
        for name, value in values.items():
            object.__setattr__(instance, name, value)
        return instance

    @property
    def metadata(self) -> dict[str, Any] | None:
        return None if self._metadata_json is None else json.loads(self._metadata_json)

    @property
    def fact(self) -> EvidenceFact:
        payload = json.loads(self._fact_json)
        return EvidenceFact(
            fact_id=payload["fact_id"],
            field=payload["field"],
            value=payload["value"],
            unit=payload["unit"],
            status=EvidenceStatus(payload["status"]),
            source_ids=tuple(payload["source_ids"]),
            method=payload["method"],
            notes=payload["notes"],
        )

    def persist(self, store: EvidenceStore) -> None:
        if not isinstance(store, EvidenceStore):
            raise TypeError("store must be an EvidenceStore")
        store.add_fact(
            self.fact,
            year=self.task.year,
            extraction_method=self.extraction_method,
            locator=self.locator,
        )
        store.add_context(
            {
                "kind": _PERSISTED_ORIGIN_KIND,
                "fact_id": self.fact.fact_id,
                "bridge_digest": self.bridge_digest,
                "origin": json.loads(self._origin_json),
            }
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "task": self.task.to_dict(),
            "profile_digest": self.profile_digest,
            "query_plan_digest": self.query_plan_digest,
            "tables": [table.to_dict() for table in self.tables],
            "adapter_rows": [row.to_dict() for row in self.adapter_rows],
            "sources": [candidate.to_dict() for candidate in self.candidates],
            "evidence_status": self.evidence_status.value,
            "source_ids": list(self.source_ids),
            "evidence_method": self.evidence_method,
            "extraction_method": self.extraction_method,
            "locator": self.locator,
            "key_digest": self.key_digest,
            "metadata": self.metadata,
            "fact": self.fact.to_dict(),
            "bridge_digest": self.bridge_digest,
        }


def _bridge_school_fit_evidence(
    *,
    profile: PlanningProfile,
    plan: QueryPlan,
    task: QueryTask,
    tables: tuple[ExtractedTable, ...],
    adapter_rows: tuple[ExtractedRow, ...],
    candidates: tuple[SourceCandidate, ...],
    public_documents: Mapping[str, Mapping[str, Any]] | None = None,
) -> SchoolFitEvidenceBridge:
    """Authenticate aligned source rows and derive one typed metadata fact."""

    canonical_profile, canonical_plan, canonical_task, plan_digest = _plan_context(
        profile, plan, task
    )
    if not isinstance(tables, tuple) or not isinstance(adapter_rows, tuple):
        raise TypeError("tables and adapter_rows must be tuples")
    if not isinstance(candidates, tuple):
        raise TypeError("candidates must be a tuple")
    if not tables or not (len(tables) == len(adapter_rows) == len(candidates)):
        raise SchoolFitBridgeError("each source requires exactly one aligned row")
    if not all(isinstance(item, SourceCandidate) for item in candidates):
        raise TypeError("candidates must contain SourceCandidate records")
    if len({item.source_id for item in candidates}) != len(candidates):
        raise SchoolFitBridgeError("candidate source IDs must be unique")

    aligned = []
    for table, row, candidate in zip(tables, adapter_rows, candidates):
        if not isinstance(table, ExtractedTable) or not isinstance(row, ExtractedRow):
            raise TypeError("tables and rows must be adapter contracts")
        if sum(item is row for item in table.rows) != 1:
            raise SchoolFitBridgeError("adapter row is detached from its table")
        if table.extraction_method not in _METHODS and not (
            public_documents is not None
            and table.extraction_method == _PUBLIC_TEXT_METHOD
        ):
            raise SchoolFitBridgeError("adapter extraction method is unsupported")
        optional_empty = _OPTIONAL_EMPTY_FIELDS.get(canonical_task.kind, frozenset())
        for name, status in row.cell_status.items():
            if status is CellStatus.EXACT:
                continue
            if (
                name in optional_empty
                and status is CellStatus.EMPTY
                and row.values.get(name) is None
            ):
                continue
            raise SchoolFitBridgeError(
                "school-fit adapter cells must be exact or explicit optional empty"
            )
        projection = _normalize_projection(
            canonical_task.kind,
            row.values,
            profile_digest=canonical_profile.digest,
            query_plan_digest=plan_digest,
            task=canonical_task,
        )
        aligned.append((candidate, table, row, projection))
    aligned.sort(key=lambda item: item[0].source_id)
    keys = {_digest(_key(canonical_task.kind, row.values)) for _c, _t, row, _p in aligned}
    if len(keys) != 1:
        raise SchoolFitBridgeError("sources do not describe one school/program key")
    key_digest = next(iter(keys))
    field = (
        f"school_fit:{canonical_task.kind}:{canonical_task.year}:"
        f"{key_digest.removeprefix('sha256:')}"
    )
    evaluated = evaluate_claims(
        field,
        tuple(
            FactClaim(
                field=field,
                value=projection,
                unit=None,
                source_id=candidate.source_id,
                method="school-fit-adapter-bridge-v1",
            )
            for candidate, _table, _row, projection in aligned
        ),
        tuple(item[0] for item in aligned),
    )
    metadata = evaluated.value if evaluated.status in _ACCEPTED else None
    fact = EvidenceFact(
        fact_id=_fact_id(canonical_task.kind, canonical_task.year, key_digest),
        field=field,
        value=metadata,
        unit=None,
        status=evaluated.status,
        source_ids=evaluated.source_ids,
        method=evaluated.method,
        notes=f"query_task:{canonical_task.task_id}",
    )
    extraction_methods = {item[1].extraction_method for item in aligned}
    extraction_method = (
        next(iter(extraction_methods))
        if len(extraction_methods) == 1
        else "mixed-structured-adapters"
    )
    locator = (
        aligned[0][2].location
        if len(aligned) == 1
        else f"school-fit-rows:{key_digest.removeprefix('sha256:')[:16]}"
    )
    if public_documents is None:
        origin = {
            "schema_version": "1.0",
            "profile_digest": canonical_profile.digest,
            "query_plan_digest": plan_digest,
            "task": canonical_task.to_dict(),
            "tables": [item[1].to_dict() for item in aligned],
            "adapter_row_indexes": [
                next(index for index, row in enumerate(item[1].rows) if row is item[2])
                for item in aligned
            ],
            "sources": [item[0].to_dict() for item in aligned],
        }
    else:
        if set(public_documents) != {
            item[0].source_id for item in aligned
        }:
            raise SchoolFitBridgeError("public text documents and sources disagree")
        origin = {
            "schema_version": "1.0",
            "adapter_kind": "public-text",
            "profile_digest": canonical_profile.digest,
            "query_plan_digest": plan_digest,
            "task": canonical_task.to_dict(),
            "documents": [
                dict(public_documents[item[0].source_id]) for item in aligned
            ],
            "sources": [item[0].to_dict() for item in aligned],
        }
    fact_json = _canonical_json(fact.to_dict())
    origin_json = _canonical_json(origin)
    bridge_digest = _digest(
        {
            "origin": origin,
            "fact": fact.to_dict(),
            "key_digest": key_digest,
            "extraction_method": extraction_method,
            "locator": locator,
        }
    )
    return SchoolFitEvidenceBridge._create(
        task=canonical_task,
        profile_digest=canonical_profile.digest,
        query_plan_digest=plan_digest,
        tables=tuple(item[1] for item in aligned),
        adapter_rows=tuple(item[2] for item in aligned),
        candidates=tuple(item[0] for item in aligned),
        evidence_status=evaluated.status,
        source_ids=evaluated.source_ids,
        evidence_method=evaluated.method,
        extraction_method=extraction_method,
        locator=locator,
        key_digest=key_digest,
        bridge_digest=bridge_digest,
        _metadata_json=(None if metadata is None else _canonical_json(metadata)),
        _fact_json=fact_json,
        _origin_json=origin_json,
    )


def bridge_school_fit_evidence(
    *,
    profile: PlanningProfile,
    plan: QueryPlan,
    task: QueryTask,
    tables: tuple[ExtractedTable, ...],
    adapter_rows: tuple[ExtractedRow, ...],
    candidates: tuple[SourceCandidate, ...],
) -> SchoolFitEvidenceBridge:
    """Authenticate aligned structured source rows and derive one metadata fact."""

    return _bridge_school_fit_evidence(
        profile=profile,
        plan=plan,
        task=task,
        tables=tables,
        adapter_rows=adapter_rows,
        candidates=candidates,
    )


def bridge_school_fit_public_text(
    profile: PlanningProfile,
    plan: QueryPlan,
    task: QueryTask,
    documents: tuple[PublicTextDocument, ...],
    candidates: tuple[SourceCandidate, ...],
) -> SchoolFitEvidenceBridge:
    """Bridge source-bound public prose through the existing school-fit policy."""

    _canonical_profile, _canonical_plan, canonical_task, _plan_digest = _plan_context(
        profile, plan, task
    )
    if not isinstance(documents, tuple):
        raise TypeError("documents must be a tuple")
    if not isinstance(candidates, tuple):
        raise TypeError("candidates must be a tuple")
    if not documents or len(documents) != len(candidates):
        raise SchoolFitBridgeError("each public document requires one source candidate")
    if not all(type(item) is PublicTextDocument for item in documents):
        raise TypeError("documents must contain PublicTextDocument records")
    if not all(isinstance(item, SourceCandidate) for item in candidates):
        raise TypeError("candidates must contain SourceCandidate records")

    tables: list[ExtractedTable] = []
    rows: list[ExtractedRow] = []
    projections: dict[str, Mapping[str, Any]] = {}
    for document, candidate in zip(documents, candidates):
        try:
            candidate_url = canonicalize_provenance_url(candidate.url)
        except (TypeError, ValueError):
            candidate_url = None
        if (
            document.source_id != candidate.source_id
            or candidate_url is None
            or document.url != candidate_url
        ):
            raise SchoolFitBridgeError(
                "public text source provenance disagrees with its candidate"
            )
        projection, table, row = _public_text_table(
            document,
            kind=canonical_task.kind,
        )
        if candidate.source_id in projections:
            raise SchoolFitBridgeError("candidate source IDs must be unique")
        projections[candidate.source_id] = projection
        tables.append(table)
        rows.append(row)
    return _bridge_school_fit_evidence(
        profile=profile,
        plan=plan,
        task=canonical_task,
        tables=tuple(tables),
        adapter_rows=tuple(rows),
        candidates=candidates,
        public_documents=projections,
    )


def _replay_school_fit_public_text_origin(
    origin: Mapping[str, Any],
    profile: PlanningProfile,
    plan: QueryPlan,
) -> SchoolFitEvidenceBridge:
    expected = {
        "schema_version",
        "adapter_kind",
        "profile_digest",
        "query_plan_digest",
        "task",
        "documents",
        "sources",
    }
    if not isinstance(origin, Mapping) or set(origin) != expected:
        raise SchoolFitBridgeError("public text school-fit origin is invalid")
    if origin["schema_version"] != "1.0" or origin["adapter_kind"] != "public-text":
        raise SchoolFitBridgeError("public text school-fit origin identity is invalid")
    task_raw = origin["task"]
    document_values = origin["documents"]
    source_values = origin["sources"]
    if (
        not isinstance(task_raw, Mapping)
        or not isinstance(document_values, list)
        or not isinstance(source_values, list)
        or not document_values
        or len(document_values) != len(source_values)
    ):
        raise SchoolFitBridgeError("public text school-fit origin is incomplete")
    try:
        task = QueryTask(**dict(task_raw))
    except (KeyError, TypeError, ValueError):
        raise SchoolFitBridgeError("public text school-fit task is invalid") from None
    if task.to_dict() != dict(task_raw):
        raise SchoolFitBridgeError("public text school-fit task is not canonical")
    if task.kind not in _KINDS:
        raise SchoolFitBridgeError("public text school-fit task kind is invalid")
    if (
        origin["profile_digest"] != profile.digest
        or origin["query_plan_digest"] != _digest(plan.to_dict())
    ):
        raise SchoolFitBridgeError("public text school-fit context disagrees")
    candidates = tuple(_candidate_from_origin(item) for item in source_values)
    documents = tuple(
        _public_text_document_from_projection(item, kind=task.kind)
        for item in document_values
    )
    return bridge_school_fit_public_text(
        profile,
        plan,
        task,
        documents,
        candidates,
    )


def validate_school_fit_evidence_bridge(
    bridge: SchoolFitEvidenceBridge,
    profile: PlanningProfile,
    plan: QueryPlan,
) -> SchoolFitEvidenceBridge:
    """Replay the factory origin and reject post-construction mutation."""

    if type(bridge) is not SchoolFitEvidenceBridge:
        raise TypeError("bridge must be a SchoolFitEvidenceBridge")
    try:
        origin = json.loads(bridge._origin_json)
    except (AttributeError, TypeError, ValueError, json.JSONDecodeError):
        raise SchoolFitBridgeError("school-fit bridge origin is invalid") from None
    if not isinstance(origin, dict) or _canonical_json(origin) != bridge._origin_json:
        raise SchoolFitBridgeError("school-fit bridge origin is not canonical")
    if (
        origin.get("profile_digest") != profile.digest
        or origin.get("query_plan_digest") != _digest(plan.to_dict())
        or origin.get("task") != bridge.task.to_dict()
    ):
        raise SchoolFitBridgeError("school-fit bridge context was mutated")
    if origin.get("adapter_kind") == "public-text":
        rebuilt = _replay_school_fit_public_text_origin(origin, profile, plan)
        if rebuilt.to_dict() != bridge.to_dict() or rebuilt._origin_json != bridge._origin_json:
            raise SchoolFitBridgeError("school-fit bridge no longer replays")
        return bridge
    if tuple(table.to_dict() for table in bridge.tables) != tuple(origin.get("tables", ())):
        raise SchoolFitBridgeError("school-fit bridge tables were mutated")
    indexes = origin.get("adapter_row_indexes")
    if not isinstance(indexes, list) or len(indexes) != len(bridge.tables):
        raise SchoolFitBridgeError("school-fit bridge row origins are invalid")
    rows = []
    for table, index in zip(bridge.tables, indexes):
        if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < len(table.rows):
            raise SchoolFitBridgeError("school-fit bridge row origin is invalid")
        rows.append(table.rows[index])
    rebuilt = bridge_school_fit_evidence(
        profile=profile,
        plan=plan,
        task=bridge.task,
        tables=bridge.tables,
        adapter_rows=tuple(rows),
        candidates=bridge.candidates,
    )
    if rebuilt.to_dict() != bridge.to_dict() or rebuilt._origin_json != bridge._origin_json:
        raise SchoolFitBridgeError("school-fit bridge no longer replays")
    return bridge


def _replay_persisted_school_fit_evidence_fact(
    fact: Mapping[str, Any],
    context: Mapping[str, Any],
    profile: PlanningProfile,
    plan: QueryPlan,
) -> SchoolFitEvidenceBridge:
    """Rebuild one persisted school-fit fact from its factory origin receipt."""

    if not isinstance(fact, Mapping) or not isinstance(context, Mapping):
        raise TypeError("persisted school-fit fact and origin must be mappings")
    if set(context) != {"kind", "fact_id", "bridge_digest", "origin"}:
        raise SchoolFitBridgeError("persisted school-fit factory origin shape is invalid")
    if context.get("kind") != _PERSISTED_ORIGIN_KIND:
        raise SchoolFitBridgeError("persisted school-fit factory origin kind is invalid")
    if context.get("fact_id") != fact.get("fact_id"):
        raise SchoolFitBridgeError("persisted school-fit factory origin is detached")
    bridge_digest = context.get("bridge_digest")
    if not isinstance(bridge_digest, str) or _DIGEST.fullmatch(bridge_digest) is None:
        raise SchoolFitBridgeError("persisted school-fit bridge digest is invalid")
    origin = context.get("origin")
    if isinstance(origin, Mapping) and origin.get("adapter_kind") == "public-text":
        rebuilt = _replay_school_fit_public_text_origin(origin, profile, plan)
        if (
            rebuilt.fact.to_dict() != dict(fact)
            or rebuilt.bridge_digest != bridge_digest
            or json.loads(rebuilt._origin_json) != dict(origin)
        ):
            raise SchoolFitBridgeError(
                "persisted school-fit fact does not match its factory origin"
            )
        return rebuilt
    expected_origin_fields = {
        "schema_version",
        "profile_digest",
        "query_plan_digest",
        "task",
        "tables",
        "adapter_row_indexes",
        "sources",
    }
    if not isinstance(origin, Mapping) or set(origin) != expected_origin_fields:
        raise SchoolFitBridgeError("persisted school-fit factory origin is invalid")
    if origin.get("schema_version") != "1.0":
        raise SchoolFitBridgeError("persisted school-fit factory origin version is invalid")
    try:
        task_raw = origin["task"]
        if not isinstance(task_raw, Mapping):
            raise TypeError
        task = QueryTask(**dict(task_raw))
        if task.to_dict() != dict(task_raw):
            raise ValueError

        table_values = origin["tables"]
        if isinstance(table_values, (str, bytes, bytearray)):
            raise TypeError
        tables: list[ExtractedTable] = []
        for table_raw in table_values:
            if not isinstance(table_raw, Mapping):
                raise TypeError
            row_values = table_raw.get("rows")
            coverage_raw = table_raw.get("coverage")
            if (
                isinstance(row_values, (str, bytes, bytearray))
                or not isinstance(coverage_raw, Mapping)
            ):
                raise TypeError
            rows = tuple(
                ExtractedRow(
                    values=row_raw["values"],
                    cell_status=row_raw["cell_status"],
                    location=row_raw["location"],
                    confidence=row_raw["confidence"],
                    warnings=tuple(row_raw["warnings"]),
                )
                for row_raw in row_values
            )
            table = ExtractedTable(
                table_id=table_raw["table_id"],
                caption=table_raw["caption"],
                sheet=table_raw["sheet"],
                rows=rows,
                coverage=ExtractedCoverage(**dict(coverage_raw)),
                warnings=tuple(table_raw["warnings"]),
                extraction_method=table_raw["extraction_method"],
            )
            if table.to_dict() != dict(table_raw):
                raise ValueError
            tables.append(table)

        source_values = origin["sources"]
        if isinstance(source_values, (str, bytes, bytearray)):
            raise TypeError
        candidates = tuple(
            SourceCandidate(
                source_id=source_raw["source_id"],
                url=source_raw["url"],
                publisher=source_raw["publisher"],
                tier=SourceTier(source_raw["tier"]),
                published_at=source_raw["published_at"],
                retrieved_at=source_raw["retrieved_at"],
                content_hash=source_raw["content_hash"],
                citation_root=source_raw["citation_root"],
                summary=source_raw["summary"],
            )
            for source_raw in source_values
        )
        if [item.to_dict() for item in candidates] != list(source_values):
            raise ValueError

        indexes = origin["adapter_row_indexes"]
        if isinstance(indexes, (str, bytes, bytearray)):
            raise TypeError
        indexes = tuple(indexes)
        if len(indexes) != len(tables):
            raise ValueError
        rows = tuple(
            table.rows[index]
            for table, index in zip(tables, indexes)
            if isinstance(index, int)
            and not isinstance(index, bool)
            and 0 <= index < len(table.rows)
        )
        if len(rows) != len(tables):
            raise ValueError
    except (KeyError, TypeError, ValueError, IndexError):
        raise SchoolFitBridgeError(
            "persisted school-fit factory origin cannot be reconstructed"
        ) from None

    rebuilt = bridge_school_fit_evidence(
        profile=profile,
        plan=plan,
        task=task,
        tables=tuple(tables),
        adapter_rows=rows,
        candidates=candidates,
    )
    if (
        rebuilt.fact.to_dict() != dict(fact)
        or rebuilt.bridge_digest != bridge_digest
        or json.loads(rebuilt._origin_json) != dict(origin)
    ):
        raise SchoolFitBridgeError(
            "persisted school-fit fact does not match its factory origin"
        )
    return rebuilt


def _fact_record(
    raw: Mapping[str, Any], profile: PlanningProfile, plan: QueryPlan
) -> dict[str, Any] | None:
    expected = {
        "fact_id",
        "field",
        "value",
        "unit",
        "status",
        "source_ids",
        "method",
        "notes",
    }
    if not isinstance(raw, Mapping) or set(raw) != expected:
        raise SchoolFitBridgeError("school-fit fact shape is invalid")
    match = _FIELD.fullmatch(str(raw["field"]))
    if match is None:
        raise SchoolFitBridgeError("school-fit fact field is invalid")
    kind, year_text, key_hex = match.groups()
    year = int(year_text)
    notes = raw["notes"]
    if not isinstance(notes, str) or not notes.startswith("query_task:"):
        raise SchoolFitBridgeError("school-fit fact lacks its task binding")
    task_id = notes.removeprefix("query_task:")
    tasks = tuple(item for item in plan.tasks if item.task_id == task_id)
    if len(tasks) != 1 or (tasks[0].kind, tasks[0].year) != (kind, year):
        raise SchoolFitBridgeError("school-fit fact task binding is invalid")
    if raw["unit"] is not None:
        raise SchoolFitBridgeError("school-fit fact unit must be null")
    try:
        status = EvidenceStatus(raw["status"])
    except (TypeError, ValueError):
        raise SchoolFitBridgeError("school-fit fact status is invalid") from None
    source_ids = raw["source_ids"]
    if (
        not isinstance(source_ids, list)
        or not source_ids
        or source_ids != sorted(set(source_ids))
        or any(not isinstance(item, str) or _SAFE_ID.fullmatch(item) is None for item in source_ids)
    ):
        raise SchoolFitBridgeError("school-fit fact source IDs are invalid")
    if status not in _ACCEPTED:
        if raw["value"] is not None:
            raise SchoolFitBridgeError("unusable school-fit facts cannot carry metadata")
        return {
            "kind": kind,
            "year": year,
            "key_digest": f"sha256:{key_hex}",
            "status": status,
            "source_ids": tuple(source_ids),
            "value": None,
        }
    value = raw["value"]
    if not isinstance(value, Mapping):
        raise SchoolFitBridgeError("usable school-fit fact lacks metadata")
    expected_fields = {
        "province_policy": _PROVINCE_VALUE_FIELDS,
        "enrollment_plan": _ENROLLMENT_VALUE_FIELDS,
        "admission_charter": _CHARTER_VALUE_FIELDS,
        "tuition_fee": _TUITION_VALUE_FIELDS,
        "subject_requirement": _SUBJECT_VALUE_FIELDS,
    }[kind]
    if set(value) != set(expected_fields):
        raise SchoolFitBridgeError("school-fit metadata fields are invalid")
    if (
        value["schema_version"] != "1.0"
        or value["profile_digest"] != profile.digest
        or value["query_plan_digest"] != _digest(plan.to_dict())
        or value["task_id"] != task_id
        or value["kind"] != kind
        or value["province"] != profile.province
        or value["year"] != year
        or value["subject_group"] != plan.subject_group
    ):
        raise SchoolFitBridgeError("school-fit metadata context is invalid")
    if kind == "province_policy":
        key = {"province": value["province"], "year": str(value["year"])}
    elif kind == "admission_charter":
        key = {
            "school_code": value["school_code"],
            "school_name": value["school_name"],
        }
    else:
        key = {
            "school_code": value["school_code"],
            "school_name": value["school_name"],
            "program_group": value["program_group"],
        }
    if _digest(key) != f"sha256:{key_hex}":
        raise SchoolFitBridgeError("school-fit fact key binding is invalid")
    if kind == "tuition_fee":
        policy = value["affordability_policy"]
        if policy != _policy():
            raise SchoolFitBridgeError("school-fit affordability policy is invalid")
        amount = _positive_integer(value["annual_fee_amount"], "annual_fee_amount")
        currency = _text(value["fee_currency"], "fee_currency")
        period = _text(value["fee_period"], "fee_period")
        if value["affordable_for"] != list(_affordable_for(amount, currency, period)):
            raise SchoolFitBridgeError("school-fit affordability derivation is invalid")
    return {
        "kind": kind,
        "year": year,
        "key_digest": f"sha256:{key_hex}",
        "status": status,
        "source_ids": tuple(source_ids),
        "value": dict(value),
    }


def _select_annual_record(
    records: Iterable[Mapping[str, Any]],
    *,
    research_year: int,
) -> dict[str, Any] | None:
    """Select one decisive year without letting other years contaminate it."""

    candidates = tuple(records)
    if not candidates:
        return None
    newest_attempt: dict[str, Any] | None = None
    for year in sorted({int(item["year"]) for item in candidates}, reverse=True):
        same_year = tuple(item for item in candidates if item["year"] == year)
        year_sources = tuple(
            sorted(
                {
                    source_id
                    for item in same_year
                    for source_id in item["source_ids"]
                }
            )
        )
        if any(item["status"] is EvidenceStatus.CONFLICT for item in same_year):
            return {
                "year": year,
                "status": EvidenceStatus.CONFLICT,
                "source_ids": year_sources,
                "value": None,
                "conflict": True,
                "current_attempt": newest_attempt,
            }
        accepted = tuple(
            item
            for item in same_year
            if item["status"] in _ACCEPTED and item["value"] is not None
        )
        if not accepted:
            attempt_status = next(
                (
                    status
                    for status in (
                        EvidenceStatus.PARTIAL,
                        EvidenceStatus.MASKED,
                        EvidenceStatus.INFERRED,
                        EvidenceStatus.MISSING,
                    )
                    if any(item["status"] is status for item in same_year)
                ),
                EvidenceStatus.MISSING,
            )
            if newest_attempt is None:
                newest_attempt = {
                    "year": year,
                    "status": attempt_status,
                    "source_ids": year_sources,
                }
            continue
        canonical_values = {_canonical_json(item["value"]) for item in accepted}
        if len(canonical_values) != 1:
            return {
                "year": year,
                "status": EvidenceStatus.CONFLICT,
                "source_ids": tuple(
                    sorted(
                        {
                            source_id
                            for item in accepted
                            for source_id in item["source_ids"]
                        }
                    )
                ),
                "value": None,
                "conflict": True,
                "current_attempt": newest_attempt,
            }
        selected_status = next(
            status
            for status in (
                EvidenceStatus.REFERENCE,
                EvidenceStatus.CORROBORATED,
                EvidenceStatus.OFFICIAL,
            )
            if any(item["status"] is status for item in accepted)
        )
        if year < research_year:
            selected_status = EvidenceStatus.REFERENCE
        return {
            "year": year,
            "status": selected_status,
            "source_ids": tuple(
                sorted(
                    {
                        source_id
                        for item in accepted
                        for source_id in item["source_ids"]
                    }
                )
            ),
            "value": accepted[0]["value"],
            "conflict": False,
            "current_attempt": newest_attempt,
        }
    if newest_attempt is None:
        return None
    return {
        **newest_attempt,
        "value": None,
        "conflict": False,
        "current_attempt": None,
    }


def merge_school_fit_metadata(
    admission_rows: tuple[ValidatedAdmissionRow, ...],
    facts: Iterable[Mapping[str, Any]],
    *,
    profile: PlanningProfile,
    plan: QueryPlan,
) -> tuple[ValidatedAdmissionRow, ...]:
    """Merge the newest conflict-free metadata by exact school/program key."""

    _profile, canonical_plan, _task, _plan_digest = _plan_context(
        profile,
        plan,
        next(item for item in plan.tasks if item.kind == "province_policy"),
    )
    if not isinstance(admission_rows, tuple) or not all(
        isinstance(row, ValidatedAdmissionRow) for row in admission_rows
    ):
        raise TypeError("admission_rows must contain ValidatedAdmissionRow records")
    if isinstance(facts, (str, bytes, bytearray)):
        raise TypeError("facts must be an iterable of mappings")
    records = tuple(_fact_record(item, profile, canonical_plan) for item in facts)
    by_key: dict[tuple[str, str], list[dict[str, Any]]] = {}
    province_records: list[dict[str, Any]] = []
    for record in records:
        assert record is not None
        if record["kind"] == "province_policy":
            province_records.append(record)
            continue
        by_key.setdefault((record["kind"], record["key_digest"]), []).append(record)

    selected_province = _select_annual_record(
        province_records,
        research_year=canonical_plan.research_year,
    )

    merged: list[ValidatedAdmissionRow] = []
    for admission in admission_rows:
        row = admission.to_dict()
        base_row_hash = admission_row_hash(admission)
        program_key_digest = _digest(
            {
                "school_code": row["school_code"],
                "school_name": row["school_name"],
                "program_group": row["program_group"],
            }
        )
        school_key_digest = _digest(
            {
                "school_code": row["school_code"],
                "school_name": row["school_name"],
            }
        )
        source_ids: set[str] = set()
        kind_source_ids: dict[str, set[str]] = {
            "enrollment_plan": set(),
            "subject_requirement": set(),
            "admission_charter": set(),
            "tuition_fee": set(),
        }
        kind_statuses: dict[str, EvidenceStatus] = {}
        kind_years: dict[str, int] = {}
        kind_current_attempts: dict[str, Mapping[str, Any]] = {}
        conflicts: set[str] = set()
        statuses: set[str] = set()
        for kind in (
            "enrollment_plan",
            "subject_requirement",
            "admission_charter",
            "tuition_fee",
        ):
            join_digest = (
                school_key_digest
                if kind == "admission_charter"
                else program_key_digest
            )
            selection = _select_annual_record(
                by_key.get((kind, join_digest), ()),
                research_year=canonical_plan.research_year,
            )
            if selection is None:
                continue
            selected_sources = tuple(selection["source_ids"])
            source_ids.update(selected_sources)
            kind_source_ids[kind].update(selected_sources)
            kind_statuses[kind] = selection["status"]
            kind_years[kind] = selection["year"]
            statuses.add(selection["status"].value)
            current_attempt = selection.get("current_attempt")
            if isinstance(current_attempt, Mapping):
                kind_current_attempts[kind] = current_attempt
                source_ids.update(current_attempt["source_ids"])
                statuses.add(current_attempt["status"].value)
            if selection["conflict"]:
                conflicts.add(kind)
                continue
            value = selection["value"]
            if value is None:
                continue
            if kind == "enrollment_plan":
                row.update(
                    {
                        "majors_in_group": tuple(value["majors_in_group"]),
                        "school_province": value["school_province"],
                        "city_location": value["city_location"],
                        "institution_type": value["institution_type"],
                    }
                )
            elif kind == "subject_requirement":
                row.update(
                    {
                        "required_secondary_subjects": tuple(
                            value["required_secondary_subjects"]
                        ),
                        "secondary_subject_rule": value["secondary_subject_rule"],
                        "subject_special_conditions": value["special_conditions"],
                    }
                )
            elif kind == "admission_charter":
                row.update(
                    {
                        "charter_admission_rules": value["admission_rules"],
                        "charter_adjustment_rules": value["adjustment_rules"],
                        "charter_adjustment_required": value[
                            "adjustment_required"
                        ],
                    }
                )
                for value_field, row_field in (
                    ("health_restrictions", "charter_health_restrictions"),
                    ("language_restrictions", "charter_language_restrictions"),
                    (
                        "single_subject_restrictions",
                        "charter_single_subject_restrictions",
                    ),
                    ("special_conditions", "charter_special_conditions"),
                ):
                    if value[value_field] is not None:
                        row[row_field] = value[value_field]
                if value["unverified_fields"]:
                    row["charter_unverified_fields"] = tuple(
                        value["unverified_fields"]
                    )
            else:
                row.update(
                    {
                        "tuition_majors": tuple(value["majors"]),
                        "tuition_annual_fee_amount": value[
                            "annual_fee_amount"
                        ],
                        "tuition_fee_currency": value["fee_currency"],
                        "tuition_fee_period": value["fee_period"],
                        "tuition_affordable_for": tuple(
                            value["affordable_for"]
                        ),
                        "tuition_affordability_policy_id": value[
                            "affordability_policy"
                        ]["policy_id"],
                        "tuition_affordability_policy_version": value[
                            "affordability_policy"
                        ]["version"],
                        "tuition_affordability_policy_digest": value[
                            "affordability_policy"
                        ]["policy_digest"],
                    }
                )
                for value_field, row_field in (
                    ("accommodation_fee", "tuition_accommodation_fee"),
                    ("other_required_fees", "tuition_other_required_fees"),
                    ("financial_aid", "tuition_financial_aid"),
                ):
                    if value[value_field] is not None:
                        row[row_field] = value[value_field]
                if value["unverified_fields"]:
                    row["tuition_unverified_fields"] = tuple(
                        value["unverified_fields"]
                    )
        if selected_province is not None and selected_province["source_ids"]:
            province_sources = set(selected_province["source_ids"])
            source_ids.update(province_sources)
            row["school_fit_province_policy_source_ids"] = tuple(
                sorted(province_sources)
            )
        if selected_province is not None:
            province_status = selected_province["status"]
            row["school_fit_province_policy_status"] = province_status.value
            row["school_fit_province_policy_year"] = selected_province["year"]
            statuses.add(province_status.value)
            province_current = selected_province.get("current_attempt")
            if isinstance(province_current, Mapping):
                row["school_fit_province_policy_current_status"] = (
                    province_current["status"].value
                )
                row["school_fit_province_policy_current_year"] = (
                    province_current["year"]
                )
                row["school_fit_province_policy_current_source_ids"] = tuple(
                    province_current["source_ids"]
                )
                source_ids.update(province_current["source_ids"])
                statuses.add(province_current["status"].value)
        if selected_province is not None and selected_province["conflict"]:
            conflicts.add("province_policy")
        elif selected_province is not None and selected_province["value"] is not None:
            province_value = selected_province["value"]
            row.update(
                {
                    "province_policy_exam_mode": province_value["exam_mode"],
                    "province_policy_subject_structure": province_value[
                        "subject_structure"
                    ],
                    "province_policy_batch_structure": province_value[
                        "batch_structure"
                    ],
                    "province_policy_effective_date": province_value[
                        "effective_date"
                    ],
                }
            )
        if source_ids:
            row["admission_evidence_row_hash"] = base_row_hash
            row["school_fit_source_ids"] = tuple(sorted(source_ids))
        if kind_source_ids["enrollment_plan"]:
            row["school_fit_enrollment_source_ids"] = tuple(
                sorted(kind_source_ids["enrollment_plan"])
            )
        if kind_source_ids["subject_requirement"]:
            row["school_fit_subject_source_ids"] = tuple(
                sorted(kind_source_ids["subject_requirement"])
            )
        if kind_source_ids["admission_charter"]:
            row["school_fit_charter_source_ids"] = tuple(
                sorted(kind_source_ids["admission_charter"])
            )
        if kind_source_ids["tuition_fee"]:
            row["school_fit_tuition_source_ids"] = tuple(
                sorted(kind_source_ids["tuition_fee"])
            )
        if "enrollment_plan" in kind_statuses:
            row["school_fit_enrollment_status"] = kind_statuses[
                "enrollment_plan"
            ].value
        if "subject_requirement" in kind_statuses:
            row["school_fit_subject_status"] = kind_statuses[
                "subject_requirement"
            ].value
        if "admission_charter" in kind_statuses:
            row["school_fit_charter_status"] = kind_statuses[
                "admission_charter"
            ].value
        if "tuition_fee" in kind_statuses:
            row["school_fit_tuition_status"] = kind_statuses[
                "tuition_fee"
            ].value
        year_fields = {
            "enrollment_plan": "school_fit_enrollment_year",
            "subject_requirement": "school_fit_subject_year",
            "admission_charter": "school_fit_charter_year",
            "tuition_fee": "school_fit_tuition_year",
        }
        for kind, year in kind_years.items():
            row[year_fields[kind]] = year
        current_status_fields = {
            "enrollment_plan": "school_fit_enrollment_current_status",
            "subject_requirement": "school_fit_subject_current_status",
            "admission_charter": "school_fit_charter_current_status",
            "tuition_fee": "school_fit_tuition_current_status",
        }
        current_year_fields = {
            "enrollment_plan": "school_fit_enrollment_current_year",
            "subject_requirement": "school_fit_subject_current_year",
            "admission_charter": "school_fit_charter_current_year",
            "tuition_fee": "school_fit_tuition_current_year",
        }
        current_source_fields = {
            "enrollment_plan": "school_fit_enrollment_current_source_ids",
            "subject_requirement": "school_fit_subject_current_source_ids",
            "admission_charter": "school_fit_charter_current_source_ids",
            "tuition_fee": "school_fit_tuition_current_source_ids",
        }
        for kind, attempt in kind_current_attempts.items():
            row[current_status_fields[kind]] = attempt["status"].value
            row[current_year_fields[kind]] = attempt["year"]
            row[current_source_fields[kind]] = tuple(attempt["source_ids"])
        if statuses:
            row["school_fit_statuses"] = tuple(sorted(statuses))
        if conflicts:
            row["school_fit_conflict_kinds"] = tuple(sorted(conflicts))
        merged.append(ValidatedAdmissionRow.from_mapping(row))
    return tuple(merged)


def validate_school_fit_enriched_admission_row(
    row: ValidatedAdmissionRow,
) -> tuple[ValidatedAdmissionRow, str]:
    """Recover and verify the admission row authenticated before enrichment."""

    if not isinstance(row, ValidatedAdmissionRow):
        raise TypeError("row must be a ValidatedAdmissionRow")
    payload = row.to_dict()
    expected_hash = payload.get("admission_evidence_row_hash")
    if not isinstance(expected_hash, str) or _DIGEST.fullmatch(expected_hash) is None:
        raise SchoolFitBridgeError(
            "enriched admission row lacks its authenticated base-row hash"
        )
    base_payload = {
        name: value
        for name, value in payload.items()
        if name not in _MERGED_ADMISSION_FIELDS
    }
    base = ValidatedAdmissionRow.from_mapping(base_payload)
    if admission_row_hash(base) != expected_hash:
        raise SchoolFitBridgeError(
            "enriched admission row does not match its authenticated base row"
        )
    return base, expected_hash


__all__ = [
    "AFFORDABILITY_POLICY_ID",
    "AFFORDABILITY_POLICY_VERSION",
    "SchoolFitBridgeError",
    "SchoolFitEvidenceBridge",
    "bridge_school_fit_evidence",
    "bridge_school_fit_public_text",
    "merge_school_fit_metadata",
    "validate_school_fit_enriched_admission_row",
    "validate_school_fit_evidence_bridge",
]
