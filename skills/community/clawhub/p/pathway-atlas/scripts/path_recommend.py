# -*- coding: utf-8 -*-
"""Evidence- and policy-backed deterministic pathway evaluation.

Callers provide an explicit profile, accepted policy records, and optionally a
documented rank-adjustment model. Without that model no numeric target rank is
produced.
"""
import math
import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
from typing import Any

if __package__:
    from .contracts import EvidenceStatus
    from .decision_policy import DecisionPolicySnapshot, DecisionReason
else:
    from contracts import EvidenceStatus
    from decision_policy import DecisionPolicySnapshot, DecisionReason


_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_SHA256_ID = re.compile(r"^sha256:[0-9a-f]{64}$")
_SUBJECT_MODES = frozenset({"3+1+2", "3+3"})
PATHWAY_TYPES = (
    "strong_foundation",
    "comprehensive_evaluation",
    "national_special",
    "local_special",
    "university_special",
    "public_funded_teacher",
    "excellent_teacher",
    "directed_medical",
    "military",
    "police_judicial_fire",
    "maritime_aviation",
    "hong_kong_macao",
    "sino_foreign",
    "arts_sports",
    "other",
)
_LEGACY_PATHWAY_TYPES = frozenset({"special_program", "public_funded_or_directed"})
_PATHWAY_TYPES = frozenset(PATHWAY_TYPES) | _LEGACY_PATHWAY_TYPES
_EXACT_EVIDENCE_MINIMUMS = {
    EvidenceStatus.OFFICIAL: 1,
    EvidenceStatus.CORROBORATED: 2,
    EvidenceStatus.REFERENCE: 3,
}
_MODEL_METHODS = frozenset({"documented_rank_delta"})
_PHONE = re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")
_LANDLINE = re.compile(r"(?<!\d)0(?:10|\d{3})\d{7,8}(?!\d)")
_PHONE_SEPARATORS = re.compile(r"[\s.\-·‐‑–—_]+")
_IDENTITY = re.compile(r"(?<!\d)\d{17}[0-9Xx](?!\d)")
_EMAIL = re.compile(r"(?i)(?<![\w.-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w.-])")
_URL_OR_LOCAL_PATH = re.compile(
    r"(?i)(?:"
    r"https?://|file://|www\.[a-z0-9-]+(?:\.[a-z0-9-]+)+(?:[\\/]|\b)|"
    r"\$(?:home|userprofile|appdata|codex_home)[\\/]|"
    r"%(?:home|userprofile|appdata|codex_home)%[\\/]|"
    r"(?:^|[\s(])\.\.?\\(?:[^\\\s]+\\)*[^\\\s]+|"
    r"[a-z]:[\\/]|\\\\[^\\\s]+[\\/]|//[^/\s]+/|~/|"
    r"/(?:home|users|tmp|var|etc|opt|srv|mnt|root)(?:/|$)|"
    r"/(?!/)(?:[a-z0-9._~-]+/)+[a-z0-9._~-]+|(?:^|\s)/[^/\s]+"
    r")"
)
_SCHEMELESS_DOMAIN = re.compile(
    r"(?i)(?<![\w@.-])(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"
    r"[a-z]{2,}(?:[/:?#][^\s]*)?"
)
_PRIVATE_OUTPUT_MARKERS = (
    "姓名", "studentname", "wechat", "weixin", "微信", "手机号",
    "联系电话", "电话", "就读学校", "currentschool", "studentschool",
    "班级", "住址",
)
_PRIVATE_LABEL = re.compile(
    r"(?i)(?<!\w)(?:student\s+name|name|wechat|weixin|phone|telephone|"
    r"current\s+school|student\s+school|address|api[\s_-]*key|secret|token|"
    r"private[\s_-]*key)\s*[:=]"
)
_WECHAT_ID = re.compile(r"(?i)(?<![a-z0-9])wxid[_-][a-z0-9_-]+")
_STRUCTURED_SECRET = re.compile(
    r"(?i)(?<![a-z0-9])(?:"
    r"gh[pousr]_[a-z0-9]{20,}|github_pat_[a-z0-9_]{20,}|"
    r"(?:akia|asia)[a-z0-9]{16}|"
    r"sk-(?:proj-)?[a-z0-9_-]{20,}|sk_(?:live|test)_[a-z0-9]{16,}|"
    r"glpat-[a-z0-9_-]{20,}|xox[baprs]-[a-z0-9-]{20,}|"
    r"aiza[a-z0-9_-]{30,}"
    r")"
)
_JWT_SECRET = re.compile(
    r"(?i)(?<![a-z0-9_-])eyj[a-z0-9_-]{8,}\.eyj[a-z0-9_-]{8,}\."
    r"[a-z0-9_-]{8,}(?![a-z0-9_-])"
)
_CHINESE_OUTPUT_CLAIMS = frozenset(
    {
        "保录",
        "保证录取",
        "包录",
        "确保录取",
        "录取概率",
        "录取几率",
        "录取成功率",
        "成功率",
        "百分比承诺",
        "投资回报",
        "投资收益",
        "收益率",
        "回报率",
        "预计收益",
        "预计回报",
        "承诺回报",
    }
)
_PROMISE_ERROR = "output text contains unsupported promise language"
_SOURCE_ID_PROMISE_ERROR = "source ID contains unsupported claim language"
_ENGLISH_CLAIM_PHRASES = (
    ("admission", "guarantee"),
    ("guarantee", "admission"),
    ("guaranteed", "admission"),
    ("admission", "guaranteed"),
    ("admission", "is", "guarantee"),
    ("admission", "is", "guaranteed"),
    ("admission", "rate"),
    ("rate", "admission"),
    ("rate", "of", "admission"),
    ("probability",),
    ("admission", "probability"),
    ("probability", "admission"),
    ("probability", "of", "admission"),
    ("admission", "chance"),
    ("chance", "admission"),
    ("chance", "of", "admission"),
    ("admission", "likelihood"),
    ("likelihood", "admission"),
    ("likelihood", "of", "admission"),
    ("success", "rate"),
    ("return", "on", "investment"),
    ("investment", "return"),
    ("r", "o", "i"),
)
_ENGLISH_CLAIM_COMPACT = frozenset(
    "".join(phrase) for phrase in _ENGLISH_CLAIM_PHRASES
)
_ROI_CLAIM_TOKENS = next(
    phrase for phrase in _ENGLISH_CLAIM_PHRASES if "".join(phrase) == "roi"
)
_ENGLISH_OUTPUT_COMPACT_CLAIMS = frozenset(
    claim for claim in _ENGLISH_CLAIM_COMPACT if claim != "roi"
)
_ROI_PATTERN_BODY = r"\s*".join(re.escape(token) for token in _ROI_CLAIM_TOKENS)
_ROI_OUTPUT_PATTERN = re.compile(
    rf"(?<![a-z0-9]){_ROI_PATTERN_BODY}(?=[0-9%]|[^a-z0-9]|$)"
)
_UNICODE_PERCENT_SIGNS = frozenset({"%", "\u066a", "\ufe6a", "\uff05"})
_CHINESE_NUMBER = r"[0-9零〇一二三四五六七八九十百千万两]+(?:\.[0-9]+)?"
_PERCENT_OF_FORM = rf"百分之{_CHINESE_NUMBER}"
_PERCENT_SYMBOL_FORM = r"[0-9]+(?:\.[0-9]+)?%"
_CHENG_FORM = rf"{_CHINESE_NUMBER}成"
_RATE_FORM = rf"(?:{_PERCENT_OF_FORM}|{_PERCENT_SYMBOL_FORM}|{_CHENG_FORM})"
_NUMERIC_ADMISSION_PATTERNS = (
    re.compile(rf"(?:预计|预估|预测)?录取(?:is)?{_RATE_FORM}"),
    re.compile(rf"{_RATE_FORM}录取(?:把握|概率|几率|可能性)?"),
    re.compile(rf"admission(?:is)?{_RATE_FORM}"),
    re.compile(rf"{_RATE_FORM}admission(?:rate|probability|chance|likelihood)?"),
)
_CHINESE_ADMISSION_RATE_TERMS = (
    "录取率",
    "录取比例",
    "录取概率",
    "录取几率",
    "录取可能性",
    "录取把握",
)
_CHINESE_REVERSE_ADMISSION_RATE_TERMS = (
    "比例录取",
    "概率录取",
    "几率录取",
    "可能性录取",
    "把握录取",
)
def _json_safe(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (tuple, list)):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise TypeError("JSON object keys must be strings")
        return {key: _json_safe(item) for key, item in value.items()}
    if is_dataclass(value) and hasattr(value, "to_dict"):
        return _json_safe(value.to_dict())
    raise TypeError(f"Value of type {type(value).__name__} is not JSON serializable")


class _Serializable:
    def to_dict(self) -> dict[str, Any]:
        return {
            item.name: _json_safe(getattr(self, item.name))
            for item in fields(self)
        }


