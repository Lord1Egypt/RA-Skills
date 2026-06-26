#!/usr/bin/env python3
"""MemHub Skill wrapper.

This file is generated from memhub_cli.__main__ for standalone Skill distribution.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import getpass
import json
import os
import random
import string
import subprocess
import sys
import threading
import time
import webbrowser
import http.server
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required. Install with: pip install pyyaml") from exc

SCHEMA_VERSION = "0.1"


def parse_dotenv_value(value: str) -> str:
    value = value.strip()
    if value and value[0] not in {'\"', "'"} and " #" in value:
        value = value.split(" #", 1)[0].strip()
    if len(value) >= 2 and ((value[0] == value[-1] == '\"') or (value[0] == value[-1] == "'")):
        value = value[1:-1]
    return value


def load_dotenv_files(paths: list[Path]) -> None:
    """Load simple KEY=VALUE lines from .env files without overriding existing env vars.

    This is intentionally tiny and dependency-free. It supports optional leading
    `export`, quoted values, blank lines, and comments. It never prints values.
    """
    seen: set[Path] = set()
    for path in paths:
        path = path.expanduser()
        if path in seen or not path.exists() or not path.is_file():
            continue
        seen.add(path)
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            lines = path.read_text(errors="replace").splitlines()
        for line in lines:
            text = line.strip()
            if not text or text.startswith("#"):
                continue
            if text.startswith("export "):
                text = text[len("export "):].strip()
            if "=" not in text:
                continue
            key, value = text.split("=", 1)
            key = key.strip()
            if not key or key in os.environ:
                continue
            os.environ[key] = parse_dotenv_value(value)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def today_month() -> str:
    return dt.datetime.now().strftime("%Y-%m")


def short_id(n: int = 6) -> str:
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))


def timestamp_id() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def read_yaml(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if data is not None else default


def write_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=1000)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run_git(repo: Path, args: list[str], check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(repo),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def ensure_repo(repo: Path) -> None:
    if not (repo / ".git").exists():
        run_git(repo, ["init"], check=False)


def init_repo(repo: Path, name: str = "user", role: str = "") -> None:
    repo.mkdir(parents=True, exist_ok=True)
    ensure_repo(repo)

    dirs = [
        ".memhub/templates",
        "identity",
        "projects/memhub",
        "knowledge",
        "relations",
        "timeline",
        "inbox",
        "exports",
        "archive",
    ]
    for d in dirs:
        (repo / d).mkdir(parents=True, exist_ok=True)

    config = {
        "schema_version": SCHEMA_VERSION,
        "repo": {"id": "user_main_memhub", "owner": name},
        "sync": {
            "type": "git",
            "remote": None,
            "branch": "main",
            "auto_pull": True,
            "auto_push": True,
            "push_throttle_seconds": 3600,
            "pull_throttle_seconds": 3600,
            "pull_strategy": "rebase",
            "commit_prefix": "memhub:",
        },
        "inbox": {"auto_archive": False, "auto_archive_confidence_threshold": 0.92},
        "context": {"default_pack": "standard", "standard_token_budget": 2000},
    }
    write_yaml(repo / ".memhub/config.yaml", config)
    write_yaml(repo / ".memhub/schema.yaml", {"schema_version": SCHEMA_VERSION, "protocol": "MemHub"})
    write_yaml(repo / ".memhub/state.yaml", {"schema_version": SCHEMA_VERSION, "last_sync_at": None})

    profile = {
        "schema_version": SCHEMA_VERSION,
        "updated_at": now_iso(),
        "profile": {
            "id": "user_main",
            "name": name,
            "display_name": name,
            "language": "zh-CN",
            "timezone": "Asia/Shanghai",
            "role": role,
            "company": None,
            "bio": "",
            "tags": [],
        },
        "communication": {
            "default_language": "zh-CN",
            "preferred_style": "direct_structured",
            "verbosity": "medium",
            "likes": ["结构化输出", "直接回答", "能落地的方案"],
            "dislikes": ["空泛表述", "过度道歉", "没有上下文就假装知道"],
        },
    }
    write_yaml(repo / "identity/profile.yaml", profile)

    preferences = {
        "schema_version": SCHEMA_VERSION,
        "updated_at": now_iso(),
        "preferences": [
            {
                "id": "pref_response_style",
                "type": "preference",
                "status": "active",
                "category": "ai_interaction",
                "key": "response_style",
                "value": "结构化、直接、少废话",
                "content": "用户偏好结构化、直接、少废话的回答风格。",
                "confidence": 0.9,
                "importance": 0.9,
                "source": {"client": "manual"},
                "created_at": now_iso(),
                "updated_at": now_iso(),
            }
        ],
    }
    write_yaml(repo / "identity/preferences.yaml", preferences)
    write_yaml(repo / "identity/conventions.yaml", {"schema_version": SCHEMA_VERSION, "updated_at": now_iso(), "conventions": []})
    write_yaml(repo / "identity/constraints.yaml", {"schema_version": SCHEMA_VERSION, "updated_at": now_iso(), "constraints": []})

    active = {
        "schema_version": SCHEMA_VERSION,
        "updated_at": now_iso(),
        "active_projects": [
            {
                "id": "memhub",
                "name": "MemHub",
                "priority": 1,
                "status": "active",
                "default": True,
                "path": "projects/memhub",
                "description": "跨平台 AI 记忆统一产品。",
            }
        ],
    }
    write_yaml(repo / "projects/_active.yaml", active)
    write_yaml(
        repo / "projects/memhub/context.yaml",
        {
            "schema_version": SCHEMA_VERSION,
            "project": {
                "id": "memhub",
                "name": "MemHub",
                "status": "active",
                "description": "无服务端、Git 同步、Agent Memory Protocol。",
                "goals": ["让多个 AI Agent 共享同一份用户记忆。", "不依赖中心化后端。"],
                "constraints": ["Local-first", "Git-first", "Agent-oriented"],
                "current_phase": "mvp",
                "updated_at": now_iso(),
            },
        },
    )
    write_yaml(repo / "projects/memhub/decisions.yaml", {"schema_version": SCHEMA_VERSION, "project_id": "memhub", "updated_at": now_iso(), "decisions": []})
    write_yaml(repo / "projects/memhub/tasks.yaml", {"schema_version": SCHEMA_VERSION, "project_id": "memhub", "updated_at": now_iso(), "tasks": []})
    write_yaml(repo / "projects/memhub/stack.yaml", {"schema_version": SCHEMA_VERSION, "project_id": "memhub", "updated_at": now_iso(), "stack": []})
    write_text(repo / "projects/memhub/notes.md", "# MemHub Notes\n\n")
    write_yaml(repo / "projects/memhub/history.yaml", {"schema_version": SCHEMA_VERSION, "project_id": "memhub", "events": []})

    write_yaml(repo / "knowledge/index.yaml", {"schema_version": SCHEMA_VERSION, "domains": []})
    write_yaml(repo / "knowledge/product.yaml", {"schema_version": SCHEMA_VERSION, "domain": "product", "items": []})
    write_yaml(repo / "knowledge/tech.yaml", {"schema_version": SCHEMA_VERSION, "domain": "tech", "items": []})
    write_yaml(repo / "relations/people.yaml", {"schema_version": SCHEMA_VERSION, "people": []})
    write_yaml(repo / "relations/orgs.yaml", {"schema_version": SCHEMA_VERSION, "orgs": []})
    write_yaml(repo / "relations/tools.yaml", {"schema_version": SCHEMA_VERSION, "tools": []})
    write_yaml(repo / f"timeline/{today_month()}.yaml", {"schema_version": SCHEMA_VERSION, "month": today_month(), "events": []})

    gitignore = """# MemHub generated local indexes/caches and secrets\n.memhub/cache/\n.memhub/indexes/\n.memhub/secrets.yaml\n.memhub/secrets/\n*.db\n.DS_Store\n"""
    write_text(repo / ".gitignore", gitignore)
    write_text(repo / ".gitattributes", GITATTRIBUTES_CONTENT)
    ensure_merge_driver_registered(repo)

    commit_all(repo, "memhub: init repository")


def get_default_project(repo: Path) -> str | None:
    active = read_yaml(repo / "projects/_active.yaml", {})
    for p in active.get("active_projects", []):
        if p.get("default"):
            return p.get("id")
    if active.get("active_projects"):
        return active["active_projects"][0].get("id")
    return None


# Per-pack limits for list sections. "project" focuses on one project and is
# otherwise close to "standard" for the identity sections.
PACK_LIMITS: dict[str, dict[str, int]] = {
    "brief": {"preferences": 3, "decisions": 3, "constraints": 0, "conventions": 0,
              "knowledge": 0, "relations": 0, "timeline": 0, "tasks": 0},
    "standard": {"preferences": 8, "decisions": 8, "constraints": 5, "conventions": 5,
                 "knowledge": 0, "relations": 0, "timeline": 0, "tasks": 5},
    "full": {"preferences": 12, "decisions": 12, "constraints": 10, "conventions": 10,
             "knowledge": 10, "relations": 10, "timeline": 8, "tasks": 10},
    "project": {"preferences": 5, "decisions": 12, "constraints": 5, "conventions": 5,
                "knowledge": 0, "relations": 0, "timeline": 0, "tasks": 12},
}


def _entry_label(item: dict[str, Any]) -> str:
    """Best-effort one-line label for a canonical entry across schemas."""
    content = item.get("content")
    if content:
        return str(content)
    key = item.get("key") or item.get("name") or item.get("title") or item.get("id")
    value = item.get("value") or item.get("summary") or item.get("description")
    if key and value:
        return f"{key}: {value}"
    return str(key or value or "")


