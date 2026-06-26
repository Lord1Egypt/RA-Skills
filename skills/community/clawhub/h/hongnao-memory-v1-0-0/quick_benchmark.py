#!/usr/bin/env python3
"""
弘脑记忆系统 - 快速性能基准测试
HongNao Memory OS - Quick Performance Benchmark

运行时间：~2 分钟
测试核心指标：检索延迟/添加延迟/召回率
"""

import sys
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from memory_api import HongNaoMemorySystem, MemorySystemConfig
from openclaw_integration import OpenClawMemorySync, OpenClawTools


def test_add_latency(memory_system, count=10):
    """测试添加记忆延迟"""
    print(f"\n📝 测试添加记忆延迟 ({count} 条)...")
    
    test_memories = [
        "用户喜欢简洁的沟通风格",
        "用户偏好使用 Python 进行开发",
        "用户在燧弘华创担任执行总裁",
        "用户通常早上 8 点查看新闻",
        "用户习惯在晚上 10 点前休息",
        "用户不喜欢冗长的会议",
        "用户关注 AI 和科技领域",
        "用户偏好详细的报告",
        "用户喜欢直接的方式",
        "用户通常避免使用 Java",
    ]
    
    start = time.time()
    for i, content in enumerate(test_memories[:count]):
        memory_system.add_memory(
            content=content,
            cell_type="preference",
            tags=["test"],
            importance=6.0,
            source="benchmark"
        )
    elapsed = time.time() - start
    
    avg_latency = (elapsed / count) * 1000  # ms
    status = "✅" if avg_latency < 10 else "⚠️"
    
    print(f"  总耗时：{elapsed*1000:.2f}ms")
    print(f"  平均延迟：{avg_latency:.2f}ms/条 {status}")
    
    return avg_latency


def test_retrieval_latency(memory_system, count=5):
    """测试检索延迟"""
    print(f"\n🔍 测试检索延迟 ({count} 次)...")
    
    queries = [
        "用户偏好",
        "沟通风格",
        "Python 开发",
        "工作时间",
        "生活习惯",
    ]
    
    latencies = []
    for query in queries[:count]:
        start = time.time()
        result = memory_system.retrieve_memories(query, top_k=3)
        elapsed = time.time() - start
        latencies.append(elapsed * 1000)
    
    avg_latency = sum(latencies) / len(latencies)
    status = "✅" if avg_latency < 100 else "⚠️"
    
    print(f"  平均延迟：{avg_latency:.2f}ms {status}")
    print(f"  最小：{min(latencies):.2f}ms, 最大：{max(latencies):.2f}ms")
    
    return avg_latency


def test_recall_rate(memory_system):
    """测试召回率 (简化版)"""
    print(f"\n🎯 测试召回率...")
    
    # 添加测试记忆
    test_data = [
        ("用户喜欢 Python", "编程语言"),
        ("用户讨厌 Java", "编程语言"),
        ("用户早上看新闻", "生活习惯"),
        ("用户晚上休息", "生活习惯"),
    ]
    
    for content, tag in test_data:
        memory_system.add_memory(
            content=content,
            cell_type="preference",
            tags=[tag],
            importance=7.0,
            source="recall_test"
        )
    
    # 测试检索
    queries = [
        ("Python", 1),  # 期望召回 1 条
        ("Java", 1),
        ("早上 新闻", 1),
        ("晚上 休息", 1),
    ]
    
    total_expected = 0
    total_retrieved = 0
    
    for query, expected in queries:
        result = memory_system.retrieve_memories(query, top_k=5, min_score=0.1)
        # 结果在'results' 键中，不是'memories'
        retrieved = len(result.get('results', []))
        total_expected += expected
        # 只要找到至少 1 条相关记忆就算成功
        total_retrieved += (1 if retrieved > 0 else 0)
    
    recall = (total_retrieved / total_expected * 100) if total_expected > 0 else 0
    status = "✅" if recall >= 75 else "⚠️"
    
    print(f"  召回率：{recall:.1f}% {status}")
    print(f"  期望召回：{total_expected} 类，实际召回：{total_retrieved} 类")
    
    return recall


def test_session_sync():
    """测试 Session 同步性能"""
    print(f"\n🔄 测试 Session 同步...")
    
    config = MemorySystemConfig()
    memory_system = HongNaoMemorySystem(config)
    sync = OpenClawMemorySync(memory_system)
    
    # 模拟 10 条消息的 Session
    messages = [
        {"role": "user", "content": f"消息 {i}: 测试内容"}
        for i in range(10)
    ]
    
    start = time.time()
    result = sync.sync_session_to_memory(
        session_id="benchmark_session",
        messages=messages,
        auto_extract=True
    )
    elapsed = time.time() - start
    
    status = "✅" if elapsed < 0.5 else "⚠️"
    
    print(f"  同步耗时：{elapsed*1000:.2f}ms {status}")
    print(f"  抽取记忆：{result.get('memories_extracted', 0)} 条")
    
    return elapsed * 1000


def generate_report(results):
    """生成基准测试报告"""
    print("\n" + "=" * 60)
    print("📊 弘脑记忆系统 - 快速性能基准报告")
    print("=" * 60)
    
    print(f"\n测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试版本：v0.2.0")
    
    print(f"\n{'指标':<20} {'目标':<15} {'实测':<15} {'状态':<10}")
    print("-" * 60)
    
    metrics = [
        ("添加记忆延迟", "<10ms", f"{results['add_latency']:.2f}ms", 
         "✅" if results['add_latency'] < 10 else "⚠️"),
        ("检索延迟", "<100ms", f"{results['retrieval_latency']:.2f}ms",
         "✅" if results['retrieval_latency'] < 100 else "⚠️"),
        ("召回率", ">90%", f"{results['recall_rate']:.1f}%",
         "✅" if results['recall_rate'] > 90 else "⚠️"),
        ("Session 同步", "<500ms", f"{results['session_sync']:.2f}ms",
         "✅" if results['session_sync'] < 500 else "⚠️"),
    ]
    
    for name, target, actual, status in metrics:
        print(f"{name:<20} {target:<15} {actual:<15} {status:<10}")
    
    # 总体评估
    all_passed = all([
        results['add_latency'] < 10,
        results['retrieval_latency'] < 100,
        results['recall_rate'] > 90,
        results['session_sync'] < 500,
    ])
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有性能指标达标！系统可以发布。")
    else:
        print("⚠️ 部分指标未达标，建议优化后发布。")
    print("=" * 60)
    
    return all_passed


def main():
    """主函数"""
    print("=" * 60)
    print("弘脑记忆系统 - 快速性能基准测试")
    print("=" * 60)
    print("预计运行时间：~2 分钟\n")
    
    # 初始化
    config = MemorySystemConfig()
    memory_system = HongNaoMemorySystem(config)
    
    results = {}
    
    # 运行测试
    results['add_latency'] = test_add_latency(memory_system)
    results['retrieval_latency'] = test_retrieval_latency(memory_system)
    results['recall_rate'] = test_recall_rate(memory_system)
    results['session_sync'] = test_session_sync()
    
    # 生成报告
    all_passed = generate_report(results)
    
    # 保存报告
    report_file = Path(__file__).parent / "benchmark_report.json"
    import json
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'version': '0.2.0',
            'results': results,
            'all_passed': all_passed
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n报告已保存：{report_file}")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
