"""Deterministic, province-mode-aware validation for public CSV datasets."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

if __package__:
    from .data_loader import (
        DataError,
        _normalize_admission_row,
        _read_csv_records,
    )
    from .province_registry import (
        ProvinceConfig,
        ProvinceConfigError,
        ProvincePathError,
        ProvinceRegistryError,
        _DirectoryIdentity,
        _parse_config,
        _read_metadata,
        canonical_subject_selection_key,
        validate_subject_selection,
    )
else:  # Direct ``python scripts/validate_data.py`` compatibility.
    from data_loader import DataError, _normalize_admission_row, _read_csv_records  # type: ignore
    from province_registry import (  # type: ignore
        ProvinceConfig,
        ProvinceConfigError,
        ProvincePathError,
        ProvinceRegistryError,
        _DirectoryIdentity,
        _parse_config,
        _read_metadata,
        canonical_subject_selection_key,
        validate_subject_selection,
    )


_INTEGER = re.compile(r"-?(?:0|[1-9][0-9]*)\Z")
_GROUP_SPLIT = re.compile(r"[+、，,/]" )

_KNOWN_TABLES = {
    "yifenyiduan": {
        "required_headers": ("year", "score", "rank", "cumulative_count", "subject_group"),
        "nonempty": ("year", "score", "rank", "cumulative_count", "subject_group"),
        "integers": ("year", "score", "rank", "cumulative_count"),
        "unique": ("year", "score", "subject_group"),
    },
    "tou_dang": {
        "required_headers": (
            "year", "province", "subject_group", "school_code", "school_name",
            "program_group", "min_score", "min_rank", "remarks",
        ),
        "nonempty": (
            "year", "province", "subject_group", "school_code", "school_name",
            "program_group", "min_score", "min_rank",
        ),
        "integers": ("year", "min_score", "min_rank"),
        "unique": (
            "year", "province", "subject_group", "school_code", "program_group", "remarks",
        ),
    },
    "xibao": {"required_headers": ("school_name", "year"), "nonempty": ("school_name", "year"), "integers": ("year",)},
    "schools": {"required_headers": ("school_name",), "nonempty": ("school_name",), "integers": ()},
    "qiangji": {"required_headers": ("year", "school_name", "major_name"), "nonempty": ("year", "school_name", "major_name"), "integers": ("year",)},
    "zongping": {"required_headers": ("year", "school_name"), "nonempty": ("year", "school_name"), "integers": ("year",)},
    "gangao": {"required_headers": ("year", "school_name"), "nonempty": ("year", "school_name"), "integers": ("year",)},
}


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    table: str
    path: str
    row: int | None = None
    field: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def sort_key(self) -> tuple[str, int, str, str, str]:
        return (
            self.path,
            self.row if self.row is not None else 0,
            self.field or "",
            self.code,
            self.message,
        )


def _cli_issue_dict(issue: ValidationIssue) -> dict[str, Any]:
    """Serialize one issue without exposing a caller-controlled local path."""

    payload = issue.to_dict()
    file_messages = {
        "duplicate_header": "文件级错误：CSV 表头包含重复字段",
        "unsafe_data_file": "文件级错误：CSV 无法安全读取",
        "data_file_changed": "文件级错误：CSV 在读取期间发生变化",
        "invalid_csv": "文件级错误：CSV 必须是严格 UTF-8 且格式有效",
    }
    if issue.code in file_messages:
        payload["message"] = file_messages[issue.code]
    if issue.table in _KNOWN_TABLES:
        payload["path"] = f"{issue.table}.csv"
    elif issue.table == "province":
        payload["path"] = "province.json"
    else:
        payload["path"] = "."
    return payload


_ADMISSION_METADATA_TEXT_FIELDS = frozenset(
    {
        "city_location",
        "school_province",
        "fee_currency",
        "fee_period",
        "affordability_policy_id",
        "affordability_policy_version",
        "affordability_policy_digest",
        "admission_evidence_row_hash",
        "subject_special_conditions",
        "school_fit_enrollment_status",
        "school_fit_subject_status",
        "school_fit_province_policy_status",
        "school_fit_charter_status",
        "school_fit_tuition_status",
        "school_fit_enrollment_current_status",
        "school_fit_subject_current_status",
        "school_fit_province_policy_current_status",
        "school_fit_charter_current_status",
        "school_fit_tuition_current_status",
        "province_policy_exam_mode",
        "province_policy_subject_structure",
        "province_policy_batch_structure",
        "province_policy_effective_date",
        "charter_admission_rules",
        "charter_adjustment_rules",
        "charter_health_restrictions",
        "charter_language_restrictions",
        "charter_single_subject_restrictions",
        "charter_special_conditions",
        "tuition_fee_currency",
        "tuition_fee_period",
        "tuition_other_required_fees",
        "tuition_financial_aid",
        "tuition_affordability_policy_id",
        "tuition_affordability_policy_version",
        "tuition_affordability_policy_digest",
    }
)
_ADMISSION_METADATA_TUPLE_FIELDS = frozenset(
    {
        "majors_in_group",
        "affordable_for",
        "required_secondary_subjects",
        "school_fit_source_ids",
        "school_fit_enrollment_source_ids",
        "school_fit_subject_source_ids",
        "school_fit_province_policy_source_ids",
        "school_fit_charter_source_ids",
        "school_fit_tuition_source_ids",
        "school_fit_enrollment_current_source_ids",
        "school_fit_subject_current_source_ids",
        "school_fit_province_policy_current_source_ids",
        "school_fit_charter_current_source_ids",
        "school_fit_tuition_current_source_ids",
        "school_fit_statuses",
        "school_fit_conflict_kinds",
        "tuition_majors",
        "tuition_affordable_for",
        "charter_unverified_fields",
        "tuition_unverified_fields",
    }
)
_INSTITUTION_TYPES = frozenset({"public", "private", "cooperative"})
_BUDGET_LEVEL_ORDER = ("limited", "moderate", "flexible")


def _canonical_metadata_text(value: Any, name: str) -> str:
    if (
        not isinstance(value, str)
        or not value
        or value != value.strip()
        or value != unicodedata.normalize("NFKC", value)
        or len(value) > 512
        or any(ord(char) < 32 or ord(char) == 127 for char in value)
    ):
        raise ValueError(f"runtime admission {name} must be canonical exact text")
    return value


def _canonical_metadata_tuple(value: Any, name: str) -> tuple[str, ...]:
    if not isinstance(value, tuple) or (
        not value and name != "required_secondary_subjects"
    ):
        raise TypeError(f"runtime admission {name} must be a non-empty canonical tuple")
    items = tuple(_canonical_metadata_text(item, name) for item in value)
    if len(items) != len(set(items)):
        raise ValueError(f"runtime admission {name} must be unique")
    expected = (
        tuple(item for item in _BUDGET_LEVEL_ORDER if item in items)
        if name in {"affordable_for", "tuition_affordable_for"}
        else tuple(sorted(items))
    )
    if items != expected:
        raise ValueError(f"runtime admission {name} must use canonical ordering")
    if name in {"affordable_for", "tuition_affordable_for"} and any(
        item not in _BUDGET_LEVEL_ORDER for item in items
    ):
        raise ValueError("runtime admission affordable_for contains an unknown level")
    return items


@dataclass(frozen=True)
class ValidatedAdmissionRow:
    """One normalized admission row captured by the validator's secure read."""

    _items: tuple[tuple[str, str | int | bool | tuple[str, ...]], ...]

    def __post_init__(self) -> None:
        if not self._items or tuple(sorted(self._items)) != self._items:
            raise ValueError("validated admission row must be a sorted non-empty snapshot")
        if len({key for key, _value in self._items}) != len(self._items):
            raise ValueError("validated admission row keys must be unique")
        for key, value in self._items:
            if not isinstance(key, str) or not key:
                raise TypeError("validated admission row keys must be non-empty text")
            if key in _ADMISSION_METADATA_TUPLE_FIELDS:
                _canonical_metadata_tuple(value, key)
            elif key in _ADMISSION_METADATA_TEXT_FIELDS:
                _canonical_metadata_text(value, key)
            elif key == "institution_type":
                if value not in _INSTITUTION_TYPES:
                    raise ValueError(
                        "validated admission institution_type is unsupported"
                    )
            elif key in {"adjustment_required", "charter_adjustment_required"}:
                if not isinstance(value, bool):
                    raise TypeError(
                        f"validated admission {key} must be boolean"
                    )
            elif key == "secondary_subject_rule":
                if value not in {"any", "all"}:
                    raise ValueError(
                        "validated admission secondary_subject_rule is unsupported"
                    )
            elif key in {
                "annual_fee_amount",
                "tuition_annual_fee_amount",
                "tuition_accommodation_fee",
            }:
                if (
                    not isinstance(value, int)
                    or isinstance(value, bool)
                    or value < 0
                ):
                    raise ValueError(
                        "validated admission annual_fee_amount must be non-negative"
                    )
            elif not isinstance(value, (str, int)) or isinstance(value, bool):
                raise TypeError(
                    "validated admission row must contain canonical JSON fields"
                )

    @classmethod
    def from_mapping(cls, row: Mapping[str, Any]) -> "ValidatedAdmissionRow":
        return cls(tuple(sorted(row.items())))

    def to_dict(self) -> dict[str, Any]:
        return dict(self._items)

    def _value(self, name: str) -> Any:
        return dict(self._items)[name]

    @property
    def year(self) -> int:
        return int(self._value("year"))

    @property
    def school_code(self) -> str:
        return str(self._value("school_code"))

    @property
    def school_name(self) -> str:
        return str(self._value("school_name"))

    @property
    def program_group(self) -> str:
        return str(self._value("program_group"))

    @property
    def min_score(self) -> int:
        return int(self._value("min_score"))

    @property
    def min_rank(self) -> int:
        return int(self._value("min_rank"))