def _active_sorted(items: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    active = [x for x in items if x.get("status", "active") == "active"]
    active.sort(key=lambda x: x.get("importance", 0), reverse=True)
    return active[:limit] if limit else active


def latest_timeline_events(repo: Path, limit: int) -> list[dict[str, Any]]:
    if not limit:
        return []
    events: list[dict[str, Any]] = []
    for path in sorted((repo / "timeline").glob("*.yaml"), reverse=True):
        data = read_yaml(path, {}) or {}
        for ev in data.get("events", []) or []:
            # Archived events were `forget`-ten; keep them out of context.
            if isinstance(ev, dict) and ev.get("status", "active") != "active":
                continue
            events.append(ev)
        if len(events) >= limit:
            break
    events.sort(key=lambda e: str(e.get("date") or e.get("created_at") or ""), reverse=True)
    return events[:limit]


def context_model(repo: Path, project: str | None = None, pack: str = "standard") -> dict[str, Any]:
    """Assemble the data the context pack renders from. Used by both the built-in
    Markdown renderer and the optional user template."""
    limits = PACK_LIMITS.get(pack, PACK_LIMITS["standard"])
    profile = read_yaml(repo / "identity/profile.yaml", {}) or {}
    prefs = read_yaml(repo / "identity/preferences.yaml", {}) or {}
    conventions = read_yaml(repo / "identity/conventions.yaml", {}) or {}
    constraints = read_yaml(repo / "identity/constraints.yaml", {}) or {}
    project_id = project or get_default_project(repo)

    model: dict[str, Any] = {
        "pack": pack,
        "generated_at": now_iso(),
        "profile": profile.get("profile", {}),
        "communication": profile.get("communication", {}),
        "preferences": _active_sorted(prefs.get("preferences", []) or [], limits["preferences"]),
        "constraints": _active_sorted(constraints.get("constraints", []) or [], limits["constraints"]),
        "conventions": _active_sorted(conventions.get("conventions", []) or [], limits["conventions"]),
        "project": {},
        "decisions": [],
        "tasks": [],
        "knowledge": [],
        "relations": {},
        "timeline": latest_timeline_events(repo, limits["timeline"]),
        "project_id": project_id,
    }

    if project_id:
        ctx = read_yaml(repo / f"projects/{project_id}/context.yaml", {}) or {}
        decisions = read_yaml(repo / f"projects/{project_id}/decisions.yaml", {}) or {}
        tasks = read_yaml(repo / f"projects/{project_id}/tasks.yaml", {}) or {}
        model["project"] = ctx.get("project", {})
        model["decisions"] = (decisions.get("decisions", []) or [])[:limits["decisions"]]
        open_tasks = [t for t in (tasks.get("tasks", []) or []) if t.get("status") not in {"done", "cancelled"}]
        model["tasks"] = open_tasks[:limits["tasks"]]

    if limits["knowledge"]:
        kn: list[dict[str, Any]] = []
        for path in sorted((repo / "knowledge").glob("*.yaml")):
            if path.name == "index.yaml":
                continue
            data = read_yaml(path, {}) or {}
            for item in (data.get("items", []) or []):
                entry = dict(item)
                entry.setdefault("domain", data.get("domain", path.stem))
                kn.append(entry)
        model["knowledge"] = _active_sorted(kn, limits["knowledge"])

    if limits["relations"]:
        rel: dict[str, list[dict[str, Any]]] = {}
        for kind, key in (("people", "people"), ("orgs", "orgs"), ("tools", "tools")):
            data = read_yaml(repo / f"relations/{kind}.yaml", {}) or {}
            items = (data.get(key, []) or [])[:limits["relations"]]
            if items:
                rel[kind] = items
        model["relations"] = rel

    return model


def build_context(repo: Path, project: str | None = None, pack: str = "standard") -> str:
    m = context_model(repo, project=project, pack=pack)
    p = m["profile"]
    c = m["communication"]

    lines: list[str] = []
    lines.append("# MemHub Context Pack")
    lines.append("")
    lines.append(f"<!-- Auto-generated by MemHub (pack: {m['pack']}). Treat as user-auditable memory, not absolute truth. -->")
    lines.append("")

    lines.append("## User")
    lines.append(f"- Name: {p.get('name') or ''}")
    if p.get("role"):
        lines.append(f"- Role: {p.get('role')}")
    if p.get("company"):
        lines.append(f"- Company: {p.get('company')}")
    if p.get("bio"):
        lines.append(f"- Bio: {p.get('bio')}")
    lines.append(f"- Default language: {c.get('default_language', 'zh-CN')}")
    lines.append(f"- Communication style: {c.get('preferred_style', 'direct_structured')}")
    if c.get("likes"):
        lines.append("- Likes: " + ", ".join(c.get("likes", [])))
    if c.get("dislikes"):
        lines.append("- Dislikes: " + ", ".join(c.get("dislikes", [])))
    lines.append("")

    if m["preferences"]:
        lines.append("## Important Preferences")
        for item in m["preferences"]:
            lines.append(f"- {_entry_label(item)}")
        lines.append("")

    if m["constraints"]:
        lines.append("## Constraints")
        for item in m["constraints"]:
            lines.append(f"- {_entry_label(item)}")
        lines.append("")

    if m["conventions"]:
        lines.append("## Conventions")
        for item in m["conventions"]:
            lines.append(f"- {_entry_label(item)}")
        lines.append("")

    proj = m["project"]
    if m["project_id"]:
        lines.append(f"## Current Project: {proj.get('name', m['project_id'])}")
        if proj.get("description"):
            lines.append(f"- Description: {proj.get('description')}")
        if proj.get("current_phase"):
            lines.append(f"- Phase: {proj.get('current_phase')}")
        if proj.get("goals"):
            lines.append("- Goals:")
            for g in proj.get("goals", [])[:5]:
                lines.append(f"  - {g}")
        if proj.get("constraints"):
            lines.append("- Constraints:")
            for con in proj.get("constraints", [])[:5]:
                lines.append(f"  - {con}")
        if m["decisions"]:
            lines.append("")
            lines.append("### Recent Decisions")
            for d in m["decisions"]:
                lines.append(f"- [{str(d.get('created_at', ''))[:10]}] {_entry_label(d)}")
        if m["tasks"]:
            lines.append("")
            lines.append("### Open Tasks")
            for t in m["tasks"]:
                status = t.get("status", "")
                suffix = f" ({status})" if status else ""
                lines.append(f"- {_entry_label(t)}{suffix}")
        lines.append("")

    if m["knowledge"]:
        lines.append("## Knowledge")
        for item in m["knowledge"]:
            domain = item.get("domain")
            prefix = f"[{domain}] " if domain else ""
            lines.append(f"- {prefix}{_entry_label(item)}")
        lines.append("")

    if m["relations"]:
        lines.append("## Relations")
        for kind in ("people", "orgs", "tools"):
            items = m["relations"].get(kind)
            if not items:
                continue
            lines.append(f"- {kind.capitalize()}:")
            for item in items:
                name = item.get("name") or item.get("id") or item.get("content") or ""
                note = item.get("role") or item.get("relation") or item.get("note") or item.get("description") or ""
                lines.append(f"  - {name}" + (f" — {note}" if note else ""))
        lines.append("")

    if m["timeline"]:
        lines.append("## Recent Timeline")
        for e in m["timeline"]:
            date = str(e.get("date") or e.get("created_at") or "")[:10]
            lines.append(f"- [{date}] {_entry_label(e)}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def build_item(content: str, type_: str = "fact", project: str | None = None) -> dict[str, Any]:
    """Build a single memory item dict shared by direct-write and inbox capture."""
    sid = short_id()
    return {
        "id": f"mem_{timestamp_id()}_{sid}",
        "type": type_,
        "scope": "project" if project else "inbox",
        "status": "pending",
        "content": content,
        "suggested_target": f"projects/{project}/decisions.yaml" if type_ == "decision" and project else None,
        "confidence": 0.8,
        "importance": 0.6,
        "created_at": now_iso(),
    }


def remember_inbox(repo: Path, content: str, type_: str = "fact", source_client: str = "manual", project: str | None = None) -> Path:
    """Capture into the inbox tier (audit buffer). One file per capture."""
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    sid = short_id()
    item = build_item(content, type_=type_, project=project)
    file = repo / "inbox" / f"{ts}-{source_client}-{sid}.yaml"
    payload = {
        "schema_version": SCHEMA_VERSION,
        "inbox_id": f"inbox_{timestamp_id()}_{sid}",
        "status": "pending",
        "created_at": now_iso(),
        "source": {"client": source_client},
        "items": [item],
    }
    write_yaml(file, payload)
    commit_all(repo, f"memhub: add inbox/{type_}: {content[:50]}")
    return file


def remember_direct(repo: Path, content: str, type_: str = "fact", source_client: str = "manual", project: str | None = None) -> tuple[Path, bool]:
    """Write straight into canonical memory (default). Returns (target, changed)."""
    item = build_item(content, type_=type_, project=project)
    item["source"] = {"client": source_client}
    target = suggested_target_for_item(repo, item)
    inbox_data = {"source": {"client": source_client}, "created_at": item["created_at"]}
    changed = apply_item_to_target(repo, target, item, inbox_data=inbox_data, source_path=None)
    if changed:
        commit_all(repo, f"memhub: remember {type_}: {content[:50]}")
    return target, changed


def remember(repo: Path, content: str, type_: str = "fact", source_client: str = "manual", project: str | None = None, to_inbox: bool = False) -> str:
    """Default: write canonical memory directly. With `to_inbox`, capture to inbox tier."""
    if to_inbox:
        file = remember_inbox(repo, content, type_=type_, source_client=source_client, project=project)
        return f"Captured to inbox: {file}"
    target, changed = remember_direct(repo, content, type_=type_, source_client=source_client, project=project)
    rel = target.relative_to(repo).as_posix()
    if changed:
        return f"Remembered ({type_}) -> {rel}"
    return f"Already present ({type_}) in {rel}; skipped duplicate."


# --- Canonical file walk: search / forget ------------------------------------

# Canonical files and the list key each one stores entries under.
CANONICAL_SOURCES: tuple[tuple[str, str], ...] = (
    ("identity/preferences.yaml", "preferences"),
    ("identity/constraints.yaml", "constraints"),
    ("identity/conventions.yaml", "conventions"),
    ("knowledge/*.yaml", "items"),
    ("relations/people.yaml", "people"),
    ("relations/orgs.yaml", "orgs"),
    ("relations/tools.yaml", "tools"),
    ("timeline/*.yaml", "events"),
    ("projects/*/decisions.yaml", "decisions"),
    ("projects/*/tasks.yaml", "tasks"),
    ("projects/*/stack.yaml", "stack"),
)


def iter_canonical_entries(repo: Path):
    """Yield (path, list_key, index, entry) for every canonical entry."""
    for pattern, key in CANONICAL_SOURCES:
        if "*" in pattern:
            paths = sorted(repo.glob(pattern))
        else:
            p = repo / pattern
            paths = [p] if p.exists() else []
        for path in paths:
            if path.name == "index.yaml":
                continue
            data = read_yaml(path, {}) or {}
            for idx, entry in enumerate(data.get(key, []) or []):
                if isinstance(entry, dict):
                    yield path, key, idx, entry


def _entry_project(repo: Path, path: Path) -> str | None:
    rel = path.relative_to(repo).as_posix()
    parts = rel.split("/")
    return parts[1] if len(parts) >= 3 and parts[0] == "projects" else None


def search(repo: Path, query: str, type_: str | None = None, project: str | None = None, limit: int = 20, include_archived: bool = False) -> str:
    q = _normalize_content(query)
    matches: list[tuple[float, str, dict[str, Any]]] = []
    for path, _key, _idx, entry in iter_canonical_entries(repo):
        if not include_archived and entry.get("status", "active") != "active":
            continue
        if type_ and entry.get("type") != type_:
            continue
        if project and _entry_project(repo, path) != project:
            continue
        label = _entry_label(entry)
        if q and q not in _normalize_content(label):
            continue
        rel = path.relative_to(repo).as_posix()
        matches.append((float(entry.get("importance", 0) or 0), rel, entry))
    if not matches:
        return "No matching memory found.\n"
    matches.sort(key=lambda m: m[0], reverse=True)
    lines = ["importance\ttype\tsource\tfile\tcontent"]
    for importance, rel, entry in matches[:limit]:
        src = (entry.get("source") or {}).get("client", "")
        content = _entry_label(entry).replace("\n", " ")
        if len(content) > 90:
            content = content[:87] + "..."
        lines.append(f"{importance:.2f}\t{entry.get('type', '')}\t{src}\t{rel}\t{content}")
    if len(matches) > limit:
        lines.append(f"... {len(matches) - limit} more (raise --limit to see all)")
    return "\n".join(lines) + "\n"


def forget(repo: Path, query: str, type_: str | None = None, project: str | None = None, apply: bool = False) -> str:
    """Soft-archive matching canonical entries (status -> archived)."""
    q = _normalize_content(query)
    # Group hits per file so we write each file once.
    hits: dict[Path, list[tuple[str, int, dict[str, Any]]]] = {}
    for path, key, idx, entry in iter_canonical_entries(repo):
        if entry.get("status", "active") != "active":
            continue
        if type_ and entry.get("type") != type_:
            continue
        if project and _entry_project(repo, path) != project:
            continue
        eid = str(entry.get("id") or "")
        label = _normalize_content(_entry_label(entry))
        if q and q != eid and q not in label:
            continue
        hits.setdefault(path, []).append((key, idx, entry))
    if not hits:
        return "No matching active memory to forget.\n"

    lines = ["Forget plan (soft-archive):"]
    total = 0
    for path in sorted(hits):
        rel = path.relative_to(repo).as_posix()
        for _key, _idx, entry in hits[path]:
            total += 1
            content = _entry_label(entry).replace("\n", " ")
            if len(content) > 80:
                content = content[:77] + "..."
            lines.append(f"- {rel} :: {entry.get('type', '')} :: {content}")

    if not apply:
        lines.append(f"Dry run only. {total} entr{'y' if total == 1 else 'ies'} would be archived. Re-run with --apply.")
        if total > 1:
            lines.append("Multiple matches — narrow with a longer query, an exact id, or --type/--project if some should be kept.")
        return "\n".join(lines) + "\n"

    for path in hits:
        data = read_yaml(path, {}) or {}
        for key, idx, _entry in hits[path]:
            items = data.get(key, []) or []
            if 0 <= idx < len(items) and isinstance(items[idx], dict):
                items[idx]["status"] = "archived"
                items[idx]["archived_at"] = now_iso()
        data["updated_at"] = now_iso()
        write_yaml(path, data)
    commit_all(repo, f"memhub: forget (archive) {total} entr{'y' if total == 1 else 'ies'}")
    lines.append(f"Applied. Archived {total} entr{'y' if total == 1 else 'ies'}.")
    return "\n".join(lines) + "\n"


def inbox_files(repo: Path, status: str | None = "pending") -> list[Path]:
    files = sorted((repo / "inbox").glob("*.yaml"))
    if status in (None, "all"):
        return files
    out: list[Path] = []
    for path in files:
        data = read_yaml(path, {})
        if data.get("status", "pending") == status:
            out.append(path)
    return out


def inbox_summary(path: Path) -> str:
    data = read_yaml(path, {})
    items = data.get("items", []) or []
    status = data.get("status", "pending")
    created = str(data.get("created_at", ""))[:19]
    source = (data.get("source") or {}).get("client", "")
    first = items[0] if items else {}
    type_ = first.get("type", "")
    content = str(first.get("content", "")).replace("\n", " ")
    if len(content) > 90:
        content = content[:87] + "..."
    return f"{path.name}\t{status}\t{type_}\t{source}\t{created}\t{content}"


def inbox_list(repo: Path, status: str | None = "pending") -> str:
    files = inbox_files(repo, status=status)
    if not files:
        return "No inbox items found.\n"
    lines = ["file\tstatus\ttype\tsource\tcreated_at\tcontent"]
    lines.extend(inbox_summary(path) for path in files)
    return "\n".join(lines) + "\n"


def resolve_inbox_file(repo: Path, ref: str) -> Path:
    direct = Path(ref)
    candidates: list[Path] = []
    if direct.is_absolute() and direct.exists():
        candidates.append(direct)
    candidates.extend([
        repo / "inbox" / ref,
        repo / "inbox" / (ref if ref.endswith(".yaml") else f"{ref}.yaml"),
    ])
    candidates.extend(sorted((repo / "inbox").glob(f"*{ref}*.yaml")))
    seen: set[Path] = set()
    unique = []
    for c in candidates:
        c = c.resolve()
        if c.exists() and c not in seen:
            unique.append(c)
            seen.add(c)
    if not unique:
        raise SystemExit(f"Inbox item not found: {ref}")
    if len(unique) > 1:
        names = ", ".join(x.name for x in unique[:5])
        raise SystemExit(f"Ambiguous inbox ref: {ref}. Matches: {names}")
    return unique[0]


def inbox_show(repo: Path, ref: str) -> str:
    path = resolve_inbox_file(repo, ref)
    return path.read_text(encoding="utf-8")


def item_project(item: dict[str, Any]) -> str | None:
    target = item.get("suggested_target") or ""
    parts = str(target).split("/")
    if len(parts) >= 3 and parts[0] == "projects":
        return parts[1]
    return None


def suggested_target_for_item(repo: Path, item: dict[str, Any]) -> Path:
    type_ = item.get("type", "fact")
    if item.get("suggested_target"):
        return repo / str(item["suggested_target"])
    if type_ == "decision":
        project = item_project(item) or get_default_project(repo) or "memhub"
        return repo / f"projects/{project}/decisions.yaml"
    if type_ == "preference":
        return repo / "identity/preferences.yaml"
    if type_ == "constraint":
        return repo / "identity/constraints.yaml"
    if type_ == "convention":
        return repo / "identity/conventions.yaml"
    if type_ == "knowledge":
        return repo / "knowledge/product.yaml"
    if type_ == "relation":
        return repo / "relations/people.yaml"
    if type_ in {"event", "fact"}:
        return repo / f"timeline/{today_month()}.yaml"
    return repo / "knowledge/product.yaml"


def canonical_entry(item: dict[str, Any], inbox_data: dict[str, Any], source_path: Path | None = None) -> dict[str, Any]:
    inbox_data = inbox_data or {}
    source = inbox_data.get("source") or {}
    entry = {
        "id": item.get("id") or f"mem_{timestamp_id()}_{short_id()}",
        "type": item.get("type", "fact"),
        "status": "active",
        "content": item.get("content", ""),
        "confidence": item.get("confidence", 0.8),
        "importance": item.get("importance", 0.6),
        "source": source,
        "created_at": item.get("created_at") or inbox_data.get("created_at") or now_iso(),
    }
    # `inbox_ref`/`promoted_at` only make sense when the entry came through the
    # inbox tier. A direct `remember` writes canonical memory with no inbox file.
    if source_path is not None:
        entry["promoted_at"] = now_iso()
        entry["inbox_ref"] = source_path.name
    return entry


def _normalize_content(value: Any) -> str:
    """Normalize an entry's content for dedup: collapse whitespace and casefold."""
    return " ".join(str(value or "").split()).casefold()


def append_unique(container: dict[str, Any], key: str, entry: dict[str, Any]) -> bool:
    """Insert entry unless an active duplicate exists. If the only match is an
    archived entry, revive it (status -> active) so re-remembering a forgotten
    memory brings it back instead of being silently dropped as a duplicate."""
    items = container.setdefault(key, [])
    content = _normalize_content(entry.get("content"))
    if content:
        archived_match: dict[str, Any] | None = None
        for existing in items:
            if _normalize_content(existing.get("content")) != content:
                continue
            if existing.get("status", "active") == "active":
                return False  # live duplicate; nothing to do
            archived_match = archived_match or existing
        if archived_match is not None:
            archived_match["status"] = "active"
            archived_match.pop("archived_at", None)
            container["updated_at"] = now_iso()
            return True
    items.insert(0, entry)
    container["updated_at"] = now_iso()
    return True


def apply_item_to_target(repo: Path, target: Path, item: dict[str, Any], inbox_data: dict[str, Any] | None = None, source_path: Path | None = None) -> bool:
    target.parent.mkdir(parents=True, exist_ok=True)
    data = read_yaml(target, {}) or {}
    rel = target.relative_to(repo).as_posix()
    entry = canonical_entry(item, inbox_data, source_path)
    type_ = item.get("type", "fact")

    if rel.startswith("projects/") and rel.endswith("/decisions.yaml"):
        data.setdefault("schema_version", SCHEMA_VERSION)
        if "project_id" not in data:
            data["project_id"] = rel.split("/")[1]
        changed = append_unique(data, "decisions", entry)
    elif rel == "identity/preferences.yaml":
        data.setdefault("schema_version", SCHEMA_VERSION)
        changed = append_unique(data, "preferences", entry)
    elif rel == "identity/constraints.yaml":
        data.setdefault("schema_version", SCHEMA_VERSION)
        changed = append_unique(data, "constraints", entry)
    elif rel == "identity/conventions.yaml":
        data.setdefault("schema_version", SCHEMA_VERSION)
        changed = append_unique(data, "conventions", entry)
    elif rel.startswith("knowledge/"):
        data.setdefault("schema_version", SCHEMA_VERSION)
        data.setdefault("domain", target.stem)
        changed = append_unique(data, "items", entry)
    elif rel.startswith("relations/"):
        data.setdefault("schema_version", SCHEMA_VERSION)
        key = target.stem  # people / orgs / tools
        changed = append_unique(data, key, entry)
    elif rel.startswith("timeline/"):
        data.setdefault("schema_version", SCHEMA_VERSION)
        data.setdefault("month", target.stem)
        event = dict(entry)
        event.setdefault("date", str(entry.get("created_at", ""))[:10])
        changed = append_unique(data, "events", event)
    else:
        data.setdefault("schema_version", SCHEMA_VERSION)
        changed = append_unique(data, "items", entry)

    if changed:
        write_yaml(target, data)
    return changed


def promote_plan(repo: Path, refs: list[str] | None = None, status: str = "pending") -> list[tuple[Path, dict[str, Any], dict[str, Any], Path]]:
    if refs:
        files = [resolve_inbox_file(repo, ref) for ref in refs]
    else:
        files = inbox_files(repo, status=status)
    plan: list[tuple[Path, dict[str, Any], dict[str, Any], Path]] = []
    for path in files:
        data = read_yaml(path, {}) or {}
        if status != "all" and data.get("status", "pending") != status and not refs:
            continue
        for item in data.get("items", []) or []:
            if item.get("status", "pending") not in {"pending", "accepted"}:
                continue
            target = suggested_target_for_item(repo, item)
            plan.append((path, data, item, target))
    return plan


def promote(repo: Path, refs: list[str] | None = None, apply: bool = False, status: str = "pending") -> str:
    plan = promote_plan(repo, refs=refs, status=status)
    if not plan:
        return "No promotable inbox items found.\n"

    lines = ["Promote plan:"]
    changed_files: set[Path] = set()
    touched_inbox: dict[Path, dict[str, Any]] = {}
    for path, data, item, target in plan:
        rel_target = target.relative_to(repo).as_posix()
        content = str(item.get("content", ""))
        lines.append(f"- {path.name} :: {item.get('type', 'fact')} -> {rel_target}")
        lines.append(f"  content: {content}")
        if apply:
            changed = apply_item_to_target(repo, target, item, data, path)
            item["status"] = "promoted"
            item["promoted_at"] = now_iso()
            item["promoted_to"] = rel_target
            touched_inbox[path] = data
            if changed:
                changed_files.add(target)

    if apply:
        for path, data in touched_inbox.items():
            items = data.get("items", []) or []
            if items and all(item.get("status") == "promoted" for item in items):
                data["status"] = "promoted"
            data["updated_at"] = now_iso()
            write_yaml(path, data)
        commit_all(repo, "memhub: promote inbox to canonical")
        lines.append(f"Applied. Updated {len(changed_files)} canonical file(s), marked {len(touched_inbox)} inbox file(s).")
    else:
        lines.append("Dry run only. Re-run with --apply to write canonical files and mark inbox items promoted.")
    return "\n".join(lines) + "\n"


# --- Sync providers: GitHub / Gitee -------------------------------------------------

PROVIDERS: dict[str, dict[str, str]] = {
    "github": {
        "display": "GitHub",
        "api_base": "https://api.github.com",
        "web_base": "https://github.com",
        "git_host": "github.com",
        "env_token": "MEMHUB_GITHUB_TOKEN",
        "token_url": "https://github.com/settings/tokens?type=beta",
        "oauth_device_code_url": "https://github.com/login/device/code",
        "oauth_access_token_url": "https://github.com/login/oauth/access_token",
        "env_client_id": "MEMHUB_GITHUB_CLIENT_ID",
        "default_client_id": 'Ov23livelceFZGWGJG0A',
        "env_broker_url": "MEMHUB_OAUTH_BROKER_URL",
        "default_broker_url": "https://oauth.1024hub.cn",
    },
    "gitee": {
        "display": "Gitee",
        "api_base": "https://gitee.com/api/v5",
        "web_base": "https://gitee.com",
        "git_host": "gitee.com",
        "env_token": "MEMHUB_GITEE_TOKEN",
        "token_url": "https://gitee.com/profile/personal_access_tokens",
        "oauth_authorize_url": "https://gitee.com/oauth/authorize",
        "oauth_access_token_url": "https://gitee.com/oauth/token",
        "env_client_id": "MEMHUB_GITEE_CLIENT_ID",
        "default_client_id": '857230fab7f3c4cf4439383f1afc236f4f3ec2435fb114e149c0cfc288e589f8',
        "env_client_secret": "MEMHUB_GITEE_CLIENT_SECRET",
        "env_broker_url": "MEMHUB_GITEE_OAUTH_BROKER_URL",
        "default_broker_url": "https://oauth.1024hub.cn",
    },
}


# Shared MemHub Auth Broker (v2 session protocol). The broker holds each
# provider's OAuth client_secret server-side, so the skill works out of the box
# with no per-user setup. Override per provider via env_broker_url or --broker-url.
DEFAULT_BROKER_URL = "https://oauth.1024hub.cn"


def config_path(repo: Path) -> Path:
    return repo / ".memhub/config.yaml"


def secrets_path(repo: Path) -> Path:
    return repo / ".memhub/secrets.yaml"


def load_config(repo: Path) -> dict[str, Any]:
    return read_yaml(config_path(repo), {}) or {}


def save_config(repo: Path, config: dict[str, Any]) -> None:
    config.setdefault("schema_version", SCHEMA_VERSION)
    write_yaml(config_path(repo), config)


def load_secrets(repo: Path) -> dict[str, Any]:
    return read_yaml(secrets_path(repo), {}) or {}


def save_secrets(repo: Path, secrets: dict[str, Any]) -> None:
    path = secrets_path(repo)
    write_yaml(path, secrets)
    try:
        path.chmod(0o600)
    except OSError:
        pass


def ensure_gitignore_secret(repo: Path) -> None:
    path = repo / ".gitignore"
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    additions = [".memhub/secrets.yaml", ".memhub/secrets/"]
    changed = False
    for item in additions:
        if item not in existing.splitlines():
            existing = existing.rstrip() + ("\n" if existing.strip() else "") + item + "\n"
            changed = True
    if changed:
        write_text(path, existing)


def get_token(repo: Path, provider: str, explicit_token: str | None = None, require: bool = True) -> str | None:
    meta = PROVIDERS[provider]
    if explicit_token:
        return explicit_token
    if os.environ.get(meta["env_token"]):
        return os.environ[meta["env_token"]]
    secrets = load_secrets(repo)
    token = ((secrets.get("sync") or {}).get(provider) or {}).get("token")
    if token:
        return token
    if require:
        raise SystemExit(
            f"Missing {meta['display']} token. Pass --token, set {meta['env_token']}, "
            f"or run `memhub --repo <path> sync setup {provider}`. Token page: {meta['token_url']}"
        )
    return None


def store_token(repo: Path, provider: str, token: str, account: str | None = None) -> None:
    ensure_gitignore_secret(repo)
    secrets = load_secrets(repo)
    sync = secrets.setdefault("sync", {})
    item = sync.setdefault(provider, {})
    item["token"] = token
    if account:
        item["account"] = account
    item["updated_at"] = now_iso()
    save_secrets(repo, secrets)


def api_json(provider: str, method: str, path: str, token: str, payload: dict[str, Any] | None = None) -> tuple[int, dict[str, Any] | list[Any] | str]:
    meta = PROVIDERS[provider]
    url = meta["api_base"] + path
    data: bytes | None = None
    headers = {"Accept": "application/json", "User-Agent": "MemHub/0.1"}
    if provider == "github":
        headers["Authorization"] = f"Bearer {token}"
        headers["X-GitHub-Api-Version"] = "2022-11-28"
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
    else:  # gitee uses access_token in JSON/body for broad compatibility
        payload = dict(payload or {})
        payload.setdefault("access_token", token)
        if method.upper() == "GET":
            sep = "&" if "?" in url else "?"
            url = url + sep + urllib.parse.urlencode(payload)
        else:
            data = urllib.parse.urlencode(payload).encode("utf-8")
            headers["Content-Type"] = "application/x-www-form-urlencoded"
    req = urllib.request.Request(url, data=data, method=method.upper(), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            if not raw:
                return resp.status, {}
            try:
                return resp.status, json.loads(raw)
            except json.JSONDecodeError:
                return resp.status, raw
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            body: dict[str, Any] | list[Any] | str = json.loads(raw)
        except json.JSONDecodeError:
            body = raw
        return exc.code, body


def provider_user(provider: str, token: str) -> str:
    status, body = api_json(provider, "GET", "/user", token)
    if status >= 400:
        raise SystemExit(f"{PROVIDERS[provider]['display']} auth failed: HTTP {status}: {body}")
    if not isinstance(body, dict):
        raise SystemExit(f"Unexpected {PROVIDERS[provider]['display']} user response: {body}")
    login = body.get("login") or body.get("username") or body.get("name")
    if not login:
        raise SystemExit(f"Cannot detect {PROVIDERS[provider]['display']} username from response: {body}")
    return str(login)


def repo_exists_or_create(provider: str, token: str, owner: str, repo_name: str, private: bool = True, create: bool = True) -> str:
    meta = PROVIDERS[provider]
    if not create:
        return f"{meta['web_base']}/{owner}/{repo_name}"
    if provider == "github":
        payload = {"name": repo_name, "private": private, "auto_init": False}
        status, body = api_json(provider, "POST", "/user/repos", token, payload)
        if status in (200, 201):
            return str((body if isinstance(body, dict) else {}).get("html_url") or f"{meta['web_base']}/{owner}/{repo_name}")
        if status == 422:
            return f"{meta['web_base']}/{owner}/{repo_name} (already exists or cannot create; continuing)"
        raise SystemExit(f"Failed to create GitHub repo: HTTP {status}: {body}")
    payload = {"name": repo_name, "private": "true" if private else "false", "auto_init": "false"}
    status, body = api_json(provider, "POST", "/user/repos", token, payload)
    if status in (200, 201):
        if isinstance(body, dict):
            return str(body.get("html_url") or body.get("human_name") or f"{meta['web_base']}/{owner}/{repo_name}")
        return f"{meta['web_base']}/{owner}/{repo_name}"
    if status in (400, 409, 422):
        return f"{meta['web_base']}/{owner}/{repo_name} (already exists or cannot create; continuing)"
    raise SystemExit(f"Failed to create Gitee repo: HTTP {status}: {body}")


def remote_url(provider: str, owner: str, repo_name: str, method: str = "https") -> str:
    host = PROVIDERS[provider]["git_host"]
    if method == "ssh":
        return f"git@{host}:{owner}/{repo_name}.git"
    scheme_host = f"https://{host}"
    return f"{scheme_host}/{owner}/{repo_name}.git"


def auth_git_prefix(repo: Path) -> list[str]:
    cfg = load_config(repo)
    sync = cfg.get("sync") or {}
    provider = sync.get("provider")
    method = sync.get("auth_method", "token")
    remote = sync.get("remote") or ""
    if provider not in PROVIDERS or method not in {"token", "oauth"} or not str(remote).startswith("https://"):
        return []
    token = get_token(repo, provider, require=False)
    if not token:
        return []
    account = sync.get("account") or ((load_secrets(repo).get("sync") or {}).get(provider) or {}).get("account") or "x-access-token"
    if provider == "github":
        raw = f"x-access-token:{token}".encode("utf-8")
    else:
        raw = f"{account}:{token}".encode("utf-8")
    encoded = base64.b64encode(raw).decode("ascii")
    return ["-c", f"http.extraHeader=Authorization: Basic {encoded}"]


def run_git_auth(repo: Path, args: list[str], check: bool = False) -> subprocess.CompletedProcess[str]:
    return run_git(repo, [*auth_git_prefix(repo), *args], check=check)



def form_post_json(url: str, payload: dict[str, Any], headers: dict[str, str] | None = None) -> tuple[int, dict[str, Any] | str]:
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req_headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded", "User-Agent": "MemHub/0.1"}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, data=data, method="POST", headers=req_headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            if not raw:
                return resp.status, {}
            try:
                return resp.status, json.loads(raw)
            except json.JSONDecodeError:
                return resp.status, raw
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            return exc.code, json.loads(raw)
        except json.JSONDecodeError:
            return exc.code, raw


def json_post(url: str, payload: dict[str, Any], headers: dict[str, str] | None = None) -> tuple[int, dict[str, Any] | str]:
    data = json.dumps(payload).encode("utf-8")
    req_headers = {"Accept": "application/json", "Content-Type": "application/json", "User-Agent": "MemHub/0.1"}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, data=data, method="POST", headers=req_headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            if not raw:
                return resp.status, {}
            try:
                return resp.status, json.loads(raw)
            except json.JSONDecodeError:
                return resp.status, raw
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            return exc.code, json.loads(raw)
        except json.JSONDecodeError:
            return exc.code, raw


def open_or_print_url(url: str, no_browser: bool = False) -> None:
    print(f"Open this URL in your browser:\n{url}\n", file=sys.stderr)
    if not no_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass


def github_device_flow(client_id: str, scope: str = "repo", no_browser: bool = False) -> str:
    meta = PROVIDERS["github"]
    status, body = form_post_json(meta["oauth_device_code_url"], {"client_id": client_id, "scope": scope})
    if status >= 400 or not isinstance(body, dict):
        raise SystemExit(f"GitHub device flow failed: HTTP {status}: {body}")
    device_code = body.get("device_code")
    user_code = body.get("user_code")
    verification_uri = body.get("verification_uri") or body.get("verification_uri_complete")
    interval = int(body.get("interval") or 5)
    if not device_code or not user_code or not verification_uri:
        raise SystemExit(f"Invalid GitHub device response: {body}")
    print("GitHub authorization required.", file=sys.stderr)
    print(f"User code: {user_code}", file=sys.stderr)
    open_or_print_url(str(verification_uri), no_browser=no_browser)
    while True:
        time.sleep(interval)
        status, token_body = form_post_json(
            meta["oauth_access_token_url"],
            {
                "client_id": client_id,
                "device_code": device_code,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            },
        )
        if status >= 400 or not isinstance(token_body, dict):
            raise SystemExit(f"GitHub token exchange failed: HTTP {status}: {token_body}")
        if token_body.get("access_token"):
            return str(token_body["access_token"])
        error = token_body.get("error")
        if error == "authorization_pending":
            continue
        if error == "slow_down":
            interval += 5
            continue
        raise SystemExit(f"GitHub authorization failed: {token_body}")


class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    server_version = "MemHubOAuth/0.1"

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        self.server.oauth_code = (params.get("code") or [None])[0]  # type: ignore[attr-defined]
        self.server.oauth_state = (params.get("state") or [None])[0]  # type: ignore[attr-defined]
        self.server.oauth_error = (params.get("error") or [None])[0]  # type: ignore[attr-defined]
        if self.server.oauth_code:  # type: ignore[attr-defined]
            body = "MemHub authorization complete. You can close this tab."
        else:
            body = "MemHub authorization failed. You can close this tab."
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body.encode("utf-8"))))
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def log_message(self, fmt: str, *args: Any) -> None:
        return


