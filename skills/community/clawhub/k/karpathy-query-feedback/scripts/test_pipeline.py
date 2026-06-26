"""
测试 Karpathy Query → Wiki 回流 Pipeline
直接使用 M-Flow，不通过 skill 导入
"""

import asyncio
import sys
import importlib.util
from pathlib import Path

# 动态加载 M-Flow 和 MFlowMemory
def _load_mflow():
    skill_path = Path(__file__).parent.parent.parent
    mflow_path = skill_path / "m_flow"
    mflow_skill_path = skill_path / "m-flow-memory"
    
    # 添加路径
    if str(mflow_path) not in sys.path:
        sys.path.insert(0, str(mflow_path))
    
    # 使用 importlib 加载 scripts 模块
    scripts_path = mflow_skill_path / "scripts" / "__init__.py"
    spec = importlib.util.spec_from_file_location("mflow_scripts", scripts_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

mflow_module = _load_mflow()
MFlowMemory = mflow_module.MFlowMemory

# 现在导入 pipeline
sys.path.insert(0, str(Path(__file__).parent))
from __init__ import QueryFeedbackPipeline, WikiEntry


async def test_pipeline():
    """测试完整管道"""
    print("=== Karpathy Query → Wiki Pipeline 测试 ===\n")
    
    # 创建管道
    print("[1] 创建 QueryFeedbackPipeline...")
    pipeline = QueryFeedbackPipeline()
    print("     OK\n")
    
    # 测试 Wiki 条目创建
    print("[2] 测试 Wiki 条目格式化...")
    entry = WikiEntry(
        source="test:session",
        content="Python is a programming language",
        tags=["python", "programming"],
        timestamp="2026-04-05"
    )
    print(f"     Markdown行: {entry.to_markdown_row()}")
    print("     OK\n")
    
    # 先添加一些测试数据到 M-Flow
    print("[3] 添加测试数据到 M-Flow...")
    test_data = [
        "Machine learning is a subset of artificial intelligence",
        "Deep learning uses neural networks with multiple layers",
        "Python has extensive libraries for data science",
        "OpenClaw is an AI agent framework for automation",
        "Vector databases are used for similarity search"
    ]
    
    for item in test_data:
        await pipeline.memory.add(item)
    await pipeline.memory.memorize()
    print(f"     添加了 {len(test_data)} 条测试数据")
    print("     OK\n")
    
    # 测试查询
    print("[4] 测试查询 (hybrid mode)...")
    result = await pipeline.query_and_save(
        "Python machine learning",
        mode="hybrid",
        top_k=5
    )
    print(f"     查询: {result['query']}")
    print(f"     模式: {result['mode']}")
    print(f"     结果数: {result['entries_count']}")
    print(f"     保存路径: {result['saved_path']}")
    print("     OK\n")
    
    # 测试 wiki 格式化
    print("[5] 测试 Wiki 格式化...")
    wiki_md = pipeline.format_as_wiki([WikiEntry(**e) for e in result['entries']])
    print(wiki_md)
    print("     OK\n")
    
    # 测试各个搜索模式
    print("[6] 测试各搜索模式...")
    modes = ["lexical", "episodic", "triplet"]
    for mode in modes:
        try:
            entries = await pipeline.query("Python", mode=mode, top_k=3)
            print(f"     [{mode}] - {len(entries)} results")
        except Exception as e:
            print(f"     [{mode}] - FAIL: {e}")
    print()
    
    print("=== Phase 1 Pipeline 测试完成 ===")


if __name__ == "__main__":
    asyncio.run(test_pipeline())
