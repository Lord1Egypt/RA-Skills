"""Safe, deterministic persistence for one local evidence bundle.

Sessions are generated below a caller-selected local root. Their manifest hash
is SHA-256 of canonical UTF-8 JSON containing schema version, capability
snapshot, rejected count, and exact persisted non-manifest records; the random
session ID and manifest hash itself are excluded.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import uuid4

if __package__ == "scripts":
    from .adapters import (
        PublicLocatorError,
        PublicLocatorPathError,
        PublicLocatorPrivacyError,
        validate_public_locator,
    )
    from .contracts import (
        CapabilityReport,
        EvidenceFact,
        EvidenceManifest,
        SourceCandidate,
    )
else:  # ``sys.path`` rooted at ``scripts`` package compatibility.
    from adapters import (  # type: ignore
        PublicLocatorError,
        PublicLocatorPathError,
        PublicLocatorPrivacyError,
        validate_public_locator,
    )
    from contracts import (  # type: ignore
        CapabilityReport,
        EvidenceFact,
        EvidenceManifest,
        SourceCandidate,
    )


class EvidenceError(Exception):
    """Base class for evidence-bundle failures."""


class EvidencePathError(EvidenceError):
    """Raised when a workspace or derived path is unsafe."""


class EvidencePrivacyError(EvidenceError):
    """Raised when evidence data contains a forbidden personal-data key."""


class EvidenceStateError(EvidenceError):
    """Raised when an operation violates the bundle lifecycle."""


_SCHEMA_VERSION = "1.0"
_SOURCE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_PHONE_IDENTIFIER = re.compile(r"1[3-9][0-9]{9}")
_IDENTITY_IDENTIFIER = re.compile(r"[0-9]{17}[0-9Xx]")
_REPARSE_POINT = 0x0400
FACT_PROVENANCE_KIND = "fact-provenance"
FACT_EXTRACTION_METHODS = (
    "html-table",
    "xlsx-worksheet",
    "xls-worksheet",
    "pdf-text-table",
    "pdfplumber-text",
    "pypdf-text",
    "host-ocr-rows",
    "host-public-text",
    "qr",
    "manual-structured",
)
_FACT_EXTRACTION_METHODS = frozenset(FACT_EXTRACTION_METHODS)
_PII_KEYS = frozenset(
    {
        "name", "student_name", "phone", "mobile", "id_card", "address",
        "姓名", "学生姓名", "手机号", "身份证", "身份证号", "地址",
        "电话", "联系电话", "手机", "联系手机", "住址", "家庭住址",
    }
)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _normalize_key(key: str) -> str:
    return re.sub(r"[\s-]+", "_", key.strip().lower())


def _reject_pii_keys(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if isinstance(key, str) and _normalize_key(key) in _PII_KEYS:
                raise EvidencePrivacyError("Personal-data keys are not allowed in evidence data")
            _reject_pii_keys(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _reject_pii_keys(item)


def _snapshot(value: Any) -> Any:
    """Validate and deep-copy JSON-safe data at every ingestion boundary."""

    _reject_pii_keys(value)
    return json.loads(_canonical_json(value))


def _reject_pii_identifier(value: Any) -> None:
    """Reject personal-number shapes in semantic evidence identifiers.

    Session UUIDs and manifest hashes do not use this scanner; their exact
    machine grammars are validated by their own contracts.
    """

    if not isinstance(value, str):
        raise EvidencePathError("Evidence identifier is unsafe")
    compact = re.sub(r"[._:-]+", "", value)
    if _PHONE_IDENTIFIER.search(compact) or _IDENTITY_IDENTIFIER.search(compact):
        raise EvidencePrivacyError("Personal-data-shaped evidence identifiers are not allowed")


def _normalize_provenance_year(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("Fact provenance year must be a mathematical integer")
    if not (float(value).is_integer() and 1 <= value <= 9999):
        raise ValueError("Fact provenance year must be a mathematical year")
    return int(value)


def _validate_extraction_method(value: Any) -> str:
    if not isinstance(value, str) or value not in _FACT_EXTRACTION_METHODS:
        raise ValueError("Fact provenance extraction method is unknown")
    return value


def _validate_locator(value: Any) -> str:
    try:
        return validate_public_locator(value)
    except PublicLocatorPrivacyError:
        raise EvidencePrivacyError(
            "Personal-data-shaped provenance locator is not allowed"
        ) from None
    except PublicLocatorPathError:
        raise EvidencePathError(
            "Fact provenance locator must not contain a local path"
        ) from None
    except PublicLocatorError:
        raise ValueError("Fact provenance locator is unsafe") from None


def _canonical_fact_provenance(
    fact: Mapping[str, Any], *, year: Any, extraction_method: Any, locator: Any
) -> dict[str, Any]:
    return {
        "kind": FACT_PROVENANCE_KIND,
        "fact_id": fact["fact_id"],
        "source_ids": list(fact["source_ids"]),
        "year": _normalize_provenance_year(year),
        "extraction_method": _validate_extraction_method(extraction_method),
        "locator": _validate_locator(locator),
    }


def _is_below(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


@dataclass(frozen=True)
class _DirectoryIdentity:
    """Resolved directory name plus identity used to notice swaps/reparse points."""

    path: Path
    device: int
    inode: int
    file_attributes: int

    @classmethod
    def capture(cls, path: Path) -> "_DirectoryIdentity":
        try:
            info = os.lstat(path)
            resolved = path.resolve(strict=True)
        except OSError as error:
            raise EvidencePathError("Evidence directory could not be verified") from error
        if not stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode):
            raise EvidencePathError("Evidence directory is not a real directory")
        attributes = getattr(info, "st_file_attributes", 0)
        if os.name == "nt" and attributes & _REPARSE_POINT:
            raise EvidencePathError("Evidence directory cannot be a reparse point")
        return cls(resolved, info.st_dev, info.st_ino, attributes)

    def verify(self) -> None:
        try:
            resolved = self.path.resolve(strict=True)
            info = os.lstat(self.path)
        except OSError as error:
            raise EvidencePathError("Evidence directory changed during operation") from error
        if resolved != self.path or not stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode):
            raise EvidencePathError("Evidence directory changed during operation")
        attributes = getattr(info, "st_file_attributes", 0)
        if os.name == "nt" and attributes & _REPARSE_POINT:
            raise EvidencePathError("Evidence directory changed during operation")
        if (info.st_dev, info.st_ino, attributes) != (self.device, self.inode, self.file_attributes):
            raise EvidencePathError("Evidence directory changed during operation")


@dataclass(frozen=True)
class _EntryIdentity:
    """Identity of a just-created file or directory used for exact cleanup."""

    device: int
    inode: int
    file_attributes: int
    mode: int

    @classmethod
    def capture(cls, path: Path) -> "_EntryIdentity":
        try:
            info = os.lstat(path)
        except OSError as error:
            raise EvidencePathError("Evidence artifact changed during operation") from error
        return cls.from_info(info)

    @classmethod
    def capture_at(cls, directory_fd: int, name: str) -> "_EntryIdentity":
        try:
            info = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        except OSError as error:
            raise EvidencePathError("Evidence artifact changed during operation") from error
        return cls.from_info(info)

    @classmethod
    def from_info(cls, info: os.stat_result) -> "_EntryIdentity":
        return cls(info.st_dev, info.st_ino, getattr(info, "st_file_attributes", 0), info.st_mode)

    def matches(self, path: Path, *, directory: bool) -> bool:
        try:
            info = os.lstat(path)
        except OSError:
            return False
        return self.matches_info(info, directory=directory)

    def matches_info(self, info: os.stat_result, *, directory: bool) -> bool:
        expected_type = stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode)
        return (
            expected_type
            and not stat.S_ISLNK(info.st_mode)
            and (info.st_dev, info.st_ino, getattr(info, "st_file_attributes", 0))
            == (self.device, self.inode, self.file_attributes)
        )


class EvidenceStore:
    """Mutable evidence collection which becomes immutable once finalized."""

    def __init__(
        self,
        root_dir: _DirectoryIdentity,
        session_dir: _DirectoryIdentity,
        raw_dir: _DirectoryIdentity,
        normalized_dir: _DirectoryIdentity,
        capability: dict[str, Any],
        capability_tier: Any,
    ):
        self._root_dir = root_dir
        self._session_dir = session_dir
        self._raw_dir = raw_dir
        self._normalized_dir = normalized_dir
        self.session_path = session_dir.path
        self._capability = capability
        self._capability_tier = capability_tier
        self._candidates: dict[str, dict[str, Any]] = {}
        self._facts: dict[str, dict[str, Any]] = {}
        self._rejections: dict[str, str] = {}
        self._contexts: list[dict[str, Any]] = []
        self._manifest: EvidenceManifest | None = None
        # Narrow test seam: it runs only between real filesystem operations.
        self._operation_hook: Callable[[str], None] | None = None

    @classmethod
    def create(cls, root: str | os.PathLike[str], capability_report: CapabilityReport) -> "EvidenceStore":
        if not isinstance(capability_report, CapabilityReport):
            raise TypeError("capability_report must be a CapabilityReport")
        try:
            requested_root = Path(root)
        except TypeError as error:
            raise EvidencePathError("Evidence workspace must be a local path") from error
        if not requested_root.is_absolute() or not requested_root.is_dir():
            raise EvidencePathError("Evidence workspace must be an existing absolute directory")
        root_dir = _DirectoryIdentity.capture(requested_root)
        evidence_dir = cls._create_or_verify_child(root_dir, "evidence")
        for _ in range(8):
            try:
                session_dir = cls._create_child(evidence_dir, uuid4().hex)
            except FileExistsError:
                continue
            raw_dir = cls._create_child(session_dir, "raw")
            normalized_dir = cls._create_child(session_dir, "normalized")
            capability = _snapshot(capability_report.to_dict())
            return cls(root_dir, session_dir, raw_dir, normalized_dir, capability, capability_report.tier)
        raise EvidencePathError("Could not allocate a unique evidence session")

    @staticmethod
    def _create_or_verify_child(parent: _DirectoryIdentity, name: str) -> _DirectoryIdentity:
        try:
            return EvidenceStore._create_child(parent, name)
        except FileExistsError:
            parent.verify()
            child = _DirectoryIdentity.capture(parent.path / name)
            if not _is_below(child.path, parent.path):
                raise EvidencePathError("Evidence directory escaped its parent")
            return child

    @staticmethod
    def _create_child(parent: _DirectoryIdentity, name: str) -> _DirectoryIdentity:
        parent.verify()
        child = parent.path / name
        try:
            if os.name != "nt" and os.open in os.supports_dir_fd:
                flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
                directory_fd = os.open(parent.path, flags)
                try:
                    parent.verify()
                    os.mkdir(name, dir_fd=directory_fd)
                finally:
                    os.close(directory_fd)
            else:
                os.mkdir(child)
        except FileExistsError:
            raise
        except OSError as error:
            raise EvidencePathError("Evidence directory could not be created") from error
        parent.verify()
        identity = _DirectoryIdentity.capture(child)
        if not _is_below(identity.path, parent.path):
            raise EvidencePathError("Evidence directory escaped its parent")
        return identity

    def add_candidate(self, candidate: SourceCandidate) -> None:
        self._require_open()
        if not isinstance(candidate, SourceCandidate):
            raise TypeError("candidate must be a SourceCandidate")
        snapshot = _snapshot(candidate.to_dict())
        source_id = snapshot["source_id"]
        self._validate_source_id(source_id)
        if source_id in self._candidates or source_id in self._rejections:
            raise EvidenceStateError("Duplicate evidence source id")
        self._candidates[source_id] = snapshot

    def add_fact(
        self,
        fact: EvidenceFact,
        *,
        year: int | float,
        extraction_method: str,
        locator: str,
    ) -> None:
        self._require_open()
        if not isinstance(fact, EvidenceFact):
            raise TypeError("fact must be an EvidenceFact")
        snapshot = _snapshot(fact.to_dict())
        if _normalize_key(snapshot["field"]) in _PII_KEYS:
            raise EvidencePrivacyError("Personal-data keys are not allowed in evidence data")
        fact_id = snapshot["fact_id"]
        _reject_pii_identifier(fact_id)
        for source_id in snapshot["source_ids"]:
            _reject_pii_identifier(source_id)
        if fact_id in self._facts:
            raise EvidenceStateError("Duplicate evidence fact id")
        if set(snapshot["source_ids"]).difference(self._candidates):
            raise EvidenceStateError("Evidence fact references an unregistered source")
        snapshot["source_ids"] = sorted(snapshot["source_ids"])
        provenance = _snapshot(
            _canonical_fact_provenance(
                snapshot,
                year=year,
                extraction_method=extraction_method,
                locator=locator,
            )
        )
        self._facts[fact_id] = snapshot
        self._contexts.append(provenance)

    def reject_candidate(self, candidate: SourceCandidate | str, reason: str) -> None:
        self._require_open()
        if isinstance(candidate, SourceCandidate):
            source_id = _snapshot(candidate.to_dict())["source_id"]
        elif isinstance(candidate, str):
            source_id = _snapshot(candidate)
        else:
            raise TypeError("candidate must be a SourceCandidate or source id")
        reason_snapshot = _snapshot(reason)
        self._validate_source_id(source_id)
        if not isinstance(reason_snapshot, str):
            raise TypeError("rejection reason must be a string")
        if source_id in self._candidates or source_id in self._rejections:
            raise EvidenceStateError("Duplicate evidence source id")
        self._rejections[source_id] = reason_snapshot

    def add_context(self, context: Mapping[str, Any]) -> None:
        self._require_open()
        if not isinstance(context, Mapping):
            raise TypeError("context must be a mapping")
        snapshot = _snapshot(context)
        if snapshot.get("kind") == FACT_PROVENANCE_KIND:
            raise EvidenceStateError("Fact provenance can only be created with add_fact")
        self._contexts.append(snapshot)

    def raw_path_for(self, source_id: str) -> Path:
        self._require_open()
        self._validate_source_id(source_id)
        if source_id not in self._candidates:
            raise EvidencePathError("Raw storage requires a registered source id")
        self._verify_layout()
        self._raw_dir.verify()
        raw_fd = self._open_directory_fd(self._raw_dir)
        created = False
        source_identity: _EntryIdentity | None = None
        source_path = self._raw_dir.path / source_id
        try:
            self._run_hook("before-raw-mkdir")
            self._verify_layout()
            self._raw_dir.verify()
            self._run_hook("after-raw-precheck-before-mkdir")
            try:
                if raw_fd is not None:
                    os.mkdir(source_id, dir_fd=raw_fd)
                else:
                    os.mkdir(source_path)
                created = True
            except FileExistsError:
                source_dir = _DirectoryIdentity.capture(source_path)
                if not _is_below(source_dir.path, self._raw_dir.path):
                    raise EvidencePathError("Raw storage path escaped the evidence session")
                return source_dir.path
            except OSError as error:
                raise EvidencePathError("Raw storage path could not be created") from error
            source_identity = (
                _EntryIdentity.capture_at(raw_fd, source_id)
                if raw_fd is not None
                else _EntryIdentity.capture(source_path)
            )
            self._run_hook("after-raw-mkdir-before-postcheck")
            self._verify_layout()
            self._raw_dir.verify()
            source_dir = _DirectoryIdentity.capture(source_path)
            if not _is_below(source_dir.path, self._raw_dir.path):
                raise EvidencePathError("Raw storage path escaped the evidence session")
            created = False
            return source_dir.path
        finally:
            if created:
                self._remove_created_raw_directory(source_id, source_identity, raw_fd)
            if raw_fd is not None:
                os.close(raw_fd)

    def finalize(self) -> EvidenceManifest:
        if self._manifest is not None:
            return self._manifest
        self._validate_persisted_identifiers()
        self._verify_layout()
        records = self._artifact_records()
        manifest = EvidenceManifest(
            schema_version=_SCHEMA_VERSION,
            session_id=self._session_dir.path.name,
            capability_tier=self._capability_tier,
            candidates_filename="candidates.jsonl",
            facts_filename="normalized/facts.jsonl",
            rejected_count=len(self._rejections),
            manifest_hash=self._manifest_hash(records),
        )
        for relative_name, content in records.items():
            self._atomic_write(relative_name, content)
        self._atomic_write("manifest.json", _canonical_json(manifest.to_dict()) + "\n")
        self._manifest = manifest
        return manifest

    def _artifact_records(self) -> dict[str, str]:
        candidates = [self._candidates[source_id] for source_id in sorted(self._candidates)]
        facts = []
        for fact_id in sorted(self._facts):
            fact = dict(self._facts[fact_id])
            fact["source_ids"] = sorted(fact["source_ids"])
            facts.append(fact)
        rejections = [
            {"source_id": source_id, "reason": self._rejections[source_id]}
            for source_id in sorted(self._rejections)
        ]
        return {
            "capability.json": _canonical_json(self._capability) + "\n",
            "candidates.jsonl": self._jsonl(candidates),
            "context.jsonl": self._jsonl(sorted(self._contexts, key=_canonical_json)),
            "normalized/facts.jsonl": self._jsonl(facts),
            "rejections.jsonl": self._jsonl(rejections),
        }

    def _validate_persisted_identifiers(self) -> None:
        for candidate in self._candidates.values():
            _reject_pii_identifier(candidate.get("source_id"))
        for fact in self._facts.values():
            _reject_pii_identifier(fact.get("fact_id"))
            source_ids = fact.get("source_ids", ())
            for source_id in source_ids:
                _reject_pii_identifier(source_id)
        for source_id in self._rejections:
            _reject_pii_identifier(source_id)
        provenance_by_fact: dict[str, list[dict[str, Any]]] = {}
        for context in self._contexts:
            if context.get("kind") != FACT_PROVENANCE_KIND:
                continue
            fact_id = context.get("fact_id")
            if not isinstance(fact_id, str):
                raise EvidenceStateError("Fact provenance is malformed")
            provenance_by_fact.setdefault(fact_id, []).append(context)
        if set(provenance_by_fact) != set(self._facts) or any(
            len(records) != 1 for records in provenance_by_fact.values()
        ):
            raise EvidenceStateError("Every fact requires exactly one provenance record")
        for fact_id, fact in self._facts.items():
            record = provenance_by_fact[fact_id][0]
            expected = _canonical_fact_provenance(
                fact,
                year=record.get("year"),
                extraction_method=record.get("extraction_method"),
                locator=record.get("locator"),
            )
            if record != expected:
                raise EvidenceStateError("Fact provenance does not match its fact")

    @staticmethod
    def _jsonl(records: list[dict[str, Any]]) -> str:
        return "".join(_canonical_json(record) + "\n" for record in records)

    def _manifest_hash(self, records: Mapping[str, str]) -> str:
        payload = {
            "schema_version": _SCHEMA_VERSION,
            "capability": self._capability,
            "rejected_count": len(self._rejections),
            "files": {name: records[name] for name in sorted(records)},
        }
        return "sha256:" + hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()

    @staticmethod
    def _open_directory_fd(directory: _DirectoryIdentity) -> int | None:
        if os.name == "nt" or os.open not in os.supports_dir_fd:
            return None
        flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
        try:
            descriptor = os.open(directory.path, flags)
            info = os.fstat(descriptor)
        except OSError as error:
            raise EvidencePathError("Evidence directory changed during operation") from error
        if (info.st_dev, info.st_ino) != (directory.device, directory.inode):
            os.close(descriptor)
            raise EvidencePathError("Evidence directory changed during operation")
        return descriptor

    def _remove_created_raw_directory(
        self,
        source_id: str,
        identity: _EntryIdentity | None,
        raw_fd: int | None,
    ) -> None:
        if raw_fd is not None:
            if identity is not None:
                self._remove_entry_by_identity_fd(raw_fd, identity, directory=True)
            return
        if identity is not None:
            self._remove_exact_entry(self._raw_dir.path / source_id, identity, directory=True)

    @staticmethod
    def _remove_entry_by_identity_fd(
        directory_fd: int,
        identity: _EntryIdentity,
        *,
        directory: bool,
    ) -> None:
        """Delete only the entry whose lstat identity matches a created object."""

        try:
            names = os.listdir(directory_fd)
        except OSError:
            return
        for name in names:
            try:
                info = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
            except OSError:
                continue
            if not identity.matches_info(info, directory=directory):
                continue
            try:
                # Re-stat immediately before removal so a reused name survives.
                current = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
                if not identity.matches_info(current, directory=directory):
                    return
                if directory:
                    os.rmdir(name, dir_fd=directory_fd)
                else:
                    os.unlink(name, dir_fd=directory_fd)
            except OSError:
                pass
            return

    def _remove_exact_entry(self, preferred: Path, identity: _EntryIdentity, *, directory: bool) -> None:
        candidates = [preferred]
        if os.name == "nt":
            found = self._find_identity_below_root(identity, directory=directory)
            if found is not None:
                candidates.append(found)
        for candidate in candidates:
            if not identity.matches(candidate, directory=directory):
                continue
            try:
                if directory:
                    candidate.rmdir()
                else:
                    candidate.unlink()
            except OSError:
                pass
            return

    def _find_identity_below_root(self, identity: _EntryIdentity, *, directory: bool) -> Path | None:
        """Locate only an exact known object below the unchanged workspace root."""

        try:
            self._root_dir.verify()
        except EvidencePathError:
            return None
        pending = [self._root_dir.path]
        while pending:
            current = pending.pop()
            try:
                with os.scandir(current) as entries:
                    for entry in entries:
                        path = Path(entry.path)
                        if identity.matches(path, directory=directory):
                            return path
                        try:
                            info = entry.stat(follow_symlinks=False)
                        except OSError:
                            continue
                        attributes = getattr(info, "st_file_attributes", 0)
                        if (
                            stat.S_ISDIR(info.st_mode)
                            and not stat.S_ISLNK(info.st_mode)
                            and not (os.name == "nt" and attributes & _REPARSE_POINT)
                        ):
                            pending.append(path)
            except OSError:
                continue
        return None

    def _atomic_write(self, relative_name: str, content: str) -> None:
        parent, destination_name = self._artifact_parent(relative_name)
        self._verify_layout()
        parent.verify()
        self._run_hook(f"before-open:{relative_name}")
        self._verify_layout()
        parent.verify()
        descriptor, temporary_name, directory_fd = self._open_temporary(parent, destination_name)
        temporary_path = parent.path / temporary_name
        temporary_identity: _EntryIdentity | None = None
        replaced = False
        published = False
        try:
            temporary_identity = _EntryIdentity.capture(temporary_path)
            self._verify_temporary(temporary_path, parent, descriptor)
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
                descriptor = -1
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            self._verify_layout()
            parent.verify()
            self._verify_temporary(temporary_path, parent)
            self._run_hook(f"before-replace:{relative_name}")
            self._verify_layout()
            parent.verify()
            self._verify_temporary(temporary_path, parent)
            self._run_hook(f"after-final-precheck-before-replace:{relative_name}")
            try:
                if directory_fd is not None:
                    os.replace(temporary_name, destination_name, src_dir_fd=directory_fd, dst_dir_fd=directory_fd)
                else:
                    os.replace(temporary_path, parent.path / destination_name)
            except OSError as error:
                raise EvidencePathError("Evidence artifact could not be published safely") from error
            replaced = True
            self._run_hook(f"after-replace-before-postcheck:{relative_name}")
            self._verify_layout()
            parent.verify()
            self._verify_regular_file(parent.path / destination_name, parent)
            if not temporary_identity.matches(parent.path / destination_name, directory=False):
                raise EvidencePathError("Evidence artifact changed during operation")
            published = True
        finally:
            if descriptor >= 0:
                os.close(descriptor)
            if directory_fd is not None:
                if not published:
                    if temporary_identity is not None:
                        self._remove_entry_by_identity_fd(
                            directory_fd,
                            temporary_identity,
                            directory=False,
                        )
                os.close(directory_fd)
            elif not published:
                if temporary_identity is not None:
                    self._remove_exact_entry(
                        parent.path / (destination_name if replaced else temporary_name),
                        temporary_identity,
                        directory=False,
                    )
                else:
                    self._remove_temporary_if_still_safe(temporary_path, parent)

    def _artifact_parent(self, relative_name: str) -> tuple[_DirectoryIdentity, str]:
        if relative_name.startswith("normalized/"):
            return self._normalized_dir, relative_name.removeprefix("normalized/")
        if "/" in relative_name or Path(relative_name).is_absolute():
            raise EvidencePathError("Evidence artifact path must be relative")
        return self._session_dir, relative_name

    @staticmethod
    def _open_temporary(parent: _DirectoryIdentity, destination_name: str) -> tuple[int, str, int | None]:
        temporary_name = f".{destination_name}.{uuid4().hex}.tmp"
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        if os.name != "nt" and os.open in os.supports_dir_fd:
            directory_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
            directory_fd = os.open(parent.path, directory_flags)
            try:
                info = os.fstat(directory_fd)
                if (info.st_dev, info.st_ino) != (parent.device, parent.inode):
                    raise EvidencePathError("Evidence directory changed during operation")
                return os.open(temporary_name, flags, 0o600, dir_fd=directory_fd), temporary_name, directory_fd
            except Exception:
                os.close(directory_fd)
                raise
        return os.open(parent.path / temporary_name, flags, 0o600), temporary_name, None

    @staticmethod
    def _verify_temporary(path: Path, parent: _DirectoryIdentity, descriptor: int | None = None) -> None:
        parent.verify()
        EvidenceStore._verify_regular_file(path, parent)
        if descriptor is not None:
            info = os.fstat(descriptor)
            disk_info = os.stat(path)
            if (info.st_dev, info.st_ino) != (disk_info.st_dev, disk_info.st_ino):
                raise EvidencePathError("Evidence temporary file changed during operation")

    @staticmethod
    def _verify_regular_file(path: Path, parent: _DirectoryIdentity) -> None:
        try:
            resolved = path.resolve(strict=True)
            info = os.lstat(path)
        except OSError as error:
            raise EvidencePathError("Evidence artifact changed during operation") from error
        if resolved.parent != parent.path or not stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode):
            raise EvidencePathError("Evidence artifact changed during operation")
        attributes = getattr(info, "st_file_attributes", 0)
        if os.name == "nt" and attributes & _REPARSE_POINT:
            raise EvidencePathError("Evidence artifact changed during operation")

    @staticmethod
    def _remove_temporary_if_still_safe(path: Path, parent: _DirectoryIdentity) -> None:
        try:
            parent.verify()
            EvidenceStore._verify_regular_file(path, parent)
            path.unlink()
        except (EvidencePathError, FileNotFoundError, OSError):
            pass

    def _verify_layout(self) -> None:
        self._root_dir.verify()
        self._session_dir.verify()
        self._raw_dir.verify()
        self._normalized_dir.verify()
        if not _is_below(self._session_dir.path, self._root_dir.path):
            raise EvidencePathError("Evidence session escaped the workspace")
        if not _is_below(self._raw_dir.path, self._session_dir.path):
            raise EvidencePathError("Raw storage escaped the evidence session")
        if not _is_below(self._normalized_dir.path, self._session_dir.path):
            raise EvidencePathError("Normalized storage escaped the evidence session")

    def _run_hook(self, stage: str) -> None:
        if self._operation_hook is not None:
            self._operation_hook(stage)

    def _require_open(self) -> None:
        if self._manifest is not None:
            raise EvidenceStateError("Evidence bundle is already finalized")

    @staticmethod
    def _validate_source_id(source_id: str) -> None:
        if not isinstance(source_id, str) or not _SOURCE_ID.fullmatch(source_id):
            raise EvidencePathError("Evidence source id is unsafe")
        _reject_pii_identifier(source_id)


__all__ = ["EvidenceError", "EvidencePathError", "EvidencePrivacyError", "EvidenceStateError", "EvidenceStore"]