def wait_for_local_oauth_code(port: int, timeout: int = 180) -> tuple[str | None, str, str | None]:
    server = http.server.HTTPServer(("127.0.0.1", port), OAuthCallbackHandler)
    server.oauth_code = None  # type: ignore[attr-defined]
    server.oauth_state = None  # type: ignore[attr-defined]
    server.oauth_error = None  # type: ignore[attr-defined]
    thread = threading.Thread(target=server.handle_request, daemon=True)
    thread.start()
    thread.join(timeout=timeout)
    code = getattr(server, "oauth_code", None)
    state = getattr(server, "oauth_state", None)
    error = getattr(server, "oauth_error", None)
    server.server_close()
    return code, error or "", state


def gitee_oauth_flow(client_id: str, client_secret: str, redirect_uri: str, scope: str = "user_info projects", no_browser: bool = False, callback_port: int = 8765, manual_code: str | None = None) -> str:
    meta = PROVIDERS["gitee"]
    if not redirect_uri:
        redirect_uri = f"http://127.0.0.1:{callback_port}/callback"
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scope,
    }
    authorize_url = meta["oauth_authorize_url"] + "?" + urllib.parse.urlencode(params)
    code = manual_code
    if not code:
        open_or_print_url(authorize_url, no_browser=no_browser)
        if redirect_uri.startswith("http://127.0.0.1") or redirect_uri.startswith("http://localhost"):
            print(f"Waiting for OAuth callback on {redirect_uri} ...", file=sys.stderr)
            code, err, _state = wait_for_local_oauth_code(callback_port)
            if err:
                raise SystemExit(f"Gitee authorization failed: {err}")
        if not code:
            if sys.stdin.isatty():
                code = input("Paste Gitee authorization code: ").strip()
            else:
                raise SystemExit("No Gitee authorization code received. Re-run with --manual-code or use an interactive terminal.")
    status, body = form_post_json(
        meta["oauth_access_token_url"],
        {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "client_secret": client_secret,
        },
    )
    if status >= 400 or not isinstance(body, dict) or not body.get("access_token"):
        raise SystemExit(f"Gitee token exchange failed: HTTP {status}: {body}")
    return str(body["access_token"])