def admission_row_hash(row: ValidatedAdmissionRow) -> str:
    """Bind every current and future normalized field in one canonical digest."""

    if not isinstance(row, ValidatedAdmissionRow):
        raise TypeError("row must be a ValidatedAdmissionRow")
    canonical = json.dumps(
        row.to_dict(),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ValidatedScoreRow:
    """One score-table row captured by the validator's authenticated read."""

    _items: tuple[tuple[str, str | int], ...]

    def __post_init__(self) -> None:
        expected = {"year", "score", "rank", "cumulative_count", "subject_group"}
        if tuple(sorted(self._items)) != self._items:
            raise ValueError("validated score row must be a sorted snapshot")
        if {key for key, _value in self._items} != expected:
            raise ValueError("validated score row fields do not match the contract")
        payload = dict(self._items)
        for name in ("year", "score", "rank", "cumulative_count"):
            value = payload[name]
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError(f"validated score row {name} must be an integer")
        if not isinstance(payload["subject_group"], str) or not payload["subject_group"]:
            raise TypeError("validated score row subject_group must be non-empty text")
        if payload["rank"] < 1 or payload["cumulative_count"] < 1:
            raise ValueError("validated score row ranks must be positive")

    @classmethod
    def from_mapping(cls, row: dict[str, str | int]) -> "ValidatedScoreRow":
        return cls(tuple(sorted(row.items())))

    def to_dict(self) -> dict[str, str | int]:
        return dict(self._items)

    def _value(self, name: str) -> str | int:
        return dict(self._items)[name]

    @property
    def year(self) -> int:
        return int(self._value("year"))

    @property
    def score(self) -> int:
        return int(self._value("score"))

    @property
    def rank(self) -> int:
        return int(self._value("rank"))

    @property
    def cumulative_count(self) -> int:
        return int(self._value("cumulative_count"))

    @property
    def subject_group(self) -> str:
        return str(self._value("subject_group"))


@dataclass(frozen=True)
class RuntimeCalculationPolicy:
    """The policy information Task 3 actually supplies, without fake deltas."""

    policy_id: str
    basis_id: str
    tier_caps: Mapping[str, int]
    rank_delta_status: str = "unavailable"

    def __post_init__(self) -> None:
        if (
            not isinstance(self.policy_id, str)
            or not self.policy_id
            or not isinstance(self.basis_id, str)
            or not self.basis_id
        ):
            raise ValueError("runtime calculation policy identities are required")
        if self.rank_delta_status != "unavailable":
            raise ValueError("rank delta policy must remain explicitly unavailable")
        if not isinstance(self.tier_caps, Mapping) or set(self.tier_caps) != {"冲", "稳", "保"}:
            raise ValueError("runtime tier caps must contain exactly 冲, 稳, 保")
        caps = dict(self.tier_caps)
        if any(not isinstance(value, int) or isinstance(value, bool) or value < 1 for value in caps.values()):
            raise ValueError("runtime tier caps must be positive integers")
        object.__setattr__(self, "tier_caps", MappingProxyType(caps))

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "basis_id": self.basis_id,
            "tier_caps": dict(self.tier_caps),
            "rank_delta_status": self.rank_delta_status,
        }


