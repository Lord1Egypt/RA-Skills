#!/usr/bin/env python3
"""
project-nerve 任务关系图谱

建模跨平台任务之间的依赖关系，支持关系查询、依赖分析、
影响评估和 Mermaid 可视化。

灵感来源: ontology (117K 下载量, 326 星)
"""

import json
import os
import sys
from collections import deque
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

from utils import (
    check_subscription,
    generate_id,
    get_data_file,
    load_input_data,
    now_iso,
    output_error,
    output_success,
    parse_common_args,
    read_json_file,
    require_paid_feature,
    write_json_file,
)


# ============================================================
# 常量定义
# ============================================================

GRAPH_FILE = "task_graph.json"

# 支持的关系类型
RELATION_TYPES = [
    "blocks",       # A 阻塞 B（A 完成后 B 才能开始）
    "blocked_by",   # A 被 B 阻塞（B 完成后 A 才能开始）
    "related_to",   # A 与 B 相关（无方向性依赖）
    "parent_of",    # A 是 B 的父任务
    "child_of",     # A 是 B 的子任务
    "duplicates",   # A 是 B 的重复
]

# 互为反向的关系映射
_INVERSE_RELATIONS = {
    "blocks": "blocked_by",
    "blocked_by": "blocks",
    "parent_of": "child_of",
    "child_of": "parent_of",
    "related_to": "related_to",
    "duplicates": "duplicates",
}


# ============================================================
# 数据读写
# ============================================================

def _get_graph() -> Dict[str, Any]:
    """读取任务关系图谱数据。

    Returns:
        包含 nodes 和 edges 列表的字典。
    """
    data = read_json_file(get_data_file(GRAPH_FILE))
    if isinstance(data, dict) and "nodes" in data and "edges" in data:
        return data
    return {
        "nodes": [],
        "edges": [],
        "metadata": {"created_at": now_iso(), "version": "1.0"},
    }


def _save_graph(graph: Dict[str, Any]) -> None:
    """保存图谱数据到文件。

    Args:
        graph: 图谱数据字典。
    """
    graph["metadata"] = graph.get("metadata", {})
    graph["metadata"]["updated_at"] = now_iso()
    write_json_file(get_data_file(GRAPH_FILE), graph)


# ============================================================
# 节点管理
# ============================================================

def _find_node(nodes: List[Dict], node_id: str) -> Optional[Dict]:
    """查找节点。

    Args:
        nodes: 节点列表。
        node_id: 节点 ID。

    Returns:
        匹配的节点字典，未找到返回 None。
    """
    for n in nodes:
        if n.get("id") == node_id:
            return n
    return None


def _ensure_node(graph: Dict[str, Any], node_id: str, source: str = "", title: str = "") -> Dict:
    """确保节点存在，若不存在则创建。

    Args:
        graph: 图谱数据。
        node_id: 节点 ID。
        source: 任务来源平台。
        title: 任务标题。

    Returns:
        节点字典。
    """
    node = _find_node(graph["nodes"], node_id)
    if node is None:
        node = {
            "id": node_id,
            "source": source,
            "title": title,
            "added_at": now_iso(),
        }
        graph["nodes"].append(node)
    else:
        # 更新信息（如果提供了新的值）
        if source and not node.get("source"):
            node["source"] = source
        if title and not node.get("title"):
            node["title"] = title
    return node


def _find_edge(edges: List[Dict], from_id: str, to_id: str, rel_type: str) -> Optional[int]:
    """查找边的索引。

    Args:
        edges: 边列表。
        from_id: 起始节点 ID。
        to_id: 目标节点 ID。
        rel_type: 关系类型。

    Returns:
        匹配的边在列表中的索引，未找到返回 None。
    """
    for i, e in enumerate(edges):
        if e.get("from") == from_id and e.get("to") == to_id and e.get("type") == rel_type:
            return i
    return None


# ============================================================
# 操作实现：添加关系
# ============================================================

