# -*- coding: utf-8 -*-
"""Bounded privacy and publication-content scanner.

The public report helpers remain intentionally small. Repository scanning is
separate: it consumes Git's tracked inventory, skips declared binary
extensions, and emits locations and rule identifiers without matched values.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Callable, Optional, Sequence


_FOREIGN_CURRENCY = r"(?:港币|澳门元)"
PRICE_RES = (
    re.compile(r"\d+(?:\.\d+)?\s*[元折块]"),
    re.compile(r"\d+(?:\.\d+)?\s*[万千](?!\s*" + _FOREIGN_CURRENCY + r")"),
    re.compile(r"[￥¥]\s*\d"),
    re.compile(r"[一二三四五六七八九十百千万两]+\s*[折元]"),
    re.compile(r"[一二三四五六七八九十百千万两]+\s*万(?!\s*" + _FOREIGN_CURRENCY + r")"),
    re.compile(r"(?:仅需|优惠价|立减|原价)\s*[0-9一二三四五六七八九十百千万两]+"),
)

_RULES: tuple[tuple[str, str, re.Pattern[str]], ...] = (
    (
        "secret",
        "github-token",
        re.compile(r"(?<![A-Za-z0-9])gh[pousr]_[A-Za-z0-9]{20,}(?![A-Za-z0-9])"),
    ),
    (
        "secret",
        "api-secret-assignment",
        re.compile(
            r"(?i)(?:api[_-]?key|access[_-]?token|auth[_-]?token|token|client[_-]?secret|password)"
            r"\s*[:=]\s*[\"']?(?!example\b|placeholder\b|redacted\b|none\b|null\b)"
            r"[A-Za-z0-9_./+=-]{12,}"
        ),
    ),
    (
        "secret",
        "private-key-header",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    ),
    (
        "secret",
        "provider-key",
        re.compile(r"(?<![A-Za-z0-9])(?:sk-[A-Za-z0-9_-]{20,}|AKIA[A-Z0-9]{16})(?![A-Za-z0-9])"),
    ),
    (
        "student_pii",
        "student-name-label",
        re.compile(r"(?:学生|考生)?(?:姓名|名字)\s*[:：=]\s*[^\s,，;；]{1,32}"),
    ),
    (
        "student_pii",
        "student-address-label",
        re.compile(
            r"(?:(?:学生|考生|家庭|居住|通讯)(?:住址|地址)|(?<![\u4e00-\u9fff])住址)"
            r"\s*[:：=]\s*[^\r\n]{2,100}"
        ),
    ),
    (
        "phone",
        "mainland-phone",
        re.compile(r"(?<![0-9A-Fa-f])1[3-9]\d{9}(?![0-9A-Fa-f])"),
    ),
    (
        "identity_number",
        "mainland-identity-number",
        re.compile(r"(?<![0-9A-Fa-f])\d{6}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[0-9Xx](?![0-9A-Fa-f])"),
    ),
    (
        "private_system_reference",
        "parent-private-system",
        re.compile(r"(?i)(?:shengxue[-_ ]system|shengxue[-_ ]ai[-_ ]planner)"),
    ),
    (
        "absolute_local_path",
        "windows-absolute-path",
        re.compile(r"(?<![A-Za-z0-9])(?:[A-Za-z]:[\\/](?:[^\s<>()\[\]{}\"']+))"),
    ),
    (
        "absolute_local_path",
        "posix-home-path",
        re.compile(r"(?<![A-Za-z0-9:])(?:/home/|/Users/)[^\s<>()\[\]{}\"']+"),
    ),
    (
        "absolute_local_path",
        "file-url",
        re.compile(r"(?i)file:///{1,3}[^\s<>()\[\]{}\"']+"),
    ),
    (
        "absolute_local_path",
        "posix-absolute-attachment",
        re.compile(
            r"(?i)(?:附件|本地文件|本地路径|attachment|local[ _-]?path)\s*[:：=]\s*"
            r"/(?!/)[^\s<>()\[\]{}\"']+"
        ),
    ),
    (
        "absolute_local_path",
        "unc-absolute-path",
        re.compile(
            r"(?i)(?:附件|本地文件|本地路径|attachment|local[ _-]?path)\s*[:：=]\s*"
            r"(?:\\\\|//)[^\\/\s]+[\\/][^\s<>()\[\]{}\"']+"
        ),
    ),
    (
        "pricing_or_sales",
        "sales-language",
        re.compile(r"(?:限时优惠|立即咨询|扫码咨询|购买咨询|报名优惠|私聊(?:咨询|购买)|加微信)"),
    ),
)

_POLICY_KEYS = frozenset(
    {
        "schema_version",
        "binary_extensions",
        "binary_release_manifest",
        "max_text_bytes",
        "forbidden_tracked_directories",
        "allowlist",
        "file_allowlist",
        "required_release_paths",
        "required_release_prefixes",
        "ci_generated_paths",
        "deterministic_test_modules",
        "docx_test_modules",
    }
)
_ALLOWLIST_KEYS = frozenset({"path", "kind", "line_sha256", "reason"})
_FILE_ALLOWLIST_KEYS = frozenset({"path", "kinds", "file_sha256", "reason"})
_BINARY_MANIFEST_KEYS = frozenset({"path", "sha256", "classification"})
_RIGHTS_REVIEWED_BINARY_MANIFEST_KEYS = _BINARY_MANIFEST_KEYS | {"rights_doc"}
_SHA256_RE = re.compile(r"[0-9a-f]{64}")
_PATH_DRIVE_RE = re.compile(r"^[A-Za-z]:")
_EDUCATIONAL_PRICE_CONTEXT_RE = re.compile(
    r"(?:学费|住宿费|教材费|奖学金|助学金|助学贷款|困难补助|生活补助|补贴|资助)"
)
_COMMERCIAL_PRICE_CONTEXT_RE = re.compile(
    r"(?:(?:产品|服务|课程|咨询|套餐|会员)(?:售价|报价|价格|收费)|"
    r"售价|报价|原价|现价|优惠价|购买价|立即购买|下单|扫码咨询|购买咨询|报名优惠|私聊)"
)
_PRICE_CLAUSE_BOUNDARIES = frozenset("。；;，,！？!?\n\r")


class PolicyError(ValueError):
    """The release policy is malformed or contains unsupported fields."""


@dataclass(frozen=True)
class AllowlistEntry:
    path: str
    kind: str
    line_sha256: str
    reason: str


@dataclass(frozen=True)
class FileAllowlistEntry:
    path: str
    kinds: frozenset[str]
    file_sha256: str
    reason: str


@dataclass(frozen=True)
class BinaryReleaseManifestEntry:
    path: str
    sha256: str
    classification: str
    rights_doc: str | None = None


@dataclass(frozen=True)
class ReleasePolicy:
    schema_version: str
    binary_extensions: frozenset[str]
    binary_release_manifest: tuple[BinaryReleaseManifestEntry, ...]
    max_text_bytes: int
    forbidden_tracked_directories: tuple[str, ...]
    allowlist: tuple[AllowlistEntry, ...]
    file_allowlist: tuple[FileAllowlistEntry, ...]
    required_release_paths: tuple[str, ...]
    required_release_prefixes: tuple[str, ...]
    ci_generated_paths: tuple[str, ...]
    deterministic_test_modules: tuple[str, ...]
    docx_test_modules: tuple[str, ...]


@dataclass(frozen=True)
class Finding:
    kind: str
    rule_id: str
    line: int
    column: int
    path: str | None = None

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "kind": self.kind,
            "rule": self.rule_id,
            "line": self.line,
        }
        if self.path is not None:
            result["path"] = self.path
        return result


@dataclass(frozen=True)
class ScanSummary:
    findings: tuple[Finding, ...]
    scanned_files: int
    skipped_binary_files: int

    @property
    def ok(self) -> bool:
        return not self.findings

    def to_dict(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "scanned_files": self.scanned_files,
            "skipped_binary_files": self.skipped_binary_files,
            "finding_count": len(self.findings),
            "findings": [finding.to_dict() for finding in self.findings],
        }


@dataclass(frozen=True)
class GitTrackedEntry:
    """One stage-zero Git index entry with a safe logical path."""

    path: str
    mode: str
    object_id: str


@dataclass(frozen=True)
class GitReplacementRef:
    """One validated Git replacement mapping, retained only as object IDs."""

    original_object_id: str
    replacement_object_id: str


@dataclass(frozen=True)
class BinaryManifestValidation:
    findings: tuple[Finding, ...]
    approved_paths: frozenset[str]

    @property
    def ok(self) -> bool:
        return not self.findings


def find_price_text(text: object) -> Optional[str]:
    """Return the first legacy price match, preserving the report API."""

    if not text:
        return None
    value = str(text)
    hits = [match for regex in PRICE_RES if (match := regex.search(value))]
    if not hits:
        return None
    return min(hits, key=lambda match: match.start()).group(0)


def contains_price_text(text: object) -> bool:
    """Return whether the legacy deterministic price rules match."""

    return find_price_text(text) is not None


def _strict_json(raw: bytes) -> object:
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeError as error:
        raise PolicyError("policy is not valid UTF-8") from error

    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise PolicyError("policy contains a duplicate key")
            result[key] = value
        return result

    def reject_nonfinite(_value: str) -> object:
        raise PolicyError("policy contains a non-finite number")

    try:
        return json.loads(
            text,
            object_pairs_hook=reject_duplicates,
            parse_constant=reject_nonfinite,
        )
    except PolicyError:
        raise
    except (TypeError, ValueError) as error:
        raise PolicyError("policy is not valid JSON") from error


def canonical_repository_path(value: object, field: str = "repository path") -> str:
    """Return one canonical, normalized POSIX repository path."""

    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        raise PolicyError(f"{field} must be a non-empty repository-relative path")
    normalized = value
    if unicodedata.normalize("NFKC", normalized) != normalized:
        raise PolicyError(f"{field} must use normalized Unicode spelling")
    pure = PurePosixPath(normalized)
    if pure.is_absolute() or _PATH_DRIVE_RE.match(normalized) or ".." in pure.parts:
        raise PolicyError(f"{field} must stay inside the repository")
    canonical = pure.as_posix()
    if canonical != normalized or canonical.startswith("./"):
        raise PolicyError(f"{field} must use canonical POSIX spelling")
    return canonical


def _string_list(value: object, field: str) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise PolicyError(f"{field} must be a list of non-empty strings")
    if len(value) != len(set(value)):
        raise PolicyError(f"{field} contains duplicate values")
    return tuple(value)


def _policy_path_list(value: object, field: str) -> tuple[str, ...]:
    paths = tuple(canonical_repository_path(item, field) for item in _string_list(value, field))
    identities = tuple(unicodedata.normalize("NFKC", item).casefold() for item in paths)
    if len(identities) != len(set(identities)):
        raise PolicyError(f"{field} contains colliding path identities")
    return paths


def parse_policy_bytes(raw: bytes) -> ReleasePolicy:
    """Parse one strict policy snapshot; unknown fields fail closed."""

    if not isinstance(raw, bytes):
        raise PolicyError("policy must be bytes")
    if len(raw) > 1024 * 1024:
        raise PolicyError("policy is too large")
    payload = _strict_json(raw)
    if not isinstance(payload, dict) or set(payload) != _POLICY_KEYS:
        raise PolicyError("policy keys do not match the supported schema")
    if payload["schema_version"] != "1.2":
        raise PolicyError("unsupported policy schema version")

    extensions = _string_list(payload["binary_extensions"], "binary_extensions")
    normalized_extensions = tuple(extension.casefold() for extension in extensions)
    if any(not extension.startswith(".") or "/" in extension or "\\" in extension for extension in normalized_extensions):
        raise PolicyError("binary extensions must begin with a dot")
    if len(normalized_extensions) != len(set(normalized_extensions)):
        raise PolicyError("binary extensions collide after case folding")

    manifest_payload = payload["binary_release_manifest"]
    if not isinstance(manifest_payload, list):
        raise PolicyError("binary_release_manifest must be a list")
    binary_manifest: list[BinaryReleaseManifestEntry] = []
    binary_identities: set[str] = set()
    for item in manifest_payload:
        if not isinstance(item, dict):
            raise PolicyError("binary manifest entry must be an object")
        classification = item.get("classification")
        expected_keys = (
            _BINARY_MANIFEST_KEYS
            if classification == "synthetic"
            else _RIGHTS_REVIEWED_BINARY_MANIFEST_KEYS
            if classification == "rights-reviewed"
            else frozenset()
        )
        if not expected_keys or set(item) != expected_keys:
            raise PolicyError("binary manifest entry keys or classification are invalid")
        entry_path = canonical_repository_path(item["path"], "binary_release_manifest.path")
        digest = item["sha256"]
        if PurePosixPath(entry_path).suffix.casefold() not in normalized_extensions:
            raise PolicyError("binary manifest path must use a declared binary extension")
        if not isinstance(digest, str) or _SHA256_RE.fullmatch(digest) is None:
            raise PolicyError("binary manifest sha256 is invalid")
        identity = unicodedata.normalize("NFKC", entry_path).casefold()
        if identity in binary_identities:
            raise PolicyError("binary manifest contains a duplicate path")
        binary_identities.add(identity)
        rights_doc = None
        if classification == "rights-reviewed":
            rights_doc = canonical_repository_path(
                item["rights_doc"],
                "binary_release_manifest.rights_doc",
            )
            if rights_doc == entry_path or PurePosixPath(rights_doc).suffix.casefold() in normalized_extensions:
                raise PolicyError("binary rights document is invalid")
        binary_manifest.append(
            BinaryReleaseManifestEntry(
                path=entry_path,
                sha256=digest,
                classification=classification,
                rights_doc=rights_doc,
            )
        )

    max_text_bytes = payload["max_text_bytes"]
    if (
        not isinstance(max_text_bytes, int)
        or isinstance(max_text_bytes, bool)
        or not 1024 <= max_text_bytes <= 16 * 1024 * 1024
    ):
        raise PolicyError("max_text_bytes is outside the supported bound")

    directories = _policy_path_list(payload["forbidden_tracked_directories"], "forbidden_tracked_directories")
    required_paths = _policy_path_list(payload["required_release_paths"], "required_release_paths")
    required_prefixes = _policy_path_list(
        payload["required_release_prefixes"],
        "required_release_prefixes",
    )
    if not required_paths or not required_prefixes:
        raise PolicyError("release path requirements must not be empty")
    generated_paths = _policy_path_list(payload["ci_generated_paths"], "ci_generated_paths")
    modules = _string_list(payload["deterministic_test_modules"], "deterministic_test_modules")
    docx_modules = _string_list(payload["docx_test_modules"], "docx_test_modules")
    if any(not re.fullmatch(r"tests\.test_[A-Za-z0-9_]+", module) for module in modules):
        raise PolicyError("deterministic_test_modules contains an invalid module name")
    if any(not re.fullmatch(r"tests\.test_[A-Za-z0-9_]+", module) for module in docx_modules):
        raise PolicyError("docx_test_modules contains an invalid module name")
    if not modules or not docx_modules:
        raise PolicyError("test module inventories must not be empty")

    supported_kinds = {rule[0] for rule in _RULES} | {"pricing_or_sales"}
    allowlist_payload = payload["allowlist"]
    if not isinstance(allowlist_payload, list):
        raise PolicyError("allowlist must be a list")
    allowlist: list[AllowlistEntry] = []
    identities: set[tuple[str, str, str]] = set()
    for item in allowlist_payload:
        if not isinstance(item, dict) or set(item) != _ALLOWLIST_KEYS:
            raise PolicyError("allowlist entry keys do not match the supported schema")
        entry_path = canonical_repository_path(item["path"], "allowlist.path")
        kind = item["kind"]
        digest = item["line_sha256"]
        reason = item["reason"]
        if not isinstance(kind, str) or kind not in supported_kinds:
            raise PolicyError("allowlist kind is unsupported")
        if not isinstance(digest, str) or _SHA256_RE.fullmatch(digest) is None:
            raise PolicyError("allowlist line_sha256 is invalid")
        if not isinstance(reason, str) or not (8 <= len(reason) <= 200) or "\n" in reason:
            raise PolicyError("allowlist reason must be documented on one line")
        identity = (unicodedata.normalize("NFKC", entry_path).casefold(), kind, digest)
        if identity in identities:
            raise PolicyError("allowlist contains a duplicate identity")
        identities.add(identity)
        allowlist.append(AllowlistEntry(entry_path, kind, digest, reason))

    file_allowlist_payload = payload["file_allowlist"]
    if not isinstance(file_allowlist_payload, list):
        raise PolicyError("file_allowlist must be a list")
    file_allowlist: list[FileAllowlistEntry] = []
    file_identities: set[str] = set()
    for item in file_allowlist_payload:
        if not isinstance(item, dict) or set(item) != _FILE_ALLOWLIST_KEYS:
            raise PolicyError("file_allowlist entry keys do not match the supported schema")
        entry_path = canonical_repository_path(item["path"], "file_allowlist.path")
        kinds = frozenset(_string_list(item["kinds"], "file_allowlist.kinds"))
        digest = item["file_sha256"]
        reason = item["reason"]
        if not kinds or not kinds <= supported_kinds:
            raise PolicyError("file_allowlist kinds are unsupported")
        if not isinstance(digest, str) or _SHA256_RE.fullmatch(digest) is None:
            raise PolicyError("file_allowlist file_sha256 is invalid")
        if not isinstance(reason, str) or not (8 <= len(reason) <= 200) or "\n" in reason:
            raise PolicyError("file_allowlist reason must be documented on one line")
        entry_identity = unicodedata.normalize("NFKC", entry_path).casefold()
        if entry_identity in file_identities:
            raise PolicyError("file_allowlist contains a duplicate path")
        file_identities.add(entry_identity)
        file_allowlist.append(FileAllowlistEntry(entry_path, kinds, digest, reason))

    return ReleasePolicy(
        schema_version="1.2",
        binary_extensions=frozenset(normalized_extensions),
        binary_release_manifest=tuple(binary_manifest),
        max_text_bytes=max_text_bytes,
        forbidden_tracked_directories=directories,
        allowlist=tuple(allowlist),
        file_allowlist=tuple(file_allowlist),
        required_release_paths=required_paths,
        required_release_prefixes=required_prefixes,
        ci_generated_paths=generated_paths,
        deterministic_test_modules=modules,
        docx_test_modules=docx_modules,
    )


def load_policy(path: Path | str) -> ReleasePolicy:
    """Load one strict policy file through the snapshot parser."""

    try:
        raw = Path(path).read_bytes()
    except OSError as error:
        raise PolicyError("policy cannot be read") from error
    return parse_policy_bytes(raw)


def missing_required_release_paths(
    policy: ReleasePolicy,
    paths: Sequence[str],
) -> tuple[str, ...]:
    """Return unsatisfied exact paths and nonempty subtree requirements."""

    inventory = frozenset(paths)
    missing = [path for path in policy.required_release_paths if path not in inventory]
    for prefix in policy.required_release_prefixes:
        marker = prefix + "/"
        if not any(path.startswith(marker) for path in inventory):
            missing.append(prefix + "/**")
    return tuple(missing)


def validate_binary_release_manifest(
    policy: ReleasePolicy,
    entries: Sequence[GitTrackedEntry],
    read_bytes: Callable[[GitTrackedEntry], bytes],
) -> BinaryManifestValidation:
    """Validate the exact binary allowlist against one caller-owned snapshot."""

    inventory = {entry.path: entry for entry in entries}
    declared = {entry.path: entry for entry in policy.binary_release_manifest}
    findings: list[Finding] = []
    approved: set[str] = set()

    for path, manifest in declared.items():
        tracked = inventory.get(path)
        if tracked is None:
            findings.append(
                Finding("binary_manifest", "binary-manifest-path-missing", 0, 0, _reported_path(path))
            )
            continue
        if re.fullmatch(r"100[0-7]{3}", tracked.mode) is None:
            findings.append(
                Finding("binary_manifest", "binary-manifest-mode-invalid", 0, 0, _reported_path(path))
            )
            continue
        if manifest.rights_doc is not None:
            rights_entry = inventory.get(manifest.rights_doc)
            if rights_entry is None or re.fullmatch(r"100[0-7]{3}", rights_entry.mode) is None:
                findings.append(
                    Finding(
                        "binary_manifest",
                        "binary-rights-document-missing",
                        0,
                        0,
                        _reported_path(path),
                    )
                )
                continue
        try:
            raw = read_bytes(tracked)
        except (OSError, RuntimeError, ValueError):
            findings.append(
                Finding("binary_manifest", "binary-manifest-unreadable", 0, 0, _reported_path(path))
            )
            continue
        if not isinstance(raw, bytes) or hashlib.sha256(raw).hexdigest() != manifest.sha256:
            findings.append(
                Finding("binary_manifest", "binary-manifest-hash-mismatch", 0, 0, _reported_path(path))
            )
            continue
        approved.add(path)

    for entry in entries:
        if (
            PurePosixPath(entry.path).suffix.casefold() in policy.binary_extensions
            and entry.path not in declared
        ):
            findings.append(
                Finding(
                    "binary_manifest",
                    "unmanifested-binary-path",
                    0,
                    0,
                    _reported_path(entry.path),
                )
            )

    return BinaryManifestValidation(tuple(findings), frozenset(approved))


def _is_allowlisted(policy: ReleasePolicy | None, path: str | None, kind: str, line: str) -> bool:
    if policy is None or path is None:
        return False
    digest = hashlib.sha256(line.encode("utf-8")).hexdigest()
    return any(
        entry.path == path and entry.kind == kind and entry.line_sha256 == digest
        for entry in policy.allowlist
    )


def _reported_path(path: str | None) -> str | None:
    if path is None:
        return None
    if any(regex.search(path) for regex in PRICE_RES) or any(
        regex.search(path)
        for kind, _rule_id, regex in _RULES
        if kind in {
            "secret",
            "student_pii",
            "phone",
            "identity_number",
            "absolute_local_path",
            "private_system_reference",
            "pricing_or_sales",
        }
    ):
        return "redacted-sensitive-path"
    if any(ord(character) < 32 or ord(character) == 127 for character in path) or len(path) > 180:
        return "redacted-sensitive-path"
    return path


def _portable_text_digest(raw: bytes) -> str:
    """Hash text canonically so exact allowlists survive Git EOL checkout policy."""

    normalized = raw.decode("utf-8", errors="strict").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def scan_text(
    text: object,
    *,
    path: str | None = None,
    policy: ReleasePolicy | None = None,
    _file_allowlisted_kinds: frozenset[str] = frozenset(),
) -> list[Finding]:
    """Scan text without including matched content in returned findings."""

    if text is None:
        return []
    value = str(text)
    findings: list[Finding] = []
    seen: set[tuple[str, str, int, int]] = set()
    for line_number, line in enumerate(value.splitlines() or [value], start=1):
        matches: list[tuple[str, str, re.Match[str]]] = []
        for kind, rule_id, regex in _RULES:
            matches.extend((kind, rule_id, match) for match in regex.finditer(line))
        for regex in PRICE_RES:
            for match in regex.finditer(line):
                clause_start = max(
                    (index + 1 for index, character in enumerate(line[: match.start()]) if character in _PRICE_CLAUSE_BOUNDARIES),
                    default=0,
                )
                prefix = line[clause_start : match.start()]
                educational = list(_EDUCATIONAL_PRICE_CONTEXT_RE.finditer(prefix))
                commercial = list(_COMMERCIAL_PRICE_CONTEXT_RE.finditer(prefix))
                if educational and (
                    not commercial or educational[-1].end() > commercial[-1].end()
                ):
                    continue
                matches.append(("pricing_or_sales", "price-expression", match))
        for kind, rule_id, match in sorted(matches, key=lambda item: (item[2].start(), item[0], item[1])):
            if kind in _file_allowlisted_kinds or _is_allowlisted(policy, path, kind, line):
                continue
            identity = (kind, rule_id, line_number, match.start() + 1)
            if identity in seen:
                continue
            seen.add(identity)
            findings.append(Finding(kind, rule_id, line_number, match.start() + 1, _reported_path(path)))
    return findings


def git_environment() -> dict[str, str]:
    """Return a child environment with every ambient Git control removed."""

    environment = {
        name: value
        for name, value in os.environ.items()
        if not name.upper().startswith("GIT_")
    }
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    return environment


def _run_git(root: Path, arguments: Sequence[str]) -> bytes:
    completed = subprocess.run(
        ["git", "--no-replace-objects", *arguments],
        cwd=root,
        check=False,
        capture_output=True,
        env=git_environment(),
    )
    if completed.returncode != 0:
        raise RuntimeError("git inventory failed")
    return completed.stdout


def git_replacement_refs(root: Path) -> tuple[GitReplacementRef, ...]:
    """Enumerate and validate the standard replacement namespace without dereferencing it."""

    output = _run_git(
        root,
        ("for-each-ref", "--format=%(refname) %(objectname)", "refs/replace/"),
    )
    replacements: list[GitReplacementRef] = []
    object_pattern = rb"(?:[0-9a-f]{40}|[0-9a-f]{64})"
    for record in output.splitlines():
        match = re.fullmatch(
            rb"refs/replace/(" + object_pattern + rb") (" + object_pattern + rb")",
            record,
        )
        if match is None:
            raise RuntimeError("git replacement inventory is malformed")
        replacements.append(
            GitReplacementRef(
                match.group(1).decode("ascii"),
                match.group(2).decode("ascii"),
            )
        )
    return tuple(replacements)


def git_write_tree(root: Path) -> str:
    """Freeze the stage-zero index and return one original tree object ID."""

    try:
        tree_oid = _run_git(root, ("write-tree",)).decode("ascii", errors="strict").strip()
    except UnicodeError as error:
        raise RuntimeError("git tree snapshot is malformed") from error
    if _SHA256_RE.fullmatch(tree_oid) is None and re.fullmatch(r"[0-9a-f]{40}", tree_oid) is None:
        raise RuntimeError("git tree snapshot is malformed")
    return tree_oid


def git_tree_entries(root: Path, tree_oid: str) -> tuple[GitTrackedEntry, ...]:
    """Read one recursive immutable tree inventory without replacement dereferencing."""

    if _SHA256_RE.fullmatch(tree_oid) is None and re.fullmatch(r"[0-9a-f]{40}", tree_oid) is None:
        raise RuntimeError("git tree object ID is malformed")
    records = _run_git(
        root,
        ("ls-tree", "-rz", "--full-tree", tree_oid, "--"),
    ).split(b"\x00")
    entries: list[GitTrackedEntry] = []
    try:
        for record in records:
            if not record:
                continue
            metadata, encoded_path = record.split(b"\t", 1)
            mode, object_type, object_id = metadata.split(b" ", 2)
            if (
                re.fullmatch(rb"[0-7]{6}", mode) is None
                or object_type not in {b"blob", b"commit"}
                or re.fullmatch(rb"(?:[0-9a-f]{40}|[0-9a-f]{64})", object_id) is None
            ):
                raise ValueError
            entries.append(
                GitTrackedEntry(
                    path=encoded_path.decode("utf-8", errors="strict"),
                    mode=mode.decode("ascii"),
                    object_id=object_id.decode("ascii"),
                )
            )
    except (UnicodeError, ValueError) as error:
        raise RuntimeError("git tree inventory is malformed") from error
    return tuple(entries)


def git_blob_bytes(root: Path, object_id: str) -> bytes:
    """Read an original blob by exact object ID."""

    if _SHA256_RE.fullmatch(object_id) is None and re.fullmatch(r"[0-9a-f]{40}", object_id) is None:
        raise RuntimeError("git blob object ID is malformed")
    return _run_git(root, ("cat-file", "blob", object_id))


def git_paths(root: Path, arguments: Sequence[str]) -> tuple[str, ...]:
    """Run one NUL-delimited Git inventory command in the isolated environment."""

    try:
        return tuple(
            item.decode("utf-8", errors="strict")
            for item in _run_git(root, arguments).split(b"\x00")
            if item
        )
    except UnicodeError as error:
        raise RuntimeError("git inventory is not UTF-8") from error


def git_top_level(root: Path) -> Path:
    """Resolve Git's top level without honoring caller-provided Git controls."""

    try:
        value = _run_git(root, ("rev-parse", "--show-toplevel")).decode("utf-8", errors="strict").strip()
        return Path(value).resolve(strict=True)
    except (UnicodeError, OSError) as error:
        raise RuntimeError("git top level is invalid") from error


