#!/usr/bin/env python3
"""
Memory Workflow CLI - 记忆工作流入口

用法:
    python memory_ops.py store --content "要记忆的内容" [--tag tag1]
    python memory_ops.py search --query "查询" [--limit 3] [--json]
    python memory_ops.py dedup [--json]
    python memory_ops.py prune --days 30 [--json]
    python memory_ops.py consolidate [--json]
    python memory_ops.py list --days 7 [--json]
    python memory_ops.py register   # 导出所有工具为 BaseTool 注册格式
"""
import argparse
import json
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# 确保 scripts 目录在 path
SCRIPT_DIR = Path(__file__).parent / "scripts"
sys.path.insert(0, str(Path(__file__).parent))

from scripts.search import search_memories, rag_search
from scripts.store import store_memory
from scripts.config import MEMORY_DIR, get_memory_files

TOOLS = None


def cmd_store(args):
    """存储记忆"""
    content = args.content
    tags = args.tag or []
    session_file = args.session_file

    # 如果指定了 session-file，读取并存储多条消息
    if session_file:
        try:
            with open(session_file, "r", encoding="utf-8") as f:
                session_data = json.load(f)
            messages = session_data.get("messages", [])
            if not isinstance(messages, list):
                messages = [messages]

            results = []
            for msg in messages:
                msg_content = msg.get("content", "") if isinstance(msg, dict) else str(msg)
                if msg_content and not msg_content.strip().startswith("## System"):
                    stored = store_memory(msg_content, tags)
                    results.append(stored)

            skipped = sum(1 for r in results if r.get("skipped"))
            stored_count = sum(1 for r in results if not r.get("skipped"))

            result = {
                "success": True,
                "stored": stored_count,
                "skipped": skipped,
                "message": f"存储完成：{stored_count} 条新记忆，{skipped} 条已存在跳过"
            }
            print(json.dumps(result, ensure_ascii=False))
            return 0
        except Exception as e:
            result = {"success": False, "error": str(e)}
            print(json.dumps(result, ensure_ascii=False))
            return 1

    # 单条存储
    if not content:
        result = {"success": False, "error": "缺少 --content 或 --session-file 参数"}
        print(json.dumps(result, ensure_ascii=False))
        return 1

    stored = store_memory(content, tags if tags else None)
    print(json.dumps(stored, ensure_ascii=False))
    return 0


def cmd_search(args):
    """搜索记忆"""
    query = args.query
    limit = args.limit or 3
    use_rerank = not args.no_rerank
    use_llm = args.llm_answer

    results = search_memories(
        query=query,
        limit=limit,
        use_rerank=use_rerank,
        use_llm=use_llm,
    )

    if args.json:
        print(json.dumps(results, ensure_ascii=False))
    else:
        if results.get("answer"):
            print(f"【总结】{results['answer']}")
            print()
        for r in results.get("results", []):
            date = r.get("date", "")
            score = r.get("rerank_score", r.get("score", 0))
            chunk = r.get("chunk", "")
            print(f"[{date}] (相似度: {score:.2f})")
            print(f"  {chunk[:200]}")
            print()

    return 0


def _ngram(text: str, n: int = 2) -> set:
    """字符级 N-gram"""
    return {text[i:i+n] for i in range(len(text) - n + 1)}


def _jaccard(text1: str, text2: str, n: int = 2) -> float:
    """字符 N-gram Jaccard 相似度"""
    ng1 = _ngram(text1.lower(), n)
    ng2 = _ngram(text2.lower(), n)
    if not ng1 or not ng2:
        return 0.0
    return len(ng1 & ng2) / len(ng1 | ng2) if len(ng1 | ng2) > 0 else 0.0


def cmd_dedup(args):
    """去除重复记忆"""
    from scripts.search import get_all_chunks

    all_chunks = get_all_chunks()
    if not all_chunks:
        result = {"success": True, "message": "记忆库为空，无需去重", "removed": 0}
        if args.json:
            print(json.dumps(result, ensure_ascii=False))
        else:
            print(f"✅ {result['message']}")
        return 0

    # 简单的文本相似度去重（基于 Jaccard 相似度）
    SIMILARITY_THRESHOLD = 0.85
    removed = 0
    seen = []

    for chunk_data in all_chunks:
        chunk = chunk_data["chunk"]
        is_dup = False
        for existing in seen:
            jaccard = _jaccard(chunk, existing["chunk"], n=2)
            if jaccard > SIMILARITY_THRESHOLD:
                # 保留更长的（信息更丰富）
                if len(chunk) > len(existing["chunk"]):
                    existing["duplicate_of"] = chunk_data.get("file", "unknown")
                    existing["chunk"] = chunk
                is_dup = True
                removed += 1
                break
        if not is_dup:
            seen.append(chunk_data)

    result = {
        "success": True,
        "message": f"去重完成，移除 {removed} 条重复记忆",
        "removed": removed,
        "kept": len(seen)
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"✅ {result['message']}，保留 {result['kept']} 条")

    return 0