def add_relation(data: Dict[str, Any]) -> None:
    """添加任务关系。

    在两个任务节点之间建立关系边。
    支持跨平台关系（如 GitHub Issue 阻塞 Trello 卡片）。

    必填字段: from_id（起始任务 ID）, to_id（目标任务 ID）, type（关系类型）
    可选字段: from_source, from_title, to_source, to_title

    关系类型: blocks, blocked_by, related_to, parent_of, child_of, duplicates

    Args:
        data: 关系数据字典。
    """
    from_id = data.get("from_id", "").strip()
    to_id = data.get("to_id", "").strip()
    rel_type = data.get("type", "").strip().lower()

    if not from_id or not to_id:
        output_error("起始任务 ID（from_id）和目标任务 ID（to_id）为必填字段", code="VALIDATION_ERROR")
        return

    if not rel_type:
        output_error("关系类型（type）为必填字段", code="VALIDATION_ERROR")
        return

    if rel_type not in RELATION_TYPES:
        valid = "、".join(RELATION_TYPES)
        output_error(f"不支持的关系类型: {rel_type}，支持的类型: {valid}", code="INVALID_TYPE")
        return

    if from_id == to_id:
        output_error("不能创建自引用关系（from_id 和 to_id 不能相同）", code="VALIDATION_ERROR")
        return

    graph = _get_graph()

    # 确保节点存在
    _ensure_node(graph, from_id, data.get("from_source", ""), data.get("from_title", ""))
    _ensure_node(graph, to_id, data.get("to_source", ""), data.get("to_title", ""))

    # 检查是否已存在
    existing = _find_edge(graph["edges"], from_id, to_id, rel_type)
    if existing is not None:
        output_error(
            f"关系已存在: {from_id} --[{rel_type}]--> {to_id}",
            code="DUPLICATE_RELATION",
        )
        return

    # 创建边
    edge = {
        "from": from_id,
        "to": to_id,
        "type": rel_type,
        "created_at": now_iso(),
    }
    graph["edges"].append(edge)

    _save_graph(graph)

    output_success({
        "message": f"已添加关系: {from_id} --[{rel_type}]--> {to_id}",
        "edge": edge,
        "total_nodes": len(graph["nodes"]),
        "total_edges": len(graph["edges"]),
    })


# ============================================================
# 操作实现：删除关系
# ============================================================

def remove_relation(data: Dict[str, Any]) -> None:
    """删除任务关系。

    必填字段: from_id, to_id, type

    Args:
        data: 关系标识字典。
    """
    from_id = data.get("from_id", "").strip()
    to_id = data.get("to_id", "").strip()
    rel_type = data.get("type", "").strip().lower()

    if not from_id or not to_id or not rel_type:
        output_error("from_id、to_id 和 type 为必填字段", code="VALIDATION_ERROR")
        return

    graph = _get_graph()
    idx = _find_edge(graph["edges"], from_id, to_id, rel_type)

    if idx is None:
        output_error(
            f"未找到关系: {from_id} --[{rel_type}]--> {to_id}",
            code="NOT_FOUND",
        )
        return

    removed = graph["edges"].pop(idx)
    _save_graph(graph)

    output_success({
        "message": f"已删除关系: {from_id} --[{rel_type}]--> {to_id}",
        "removed_edge": removed,
        "remaining_edges": len(graph["edges"]),
    })


# ============================================================
# 操作实现：查询
# ============================================================

def _build_adjacency(edges: List[Dict]) -> Dict[str, List[Dict]]:
    """构建邻接表（双向）。

    Args:
        edges: 边列表。

    Returns:
        邻接表字典，键为节点 ID，值为相关边的列表。
    """
    adj: Dict[str, List[Dict]] = {}
    for e in edges:
        from_id = e.get("from", "")
        to_id = e.get("to", "")
        if from_id:
            if from_id not in adj:
                adj[from_id] = []
            adj[from_id].append(e)
        if to_id:
            if to_id not in adj:
                adj[to_id] = []
            adj[to_id].append(e)
    return adj