def validate_runtime_score_row(
    row: Mapping[str, Any],
    *,
    score_scale: int,
    subject_group: str,
    allowed_years: tuple[int, ...],
) -> ValidatedScoreRow:
    """Validate one authenticated in-memory score row without filesystem I/O."""

    if not isinstance(row, Mapping) or set(row) != {
        "year", "score", "rank", "cumulative_count", "subject_group"
    }:
        raise ValueError("runtime score row fields do not match the contract")
    result = ValidatedScoreRow.from_mapping(dict(row))
    payload = result.to_dict()
    if payload["year"] not in allowed_years:
        raise ValueError("runtime score row year is outside the query window")
    if payload["subject_group"] != subject_group:
        raise ValueError("runtime score row subject does not match the query plan")
    if not 0 <= payload["score"] <= score_scale:
        raise ValueError("runtime score row is outside the profile score scale")
    if payload["cumulative_count"] < payload["rank"]:
        raise ValueError("runtime cumulative count cannot be below rank")
    return result


def validate_runtime_admission_row(
    row: Mapping[str, Any],
    *,
    province: str,
    subject_group: str,
    score_scale: int,
    allowed_years: tuple[int, ...],
) -> ValidatedAdmissionRow:
    """Validate one authenticated in-memory admission row and its full hash."""

    required = {
        "year", "province", "subject_group", "school_code", "school_name",
        "program_group", "min_score", "min_rank", "remarks",
    }
    allowed = required | {
        "major_group_name",
        *_ADMISSION_METADATA_TEXT_FIELDS,
        *_ADMISSION_METADATA_TUPLE_FIELDS,
        "institution_type",
        "adjustment_required",
    }
    if not isinstance(row, Mapping) or not required.issubset(row) or not set(row) <= allowed:
        raise ValueError("runtime admission row fields do not match the contract")
    result = ValidatedAdmissionRow.from_mapping(dict(row))
    payload = result.to_dict()
    if payload["year"] not in allowed_years:
        raise ValueError("runtime admission row year is outside the query window")
    if payload["province"] != province or payload["subject_group"] != subject_group:
        raise ValueError("runtime admission row context does not match the query plan")
    if not isinstance(payload["min_score"], int) or isinstance(payload["min_score"], bool) or not 0 <= payload["min_score"] <= score_scale:
        raise ValueError("runtime admission score is outside the profile score scale")
    if not isinstance(payload["min_rank"], int) or isinstance(payload["min_rank"], bool) or payload["min_rank"] < 1:
        raise ValueError("runtime admission rank must be a positive integer")
    for name in ("school_code", "school_name", "program_group"):
        if not isinstance(payload[name], str) or not payload[name] or payload[name] != payload[name].strip():
            raise ValueError("runtime admission identities must be exact text")
    for name in _ADMISSION_METADATA_TEXT_FIELDS & set(payload):
        _canonical_metadata_text(payload[name], name)
    if "majors_in_group" in payload:
        _canonical_metadata_tuple(payload["majors_in_group"], "majors_in_group")
    if "institution_type" in payload:
        if payload["institution_type"] not in _INSTITUTION_TYPES:
            raise ValueError("runtime admission institution_type is unsupported")
    if "affordable_for" in payload:
        _canonical_metadata_tuple(payload["affordable_for"], "affordable_for")
    if "adjustment_required" in payload and not isinstance(
        payload["adjustment_required"], bool
    ):
        raise TypeError("runtime admission adjustment_required must be boolean")
    admission_row_hash(result)
    return result


