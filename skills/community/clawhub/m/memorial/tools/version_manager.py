#!/usr/bin/env python3
"""
version_manager.py — 版本管理与回滚工具

用法：
  python version_manager.py --action backup  --slug grandpa_wang
  python version_manager.py --action list    --slug grandpa_wang
  python version_manager.py --action rollback --slug grandpa_wang --to v2
  python version_manager.py --action cleanup --slug grandpa_wang
"""

import argparse
import json
import os
import shutil
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
MEMORIALS_DIR = os.path.join(PROJECT_ROOT, "memorials")

MAX_VERSIONS = 10
TRACKED_FILES = ["remembrance.md", "persona.md", "SKILL.md", "meta.json"]


def memorial_dir(slug: str) -> str:
    return os.path.join(MEMORIALS_DIR, slug)


def versions_dir(slug: str) -> str:
    return os.path.join(memorial_dir(slug), "versions")


def read_meta(slug: str) -> dict:
    path = os.path.join(memorial_dir(slug), "meta.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


# ── 操作 ──────────────────────────────────────────────────────────────────────

def action_backup(slug: str) -> str:
    """将当前版本备份到 versions/ 目录，返回备份路径。"""
    base = memorial_dir(slug)
    vdir = versions_dir(slug)
    os.makedirs(vdir, exist_ok=True)

    meta = read_meta(slug)
    version = meta.get("version", "v1")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:20]
    backup_name = f"{version}_{timestamp}"
    backup_path = os.path.join(vdir, backup_name)

    os.makedirs(backup_path, exist_ok=True)
    for fname in TRACKED_FILES:
        src = os.path.join(base, fname)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(backup_path, fname))

    print(f"[备份] memorials/{slug}/versions/{backup_name}/")
    action_cleanup(slug)
    return backup_path


def action_list(slug: str) -> None:
    """列出所有备份版本。"""
    vdir = versions_dir(slug)
    if not os.path.exists(vdir):
        print(f"[空] memorials/{slug}/ 没有历史版本。")
        return

    entries = sorted([
        d for d in os.listdir(vdir)
        if os.path.isdir(os.path.join(vdir, d))
    ], reverse=True)

    if not entries:
        print(f"[空] memorials/{slug}/ 没有历史版本。")
        return

    print(f"memorials/{slug}/ 的历史版本（共 {len(entries)} 个）：\n")
    for entry in entries:
        backup_path = os.path.join(vdir, entry)
        files = [f for f in TRACKED_FILES if os.path.exists(os.path.join(backup_path, f))]
        print(f"  {entry:<35} 包含：{', '.join(files)}")


def action_rollback(slug: str, to_version: str) -> None:
    """
    回滚到指定版本。
    to_version 可以是：
    - 精确备份名（如 "v2_20260401_120000"）
    - 版本号前缀（如 "v2"，取最新的 v2_* 备份）
    """
    vdir = versions_dir(slug)
    base = memorial_dir(slug)

    # 找到目标备份
    all_entries = sorted([
        d for d in os.listdir(vdir)
        if os.path.isdir(os.path.join(vdir, d))
    ], reverse=True)

    target = None
    for entry in all_entries:
        if entry == to_version or entry.startswith(to_version + "_"):
            target = entry
            break

    if not target:
        print(f"[错误] 找不到版本 {to_version}")
        print(f"可用版本：{', '.join(all_entries[:5])}")
        return

    # 先备份当前版本（防止回滚后丢失数据）
    print(f"[安全备份] 先保存当前版本...")
    action_backup(slug)

    # 恢复目标版本
    backup_path = os.path.join(vdir, target)
    restored = []
    for fname in TRACKED_FILES:
        src = os.path.join(backup_path, fname)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(base, fname))
            restored.append(fname)

    print(f"[已回滚] memorials/{slug}/ → {target}")
    print(f"  恢复的文件：{', '.join(restored)}")


def action_cleanup(slug: str) -> None:
    """保留最新的 MAX_VERSIONS 个备份，删除旧的。"""
    vdir = versions_dir(slug)
    if not os.path.exists(vdir):
        return

    entries = sorted([
        d for d in os.listdir(vdir)
        if os.path.isdir(os.path.join(vdir, d))
    ], reverse=True)

    to_delete = entries[MAX_VERSIONS:]
    for entry in to_delete:
        shutil.rmtree(os.path.join(vdir, entry))
        print(f"[清理] 删除旧版本 {entry}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="纪念 Skill 版本管理工具")
    parser.add_argument("--action", required=True,
                        choices=["backup", "list", "rollback", "cleanup"],
                        help="操作类型")
    parser.add_argument("--slug", required=True, help="纪念档案的 slug")
    parser.add_argument("--to", help="回滚目标版本（rollback 时必填）")
    args = parser.parse_args()

    if args.action == "backup":
        action_backup(args.slug)
    elif args.action == "list":
        action_list(args.slug)
    elif args.action == "rollback":
        if not args.to:
            parser.error("--action rollback 需要 --to 参数")
        action_rollback(args.slug, args.to)
    elif args.action == "cleanup":
        action_cleanup(args.slug)


if __name__ == "__main__":
    main()
