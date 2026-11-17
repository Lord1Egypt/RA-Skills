#!/usr/bin/env python3
"""Audit selected GitHub repository documents for locale parity.

The audit is deliberately offline and deterministic. It checks document
structure and references, plus an optional local repository-metadata snapshot.
It does not translate text, call GitHub, inspect remote state, or scan public
repository suitability.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Optional, Sequence
from urllib.parse import unquote, urlsplit


_LOCALE_RE = re.compile(r"^[A-Za-z]{2,3}(?:[-_][A-Za-z0-9]{2,8})*$")
_FENCE_RE = re.compile(
    r"^\s{0,3}(" + chr(96) + r"{3,}|~{3,})(.*)$"
)
_HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})[ \t]+(.+?)\s*#*\s*$")
_MARKDOWN_IMAGE_RE = re.compile(
    r"!\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))"
)
_MARKDOWN_LINK_RE = re.compile(
    r"(?<!!)\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))"
)
_HTML_IMAGE_RE = re.compile(
    r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE
)
_HTML_LINK_RE = re.compile(
    r"<a\b[^>]*\bhref=[\"']([^\"']+)[\"']", re.IGNORECASE
)
_TOPIC_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel", "data"}


@dataclass(frozen=True)
class DocumentSpec:
    locale: str
    path: Path


@dataclass(frozen=True)
class Issue:
    code: str
    message: str


@dataclass(frozen=True)
class AuditReport:
    repository: Path
    documents: tuple[DocumentSpec, ...]
    issues: tuple[Issue, ...]
    manual_review: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.issues


@dataclass(frozen=True)
class _MarkdownSnapshot:
    heading_levels: tuple[int, ...]
    fence_languages: tuple[str, ...]
    links: tuple[str, ...]
    images: tuple[str, ...]
    unclosed_fence: bool


def normalize_locale(value: str) -> str:
    """Return a predictable BCP-47-like locale spelling for comparison."""
    raw = value.strip().replace("_", "-")
    if not _LOCALE_RE.fullmatch(raw):
        raise ValueError(f"invalid locale: {value!r}")

    parts = raw.split("-")
    normalized = [parts[0].lower()]
    for part in parts[1:]:
        if len(part) == 4 and part.isalpha():
            normalized.append(part.title())
        elif (len(part) == 2 and part.isalpha()) or (
            len(part) == 3 and part.isdigit()
        ):
            normalized.append(part.upper())
        else:
            normalized.append(part.lower())
    return "-".join(normalized)


def _repository_path(path: Path) -> Path:
    return path.expanduser().resolve()


def _inside_repository(path: Path, repository: Path) -> bool:
    try:
        path.relative_to(repository)
    except ValueError:
        return False
    return True


def _case_sensitive_existing_path(path: Path, repository: Path) -> Optional[Path]:
    """Find a path using exact directory-entry casing on case-insensitive hosts."""
    try:
        relative = path.relative_to(repository)
    except ValueError:
        return None

    current = repository
    for part in relative.parts:
        if not current.is_dir():
            return None
        exact = next(
            (child for child in current.iterdir() if child.name == part),
            None,
        )
        if exact is None:
            return None
        current = exact
    return current


def parse_document_specs(
    values: Sequence[str], repo: Path
) -> tuple[DocumentSpec, ...]:
    """Parse repeated LOCALE=PATH arguments into repository-relative documents."""
    repository = _repository_path(Path(repo))
    if not repository.is_dir():
        raise ValueError(f"repository is not a directory: {repository}")
    if not values:
        raise ValueError("at least one --document LOCALE=PATH is required")

    documents: list[DocumentSpec] = []
    seen_locales: set[str] = set()
    for value in values:
        if "=" not in value:
            raise ValueError(f"document must use LOCALE=PATH: {value!r}")
        locale_text, path_text = value.split("=", 1)
        locale = normalize_locale(locale_text)
        if locale in seen_locales:
            raise ValueError(f"duplicate locale: {locale}")
        if not path_text.strip():
            raise ValueError(f"document path is empty for locale: {locale}")

        candidate = Path(path_text).expanduser()
        if not candidate.is_absolute():
            candidate = repository / candidate
        path = _repository_path(candidate)
        if not _inside_repository(path, repository):
            raise ValueError(f"document is outside repository: {path}")
        exact_path = _case_sensitive_existing_path(path, repository)
        if exact_path is None and path.is_file():
            raise ValueError(f"document path case mismatch: {path}")
        if exact_path is None or not exact_path.is_file():
            raise ValueError(f"document not found: {path}")

        seen_locales.add(locale)
        if path in (document.path for document in documents):
            raise ValueError(f"duplicate document path: {path}")
        documents.append(DocumentSpec(locale=locale, path=path))

    return tuple(documents)


def _extract_targets(text: str) -> _MarkdownSnapshot:
    headings: list[int] = []
    fence_languages: list[str] = []
    links: list[str] = []
    images: list[str] = []
    in_fence = False
    fence_char = ""
    fence_length = 0

    for line in text.splitlines():
        fence_match = _FENCE_RE.match(line)
        if fence_match:
            marker, info = fence_match.groups()
            if not in_fence:
                in_fence = True
                fence_char = marker[0]
                fence_length = len(marker)
                language = info.strip().split(maxsplit=1)[0].lower()
                fence_languages.append(language)
            elif marker[0] == fence_char and len(marker) >= fence_length:
                in_fence = False
                fence_char = ""
                fence_length = 0
            continue

        if in_fence:
            continue

        heading_match = _HEADING_RE.match(line)
        if heading_match:
            headings.append(len(heading_match.group(1)))

        for match in _MARKDOWN_IMAGE_RE.finditer(line):
            images.append(match.group(1) or match.group(2))
        for match in _MARKDOWN_LINK_RE.finditer(line):
            links.append(match.group(1) or match.group(2))
        for match in _HTML_IMAGE_RE.finditer(line):
            images.append(match.group(1))
        for match in _HTML_LINK_RE.finditer(line):
            links.append(match.group(1))

    return _MarkdownSnapshot(
        heading_levels=tuple(headings),
        fence_languages=tuple(fence_languages),
        links=tuple(links),
        images=tuple(images),
        unclosed_fence=in_fence,
    )


def _resolve_local_target(
    target: str, document: DocumentSpec, repository: Path
) -> tuple[Optional[Path], Optional[str]]:
    """Return a local path, or a non-local classification for one target."""
    clean = unquote(target.strip())
    if not clean or clean.startswith("#"):
        return None, None

    parsed = urlsplit(clean)
    if parsed.scheme:
        if parsed.scheme.lower() == "file":
            return None, "unsupported-file-url"
        if parsed.scheme.lower() in _EXTERNAL_SCHEMES or parsed.netloc:
            return None, None
        return None, None

    if clean.startswith("//") or clean.startswith("/"):
        return None, None

    target_path = Path(parsed.path)
    resolved = _repository_path(document.path.parent / target_path)
    if not _inside_repository(resolved, repository):
        return None, "local-target-outside-repository"
    return resolved, None


def _canonical_targets(
    targets: Sequence[str],
    document: DocumentSpec,
    repository: Path,
    selected_paths: set[Path],
    issues: list[Issue],
) -> set[str]:
    canonical: set[str] = set()
    for target in targets:
        resolved, classification = _resolve_local_target(
            target, document, repository
        )
        if classification:
            issues.append(
                Issue(
                    classification,
                    f"{document.path}: unsupported local target {target}",
                )
            )
            continue
        if resolved is None:
            parsed = urlsplit(target.strip())
            if parsed.fragment and not parsed.path and not parsed.scheme:
                continue
            if parsed.scheme.lower() in _EXTERNAL_SCHEMES or parsed.netloc:
                canonical.add(f"url:{target.strip()}")
            continue

        if resolved in selected_paths:
            continue
        exact_path = _case_sensitive_existing_path(resolved, repository)
        if exact_path is None and resolved.is_file():
            issues.append(
                Issue(
                    "case-sensitive-target-mismatch",
                    f"{document.path}: target casing does not match {target}",
                )
            )
        elif exact_path is None or not exact_path.is_file():
            issues.append(
                Issue(
                    "missing-local-target",
                    f"{document.path}: missing local target {target}",
                )
            )
        relative = resolved.relative_to(repository).as_posix()
        canonical.add(f"path:{relative}")
    return canonical


def audit_documents(
    repo: Path,
    documents: Sequence[DocumentSpec],
    default_locale: str,
    require_locale_links: bool,
) -> AuditReport:
    """Audit selected documents for deterministic cross-locale parity."""
    repository = _repository_path(Path(repo))
    if not documents:
        raise ValueError("at least one document is required")
    normalized_default = normalize_locale(default_locale)
    by_locale = {document.locale: document for document in documents}
    if normalized_default not in by_locale:
        raise ValueError(
            f"default locale {normalized_default} is not among selected documents"
        )

    selected_paths = {document.path.resolve() for document in documents}
    snapshots: dict[str, _MarkdownSnapshot] = {}
    issues: list[Issue] = []

    for document in documents:
        try:
            text = document.path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            issues.append(
                Issue(
                    "document-not-utf8",
                    f"{document.path}: cannot decode as UTF-8 ({exc})",
                )
            )
            continue

        snapshot = _extract_targets(text)
        snapshots[document.locale] = snapshot
        if snapshot.unclosed_fence:
            issues.append(
                Issue(
                    "unclosed-code-fence",
                    f"{document.path}: an opening code fence is not closed",
                )
            )

    default_snapshot = snapshots.get(normalized_default)
    if default_snapshot is None:
        return AuditReport(
            repository=repository,
            documents=tuple(documents),
            issues=tuple(issues),
            manual_review=(
                "Perform a manual semantic review of translation completeness and naturalness.",
            ),
        )

    canonical_by_locale: dict[str, tuple[set[str], set[str]]] = {}
    for document in documents:
        snapshot = snapshots.get(document.locale)
        if snapshot is None:
            continue
        if snapshot.heading_levels != default_snapshot.heading_levels:
            issues.append(
                Issue(
                    "heading-structure-mismatch",
                    f"{document.path}: heading levels differ from "
                    f"{by_locale[normalized_default].path}",
                )
            )
        if snapshot.fence_languages != default_snapshot.fence_languages:
            issues.append(
                Issue(
                    "code-fence-mismatch",
                    f"{document.path}: code-fence languages or count differ from "
                    f"{by_locale[normalized_default].path}",
                )
            )

        link_targets = _canonical_targets(
            snapshot.links, document, repository, selected_paths, issues
        )
        image_targets = _canonical_targets(
            snapshot.images, document, repository, selected_paths, issues
        )
        canonical_by_locale[document.locale] = (link_targets, image_targets)

    default_links, default_images = canonical_by_locale.get(
        normalized_default, (set(), set())
    )
    for locale, (links, images) in canonical_by_locale.items():
        if locale == normalized_default:
            continue
        if links != default_links:
            issues.append(
                Issue(
                    "content-link-mismatch",
                    f"{by_locale[locale].path}: non-locale link targets differ from "
                    f"{by_locale[normalized_default].path}",
                )
            )
        if images != default_images:
            issues.append(
                Issue(
                    "content-image-mismatch",
                    f"{by_locale[locale].path}: image targets differ from "
                    f"{by_locale[normalized_default].path}",
                )
            )

    if require_locale_links:
        for document in documents:
            snapshot = snapshots.get(document.locale)
            if snapshot is None:
                continue
            linked_paths: set[Path] = set()
            for target in snapshot.links:
                resolved, classification = _resolve_local_target(
                    target, document, repository
                )
                if resolved is not None and classification is None:
                    linked_paths.add(resolved)
            for other in documents:
                if other.locale == document.locale:
                    continue
                if other.path.resolve() not in linked_paths:
                    relative = other.path.relative_to(repository).as_posix()
                    issues.append(
                        Issue(
                            "locale-link-missing",
                            f"{document.path}: no link to locale {other.locale} "
                            f"({relative})",
                        )
                    )

    return AuditReport(
        repository=repository,
        documents=tuple(documents),
        issues=tuple(issues),
        manual_review=(
            "Perform a manual semantic review of translation completeness and naturalness.",
        ),
    )


def audit_metadata(path: Path) -> tuple[Issue, ...]:
    """Validate an optional local description/topics JSON snapshot."""
    metadata_path = _repository_path(Path(path))
    issues: list[Issue] = []
    try:
        payload: Any = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return (Issue("metadata-invalid-json", f"{metadata_path}: {exc}"),)

    if not isinstance(payload, dict):
        return (
            Issue(
                "metadata-root-not-object",
                f"{metadata_path}: metadata snapshot must be a JSON object",
            ),
        )

    supported = False
    if "description" in payload:
        supported = True
        description = payload["description"]
        if not isinstance(description, str):
            issues.append(
                Issue(
                    "metadata-description-not-string",
                    f"{metadata_path}: description must be a string",
                )
            )
        elif not description.strip():
            issues.append(
                Issue(
                    "metadata-description-empty",
                    f"{metadata_path}: description must not be empty",
                )
            )
        elif "\n" in description or "\r" in description:
            issues.append(
                Issue(
                    "metadata-description-multiline",
                    f"{metadata_path}: description must be a single line",
                )
            )

    if "topics" in payload:
        supported = True
        topics = payload["topics"]
        if not isinstance(topics, list):
            issues.append(
                Issue(
                    "metadata-topics-not-list",
                    f"{metadata_path}: topics must be a list",
                )
            )
        else:
            seen: set[str] = set()
            for topic in topics:
                topic_key = topic.casefold() if isinstance(topic, str) else None
                if topic_key is not None and topic_key in seen:
                    issues.append(
                        Issue(
                            "metadata-topics-duplicate",
                            f"{metadata_path}: duplicate topic {topic!r}",
                        )
                    )
                if topic_key is not None:
                    seen.add(topic_key)
                if not isinstance(topic, str) or not _TOPIC_RE.fullmatch(topic):
                    issues.append(
                        Issue(
                            "metadata-topic-invalid",
                            f"{metadata_path}: invalid topic {topic!r}",
                        )
                    )
                    continue

    if not supported:
        issues.append(
            Issue(
                "metadata-no-supported-fields",
                f"{metadata_path}: expected description or topics",
            )
        )
    return tuple(issues)


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ValueError(message)


def _build_parser() -> argparse.ArgumentParser:
    parser = _ArgumentParser(
        description="Audit selected repository documents for locale parity."
    )
    parser.add_argument("repo", type=Path, help="repository root")
    parser.add_argument(
        "--document",
        action="append",
        required=True,
        metavar="LOCALE=PATH",
        help="selected document mapping; repeat once per locale",
    )
    parser.add_argument(
        "--default-locale",
        default="en",
        help="default locale, default: en",
    )
    parser.add_argument(
        "--require-locale-links",
        action="store_true",
        help="require every selected document to link to every other locale",
    )
    parser.add_argument(
        "--metadata",
        type=Path,
        help="optional local JSON snapshot with description and topics",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="output format, default: text",
    )
    return parser


def _report_with_metadata(
    report: AuditReport, metadata_issues: Sequence[Issue]
) -> AuditReport:
    return AuditReport(
        repository=report.repository,
        documents=report.documents,
        issues=report.issues + tuple(metadata_issues),
        manual_review=report.manual_review,
    )


def _print_report(report: AuditReport, output_format: str) -> None:
    if output_format == "json":
        payload = {
            "ok": report.ok,
            "repository": str(report.repository),
            "documents": [
                {
                    "locale": document.locale,
                    "path": document.path.relative_to(report.repository).as_posix(),
                }
                for document in report.documents
            ],
            "issues": [asdict(issue) for issue in report.issues],
            "manual_review": list(report.manual_review),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print(f"Repository: {report.repository}")
    print("Documents:")
    for document in report.documents:
        relative = document.path.relative_to(report.repository).as_posix()
        print(f"- {document.locale}: {relative}")
    if report.issues:
        print("Deterministic checks: FAILED")
        print("Issues:")
        for issue in report.issues:
            print(f"- [{issue.code}] {issue.message}")
    else:
        print("Deterministic checks: PASSED")
    print("Manual review:")
    for item in report.manual_review:
        print(f"- {item}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    try:
        args = _build_parser().parse_args(argv)
        documents = parse_document_specs(args.document, args.repo)
        report = audit_documents(
            args.repo,
            documents,
            args.default_locale,
            args.require_locale_links,
        )
        if args.metadata is not None:
            report = _report_with_metadata(
                report, audit_metadata(args.metadata)
            )
        _print_report(report, args.format)
        return 1 if report.issues else 0
    except SystemExit:
        raise
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
