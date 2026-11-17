"""Build a host-neutral, deterministic research query plan.

The module is deliberately file- and network-free except for its CLI input
boundary.  Query execution belongs to the host; this contract only describes
what must be researched and how missing current-year material is represented.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime, timezone
import hashlib
import ipaddress
import json
import math
import os
from pathlib import Path
import re
import stat
import sys
from types import MappingProxyType
from typing import Any
import unicodedata
from urllib.parse import urlsplit

_MISSING_LOCAL_CAPABILITY: str | None = None

if __package__:
    try:
        from .contracts import OrdinaryBatchPolicy, RecommendationProfile
    except ModuleNotFoundError as error:
        if error.name != f"{__package__}.contracts":
            raise
        _MISSING_LOCAL_CAPABILITY = "contracts"
    if _MISSING_LOCAL_CAPABILITY is None:
        try:
            from .decision_policy import DecisionPolicySnapshot
        except ModuleNotFoundError as error:
            if error.name != f"{__package__}.decision_policy":
                raise
            _MISSING_LOCAL_CAPABILITY = "decision_policy"
    if _MISSING_LOCAL_CAPABILITY is None:
        try:
            from .planning_profile import PlanningProfile, load_planning_profile
        except ModuleNotFoundError as error:
            if error.name != f"{__package__}.planning_profile":
                raise
            _MISSING_LOCAL_CAPABILITY = "planning_profile"
    if _MISSING_LOCAL_CAPABILITY is None:
        try:
            from .path_recommend import validate_public_output_text
        except ModuleNotFoundError as error:
            if error.name != f"{__package__}.path_recommend":
                raise
            _MISSING_LOCAL_CAPABILITY = "path_recommend"
    if _MISSING_LOCAL_CAPABILITY is None:
        try:
            from .year_fallback import year_window
        except ModuleNotFoundError as error:
            if error.name != f"{__package__}.year_fallback":
                raise
            _MISSING_LOCAL_CAPABILITY = "year_fallback"
    if _MISSING_LOCAL_CAPABILITY is None:
        try:
            from .province_registry import (
                ProvinceConfig,
                _parse_config,
                canonical_discovery_subject_key,
                canonical_subject_selection_key,
            )
        except ModuleNotFoundError as error:
            if error.name != f"{__package__}.province_registry":
                raise
            _MISSING_LOCAL_CAPABILITY = "province_registry"
else:  # pragma: no cover - exercised by the real CLI and flat-import tests
    try:
        from contracts import OrdinaryBatchPolicy, RecommendationProfile
    except ModuleNotFoundError as error:
        if error.name != "contracts":
            raise
        _MISSING_LOCAL_CAPABILITY = "contracts"
    if _MISSING_LOCAL_CAPABILITY is None:
        try:
            from decision_policy import DecisionPolicySnapshot
        except ModuleNotFoundError as error:
            if error.name != "decision_policy":
                raise
            _MISSING_LOCAL_CAPABILITY = "decision_policy"
    if _MISSING_LOCAL_CAPABILITY is None:
        try:
            from planning_profile import PlanningProfile, load_planning_profile
        except ModuleNotFoundError as error:
            if error.name != "planning_profile":
                raise
            _MISSING_LOCAL_CAPABILITY = "planning_profile"
    if _MISSING_LOCAL_CAPABILITY is None:
        try:
            from path_recommend import validate_public_output_text
        except ModuleNotFoundError as error:
            if error.name != "path_recommend":
                raise
            _MISSING_LOCAL_CAPABILITY = "path_recommend"
    if _MISSING_LOCAL_CAPABILITY is None:
        try:
            from year_fallback import year_window
        except ModuleNotFoundError as error:
            if error.name != "year_fallback":
                raise
            _MISSING_LOCAL_CAPABILITY = "year_fallback"
    if _MISSING_LOCAL_CAPABILITY is None:
        try:
            from province_registry import (
                ProvinceConfig,
                _parse_config,
                canonical_discovery_subject_key,
                canonical_subject_selection_key,
            )
        except ModuleNotFoundError as error:
            if error.name != "province_registry":
                raise
            _MISSING_LOCAL_CAPABILITY = "province_registry"

if _MISSING_LOCAL_CAPABILITY is not None:
    OrdinaryBatchPolicy = RecommendationProfile = PlanningProfile = ProvinceConfig = None
    DecisionPolicySnapshot = None
    load_planning_profile = None
    validate_public_output_text = _parse_config = canonical_subject_selection_key = None
    canonical_discovery_subject_key = None
    year_window = None


_SCHEMA_VERSION = "1.0"
_KINDS = frozenset(
    {
        "province_policy",
        "score_table",
        "batch_admission",
        "joy_report",
        "enrollment_plan",
        "admission_charter",
        "tuition_fee",
        "subject_requirement",
        "strong_foundation",
        "comprehensive_evaluation",
        "hk_macao_admission",
        "special_pathway",
    }
)
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_FIELD_ID = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
_ENV_REFERENCE = re.compile(
    r"(?i)(?:%[A-Z_][A-Z0-9_]*%|\$[A-Z_][A-Z0-9_]*)"
)
_DRIVE_REFERENCE = re.compile(r"(?i)(?:^|[\s(])[A-Z]:")
_EXPECTATIONS = frozenset(
    {"current_year_availability_must_be_checked", "expected_available"}
)
_FRESHNESS_BY_EXPECTATION = {
    "current_year_availability_must_be_checked": "verify_exact_current_year_availability",
    "expected_available": "query_exact_expected_available_year",
}
_STOP_CONDITIONS = ("accepted", "candidate-cap", "variants-exhausted", "unavailable")
_UNAVAILABLE_REASONS = (
    "current_year_not_published",
    "source_threshold_not_met",
    "source_conflict",
    "network_unavailable",
    "capability_unavailable",
    "newer_comparable_year_accepted",
)
_GENERIC_KIND_SYNONYMS = {
    "joy_report": ("高中喜报", "高考光荣榜", "高中升学成果"),
}
MAX_PROVINCE_ALIASES = 3
_CATALOG_FIELDS = frozenset(
    {"schema_version", "verified_at", "coverage_note", "mode_authority_urls", "provinces"}
)
_CATALOG_RECORD_FIELDS = frozenset(
    {
        "province",
        "aliases",
        "mode",
        "authority_name",
        "official_roots",
        "mode_source_url",
        "verified_at",
        "notes",
    }
)
_CATALOG_PROVINCES = (
    "北京", "天津", "上海", "浙江", "山东", "海南", "河北", "山西", "内蒙古",
    "辽宁", "吉林", "黑龙江", "江苏", "安徽", "福建", "江西", "河南", "湖北",
    "湖南", "广东", "广西", "重庆", "四川", "贵州", "云南", "陕西", "甘肃",
    "青海", "宁夏",
)
_CATALOG_MODES = {
    **{name: "3+3" for name in _CATALOG_PROVINCES[:6]},
    **{name: "3+1+2" for name in _CATALOG_PROVINCES[6:]},
}
_SPECIAL_USE_SUFFIXES = frozenset(
    {"alt", "arpa", "example", "internal", "invalid", "local", "localhost", "onion", "test"}
)
_TASK_FIELDS = frozenset(
    {
        "task_id",
        "kind",
        "province",
        "year",
        "subject_group",
        "authority_name",
        "official_roots",
        "target_name",
        "query_variants",
        "preferred_source_tiers",
        "max_candidates",
        "freshness_rule",
        "required_extraction_fields",
        "availability_expectation",
        "max_network_retries",
        "stop_conditions",
        "unavailable_reasons",
        "source_policy_id",
        "source_policy_version",
    }
)
_PLAN_FIELDS = frozenset(
    {
        "schema_version",
        "province",
        "exam_year",
        "research_year",
        "subject_group",
        "authority_name",
        "official_roots",
        "catalog_verified_at",
        "catalog_digest",
        "mode",
        "decision_policy_id",
        "decision_policy_digest",
        "decision_basis_id",
        "decision_source_id",
        "decision_source_version",
        "source_policy_id",
        "source_policy_version",
        "pathway_trace",
        "tasks",
    }
)
_PATHWAY_TRACE_FIELDS = frozenset(
    {"pathway_id", "preference", "decision", "reason_code"}
)
_PROFILE_FIELDS = frozenset(
    {
        "schema_version",
        "province",
        "subject_mode",
        "subject_group",
        "secondary_subjects",
        "rank",
        "grade",
        "current_year",
        "target_major_categories",
        "target_cities",
        "target_schools",
        "eligibility_facts",
    }
)
_MAX_INPUT_BYTES = 1024 * 1024


class QueryPlanCapabilityError(RuntimeError):
    """A capability required to emit the plan is unavailable."""


class QueryPlanInputError(ValueError):
    """The CLI received an invalid argument shape."""


class ProvinceCatalogError(ValueError):
    """The discovery catalog is malformed or cannot resolve one province."""


def _calendar_date(value: Any, name: str) -> str:
    if not isinstance(value, str) or value != value.strip():
        raise ProvinceCatalogError(f"{name} must be an ISO calendar date")
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        raise ProvinceCatalogError(f"{name} must be an ISO calendar date") from None
    if parsed.isoformat() != value:
        raise ProvinceCatalogError(f"{name} must be an ISO calendar date")
    return value


def _public_https_url(value: Any, name: str) -> str:
    """Validate one catalog URL while preserving its exact tracked spelling."""

    if not isinstance(value, str) or not value or value != value.strip():
        raise ProvinceCatalogError(f"{name} must be a public HTTPS URL")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise ProvinceCatalogError(f"{name} must be a public HTTPS URL")
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        port = parsed.port
    except ValueError:
        raise ProvinceCatalogError(f"{name} must be a public HTTPS URL") from None
    if (
        parsed.scheme != "https"
        or not hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
        or port not in {None, 443}
        or not parsed.path.startswith("/")
        or "\\" in parsed.path
        or any(component in {".", ".."} for component in parsed.path.split("/"))
    ):
        raise ProvinceCatalogError(f"{name} must be a public HTTPS URL")
    try:
        canonical_host = hostname.encode("idna").decode("ascii").casefold().rstrip(".")
    except UnicodeError:
        raise ProvinceCatalogError(f"{name} must use a public DNS host") from None
    labels = canonical_host.split(".")
    if (
        len(labels) < 2
        or any(
            not label
            or len(label) > 63
            or re.fullmatch(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", label) is None
            for label in labels
        )
        or any(canonical_host == suffix or canonical_host.endswith("." + suffix) for suffix in _SPECIAL_USE_SUFFIXES)
        or all(re.fullmatch(r"(?:[0-9]+|0x[0-9a-f]+)", label) for label in labels)
    ):
        raise ProvinceCatalogError(f"{name} must use a public DNS host")
    try:
        ipaddress.ip_address(canonical_host)
    except ValueError:
        pass
    else:
        raise ProvinceCatalogError(f"{name} must use a public DNS host")
    return value


def _exact_string_collection(value: Any, name: str) -> tuple[str, ...]:
    if isinstance(value, (str, bytes, bytearray)):
        raise TypeError(f"{name} must be an ordered string collection")
    try:
        items = tuple(value)
    except TypeError as error:
        raise TypeError(f"{name} must be an ordered string collection") from error
    if not items or any(
        not isinstance(item, str) or not item or item != item.strip()
        for item in items
    ):
        raise ValueError(f"{name} must contain nonempty exact strings")
    if len(items) != len(set(items)):
        raise ValueError(f"{name} must not contain duplicates")
    return items


@dataclass(frozen=True)
class ProvinceDiscovery:
    """Immutable discovery metadata sourced only from the tracked catalog."""

    province: str
    aliases: tuple[str, ...]
    mode: str
    authority_name: str
    official_roots: tuple[str, ...]
    mode_source_url: str
    verified_at: str
    notes: str

    def __post_init__(self) -> None:
        province = _public_text(self.province, "catalog province")
        aliases = _text_collection(self.aliases, "catalog aliases", nonempty=True)
        if len(aliases) > MAX_PROVINCE_ALIASES:
            raise ProvinceCatalogError("catalog aliases exceed the supported bound")
        if province not in aliases:
            raise ProvinceCatalogError("catalog aliases must contain the canonical province")
        if self.mode not in {"3+3", "3+1+2"}:
            raise ProvinceCatalogError("catalog mode is unsupported")
        authority = _public_text(self.authority_name, "catalog authority_name", maximum=512)
        roots = tuple(
            _public_https_url(item, "catalog official root")
            for item in _exact_string_collection(self.official_roots, "catalog official_roots")
        )
        if len(roots) != len(set(roots)):
            raise ProvinceCatalogError("catalog official roots must be unique")
        object.__setattr__(self, "province", province)
        object.__setattr__(self, "aliases", aliases)
        object.__setattr__(self, "authority_name", authority)
        object.__setattr__(self, "official_roots", roots)
        object.__setattr__(
            self,
            "mode_source_url",
            _public_https_url(self.mode_source_url, "catalog mode source URL"),
        )
        object.__setattr__(self, "verified_at", _calendar_date(self.verified_at, "catalog record verified_at"))
        object.__setattr__(self, "notes", _public_text(self.notes, "catalog notes", maximum=2048))

    def to_dict(self) -> dict[str, Any]:
        return {
            "province": self.province,
            "aliases": list(self.aliases),
            "mode": self.mode,
            "authority_name": self.authority_name,
            "official_roots": list(self.official_roots),
            "mode_source_url": self.mode_source_url,
            "verified_at": self.verified_at,
            "notes": self.notes,
        }


def _catalog_digest(
    schema_version: str,
    verified_at: str,
    coverage_note: str,
    mode_authority_urls: tuple[str, ...],
    provinces: tuple[ProvinceDiscovery, ...],
) -> str:
    payload = {
        "schema_version": schema_version,
        "verified_at": verified_at,
        "coverage_note": coverage_note,
        "mode_authority_urls": list(mode_authority_urls),
        "provinces": [item.to_dict() for item in provinces],
    }
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


@dataclass(frozen=True, init=False)
class ProvinceCatalogSnapshot:
    """Strict immutable snapshot of ``references/provinces/index.json``."""

    schema_version: str
    verified_at: str
    coverage_note: str
    mode_authority_urls: tuple[str, ...]
    provinces: tuple[ProvinceDiscovery, ...]
    digest: str

    def __init__(self) -> None:
        raise TypeError("ProvinceCatalogSnapshot is factory-only")

    @classmethod
    def _create(cls, **values: Any) -> "ProvinceCatalogSnapshot":
        expected = {
            "schema_version",
            "verified_at",
            "coverage_note",
            "mode_authority_urls",
            "provinces",
            "digest",
        }
        if set(values) != expected:
            raise TypeError("catalog factory fields do not match the contract")
        instance = object.__new__(cls)
        for name, value in values.items():
            object.__setattr__(instance, name, value)
        instance.__post_init__()
        return instance

    def __post_init__(self) -> None:
        if self.schema_version != "1.0":
            raise ProvinceCatalogError("unsupported province catalog schema version")
        verified_at = _calendar_date(self.verified_at, "catalog verified_at")
        coverage_note = _public_text(self.coverage_note, "catalog coverage_note", maximum=2048)
        authority_urls = tuple(
            _public_https_url(item, "catalog mode authority URL")
            for item in _exact_string_collection(
                self.mode_authority_urls,
                "catalog mode_authority_urls",
            )
        )
        if isinstance(self.provinces, (str, bytes, bytearray)):
            raise TypeError("catalog provinces must be an ordered collection")
        try:
            provinces = tuple(self.provinces)
        except TypeError as error:
            raise TypeError("catalog provinces must be an ordered collection") from error
        if any(not isinstance(item, ProvinceDiscovery) for item in provinces):
            raise TypeError("catalog provinces must contain ProvinceDiscovery records")
        if tuple(item.province for item in provinces) != _CATALOG_PROVINCES:
            raise ProvinceCatalogError("catalog province order or completeness is invalid")
        if any(item.mode != _CATALOG_MODES[item.province] for item in provinces):
            raise ProvinceCatalogError("catalog province mode partition is invalid")
        aliases = [unicodedata.normalize("NFKC", alias).casefold() for item in provinces for alias in item.aliases]
        if len(aliases) != len(set(aliases)):
            raise ProvinceCatalogError("catalog aliases must be globally unique")
        if any(item.verified_at != verified_at for item in provinces):
            raise ProvinceCatalogError("catalog record verification dates must match the snapshot")
        expected_digest = _catalog_digest(
            self.schema_version,
            verified_at,
            coverage_note,
            authority_urls,
            provinces,
        )
        if self.digest != expected_digest:
            raise ProvinceCatalogError("catalog digest does not bind the validated snapshot")
        object.__setattr__(self, "verified_at", verified_at)
        object.__setattr__(self, "coverage_note", coverage_note)
        object.__setattr__(self, "mode_authority_urls", authority_urls)
        object.__setattr__(self, "provinces", provinces)
        object.__setattr__(self, "digest", expected_digest)

    def resolve(self, province_or_alias: Any) -> ProvinceDiscovery:
        normalized = unicodedata.normalize(
            "NFKC", _public_text(province_or_alias, "province catalog lookup")
        ).casefold()
        matches = [
            item
            for item in self.provinces
            if normalized in {unicodedata.normalize("NFKC", alias).casefold() for alias in item.aliases}
        ]
        if len(matches) != 1:
            raise ProvinceCatalogError("province catalog lookup is unknown or ambiguous")
        return matches[0]


def _catalog_from_payload(payload: Any) -> ProvinceCatalogSnapshot:
    if not isinstance(payload, dict) or set(payload) != _CATALOG_FIELDS:
        raise ProvinceCatalogError("province catalog fields do not match the strict contract")
    raw_records = payload["provinces"]
    if not isinstance(raw_records, list):
        raise ProvinceCatalogError("province catalog records must be an array")
    records: list[ProvinceDiscovery] = []
    for raw_record in raw_records:
        if not isinstance(raw_record, dict) or set(raw_record) != _CATALOG_RECORD_FIELDS:
            raise ProvinceCatalogError("province catalog record fields do not match the strict contract")
        if not isinstance(raw_record["aliases"], list) or not isinstance(
            raw_record["official_roots"], list
        ):
            raise ProvinceCatalogError("province catalog collections must be arrays")
        records.append(
            ProvinceDiscovery(
                province=raw_record["province"],
                aliases=tuple(raw_record["aliases"]),
                mode=raw_record["mode"],
                authority_name=raw_record["authority_name"],
                official_roots=tuple(raw_record["official_roots"]),
                mode_source_url=raw_record["mode_source_url"],
                verified_at=raw_record["verified_at"],
                notes=raw_record["notes"],
            )
        )
    raw_authorities = payload["mode_authority_urls"]
    if not isinstance(raw_authorities, list):
        raise ProvinceCatalogError("catalog mode authority URLs must be an array")
    records_tuple = tuple(records)
    authority_tuple = tuple(raw_authorities)
    return ProvinceCatalogSnapshot._create(
        schema_version=payload["schema_version"],
        verified_at=payload["verified_at"],
        coverage_note=payload["coverage_note"],
        mode_authority_urls=authority_tuple,
        provinces=records_tuple,
        digest=_catalog_digest(
            payload["schema_version"],
            payload["verified_at"],
            _public_text(payload["coverage_note"], "catalog coverage_note", maximum=2048),
            tuple(_public_https_url(item, "catalog mode authority URL") for item in authority_tuple),
            records_tuple,
        ),
    )


def _catalog_provenance_seam():
    tracked: dict[int, tuple[ProvinceCatalogSnapshot, str]] = {}

    def load_tracked() -> ProvinceCatalogSnapshot:
        canonical_path = (
            Path(__file__).parent.parent
            / "references"
            / "provinces"
            / "index.json"
        )
        validated = _catalog_from_payload(_strict_json_file(canonical_path))
        snapshot = object.__new__(ProvinceCatalogSnapshot)
        for name in (
            "schema_version",
            "verified_at",
            "coverage_note",
            "mode_authority_urls",
            "provinces",
            "digest",
        ):
            object.__setattr__(snapshot, name, getattr(validated, name))
        snapshot.__post_init__()
        tracked[id(snapshot)] = (snapshot, snapshot.digest)
        return snapshot

    def recognizes(snapshot: Any) -> bool:
        registered = tracked.get(id(snapshot))
        return (
            registered is not None
            and registered[0] is snapshot
            and registered[1] == snapshot.digest
        )

    return load_tracked, recognizes


_load_tracked_catalog, _is_tracked_catalog = _catalog_provenance_seam()
del _catalog_provenance_seam


def load_province_catalog(path: Any = None) -> ProvinceCatalogSnapshot:
    """Read one strict tracked catalog snapshot; import itself performs no I/O."""

    if path is None:
        return _load_tracked_catalog()
    return _catalog_from_payload(_strict_json_file(path))


_PATHWAY_IDS = (
    "strong_foundation",
    "comprehensive_evaluation",
    "special_program",
    "service_oriented",
    "uniformed_service",
    "cross_border",
    "arts_sports",
)
_PATHWAY_TASK_FAMILIES = MappingProxyType({
    "strong_foundation": (("strong_foundation", "强基计划"),),
    "comprehensive_evaluation": (("comprehensive_evaluation", "综合评价"),),
    "special_program": (
        ("special_pathway", "国家专项"),
        ("special_pathway", "地方专项"),
        ("special_pathway", "高校专项"),
    ),
    "service_oriented": (
        ("special_pathway", "公费师范"),
        ("special_pathway", "优师计划"),
        ("special_pathway", "定向医学生"),
    ),
    "uniformed_service": (
        ("special_pathway", "军校"),
        ("special_pathway", "公安司法消防"),
        ("special_pathway", "航海航空"),
    ),
    "cross_border": (
        ("hk_macao_admission", "港澳招生"),
        ("special_pathway", "中外合作办学"),
    ),
    "arts_sports": (("special_pathway", "艺体类"),),
})
_PATHWAY_TASK_UNIVERSE = frozenset(
    identity
    for family in _PATHWAY_TASK_FAMILIES.values()
    for identity in family
)
_PATHWAY_KINDS = frozenset(kind for kind, _target in _PATHWAY_TASK_UNIVERSE)
_PATHWAY_QUERY_TERMS = {
    ("strong_foundation", "强基计划"): (
        "强基计划 招生专业 入围 录取",
        "强基计划 培养方案 转段方向 出口",
    ),
    ("comprehensive_evaluation", "综合评价"): (
        "综合评价 报考条件 成绩比例",
        "综合评价 校测 录取 出口",
    ),
    ("hk_macao_admission", "港澳招生"): (
        "港澳招生 招生方式 英语要求",
        "港澳院校 费用 奖学金 出口",
    ),
}


@dataclass(frozen=True)
class PathwayResearchTrace:
    pathway_id: str
    preference: str
    decision: str
    reason_code: str

    def __post_init__(self) -> None:
        if self.pathway_id not in _PATHWAY_IDS:
            raise ValueError("unsupported pathway trace ID")
        if self.preference not in {"unknown", "interested", "not_interested", "not_applicable"}:
            raise ValueError("unsupported pathway preference")
        if self.decision not in {"include", "discover", "exclude"}:
            raise ValueError("unsupported pathway research decision")
        expected = {
            "profile_interested": "include",
            "preference_unknown_requires_discovery": "discover",
            "profile_not_interested": "exclude",
            "profile_not_applicable": "exclude",
            "service_commitment_rejected": "exclude",
            "legacy_private_compatibility": "discover",
        }
        if expected.get(self.reason_code) != self.decision:
            raise ValueError("pathway trace reason does not match its decision")

    def to_dict(self) -> dict[str, str]:
        return {
            "pathway_id": self.pathway_id,
            "preference": self.preference,
            "decision": self.decision,
            "reason_code": self.reason_code,
        }


def _pathway_trace(profile: PlanningProfile) -> tuple[PathwayResearchTrace, ...]:
    records: list[PathwayResearchTrace] = []
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
        records.append(PathwayResearchTrace(pathway_id, preference, decision, reason))
    return tuple(records)


@dataclass(frozen=True, init=False)
class ResearchContext:
    province: str
    mode: str
    subject_group: str
    exam_year: int
    authority_name: str
    official_roots: tuple[str, ...]
    requested_pathways: tuple[str, ...]
    catalog_verified_at: str
    catalog_digest: str

    def __init__(self) -> None:
        raise TypeError("ResearchContext is factory-only")

    @classmethod
    def create(
        cls,
        profile: PlanningProfile,
        catalog: ProvinceCatalogSnapshot,
    ) -> "ResearchContext":
        if type(profile) is not PlanningProfile:
            raise TypeError("profile must be a strict PlanningProfile")
        if type(catalog) is not ProvinceCatalogSnapshot:
            raise TypeError("catalog must be a strict ProvinceCatalogSnapshot")
        if not _is_tracked_catalog(catalog):
            raise ProvinceCatalogError("public research requires the tracked trusted catalog")
        # Recompute the catalog binding before trusting authority/root/date.
        expected_digest = _catalog_digest(
            catalog.schema_version,
            catalog.verified_at,
            catalog.coverage_note,
            catalog.mode_authority_urls,
            catalog.provinces,
        )
        if catalog.digest != expected_digest:
            raise ProvinceCatalogError("catalog digest does not bind the validated snapshot")
        discovery = catalog.resolve(profile.province)
        if profile.subject_mode != discovery.mode:
            raise ValueError("profile subject mode conflicts with the trusted catalog")
        subject_group = canonical_discovery_subject_key(
            discovery.mode,
            profile.subject_group,
            profile.secondary_subjects,
            province=discovery.province,
        )
        trace = _pathway_trace(profile)
        requested = tuple(item.pathway_id for item in trace if item.decision != "exclude")
        instance = object.__new__(cls)
        for name, value in (
            ("province", discovery.province),
            ("mode", discovery.mode),
            ("subject_group", subject_group),
            ("exam_year", _normalize_exam_year(profile.exam_year)),
            ("authority_name", discovery.authority_name),
            ("official_roots", discovery.official_roots),
            ("requested_pathways", requested),
            ("catalog_verified_at", catalog.verified_at),
            ("catalog_digest", catalog.digest),
        ):
            object.__setattr__(instance, name, value)
        return instance


class _SafeArgumentParser(argparse.ArgumentParser):
    def error(self, _message: str) -> None:
        raise QueryPlanInputError("invalid command-line arguments")

    def exit(self, status: int = 0, message: str | None = None) -> None:
        if status:
            raise QueryPlanInputError("invalid command-line arguments")
        super().exit(status, message)


def _normalize_mathematical_integer(
    value: Any, name: str, *, minimum: int, maximum: int
) -> int:
    if isinstance(value, (bool, str, bytes, bytearray)):
        raise TypeError(f"{name} must be a finite mathematical integer")
    try:
        finite = math.isfinite(value)
        normalized = int(value)
    except (OverflowError, TypeError, ValueError) as error:
        raise TypeError(f"{name} must be a finite mathematical integer") from error
    if not finite or value != normalized:
        raise ValueError(f"{name} must be a finite mathematical integer")
    if not minimum <= normalized <= maximum:
        raise ValueError(f"{name} is outside the supported range")
    return normalized


def _normalize_exam_year(value: Any) -> int:
    return _normalize_mathematical_integer(
        value, "exam_year", minimum=2000, maximum=2100
    )


def _current_utc_year() -> int:
    """Capture the trusted research clock once at a query-plan boundary."""

    return datetime.now(timezone.utc).year


def _normalize_research_year(value: Any) -> int:
    return _normalize_mathematical_integer(
        value, "research_year", minimum=2000, maximum=2100
    )


def _validate_province_config(value: Any) -> ProvinceConfig:
    """Recheck a Plan02 config snapshot without reopening its source file."""

    if type(value) is not ProvinceConfig:
        raise TypeError("province must be a strict ProvinceConfig")
    if value.schema_version != "1.0":
        raise ValueError("province schema version is invalid")
    if value.mode not in {"3+1+2", "3+3"}:
        raise ValueError("province mode is invalid")
    for name in ("primary_subjects", "secondary_subjects"):
        subjects = getattr(value, name)
        if type(subjects) is not tuple or not subjects:
            raise TypeError(f"province {name} must be a non-empty tuple")
        normalized = tuple(_public_text(item, f"province {name} item") for item in subjects)
        if len(normalized) != len(set(normalized)):
            raise ValueError(f"province {name} contains duplicate subjects")
    if value.mode == "3+1+2" and len(value.secondary_subjects) < 2:
        raise ValueError("3+1+2 province requires configurable secondary subjects")
    if value.mode == "3+3" and len(set(value.primary_subjects) | set(value.secondary_subjects)) < 3:
        raise ValueError("3+3 province requires at least three configured subjects")
    if (
        isinstance(value.score_scale, bool)
        or not isinstance(value.score_scale, (int, float))
        or not math.isfinite(value.score_scale)
        or not 100 <= value.score_scale <= 1000
    ):
        raise ValueError("province score scale is invalid")
    if not isinstance(value.directory, Path) or not value.directory.is_absolute():
        raise TypeError("province directory must be an absolute Path snapshot")
    policy = value.ordinary_batch_policy
    if type(policy) is not OrdinaryBatchPolicy:
        raise TypeError("province ordinary-batch policy is invalid")
    policy_payload = policy.to_dict()
    expected_policy_fields = {
        "schema_version",
        "policy_id",
        "basis_id",
        "search_delta_min",
        "search_delta_max",
        "challenge_delta_lt",
        "stable_delta_le",
        "tier_caps",
    }
    if not isinstance(policy_payload, dict) or set(policy_payload) != expected_policy_fields:
        raise ValueError("province ordinary-batch policy serialization is invalid")
    try:
        reconstructed = OrdinaryBatchPolicy(**policy_payload)
    except (TypeError, ValueError) as error:
        raise ValueError("province ordinary-batch policy semantics are invalid") from error
    if reconstructed.to_dict() != policy_payload:
        raise ValueError("province ordinary-batch policy snapshot is unstable")
    return value


def _public_text(value: Any, name: str, *, maximum: int = 256) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if not value or value != value.strip():
        raise ValueError(f"{name} must be a non-empty trimmed string")
    if any(unicodedata.category(character) == "Cf" for character in value):
        raise ValueError(f"{name} must not contain Unicode format controls")
    normalized = unicodedata.normalize("NFKC", value)
    if not normalized or normalized != normalized.strip():
        raise ValueError(f"{name} must be a non-empty trimmed string")
    if (
        len(normalized) > maximum
        or any(
            ord(character) < 32
            or ord(character) == 127
            or unicodedata.category(character) == "Cf"
            for character in normalized
        )
    ):
        raise ValueError(f"{name} must be bounded single-line public text")
    if (
        "/" in normalized
        or "\\" in normalized
        or _ENV_REFERENCE.search(normalized) is not None
        or _DRIVE_REFERENCE.search(normalized) is not None
    ):
        raise ValueError(f"{name} contains path-like text")
    try:
        validate_public_output_text(normalized)
    except ValueError as error:
        raise ValueError(f"{name} contains private or non-public text") from error
    return normalized


def _text_collection(
    value: Any,
    name: str,
    *,
    nonempty: bool = False,
    public: bool = True,
    sort_values: bool = False,
) -> tuple[str, ...]:
    if isinstance(value, (str, bytes, bytearray)):
        raise TypeError(f"{name} must be a collection of strings")
    try:
        items = tuple(value)
    except TypeError as error:
        raise TypeError(f"{name} must be a collection of strings") from error
    normalized: list[str] = []
    for item in items:
        if public:
            normalized.append(_public_text(item, f"{name} item", maximum=512))
        else:
            if not isinstance(item, str) or _FIELD_ID.fullmatch(item) is None:
                raise ValueError(f"{name} must contain safe field identifiers")
            normalized.append(item)
    if nonempty and not normalized:
        raise ValueError(f"{name} must not be empty")
    if len(normalized) != len(set(normalized)):
        raise ValueError(f"{name} must not contain duplicates")
    if sort_values:
        normalized.sort()
    return tuple(normalized)


def _task_identity_payload(task: "QueryTask") -> dict[str, Any]:
    return {
        "kind": task.kind,
        "province": task.province,
        "year": task.year,
        "subject_group": task.subject_group,
        "authority_name": task.authority_name,
        "official_roots": list(task.official_roots),
        "target_name": task.target_name,
        "query_variants": list(task.query_variants),
        "preferred_source_tiers": list(task.preferred_source_tiers),
        "max_candidates": task.max_candidates,
        "freshness_rule": task.freshness_rule,
        "required_extraction_fields": list(task.required_extraction_fields),
        "availability_expectation": task.availability_expectation,
        "max_network_retries": task.max_network_retries,
        "stop_conditions": list(task.stop_conditions),
        "unavailable_reasons": list(task.unavailable_reasons),
        "source_policy_id": task.source_policy_id,
        "source_policy_version": task.source_policy_version,
    }


def _expected_task_id(task: "QueryTask") -> str:
    normalized = json.dumps(
        _task_identity_payload(task),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    digest = hashlib.sha256(normalized).hexdigest()[:24]
    return f"{task.kind.replace('_', '-')}:{digest}"


@dataclass(frozen=True)
class QueryTask:
    task_id: str
    kind: str
    province: str
    year: int
    subject_group: str
    authority_name: str
    official_roots: tuple[str, ...]
    target_name: str | None
    query_variants: tuple[str, ...]
    preferred_source_tiers: tuple[str, ...]
    max_candidates: int
    freshness_rule: str
    required_extraction_fields: tuple[str, ...]
    availability_expectation: str
    max_network_retries: int
    stop_conditions: tuple[str, ...]
    unavailable_reasons: tuple[str, ...]
    source_policy_id: str
    source_policy_version: str

    def __post_init__(self) -> None:
        if not isinstance(self.kind, str) or self.kind not in _KINDS:
            raise ValueError("unsupported query kind")
        object.__setattr__(self, "province", _public_text(self.province, "province"))
        object.__setattr__(
            self,
            "year",
            _normalize_mathematical_integer(
                self.year, "task year", minimum=1998, maximum=2100
            ),
        )
        object.__setattr__(
            self, "subject_group", _public_text(self.subject_group, "subject_group")
        )
        object.__setattr__(
            self,
            "authority_name",
            _public_text(self.authority_name, "authority_name", maximum=512),
        )
        roots = tuple(
            _public_https_url(root, "official root")
            for root in _exact_string_collection(self.official_roots, "official_roots")
        )
        object.__setattr__(self, "official_roots", roots)
        if self.target_name is not None:
            object.__setattr__(
                self, "target_name", _public_text(self.target_name, "target_name")
            )
        if self.kind in {
            "province_policy",
            "score_table",
            "enrollment_plan",
            "admission_charter",
            "tuition_fee",
            "subject_requirement",
        } and self.target_name is not None:
            raise ValueError("this query kind cannot carry a structured target")
        if self.kind in {
            "batch_admission",
            "strong_foundation",
            "comprehensive_evaluation",
            "hk_macao_admission",
            "special_pathway",
        } and self.target_name is None:
            raise ValueError("this query kind requires a structured target")
        object.__setattr__(
            self,
            "query_variants",
            _text_collection(self.query_variants, "query_variants", nonempty=True),
        )
        tiers = _text_collection(
            self.preferred_source_tiers,
            "preferred_source_tiers",
            nonempty=True,
        )
        if tiers != ("A", "B", "C"):
            raise ValueError("preferred_source_tiers must be exactly A, B, C")
        object.__setattr__(self, "preferred_source_tiers", tiers)
        object.__setattr__(
            self,
            "max_candidates",
            _normalize_mathematical_integer(
                self.max_candidates, "max_candidates", minimum=10, maximum=10
            ),
        )
        if self.availability_expectation not in _EXPECTATIONS:
            raise ValueError("unsupported availability expectation")
        expected_freshness = _FRESHNESS_BY_EXPECTATION[self.availability_expectation]
        if self.freshness_rule != expected_freshness:
            raise ValueError("freshness rule and availability expectation disagree")
        object.__setattr__(
            self,
            "required_extraction_fields",
            _text_collection(
                self.required_extraction_fields,
                "required_extraction_fields",
                nonempty=True,
                public=False,
            ),
        )
        if self.required_extraction_fields != _EXTRACTION_FIELDS[self.kind]:
            raise ValueError("required extraction fields do not match query kind")
        object.__setattr__(
            self,
            "max_network_retries",
            _normalize_mathematical_integer(
                self.max_network_retries,
                "max_network_retries",
                minimum=1,
                maximum=1,
            ),
        )
        if tuple(self.stop_conditions) != _STOP_CONDITIONS:
            raise ValueError("stop_conditions must use the bounded retrieval contract")
        object.__setattr__(self, "stop_conditions", _STOP_CONDITIONS)
        if tuple(self.unavailable_reasons) != _UNAVAILABLE_REASONS:
            raise ValueError("unavailable_reasons must use the bounded vocabulary")
        object.__setattr__(self, "unavailable_reasons", _UNAVAILABLE_REASONS)
        if self.source_policy_id != "pathway-atlas-source-policy" or self.source_policy_version != "1.0":
            raise ValueError("query task must reference the unique source policy")
        query_text = " ".join(self.query_variants)
        for context in (
            self.province,
            str(self.year),
            self.subject_group,
            self.authority_name,
        ):
            if context not in query_text:
                raise ValueError("query variants do not carry the task context")
        if self.target_name is not None and self.target_name not in query_text:
            raise ValueError("query variants do not carry the structured target")
        if self.target_name is None and self.kind in _GENERIC_KIND_SYNONYMS:
            if any(
                synonym not in query_text
                for synonym in _GENERIC_KIND_SYNONYMS[self.kind]
            ):
                raise ValueError("generic query task is missing fixed kind synonyms")
        if not isinstance(self.task_id, str) or _SAFE_ID.fullmatch(self.task_id) is None:
            raise ValueError("task_id must use the evidence safe-ID syntax")
        if self.task_id != _expected_task_id(self):
            raise ValueError("task_id does not match normalized task content")

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "kind": self.kind,
            "province": self.province,
            "year": self.year,
            "subject_group": self.subject_group,
            "authority_name": self.authority_name,
            "official_roots": list(self.official_roots),
            "target_name": self.target_name,
            "query_variants": list(self.query_variants),
            "preferred_source_tiers": list(self.preferred_source_tiers),
            "max_candidates": self.max_candidates,
            "freshness_rule": self.freshness_rule,
            "required_extraction_fields": list(self.required_extraction_fields),
            "availability_expectation": self.availability_expectation,
            "max_network_retries": self.max_network_retries,
            "stop_conditions": list(self.stop_conditions),
            "unavailable_reasons": list(self.unavailable_reasons),
            "source_policy_id": self.source_policy_id,
            "source_policy_version": self.source_policy_version,
        }


@dataclass(frozen=True)
class QueryPlan:
    schema_version: str
    province: str
    mode: str
    exam_year: int
    research_year: int
    subject_group: str
    authority_name: str
    official_roots: tuple[str, ...]
    catalog_verified_at: str
    catalog_digest: str
    decision_policy_id: str
    decision_policy_digest: str
    decision_basis_id: str
    decision_source_id: str
    decision_source_version: str
    source_policy_id: str
    source_policy_version: str
    pathway_trace: tuple[PathwayResearchTrace, ...]
    tasks: tuple[QueryTask, ...]

    def __post_init__(self) -> None:
        if self.schema_version != _SCHEMA_VERSION:
            raise ValueError("unsupported query-plan schema version")
        object.__setattr__(self, "province", _public_text(self.province, "province"))
        if self.mode not in {"3+1+2", "3+3"}:
            raise ValueError("query-plan mode is unsupported")
        object.__setattr__(self, "exam_year", _normalize_exam_year(self.exam_year))
        object.__setattr__(
            self, "research_year", _normalize_research_year(self.research_year)
        )
        object.__setattr__(
            self, "subject_group", _public_text(self.subject_group, "subject_group")
        )
        object.__setattr__(
            self,
            "authority_name",
            _public_text(self.authority_name, "authority_name", maximum=512),
        )
        roots = tuple(
            _public_https_url(item, "official root")
            for item in _exact_string_collection(self.official_roots, "official_roots")
        )
        object.__setattr__(self, "official_roots", roots)
        object.__setattr__(
            self,
            "catalog_verified_at",
            _calendar_date(self.catalog_verified_at, "catalog_verified_at"),
        )
        if not isinstance(self.catalog_digest, str) or re.fullmatch(r"sha256:[0-9a-f]{64}", self.catalog_digest) is None:
            raise ValueError("catalog_digest must be a SHA-256 identity")
        for name in ("decision_policy_id", "decision_basis_id", "decision_source_id"):
            if not isinstance(getattr(self, name), str) or _SAFE_ID.fullmatch(getattr(self, name)) is None:
                raise ValueError(f"{name} must use the public safe-ID syntax")
        if not isinstance(self.decision_policy_digest, str) or re.fullmatch(r"sha256:[0-9a-f]{64}", self.decision_policy_digest) is None:
            raise ValueError("decision_policy_digest must be a SHA-256 identity")
        if not isinstance(self.decision_source_version, str) or re.fullmatch(r"[0-9]+\.[0-9]+(?:\.[0-9]+)?", self.decision_source_version) is None:
            raise ValueError("decision_source_version must be public and versioned")
        if self.source_policy_id != "pathway-atlas-source-policy" or self.source_policy_version != "1.0":
            raise ValueError("query plan must reference the unique source policy")
        try:
            pathway_trace = tuple(self.pathway_trace)
        except TypeError as error:
            raise TypeError("pathway_trace must be a collection") from error
        if tuple(item.pathway_id for item in pathway_trace) != _PATHWAY_IDS or any(
            not isinstance(item, PathwayResearchTrace) for item in pathway_trace
        ):
            raise ValueError("pathway_trace must cover each pathway exactly once")
        object.__setattr__(self, "pathway_trace", pathway_trace)
        if isinstance(self.tasks, (str, bytes, bytearray)):
            raise TypeError("tasks must be a collection of QueryTask records")
        try:
            tasks = tuple(self.tasks)
        except TypeError as error:
            raise TypeError("tasks must be a collection of QueryTask records") from error
        if not tasks or any(not isinstance(task, QueryTask) for task in tasks):
            raise TypeError("tasks must contain QueryTask records")
        object.__setattr__(self, "tasks", tasks)
        if len({task.task_id for task in tasks}) != len(tasks):
            raise ValueError("query plan contains duplicate task IDs")
        window = set(year_window(self.research_year))
        for task in tasks:
            if (
                task.province != self.province
                or task.subject_group != self.subject_group
                or task.authority_name != self.authority_name
                or task.official_roots != self.official_roots
                or task.source_policy_id != self.source_policy_id
                or task.source_policy_version != self.source_policy_version
            ):
                raise ValueError("task context does not match query plan")
            if task.year not in window:
                raise ValueError("task year is outside the explicit four-year window")
            expectation = (
                "current_year_availability_must_be_checked"
                if task.year == self.research_year
                else "expected_available"
            )
            if task.availability_expectation != expectation:
                raise ValueError("task availability does not match its explicit year")
        by_kind = {
            kind: tuple(task for task in tasks if task.kind == kind) for kind in _KINDS
        }
        if {task.year for task in by_kind["score_table"]} != window:
            raise ValueError("score_table tasks must cover the exact four-year window")
        batch_targets = {task.target_name for task in by_kind["batch_admission"]}
        if batch_targets not in ({"普通批"}, {"普通批", "提前批", "综合评价批"}):
            raise ValueError("batch admission tasks must cover the public or private compatibility scope")
        for target in batch_targets:
            target_years = tuple(
                task.year
                for task in by_kind["batch_admission"]
                if task.target_name == target
            )
            if len(target_years) != 4 or set(target_years) != window:
                raise ValueError(
                    "each batch admission target must cover the exact four-year window"
                )
        required_annual_single_target_kinds = (
            "province_policy",
            "score_table",
            "joy_report",
            "enrollment_plan",
            "admission_charter",
            "tuition_fee",
            "subject_requirement",
        )
        for kind in required_annual_single_target_kinds:
            kind_years = tuple(task.year for task in by_kind[kind])
            if kind_years != year_window(self.research_year):
                raise ValueError(f"{kind} tasks must cover the exact four-year window")
        for kind in ("strong_foundation", "comprehensive_evaluation", "hk_macao_admission"):
            kind_years = tuple(task.year for task in by_kind[kind])
            if kind_years and kind_years != year_window(self.research_year):
                raise ValueError(f"{kind} tasks must cover the exact four-year window")
        special_targets = {
            task.target_name for task in by_kind["special_pathway"]
        }
        for target in special_targets:
            target_years = tuple(
                task.year
                for task in by_kind["special_pathway"]
                if task.target_name == target
            )
            if len(target_years) != 4 or set(target_years) != window:
                raise ValueError(
                    "each special pathway must cover the exact four-year window"
                )
        task_identities = {(task.kind, task.target_name) for task in tasks}
        pathway_task_identities = {
            identity for identity in task_identities if identity[0] in _PATHWAY_KINDS
        }
        if not pathway_task_identities <= _PATHWAY_TASK_UNIVERSE:
            raise ValueError("pathway task identity is outside the finite universe")
        trace_by_pathway = {item.pathway_id: item for item in pathway_trace}
        for pathway_id, expected_family in _PATHWAY_TASK_FAMILIES.items():
            expected = set(expected_family)
            present = expected & pathway_task_identities
            if trace_by_pathway[pathway_id].decision == "exclude":
                if present:
                    raise ValueError("excluded pathway must not emit query tasks")
            elif present != expected:
                raise ValueError("active pathway must emit its complete query family")
        identities = tuple(dict.fromkeys((task.kind, task.target_name) for task in tasks))
        for identity in identities:
            years = tuple(
                task.year for task in tasks if (task.kind, task.target_name) == identity
            )
            if years != year_window(self.research_year):
                raise ValueError("each data type must use strict Y through Y-3 order")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "province": self.province,
            "mode": self.mode,
            "exam_year": self.exam_year,
            "research_year": self.research_year,
            "subject_group": self.subject_group,
            "authority_name": self.authority_name,
            "official_roots": list(self.official_roots),
            "catalog_verified_at": self.catalog_verified_at,
            "catalog_digest": self.catalog_digest,
            "decision_policy_id": self.decision_policy_id,
            "decision_policy_digest": self.decision_policy_digest,
            "decision_basis_id": self.decision_basis_id,
            "decision_source_id": self.decision_source_id,
            "decision_source_version": self.decision_source_version,
            "source_policy_id": self.source_policy_id,
            "source_policy_version": self.source_policy_version,
            "pathway_trace": [item.to_dict() for item in self.pathway_trace],
            "tasks": [task.to_dict() for task in self.tasks],
        }


_EXTRACTION_FIELDS = {
    "province_policy": (
        "province",
        "year",
        "exam_mode",
        "subject_structure",
        "batch_structure",
        "effective_date",
        "source_url",
        "publisher",
        "publication_date",
    ),
    "score_table": (
        "province",
        "year",
        "subject_group",
        "score",
        "cumulative_rank",
        "source_url",
        "publisher",
        "publication_date",
    ),
    "batch_admission": (
        "province",
        "year",
        "subject_group",
        "batch",
        "institution",
        "program_group",
        "min_score",
        "min_rank",
        "source_url",
        "publisher",
        "publication_date",
    ),
    "joy_report": (
        "province",
        "year",
        "high_school",
        "metric",
        "value",
        "source_url",
        "publisher",
        "publication_date",
    ),
    "enrollment_plan": (
        "province",
        "year",
        "subject_group",
        "institution",
        "institution_code",
        "program_group",
        "majors",
        "plan_count",
        "batch",
        "school_province",
        "school_city",
        "institution_type",
        "source_url",
        "publisher",
        "publication_date",
    ),
    "admission_charter": (
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
        "source_url",
        "publisher",
        "publication_date",
    ),
    "tuition_fee": (
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
        "source_url",
        "publisher",
        "publication_date",
    ),
    "subject_requirement": (
        "province",
        "year",
        "subject_group",
        "institution",
        "institution_code",
        "program_group",
        "required_secondary_subjects",
        "secondary_subject_rule",
        "special_conditions",
        "source_url",
        "publisher",
        "publication_date",
    ),
    "strong_foundation": (
        "province",
        "year",
        "institutions",
        "majors",
        "shortlist_rules",
        "admission_rules",
        "training_model",
        "transition_routes",
        "outcomes",
        "source_url",
        "publisher",
        "publication_date",
    ),
    "comprehensive_evaluation": (
        "province",
        "year",
        "institutions",
        "eligibility",
        "score_ratio",
        "school_assessment",
        "admission_rules",
        "outcomes",
        "source_url",
        "publisher",
        "publication_date",
    ),
    "hk_macao_admission": (
        "province",
        "year",
        "institutions",
        "admission_method",
        "english_requirement",
        "fees",
        "scholarships",
        "outcomes",
        "source_url",
        "publisher",
        "publication_date",
    ),
    "special_pathway": (
        "province",
        "year",
        "pathway",
        "eligibility",
        "ordinary_path_difference",
        "employment_restrictions",
        "geographic_restrictions",
        "service_term",
        "breach_consequences",
        "fees_and_subsidies",
        "source_url",
        "publisher",
        "publication_date",
    ),
}


def _make_task(
    *,
    kind: str,
    province: str,
    year: int,
    subject_group: str,
    authority_name: str,
    official_roots: tuple[str, ...],
    target_name: str | None,
    query_variants: tuple[str, ...],
    research_year: int,
    source_policy_id: str = "pathway-atlas-source-policy",
    source_policy_version: str = "1.0",
) -> QueryTask:
    expectation = (
        "current_year_availability_must_be_checked"
        if year == research_year
        else "expected_available"
    )
    values = {
        "task_id": "temporary",
        "kind": kind,
        "province": province,
        "year": year,
        "subject_group": subject_group,
        "authority_name": authority_name,
        "official_roots": official_roots,
        "target_name": target_name,
        "query_variants": query_variants,
        "preferred_source_tiers": ("A", "B", "C"),
        "max_candidates": 10,
        "freshness_rule": _FRESHNESS_BY_EXPECTATION[expectation],
        "required_extraction_fields": _EXTRACTION_FIELDS[kind],
        "availability_expectation": expectation,
        "max_network_retries": 1,
        "stop_conditions": _STOP_CONDITIONS,
        "unavailable_reasons": _UNAVAILABLE_REASONS,
        "source_policy_id": source_policy_id,
        "source_policy_version": source_policy_version,
    }
    prototype = object.__new__(QueryTask)
    for name, value in values.items():
        object.__setattr__(prototype, name, value)
    values["task_id"] = _expected_task_id(prototype)
    return QueryTask(**values)


def _policy_digest(policy: DecisionPolicySnapshot) -> str:
    encoded = json.dumps(
        policy.to_dict(),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _legacy_pathway_trace() -> tuple[PathwayResearchTrace, ...]:
    return tuple(
        PathwayResearchTrace(
            pathway_id=pathway_id,
            preference="unknown",
            decision="discover",
            reason_code="legacy_private_compatibility",
        )
        for pathway_id in _PATHWAY_IDS
    )


def _build_query_plan_legacy(
    profile: RecommendationProfile | PlanningProfile,
    province: ProvinceConfig,
    exam_year: Any,
    *,
    high_school_name: str | None = None,
    requested_pathways: Any = (),
    catalog: ProvinceCatalogSnapshot | None = None,
) -> QueryPlan:
    """Private ProvinceConfig compatibility adapter pending Task 9 migration."""

    if not isinstance(profile, (RecommendationProfile, PlanningProfile)):
        raise TypeError("profile must be a recommendation or planning profile")
    province = _validate_province_config(province)
    year = _normalize_exam_year(exam_year)
    if catalog is None:
        catalog = load_province_catalog()
    if type(catalog) is not ProvinceCatalogSnapshot:
        raise TypeError("catalog must be a strict ProvinceCatalogSnapshot")
    discovery = catalog.resolve(province.province)
    policy = DecisionPolicySnapshot.load_default()
    province_name = discovery.province
    if province.mode != discovery.mode:
        raise ValueError("province policy mode conflicts with discovery catalog mode")
    if isinstance(profile, PlanningProfile):
        profile_province_value = profile.province
        primary_value = profile.subject_group
        secondary_values = profile.secondary_subjects
        profile_school = profile.high_school
    else:
        profile_province_value = profile.target_province
        primary_value = profile.subject_group
        secondary_values = profile.secondary_subjects
        profile_school = None
    profile_province = _public_text(profile_province_value, "profile target_province")
    if catalog.resolve(profile_province).province != province_name:
        raise ValueError("profile and province configuration do not match")
    primary = _public_text(primary_value, "profile subject_group")
    secondary = tuple(
        _public_text(item, "profile secondary_subject")
        for item in secondary_values
    )
    subject_group = canonical_subject_selection_key(province, primary, list(secondary))
    _public_text(subject_group, "canonical subject_group")

    school = profile_school
    if high_school_name is not None:
        school = _public_text(high_school_name, "high_school_name")
    pathways = _text_collection(
        requested_pathways,
        "requested_pathways",
        sort_values=True,
    )

    authority = discovery.authority_name
    roots = discovery.official_roots
    years = year_window(year)
    tasks: list[QueryTask] = []

    def add_task(
        kind: str,
        task_year: int,
        target: str | None,
        queries: tuple[str, ...],
    ) -> None:
        tasks.append(
            _make_task(
                kind=kind,
                province=province_name,
                year=task_year,
                subject_group=subject_group,
                authority_name=authority,
                official_roots=roots,
                target_name=target,
                research_year=year,
                query_variants=queries,
            )
        )

    for task_year in years:
        add_task(
            "province_policy",
            task_year,
            None,
            (
                f"{authority} {province_name} {task_year} {subject_group} 高考政策 考试模式",
                f"{authority} {province_name} {task_year} {subject_group} 批次设置 选科模式",
            ),
        )
    for task_year in years:
        add_task(
            "score_table",
            task_year,
            None,
            (
                f"{authority} {province_name} {task_year} {subject_group} 一分一段表",
                f"{province_name} {task_year} {subject_group} 一分一段 {authority}",
            ),
        )
    for batch in ("普通批", "提前批", "综合评价批"):
        for task_year in years:
            add_task(
                "batch_admission",
                task_year,
                batch,
                (
                    f"{authority} {province_name} {task_year} {subject_group} {batch} 投档录取",
                    f"{province_name} {task_year} {subject_group} {batch} 院校专业组 {authority}",
                ),
            )
    for task_year in years:
        if school is None:
            joy_queries = (
                f"{authority} {province_name} {task_year} {subject_group} 高中喜报",
                f"{authority} {task_year} {subject_group} 高考光荣榜",
                f"{province_name} {task_year} {subject_group} 高中升学成果 {authority}",
            )
        else:
            joy_queries = (
                f"{authority} {province_name} {school} {task_year} {subject_group} 高考喜报",
                f"{school} {province_name} {task_year} {subject_group} 高考成绩 光荣榜 {authority}",
                f"{authority} {school} {task_year} {subject_group} 升学成果",
            )
        add_task("joy_report", task_year, school, joy_queries)

    for task_year in years:
        add_task(
            "enrollment_plan",
            task_year,
            None,
            (
                f"{authority} {province_name} {task_year} {subject_group} 高校 招生计划 专业 计划数",
                f"{authority} {province_name} {task_year} {subject_group} 院校代码 专业代码 招生批次",
            ),
        )
        add_task(
            "admission_charter",
            task_year,
            None,
            (
                f"{authority} {province_name} {task_year} {subject_group} 高校 招生章程 录取规则 调剂规则",
                f"{authority} {province_name} {task_year} {subject_group} 招生章程 体检 外语语种 单科 特殊条件",
            ),
        )
        add_task(
            "tuition_fee",
            task_year,
            None,
            (
                f"{authority} {province_name} {task_year} {subject_group} 高校 学费 收费标准 专业",
                f"{authority} {province_name} {task_year} {subject_group} 学费 住宿费 其他费用 奖助信息",
            ),
        )
        add_task(
            "subject_requirement",
            task_year,
            None,
            (
                f"{authority} {province_name} {task_year} {subject_group} 招生专业 选科要求",
                f"{authority} {province_name} {task_year} {subject_group} 院校专业 选考科目要求",
            ),
        )
        add_task(
            "strong_foundation",
            task_year,
            "强基计划",
            (
                f"{authority} {province_name} {task_year} {subject_group} 强基计划 招生专业 入围 录取",
                f"{authority} {province_name} {task_year} {subject_group} 强基计划 培养方案 转段方向 出口",
            ),
        )
        add_task(
            "comprehensive_evaluation",
            task_year,
            "综合评价",
            (
                f"{authority} {province_name} {task_year} {subject_group} 综合评价 报考条件 成绩比例",
                f"{authority} {province_name} {task_year} {subject_group} 综合评价 校测 录取 出口",
            ),
        )
        add_task(
            "hk_macao_admission",
            task_year,
            "港澳招生",
            (
                f"{authority} {province_name} {task_year} {subject_group} 港澳招生 招生方式 英语要求",
                f"{authority} {province_name} {task_year} {subject_group} 港澳院校 费用 奖学金 出口",
            ),
        )

    built_in_pathways = frozenset({"强基", "强基计划", "综合评价", "综评", "港澳", "港澳招生"})
    default_special_pathways = (
        "国家专项",
        "地方专项",
        "高校专项",
        "公费师范",
        "优师计划",
        "定向医学生",
        "军校",
        "公安司法消防",
        "航海航空",
        "中外合作办学",
        "艺体类",
    )
    requested_special = tuple(
        pathway for pathway in pathways if pathway not in built_in_pathways
    )
    special_pathways = tuple(
        dict.fromkeys(requested_special + default_special_pathways)
    )
    for pathway in special_pathways:
        for task_year in years:
            add_task(
                "special_pathway",
                task_year,
                pathway,
                (
                    f"{authority} {province_name} {task_year} {subject_group} "
                    f"{pathway} 报考条件 普通路径区别",
                    f"{authority} {province_name} {task_year} {subject_group} "
                    f"{pathway} 就业 地域限制 服务期 违约后果",
                    f"{authority} {province_name} {task_year} {subject_group} "
                    f"{pathway} 费用 补助 特殊限制",
                ),
            )
    return QueryPlan(
        schema_version=_SCHEMA_VERSION,
        province=province_name,
        mode=discovery.mode,
        exam_year=year,
        research_year=year,
        subject_group=subject_group,
        authority_name=authority,
        official_roots=roots,
        catalog_verified_at=catalog.verified_at,
        catalog_digest=catalog.digest,
        decision_policy_id=policy.policy_id,
        decision_policy_digest=_policy_digest(policy),
        decision_basis_id=policy.basis.basis_id,
        decision_source_id=policy.basis.source_id,
        decision_source_version=policy.basis.source_version,
        source_policy_id=policy.source_policy.policy_id,
        source_policy_version=policy.source_policy.version,
        pathway_trace=_legacy_pathway_trace(),
        tasks=tuple(tasks),
    )


def _build_query_plan_for_year(
    profile: PlanningProfile,
    catalog: ProvinceCatalogSnapshot,
    policy: DecisionPolicySnapshot,
    *,
    research_year: int,
) -> QueryPlan:
    """Build the exact task universe for one already-selected research clock."""

    if type(policy) is not DecisionPolicySnapshot:
        raise TypeError("policy must be a strict DecisionPolicySnapshot")
    research_year = _normalize_research_year(research_year)
    context = ResearchContext.create(profile, catalog)
    trace = _pathway_trace(profile)
    included = {item.pathway_id for item in trace if item.decision != "exclude"}
    tasks: list[QueryTask] = []
    years = year_window(research_year)

    def add_family(
        kind: str,
        target: str | None,
        query_terms: tuple[str, ...],
    ) -> None:
        for task_year in years:
            queries = tuple(
                f"{context.authority_name} {context.province} {task_year} "
                f"{context.subject_group} {term}"
                for term in query_terms
            )
            tasks.append(
                _make_task(
                    kind=kind,
                    province=context.province,
                    year=task_year,
                    subject_group=context.subject_group,
                    authority_name=context.authority_name,
                    official_roots=context.official_roots,
                    target_name=target,
                    query_variants=queries,
                    research_year=research_year,
                    source_policy_id=policy.source_policy.policy_id,
                    source_policy_version=policy.source_policy.version,
                )
            )

    add_family(
        "province_policy",
        None,
        ("高考政策 考试模式", "批次设置 选科模式"),
    )
    add_family("score_table", None, ("一分一段表", "一分一段 位次"))
    add_family(
        "batch_admission",
        "普通批",
        ("普通批 投档录取", "普通批 院校专业组"),
    )
    if profile.high_school is None:
        add_family(
            "joy_report",
            None,
            ("高中喜报 高考光荣榜 高中升学成果",),
        )
    else:
        add_family(
            "joy_report",
            profile.high_school,
            (
                f"{profile.high_school} 高考喜报 高考光荣榜 高中升学成果",
            ),
        )
    add_family(
        "enrollment_plan",
        None,
        ("高校 招生计划 专业 计划数", "院校代码 专业代码 招生批次"),
    )
    add_family(
        "admission_charter",
        None,
        (
            "高校 招生章程 录取规则 调剂规则",
            "招生章程 体检 外语语种 单科 特殊条件",
        ),
    )
    add_family(
        "tuition_fee",
        None,
        (
            "高校 学费 收费标准 专业",
            "学费 住宿费 其他费用 奖助信息",
        ),
    )
    add_family(
        "subject_requirement",
        None,
        ("招生专业 选科要求", "院校专业 选考科目要求"),
    )

    for pathway_id in _PATHWAY_IDS:
        if pathway_id not in included:
            continue
        for identity in _PATHWAY_TASK_FAMILIES[pathway_id]:
            kind, target = identity
            terms = _PATHWAY_QUERY_TERMS.get(
                identity,
                (
                    f"{target} 报考条件 普通路径区别",
                    f"{target} 就业 地域限制 服务期 违约后果",
                    f"{target} 费用 补助 特殊限制",
                ),
            )
            add_family(kind, target, terms)

    return QueryPlan(
        schema_version=_SCHEMA_VERSION,
        province=context.province,
        mode=context.mode,
        exam_year=context.exam_year,
        research_year=research_year,
        subject_group=context.subject_group,
        authority_name=context.authority_name,
        official_roots=context.official_roots,
        catalog_verified_at=context.catalog_verified_at,
        catalog_digest=context.catalog_digest,
        decision_policy_id=policy.policy_id,
        decision_policy_digest=_policy_digest(policy),
        decision_basis_id=policy.basis.basis_id,
        decision_source_id=policy.basis.source_id,
        decision_source_version=policy.basis.source_version,
        source_policy_id=policy.source_policy.policy_id,
        source_policy_version=policy.source_policy.version,
        pathway_trace=trace,
        tasks=tuple(tasks),
    )


def build_query_plan(
    profile: PlanningProfile,
    catalog: ProvinceCatalogSnapshot,
    policy: DecisionPolicySnapshot,
) -> QueryPlan:
    """Build public research work from a confirmed profile and trusted catalog."""

    return _build_query_plan_for_year(
        profile,
        catalog,
        policy,
        research_year=_current_utc_year(),
    )


def validate_query_plan_for_profile(
    profile: PlanningProfile,
    plan: QueryPlan,
    *,
    catalog: ProvinceCatalogSnapshot | None = None,
) -> QueryPlan:
    """Replay every profile-derived trace and task against a canonical plan.

    Context fields alone are insufficient: pathway preferences and school
    context also change the task universe. Rebuilding with the plan-bound
    research year prevents a different canonical profile from silently
    authorizing a compatible-looking plan.
    """

    if type(profile) is not PlanningProfile:
        raise TypeError("profile must be a strict PlanningProfile")
    if type(plan) is not QueryPlan:
        raise TypeError("plan must be a strict QueryPlan")
    active_catalog = load_province_catalog() if catalog is None else catalog
    canonical = validate_query_plan_payload(
        plan.to_dict(),
        catalog=active_catalog,
    )
    expected = _build_query_plan_for_year(
        profile,
        active_catalog,
        DecisionPolicySnapshot.load_default(),
        research_year=canonical.research_year,
    )
    if expected.to_dict() != canonical.to_dict():
        raise QueryPlanInputError(
            "query plan does not match the complete profile-derived task universe"
        )
    return canonical


def validate_query_plan_payload(
    payload: Any,
    *,
    catalog: ProvinceCatalogSnapshot | None = None,
) -> QueryPlan:
    """Validate JSON semantics against one trusted province catalog snapshot."""

    if not isinstance(payload, dict) or set(payload) != _PLAN_FIELDS:
        raise ValueError("query-plan object fields do not match the contract")
    raw_tasks = payload["tasks"]
    if not isinstance(raw_tasks, list):
        raise TypeError("query-plan tasks must be an array")
    tasks: list[QueryTask] = []
    for raw_task in raw_tasks:
        if not isinstance(raw_task, dict) or set(raw_task) != _TASK_FIELDS:
            raise ValueError("query-task object fields do not match the contract")
        tasks.append(QueryTask(**raw_task))
    raw_trace = payload["pathway_trace"]
    if not isinstance(raw_trace, list):
        raise TypeError("query-plan pathway_trace must be an array")
    pathway_trace: list[PathwayResearchTrace] = []
    for raw_item in raw_trace:
        if not isinstance(raw_item, dict) or set(raw_item) != _PATHWAY_TRACE_FIELDS:
            raise ValueError("pathway trace fields do not match the contract")
        pathway_trace.append(PathwayResearchTrace(**raw_item))
    plan = QueryPlan(
        schema_version=payload["schema_version"],
        province=payload["province"],
        mode=payload["mode"],
        exam_year=payload["exam_year"],
        research_year=payload["research_year"],
        subject_group=payload["subject_group"],
        authority_name=payload["authority_name"],
        official_roots=tuple(payload["official_roots"]),
        catalog_verified_at=payload["catalog_verified_at"],
        catalog_digest=payload["catalog_digest"],
        decision_policy_id=payload["decision_policy_id"],
        decision_policy_digest=payload["decision_policy_digest"],
        decision_basis_id=payload["decision_basis_id"],
        decision_source_id=payload["decision_source_id"],
        decision_source_version=payload["decision_source_version"],
        source_policy_id=payload["source_policy_id"],
        source_policy_version=payload["source_policy_version"],
        pathway_trace=tuple(pathway_trace),
        tasks=tuple(tasks),
    )
    if plan.research_year > _current_utc_year():
        raise ValueError("query-plan research_year cannot be in the future")
    if catalog is None:
        catalog = load_province_catalog()
    if type(catalog) is not ProvinceCatalogSnapshot:
        raise TypeError("catalog must be a strict ProvinceCatalogSnapshot")
    if not _is_tracked_catalog(catalog):
        raise ProvinceCatalogError("query-plan validation requires the tracked trusted catalog")
    discovery = catalog.resolve(plan.province)
    default_policy = DecisionPolicySnapshot.load_default()
    if (
        discovery.province != plan.province
        or discovery.mode != plan.mode
        or discovery.authority_name != plan.authority_name
        or discovery.official_roots != plan.official_roots
        or catalog.verified_at != plan.catalog_verified_at
        or catalog.digest != plan.catalog_digest
    ):
        raise ValueError(
            "query-plan discovery metadata does not match the trusted catalog"
        )
    if (
        plan.decision_policy_id != default_policy.policy_id
        or plan.decision_policy_digest != _policy_digest(default_policy)
        or plan.decision_basis_id != default_policy.basis.basis_id
        or plan.decision_source_id != default_policy.basis.source_id
        or plan.decision_source_version != default_policy.basis.source_version
        or plan.source_policy_id != default_policy.source_policy.policy_id
        or plan.source_policy_version != default_policy.source_policy.version
    ):
        raise ValueError("query-plan decision metadata does not match the reviewed policy")
    return plan


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _reject_constant(_value: str) -> None:
    raise ValueError("non-finite JSON number")


def _strict_json_file(path_value: Any) -> Any:
    try:
        path = Path(path_value)
        before = os.lstat(path)
        if (
            not stat.S_ISREG(before.st_mode)
            or stat.S_ISLNK(before.st_mode)
            or before.st_size > _MAX_INPUT_BYTES
        ):
            raise ValueError("unsafe input file")
        data = path.read_bytes()
        after = os.lstat(path)
        if (
            before.st_dev,
            before.st_ino,
            before.st_size,
            before.st_mtime_ns,
        ) != (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
        ):
            raise ValueError("input file changed while reading")
        text = data.decode("utf-8")
        return json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("input is not strict UTF-8 JSON") from error


def _strict_json_bytes(data: Any) -> Any:
    if not isinstance(data, bytes) or len(data) > _MAX_INPUT_BYTES:
        raise ValueError("input is not bounded bytes")
    try:
        return json.loads(
            data.decode("utf-8"),
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("input is not strict UTF-8 JSON") from error


def _read_stdin_profile() -> Any:
    stream = getattr(sys.stdin, "buffer", None)
    if stream is None:
        text = sys.stdin.read(_MAX_INPUT_BYTES + 1)
        if not isinstance(text, str):
            raise ValueError("stdin did not provide text")
        data = text.encode("utf-8")
    else:
        data = stream.read(_MAX_INPUT_BYTES + 1)
    return _strict_json_bytes(data)


def _profile_array(payload: dict[str, Any], name: str) -> tuple[str, ...]:
    value = payload[name]
    if not isinstance(value, list):
        raise TypeError("profile collection must be an array")
    return _text_collection(value, f"profile {name}")


def _load_profile(path: Any) -> tuple[RecommendationProfile | PlanningProfile, str, int]:
    payload = _strict_json_file(path)
    if isinstance(payload, dict) and payload.get("schema_version") in {"2.0", "3.0"}:
        profile = load_planning_profile(payload)
        return profile, profile.subject_mode, profile.exam_year
    if not isinstance(payload, dict) or set(payload) != _PROFILE_FIELDS:
        raise ValueError("profile fields do not match the strict anonymous contract")
    if payload["schema_version"] != "1.0":
        raise ValueError("unsupported profile schema version")
    province = _public_text(payload["province"], "profile province")
    subject_mode = _public_text(payload["subject_mode"], "profile subject_mode")
    subject_group = _public_text(payload["subject_group"], "profile subject_group")
    _public_text(payload["grade"], "profile grade")
    current_year = _normalize_exam_year(payload["current_year"])
    secondary = _profile_array(payload, "secondary_subjects")
    majors = _profile_array(payload, "target_major_categories")
    cities = _profile_array(payload, "target_cities")
    schools = _profile_array(payload, "target_schools")
    _profile_array(payload, "eligibility_facts")
    profile = RecommendationProfile(
        rank=payload["rank"],
        target_province=province,
        subject_group=subject_group,
        secondary_subjects=frozenset(secondary),
        target_major_categories=majors,
        target_cities=cities,
        target_schools=schools,
    )
    return profile, subject_mode, current_year


def _load_province(path: Any) -> ProvinceConfig:
    payload = _strict_json_file(path)
    if not isinstance(payload, dict):
        raise ValueError("province input must be an object")
    absolute_path = Path(os.path.abspath(os.fspath(path)))
    return _parse_config(payload, absolute_path.parent)


def _parser() -> argparse.ArgumentParser:
    return _SafeArgumentParser(
        description="Build a deterministic research query plan from a v3 profile on stdin"
    )


def main(argv: list[str] | None = None) -> int:
    if sys.version_info < (3, 10) or _MISSING_LOCAL_CAPABILITY is not None:
        sys.stderr.write("query-plan: missing capability\n")
        return 3
    try:
        _parser().parse_args(argv)
        raw_profile = _read_stdin_profile()
        if not isinstance(raw_profile, dict) or raw_profile.get("schema_version") != "3.0":
            raise ValueError("public query-plan input must be a v3 profile")
        profile = PlanningProfile.create(raw_profile)
        catalog = load_province_catalog()
        policy = DecisionPolicySnapshot.load_default()
        plan = build_query_plan(profile, catalog, policy)
        payload = plan.to_dict()
        validate_query_plan_payload(payload, catalog=catalog)
        encoded = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        sys.stdout.write(encoded + "\n")
        return 0
    except QueryPlanCapabilityError:
        sys.stderr.write("query-plan: missing capability\n")
        return 3
    except (TypeError, ValueError, OSError, UnicodeError):
        sys.stderr.write("query-plan: invalid input\n")
        return 2


def _reconfigure_utf8() -> None:
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


__all__ = [
    "MAX_PROVINCE_ALIASES",
    "ProvinceCatalogError",
    "ProvinceCatalogSnapshot",
    "ProvinceDiscovery",
    "ResearchContext",
    "QueryPlan",
    "QueryPlanCapabilityError",
    "QueryTask",
    "build_query_plan",
    "load_province_catalog",
    "validate_query_plan_for_profile",
    "validate_query_plan_payload",
]


if __name__ == "__main__":
    _reconfigure_utf8()
    raise SystemExit(main())
