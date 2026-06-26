#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化数据库 v2.0
Initialize Database v2.0
"""

import sqlite3
import os
from datetime import datetime

def create_database_directory(db_path):
    """创建数据库目录"""
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
        print(f"[OK] Created directory: {db_dir}")

def initialize_database(db_path):
    """初始化数据库"""
    conn = sqlite3.connect(db_path)
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

    print("[OK] Database initialized")

def verify_database(db_path):
    """验证数据库"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    expected_tables = [
        'memories',
        'causal_relations',
        'knowledge_relations',
        'memory_associations',
        'memory_communities',
        'graph_insights',
        'review_queue',
        'deep_research',
        'ingestion_cache',
        'retrieval_history',
        'evolution_log'
    ]

    print("\n[Verification]")
    for table in expected_tables:
        if table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  [OK] {table} ({count} records)")
        else:
            print(f"  [X] {table} (not found)")

    conn.close()

def main():
    """主函数"""
    print("="*60)
    print("Initialize Memory System Database v2.0")
    print("="*60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")

    db_path = "memory/database/xiaozhi_memory.db"

    # 1. 创建数据库目录
    print("[1/3] Creating database directory...")
    create_database_directory(db_path)

    # 2. 初始化数据库
    print("\n[2/3] Initializing database...")
    initialize_database(db_path)

    # 3. 验证数据库
    print("\n[3/3] Verifying database...")
    verify_database(db_path)

    print("\n" + "="*60)
    print("Initialization Complete!")
    print("="*60)
    print("\nNext Steps:")
    print("1. Run: python scripts/verify_install_v2.py")
    print("2. Start using: from scripts.memory_system_v2 import MemorySystemV2")
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