@dataclass(frozen=True)
class ValidatedDatasetSnapshot:
    """Authenticated province metadata and data parsed during one validation pass."""

    config: ProvinceConfig
    admission_rows: tuple[ValidatedAdmissionRow, ...]
    score_rows: tuple[ValidatedScoreRow, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.config, ProvinceConfig):
            raise TypeError("snapshot config must be ProvinceConfig")
        rows = tuple(self.admission_rows)
        if not all(isinstance(row, ValidatedAdmissionRow) for row in rows):
            raise TypeError("snapshot rows must be ValidatedAdmissionRow records")
        object.__setattr__(self, "admission_rows", rows)
        score_rows = tuple(self.score_rows)
        if not all(isinstance(row, ValidatedScoreRow) for row in score_rows):
            raise TypeError("snapshot score_rows must be ValidatedScoreRow records")
        object.__setattr__(self, "score_rows", score_rows)

    def validate_subjects(
        self,
        primary_subject: str,
        secondary_subjects: tuple[str, ...],
    ) -> None:
        validate_subject_selection(
            self.config,
            primary_subject,
            list(secondary_subjects),
        )


@dataclass(frozen=True)
class DatasetValidationResult:
    snapshot: ValidatedDatasetSnapshot | None
    issues: tuple[ValidationIssue, ...]

    def __post_init__(self) -> None:
        issues = tuple(self.issues)
        if not all(isinstance(issue, ValidationIssue) for issue in issues):
            raise TypeError("validation result issues must be ValidationIssue records")
        if (self.snapshot is None) == (not issues):
            raise ValueError("validation result must contain exactly snapshot or issues")
        object.__setattr__(self, "issues", issues)


