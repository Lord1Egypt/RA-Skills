#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


CORE_FILES = ("AGENTS.md", "README.md", "code.md")
LAYERED_DIRS = ("AGENTS", "README", "code")
STATE_FILE = Path(".learnings") / "GOVERNANCE_STATE.json"
TMP_OUTLINE = "tmp.md"
TMP_DIR = "tmp"
LEGACY_CANDIDATES = (
    "tmp.md",
    "tmp",
    "docs",
    "doc",
    "documentation",
    "notes",
    "plan",
    "plans",
    "work",
    "tasks",
    "specs",
    "design",
    "adr",
    "decisions",
    "handoff",
    ".cursor/rules",
    ".cursor",
    ".cursorrules",
    ".continue",
    ".github",
    "CLAUDE.md",
    "GEMINI.md",
    "CONTRIBUTING.md",
    "RULES.md",
    "PROJECT.md",
    "TODO.md",
    "CHANGELOG.md",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect whether a project already has project-management governance scaffold."
    )
    parser.add_argument("--root", default=".", help="Project root to inspect.")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. Default: text.",
    )
    return parser.parse_args()


def load_marker(path: Path) -> dict[str, object]:
    if not path.exists() or not path.is_file():
        return {"exists": False, "valid": False, "initialized": False, "profile": None}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "exists": True,
            "valid": False,
            "initialized": False,
            "profile": None,
            "error": str(exc),
        }

    if not isinstance(data, dict):
        return {"exists": True, "valid": False, "initialized": False, "profile": None, "error": "state must be a JSON object"}
    payload = data.get("project_management_governance", data)
    if not isinstance(payload, dict):
        payload = {}
    return {
        "exists": True,
        "valid": True,
        "initialized": bool(payload.get("initialized") or payload.get("governance_initialized")),
        "profile": payload.get("profile"),
    }


def detect(root: Path) -> dict[str, object]:
    present_core = [name for name in CORE_FILES if (root / name).is_file()]
    missing_core = [name for name in CORE_FILES if name not in present_core]
    learnings_dir = root / ".learnings"
    tmp_outline = root / TMP_OUTLINE
    tmp_dir = root / TMP_DIR
    layered_dirs = [name for name in LAYERED_DIRS if (root / name).is_dir()]
    legacy_candidates = [name for name in LEGACY_CANDIDATES if (root / name).exists()]
    marker = load_marker(root / STATE_FILE)

    has_all_core = len(present_core) == len(CORE_FILES)
    has_learnings = learnings_dir.is_dir()

    if marker["initialized"] or (has_all_core and has_learnings):
        status = "initialized"
        recommended_action = "use_existing_governance_workflow"
    elif present_core or has_learnings or layered_dirs or legacy_candidates:
        status = "partial"
        recommended_action = "inspect_existing_structure_and_adapt_only_if_requested"
    else:
        status = "uninitialized"
        recommended_action = "initialize_only_if_requested"

    if marker.get("profile"):
        profile_hint = marker["profile"]
    elif len(layered_dirs) == len(LAYERED_DIRS):
        profile_hint = "layered"
    elif has_all_core:
        profile_hint = "lightweight"
    elif has_learnings:
        profile_hint = "memory-only"
    else:
        profile_hint = None

    return {
        "root": str(root),
        "status": status,
        "recommended_action": recommended_action,
        "profile_hint": profile_hint,
        "state_file": {
            "path": str(root / STATE_FILE),
            **marker,
        },
        "present_core_files": present_core,
        "missing_core_files": missing_core,
        "learnings_dir": {
            "path": str(learnings_dir),
            "exists": has_learnings,
        },
        "memory_layer": {
            "outline_path": str(tmp_outline),
            "outline_exists": tmp_outline.is_file(),
            "daily_dir_path": str(tmp_dir),
            "daily_dir_exists": tmp_dir.is_dir(),
            "daily_markdown_count": len(list(tmp_dir.glob("*.md"))) if tmp_dir.is_dir() else 0,
        },
        "present_layered_dirs": layered_dirs,
        "missing_layered_dirs": [name for name in LAYERED_DIRS if name not in layered_dirs],
        "legacy_scaffold_candidates": legacy_candidates,
    }


def emit_text(result: dict[str, object]) -> None:
    print(f"Project root: {result['root']}")
    print(f"Governance status: {result['status']}")
    print(f"Recommended action: {result['recommended_action']}")
    print(f"Profile hint: {result['profile_hint'] or '-'}")
    print(f"Present core files: {', '.join(result['present_core_files']) or '-'}")
    print(f"Missing core files: {', '.join(result['missing_core_files']) or '-'}")
    print(f".learnings exists: {result['learnings_dir']['exists']}")
    print(f"tmp.md exists: {result['memory_layer']['outline_exists']}")
    print(f"tmp/ exists: {result['memory_layer']['daily_dir_exists']}")
    print(f"State file exists: {result['state_file']['exists']}")
    print(f"Legacy scaffold candidates: {', '.join(result['legacy_scaffold_candidates']) or '-'}")


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"Project root does not exist or is not a directory: {root}", file=sys.stderr)
        return 2
    result = detect(root)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        emit_text(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
