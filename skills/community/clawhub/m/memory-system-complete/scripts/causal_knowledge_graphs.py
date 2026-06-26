#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
因果关系图谱和知识点关系图谱实现
Causal Graph and Knowledge Graph Implementation
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import networkx as nx

class CausalGraph:
    """因果关系图谱"""

    def __init__(self, db_path: str):
        self.db_path = db_path

    def add_causal_relation(self, cause_id: int, effect_id: int, causal_type: str,
                          strength: float = 0.5, confidence: float = 0.5,
                          evidence: str = "", conditions: Dict = None,
                          time_delay: int = 0) -> int:
        """添加因果关系"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        conditions_json = json.dumps(conditions) if conditions else None

        cursor.execute("""
            INSERT INTO causal_relations
            (cause_memory_id, effect_memory_id, causal_type, strength, confidence, evidence, conditions, time_delay, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (cause_id, effect_id, causal_type, strength, confidence, evidence, conditions_json, time_delay, datetime.now(), datetime.now()))

        relation_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return relation_id

    def get_causes(self, effect_id: int, causal_type: str = None, min_strength: float = 0.0) -> List[Dict]:
        """获取某个记忆的所有原因"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if causal_type:
            cursor.execute("""
                SELECT cr.*, m1.title as cause_title, m2.title as effect_title
                FROM causal_relations cr
                JOIN memories m1 ON cr.cause_memory_id = m1.id
                JOIN memories m2 ON cr.effect_memory_id = m2.id
                WHERE cr.effect_memory_id = ? AND cr.causal_type = ? AND cr.strength >= ?
                ORDER BY cr.strength DESC
            """, (effect_id, causal_type, min_strength))
        else:
            cursor.execute("""
                SELECT cr.*, m1.title as cause_title, m2.title as effect_title
                FROM causal_relations cr
                JOIN memories m1 ON cr.cause_memory_id = m1.id
                JOIN memories m2 ON cr.effect_memory_id = m2.id
                WHERE cr.effect_memory_id = ? AND cr.strength >= ?
                ORDER BY cr.strength DESC
            """, (effect_id, min_strength))

        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'cause_id': row[1],
                'effect_id': row[2],
                'causal_type': row[3],
                'strength': row[4],
                'confidence': row[5],
                'evidence': row[6],
                'conditions': json.loads(row[7]) if row[7] else None,
                'time_delay': row[8],
                'cause_title': row[9],
                'effect_title': row[10]
            })

        conn.close()
        return results

    def get_effects(self, cause_id: int, causal_type: str = None, min_strength: float = 0.0) -> List[Dict]:
        """获取某个记忆的所有结果"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if causal_type:
            cursor.execute("""
                SELECT cr.*, m1.title as cause_title, m2.title as effect_title
                FROM causal_relations cr
                JOIN memories m1 ON cr.cause_memory_id = m1.id
                JOIN memories m2 ON cr.effect_memory_id = m2.id
                WHERE cr.cause_memory_id = ? AND cr.causal_type = ? AND cr.strength >= ?
                ORDER BY cr.strength DESC
            """, (cause_id, causal_type, min_strength))
        else:
            cursor.execute("""
                SELECT cr.*, m1.title as cause_title, m2.title as effect_title
                FROM causal_relations cr
                JOIN memories m1 ON cr.cause_memory_id = m1.id
                JOIN memories m2 ON cr.effect_memory_id = m2.id
                WHERE cr.cause_memory_id = ? AND cr.strength >= ?
                ORDER BY cr.strength DESC
            """, (cause_id, min_strength))

        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'cause_id': row[1],
                'effect_id': row[2],
                'causal_type': row[3],
                'strength': row[4],
                'confidence': row[5],
                'evidence': row[6],
                'conditions': json.loads(row[7]) if row[7] else None,
                'time_delay': row[8],
                'cause_title': row[9],
                'effect_title': row[10]
            })

        conn.close()
        return results

    def get_causal_chain(self, start_id: int, max_depth: int = 5) -> List[List[int]]:
        """获取因果链"""
        chain = [[start_id]]
        current_level = [start_id]

        for depth in range(max_depth):
            next_level = []
            for memory_id in current_level:
                effects = self.get_effects(memory_id)
                for effect in effects:
                    if effect['effect_id'] not in next_level:
                        next_level.append(effect['effect_id'])

            if not next_level:
                break

            chain.append(next_level)
            current_level = next_level

        return chain

    def detect_causal_cycles(self) -> List[List[int]]:
        """检测因果循环"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT cause_memory_id, effect_memory_id
            FROM causal_relations
        """)

        edges = []
        for row in cursor.fetchall():
            edges.append((row[0], row[1]))

        conn.close()

        G = nx.DiGraph()
        G.add_edges_from(edges)

        cycles = list(nx.simple_cycles(G))
        return cycles

    def compute_causal_strength(self, cause_id: int, effect_id: int) -> float:
        """计算因果强度"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT strength, confidence
            FROM causal_relations
            WHERE cause_memory_id = ? AND effect_memory_id = ?
        """, (cause_id, effect_id))

        row = cursor.fetchone()
        conn.close()

        if row:
            strength, confidence = row
            return strength * confidence
        return 0.0

    def update_causal_strength(self, cause_id: int, effect_id: int, new_strength: float) -> bool:
        """更新因果强度"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE causal_relations
            SET strength = ?, updated_at = ?
            WHERE cause_memory_id = ? AND effect_memory_id = ?
        """, (new_strength, datetime.now(), cause_id, effect_id))

        affected = cursor.rowcount
        conn.commit()
        conn.close()

        return affected > 0

    def remove_causal_relation(self, cause_id: int, effect_id: int) -> bool:
        """删除因果关系"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM causal_relations
            WHERE cause_memory_id = ? AND effect_memory_id = ?
        """, (cause_id, effect_id))

        affected = cursor.rowcount
        conn.commit()
        conn.close()

        return affected > 0


