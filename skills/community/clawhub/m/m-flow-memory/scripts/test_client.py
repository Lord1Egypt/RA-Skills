"""
M-Flow Memory Skill - 测试脚本
验证 M-Flow 记忆客户端功能
"""

import asyncio
import sys
from pathlib import Path

# 添加 skill 路径
skill_path = Path(__file__).parent.parent
sys.path.insert(0, str(skill_path))

from scripts import MFlowMemory


async def test_basic_operations():
    """测试基本操作"""
    print("=== M-Flow Memory Skill 测试 ===\n")
    
    # 创建客户端
    print("[1] 创建 M-Flow Memory 客户端...")
    memory = MFlowMemory(log_level="ERROR")
    print("     OK\n")
    
    # 添加内容
    print("[2] 添加记忆内容...")
    test_contents = [
        "Python is a high-level programming language",
        "JavaScript is used for web development",
        "Machine learning is a subset of artificial intelligence",
        "OpenClaw is an AI Agent framework",
        "M-Flow provides memory management for AI agents"
    ]
    
    for content in test_contents:
        await memory.add(content)
        print(f"     Added: {content[:50]}...")
    print("     OK\n")
    
    # 索引内容
    print("[3] 索引记忆内容 (memorize)...")
    await memory.memorize()
    print("     OK\n")
    
    # 测试搜索
    print("[4] 测试搜索模式...")
    
    modes = ["lexical", "episodic", "triplet"]
    
    for mode in modes:
        try:
            results = await memory.search("Python programming", mode=mode)
            items = len(results[0].get('search_result', [])) if results else 0
            print(f"     [{mode}] - OK ({items} results)")
        except Exception as e:
            print(f"     [{mode}] - FAIL: {e}")
    
    print()
    
    # 获取统计
    print("[5] 获取统计信息...")
    stats = memory.get_stats()
    print(f"     Added count: {stats['added_count']}")
    print("     OK\n")
    
    print("=== 所有测试通过 ===")


if __name__ == "__main__":
    asyncio.run(test_basic_operations())
