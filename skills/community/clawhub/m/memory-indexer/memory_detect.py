#!/usr/bin/env python3
"""
Memory Indexer - 压缩检测工具
检测 memory 目录的压缩风险
"""

import os
import sys
from pathlib import Path

# 导入配置模块
from memory_config import (
    load_config, get_memory_dir, get_snapshot_dir, get_workspace,
    get_warning_threshold, get_critical_threshold
)

# 加载配置
config = load_config()

# 从配置获取阈值
WARNING_THRESHOLD = get_warning_threshold()
CRITICAL_THRESHOLD = get_critical_threshold()


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


def check_compression_risk() -> dict:
    """检测压缩风险"""
    memory_dir = get_memory_dir()
    
    if not memory_dir.exists():
        return {
            "exists": False,
            "total_mb": 0,
            "risk": "none",
            "message": "Memory 目录不存在"
        }

    total_bytes = get_dir_size(memory_dir)
    total_mb = bytes_to_mb(total_bytes)

    # 估算上下文使用（假设上下文窗口 200KB）
    estimated_contexts = total_mb / 0.2

    # 简单风险评估
    if total_mb < WARNING_THRESHOLD:
        risk = "safe"
        emoji = "✅"
    elif total_mb < CRITICAL_THRESHOLD:
        risk = "warning"
        emoji = "⚠️"
    else:
        risk = "critical"
        emoji = "🚨"

    # 统计文件数
    file_count = len(list(memory_dir.rglob("*.md")))

    return {
        "exists": True,
        "total_bytes": total_bytes,
        "total_mb": round(total_mb, 2),
        "file_count": file_count,
        "estimated_contexts": int(estimated_contexts),
        "risk": risk,
        "emoji": emoji,
        "message": f"{emoji} {'安全' if risk == 'safe' else '警告' if risk == 'warning' else '危险'}: {total_mb:.1f}MB ({file_count} 个文件)",
        "warning_threshold": WARNING_THRESHOLD,
        "critical_threshold": CRITICAL_THRESHOLD,
    }


def main():
    print("🔍 Memory Indexer - 压缩检测")
    print("=" * 40)
    print(f"阈值配置: WARNING={WARNING_THRESHOLD}MB, CRITICAL={CRITICAL_THRESHOLD}MB")

    result = check_compression_risk()

    if not result["exists"]:
        print(result["message"])
        print(f"\n默认 memory 目录: {get_memory_dir()}")
        print("\n初始化 memory 目录后即可使用检测功能")
        return

    print(f"\n📊 检测结果:")
    print(f"   目录: {get_memory_dir()}")
    print(f"   大小: {result['total_mb']} MB")
    print(f"   文件: {result['file_count']} 个")
    print(f"   估算上下文: ~{result['estimated_contexts']} 轮对话")
    print(f"\n🟢 风险等级: {result['emoji']} {result['risk'].upper()}")

    print("\n" + "=" * 40)
    print("💡 建议:")
    if result["risk"] == "safe":
        print("   - 状态良好，继续使用")
    elif result["risk"] == "warning":
        print("   - 建议运行: python memory_compact.py --auto-snapshot")
        print("   - 或标记重要记忆: python memory-indexer.py star <file>")
    else:
        print("   - 立即运行: python memory_compact.py --auto-snapshot")
        print("   - 优先保留标记过的记忆")
        print("   - 清理不重要的记忆")

    # 检查 snapshots 目录
    snapshot_dir = get_snapshot_dir()
    if snapshot_dir.exists():
        snapshot_count = len(list(snapshot_dir.glob("*.zip")))
        print(f"\n📦 已有快照: {snapshot_count} 个")
    else:
        print(f"\n📦 快照目录: 未创建")

    # 显示配置信息
    print("\n" + "=" * 40)
    print(f"💾 配置文件: ~/.memory-indexer/config.json")
    print(f"   可通过环境变量覆盖: MEMORY_INDEXER_WARNING, MEMORY_INDEXER_CRITICAL")

    return result


if __name__ == "__main__":
    main()
