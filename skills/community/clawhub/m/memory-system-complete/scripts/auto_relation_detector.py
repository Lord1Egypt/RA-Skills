#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动检测因果关系和知识点关系
Automatic Detection of Causal Relations and Knowledge Relations
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import re

class RelationDetector:
    """关系检测器"""

    def __init__(self, db_path: str):
        self.db_path = db_path

    def detect_causal_relations(self, memory_id: int) -> List[Dict]:
        """检测因果关系"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 获取记忆内容
        cursor.execute("""
            SELECT id, title, content, type
            FROM memories
            WHERE id = ?
        """, (memory_id,))

        row = cursor.fetchone()
        if not row:
            conn.close()
            return []

        memory_id, title, content, memory_type = row

        # 获取所有其他记忆
        cursor.execute("""
            SELECT id, title, content, type
            FROM memories
            WHERE id != ?
            ORDER BY created_at DESC
            LIMIT 50
        """, (memory_id,))

        other_memories = cursor.fetchall()
        conn.close()

        causal_relations = []

        # 简单的关键词匹配检测
        causal_keywords = {
            'direct': ['导致', '引起', '造成', '产生', '触发', '引发', 'cause', 'cause', 'result in', 'lead to'],
            'indirect': ['间接导致', '间接引起', '间接造成', 'indirectly cause', 'indirectly lead to'],
            'conditional': ['如果...那么', '当...时', '在...条件下', 'if...then', 'when...then', 'under condition'],
            'probabilistic': ['可能', '也许', '大概', 'likely', 'probably', 'possibly']
        }

        for other_id, other_title, other_content, other_type in other_memories:
            # 检查当前记忆是否导致其他记忆
            for causal_type, keywords in causal_keywords.items():
                for keyword in keywords:
                    if keyword in content.lower():
                        # 检查是否提到其他记忆
                        if other_title.lower() in content.lower() or str(other_id) in content:
                            causal_relations.append({
                                'cause_id': memory_id,
                                'effect_id': other_id,
                                'causal_type': causal_type,
                                'strength': 0.6,
                                'confidence': 0.5,
                                'evidence': f"Keyword '{keyword}' found in content",
                                'conditions': None,
                                'time_delay': 0
                            })
                            break

        return causal_relations

    def detect_knowledge_relations(self, memory_id: int) -> List[Dict]:
        """检测知识点关系"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 获取记忆内容
        cursor.execute("""
            SELECT id, title, content, type, category
            FROM memories
            WHERE id = ?
        """, (memory_id,))

        row = cursor.fetchone()
        if not row:
            conn.close()
            return []

        memory_id, title, content, memory_type, category = row

        # 获取所有其他记忆
        cursor.execute("""
            SELECT id, title, content, type, category
            FROM memories
            WHERE id != ?
            ORDER BY created_at DESC
            LIMIT 50
        """, (memory_id,))

        other_memories = cursor.fetchall()
        conn.close()

        knowledge_relations = []

        # 关系类型关键词
        relation_keywords = {
            'is_a': ['是一种', '是', '属于', 'is a', 'is an', 'belongs to'],
            'part_of': ['是...的一部分', '包含在', 'part of', 'contained in'],
            'related_to': ['相关', '关联', 'related to', 'associated with'],
            'similar_to': ['相似', '类似', 'similar to', 'like'],
            'opposite_of': ['相反', '对立', 'opposite of', 'opposite'],
            'depends_on': ['依赖', '依赖于', 'depends on', 'rely on'],
            'precedes': ['先于', '在...之前', 'precedes', 'before'],
            'follows': ['跟随', '在...之后', 'follows', 'after'],
            'causes': ['导致', '引起', 'causes', 'leads to'],
            'caused_by': ['由...导致', '被...引起', 'caused by', 'resulted from'],
            'contains': ['包含', '含有', 'contains', 'includes'],
            'contained_in': ['包含于', 'contained in', 'included in'],
            'exemplifies': ['例证', '举例说明', 'exemplifies', 'illustrates'],
            'exemplified_by': ['被例证', '被举例说明', 'exemplified by', 'illustrated by'],
            'context_for': ['是...的上下文', 'context for', 'context of'],
            'context_of': ['...的上下文', 'context of']
        }

        for other_id, other_title, other_content, other_type, other_category in other_memories:
            # 检查关系关键词
            for relation_type, keywords in relation_keywords.items():
                for keyword in keywords:
                    if keyword in content.lower():
                        # 检查是否提到其他记忆
                        if other_title.lower() in content.lower() or str(other_id) in content:
                            knowledge_relations.append({
                                'source_id': memory_id,
                                'target_id': other_id,
                                'relation_type': relation_type,
                                'strength': 0.6,
                                'direction': 'unidirectional',
                                'attributes': {
                                    'keyword': keyword,
                                    'source_type': memory_type,
                                    'target_type': other_type,
                                    'source_category': category,
                                    'target_category': other_category
                                }
                            })
                            break

        return knowledge_relations

    def detect_relations_by_similarity(self, memory_id: int, threshold: float = 0.3) -> List[Dict]:
        """基于相似度检测关系"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 获取记忆内容
        cursor.execute("""
            SELECT id, title, content, type, category
            FROM memories
            WHERE id = ?
        """, (memory_id,))

        row = cursor.fetchone()
        if not row:
            conn.close()
            return []

        memory_id, title, content, memory_type, category = row

        # 获取所有其他记忆
        cursor.execute("""
            SELECT id, title, content, type, category
            FROM memories
            WHERE id != ?
            ORDER BY created_at DESC
            LIMIT 50
        """, (memory_id,))

        other_memories = cursor.fetchall()
        conn.close()

        knowledge_relations = []

        # 简单的相似度计算（基于关键词重叠）
        content_words = set(re.findall(r'\w+', content.lower()))

        for other_id, other_title, other_content, other_type, other_category in other_memories:
            other_words = set(re.findall(r'\w+', other_content.lower()))

            # 计算Jaccard相似度
            intersection = len(content_words & other_words)
            union = len(content_words | other_words)

            if union > 0:
                similarity = intersection / union

                if similarity >= threshold:
                    knowledge_relations.append({
                        'source_id': memory_id,
                        'target_id': other_id,
                        'relation_type': 'similar_to',
                        'strength': similarity,
                        'direction': 'bidirectional',
                        'attributes': {
                            'similarity': similarity,
                            'intersection': intersection,
                            'union': union,
                            'source_type': memory_type,
                            'target_type': other_type,
                            'source_category': category,
                            'target_category': other_category
                        }
                    })

        return knowledge_relations

    def detect_relations_by_category(self, memory_id: int) -> List[Dict]:
        """基于类别检测关系"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 获取记忆内容
        cursor.execute("""
            SELECT id, title, content, type, category
            FROM memories
            WHERE id = ?
        """, (memory_id,))

        row = cursor.fetchone()
        if not row:
            conn.close()
            return []

        memory_id, title, content, memory_type, category = row

        if not category:
            conn.close()
            return []

        # 获取同类别记忆
        cursor.execute("""
            SELECT id, title, content, type, category
            FROM memories
            WHERE id != ? AND category = ?
            ORDER BY created_at DESC
            LIMIT 20
        """, (memory_id, category))

        other_memories = cursor.fetchall()
        conn.close()

        knowledge_relations = []

        for other_id, other_title, other_content, other_type, other_category in other_memories:
            knowledge_relations.append({
                'source_id': memory_id,
                'target_id': other_id,
                'relation_type': 'related_to',
                'strength': 0.5,
                'direction': 'bidirectional',
                'attributes': {
                    'reason': 'same_category',
                    'category': category,
                    'source_type': memory_type,
                    'target_type': other_type
                }
            })

        return knowledge_relations


