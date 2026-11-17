"""Immutable contracts and file guards for structured source adapters.

Importing this package is deliberately side-effect free.  The adapters accept
only caller-selected local files and never assign evidence trust tiers.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
import json
import math
import os
from pathlib import Path
import re
import stat
import unicodedata
from types import MappingProxyType
from typing import Any


MAX_FILE_BYTES = 25 * 1024 * 1024
_FILE_ATTRIBUTE_REPARSE_POINT = 0x400


class StructuredAdapterError(Exception):
    """Base class for controlled structured extraction failures."""


class StructuredFileError(StructuredAdapterError):
    """Raised when an input fails the local-file safety boundary."""


class MappingError(StructuredAdapterError):
    """Raised when an explicit column mapping cannot be applied exactly."""


class StructuredValidationError(StructuredAdapterError):
    """Raised when selected source data violates structural invariants."""


class PublicLocatorError(StructuredValidationError, ValueError):
    """A serialized adapter locator violates the public locator contract."""


class PublicLocatorPathError(PublicLocatorError):
    """A serialized adapter locator contains local or remote path material."""


class PublicLocatorPrivacyError(PublicLocatorError):
    """A serialized adapter locator contains personal or secret-shaped data."""


_LOCATOR_PHONE = re.compile(r"(?<![0-9])1[3-9][0-9]{9}(?![0-9])")
_LOCATOR_PHONE_SEPARATORS = re.compile(r"[\s._:\-‐-―]+")
_LOCATOR_IDENTITY = re.compile(r"[0-9]{17}[0-9Xx]")
_LOCATOR_LANDLINE = re.compile(r"(?<![0-9])0[0-9]{2,3}-?[0-9]{7,8}(?![0-9])")
_LOCATOR_LOCAL_PATH = re.compile(
    r"(?i)(?:[a-z]:[\\/]|//|/(?:home|users|tmp|var|etc|private|mnt|opt)(?:/|\]))"
)
_LOCATOR_DRIVE_PREFIX = re.compile(r"(?:^|[^A-Za-z0-9])[A-Za-z]:")
_LOCATOR_ENVIRONMENT = re.compile(
    r"%(?:[A-Za-z_][A-Za-z0-9_]*)%|\$(?:[A-Za-z_][A-Za-z0-9_]*|\{[A-Za-z_][A-Za-z0-9_]*\})"
)
_LOCATOR_SECRET = re.compile(
    r"(?i)(?:(?:api[\s_-]*key|password|bearer|private[\s_-]*key|token|secret)\s*[:=]|"
    r"(?<![a-z0-9])(?:gh[pousr]_[a-z0-9]{20,}|github_pat_[a-z0-9_]{20,}|"
    r"(?:akia|asia)[a-z0-9]{16}|sk-(?:proj-)?[a-z0-9_-]{20,}|"
    r"sk_(?:live|test)_[a-z0-9]{16,}|glpat-[a-z0-9_-]{20,}|"
    r"xox[baprs]-[a-z0-9-]{20,}|aiza[a-z0-9_-]{30,}|sk[-_](?:live|test))(?![a-z0-9]))"
)
_LOCATOR_EMBEDDED_ABSOLUTE = re.compile(r"(?:^|[\[({=:,\s])/(?!/)")
_LOCATOR_TRAVERSAL = re.compile(r"(?:^|[/\[({=:,\s])\.\.(?=$|[/\]})=,\s])")
_LOCATOR_HOME = re.compile(r"(?:^|[/\[({=:,\s])~(?:[/\\]|$)")


def validate_public_locator(value: Any) -> str:
    """Return one path-neutral, PII-safe locator without echoing rejected data."""

    if not isinstance(value, str):
        raise TypeError("public locator must be a string")
    if (
        not value
        or value != value.strip()
        or len(value) > 512
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        raise PublicLocatorError("public locator is unsafe")
    normalized = unicodedata.normalize("NFKC", value)
    compact = _LOCATOR_PHONE_SEPARATORS.sub("", normalized)
    if (
        _LOCATOR_PHONE.search(compact)
        or _LOCATOR_IDENTITY.search(compact)
        or _LOCATOR_LANDLINE.search(normalized)
        or _LOCATOR_SECRET.search(normalized)
        or "@" in normalized
    ):
        raise PublicLocatorPrivacyError("public locator contains private data")
    if (
        _LOCATOR_LOCAL_PATH.search(normalized)
        or _LOCATOR_DRIVE_PREFIX.search(normalized)
        or _LOCATOR_ENVIRONMENT.search(normalized)
        or _LOCATOR_EMBEDDED_ABSOLUTE.search(normalized)
        or _LOCATOR_TRAVERSAL.search(normalized)
        or _LOCATOR_HOME.search(normalized)
        or "\\" in normalized
        or "://" in normalized
        or normalized.startswith("/")
        or any(
            component in {".", "..", "~"} for component in normalized.split("/")
        )
    ):
        raise PublicLocatorPathError("public locator contains path material")
    return value


class CellStatus(str, Enum):
    """Finite extraction-state vocabulary, separate from evidence status."""

    EXACT = "exact"
    FORMULA = "formula"
    MERGED = "merged"
    EMPTY = "empty"
    MASKED = "masked"
    UNCERTAIN = "uncertain"
    INVALID = "invalid"


def _mathematical_integer(value: object, name: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a mathematical integer or null")
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite")
        if not value.is_integer():
            raise ValueError(f"{name} must be a mathematical integer")
    return int(value)


def _freeze_json(value: Any) -> Any:
    if isinstance(value, Enum):
        return _freeze_json(value.value)
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("contract values must be finite")
        return value
    if isinstance(value, Mapping):
        snapshot: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("contract mapping keys must be strings")
            if key in snapshot:
                raise ValueError("contract mapping keys must be unique")
            snapshot[key] = _freeze_json(item)
        return MappingProxyType(snapshot)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item) for item in value)
    raise TypeError(f"unsupported contract value type: {type(value).__name__}")


def _thaw_json(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {key: _thaw_json(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    if is_dataclass(value) and hasattr(value, "to_dict"):
        return value.to_dict()
    return value


def _ordered_warnings(value: object) -> tuple[str, ...]:
    if isinstance(value, (str, bytes, bytearray)):
        raise TypeError("warnings must be an ordered collection of strings")
    try:
        warnings = tuple(value)  # type: ignore[arg-type]
    except TypeError as error:
        raise TypeError("warnings must be an ordered collection of strings") from error
    for warning in warnings:
        if not isinstance(warning, str) or not warning or warning != warning.strip():
            raise ValueError("warnings must contain nonempty exact strings")
    return warnings


class _Serializable:
    def to_dict(self) -> dict[str, Any]:
        return {
            item.name: _thaw_json(getattr(self, item.name))
            for item in fields(self)
        }


@dataclass(frozen=True)
class ExtractedCoverage(_Serializable):
    lower_score: int | None = None
    upper_score: int | None = None
    lower_rank: int | None = None
    upper_rank: int | None = None

    def __post_init__(self) -> None:
        for name in ("lower_score", "upper_score", "lower_rank", "upper_rank"):
            object.__setattr__(self, name, _mathematical_integer(getattr(self, name), name))
        if self.lower_score is not None and self.upper_score is not None and self.lower_score > self.upper_score:
            raise ValueError("score coverage bounds are out of order")
        if self.lower_rank is not None and self.upper_rank is not None and self.lower_rank > self.upper_rank:
            raise ValueError("rank coverage bounds are out of order")


@dataclass(frozen=True)
class ExtractedRow(_Serializable):
    values: Mapping[str, Any]
    cell_status: Mapping[str, CellStatus | str]
    location: str
    confidence: float
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        frozen_values = _freeze_json(self.values)
        if not isinstance(frozen_values, Mapping):
            raise TypeError("values must be a mapping")
        if not isinstance(self.cell_status, Mapping):
            raise TypeError("cell_status must be a mapping")
        statuses: dict[str, CellStatus] = {}
        for key, status_value in self.cell_status.items():
            if not isinstance(key, str):
                raise TypeError("cell_status keys must be strings")
            if key in statuses:
                raise ValueError("cell_status keys must be unique")
            try:
                status_item = status_value if isinstance(status_value, CellStatus) else CellStatus(status_value)
            except (TypeError, ValueError) as error:
                raise ValueError("unknown cell status") from error
            statuses[key] = status_item
        if set(frozen_values) != set(statuses):
            raise ValueError("values and cell_status must contain identical keys")
        location = validate_public_locator(self.location)
        if isinstance(self.confidence, bool) or not isinstance(self.confidence, (int, float)):
            raise TypeError("confidence must be a finite number")
        confidence = float(self.confidence)
        if not math.isfinite(confidence) or not 0 <= confidence <= 1:
            raise ValueError("confidence must be between zero and one")
        object.__setattr__(self, "values", frozen_values)
        object.__setattr__(self, "cell_status", MappingProxyType(statuses))
        object.__setattr__(self, "location", location)
        object.__setattr__(self, "confidence", confidence)
        object.__setattr__(self, "warnings", _ordered_warnings(self.warnings))


@dataclass(frozen=True)
class ExtractedTable(_Serializable):
    table_id: str
    caption: str | None
    sheet: str | None
    rows: tuple[ExtractedRow, ...]
    coverage: ExtractedCoverage
    warnings: tuple[str, ...]
    extraction_method: str

    def __post_init__(self) -> None:
        table_id = validate_public_locator(self.table_id)
        if (
            not isinstance(self.extraction_method, str)
            or not self.extraction_method
            or self.extraction_method != self.extraction_method.strip()
        ):
            raise ValueError("extraction_method must be a nonempty exact string")
        for name in ("caption", "sheet"):
            value = getattr(self, name)
            if value is not None and (not isinstance(value, str) or not value or value != value.strip()):
                raise ValueError(f"{name} must be null or a nonempty exact string")
        if isinstance(self.rows, (str, bytes, bytearray)):
            raise TypeError("rows must be an ordered collection")
        try:
            rows = tuple(self.rows)
        except TypeError as error:
            raise TypeError("rows must be an ordered collection") from error
        if not all(isinstance(row, ExtractedRow) for row in rows):
            raise TypeError("rows must contain only ExtractedRow values")
        if not isinstance(self.coverage, ExtractedCoverage):
            raise TypeError("coverage must be ExtractedCoverage")
        object.__setattr__(self, "table_id", table_id)
        object.__setattr__(self, "rows", rows)
        object.__setattr__(self, "coverage", ExtractedCoverage(**self.coverage.to_dict()))
        object.__setattr__(self, "warnings", _ordered_warnings(self.warnings))


@dataclass(frozen=True, init=False)
class ColumnMapping(Mapping[str, tuple[str, ...]]):
    """Immutable explicit mapping from canonical fields to exact aliases."""

    columns: Mapping[str, tuple[str, ...]]
    roles: Mapping[str, str]
    score_scale: tuple[int, int] | None

    def __init__(
        self,
        columns: Mapping[str, object],
        *,
        roles: Mapping[str, str] | None = None,
        score_scale: Sequence[object] | None = None,
    ) -> None:
        if not isinstance(columns, Mapping):
            raise TypeError("mapping must be a mapping")
        entries = list(columns.items())
        snapshot: dict[str, tuple[str, ...]] = {}
        used_aliases: set[str] = set()
        for canonical, raw_aliases in entries:
            if not isinstance(canonical, str) or not canonical or canonical != canonical.strip():
                raise ValueError("canonical fields must be nonempty exact strings")
            if canonical in snapshot:
                raise ValueError("canonical fields must not repeat")
            if isinstance(raw_aliases, str):
                aliases = (raw_aliases,)
            elif isinstance(raw_aliases, Sequence) and not isinstance(raw_aliases, (bytes, bytearray)):
                aliases = tuple(raw_aliases)
            else:
                raise TypeError("header aliases must be a string or ordered strings")
            if not aliases:
                raise ValueError("header aliases must be nonempty")
            local: set[str] = set()
            for alias in aliases:
                if not isinstance(alias, str) or not alias or alias != alias.strip():
                    raise ValueError("header aliases must be nonempty exact strings")
                if alias in local or alias in used_aliases:
                    raise ValueError("header aliases must be globally unique")
                local.add(alias)
                used_aliases.add(alias)
            snapshot[canonical] = aliases
        if not snapshot:
            raise ValueError("mapping must contain at least one canonical field")

        if roles is None:
            role_items: list[tuple[str, str]] = []
        elif not isinstance(roles, Mapping):
            raise TypeError("roles must be a mapping")
        else:
            role_items = list(roles.items())
        role_snapshot: dict[str, str] = {}
        for field_name, role in role_items:
            if field_name not in snapshot:
                raise ValueError("numeric roles must reference mapped fields")
            if field_name in role_snapshot:
                raise ValueError("numeric roles must not repeat")
            if role not in {"score", "rank"}:
                raise ValueError("numeric role must be score or rank")
            role_snapshot[field_name] = role
        for field_name in snapshot:
            lowered = field_name.casefold()
            if field_name not in role_snapshot and (lowered == "score" or lowered.endswith("_score")):
                role_snapshot[field_name] = "score"
            elif field_name not in role_snapshot and (lowered == "rank" or lowered.endswith("_rank")):
                role_snapshot[field_name] = "rank"

        normalized_scale: tuple[int, int] | None = None
        if score_scale is not None:
            if not isinstance(score_scale, Sequence) or isinstance(score_scale, (str, bytes, bytearray)):
                raise TypeError("score_scale must be an ordered pair of integer bounds")
            if len(score_scale) != 2:
                raise ValueError("score_scale must contain exactly two integer bounds")
            lower = _mathematical_integer(score_scale[0], "score_scale lower")
            upper = _mathematical_integer(score_scale[1], "score_scale upper")
            if lower is None or upper is None or lower > upper:
                raise ValueError("score_scale bounds are out of order")
            normalized_scale = (lower, upper)

        object.__setattr__(self, "columns", MappingProxyType(snapshot))
        object.__setattr__(self, "roles", MappingProxyType(role_snapshot))
        object.__setattr__(self, "score_scale", normalized_scale)

    def __getitem__(self, key: str) -> tuple[str, ...]:
        return self.columns[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self.columns)

    def __len__(self) -> int:
        return len(self.columns)


def coerce_column_mapping(mapping: Mapping[str, object] | ColumnMapping) -> ColumnMapping:
    if isinstance(mapping, ColumnMapping):
        return ColumnMapping(mapping.columns, roles=mapping.roles, score_scale=mapping.score_scale)
    return ColumnMapping(mapping)


def resolve_headers(headers: list[str], mapping: ColumnMapping) -> dict[str, int]:
    duplicates = {header for header in headers if header and headers.count(header) > 1}
    if duplicates:
        raise MappingError("selected table contains duplicate headers")
    positions: dict[str, int] = {}
    used_positions: set[int] = set()
    for canonical, aliases in mapping.items():
        matches = [index for index, header in enumerate(headers) if header in aliases]
        if not matches:
            normalized_aliases = {alias.strip() for alias in aliases}
            if any(header.strip() in normalized_aliases for header in headers):
                raise MappingError("header matches only after whitespace normalization")
            raise MappingError("required mapped header is missing")
        if len(matches) != 1:
            raise MappingError("mapped header aliases are ambiguous")
        position = matches[0]
        if position in used_positions:
            raise MappingError("one source header cannot satisfy repeated canonical fields")
        positions[canonical] = position
        used_positions.add(position)
    return positions


def reject_duplicate_rows(rows: list[ExtractedRow]) -> None:
    seen: set[str] = set()
    for row in rows:
        if all(value is None for value in row.values.values()):
            continue
        key = json.dumps(row.to_dict()["values"], sort_keys=True, ensure_ascii=False, allow_nan=False)
        if key in seen:
            raise StructuredValidationError("duplicate semantic rows are ambiguous")
        seen.add(key)


def exact_rows(rows: list[ExtractedRow]) -> list[ExtractedRow]:
    return [row for row in rows if all(status is CellStatus.EXACT for status in row.cell_status.values())]


def validate_monotonicity(rows: list[ExtractedRow], mapping: ColumnMapping) -> None:
    for role, descending in (("score", True), ("rank", False)):
        fields_for_role = [field for field, declared in mapping.roles.items() if declared == role]
        for field in fields_for_role:
            sequence = [
                row.values[field]
                for row in rows
                if row.cell_status[field] is CellStatus.EXACT
                and isinstance(row.values[field], (int, float))
                and not isinstance(row.values[field], bool)
            ]
            for previous, current in zip(sequence, sequence[1:]):
                if (descending and current > previous) or (not descending and current < previous):
                    raise StructuredValidationError("numeric rows violate declared monotonic order")


def derive_coverage(
    rows: list[ExtractedRow], mapping: ColumnMapping
) -> tuple[ExtractedCoverage, list[str]]:
    exact = exact_rows(rows)
    role_values: dict[str, list[int]] = {"score": [], "rank": []}
    warnings: list[str] = []
    for field, role in mapping.roles.items():
        for row in exact:
            value = row.values[field]
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                continue
            if isinstance(value, float) and (not math.isfinite(value) or not value.is_integer()):
                if role == "score" and "coverage-nonintegral-score-excluded" not in warnings:
                    warnings.append("coverage-nonintegral-score-excluded")
                continue
            role_values[role].append(int(value))
    for role in ("score", "rank"):
        if role in mapping.roles.values() and not role_values[role]:
            warnings.append(f"coverage-{role}-unavailable")
    return (
        ExtractedCoverage(
            lower_score=min(role_values["score"]) if role_values["score"] else None,
            upper_score=max(role_values["score"]) if role_values["score"] else None,
            lower_rank=min(role_values["rank"]) if role_values["rank"] else None,
            upper_rank=max(role_values["rank"]) if role_values["rank"] else None,
        ),
        warnings,
    )


def read_stable_local_file(
    path: str | os.PathLike[str],
    *,
    suffixes: tuple[str, ...],
) -> bytes:
    """Read a small regular file while detecting links and path replacement."""

    if not isinstance(path, (str, os.PathLike)):
        raise StructuredFileError("input must be an absolute local file")
    try:
        raw = os.fspath(path)
    except Exception:
        raise StructuredFileError("input path could not be interpreted safely") from None
    if not isinstance(raw, str) or "://" in raw or raw.casefold().startswith("file:"):
        raise StructuredFileError("input must be an absolute local file")
    if (
        raw.startswith(("\\\\", "//"))
        or re.match(r"^[A-Za-z]:(?![\\/])", raw)
        or re.match(r"^[\\/](?:\?\?|globalroot)[\\/]", raw, flags=re.IGNORECASE)
    ):
        raise StructuredFileError("input must use a local filesystem namespace")
    candidate = Path(raw)
    if not candidate.is_absolute() or ".." in candidate.parts:
        raise StructuredFileError("input must be an absolute traversal-free local file")
    if candidate.suffix not in suffixes:
        raise StructuredFileError("input has an unsupported exact suffix")
    try:
        resolved = candidate.resolve(strict=True)
        before = candidate.lstat()
    except OSError:
        raise StructuredFileError("input file is unavailable") from None
    if resolved != candidate:
        raise StructuredFileError("input path must not traverse links or reparse points")
    if candidate.is_symlink() or getattr(before, "st_file_attributes", 0) & _FILE_ATTRIBUTE_REPARSE_POINT:
        raise StructuredFileError("linked or reparse-point inputs are not allowed")
    if not stat.S_ISREG(before.st_mode):
        raise StructuredFileError("input must be a regular file")
    if before.st_size > MAX_FILE_BYTES:
        raise StructuredFileError("input exceeds the size limit")
    identity = _file_identity(before)
    try:
        with candidate.open("rb") as handle:
            opened = os.fstat(handle.fileno())
            if _file_identity(opened) != identity:
                raise StructuredFileError("input identity changed during open")
            chunks: list[bytes] = []
            total = 0
            while True:
                chunk = handle.read(64 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_FILE_BYTES:
                    raise StructuredFileError("input exceeds the size limit")
                chunks.append(chunk)
            if _file_identity(os.fstat(handle.fileno())) != identity:
                raise StructuredFileError("input identity changed during read")
        after = candidate.lstat()
    except StructuredFileError:
        raise
    except OSError:
        raise StructuredFileError("input could not be read safely") from None
    if _file_identity(after) != identity:
        raise StructuredFileError("input identity changed during read")
    return b"".join(chunks)


def _file_identity(metadata: os.stat_result) -> tuple[int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_size,
        metadata.st_mtime_ns,
    )


def __getattr__(name: str) -> Any:
    """Lazily expose the rank bridge without creating an import cycle."""

    if name in {
        "RankBridgeError",
        "RankEvidenceBridge",
        "bridge_rank_evidence",
        "validate_rank_evidence_bridge",
    }:
        from . import rank_bridge

        return getattr(rank_bridge, name)
    raise AttributeError(name)


__all__ = [
    "CellStatus",
    "ColumnMapping",
    "ExtractedCoverage",
    "ExtractedRow",
    "ExtractedTable",
    "MAX_FILE_BYTES",
    "MappingError",
    "PublicLocatorError",
    "PublicLocatorPathError",
    "PublicLocatorPrivacyError",
    "RankBridgeError",
    "RankEvidenceBridge",
    "StructuredAdapterError",
    "StructuredFileError",
    "StructuredValidationError",
    "bridge_rank_evidence",
    "validate_rank_evidence_bridge",
    "validate_public_locator",
]
