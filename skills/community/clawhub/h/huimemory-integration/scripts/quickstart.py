#!/usr/bin/env python3
"""
HuiMemory 快速入门脚本

这个脚本演示了 HuiMemory 的核心功能：
1. 索引对话文件
2. 检索历史对话
3. 时间过滤
4. 分段扫描
5. 轮次导航

使用方法：
    python scripts/quickstart.py
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from huimemory import Retriever
from huimemory.chunker import TurnChunker
from huimemory.embedding import BGEMockEmbedding  # 使用 Mock 避免下载模型


def main():
    print("=" * 60)
    print("HuiMemory 快速入门")
    print("=" * 60)
    
    # 1. 初始化
    print("\n[1/5] 初始化 Retriever...")
    embedding = BGEMockEmbedding()  # 生产环境使用 BGEEmbedding
    retriever = Retriever(embedding=embedding)
    print("✓ 初始化完成")
    
    # 2. 索引对话文件
    print("\n[2/5] 索引对话文件...")
    chunker = TurnChunker()
    
    # 创建示例对话
    sample_dir = project_root / "memory" / "sessions" / "2026-W15" / "2026-04-13"
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    sample_file = sample_dir / "chat_demo.md"
    sample_file.write_text("""
[id:a3f2c7]
<user timestamp="2026-04-13T10:00:07">我想了解一下本地模型部署</user>
<assistant timestamp="2026-04-13T10:00:15">好的，本地模型部署需要考虑硬件配置、模型选择、推理框架等因素...</assistant>

[id:k7f2a1]
<user timestamp="2026-04-13T10:01:20">BGE-M3 和 bge-small-zh-v1.5 有什么区别？</user>
<assistant timestamp="2026-04-13T10:01:30">BGE-M3 是 1024 维的重模型，性能最好；bge-small-zh-v1.5 是 384 维的轻量模型，部署成本低 20 倍...</assistant>

[id:d2n7p3]
<user timestamp="2026-04-13T10:02:45">AI 会有意识吗？</user>
<assistant timestamp="2026-04-13T10:02:55">这是一个深刻的哲学问题。目前主流观点认为 AI 没有意识，但也有一些研究者持不同看法...</assistant>
""".strip(), encoding="utf-8")
    
    chunks = chunker.chunk_file(str(sample_file))
    retriever.store.add(chunks)
    print(f"✓ 索引了 {len(chunks)} 个对话轮次")
    
    # 3. 关键词检索
    print("\n[3/5] 关键词检索...")
    results = retriever.search(query="AI 意识", top_k=3)
    print(f"✓ 找到 {len(results)} 条结果")
    if results:
        print("\n检索结果：")
        print(retriever.format_search_result(results[0]))
    
    # 4. 时间过滤
    print("\n[4/5] 时间过滤...")
    results = retriever.search(
        query="模型",
        top_k=3,
        filter_expr="timestamp >= '2026-04-13T10:00:00' AND timestamp <= '2026-04-13T10:01:00'"
    )
    print(f"✓ 找到 {len(results)} 条结果")
    
    # 5. 轮次导航
    print("\n[5/5] 轮次导航...")
    if results:
        # 提取 turn_id
        turn_id = results[0].metadata.get("turn_id")
        if turn_id:
            print(f"当前轮次 ID: {turn_id}")
            
            # 获取相邻轮次
            session_file = results[0].metadata.get("session_file")
            turn_index = results[0].metadata.get("turn_index")
            
            if session_file and turn_index is not None:
                prev_id, next_id = retriever._get_neighbor_ids(session_file, turn_index)
                print(f"上一轮 ID: {prev_id}")
                print(f"下一轮 ID: {next_id}")
    
    print("\n" + "=" * 60)
    print("快速入门完成！")
    print("=" * 60)
    
    print("\n下一步：")
    print("1. 下载模型: git clone https://gitcode.com/hf_mirrors/BAAI/bge-base-zh-v1.5.git models/bge-base-zh-v1.5")
    print("2. 替换 BGEMockEmbedding → BGEEmbedding(model_path='models/bge-base-zh-v1.5')")
    print("3. 集成到你的 LLM 应用中")


if __name__ == "__main__":
    main()
