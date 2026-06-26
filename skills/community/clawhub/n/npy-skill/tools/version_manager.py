#!/usr/bin/env python3
"""
伴侣 Skill 版本管理器
负责版本存档、历史查看和回滚操作。

用法：
python version_manager.py --action list --slug xiaoming
python version_manager.py --action save --slug xiaoming --note "添加温柔特质"
python version_manager.py --action rollback --slug xiaoming --version v2
"""

from __future__ import annotations
import json
import argparse
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional
import shutil


def list_versions(skill_dir: Path) -> list:
    """列出某个伴侣 Skill 的所有版本"""

    versions_dir = skill_dir / "versions"
    if not versions_dir.exists():
        return []

    versions = []
    for version_dir in sorted(versions_dir.iterdir(), reverse=True):
        if not version_dir.is_dir():
            continue

        # 尝试读取版本说明
        note_path = version_dir / "version_note.txt"
        note = ""
        if note_path.exists():
            note = note_path.read_text(encoding="utf-8").strip()

        versions.append({
            "version": version_dir.name,
            "path": str(version_dir),
            "note": note,
            "created": datetime.fromtimestamp(version_dir.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
        })

    return versions


def save_version(skill_dir: Path, note: str = "") -> str:
    """手动保存当前版本"""

    meta_path = skill_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    current_version = meta.get("version", "v1")
    try:
        version_num = int(current_version.lstrip("v").split("_")[0]) + 1
    except ValueError:
        version_num = 2

    new_version = f"v{version_num}_manual"

    # 存档当前版本
    version_dir = skill_dir / "versions" / new_version
    version_dir.mkdir(parents=True, exist_ok=True)

    for fname in ("SKILL.md", "persona.md", "relationship.md", "meta.json"):
        src = skill_dir / fname
        if src.exists():
            shutil.copy2(src, version_dir / fname)

    # 写入版本说明
    if note:
        (version_dir / "version_note.txt").write_text(note, encoding="utf-8")

    return new_version


def rollback_version(skill_dir: Path, target_version: str) -> bool:
    """回滚到指定版本"""

    versions_dir = skill_dir / "versions"
    target_dir = versions_dir / target_version

    if not target_dir.exists():
        return False

    # 先保存当前版本
    meta_path = skill_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    current_version = meta.get("version", "v1")

    backup_dir = versions_dir / f"{current_version}_before_rollback"
    backup_dir.mkdir(parents=True, exist_ok=True)
    for fname in ("SKILL.md", "persona.md", "relationship.md", "meta.json"):
        src = skill_dir / fname
        if src.exists():
            shutil.copy2(src, backup_dir / fname)
    (backup_dir / "version_note.txt").write_text(f"回滚前自动备份，准备回滚到 {target_version}", encoding="utf-8")

    # 从目标版本恢复文件
    for fname in ("SKILL.md", "persona.md", "relationship.md"):
        src = target_dir / fname
        dst = skill_dir / fname
        if src.exists():
            shutil.copy2(src, dst)

    # 更新 meta.json
    meta["version"] = target_version
    meta["updated_at"] = datetime.now(timezone.utc).isoformat()
    meta["rollback_from"] = current_version
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="伴侣 Skill 版本管理器")
    parser.add_argument("--action", required=True, choices=["list", "save", "rollback"])
    parser.add_argument("--slug", help="伴侣 slug")
    parser.add_argument("--version", help="目标版本（用于 rollback）")
    parser.add_argument("--note", help="版本说明（用于 save）")
    parser.add_argument(
        "--base-dir",
        default="",
        help="npy Skill 根目录（默认：.claude/skills/）",
    )
    args = parser.parse_args()

    # 如果没有指定 base_dir，尝试自动检测
    if args.base_dir:
        base_dir = Path(args.base_dir).expanduser()
    else:
        current = Path.cwd()
        # 检查是否在 .claude/skills/npy 目录
        if (current.name == "npy" and (current.parent.name == "skills")):
            base_dir = current.parent
        elif (current / ".claude" / "skills").exists():
            base_dir = current / ".claude" / "skills"
        elif (current / "SKILL.md").exists():
            # 当前目录是某个 skill 目录
            base_dir = current.parent
        else:
            base_dir = current / ".claude" / "skills"

    if not args.slug:
        print("错误：需要 --slug 参数", file=sys.stderr)
        sys.exit(1)

    skill_dir = base_dir / args.slug
    if not skill_dir.exists():
        print(f"错误：找不到 Skill 目录 {skill_dir}", file=sys.stderr)
        sys.exit(1)

    if args.action == "list":
        versions = list_versions(skill_dir)
        if not versions:
            print("暂无历史版本")
        else:
            print(f"{args.slug} 的版本历史：\n")
            for v in versions:
                print(f" [{v['version']}] 更新时间: {v['created']}")
                if v['note']:
                    print(f"  说明: {v['note']}")
                print()

            print("回滚命令：")
            print(f"  python version_manager.py --action rollback --slug {args.slug} --version v2")

    elif args.action == "save":
        note = args.note or f"手动保存于 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        new_version = save_version(skill_dir, note)
        print(f"✅ 已保存当前版本为 {new_version}")

    elif args.action == "rollback":
        if not args.version:
            print("错误：rollback 需要 --version 参数", file=sys.stderr)
            sys.exit(1)

        success = rollback_version(skill_dir, args.version)
        if success:
            print(f"✅ 已回滚到 {args.version}")
            print(f"  当前版本已备份为 {args.version}_before_rollback")
        else:
            print(f"错误：找不到版本 {args.version}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()