def gitee_broker_oauth_flow(broker_url: str, redirect_uri: str, scope: str = "user_info projects", no_browser: bool = False, callback_port: int = 8765, manual_code: str | None = None) -> str:
    """DEPRECATED legacy broker protocol (broker < 2.0 with /oauth/gitee/*
    endpoints). Superseded by broker_session_flow() for the v2 session API.
    Kept for reference / old self-hosted brokers; not called by default.

    Gitee OAuth via MemHub OAuth Broker.

    Broker protocol:
    - GET  {broker}/oauth/gitee/authorize?redirect_uri=...&scope=...&state=...
      redirects user to Gitee, then back to the local redirect_uri with a short `code`.
    - POST {broker}/oauth/gitee/token {code, redirect_uri, state}
      returns {access_token}. The Gitee client_secret stays on the broker server.
    """
    broker = broker_url.rstrip("/")
    if not redirect_uri:
        redirect_uri = f"http://127.0.0.1:{callback_port}/callback"
    state = short_id(24)
    authorize_url = broker + "/oauth/gitee/authorize?" + urllib.parse.urlencode({
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state,
    })
    code = manual_code
    returned_state = None
    if not code:
        open_or_print_url(authorize_url, no_browser=no_browser)
        if redirect_uri.startswith("http://127.0.0.1") or redirect_uri.startswith("http://localhost"):
            print(f"Waiting for Gitee OAuth broker callback on {redirect_uri} ...", file=sys.stderr)
            code, err, returned_state = wait_for_local_oauth_code(callback_port)
            if err:
                raise SystemExit(f"Gitee authorization failed: {err}")
        if not code:
            if sys.stdin.isatty():
                code = input("Paste MemHub/Gitee broker authorization code: ").strip()
            else:
                raise SystemExit("No Gitee authorization code received. Re-run with --manual-code or use an interactive terminal.")
    if returned_state and returned_state != state:
        raise SystemExit("Gitee authorization failed: OAuth state mismatch.")
    status, body = json_post(broker + "/oauth/gitee/token", {"code": code, "redirect_uri": redirect_uri, "state": state})
    if status >= 400 or not isinstance(body, dict) or not body.get("access_token"):
        raise SystemExit(f"Gitee broker token exchange failed: HTTP {status}: {body}")
    return str(body["access_token"])


