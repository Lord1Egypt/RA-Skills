#!/usr/bin/env python3
"""
memory_manager.py — ontology-pro 知识持久化管理器

功能：
  - 创建/加载/更新/查询 JSON 格式知识图谱
  - 增量合并：新实体、新关系去重追加
  - 版本管理 + 变更日志
  - 上下文注入：生成用于 AI prompt 的图谱摘要

用法：
  python memory_manager.py init   [--domain DOMAIN] [--path PATH]
  python memory_manager.py load   [--path PATH]
  python memory_manager.py add    --entity '{"id":"e001","name":"储能","type":"concept"}'
  python memory_manager.py add    --relation '{"source":"e001","target":"e002","type":"includes","weight":0.9}'
  python memory_manager.py merge  --input graph_delta.json
  python memory_manager.py query  --entity "储能"
  python memory_manager.py summary
  python memory_manager.py list
  python memory_manager.py export --format mermaid

默认存储路径：~/.ontology-pro/graphs/
"""

import argparse
import json
import os
import sys
import hashlib
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

# ──────────────────────────────────────────────
# 配置
# ──────────────────────────────────────────────

DEFAULT_BASE_DIR = Path.home() / ".ontology-pro" / "graphs"
TIMEZONE = timezone(timedelta(hours=8))  # Asia/Shanghai


def now_str() -> str:
    return datetime.now(TIMEZONE).isoformat(timespec="seconds")


def short_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()[:8]


# ──────────────────────────────────────────────
# 图谱数据结构
# ──────────────────────────────────────────────

def new_graph(domain: str = "general") -> dict:
    return {
        "version": "1.0.0",
        "domain": domain,
        "created_at": now_str(),
        "updated_at": now_str(),
        "entities": [],
        "relations": [],
        "sessions": [],
        "changelog": [],
        "metadata": {
            "total_entities": 0,
            "total_relations": 0,
            "sessions_analyzed": 0
        }
    }


def _rebuild_metadata(graph: dict) -> dict:
    graph["metadata"]["total_entities"] = len(graph["entities"])
    graph["metadata"]["total_relations"] = len(graph["relations"])
    graph["metadata"]["sessions_analyzed"] = len(graph["sessions"])
    return graph


# ──────────────────────────────────────────────
# 存储层
# ──────────────────────────────────────────────

def resolve_path(base_dir: Path, domain: str = "general") -> Path:
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / f"{domain}.json"


def save_graph(graph: dict, path: Path) -> None:
    graph["updated_at"] = now_str()
    _rebuild_metadata(graph)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    print(f"[memory_manager] ✅ 图谱已保存 → {path}")


def load_graph(path: Path) -> Optional[dict]:
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ──────────────────────────────────────────────
# 实体操作
# ──────────────────────────────────────────────

def add_entity(graph: dict, entity: dict) -> tuple[dict, bool]:
    """
    添加实体，若 id 已存在则合并 attributes，返回 (graph, is_new)
    """
    existing = {e["id"]: i for i, e in enumerate(graph["entities"])}
    if entity["id"] in existing:
        idx = existing[entity["id"]]
        old = graph["entities"][idx]
        # 合并 attributes
        old_attrs = old.get("attributes", {})
        new_attrs = entity.get("attributes", {})
        old_attrs.update(new_attrs)
        graph["entities"][idx]["attributes"] = old_attrs
        return graph, False
    graph["entities"].append(entity)
    graph["changelog"].append({
        "ts": now_str(),
        "action": "add_entity",
        "id": entity["id"],
        "name": entity.get("name", "")
    })
    return graph, True


def add_relation(graph: dict, relation: dict) -> tuple[dict, bool]:
    """
    添加关系，若 (source, target, type) 三元组已存在则更新 weight，返回 (graph, is_new)
    """
    key = (relation["source"], relation["target"], relation["type"])
    for i, r in enumerate(graph["relations"]):
        if (r["source"], r["target"], r["type"]) == key:
            graph["relations"][i]["weight"] = relation.get("weight", r.get("weight", 0.5))
            if "evidence" in relation:
                graph["relations"][i]["evidence"] = relation["evidence"]
            return graph, False
    relation.setdefault("timestamp", now_str())
    graph["relations"].append(relation)
    graph["changelog"].append({
        "ts": now_str(),
        "action": "add_relation",
        "source": relation["source"],
        "target": relation["target"],
        "type": relation["type"]
    })
    return graph, True


# ──────────────────────────────────────────────
# 增量合并
# ──────────────────────────────────────────────

def merge_delta(graph: dict, delta: dict) -> dict:
    """
    合并增量 JSON（支持 add_entities / add_relations / update_entities / conflicts）
    """
    added_e = added_r = updated_e = 0

    for e in delta.get("add_entities", []):
        graph, is_new = add_entity(graph, e)
        if is_new:
            added_e += 1

    for e in delta.get("update_entities", []):
        graph, _ = add_entity(graph, e)
        updated_e += 1

    for r in delta.get("add_relations", []):
        graph, is_new = add_relation(graph, r)
        if is_new:
            added_r += 1

    for conflict in delta.get("conflicts", []):
        graph["changelog"].append({
            "ts": now_str(),
            "action": "conflict",
            "detail": conflict
        })

    print(f"[memory_manager] 增量合并完成：+{added_e} 实体 | +{added_r} 关系 | ~{updated_e} 更新")
    return graph


