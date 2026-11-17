"""Validate a finalized evidence bundle before deterministic calculation.

The validator is deliberately standard-library-only.  It reads only the
fixed artifacts emitted by :class:`scripts.evidence.EvidenceStore`, validates
their complete serialized shape, recomputes the store's canonical manifest
hash, and reapplies the shared source-independence policy.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any, Callable

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.contracts import (  # noqa: E402
    CapabilityReport,
    CapabilityTier,
    EvidenceManifest,
    EvidenceStatus,
    FactClaim,
    SourceCandidate,
    SourceTier,
)
from scripts.evidence import (  # noqa: E402
    FACT_PROVENANCE_KIND,
    EvidencePathError,
    EvidencePrivacyError,
    EvidenceStore,
    _canonical_fact_provenance,
    _PII_KEYS,
    _normalize_key,
    _reject_pii_identifier,
    _reject_pii_keys,
)
from scripts.source_policy import (  # noqa: E402
    canonicalize_provenance_url,
    deduplicate_candidates,
    evaluate_claims,
)


_EXPECTED_ARTIFACTS = (
    "manifest.json",
    "capability.json",
    "candidates.jsonl",
    "context.jsonl",
    "normalized/facts.jsonl",
    "rejections.jsonl",
)
_MAX_ARTIFACT_BYTES = 8 * 1024 * 1024
_MAX_BUNDLE_BYTES = 24 * 1024 * 1024
_REPARSE_POINT = 0x0400
_SOURCE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_PROVENANCE_FIELDS = {
    "kind", "fact_id", "source_ids", "year", "extraction_method", "locator"
}


@dataclass(frozen=True)
class FrozenJsonRecord:
    """Canonical JSON object whose callers only receive detached copies."""

    _canonical_json: str

    @classmethod
    def _from_mapping(cls, value: dict[str, Any]) -> "FrozenJsonRecord":
        return cls(
            json.dumps(
                value,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            )
        )

    def to_dict(self) -> dict[str, Any]:
        value = json.loads(self._canonical_json)
        if not isinstance(value, dict):  # Defensive invariant for corrupted instances.
            raise TypeError("frozen JSON record is not an object")
        return value


def _snapshot_records(value: Any, label: str) -> tuple[FrozenJsonRecord, ...]:
    if isinstance(value, (str, bytes, bytearray)):
        raise TypeError(f"{label} must be frozen JSON records")
    try:
        records = tuple(value)
    except TypeError:
        raise TypeError(f"{label} must be frozen JSON records") from None
    if any(type(item) is not FrozenJsonRecord for item in records):
        raise TypeError(f"{label} must be frozen JSON records")
    return tuple(FrozenJsonRecord._from_mapping(item.to_dict()) for item in records)


def _facts_digest(facts: tuple[FrozenJsonRecord, ...]) -> str:
    encoded = json.dumps(
        [item.to_dict() for item in facts],
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True, init=False)
class ValidatedEvidenceSnapshot:
    """Immutable bundle snapshot with a diagnostic canonical facts digest."""

    manifest: EvidenceManifest
    capability: CapabilityReport
    retrieval_dates: tuple[str, ...]
    facts: tuple[FrozenJsonRecord, ...]
    rejections: tuple[FrozenJsonRecord, ...]
    candidates: tuple[FrozenJsonRecord, ...]
    contexts: tuple[FrozenJsonRecord, ...]
    manifest_hash: str
    facts_digest: str

    def __init__(self) -> None:
        raise TypeError("ValidatedEvidenceSnapshot is factory-only")

    @classmethod
    def _create(
        cls,
        manifest: EvidenceManifest,
        capability: CapabilityReport,
        retrieval_dates: tuple[str, ...],
        facts: tuple[FrozenJsonRecord, ...],
        rejections: tuple[FrozenJsonRecord, ...],
        *,
        candidates: tuple[FrozenJsonRecord, ...] = (),
        contexts: tuple[FrozenJsonRecord, ...] = (),
    ) -> "ValidatedEvidenceSnapshot":
        fact_records = _snapshot_records(facts, "facts")
        rejection_records = _snapshot_records(rejections, "rejections")
        candidate_records = _snapshot_records(candidates, "candidates")
        context_records = _snapshot_records(contexts, "contexts")
        digest = _facts_digest(fact_records)
        instance = object.__new__(cls)
        object.__setattr__(instance, "manifest", manifest)
        object.__setattr__(instance, "capability", capability)
        object.__setattr__(instance, "retrieval_dates", tuple(retrieval_dates))
        object.__setattr__(instance, "facts", fact_records)
        object.__setattr__(instance, "rejections", rejection_records)
        object.__setattr__(instance, "candidates", candidate_records)
        object.__setattr__(instance, "contexts", context_records)
        object.__setattr__(instance, "manifest_hash", manifest.manifest_hash)
        object.__setattr__(instance, "facts_digest", digest)
        return instance


@dataclass(frozen=True)
class EvidenceValidationResult:
    snapshot: ValidatedEvidenceSnapshot | None
    issues: tuple[tuple[str, str, str], ...]

    def __post_init__(self) -> None:
        issues = tuple(self.issues)
        if (self.snapshot is None) == (not issues):
            raise ValueError("evidence validation must contain exactly snapshot or issues")
        object.__setattr__(self, "issues", issues)


class BundleArtifactError(Exception):
    """A required bundle path cannot be read safely."""


class JsonDataError(Exception):
    """An artifact is not strict JSON."""


def _error(code: str, message: str, location: str = "bundle") -> dict[str, str]:
    return {"code": code, "message": message, "location": location}


def _is_reparse(info: os.stat_result) -> bool:
    return bool(getattr(info, "st_file_attributes", 0) & _REPARSE_POINT)


class _BundleReader:
    def __init__(
        self,
        bundle: Path,
        operation_hook: Callable[[str], None] | None = None,
    ):
        self._requested = bundle
        self._total = 0
        self._operation_hook = operation_hook
        self._root_fd: int | None = None
        try:
            info = os.lstat(bundle)
            resolved = bundle.resolve(strict=True)
        except OSError as error:
            raise BundleArtifactError("bundle directory is unavailable") from error
        if (
            not stat.S_ISDIR(info.st_mode)
            or stat.S_ISLNK(info.st_mode)
            or _is_reparse(info)
        ):
            raise BundleArtifactError("bundle path must be a real directory")
        self.root = resolved
        self._identity = (
            info.st_dev,
            info.st_ino,
            getattr(info, "st_file_attributes", 0),
        )
        if os.name != "nt" and os.open in os.supports_dir_fd:
            flags = (
                os.O_RDONLY
                | getattr(os, "O_DIRECTORY", 0)
                | getattr(os, "O_NOFOLLOW", 0)
            )
            descriptor = None
            try:
                descriptor = os.open(self.root, flags)
                opened = os.fstat(descriptor)
            except OSError as error:
                if descriptor is not None:
                    os.close(descriptor)
                raise BundleArtifactError("bundle directory is unavailable") from error
            if (
                not stat.S_ISDIR(opened.st_mode)
                or _is_reparse(opened)
                or (opened.st_dev, opened.st_ino) != self._identity[:2]
            ):
                os.close(descriptor)
                raise BundleArtifactError("bundle directory changed during validation")
            self._root_fd = descriptor
        self.verify_root()

    def close(self) -> None:
        if self._root_fd is not None:
            os.close(self._root_fd)
            self._root_fd = None

    def run_hook(self, stage: str) -> None:
        if self._operation_hook is not None:
            self._operation_hook(stage)

    def verify_root(self) -> None:
        try:
            info = os.lstat(self.root)
            resolved = self.root.resolve(strict=True)
        except OSError as error:
            raise BundleArtifactError("bundle directory changed during validation") from error
        identity = (
            info.st_dev,
            info.st_ino,
            getattr(info, "st_file_attributes", 0),
        )
        if (
            resolved != self.root
            or not stat.S_ISDIR(info.st_mode)
            or stat.S_ISLNK(info.st_mode)
            or _is_reparse(info)
            or identity != self._identity
        ):
            raise BundleArtifactError("bundle directory changed during validation")
        if self._root_fd is not None:
            try:
                opened = os.fstat(self._root_fd)
            except OSError as error:
                raise BundleArtifactError("bundle directory changed during validation") from error
            if (
                not stat.S_ISDIR(opened.st_mode)
                or _is_reparse(opened)
                or (opened.st_dev, opened.st_ino) != self._identity[:2]
            ):
                raise BundleArtifactError("bundle directory changed during validation")

    def _open_artifact(self, parts: list[str], flags: int) -> int:
        if self._root_fd is None:
            return os.open(self.root.joinpath(*parts), flags)
        parent_fd = os.dup(self._root_fd)
        try:
            directory_flags = (
                os.O_RDONLY
                | getattr(os, "O_DIRECTORY", 0)
                | getattr(os, "O_NOFOLLOW", 0)
            )
            for component in parts[:-1]:
                next_fd = os.open(component, directory_flags, dir_fd=parent_fd)
                os.close(parent_fd)
                parent_fd = next_fd
                info = os.fstat(parent_fd)
                if not stat.S_ISDIR(info.st_mode) or _is_reparse(info):
                    raise BundleArtifactError("artifact directory is unsafe")
            return os.open(parts[-1], flags, dir_fd=parent_fd)
        finally:
            os.close(parent_fd)

    def read(self, relative_name: str) -> str:
        if relative_name not in _EXPECTED_ARTIFACTS:
            raise BundleArtifactError("artifact name is not part of the finalized bundle")
        self.verify_root()
        parts = relative_name.split("/")
        current = self.root
        for component in parts[:-1]:
            current = current / component
            try:
                info = os.lstat(current)
                resolved = current.resolve(strict=True)
            except OSError as error:
                raise BundleArtifactError("required artifact directory is unavailable") from error
            if (
                not stat.S_ISDIR(info.st_mode)
                or stat.S_ISLNK(info.st_mode)
                or _is_reparse(info)
                or resolved.parent != self.root
            ):
                raise BundleArtifactError("artifact directory is unsafe")

        path = self.root.joinpath(*parts)
        try:
            before = os.lstat(path)
            resolved = path.resolve(strict=True)
        except OSError as error:
            raise BundleArtifactError("required artifact is unavailable") from error
        if (
            not stat.S_ISREG(before.st_mode)
            or stat.S_ISLNK(before.st_mode)
            or _is_reparse(before)
            or resolved.parent != current.resolve(strict=True)
        ):
            raise BundleArtifactError("artifact path is unsafe")
        if before.st_size > _MAX_ARTIFACT_BYTES:
            raise BundleArtifactError("artifact exceeds the validation size limit")
        if self._total + before.st_size > _MAX_BUNDLE_BYTES:
            raise BundleArtifactError("bundle exceeds the validation size limit")

        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
        try:
            descriptor = self._open_artifact(parts, flags)
            try:
                opened = os.fstat(descriptor)
                if (
                    not stat.S_ISREG(opened.st_mode)
                    or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino)
                    or _is_reparse(opened)
                ):
                    raise BundleArtifactError("artifact changed while it was opened")
                chunks: list[bytes] = []
                remaining = _MAX_ARTIFACT_BYTES + 1
                while remaining > 0:
                    chunk = os.read(descriptor, min(64 * 1024, remaining))
                    if not chunk:
                        break
                    chunks.append(chunk)
                    remaining -= len(chunk)
                payload = b"".join(chunks)
                if len(payload) > _MAX_ARTIFACT_BYTES or os.read(descriptor, 1):
                    raise BundleArtifactError("artifact exceeds the validation size limit")
                after = os.fstat(descriptor)
                if (after.st_dev, after.st_ino, after.st_size) != (
                    opened.st_dev,
                    opened.st_ino,
                    opened.st_size,
                ):
                    raise BundleArtifactError("artifact changed while it was read")
            finally:
                os.close(descriptor)
        except BundleArtifactError:
            raise
        except OSError as error:
            raise BundleArtifactError("artifact could not be read safely") from error
        self.run_hook(f"after_read:{relative_name}")
        self.verify_root()
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as error:
            raise BundleArtifactError("artifact is not UTF-8") from error
        self._total += len(payload)
        return text


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise JsonDataError("duplicate JSON object key")
        value[key] = item
    return value


def _reject_constant(_value: str) -> None:
    raise JsonDataError("non-finite JSON number")


def _parse_json(text: str, location: str) -> Any:
    try:
        return json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
    except (json.JSONDecodeError, JsonDataError) as error:
        raise JsonDataError(f"{location} is not strict JSON") from error


def _parse_jsonl(text: str, location: str) -> list[Any]:
    records = []
    for index, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            raise JsonDataError(f"{location} contains a blank JSONL record")
        records.append(_parse_json(line, f"{location}:{index}"))
    return records


def _is_string(value: Any) -> bool:
    return isinstance(value, str)


def _is_nullable_string(value: Any) -> bool:
    return value is None or isinstance(value, str)


def _is_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _retrieval_date(value: Any) -> str | None:
    if not isinstance(value, str) or re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T.+(?:Z|[+-]\d{2}:\d{2})", value
    ) is None:
        return None
    try:
        parsed = datetime.fromisoformat(
            value[:-1] + "+00:00" if value.endswith("Z") else value
        )
        result = parsed.date().isoformat()
        date.fromisoformat(result)
    except ValueError:
        return None
    return result if parsed.tzinfo is not None else None


def _is_string_array(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _check_object(
    value: Any,
    fields: dict[str, Callable[[Any], bool]],
    location: str,
    errors: list[dict[str, str]],
) -> bool:
    if not isinstance(value, dict):
        errors.append(_error("schema", "expected a JSON object", location))
        return False
    expected = set(fields)
    actual = set(value)
    if actual != expected:
        errors.append(_error("schema", "object fields do not match the contract", location))
        return False
    valid = True
    for name, predicate in fields.items():
        if not predicate(value[name]):
            errors.append(_error("schema", f"field {name} has an invalid type or value", location))
            valid = False
    return valid


def _one_of(values: set[str]) -> Callable[[Any], bool]:
    return lambda value: isinstance(value, str) and value in values


_MANIFEST_FIELDS = {
    "schema_version": lambda value: value == "1.0",
    "session_id": lambda value: isinstance(value, str)
    and bool(re.fullmatch(r"[0-9a-f]{32}", value)),
    "capability_tier": _one_of({item.value for item in CapabilityTier}),
    "candidates_filename": _is_string,
    "facts_filename": _is_string,
    "rejected_count": lambda value: _is_integer(value) and value >= 0,
    "manifest_hash": lambda value: isinstance(value, str)
    and bool(re.fullmatch(r"sha256:[0-9a-f]{64}", value)),
}
_CAPABILITY_FIELDS = {
    "tier": _one_of({item.value for item in CapabilityTier}),
    "host_capabilities": _is_string_array,
    "available_capabilities": _is_string_array,
    "missing_capabilities": _is_string_array,
    "degradations": _is_string_array,
    "python_version": _is_string,
    "optional_modules": _is_string_array,
}
_CANDIDATE_FIELDS = {
    "source_id": lambda value: isinstance(value, str) and bool(_SOURCE_ID.fullmatch(value)),
    "url": _is_string,
    "publisher": lambda value: isinstance(value, str) and bool(value.strip()),
    "tier": _one_of({item.value for item in SourceTier}),
    "published_at": _is_nullable_string,
    "retrieved_at": lambda value: _retrieval_date(value) is not None,
    "content_hash": lambda value: isinstance(value, str) and bool(value.strip()),
    "citation_root": lambda value: isinstance(value, str) and bool(value.strip()),
    "summary": _is_string,
}
_FACT_FIELDS = {
    "fact_id": _is_string,
    "field": _is_string,
    "value": lambda _value: True,
    "unit": _is_nullable_string,
    "status": _one_of({item.value for item in EvidenceStatus}),
    "source_ids": _is_string_array,
    "method": _is_string,
    "notes": _is_string,
}
_REJECTION_FIELDS = {"source_id": _is_string, "reason": _is_string}


def _valid_public_document_url(value: str) -> bool:
    return bool(canonicalize_provenance_url(value))


def _validate_shapes(
    manifest: Any,
    capability: Any,
    candidates: list[Any],
    contexts: list[Any],
    facts: list[Any],
    rejections: list[Any],
    *,
    allow_empty: bool = False,
) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    manifest_ok = _check_object(manifest, _MANIFEST_FIELDS, "manifest.json", errors)
    capability_ok = _check_object(capability, _CAPABILITY_FIELDS, "capability.json", errors)
    if manifest_ok and capability_ok and manifest["capability_tier"] != capability["tier"]:
        errors.append(_error("schema", "manifest and capability tiers disagree", "manifest.json"))

    if not candidates and not allow_empty:
        errors.append(_error("schema", "at least one candidate is required", "candidates.jsonl"))
    for index, candidate in enumerate(candidates, 1):
        location = f"candidates.jsonl:{index}"
        if _check_object(candidate, _CANDIDATE_FIELDS, location, errors):
            if not _valid_public_document_url(candidate["url"]):
                errors.append(_error("schema", "candidate URL must be absolute HTTP(S)", location))
            if not canonicalize_provenance_url(candidate["citation_root"]):
                errors.append(
                    _error(
                        "schema",
                        "citation root must be an absolute HTTP(S) provenance URL",
                        location,
                    )
                )
    if not facts and not allow_empty:
        errors.append(_error("schema", "at least one fact is required", "normalized/facts.jsonl"))
    for index, fact in enumerate(facts, 1):
        _check_object(fact, _FACT_FIELDS, f"normalized/facts.jsonl:{index}", errors)
    for index, context in enumerate(contexts, 1):
        if not isinstance(context, dict):
            errors.append(_error("schema", "context record must be an object", f"context.jsonl:{index}"))
    for index, rejection in enumerate(rejections, 1):
        _check_object(rejection, _REJECTION_FIELDS, f"rejections.jsonl:{index}", errors)

    if manifest_ok:
        if manifest["candidates_filename"] != "candidates.jsonl":
            errors.append(_error("artifact", "candidate artifact path is not canonical", "manifest.json"))
        if manifest["facts_filename"] != "normalized/facts.jsonl":
            errors.append(_error("artifact", "fact artifact path is not canonical", "manifest.json"))
        if manifest["rejected_count"] != len(rejections):
            errors.append(_error("schema", "rejected_count does not match records", "manifest.json"))
    errors.extend(_validate_rejection_links(candidates, facts, rejections))
    errors.extend(_validate_fact_provenance(candidates, facts, contexts))
    return errors


def _validate_fact_provenance(
    candidates: list[Any], facts: list[Any], contexts: list[Any]
) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    candidate_by_id = {
        item.get("source_id"): item
        for item in candidates
        if isinstance(item, dict) and isinstance(item.get("source_id"), str)
    }
    fact_by_id = {
        item.get("fact_id"): item
        for item in facts
        if isinstance(item, dict) and isinstance(item.get("fact_id"), str)
    }
    provenance_by_fact: dict[str, list[tuple[int, dict[str, Any]]]] = {}
    for index, context in enumerate(contexts, 1):
        if not isinstance(context, dict) or context.get("kind") != FACT_PROVENANCE_KIND:
            continue
        location = f"context.jsonl:{index}"
        if set(context) != _PROVENANCE_FIELDS:
            errors.append(_error("provenance", "fact provenance shape is not canonical", location))
            continue
        fact_id = context.get("fact_id")
        if not isinstance(fact_id, str):
            errors.append(_error("provenance", "fact provenance fact_id is invalid", location))
            continue
        if type(context.get("year")) is not int:
            errors.append(_error("provenance", "fact provenance year is not canonical", location))
            continue
        try:
            canonical = _canonical_fact_provenance(
                {
                    "fact_id": fact_id,
                    "source_ids": context.get("source_ids"),
                },
                year=context.get("year"),
                extraction_method=context.get("extraction_method"),
                locator=context.get("locator"),
            )
        except (KeyError, TypeError, ValueError, EvidencePathError, EvidencePrivacyError):
            errors.append(_error("provenance", "fact provenance values are invalid", location))
            continue
        if context != canonical:
            errors.append(_error("provenance", "fact provenance is not canonical", location))
            continue
        provenance_by_fact.setdefault(fact_id, []).append((index, context))

    for fact_id, fact in fact_by_id.items():
        records = provenance_by_fact.get(fact_id, [])
        if len(records) != 1:
            errors.append(
                _error(
                    "provenance",
                    "every fact requires exactly one provenance record",
                    "context.jsonl",
                )
            )
            continue
        index, provenance = records[0]
        location = f"context.jsonl:{index}"
        if provenance["source_ids"] != fact.get("source_ids"):
            errors.append(_error("provenance", "fact provenance source_ids do not match", location))
            continue
        for source_id in provenance["source_ids"]:
            candidate = candidate_by_id.get(source_id)
            if (
                not isinstance(candidate, dict)
                or not isinstance(candidate.get("url"), str)
                or not _valid_public_document_url(candidate["url"])
                or not isinstance(candidate.get("citation_root"), str)
                or not canonicalize_provenance_url(candidate["citation_root"])
            ):
                errors.append(
                    _error("provenance", "linked source lacks a validated citation chain", location)
                )
                break
    for fact_id, records in provenance_by_fact.items():
        if fact_id not in fact_by_id:
            for index, _record in records:
                errors.append(
                    _error("provenance", "fact provenance references an unknown fact", f"context.jsonl:{index}")
                )
        elif len(records) > 1:
            errors.append(
                _error("provenance", "fact provenance is duplicated", "context.jsonl")
            )
    return errors


def _validate_rejection_links(
    candidates: list[Any], facts: list[Any], rejections: list[Any]
) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    rejected_ids: set[str] = set()
    for index, rejection in enumerate(rejections, 1):
        if not isinstance(rejection, dict):
            continue
        source_id = rejection.get("source_id")
        if not isinstance(source_id, str):
            continue
        location = f"rejections.jsonl:{index}"
        if not _SOURCE_ID.fullmatch(source_id):
            errors.append(_error("rejections", "rejection source_id is unsafe", location))
            continue
        if source_id in rejected_ids:
            errors.append(_error("rejections", "rejection source_id is duplicated", location))
            continue
        rejected_ids.add(source_id)

    candidate_ids = {
        candidate.get("source_id")
        for candidate in candidates
        if isinstance(candidate, dict) and isinstance(candidate.get("source_id"), str)
    }
    if candidate_ids.intersection(rejected_ids):
        errors.append(
            _error(
                "rejected_source",
                "accepted candidates and rejected sources must be disjoint",
                "rejections.jsonl",
            )
        )
    for index, fact in enumerate(facts, 1):
        if not isinstance(fact, dict) or not isinstance(fact.get("source_ids"), list):
            continue
        if rejected_ids.intersection(item for item in fact["source_ids"] if isinstance(item, str)):
            errors.append(
                _error(
                    "rejected_source",
                    "fact references a rejected source",
                    f"normalized/facts.jsonl:{index}",
                )
            )
    return errors


def _validate_privacy(values: list[tuple[str, Any]]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    facts: list[Any] = []
    candidates: list[Any] = []
    rejections: list[Any] = []
    for location, value in values:
        try:
            _reject_pii_keys(value)
        except EvidencePrivacyError:
            errors.append(_error("privacy", "personal-data key is not allowed", location))
        if location == "normalized/facts.jsonl" and isinstance(value, list):
            facts = value
        elif location == "candidates.jsonl" and isinstance(value, list):
            candidates = value
        elif location == "rejections.jsonl" and isinstance(value, list):
            rejections = value
    for index, candidate in enumerate(candidates, 1):
        if isinstance(candidate, dict):
            _append_identifier_privacy_issue(
                candidate.get("source_id"), f"candidates.jsonl:{index}", errors
            )
    for index, fact in enumerate(facts, 1):
        if isinstance(fact, dict):
            if isinstance(fact.get("field"), str) and _normalize_key(fact["field"]) in _PII_KEYS:
                errors.append(
                    _error("privacy", "personal-data fact field is not allowed", f"normalized/facts.jsonl:{index}")
                )
            _append_identifier_privacy_issue(
                fact.get("fact_id"), f"normalized/facts.jsonl:{index}", errors
            )
            source_ids = fact.get("source_ids")
            if isinstance(source_ids, list):
                for source_id in source_ids:
                    _append_identifier_privacy_issue(
                        source_id, f"normalized/facts.jsonl:{index}", errors
                    )
    for index, rejection in enumerate(rejections, 1):
        if isinstance(rejection, dict):
            _append_identifier_privacy_issue(
                rejection.get("source_id"), f"rejections.jsonl:{index}", errors
            )
    return errors


def _append_identifier_privacy_issue(
    value: Any,
    location: str,
    errors: list[dict[str, str]],
) -> None:
    try:
        _reject_pii_identifier(value)
    except EvidencePrivacyError:
        errors.append(
            _error("privacy", "personal-data-shaped evidence identifier is not allowed", location)
        )
    except EvidencePathError:
        return


def _expected_manifest_hash(
    capability: dict[str, Any],
    rejections: list[dict[str, Any]],
    texts: dict[str, str],
) -> str:
    # Reuse EvidenceStore's canonical payload/hash implementation verbatim.
    store = object.__new__(EvidenceStore)
    store._capability = capability
    store._rejections = {str(index): None for index in range(len(rejections))}
    records = {
        name: texts[name]
        for name in (
            "capability.json",
            "candidates.jsonl",
            "context.jsonl",
            "normalized/facts.jsonl",
            "rejections.jsonl",
        )
    }
    return EvidenceStore._manifest_hash(store, records)


def _to_candidate(value: dict[str, Any]) -> SourceCandidate:
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


def _independent_candidate_count(candidate_values: list[Any]) -> int:
    candidates: list[SourceCandidate] = []
    for value in candidate_values:
        if not isinstance(value, dict) or set(value) != set(_CANDIDATE_FIELDS):
            continue
        if any(not predicate(value[name]) for name, predicate in _CANDIDATE_FIELDS.items()):
            continue
        try:
            candidates.append(_to_candidate(value))
        except (KeyError, TypeError, ValueError):
            continue
    unique, _rejected = deduplicate_candidates(candidates)
    return len(unique)


def _validate_policy(
    candidate_values: list[dict[str, Any]], fact_values: list[dict[str, Any]]
) -> tuple[list[dict[str, str]], int]:
    errors: list[dict[str, str]] = []
    candidates = [_to_candidate(value) for value in candidate_values]
    unique, _rejected = deduplicate_candidates(candidates)
    candidate_ids = {candidate.source_id for candidate in candidates}
    fact_ids: set[str] = set()
    fields: set[str] = set()
    for index, fact in enumerate(fact_values, 1):
        location = f"normalized/facts.jsonl:{index}"
        if fact["fact_id"] in fact_ids:
            errors.append(_error("schema", "duplicate fact_id", location))
        fact_ids.add(fact["fact_id"])
        if fact["field"] in fields:
            errors.append(_error("independent_sources", "field has more than one normalized fact", location))
        fields.add(fact["field"])
        missing = set(fact["source_ids"]).difference(candidate_ids)
        if missing:
            errors.append(_error("schema", "fact references an unknown source", location))
            continue
        if len(set(fact["source_ids"])) != len(fact["source_ids"]):
            errors.append(_error("independent_sources", "fact repeats a source identifier", location))
            continue

        status = EvidenceStatus(fact["status"])
        if status == EvidenceStatus.INFERRED:
            errors.append(
                _error(
                    "unsupported_derivation",
                    "schema version 1 cannot replay derived facts",
                    location,
                )
            )
            continue
        if status not in {
            EvidenceStatus.OFFICIAL,
            EvidenceStatus.CORROBORATED,
            EvidenceStatus.REFERENCE,
        }:
            if fact["value"] is not None:
                errors.append(
                    _error(
                        "unsupported_status",
                        "non-consensus fact status cannot carry an exact value",
                        location,
                    )
                )
            if status in {EvidenceStatus.MASKED, EvidenceStatus.PARTIAL} and (
                not fact["source_ids"] or not fact["method"].strip()
            ):
                errors.append(
                    _error(
                        "unsupported_status",
                        "boundary facts require known sources and a method",
                        location,
                    )
                )
            continue
        claims = [
            FactClaim(
                field=fact["field"],
                value=fact["value"],
                unit=fact["unit"],
                source_id=source_id,
                method=fact["method"],
            )
            for source_id in fact["source_ids"]
        ]
        evaluated = evaluate_claims(fact["field"], claims, candidates)
        if (
            evaluated.status != status
            or evaluated.value != fact["value"]
            or evaluated.unit != fact["unit"]
            or set(evaluated.source_ids) != set(fact["source_ids"])
        ):
            errors.append(
                _error(
                    "independent_sources",
                    "fact is not supported by the shared source-independence policy",
                    location,
                )
            )
        elif evaluated.method != fact["method"]:
            errors.append(
                _error(
                    "method",
                    "fact method does not match the shared source policy",
                    location,
                )
            )
    source_ids = [candidate.source_id for candidate in candidates]
    if len(source_ids) != len(set(source_ids)):
        errors.append(_error("schema", "duplicate candidate source_id", "candidates.jsonl"))
    return errors, len(unique)


def _validate_bundle_with_payload(
    bundle: Path,
    *,
    _operation_hook: Callable[[str], None] | None = None,
    _allow_empty: bool = False,
) -> tuple[dict[str, Any], dict[str, Any] | None, _BundleReader | None]:
    summary: dict[str, Any] = {
        "valid": False,
        "candidate_count": 0,
        "fact_count": 0,
        "independent_source_count": 0,
        "errors": [],
    }
    reader: _BundleReader | None = None
    try:
        reader = _BundleReader(bundle, _operation_hook)
        texts = {name: reader.read(name) for name in _EXPECTED_ARTIFACTS}
    except BundleArtifactError as error:
        if reader is not None:
            reader.close()
        summary["errors"].append(_error("artifact", str(error)))
        return summary, None, None

    try:
        manifest = _parse_json(texts["manifest.json"], "manifest.json")
        capability = _parse_json(texts["capability.json"], "capability.json")
        candidates = _parse_jsonl(texts["candidates.jsonl"], "candidates.jsonl")
        contexts = _parse_jsonl(texts["context.jsonl"], "context.jsonl")
        facts = _parse_jsonl(texts["normalized/facts.jsonl"], "normalized/facts.jsonl")
        rejections = _parse_jsonl(texts["rejections.jsonl"], "rejections.jsonl")
    except JsonDataError as error:
        summary["errors"].append(_error("schema", str(error)))
        return summary, None, reader

    summary["candidate_count"] = len(candidates)
    summary["fact_count"] = len(facts)
    summary["independent_source_count"] = _independent_candidate_count(candidates)
    errors = _validate_shapes(
        manifest,
        capability,
        candidates,
        contexts,
        facts,
        rejections,
        allow_empty=_allow_empty,
    )
    errors.extend(
        _validate_privacy(
            [
                ("manifest.json", manifest),
                ("capability.json", capability),
                ("candidates.jsonl", candidates),
                ("context.jsonl", contexts),
                ("normalized/facts.jsonl", facts),
                ("rejections.jsonl", rejections),
            ]
        )
    )

    if isinstance(manifest, dict) and isinstance(capability, dict) and all(
        isinstance(item, dict) for item in rejections
    ):
        try:
            expected_hash = _expected_manifest_hash(capability, rejections, texts)
        except (TypeError, ValueError):
            errors.append(_error("schema", "bundle content is not canonically serializable"))
        else:
            if manifest.get("manifest_hash") != expected_hash:
                errors.append(_error("manifest_hash", "manifest hash does not match bundle content", "manifest.json"))

    shape_errors = any(item["code"] == "schema" for item in errors)
    if not shape_errors and all(isinstance(item, dict) for item in candidates + facts):
        policy_errors, independent_count = _validate_policy(candidates, facts)
        errors.extend(policy_errors)
        summary["independent_source_count"] = independent_count

    summary["errors"] = errors
    summary["valid"] = not errors
    payload = {
        "manifest": manifest,
        "capability": capability,
        "candidates": candidates,
        "contexts": contexts,
        "facts": facts,
        "rejections": rejections,
    }
    return summary, payload, reader


def validate_bundle(bundle: Path) -> dict[str, Any]:
    """Return the historical machine-readable validation summary."""

    summary, _payload, reader = _validate_bundle_with_payload(bundle)
    try:
        return summary
    finally:
        if reader is not None:
            reader.close()


def validate_bundle_snapshot(
    bundle: Path,
    *,
    _operation_hook: Callable[[str], None] | None = None,
    _allow_empty: bool = False,
) -> EvidenceValidationResult:
    """Return a factory-only snapshot only when the exact read bundle is valid."""

    summary, payload, reader = _validate_bundle_with_payload(
        bundle,
        _operation_hook=_operation_hook,
        _allow_empty=_allow_empty,
    )
    if not summary["valid"] or payload is None:
        issues = tuple(
            (
                str(item.get("code", "invalid")),
                str(item.get("message", "bundle validation failed")),
                str(item.get("location", "bundle")),
            )
            for item in summary["errors"]
        )
        if not issues:
            issues = (("invalid", "bundle validation failed", "bundle"),)
        if reader is not None:
            reader.close()
        return EvidenceValidationResult(None, issues)
    try:
        manifest_value = payload["manifest"]
        capability_value = payload["capability"]
        candidates = payload["candidates"]
        contexts = payload["contexts"]
        facts = payload["facts"]
        rejections = payload["rejections"]
        manifest = EvidenceManifest(
            schema_version=manifest_value["schema_version"],
            session_id=manifest_value["session_id"],
            capability_tier=CapabilityTier(manifest_value["capability_tier"]),
            candidates_filename=manifest_value["candidates_filename"],
            facts_filename=manifest_value["facts_filename"],
            rejected_count=manifest_value["rejected_count"],
            manifest_hash=manifest_value["manifest_hash"],
        )
        capability = CapabilityReport(
            tier=CapabilityTier(capability_value["tier"]),
            host_capabilities=tuple(capability_value["host_capabilities"]),
            available_capabilities=tuple(capability_value["available_capabilities"]),
            missing_capabilities=tuple(capability_value["missing_capabilities"]),
            degradations=tuple(capability_value["degradations"]),
            python_version=capability_value["python_version"],
            optional_modules=tuple(capability_value["optional_modules"]),
        )
        retrieval_dates = tuple(
            sorted({_retrieval_date(item["retrieved_at"]) for item in candidates})
        )
        if (
            (not retrieval_dates and not _allow_empty)
            or any(item is None for item in retrieval_dates)
        ):
            raise ValueError("validated candidates lack retrieval dates")
        if reader is None:
            raise BundleArtifactError("bundle directory identity is unavailable")
        reader.run_hook("before_snapshot")
        reader.verify_root()
        snapshot = ValidatedEvidenceSnapshot._create(
            manifest,
            capability,
            tuple(item for item in retrieval_dates if item is not None),
            tuple(FrozenJsonRecord._from_mapping(item) for item in facts),
            tuple(FrozenJsonRecord._from_mapping(item) for item in rejections),
            candidates=tuple(
                FrozenJsonRecord._from_mapping(item) for item in candidates
            ),
            contexts=tuple(
                FrozenJsonRecord._from_mapping(item) for item in contexts
            ),
        )
    except BundleArtifactError as error:
        return EvidenceValidationResult(
            None,
            (("artifact", str(error), "bundle"),),
        )
    except (KeyError, TypeError, ValueError):
        return EvidenceValidationResult(
            None,
            (("snapshot", "validated bundle could not form a snapshot", "bundle"),),
        )
    finally:
        if reader is not None:
            reader.close()
    return EvidenceValidationResult(snapshot, ())


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path, help="finalized evidence-bundle directory")
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        summary = validate_bundle(arguments.bundle)
    except Exception:
        summary = {
            "valid": False,
            "candidate_count": 0,
            "fact_count": 0,
            "independent_source_count": 0,
            "errors": [_error("internal", "unexpected validator failure")],
        }
        print(json.dumps(summary, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 1
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if summary["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