def query(data: Dict[str, Any]) -> None:
    """查询与指定任务相关的所有任务（BFS 遍历）。

    从给定任务出发，通过 BFS 遍历找出所有直接和间接相关的任务。

    必填字段: task_id（要查询的任务 ID）
    可选字段: max_depth（最大遍历深度，默认 3）, type（过滤关系类型）

    Args:
        data: 查询参数字典。
    """
    task_id = data.get("task_id", "").strip()
    if not task_id:
        output_error("任务 ID（task_id）为必填字段", code="VALIDATION_ERROR")
        return

    max_depth = int(data.get("max_depth", 3))
    type_filter = data.get("type", "").strip().lower()

    graph = _get_graph()
    edges = graph["edges"]
    nodes = graph["nodes"]

    # 如果指定了关系类型过滤
    if type_filter:
        edges = [e for e in edges if e.get("type") == type_filter]

    adj = _build_adjacency(edges)

    # BFS 遍历
    visited: Set[str] = set()
    queue: deque = deque()
    queue.append((task_id, 0))
    visited.add(task_id)

    related_tasks: List[Dict[str, Any]] = []
    related_edges: List[Dict[str, Any]] = []

    while queue:
        current_id, depth = queue.popleft()

        if depth >= max_depth:
            continue

        for edge in adj.get(current_id, []):
            # 确定另一端的节点
            other_id = edge["to"] if edge["from"] == current_id else edge["from"]

            related_edges.append({
                "from": edge.get("from", ""),
                "to": edge.get("to", ""),
                "type": edge.get("type", ""),
                "depth": depth + 1,
            })

            if other_id not in visited:
                visited.add(other_id)
                node = _find_node(nodes, other_id)
                related_tasks.append({
                    "id": other_id,
                    "source": node.get("source", "") if node else "",
                    "title": node.get("title", "") if node else "",
                    "depth": depth + 1,
                })
                queue.append((other_id, depth + 1))

    # 去重边
    seen_edges: Set[str] = set()
    unique_edges = []
    for e in related_edges:
        key = f"{e['from']}|{e['to']}|{e['type']}"
        if key not in seen_edges:
            seen_edges.add(key)
            unique_edges.append(e)

    output_success({
        "task_id": task_id,
        "related_tasks": related_tasks,
        "related_edges": unique_edges,
        "total_related": len(related_tasks),
        "max_depth": max_depth,
    })


# ============================================================
# 操作实现：依赖分析
# ============================================================

def _detect_cycles(edges: List[Dict], relation_types: Optional[List[str]] = None) -> List[List[str]]:
    """检测有向图中的环。

    使用 DFS 检测循环依赖。

    Args:
        edges: 边列表。
        relation_types: 要检查的关系类型，默认检查 blocks 和 parent_of。

    Returns:
        环路列表，每个环路是节点 ID 的列表。
    """
    if relation_types is None:
        relation_types = ["blocks", "parent_of"]

    # 构建有向邻接表
    directed_adj: Dict[str, List[str]] = {}
    for e in edges:
        if e.get("type") in relation_types:
            from_id = e.get("from", "")
            to_id = e.get("to", "")
            if from_id not in directed_adj:
                directed_adj[from_id] = []
            directed_adj[from_id].append(to_id)

    cycles: List[List[str]] = []
    visited: Set[str] = set()
    rec_stack: Set[str] = set()
    path: List[str] = []

    def _dfs(node: str) -> None:
        """深度优先搜索检测环。"""
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in directed_adj.get(node, []):
            if neighbor not in visited:
                _dfs(neighbor)
            elif neighbor in rec_stack:
                # 找到环
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                cycles.append(cycle)

        path.pop()
        rec_stack.discard(node)

    all_nodes = set()
    for e in edges:
        if e.get("type") in relation_types:
            all_nodes.add(e.get("from", ""))
            all_nodes.add(e.get("to", ""))

    for node in all_nodes:
        if node and node not in visited:
            _dfs(node)

    return cycles