def _strict_positive_int(value: Any, name: str, *, minimum: int = 1) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def _strict_int(value: Any, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    return value


def _schema_integer(value: Any, name: str) -> int:
    """Normalize a Draft 2020-12 mathematical integer to Python ``int``."""

    if isinstance(value, bool):
        raise TypeError(f"{name} must be a JSON Schema integer")
    if isinstance(value, int):
        return value
    if isinstance(value, float) and math.isfinite(value) and value.is_integer():
        return int(value)
    raise TypeError(f"{name} must be a JSON Schema integer")


def _text(value: Any, name: str, *, optional: bool = False) -> str | None:
    if value is None and optional:
        return None
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{name} must not be blank")
    if normalized != value:
        raise ValueError(f"{name} must not have surrounding whitespace")
    return normalized


def _normalize_claim_text(value: str) -> str:
    """Canonicalize claim text without merging distinct semantic tokens."""

    characters: list[str] = []
    for character in unicodedata.normalize("NFKC", value).casefold():
        try:
            characters.append(str(unicodedata.decimal(character)))
            continue
        except (TypeError, ValueError):
            pass
        if character in _UNICODE_PERCENT_SIGNS:
            characters.append("%")
        elif character.isalnum():
            characters.append(character)
        else:
            characters.append(" ")
    return " ".join("".join(characters).split())


def _compact_claim_text(normalized: str) -> str:
    return "".join(
        character for character in normalized
        if character.isalnum() or character == "%"
    )


def _contains_admission_rate_claim(compact: str) -> bool:
    if any(term in compact for term in _CHINESE_ADMISSION_RATE_TERMS):
        return True
    if any(term in compact for term in _CHINESE_REVERSE_ADMISSION_RATE_TERMS):
        return True
    return any(pattern.search(compact) for pattern in _NUMERIC_ADMISSION_PATTERNS)


def _validate_output_text(value: str) -> None:
    normalized = _normalize_claim_text(value)
    compact = _compact_claim_text(normalized)
    if (
        any(token in compact for token in _CHINESE_OUTPUT_CLAIMS)
        or any(token in compact for token in _ENGLISH_OUTPUT_COMPACT_CLAIMS)
        or _contains_admission_rate_claim(compact)
        or _ROI_OUTPUT_PATTERN.search(normalized) is not None
    ):
        raise ValueError(_PROMISE_ERROR)


def validate_public_output_text(value: str) -> None:
    """Reject PII, secrets, URLs, and local paths from persisted output text."""

    normalized = "".join(
        character
        for character in unicodedata.normalize("NFKC", value).casefold()
        if unicodedata.category(character) != "Cf"
    )
    compact = re.sub(r"[\s_\-:：=]+", "", normalized)
    phone_view = _PHONE_SEPARATORS.sub("", normalized)
    if (
        _PHONE.search(phone_view)
        or _LANDLINE.search(phone_view)
        or _IDENTITY.search(normalized)
        or _EMAIL.search(normalized)
        or _URL_OR_LOCAL_PATH.search(normalized)
        or _SCHEMELESS_DOMAIN.search(normalized)
        or any(marker in compact for marker in _PRIVATE_OUTPUT_MARKERS)
        or _PRIVATE_LABEL.search(normalized)
        or _WECHAT_ID.search(normalized)
        or _STRUCTURED_SECRET.search(normalized)
        or _JWT_SECRET.search(normalized)
        or re.search(r"高三[（(]?\d+[)）]?班", compact)
    ):
        raise ValueError("output text contains private or non-public content")


def _validate_source_id_claim(value: str) -> None:
    segments = tuple(
        segment.casefold()
        for segment in re.split(r"[-._:]+", value)
        if segment
    )
    if any(segment in _ENGLISH_CLAIM_COMPACT for segment in segments):
        raise ValueError(_SOURCE_ID_PROMISE_ERROR)
    for phrase in _ENGLISH_CLAIM_PHRASES:
        width = len(phrase)
        if any(
            segments[index:index + width] == phrase
            for index in range(len(segments) - width + 1)
        ):
            raise ValueError(_SOURCE_ID_PROMISE_ERROR)


def _output_text(value: Any, name: str, *, optional: bool = False) -> str | None:
    normalized = _text(value, name, optional=optional)
    if normalized is not None:
        validate_public_output_text(normalized)
        _validate_output_text(normalized)
    return normalized


def _string_tuple(
    value: Any,
    name: str,
    *,
    allow_empty: bool = True,
    safe_ids: bool = False,
    sort: bool = False,
) -> tuple[str, ...]:
    if isinstance(value, (str, bytes, bytearray)):
        raise TypeError(f"{name} must be a collection of strings")
    try:
        items = tuple(value)
    except TypeError as error:
        raise TypeError(f"{name} must be a collection of strings") from error
    if not allow_empty and not items:
        raise ValueError(f"{name} must not be empty")
    normalized: list[str] = []
    for item in items:
        if not isinstance(item, str):
            raise TypeError(f"{name} must contain only strings")
        stripped = item.strip()
        if not stripped:
            raise ValueError(f"{name} must not contain blank strings")
        if stripped != item:
            raise ValueError(f"{name} must not contain surrounding whitespace")
        if safe_ids and _SAFE_ID.fullmatch(stripped) is None:
            raise ValueError(f"{name} must use the public safe-ID syntax")
        normalized.append(stripped)
    if len(normalized) != len(set(normalized)):
        raise ValueError(f"{name} must contain unique values")
    if sort:
        normalized.sort()
    return tuple(normalized)


def _output_string_tuple(
    value: Any, name: str, *, allow_empty: bool = True
) -> tuple[str, ...]:
    normalized = _string_tuple(value, name, allow_empty=allow_empty)
    for item in normalized:
        validate_public_output_text(item)
        _validate_output_text(item)
    return normalized


def _canonical_professional_options(value: Any) -> tuple[str, ...]:
    """Use the same major ordering for displayed values and their evidence."""

    return tuple(sorted(_output_string_tuple(value, "professional_options")))


def _source_id_tuple(value: Any, name: str) -> tuple[str, ...]:
    normalized = _string_tuple(
        value,
        name,
        allow_empty=False,
        safe_ids=True,
        sort=True,
    )
    for item in normalized:
        _validate_source_id_claim(item)
    return normalized


def _status(value: Any, name: str = "evidence_status") -> EvidenceStatus:
    if isinstance(value, EvidenceStatus):
        return value
    if isinstance(value, str):
        try:
            return EvidenceStatus(value)
        except ValueError as error:
            raise ValueError(f"{name} is not a supported evidence status") from error
    raise TypeError(f"{name} must be an EvidenceStatus or status string")


PATHWAY_POLICY_EVIDENCE_FIELDS = (
    "institution", "province", "subject_mode", "data_year",
    "eligibility_requirements", "grade_requirements", "subject_requirements",
    "award_requirements", "activity_requirements", "disqualifying_facts",
    "professional_options", "training_arrangements", "transition_rules",
    "outcomes", "service_employment_obligations", "penalty_exit_rules",
    "fees_and_subsidies", "timeline", "application_materials",
    "preparation_actions",
)
PATHWAY_DISPLAY_EVIDENCE_FIELDS = (
    "title", "institution", "investment_decision", "qualification_status",
    "status", "eligibility", "evidence_status", "source_ids",
    "professional_options",
    "training_arrangements", "transition_rules", "outcomes",
    "service_employment_obligations", "penalty_exit_rules",
    "fees_and_subsidies", "satisfied_conditions", "missing_constraints",
    "timeline", "preparation_actions", "decision_reasons",
    "year_basis", "calculation_basis",
)


class PathwayFieldEvidenceOrigin(str, Enum):
    """Authority boundary that produced one displayed-field trail."""

    POLICY_SOURCE = "policy_source"
    QUERY_CONTEXT = "query_context"
    DERIVED_DECISION = "derived_decision"
    LEGACY = "legacy"


def _canonical_field_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise TypeError("pathway field values must be finite JSON values")
        return value
    if isinstance(value, (tuple, list)):
        return [_canonical_field_value(item) for item in value]
    if isinstance(value, dict):
        if any(not isinstance(key, str) for key in value):
            raise TypeError("pathway field value mappings require string keys")
        return {
            key: _canonical_field_value(value[key])
            for key in sorted(value)
        }
    if is_dataclass(value) and hasattr(value, "to_dict"):
        return _canonical_field_value(value.to_dict())
    raise TypeError(
        f"pathway field value of type {type(value).__name__} is not canonical"
    )


def _pathway_digest(value: Any) -> str:
    encoded = json.dumps(
        _canonical_field_value(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _pathway_field_context_binding(value: Any) -> str:
    """Bind field trails to one authenticated projection/legacy decision context."""

    return _pathway_digest({"contract": "pathway-field-context-v1", "value": value})


@dataclass(frozen=True, init=False)
class PathwayFieldEvidence(_Serializable):
    """Factory-only, value-bound evidence/status/coverage trail."""

    field: str
    origin: PathwayFieldEvidenceOrigin
    value_digest: str
    context_binding: str
    origin_binding: str
    status: EvidenceStatus
    coverage: str
    source_ids: tuple[str, ...]
    locators: tuple[str, ...]
    extraction_methods: tuple[str, ...]
    evidence_method: str
    upstream_fields: tuple[str, ...]
    profile_fields: tuple[str, ...] = ()
    upstream_evidence_digests: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    digest: str = ""

    def __init__(self) -> None:
        raise TypeError("PathwayFieldEvidence is factory-only")

    @classmethod
    def _create(cls, **values: Any) -> "PathwayFieldEvidence":
        instance = object.__new__(cls)
        for name, value in values.items():
            object.__setattr__(instance, name, value)
        return instance


def _new_pathway_field_evidence(
    *,
    field: Any,
    origin: Any,
    value_digest: Any,
    context_binding: Any,
    origin_binding: Any,
    status: Any,
    coverage: Any,
    source_ids: Any,
    locators: Any,
    extraction_methods: Any,
    evidence_method: Any,
    upstream_fields: Any,
    profile_fields: Any = (),
    upstream_evidence_digests: Any = (),
    warnings: Any = (),
) -> PathwayFieldEvidence:
        field = _text(field, "field evidence field")
        assert field is not None
        if re.fullmatch(r"[a-z][a-z0-9_]{0,63}", field) is None:
            raise ValueError("field evidence field is invalid")
        try:
            normalized_origin = (
                origin
                if isinstance(origin, PathwayFieldEvidenceOrigin)
                else PathwayFieldEvidenceOrigin(origin)
            )
        except (TypeError, ValueError):
            raise ValueError("field evidence origin is invalid") from None
        for name, value in (
            ("value_digest", value_digest),
            ("context_binding", context_binding),
            ("origin_binding", origin_binding),
        ):
            if not isinstance(value, str) or _SHA256_ID.fullmatch(value) is None:
                raise ValueError(f"field evidence {name} is invalid")
        normalized_status = _status(status, "field evidence status")
        if coverage not in {"complete", "partial", "missing", "conflict"}:
            raise ValueError("field evidence coverage is invalid")
        if coverage == "complete" and normalized_status not in {
            EvidenceStatus.OFFICIAL,
            EvidenceStatus.CORROBORATED,
            EvidenceStatus.REFERENCE,
            EvidenceStatus.INFERRED,
        }:
            raise ValueError("complete field evidence has an unusable status")
        if coverage != "complete" and normalized_status in {
            EvidenceStatus.OFFICIAL,
            EvidenceStatus.CORROBORATED,
            EvidenceStatus.REFERENCE,
        }:
            raise ValueError("accepted field evidence must have complete coverage")
        if source_ids:
            normalized_sources = _source_id_tuple(
                source_ids, "field evidence sources"
            )
        elif (
            coverage == "missing"
            and normalized_status in {EvidenceStatus.MISSING, EvidenceStatus.MASKED}
        ) or (
            coverage == "complete"
            and normalized_status is EvidenceStatus.INFERRED
            and normalized_origin
            in {
                PathwayFieldEvidenceOrigin.QUERY_CONTEXT,
                PathwayFieldEvidenceOrigin.DERIVED_DECISION,
            }
        ):
            normalized_sources = ()
        else:
            raise ValueError("field evidence sources must not be empty")
        normalized_locators = _string_tuple(
            locators, "field evidence locators", allow_empty=False, sort=True
        )
        normalized_extraction_methods = _string_tuple(
            extraction_methods,
            "field evidence extraction methods",
            allow_empty=False,
            sort=True,
        )
        method = _text(evidence_method, "field evidence method")
        assert method is not None
        normalized_upstream_fields = _string_tuple(
            upstream_fields, "upstream_fields", allow_empty=False, sort=True
        )
        normalized_profile_fields = _string_tuple(
            profile_fields, "profile_fields", allow_empty=True, sort=True
        )
        normalized_upstream_digests = _string_tuple(
            upstream_evidence_digests,
            "upstream_evidence_digests",
            allow_empty=True,
            sort=True,
        )
        if any(_SHA256_ID.fullmatch(item) is None for item in normalized_upstream_digests):
            raise ValueError("upstream evidence digest is invalid")
        normalized_warnings = _string_tuple(warnings, "field evidence warnings")
        payload = {
            "field": field,
            "origin": normalized_origin.value,
            "value_digest": value_digest,
            "context_binding": context_binding,
            "origin_binding": origin_binding,
            "status": normalized_status.value,
            "coverage": coverage,
            "source_ids": list(normalized_sources),
            "locators": list(normalized_locators),
            "extraction_methods": list(normalized_extraction_methods),
            "evidence_method": method,
            "upstream_fields": list(normalized_upstream_fields),
            "profile_fields": list(normalized_profile_fields),
            "upstream_evidence_digests": list(normalized_upstream_digests),
            "warnings": list(normalized_warnings),
        }
        return PathwayFieldEvidence._create(
            field=field,
            origin=normalized_origin,
            value_digest=value_digest,
            context_binding=context_binding,
            origin_binding=origin_binding,
            status=normalized_status,
            coverage=coverage,
            source_ids=normalized_sources,
            locators=normalized_locators,
            extraction_methods=normalized_extraction_methods,
            evidence_method=method,
            upstream_fields=normalized_upstream_fields,
            profile_fields=normalized_profile_fields,
            upstream_evidence_digests=normalized_upstream_digests,
            warnings=normalized_warnings,
            digest=_pathway_digest(
                {"contract": "pathway-field-evidence-v2", "record": payload}
            ),
        )


def _create_pathway_field_evidence(
    *,
    field: str,
    value: Any,
    origin: PathwayFieldEvidenceOrigin,
    context_binding: str,
    origin_payload: Any,
    status: EvidenceStatus,
    coverage: str,
    source_ids: tuple[str, ...],
    locators: tuple[str, ...],
    extraction_methods: tuple[str, ...],
    evidence_method: str,
    upstream_fields: tuple[str, ...],
    profile_fields: tuple[str, ...] = (),
    upstream_evidence: tuple[PathwayFieldEvidence, ...] = (),
    warnings: tuple[str, ...] = (),
) -> PathwayFieldEvidence:
    return _new_pathway_field_evidence(
        field=field,
        origin=origin,
        value_digest=_pathway_digest(value),
        context_binding=context_binding,
        origin_binding=_pathway_digest(
            {
                "contract": "pathway-field-origin-v1",
                "origin": origin.value,
                "payload": origin_payload,
            }
        ),
        status=status,
        coverage=coverage,
        source_ids=source_ids,
        locators=locators,
        extraction_methods=extraction_methods,
        evidence_method=evidence_method,
        upstream_fields=upstream_fields,
        profile_fields=profile_fields,
        upstream_evidence_digests=tuple(item.digest for item in upstream_evidence),
        warnings=warnings,
    )


def _replay_pathway_field_evidence(
    record: PathwayFieldEvidence,
) -> PathwayFieldEvidence:
    rebuilt = _new_pathway_field_evidence(
        field=record.field,
        origin=record.origin,
        value_digest=record.value_digest,
        context_binding=record.context_binding,
        origin_binding=record.origin_binding,
        status=record.status,
        coverage=record.coverage,
        source_ids=record.source_ids,
        locators=record.locators,
        extraction_methods=record.extraction_methods,
        evidence_method=record.evidence_method,
        upstream_fields=record.upstream_fields,
        profile_fields=record.profile_fields,
        upstream_evidence_digests=record.upstream_evidence_digests,
        warnings=record.warnings,
    )
    if rebuilt.to_dict() != record.to_dict():
        raise ValueError(f"{record.field} field evidence digest does not replay")
    return record


def validate_pathway_field_evidence(
    value: Any,
    required_fields: tuple[str, ...],
    *,
    owner: str,
    field_values: dict[str, Any] | None = None,
    context_binding: str | None = None,
) -> tuple[PathwayFieldEvidence, ...]:
    if isinstance(value, (str, bytes, bytearray)):
        raise TypeError(f"{owner} field evidence must be a collection")
    try:
        records = tuple(value)
    except TypeError as error:
        raise TypeError(f"{owner} field evidence must be a collection") from error
    if any(type(item) is not PathwayFieldEvidence for item in records):
        raise TypeError(f"{owner} field evidence must contain typed records")
    for item in records:
        _replay_pathway_field_evidence(item)
    by_field = {item.field: item for item in records}
    missing = tuple(field for field in required_fields if field not in by_field)
    extras = tuple(field for field in by_field if field not in required_fields)
    if len(by_field) != len(records) or missing or extras:
        detail = missing[0] if missing else extras[0] if extras else "duplicate"
        raise ValueError(f"{owner} field evidence is incomplete: {detail}")
    ordered = tuple(by_field[field] for field in required_fields)
    if context_binding is not None:
        if _SHA256_ID.fullmatch(context_binding) is None:
            raise ValueError(f"{owner} field evidence context is invalid")
        if any(item.context_binding != context_binding for item in ordered):
            raise ValueError(f"{owner} field evidence context binding disagrees")
    if field_values is not None:
        if set(field_values) != set(required_fields):
            raise ValueError(f"{owner} displayed field value set is incomplete")
        for item in ordered:
            if item.value_digest != _pathway_digest(field_values[item.field]):
                raise ValueError(
                    f"{item.field} field evidence value digest disagrees"
                )
    for item in ordered:
        if item.origin is PathwayFieldEvidenceOrigin.DERIVED_DECISION and (
            not item.upstream_evidence_digests
        ):
            raise ValueError(
                f"{item.field} derived field evidence is detached from its upstream trail"
            )
    return ordered


def _pathway_type(value: Any, name: str = "pathway_type") -> str:
    normalized = _text(value, name)
    assert normalized is not None
    if normalized not in _PATHWAY_TYPES:
        raise ValueError(f"{name} is not a supported pathway type")
    return normalized


@dataclass(frozen=True)
class PathwayProfile(_Serializable):
    """Privacy-minimal inputs for deterministic pathway evaluation."""

    rank: int | None
    province: str
    subject_mode: str
    current_year: int
    eligibility_facts: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.rank is not None:
            object.__setattr__(self, "rank", _strict_positive_int(self.rank, "rank"))
        object.__setattr__(self, "province", _output_text(self.province, "province"))
        object.__setattr__(self, "subject_mode", _text(self.subject_mode, "subject_mode"))
        if self.subject_mode not in _SUBJECT_MODES:
            raise ValueError("subject_mode must be 3+1+2 or 3+3")
        object.__setattr__(
            self,
            "current_year",
            _strict_positive_int(self.current_year, "current_year", minimum=2000),
        )
        if self.current_year > 2100:
            raise ValueError("current_year must not exceed 2100")
        object.__setattr__(
            self,
            "eligibility_facts",
            tuple(sorted(_output_string_tuple(self.eligibility_facts, "eligibility_facts"))),
        )


@dataclass(frozen=True)
class PathwayPolicy(_Serializable):
    """One accepted, year- and province-scoped pathway policy record."""

    policy_id: str
    pathway_type: str
    title: str
    institution: str
    province: str
    subject_mode: str
    valid_year: int | None
    eligibility_requirements: tuple[str, ...]
    disqualifying_facts: tuple[str, ...]
    professional_options: tuple[str, ...]
    training_arrangements: str | None
    transition_rules: str | None
    outcomes: str | None
    service_employment_obligations: str | None
    penalty_exit_rules: str | None
    fees_and_subsidies: str | None
    policy_source_ids: tuple[str, ...]
    evidence_status: EvidenceStatus
    calculation_basis: str
    target_year: int | None = None
    data_year: int | None = None
    fallback_distance: int = 0
    year_basis: str = "current_year"
    timeline: tuple[str, ...] = ()
    preparation_actions: tuple[str, ...] = ()
    grade_requirements: tuple[str, ...] | None = None
    subject_requirements: tuple[str, ...] | None = None
    award_requirements: tuple[str, ...] | None = None
    activity_requirements: tuple[str, ...] | None = None
    application_materials: tuple[str, ...] | None = None
    profile_digest: str | None = None
    query_plan_digest: str | None = None
    field_evidence: tuple[PathwayFieldEvidence, ...] = ()
    _authenticated_projection: Any = None

    def __post_init__(self) -> None:
        policy_id = _text(self.policy_id, "policy_id")
        assert policy_id is not None
        if _SAFE_ID.fullmatch(policy_id) is None:
            raise ValueError("policy_id must use the public safe-ID syntax")
        object.__setattr__(self, "policy_id", policy_id)
        object.__setattr__(self, "pathway_type", _pathway_type(self.pathway_type))
        for name in ("title", "institution", "province"):
            object.__setattr__(self, name, _output_text(getattr(self, name), name))
        object.__setattr__(self, "subject_mode", _text(self.subject_mode, "subject_mode"))
        if self.subject_mode not in _SUBJECT_MODES:
            raise ValueError("subject_mode must be 3+1+2 or 3+3")
        if self.valid_year is not None:
            valid_year = _schema_integer(self.valid_year, "valid_year")
            if valid_year < 2000:
                raise ValueError("valid_year must be at least 2000")
            if valid_year > 2100:
                raise ValueError("valid_year must not exceed 2100")
            object.__setattr__(self, "valid_year", valid_year)
        for name in ("eligibility_requirements", "disqualifying_facts"):
            object.__setattr__(
                self,
                name,
                tuple(sorted(_output_string_tuple(getattr(self, name), name))),
            )
        object.__setattr__(
            self,
            "professional_options",
            _canonical_professional_options(self.professional_options),
        )
        for name in (
            "training_arrangements",
            "transition_rules",
            "outcomes",
            "service_employment_obligations",
            "penalty_exit_rules",
            "fees_and_subsidies",
        ):
            object.__setattr__(
                self,
                name,
                _output_text(getattr(self, name), name, optional=True),
            )
        object.__setattr__(
            self,
            "policy_source_ids",
            _source_id_tuple(self.policy_source_ids, "policy_source_ids"),
        )
        object.__setattr__(self, "evidence_status", _status(self.evidence_status))
        basis = _output_text(self.calculation_basis, "calculation_basis")
        assert basis is not None
        object.__setattr__(self, "calculation_basis", basis)
        target_year = self.valid_year if self.target_year is None else self.target_year
        data_year = self.valid_year if self.data_year is None else self.data_year
        if target_year is None or data_year is None:
            if target_year is not None or data_year is not None or self.fallback_distance != 0:
                raise ValueError("incomplete pathway year metadata")
            object.__setattr__(self, "target_year", None)
            object.__setattr__(self, "data_year", None)
            object.__setattr__(self, "year_basis", "unverified")
        else:
            target_year = _strict_positive_int(target_year, "target_year", minimum=2000)
            data_year = _strict_positive_int(data_year, "data_year", minimum=2000)
            distance = _strict_int(self.fallback_distance, "fallback_distance")
            if target_year > 2100 or data_year > 2100 or not 0 <= distance <= 3:
                raise ValueError("pathway year metadata is outside its supported range")
            if target_year - data_year != distance or self.valid_year != data_year:
                raise ValueError("pathway fallback distance does not match policy years")
            expected_basis = "current_year" if distance == 0 else "historical_fallback"
            if self.year_basis != expected_basis:
                raise ValueError("pathway year basis does not match fallback distance")
            object.__setattr__(self, "target_year", target_year)
            object.__setattr__(self, "data_year", data_year)
            object.__setattr__(self, "fallback_distance", distance)
        object.__setattr__(
            self,
            "timeline",
            _output_string_tuple(self.timeline, "timeline"),
        )
        object.__setattr__(
            self,
            "preparation_actions",
            _output_string_tuple(self.preparation_actions, "preparation_actions"),
        )
        for name in (
            "grade_requirements",
            "subject_requirements",
            "award_requirements",
            "activity_requirements",
            "application_materials",
        ):
            value = getattr(self, name)
            object.__setattr__(
                self,
                name,
                None if value is None else _output_string_tuple(value, name),
            )
        if (self.profile_digest is None) != (self.query_plan_digest is None):
            raise ValueError("pathway planning bindings must be complete")
        for name in ("profile_digest", "query_plan_digest"):
            value = getattr(self, name)
            if value is not None and re.fullmatch(r"sha256:[0-9a-f]{64}", value) is None:
                raise ValueError(f"{name} must be a lower-case SHA-256 identity")
        if self.field_evidence:
            object.__setattr__(
                self,
                "field_evidence",
                validate_pathway_field_evidence(
                    self.field_evidence,
                    PATHWAY_POLICY_EVIDENCE_FIELDS,
                    owner="pathway policy",
                ),
            )

    def to_dict(self) -> dict[str, Any]:
        """Keep the published v1 policy schema stable; decision fields are internal."""

        excluded = {
            "grade_requirements",
            "subject_requirements",
            "award_requirements",
            "activity_requirements",
            "application_materials",
            "profile_digest",
            "query_plan_digest",
            "field_evidence",
            "_authenticated_projection",
        }
        return {
            item.name: _json_safe(getattr(self, item.name))
            for item in fields(self)
            if item.name not in excluded
        }


def pathway_policy_field_values(policy: PathwayPolicy) -> dict[str, Any]:
    """Return the exact policy values covered by authenticated raw-field trails."""

    if type(policy) is not PathwayPolicy:
        raise TypeError("policy field values require a strict PathwayPolicy")
    return {
        field: getattr(policy, field)
        for field in PATHWAY_POLICY_EVIDENCE_FIELDS
    }


def pathway_policy_internal_payload(policy: PathwayPolicy) -> dict[str, Any]:
    """Private replay payload including all decision inputs and field trails."""

    if type(policy) is not PathwayPolicy:
        raise TypeError("policy replay requires a strict PathwayPolicy")
    return {
        item.name: _json_safe(getattr(policy, item.name))
        for item in fields(policy)
        if item.name != "_authenticated_projection"
    }


@dataclass(frozen=True)
class RankAdjustmentModel(_Serializable):
    """Explicit, evidence-backed rank transformation with bounded applicability."""

    model_id: str
    province: str
    subject_mode: str
    cohort_years: tuple[int, ...]
    source_ids: tuple[str, ...]
    evidence_status: EvidenceStatus
    method: str
    pathway_types: tuple[str, ...]
    applicability_rank_min: int
    applicability_rank_max: int
    score_table_rank_min: int
    score_table_rank_max: int
    rank_delta: int

    def __post_init__(self) -> None:
        model_id = _text(self.model_id, "model_id")
        assert model_id is not None
        if _SAFE_ID.fullmatch(model_id) is None:
            raise ValueError("model_id must use the public safe-ID syntax")
        object.__setattr__(self, "model_id", model_id)
        object.__setattr__(self, "province", _output_text(self.province, "province"))
        object.__setattr__(self, "subject_mode", _text(self.subject_mode, "subject_mode"))
        method = _text(self.method, "method")
        if method not in _MODEL_METHODS:
            raise ValueError("unsupported model method")
        object.__setattr__(self, "method", method)
        if self.subject_mode not in _SUBJECT_MODES:
            raise ValueError("subject_mode must be 3+1+2 or 3+3")
        if isinstance(self.cohort_years, (str, bytes, bytearray)):
            raise TypeError("cohort_years must be a collection of integers")
        try:
            cohort_years = tuple(self.cohort_years)
        except TypeError as error:
            raise TypeError("cohort_years must be a collection of integers") from error
        if not cohort_years:
            raise ValueError("cohort_years must not be empty")
        for year in cohort_years:
            _strict_positive_int(year, "cohort_year", minimum=2000)
            if year > 2100:
                raise ValueError("cohort_year must not exceed 2100")
        if len(cohort_years) != len(set(cohort_years)):
            raise ValueError("cohort_years must be unique")
        object.__setattr__(self, "cohort_years", tuple(sorted(cohort_years)))
        object.__setattr__(
            self,
            "source_ids",
            _source_id_tuple(self.source_ids, "source_ids"),
        )
        object.__setattr__(self, "evidence_status", _status(self.evidence_status))
        pathway_types = _string_tuple(
            self.pathway_types, "pathway_types", allow_empty=False, sort=True
        )
        for item in pathway_types:
            _pathway_type(item, "pathway_types item")
        object.__setattr__(self, "pathway_types", pathway_types)
        for name in (
            "applicability_rank_min",
            "applicability_rank_max",
            "score_table_rank_min",
            "score_table_rank_max",
        ):
            object.__setattr__(
                self, name, _strict_positive_int(getattr(self, name), name)
            )
        if self.applicability_rank_min > self.applicability_rank_max:
            raise ValueError("applicability rank bounds are reversed")
        if self.score_table_rank_min > self.score_table_rank_max:
            raise ValueError("score-table rank bounds are reversed")
        object.__setattr__(self, "rank_delta", _strict_int(self.rank_delta, "rank_delta"))


def pathway_display_field_values(value: Any) -> dict[str, Any]:
    """Canonical values for every pathway field shown in reports."""

    source_ids = (
        getattr(value, "policy_source_ids")
        if hasattr(value, "policy_source_ids")
        else getattr(value, "source_ids")
    )
    result = {
        field: (
            source_ids
            if field == "source_ids"
            else {
                "year_basis": getattr(value, "year_basis"),
                "target_year": getattr(value, "target_year"),
                "data_year": getattr(value, "data_year"),
                "fallback_distance": getattr(value, "fallback_distance"),
            }
            if field == "year_basis"
            else getattr(value, field)
        )
        for field in PATHWAY_DISPLAY_EVIDENCE_FIELDS
    }
    return result


def validate_pathway_display_evidence(
    value: Any,
    *,
    owner: str,
) -> tuple[PathwayFieldEvidence, ...]:
    """Replay records and bind them to the owner's current displayed values."""

    context_binding = getattr(value, "field_evidence_context", None)
    if not isinstance(context_binding, str):
        raise ValueError(f"{owner} field evidence context is missing")
    return validate_pathway_field_evidence(
        getattr(value, "field_evidence", ()),
        PATHWAY_DISPLAY_EVIDENCE_FIELDS,
        owner=owner,
        field_values=pathway_display_field_values(value),
        context_binding=context_binding,
    )


@dataclass(frozen=True)
class PathwayItem(_Serializable):
    policy_id: str
    pathway_type: str
    title: str
    institution: str
    status: str
    eligibility: str
    missing_constraints: tuple[str, ...]
    professional_options: tuple[str, ...]
    training_arrangements: str | None
    transition_rules: str | None
    outcomes: str | None
    service_employment_obligations: str | None
    penalty_exit_rules: str | None
    fees_and_subsidies: str | None
    policy_source_ids: tuple[str, ...]
    evidence_status: EvidenceStatus
    calculation_basis: str
    target_rank: int | None = None
    investment_decision: str = ""
    qualification_status: str = ""
    satisfied_conditions: tuple[str, ...] = ()
    timeline: tuple[str, ...] = ()
    preparation_actions: tuple[str, ...] = ()
    target_year: int | None = None
    data_year: int | None = None
    fallback_distance: int = 0
    year_basis: str = "unverified"
    decision_reasons: tuple[DecisionReason, ...] = ()
    field_evidence: tuple[PathwayFieldEvidence, ...] = ()
    field_evidence_context: str | None = None

    def __post_init__(self) -> None:
        policy_id = _text(self.policy_id, "policy_id")
        assert policy_id is not None
        if _SAFE_ID.fullmatch(policy_id) is None:
            raise ValueError("policy_id must use the public safe-ID syntax")
        object.__setattr__(self, "policy_id", policy_id)
        object.__setattr__(self, "pathway_type", _pathway_type(self.pathway_type))
        for name in ("title", "institution", "calculation_basis"):
            object.__setattr__(self, name, _output_text(getattr(self, name), name))
        allowed_pairs = {
            "formal": "eligible",
            "pending_verification": "pending_verification",
            "excluded": "ineligible",
        }
        if self.status not in allowed_pairs:
            raise ValueError("status is not supported")
        if self.eligibility != allowed_pairs[self.status]:
            raise ValueError("eligibility is inconsistent with status")
        constraints = _output_string_tuple(
            self.missing_constraints, "missing_constraints"
        )
        if self.status == "formal" and constraints:
            raise ValueError("formal items cannot have missing constraints")
        if self.status != "formal" and not constraints:
            raise ValueError("non-formal items require an explicit constraint or reason")
        object.__setattr__(self, "missing_constraints", constraints)
        object.__setattr__(
            self,
            "professional_options",
            _canonical_professional_options(self.professional_options),
        )
        for name in (
            "training_arrangements",
            "transition_rules",
            "outcomes",
            "service_employment_obligations",
            "penalty_exit_rules",
            "fees_and_subsidies",
        ):
            object.__setattr__(
                self,
                name,
                _output_text(getattr(self, name), name, optional=True),
            )
        complete_details = bool(self.professional_options) and all(
            getattr(self, name) is not None
            for name in (
                "training_arrangements",
                "transition_rules",
                "outcomes",
                "service_employment_obligations",
                "penalty_exit_rules",
                "fees_and_subsidies",
            )
        )
        if self.status == "formal" and not complete_details:
            raise ValueError("formal items require complete policy details")
        normalized_evidence_status = _status(self.evidence_status)
        if self.policy_source_ids:
            normalized_policy_sources = _source_id_tuple(
                self.policy_source_ids, "policy_source_ids"
            )
        elif (
            self.status == "pending_verification"
            and normalized_evidence_status
            in {EvidenceStatus.MISSING, EvidenceStatus.MASKED}
        ):
            normalized_policy_sources = ()
        else:
            raise ValueError("policy_source_ids must not be empty")
        object.__setattr__(self, "policy_source_ids", normalized_policy_sources)
        object.__setattr__(self, "evidence_status", normalized_evidence_status)
        if self.status == "formal":
            evidence_problem = _exact_evidence_problem(
                self.evidence_status, self.policy_source_ids, "政策"
            )
            if evidence_problem is not None:
                raise ValueError("formal items require accepted exact evidence")
        if self.target_rank is not None:
            object.__setattr__(
                self,
                "target_rank",
                _strict_positive_int(self.target_rank, "target_rank"),
            )
            if self.status != "formal":
                raise ValueError("only formal items may carry a target rank")
        decisions = {"主攻", "重点准备", "备选", "观察", "不建议"}
        qualifications = {"已满足", "部分满足", "暂未满足", "待核验", "不适用"}
        decision = self.investment_decision or {
            "formal": "主攻",
            "pending_verification": "观察",
            "excluded": "不建议",
        }[self.status]
        qualification = self.qualification_status or {
            "formal": "已满足",
            "pending_verification": "待核验",
            "excluded": "不适用",
        }[self.status]
        if decision not in decisions:
            raise ValueError("investment_decision is not supported")
        if qualification not in qualifications:
            raise ValueError("qualification_status is not supported")
        if self.status == "excluded" and (
            decision != "不建议" or qualification != "不适用"
        ):
            raise ValueError("excluded pathway decision is inconsistent")
        object.__setattr__(self, "investment_decision", decision)
        object.__setattr__(self, "qualification_status", qualification)
        for name in ("satisfied_conditions", "timeline", "preparation_actions"):
            object.__setattr__(
                self,
                name,
                _output_string_tuple(getattr(self, name), name),
            )
        if self.target_year is None or self.data_year is None:
            if self.target_year is not None or self.data_year is not None:
                raise ValueError("incomplete pathway item year metadata")
            if self.fallback_distance != 0 or self.year_basis != "unverified":
                raise ValueError("unverified pathway item has inconsistent year metadata")
        else:
            target_year = _strict_positive_int(self.target_year, "target_year", minimum=2000)
            data_year = _strict_positive_int(self.data_year, "data_year", minimum=2000)
            distance = _strict_int(self.fallback_distance, "fallback_distance")
            if target_year - data_year != distance or not 0 <= distance <= 3:
                raise ValueError("pathway item fallback metadata is inconsistent")
            expected_basis = "current_year" if distance == 0 else "historical_fallback"
            if self.year_basis != expected_basis:
                raise ValueError("pathway item year basis is inconsistent")
        reasons = tuple(self.decision_reasons)
        if reasons:
            if not all(isinstance(item, DecisionReason) for item in reasons):
                raise TypeError("decision_reasons must contain DecisionReason records")
            dimensions = tuple(item.dimension for item in reasons)
            expected_dimensions = DecisionPolicySnapshot.load_default().pathway_reason_order
            if dimensions != expected_dimensions:
                raise ValueError("decision_reasons must cover all eight dimensions in policy order")
        object.__setattr__(self, "decision_reasons", reasons)
        raw_records = tuple(self.field_evidence)
        context_binding = self.field_evidence_context
        if context_binding is None and raw_records:
            context_binding = raw_records[0].context_binding
        if not isinstance(context_binding, str) or _SHA256_ID.fullmatch(context_binding) is None:
            raise ValueError("pathway item field evidence context is invalid")
        object.__setattr__(self, "field_evidence_context", context_binding)
        object.__setattr__(self, "field_evidence", raw_records)
        object.__setattr__(
            self,
            "field_evidence",
            validate_pathway_display_evidence(self, owner="pathway item"),
        )


@dataclass(frozen=True)
class PathwayResult(_Serializable):
    """Policy evaluation result; numeric output is absent without a model."""

    items: tuple[PathwayItem, ...] = ()
    formal_shortlist: tuple[str, ...] = ()
    target_rank: int | None = None
    transformation: str | None = None
    model_source_ids: tuple[str, ...] = ()
    model_id: str | None = None
    model_method: str | None = None
    model_evidence_status: EvidenceStatus | None = None
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if isinstance(self.items, (str, bytes, bytearray)):
            raise TypeError("items must be a collection of PathwayItem records")
        try:
            items = tuple(self.items)
        except TypeError as error:
            raise TypeError("items must be a collection of PathwayItem records") from error
        if not all(isinstance(item, PathwayItem) for item in items):
            raise TypeError("items must contain only PathwayItem records")
        if len({item.policy_id for item in items}) != len(items):
            raise ValueError("items must have unique policy IDs")
        items = tuple(sorted(items, key=lambda item: item.policy_id))
        object.__setattr__(self, "items", items)

        shortlist = _string_tuple(
            self.formal_shortlist,
            "formal_shortlist",
            safe_ids=True,
            sort=True,
        )
        expected = tuple(
            item.policy_id for item in items if item.status == "formal"
        )
        if shortlist != expected:
            raise ValueError("formal_shortlist must name every and only formal item")
        object.__setattr__(self, "formal_shortlist", shortlist)

        if self.target_rank is None:
            if self.transformation is not None:
                raise ValueError("transformation requires a target_rank")
            if any(item.target_rank is not None for item in items):
                raise ValueError("item target ranks require a result target_rank")
            if self.model_source_ids:
                raise ValueError("model_source_ids require a target_rank")
            if self.model_id is not None or self.model_method is not None or self.model_evidence_status is not None:
                raise ValueError("model metadata requires a target_rank")
        else:
            target_rank = _strict_positive_int(self.target_rank, "target_rank")
            object.__setattr__(self, "target_rank", target_rank)
            transformation = _output_text(self.transformation, "transformation")
            object.__setattr__(self, "transformation", transformation)
            if not any(item.status == "formal" for item in items):
                raise ValueError("target_rank requires at least one formal item")
            if any(
                item.status == "formal" and item.target_rank != target_rank
                for item in items
            ):
                raise ValueError("formal item target ranks must match the result")
        model_source_ids = (
            _source_id_tuple(self.model_source_ids, "model_source_ids")
            if self.model_source_ids else ()
        )
        if self.target_rank is not None and not model_source_ids:
            raise ValueError("target_rank requires model_source_ids")
        object.__setattr__(self, "model_source_ids", model_source_ids)
        if self.target_rank is not None:
            model_id = _text(self.model_id, "model_id")
            assert model_id is not None
            if _SAFE_ID.fullmatch(model_id) is None:
                raise ValueError("model_id must use the public safe-ID syntax")
            model_method = _text(self.model_method, "model_method")
            if model_method not in _MODEL_METHODS:
                raise ValueError("unsupported model method")
            model_status = _status(self.model_evidence_status, "model_evidence_status")
            if _exact_evidence_problem(model_status, model_source_ids, "位次模型") is not None:
                raise ValueError("target_rank requires exact sufficient model evidence")
            object.__setattr__(self, "model_id", model_id)
            object.__setattr__(self, "model_method", model_method)
            object.__setattr__(self, "model_evidence_status", model_status)
        object.__setattr__(
            self, "warnings", _output_string_tuple(self.warnings, "warnings")
        )


def _observation_pathway_item(observation: Any) -> PathwayItem:
    """Project one authenticated evidence gap without inventing policy facts."""

    calculation_basis = (
        "画像已确认且查询计划已纳入该路径；政策证据冲突，"
        "仅保留观察并等待核验"
        if observation.evidence_status is EvidenceStatus.CONFLICT
        else "画像已确认且查询计划已纳入该路径；政策证据尚未形成"
        "可核验结论，仅保留观察并等待核验"
    )
    known_fields = {item.field: item for item in observation.field_provenance}
    values = {
        "title": observation.title,
        "institution": observation.institution or "待核验",
        "investment_decision": "观察",
        "qualification_status": "待核验",
        "status": "pending_verification",
        "eligibility": "pending_verification",
        "evidence_status": observation.evidence_status,
        "source_ids": observation.source_ids,
        # Bind the displayed ordering while the observation and its raw
        # provenance remain unchanged for authenticated journal replay.
        "professional_options": _canonical_professional_options(
            observation.professional_options
        ),
        "training_arrangements": None,
        "transition_rules": None,
        "outcomes": None,
        "service_employment_obligations": None,
        "penalty_exit_rules": None,
        "fees_and_subsidies": None,
        "satisfied_conditions": (),
        "missing_constraints": observation.missing_constraints,
        "timeline": (),
        "preparation_actions": observation.preparation_actions,
        "decision_reasons": (),
        "year_basis": {
            "year_basis": "unverified",
            "target_year": None,
            "data_year": None,
            "fallback_distance": 0,
        },
        "calculation_basis": calculation_basis,
    }
    context_binding = _pathway_field_context_binding(
        {
            "contract": "pathway-observation-decision-v1",
            "observation_digest": observation.digest,
            "profile_digest": observation.profile_digest,
            "query_plan_digest": observation.query_plan_digest,
        }
    )
    coverage = {
        EvidenceStatus.CONFLICT: "conflict",
        EvidenceStatus.PARTIAL: "partial",
        EvidenceStatus.MASKED: "missing",
        EvidenceStatus.MISSING: "missing",
    }[observation.evidence_status]
    common_origin = {
        "observation_id": observation.observation_id,
        "observation_digest": observation.digest,
    }
    source_record = _create_pathway_field_evidence(
        field="source_ids",
        value=values["source_ids"],
        origin=PathwayFieldEvidenceOrigin.POLICY_SOURCE,
        context_binding=context_binding,
        origin_payload={**common_origin, "field": "source_ids"},
        status=observation.evidence_status,
        coverage=coverage,
        source_ids=observation.source_ids,
        locators=observation.locators,
        extraction_methods=observation.extraction_methods,
        evidence_method=observation.evidence_method,
        upstream_fields=("pathway_observation.source_ids",),
        warnings=observation.missing_constraints,
    )
    policy_fields = {
        "institution",
        "evidence_status",
        "source_ids",
        "professional_options",
        "training_arrangements",
        "transition_rules",
        "outcomes",
        "service_employment_obligations",
        "penalty_exit_rules",
        "fees_and_subsidies",
        "timeline",
    }
    records: dict[str, PathwayFieldEvidence] = {"source_ids": source_record}
    for field in PATHWAY_DISPLAY_EVIDENCE_FIELDS:
        if field == "source_ids":
            continue
        if field == "title":
            records[field] = _create_pathway_field_evidence(
                field=field,
                value=values[field],
                origin=PathwayFieldEvidenceOrigin.QUERY_CONTEXT,
                context_binding=context_binding,
                origin_payload={**common_origin, "query_task_ids": observation.query_task_ids},
                status=EvidenceStatus.INFERRED,
                coverage="complete",
                source_ids=(),
                locators=observation.locators,
                extraction_methods=("authenticated-query-plan",),
                evidence_method="query-plan-pathway-title-v1",
                upstream_fields=("query_task.target_name",),
                profile_fields=("pathway_preferences",),
            )
        elif field in policy_fields:
            retained = known_fields.get(field)
            if retained is None:
                records[field] = _create_pathway_field_evidence(
                    field=field,
                    value=values[field],
                    origin=PathwayFieldEvidenceOrigin.POLICY_SOURCE,
                    context_binding=context_binding,
                    origin_payload={**common_origin, "field": field},
                    status=observation.evidence_status,
                    coverage=coverage,
                    source_ids=observation.source_ids,
                    locators=observation.locators,
                    extraction_methods=observation.extraction_methods,
                    evidence_method=observation.evidence_method,
                    upstream_fields=(f"pathway_observation.{field}",),
                    warnings=observation.missing_constraints,
                )
            else:
                records[field] = _create_pathway_field_evidence(
                    field=field,
                    value=values[field],
                    origin=PathwayFieldEvidenceOrigin.POLICY_SOURCE,
                    context_binding=context_binding,
                    origin_payload={
                        **common_origin,
                        "field": field,
                        "field_provenance": retained.to_dict(),
                    },
                    status=retained.status,
                    coverage="complete",
                    source_ids=retained.source_ids,
                    locators=retained.locators,
                    extraction_methods=retained.extraction_methods,
                    evidence_method=retained.evidence_method,
                    upstream_fields=(f"pathway_observation.{field}",),
                    warnings=retained.warnings,
                )
        else:
            records[field] = _create_pathway_field_evidence(
                field=field,
                value=values[field],
                origin=PathwayFieldEvidenceOrigin.DERIVED_DECISION,
                context_binding=context_binding,
                origin_payload={**common_origin, "field": field},
                status=EvidenceStatus.INFERRED,
                coverage="complete",
                source_ids=observation.source_ids,
                locators=observation.locators,
                extraction_methods=("pathway-observation-decision-v1",),
                evidence_method="pathway-observation-decision-v1",
                upstream_fields=(
                    "pathway_observation.evidence_status",
                    "pathway_observation.missing_constraints",
                ),
                profile_fields=("pathway_preferences", "eligibility_facts"),
                upstream_evidence=(source_record,),
                warnings=observation.missing_constraints,
            )
    return PathwayItem(
        policy_id=observation.observation_id,
        pathway_type=observation.pathway_type,
        title=observation.title,
        institution=values["institution"],
        status="pending_verification",
        eligibility="pending_verification",
        missing_constraints=observation.missing_constraints,
        professional_options=values["professional_options"],
        training_arrangements=None,
        transition_rules=None,
        outcomes=None,
        service_employment_obligations=None,
        penalty_exit_rules=None,
        fees_and_subsidies=None,
        policy_source_ids=observation.source_ids,
        evidence_status=observation.evidence_status,
        calculation_basis=calculation_basis,
        target_rank=None,
        investment_decision="观察",
        qualification_status="待核验",
        satisfied_conditions=(),
        timeline=(),
        preparation_actions=observation.preparation_actions,
        target_year=None,
        data_year=None,
        fallback_distance=0,
        year_basis="unverified",
        decision_reasons=(),
        field_evidence=tuple(
            records[field] for field in PATHWAY_DISPLAY_EVIDENCE_FIELDS
        ),
        field_evidence_context=context_binding,
    )


def evaluate_pathways(
    profile: Any,
    policies: tuple[PathwayPolicy, ...],
    model: RankAdjustmentModel | None = None,
    *,
    rank_scenario: Any = None,
    decision_policy: DecisionPolicySnapshot | None = None,
    query_plan: Any = None,
    observations: tuple[Any, ...] = (),
) -> PathwayResult:
    """Evaluate eligibility and, only when documented, a bounded rank model."""

    full_profile = None
    if isinstance(profile, PathwayProfile):
        evaluation_profile = profile
    else:
        if __package__:
            from .planning_profile import PlanningProfile
            from .rank_locator import RankScenario
        else:  # pragma: no cover - flat compatibility is exercised separately
            from planning_profile import PlanningProfile
            from rank_locator import RankScenario
        if not isinstance(profile, PlanningProfile):
            raise TypeError("profile must be a PlanningProfile or PathwayProfile")
        try:
            canonical_rank_scenario = RankScenario._create(**rank_scenario.to_dict())
        except (AttributeError, TypeError, ValueError):
            raise TypeError(
                "full planning profiles require an authenticated RankScenario"
            ) from None
        if canonical_rank_scenario.to_dict() != rank_scenario.to_dict():
            raise TypeError("full planning profiles require an authenticated RankScenario")
        rank_scenario = canonical_rank_scenario
        numeric_rank = (
            rank_scenario.central_rank
            if rank_scenario.status in {EvidenceStatus.OFFICIAL, EvidenceStatus.INFERRED}
            else None
        )
        if query_plan is None or type(query_plan).__name__ != "QueryPlan":
            raise TypeError(
                "full planning profiles require a canonical typed QueryPlan"
            )
        if __package__:
            from .query_plan import validate_query_plan_payload
        else:  # pragma: no cover - flat compatibility is exercised separately
            from query_plan import validate_query_plan_payload
        try:
            canonical_plan = validate_query_plan_payload(query_plan.to_dict())
        except (AttributeError, TypeError, ValueError):
            raise TypeError(
                "full planning profiles require a canonical typed QueryPlan"
            ) from None
        if canonical_plan.to_dict() != query_plan.to_dict():
            raise TypeError(
                "full planning profiles require a canonical typed QueryPlan"
            )
        query_plan_digest = "sha256:" + hashlib.sha256(
            json.dumps(
                canonical_plan.to_dict(),
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ).encode("utf-8")
        ).hexdigest()
        current_year = canonical_plan.research_year
        evaluation_profile = PathwayProfile(
            rank=numeric_rank,
            province=profile.province,
            subject_mode=profile.subject_mode,
            current_year=current_year,
            eligibility_facts=profile.eligibility_facts,
        )
        full_profile = profile
    if isinstance(observations, (str, bytes, bytearray)):
        raise TypeError(
            "observations must be a collection of PathwayEvidenceObservation records"
        )
    try:
        observation_records = tuple(observations)
    except TypeError as error:
        raise TypeError(
            "observations must be a collection of PathwayEvidenceObservation records"
        ) from error
    if observation_records and full_profile is None:
        raise TypeError("pathway observations require a full PlanningProfile")
    if observation_records:
        if __package__:
            from .adapters.pathway_bridge import (
                PathwayEvidenceObservation,
                validate_pathway_evidence_observation,
            )
        else:  # pragma: no cover - flat compatibility is exercised separately
            from adapters.pathway_bridge import (  # type: ignore
                PathwayEvidenceObservation,
                validate_pathway_evidence_observation,
            )
        if any(type(item) is not PathwayEvidenceObservation for item in observation_records):
            raise TypeError(
                "observations must contain only PathwayEvidenceObservation records"
            )
        observation_records = tuple(
            validate_pathway_evidence_observation(item, full_profile, canonical_plan)
            for item in observation_records
        )
        if len({item.observation_id for item in observation_records}) != len(
            observation_records
        ):
            raise ValueError("pathway observation IDs must be unique")
    reviewed = decision_policy or DecisionPolicySnapshot.load_default()
    if type(reviewed) is not DecisionPolicySnapshot:
        raise TypeError("decision_policy must be a strict DecisionPolicySnapshot")
    if isinstance(policies, (str, bytes, bytearray)):
        raise TypeError("policies must be a collection of PathwayPolicy records")
    try:
        records = tuple(policies)
    except TypeError as error:
        raise TypeError("policies must be a collection of PathwayPolicy records") from error
    if not all(isinstance(item, PathwayPolicy) for item in records):
        raise TypeError("policies must contain only PathwayPolicy records")
    if len({item.policy_id for item in records}) != len(records):
        raise ValueError("policy_id must be unique within one evaluation")
    records = tuple(sorted(records, key=lambda item: item.policy_id))
    if full_profile is not None:
        if __package__:
            from .adapters.pathway_bridge import validate_authenticated_domain_policy
        else:  # pragma: no cover - flat compatibility is exercised separately
            from adapters.pathway_bridge import validate_authenticated_domain_policy
        records = tuple(
            validate_authenticated_domain_policy(
                item,
                full_profile,
                canonical_plan,
            )
            for item in records
        )
    if full_profile is not None and any(
        item.profile_digest != full_profile.digest
        or item.query_plan_digest != query_plan_digest
        or item.target_year != current_year
        for item in records
    ):
        raise ValueError(
            "pathway policies do not match the authenticated planning context"
        )
    accepted_task_ids = (
        {item._authenticated_projection.query_task_id for item in records}
        if observation_records
        else set()
    )
    if any(
        accepted_task_ids.intersection(item.query_task_ids)
        for item in observation_records
    ):
        raise ValueError(
            "decisive pathway policy must replace its non-decisive observation"
        )
    if model is not None and not isinstance(model, RankAdjustmentModel):
        raise TypeError("model must be a RankAdjustmentModel or None")

    items = tuple(
        _evaluate_policy(
            evaluation_profile,
            record,
            None,
            None,
            full_profile=full_profile,
            rank_scenario=rank_scenario,
            decision_policy=reviewed,
            model=None,
        )
        for record in records
    )
    observation_items = tuple(
        _observation_pathway_item(item) for item in observation_records
    )
    formal_policy_ids = {
        item.policy_id for item in items if item.status == "formal"
    }
    formal_policies = tuple(
        record for record in records if record.policy_id in formal_policy_ids
    )
    warnings: list[str] = []
    target_rank: int | None = None
    transformation: str | None = None
    if model is None:
        warnings.append("未提供有依据的位次模型")
    else:
        model_problem = _model_problem(evaluation_profile, formal_policies, model)
        if model_problem is not None:
            warnings.append(model_problem)
        else:
            raw_target = evaluation_profile.rank + model.rank_delta
            target_rank = min(
                model.score_table_rank_max,
                max(model.score_table_rank_min, raw_target),
            )
            transformation = (
                f"模型 {model.model_id}：{model.method}；队列年份 "
                f"{','.join(str(year) for year in model.cohort_years)}；"
                f"{evaluation_profile.rank} + "
                f"({model.rank_delta}) = {raw_target}；按一分一段位次域 "
                f"[{model.score_table_rank_min}, {model.score_table_rank_max}] "
                f"钳制为 {target_rank}"
            )
            if target_rank != raw_target:
                warnings.append("模型原始结果超出声明的一分一段位次域，已按边界钳制")
            items = tuple(
                _evaluate_policy(
                    evaluation_profile,
                    record,
                    target_rank,
                    transformation,
                    full_profile=full_profile,
                    rank_scenario=rank_scenario,
                    decision_policy=reviewed,
                    model=model,
                )
                for record in records
            )
    items = (*items, *observation_items)
    if observation_items:
        warnings.append(
            "部分多元路径仅为观察项：政策或资格证据待补齐，未形成可申报结论"
        )
    return PathwayResult(
        items=items,
        formal_shortlist=tuple(
            item.policy_id for item in items if item.status == "formal"
        ),
        target_rank=target_rank,
        transformation=transformation,
        model_source_ids=model.source_ids if target_rank is not None else (),
        model_id=model.model_id if target_rank is not None else None,
        model_method=model.method if target_rank is not None else None,
        model_evidence_status=model.evidence_status if target_rank is not None else None,
        warnings=tuple(warnings),
    )


def _exact_evidence_problem(
    status: EvidenceStatus, source_ids: tuple[str, ...], noun: str
) -> str | None:
    minimum = _EXACT_EVIDENCE_MINIMUMS.get(status)
    if minimum is None:
        return f"{noun}证据状态不是可接受的精确状态"
    if len(source_ids) < minimum:
        return f"{noun}独立来源不足：{status.value} 至少需要 {minimum} 个来源"
    return None


def exact_evidence_problem(
    status: EvidenceStatus, source_ids: tuple[str, ...], noun: str = "政策"
) -> str | None:
    """Expose the single source-policy threshold seam to internal adapters."""

    return _exact_evidence_problem(status, source_ids, noun)


def _model_problem(
    profile: PathwayProfile,
    policies: tuple[PathwayPolicy, ...],
    model: RankAdjustmentModel,
) -> str | None:
    evidence_problem = _exact_evidence_problem(
        model.evidence_status, model.source_ids, "位次模型"
    )
    if evidence_problem is not None:
        return evidence_problem
    if model.province != profile.province:
        return "位次模型省份与用户画像不匹配"
    if model.subject_mode != profile.subject_mode:
        return "位次模型选科模式与用户画像不匹配"
    if profile.rank is None:
        return "用户画像暂无可靠位次，位次模型未执行"
    if profile.current_year not in model.cohort_years:
        return "用户当前年份不在模型声明的队列年份中"
    if not (model.applicability_rank_min <= profile.rank <= model.applicability_rank_max):
        return "用户位次超出模型声明的适用范围"
    if not policies:
        return "无满足正式候选条件的政策，位次模型未执行"
    for record in policies:
        if record.province != model.province or record.subject_mode != model.subject_mode:
            return "政策记录与位次模型的省份或选科模式不匹配"
        if record.pathway_type not in model.pathway_types:
            return "政策路径类型不在位次模型声明的适用范围"
    return None


def _pathway_preference_key(pathway_type: str) -> str:
    if pathway_type == "strong_foundation":
        return "strong_foundation"
    if pathway_type == "comprehensive_evaluation":
        return "comprehensive_evaluation"
    if pathway_type in {
        "national_special", "local_special", "university_special", "special_program",
    }:
        return "special_program"
    if pathway_type in {
        "public_funded_teacher", "excellent_teacher", "directed_medical",
        "public_funded_or_directed",
    }:
        return "service_oriented"
    if pathway_type in {"military", "police_judicial_fire", "maritime_aviation"}:
        return "uniformed_service"
    if pathway_type in {"hong_kong_macao", "sino_foreign"}:
        return "cross_border"
    if pathway_type == "arts_sports":
        return "arts_sports"
    return "special_program"


def _text_matches(options: tuple[str, ...], targets: tuple[str, ...]) -> bool:
    return any(
        len(target.strip()) >= 2
        and (target.strip() in option or option in target.strip())
        for option in options
        for target in targets
    )


def _requires_service(policy: PathwayPolicy) -> bool:
    if policy.pathway_type not in {
        "public_funded_teacher", "excellent_teacher", "directed_medical",
        "public_funded_or_directed", "military", "police_judicial_fire",
        "maritime_aviation",
    }:
        return False
    statement = policy.service_employment_obligations or ""
    return not any(
        marker in statement for marker in ("无额外服务期", "无服务期", "无额外服务")
    )


def _future_plan_matches(pathway_type: str, future_plan: str) -> bool:
    matches = {
        "postgraduate": {"strong_foundation", "comprehensive_evaluation"},
        "public_service": {
            "public_funded_teacher", "excellent_teacher", "directed_medical",
            "public_funded_or_directed", "national_special", "local_special",
        },
        "overseas": {"hong_kong_macao", "sino_foreign"},
        "employment": {"directed_medical", "public_funded_teacher", "excellent_teacher"},
    }
    return pathway_type in matches.get(future_plan, set())


def _explicit_required_gender(statement: str) -> str | None:
    male = any(marker in statement for marker in ("仅限男生", "只招男生", "限男生"))
    female = any(marker in statement for marker in ("仅限女生", "只招女生", "限女生"))
    if male == female:
        return None
    return "男" if male else "女"


def _explicit_disqualified_gender(statement: str) -> str | None:
    if statement in {"男", "男生", "男性"}:
        return "男"
    if statement in {"女", "女生", "女性"}:
        return "女"
    return None


def _subject_requirement_status(
    statements: tuple[str, ...], selected: set[str]
) -> str:
    known = ("物理", "历史", "化学", "生物", "政治", "地理", "技术")
    if not statements:
        return "none"
    uncertain = False
    for statement in statements:
        required = {subject for subject in known if subject in statement}
        grammar = "".join(statement.split())
        for subject in known:
            grammar = grammar.replace(subject, "")
        pure_any = (
            len(required) >= 2
            and bool(grammar)
            and not grammar.replace("或", "")
        )
        pure_all = (
            len(required) >= 2
            and bool(grammar)
            and not grammar.replace("和", "").replace("及", "").replace("与", "").replace("、", "")
        )
        pure_single = len(required) == 1 and not grammar
        if not required or not (pure_any or pure_all or pure_single):
            uncertain = True
            continue
        if pure_any:
            if not required & selected:
                return "blocked"
        else:
            if not required <= selected:
                return "blocked"
    return "uncertain" if uncertain else "match"


def _full_profile_reasons(
    profile: Any,
    policy: PathwayPolicy,
    rank_scenario: Any,
    *,
    has_ineligible: bool,
    has_missing_eligibility: bool,
    eligibility_input_fields: tuple[str, ...],
    evidence_problem: str | None,
    historical: bool,
    decision_policy: DecisionPolicySnapshot,
) -> tuple[DecisionReason, ...]:
    source_ids = tuple(policy.policy_source_ids)

    def reason(
        code: str,
        explanation: str,
        sources: tuple[str, ...] = (),
        *,
        input_fields: tuple[str, ...],
    ) -> DecisionReason:
        return DecisionReason.create(
            profile,
            code=code,
            explanation=explanation,
            input_fields=input_fields,
            source_ids=sources,
        )

    if has_ineligible:
        eligibility = reason(
            "PATH_ELIGIBILITY_BLOCKED",
            "画像命中认证政策硬性排除条件",
            input_fields=eligibility_input_fields,
        )
    elif has_missing_eligibility:
        eligibility = reason(
            "PATH_ELIGIBILITY_REQUIREMENT_MISSING",
            "认证政策资格条件尚未由画像事实完整满足",
            input_fields=eligibility_input_fields,
        )
    else:
        eligibility = reason(
            "PATH_ELIGIBILITY_SATISFIED",
            "认证政策基础资格条件已由画像事实满足",
            input_fields=eligibility_input_fields,
        )

    selected = {profile.subject_group, *profile.secondary_subjects}
    subject_status = _subject_requirement_status(
        tuple(policy.subject_requirements or ()), selected
    )
    required_grades = {
        grade
        for statement in (policy.grade_requirements or ())
        for grade in ("高一", "高二", "高三")
        if grade in statement
    }
    strength_match = _text_matches(
        tuple(policy.subject_requirements) + tuple(policy.professional_options),
        profile.preparation_assets.subject_strengths,
    )
    required_subject_names = {
        subject
        for statement in policy.subject_requirements
        for subject in ("物理", "历史", "化学", "生物", "政治", "地理", "技术")
        if subject in statement
    }
    subject_input_fields = (
        *(
            ("subject_group",)
            if required_subject_names
            & (
                {"物理", "历史"}
                if profile.subject_mode == "3+1+2"
                else required_subject_names
            )
            else ()
        ),
        *(
            ("secondary_subjects",)
            if required_subject_names
            - ({"物理", "历史"} if profile.subject_mode == "3+1+2" else set())
            else ()
        ),
    )
    if required_grades and profile.grade not in required_grades:
        academic = reason(
            "PATH_ACADEMIC_GRADE_BLOCKED",
            "当前年级与认证政策明确列出的年级要求不相符",
            source_ids,
            input_fields=("grade",),
        )
    elif subject_status == "blocked":
        academic = reason(
            "PATH_ACADEMIC_SUBJECT_BLOCKED",
            "认证政策明确要求的选科未被画像选科覆盖",
            source_ids,
            input_fields=subject_input_fields,
        )
    elif subject_status == "uncertain":
        academic = reason(
            "PATH_ACADEMIC_SUBJECT_UNCERTAIN",
            "认证选科要求语法不能保守确定为合取或析取，需复核原文",
            source_ids,
            input_fields=subject_input_fields,
        )
    elif required_grades or subject_status == "match" or strength_match:
        academic_inputs = (
            *(("grade",) if required_grades else ()),
            *(subject_input_fields if subject_status == "match" else ()),
            *(("preparation_assets.subject_strengths",) if strength_match else ()),
        )
        academic = reason(
            "PATH_ACADEMIC_MATCH",
            "当前年级、已确认选科或路径相关学科优势与认证要求相符",
            tuple(sorted(set(source_ids) | set(getattr(rank_scenario, "source_ids", ())))),
            input_fields=academic_inputs,
        )
    else:
        academic = reason(
            "PATH_ACADEMIC_UNVERIFIED",
            "学科优势或认证位次不足以形成清晰学业匹配",
            source_ids,
            input_fields=("preparation_assets.subject_strengths",),
        )

    preference_key = _pathway_preference_key(policy.pathway_type)
    preference_field = f"pathway_preferences.{preference_key}"
    preference = profile.pathway_preferences[preference_key]
    major_match = _text_matches(policy.professional_options, profile.target_majors)
    school_match = _text_matches((policy.institution,), profile.target_schools)
    future_match = _future_plan_matches(policy.pathway_type, profile.future_plan)
    if preference in {"not_interested", "not_applicable"}:
        interest = reason(
            "PATH_INTEREST_REJECTED",
            "画像明确不投入或不适用该路径",
            input_fields=(preference_field,),
        )
    elif preference == "interested" or major_match or future_match:
        interest_inputs = (
            *((preference_field,) if preference == "interested" else ()),
            *(("priorities.target_majors",) if major_match else ()),
            *(("priorities.future_plan",) if future_match else ()),
        )
        interest = reason(
            "PATH_INTEREST_DECLARED",
            "路径偏好、目标专业或未来计划至少一项明确匹配",
            input_fields=interest_inputs,
        )
    else:
        interest = reason(
            "PATH_INTEREST_UNVERIFIED",
            "路径兴趣、目标专业与未来计划尚未形成明确匹配",
            input_fields=(
                "priorities.target_majors",
                "priorities.future_plan",
                preference_field,
            ),
        )

    negative_requirement_markers = ("未要求", "无需", "不要求")
    award_required = bool(policy.award_requirements) and not all(
        any(marker in item for marker in negative_requirement_markers)
        for item in policy.award_requirements
    )
    active_activity_requirements = tuple(
        item
        for item in policy.activity_requirements
        if not any(marker in item for marker in negative_requirement_markers)
    )
    research_required = any(
        any(marker in item for marker in ("研究", "科研", "课题"))
        for item in active_activity_requirements
    )
    activity_required = any(
        any(marker in item for marker in ("活动", "实践", "志愿"))
        for item in active_activity_requirements
    )
    generic_activity_required = bool(active_activity_requirements) and not (
        research_required or activity_required
    )
    award_gap = award_required and not profile.preparation_assets.awards
    research_gap = (
        research_required and not profile.preparation_assets.research_experiences
    )
    activity_gap = activity_required and not profile.preparation_assets.activities
    generic_activity_gap = generic_activity_required and not (
        profile.preparation_assets.activities
        or profile.preparation_assets.research_experiences
    )
    readiness_texts = tuple(
        policy.eligibility_requirements
        + policy.award_requirements
        + policy.activity_requirements
        + policy.application_materials
        + policy.preparation_actions
    )

    def skill_required(markers: tuple[str, ...]) -> bool:
        return any(
            any(marker in statement for marker in markers)
            and not any(
                negative in statement for negative in negative_requirement_markers
            )
            for statement in readiness_texts
        )

    skill_states = tuple(
        (field, state)
        for relevant, field, state in (
            (
                skill_required(("英语", "英文", "雅思", "托福")),
                "preparation_assets.english_readiness",
                profile.preparation_assets.english_readiness,
            ),
            (
                skill_required(("面试", "答辩")),
                "preparation_assets.interview_readiness",
                profile.preparation_assets.interview_readiness,
            ),
            (
                skill_required(("体能", "体测", "体育测试")),
                "preparation_assets.physical_readiness",
                profile.preparation_assets.physical_readiness,
            ),
        )
        if relevant
    )
    readiness_input_fields = (
        *(("preparation_assets.awards",) if award_required else ()),
        *(("preparation_assets.research_experiences",) if research_required else ()),
        *(("preparation_assets.activities",) if activity_required else ()),
        *(
            ("preparation_assets.activities",)
            if generic_activity_required and profile.preparation_assets.activities
            else ("preparation_assets.research_experiences",)
            if generic_activity_required and profile.preparation_assets.research_experiences
            else (
                "preparation_assets.research_experiences",
                "preparation_assets.activities",
            )
            if generic_activity_required
            else ()
        ),
        *(field for field, _state in skill_states),
    )
    relevant_readiness = (
        award_required
        or research_required
        or activity_required
        or generic_activity_required
        or bool(skill_states)
    )
    if award_gap or research_gap or activity_gap or generic_activity_gap or any(
        state == "not_ready" for _field, state in skill_states
    ):
        readiness = reason(
            "PATH_READINESS_GAP",
            "认证准备要求与现有奖项、活动或能力准备之间存在缺口",
            source_ids,
            input_fields=readiness_input_fields,
        )
    elif relevant_readiness and skill_states and any(
        state in {"unknown", "developing"} for _field, state in skill_states
    ):
        readiness = reason(
            "PATH_READINESS_GAP",
            "认证能力准备要求仍处于待确认或发展阶段",
            source_ids,
            input_fields=readiness_input_fields,
        )
    elif relevant_readiness:
        readiness = reason(
            "PATH_READINESS_READY",
            "已有与认证要求对应的准备资产或能力准备可支持继续投入",
            source_ids,
            input_fields=readiness_input_fields,
        )
    else:
        readiness = reason(
            "PATH_READINESS_UNVERIFIED",
            "当前画像没有足够准备资产形成清晰判断",
            source_ids,
            input_fields=(),
        )

    if profile.grade == "高三" and policy.timeline:
        urgency = reason(
            "PATH_URGENCY_CURRENT",
            "当前年级且认证时间线要求近期复核或准备",
            source_ids,
            input_fields=("grade",),
        )
    elif profile.grade in {"高一", "高二"}:
        urgency = reason(
            "PATH_URGENCY_EARLY",
            "当前年级仍有准备时间，需按认证时间线滚动复核",
            source_ids,
            input_fields=("grade",),
        )
    else:
        urgency = reason(
            "PATH_URGENCY_UNVERIFIED",
            "认证政策未提供可判定时间线",
            source_ids,
            input_fields=("grade",),
        )

    service_required = _requires_service(policy)
    burden_concern = any(
        marker in concern
        for concern in profile.concerns
        for marker in (
            "申请", "材料", "准备", "时间", "费用", "预算",
            "服务", "就业", "异地", "违约", "退出",
        )
    )
    if service_required and profile.constraints.service_commitment == "reject":
        burden = reason(
            "PATH_SERVICE_REJECTED",
            "画像明确拒绝该认证政策包含的服务约定",
            source_ids,
            input_fields=("constraints.service_commitment",),
        )
    elif profile.constraints.budget_level in {"limited", "moderate"}:
        burden = reason(
            "PATH_AFFORDABILITY_UNVERIFIED",
            "政策仅提供费用文字，尚无与画像预算档位可直接比较的认证金额",
            source_ids,
            input_fields=("constraints.budget_level",),
        )
    elif burden_concern:
        burden = reason(
            "PATH_BURDEN_UNVERIFIED",
            "画像明确提出与申请、费用、时间或服务投入相关的家庭关切，需专项核实",
            source_ids,
            input_fields=("priorities.concerns",),
        )
    elif service_required and profile.constraints.service_commitment == "accept":
        burden = reason(
            "PATH_SERVICE_ACCEPTED",
            "画像明确接受该认证政策包含的服务约定",
            source_ids,
            input_fields=("constraints.service_commitment",),
        )
    elif (policy.preparation_actions or policy.application_materials) and readiness.code in {
        "PATH_READINESS_GAP", "PATH_READINESS_UNVERIFIED",
    }:
        burden = reason(
            "PATH_EFFORT_GAP",
            "认证准备动作与当前准备程度之间存在时间或投入缺口",
            source_ids,
            input_fields=readiness.input_fields,
        )
    elif profile.constraints.budget_level == "flexible" and (
        not service_required or profile.constraints.service_commitment in {"accept", "consider"}
    ):
        burden = reason(
            "PATH_BURDEN_ACCEPTABLE",
            "预算与服务承诺未形成已知阻断",
            source_ids,
            input_fields=(
                "constraints.budget_level",
                *(("constraints.service_commitment",) if service_required else ()),
            ),
        )
    else:
        burden_inputs = (
            "constraints.budget_level",
            *(("constraints.service_commitment",) if service_required else ()),
            "priorities.concerns",
            *(
                readiness.input_fields
                if (policy.preparation_actions or policy.application_materials)
                else ()
            ),
        )
        burden = reason(
            "PATH_BURDEN_UNVERIFIED",
            "费用、服务或准备投入仍需进一步确认",
            source_ids,
            input_fields=burden_inputs,
        )

    wants_pathway_output = any("路径" in item for item in profile.desired_outcomes)
    major_committed = major_match and bool(profile.target_major_reasons)
    school_committed = school_match and bool(profile.target_school_reasons)
    committed_target = major_committed or school_committed
    if committed_target:
        strategic_inputs = (
            *(
                ("priorities.target_majors", "target_major_reasons")
                if major_committed
                else ()
            ),
            *(
                ("priorities.target_schools", "target_school_reasons")
                if school_committed
                else ()
            ),
        )
        strategic = reason(
            "PATH_STRATEGIC_COMMITTED",
            "路径命中已确认目标，且画像记录了对应目标承诺理由",
            input_fields=strategic_inputs,
        )
    elif major_match or school_match or future_match or wants_pathway_output:
        strategic_inputs = (
            *(
                ("priorities.target_majors", "target_major_reasons")
                if major_match
                else ()
            ),
            *(
                ("priorities.target_schools", "target_school_reasons")
                if school_match
                else ()
            ),
            *(("priorities.future_plan",) if future_match else ()),
            *(("priorities.desired_outcomes",) if wants_pathway_output else ()),
        )
        strategic = reason(
            "PATH_STRATEGIC_MATCH",
            "目标院校、目标专业、未来计划或期望交付支持评估该路径的战略价值",
            input_fields=strategic_inputs,
        )
    else:
        strategic = reason(
            "PATH_STRATEGIC_UNVERIFIED",
            "家庭关切与长期目标尚不足以确认该路径的战略优先级",
            input_fields=(
                "priorities.target_schools",
                "priorities.target_majors",
                "priorities.future_plan",
                "priorities.desired_outcomes",
            ),
        )

    if evidence_problem is not None:
        evidence = reason(
            "PATH_EVIDENCE_UNRESOLVED",
            "政策证据未达到可作明确判断的门槛",
            source_ids,
            input_fields=(),
        )
    elif historical:
        evidence = reason(
            "PATH_EVIDENCE_HISTORICAL",
            "认证政策来自历史回退，必须复核目标年份",
            source_ids,
            input_fields=(),
        )
    elif policy.evidence_status is EvidenceStatus.OFFICIAL:
        evidence = reason(
            "PATH_EVIDENCE_OFFICIAL",
            "当前政策由官方来源认证",
            source_ids,
            input_fields=(),
        )
    elif policy.evidence_status is EvidenceStatus.CORROBORATED:
        evidence = reason(
            "PATH_EVIDENCE_CORROBORATED",
            "当前政策由独立第三方交叉印证",
            source_ids,
            input_fields=(),
        )
    else:
        evidence = reason(
            "PATH_EVIDENCE_REFERENCE",
            "当前政策达到多源参考门槛并明确标注",
            source_ids,
            input_fields=(),
        )

    by_dimension = {
        item.dimension: item
        for item in (
            eligibility, academic, interest, readiness, urgency, burden, strategic, evidence
        )
    }
    return tuple(by_dimension[name] for name in decision_policy.pathway_reason_order)


def _policy_field_evidence_index(
    policy: PathwayPolicy,
    *,
    allow_legacy: bool,
) -> dict[str, PathwayFieldEvidence]:
    if policy.field_evidence:
        context_binding = policy.field_evidence[0].context_binding
        records = validate_pathway_field_evidence(
            policy.field_evidence,
            PATHWAY_POLICY_EVIDENCE_FIELDS,
            owner="pathway policy",
            field_values=pathway_policy_field_values(policy),
            context_binding=context_binding,
        )
        if not allow_legacy and any(
            item.origin is not PathwayFieldEvidenceOrigin.POLICY_SOURCE
            for item in records
        ):
            raise ValueError(
                "full planning profile policies require authenticated policy-source trails"
            )
        return {item.field: item for item in records}
    if not allow_legacy:
        raise ValueError(
            "full planning profile policies require field-bound evidence"
        )
    coverage = {
        EvidenceStatus.OFFICIAL: "complete",
        EvidenceStatus.CORROBORATED: "complete",
        EvidenceStatus.REFERENCE: "complete",
        EvidenceStatus.CONFLICT: "conflict",
        EvidenceStatus.MISSING: "missing",
        EvidenceStatus.MASKED: "missing",
    }.get(policy.evidence_status, "partial")
    context_binding = _pathway_field_context_binding(
        {
            "legacy_policy": pathway_policy_internal_payload(policy),
            "policy_id": policy.policy_id,
        }
    )
    values = pathway_policy_field_values(policy)
    return {
        field: _create_pathway_field_evidence(
            field=field,
            value=values[field],
            origin=PathwayFieldEvidenceOrigin.LEGACY,
            context_binding=context_binding,
            origin_payload={"policy_id": policy.policy_id, "field": field},
            status=policy.evidence_status,
            coverage=coverage,
            source_ids=policy.policy_source_ids,
            locators=(f"policy-record:{policy.policy_id}:{field}",),
            extraction_methods=("legacy-policy-record",),
            evidence_method="legacy-policy-field-v1",
            upstream_fields=(field,),
        )
        for field in PATHWAY_POLICY_EVIDENCE_FIELDS
    }


def _derived_field_evidence(
    field: str,
    value: Any,
    upstream_fields: tuple[str, ...],
    policy_index: dict[str, PathwayFieldEvidence],
    *,
    origin_payload: Any,
    context_binding: str,
    profile_fields: tuple[str, ...] = (),
    source_ids: tuple[str, ...] | None = None,
    locators: tuple[str, ...] | None = None,
    extraction_methods: tuple[str, ...] | None = None,
    declared_upstream_fields: tuple[str, ...] | None = None,
) -> PathwayFieldEvidence:
    records = tuple(policy_index[name] for name in upstream_fields)
    return _create_pathway_field_evidence(
        field=field,
        value=value,
        origin=PathwayFieldEvidenceOrigin.DERIVED_DECISION,
        context_binding=context_binding,
        origin_payload=origin_payload,
        status=EvidenceStatus.INFERRED,
        coverage=(
            "complete"
            if all(item.coverage == "complete" for item in records)
            else "partial"
        ),
        source_ids=(
            tuple(sorted({source for item in records for source in item.source_ids}))
            if source_ids is None else source_ids
        ),
        locators=(
            tuple(sorted({locator for item in records for locator in item.locators}))
            if locators is None else locators
        ),
        extraction_methods=(
            tuple(sorted({method for item in records for method in item.extraction_methods}))
            if extraction_methods is None else extraction_methods
        ),
        evidence_method=f"pathway-{field.replace('_', '-')}-v1",
        upstream_fields=declared_upstream_fields or upstream_fields,
        profile_fields=profile_fields,
        upstream_evidence=records,
        warnings=tuple(dict.fromkeys(warning for item in records for warning in item.warnings)),
    )


def _item_field_evidence(
    policy: PathwayPolicy,
    reasons: tuple[DecisionReason, ...],
    *,
    allow_legacy: bool,
    field_values: dict[str, Any],
    research_year: int,
    target_rank: int | None,
    transformation: str | None,
    model: RankAdjustmentModel | None,
    rank_scenario: Any,
) -> tuple[PathwayFieldEvidence, ...]:
    index = _policy_field_evidence_index(policy, allow_legacy=allow_legacy)
    context_binding = next(iter(index.values())).context_binding
    direct_fields = {
        "institution", "professional_options", "training_arrangements", "transition_rules",
        "outcomes", "service_employment_obligations", "penalty_exit_rules",
        "fees_and_subsidies", "timeline", "preparation_actions",
    }
    eligibility_inputs = (
        "province", "subject_mode", "data_year", "eligibility_requirements",
        "grade_requirements", "subject_requirements", "award_requirements",
        "activity_requirements", "disqualifying_facts", "professional_options",
        "training_arrangements", "transition_rules", "outcomes",
        "service_employment_obligations", "penalty_exit_rules",
        "fees_and_subsidies",
    )
    all_policy_inputs = PATHWAY_POLICY_EVIDENCE_FIELDS
    reason_profile_fields = tuple(
        sorted({field for reason in reasons for field in reason.input_fields})
    )
    result: list[PathwayFieldEvidence] = []
    for field in PATHWAY_DISPLAY_EVIDENCE_FIELDS:
        if field == "title":
            if not allow_legacy:
                projection = policy._authenticated_projection
                task = projection.input_projection["task"]
                result.append(
                    _create_pathway_field_evidence(
                        field=field,
                        value=field_values[field],
                        origin=PathwayFieldEvidenceOrigin.QUERY_CONTEXT,
                        context_binding=context_binding,
                        origin_payload={
                            "projection_digest": projection.digest,
                            "task": task,
                            "field": "target_name",
                        },
                        status=EvidenceStatus.INFERRED,
                        coverage="complete",
                        source_ids=policy.policy_source_ids,
                        locators=(f"query-task:{task['task_id']}/target_name",),
                        extraction_methods=("authenticated-query-plan",),
                        evidence_method="query-plan-pathway-title-v2",
                        upstream_fields=("query_task.target_name",),
                    )
                )
            else:
                source = index["institution"]
                result.append(
                    _create_pathway_field_evidence(
                        field=field,
                        value=field_values[field],
                        origin=PathwayFieldEvidenceOrigin.LEGACY,
                        context_binding=context_binding,
                        origin_payload={"policy_id": policy.policy_id, "field": "title"},
                        status=EvidenceStatus.INFERRED,
                        coverage=source.coverage,
                        source_ids=source.source_ids,
                        locators=(f"policy-record:{policy.policy_id}:title",),
                        extraction_methods=("legacy-policy-record",),
                        evidence_method="legacy-pathway-title-v1",
                        upstream_fields=("title",),
                    )
                )
            continue
        if field in {"evidence_status", "source_ids"}:
            records = tuple(index[name] for name in all_policy_inputs)
            coverage = (
                "complete"
                if all(item.coverage == "complete" for item in records)
                else "partial"
            )
            result.append(
                _create_pathway_field_evidence(
                    field=field,
                    value=field_values[field],
                    origin=PathwayFieldEvidenceOrigin.DERIVED_DECISION,
                    context_binding=context_binding,
                    origin_payload={
                        "policy_id": policy.policy_id,
                        "evidence_status": policy.evidence_status.value,
                        "source_ids": list(policy.policy_source_ids),
                    },
                    status=EvidenceStatus.INFERRED,
                    coverage=coverage,
                    source_ids=tuple(
                        sorted({source for item in records for source in item.source_ids})
                    ),
                    locators=tuple(
                        sorted({locator for item in records for locator in item.locators})
                    ),
                    extraction_methods=tuple(
                        sorted({method for item in records for method in item.extraction_methods})
                    ),
                    evidence_method=f"pathway-{field.replace('_', '-')}-v2",
                    upstream_fields=all_policy_inputs,
                    upstream_evidence=records,
                    warnings=tuple(
                        dict.fromkeys(
                            warning for item in records for warning in item.warnings
                        )
                    ),
                )
            )
            continue
        if field in direct_fields:
            source = index[field]
            result.append(
                _create_pathway_field_evidence(
                    field=field,
                    value=field_values[field],
                    origin=source.origin,
                    context_binding=context_binding,
                    origin_payload={
                        "policy_field": field,
                        "policy_field_evidence_digest": source.digest,
                    },
                    status=source.status,
                    coverage=source.coverage,
                    source_ids=source.source_ids,
                    locators=source.locators,
                    extraction_methods=source.extraction_methods,
                    evidence_method=source.evidence_method,
                    upstream_fields=source.upstream_fields,
                    profile_fields=source.profile_fields,
                    upstream_evidence=(source,),
                    warnings=source.warnings,
                )
            )
            continue
        dependencies = (
            ("eligibility_requirements", "disqualifying_facts")
            if field == "satisfied_conditions"
            else ("data_year",)
            if field in {"year_basis", "calculation_basis"}
            else eligibility_inputs
            if field in {
                "status", "eligibility", "qualification_status",
                "missing_constraints",
            }
            else all_policy_inputs
        )
        origin_payload: dict[str, Any] = {
            "policy_id": policy.policy_id,
            "field": field,
            "decision_reasons": [item.to_dict() for item in reasons],
        }
        derived_sources: tuple[str, ...] | None = None
        derived_locators: tuple[str, ...] | None = None
        derived_methods: tuple[str, ...] | None = None
        declared_upstream_fields: tuple[str, ...] | None = None
        profile_fields = (
            ("query_plan.research_year",)
            if field == "year_basis"
            else reason_profile_fields
            if field in {
                "investment_decision", "status", "eligibility",
                "qualification_status", "satisfied_conditions", "missing_constraints",
                "decision_reasons", "calculation_basis",
            }
            else ()
        )
        if field == "year_basis":
            projection = policy._authenticated_projection
            task = None if projection is None else projection.input_projection["task"]
            origin_payload.update(
                {
                    "year_basis": policy.year_basis,
                    "target_year": policy.target_year,
                    "data_year": policy.data_year,
                    "fallback_distance": policy.fallback_distance,
                    "research_year": research_year,
                    "query_task_digest": None if task is None else task["task_digest"],
                }
            )
            declared_upstream_fields = (
                "data_year", "query_task.target_year", "query_plan.research_year",
            )
            if task is not None:
                derived_locators = (
                    *index["data_year"].locators,
                    f"query-task:{task['task_id']}/target_year",
                )
                derived_methods = tuple(
                    sorted(
                        {
                            *index["data_year"].extraction_methods,
                            "authenticated-query-plan",
                        }
                    )
                )
        elif field == "calculation_basis":
            scenario_payload = (
                None if rank_scenario is None else rank_scenario.to_dict()
            )
            origin_payload.update(
                {
                    "target_rank": target_rank,
                    "transformation": transformation,
                    "rank_scenario": scenario_payload,
                    "rank_model": None if model is None else model.to_dict(),
                }
            )
            if rank_scenario is not None:
                derived_sources = tuple(
                    sorted(
                        set(policy.policy_source_ids)
                        | set(rank_scenario.source_ids)
                    )
                )
                scenario_locator = (
                    "rank-scenario:"
                    + _pathway_digest(scenario_payload)[7:23]
                )
                derived_locators = (
                    *index["data_year"].locators,
                    scenario_locator,
                )
                derived_methods = tuple(
                    sorted(
                        {
                            *index["data_year"].extraction_methods,
                            rank_scenario.basis,
                        }
                    )
                )
                declared_upstream_fields = (
                    "data_year", "rank_scenario.status",
                    "rank_scenario.source_ids", "rank_scenario.basis",
                    "rank_scenario.central_rank",
                )
            if model is not None and target_rank is not None:
                derived_sources = tuple(
                    sorted(
                        set(policy.policy_source_ids)
                        | set(model.source_ids)
                        | (
                            set()
                            if rank_scenario is None
                            else set(rank_scenario.source_ids)
                        )
                    )
                )
                derived_locators = (
                    *index["data_year"].locators,
                    *(
                        ()
                        if rank_scenario is None
                        else (
                            "rank-scenario:"
                            + _pathway_digest(scenario_payload)[7:23],
                        )
                    ),
                    f"rank-model:{model.model_id}",
                )
                derived_methods = tuple(
                    sorted(
                        {
                            *index["data_year"].extraction_methods,
                            model.method,
                        }
                    )
                )
                declared_upstream_fields = (
                    "data_year", "rank_scenario.status",
                    "rank_scenario.source_ids", "rank_scenario.basis",
                    "rank_scenario.central_rank", "rank_model.source_ids",
                    "rank_model.evidence_status", "rank_model.method",
                    "rank_model.model_id", "rank_model.cohort_years",
                )
        result.append(
            _derived_field_evidence(
                field,
                field_values[field],
                tuple(dependencies),
                index,
                origin_payload=origin_payload,
                context_binding=context_binding,
                profile_fields=profile_fields,
                source_ids=derived_sources,
                locators=derived_locators,
                extraction_methods=derived_methods,
                declared_upstream_fields=declared_upstream_fields,
            )
        )
    return tuple(result)


def _evaluate_policy(
    profile: PathwayProfile,
    policy: PathwayPolicy,
    target_rank: int | None,
    transformation: str | None,
    *,
    full_profile: Any = None,
    rank_scenario: Any = None,
    decision_policy: DecisionPolicySnapshot | None = None,
    model: RankAdjustmentModel | None = None,
) -> PathwayItem:
    missing: list[str] = []
    ineligible: list[str] = []
    if policy.province != profile.province:
        ineligible.append("政策省份与用户省份不匹配")
    if policy.subject_mode != profile.subject_mode:
        ineligible.append("政策选科模式与用户选科模式不匹配")
    matched_disqualifiers = set(policy.disqualifying_facts).intersection(
        profile.eligibility_facts
    )
    gender_satisfied: set[str] = set()
    eligibility_input_fields: list[str] = []
    if policy.eligibility_requirements or matched_disqualifiers:
        eligibility_input_fields.append("eligibility_facts")
    if full_profile is not None:
        matched_health = set(policy.disqualifying_facts).intersection(
            full_profile.constraints.health_constraints
        )
        matched_gender = {
            statement
            for statement in policy.disqualifying_facts
            if _explicit_disqualified_gender(statement) == full_profile.gender
        }
        matched_disqualifiers.update(matched_health)
        matched_disqualifiers.update(matched_gender)
        if matched_health:
            eligibility_input_fields.append("constraints.health_constraints")
        if matched_gender:
            eligibility_input_fields.append("gender")
        for requirement in policy.eligibility_requirements:
            required_gender = _explicit_required_gender(requirement)
            if required_gender is None:
                continue
            if "gender" not in eligibility_input_fields:
                eligibility_input_fields.append("gender")
            if full_profile.gender == required_gender:
                gender_satisfied.add(requirement)
            elif full_profile.gender in {"男", "女"}:
                ineligible.append("画像性别与认证政策明确性别要求不相符")
    ineligible.extend(
        f"命中排除条件：{item}" for item in sorted(matched_disqualifiers)
    )

    eligibility_missing = [
        item
        for item in policy.eligibility_requirements
        if item not in profile.eligibility_facts and item not in gender_satisfied
    ]
    missing.extend(eligibility_missing)
    satisfied = tuple(
        item
        for item in policy.eligibility_requirements
        if item in profile.eligibility_facts or item in gender_satisfied
    )
    critical_fields = (
        ("training_arrangements", "培养安排未核实"),
        ("transition_rules", "转段规则未核实"),
        ("outcomes", "毕业或升学出口未核实"),
        ("service_employment_obligations", "服务期或就业义务未核实"),
        ("penalty_exit_rules", "违约或退出规则未核实"),
        ("fees_and_subsidies", "费用或补助未核实"),
    )
    missing.extend(
        label for field_name, label in critical_fields if getattr(policy, field_name) is None
    )
    if not policy.professional_options:
        missing.append("专业选项未核实")
    historical = policy.fallback_distance > 0
    if policy.valid_year is None:
        missing.append("政策有效年份未核实")
    elif policy.target_year != profile.current_year:
        missing.append("政策目标年份与用户规划年份不一致")
    elif historical:
        missing.append(f"政策为历史回退版本：{policy.data_year}")
    evidence_problem = _exact_evidence_problem(
        policy.evidence_status, policy.policy_source_ids, "政策"
    )
    if evidence_problem is not None:
        missing.append(evidence_problem)

    missing_eligibility = bool(eligibility_missing)
    reasons: tuple[DecisionReason, ...] = ()
    if full_profile is not None:
        assert decision_policy is not None
        reasons = _full_profile_reasons(
            full_profile,
            policy,
            rank_scenario,
            has_ineligible=bool(ineligible),
            has_missing_eligibility=missing_eligibility,
            eligibility_input_fields=tuple(eligibility_input_fields),
            evidence_problem=evidence_problem,
            historical=historical,
            decision_policy=decision_policy,
        )
        reason_by_dimension = {item.dimension: item for item in reasons}
        profile_blocks = tuple(
            item for item in reasons
            if item.effect == "blocks"
            and item.dimension in {"eligibility", "academic_fit", "interest_fit", "burden"}
        )
        if profile_blocks:
            ineligible.extend(item.explanation for item in profile_blocks)

    if ineligible:
        status = "excluded"
        eligibility = "ineligible"
        constraints = tuple(ineligible + missing)
        investment_decision = "不建议"
        qualification_status = "不适用"
    elif missing:
        status = "pending_verification"
        eligibility = "pending_verification"
        constraints = tuple(missing)
        if full_profile is not None:
            interest_reason = reason_by_dimension["interest_fit"]
            academic_reason = reason_by_dimension["academic_fit"]
            readiness_reason = reason_by_dimension["readiness"]
            if evidence_problem is not None:
                investment_decision = "观察"
            elif missing_eligibility:
                investment_decision = "备选"
            elif (
                interest_reason.effect == "supports"
                and academic_reason.effect == "supports"
                and readiness_reason.effect == "supports"
            ):
                investment_decision = "重点准备"
            elif interest_reason.effect == "supports":
                investment_decision = "备选"
            else:
                investment_decision = "观察"
            qualification_status = (
                "部分满足" if missing_eligibility and satisfied else
                "暂未满足" if missing_eligibility else
                "待核验"
            )
        elif evidence_problem is not None:
            investment_decision = "观察"
            qualification_status = "待核验"
        elif historical:
            investment_decision = "重点准备"
            qualification_status = "待核验"
        elif any(
            requirement not in profile.eligibility_facts
            for requirement in policy.eligibility_requirements
        ):
            investment_decision = "备选"
            qualification_status = "部分满足" if satisfied else "暂未满足"
        else:
            investment_decision = "观察"
            qualification_status = "待核验"
    else:
        status = "formal"
        eligibility = "eligible"
        constraints = ()
        if full_profile is None:
            investment_decision = "观察"
        else:
            interest_reason = reason_by_dimension["interest_fit"]
            academic_reason = reason_by_dimension["academic_fit"]
            readiness_reason = reason_by_dimension["readiness"]
            burden_reason = reason_by_dimension["burden"]
            strategic_reason = reason_by_dimension["strategic_value"]
            evidence_reason = reason_by_dimension["evidence_quality"]
            if (
                interest_reason.effect == "supports"
                and academic_reason.effect == "supports"
                and readiness_reason.effect == "supports"
                and burden_reason.effect == "supports"
                and strategic_reason.effect == "supports"
                and evidence_reason.effect == "supports"
            ):
                investment_decision = "主攻"
            elif interest_reason.effect == "supports" and readiness_reason.effect == "supports":
                investment_decision = "重点准备"
            elif interest_reason.effect == "supports":
                investment_decision = "备选"
            else:
                investment_decision = "观察"
        qualification_status = "已满足"
    basis = policy.calculation_basis
    item_target_rank = target_rank if status == "formal" else None
    if transformation is not None and status == "formal":
        basis = f"{basis}；{transformation}"
    else:
        basis = f"{basis}；未执行位次换算"
    if historical:
        basis = (
            f"{basis}；历史回退 {policy.data_year}→{policy.target_year}，"
            "仅用于规划，不确认当年资格"
        )
    item_field_values = {
        "title": policy.title,
        "institution": policy.institution,
        "investment_decision": investment_decision,
        "qualification_status": qualification_status,
        "status": status,
        "eligibility": eligibility,
        "evidence_status": policy.evidence_status,
        "source_ids": policy.policy_source_ids,
        "professional_options": policy.professional_options,
        "training_arrangements": policy.training_arrangements,
        "transition_rules": policy.transition_rules,
        "outcomes": policy.outcomes,
        "service_employment_obligations": policy.service_employment_obligations,
        "penalty_exit_rules": policy.penalty_exit_rules,
        "fees_and_subsidies": policy.fees_and_subsidies,
        "satisfied_conditions": satisfied,
        "missing_constraints": constraints,
        "timeline": policy.timeline,
        "preparation_actions": policy.preparation_actions,
        "decision_reasons": reasons,
        "year_basis": {
            "year_basis": policy.year_basis,
            "target_year": policy.target_year,
            "data_year": policy.data_year,
            "fallback_distance": policy.fallback_distance,
        },
        "calculation_basis": basis,
    }
    evidence = _item_field_evidence(
        policy,
        reasons,
        allow_legacy=full_profile is None,
        field_values=item_field_values,
        research_year=profile.current_year,
        target_rank=item_target_rank,
        transformation=transformation,
        model=model,
        rank_scenario=rank_scenario,
    )
    return PathwayItem(
        policy_id=policy.policy_id,
        pathway_type=policy.pathway_type,
        title=policy.title,
        institution=policy.institution,
        status=status,
        eligibility=eligibility,
        missing_constraints=constraints,
        professional_options=policy.professional_options,
        training_arrangements=policy.training_arrangements,
        transition_rules=policy.transition_rules,
        outcomes=policy.outcomes,
        service_employment_obligations=policy.service_employment_obligations,
        penalty_exit_rules=policy.penalty_exit_rules,
        fees_and_subsidies=policy.fees_and_subsidies,
        policy_source_ids=policy.policy_source_ids,
        evidence_status=policy.evidence_status,
        calculation_basis=basis,
        target_rank=item_target_rank,
        investment_decision=investment_decision,
        qualification_status=qualification_status,
        satisfied_conditions=satisfied,
        timeline=policy.timeline,
        preparation_actions=policy.preparation_actions,
        target_year=policy.target_year,
        data_year=policy.data_year,
        fallback_distance=policy.fallback_distance,
        year_basis=policy.year_basis,
        decision_reasons=reasons,
        field_evidence=evidence,
        field_evidence_context=evidence[0].context_binding,
    )