def _issue(
    code: str,
    message: str,
    table: str,
    path: Path,
    row: int | None = None,
    field: str | None = None,
) -> ValidationIssue:
    return ValidationIssue(code, message, table, os.fspath(path), row, field)


def _verify_dataset_identity(
    parent: _DirectoryIdentity, child: _DirectoryIdentity
) -> None:
    parent.verify("省份数据父目录")
    child.verify("省份数据目录")
    if child.path.parent != parent.path:
        raise ProvincePathError("省份数据目录在校验期间越出父目录")


def _load_config(
    parent: _DirectoryIdentity, child: _DirectoryIdentity
) -> ProvinceConfig:
    _verify_dataset_identity(parent, child)
    document = _read_metadata(parent, child)
    if document is None:
        raise DataError(f"省份配置缺失：{child.path / 'province.json'}")
    document.verify(parent)
    config = _parse_config(document.payload, child.path)
    _verify_dataset_identity(parent, child)
    return config


def _canonical_headers(table: str, headers: tuple[str, ...]) -> set[str]:
    result = set(headers)
    if table == "tou_dang":
        if "remarks" not in result and "remark" in result:
            result.add("remarks")
        if "program_group" not in result and "major_group_name" in result:
            result.add("program_group")
    return result


def _valid_subject_group(config: ProvinceConfig, raw: str) -> bool:
    if not raw or raw != raw.strip():
        return False
    subjects = tuple(part.strip() for part in _GROUP_SPLIT.split(raw))
    if config.mode == "3+1+2":
        return len(subjects) == 1 and raw in config.primary_subjects
    if len(subjects) != 3:
        return False
    try:
        return raw == canonical_subject_selection_key(
            config, subjects[0], list(subjects[1:])
        )
    except ProvinceRegistryError:
        return False


