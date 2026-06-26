#!/usr/bin/env python3
"""
Discover, deduplicate, and safely share local skills across AI agent hosts.

Examples:
    python3 scripts/skill_sync.py
    python3 scripts/skill_sync.py --status shared,specific --list-names
    python3 scripts/skill_sync.py --diff rapid-ocr
    python3 scripts/skill_sync.py --dedupe --strategy strict
    python3 scripts/skill_sync.py --adopt-root agents
    python3 scripts/skill_sync.py --adopt-root agents --apply
    python3 scripts/skill_sync.py --restore latest
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable


IGNORE_NAMES = {
    ".DS_Store",
    "__pycache__",
    ".venv",
    "node_modules",
    ".git",
    "logs",
    ".pytest_cache",
}
PRIMARY_PLATFORMS = ("agents", "codex", "claude", "opencode", "openclaw")
ALL_PLATFORMS = PRIMARY_PLATFORMS + ("workspace",)
STATUS_ORDER = ("shared", "duplicate", "compatible", "specific", "mixed")
SCRIPT_PATH = Path(__file__).resolve()
RECOMMENDATION_LIMIT = 6
LAYOUT_MANIFEST_KIND = "skill-sync-layout"


@dataclass(frozen=True)
class RootSpec:
    platform: str
    label: str
    path: Path
    link_target: bool


@dataclass(frozen=True)
class SkillEntry:
    name: str
    platform: str
    root_label: str
    path: Path
    resolved_path: Path
    format: str
    portable: bool
    symlinked: bool
    link_target: bool
    content_hash: str | None
    latest_mtime_ns: int


def env_path(name: str, default: str) -> Path:
    return Path(os.environ.get(name, default)).expanduser()


def build_root_specs(workdir: Path) -> list[RootSpec]:
    home = Path.home()
    roots: list[RootSpec] = []

    workspace_skills = (workdir / "skills").resolve()
    if workspace_skills.is_dir():
        roots.append(
            RootSpec(
                platform="workspace",
                label=str(workdir),
                path=workspace_skills,
                link_target=False,
            )
        )

    primary_roots = [
        RootSpec(
            platform="codex",
            label="home",
            path=env_path("SKILL_SYNC_CODEX_ROOT", str(home / ".codex" / "skills")),
            link_target=True,
        ),
        RootSpec(
            platform="agents",
            label="shared",
            path=env_path("SKILL_SYNC_AGENTS_ROOT", str(home / ".agents" / "skills")),
            link_target=True,
        ),
        RootSpec(
            platform="claude",
            label="home",
            path=env_path("SKILL_SYNC_CLAUDE_ROOT", str(home / ".claude" / "skills")),
            link_target=True,
        ),
        RootSpec(
            platform="opencode",
            label="home",
            path=env_path(
                "SKILL_SYNC_OPENCODE_ROOT",
                str(home / ".config" / "opencode" / "skills"),
            ),
            link_target=True,
        ),
        RootSpec(
            platform="openclaw",
            label="home",
            path=env_path(
                "SKILL_SYNC_OPENCLAW_ROOT",
                str(home / ".openclaw" / "skills"),
            ),
            link_target=True,
        ),
    ]
    roots.extend(root for root in primary_roots if root.path.is_dir())

    claude_vendor = env_path(
        "SKILL_SYNC_CLAUDE_VENDOR_ROOT",
        str(home / ".claude" / "skills" / "anthropic-skills" / "skills"),
    )
    if claude_vendor.is_dir():
        roots.append(
            RootSpec(
                platform="claude",
                label="vendor",
                path=claude_vendor,
                link_target=False,
            )
        )

    openclaw_extensions_root = env_path(
        "SKILL_SYNC_OPENCLAW_EXTENSIONS_ROOT",
        str(home / ".openclaw" / "extensions"),
    )
    if openclaw_extensions_root.is_dir():
        for skills_root in sorted(openclaw_extensions_root.glob("*/skills")):
            roots.append(
                RootSpec(
                    platform="openclaw",
                    label=f"plugin:{skills_root.parent.name}",
                    path=skills_root,
                    link_target=False,
                )
            )

    return roots


def iter_root_entries(root: RootSpec) -> Iterable[Path]:
    try:
        children = sorted(root.path.iterdir(), key=lambda item: item.name.lower())
    except OSError:
        return []
    return [child for child in children if not child.name.startswith(".")]


def hash_file(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def latest_mtime_ns(path: Path) -> int:
    try:
        latest = path.lstat().st_mtime_ns
    except OSError:
        return 0

    if not path.is_dir():
        return latest

    for current_root, dirnames, filenames in os.walk(
        path, topdown=True, followlinks=False
    ):
        current = Path(current_root)
        dirnames[:] = sorted(name for name in dirnames if name not in IGNORE_NAMES)
        filenames = sorted(name for name in filenames if name not in IGNORE_NAMES)

        for name in dirnames:
            try:
                latest = max(latest, (current / name).lstat().st_mtime_ns)
            except OSError:
                continue
        for name in filenames:
            try:
                latest = max(latest, (current / name).lstat().st_mtime_ns)
            except OSError:
                continue

    return latest


def hash_directory(path: Path) -> str | None:
    try:
        digest = hashlib.sha256()
        digest.update(b"skill-sync-directory-v2\n")
        for current_root, dirnames, filenames in os.walk(
            path, topdown=True, followlinks=False
        ):
            current = Path(current_root)
            keep_dirs: list[str] = []

            for name in sorted(name for name in dirnames if name not in IGNORE_NAMES):
                full_path = current / name
                relative = full_path.relative_to(path).as_posix()
                if full_path.is_symlink():
                    digest.update(
                        f"L {relative} -> {os.readlink(full_path)}\n".encode("utf-8")
                    )
                else:
                    digest.update(f"D {relative}\n".encode("utf-8"))
                    keep_dirs.append(name)
            dirnames[:] = keep_dirs

            for name in sorted(name for name in filenames if name not in IGNORE_NAMES):
                full_path = current / name
                relative = full_path.relative_to(path).as_posix()
                if full_path.is_symlink():
                    digest.update(
                        f"L {relative} -> {os.readlink(full_path)}\n".encode("utf-8")
                    )
                    continue
                digest.update(f"F {relative}\n".encode("utf-8"))
                digest.update(full_path.read_bytes())
                digest.update(b"\n")
    except OSError:
        return None

    return digest.hexdigest()


def analyze_path(
    path: Path,
    entry_format: str,
    portable: bool,
    cache: dict[str, tuple[str | None, int]],
) -> tuple[str | None, int]:
    cache_key = f"{path}:{entry_format}:{portable}"
    if cache_key in cache:
        return cache[cache_key]

    if portable and path.is_dir():
        result = (hash_directory(path), latest_mtime_ns(path))
    elif path.is_file():
        result = (hash_file(path), latest_mtime_ns(path))
    else:
        result = (None, latest_mtime_ns(path))

    cache[cache_key] = result
    return result


def detect_entry(path: Path) -> tuple[str, bool] | None:
    if path.is_file() and path.suffix == ".skill":
        return ("claude-skill-file", False)

    if not path.is_dir():
        return None
    if (path / "SKILL.md").is_file():
        return ("skill-md", True)
    if (path / "_meta.json").is_file():
        return ("openclaw-meta", False)

    embedded_skill_files = sorted(path.glob("*.skill"))
    if embedded_skill_files:
        return ("claude-skill-bundle", False)
    if (path / "skills").is_dir():
        return None

    try:
        has_visible_content = any(not child.name.startswith(".") for child in path.iterdir())
    except OSError:
        has_visible_content = False
    if has_visible_content:
        return ("directory-unknown", False)
    return None


def discover_skills(roots: list[RootSpec], skill_filter: set[str]) -> list[SkillEntry]:
    entries: list[SkillEntry] = []
    cache: dict[str, tuple[str | None, int]] = {}

    for root in roots:
        for path in iter_root_entries(root):
            detected = detect_entry(path)
            if detected is None:
                continue

            name = path.stem if path.is_file() else path.name
            if skill_filter and name not in skill_filter:
                continue

            entry_format, portable = detected
            try:
                resolved_path = path.resolve(strict=False)
            except OSError:
                resolved_path = path

            content_hash, last_mtime = analyze_path(
                resolved_path, entry_format, portable, cache
            )

            entries.append(
                SkillEntry(
                    name=name,
                    platform=root.platform,
                    root_label=root.label,
                    path=path,
                    resolved_path=resolved_path,
                    format=entry_format,
                    portable=portable,
                    symlinked=path.is_symlink(),
                    link_target=root.link_target,
                    content_hash=content_hash,
                    latest_mtime_ns=last_mtime,
                )
            )

    return entries


def classify_group(entries: list[SkillEntry]) -> dict:
    portable_entries = [entry for entry in entries if entry.portable]
    resolved_paths = {str(entry.resolved_path) for entry in entries}
    content_hashes = {
        entry.content_hash for entry in portable_entries if entry.content_hash is not None
    }
    platforms = sorted({entry.platform for entry in entries})

    if len(entries) == 1:
        status = "specific"
        reason = "only found on one host"
    elif len(resolved_paths) == 1:
        status = "shared"
        reason = "all hosts point to the same real path"
    elif portable_entries and len(portable_entries) == len(entries) and len(content_hashes) == 1:
        status = "duplicate"
        reason = "portable skill content matches across multiple real paths"
    elif portable_entries and len(portable_entries) == len(entries):
        status = "compatible"
        reason = "portable skill exists on multiple hosts but content differs"
    else:
        status = "mixed"
        reason = "same skill name exists with incompatible formats or host-specific content"

    return {"status": status, "reason": reason, "platforms": platforms}


def should_use_group_for_canonical(status: str, strategy: str, allow_specific: bool) -> bool:
    if allow_specific and status == "specific":
        return True
    if strategy == "strict":
        return status in {"shared", "duplicate"}
    return status in {"shared", "duplicate", "compatible"}


def choose_canonical_source(
    entries: list[SkillEntry],
    source_order: list[str],
    strategy: str,
    allow_specific: bool = False,
) -> dict | None:
    summary = classify_group(entries)
    if not should_use_group_for_canonical(summary["status"], strategy, allow_specific):
        return None

    portable_entries = [entry for entry in entries if entry.portable]
    if not portable_entries:
        return None

    order_index = {platform: index for index, platform in enumerate(source_order)}
    grouped_by_real_path: dict[str, list[SkillEntry]] = defaultdict(list)
    for entry in portable_entries:
        grouped_by_real_path[str(entry.resolved_path)].append(entry)

    candidates: list[dict] = []
    for resolved_path, candidate_entries in grouped_by_real_path.items():
        representative = sorted(
            candidate_entries,
            key=lambda entry: (
                0 if not entry.symlinked else 1,
                order_index.get(entry.platform, len(order_index) + 1),
                -entry.latest_mtime_ns,
                str(entry.path),
            ),
        )[0]
        candidates.append(
            {
                "display_path": str(representative.path),
                "source_path": resolved_path,
                "resolved_path": resolved_path,
                "platform": representative.platform,
                "root_label": representative.root_label,
                "shared_count": len(candidate_entries),
                "content_hash": representative.content_hash,
                "latest_mtime_ns": max(
                    entry.latest_mtime_ns for entry in candidate_entries
                ),
                "platform_rank": min(
                    order_index.get(entry.platform, len(order_index) + 1)
                    for entry in candidate_entries
                ),
            }
        )

    if not candidates:
        return None

    if strategy == "strict":
        selected = sorted(
            candidates,
            key=lambda item: (
                -item["shared_count"],
                item["platform_rank"],
                -item["latest_mtime_ns"],
                item["source_path"],
            ),
        )[0]
        selected_by = "strict: shared-count then source-order"
    else:
        selected = sorted(
            candidates,
            key=lambda item: (
                -item["latest_mtime_ns"],
                -item["shared_count"],
                item["platform_rank"],
                item["source_path"],
            ),
        )[0]
        selected_by = f"{strategy}: latest-mtime then shared-count"

    selected["selected_by"] = selected_by
    selected["group_status"] = summary["status"]
    return selected


def build_missing_link_plan(
    grouped_entries: dict[str, list[SkillEntry]],
    roots: list[RootSpec],
    source_order: list[str],
    strategy: str,
) -> list[dict]:
    primary_roots = {
        root.platform: root
        for root in roots
        if root.link_target and root.platform in PRIMARY_PLATFORMS
    }
    plans: list[dict] = []

    for name, entries in sorted(grouped_entries.items()):
        source = choose_canonical_source(entries, source_order, strategy, allow_specific=True)
        if source is None:
            continue

        existing_platforms = {entry.platform for entry in entries}
        destinations: list[dict] = []
        for platform in PRIMARY_PLATFORMS:
            if platform in existing_platforms:
                continue
            destination_root = primary_roots.get(platform)
            if destination_root is None:
                continue

            destination_path = destination_root.path / name
            if destination_path.exists() or destination_path.is_symlink():
                continue
            destinations.append({"platform": platform, "path": str(destination_path)})

        if destinations:
            plans.append(
                {
                    "name": name,
                    "group_status": source["group_status"],
                    "source_platform": source["platform"],
                    "source_root_label": source["root_label"],
                    "source_display_path": source["display_path"],
                    "source_path": source["source_path"],
                    "selected_by": source["selected_by"],
                    "destinations": destinations,
                }
            )

    return plans


def can_replace_entry(entry: SkillEntry, strategy: str) -> bool:
    return entry.portable and (entry.link_target or strategy == "trust-high")


def build_dedupe_plan(
    grouped_entries: dict[str, list[SkillEntry]],
    source_order: list[str],
    strategy: str,
) -> list[dict]:
    plans: list[dict] = []

    for name, entries in sorted(grouped_entries.items()):
        if len(entries) < 2:
            continue
        source = choose_canonical_source(entries, source_order, strategy, allow_specific=False)
        if source is None:
            continue

        replacements: list[dict] = []
        for entry in sorted(entries, key=lambda item: (item.platform, item.root_label, str(item.path))):
            if not can_replace_entry(entry, strategy):
                continue
            if str(entry.resolved_path) == source["resolved_path"]:
                continue
            replacements.append(
                {
                    "platform": entry.platform,
                    "root_label": entry.root_label,
                    "path": str(entry.path),
                    "resolved_path": str(entry.resolved_path),
                    "symlinked": entry.symlinked,
                }
            )

        if replacements:
            plans.append(
                {
                    "name": name,
                    "group_status": source["group_status"],
                    "source_platform": source["platform"],
                    "source_root_label": source["root_label"],
                    "source_display_path": source["display_path"],
                    "source_path": source["source_path"],
                    "selected_by": source["selected_by"],
                    "replacements": replacements,
                }
            )

    return plans


def build_health_summary(groups: list[dict]) -> dict:
    counts = Counter(group["status"] for group in groups)
    penalty = (
        counts.get("duplicate", 0) * 2
        + counts.get("compatible", 0) * 7
        + counts.get("mixed", 0) * 12
    )
    score = max(0, 100 - penalty)
    if score >= 90:
        label = "excellent"
    elif score >= 75:
        label = "good"
    elif score >= 55:
        label = "fair"
    else:
        label = "risky"

    total = len(groups) or 1
    shared_ratio = round(counts.get("shared", 0) / total, 3)
    review_count = counts.get("compatible", 0) + counts.get("mixed", 0)
    return {
        "score": score,
        "label": label,
        "shared_ratio": shared_ratio,
        "review_count": review_count,
        "duplicate_count": counts.get("duplicate", 0),
    }


def build_recommendations(report: dict) -> list[dict]:
    recommendations: list[dict] = []
    groups = report["groups"]
    compatible = [group for group in groups if group["status"] == "compatible"]
    mixed = [group for group in groups if group["status"] == "mixed"]
    duplicates = [group for group in groups if group["status"] == "duplicate"]
    specific_with_links = [
        plan for plan in report["planned_links"] if plan["group_status"] == "specific"
    ]

    if compatible:
        recommendations.append(
            {
                "priority": "high",
                "title": f"Review {len(compatible)} compatible skills before dedupe",
                "why": "These skills are portable but differ in content across hosts.",
                "command": (
                    "python3 scripts/skill_sync.py --status compatible --list-names"
                ),
            }
        )
        recommendations.append(
            {
                "priority": "high",
                "title": "Inspect one compatible skill with file-level diff",
                "why": "Use diff to verify which copy should become the canonical source.",
                "command": (
                    f"python3 scripts/skill_sync.py --diff {compatible[0]['name']}"
                ),
            }
        )

    if mixed:
        recommendations.append(
            {
                "priority": "high",
                "title": f"Manually audit {len(mixed)} mixed skills",
                "why": "Mixed groups contain incompatible formats or host-specific layouts.",
                "command": "python3 scripts/skill_sync.py --status mixed --list-names",
            }
        )

    if duplicates:
        recommendations.append(
            {
                "priority": "medium",
                "title": f"Deduplicate {len(duplicates)} identical multi-host skills",
                "why": "These groups have matching portable content and can usually be converged safely.",
                "command": "python3 scripts/skill_sync.py --dedupe --strategy strict",
            }
        )

    if specific_with_links:
        recommendations.append(
            {
                "priority": "medium",
                "title": f"Propagate {len(specific_with_links)} host-specific portable skills",
                "why": "These skills exist on only one host and can be linked into missing hosts.",
                "command": "python3 scripts/skill_sync.py --sync-missing --strategy prefer-latest",
            }
        )

    if report.get("adopt_root"):
        recommendations.append(
            {
                "priority": "medium",
                "title": f"Adopt {report['adopt_root']} as the canonical root",
                "why": "This run prefers one shared source of truth for future dedupe and sync operations.",
                "command": (
                    f"python3 scripts/skill_sync.py --adopt-root {report['adopt_root']}"
                ),
            }
        )
    else:
        recommendations.append(
            {
                "priority": "low",
                "title": "Preview a single-root convergence plan",
                "why": "Adopting one canonical root makes long-term skill maintenance easier.",
                "command": "python3 scripts/skill_sync.py --adopt-root agents",
            }
        )

    return recommendations[:RECOMMENDATION_LIMIT]


def enrich_report(report: dict) -> dict:
    enriched = dict(report)
    enriched["health"] = build_health_summary(enriched["groups"])
    enriched["recommended_actions"] = build_recommendations(enriched)
    return enriched


def group_entries_from_report(group: dict) -> list[SkillEntry]:
    entries: list[SkillEntry] = []
    for item in group["entries"]:
        entries.append(
            SkillEntry(
                name=group["name"],
                platform=item["platform"],
                root_label=item["root_label"],
                path=Path(item["path"]),
                resolved_path=Path(item["resolved_path"]),
                format=item["format"],
                portable=item["portable"],
                symlinked=item["symlinked"],
                link_target=item["link_target"],
                content_hash=item["content_hash"],
                latest_mtime_ns=item["latest_mtime_ns"],
            )
        )
    return entries


def build_report(
    entries: list[SkillEntry],
    roots: list[RootSpec],
    source_order: list[str],
    strategy: str,
    adopt_root: str | None,
) -> dict:
    grouped_entries: dict[str, list[SkillEntry]] = defaultdict(list)
    for entry in entries:
        grouped_entries[entry.name].append(entry)

    groups: list[dict] = []
    for name in sorted(grouped_entries):
        entries_for_name = sorted(
            grouped_entries[name],
            key=lambda entry: (entry.platform, entry.root_label, str(entry.path)),
        )
        summary = classify_group(entries_for_name)
        groups.append(
            {
                "name": name,
                "status": summary["status"],
                "reason": summary["reason"],
                "platforms": summary["platforms"],
                "entries": [
                    {
                        "platform": entry.platform,
                        "root_label": entry.root_label,
                        "path": str(entry.path),
                        "resolved_path": str(entry.resolved_path),
                        "format": entry.format,
                        "portable": entry.portable,
                        "symlinked": entry.symlinked,
                        "link_target": entry.link_target,
                        "content_hash": entry.content_hash,
                        "latest_mtime_ns": entry.latest_mtime_ns,
                    }
                    for entry in entries_for_name
                ],
            }
        )

    status_counts: dict[str, int] = defaultdict(int)
    for group in groups:
        status_counts[group["status"]] += 1

    planned_links = build_missing_link_plan(grouped_entries, roots, source_order, strategy)
    dedupe_plan = build_dedupe_plan(grouped_entries, source_order, strategy)

    report = {
        "roots": [
            {
                "platform": root.platform,
                "label": root.label,
                "path": str(root.path),
                "link_target": root.link_target,
            }
            for root in roots
        ],
        "summary": {
            "total_skills": len(groups),
            "status_counts": {status: status_counts.get(status, 0) for status in STATUS_ORDER},
            "discovered_entries": len(entries),
            "planned_missing_links": sum(len(item["destinations"]) for item in planned_links),
            "planned_dedupe_replacements": sum(len(item["replacements"]) for item in dedupe_plan),
        },
        "groups": groups,
        "planned_links": planned_links,
        "dedupe_plan": dedupe_plan,
        "strategy": strategy,
        "source_order": source_order,
        "adopt_root": adopt_root,
    }
    return enrich_report(report)


def filter_report_groups(report: dict, statuses: set[str]) -> dict:
    if not statuses:
        return report

    groups = [group for group in report["groups"] if group["status"] in statuses]
    allowed_names = {group["name"] for group in groups}
    status_counts = Counter(group["status"] for group in groups)

    filtered = dict(report)
    filtered["groups"] = groups
    filtered["planned_links"] = [
        plan for plan in report["planned_links"] if plan["name"] in allowed_names
    ]
    filtered["dedupe_plan"] = [
        plan for plan in report["dedupe_plan"] if plan["name"] in allowed_names
    ]
    filtered["summary"] = {
        "total_skills": len(groups),
        "status_counts": {status: status_counts.get(status, 0) for status in STATUS_ORDER},
        "discovered_entries": sum(len(group["entries"]) for group in groups),
        "planned_missing_links": sum(
            len(item["destinations"]) for item in filtered["planned_links"]
        ),
        "planned_dedupe_replacements": sum(
            len(item["replacements"]) for item in filtered["dedupe_plan"]
        ),
    }
    filtered["status_filter"] = sorted(statuses)
    return enrich_report(filtered)


def parse_status_filters(raw_filters: list[str]) -> set[str]:
    if not raw_filters:
        return set()

    statuses: set[str] = set()
    for raw in raw_filters:
        for part in raw.split(","):
            value = part.strip()
            if not value:
                continue
            if value not in STATUS_ORDER:
                raise SystemExit(
                    f"Invalid status filter: {value}. "
                    f"Valid values: {', '.join(STATUS_ORDER)}"
                )
            statuses.add(value)
    return statuses


def reorder_source_order(raw_order: str, prefer_root: str | None) -> list[str]:
    order = [platform.strip() for platform in raw_order.split(",") if platform.strip()]
    seen: set[str] = set()
    normalized: list[str] = []
    for platform in order:
        if platform not in ALL_PLATFORMS:
            raise SystemExit(
                f"Invalid platform in --source-order: {platform}. "
                f"Valid values: {', '.join(ALL_PLATFORMS)}"
            )
        if platform not in seen:
            normalized.append(platform)
            seen.add(platform)

    for platform in ALL_PLATFORMS:
        if platform not in seen:
            normalized.append(platform)

    if prefer_root and prefer_root in normalized:
        normalized.remove(prefer_root)
        normalized.insert(0, prefer_root)

    return normalized


def iter_relative_files(path: Path) -> dict[str, dict]:
    inventory: dict[str, dict] = {}
    if path.is_file():
        inventory[path.name] = {
            "kind": "file",
            "hash": hash_file(path),
            "target": None,
        }
        return inventory

    if not path.is_dir():
        return inventory

    for current_root, dirnames, filenames in os.walk(path, topdown=True, followlinks=False):
        current = Path(current_root)
        dirnames[:] = sorted(name for name in dirnames if name not in IGNORE_NAMES)
        filenames = sorted(name for name in filenames if name not in IGNORE_NAMES)

        for name in dirnames:
            full_path = current / name
            relative = full_path.relative_to(path).as_posix()
            if full_path.is_symlink():
                inventory[relative] = {
                    "kind": "symlink",
                    "hash": None,
                    "target": os.readlink(full_path),
                }
            else:
                inventory[relative] = {"kind": "dir", "hash": None, "target": None}

        for name in filenames:
            full_path = current / name
            relative = full_path.relative_to(path).as_posix()
            if full_path.is_symlink():
                inventory[relative] = {
                    "kind": "symlink",
                    "hash": None,
                    "target": os.readlink(full_path),
                }
            else:
                inventory[relative] = {
                    "kind": "file",
                    "hash": hash_file(full_path),
                    "target": None,
                }
    return inventory


def diff_inventories(base: dict[str, dict], other: dict[str, dict]) -> dict:
    base_keys = set(base)
    other_keys = set(other)
    added = sorted(other_keys - base_keys)
    removed = sorted(base_keys - other_keys)
    changed: list[str] = []
    for key in sorted(base_keys & other_keys):
        if base[key] != other[key]:
            changed.append(key)
    return {
        "added": added,
        "removed": removed,
        "changed": changed,
        "same": len(base_keys & other_keys) - len(changed),
    }


def build_skill_diff(
    entries: list[SkillEntry],
    skill_name: str,
    source_order: list[str],
    strategy: str,
) -> dict:
    skill_entries = [entry for entry in entries if entry.name == skill_name]
    if not skill_entries:
        raise SystemExit(f"Skill not found: {skill_name}")

    summary = classify_group(skill_entries)
    canonical = choose_canonical_source(
        skill_entries, source_order, strategy, allow_specific=True
    )
    if canonical is None:
        canonical = choose_canonical_source(
            skill_entries, source_order, "prefer-latest", allow_specific=True
        )
    portable_entries = [entry for entry in skill_entries if entry.portable]
    if not portable_entries:
        raise SystemExit(f"Skill is not portable and cannot be diffed: {skill_name}")

    unique_entries: list[SkillEntry] = []
    seen_paths: set[str] = set()
    for entry in sorted(
        portable_entries,
        key=lambda item: (item.platform, item.root_label, str(item.path)),
    ):
        resolved_key = str(entry.resolved_path)
        if resolved_key in seen_paths:
            continue
        unique_entries.append(entry)
        seen_paths.add(resolved_key)

    if canonical is None:
        canonical_entry = unique_entries[0]
        canonical_info = {
            "platform": canonical_entry.platform,
            "root_label": canonical_entry.root_label,
            "path": str(canonical_entry.path),
            "resolved_path": str(canonical_entry.resolved_path),
            "selected_by": "fallback:first-portable-entry",
        }
    else:
        canonical_entry = next(
            entry
            for entry in unique_entries
            if str(entry.resolved_path) == canonical["resolved_path"]
        )
        canonical_info = {
            "platform": canonical["platform"],
            "root_label": canonical["root_label"],
            "path": canonical["display_path"],
            "resolved_path": canonical["resolved_path"],
            "selected_by": canonical["selected_by"],
        }

    canonical_inventory = iter_relative_files(canonical_entry.resolved_path)
    comparisons: list[dict] = []
    for entry in unique_entries:
        if str(entry.resolved_path) == str(canonical_entry.resolved_path):
            continue
        delta = diff_inventories(canonical_inventory, iter_relative_files(entry.resolved_path))
        comparisons.append(
            {
                "platform": entry.platform,
                "root_label": entry.root_label,
                "path": str(entry.path),
                "resolved_path": str(entry.resolved_path),
                "added": delta["added"],
                "removed": delta["removed"],
                "changed": delta["changed"],
                "summary": {
                    "added": len(delta["added"]),
                    "removed": len(delta["removed"]),
                    "changed": len(delta["changed"]),
                    "same": delta["same"],
                },
            }
        )

    return {
        "skill": skill_name,
        "status": summary["status"],
        "reason": summary["reason"],
        "canonical": canonical_info,
        "comparisons": comparisons,
    }


def build_layout_manifest(report: dict) -> dict:
    planned_links_by_name = {item["name"]: item for item in report["planned_links"]}
    roots_by_platform: dict[str, list[str]] = defaultdict(list)
    for root in report["roots"]:
        roots_by_platform[root["platform"]].append(root["path"])

    skills: list[dict] = []
    for group in report["groups"]:
        entries = group_entries_from_report(group)
        portable = all(entry.portable for entry in entries) and bool(entries)
        canonical = None
        if portable:
            canonical = choose_canonical_source(
                entries,
                report["source_order"],
                report["strategy"],
                allow_specific=True,
            )

        existing_primary_platforms = sorted(
            {entry.platform for entry in entries if entry.platform in PRIMARY_PLATFORMS}
        )
        desired_platforms = set(existing_primary_platforms)
        planned_links = planned_links_by_name.get(group["name"])
        if planned_links:
            desired_platforms.update(
                destination["platform"] for destination in planned_links["destinations"]
            )

        skills.append(
            {
                "name": group["name"],
                "status": group["status"],
                "reason": group["reason"],
                "portable": portable,
                "importable": portable and canonical is not None,
                "existing_platforms": existing_primary_platforms,
                "desired_platforms": sorted(desired_platforms),
                "canonical": (
                    {
                        "platform": canonical["platform"],
                        "root_label": canonical["root_label"],
                        "path": canonical["display_path"],
                        "resolved_path": canonical["resolved_path"],
                        "selected_by": canonical["selected_by"],
                    }
                    if canonical is not None
                    else None
                ),
            }
        )

    importable_count = sum(1 for skill in skills if skill["importable"])
    desired_placements = sum(len(skill["desired_platforms"]) for skill in skills)
    return {
        "kind": LAYOUT_MANIFEST_KIND,
        "version": 1,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "strategy": report["strategy"],
        "source_order": report["source_order"],
        "adopt_root": report.get("adopt_root"),
        "roots": roots_by_platform,
        "summary": {
            "total_skills": len(skills),
            "importable_skills": importable_count,
            "desired_placements": desired_placements,
            "status_counts": report["summary"]["status_counts"],
        },
        "skills": skills,
    }


def build_operations(report: dict, sync_missing: bool, dedupe: bool) -> list[dict]:
    operations: list[dict] = []

    if dedupe:
        for plan in report["dedupe_plan"]:
            for replacement in plan["replacements"]:
                operations.append(
                    {
                        "action": "replace_with_symlink",
                        "name": plan["name"],
                        "strategy": report["strategy"],
                        "path": replacement["path"],
                        "target_path": plan["source_path"],
                        "target_is_directory": True,
                    }
                )

    if sync_missing:
        for plan in report["planned_links"]:
            for destination in plan["destinations"]:
                operations.append(
                    {
                        "action": "create_symlink",
                        "name": plan["name"],
                        "strategy": report["strategy"],
                        "path": destination["path"],
                        "target_path": plan["source_path"],
                        "target_is_directory": True,
                    }
                )

    return operations


def make_run_id(backup_root: Path) -> str:
    base = datetime.now().strftime("%Y%m%d-%H%M%S")
    candidate = base
    suffix = 1
    while (backup_root / candidate).exists():
        suffix += 1
        candidate = f"{base}-{suffix:02d}"
    return candidate


def absolute_to_backup_path(run_dir: Path, original_path: Path) -> Path:
    absolute = Path(os.path.abspath(str(original_path.expanduser())))
    relative = Path(str(absolute).lstrip("/"))
    return run_dir / "originals" / relative


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def update_latest_pointer(backup_root: Path, run_dir: Path) -> None:
    latest = backup_root / "latest"
    try:
        if latest.is_symlink() or latest.is_file():
            latest.unlink()
        elif latest.is_dir():
            return
    except OSError:
        return

    try:
        latest.symlink_to(run_dir, target_is_directory=True)
    except OSError:
        return


def apply_operations(operations: list[dict], backup_root: Path) -> dict | None:
    if not operations:
        return None

    backup_root.mkdir(parents=True, exist_ok=True)
    run_id = make_run_id(backup_root)
    run_dir = backup_root / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    manifest = {
        "version": 1,
        "run_id": run_id,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "backup_root": str(backup_root),
        "run_dir": str(run_dir),
        "actions": [],
    }
    manifest_path = run_dir / "manifest.json"
    write_json(manifest_path, manifest)

    for operation in operations:
        destination = Path(operation["path"])
        target_path = Path(operation["target_path"])
        action_record = dict(operation)
        action_record["target_path"] = str(target_path)

        if operation["action"] == "replace_with_symlink":
            backup_path = absolute_to_backup_path(run_dir, destination)
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(destination), str(backup_path))
            destination.symlink_to(
                target_path, target_is_directory=bool(operation["target_is_directory"])
            )
            action_record["backup_path"] = str(backup_path)
        elif operation["action"] == "create_symlink":
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.symlink_to(
                target_path, target_is_directory=bool(operation["target_is_directory"])
            )
        else:
            raise ValueError(f"Unsupported action: {operation['action']}")

        manifest["actions"].append(action_record)
        write_json(manifest_path, manifest)

    update_latest_pointer(backup_root, run_dir)
    return manifest


def resolve_run_dir(backup_root: Path, run_id: str) -> Path:
    if run_id == "latest":
        latest = backup_root / "latest"
        if latest.is_symlink():
            return latest.resolve(strict=False)
        raise SystemExit("No latest backup run is available")

    run_dir = backup_root / run_id
    if not run_dir.is_dir():
        raise SystemExit(f"Backup run not found: {run_id}")
    return run_dir


def restore_run(run_dir: Path, apply: bool) -> dict:
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.is_file():
        raise SystemExit(f"Missing manifest: {manifest_path}")

    manifest = read_json(manifest_path)
    actions = manifest.get("actions", [])
    if not apply:
        return manifest

    for action in reversed(actions):
        destination = Path(action["path"])
        if destination.is_symlink():
            destination.unlink()
        elif destination.exists():
            raise SystemExit(
                f"Restore blocked because destination is no longer a symlink: {destination}"
            )

        backup_path = action.get("backup_path")
        if backup_path:
            source_backup = Path(backup_path)
            if not source_backup.exists() and not source_backup.is_symlink():
                raise SystemExit(f"Missing backup payload: {source_backup}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source_backup), str(destination))

    manifest["restored_at"] = datetime.now().isoformat(timespec="seconds")
    write_json(manifest_path, manifest)
    return manifest


def load_layout_manifest(path: Path) -> dict:
    manifest = read_json(path)
    if manifest.get("kind") != LAYOUT_MANIFEST_KIND:
        raise SystemExit(f"Unsupported manifest kind in {path}")
    if manifest.get("version") != 1:
        raise SystemExit(f"Unsupported manifest version in {path}")
    return manifest


def find_manifest_source_entry(
    skill_spec: dict,
    grouped_entries: dict[str, list[SkillEntry]],
    source_order: list[str],
) -> SkillEntry | None:
    entries = grouped_entries.get(skill_spec["name"], [])
    if not entries:
        return None

    portable_entries = [entry for entry in entries if entry.portable]
    if not portable_entries:
        return None

    canonical_spec = skill_spec.get("canonical") or {}
    canonical_platform = canonical_spec.get("platform")
    canonical_root_label = canonical_spec.get("root_label")
    exact_matches = [
        entry
        for entry in portable_entries
        if entry.platform == canonical_platform and entry.root_label == canonical_root_label
    ]
    if exact_matches:
        return sorted(
            exact_matches,
            key=lambda entry: (0 if not entry.symlinked else 1, -entry.latest_mtime_ns),
        )[0]

    platform_matches = [
        entry for entry in portable_entries if entry.platform == canonical_platform
    ]
    if platform_matches:
        return sorted(
            platform_matches,
            key=lambda entry: (0 if not entry.symlinked else 1, -entry.latest_mtime_ns),
        )[0]

    canonical = choose_canonical_source(
        portable_entries, source_order, "prefer-latest", allow_specific=True
    )
    if canonical is None:
        return None

    resolved_path = canonical["resolved_path"]
    return next(
        (entry for entry in portable_entries if str(entry.resolved_path) == resolved_path),
        portable_entries[0],
    )


def build_import_plan(
    manifest: dict,
    roots: list[RootSpec],
    entries: list[SkillEntry],
    source_order: list[str],
) -> dict:
    grouped_entries: dict[str, list[SkillEntry]] = defaultdict(list)
    for entry in entries:
        grouped_entries[entry.name].append(entry)

    primary_roots = {
        root.platform: root
        for root in roots
        if root.link_target and root.platform in PRIMARY_PLATFORMS
    }

    operations: list[dict] = []
    issues: list[dict] = []
    unchanged: list[dict] = []

    for skill_spec in manifest["skills"]:
        if not skill_spec.get("importable"):
            issues.append(
                {
                    "type": "not_importable",
                    "name": skill_spec["name"],
                    "detail": skill_spec["status"],
                }
            )
            continue

        source_entry = find_manifest_source_entry(skill_spec, grouped_entries, source_order)
        if source_entry is None:
            issues.append(
                {
                    "type": "missing_source",
                    "name": skill_spec["name"],
                    "detail": skill_spec.get("canonical", {}).get("platform"),
                }
            )
            continue

        source_target = str(source_entry.resolved_path)
        source_path = str(source_entry.path)
        for platform in skill_spec.get("desired_platforms", []):
            if platform not in PRIMARY_PLATFORMS:
                continue

            root = primary_roots.get(platform)
            if root is None:
                issues.append(
                    {
                        "type": "missing_root",
                        "name": skill_spec["name"],
                        "detail": platform,
                    }
                )
                continue

            destination = root.path / skill_spec["name"]
            destination_key = str(destination)
            if destination_key == source_path or str(destination.resolve(strict=False)) == source_target:
                unchanged.append(
                    {
                        "name": skill_spec["name"],
                        "platform": platform,
                        "path": destination_key,
                        "state": "already_canonical",
                    }
                )
                continue

            if destination.exists() or destination.is_symlink():
                try:
                    current_target = str(destination.resolve(strict=False))
                except OSError:
                    current_target = destination_key
                if current_target == source_target:
                    unchanged.append(
                        {
                            "name": skill_spec["name"],
                            "platform": platform,
                            "path": destination_key,
                            "state": "already_linked",
                        }
                    )
                    continue
                operations.append(
                    {
                        "action": "replace_with_symlink",
                        "name": skill_spec["name"],
                        "strategy": manifest.get("strategy", "import-manifest"),
                        "path": destination_key,
                        "target_path": source_target,
                        "target_is_directory": True,
                    }
                )
                continue

            operations.append(
                {
                    "action": "create_symlink",
                    "name": skill_spec["name"],
                    "strategy": manifest.get("strategy", "import-manifest"),
                    "path": destination_key,
                    "target_path": source_target,
                    "target_is_directory": True,
                }
            )

    return {
        "kind": manifest["kind"],
        "version": manifest["version"],
        "generated_at": manifest["generated_at"],
        "strategy": manifest["strategy"],
        "adopt_root": manifest.get("adopt_root"),
        "summary": {
            "recorded_skills": manifest["summary"]["total_skills"],
            "importable_skills": manifest["summary"]["importable_skills"],
            "desired_placements": manifest["summary"]["desired_placements"],
            "planned_operations": len(operations),
            "unchanged": len(unchanged),
            "issues": len(issues),
        },
        "operations": operations,
        "issues": issues,
        "unchanged": unchanged,
    }


def format_recommendations(report: dict) -> list[str]:
    lines: list[str] = []
    for item in report.get("recommended_actions", []):
        lines.append(f"- [{item['priority']}] {item['title']}")
        lines.append(f"  why: {item['why']}")
        lines.append(f"  try: {item['command']}")
    return lines


def format_text(report: dict, sync_missing: bool, dedupe: bool, apply: bool) -> str:
    lines: list[str] = []
    summary = report["summary"]
    health = report["health"]

    lines.append(
        f"Discovered {summary['total_skills']} unique skills from "
        f"{summary['discovered_entries']} installs."
    )
    lines.append(f"Strategy: {report['strategy']}")
    if report.get("status_filter"):
        lines.append("Status filter: " + ", ".join(report["status_filter"]))
    if report.get("adopt_root"):
        lines.append(f"Adopt root: {report['adopt_root']}")
    lines.append(
        f"Hygiene score: {health['score']}/100 ({health['label']}) | "
        f"shared_ratio={health['shared_ratio']:.1%} | "
        f"review={health['review_count']} | "
        f"duplicates={health['duplicate_count']}"
    )
    lines.append(
        "Status counts: "
        + ", ".join(
            f"{key}={summary['status_counts'].get(key, 0)}" for key in STATUS_ORDER
        )
    )
    lines.append("")

    lines.append("RECOMMENDED ACTIONS")
    recommendation_lines = format_recommendations(report)
    if recommendation_lines:
        lines.extend(recommendation_lines)
    else:
        lines.append("- none")
    lines.append("")

    for status in STATUS_ORDER:
        matching = [group for group in report["groups"] if group["status"] == status]
        if not matching:
            continue
        lines.append(status.upper())
        for group in matching:
            lines.append(
                f"- {group['name']}: {', '.join(group['platforms'])} "
                f"({group['reason']})"
            )
        lines.append("")

    if dedupe or report.get("adopt_root"):
        title = "APPLIED DEDUPE" if apply else "PLANNED DEDUPE"
        lines.append(title)
        if not report["dedupe_plan"]:
            lines.append("- none")
        else:
            for plan in report["dedupe_plan"]:
                replacements = ", ".join(
                    f"{item['platform']}:{item['path']}" for item in plan["replacements"]
                )
                lines.append(
                    f"- {plan['name']}: keep {plan['source_path']} "
                    f"({plan['selected_by']}) | replace {replacements}"
                )
        lines.append("")

    if sync_missing or report.get("adopt_root"):
        title = "APPLIED MISSING LINKS" if apply else "PLANNED MISSING LINKS"
        lines.append(title)
        if not report["planned_links"]:
            lines.append("- none")
        else:
            for plan in report["planned_links"]:
                destinations = ", ".join(
                    f"{item['platform']}:{item['path']}" for item in plan["destinations"]
                )
                lines.append(
                    f"- {plan['name']}: source {plan['source_path']} "
                    f"({plan['selected_by']}) | add {destinations}"
                )

    if apply and report.get("run"):
        lines.append("")
        lines.append("BACKUP RUN")
        lines.append(f"- run_id: {report['run']['run_id']}")
        lines.append(f"- backup_root: {report['run']['backup_root']}")
        lines.append(
            f"- restore: python3 {SCRIPT_PATH} --restore {report['run']['run_id']}"
        )

    return "\n".join(lines).strip()


def format_name_list(report: dict) -> str:
    lines: list[str] = []
    for status in STATUS_ORDER:
        matching = [group for group in report["groups"] if group["status"] == status]
        if not matching:
            continue
        lines.append(f"[{status}]")
        for group in matching:
            lines.append(group["name"])
        lines.append("")
    return "\n".join(lines).strip()


def format_restore_text(manifest: dict, apply: bool) -> str:
    lines = [
        f"Restore run: {manifest['run_id']}",
        f"Created at: {manifest['created_at']}",
        f"Backup root: {manifest['backup_root']}",
        f"Actions: {len(manifest.get('actions', []))}",
        "",
        "RESTORE ACTIONS" if apply else "RESTORE PREVIEW",
    ]

    if not manifest.get("actions"):
        lines.append("- none")
    else:
        for action in manifest["actions"]:
            if action["action"] == "replace_with_symlink":
                lines.append(
                    f"- restore {action['name']}: {action['path']} from {action['backup_path']}"
                )
            else:
                lines.append(f"- remove created link {action['name']}: {action['path']}")

    if apply and manifest.get("restored_at"):
        lines.extend(["", f"Restored at: {manifest['restored_at']}"])
    return "\n".join(lines).strip()


def format_export_text(manifest: dict, manifest_path: Path) -> str:
    lines = [
        f"Exported manifest: {manifest_path}",
        f"Generated at: {manifest['generated_at']}",
        f"Skills: {manifest['summary']['total_skills']}",
        f"Importable skills: {manifest['summary']['importable_skills']}",
        f"Desired placements: {manifest['summary']['desired_placements']}",
        f"Strategy: {manifest['strategy']}",
    ]
    if manifest.get("adopt_root"):
        lines.append(f"Adopt root: {manifest['adopt_root']}")
    return "\n".join(lines)


def format_import_text(plan: dict, apply: bool, manifest_path: Path) -> str:
    lines = [
        f"Import manifest: {manifest_path}",
        f"Generated at: {plan['generated_at']}",
        f"Recorded skills: {plan['summary']['recorded_skills']}",
        f"Planned operations: {plan['summary']['planned_operations']}",
        f"Unchanged placements: {plan['summary']['unchanged']}",
        f"Issues: {plan['summary']['issues']}",
        "",
        "IMPORT ISSUES",
    ]

    if plan["issues"]:
        for issue in plan["issues"]:
            lines.append(f"- {issue['type']} {issue['name']}: {issue['detail']}")
    else:
        lines.append("- none")

    lines.extend(["", "IMPORTED LINKS" if apply else "PLANNED IMPORT"])
    if plan["operations"]:
        for operation in plan["operations"]:
            verb = "replace" if operation["action"] == "replace_with_symlink" else "create"
            lines.append(f"- {verb} {operation['name']}: {operation['path']} -> {operation['target_path']}")
    else:
        lines.append("- none")

    if apply and plan.get("run"):
        lines.extend(
            [
                "",
                "BACKUP RUN",
                f"- run_id: {plan['run']['run_id']}",
                f"- backup_root: {plan['run']['backup_root']}",
                f"- restore: python3 {SCRIPT_PATH} --restore {plan['run']['run_id']}",
            ]
        )
    return "\n".join(lines).strip()


def format_diff_text(diff_report: dict) -> str:
    lines = [
        f"Skill: {diff_report['skill']}",
        f"Status: {diff_report['status']}",
        f"Reason: {diff_report['reason']}",
        "Canonical source:",
        f"- {diff_report['canonical']['platform']}:{diff_report['canonical']['path']}",
        f"- selected_by: {diff_report['canonical']['selected_by']}",
        "",
    ]

    if not diff_report["comparisons"]:
        lines.append("No alternate portable installs to compare.")
        return "\n".join(lines)

    lines.append("COMPARISONS")
    for item in diff_report["comparisons"]:
        lines.append(
            f"- {item['platform']}:{item['path']} | "
            f"changed={item['summary']['changed']} "
            f"added={item['summary']['added']} "
            f"removed={item['summary']['removed']}"
        )
        sample_paths = (
            item["changed"][:5] + item["added"][:5] + item["removed"][:5]
        )
        if sample_paths:
            for path in sample_paths[:8]:
                lines.append(f"  {path}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--skill", action="append", default=[], help="Limit scan to one or more skill names")
    parser.add_argument("--status", action="append", default=[], help="Filter by one or more statuses; repeat or use comma-separated values")
    parser.add_argument("--list-names", action="store_true", help="Print only skill names grouped by status")
    parser.add_argument("--diff", metavar="SKILL", help="Show file-level diff for one portable skill across installs")
    parser.add_argument("--sync-missing", action="store_true", help="Plan or create symlinks for missing host installs")
    parser.add_argument("--dedupe", action="store_true", help="Plan or replace duplicate installs with symlinks to a canonical source")
    parser.add_argument("--strategy", choices=("strict", "prefer-latest", "trust-high"), default="strict")
    parser.add_argument("--prefer-root", choices=ALL_PLATFORMS, help="Prefer one root as canonical source when selecting winners")
    parser.add_argument("--adopt-root", choices=ALL_PLATFORMS, help="Preview or apply a single-root convergence plan; implies --dedupe and --sync-missing")
    parser.add_argument("--apply", action="store_true", help="Execute the requested sync or dedupe plan")
    parser.add_argument("--dry-run", action="store_true", help="Explicitly request preview mode")
    parser.add_argument("--restore", help="Restore a previous backup run id or 'latest'")
    parser.add_argument("--export-manifest", help="Write a portable layout manifest for cross-machine skill convergence")
    parser.add_argument("--import-manifest", help="Preview or apply a previously exported layout manifest")
    parser.add_argument(
        "--backup-root",
        default=str(env_path("SKILL_SYNC_BACKUP_ROOT", str(Path.home() / ".skill-sync" / "backups"))),
        help="Directory for backup runs and restore manifests",
    )
    parser.add_argument("--workdir", default=".", help="Workspace directory used to detect ./skills roots")
    parser.add_argument(
        "--source-order",
        default="agents,codex,claude,opencode,openclaw,workspace",
        help="Preferred source host order when timestamps are tied",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    backup_root = Path(args.backup_root).expanduser()

    if args.restore:
        run_dir = resolve_run_dir(backup_root, args.restore)
        manifest = restore_run(run_dir, apply=args.apply)
        if args.format == "json":
            print(json.dumps(manifest, indent=2, ensure_ascii=False))
        else:
            print(format_restore_text(manifest, apply=args.apply))
        return 0

    adopt_root = args.adopt_root
    sync_missing = args.sync_missing or bool(adopt_root)
    dedupe = args.dedupe or bool(adopt_root)

    if args.apply and not (sync_missing or dedupe or args.import_manifest):
        raise SystemExit(
            "--apply requires --sync-missing, --dedupe, --adopt-root, or --import-manifest"
        )

    workdir = Path(args.workdir).expanduser().resolve()
    roots = build_root_specs(workdir)
    prefer_root = adopt_root or args.prefer_root
    source_order = reorder_source_order(args.source_order, prefer_root)

    skill_filter = {item.strip() for item in args.skill if item.strip()}
    if args.diff:
        skill_filter.add(args.diff)

    entries = discover_skills(roots, skill_filter)

    if args.import_manifest:
        manifest_path = Path(args.import_manifest).expanduser().resolve()
        manifest = load_layout_manifest(manifest_path)
        import_source_order = reorder_source_order(
            ",".join(manifest.get("source_order", args.source_order)),
            manifest.get("adopt_root") or args.prefer_root,
        )
        import_plan = build_import_plan(
            manifest=manifest,
            roots=roots,
            entries=entries,
            source_order=import_source_order,
        )
        if args.apply and not args.dry_run:
            applied = apply_operations(import_plan["operations"], backup_root=backup_root)
            if applied:
                import_plan["run"] = {
                    "run_id": applied["run_id"],
                    "backup_root": applied["backup_root"],
                }

        if args.format == "json":
            print(json.dumps(import_plan, indent=2, ensure_ascii=False))
        else:
            print(format_import_text(import_plan, apply=args.apply and not args.dry_run, manifest_path=manifest_path))
        return 0

    if args.diff:
        diff_report = build_skill_diff(entries, args.diff, source_order, args.strategy)
        if args.format == "json":
            print(json.dumps(diff_report, indent=2, ensure_ascii=False))
        else:
            print(format_diff_text(diff_report))
        return 0

    report = build_report(
        entries=entries,
        roots=roots,
        source_order=source_order,
        strategy=args.strategy,
        adopt_root=adopt_root,
    )
    report = filter_report_groups(report, parse_status_filters(args.status))

    if args.export_manifest:
        manifest_path = Path(args.export_manifest).expanduser().resolve()
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        export_manifest = build_layout_manifest(report)
        write_json(manifest_path, export_manifest)
        if args.format == "json":
            print(json.dumps(export_manifest, indent=2, ensure_ascii=False))
        else:
            print(format_export_text(export_manifest, manifest_path))
        return 0

    if args.apply and not args.dry_run:
        operations = build_operations(report, sync_missing=sync_missing, dedupe=dedupe)
        manifest = apply_operations(operations, backup_root=backup_root)
        if manifest:
            report["run"] = {
                "run_id": manifest["run_id"],
                "backup_root": manifest["backup_root"],
            }

    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0
    if args.list_names:
        print(format_name_list(report))
        return 0

    print(
        format_text(
            report,
            sync_missing=sync_missing,
            dedupe=dedupe,
            apply=args.apply and not args.dry_run,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
