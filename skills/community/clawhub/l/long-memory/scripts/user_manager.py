#!/usr/bin/env python3
"""多用户隔离：支持多人的独立记忆空间"""

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.filelock import safe_write, safe_write_json, safe_read_json

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
CONFIG_FILE = ".users.json"


def get_users_config(memory_dir: Path) -> dict:
    fp = memory_dir / CONFIG_FILE
    if fp.exists():
        return safe_read_json(fp)
    return {"current_user": "default", "users": ["default"]}


def save_users_config(memory_dir: Path, config: dict):
    safe_write_json(memory_dir / CONFIG_FILE, config)


def get_user_dir(memory_dir: Path, user: str) -> Path:
    return memory_dir / "users" / user


def switch_user(memory_dir: Path, user: str):
    """切换用户"""
    config = get_users_config(memory_dir)
    if user not in config["users"]:
        config["users"].append(user)
    config["current_user"] = user
    save_users_config(memory_dir, config)

    user_dir = get_user_dir(memory_dir, user)
    user_dir.mkdir(parents=True, exist_ok=True)
    
    for subdir in ["conversations", "summaries", "distillations", "archive"]:
        (user_dir / subdir).mkdir(parents=True, exist_ok=True)

    print(f"✅ 已切换到用户: {user}")
    print(f"   记忆目录: {user_dir}")


def get_active_memory_dir(memory_dir: Path) -> Path:
    """获取当前活跃用户的记忆目录"""
    config = get_users_config(memory_dir)
    user = config.get("current_user", "default")
    user_dir = get_user_dir(memory_dir, user)
    
    if user_dir.exists():
        return user_dir
    return memory_dir


def list_users(memory_dir: Path):
    config = get_users_config(memory_dir)
    current = config.get("current_user", "default")
    
    print("=" * 60)
    print(f"👥 用户管理（当前: {current}）")
    print("=" * 60)
    
    for user in config["users"]:
        icon = "👉" if user == current else "  "
        user_dir = get_user_dir(memory_dir, user)
        
        # 统计
        conv_dir = user_dir / "conversations"
        conv_count = len(list(conv_dir.glob("*.md"))) if conv_dir.exists() else 0
        size = sum(f.stat().st_size for f in user_dir.rglob("*.md") if f.is_file()) if user_dir.exists() else 0
        
        size_str = f"{size / 1024:.1f} KB" if size > 1024 else f"{size} B"
        print(f"  {icon} {user:<20s} {conv_count:>3d} 对话  {size_str:>10s}")


def merge_users(memory_dir: Path, source: str, target: str):
    """合并两个用户的记忆"""
    src_dir = get_user_dir(memory_dir, source)
    tgt_dir = get_user_dir(memory_dir, target)

    if not src_dir.exists():
        print(f"⚠️ 源用户 {source} 不存在")
        return

    for subdir in ["conversations", "summaries", "distillations"]:
        src_sub = src_dir / subdir
        tgt_sub = tgt_dir / subdir
        if not src_sub.exists():
            continue
        tgt_sub.mkdir(parents=True, exist_ok=True)

        for fp in src_sub.glob("*.md"):
            dest = tgt_sub / f"{source}_{fp.name}"
            if dest.exists():
                # 追加
                dest.write_text(dest.read_text(encoding="utf-8") + "\n\n" + 
                              fp.read_text(encoding="utf-8"), encoding="utf-8")
            else:
                shutil.copy2(fp, dest)
            print(f"  ✅ {fp.name} → {dest.name}")

    print(f"\n✅ 用户 {source} 的记忆已合并到 {target}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="多用户隔离")
    sub = p.add_subparsers(dest="command")

    sw = sub.add_parser("switch", help="切换用户")
    sw.add_argument("user", help="用户名")

    sub.add_parser("list", help="列出用户")

    sub.add_parser("current", help="显示当前用户")

    mg = sub.add_parser("merge", help="合并用户记忆")
    mg.add_argument("source")
    mg.add_argument("target")

    args = p.parse_args()
    md = DEFAULT_MEMORY_DIR

    if args.command == "switch":
        switch_user(md, args.user)
    elif args.command == "list":
        list_users(md)
    elif args.command == "current":
        config = get_users_config(md)
        print(f"当前用户: {config.get('current_user', 'default')}")
    elif args.command == "merge":
        merge_users(md, args.source, args.target)
    else:
        list_users(md)
