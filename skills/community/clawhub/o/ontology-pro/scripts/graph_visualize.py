#!/usr/bin/env python3
"""
graph_visualize.py — ontology-pro 知识图谱可视化工具

功能：
  - JSON 图谱 → Mermaid flowchart 文本（可渲染为图谱）
  - JSON 图谱 → Mermaid mindmap 文本（以核心实体为根）
  - JSON 图谱 → 统计摘要报告
  - 支持过滤：按实体类型 / 关系类型 / 最小 weight 过滤

用法：
  python graph_visualize.py --input graph.json
  python graph_visualize.py --input graph.json --format flowchart --output graph.md
  python graph_visualize.py --input graph.json --format mindmap --center "储能系统"
  python graph_visualize.py --input graph.json --format stats
  python graph_visualize.py --domain general                  # 从默认存储读取
  python graph_visualize.py --domain energy --min-weight 0.6 --max-nodes 30

支持的 Mermaid 格式：
  flowchart   有向图，适合展示关系网络（默认）
  mindmap     思维导图，以某个中心实体为根展开
  stats       文本统计报告（不是图，是摘要数据）
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Optional

DEFAULT_BASE_DIR = Path.home() / ".ontology-pro" / "graphs"

# Mermaid 中不允许的字符，需要清洗
MERMAID_ESCAPE_RE = re.compile(r'["\[\](){}|<>]')

# 关系类型 → Mermaid 箭头样式
RELATION_ARROW = {
    "is_a":         "-->",
    "part_of":      "-->",
    "includes":     "-->",
    "causes":       "==>",
    "depends_on":   "-.->",
    "related_to":   "<-->",
    "contradicts":  "x--x",
    "similar_to":   "---",
    "regulated_by": "-.->",
    "located_in":   "-->",
}

# 实体类型 → Mermaid 节点形状
ENTITY_SHAPE = {
    "organization":     ("[", "]"),
    "person":           ("((", "))"),
    "product":          ("[/", "/]"),
    "technology":       ("[", "]"),
    "concept":          ("([", "])"),
    "event":            (">", "]"),
    "document":         ("[", "]"),
    "location":         ("(", ")"),
    "metric":           ("{", "}"),
    "role":             ("[", "]"),
    # 能源领域
    "energy_source":    ("([", "])"),
    "market_mechanism": ("{", "}"),
    "policy":           ("[/", "/]"),
    "equipment":        ("[", "]"),
    # 医疗领域
    "disease":          ("([", "])"),
    "treatment":        ("[", "]"),
    "biomarker":        ("{", "}"),
    "institution":      ("[", "]"),
    # AI 领域
    "model":            ("([", "])"),
    "algorithm":        ("[", "]"),
    "dataset":          ("[/", "/]"),
}

DEFAULT_SHAPE = ("[", "]")

# 颜色主题（按实体类型分组着色）
COLOR_GROUPS = {
    "concept_group":      ["concept", "technology", "algorithm"],
    "org_group":          ["organization", "institution"],
    "domain_group":       ["energy_source", "market_mechanism", "disease", "treatment", "model"],
    "document_group":     ["document", "policy", "dataset"],
}

COLOR_CSS = {
    "concept_group":  "fill:#dbeafe,stroke:#3b82f6,color:#1e40af",
    "org_group":      "fill:#dcfce7,stroke:#22c55e,color:#166534",
    "domain_group":   "fill:#fef9c3,stroke:#eab308,color:#713f12",
    "document_group": "fill:#fce7f3,stroke:#ec4899,color:#831843",
}


def clean_mermaid(text: str) -> str:
    """清洗节点名称，防止 Mermaid 语法冲突"""
    text = MERMAID_ESCAPE_RE.sub("", text)
    return text.strip()


def node_id(entity_id: str) -> str:
    """将实体 ID 转换为合法的 Mermaid 节点 ID"""
    return entity_id.replace("-", "_").replace(" ", "_")


# ──────────────────────────────────────────────
# Mermaid Flowchart 生成
# ──────────────────────────────────────────────

def to_flowchart(
    graph: dict,
    max_nodes: int = 40,
    max_edges: int = 60,
    min_weight: float = 0.0,
    filter_entity_types: Optional[list] = None,
    filter_relation_types: Optional[list] = None,
) -> str:
    """
    生成 Mermaid flowchart 文本
    """
    entities = graph.get("entities", [])
    relations = graph.get("relations", [])

    # 过滤关系
    filtered_relations = [
        r for r in relations
        if r.get("weight", 0.5) >= min_weight
        and (filter_relation_types is None or r["type"] in filter_relation_types)
    ]
    # 按 weight 降序截取
    filtered_relations = sorted(
        filtered_relations, key=lambda r: r.get("weight", 0.5), reverse=True
    )[:max_edges]

    # 确定涉及的实体 ID
    used_ids = set()
    for r in filtered_relations:
        used_ids.add(r["source"])
        used_ids.add(r["target"])

    # 过滤实体
    filtered_entities = [
        e for e in entities
        if e["id"] in used_ids
        and (filter_entity_types is None or e.get("type") in filter_entity_types)
    ][:max_nodes]
    filtered_entity_ids = {e["id"] for e in filtered_entities}

    # 再次过滤关系（保证两端实体都在过滤集中）
    filtered_relations = [
        r for r in filtered_relations
        if r["source"] in filtered_entity_ids and r["target"] in filtered_entity_ids
    ]

    lines = [
        "```mermaid",
        "flowchart TD",
        "",
        "  %% === 节点定义 ==="
    ]

    # 实体分组（用于着色）
    type_to_group = {}
    for group_name, types in COLOR_GROUPS.items():
        for t in types:
            type_to_group[t] = group_name

    group_nodes = defaultdict(list)

    for e in filtered_entities:
        nid = node_id(e["id"])
        name = clean_mermaid(e.get("name", e["id"]))
        etype = e.get("type", "")
        shape_open, shape_close = ENTITY_SHAPE.get(etype, DEFAULT_SHAPE)
        label = f'{name}\\n<small>{etype}</small>' if etype else name
        lines.append(f'  {nid}{shape_open}"{name}"{shape_close}')
        group = type_to_group.get(etype)
        if group:
            group_nodes[group].append(nid)

    lines += ["", "  %% === 关系定义 ==="]

    for r in filtered_relations:
        src = node_id(r["source"])
        tgt = node_id(r["target"])
        rtype = r.get("type", "related_to")
        arrow = RELATION_ARROW.get(rtype, "-->")
        weight = r.get("weight", 0.5)
        weight_str = f"{weight:.1f}" if isinstance(weight, float) else str(weight)
        lines.append(f'  {src} {arrow}|"{rtype} w={weight_str}"| {tgt}')

    # 添加样式
    lines += ["", "  %% === 节点样式 ==="]
    for group_name, node_ids in group_nodes.items():
        css = COLOR_CSS.get(group_name, "")
        if css and node_ids:
            ids_str = ",".join(node_ids)
            lines.append(f"  style {node_ids[0]} {css}")
            if len(node_ids) > 1:
                lines.append(f"  classDef {group_name} {css}")
                lines.append(f"  class {ids_str} {group_name}")

    lines.append("```")
    return "\n".join(lines)


# ──────────────────────────────────────────────
# Mermaid Mindmap 生成
# ──────────────────────────────────────────────

def to_mindmap(
    graph: dict,
    center: Optional[str] = None,
    max_depth: int = 2,
    max_children: int = 6,
) -> str:
    """
    生成 Mermaid mindmap 文本
    center: 中心实体名称（默认选关系最多的实体）
    """
    entities = graph.get("entities", [])
    relations = graph.get("relations", [])

    if not entities:
        return "```mermaid\nmindmap\n  root((空图谱))\n```"

    entity_map = {e["id"]: e for e in entities}
    name_to_id = {e.get("name", e["id"]): e["id"] for e in entities}

    # 确定中心实体
    if center:
        center_id = name_to_id.get(center) or center
    else:
        # 选出度最大的实体（关系最多）
        degree = defaultdict(int)
        for r in relations:
            degree[r["source"]] += 1
            degree[r["target"]] += 1
        center_id = max(degree, key=lambda k: degree[k]) if degree else entities[0]["id"]

    center_entity = entity_map.get(center_id, {"id": center_id, "name": center_id})
    center_name = clean_mermaid(center_entity.get("name", center_id))

    # 建立邻接表
    adjacency = defaultdict(list)
    for r in relations:
        adjacency[r["source"]].append((r["target"], r["type"], r.get("weight", 0.5)))
        if r["type"] in ("related_to", "similar_to", "contradicts"):
            adjacency[r["target"]].append((r["source"], r["type"], r.get("weight", 0.5)))

    lines = ["```mermaid", "mindmap", f"  root(({center_name}))"]

    visited = {center_id}

    def render_children(parent_id: str, depth: int, indent: str):
        if depth > max_depth:
            return
        neighbors = sorted(adjacency[parent_id], key=lambda x: -x[2])[:max_children]
        for child_id, rel_type, weight in neighbors:
            if child_id in visited:
                continue
            visited.add(child_id)
            child = entity_map.get(child_id, {"name": child_id, "type": ""})
            child_name = clean_mermaid(child.get("name", child_id))
            child_type = child.get("type", "")
            # mindmap 节点形状
            if child_type in ("concept", "model", "energy_source"):
                node_str = f"{indent}  (({child_name}))"
            elif child_type in ("organization", "institution"):
                node_str = f"{indent}  [{child_name}]"
            else:
                node_str = f"{indent}  {child_name}"
            lines.append(node_str)
            render_children(child_id, depth + 1, indent + "  ")

    render_children(center_id, 1, "  ")

    lines.append("```")
    return "\n".join(lines)


# ──────────────────────────────────────────────
# 统计报告
# ──────────────────────────────────────────────

def to_stats(graph: dict) -> str:
    entities = graph.get("entities", [])
    relations = graph.get("relations", [])
    meta = graph.get("metadata", {})
    domain = graph.get("domain", "general")
    updated = graph.get("updated_at", "unknown")

    # 实体类型分布
    type_count = defaultdict(int)
    for e in entities:
        type_count[e.get("type", "unknown")] += 1

    # 关系类型分布
    rel_type_count = defaultdict(int)
    for r in relations:
        rel_type_count[r.get("type", "unknown")] += 1

    # 平均 weight
    weights = [r.get("weight", 0.5) for r in relations if isinstance(r.get("weight"), (int, float))]
    avg_weight = sum(weights) / len(weights) if weights else 0

    # 度数最高的实体（出度 + 入度）
    degree = defaultdict(int)
    for r in relations:
        degree[r["source"]] += 1
        degree[r["target"]] += 1

    entity_map = {e["id"]: e.get("name", e["id"]) for e in entities}
    top_entities = sorted(degree.items(), key=lambda x: -x[1])[:10]

    lines = [
        f"# 📊 ontology-pro 图谱统计报告",
        f"",
        f"## 基本信息",
        f"- 领域：{domain}",
        f"- 最后更新：{updated}",
        f"- 分析会话：{meta.get('sessions_analyzed', 0)} 次",
        f"",
        f"## 规模",
        f"- 实体总数：{len(entities)}",
        f"- 关系总数：{len(relations)}",
        f"- 平均关系置信度：{avg_weight:.2f}",
        f"",
        f"## 实体类型分布",
    ]
    for etype, count in sorted(type_count.items(), key=lambda x: -x[1]):
        bar = "█" * min(count, 30)
        lines.append(f"  {etype:<20} {count:>4}  {bar}")

    lines += ["", "## 关系类型分布"]
    for rtype, count in sorted(rel_type_count.items(), key=lambda x: -x[1]):
        bar = "█" * min(count, 30)
        lines.append(f"  {rtype:<20} {count:>4}  {bar}")

    lines += ["", "## 核心节点（度数排名 Top 10）"]
    for eid, deg in top_entities:
        name = entity_map.get(eid, eid)
        lines.append(f"  [{eid}] {name:<30} 度数: {deg}")

    # 最近变更日志（最新5条）
    changelog = graph.get("changelog", [])[-5:]
    if changelog:
        lines += ["", "## 最近变更（最新5条）"]
        for entry in reversed(changelog):
            action = entry.get("action", "?")
            ts = entry.get("ts", "?")
            detail = entry.get("name") or f"{entry.get('source','?')}→{entry.get('target','?')}"
            lines.append(f"  {ts}  [{action}]  {detail}")

    return "\n".join(lines)


# ──────────────────────────────────────────────
# CLI 入口
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="ontology-pro graph visualizer — 知识图谱可视化工具",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--input", default=None, help="输入 JSON 图谱文件路径")
    parser.add_argument("--domain", default="general", help="从默认存储读取的领域名称")
    parser.add_argument("--base-dir", default=None, help="图谱存储目录（默认: ~/.ontology-pro/graphs/）")
    parser.add_argument("--format", default="flowchart",
                        choices=["flowchart", "mindmap", "stats"],
                        help="输出格式（默认: flowchart）")
    parser.add_argument("--output", default=None, help="输出文件路径（默认: 打印到 stdout）")
    parser.add_argument("--center", default=None, help="mindmap 中心实体名称")
    parser.add_argument("--max-nodes", type=int, default=40, help="最大节点数（默认: 40）")
    parser.add_argument("--max-edges", type=int, default=60, help="最大关系数（默认: 60）")
    parser.add_argument("--min-weight", type=float, default=0.0, help="最小置信度过滤（0.0-1.0）")
    parser.add_argument("--entity-types", default=None,
                        help="只显示指定实体类型，逗号分隔，如: concept,technology")
    parser.add_argument("--relation-types", default=None,
                        help="只显示指定关系类型，逗号分隔，如: causes,includes")

    args = parser.parse_args()

    # 加载图谱
    if args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"[graph_visualize] ❌ 文件不存在: {input_path}")
            sys.exit(1)
        with open(input_path, "r", encoding="utf-8") as f:
            graph = json.load(f)
    else:
        base_dir = Path(args.base_dir) if args.base_dir else DEFAULT_BASE_DIR
        graph_path = base_dir / f"{args.domain}.json"
        if not graph_path.exists():
            print(f"[graph_visualize] ❌ 图谱不存在: {graph_path}（请先执行 memory_manager.py init）")
            sys.exit(1)
        with open(graph_path, "r", encoding="utf-8") as f:
            graph = json.load(f)

    print(f"[graph_visualize] 📥 已加载图谱: {graph.get('domain', '?')} "
          f"({len(graph.get('entities', []))} 实体, {len(graph.get('relations', []))} 关系)")

    # 解析过滤参数
    filter_entity_types = [t.strip() for t in args.entity_types.split(",")] if args.entity_types else None
    filter_relation_types = [t.strip() for t in args.relation_types.split(",")] if args.relation_types else None

    # 生成输出
    if args.format == "flowchart":
        result = to_flowchart(
            graph,
            max_nodes=args.max_nodes,
            max_edges=args.max_edges,
            min_weight=args.min_weight,
            filter_entity_types=filter_entity_types,
            filter_relation_types=filter_relation_types,
        )
    elif args.format == "mindmap":
        result = to_mindmap(graph, center=args.center)
    elif args.format == "stats":
        result = to_stats(graph)
    else:
        result = to_flowchart(graph)

    # 输出
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"[graph_visualize] ✅ 已输出到: {output_path}")
    else:
        print("\n" + result)


if __name__ == "__main__":
    main()