# ──────────────────────────────────────────────
# 查询
# ──────────────────────────────────────────────

def query_entity(graph: dict, keyword: str) -> list:
    """模糊匹配实体名称"""
    keyword_lower = keyword.lower()
    results = []
    for e in graph["entities"]:
        name = e.get("name", "")
        aliases = e.get("attributes", {}).get("aliases", [])
        if keyword_lower in name.lower() or any(keyword_lower in a.lower() for a in aliases):
            results.append(e)
    return results


def query_relations(graph: dict, entity_id: str) -> list:
    """查询某实体的所有关系"""
    return [r for r in graph["relations"]
            if r["source"] == entity_id or r["target"] == entity_id]


# ──────────────────────────────────────────────
# 上下文摘要（注入到 AI prompt 用）
# ──────────────────────────────────────────────

def generate_summary(graph: dict, max_entities: int = 20, max_relations: int = 30) -> str:
    """
    生成用于 AI prompt 的图谱摘要文本
    优先输出高 weight 的关系
    """
    meta = graph["metadata"]
    domain = graph.get("domain", "general")
    updated = graph.get("updated_at", "unknown")

    # 高置信关系排序
    sorted_relations = sorted(
        graph["relations"],
        key=lambda r: r.get("weight", 0.5),
        reverse=True
    )[:max_relations]

    # 涉及的实体 ID
    entity_ids = set()
    for r in sorted_relations:
        entity_ids.add(r["source"])
        entity_ids.add(r["target"])

    entity_map = {e["id"]: e["name"] for e in graph["entities"]}

    lines = [
        f"## 知识图谱摘要 [{domain}]",
        f"- 更新时间：{updated}",
        f"- 实体总数：{meta['total_entities']} | 关系总数：{meta['total_relations']}",
        f"- 分析会话：{meta['sessions_analyzed']} 次",
        "",
        "### 关键实体",
    ]

    shown_entities = [e for e in graph["entities"] if e["id"] in entity_ids][:max_entities]
    for e in shown_entities:
        aliases = e.get("attributes", {}).get("aliases", [])
        alias_str = f"（{', '.join(aliases)}）" if aliases else ""
        lines.append(f"- [{e['id']}] {e['name']}{alias_str} | 类型: {e.get('type', '?')}")

    lines += ["", "### 关键关系（按置信度排序）"]
    for r in sorted_relations:
        src_name = entity_map.get(r["source"], r["source"])
        tgt_name = entity_map.get(r["target"], r["target"])
        evidence = r.get("evidence", "")
        ev_str = f' ← "{evidence[:40]}..."' if evidence else ""
        lines.append(
            f"- {src_name} →[{r['type']}]→ {tgt_name} (置信度:{r.get('weight', '?')}){ev_str}"
        )

    return "\n".join(lines)


# ──────────────────────────────────────────────
# 会话记录
# ──────────────────────────────────────────────

def record_session(graph: dict, session_id: str, description: str = "") -> dict:
    graph["sessions"].append({
        "session_id": session_id,
        "timestamp": now_str(),
        "description": description
    })
    return graph


# ──────────────────────────────────────────────
# 列出所有图谱
# ──────────────────────────────────────────────

def list_graphs(base_dir: Path) -> list[dict]:
    results = []
    if not base_dir.exists():
        return results
    for f in sorted(base_dir.glob("*.json")):
        try:
            with open(f, "r", encoding="utf-8") as fp:
                g = json.load(fp)
            results.append({
                "file": f.name,
                "domain": g.get("domain", "?"),
                "entities": g["metadata"]["total_entities"],
                "relations": g["metadata"]["total_relations"],
                "updated_at": g.get("updated_at", "?")
            })
        except Exception:
            pass
    return results