def resolve_broker_url(provider: str, broker_url: str | None = None) -> str | None:
    """Broker URL precedence: explicit arg -> provider env -> generic env ->
    built-in default."""
    meta = PROVIDERS.get(provider, {})
    return (
        broker_url
        or os.environ.get(meta.get("env_broker_url", ""))
        or os.environ.get("MEMHUB_OAUTH_BROKER_URL", "")
        or meta.get("default_broker_url")
        or DEFAULT_BROKER_URL
        or None
    )


def _http_get_json(url: str) -> tuple[int, dict[str, Any] | str]:
    req = urllib.request.Request(url, method="GET", headers={"Accept": "application/json", "User-Agent": "MemHub/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            try:
                return resp.status, json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                return resp.status, raw
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            return exc.code, json.loads(raw)
        except json.JSONDecodeError:
            return exc.code, raw


def _extract_broker_token(body: dict[str, Any]) -> str | None:
    """Pull an access token out of a broker session-status payload, tolerating
    several field names so a minor broker schema change doesn't break us."""
    for key in ("access_token", "token", "accessToken"):
        if body.get(key):
            return str(body[key])
    for outer in ("token", "data", "result", "credential"):
        inner = body.get(outer)
        if isinstance(inner, dict):
            for key in ("access_token", "token", "accessToken"):
                if inner.get(key):
                    return str(inner[key])
    return None


def broker_session_flow(broker_url: str, provider: str, no_browser: bool = False, poll_timeout: int = 300) -> str:
    """MemHub Auth Broker v2 session flow.

    1. POST {broker}/auth/session?provider=<p>  -> { session_id, auth_url, expires_in }
    2. Open auth_url; the user approves at the provider. The broker holds the
       client_secret and handles the callback.
    3. Poll GET {broker}/auth/session/{session_id} until a token is issued
       (status leaves "pending"). Returns the access token.
    """
    broker = broker_url.rstrip("/")
    status, body = json_post(f"{broker}/auth/session?provider={urllib.parse.quote(provider)}", {"provider": provider})
    if status >= 400 or not isinstance(body, dict) or not body.get("session_id"):
        raise SystemExit(f"Broker session create failed: HTTP {status}: {body}")
    session_id = str(body["session_id"])
    auth_url = body.get("auth_url") or f"{broker}/auth/start?session_id={session_id}"
    expires_in = int(body.get("expires_in") or poll_timeout)

    print(f"{PROVIDERS[provider]['display']} 授权：在浏览器中完成授权即可。", file=sys.stderr)
    open_or_print_url(str(auth_url), no_browser=no_browser)

    waited = 0
    interval = 3
    while waited < expires_in:
        time.sleep(interval)
        waited += interval
        st, sbody = _http_get_json(f"{broker}/auth/session/{urllib.parse.quote(session_id)}")
        if st >= 400 or not isinstance(sbody, dict):
            continue
        token = _extract_broker_token(sbody)
        if token:
            return token
        state = str(sbody.get("status", "")).lower()
        if state in {"error", "failed", "denied", "expired"}:
            raise SystemExit(f"Broker authorization failed: {sbody}")
    raise SystemExit("Broker authorization timed out before a token was issued. Re-run sync setup.")


def oauth_token(
    provider: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    scope: str | None = None,
    redirect_uri: str | None = None,
    callback_port: int = 8765,
    no_browser: bool = False,
    manual_code: str | None = None,
    broker_url: str | None = None,
) -> str:
    meta = PROVIDERS[provider]

    # Default path: the shared MemHub Auth Broker (v2 session flow). It keeps
    # each provider's client_secret server-side, so this works out of the box
    # for both GitHub and Gitee with no per-user configuration. A developer can
    # still opt into a direct flow by passing --client-secret (Gitee) or by
    # explicitly disabling the broker via --broker-url "" .
    explicit_secret = client_secret or os.environ.get(meta.get("env_client_secret", ""))
    if not explicit_secret:
        broker = resolve_broker_url(provider, broker_url)
        if broker:
            return broker_session_flow(broker, provider, no_browser=no_browser)

    # --- Fallbacks (no broker, or developer direct mode) ---------------------
    client_id = client_id or os.environ.get(meta.get("env_client_id", "")) or meta.get("default_client_id")
    if not client_id:
        raise SystemExit(f"Missing {meta['display']} OAuth client id. Pass --client-id or set {meta.get('env_client_id', '')}.")
    if provider == "github":
        return github_device_flow(client_id, scope=scope or "repo", no_browser=no_browser)
    if not explicit_secret:
        raise SystemExit(
            "Gitee OAuth needs either the MemHub Auth Broker (default) or developer "
            "direct mode with --client-secret / MEMHUB_GITEE_CLIENT_SECRET. "
            "Do not embed Gitee client_secret in public code."
        )
    return gitee_oauth_flow(
        client_id,
        explicit_secret,
        redirect_uri=redirect_uri or f"http://127.0.0.1:{callback_port}/callback",
        scope=scope or "user_info projects",
        no_browser=no_browser,
        callback_port=callback_port,
        manual_code=manual_code,
    )

def setup_git_sync(
    repo: Path,
    provider: str,
    repo_name: str,
    owner: str | None = None,
    token: str | None = None,
    branch: str = "main",
    private: bool = True,
    create_repo: bool = True,
    auth_method: str = "token",
    remote_method: str = "https",
    client_id: str | None = None,
    client_secret: str | None = None,
    scope: str | None = None,
    redirect_uri: str | None = None,
    callback_port: int = 8765,
    no_browser: bool = False,
    manual_code: str | None = None,
    broker_url: str | None = None,
) -> str:
    repo.mkdir(parents=True, exist_ok=True)
    ensure_repo(repo)
    if provider not in PROVIDERS:
        raise SystemExit(f"Unsupported provider: {provider}. Choose: {', '.join(PROVIDERS)}")
    if auth_method == "ssh" and remote_method != "ssh":
        raise SystemExit("--auth ssh requires --remote-method ssh")
    if auth_method in {"token", "oauth"} and remote_method != "https":
        raise SystemExit("--auth token/oauth requires --remote-method https")
    if auth_method in {"token", "oauth"}:
        if auth_method == "oauth":
            token = oauth_token(
                provider,
                client_id=client_id,
                client_secret=client_secret,
                scope=scope,
                redirect_uri=redirect_uri,
                callback_port=callback_port,
                no_browser=no_browser,
                manual_code=manual_code,
                broker_url=broker_url,
            )
        else:
            token = get_token(repo, provider, explicit_token=token, require=False)
            if not token:
                if sys.stdin.isatty():
                    token = getpass.getpass(f"{PROVIDERS[provider]['display']} token: ")
                else:
                    raise SystemExit(f"Token required. Use --token or set {PROVIDERS[provider]['env_token']}.")
        account = provider_user(provider, token)
        owner = owner or account
        store_token(repo, provider, token, account=account)
    else:
        token = None
        account = owner or ""
        if not owner:
            raise SystemExit("--owner is required when --auth ssh is used")

    owner = owner or account
    web_url = repo_exists_or_create(provider, token, owner, repo_name, private=private, create=create_repo) if token else f"{PROVIDERS[provider]['web_base']}/{owner}/{repo_name}"
    remote = remote_url(provider, owner, repo_name, method=remote_method)
    run_git(repo, ["remote", "remove", "origin"], check=False)
    run_git(repo, ["remote", "add", "origin", remote], check=False)
    run_git(repo, ["branch", "-M", branch], check=False)

    cfg = load_config(repo)
    sync_cfg = cfg.setdefault("sync", {})
    sync_cfg.update({
        "backend": "git",
        "type": "git",
        "provider": provider,
        "remote": remote,
        "repo": f"{owner}/{repo_name}",
        "branch": branch,
        "auth_method": auth_method,
        "remote_method": remote_method,
        "auto_pull": True,
        "auto_push": True,
        "push_throttle_seconds": sync_cfg.get("push_throttle_seconds", 3600),
        "pull_throttle_seconds": sync_cfg.get("pull_throttle_seconds", 3600),
        "pull_strategy": "rebase",
        "commit_prefix": "memhub:",
        "updated_at": now_iso(),
    })
    if account:
        sync_cfg["account"] = account
    save_config(repo, cfg)
    commit_all(repo, f"memhub: configure {provider} sync")
    if auth_method == "oauth":
        credential_line = "OAuth token is stored locally in .memhub/secrets.yaml and ignored by git."
    elif auth_method == "token":
        credential_line = "Token is stored locally in .memhub/secrets.yaml and ignored by git."
    else:
        credential_line = "SSH auth selected; no token stored by MemHub."
    return "\n".join([
        f"Connected {PROVIDERS[provider]['display']} sync.",
        f"Account: {account or owner}",
        f"Repository: {owner}/{repo_name}",
        f"Remote: {remote}",
        f"Repo page: {web_url}",
        credential_line,
    ]) + "\n"


def _remote_has_memory(repo: Path, branch: str) -> bool:
    """True if the remote branch already contains a MemHub repo (has
    .memhub/config.yaml). Used to decide seed-vs-pull on first onboarding."""
    if not _remote_has_branch(repo, branch):
        return False
    # ls-tree against the remote ref without checking anything out.
    run_git_auth(repo, ["fetch", "origin", branch], check=False)
    res = run_git(repo, ["ls-tree", "-r", "--name-only", f"origin/{branch}"], check=False)
    files = res.stdout.splitlines()
    return any(f == ".memhub/config.yaml" for f in files)


def onboard(
    repo: Path,
    provider: str,
    repo_name: str,
    *,
    name: str = "user",
    role: str = "",
    owner: str | None = None,
    branch: str = "main",
    private: bool = True,
    auth_method: str = "oauth",
    no_browser: bool = False,
    broker_url: str | None = None,
) -> str:
    """First-run onboarding for a new agent/machine.

    1. Authorize and configure the remote (no seeding yet).
    2. If the remote already holds a MemHub repo, pull it as the source of
       truth — do NOT seed local defaults (which would pollute real memory).
    3. Otherwise seed a fresh repo (init defaults) and push to establish it.
    4. Register the merge driver and report readiness.
    """
    repo.mkdir(parents=True, exist_ok=True)
    ensure_repo(repo)

    # Configure remote + credentials. create_repo=True is idempotent: it creates
    # the remote if missing, or continues if it already exists.
    setup_msg = setup_git_sync(
        repo,
        provider=provider,
        repo_name=repo_name,
        owner=owner,
        branch=branch,
        private=private,
        create_repo=True,
        auth_method=auth_method,
        remote_method="https" if auth_method in {"oauth", "token"} else "ssh",
        no_browser=no_browser,
        broker_url=broker_url,
    )

    outputs = [setup_msg.rstrip(), ""]

    if _remote_has_memory(repo, branch):
        # Remote is the source of truth on a fresh onboarding. The local repo
        # only holds the setup config/secret commit, so align hard to the remote
        # rather than risk an "unrelated histories" rebase conflict. We avoid
        # writing .gitattributes first so there are no untracked-file collisions.
        outputs.append("检测到远端已有记忆仓库 → 以远端为准，拉取到本地（不写入默认数据）。")
        run_git_auth(repo, ["fetch", "origin", branch], check=False)
        reset = run_git(repo, ["reset", "--hard", f"origin/{branch}"], check=False)
        outputs.append((reset.stdout + reset.stderr).strip())
        # Re-assert our sync config/credentials + merge driver on top of the
        # pulled tree (the remote tree may predate these).
        ensure_merge_driver_registered(repo)
        if not (repo / ".gitattributes").exists():
            write_text(repo / ".gitattributes", GITATTRIBUTES_CONTENT)
        _reassert_sync_config(repo, provider, owner, repo_name, branch, auth_method)
        _write_sync_cache(repo, last_pull_at=now_iso())
        outputs.append("\n本地记忆已与远端同步。")
    else:
        # Brand-new remote: seed defaults, then push to establish it.
        outputs.append("远端为空 → 初始化默认记忆并推送，建立远端仓库。")
        ensure_merge_driver_registered(repo)
        if not (repo / "identity/profile.yaml").exists():
            init_repo(repo, name=name, role=role)
            # init_repo rewrites config without sync details; restore them.
            _reassert_sync_config(repo, provider, owner, repo_name, branch, auth_method)
        if not (repo / ".gitattributes").exists():
            write_text(repo / ".gitattributes", GITATTRIBUTES_CONTENT)
            commit_all(repo, "memhub: add gitattributes")
        push = run_git_auth(repo, ["push", "-u", "origin", f"HEAD:{branch}"], check=False)
        outputs.append((push.stdout + push.stderr).strip())
        _write_sync_cache(repo, last_push_at=now_iso(), last_pull_at=now_iso())
        outputs.append("\n默认记忆已建立并推送到远端。")

    outputs.append("")
    outputs.append(doctor(repo))
    return "\n".join(outputs) + "\n"


def _reassert_sync_config(repo: Path, provider: str, owner: str | None, repo_name: str, branch: str, auth_method: str) -> None:
    """Restore MemHub sync config + remote after a pull/seed may have changed
    the working tree, without re-running authorization."""
    secrets = load_secrets(repo)
    account = ((secrets.get("sync") or {}).get(provider) or {}).get("account") or owner or ""
    owner = owner or account
    remote = remote_url(provider, owner, repo_name, method="https" if auth_method in {"oauth", "token"} else "ssh")
    run_git(repo, ["remote", "remove", "origin"], check=False)
    run_git(repo, ["remote", "add", "origin", remote], check=False)
    cfg = load_config(repo)
    sync_cfg = cfg.setdefault("sync", {})
    sync_cfg.update({
        "backend": "git", "type": "git", "provider": provider, "remote": remote,
        "repo": f"{owner}/{repo_name}", "branch": branch, "auth_method": auth_method,
        "remote_method": "https" if auth_method in {"oauth", "token"} else "ssh",
        "auto_pull": True, "auto_push": True,
        "push_throttle_seconds": sync_cfg.get("push_throttle_seconds", 3600),
        "pull_throttle_seconds": sync_cfg.get("pull_throttle_seconds", 3600),
        "pull_strategy": "rebase", "commit_prefix": "memhub:", "updated_at": now_iso(),
    })
    if account:
        sync_cfg["account"] = account
    save_config(repo, cfg)
    commit_all(repo, f"memhub: configure {provider} sync")


def sync_status(repo: Path) -> str:
    cfg = load_config(repo)
    sync = cfg.get("sync") or {}
    lines = ["MemHub sync status:"]
    lines.append(f"- backend: {sync.get('backend') or sync.get('type') or 'git'}")
    lines.append(f"- provider: {sync.get('provider') or 'custom'}")
    lines.append(f"- repo: {sync.get('repo') or ''}")
    lines.append(f"- branch: {sync.get('branch') or 'main'}")
    lines.append(f"- remote: {sync.get('remote') or run_git(repo, ['remote', 'get-url', 'origin'], check=False).stdout.strip()}")
    token_state = "not needed"
    provider = sync.get("provider")
    if provider in PROVIDERS and sync.get("auth_method") in {"token", "oauth"}:
        token_state = "available" if get_token(repo, provider, require=False) else "missing"
    lines.append(f"- credential: {token_state}")
    lines.append(run_git(repo, ["status", "--short", "--branch"], check=False).stdout.strip())
    return "\n".join(lines).strip() + "\n"


def _fmt_ago(iso_ts: str | None) -> str:
    secs = _seconds_since(iso_ts)
    if secs == float("inf"):
        return "never"
    secs = int(secs)
    if secs < 90:
        return f"{secs}s ago"
    if secs < 5400:
        return f"{secs // 60}m ago"
    if secs < 172800:
        return f"{secs // 3600}h ago"
    return f"{secs // 86400}d ago"


def doctor(repo: Path) -> str:
    """Diagnose whether automatic memory sync is ready on this machine/repo.

    Checks each precondition maybe_auto_push/maybe_auto_pull rely on and prints
    OK / WARN / FAIL with a fix hint, so a fresh agent or new machine can tell at
    a glance what (if anything) still needs doing."""
    checks: list[tuple[str, str, str]] = []  # (status, label, detail)

    def add(ok: str, label: str, detail: str = "") -> None:
        checks.append((ok, label, detail))

    # 1. Repo path / MEMHUB_REPO
    env_repo = os.environ.get("MEMHUB_REPO")
    if env_repo:
        same = Path(env_repo).expanduser().resolve() == repo
        add("OK" if same else "WARN", "MEMHUB_REPO",
            f"= {repo}" if same else f"env={env_repo} but operating on {repo}; agents must share one path")
    else:
        add("WARN", "MEMHUB_REPO",
            f"unset; using {repo}. Set MEMHUB_REPO so every agent points at the same repo")

    # 2. Git repository present
    is_git = (repo / ".git").exists()
    add("OK" if is_git else "FAIL", "git repo",
        str(repo) if is_git else f"not a git repo; run `memhub --repo {repo} init`")
    if not is_git:
        return _render_doctor(checks)

    cfg = load_config(repo)
    sync = cfg.get("sync") or {}
    provider = sync.get("provider")
    branch = sync.get("branch") or "main"

    # 3. Remote configured
    remote = sync.get("remote") or run_git(repo, ["remote", "get-url", "origin"], check=False).stdout.strip()
    add("OK" if remote else "FAIL", "remote",
        remote if remote else "no remote; run `memhub sync setup github` (or gitee)")

    # 4. Credential (token) reachable on THIS machine
    if provider in PROVIDERS and sync.get("auth_method") in {"token", "oauth"}:
        tok = get_token(repo, provider, require=False)
        add("OK" if tok else "FAIL", "credential",
            f"{provider} token available" if tok
            else f"no {provider} token on this machine; re-run `memhub sync setup {provider}` "
                 f"or set {PROVIDERS[provider]['env_token']}")
    elif sync.get("auth_method") == "ssh":
        add("OK", "credential", "ssh (no token stored by MemHub)")
    elif remote:
        add("WARN", "credential", "auth method unknown; sync may prompt for credentials")

    # 4b. OAuth broker reachability (only relevant for oauth auth without a token yet)
    if sync.get("auth_method") == "oauth" or (provider in PROVIDERS and not sync.get("auth_method")):
        broker = resolve_broker_url(provider or "gitee")
        if broker:
            st, body = _http_get_json(f"{broker.rstrip('/')}/auth/providers")
            if st == 200 and isinstance(body, dict) and provider in (body.get("providers") or []):
                add("OK", "oauth broker", f"{broker} (supports {provider})")
            elif st == 200 and isinstance(body, dict):
                add("WARN", "oauth broker",
                    f"{broker} reachable but provider '{provider}' not in {body.get('providers')}")
            else:
                add("WARN", "oauth broker", f"{broker} not reachable (HTTP {st}); OAuth setup may fail")
        else:
            add("WARN", "oauth broker", "no broker configured; Gitee one-click OAuth unavailable")

    # 5. Merge driver registered (per-machine, not cloned)
    driver = run_git(repo, ["config", "--local", "merge.memhub.driver"], check=False).stdout.strip()
    add("OK" if driver else "WARN", "merge driver",
        "registered" if driver else "not registered yet; runs automatically on next `sync`")

    # 6. Auto flags
    add("OK" if sync.get("auto_push", True) else "WARN", "auto_push",
        "on" if sync.get("auto_push", True) else "off; writes won't push until manual sync")
    add("OK" if sync.get("auto_pull", True) else "WARN", "auto_pull",
        "on" if sync.get("auto_pull", True) else "off; context won't pull automatically")

    # 7. Throttle config
    add("OK", "throttle",
        f"push {sync.get('push_throttle_seconds', 3600)}s / pull {sync.get('pull_throttle_seconds', 3600)}s")

    # 8. Last sync activity (per-machine cache)
    cache = _read_sync_cache(repo)
    add("OK", "last push", _fmt_ago(cache.get("last_push_at")))
    add("OK", "last pull", _fmt_ago(cache.get("last_pull_at")))

    # 9. Uncommitted local changes
    dirty = run_git(repo, ["status", "--porcelain"], check=False).stdout.strip()
    add("OK" if not dirty else "WARN", "working tree",
        "clean" if not dirty else "uncommitted changes present (will be committed on next write/sync)")

    return _render_doctor(checks)


def _render_doctor(checks: list[tuple[str, str, str]]) -> str:
    icon = {"OK": "✓", "WARN": "!", "FAIL": "✗"}
    width = max((len(label) for _, label, _ in checks), default=0)
    lines = ["MemHub doctor — automatic sync readiness:"]
    for status, label, detail in checks:
        lines.append(f"  [{icon.get(status, '?')}] {label.ljust(width)}  {detail}".rstrip())
    fails = sum(1 for s, _, _ in checks if s == "FAIL")
    warns = sum(1 for s, _, _ in checks if s == "WARN")
    if fails:
        lines.append(f"\n{fails} blocker(s): automatic sync is NOT ready. Fix the ✗ items above.")
    elif warns:
        lines.append(f"\nReady with {warns} note(s). Auto-sync works; review the ! items.")
    else:
        lines.append("\nAll good — memory syncs automatically on this machine.")
    return "\n".join(lines) + "\n"


    """Render a minimal `{{ key }}` template with stdlib only.

    Intentionally tiny: supports `{{ name }}` substitution with optional inner
    whitespace. Unknown placeholders render empty. This avoids a Jinja2 runtime
    dependency while still letting users customize exports via the template file.
    """
    import re

    def repl(match: "re.Match[str]") -> str:
        return str(values.get(match.group(1).strip(), ""))

    return re.sub(r"\{\{\s*([\w.]+)\s*\}\}", repl, tpl)


def _template_values(repo: Path, project: str | None) -> dict[str, str]:
    m = context_model(repo, project=project, pack="brief")
    p = m["profile"]
    c = m["communication"]
    proj = m["project"]
    proj_lines: list[str] = []
    if m["project_id"]:
        proj_lines.append(f"- {proj.get('name', m['project_id'])}: {proj.get('description', '')}".rstrip())
        if proj.get("current_phase"):
            proj_lines.append(f"- Phase: {proj['current_phase']}")
    decisions = "\n".join(f"- {_entry_label(d)}" for d in m["decisions"]) or "- (none)"
    return {
        "name": p.get("name", ""),
        "role": p.get("role", ""),
        "style": c.get("preferred_style", "direct_structured"),
        "project_context": "\n".join(proj_lines) or "- (none)",
        "recent_decisions": decisions,
    }


def export_chatbot(repo: Path, project: str | None = None) -> Path:
    template_path = repo / ".memhub/templates/context-pack.md.j2"
    if template_path.exists():
        body = _render_simple_template(template_path.read_text(encoding="utf-8"), _template_values(repo, project))
    else:
        body = build_context(repo, project=project, pack="brief")
    out = repo / "exports/chatbot.md"
    header = f"<!-- Auto-generated by MemHub. Generated at: {now_iso()} -->\n\n"
    write_text(out, header + body)
    commit_all(repo, "memhub: export chatbot context")
    return out


def commit_all(repo: Path, message: str) -> None:
    ensure_repo(repo)
    run_git(repo, ["add", "."], check=False)
    status = run_git(repo, ["status", "--porcelain"], check=False)
    if status.stdout.strip():
        # Avoid failure if git user isn't configured globally.
        run_git(repo, ["-c", "user.name=MemHub", "-c", "user.email=memhub@example.local", "commit", "-m", message], check=False)


# --- Structured merge driver -------------------------------------------------
#
# Canonical files are append-mostly YAML lists. A plain line-level union would
# interleave multi-line entries and corrupt the YAML, so MemHub registers a
# structured driver that merges the *lists* by entry identity. This lets two
# devices that each appended memory auto-merge instead of hitting a conflict.

# List keys that hold canonical entries and are safe to union-merge.
MERGE_LIST_KEYS = (
    "preferences", "constraints", "conventions", "decisions", "tasks",
    "stack", "items", "events", "people", "orgs", "tools", "active_projects",
)


def _entry_key(entry: Any) -> str:
    """Identity for dedup during merge: prefer id, else normalized content/name."""
    if isinstance(entry, dict):
        if entry.get("id"):
            return f"id::{entry['id']}"
        label = entry.get("content") or entry.get("name") or entry.get("key") or entry.get("title")
        if label:
            return f"c::{_normalize_content(label)}"
    return f"raw::{_normalize_content(entry)}"


def _union_lists(ours: list[Any], theirs: list[Any]) -> list[Any]:
    """Union two entry lists by identity, keeping ours first then new theirs."""
    out = list(ours)
    seen = {_entry_key(e) for e in ours}
    for entry in theirs:
        key = _entry_key(entry)
        if key not in seen:
            out.append(entry)
            seen.add(key)
    return out


def merge_yaml_docs(base: Any, ours: Any, theirs: Any) -> Any:
    """Three-way merge for MemHub canonical YAML. Union known list keys, prefer
    the newer side for scalars. `base` is currently unused but kept for the git
    driver contract and future smarter merges."""
    if not isinstance(ours, dict) or not isinstance(theirs, dict):
        return ours if ours is not None else theirs
    merged: dict[str, Any] = dict(ours)
    for key, their_val in theirs.items():
        if key not in merged:
            merged[key] = their_val
            continue
        our_val = merged[key]
        if key in MERGE_LIST_KEYS and isinstance(our_val, list) and isinstance(their_val, list):
            merged[key] = _union_lists(our_val, their_val)
    # Prefer the more recently updated side for the bookkeeping timestamp.
    our_ts = str(ours.get("updated_at") or "")
    their_ts = str(theirs.get("updated_at") or "")
    if their_ts > our_ts:
        merged["updated_at"] = their_ts
    return merged


def run_merge_driver(base_path: str, ours_path: str, theirs_path: str) -> int:
    """Git merge driver entrypoint. Writes the merged result back into `ours_path`."""
    base = read_yaml(Path(base_path), {})
    ours = read_yaml(Path(ours_path), {})
    theirs = read_yaml(Path(theirs_path), {})
    try:
        merged = merge_yaml_docs(base, ours, theirs)
    except Exception:
        # On any failure, fall back to a conflict so the user resolves by hand
        # rather than silently losing memory.
        return 1
    with Path(ours_path).open("w", encoding="utf-8") as f:
        yaml.safe_dump(merged, f, allow_unicode=True, sort_keys=False, width=1000)
    return 0


GITATTRIBUTES_CONTENT = """# MemHub: union-merge append-mostly canonical memory lists.
identity/*.yaml          merge=memhub
projects/**/*.yaml       merge=memhub
knowledge/*.yaml         merge=memhub
relations/*.yaml         merge=memhub
timeline/*.yaml          merge=memhub
inbox/*.yaml             merge=memhub
"""


def ensure_merge_driver_registered(repo: Path) -> None:
    """Register (or refresh) the MemHub merge driver in repo-local git config.

    Local git config is not cloned, so each machine must register the driver
    once. The command embeds an absolute interpreter + script path, which can go
    stale if the skill package moves; we therefore refresh the entry whenever the
    current path differs from what is registered. Idempotent on init and sync.
    """
    script = Path(__file__).resolve()
    driver_cmd = f'{json.dumps(sys.executable)} {json.dumps(str(script))} merge-driver %O %A %B'
    existing = run_git(repo, ["config", "--local", "merge.memhub.driver"], check=False).stdout.strip()
    if existing == driver_cmd:
        return
    run_git(repo, ["config", "--local", "merge.memhub.name", "MemHub structured YAML merge"], check=False)
    run_git(repo, ["config", "--local", "merge.memhub.driver", driver_cmd], check=False)


def _remote_has_branch(repo: Path, branch: str) -> bool:
    res = run_git_auth(repo, ["ls-remote", "--heads", "origin", branch], check=False)
    return bool(res.stdout.strip())


def _sync_cache_path(repo: Path) -> Path:
    # Per-machine, git-ignored. Throttle state must NOT be committed: it is local
    # to each device and committing it would create cross-device merge churn.
    return repo / ".memhub/cache/sync.yaml"


def _read_sync_cache(repo: Path) -> dict[str, Any]:
    return read_yaml(_sync_cache_path(repo), {}) or {}


def _write_sync_cache(repo: Path, **updates: Any) -> None:
    cache = _read_sync_cache(repo)
    cache.update(updates)
    write_yaml(_sync_cache_path(repo), cache)


def _seconds_since(iso_ts: str | None) -> float:
    """Seconds since an ISO timestamp, or +inf if missing/unparseable."""
    if not iso_ts:
        return float("inf")
    try:
        then = dt.datetime.fromisoformat(iso_ts)
    except (ValueError, TypeError):
        return float("inf")
    now = dt.datetime.now(then.tzinfo) if then.tzinfo else dt.datetime.now()
    return (now - then).total_seconds()


def _sync_now(repo: Path, quiet: bool = False) -> str:
    """Commit local changes, pull --rebase (if remote branch exists), then push.
    Shared by the manual `sync` command and the throttled auto-sync helpers."""
    cfg = load_config(repo)
    sync = cfg.get("sync") or {}
    branch = sync.get("branch") or "main"
    remote_names = run_git(repo, ["remote"], check=False).stdout.strip()
    outputs: list[str] = []

    if not remote_names:
        outputs.append("No git remote configured; local repository only. Run `memhub sync setup github` or `memhub sync setup gitee`.\n")
        state = read_yaml(repo / ".memhub/state.yaml", {}) or {}
        state["last_sync_at"] = now_iso()
        write_yaml(repo / ".memhub/state.yaml", state)
        commit_all(repo, "memhub: update sync state")
        return "" if quiet else "".join(outputs)

    # Commit local changes first so a pull --rebase has a clean tree to work on.
    commit_all(repo, "memhub: sync local changes")

    # Only rebase against the remote branch if it actually exists; a brand-new
    # remote has no branch yet and `pull` would fail noisily.
    if _remote_has_branch(repo, branch):
        pull = run_git_auth(repo, ["pull", "--rebase", "origin", branch], check=False)
        outputs.append(pull.stdout + pull.stderr)
        if pull.returncode != 0:
            # Most likely a rebase conflict. Abort to leave the repo in a clean,
            # usable state rather than stuck mid-rebase, and stop before pushing.
            if (repo / ".git" / "rebase-merge").exists() or (repo / ".git" / "rebase-apply").exists():
                run_git(repo, ["rebase", "--abort"], check=False)
                outputs.append(
                    "\nMemHub: pull --rebase hit a conflict and was aborted. "
                    "Local memory is intact and NOT pushed. Resolve manually:\n"
                    f"  cd {repo} && git pull --rebase origin {branch}\n"
                    "then re-run `memhub sync`.\n"
                )
            else:
                outputs.append(
                    "\nMemHub: pull failed (no conflict detected). Local memory is intact and NOT pushed. "
                    "Check the remote/credentials and re-run `memhub sync`.\n"
                )
            # Record the pull attempt so auto-pull doesn't hammer a broken remote.
            _write_sync_cache(repo, last_pull_at=now_iso())
            return "".join(outputs)
        _write_sync_cache(repo, last_pull_at=now_iso())

    state = read_yaml(repo / ".memhub/state.yaml", {}) or {}
    state["last_sync_at"] = now_iso()
    write_yaml(repo / ".memhub/state.yaml", state)
    commit_all(repo, "memhub: update sync state")
    push = run_git_auth(repo, ["push", "-u", "origin", f"HEAD:{branch}"], check=False)
    outputs.append(push.stdout + push.stderr)
    # Record the push attempt either way: on failure this still advances the
    # throttle window so a broken remote (e.g. missing token) isn't hammered on
    # every single write. last_pull_at is only set where a pull actually ran
    # (above), so a brand-new remote's first auto-pull isn't suppressed here.
    _write_sync_cache(repo, last_push_at=now_iso())
    if push.returncode != 0:
        outputs.append(
            "\nMemHub: push failed. Local memory is committed but not on the remote. "
            "Check credentials/remote and re-run `memhub sync`.\n"
        )
    return "" if quiet else "".join(outputs)


def sync_repo(repo: Path) -> str:
    ensure_repo(repo)
    # Local git config isn't cloned, so register the structured merge driver on
    # each machine before any pull --rebase might need it. Also backfill
    # .gitattributes for repos created before merge support existed.
    ensure_merge_driver_registered(repo)
    if not (repo / ".gitattributes").exists():
        write_text(repo / ".gitattributes", GITATTRIBUTES_CONTENT)
    # Manual sync always runs immediately, ignoring throttle.
    return _sync_now(repo, quiet=False)


def maybe_auto_push(repo: Path) -> str:
    """Auto-push after a write, throttled per-machine. Always a no-op-safe call:
    skips silently when auto_push is off, no remote is set, or the throttle
    window hasn't elapsed. Local memory is already committed by the caller."""
    cfg = load_config(repo)
    sync = cfg.get("sync") or {}
    if not sync.get("auto_push", True):
        return ""
    if not (sync.get("remote") or run_git(repo, ["remote"], check=False).stdout.strip()):
        return ""
    throttle = float(sync.get("push_throttle_seconds", 3600) or 0)
    if _seconds_since(_read_sync_cache(repo).get("last_push_at")) < throttle:
        return ""  # within window — stay local, will push on a later write or manual sync
    ensure_merge_driver_registered(repo)
    return _sync_now(repo, quiet=True)


def maybe_auto_pull(repo: Path) -> str:
    """Auto-pull before a read, throttled per-machine. Returns a human-facing
    warning string only when a pull was attempted and failed; empty otherwise."""
    cfg = load_config(repo)
    sync = cfg.get("sync") or {}
    if not sync.get("auto_pull", True):
        return ""
    if not (sync.get("remote") or run_git(repo, ["remote"], check=False).stdout.strip()):
        return ""
    throttle = float(sync.get("pull_throttle_seconds", 3600) or 0)
    if _seconds_since(_read_sync_cache(repo).get("last_pull_at")) < throttle:
        return ""
    branch = sync.get("branch") or "main"
    ensure_merge_driver_registered(repo)
    if not _remote_has_branch(repo, branch):
        return ""
    # Commit local edits first so rebase has a clean tree.
    commit_all(repo, "memhub: sync local changes")
    pull = run_git_auth(repo, ["pull", "--rebase", "origin", branch], check=False)
    if pull.returncode != 0:
        if (repo / ".git" / "rebase-merge").exists() or (repo / ".git" / "rebase-apply").exists():
            run_git(repo, ["rebase", "--abort"], check=False)
        _write_sync_cache(repo, last_pull_at=now_iso())
        return "MemHub: 远端同步失败，当前上下文可能不是最新（使用本地记忆）。\n"
    _write_sync_cache(repo, last_pull_at=now_iso())
    return ""


def main(argv: list[str] | None = None) -> int:
    load_dotenv_files([Path.cwd() / ".env", Path.home() / ".env"])
    parser = argparse.ArgumentParser(prog="memhub", description="MemHub Protocol v0.1 reference CLI")
    parser.add_argument("--repo", default=os.environ.get("MEMHUB_REPO", "./memhub-data"), help="MemHub repository path")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="Initialize a MemHub repository")
    p_init.add_argument("--name", default="user")
    p_init.add_argument("--role", default="")

    p_context = sub.add_parser("context", help="Print context pack")
    p_context.add_argument("--project", default=None)
    p_context.add_argument("--pack", default="standard", choices=["brief", "standard", "full", "project"])

    p_rem = sub.add_parser("remember", help="Write a memory (default: directly into canonical memory)")
    p_rem.add_argument("content")
    p_rem.add_argument("--type", default="fact")
    p_rem.add_argument("--source", default="manual")
    p_rem.add_argument("--project", default=None)
    p_rem.add_argument("--inbox", action="store_true", help="Capture into the inbox audit buffer instead of writing canonical memory")
    p_rem.add_argument("--no-sync", action="store_true", help="Skip throttled auto-push for this write (stays local)")

    p_inbox = sub.add_parser("inbox", help="Inspect inbox items")
    inbox_sub = p_inbox.add_subparsers(dest="inbox_cmd", required=True)
    p_inbox_list = inbox_sub.add_parser("list", help="List inbox items")
    p_inbox_list.add_argument("--status", default="pending", choices=["pending", "promoted", "all"])
    p_inbox_show = inbox_sub.add_parser("show", help="Show one inbox YAML file")
    p_inbox_show.add_argument("ref")

    p_promote = sub.add_parser("promote", help="Promote inbox items into canonical memory")
    p_promote.add_argument("refs", nargs="*", help="Optional inbox filename/id substrings. Defaults to all pending items.")
    p_promote.add_argument("--dry-run", action="store_true", help="Preview only; this is the default unless --apply is set")
    p_promote.add_argument("--apply", action="store_true", help="Write canonical files and mark inbox items promoted")
    p_promote.add_argument("--status", default="pending", choices=["pending", "all"], help="Inbox status to scan when refs are omitted")
    p_promote.add_argument("--no-sync", action="store_true", help="Skip throttled auto-push after applying (stays local)")

    p_export = sub.add_parser("export", help="Export context")
    p_export.add_argument("target", choices=["chatbot"])
    p_export.add_argument("--project", default=None)

    p_search = sub.add_parser("search", help="Search canonical memory")
    p_search.add_argument("query")
    p_search.add_argument("--type", default=None)
    p_search.add_argument("--project", default=None)
    p_search.add_argument("--limit", type=int, default=20)
    p_search.add_argument("--include-archived", action="store_true", help="Also match archived entries")

    p_forget = sub.add_parser("forget", help="Soft-archive matching canonical memory")
    p_forget.add_argument("query", help="Entry id or content substring")
    p_forget.add_argument("--type", default=None)
    p_forget.add_argument("--project", default=None)
    p_forget.add_argument("--apply", action="store_true", help="Archive matches; default is dry-run preview")
    p_forget.add_argument("--no-sync", action="store_true", help="Skip throttled auto-push after archiving (stays local)")

    p_sync = sub.add_parser("sync", help="Configure or run GitHub/Gitee sync")
    sync_sub = p_sync.add_subparsers(dest="sync_cmd")
    p_sync_setup = sync_sub.add_parser("setup", help="Set up hosted Git sync")
    p_sync_setup.add_argument("provider", choices=["github", "gitee"])
    p_sync_setup.add_argument("--repo-name", default="mymemhub", help="Remote repository name")
    p_sync_setup.add_argument("--owner", default=None, help="Owner/login. Defaults to authenticated account")
    p_sync_setup.add_argument("--token", default=None, help="Provider token. Prefer env vars MEMHUB_GITHUB_TOKEN/MEMHUB_GITEE_TOKEN")
    p_sync_setup.add_argument("--branch", default="main")
    p_sync_setup.add_argument("--public", action="store_true", help="Create public repo instead of private")
    p_sync_setup.add_argument("--no-create", action="store_true", help="Do not call provider API to create repo")
    p_sync_setup.add_argument("--auth", default="oauth", choices=["oauth", "token", "ssh"], help="Git auth mode. OAuth uses GitHub Device Flow or Gitee authorization-code flow")
    p_sync_setup.add_argument("--remote-method", default="https", choices=["https", "ssh"], help="Remote URL style")
    p_sync_setup.add_argument("--client-id", default=None, help="OAuth client id. Or set MEMHUB_GITHUB_CLIENT_ID / MEMHUB_GITEE_CLIENT_ID")
    p_sync_setup.add_argument("--client-secret", default=None, help="Gitee OAuth client secret. Or set MEMHUB_GITEE_CLIENT_SECRET")
    p_sync_setup.add_argument("--scope", default=None, help="OAuth scope. Defaults: GitHub repo; Gitee user_info projects")
    p_sync_setup.add_argument("--redirect-uri", default=None, help="Gitee OAuth redirect URI. Defaults to local callback")
    p_sync_setup.add_argument("--callback-port", type=int, default=8765, help="Local callback port for Gitee OAuth")
    p_sync_setup.add_argument("--no-browser", action="store_true", help="Print OAuth URL/code but do not try to open browser")
    p_sync_setup.add_argument("--manual-code", default=None, help="Gitee OAuth authorization code for manual callback flow")
    p_sync_setup.add_argument("--broker-url", default=None, help="MemHub OAuth Broker base URL for Gitee one-click OAuth. Or set MEMHUB_GITEE_OAUTH_BROKER_URL")
    sync_sub.add_parser("status", help="Show sync config/status")

    sub.add_parser("doctor", help="Diagnose whether automatic memory sync is ready")

    p_onboard = sub.add_parser("onboard", help="First-run setup: authorize, then pull remote memory or seed+push a new repo")
    p_onboard.add_argument("provider", choices=["github", "gitee"])
    p_onboard.add_argument("--repo-name", default="mymemhub", help="Remote repository name")
    p_onboard.add_argument("--name", default="user", help="User name to seed when the remote is empty")
    p_onboard.add_argument("--role", default="", help="User role to seed when the remote is empty")
    p_onboard.add_argument("--owner", default=None, help="Owner/login. Defaults to authenticated account")
    p_onboard.add_argument("--branch", default="main")
    p_onboard.add_argument("--public", action="store_true", help="Create public repo instead of private")
    p_onboard.add_argument("--auth", default="oauth", choices=["oauth", "token", "ssh"], help="Git auth mode")
    p_onboard.add_argument("--no-browser", action="store_true", help="Print OAuth URL but do not open a browser")
    p_onboard.add_argument("--broker-url", default=None, help="Override the MemHub Auth Broker base URL")

    p_merge = sub.add_parser("merge-driver", help=argparse.SUPPRESS)
    p_merge.add_argument("base")
    p_merge.add_argument("ours")
    p_merge.add_argument("theirs")

    args = parser.parse_args(argv)

    if args.cmd == "merge-driver":
        # Invoked by git with temp file paths; no MemHub repo context needed.
        return run_merge_driver(args.base, args.ours, args.theirs)

    repo = Path(args.repo).expanduser().resolve()

    if args.cmd == "init":
        init_repo(repo, name=args.name, role=args.role)
        print(f"Initialized MemHub repository: {repo}")
    elif args.cmd == "context":
        warn = maybe_auto_pull(repo)
        if warn:
            print(warn, end="", file=sys.stderr)
        print(build_context(repo, project=args.project, pack=args.pack), end="")
    elif args.cmd == "remember":
        print(remember(repo, args.content, type_=args.type, source_client=args.source, project=args.project, to_inbox=args.inbox))
        if not args.no_sync:
            out = maybe_auto_push(repo)
            if out.strip():
                print(out, end="", file=sys.stderr)
    elif args.cmd == "inbox":
        if args.inbox_cmd == "list":
            print(inbox_list(repo, status=args.status), end="")
        elif args.inbox_cmd == "show":
            print(inbox_show(repo, args.ref), end="")
    elif args.cmd == "promote":
        refs = args.refs if args.refs else None
        print(promote(repo, refs=refs, apply=args.apply, status=args.status), end="")
        if args.apply and not args.no_sync:
            out = maybe_auto_push(repo)
            if out.strip():
                print(out, end="", file=sys.stderr)
    elif args.cmd == "export":
        out = export_chatbot(repo, project=args.project)
        print(f"Exported chatbot context: {out}")
    elif args.cmd == "search":
        print(search(repo, args.query, type_=args.type, project=args.project, limit=args.limit, include_archived=args.include_archived), end="")
    elif args.cmd == "forget":
        print(forget(repo, args.query, type_=args.type, project=args.project, apply=args.apply), end="")
        if args.apply and not args.no_sync:
            out = maybe_auto_push(repo)
            if out.strip():
                print(out, end="", file=sys.stderr)
    elif args.cmd == "sync":
        if getattr(args, "sync_cmd", None) == "setup":
            print(setup_git_sync(
                repo,
                provider=args.provider,
                repo_name=args.repo_name,
                owner=args.owner,
                token=args.token,
                branch=args.branch,
                private=not args.public,
                create_repo=not args.no_create,
                auth_method=args.auth,
                remote_method=args.remote_method,
                client_id=args.client_id,
                client_secret=args.client_secret,
                scope=args.scope,
                redirect_uri=args.redirect_uri,
                callback_port=args.callback_port,
                no_browser=args.no_browser,
                manual_code=args.manual_code,
                broker_url=args.broker_url,
            ), end="")
        elif getattr(args, "sync_cmd", None) == "status":
            print(sync_status(repo), end="")
        else:
            print(sync_repo(repo), end="")
    elif args.cmd == "doctor":
        print(doctor(repo), end="")
    elif args.cmd == "onboard":
        print(onboard(
            repo,
            provider=args.provider,
            repo_name=args.repo_name,
            name=args.name,
            role=args.role,
            owner=args.owner,
            branch=args.branch,
            private=not args.public,
            auth_method=args.auth,
            no_browser=args.no_browser,
            broker_url=args.broker_url,
        ), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
