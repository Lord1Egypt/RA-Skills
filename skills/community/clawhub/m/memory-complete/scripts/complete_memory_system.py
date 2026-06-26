#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Memory System v4.0
完整记忆系统 - 统一入口
整合所有记忆相关功能：双脑架构、四层记忆栈、四策略检索、ToM、情感分析、GBrain等
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any

# 导入所有子系统
from retrieval_strategies import FourStrategyRetrieval
from memory_palace import MemPalace
from tom_engine import ToMEngine
from emotional_analyzer import EmotionalAnalyzer
from enhanced_retrieval import EnhancedRetrieval
from ollama_embedding import OllamaEmbedding

class CompleteMemorySystem:
    """完整记忆系统 - 统一入口"""

    def __init__(self, db_path: str = None, config: Dict = None):
        """
        初始化完整记忆系统

        Args:
            db_path: SQLite数据库路径
            config: 配置字典
        """
        if db_path is None:
            db_path = "memory/database/xiaozhi_memory.db"

        self.db_path = db_path
        self.config = config or {}
        self.conn = None

        # 初始化子系统
        self.retrieval = FourStrategyRetrieval(db_path)
        self.palace = MemPalace(db_path)
        self.tom = ToMEngine(db_path)
        self.emotional = EmotionalAnalyzer()
        self.enhanced = EnhancedRetrieval(db_path)

        # 初始化Ollama（可选）
        self.ollama = None
        if self.config.get('use_ollama', False):
            ollama_model = self.config.get('ollama_model', 'nomic-embed-text')
            ollama_url = self.config.get('ollama_url', 'http://localhost:11434')
            self.ollama = OllamaEmbedding(model=ollama_model, base_url=ollama_url)

    def initialize(self) -> bool:
        """初始化所有子系统"""
        try:
            # 连接数据库
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row

            # 初始化子系统
            self.palace.connect()
            self.tom.initialize()
            self.enhanced.initialize()

            # 创建所有表
            self._create_all_tables()

            return True
        except Exception as e:
            print(f"初始化失败: {e}")
            return False

    def _create_all_tables(self):
        """创建所有20个表"""
        cursor = self.conn.cursor()

        # 1. 核心记忆表
        cursor.execute("""
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
        """)

        # 2. 情景记忆表
        cursor.execute("""
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
        """)

        # 3. 语义记忆表
        cursor.execute("""
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
        """)

        # 4. 程序记忆表
        cursor.execute("""
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
        """)

        # 5. 工作记忆表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS working_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT,
                ttl_seconds INTEGER,
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 6. Agent日记表
        cursor.execute("""
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
        """)

        # 7. 检索缓存表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS retrieval_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                strategy TEXT NOT NULL,
                results TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 8. 原创想法表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS originals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                slug TEXT,
                importance INTEGER DEFAULT 10,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 9. 实体表
        cursor.execute("""
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
        """)

        # 10. 实体时间线表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entity_timelines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                event TEXT NOT NULL,
                source TEXT,
                FOREIGN KEY (entity_id) REFERENCES entities(id)
            )
        """)

        # 11. 分层上下文表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS layered_context (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                layer INTEGER NOT NULL,
                scope TEXT NOT NULL,
                data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 12. 自进化记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evolution_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                description TEXT,
                impact TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 13. 工具注册表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registered_tools (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                description TEXT,
                capabilities TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 14. 平台消息表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS platform_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                channel TEXT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 15. 会话摘要表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS session_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                summary TEXT,
                key_points TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 16. 安全扫描表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS security_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                scan_type TEXT NOT NULL,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 17. 漏洞发现表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vulnerability_findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id INTEGER NOT NULL,
                severity TEXT NOT NULL,
                location TEXT,
                description TEXT,
                FOREIGN KEY (scan_id) REFERENCES security_scans(id)
            )
        """)

        # 18. OSINT情报表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS osint_intel (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                intel_type TEXT NOT NULL,
                data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 19. 攻击链表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attack_chains (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                chain_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 20. 系统配置表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 创建索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_episodic_emotion ON episodic_memories(emotion)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_semantic_subject ON semantic_memories(subject)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_procedural_skill ON procedural_memories(skill_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_working_session ON working_memory(session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_timeline_entity ON entity_timelines(entity_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_context_layer ON layered_context(layer)")

        self.conn.commit()

    # ==================== 统一API ====================

    def add_memory(self, memory_type: str, title: str, content: str,
                   category: str = None, tags: List[str] = None,
                   importance: int = 5) -> int:
        """添加记忆（统一API）"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO memories (type, title, content, category, tags, importance)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (memory_type, title, content, category,
              json.dumps(tags or []), importance))
        self.conn.commit()
        return cursor.lastrowid

    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """搜索记忆（统一API）"""
        return self.enhanced.search(query, limit=limit)

    def smart_search(self, query: str, mode: str = "balanced") -> Dict:
        """智能搜索（四策略）"""
        return self.retrieval.smart_retrieve(query, mode=mode)

    def analyze_emotion(self, text: str) -> Dict:
        """分析情感（统一API）"""
        return self.emotional.analyze(text)

    def update_belief(self, entity: str, belief_type: str,
                     content: str, confidence: float = 0.5) -> int:
        """更新信念（ToM）"""
        return self.tom.update_belief(entity, belief_type, content, confidence)

    def write_diary(self, summary: str, learnings: List[str] = None,
                    decisions: List[str] = None) -> int:
        """写日记（统一API）"""
        return self.palace.write_diary(summary, learnings or [], decisions or [])

    def add_knowledge(self, subject: str, predicate: str, obj: str) -> int:
        """添加知识（统一API）"""
        return self.palace.add_knowledge(subject, predicate, obj)

    def add_skill(self, skill_name: str, skill_type: str,
                  description: str, steps: List[str]) -> int:
        """添加技能（统一API）"""
        return self.palace.add_skill(skill_name, skill_type, description, steps)

    def get_statistics(self) -> Dict:
        """获取统计信息（统一API）"""
        return self.enhanced.get_statistics()

    def close(self):
        """关闭所有连接"""
        if self.conn:
            self.conn.close()
        self.palace.close()
        self.tom.close()
        self.enhanced.close()


def main():
    """测试完整记忆系统"""
    print("="*60)
    print("完整记忆系统 v4.0 - 测试")
    print("="*60)

    # 初始化
    system = CompleteMemorySystem()
    if not system.initialize():
        print("初始化失败！")
        return

    print("\n[OK] 系统初始化成功")

    # 测试添加记忆
    print("\n--- 测试添加记忆 ---")
    mem_id = system.add_memory(
        memory_type="test",
        title="测试记忆",
        content="这是一条测试记忆",
        importance=8
    )
    print(f"[OK] 添加记忆 ID: {mem_id}")

    # 测试搜索
    print("\n--- 测试搜索 ---")
    results = system.search("测试", limit=5)
    print(f"[OK] 找到 {len(results)} 条结果")

    # 测试情感分析
    print("\n--- 测试情感分析 ---")
    emotion = system.analyze_emotion("I am very happy!")
    print(f"[OK] 情感: {emotion['primary_emotion']} (置信度: {emotion['confidence']:.2f})")

    # 测试智能搜索
    print("\n--- 测试智能搜索 ---")
    smart = system.smart_search("测试", mode="balanced")
    print(f"[OK] 智能搜索: {len(smart['merged'])} 条结果")

    # 测试统计
    print("\n--- 测试统计 ---")
    stats = system.get_statistics()
    print(f"[OK] 总记忆数: {stats['total']}")

    # 关闭
    system.close()
    print("\n[OK] 测试完成")


if __name__ == "__main__":
    main()
