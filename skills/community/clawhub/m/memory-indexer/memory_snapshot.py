#!/usr/bin/env python3
"""
Memory Indexer - 自动快照工具
在压缩/清理前自动创建快照备份
"""

import os
import json
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

# 导入配置模块
from memory_config import (
    load_config, get_memory_dir, get_snapshot_dir, get_workspace
)

# 加载配置
config = load_config()

# 获取路径配置
WORKSPACE = get_workspace()
MEMORY_DIR = get_memory_dir()
SNAPSHOT_DIR = get_snapshot_dir()
INDEX_FILE = WORKSPACE / "memory-indexer" / "memory_index.json"
STARS_FILE = WORKSPACE / "memory-indexer" / "stars.json"

# 阈值从配置获取
WARNING_THRESHOLD = config.get("warning_threshold", 70)
CRITICAL_THRESHOLD = config.get("critical_threshold", 85)


def ensure_dirs():
    """确保目录存在"""
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)


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


def create_snapshot(name: str = None) -> Path:
    """创建快照"""
    ensure_dirs()

    if name is None:
        name = datetime.now().strftime("%Y%m%d_%H%M%S")

    snapshot_file = SNAPSHOT_DIR / f"snapshot_{name}.zip"

    with zipfile.ZipFile(snapshot_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        # 备份 memory 目录
        if MEMORY_DIR.exists():
            for file in MEMORY_DIR.rglob("*"):
                if file.is_file():
                    arcname = f"memory/{file.relative_to(MEMORY_DIR)}"
                    zipf.write(file, arcname)

        # 备份索引文件
        if INDEX_FILE.exists():
            zipf.write(INDEX_FILE, "memory_index.json")

        if STARS_FILE.exists():
            zipf.write(STARS_FILE, "stars.json")

        # 添加元数据
        metadata = {
            "created": datetime.now().isoformat(),
            "memory_size_mb": bytes_to_mb(get_dir_size(MEMORY_DIR)),
            "name": name
        }
        zipf.writestr("metadata.json", json.dumps(metadata, indent=2))

    return snapshot_file


def list_snapshots():
    """列出快照"""
    if not SNAPSHOT_DIR.exists():
        print("暂无快照")
        return []

    snapshots = sorted(SNAPSHOT_DIR.glob("snapshot_*.zip"), reverse=True)

    print("📦 快照列表:")
    print("=" * 50)

    for snap in snapshots:
        # 读取元数据
        with zipfile.ZipFile(snap, "r") as zipf:
            try:
                metadata = json.loads(zipf.read("metadata.json"))
                print(f"  {snap.name}")
                print(f"     时间: {metadata['created'][:19]}")
                print(f"     大小: {metadata.get('memory_size_mb', '?')} MB")
            except:
                print(f"  {snap.name} (无元数据)")

        print()

    return snapshots


def restore_snapshot(snapshot_name: str):
    """恢复快照"""
    snapshot_file = SNAPSHOT_DIR / f"snapshot_{snapshot_name}.zip"

    if not snapshot_file.exists():
        print(f"❌ 快照不存在: {snapshot_name}")
        return

    # 备份当前状态
    if MEMORY_DIR.exists():
        backup_dir = MEMORY_DIR.parent / f"memory_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copytree(MEMORY_DIR, backup_dir)
        print(f"📁 已备份当前 memory 到: {backup_dir}")

    # 解压快照
    with zipfile.ZipFile(snapshot_file, "r") as zipf:
        for member in zipf.namelist():
            if member == "metadata.json":
                continue

            target = WORKSPACE / member
            target.parent.mkdir(parents=True, exist_ok=True)

            if not member.endswith("/"):
                with zipf.open(member) as source:
                    with open(target, "wb") as dest:
                        dest.write(source.read())

    print(f"✅ 已恢复快照: {snapshot_name}")


def auto_snapshot_if_needed() -> bool:
    """检查是否需要自动快照"""
    if not MEMORY_DIR.exists():
        return False

    size_mb = bytes_to_mb(get_dir_size(MEMORY_DIR))

    if size_mb >= WARNING_THRESHOLD:
        print(f"⚠️ Memory 大小 {size_mb:.1f}MB >= 阈值 {WARNING_THRESHOLD}MB")
        print("📦 正在创建自动快照...")
        snapshot = create_snapshot(f"auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        print(f"✅ 快照已创建: {snapshot.name}")
        return True

    return False


def main():
    import sys

    if len(sys.argv) < 2:
        # 默认显示统计
        print("📦 Memory Indexer - 快照管理")
        print("=" * 50)
        print(f"阈值配置: WARNING={WARNING_THRESHOLD}MB, CRITICAL={CRITICAL_THRESHOLD}MB")
        print()
        list_snapshots()
        print("\n用法:")
        print("  python memory_snapshot.py create      # 创建快照")
        print("  python memory_snapshot.py list        # 列出快照")
        print("  python memory_snapshot.py restore <name>  # 恢复快照")
        print("  python memory_snapshot.py auto        # 检查并自动快照")
        print(f"\n💾 配置文件: ~/.memory-indexer/config.json")
        return

    command = sys.argv[1]

    if command == "create":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        snapshot = create_snapshot(name)
        print(f"✅ 快照已创建: {snapshot}")

    elif command == "list":
        list_snapshots()

    elif command == "restore":
        if len(sys.argv) < 3:
            print("用法: python memory_snapshot.py restore <snapshot_name>")
            return
        restore_snapshot(sys.argv[2])

    elif command == "auto":
        auto_snapshot_if_needed()

    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
