#!/usr/bin/env python3
"""Fail closed when a public artifact leaks another registered client name."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from client_registry import resolve_client_registry


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = resolve_client_registry(ROOT)
TEXT_SUFFIXES = {".md", ".html", ".htm", ".txt", ".json", ".csv", ".xml"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", action="append", default=[], required=True)
    parser.add_argument("--allowed-term", action="append", default=[])
    parser.add_argument("--forbidden-term", action="append", default=[])
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    parser.add_argument("--output", help="Write an immutable-style pass receipt with artifact hashes")
    parser.add_argument("--team-version", help="生成该公域检查回执的专家团版本；写回执时必填")
    return parser.parse_args()


def normalize(value: str) -> str:
    return re.sub(r"\s+", "", value).casefold()


def term_token(term: str) -> str:
    return hashlib.sha256(normalize(term).encode("utf-8")).hexdigest()[:12]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_registry(path: Path) -> list[str]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    terms = payload.get("registered_client_terms", [])
    if not isinstance(terms, list) or not all(isinstance(item, str) and item.strip() for item in terms):
        raise ValueError("client brand registry is invalid")
    return terms


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in TEXT_SUFFIXES:
        return path.read_text(encoding="utf-8-sig", errors="strict")
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("PDF text extractor unavailable") from exc
        return "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
    raise RuntimeError(f"unsupported public artifact suffix: {suffix or '<none>'}")


def main() -> int:
    args = parse_args()
    registry_path = Path(args.registry).expanduser().resolve()
    registered = load_registry(registry_path)
    allowed = {normalize(item) for item in args.allowed_term if item.strip()}
    forbidden = [item for item in [*registered, *args.forbidden_term] if normalize(item) not in allowed]

    findings: list[dict[str, str]] = []
    scanned: list[str] = []
    artifacts: list[dict[str, str | int]] = []
    for raw_path in args.file:
        path = Path(raw_path).expanduser().resolve()
        if not path.is_file():
            print(json.dumps({"status": "client_scope_leak_blocked", "reason": "artifact_missing", "file": path.name}, ensure_ascii=False))
            return 2
        try:
            normalized_text = normalize(extract_text(path))
        except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
            print(json.dumps({"status": "client_scope_leak_blocked", "reason": type(exc).__name__, "file": path.name}, ensure_ascii=False))
            return 2
        scanned.append(path.name)
        artifacts.append({"file": path.name, "sha256": file_sha256(path), "bytes": path.stat().st_size})
        for term in forbidden:
            if normalize(term) in normalized_text:
                findings.append({"file": path.name, "term_token": term_token(term)})

    if findings:
        print(json.dumps({
            "status": "client_scope_leak_blocked",
            "finding_count": len(findings),
            "findings": findings,
        }, ensure_ascii=False))
        return 2

    if args.output and not args.team_version:
        print(json.dumps({"status": "client_scope_leak_blocked", "reason": "team_version_required"}, ensure_ascii=False))
        return 2
    identity = {}
    if args.output:
        from artifact_contract import native_receipt_identity
        try:
            identity = native_receipt_identity("public_output_guard", args.team_version)
        except ValueError as exc:
            print(json.dumps({"status": "client_scope_leak_blocked", "reason": str(exc)}, ensure_ascii=False))
            return 2
    result = {
        **identity,
        "status": "public_output_guard_passed",
        "scanned": scanned,
        "registered_terms_checked": len(forbidden),
        "artifacts": artifacts,
    }
    if args.output:
        output = Path(args.output).expanduser().resolve()
        if output.exists():
            print(json.dumps({"status": "client_scope_leak_blocked", "reason": "guard_receipt_already_exists", "file": output.name}, ensure_ascii=False))
            return 2
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output"] = output.name
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
