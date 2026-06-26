#!/usr/bin/env python3
"""
列出历史电台脚本

列出用户生成的历史电台。
"""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.audio_manager import AudioManager


def list_radios(user_id: str = None, limit: int = 20):
    """
    列出历史电台
    
    Args:
        user_id: 用户ID
        limit: 返回数量限制
    """
    audio_manager = AudioManager()
    
    print("📻 历史电台列表")
    print("=" * 60)
    
    files = audio_manager.list_files(user_id=user_id, limit=limit)
    
    if not files:
        print("\n暂无历史电台")
        return
    
    for i, file in enumerate(files, 1):
        print(f"\n{i}. {file['metadata'].get('title', '未命名电台')}")
        print(f"   📅 创建时间: {file['created_at']}")
        print(f"   ⏱️ 时长: {file['metadata'].get('duration', 0):.1f}秒")
        print(f"   📝 摘要: {file['metadata'].get('summary', '无摘要')[:50]}...")
        print(f"   🎧 播放: {file['url']}")
        print(f"   📥 下载: {file['url']}")
    
    print("\n" + "=" * 60)
    
    storage_info = audio_manager.get_storage_info()
    print(f"\n📊 存储信息:")
    print(f"   文件总数: {storage_info['total_files']}")
    print(f"   总大小: {storage_info['total_size_mb']} MB")


def cleanup_radios(days: int = 30):
    """
    清理过期电台
    
    Args:
        days: 保留天数
    """
    audio_manager = AudioManager()
    
    print(f"🗑️ 正在清理{days}天前的电台...")
    
    deleted_count = audio_manager.cleanup(days=days)
    
    print(f"✅ 已删除 {deleted_count} 个过期电台")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='列出历史电台')
    parser.add_argument('--user-id', type=str, help='用户ID')
    parser.add_argument('--limit', type=int, default=20, help='返回数量限制')
    parser.add_argument('--cleanup', type=int, help='清理指定天数前的电台')
    
    args = parser.parse_args()
    
    if args.cleanup:
        cleanup_radios(days=args.cleanup)
    else:
        list_radios(user_id=args.user_id, limit=args.limit)


if __name__ == "__main__":
    main()
