#!/usr/bin/env python3
"""记忆统计：统计对话数量、话题分布、记忆体积"""

import argparse
from collections import Counter
from datetime import datetime
from pathlib import Path

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"


def human_size(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    elif size < 1024 ** 2:
        return f"{size / 1024:.1f} KB"
    else:
        return f"{size / (1024 ** 2):.1f} MB"


def get_stats(memory_dir: Path) -> dict:
    stats = {
        "total_size": 0,
        "files": 0,
        "conversations": 0,
        "sessions": 0,
        "topics": Counter(),
        "tags": Counter(),
        "dates": [],
        "daily_sizes": {},
        "distillations": 0,
        "memory_md_size": 0,
    }

    conv_dir = memory_dir / "conversations"
    distill_dir = memory_dir / "distillations"
    memory_md = memory_dir.parent / "MEMORY.md"

    # MEMORY.md
    if memory_md.exists():
        stats["memory_md_size"] = memory_md.stat().st_size

    # 对话文件
    if conv_dir.exists():
        for f in sorted(conv_dir.glob("*.md")):
            content = f.read_text(encoding="utf-8")
            size = f.stat().st_size
            stats["total_size"] += size
            stats["files"] += 1
            stats["conversations"] += 1
            stats["dates"].append(f.stem)

            # 统计 session 数
            sessions = content.count("## [")
            stats["sessions"] += sessions

            # 提取话题
            import re
            for topic in re.findall(r'### 话题：(.+)', content):
                stats["topics"][topic.strip().rstrip(".")] += 1

            # 提取标签
            for tags in re.findall(r'\*\*标签：\*\*\s*(.+)', content):
                for tag in tags.split("，"):
                    tag = tag.strip()
                    if tag:
                        stats["tags"][tag] += 1

            stats["daily_sizes"][f.stem] = size

    # 蒸馏文件
    if distill_dir.exists():
        for f in distill_dir.glob("*.md"):
            stats["total_size"] += f.stat().st_size
            stats["files"] += 1
            stats["distillations"] += 1

    return stats


def print_stats(stats: dict, verbose: bool = False):
    print("=" * 50)
    print("📊 记忆系统统计")
    print("=" * 50)
    print(f"\n📁 总文件数: {stats['files']}")
    print(f"📦 总体积:   {human_size(stats['total_size'])}")
    print(f"📝 MEMORY.md: {human_size(stats['memory_md_size'])}")
    print(f"\n📅 对话天数: {stats['conversations']}")
    print(f"💬 对话段数: {stats['sessions']}")

    if stats["topics"]:
        print(f"\n🏷️  话题 TOP 10:")
        for topic, count in stats["topics"].most_common(10):
            print(f"   {topic}: {count} 次")

    if stats["tags"]:
        print(f"\n📌 标签分布:")
        for tag, count in stats["tags"].most_common():
            print(f"   {tag}: {count} 次")

    if stats["dates"]:
        print(f"\n📆 日期范围: {stats['dates'][0]} → {stats['dates'][-1]}")

    if verbose and stats["daily_sizes"]:
        print(f"\n📋 每日详情:")
        for date, size in sorted(stats["daily_sizes"].items()):
            print(f"   {date}: {human_size(size)}")

    print()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="记忆统计")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--verbose", "-v", action="store_true", help="显示每日详情")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)
    stats = get_stats(md)
    print_stats(stats, args.verbose)
