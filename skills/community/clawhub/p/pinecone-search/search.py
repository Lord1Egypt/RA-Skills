#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pinecone 知识库搜索命令 - 支持混合搜索、元数据过滤、相似度阈值
"""

import argparse
import sys

from pinecone_tool import KnowledgeBase, Config


def main():
    parser = argparse.ArgumentParser(
        description="搜索 Pinecone 知识库（支持混合搜索）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础搜索
  python search.py "混凝土浇筑标准是什么？"

  # 返回更多结果
  python search.py "查询内容" --top-k 10

  # 按命名空间过滤
  python search.py "查询" --namespace project-a

  # 按文件类型过滤
  python search.py "查询" --file-type markdown

  # 按文件名过滤（支持部分匹配）
  python search.py "查询" --filename "施工规范"

  # 设置相似度阈值（只返回相似度>0.7的结果）
  python search.py "查询" --min-score 0.7

  # 纯向量搜索（不使用混合排序）
  python search.py "查询" --no-hybrid

  # 组合使用
  python search.py "混凝土标准" --file-type markdown --min-score 0.6 --top-k 5
        """
    )

    parser.add_argument(
        "query",
        type=str,
        help="搜索查询内容"
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="返回结果数量 (默认: 3)"
    )

    parser.add_argument(
        "-n", "--namespace",
        type=str,
        default="",
        help="Pinecone 命名空间"
    )

    parser.add_argument(
        "--file-type",
        type=str,
        choices=["markdown", "txt"],
        help="按文件类型过滤 (markdown 或 txt)"
    )

    parser.add_argument(
        "--filename",
        type=str,
        help="按文件名过滤（支持部分匹配，如 '施工规范' 匹配 '施工规范.md'）"
    )

    parser.add_argument(
        "--min-score",
        type=float,
        default=0.0,
        help="最小相似度阈值 0-1 (默认: 0，不过滤)"
    )

    parser.add_argument(
        "--no-hybrid",
        action="store_true",
        help="禁用混合搜索，仅使用向量搜索"
    )

    parser.add_argument(
        "--vector-candidates",
        type=int,
        default=20,
        help="混合搜索时的向量候选集大小 (默认: 20)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细分数（向量分数、BM25分数、混合分数）"
    )

    args = parser.parse_args()

    # 验证参数
    if args.min_score < 0 or args.min_score > 1:
        print("错误: --min-score 必须在 0-1 之间", file=sys.stderr)
        sys.exit(1)

    # 加载配置
    try:
        config = Config()
        if args.namespace:
            config.NAMESPACE = args.namespace
    except Exception as e:
        print(f"配置错误: {e}", file=sys.stderr)
        print("\n请确保 .env 文件中包含以下配置:", file=sys.stderr)
        print("  PINECONE_API_KEY=your_key", file=sys.stderr)
        print("  EMBEDDING_API_KEY=your_key", file=sys.stderr)
        print("  EMBEDDING_BASE_URL=your_url", file=sys.stderr)
        sys.exit(1)

    # 初始化知识库
    kb = KnowledgeBase(config)

    print(f"正在搜索: {args.query}")

    # 显示搜索配置
    filters = []
    if args.file_type:
        filters.append(f"文件类型={args.file_type}")
    if args.filename:
        filters.append(f"文件名包含='{args.filename}'")
    if args.min_score > 0:
        filters.append(f"相似度>={args.min_score}")
    if not args.no_hybrid:
        filters.append(f"混合搜索(候选集={args.vector_candidates})")

    if filters:
        print(f"过滤条件: {' | '.join(filters)}")
    print()

    try:
        # 执行搜索
        results = kb.search(
            query=args.query,
            top_k=args.top_k,
            min_score=args.min_score,
            file_type=args.file_type,
            filename=args.filename,
            use_hybrid=not args.no_hybrid,
            vector_candidates=args.vector_candidates
        )

        if results:
            print("=" * 70)
            for i, result in enumerate(results, 1):
                metadata = result.get("metadata", {})
                print(f"\n[结果 #{i}]")

                # 显示分数
                if args.verbose and not args.no_hybrid:
                    print(f"混合分数: {result.get('hybrid_score', 0):.4f}")
                    print(f"向量分数: {result.get('vector_score', 0):.4f}")
                    print(f"BM25分数: {result.get('bm25_score', 0):.4f}")
                else:
                    score = result.get('hybrid_score') if not args.no_hybrid else result.get('score')
                    print(f"匹配度: {score:.4f}")

                print(f"来源: {metadata.get('source', 'N/A')}")
                print(f"文件名: {metadata.get('filename', 'N/A')}")
                if metadata.get('title'):
                    print(f"标题: {metadata['title']}")
                print(f"文件类型: {metadata.get('file_type', 'N/A')}")
                print(f"块索引: {metadata.get('chunk_index', 0) + 1}/{metadata.get('total_chunks', 1)}")

                print(f"内容:")
                text = metadata.get('text', '')
                # 格式化输出，限制宽度
                lines = [text[i:i+68] for i in range(0, len(text), 68)]
                for line in lines[:15]:  # 最多显示15行
                    print(f"  {line}")
                if len(lines) > 15:
                    print(f"  ... ({len(lines) - 15} 行省略)")
                print("-" * 70)
        else:
            print("未找到任何结果")
            print("\n建议:")
            print("  - 尝试降低 --min-score 阈值")
            print("  - 尝试移除 --file-type 或 --filename 过滤")
            print("  - 尝试使用 --no-hybrid 禁用混合搜索")

    except Exception as e:
        print(f"搜索失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