# ──────────────────────────────────────────────
# CLI 入口
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="ontology-pro memory manager — 知识图谱持久化管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("command", choices=[
        "init", "load", "add", "merge", "query", "summary", "list", "session"
    ], help="操作命令")
    parser.add_argument("--domain", default="general", help="领域名称（默认: general）")
    parser.add_argument("--path", default=None, help="图谱存储目录（默认: ~/.ontology-pro/graphs/）")
    parser.add_argument("--entity", default=None, help="实体 JSON 字符串")
    parser.add_argument("--relation", default=None, help="关系 JSON 字符串")
    parser.add_argument("--input", default=None, help="增量合并的 JSON 文件路径")
    parser.add_argument("--keyword", default=None, help="查询关键词")
    parser.add_argument("--session-id", default=None, help="会话 ID")
    parser.add_argument("--description", default="", help="会话描述")
    parser.add_argument("--max-entities", type=int, default=20, help="摘要最大实体数")
    parser.add_argument("--max-relations", type=int, default=30, help="摘要最大关系数")

    args = parser.parse_args()

    # 解析路径
    base_dir = Path(args.path) if args.path else DEFAULT_BASE_DIR
    graph_path = resolve_path(base_dir, args.domain)

    # ── init ──
    if args.command == "init":
        if graph_path.exists():
            print(f"[memory_manager] ⚠️  图谱已存在：{graph_path}")
            print("  使用 load 命令加载，或手动删除后重新初始化。")
            return
        graph = new_graph(domain=args.domain)
        save_graph(graph, graph_path)
        print(f"[memory_manager] 🎉 初始化完成 | 领域: {args.domain} | 路径: {graph_path}")

    # ── load ──
    elif args.command == "load":
        graph = load_graph(graph_path)
        if graph is None:
            print(f"[memory_manager] ❌ 图谱不存在：{graph_path}（请先执行 init）")
            return
        meta = graph["metadata"]
        print(f"[memory_manager] ✅ 图谱已加载")
        print(f"  领域: {graph['domain']} | 实体: {meta['total_entities']} | 关系: {meta['total_relations']}")
        print(f"  最后更新: {graph.get('updated_at', 'unknown')}")

    # ── add ──
    elif args.command == "add":
        graph = load_graph(graph_path)
        if graph is None:
            print(f"[memory_manager] ❌ 图谱不存在，请先执行 init")
            return
        if args.entity:
            try:
                entity = json.loads(args.entity)
                graph, is_new = add_entity(graph, entity)
                action = "新增" if is_new else "合并更新"
                print(f"[memory_manager] {action} 实体: [{entity['id']}] {entity.get('name', '')}")
            except json.JSONDecodeError as e:
                print(f"[memory_manager] ❌ 实体 JSON 解析失败: {e}")
                return
        if args.relation:
            try:
                relation = json.loads(args.relation)
                graph, is_new = add_relation(graph, relation)
                action = "新增" if is_new else "更新"
                print(f"[memory_manager] {action} 关系: {relation['source']} →[{relation['type']}]→ {relation['target']}")
            except json.JSONDecodeError as e:
                print(f"[memory_manager] ❌ 关系 JSON 解析失败: {e}")
                return
        save_graph(graph, graph_path)

    # ── merge ──
    elif args.command == "merge":
        if not args.input:
            print("[memory_manager] ❌ 请指定 --input 增量 JSON 文件")
            return
        graph = load_graph(graph_path)
        if graph is None:
            print(f"[memory_manager] ❌ 图谱不存在，请先执行 init")
            return
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                delta = json.load(f)
        except Exception as e:
            print(f"[memory_manager] ❌ 读取增量文件失败: {e}")
            return
        graph = merge_delta(graph, delta)
        save_graph(graph, graph_path)

    # ── query ──
    elif args.command == "query":
        graph = load_graph(graph_path)
        if graph is None:
            print(f"[memory_manager] ❌ 图谱不存在")
            return
        keyword = args.keyword or ""
        results = query_entity(graph, keyword)
        if not results:
            print(f"[memory_manager] 未找到匹配 '{keyword}' 的实体")
            return
        print(f"[memory_manager] 找到 {len(results)} 个匹配实体：")
        entity_map = {e["id"]: e["name"] for e in graph["entities"]}
        for e in results:
            print(f"\n  [{e['id']}] {e['name']} ({e.get('type', '?')})")
            attrs = e.get("attributes", {})
            if attrs:
                print(f"    属性: {json.dumps(attrs, ensure_ascii=False)}")
            relations = query_relations(graph, e["id"])
            if relations:
                print(f"    关系({len(relations)}):")
                for r in relations[:5]:
                    src_name = entity_map.get(r["source"], r["source"])
                    tgt_name = entity_map.get(r["target"], r["target"])
                    print(f"      {src_name} →[{r['type']}]→ {tgt_name} (w={r.get('weight', '?')})")

    # ── summary ──
    elif args.command == "summary":
        graph = load_graph(graph_path)
        if graph is None:
            print(f"[memory_manager] ❌ 图谱不存在")
            return
        summary = generate_summary(graph, args.max_entities, args.max_relations)
        print(summary)

    # ── list ──
    elif args.command == "list":
        graphs = list_graphs(base_dir)
        if not graphs:
            print(f"[memory_manager] 暂无图谱（目录: {base_dir}）")
            return
        print(f"[memory_manager] 共 {len(graphs)} 个图谱（{base_dir}）：")
        print(f"  {'领域':<20} {'实体':>6} {'关系':>6}  最后更新")
        print("  " + "-" * 60)
        for g in graphs:
            print(f"  {g['domain']:<20} {g['entities']:>6} {g['relations']:>6}  {g['updated_at']}")

    # ── session ──
    elif args.command == "session":
        graph = load_graph(graph_path)
        if graph is None:
            print(f"[memory_manager] ❌ 图谱不存在")
            return
        session_id = args.session_id or short_hash(now_str())
        graph = record_session(graph, session_id, args.description)
        save_graph(graph, graph_path)
        print(f"[memory_manager] 会话已记录: {session_id} | {args.description}")


if __name__ == "__main__":
    main()
