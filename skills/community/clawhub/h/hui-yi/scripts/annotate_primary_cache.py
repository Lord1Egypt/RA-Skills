#!/usr/bin/env python3
"""Append source-bound native trigger metadata to existing primary-memory bullets.

Plan schema: {"files": [{"path": "MEMORY.md" | "USER.md", "expected_sha256":
"<original byte hash>", "entries": [{"line": 1, "line_sha256": "<UTF-8 hash
of the original line without its newline or file BOM>", "triggers": ["phrase"]}]}]}.
Line numbering uses UTF-8-SIG decoded splitlines(). The source bytes, BOM, line
endings, facts, and counters are preserved; only inline HTML comments are added.
Trigger phrases are exact-match retrieval metadata, never authorization or proof
of trust. Preview is the default. All ancestors must satisfy core.safe_fs; this
is not a transaction/lock against arbitrary concurrent editors in trusted dirs.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import secrets
import sys
import unicodedata

SKILL_ROOT = Path(__file__).absolute().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from core.safe_fs import atomic_write_bytes, check_directory, check_file, lexical_path, read_bytes
from scripts.configure_native_memory import protected_backup

ALLOWED_FILES = frozenset({"MEMORY.md", "USER.md"})
MAX_PLAN_BYTES = 64 * 1024
MAX_SOURCE_BYTES = 4 * 1024 * 1024
MAX_ENTRIES = 32
MAX_TRIGGERS = 6
MAX_TRIGGER_CHARS = 64
MAX_ENTRY_TRIGGER_CHARS = 256
_HASH = re.compile(r"^[0-9a-fA-F]{64}$")
_BULLET = re.compile(r"^ {0,3}[-+*][ \t]+\S")
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
_TRIGGER = re.compile(r"<!--\s*triggers?\b", re.IGNORECASE)
_ENDINGS = ("\r\n", "\n", "\r", "\v", "\f", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029")


class AnnotationError(ValueError):
    """Fixed error codes only: never include a source line or trigger phrase."""


@dataclass(frozen=True)
class PreparedFile:
    name: str
    path: Path
    original: bytes
    updated: bytes
    entry_count: int
    trigger_count: int


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def exact_keys(value: object, expected: set[str]) -> dict:
    if not isinstance(value, dict) or set(value) != expected:
        raise AnnotationError("invalid_plan_schema")
    return value


def unique_json_object(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise AnnotationError("duplicate_json_field")
        result[key] = value
    return result


def expected_hash(value: object) -> str:
    if not isinstance(value, str) or not _HASH.fullmatch(value):
        raise AnnotationError("invalid_hash")
    return value.lower()


def split_ending(line: str) -> tuple[str, str]:
    for ending in _ENDINGS:
        if line.endswith(ending):
            return line[:-len(ending)], ending
    return line, ""


def validate_triggers(values: object) -> list[str]:
    if not isinstance(values, list) or not 1 <= len(values) <= MAX_TRIGGERS:
        raise AnnotationError("invalid_trigger_count")
    seen: set[str] = set()
    total = 0
    for value in values:
        if (not isinstance(value, str) or value != value.strip()
                or not 2 <= len(value) <= MAX_TRIGGER_CHARS
                or any(character in value for character in "<>;；|\r\n") or "--" in value
                or any(unicodedata.category(character).startswith("C") or character in "\u2028\u2029" for character in value)):
            raise AnnotationError("invalid_trigger_phrase")
        normalized = unicodedata.normalize("NFKC", value).casefold()
        if normalized in seen:
            raise AnnotationError("duplicate_trigger_phrase")
        seen.add(normalized)
        total += len(value)
    if total > MAX_ENTRY_TRIGGER_CHARS:
        raise AnnotationError("trigger_text_too_long")
    return values


def eligible_bullet_lines(lines: list[str]) -> set[int]:
    eligible: set[int] = set()
    fence: tuple[str, int] | None = None
    comment_open = False
    front_matter = bool(lines and split_ending(lines[0])[0] == "---")
    for number, line in enumerate(lines, 1):
        body, _ = split_ending(line)
        if front_matter:
            if number > 1 and body in {"---", "..."}:
                front_matter = False
            continue
        marker = _FENCE.match(body)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= fence[1] and not marker[2].strip():
                fence = None
            continue
        if marker and not comment_open:
            fence = marker[1][0], len(marker[1])
            continue
        was_comment = comment_open
        cursor = 0
        while cursor < len(body):
            marker_text = "-->" if comment_open else "<!--"
            start = body.find(marker_text, cursor)
            if start < 0:
                break
            comment_open = not comment_open
            cursor = start + len(marker_text)
        if not was_comment and not comment_open and _BULLET.match(body):
            eligible.add(number)
    return eligible


def prepare_file(root: Path, spec: dict) -> PreparedFile:
    exact_keys(spec, {"path", "expected_sha256", "entries"})
    name = spec["path"]
    if not isinstance(name, str) or name not in ALLOWED_FILES:
        raise AnnotationError("unsupported_source_file")
    path = check_file(root / name)
    original = read_bytes(path)
    if len(original) > MAX_SOURCE_BYTES:
        raise AnnotationError("source_too_large")
    if sha256(original) != expected_hash(spec["expected_sha256"]):
        raise AnnotationError("source_hash_mismatch")
    text = original.decode("utf-8-sig")
    bom = b"\xef\xbb\xbf" if original.startswith(b"\xef\xbb\xbf") else b""
    lines = text.splitlines(keepends=True)
    if bom + "".join(lines).encode("utf-8") != original:
        raise AnnotationError("source_encoding_not_preservable")
    entries = spec["entries"]
    if not isinstance(entries, list) or not 1 <= len(entries) <= MAX_ENTRIES:
        raise AnnotationError("invalid_entry_count")
    eligible = eligible_bullet_lines(lines)
    selected: set[int] = set()
    additions: dict[int, str] = {}
    trigger_count = 0
    for entry in entries:
        exact_keys(entry, {"line", "line_sha256", "triggers"})
        number = entry["line"]
        if type(number) is not int or number < 1 or number > len(lines):
            raise AnnotationError("invalid_line_number")
        if number in selected:
            raise AnnotationError("duplicate_line")
        selected.add(number)
        if number not in eligible:
            raise AnnotationError("line_is_not_an_unambiguous_bullet")
        body, _ = split_ending(lines[number - 1])
        if sha256(body.encode("utf-8")) != expected_hash(entry["line_sha256"]):
            raise AnnotationError("line_hash_mismatch")
        # Refuse existing trigger comments on the item or its continuation;
        # never silently merge, replace, or reinterpret pre-existing metadata.
        block = [body]
        for later in lines[number:]:
            if _BULLET.match(later) or later.lstrip().startswith("#"):
                break
            block.append(later)
        if _TRIGGER.search("\n".join(block)):
            raise AnnotationError("existing_trigger_metadata")
        triggers = validate_triggers(entry["triggers"])
        additions[number] = " <!-- trigger: " + "; ".join(triggers) + " -->"
        trigger_count += len(triggers)
    updated_lines = list(lines)
    for number, addition in additions.items():
        body, ending = split_ending(lines[number - 1])
        updated_lines[number - 1] = body + addition + ending
    updated = bom + "".join(updated_lines).encode("utf-8")
    # Verify byte-for-byte preservation after removing only our known additions.
    restored_lines = list(updated_lines)
    for number, addition in additions.items():
        body, ending = split_ending(restored_lines[number - 1])
        if not body.endswith(addition):
            raise AnnotationError("annotation_integrity_error")
        restored_lines[number - 1] = body[:-len(addition)] + ending
    if bom + "".join(restored_lines).encode("utf-8") != original:
        raise AnnotationError("source_preservation_error")
    return PreparedFile(name, path, original, updated, len(entries), trigger_count)


def prepare_plan(workspace_root: Path, plan: object) -> list[PreparedFile]:
    root = check_directory(workspace_root)
    data = exact_keys(plan, {"files"})
    specs = data["files"]
    if not isinstance(specs, list) or not 1 <= len(specs) <= len(ALLOWED_FILES):
        raise AnnotationError("invalid_file_count")
    prepared: list[PreparedFile] = []
    seen: set[str] = set()
    for spec in specs:
        item = prepare_file(root, spec)
        if item.name in seen:
            raise AnnotationError("duplicate_source_file")
        seen.add(item.name)
        prepared.append(item)
    return prepared


def annotate(workspace_root: Path, plan: object, backup_dir: Path, *, apply: bool = False) -> dict:
    prepared = prepare_plan(workspace_root, plan)
    backup_root = check_directory(backup_dir, allow_missing=True)
    report = {"ok": True, "mode": "apply" if apply else "preview", "file_count": len(prepared),
              "entry_count": sum(item.entry_count for item in prepared),
              "trigger_count": sum(item.trigger_count for item in prepared),
              "new_fact_count": 0, "counter_change_count": 0, "written_file_count": 0,
              "files": [{"path": item.name, "original_sha256": sha256(item.original),
                         "updated_sha256": sha256(item.updated), "entry_count": item.entry_count,
                         "trigger_count": item.trigger_count, "backup_path": None} for item in prepared]}
    if not apply:
        return report
    # Prepare every protected backup before changing either original. The
    # helper freezes source permissions on an empty backup before secret bytes.
    for item, record in zip(prepared, report["files"]):
        if read_bytes(item.path) != item.original:
            raise AnnotationError("source_changed_before_backup")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        backup = backup_root / f"{item.path.stem}-before-triggers-{stamp}-{secrets.token_hex(4)}.md"
        protected_backup(item.path, backup, item.original)
        if read_bytes(backup) != item.original:
            raise AnnotationError("backup_integrity_error")
        record["backup_path"] = str(backup)
    for item in prepared:
        if read_bytes(item.path) != item.original:
            raise AnnotationError("source_changed_during_backup")
    for item in prepared:
        if read_bytes(item.path) != item.original:
            raise AnnotationError("source_changed_before_write")
        atomic_write_bytes(item.path, item.updated)
        if read_bytes(item.path) != item.updated:
            raise AnnotationError("source_changed_after_write")
        report["written_file_count"] += 1
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", required=True)
    parser.add_argument("--plan", required=True, help="path to source-bound JSON plan; never prints entries or triggers")
    parser.add_argument("--backup-dir", required=True)
    parser.add_argument("--apply", action="store_true", help="append validated trigger comments after protected backups")
    args = parser.parse_args(argv)
    raw = read_bytes(lexical_path(args.plan))
    if len(raw) > MAX_PLAN_BYTES:
        raise AnnotationError("plan_too_large")
    plan = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_json_object)
    report = annotate(lexical_path(args.workspace_root), plan, lexical_path(args.backup_dir), apply=args.apply)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as error:
        # Some filesystem/JSON/Unicode exceptions include source data; emit
        # only their class, never exception messages or tracebacks.
        print(json.dumps({"ok": False, "error_type": type(error).__name__}), file=sys.stderr)
        raise SystemExit(1)