def _integer(raw: str) -> int | None:
    if not isinstance(raw, str) or _INTEGER.fullmatch(raw) is None:
        return None
    try:
        return int(raw)
    except ValueError:
        return None


def _validate_table(
    path: Path,
    table: str,
    config: ProvinceConfig,
    parent_identity: _DirectoryIdentity,
    dataset_identity: _DirectoryIdentity,
    operation_hook: Callable[[], None] | None = None,
) -> tuple[
    list[ValidationIssue],
    tuple[ValidatedAdmissionRow, ...],
    tuple[ValidatedScoreRow, ...],
]:
    issues: list[ValidationIssue] = []
    rule = _KNOWN_TABLES[table]
    _verify_dataset_identity(parent_identity, dataset_identity)
    try:
        headers, rows = _read_csv_records(
            path,
            _parent_identity=dataset_identity,
            _operation_hook=operation_hook,
        )
    except DataError as error:
        _verify_dataset_identity(parent_identity, dataset_identity)
        text = str(error)
        code = "duplicate_header" if "重复字段" in text else "unsafe_data_file"
        if "发生变化" in text:
            code = "data_file_changed"
        if "格式损坏" in text or "严格 UTF-8" in text:
            code = "invalid_csv"
        return [_issue(code, f"文件级错误：{text}", table, path)], (), ()
    _verify_dataset_identity(parent_identity, dataset_identity)

    if not headers or not rows:
        return [_issue("empty_file", "文件级错误：文件为空（无数据行）", table, path)], (), ()

    canonical_headers = _canonical_headers(table, headers)
    missing = [field for field in rule["required_headers"] if field not in canonical_headers]
    if missing:
        return [
            _issue(
                "missing_required_header",
                "文件级错误：表头缺少必填字段 " + "、".join(missing),
                table,
                path,
            )
        ], (), ()

    seen: set[tuple[str, ...]] = set()
    school_identities: dict[tuple[int, str, str], str] = {}
    valid_years: set[int] = set()
    admission_rows: list[ValidatedAdmissionRow] = []
    score_rows: list[ValidatedScoreRow] = []
    for line, source_row in enumerate(rows, start=2):
        try:
            row = _normalize_admission_row(source_row) if table == "tou_dang" else source_row
        except DataError:
            issues.append(_issue("alias_conflict", f"行{line}：字段迁移别名冲突", table, path, line))
            continue

        if table == "tou_dang":
            typed_row: dict[str, str | int] = dict(row)
            for integer_field in rule["integers"]:
                parsed_value = _integer(row.get(integer_field, ""))
                if parsed_value is not None:
                    typed_row[integer_field] = parsed_value
            typed_row["major_group_name"] = row.get("program_group", "")
            admission_rows.append(ValidatedAdmissionRow.from_mapping(typed_row))

        for field in rule["nonempty"]:
            value = row.get(field, "")
            if not isinstance(value, str) or not value.strip():
                issues.append(_issue("required_value_missing", f"行{line}：必填字段 {field} 为空", table, path, line, field))

        parsed: dict[str, int] = {}
        for field in rule["integers"]:
            raw = row.get(field, "")
            number = _integer(raw)
            if number is None:
                issues.append(_issue("invalid_integer", f"行{line}：{field} 不是严格整数", table, path, line, field))
            else:
                parsed[field] = number

        if table == "yifenyiduan" and set(rule["integers"]) <= set(parsed):
            score_rows.append(
                ValidatedScoreRow.from_mapping(
                    {
                        "year": parsed["year"],
                        "score": parsed["score"],
                        "rank": parsed["rank"],
                        "cumulative_count": parsed["cumulative_count"],
                        "subject_group": row.get("subject_group", "").strip(),
                    }
                )
            )

        year = parsed.get("year")
        if year is not None:
            if 2000 <= year <= 2100:
                valid_years.add(year)
            else:
                issues.append(_issue("year_out_of_range", f"行{line}：year 超出 2000..2100", table, path, line, "year"))

        for field in ("rank", "min_rank", "cumulative_count"):
            if field in parsed and parsed[field] < 1:
                issues.append(_issue("rank_out_of_range", f"行{line}：{field} 必须大于等于 1", table, path, line, field))

        for field in ("score", "min_score"):
            if field in parsed and not 0 <= parsed[field] <= config.score_scale:
                issues.append(_issue("score_out_of_range", f"行{line}：{field} 超出省份量表范围", table, path, line, field))

        if table in ("yifenyiduan", "tou_dang"):
            subject = row.get("subject_group", "")
            if not _valid_subject_group(config, subject):
                issues.append(_issue("invalid_subject_group", f"行{line}：subject_group 不符合省份考试模式", table, path, line, "subject_group"))
        if table == "tou_dang" and row.get("province", "").strip() != config.province:
            issues.append(_issue("province_mismatch", f"行{line}：province 与 province.json 不一致", table, path, line, "province"))
        if table == "tou_dang" and year is not None:
            province = row.get("province", "").strip()
            school_code = row.get("school_code", "").strip()
            school_name = row.get("school_name", "").strip()
            if province and school_code and school_name:
                identity_key = (year, province, school_code)
                existing_name = school_identities.get(identity_key)
                if existing_name is None:
                    school_identities[identity_key] = school_name
                elif existing_name != school_name:
                    issues.append(
                        _issue(
                            "conflicting_school_identity",
                            f"行{line}：同一年度、省份和院校代码对应多个院校名称",
                            table,
                            path,
                            line,
                            "school_name",
                        )
                    )

        unique_fields = rule.get("unique")
        if unique_fields:
            key = tuple(row.get(field, "").strip() for field in unique_fields)
            required_key_values = tuple(
                row.get(field, "").strip()
                for field in unique_fields
                if field in rule["nonempty"]
            )
            if all(required_key_values):
                if key in seen:
                    code = "duplicate_admission_key" if table == "tou_dang" else "duplicate_row_key"
                    issues.append(_issue(code, f"行{line}：唯一键重复", table, path, line))
                else:
                    seen.add(key)

    if "year" in rule["integers"] and not valid_years:
        issues.append(_issue("missing_year_coverage", "文件级错误：没有 2000..2100 内的有效年份覆盖", table, path))
    _verify_dataset_identity(parent_identity, dataset_identity)
    return issues, tuple(admission_rows), tuple(score_rows)