class AutoRelationManager:
    """自动关系管理器"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.detector = RelationDetector(db_path)

    def auto_detect_and_add_relations(self, memory_id: int) -> Dict:
        """自动检测并添加关系"""
        results = {
            'memory_id': memory_id,
            'causal_relations': [],
            'knowledge_relations': [],
            'timestamp': datetime.now().isoformat()
        }

        # 检测因果关系
        causal_relations = self.detector.detect_causal_relations(memory_id)
        for relation in causal_relations:
            self._add_causal_relation(relation)
            results['causal_relations'].append(relation)

        # 检测知识点关系（关键词）
        knowledge_relations = self.detector.detect_knowledge_relations(memory_id)
        for relation in knowledge_relations:
            self._add_knowledge_relation(relation)
            results['knowledge_relations'].append(relation)

        # 检测知识点关系（相似度）
        similarity_relations = self.detector.detect_relations_by_similarity(memory_id)
        for relation in similarity_relations:
            self._add_knowledge_relation(relation)
            results['knowledge_relations'].append(relation)

        # 检测知识点关系（类别）
        category_relations = self.detector.detect_relations_by_category(memory_id)
        for relation in category_relations:
            self._add_knowledge_relation(relation)
            results['knowledge_relations'].append(relation)

        return results

    def _add_causal_relation(self, relation: Dict) -> bool:
        """添加因果关系"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            conditions_json = json.dumps(relation.get('conditions')) if relation.get('conditions') else None

            cursor.execute("""
                INSERT INTO causal_relations
                (cause_memory_id, effect_memory_id, causal_type, strength, confidence, evidence, conditions, time_delay, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                relation['cause_id'],
                relation['effect_id'],
                relation['causal_type'],
                relation['strength'],
                relation['confidence'],
                relation['evidence'],
                conditions_json,
                relation.get('time_delay', 0),
                datetime.now(),
                datetime.now()
            ))

            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding causal relation: {e}")
            return False
        finally:
            conn.close()

    def _add_knowledge_relation(self, relation: Dict) -> bool:
        """添加知识点关系"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            attributes_json = json.dumps(relation.get('attributes')) if relation.get('attributes') else None

            cursor.execute("""
                INSERT INTO knowledge_relations
                (source_memory_id, target_memory_id, relation_type, relation_strength, relation_direction, attributes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                relation['source_id'],
                relation['target_id'],
                relation['relation_type'],
                relation['strength'],
                relation['direction'],
                attributes_json,
                datetime.now(),
                datetime.now()
            ))

            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding knowledge relation: {e}")
            return False
        finally:
            conn.close()

    def batch_detect_relations(self, limit: int = 100) -> List[Dict]:
        """批量检测关系"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 获取最近的记忆
        cursor.execute("""
            SELECT id
            FROM memories
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))

        memory_ids = [row[0] for row in cursor.fetchall()]
        conn.close()

        results = []
        for memory_id in memory_ids:
            result = self.auto_detect_and_add_relations(memory_id)
            results.append(result)

        return results


if __name__ == "__main__":
    # 测试代码
    db_path = "C:\\Users\\Administrator\\.openclaw\\workspace\\memory\\database\\xiaozhi_memory.db"

    manager = AutoRelationManager(db_path)

    print("Auto Relation Manager initialized successfully!")

    # 测试单个记忆
    print("\nTesting single memory detection...")
    result = manager.auto_detect_and_add_relations(1)
    print(f"Found {len(result['causal_relations'])} causal relations")
    print(f"Found {len(result['knowledge_relations'])} knowledge relations")