def git_tracked_entries(root: Path) -> tuple[GitTrackedEntry, ...]:
    """Read and strictly parse stage-zero index entries."""

    records = _run_git(root, ("ls-files", "--stage", "-z", "--")).split(b"\x00")
    entries: list[GitTrackedEntry] = []
    try:
        for record in records:
            if not record:
                continue
            metadata, encoded_path = record.split(b"\t", 1)
            mode, object_id, stage = metadata.split(b" ", 2)
            if re.fullmatch(rb"[0-7]{6}", mode) is None or re.fullmatch(
                rb"(?:[0-9a-f]{40}|[0-9a-f]{64})", object_id
            ) is None:
                raise ValueError
            if stage != b"0":
                raise ValueError
            entries.append(
                GitTrackedEntry(
                    encoded_path.decode("utf-8", errors="strict"),
                    mode.decode("ascii"),
                    object_id.decode("ascii"),
                )
            )
    except (UnicodeError, ValueError) as error:
        raise RuntimeError("git index inventory is malformed") from error
    return tuple(entries)


def safe_tracked_file(root: Path, relative: str) -> tuple[Path | None, Finding | None]:
    """Validate every component of one tracked path without following reparses."""

    try:
        canonical = canonical_repository_path(relative, "tracked path")
    except PolicyError:
        return None, Finding("tracked_path", "noncanonical-tracked-path", 0, 0, None)
    candidate = root
    metadata = None
    for part in PurePosixPath(canonical).parts:
        candidate = candidate / part
        try:
            metadata = candidate.lstat()
        except OSError:
            return None, Finding("tracked_path", "missing-tracked-path", 0, 0, _reported_path(canonical))
        attributes = getattr(metadata, "st_file_attributes", 0)
        reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        if stat.S_ISLNK(metadata.st_mode) or bool(attributes & reparse_flag):
            return None, Finding("tracked_path", "tracked-link-or-reparse", 0, 0, _reported_path(canonical))
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError):
        return None, Finding("tracked_path", "tracked-path-outside-root", 0, 0, _reported_path(canonical))
    if not candidate.is_file():
        return None, Finding("tracked_path", "tracked-path-not-file", 0, 0, _reported_path(canonical))
    return candidate, None


