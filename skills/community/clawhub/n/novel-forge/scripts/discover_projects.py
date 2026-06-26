#!/usr/bin/env python3
"""Discover candidate Novel Forge projects in the workspace.

Prints compact JSON to stdout with project roots that contain a project.json.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

WORKSPACE_ENV_VARS = ("OPENCLAW_WORKSPACE", "NOVEL_FORGE_WORKSPACE", "CLAUDE_WORKSPACE")


def resolve_workspace() -> Path:
    for env_name in WORKSPACE_ENV_VARS:
        raw = os.getenv(env_name, "").strip()
        if raw:
            return Path(raw).expanduser().resolve()
    for candidate in (Path.home() / ".openclaw/workspace", Path.home() / ".claude/workspace"):
        if candidate.exists():
            return candidate.resolve()
    return (Path.home() / ".openclaw/workspace").resolve()


def build_search_roots(workspace: Path) -> list[Path]:
    return [workspace / "novel"]


def safe_read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8")), ""
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def summarize_project(project_json: Path):
    data, load_error = safe_read_json(project_json)
    state_json = project_json.parent / "state" / "current.json"
    has_state_snapshot = state_json.exists()
    if not isinstance(data, dict):
        return {
            "root": str(project_json.parent),
            "projectJson": str(project_json),
            "title": "",
            "genre": "",
            "audience": "",
            "status": "",
            "latestChapterIndex": None,
            "resumeFrom": "",
            "resumeMode": "",
            "lastCheckpoint": "",
            "targetChapters": None,
            "chapterWordRange": [],
            "executionMode": "",
            "bootstrapLocked": None,
            "hasOutline": False,
            "hasCurrentBeat": False,
            "partialDraftCount": 0,
            "hasRecentSummaries": False,
            "hasRecoverySummary": False,
            "hasStateSnapshot": has_state_snapshot,
            "modelRoles": [],
            "modelAssignments": {},
            "loadError": load_error,
        }
    project = data.get("project", {}) if isinstance(data.get("project", {}), dict) else {}
    memory = data.get("memory", {}) if isinstance(data.get("memory", {}), dict) else {}
    planning = data.get("planning", {}) if isinstance(data.get("planning", {}), dict) else {}
    models = data.get("models", {}) if isinstance(data.get("models", {}), dict) else {}
    explicit_models = {k: v for k, v in models.items() if isinstance(v, str) and v and v != "n/a"}
    partial_drafts = planning.get("partialDrafts", []) if isinstance(planning.get("partialDrafts", []), list) else []
    current_beat = planning.get("currentBeat", {}) if isinstance(planning.get("currentBeat", {}), dict) else {}
    chapter_word_range = project.get("chapterWordRange", [])
    if not isinstance(chapter_word_range, list):
        chapter_word_range = []
    return {
        "root": str(project_json.parent),
        "projectJson": str(project_json),
        "title": project.get("title", ""),
        "genre": project.get("genre", ""),
        "audience": project.get("audience", ""),
        "status": project.get("status", ""),
        "latestChapterIndex": project.get("latestChapterIndex", None),
        "resumeFrom": project.get("resumeFrom", ""),
        "resumeMode": project.get("resumeMode", ""),
        "lastCheckpoint": project.get("lastCheckpoint", ""),
        "targetChapters": project.get("targetChapters", None),
        "chapterWordRange": chapter_word_range,
        "executionMode": project.get("executionMode", ""),
        "bootstrapLocked": project.get("bootstrapLocked", None),
        "hasOutline": bool(planning.get("outline")),
        "hasCurrentBeat": bool(current_beat),
        "partialDraftCount": len(partial_drafts),
        "hasRecentSummaries": bool(memory.get("recentSummaries")),
        "hasRecoverySummary": bool(memory.get("recoverySummary")),
        "hasStateSnapshot": has_state_snapshot,
        "modelRoles": sorted(explicit_models.keys()),
        "modelAssignments": explicit_models,
        "loadError": load_error,
    }


def main() -> int:
    workspace = resolve_workspace()
    search_roots = build_search_roots(workspace)
    seen = set()
    projects = []
    for root in search_roots:
        if not root.exists():
            continue
        for pj in root.rglob("project.json"):
            if pj in seen:
                continue
            seen.add(pj)
            summary = summarize_project(pj)
            if summary:
                projects.append(summary)
    projects.sort(key=lambda x: (x.get("loadError", "") != "", x["title"] or "", x["root"]))
    print(json.dumps({"workspace": str(workspace), "projects": projects}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
