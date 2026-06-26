#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Memory System - Database Initialization
完整记忆系统 - 数据库初始化脚本
"""

import sqlite3
import os
from datetime import datetime

def init_database(db_path: str = "memory/database/xiaozhi_memory.db") -> bool:
    """
    初始化完整记忆系统数据库

    Args:
        db_path: 数据库路径

    Returns:
        是否成功
    """
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("开始初始化数据库...")
        print(f"数据库路径: {db_path}")

        # 创建所有20个表
        tables = [
            # 1. 核心记忆表
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                category TEXT,
                tags TEXT,
                importance INTEGER DEFAULT 5,
                confidence REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,

            # 2. 情景记忆表
            """
            CREATE TABLE IF NOT EXISTS episodic_memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                content TEXT NOT NULL,
                emotion TEXT,
                importance INTEGER DEFAULT 5,
                source TEXT,
                aaak_content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,

            # 3. 语义记忆表
            """
            CREATE TABLE IF NOT EXISTS semantic_memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                predicate TEXT NOT NULL,
                object TEXT NOT NULL,
                confidence REAL DEFAULT 1.0,
                source TEXT,
                valid_until TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,

            # 4. 程序记忆表
            """
            CREATE TABLE IF NOT EXISTS procedural_memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                skill_name TEXT NOT NULL,
                skill_type TEXT,
                description TEXT,
                steps TEXT,
                success_count INTEGER DEFAULT 0,
                fail_count INTEGER DEFAULT 0,
                last_used TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,

            # 5. 工作记忆表
            """
            CREATE TABLE IF NOT EXISTS working_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT,
                ttl_seconds INTEGER,
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,

            # 6. Agent日记表
            """
            CREATE TABLE IF NOT EXISTS agent_diary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                date TEXT NOT NULL,
                summary TEXT NOT NULL,
                aaak_entry TEXT,
                learnings TEXT,
                decisions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,

            # 7. 检索缓存表
            """
            CREATE TABLE IF NOT EXISTS retrieval_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                strategy TEXT NOT NULL,
                results TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,

            # 8. 原创想法表
            """
            CREATE TABLE IF NOT EXISTS originals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                slug TEXT,
                importance INTEGER DEFAULT 10,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,

            # 9. 实体表
            """
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                tier INTEGER DEFAULT 2,
                compiled_truth TEXT,
                timeline TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,

            # 10. 实体时间线表
            """
            CREATE TABLE IF NOT EXISTS entity_timelines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                event TEXT NOT NULL,
                source TEXT,
                FOREIGN KEY (entity_id) REFERENCES entities(id)
            )
            """,

            # 11. 分层上下文表
            """
            CREATE TABLE IF NOT EXISTS layered_context (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                layer INTEGER NOT NULL,
                scope TEXT NOT NULL,
                data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,

            # 12. 自进化记录表
            """
            CREATE TABLE IF NOT EXISTS evolution_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                description TEXT,
                impact TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,

            # 13. 工具注册表
            """
            CREATE TABLE IF NOT EXISTS registered_tools (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                description TEXT,
                capabilities TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,

            # 14. 平台消息表
            """
            CREATE TABLE IF NOT EXISTS platform_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                channel TEXT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,

            # 15. 会话摘要表
            """
            CREATE TABLE IF NOT EXISTS session_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                summary TEXT,
                key_points TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,

            # 16. 安全扫描表
            """
            CREATE TABLE IF NOT EXISTS security_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                scan_type TEXT NOT NULL,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,

            # 17. 漏洞发现表
            """
            CREATE TABLE IF NOT EXISTS vulnerability_findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id INTEGER NOT NULL,
                severity TEXT NOT NULL,
                location TEXT,
                description TEXT,
                FOREIGN KEY (scan_id) REFERENCES security_scans(id)
            )
            """,

            # 18. OSINT情报表
            """
            CREATE TABLE IF NOT EXISTS osint_intel (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                intel_type TEXT NOT NULL,
                data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,

            # 19. 攻击链表
            """
            CREATE TABLE IF NOT EXISTS attack_chains (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                chain_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,

            # 20. 系统配置表
            """
            CREATE TABLE IF NOT EXISTS system_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
        ]

        # 创建表
        for i, table_sql in enumerate(tables, 1):
            cursor.execute(table_sql)
            print(f"  [OK] 创建表 {i}/20")

        # 创建索引
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(type)",
            "CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance)",
            "CREATE INDEX IF NOT EXISTS idx_episodic_emotion ON episodic_memories(emotion)",
            "CREATE INDEX IF NOT EXISTS idx_semantic_subject ON semantic_memories(subject)",
            "CREATE INDEX IF NOT EXISTS idx_procedural_skill ON procedural_memories(skill_name)",
            "CREATE INDEX IF NOT EXISTS idx_working_session ON working_memory(session_id)",
            "CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name)",
            "CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(type)",
            "CREATE INDEX IF NOT EXISTS idx_timeline_entity ON entity_timelines(entity_id)",
            "CREATE INDEX IF NOT EXISTS idx_context_layer ON layered_context(layer)",
        ]

        for i, index_sql in enumerate(indexes, 1):
            cursor.execute(index_sql)
            print(f"  [OK] 创建索引 {i}/10")

        # 提交
        conn.commit()

        # 验证表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables_created = [row[0] for row in cursor.fetchall()]

        print(f"\n[OK] 数据库初始化完成！")
        print(f"  总计 {len(tables_created)} 个表")

        conn.close()
        return True

    except Exception as e:
        print(f"[ERROR] 初始化失败: {e}")
        return False


if __name__ == "__main__":
    import sys

    # 获取数据库路径
    db_path = sys.argv[1] if len(sys.argv) > 1 else "memory/database/xiaozhi_memory.db"

    # 初始化
    success = init_database(db_path)

    if success:
        print("\n[OK] 数据库初始化成功！")
        sys.exit(0)
    else:
        print("\n[ERROR] 数据库初始化失败！")
        sys.exit(1)