def scan_tracked(
    root: Path | str,
    policy: ReleasePolicy,
    entries: Sequence[GitTrackedEntry] | None = None,
) -> ScanSummary:
    """Scan only Git-tracked, bounded UTF-8 text files beneath ``root``."""

    repo = Path(root).resolve()
    replacements = git_replacement_refs(repo)
    if replacements:
        return ScanSummary(
            (Finding("git_state", "replacement-refs-present", 0, 0, None),),
            0,
            0,
        )
    inventory = tuple(entries) if entries is not None else git_tracked_entries(repo)
    findings: list[Finding] = []
    scanned = 0
    skipped = 0
    binary_cache: dict[str, bytes] = {}

    def read_worktree_entry(entry: GitTrackedEntry) -> bytes:
        if entry.path in binary_cache:
            return binary_cache[entry.path]
        candidate, path_finding = safe_tracked_file(repo, entry.path)
        if path_finding is not None or candidate is None:
            raise OSError("unsafe tracked binary path")
        raw = candidate.read_bytes()
        binary_cache[entry.path] = raw
        return raw

    binary_validation = validate_binary_release_manifest(
        policy,
        inventory,
        read_worktree_entry,
    )
    findings.extend(binary_validation.findings)
    for entry in inventory:
        relative = entry.path
        if re.fullmatch(r"100[0-7]{3}", entry.mode) is None:
            findings.append(Finding("tracked_path", "unsupported-tracked-mode", 0, 0, _reported_path(relative)))
            continue
        candidate, path_finding = safe_tracked_file(repo, relative)
        if path_finding is not None:
            findings.append(path_finding)
            continue
        assert candidate is not None
        if candidate.suffix.casefold() in policy.binary_extensions:
            if relative in binary_validation.approved_paths:
                skipped += 1
            continue
        try:
            size = candidate.stat().st_size
        except OSError:
            findings.append(Finding("tracked_path", "unreadable-tracked-file", 0, 0, _reported_path(relative)))
            continue
        if size > policy.max_text_bytes:
            findings.append(Finding("tracked_path", "tracked-text-too-large", 0, 0, _reported_path(relative)))
            continue
        try:
            raw = candidate.read_bytes()
        except OSError:
            findings.append(Finding("tracked_path", "unreadable-tracked-file", 0, 0, _reported_path(relative)))
            continue
        if b"\x00" in raw:
            findings.append(Finding("tracked_path", "undeclared-binary-content", 0, 0, _reported_path(relative)))
            continue
        try:
            content = raw.decode("utf-8", errors="strict")
        except UnicodeError:
            findings.append(Finding("tracked_path", "tracked-text-not-utf8", 0, 0, _reported_path(relative)))
            continue
        scanned += 1
        file_digest = _portable_text_digest(raw)
        file_allowlisted_kinds = frozenset().union(
            *(entry.kinds for entry in policy.file_allowlist if entry.path == relative and entry.file_sha256 == file_digest)
        )
        findings.extend(
            scan_text(
                content,
                path=relative,
                policy=policy,
                _file_allowlisted_kinds=file_allowlisted_kinds,
            )
        )
    return ScanSummary(tuple(findings), scanned, skipped)


