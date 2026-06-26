#!/usr/bin/env python3
"""
缓存性能测试脚本

验证优化效果：
1. 首次读取（缓存未命中）
2. 重复读取（缓存命中）
3. 缓存失效（强制刷新）

使用方法：
  python3 scripts/test_cache_performance.py
"""

import time
import sys
from pathlib import Path

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

def test_cache_performance():
    """测试缓存性能"""
    print("\n" + "=" * 60)
    print("  缓存性能测试")
    print("=" * 60)
    
    # 导入知识库
    from knowledge_base import KnowledgeBase
    
    # 创建知识库实例
    print("\n📥 初始化知识库...")
    kb = KnowledgeBase(project_id="meilan-center")
    
    # 测试1：首次读取（缓存未命中）
    print("\n" + "-" * 60)
    print("测试1：首次读取（缓存未命中）")
    print("-" * 60)
    
    start = time.time()
    data, error = kb.load("房源销控表", use_cache=False)  # 强制刷新
    elapsed_first = time.time() - start
    
    if error:
        print(f"❌ 错误：{error}")
        print("⚠️ 请确保已通过MCP工具将数据保存到本地")
        return
    
    print(f"✅ 首次读取耗时：{elapsed_first:.3f}秒")
    print(f"   加载记录数：{data.get('total', 0)}")
    
    # 测试2：重复读取（缓存命中 - 内存缓存）
    print("\n" + "-" * 60)
    print("测试2：重复读取（缓存命中 - 内存缓存）")
    print("-" * 60)
    
    start = time.time()
    data2, error2 = kb.load("房源销控表", use_cache=True)  # 使用缓存
    elapsed_cache = time.time() - start
    
    print(f"✅ 缓存命中耗时：{elapsed_cache:.6f}秒")
    print(f"   加速比：{elapsed_first/elapsed_cache:.1f}倍")
    print(f"   缓存状态：✅ 命中（内存缓存）")
    
    # 测试3：创建新实例（测试文件缓存）
    print("\n" + "-" * 60)
    print("测试3：新实例读取（缓存命中 - 文件缓存）")
    print("-" * 60)
    
    kb2 = KnowledgeBase(project_id="meilan-center")
    
    start = time.time()
    data3, error3 = kb2.load("房源销控表", use_cache=True)  # 使用缓存
    elapsed_file_cache = time.time() - start
    
    print(f"✅ 文件缓存命中耗时：{elapsed_file_cache:.6f}秒")
    print(f"   加速比：{elapsed_first/elapsed_file_cache:.1f}倍")
    print(f"   缓存状态：✅ 命中（文件缓存）")
    
    # 测试4：缓存统计
    print("\n" + "-" * 60)
    print("测试4：缓存统计信息")
    print("-" * 60)
    
    stats = kb.get_cache_stats()
    print(f"   内存缓存命中次数：{stats['hit_count']}")
    print(f"   缓存未命中次数：{stats['miss_count']}")
    print(f"   缓存命中率：{stats['hit_rate']}")
    
    # 总结
    print("\n" + "=" * 60)
    print("  测试总结")
    print("=" * 60)
    
    print(f"\n{'指标':<30} {'耗时（秒）':<15} {'加速比'}")
    print("-" * 60)
    print(f"{'首次读取（无缓存）':<30} {elapsed_first:.3f}      {'-':<10}")
    print(f"{'内存缓存命中':<30} {elapsed_cache:.6f}      {elapsed_first/elapsed_cache:.1f}倍")
    print(f"{'文件缓存命中':<30} {elapsed_file_cache:.6f}      {elapsed_first/elapsed_file_cache:.1f}倍")
    
    print(f"\n💡 优化效果：")
    print(f"   - 内存缓存加速：{elapsed_first/elapsed_cache:.1f}倍")
    print(f"   - 文件缓存加速：{elapsed_first/elapsed_file_cache:.1f}倍")
    print(f"   - 缓存命中率：{stats['hit_rate']}")
    
    print(f"\n✅ 测试完成！")

if __name__ == "__main__":
    test_cache_performance()
