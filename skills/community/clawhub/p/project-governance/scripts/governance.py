#!/usr/bin/env python3
"""Project governance workspace scaffold & registry validator.

Subcommands:
  init      Create AGENTS.md, index.md, LESSONS.md, session_handoff.md,
            CHANGELOG.md, VERSIONS.md, blacklist.json, whitelist.json,
            index_notes.json from templates/.
  validate  Check that blacklist.json / whitelist.json conform to the schema.
  index     Refresh the directory-map section of index.md from a filesystem
            scan, with clickable links and optional short notes from
            index_notes.json.
  check     Verify the governance workspace is complete, valid, and the index
            is up to date.

The script is deterministic and idempotent: it never overwrites existing files
unless --force is passed.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

TEMPLATE_FILES = [
    "AGENTS.md",
    "ARCHITECTURE.md",
    "PROJECT.md",
    "index.md",
    "index_notes.json",
    "LESSONS.md",
    "session_handoff.md",
    "CHANGELOG.md",
    "VERSIONS.md",
    "blacklist.json",
    "whitelist.json",
]

# Files that must exist for a governance workspace to be usable.
CORE_REQUIRED_FILES = [
    "AGENTS.md",
    "index.md",
    "session_handoff.md",
    "LESSONS.md",
    "CHANGELOG.md",
    "VERSIONS.md",
    "blacklist.json",
    "whitelist.json",
]

# Only placeholders that can be auto-filled are substituted; the rest stay
# as {{PLACEHOLDER}} for the user to fill in.
AUTO_PLACEHOLDERS = {
    "{{PROJECT_NAME}}": "My Project",
    "{{PROJECT_ROOT}}": ".",
    "{{DATE}}": date.today().isoformat(),
    "{{CHANGES}}": "Initial scaffold.",
}

SKIP_DIRS = {
    ".git", ".hg", ".svn", "__pycache__", ".pytest_cache", ".mypy_cache",
    "node_modules", ".venv", "venv", ".idea", ".vscode", "dist", "build",
}

BLACKLIST_REQUIRED = ["id", "reason", "permanent_ban", "alternative", "test_ref", "judge", "scope", "status"]
WHITELIST_REQUIRED = ["id", "score", "config", "test_ref", "judge", "last_verified", "scope", "status"]
VALID_STATUS = {"active", "superseded", "deprecated"}
VALID_JUDGE = {"ai", "human"}

DEFAULT_ROOT_SECTION = "## Root layout"
DEFAULT_CHANGELOG_SECTION = "## Change log"
DEFAULT_MAX_NOTE_LENGTH = 60


def _templates_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "templates"


def cmd_init(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_dir).resolve()
    if project_dir.exists() and not project_dir.is_dir():
        print(f"ERROR: project directory path is an existing file: {project_dir}")
        return 1
    project_dir.mkdir(parents=True, exist_ok=True)
    templates = _templates_dir()
    if not templates.is_dir():
        print(f"ERROR: templates directory not found: {templates}")
        print("HINT: keep templates/ next to scripts/ when copying this skill.")
        return 1

    if getattr(args, "project_name", None):
        AUTO_PLACEHOLDERS["{{PROJECT_NAME}}"] = args.project_name

    created, skipped = [], []
    for name in TEMPLATE_FILES:
        dst = project_dir / name
        if dst.is_dir():
            print(f"ERROR: target path is a directory, not a file: {dst}")
            return 1
        if dst.exists() and not args.force:
            skipped.append(name)
            continue
        src = templates / name
        if not src.exists():
            print(f"ERROR: template missing: {src}")
            return 1
        text = src.read_text(encoding="utf-8")
        for key, value in AUTO_PLACEHOLDERS.items():
            text = text.replace(key, value)
        dst.write_text(text, encoding="utf-8")
        created.append(name)

    print(f"Created {len(created)} governance files in {project_dir}")
    for name in created:
        print(f"  + {name}")
    if skipped:
        print(f"Skipped {len(skipped)} existing files (use --force to overwrite):")
        for name in skipped:
            print(f"  = {name}")
    return 0


def _validate_registry(path: Path, required: list[str], label: str, relaxed: bool = False) -> list[str]:
    errors = []
    if not path.exists():
        errors.append(f"{label}: file not found: {path}")
        return errors
    if not path.is_file():
        errors.append(f"{label}: not a regular file: {path}")
        return errors
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError as exc:
        errors.append(f"{label}: file is not valid UTF-8 text: {exc}")
        return errors
    except json.JSONDecodeError as exc:
        errors.append(f"{label}: invalid JSON at line {exc.lineno}: {exc.msg}")
        return errors
    if not isinstance(data, dict):
        errors.append(f"{label}: top-level JSON must be an object, got {type(data).__name__}")
        return errors

    entries = data.get(label)
    if not isinstance(entries, list):
        errors.append(f"{label}: top-level '{label}' must be a list")
        return errors

    seen_ids = set()
    for idx, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"{label}[{idx}]: entry must be an object")
            continue
        if not relaxed:
            missing = [f for f in required if f not in entry]
            if missing:
                errors.append(f"{label}[{idx}]: missing required fields: {', '.join(missing)}")
        if "id" in entry:
            if not isinstance(entry["id"], str):
                errors.append(f"{label}[{idx}]: id must be a string, got {entry['id']!r}")
            elif entry["id"] in seen_ids:
                errors.append(f"{label}[{idx}]: duplicate id '{entry['id']}'")
            else:
                seen_ids.add(entry["id"])
        if "status" in entry and entry["status"] not in VALID_STATUS:
            errors.append(f"{label}[{idx}]: invalid status '{entry['status']}' (valid: {sorted(VALID_STATUS)})")
        if "judge" in entry and entry["judge"] not in VALID_JUDGE:
            errors.append(f"{label}[{idx}]: invalid judge '{entry['judge']}' (valid: {sorted(VALID_JUDGE)})")
        if label == "blacklist" and "permanent_ban" in entry and not isinstance(entry["permanent_ban"], bool):
            errors.append(f"{label}[{idx}]: permanent_ban must be a boolean, got {entry['permanent_ban']!r}")
        if label == "whitelist" and "score" in entry:
            score = entry["score"]
            if isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= score <= 1:
                errors.append(f"{label}[{idx}]: score must be a number in [0, 1], got {score!r}")
    return errors


def cmd_validate(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_dir).resolve()
    relaxed = getattr(args, "relaxed", False)
    errors = []
    errors += _validate_registry(project_dir / "blacklist.json", BLACKLIST_REQUIRED, "blacklist", relaxed)
    errors += _validate_registry(project_dir / "whitelist.json", WHITELIST_REQUIRED, "whitelist", relaxed)
    if errors:
        print("VALIDATION FAILED:")
        for err in errors:
            print(f"  - {err}")
        return 1
    mode = "relaxed " if relaxed else ""
    print(f"VALIDATION PASSED: blacklist.json and whitelist.json conform to the {mode}schema.")
    return 0


def _find_heading_line(text: str, heading: str) -> int:
    """Return the 0-based line index of the first heading equal to `heading`
    that is NOT inside a fenced code block, or -1 if not found."""
    lines = text.splitlines()
    in_fence = False
    fence_char = ""
    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith("```") or s.startswith("~~~"):
            ch = s[0]
            if in_fence and ch == fence_char:
                in_fence = False
                fence_char = ""
            elif not in_fence:
                in_fence = True
                fence_char = ch
            continue
        if in_fence:
            continue
        if s == heading or s.startswith(heading + " "):
            return i
    return -1


def _link_target(rel: str) -> str:
    """Wrap a relative path in angle brackets when it contains characters that
    would break a bare markdown link (spaces, parens, angle brackets)."""
    if any(c in rel for c in " <>()"):
        return f"<{rel}>"
    return rel


def _load_notes(project_dir: Path) -> dict[str, str]:
    """Read index_notes.json into {rel_path: note}. Returns {} on any problem
    and prints a warning so the index command can degrade gracefully."""
    notes_path = project_dir / "index_notes.json"
    if not notes_path.exists():
        return {}
    if not notes_path.is_file():
        print("WARNING: index_notes.json is not a regular file; ignoring notes.")
        return {}
    try:
        data = json.loads(notes_path.read_text(encoding="utf-8"))
    except UnicodeDecodeError as exc:
        print(f"WARNING: index_notes.json is not valid UTF-8 ({exc}); ignoring notes.")
        return {}
    except json.JSONDecodeError as exc:
        print(f"WARNING: index_notes.json is invalid JSON at line {exc.lineno} ({exc.msg}); ignoring notes.")
        return {}
    if not isinstance(data, dict):
        print("WARNING: index_notes.json top-level must be an object; ignoring notes.")
        return {}
    return {str(k): str(v) for k, v in data.items() if isinstance(v, str)}


def _build_tree(root: Path, max_depth: int, notes: dict[str, str] | None = None,
                max_note_length: int = DEFAULT_MAX_NOTE_LENGTH) -> list[str]:
    notes = notes or {}
    lines = []

    def walk(path: Path, prefix: str, depth: int) -> None:
        if depth > max_depth:
            lines.append(f"{prefix}└── ...")
            return
        try:
            entries = sorted(
                (p for p in path.iterdir() if p.name not in SKIP_DIRS and not p.name.startswith(".")),
                key=lambda p: (p.is_file(), p.name.lower()),
            )
        except OSError:
            lines.append(f"{prefix}└── <unreadable>")
            return
        for i, entry in enumerate(entries):
            last = i == len(entries) - 1
            connector = "└── " if last else "├── "
            rel = entry.relative_to(root).as_posix()
            name = entry.name + ("/" if entry.is_dir() else "")
            line = f"{prefix}{connector}[{name}]({_link_target(rel)})"
            note = notes.get(rel) or notes.get(rel + "/")
            if note:
                if len(note) > max_note_length:
                    note = note[:max_note_length] + "…"
                line += f" — {note}"
            lines.append(line)
            if entry.is_dir():
                walk(entry, prefix + ("    " if last else "│   "), depth + 1)

    walk(root, "", 0)
    return lines


def _extract_fenced_block(text: str, start: int, end: int) -> str | None:
    """Return the content of the first fenced code block within lines
    [start, end), or None if no complete block is found."""
    lines = text.splitlines()
    content: list[str] = []
    in_block = False
    for i in range(start, end):
        s = lines[i].strip()
        if s.startswith("```"):
            if not in_block:
                in_block = True
            else:
                return "\n".join(content)
            continue
        if in_block:
            content.append(lines[i])
    return None


def _is_index_fresh(project_dir: Path, index_path: Path, args: argparse.Namespace) -> bool:
    try:
        text = index_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    root_section = getattr(args, "root_section", DEFAULT_ROOT_SECTION)
    changelog_section = getattr(args, "changelog_section", DEFAULT_CHANGELOG_SECTION)
    start = _find_heading_line(text, root_section)
    end = _find_heading_line(text, changelog_section)
    if start == -1 or end == -1 or end <= start:
        return False
    block = _extract_fenced_block(text, start, end)
    if block is None:
        return False
    notes = _load_notes(project_dir)
    tree = _build_tree(project_dir, getattr(args, "max_depth", 4), notes,
                       getattr(args, "max_note_length", DEFAULT_MAX_NOTE_LENGTH))
    return block == "\n".join(tree)


def cmd_index(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_dir).resolve()
    index_path = project_dir / "index.md"
    if not index_path.exists():
        print(f"ERROR: index.md not found: {index_path}")
        print("HINT: run 'governance.py init' first to scaffold the workspace.")
        return 1
    if not index_path.is_file():
        print(f"ERROR: index.md is not a regular file: {index_path}")
        return 1

    root_section = getattr(args, "root_section", DEFAULT_ROOT_SECTION)
    changelog_section = getattr(args, "changelog_section", DEFAULT_CHANGELOG_SECTION)
    notes = _load_notes(project_dir)
    tree = _build_tree(project_dir, args.max_depth, notes,
                       getattr(args, "max_note_length", DEFAULT_MAX_NOTE_LENGTH))
    section = f"{root_section}\n```\n" + "\n".join(tree) + "\n```\n"

    try:
        text = index_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        print(f"ERROR: index.md is not valid UTF-8 text: {exc}")
        return 1
    start = _find_heading_line(text, root_section)
    end = _find_heading_line(text, changelog_section)
    if start == -1 or end == -1 or end <= start:
        print(f"ERROR: index.md must contain '{root_section}' before '{changelog_section}' sections.")
        return 1
    lines = text.splitlines(keepends=True)
    new_text = "".join(lines[:start]) + section + "".join(lines[end:])
    index_path.write_text(new_text, encoding="utf-8")
    print(f"Updated '{root_section}' in {index_path} ({len(tree)} lines).")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    project_dir = Path(args.project_dir).resolve()
    errors = []

    for f in CORE_REQUIRED_FILES:
        p = project_dir / f
        if not p.exists():
            errors.append(f"missing required file: {f}")
        elif not p.is_file():
            errors.append(f"required path is not a regular file: {f}")

    errors += _validate_registry(project_dir / "blacklist.json", BLACKLIST_REQUIRED, "blacklist")
    errors += _validate_registry(project_dir / "whitelist.json", WHITELIST_REQUIRED, "whitelist")

    notes_path = project_dir / "index_notes.json"
    if notes_path.exists():
        if not notes_path.is_file():
            errors.append("index_notes.json is not a regular file")
        else:
            try:
                data = json.loads(notes_path.read_text(encoding="utf-8"))
                if not isinstance(data, dict):
                    errors.append("index_notes.json: top-level must be an object")
            except UnicodeDecodeError as exc:
                errors.append(f"index_notes.json: not valid UTF-8: {exc}")
            except json.JSONDecodeError as exc:
                errors.append(f"index_notes.json: invalid JSON at line {exc.lineno}: {exc.msg}")

    index_path = project_dir / "index.md"
    if index_path.is_file() and not _is_index_fresh(project_dir, index_path, args):
        errors.append("index.md is outdated (run 'governance.py index' to update)")

    if errors:
        print("CHECK FAILED:")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("CHECK PASSED: governance workspace is complete, valid, and up-to-date.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="scaffold the governance workspace from templates")
    p_init.add_argument("--project-dir", required=True, help="target project directory")
    p_init.add_argument("--project-name", default="My Project", help="project name (default: My Project)")
    p_init.add_argument("--force", action="store_true", help="overwrite existing files")
    p_init.set_defaults(func=cmd_init)

    p_val = sub.add_parser("validate", help="validate blacklist.json / whitelist.json schema")
    p_val.add_argument("--project-dir", required=True, help="project directory containing the registries")
    p_val.add_argument("--relaxed", action="store_true",
                       help="do not fail on missing optional fields (eases migration of older registries)")
    p_val.set_defaults(func=cmd_validate)

    p_idx = sub.add_parser("index", help="refresh the directory-map section of index.md")
    p_idx.add_argument("--project-dir", required=True, help="project directory containing index.md")
    p_idx.add_argument("--max-depth", type=int, default=4, help="max tree depth (default: 4)")
    p_idx.add_argument("--root-section", default=DEFAULT_ROOT_SECTION,
                       help=f"index section heading to replace (default: '{DEFAULT_ROOT_SECTION}')")
    p_idx.add_argument("--changelog-section", default=DEFAULT_CHANGELOG_SECTION,
                       help=f"section heading that ends the map (default: '{DEFAULT_CHANGELOG_SECTION}')")
    p_idx.add_argument("--max-note-length", type=int, default=DEFAULT_MAX_NOTE_LENGTH,
                       help="max length of index_notes.json notes before truncation (default: 60)")
    p_idx.set_defaults(func=cmd_index)

    p_chk = sub.add_parser("check", help="verify the governance workspace is complete, valid, and up-to-date")
    p_chk.add_argument("--project-dir", required=True, help="project directory to check")
    p_chk.add_argument("--max-depth", type=int, default=4, help="max tree depth used for freshness check (default: 4)")
    p_chk.add_argument("--root-section", default=DEFAULT_ROOT_SECTION,
                       help=f"index section heading to check (default: '{DEFAULT_ROOT_SECTION}')")
    p_chk.add_argument("--changelog-section", default=DEFAULT_CHANGELOG_SECTION,
                       help=f"section heading that ends the map (default: '{DEFAULT_CHANGELOG_SECTION}')")
    p_chk.add_argument("--max-note-length", type=int, default=DEFAULT_MAX_NOTE_LENGTH,
                       help="max note length used for freshness check (default: 60)")
    p_chk.set_defaults(func=cmd_check)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: unexpected failure: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