def scan_git_snapshot(
    root: Path | str,
    policy: ReleasePolicy,
    entries: Sequence[GitTrackedEntry],
) -> ScanSummary:
    """Scan one immutable Git tree using only original blob object IDs."""

    repo = Path(root).resolve()
    inventory = tuple(entries)
    findings: list[Finding] = []
    scanned = 0
    skipped = 0

    binary_validation = validate_binary_release_manifest(
        policy,
        inventory,
        lambda entry: git_blob_bytes(repo, entry.object_id),
    )
    findings.extend(binary_validation.findings)
    for entry in inventory:
        relative = entry.path
        try:
            canonical = canonical_repository_path(relative, "tracked path")
        except PolicyError:
            findings.append(Finding("tracked_path", "noncanonical-tracked-path", 0, 0, None))
            continue
        if re.fullmatch(r"100[0-7]{3}", entry.mode) is None:
            findings.append(
                Finding("tracked_path", "unsupported-tracked-mode", 0, 0, _reported_path(canonical))
            )
            continue
        if PurePosixPath(canonical).suffix.casefold() in policy.binary_extensions:
            if canonical in binary_validation.approved_paths:
                skipped += 1
            continue
        try:
            raw = git_blob_bytes(repo, entry.object_id)
        except RuntimeError:
            findings.append(
                Finding("tracked_path", "unreadable-tracked-blob", 0, 0, _reported_path(canonical))
            )
            continue
        if len(raw) > policy.max_text_bytes:
            findings.append(
                Finding("tracked_path", "tracked-text-too-large", 0, 0, _reported_path(canonical))
            )
            continue
        if b"\x00" in raw:
            findings.append(
                Finding("tracked_path", "undeclared-binary-content", 0, 0, _reported_path(canonical))
            )
            continue
        try:
            content = raw.decode("utf-8", errors="strict")
        except UnicodeError:
            findings.append(
                Finding("tracked_path", "tracked-text-not-utf8", 0, 0, _reported_path(canonical))
            )
            continue
        scanned += 1
        file_digest = _portable_text_digest(raw)
        file_allowlisted_kinds = frozenset().union(
            *(
                item.kinds
                for item in policy.file_allowlist
                if item.path == canonical and item.file_sha256 == file_digest
            )
        )
        findings.extend(
            scan_text(
                content,
                path=canonical,
                policy=policy,
                _file_allowlisted_kinds=file_allowlisted_kinds,
            )
        )
    return ScanSummary(tuple(findings), scanned, skipped)


