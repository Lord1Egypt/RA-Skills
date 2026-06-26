#!/usr/bin/env python3
"""
Memory Indexer - 统计工具
显示 memory 使用统计信息
"""

import os
import json
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path.home() / ".openclaw" / "agents" / "github-workflow"
MEMORY_DIR = WORKSPACE / "memory"
INDEX_FILE = WORKSPACE / "memory-indexer" / "memory_index.json"
STARS_FILE = WORKSPACE / "memory-indexer" / "stars.json"


def get_dir_size(path: Path) -> int:
    """获取目录大小（字节）"""
    total = 0
    try:
        for entry in path.rglob("*"):
            if entry.is_file():
                total += entry.stat().st_size
    except FileNotFoundError:
        pass
    return total


def bytes_to_mb(bytes_size: int) -> float:
    """字节转 MB"""
    return bytes_size / (1024 * 1024)


def load_index() -> dict:
    """加载索引"""
    if INDEX_FILE.exists():
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def load_stars() -> set:
    """加载星标记忆"""
    if STARS_FILE.exists():
        with open(STARS_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def show_stats():
    """显示统计信息"""
    print("📊 Memory Indexer - 统计信息")
    print("=" * 50)

    # Memory 目录统计
    if MEMORY_DIR.exists():
        total_bytes = get_dir_size(MEMORY_DIR)
        total_mb = bytes_to_mb(total_bytes)
        file_count = len(list(MEMORY_DIR.rglob("*.md")))

        print(f"\n📁 Memory 目录: {MEMORY_DIR}")
        print(f"   大小: {total_mb:.2f} MB")
        print(f"   文件: {file_count} 个")

        # 文件类型分布
        md_count = len(list(MEMORY_DIR.glob("*.md")))
        print(f"   Markdown: {md_count}")
    else:
        print(f"\n📁 Memory 目录不存在")

    # 索引统计
    index = load_index()
    print(f"\n🔑 索引统计:")
    print(f"   关键词数: {len(index.get('keywords', {}))}")
    print(f"   记忆条目: {len(index.get('memories', {}))}")

    # 星标统计
    stars = load_stars()
    print(f"\n⭐ 星标记忆: {len(stars)} 个")

    # 最近修改的文件
    if MEMORY_DIR.exists():
        files = sorted(
            MEMORY_DIR.rglob("*.md"),
            key=lambda f: f.stat().st_mtime,
            reverse=True
        )[:5]

        if files:
            print(f"\n📝 最近修改:")
            for f in files:
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                size = bytes_to_mb(f.stat().st_size)
                star = "⭐" if f.name in stars else "  "
                print(f"   {star} {f.name[:30]:30} {size:.1f}KB {mtime.strftime('%Y-%m-%d')}")

    print("\n" + "=" * 50)

    # 建议
    print("💡 提示:")
    print("   python memory-indexer.py list        # 列出所有记忆")
    print("   python memory-indexer.py search <kw> # 搜索记忆")
    print("   python memory_detect.py              # 检测压缩风险")


if __name__ == "__main__":
    show_stats()
