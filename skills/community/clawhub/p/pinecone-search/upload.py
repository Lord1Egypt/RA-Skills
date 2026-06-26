#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档上传命令 - 支持 TXT、Markdown 文件上传到 Pinecone
"""

import argparse
import json
import sys
from pathlib import Path

from pinecone_tool import KnowledgeBase, Config, UploadStats


def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def print_stats(stats: UploadStats):
    """打印上传统计信息"""
    print("\n" + "=" * 60)
    print("上传统计报告")
    print("=" * 60)

    print(f"\nWorkspace: {stats.workspace}")
    print(f"Namespace: {stats.namespace if stats.namespace else 'default'}")
    print(f"总文件数: {stats.total_files}")
    print(f"总块数: {stats.total_chunks}")
    print(f"成功上传: {stats.successful_chunks}")
    print(f"失败: {stats.failed_chunks}")

    if stats.end_time and stats.start_time:
        duration = (stats.end_time - stats.start_time).total_seconds()
        print(f"耗时: {duration:.2f} 秒")
        if stats.successful_chunks > 0:
            print(f"平均速度: {stats.successful_chunks / duration:.2f} chunks/秒")

    if stats.file_stats:
        print("\n文件详情:")
        print("-" * 60)
        for file_stat in stats.file_stats:
            print(f"  {file_stat['filename']}")
            print(f"     路径: {file_stat['source']}")
            print(f"     类型: {file_stat['file_type']}")
            print(f"     块数: {file_stat['chunks']}")
            print(f"     Token数: {file_stat.get('tokens', 'N/A')}")
            if 'successful' in file_stat:
                print(f"     成功: {file_stat['successful']}")
            if 'failed' in file_stat and file_stat['failed'] > 0:
                print(f"     失败: {file_stat['failed']}")
            print()

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="上传文档到 Pinecone 知识库",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 上传单个文件
  python upload.py path/to/file.txt

  # 上传多个文件
  python upload.py file1.txt file2.md

  # 上传整个目录
  python upload.py ./docs/ --recursive

  # 指定命名空间
  python upload.py ./docs/ --namespace project-a

  # 自定义分块大小
  python upload.py ./docs/ --chunk-size 512 --overlap 100

  # 输出 JSON 格式统计（供 agent 使用）
  python upload.py ./docs/ --json
        """
    )

    parser.add_argument(
        "paths",
        nargs="+",
        help="要上传的文件或目录路径"
    )

    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="递归上传目录中的文件"
    )

    parser.add_argument(
        "-n", "--namespace",
        type=str,
        default="",
        help="Pinecone 命名空间"
    )

    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1000,
        help="每个文本块的 token 数量（默认: 1000）"
    )

    parser.add_argument(
        "--overlap",
        type=int,
        default=200,
        help="文本块之间的重叠 token 数量（默认: 200）"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 格式输出统计信息"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="预览模式，不实际上传"
    )

    args = parser.parse_args()

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

    # 收集所有要处理的文件
    files_to_process = []
    directories_to_process = []

    for path_str in args.paths:
        path = Path(path_str)

        if not path.exists():
            print(f"路径不存在: {path_str}")
            continue

        if path.is_file():
            files_to_process.append(path_str)
        elif path.is_dir():
            directories_to_process.append(path_str)

    # 检查是否有有效路径
    if not files_to_process and not directories_to_process:
        print("没有有效的文件或目录需要处理")
        sys.exit(1)

    # 预览模式
    if args.dry_run:
        print("预览模式（不实际上传）\n")

        all_files = []

        # 收集单个文件
        for file_path in files_to_process:
            doc = kb.loader.load(file_path)
            if doc:
                all_files.append(doc)

        # 收集目录文件
        for dir_path in directories_to_process:
            docs = kb.loader.load_directory(dir_path, args.recursive)
            all_files.extend(docs)

        print(f"找到 {len(all_files)} 个文件:\n")

        total_chunks = 0
        for doc in all_files:
            chunks = kb.splitter.split(doc)
            total_chunks += len(chunks)

            print(f"  {doc.filename}")
            print(f"     路径: {doc.source}")
            print(f"     类型: {doc.file_type}")
            print(f"     大小: {format_size(doc.metadata.get('size_bytes', 0))}")
            print(f"     预计块数: {len(chunks)}")
            print()

        print(f"\n预计总块数: {total_chunks}")
        print("\n预览完成，移除 --dry-run 参数执行实际上传")
        return

    # 执行上传
    all_stats = []

    # 上传单个文件
    for file_path in files_to_process:
        print(f"\n正在上传文件: {file_path}")
        stats = kb.upload_file(
            file_path,
            chunk_size=args.chunk_size,
            chunk_overlap=args.overlap
        )
        all_stats.append(stats)

        if not args.json:
            print_stats(stats)

    # 上传目录
    for dir_path in directories_to_process:
        print(f"\n正在上传目录: {dir_path}")
        stats = kb.upload_directory(
            dir_path,
            recursive=args.recursive,
            chunk_size=args.chunk_size,
            chunk_overlap=args.overlap
        )
        all_stats.append(stats)

        if not args.json:
            print_stats(stats)

    # 合并统计信息
    merged_stats = {
        "workspace": config.INDEX_NAME,
        "namespace": config.NAMESPACE if config.NAMESPACE else "default",
        "total_files": sum(s.total_files for s in all_stats),
        "total_chunks": sum(s.total_chunks for s in all_stats),
        "successful_chunks": sum(s.successful_chunks for s in all_stats),
        "failed_chunks": sum(s.failed_chunks for s in all_stats),
        "files": []
    }

    for stats in all_stats:
        merged_stats["files"].extend(stats.file_stats)

    # 计算总耗时
    if all_stats and all_stats[0].start_time and all_stats[-1].end_time:
        total_duration = (all_stats[-1].end_time - all_stats[0].start_time).total_seconds()
        merged_stats["duration_seconds"] = total_duration

    # JSON 输出（供 agent 使用）
    if args.json:
        print(json.dumps(merged_stats, ensure_ascii=False, indent=2))
    else:
        # 打印汇总
        print("\n" + "=" * 60)
        print("上传汇总")
        print("=" * 60)
        print(f"Workspace: {merged_stats['workspace']}")
        print(f"Namespace: {merged_stats['namespace']}")
        print(f"总文件数: {merged_stats['total_files']}")
        print(f"总块数: {merged_stats['total_chunks']}")
        print(f"成功上传: {merged_stats['successful_chunks']}")
        print(f"失败: {merged_stats['failed_chunks']}")
        if 'duration_seconds' in merged_stats:
            print(f"总耗时: {merged_stats['duration_seconds']:.2f} 秒")
        print("=" * 60)


if __name__ == "__main__":
    main()