def validate_dataset(province_dir: os.PathLike[str] | str) -> list[ValidationIssue]:
    """Return a sorted issue list; malformed user data never escapes as a parser error."""

    return list(_validate_dataset_snapshot(province_dir).issues)


def validate_dataset_snapshot(
    province_dir: os.PathLike[str] | str,
) -> DatasetValidationResult:
    """Validate and return only data parsed by the authenticated secure reads."""

    return _validate_dataset_snapshot(province_dir)


def _validate_dataset(
    province_dir: os.PathLike[str] | str,
    *,
    operation_hook: Callable[[], None] | None = None,
    table_operation_hook: Callable[[str, Path], None] | None = None,
) -> list[ValidationIssue]:
    """Internal implementation with deterministic filesystem race-test seams."""

    return list(
        _validate_dataset_snapshot(
            province_dir,
            operation_hook=operation_hook,
            table_operation_hook=table_operation_hook,
        ).issues
    )


def _validate_dataset_snapshot(
    province_dir: os.PathLike[str] | str,
    *,
    operation_hook: Callable[[], None] | None = None,
    table_operation_hook: Callable[[str, Path], None] | None = None,
) -> DatasetValidationResult:
    """Internal authenticated snapshot implementation with race-test seams."""

    try:
        candidate = Path(province_dir)
        normalized = Path(os.path.abspath(os.fspath(candidate)))
        if not candidate.is_absolute() or candidate != normalized:
            return DatasetValidationResult(None, (_issue("unsafe_dataset_path", "数据目录必须是已解析的绝对规范路径", "dataset", normalized),))
        parent_identity = _DirectoryIdentity.capture(normalized.parent, "省份数据父目录")
        dataset_identity = _DirectoryIdentity.capture(normalized, "省份数据目录")
        _verify_dataset_identity(parent_identity, dataset_identity)
        config = _load_config(parent_identity, dataset_identity)
    except ProvincePathError:
        return DatasetValidationResult(None, (_issue("dataset_path_changed", "省份数据目录在校验期间发生变化", "dataset", normalized),))
    except (DataError, ProvinceConfigError, ProvinceRegistryError, OSError, RuntimeError, TypeError, ValueError):
        path = Path(os.path.abspath(os.fspath(province_dir))) if isinstance(province_dir, (str, os.PathLike)) else Path(".").resolve()
        return DatasetValidationResult(None, (_issue("invalid_province_config", "province.json 未通过严格配置校验", "province", path / "province.json"),))

    directory = dataset_identity.path
    found = 0
    issues: list[ValidationIssue] = []
    admission_rows: tuple[ValidatedAdmissionRow, ...] = ()
    score_rows: tuple[ValidatedScoreRow, ...] = ()
    try:
        if operation_hook is not None:
            operation_hook()
        _verify_dataset_identity(parent_identity, dataset_identity)
        for table in sorted(_KNOWN_TABLES):
            _verify_dataset_identity(parent_identity, dataset_identity)
            path = directory / f"{table}.csv"
            try:
                os.lstat(path)
            except FileNotFoundError:
                continue
            except OSError:
                found += 1
                issues.append(_issue("unsafe_data_file", "文件级错误：CSV 无法安全检查", table, path))
                continue
            found += 1
            table_hook = None
            if table_operation_hook is not None:
                table_hook = lambda table=table, path=path: table_operation_hook(table, path)
            table_issues, table_rows, table_score_rows = _validate_table(
                path,
                table,
                config,
                parent_identity,
                dataset_identity,
                table_hook,
            )
            issues.extend(table_issues)
            if table == "tou_dang":
                admission_rows = table_rows
            if table == "yifenyiduan":
                score_rows = table_score_rows
            _verify_dataset_identity(parent_identity, dataset_identity)
        _verify_dataset_identity(parent_identity, dataset_identity)
        if found == 0:
            issues.append(_issue("no_known_data_files", "目录内未找到任何已知数据文件", "dataset", directory))
        _verify_dataset_identity(parent_identity, dataset_identity)
        ordered = tuple(sorted(issues, key=ValidationIssue.sort_key))
        if ordered:
            return DatasetValidationResult(None, ordered)
        return DatasetValidationResult(
            ValidatedDatasetSnapshot(
                config=config,
                admission_rows=admission_rows,
                score_rows=score_rows,
            ),
            (),
        )
    except ProvincePathError:
        return DatasetValidationResult(None, (_issue("dataset_path_changed", "省份数据目录在校验期间发生变化", "dataset", directory),))


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    parser = argparse.ArgumentParser(description="校验一个已解析的省份数据目录")
    parser.add_argument("dataset", nargs="?", help="省份数据目录")
    parser.add_argument("--province-dir", dest="legacy_dataset", help="已弃用：请改用位置参数")
    args = parser.parse_args(argv)
    if bool(args.dataset) == bool(args.legacy_dataset):
        parser.error("必须且只能提供位置参数 dataset 或 --province-dir")
    requested = Path(args.dataset or args.legacy_dataset)
    try:
        directory = requested.resolve(strict=True)
    except (OSError, RuntimeError):
        directory = Path(os.path.abspath(os.fspath(requested)))
    issues = validate_dataset(directory)
    payload = {
        "valid": not issues,
        "directory": ".",
        "issues": [_cli_issue_dict(item) for item in issues],
    }
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0 if not issues else 2


if __name__ == "__main__":
    raise SystemExit(main())
