#!/usr/bin/env python3
"""
NovaMemory CLI — 命令行记忆工具

用法示例:
    python memory_cli.py remember "内容" --tags tag1,tag2
    python memory_cli.py recall "查询"
    python memory_cli.py entity add "名字" --facts k=v,k2=v2
    python memory_cli.py entity get "名字"
    python memory_cli.py tags search "标签"
    python memory_cli.py graph
    python memory_cli.py reflect
    python memory_cli.py stats
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# 添加 src 到路径，支持直接运行脚本
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))

from memory_core import NovaMemory


# ---------------------------------------------------------------------------
# 默认存储路径
# ---------------------------------------------------------------------------
DEFAULT_STORAGE = "/workspace/memory/nova-memory"


# ---------------------------------------------------------------------------
# 命令处理器
# ---------------------------------------------------------------------------

def cmd_remember(args: argparse.Namespace) -> None:
    """记忆一条信息。"""
    mem = NovaMemory(storage_dir=args.storage or DEFAULT_STORAGE)

    tags = None
    if args.tags:
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]

    mid = mem.remember(content=args.content, tags=tags, entity=args.entity)
    mem.save()

    print(f"✅ 已记忆，ID: {mid}")
    print(f"   内容: {args.content[:80]}{'…' if len(args.content) > 80 else ''}")
    if tags:
        print(f"   标签: {', '.join(tags)}")
    if args.entity:
        print(f"   实体: {args.entity}")


def cmd_recall(args: argparse.Namespace) -> None:
    """语义检索记忆。"""
    mem = NovaMemory(storage_dir=args.storage or DEFAULT_STORAGE)

    results = mem.recall(args.query, top_k=args.top_k)

    if not results:
        print("📭 未找到相关记忆。")
        return

    print(f"🔍 找到 {len(results)} 条相关记忆（top_k={args.top_k}）：\n")
    for i, r in enumerate(results, 1):
        tags_str = f" [🏷️ {', '.join(r['tags'])}]" if r["tags"] else ""
        entity_str = f" 👤 {r['entity']}" if r.get("entity") else ""
        print(f"  {i}. 【{r['score']:.4f}】{r['content'][:100]}{'…' if len(r['content']) > 100 else ''}{tags_str}{entity_str}")
        print(f"     ↳ ID: {r['id']} | 创建: {r.get('created_at', 'N/A')[:10]}\n")


def cmd_entity_add(args: argparse.Namespace) -> None:
    """添加/更新实体。"""
    mem = NovaMemory(storage_dir=args.storage or DEFAULT_STORAGE)

    facts: dict[str, str] = {}
    if args.facts:
        for item in args.facts.split(","):
            if "=" in item:
                k, v = item.split("=", 1)
                facts[k.strip()] = v.strip()

    mem.remember_entity(args.name, facts)
    mem.save()

    print(f"✅ 实体「{args.name}」已更新，属性：")
    for k, v in facts.items():
        print(f"   {k} = {v}")


def cmd_entity_get(args: argparse.Namespace) -> None:
    """获取实体信息。"""
    mem = NovaMemory(storage_dir=args.storage or DEFAULT_STORAGE)

    info = mem.get_entity(args.name)
    if not info:
        print(f"📭 未找到实体「{args.name}」")
        return

    print(f"👤 实体「{args.name}」：")
    for k, v in info.items():
        if not k.startswith("_"):
            print(f"   {k}: {v}")


def cmd_entity_list(args: argparse.Namespace) -> None:
    """列出所有实体。"""
    mem = NovaMemory(storage_dir=args.storage or DEFAULT_STORAGE)
    graph = mem.get_memory_graph()

    entities = [n for n in graph["nodes"] if n["type"] == "entity"]
    if not entities:
        print("📭 暂无实体记录。")
        return

    print(f"👥 共 {len(entities)} 个实体：\n")
    for e in entities:
        facts = e.get("facts", {})
        fact_preview = ", ".join(f"{k}={v}" for k, v in list(facts.items())[:3])
        print(f"  • {e['label']}")
        if fact_preview:
            print(f"    {fact_preview}")


def cmd_tags_search(args: argparse.Namespace) -> None:
    """按标签搜索记忆。"""
    mem = NovaMemory(storage_dir=args.storage or DEFAULT_STORAGE)

    results = mem.search_by_tag(args.tag)
    if not results:
        print(f"📭 没有找到标签为「{args.tag}」的记忆。")
        return

    print(f"🏷️ 标签「{args.tag}」共 {len(results)} 条记忆：\n")
    for r in results:
        entity_str = f" 👤 {r.get('entity', '')}" if r.get("entity") else ""
        print(f"  • {r['content'][:100]}{'…' if len(r['content']) > 100 else ''}{entity_str}")
        print(f"    ID: {r['id']} | 创建: {r.get('created_at', 'N/A')[:10]}\n")


def cmd_graph(args: argparse.Namespace) -> None:
    """打印记忆图谱。"""
    mem = NovaMemory(storage_dir=args.storage or DEFAULT_STORAGE)
    graph = mem.get_memory_graph()

    stats = graph.get("stats", {})
    print(f"🕸️ 记忆图谱概览")
    print(f"   记忆总数: {stats.get('total_memories', 0)}")
    print(f"   实体总数: {stats.get('total_entities', 0)}")
    print(f"   标签总数: {stats.get('total_tags', 0)}")
    print()

    # 实体节点
    entities = [n for n in graph["nodes"] if n["type"] == "entity"]
    if entities:
        print("👥 实体节点：")
        for e in entities:
            facts = e.get("facts", {})
            fact_str = " | ".join(f"{k}={v}" for k, v in list(facts.items())[:4])
            print(f"  ● {e['label']} {('(' + fact_str + ')') if fact_str else ''}")
        print()

    # 边
    edges = graph.get("edges", [])
    if edges:
        print(f"🔗 关系边（共 {len(edges)} 条）：")
        for edge in edges[:20]:  # 最多展示 20 条
            print(f"  {edge['from']} --[{edge.get('label', 'related')}]--> {edge.get('to', '')}")
        if len(edges) > 20:
            print(f"  … 还有 {len(edges) - 20} 条边")
        print()

    # 记忆节点（仅展示有实体的）
    memories = [n for n in graph["nodes"] if n["type"] == "memory"]
    if memories:
        print(f"💭 近期记忆节点（关联实体的前 10 条）：")
        for m in memories[:10]:
            tags_str = f"[{'|'.join(m.get('tags', [])[:3])}]"
            print(f"  ○ {m['label']} {tags_str} ← {m.get('entity', '')}")


def cmd_reflect(args: argparse.Namespace) -> None:
    """运行自动反思。"""
    mem = NovaMemory(storage_dir=args.storage or DEFAULT_STORAGE)
    report = mem.auto_reflect()
    print(report)


def cmd_stats(args: argparse.Namespace) -> None:
    """显示记忆库统计。"""
    mem = NovaMemory(storage_dir=args.storage or DEFAULT_STORAGE)
    stats = mem.stats

    print("📊 NovaMemory 统计：")
    print(f"   总记忆数 : {stats['total_memories']}")
    print(f"   总实体数 : {stats['total_entities']}")
    print(f"   总标签数 : {stats['total_tags']}")
    print(f"   存储路径 : {mem.storage_dir}")

    # top tags
    if mem._tag_index:
        top_tags = sorted(mem._tag_index.items(), key=lambda x: len(x[1]), reverse=True)[:5]
        print("\n🏷️ 标签 TOP5（按记忆数量）：")
        for tag, mids in top_tags:
            print(f"   {tag:<20} {len(mids)} 条记忆")


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nova-memory",
        description="Nova 工作空间记忆技能 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--storage",
        default=None,
        help=f"存储目录（默认：{DEFAULT_STORAGE}）",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # remember
    p_remember = sub.add_parser("remember", help="记忆一条信息")
    p_remember.add_argument("content", help="记忆内容")
    p_remember.add_argument("--tags", help="逗号分隔的标签")
    p_remember.add_argument("--entity", help="关联实体名称")
    p_remember.set_defaults(func=cmd_remember)

    # recall
    p_recall = sub.add_parser("recall", help="语义检索记忆")
    p_recall.add_argument("query", help="查询内容")
    p_recall.add_argument("--top-k", type=int, default=5, help="返回数量（默认 5）")
    p_recall.set_defaults(func=cmd_recall)

    # entity add
    p_ent_add = sub.add_parser("entity", help="实体操作（子命令见 sub-add/sub-get/sub-list）")
    p_ent_subs = p_ent_add.add_subparsers(dest="entity_cmd", required=True)

    p_add = p_ent_subs.add_parser("add", help="添加/更新实体")
    p_add.add_argument("name", help="实体名称")
    p_add.add_argument("--facts", required=True, help="属性，格式 k=v,k2=v2")
    p_add.set_defaults(func=cmd_entity_add)

    p_get = p_ent_subs.add_parser("get", help="获取实体信息")
    p_get.add_argument("name", help="实体名称")
    p_get.set_defaults(func=cmd_entity_get)

    p_list = p_ent_subs.add_parser("list", help="列出所有实体")
    p_list.set_defaults(func=cmd_entity_list)

    # tags
    p_tags = sub.add_parser("tags", help="标签操作")
    p_tags_subs = p_tags.add_subparsers(dest="tags_cmd", required=True)

    p_search = p_tags_subs.add_parser("search", help="按标签搜索")
    p_search.add_argument("tag", help="标签名")
    p_search.set_defaults(func=cmd_tags_search)

    # graph
    p_graph = sub.add_parser("graph", help="打印记忆图谱")
    p_graph.set_defaults(func=cmd_graph)

    # reflect
    p_reflect = sub.add_parser("reflect", help="运行自动反思")
    p_reflect.set_defaults(func=cmd_reflect)

    # stats
    p_stats = sub.add_parser("stats", help="显示统计信息")
    p_stats.set_defaults(func=cmd_stats)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # 处理 entity 子命令分发
    if hasattr(args, "entity_cmd"):
        entity_dispatch = {
            "add": cmd_entity_add,
            "get": cmd_entity_get,
            "list": cmd_entity_list,
        }
        args.func = entity_dispatch.get(args.entity_cmd, cmd_entity_list)

    # 处理 tags 子命令分发
    if hasattr(args, "tags_cmd"):
        if args.tags_cmd == "search":
            args.func = cmd_tags_search

    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\n⏹ 中断")
        sys.exit(0)
    except Exception as exc:
        print(f"❌ 错误：{exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
