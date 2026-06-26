#!/usr/bin/env python3
"""
知识图谱 - 基于 SQLite 的实体关系网络管理
支持实体增删改查、关系追踪、路径查询、邻居查询
数据存储在 novel_memory.db 的 kg_nodes / kg_edges 表中
"""

import os
import json
import hashlib
import sqlite3
import argparse
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any


class KnowledgeGraph:
    """知识图谱 - SQLite 存储的实体关系网络"""

    def __init__(self, db_path: str):
        """
        初始化知识图谱

        Args:
            db_path: SQLite 数据库路径（与 MemoryEngine 共享 novel_memory.db）
        """
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self._ensure_tables()

    def _ensure_tables(self):
        """确保所需表存在（支持独立使用，无需依赖 MemoryEngine 先建表）"""
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS kg_nodes (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                tags TEXT DEFAULT '[]',
                properties TEXT DEFAULT '{}',
                created_at TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS kg_edges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                target TEXT NOT NULL,
                relation TEXT NOT NULL,
                properties TEXT DEFAULT '{}',
                created_at TEXT
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_kg_nodes_type ON kg_nodes(type)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_kg_nodes_name ON kg_nodes(name)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_kg_edges_source ON kg_edges(source)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_kg_edges_target ON kg_edges(target)")
        self.conn.commit()

    def add_node(self, name: str, node_type: str, tags: List[str] = None,
                 properties: Dict[str, Any] = None, node_id: str = None) -> str:
        """
        添加或更新节点

        Args:
            name: 实体名称
            node_type: 类型（character / location / item / faction / concept）
            tags: 标签列表
            properties: 属性字典
            node_id: 自定义ID（默认自动生成）

        Returns:
            节点ID
        """
        if not node_id:
            node_id = f"{node_type}_{hashlib.md5(name.encode()).hexdigest()[:8]}"

        tags_json = json.dumps(tags or [], ensure_ascii=False)
        props_json = json.dumps(properties or {}, ensure_ascii=False)
        now = datetime.now().isoformat()

        cur = self.conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO kg_nodes (id, type, name, tags, properties, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (node_id, node_type, name, tags_json, props_json, now))
        self.conn.commit()
        return node_id

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """获取节点"""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM kg_nodes WHERE id = ?", (node_id,))
        row = cur.fetchone()
        if not row:
            return None
        result = dict(row)
        result["tags"] = json.loads(result.get("tags", "[]"))
        result["properties"] = json.loads(result.get("properties", "{}"))
        return result

    def find_node_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """按名称查找节点"""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM kg_nodes WHERE name = ?", (name,))
        row = cur.fetchone()
        if not row:
            return None
        result = dict(row)
        result["tags"] = json.loads(result.get("tags", "[]"))
        result["properties"] = json.loads(result.get("properties", "{}"))
        return result

    def list_nodes(self, node_type: str = None, tag: str = None) -> List[Dict[str, Any]]:
        """列出节点（可按类型或标签过滤）"""
        cur = self.conn.cursor()
        if node_type:
            cur.execute("SELECT * FROM kg_nodes WHERE type = ? ORDER BY name", (node_type,))
        elif tag:
            cur.execute("SELECT * FROM kg_nodes WHERE tags LIKE ? ORDER BY name",
                       (f'%"{tag}"%',))
        else:
            cur.execute("SELECT * FROM kg_nodes ORDER BY type, name")
        results = []
        for row in cur.fetchall():
            r = dict(row)
            r["tags"] = json.loads(r.get("tags", "[]"))
            r["properties"] = json.loads(r.get("properties", "{}"))
            results.append(r)
        return results

    def update_node(self, node_id: str, name: str = None, node_type: str = None,
                    tags: List[str] = None, properties: Dict[str, Any] = None) -> bool:
        """更新节点属性"""
        node = self.get_node(node_id)
        if not node:
            return False
        cur = self.conn.cursor()
        if name is not None:
            cur.execute("UPDATE kg_nodes SET name = ? WHERE id = ?", (name, node_id))
        if node_type is not None:
            cur.execute("UPDATE kg_nodes SET type = ? WHERE id = ?", (node_type, node_id))
        if tags is not None:
            cur.execute("UPDATE kg_nodes SET tags = ? WHERE id = ?",
                       (json.dumps(tags, ensure_ascii=False), node_id))
        if properties is not None:
            cur.execute("UPDATE kg_nodes SET properties = ? WHERE id = ?",
                       (json.dumps(properties, ensure_ascii=False), node_id))
        self.conn.commit()
        return True

    def delete_node(self, node_id: str) -> bool:
        """删除节点及其所有关系"""
        cur = self.conn.cursor()
        cur.execute("DELETE FROM kg_edges WHERE source = ? OR target = ?", (node_id, node_id))
        cur.execute("DELETE FROM kg_nodes WHERE id = ?", (node_id,))
        self.conn.commit()
        return cur.rowcount > 0

    # ==================== 关系管理 ====================

    def add_edge(self, source: str, target: str, relation: str,
                 properties: Dict[str, Any] = None) -> int:
        """添加关系"""
        props_json = json.dumps(properties or {}, ensure_ascii=False)
        now = datetime.now().isoformat()
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO kg_edges (source, target, relation, properties, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (source, target, relation, props_json, now))
        self.conn.commit()
        return cur.lastrowid

    def delete_edge(self, edge_id: int) -> bool:
        """按ID删除关系"""
        cur = self.conn.cursor()
        cur.execute("DELETE FROM kg_edges WHERE id = ?", (edge_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def find_edge_by_names(self, source_name: str, target_name: str,
                           relation: str = None) -> List[Dict[str, Any]]:
        """按端点名称查找关系边"""
        source_node = self.find_node_by_name(source_name)
        target_node = self.find_node_by_name(target_name)
        if not source_node or not target_node:
            return []
        cur = self.conn.cursor()
        if relation:
            cur.execute("""
                SELECT * FROM kg_edges
                WHERE source = ? AND target = ? AND relation = ?
            """, (source_node["id"], target_node["id"], relation))
        else:
            cur.execute("""
                SELECT * FROM kg_edges
                WHERE source = ? AND target = ?
            """, (source_node["id"], target_node["id"]))
        results = []
        for row in cur.fetchall():
            r = dict(row)
            r["properties"] = json.loads(r.get("properties", "{}"))
            results.append(r)
        return results

    def get_edges(self, node_id: str, direction: str = "both",
                  relation: str = None) -> List[Dict[str, Any]]:
        """
        获取节点的所有关系

        Args:
            node_id: 节点ID
            direction: 方向（outgoing / incoming / both）
            relation: 关系类型过滤
        """
        cur = self.conn.cursor()
        conditions = []
        params = []

        if direction in ("outgoing", "both"):
            conditions.append("source = ?")
            params.append(node_id)
        if direction in ("incoming", "both"):
            conditions.append("target = ?")
            params.append(node_id)

        sql = f"SELECT * FROM kg_edges WHERE ({' OR '.join(conditions)})"
        if relation:
            sql += " AND relation = ?"
            params.append(relation)

        cur.execute(sql, params)
        results = []
        for row in cur.fetchall():
            r = dict(row)
            r["properties"] = json.loads(r.get("properties", "{}"))
            results.append(r)
        return results

    def get_neighbors(self, node_id: str, depth: int = 1,
                      relation: str = None) -> Dict[str, Any]:
        """获取邻居节点（BFS）"""
        visited = {node_id}
        current_level = [node_id]
        all_edges = []

        for d in range(depth):
            next_level = []
            for nid in current_level:
                edges = self.get_edges(nid, "both", relation)
                for edge in edges:
                    target_node = edge["target"] if edge["source"] == nid else edge["source"]
                    all_edges.append(edge)
                    if target_node not in visited:
                        visited.add(target_node)
                        next_level.append(target_node)
            current_level = next_level
            if not current_level:
                break

        # 获取所有涉及的节点
        nodes = {}
        for nid in visited:
            node = self.get_node(nid)
            if node:
                nodes[nid] = node

        return {"nodes": nodes, "edges": all_edges}

    def find_path(self, source_id: str, target_id: str,
                  max_depth: int = 5) -> List[Dict[str, Any]]:
        """查找两个节点之间的最短路径（BFS）"""
        from collections import deque

        queue = deque([(source_id, [])])
        visited = {source_id}

        while queue:
            current, path = queue.popleft()
            if current == target_id:
                return path

            if len(path) >= max_depth:
                continue

            edges = self.get_edges(current, "both")
            for edge in edges:
                neighbor = edge["target"] if edge["source"] == current else edge["source"]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [edge]))

        return []

    def get_graph_stats(self) -> Dict[str, Any]:
        """获取图谱统计"""
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM kg_nodes")
        node_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM kg_edges")
        edge_count = cur.fetchone()[0]
        cur.execute("SELECT type, COUNT(*) FROM kg_nodes GROUP BY type")
        type_counts = {row[0]: row[1] for row in cur.fetchall()}
        cur.execute("SELECT relation, COUNT(*) FROM kg_edges GROUP BY relation")
        rel_counts = {row[0]: row[1] for row in cur.fetchall()}
        return {
            "node_count": node_count,
            "edge_count": edge_count,
            "node_types": type_counts,
            "relation_types": rel_counts
        }

    def export_subgraph(self, node_ids: List[str]) -> Dict[str, Any]:
        """导出子图"""
        nodes = []
        for nid in node_ids:
            node = self.get_node(nid)
            if node:
                nodes.append(node)

        placeholders = ",".join("?" * len(node_ids))
        cur = self.conn.cursor()
        cur.execute(f"""
            SELECT * FROM kg_edges
            WHERE source IN ({placeholders}) AND target IN ({placeholders})
        """, node_ids + node_ids)
        edges = []
        for row in cur.fetchall():
            r = dict(row)
            r["properties"] = json.loads(r.get("properties", "{}"))
            edges.append(r)

        return {"nodes": nodes, "edges": edges}

    def execute_action(self, action: str, params: dict) -> dict:
        """统一调度入口"""
        if action == "add-node":
            name = params.get("name")
            node_type = params.get("type") or params.get("node_type")
            if not name or not node_type:
                raise ValueError("add-node需要name和type")
            tags = params.get("tags", "").split(",") if params.get("tags") else []
            props = json.loads(params["properties"]) if params.get("properties") else {}
            nid = self.add_node(name, node_type, tags, props, params.get("node_id"))
            return {"node_id": nid}

        elif action == "add-edge":
            source = params.get("source") or params.get("from_name") or params.get("from")
            target = params.get("target") or params.get("to_name") or params.get("to")
            relation = params.get("relation")
            if not source or not target or not relation:
                raise ValueError("add-edge需要source/target/relation")
            props = json.loads(params["properties"]) if params.get("properties") else {}
            # 自动将名称解析为节点ID
            src_node = self.find_node_by_name(source)
            if src_node:
                source = src_node["id"]
            tgt_node = self.find_node_by_name(target)
            if tgt_node:
                target = tgt_node["id"]
            eid = self.add_edge(source, target, relation, props)
            return {"edge_id": eid}

        elif action == "find-node":
            name = params.get("name")
            if not name:
                raise ValueError("find-node需要name")
            return self.find_node_by_name(name)

        elif action == "delete-edge":
            edge_id = params.get("edge_id")
            if edge_id:
                return {"deleted": self.delete_edge(int(edge_id))}
            # 支持通过source+target+relation删除：先查找再删除
            source = params.get("source") or params.get("source_name")
            target = params.get("target") or params.get("target_name")
            if source and target:
                relation = params.get("relation")
                edges = self.find_edge_by_names(source, target, relation)
                if not edges:
                    return {"deleted": 0, "message": f"未找到 {source}→{target} 的边"}
                deleted = 0
                for edge in edges:
                    try:
                        self.delete_edge(edge["id"])
                        deleted += 1
                    except Exception:
                        pass
                return {"deleted": deleted}
            raise ValueError("delete-edge需要edge_id或source+target")

        elif action == "find-edge-by-names":
            source = params.get("source") or params.get("source_name")
            target = params.get("target") or params.get("target_name")
            if not source or not target:
                raise ValueError("find-edge-by-names需要source和target(名称)")
            return {"edges": self.find_edge_by_names(source, target, params.get("relation"))}

        elif action == "get-neighbors":
            nid = params.get("node_id")
            name = params.get("name")
            if not nid and name:
                found = self.find_node_by_name(name)
                if found:
                    nid = found["id"]
            if not nid:
                raise ValueError("get-neighbors需要node_id或name")
            depth = int(params.get("depth", 1))
            return self.get_neighbors(nid, depth, params.get("relation"))

        elif action == "find-path":
            source = params.get("source") or params.get("from_name") or params.get("from")
            target = params.get("target") or params.get("to_name") or params.get("to")
            if not source or not target:
                raise ValueError("find-path需要source/target(或from_name/to_name)")
            return {"path": self.find_path(source, target)}

        elif action == "list-nodes":
            return {"nodes": self.list_nodes(params.get("type"), params.get("tag"))}

        elif action == "stats":
            return self.get_graph_stats()

        else:
            raise ValueError(f"未知操作: {action}")

    def close(self):
        """关闭连接"""
        self.conn.close()


def main():
    parser = argparse.ArgumentParser(description='知识图谱管理')
    parser.add_argument('--db-path', required=True, help='数据库路径')
    parser.add_argument('--action', required=True,
                       choices=['add-node', 'get-node', 'find-node', 'list-nodes',
                               'update-node', 'delete-node', 'add-edge', 'delete-edge',
                               'find-edge-by-names', 'get-edges',
                               'get-neighbors', 'find-path', 'stats', 'export-subgraph'],
                       help='操作类型')
    parser.add_argument('--node-id', help='节点ID')
    parser.add_argument('--name', help='节点名称')
    parser.add_argument('--type', help='节点类型')
    parser.add_argument('--tags', help='标签(逗号分隔)')
    parser.add_argument('--properties', help='属性JSON')
    parser.add_argument('--source', help='关系源节点ID')
    parser.add_argument('--target', help='关系目标节点ID')
    parser.add_argument('--relation', help='关系类型')
    parser.add_argument('--direction', choices=['outgoing', 'incoming', 'both'],
                       default='both', help='关系方向')
    parser.add_argument('--depth', type=int, default=1, help='邻居查询深度')
    parser.add_argument('--tag', help='标签过滤')
    parser.add_argument('--node-ids', help='子图导出节点ID(逗号分隔)')
    parser.add_argument('--output', choices=['text', 'json'], default='json')

    args = parser.parse_args()
    kg = KnowledgeGraph(args.db_path)
    try:
        skip_keys = {"db_path", "action", "output"}
        params = {k: v for k, v in vars(args).items()
                  if v is not None and k not in skip_keys and not k.startswith('_')}
        result = kg.execute_action(args.action, params)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    finally:
        kg.close()

if __name__ == '__main__':
    main()
