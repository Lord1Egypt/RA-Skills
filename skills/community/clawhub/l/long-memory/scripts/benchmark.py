#!/usr/bin/env python3
"""性能基准测试：大量数据下的性能测量"""

import argparse
import os
import tempfile
import time
from datetime import datetime, timedelta
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))


def generate_test_data(memory_dir: Path, days: int = 365) -> dict:
    """生成测试数据"""
    conv_dir = memory_dir / "conversations"
    conv_dir.mkdir(parents=True, exist_ok=True)

    topics = ["日常对话", "项目讨论", "技术方案", "需求分析", "代码评审",
              "会议纪要", "学习笔记", "问题排查", "架构设计", "性能优化"]
    tags_pool = ["工作", "个人", "技术", "管理", "学习", "沟通"]
    user_msgs = [
        "你觉得这个方案怎么样？我觉得可以再优化一下。",
        "帮我分析一下这个问题，我觉得可能是配置的问题。",
        "今天开会讨论了下个迭代的需求，主要涉及三个方面。",
        "我在看这个文档的时候发现了一些矛盾的地方，帮我确认下。",
        "上次说的那个功能什么时候能完成？客户在催了。",
        "这个 bug 我查了两天了还是没找到原因，你帮看看。",
        "我觉得应该优先处理性能问题，用户体验太差了。",
        "周末有个技术分享会，你准备讲什么？",
        "最近在学 Rust，感觉和 Python 思维方式差很多。",
        "这个项目的架构需要重构了，现在维护成本太高。",
        "帮我写个测试用例，覆盖边界情况。",
        "这个 API 的响应时间太长了，有没有优化方案？",
        "今天的日报我写好了，你帮我看看有没有遗漏。",
        "我决定把这个模块拆分成独立的微服务。",
        "最近记忆力不太好，帮我记一下这些要点。",
    ]
    assistant_msgs = [
        "好的，我来分析一下。首先需要确认几个前置条件...",
        "这个问题的根本原因是数据量增长导致的，建议分批处理。",
        "我同意你的看法，可以按这个方向继续推进。",
        "我帮你梳理了一下，总结为以下三点...",
        "方案已经验证通过了，可以部署到测试环境。",
        "这个问题比较复杂，建议分步骤排查。先检查...",
        "已经修复了，主要改动是调整了缓存策略。",
        "我觉得可以采用渐进式重构，不影响现有功能。",
        "测试用例已经写好了，覆盖了正常和异常场景。",
        "我帮你整理了一份详细的技术方案文档。",
    ]

    stats = {"files": 0, "total_size": 0, "total_sessions": 0}
    
    for i in range(days):
        date = (datetime.now() - timedelta(days=days - i - 1)).strftime("%Y-%m-%d")
        sessions = 1 + (i % 4)  # 每天1-4个session
        content = f"# {date} 对话记录\n"

        for s in range(sessions):
            hour = 8 + (s * 3) % 12
            minute = (i * 7 + s * 13) % 60
            topic = topics[(i + s) % len(topics)]
            tags = [tags_pool[(i + s * 2) % len(tags_pool)],
                   tags_pool[(i + s * 3) % len(tags_pool)]]
            
            content += f"\n## [{hour:02d}:{minute:02d}] Session: webchat\n"
            content += f"### 话题：{topic}\n"
            content += f"**标签：** {', '.join(tags)}\n\n"
            
            # 3-8轮对话
            rounds = 3 + (i + s) % 6
            for r in range(rounds):
                user_msg = user_msgs[(i + s + r) % len(user_msgs)]
                assistant_msg = assistant_msgs[(i + s + r * 2) % len(assistant_msgs)]
                content += f"**用户：** {user_msg}\n"
                content += f"**助手：** {assistant_msg}\n\n"

            if s % 2 == 0:
                content += f"**关键决策：**\n- 确定了{topic}的方向\n"

        fp = conv_dir / f"{date}.md"
        fp.write_text(content, encoding="utf-8")
        stats["files"] += 1
        stats["total_size"] += fp.stat().st_size
        stats["total_sessions"] += sessions

    return stats


