#!/usr/bin/env python3
"""scripts/version_manager.py

GuruTalk 版本管理器（guru profiles）

目的：
- 为单个 guru 目录创建可回滚的本地快照（meta.json/profile.md/SKILL.md）
- 列出快照、回滚到某个快照、清理旧快照

约定目录：
- ~/.claude/skills/{slug}/versions/{label}/ (Claude)
- ~/.openclaw/workspace/skills/{slug}/versions/{label}/ (OpenClaw)

用法：
  python scripts/version_manager.py --action snapshot --agent claude --slug elon-musk
  python scripts/version_manager.py --action list --agent claude --slug elon-musk
  python scripts/version_manager.py --action rollback --agent claude --slug elon-musk --version 2026-04-04.1__20260405T101010Z
  python scripts/version_manager.py --action cleanup --agent claude --slug elon-musk --keep 20
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

# Agent skills directory mapping
AGENT_SKILLS_DIRS = {
    "claude": "~/.claude/skills",
    "codex": "~/.codex/skills",
    "openclaw": "~/.openclaw/workspace/skills",
}

DEFAULT_AGENT = "claude"
DEFAULT_GURU_BASE_DIR = None  # Will be set based on agent type
DEFAULT_KEEP_VERSIONS = 20

DEFAULT_FILES = ("meta.json", "profile.md", "SKILL.md")
BACKUP_PREFIX = "_before_rollback__"
MANIFEST_NAME = "manifest.json"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _utc_now_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _safe_label(label: str) -> str:
    # Folder name safety: disallow path separators and trim.
    label = label.strip()
    label = label.replace("/", "_").replace("\\\\", "_")
    if not label or label in (".", ".."):
        raise ValueError("Empty/invalid label")
    return label


def _iter_version_dirs(versions_dir: Path) -> list[Path]:
    if not versions_dir.exists():
        return []
    dirs = [p for p in versions_dir.iterdir() if p.is_dir()]
    # Sort by name descending; naming includes timestamps in our default labels.
    return sorted(dirs, key=lambda p: p.name, reverse=True)


def _load_manifest(version_dir: Path) -> dict[str, Any] | None:
    m = version_dir / MANIFEST_NAME
    if not m.exists():
        return None
    try:
        return _read_json(m)
    except Exception:
        return None


def snapshot_guru(
    *,
    guru_dir: Path,
    label: str | None = None,
    include_files: Iterable[str] = DEFAULT_FILES,
) -> str:
    versions_dir = guru_dir / "versions"
    versions_dir.mkdir(parents=True, exist_ok=True)

    meta: dict[str, Any] = {}
    meta_path = guru_dir / "meta.json"
    if meta_path.exists():
        try:
            meta = _read_json(meta_path)
        except Exception:
            meta = {}

    profile_version = str(meta.get("profile_version") or "unknown")
    if label is None:
        label = f"{profile_version}__{_utc_now_compact()}"
    label = _safe_label(label)

    version_dir = versions_dir / label
    if version_dir.exists():
        raise RuntimeError(f"Version already exists: {version_dir}")
    version_dir.mkdir(parents=True, exist_ok=False)

    copied: list[dict[str, Any]] = []
    missing: list[str] = []

    for name in include_files:
        src = guru_dir / name
        if not src.exists():
            missing.append(name)
            continue
        dst = version_dir / name
        shutil.copy2(src, dst)
        copied.append({"name": name, "size": dst.stat().st_size, "sha256": _sha256(dst)})

    manifest: dict[str, Any] = {
        "kind": "guru-snapshot",
        "slug": str(meta.get("slug") or guru_dir.name),
        "label": label,
        "created_at": _utc_now_iso(),
        "source": {
            "profile_version": meta.get("profile_version"),
            "updated_at": meta.get("updated_at"),
        },
        "files": copied,
        "missing_files": missing,
    }
    _write_json(version_dir / MANIFEST_NAME, manifest)

    if not copied:
        shutil.rmtree(version_dir)
        raise RuntimeError(
            f"No files copied (missing={missing}). "
            "This usually means the guru directory is incomplete."
        )

    return label


def list_versions(*, guru_dir: Path) -> list[dict[str, Any]]:
    versions_dir = guru_dir / "versions"
    out: list[dict[str, Any]] = []
    for d in _iter_version_dirs(versions_dir):
        manifest = _load_manifest(d)
        out.append(
            {
                "label": d.name,
                "created_at": (manifest or {}).get("created_at"),
                "profile_version": (manifest or {}).get("source", {}).get("profile_version"),
                "files": [f.name for f in d.iterdir() if f.is_file()],
            }
        )
    return out


def rollback(*, guru_dir: Path, target_label: str) -> None:
    versions_dir = guru_dir / "versions"
    target_label = _safe_label(target_label)
    target_dir = versions_dir / target_label
    if not target_dir.exists():
        raise RuntimeError(f"Target version not found: {target_dir}")

    # Safety backup of current state before restoring.
    backup_label = f"{BACKUP_PREFIX}{_utc_now_compact()}"
    snapshot_guru(guru_dir=guru_dir, label=backup_label)

    restored: list[str] = []
    for name in DEFAULT_FILES:
        src = target_dir / name
        if not src.exists():
            continue
        shutil.copy2(src, guru_dir / name)
        restored.append(name)

    if not restored:
        raise RuntimeError(f"Target version contains none of {DEFAULT_FILES}: {target_dir}")


def cleanup(*, guru_dir: Path, keep: int, prune_backups: bool) -> int:
    if keep < 0:
        raise ValueError("--keep must be >= 0")

    versions_dir = guru_dir / "versions"
    if not versions_dir.exists():
        return 0

    all_dirs = _iter_version_dirs(versions_dir)
    candidates: list[Path] = []
    for d in all_dirs:
        if not prune_backups and d.name.startswith(BACKUP_PREFIX):
            continue
        candidates.append(d)

    to_delete = candidates[keep:]
    for d in to_delete:
        shutil.rmtree(d)

    return len(to_delete)


def _require_guru_dir(base_dir: Path, slug: str) -> Path:
    guru_dir = (base_dir / slug).expanduser()
    if not guru_dir.exists():
        raise RuntimeError(f"Guru directory not found: {guru_dir}")
    return guru_dir


def _get_agent_skills_dir(agent: str) -> Path:
    """Get the skills directory for the specified agent type."""
    if agent not in AGENT_SKILLS_DIRS:
        raise RuntimeError(f"Unknown agent type: {agent}. Supported: {list(AGENT_SKILLS_DIRS.keys())}")
    return Path(AGENT_SKILLS_DIRS[agent]).expanduser()


def main() -> None:
    parser = argparse.ArgumentParser(description="GuruTalk version manager (skills/{slug}/versions)")
    parser.add_argument(
        "--action",
        required=True,
        choices=["snapshot", "list", "rollback", "cleanup"],
    )
    parser.add_argument("--slug", required=True, help="人物 slug（对应 skills/{slug}）")
    parser.add_argument(
        "--agent",
        default=DEFAULT_AGENT,
        choices=list(AGENT_SKILLS_DIRS.keys()),
        help=f"Agent 类型（默认: {DEFAULT_AGENT}）",
    )
    parser.add_argument(
        "--base-dir",
        default=None,
        help="根目录（默认: {agent_skills_dir}）",
    )

    parser.add_argument("--label", help="快照 label（仅 snapshot，可选）")
    parser.add_argument("--version", help="目标版本 label（仅 rollback）")
    parser.add_argument("--keep", type=int, default=DEFAULT_KEEP_VERSIONS, help="保留最近 N 个快照（仅 cleanup）")
    parser.add_argument(
        "--prune-backups",
        action="store_true",
        help=f"cleanup 时也删除 {BACKUP_PREFIX}* 的回滚备份",
    )

    args = parser.parse_args()

    # Resolve base_dir based on agent type
    if args.base_dir:
        base_dir = Path(args.base_dir).expanduser()
    else:
        base_dir = _get_agent_skills_dir(args.agent)
    try:
        guru_dir = _require_guru_dir(base_dir, args.slug)
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)

    try:
        if args.action == "snapshot":
            label = snapshot_guru(guru_dir=guru_dir, label=args.label)
            print(f"✅ 已创建快照：{args.slug}  {label}")
            return

        if args.action == "list":
            versions = list_versions(guru_dir=guru_dir)
            if not versions:
                print(f"{args.slug} 暂无快照")
                return
            print(f"{args.slug} 的快照列表（新 → 旧）：\n")
            for v in versions:
                pv = v.get("profile_version") or ""
                created = v.get("created_at") or ""
                print(f"  {v['label']}  {pv}  {created}")
            return

        if args.action == "rollback":
            if not args.version:
                raise RuntimeError("rollback 需要 --version")
            rollback(guru_dir=guru_dir, target_label=args.version)
            print(f"✅ 已回滚：{args.slug} -> {args.version}（已自动备份当前状态）")
            return

        if args.action == "cleanup":
            deleted = cleanup(guru_dir=guru_dir, keep=int(args.keep), prune_backups=bool(args.prune_backups))
            print(f"✅ 清理完成：删除 {deleted} 个旧快照")
            return

        raise RuntimeError(f"Unknown action: {args.action}")
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