def dependencies(data: Dict[str, Any]) -> None:
    """构建依赖树并检测循环依赖。

    分析任务之间的 blocks/blocked_by 关系，构建依赖树，
    并检测是否存在循环依赖。

    必填字段: task_id
    可选字段: direction（up 向上追溯依赖 / down 向下展开被阻塞任务，默认 both）

    Args:
        data: 查询参数字典。
    """
    task_id = data.get("task_id", "").strip()
    if not task_id:
        output_error("任务 ID（task_id）为必填字段", code="VALIDATION_ERROR")
        return

    direction = data.get("direction", "both").strip().lower()

    graph = _get_graph()
    edges = graph["edges"]
    nodes = graph["nodes"]

    # 只看 blocks 类型的关系
    block_edges = [e for e in edges if e.get("type") in ("blocks", "blocked_by")]

    # 构建有向图（统一为 blocks 方向）
    blocks_adj: Dict[str, List[str]] = {}  # 阻塞者 -> 被阻塞者列表
    blocked_by_adj: Dict[str, List[str]] = {}  # 被阻塞者 -> 阻塞者列表

    for e in block_edges:
        if e.get("type") == "blocks":
            blocker = e["from"]
            blocked = e["to"]
        else:  # blocked_by
            blocker = e["to"]
            blocked = e["from"]

        if blocker not in blocks_adj:
            blocks_adj[blocker] = []
        blocks_adj[blocker].append(blocked)

        if blocked not in blocked_by_adj:
            blocked_by_adj[blocked] = []
        blocked_by_adj[blocked].append(blocker)

    # 向上追溯：这个任务被哪些任务阻塞
    upstream: List[Dict[str, Any]] = []
    if direction in ("up", "both"):
        visited: Set[str] = set()
        queue: deque = deque()
        queue.append((task_id, 0))
        visited.add(task_id)

        while queue:
            current, depth = queue.popleft()
            for blocker_id in blocked_by_adj.get(current, []):
                if blocker_id not in visited:
                    visited.add(blocker_id)
                    node = _find_node(nodes, blocker_id)
                    upstream.append({
                        "id": blocker_id,
                        "source": node.get("source", "") if node else "",
                        "title": node.get("title", "") if node else "",
                        "depth": depth + 1,
                    })
                    queue.append((blocker_id, depth + 1))

    # 向下展开：这个任务阻塞了哪些任务
    downstream: List[Dict[str, Any]] = []
    if direction in ("down", "both"):
        visited_down: Set[str] = set()
        queue_down: deque = deque()
        queue_down.append((task_id, 0))
        visited_down.add(task_id)

        while queue_down:
            current, depth = queue_down.popleft()
            for blocked_id in blocks_adj.get(current, []):
                if blocked_id not in visited_down:
                    visited_down.add(blocked_id)
                    node = _find_node(nodes, blocked_id)
                    downstream.append({
                        "id": blocked_id,
                        "source": node.get("source", "") if node else "",
                        "title": node.get("title", "") if node else "",
                        "depth": depth + 1,
                    })
                    queue_down.append((blocked_id, depth + 1))

    # 检测循环依赖
    cycles = _detect_cycles(edges)
    task_in_cycle = any(task_id in cycle for cycle in cycles)

    output_success({
        "task_id": task_id,
        "upstream_dependencies": upstream,
        "downstream_blocked": downstream,
        "total_upstream": len(upstream),
        "total_downstream": len(downstream),
        "has_circular_dependency": task_in_cycle,
        "circular_dependencies": [c for c in cycles if task_id in c],
    })


# ============================================================
# 操作实现：影响分析
# ============================================================

def impact(data: Dict[str, Any]) -> None:
    """分析阻塞一个任务会影响多少下游任务。

    计算如果指定任务被阻塞，有多少任务会受到影响（直接和间接）。

    必填字段: task_id

    Args:
        data: 查询参数字典。
    """
    task_id = data.get("task_id", "").strip()
    if not task_id:
        output_error("任务 ID（task_id）为必填字段", code="VALIDATION_ERROR")
        return

    graph = _get_graph()
    edges = graph["edges"]
    nodes = graph["nodes"]

    # 构建 blocks 方向的有向图
    blocks_adj: Dict[str, List[str]] = {}
    for e in edges:
        if e.get("type") == "blocks":
            from_id = e["from"]
            to_id = e["to"]
            if from_id not in blocks_adj:
                blocks_adj[from_id] = []
            blocks_adj[from_id].append(to_id)
        elif e.get("type") == "blocked_by":
            from_id = e["to"]  # 反转方向
            to_id = e["from"]
            if from_id not in blocks_adj:
                blocks_adj[from_id] = []
            blocks_adj[from_id].append(to_id)

    # BFS 计算所有受影响的下游任务
    affected: List[Dict[str, Any]] = []
    visited: Set[str] = {task_id}
    queue: deque = deque()

    # 从直接被阻塞的任务开始
    for blocked_id in blocks_adj.get(task_id, []):
        if blocked_id not in visited:
            visited.add(blocked_id)
            queue.append((blocked_id, 1))

    while queue:
        current, depth = queue.popleft()
        node = _find_node(nodes, current)
        affected.append({
            "id": current,
            "source": node.get("source", "") if node else "",
            "title": node.get("title", "") if node else "",
            "impact_depth": depth,
            "impact_type": "直接" if depth == 1 else "间接",
        })

        for next_id in blocks_adj.get(current, []):
            if next_id not in visited:
                visited.add(next_id)
                queue.append((next_id, depth + 1))

    # 按影响深度分组统计
    depth_stats: Dict[int, int] = {}
    for a in affected:
        d = a["impact_depth"]
        depth_stats[d] = depth_stats.get(d, 0) + 1

    # 影响等级评估
    impact_level = "无"
    total_affected = len(affected)
    if total_affected >= 5:
        impact_level = "严重"
    elif total_affected >= 3:
        impact_level = "较大"
    elif total_affected >= 1:
        impact_level = "一般"

    output_success({
        "task_id": task_id,
        "total_affected": total_affected,
        "impact_level": impact_level,
        "affected_tasks": affected,
        "depth_distribution": depth_stats,
        "summary": (
            f"如果 {task_id} 被阻塞，将影响 {total_affected} 个下游任务"
            if total_affected > 0
            else f"{task_id} 没有下游阻塞任务"
        ),
    })


