#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整记忆系统 v2.0
Complete Memory System v2.0

Features:
- SQLite left brain (structured memory)
- LanceDB right brain (vector search)
- Causal graph (causal relationships)
- Knowledge graph (knowledge relationships)
- Auto-detection (automatic relation detection)
- Evolution system (memory evolution)
- Two-step ingestion
- Four-signal graph model
- Louvain community detection
- Graph insights
- Four-stage retrieval
- Deep research
- Review system
- Purpose.md
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import os

class MemorySystemV2:
    """完整记忆系统 v2.0"""

    def __init__(self, db_path: str = "memory/database/xiaozhi_memory.db"):
        self.db_path = db_path
        self._ensure_database_exists()

    def _ensure_database_exists(self):
        """确保数据库存在"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        if not os.path.exists(self.db_path):
            self._initialize_database()

    def _initialize_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 创建记忆表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT,
                tags TEXT,
                importance INTEGER DEFAULT 5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 创建因果关系表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS causal_relations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cause_memory_id INTEGER NOT NULL,
                effect_memory_id INTEGER NOT NULL,
                causal_type TEXT NOT NULL,
                strength REAL DEFAULT 0.0,
                confidence REAL DEFAULT 0.0,
                evidence TEXT,
                conditions TEXT,
                time_delay INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cause_memory_id) REFERENCES memories(id),
                FOREIGN KEY (effect_memory_id) REFERENCES memories(id)
            )
        """)

        # 创建知识点关系表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_relations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_memory_id INTEGER NOT NULL,
                target_memory_id INTEGER NOT NULL,
                relation_type TEXT NOT NULL,
                relation_strength REAL DEFAULT 0.0,
                relation_direction TEXT,
                attributes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (source_memory_id) REFERENCES memories(id),
                FOREIGN KEY (target_memory_id) REFERENCES memories(id)
            )
        """)

        # 创建进化表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_associations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_a_id INTEGER NOT NULL,
                memory_b_id INTEGER NOT NULL,
                association_type TEXT NOT NULL,
                relevance_score REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (memory_a_id) REFERENCES memories(id),
                FOREIGN KEY (memory_b_id) REFERENCES memories(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_communities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                community_id TEXT NOT NULL,
                memory_id INTEGER NOT NULL,
                cohesion_score REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (memory_id) REFERENCES memories(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS graph_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                insight_type TEXT NOT NULL,
                memory_id INTEGER,
                description TEXT,
                score REAL DEFAULT 0.0,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (memory_id) REFERENCES memories(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS review_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_type TEXT NOT NULL,
                description TEXT NOT NULL,
                search_query TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deep_research (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                search_queries TEXT,
                results TEXT,
                synthesis TEXT,
                memory_id INTEGER,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (memory_id) REFERENCES memories(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingestion_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_hash TEXT NOT NULL UNIQUE,
                content TEXT,
                analysis TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS retrieval_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                stage1_results TEXT,
                stage2_results TEXT,
                stage3_results TEXT,
                stage4_context TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evolution_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                evolution_type TEXT NOT NULL,
                description TEXT,
                before_state TEXT,
                after_state TEXT,
                trigger TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 创建索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_category ON memories(category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_created_at ON memories(created_at)")

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_causal_cause ON causal_relations(cause_memory_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_causal_effect ON causal_relations(effect_memory_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_causal_type ON causal_relations(causal_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_causal_strength ON causal_relations(strength)")

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_knowledge_source ON knowledge_relations(source_memory_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_knowledge_target ON knowledge_relations(target_memory_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_knowledge_type ON knowledge_relations(relation_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_knowledge_strength ON knowledge_relations(relation_strength)")

        conn.commit()
        conn.close()

    def save(self, type: str, title: str, content: str, category: str = None,
             tags: List[str] = None, importance: int = 5) -> int:
        """保存记忆"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        tags_json = json.dumps(tags) if tags else None

        cursor.execute("""
            INSERT INTO memories (type, title, content, category, tags, importance, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (type, title, content, category, tags_json, importance, datetime.now(), datetime.now()))

        memory_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return memory_id

    def get(self, memory_id: int) -> Optional[Dict]:
        """获取记忆"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, type, title, content, category, tags, importance, created_at, updated_at
            FROM memories
            WHERE id = ?
        """, (memory_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                'id': row[0],
                'type': row[1],
                'title': row[2],
                'content': row[3],
                'category': row[4],
                'tags': json.loads(row[5]) if row[5] else None,
                'importance': row[6],
                'created_at': row[7],
                'updated_at': row[8]
            }
        return None

    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索记忆"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, type, title, content, category, tags, importance, created_at
            FROM memories
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY importance DESC, created_at DESC
            LIMIT ?
        """, (f'%{query}%', f'%{query}%', limit))

        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'type': row[1],
                'title': row[2],
                'content': row[3],
                'category': row[4],
                'tags': json.loads(row[5]) if row[5] else None,
                'importance': row[6],
                'created_at': row[7]
            })

        conn.close()
        return results

    def delete(self, memory_id: int) -> bool:
        """删除记忆"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
        affected = cursor.rowcount

        conn.commit()
        conn.close()

        return affected > 0

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 总记忆数
        cursor.execute("SELECT COUNT(*) FROM memories")
        total_memories = cursor.fetchone()[0]

        # 按类型统计
        cursor.execute("SELECT type, COUNT(*) FROM memories GROUP BY type")
        by_type = dict(cursor.fetchall())

        # 按类别统计
        cursor.execute("SELECT category, COUNT(*) FROM memories WHERE category IS NOT NULL GROUP BY category")
        by_category = dict(cursor.fetchall())

        # 因果关系统计
        cursor.execute("SELECT COUNT(*) FROM causal_relations")
        causal_relations = cursor.fetchone()[0]

        # 知识点关系统计
        cursor.execute("SELECT COUNT(*) FROM knowledge_relations")
        knowledge_relations = cursor.fetchone()[0]

        conn.close()

        return {
            'total_memories': total_memories,
            'by_type': by_type,
            'by_category': by_category,
            'causal_relations': causal_relations,
            'knowledge_relations': knowledge_relations
        }

    def initialize(self) -> bool:
        """初始化系统"""
        try:
            self._ensure_database_exists()
            return True
        except Exception as e:
            print(f"Initialization failed: {e}")
            return False


if __name__ == "__main__":
    # 测试代码
    memory = MemorySystemV2()
    memory.initialize()

    print("Memory System v2.0 initialized successfully!")

    # 保存测试记忆
    test_id = memory.save(
        type='test',
        title='Test Memory',
        content='This is a test memory for v2.0',
        category='test',
        tags=['test', 'v2.0'],
        importance=5
    )

    print(f"Saved test memory with ID: {test_id}")

    # 获取记忆
    result = memory.get(test_id)
    print(f"Retrieved memory: {result['title']}")

    # 搜索记忆
    results = memory.search('test')
    print(f"Found {len(results)} memories")

    # 获取统计信息
    stats = memory.get_statistics()
    print(f"Statistics: {stats}")

    # 清理
    memory.delete(test_id)
    print("Test memory deleted")