def _configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def _file_mode(path: str) -> int:
    try:
        with open(path, encoding="utf-8") as handle:
            content = handle.read(16 * 1024 * 1024 + 1)
        if len(content.encode("utf-8")) > 16 * 1024 * 1024 or "\x00" in content:
            raise ValueError
    except (OSError, UnicodeError, ValueError):
        print("错误：无法读取输入文件", file=sys.stderr)
        return 2
    findings = scan_text(content)
    if findings:
        first = findings[0]
        print(
            f"合规扫描未通过：kind={first.kind} line={first.line} rule={first.rule_id}；请移除后重新交付",
            file=sys.stderr,
        )
        return 2
    print("合规扫描通过")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run a privacy-safe single-file or Git-tracked compliance scan."""

    _configure_stdio()
    arguments = list(sys.argv[1:] if argv is None else argv)
    if len(arguments) == 1 and not arguments[0].startswith("-"):
        return _file_mode(arguments[0])

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("path", nargs="?")
    parser.add_argument("--tracked", action="store_true")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--policy", type=Path, default=None)
    try:
        parsed = parser.parse_args(arguments)
    except SystemExit as error:
        return int(error.code)
    if parsed.path is not None and not parsed.tracked:
        return _file_mode(parsed.path)
    if not parsed.tracked or parsed.path is not None:
        print("用法：python scripts/compliance_scan.py <文件路径> 或 --tracked", file=sys.stderr)
        return 2
    root = parsed.root.resolve()
    policy_path = parsed.policy or root / "release-policy.json"
    try:
        policy = load_policy(policy_path)
        summary = scan_tracked(root, policy)
    except (PolicyError, RuntimeError):
        print(
            json.dumps(
                {"ok": False, "error": "compliance-scan-configuration-error"},
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 2
    print(json.dumps(summary.to_dict(), ensure_ascii=False, sort_keys=True))
    return 0 if summary.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