# ============================================================
# 操作实现：可视化（付费功能）
# ============================================================

def visualize(data: Optional[Dict[str, Any]] = None) -> None:
    """生成任务关系的 Mermaid 流程图（付费功能）。

    将图谱中的任务关系可视化为 Mermaid flowchart 格式。

    可选字段: task_id（聚焦某个任务的子图）, type（过滤关系类型）

    Args:
        data: 可选的过滤参数。
    """
    if not require_paid_feature("mermaid_chart", "任务关系图谱可视化"):
        return

    graph = _get_graph()
    edges = graph["edges"]
    nodes = graph["nodes"]

    if not edges:
        output_success({
            "message": "图谱中暂无关系数据",
            "mermaid": "",
        })
        return

    task_filter = ""
    type_filter = ""
    if data:
        task_filter = data.get("task_id", "").strip()
        type_filter = data.get("type", "").strip().lower()

    # 过滤
    filtered_edges = edges
    if type_filter:
        filtered_edges = [e for e in filtered_edges if e.get("type") == type_filter]

    if task_filter:
        # 只保留与指定任务相关的边
        filtered_edges = [
            e for e in filtered_edges
            if e.get("from") == task_filter or e.get("to") == task_filter
        ]

    if not filtered_edges:
        output_success({
            "message": "过滤后无匹配的关系数据",
            "mermaid": "",
        })
        return

    # 生成 Mermaid 代码
    lines = ["```mermaid", "flowchart TD"]

    # 收集涉及的节点
    involved_nodes: Set[str] = set()
    for e in filtered_edges:
        involved_nodes.add(e.get("from", ""))
        involved_nodes.add(e.get("to", ""))

    # 节点定义（使用方括号表示节点，显示标题）
    node_map: Dict[str, str] = {}
    for node_id in involved_nodes:
        if not node_id:
            continue
        node = _find_node(nodes, node_id)
        # 生成安全的 Mermaid 节点 ID（替换特殊字符）
        safe_id = node_id.replace("-", "_").replace(".", "_").replace(" ", "_")
        title = node.get("title", node_id) if node else node_id
        source = node.get("source", "") if node else ""
        label = title
        if source:
            label = f"{title}\\n[{source}]"
        # 截断过长的标签
        if len(label) > 50:
            label = label[:47] + "..."
        lines.append(f"    {safe_id}[\"{label}\"]")
        node_map[node_id] = safe_id

    # 关系类型到箭头样式的映射
    arrow_styles = {
        "blocks": "-->|阻塞|",
        "blocked_by": "-->|被阻塞|",
        "related_to": "---|相关|",
        "parent_of": "-->|父任务|",
        "child_of": "-->|子任务|",
        "duplicates": "-.->|重复|",
    }

    # 边定义
    for e in filtered_edges:
        from_safe = node_map.get(e.get("from", ""), "")
        to_safe = node_map.get(e.get("to", ""), "")
        rel = e.get("type", "related_to")
        arrow = arrow_styles.get(rel, "-->")

        if from_safe and to_safe:
            lines.append(f"    {from_safe} {arrow} {to_safe}")

    lines.append("```")
    mermaid_code = "\n".join(lines)

    output_success({
        "message": f"已生成包含 {len(involved_nodes)} 个节点和 {len(filtered_edges)} 条关系的图谱",
        "mermaid": mermaid_code,
        "node_count": len(involved_nodes),
        "edge_count": len(filtered_edges),
    })


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("project-nerve 任务关系图谱")
    args = parser.parse_args()

    action = args.action.lower().replace("-", "_")

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "add_relation": lambda: add_relation(data or {}),
        "remove_relation": lambda: remove_relation(data or {}),
        "query": lambda: query(data or {}),
        "dependencies": lambda: dependencies(data or {}),
        "impact": lambda: impact(data or {}),
        "visualize": lambda: visualize(data),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join([
            "add-relation", "remove-relation", "query",
            "dependencies", "impact", "visualize",
        ])
        output_error(
            f"未知操作: {args.action}，支持的操作: {valid_actions}",
            code="INVALID_ACTION",
        )


if __name__ == "__main__":
    main()