def benchmark_search(memory_dir: Path, query: str = "性能优化 方案") -> dict:
    """基准测试：搜索性能"""
    from scripts.search_memory import search
    import time

    start = time.perf_counter()
    results = search(memory_dir, query)
    elapsed = time.perf_counter() - start

    return {"query": query, "results": len(results), "time_ms": round(elapsed * 1000, 2)}


def benchmark_stats(memory_dir: Path) -> dict:
    """基准测试：统计性能"""
    from scripts.memory_stats import get_stats

    start = time.perf_counter()
    stats = get_stats(memory_dir)
    elapsed = time.perf_counter() - start

    return {"files": stats["conversations"], "time_ms": round(elapsed * 1000, 2)}


def benchmark_index(memory_dir: Path) -> dict:
    """基准测试：索引构建"""
    from scripts.index_manager import build_index

    start = time.perf_counter()
    index = build_index(memory_dir)
    elapsed = time.perf_counter() - start

    return {"files": index["stats"]["total_files"], "time_ms": round(elapsed * 1000, 2)}


def benchmark_tfidf(memory_dir: Path, query: str = "性能优化方案") -> dict:
    """基准测试：TF-IDF 搜索"""
    from scripts.tfidf_search import search_tfidf

    start = time.perf_counter()
    results = search_tfidf(memory_dir, query, top_n=10)
    elapsed = time.perf_counter() - start

    return {"query": query, "results": len(results), "time_ms": round(elapsed * 1000, 2)}


def run_benchmark(memory_dir: Path, days: int = 365) -> dict:
    """运行完整基准测试"""
    print(f"📊 生成测试数据（{days} 天）...")
    stats = generate_test_data(memory_dir, days)
    print(f"  ✅ {stats['files']} 文件, {stats['total_sessions']} sessions, "
          f"{stats['total_size'] / 1024 / 1024:.1f} MB\n")

    print("🔍 运行基准测试...\n")
    results = {}

    tests = [
        ("统计", lambda: benchmark_stats(memory_dir)),
        ("索引构建", lambda: benchmark_index(memory_dir)),
        ("关键词搜索", lambda: benchmark_search(memory_dir, "性能优化方案")),
        ("TF-IDF搜索", lambda: benchmark_tfidf(memory_dir, "性能优化方案")),
        ("模糊搜索", lambda: benchmark_search(memory_dir, "这个那个什么")),
    ]

    for name, fn in tests:
        result = fn()
        results[name] = result
        status = "🟢" if result["time_ms"] < 100 else "🟡" if result["time_ms"] < 1000 else "🔴"
        print(f"  {status} {name:15s} {result['time_ms']:>8.2f} ms")

    return {"data_stats": stats, "benchmarks": results}


def print_report(bench: dict):
    print(f"\n{'=' * 50}")
    print("📊 性能基准测试报告")
    print(f"{'=' * 50}")
    print(f"\n数据量: {bench['data_stats']['files']} 文件, "
          f"{bench['data_stats']['total_sessions']} sessions, "
          f"{bench['data_stats']['total_size'] / 1024 / 1024:.1f} MB")

    avg_time = sum(b["time_ms"] for b in bench["benchmarks"].values()) / len(bench["benchmarks"])
    print(f"平均响应: {avg_time:.2f} ms")

    all_fast = all(b["time_ms"] < 1000 for b in bench["benchmarks"].values())
    print(f"{'✅ 所有操作 < 1秒，性能达标' if all_fast else '⚠️ 部分操作超过 1秒'}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="性能基准测试")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--days", type=int, default=365, help="生成多少天的测试数据")
    p.add_argument("--use-existing", action="store_true", help="使用现有数据")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)

    if not args.use_existing:
        # 使用临时目录
        import tempfile
        tmp = Path(tempfile.mkdtemp(prefix="long-memory-bench-"))
        md = tmp / "memory"

    bench = run_benchmark(md, args.days if not args.use_existing else 0)
    print_report(bench)