class KnowledgeGraph:
    """知识点关系图谱"""

    def __init__(self, db_path: str):
        self.db_path = db_path

    def add_relation(self, source_id: int, target_id: int, relation_type: str,
                   strength: float = 0.5, direction: str = 'bidirectional',
                   attributes: Dict = None) -> int:
        """添加知识点关系"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        attributes_json = json.dumps(attributes) if attributes else None

        cursor.execute("""
            INSERT INTO knowledge_relations
            (source_memory_id, target_memory_id, relation_type, relation_strength, relation_direction, attributes, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (source_id, target_id, relation_type, strength, direction, attributes_json, datetime.now(), datetime.now()))

        relation_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return relation_id

    def get_relations(self, memory_id: int, relation_type: str = None, min_strength: float = 0.0) -> List[Dict]:
        """获取某个记忆的所有关系"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if relation_type:
            cursor.execute("""
                SELECT kr.*, m1.title as source_title, m2.title as target_title
                FROM knowledge_relations kr
                JOIN memories m1 ON kr.source_memory_id = m1.id
                JOIN memories m2 ON kr.target_memory_id = m2.id
                WHERE (kr.source_memory_id = ? OR kr.target_memory_id = ?)
                  AND kr.relation_type = ? AND kr.relation_strength >= ?
                ORDER BY kr.relation_strength DESC
            """, (memory_id, memory_id, relation_type, min_strength))
        else:
            cursor.execute("""
                SELECT kr.*, m1.title as source_title, m2.title as target_title
                FROM knowledge_relations kr
                JOIN memories m1 ON kr.source_memory_id = m1.id
                JOIN memories m2 ON kr.target_memory_id = m2.id
                WHERE (kr.source_memory_id = ? OR kr.target_memory_id = ?)
                  AND kr.relation_strength >= ?
                ORDER BY kr.relation_strength DESC
            """, (memory_id, memory_id, min_strength))

        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'source_id': row[1],
                'target_id': row[2],
                'relation_type': row[3],
                'strength': row[4],
                'direction': row[5],
                'attributes': json.loads(row[6]) if row[6] else None,
                'source_title': row[7],
                'target_title': row[8]
            })

        conn.close()
        return results

    def get_related_memories(self, memory_id: int, relation_type: str, max_depth: int = 2) -> List[int]:
        """获取相关记忆（多跳）"""
        related = set([memory_id])
        current_level = [memory_id]

        for depth in range(max_depth):
            next_level = []
            for mid in current_level:
                relations = self.get_relations(mid, relation_type)
                for rel in relations:
                    if rel['source_id'] == mid and rel['target_id'] not in related:
                        next_level.append(rel['target_id'])
                        related.add(rel['target_id'])
                    elif rel['target_id'] == mid and rel['source_id'] not in related:
                        next_level.append(rel['source_id'])
                        related.add(rel['source_id'])

            if not next_level:
                break

            current_level = next_level

        return list(related)

    def find_shortest_path(self, source_id: int, target_id: int) -> Optional[List[int]]:
        """查找最短路径"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT source_memory_id, target_memory_id
            FROM knowledge_relations
        """)

        edges = []
        for row in cursor.fetchall():
            edges.append((row[0], row[1]))

        conn.close()

        G = nx.Graph()
        G.add_edges_from(edges)

        try:
            path = nx.shortest_path(G, source_id, target_id)
            return path
        except nx.NetworkXNoPath:
            return None

    def compute_relation_strength(self, source_id: int, target_id: int, relation_type: str) -> float:
        """计算关系强度"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT relation_strength
            FROM knowledge_relations
            WHERE source_memory_id = ? AND target_memory_id = ? AND relation_type = ?
        """, (source_id, target_id, relation_type))

        row = cursor.fetchone()
        conn.close()

        if row:
            return row[0]
        return 0.0

    def update_relation_strength(self, source_id: int, target_id: int, relation_type: str, new_strength: float) -> bool:
        """更新关系强度"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE knowledge_relations
            SET relation_strength = ?, updated_at = ?
            WHERE source_memory_id = ? AND target_memory_id = ? AND relation_type = ?
        """, (new_strength, datetime.now(), source_id, target_id, relation_type))

        affected = cursor.rowcount
        conn.commit()
        conn.close()

        return affected > 0

    def remove_relation(self, source_id: int, target_id: int, relation_type: str) -> bool:
        """删除关系"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM knowledge_relations
            WHERE source_memory_id = ? AND target_memory_id = ? AND relation_type = ?
        """, (source_id, target_id, relation_type))

        affected = cursor.rowcount
        conn.commit()
        conn.close()

        return affected > 0

    def get_subgraph(self, center_id: int, radius: int = 2) -> nx.Graph:
        """获取子图"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT source_memory_id, target_memory_id, relation_type, relation_strength
            FROM knowledge_relations
        """)

        edges = []
        for row in cursor.fetchall():
            edges.append((row[0], row[1], {'type': row[2], 'strength': row[3]}))

        conn.close()

        G = nx.Graph()
        G.add_edges_from(edges)

        subgraph = nx.ego_graph(G, center_id, radius=radius)
        return subgraph

    def detect_communities(self) -> Dict[int, List[int]]:
        """检测社区"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT source_memory_id, target_memory_id
            FROM knowledge_relations
        """)

        edges = []
        for row in cursor.fetchall():
            edges.append((row[0], row[1]))

        conn.close()

        G = nx.Graph()
        G.add_edges_from(edges)

        communities = nx.community.greedy_modularity_communities(G)

        community_dict = {}
        for i, community in enumerate(communities):
            community_dict[i] = list(community)

        return community_dict


if __name__ == "__main__":
    # 测试代码
    db_path = "C:\\Users\\Administrator\\.openclaw\\workspace\\memory\\database\\xiaozhi_memory.db"

    causal_graph = CausalGraph(db_path)
    knowledge_graph = KnowledgeGraph(db_path)

    print("Causal Graph and Knowledge Graph initialized successfully!")