def cmd_prune(args):
    """删除旧记忆"""
    days = args.days or 30
    cutoff = datetime.now() - timedelta(days=days)

    memory_files = get_memory_files()
    removed = 0
    for mf in memory_files:
        # 从文件名提取日期
        name = mf.stem  # YYYY-MM-DD
        try:
            file_date = datetime.strptime(name, "%Y-%m-%d")
            if file_date < cutoff:
                mf.unlink()
                removed += 1
        except ValueError:
            continue

    result = {
        "success": True,
        "message": f"清理完成，删除 {removed} 个过时记忆文件（>{days}天）",
        "removed": removed
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"✅ {result['message']}")

    return 0


def cmd_consolidate(args):
    """合并相似记忆"""
    from scripts.search import get_all_chunks

    all_chunks = get_all_chunks()
    if len(all_chunks) < 2:
        result = {"success": True, "message": "记忆库条目少于2条，无需合并", "merged": 0}
        if args.json:
            print(json.dumps(result, ensure_ascii=False))
        else:
            print(f"✅ {result['message']}")
        return 0

    # 按日期排序
    all_chunks.sort(key=lambda x: x.get("date", ""))
    merged = 0

    # 合并相邻的相似记忆
    i = 0
    while i < len(all_chunks) - 1:
        curr = all_chunks[i]
        next_chunk = all_chunks[i + 1]

        jaccard = _jaccard(curr["chunk"], next_chunk["chunk"], n=2)
        if jaccard > 0.7:
            # 合并：保留更长的
            if len(next_chunk["chunk"]) > len(curr["chunk"]):
                all_chunks[i] = next_chunk
            all_chunks.pop(i + 1)
            merged += 1
        else:
            i += 1

    result = {
        "success": True,
        "message": f"合并完成，{merged} 组相似记忆已合并",
        "merged": merged,
        "remaining": len(all_chunks)
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"✅ {result['message']}，剩余 {result['remaining']} 条")

    return 0


def cmd_list(args):
    """列出记忆文件"""
    days = args.days or 7
    cutoff = datetime.now() - timedelta(days=days)

    memory_files = get_memory_files()
    files_info = []

    for mf in memory_files:
        name = mf.stem
        try:
            file_date = datetime.strptime(name, "%Y-%m-%d")
            if file_date >= cutoff:
                files_info.append({
                    "file": str(mf),
                    "date": name,
                    "size": mf.stat().st_size
                })
        except ValueError:
            continue

    result = {
        "success": True,
        "files": files_info,
        "count": len(files_info)
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"📋 最近 {days} 天记忆 ({len(files_info)} 个文件):")
        for f in files_info:
            print(f"  [{f['date']}] {f['file']} ({f['size']} bytes)")

    return 0


def cmd_register(args):
    """导出所有工具为 JSON（供 Agent 注册用）"""
    from scripts.tools import (
        MemorySearchTool, MemoryStoreTool, MemoryDedupTool,
        MemoryPruneTool, MemoryConsolidateTool, MemoryListTool
    )

    tools = [
        {
            "name": t.name,
            "description": t.description,
            "input_schema": t.input_schema,
        }
        for t in [
            MemorySearchTool, MemoryStoreTool, MemoryDedupTool,
            MemoryPruneTool, MemoryConsolidateTool, MemoryListTool
        ]
    ]

    print(json.dumps(tools, indent=2, ensure_ascii=False))
    return 0


def main():
    parser = argparse.ArgumentParser(description="Memory Workflow CLI")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # store
    p_store = subparsers.add_parser("store", help="存储记忆")
    p_store.add_argument("--content", help="记忆内容（与 --session-file 二选一）")
    p_store.add_argument("--session-file", help="从 session 文件读取消息列表存储")
    p_store.add_argument("--tag", action="append", help="标签（可多次指定）")
    p_store.add_argument("--json", action="store_true", help="JSON 输出")

    # search
    p_search = subparsers.add_parser("search", help="搜索记忆")
    p_search.add_argument("--query", required=True, help="搜索查询")
    p_search.add_argument("--limit", type=int, default=3)
    p_search.add_argument("--no-rerank", action="store_true", help="禁用 rerank")
    p_search.add_argument("--llm-answer", action="store_true", help="启用 LLM 总结")
    p_search.add_argument("--json", action="store_true", help="JSON 输出")

    # dedup
    p_dedup = subparsers.add_parser("dedup", help="去重")
    p_dedup.add_argument("--json", action="store_true", help="JSON 输出")

    # prune
    p_prune = subparsers.add_parser("prune", help="清理旧记忆")
    p_prune.add_argument("--days", type=int, default=30)
    p_prune.add_argument("--json", action="store_true", help="JSON 输出")

    # consolidate
    p_cons = subparsers.add_parser("consolidate", help="合并相似记忆")
    p_cons.add_argument("--json", action="store_true", help="JSON 输出")

    # list
    p_list = subparsers.add_parser("list", help="列出记忆")
    p_list.add_argument("--days", type=int, default=7)
    p_list.add_argument("--json", action="store_true", help="JSON 输出")

    # register
    subparsers.add_parser("register", help="导出工具定义")

    args = parser.parse_args()

    if args.command == "store":
        return cmd_store(args)
    elif args.command == "search":
        return cmd_search(args)
    elif args.command == "dedup":
        return cmd_dedup(args)
    elif args.command == "prune":
        return cmd_prune(args)
    elif args.command == "consolidate":
        return cmd_consolidate(args)
    elif args.command == "list":
        return cmd_list(args)
    elif args.command == "register":
        return cmd_register(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
