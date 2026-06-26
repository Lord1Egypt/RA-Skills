#!/usr/bin/env python3
"""
Hermes Agent - 主动记忆与自我建模
提取用户偏好习惯，形成结构化洞察，支持全文检索定位历史

隐私说明：
- 所有持久化行为受 hermes_config 控制
- 需显式设置 HERMES_PERSISTENCE_ENABLED=true 或调用 hermes_config.set_persistence(True) 才会写磁盘
- 敏感内容自动过滤，避免存储密码、密钥等敏感信息
"""
import sqlite3
import json
import threading
import time
import hashlib
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict

from hermes_config import hermes_config


# === 敏感内容检测 ===
_SENSITIVE_PATTERNS = [
    (re.compile(r'api[_-]?key', re.IGNORECASE), "[API_KEY]"),
    (re.compile(r'secret[_-]?key', re.IGNORECASE), "[SECRET]"),
    (re.compile(r'password', re.IGNORECASE), "[PASSWORD]"),
    (re.compile(r'token[=:\s]+[\w\-]{10,}', re.IGNORECASE), "[TOKEN]"),
    (re.compile(r'bearer\s+[\w\-]{10,}', re.IGNORECASE), "[TOKEN]"),
    (re.compile(r'-----BEGIN\s+(RSA|DSA|EC|OPENSSH|PGP)\s+PRIVATE KEY-----'), "[PRIVATE_KEY]"),
    (re.compile(r'-----BEGIN\s+CERTIFICATE-----'), "[CERTIFICATE]"),
    (re.compile(r'AKIA[0-9A-Z]{16}'), "[AWS_KEY]"),
    (re.compile(r'ghp?_[0-9a-zA-Z]{36,}'), "[GITHUB_TOKEN]"),
    (re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'), "[EMAIL]"),
]


def _filter_sensitive(text: str) -> str:
    """过滤文本中的敏感信息"""
    if not hermes_config.sensitive_filter_enabled:
        return text
    result = text
    for pattern, replacement in _SENSITIVE_PATTERNS:
        result = pattern.sub(replacement, result)
    return result

@dataclass
class UserInsight:
    """用户洞察结构化存储"""
    insight_id: str
    insight_type: str  # preference/habit/decision/fact
    content: str
    tags: List[str]
    created_at: float
    updated_at: float
    confidence: float  # 0-1，置信度
    reference_context: str  # 来自哪段对话

@dataclass
class MemoryEntry:
    """记忆条目，支持全文检索"""
    entry_id: str
    content: str
    category: str
    tags: List[str]
    created_at: float
    metadata: Dict[str, Any]

class HermesInsightDB:
    """
    基于 SQLite FTS5 的洞察记忆数据库
    支持全文检索快速定位历史细节

    惰性初始化：只有在 hermes_config.persistence_enabled=True 时才创建 DB 连接。
    所有持久化操作检查开关，不会在未授权情况下写入磁盘。
    """
    def __init__(self, db_path: str = "~/.hermes/insights.db"):
        self._db_path = db_path
        self._lock = threading.RLock()
        self._conn = None
        self._db_initialized = False

    def _ensure_db(self) -> bool:
        """确保数据库已初始化，返回是否可用"""
        if not hermes_config.is_persistence_enabled():
            return False
        if self._conn is not None:
            return True
        if self._db_initialized:
            return True
        with self._lock:
            if self._db_initialized:
                return True
            import os
            db_path = os.path.expanduser(self._db_path)
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            self._conn = sqlite3.connect(db_path, check_same_thread=False)
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA synchronous=NORMAL")
            self._init_tables()
            self._db_initialized = True
            return True

    def _init_tables(self):
        cursor = self._conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS insights (
                insight_id TEXT PRIMARY KEY,
                insight_type TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT NOT NULL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                confidence REAL NOT NULL,
                reference_context TEXT
            )
        """)
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts
            USING fts5(entry_id, content, category, tags, created_at, metadata);
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_insights_type ON insights(insight_type);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_insights_tags ON insights(tags);")
        self._conn.commit()

    def _get_conn(self):
        if not self._ensure_db():
            raise RuntimeError(
                "Hermes persistence is disabled. "
                "Set HERMES_PERSISTENCE_ENABLED=true or call hermes_config.set_persistence(True)"
            )
        return self._conn

    def add_insight(self, insight: UserInsight) -> str:
        """添加用户洞察（受持久化开关控制）"""
        if not hermes_config.is_persistence_enabled():
            return ""
        if not self._ensure_db():
            return ""
        if not insight.insight_id:
            insight.insight_id = self._hash_id(insight.content)
        insight.content = _filter_sensitive(insight.content)
        insight.reference_context = _filter_sensitive(insight.reference_context)
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute("""
                REPLACE INTO insights
                (insight_id, insight_type, content, tags, created_at, updated_at, confidence, reference_context)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                insight.insight_id,
                insight.insight_type,
                insight.content,
                json.dumps(insight.tags),
                insight.created_at,
                insight.updated_at,
                insight.confidence,
                insight.reference_context
            ))
            self._conn.commit()
        return insight.insight_id

    def search_insights(self, query: str, limit: int = 20) -> List[UserInsight]:
        """全文检索洞察（受持久化开关控制）"""
        if not hermes_config.is_persistence_enabled():
            return []
        if not self._ensure_db():
            return []
        safe_query = '"' + query.replace('"', '""') + '"'
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute("""
                SELECT i.insight_id, i.insight_type, i.content, i.tags,
                       i.created_at, i.updated_at, i.confidence, i.reference_context
                FROM insights i
                JOIN memory_fts m ON i.insight_id = m.entry_id
                WHERE memory_fts MATCH ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (safe_query, limit))

            results = []
            for row in cursor.fetchall():
                insight = UserInsight(
                    insight_id=row[0],
                    insight_type=row[1],
                    content=row[2],
                    tags=json.loads(row[3]),
                    created_at=row[4],
                    updated_at=row[5],
                    confidence=row[6],
                    reference_context=row[7]
                )
                results.append(insight)
            return results

    def add_memory(self, content: str, category: str, tags: List[str],
                  metadata: Dict[str, Any] = None) -> str:
        """添加记忆条目（受持久化开关控制）"""
        if not hermes_config.is_persistence_enabled():
            return ""
        if not self._ensure_db():
            return ""
        entry_id = self._hash_id(f"{content}{time.time()}")
        entry = MemoryEntry(
            entry_id=entry_id,
            content=_filter_sensitive(content),
            category=category,
            tags=tags,
            created_at=time.time(),
            metadata=metadata or {}
        )
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute("""
                INSERT INTO memory_fts
                (entry_id, content, category, tags, created_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                entry.entry_id,
                entry.content,
                entry.category,
                json.dumps(entry.tags),
                entry.created_at,
                json.dumps(entry.metadata)
            ))
            self._conn.commit()
        return entry_id

    def search_memory(self, query: str, category: Optional[str] = None,
                     limit: int = 20) -> List[Dict[str, Any]]:
        """全文检索记忆（受持久化开关控制）"""
        if not hermes_config.is_persistence_enabled():
            return []
        if not self._ensure_db():
            return []
        safe_query = '"' + query.replace('"', '""') + '"'
        with self._lock:
            cursor = self._conn.cursor()

            if category:
                sql = """
                    SELECT entry_id, content, category, tags, created_at, metadata
                    FROM memory_fts
                    WHERE memory_fts MATCH ? AND category = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                """
                params = (safe_query, category, limit)
            else:
                sql = """
                    SELECT entry_id, content, category, tags, created_at, metadata
                    FROM memory_fts
                    WHERE memory_fts MATCH ?
                    ORDER BY created_at DESC
                    LIMIT ?
                """
                params = (safe_query, limit)

            cursor.execute(sql, params)
            results = []
            for row in cursor.fetchall():
                results.append({
                    "entry_id": row[0],
                    "content": row[1],
                    "category": row[2],
                    "tags": json.loads(row[3]),
                    "created_at": row[4],
                    "metadata": json.loads(row[5])
                })
            return results

    def _hash_id(self, text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()[:12]

    def get_stats(self):
        if not hermes_config.is_persistence_enabled():
            return {"insights_count": 0, "memory_count": 0}
        if not self._ensure_db():
            return {"insights_count": 0, "memory_count": 0}
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM insights")
            insights_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM memory_fts")
            memory_count = cursor.fetchone()[0]
            return {
                "insights_count": insights_count,
                "memory_count": memory_count
            }

# === 主动分析对话提取洞察 ===

class InsightExtractor:
    """
    主动分析对话，提取用户偏好习惯，生成结构化洞察
    """
    PATTERNS = [
        # (pattern_type, trigger_keywords)
        ("preference", ["喜欢", "偏爱", "偏好", "更喜欢", "不要", "别用", "讨厌"]),
        ("habit", ["习惯", "通常", "一般", "每次", "总是", "经常"]),
        ("decision", ["决定", "选择", "选这个", "就用", "就这样"]),
        ("fact", ["我是", "我的", "我在", "我需要", "我想"]),
    ]

    def extract_from_conversation(self, text: str, context: str = "") -> List[UserInsight]:
        """从对话文本提取洞察（受 hermes_config 配置控制）"""
        insights = []
        now = time.time()
        safe_text = _filter_sensitive(text.strip())
        safe_context = _filter_sensitive(context[:200])

        for insight_type, keywords in self.PATTERNS:
            for kw in keywords:
                if kw in safe_text:
                    insight = UserInsight(
                        insight_id="",
                        insight_type=insight_type,
                        content=safe_text,
                        tags=[insight_type] + self._extract_tags(safe_text),
                        created_at=now,
                        updated_at=now,
                        confidence=0.7,
                        reference_context=safe_context
                    )
                    insights.append(insight)
                    break

        return insights

    def _extract_tags(self, text: str) -> List[str]:
        """简单从文本提取标签"""
        tags = []
        common_topics = ["code", "python", "go", "前端", "后端", "设计", "视频", "图片",
                         "笔记", "文档", "会议", "日程", "任务", "邮件"]
        for topic in common_topics:
            if topic in text.lower():
                tags.append(topic)
        return tags[:5]

# === 全局实例 ===
hermes_insight = HermesInsightDB()
insight_extractor = InsightExtractor()

if __name__ == "__main__":
    print("🧠 Hermes Agent - 主动记忆与自我建模")
    print("=" * 60)

    print("当前持久化状态:", hermes_config.is_persistence_enabled())

    # 测试：提取洞察（不依赖持久化开关）
    extracted = insight_extractor.extract_from_conversation(
        "我喜欢用 Python 写脚本，更快，不喜欢重型框架",
        "对话上下文..."
    )

    print(f"提取到 {len(extracted)} 条洞察:")
    for ins in extracted:
        print(f"  [{ins.insight_type}] {ins.content}")

    # 仅在持久化开启时才写入 DB
    if hermes_config.is_persistence_enabled():
        for ins in extracted:
            hermes_insight.add_insight(ins)
        hermes_insight.add_memory(
            "用户偏好 Python 轻量脚本，不喜欢重型框架",
            "preference",
            ["python", "lightweight"],
            {"source": "conversation-2026-04-17"}
        )
        print("\n🔍 全文检索 'Python':")
        results = hermes_insight.search_memory("Python", limit=5)
        for r in results:
            print(f"  - {r['content']}")
    else:
        print("\n(持久化未开启，跳过 DB 写入。使用 hermes_config.set_persistence(True) 开启)")

    print("\n📊 统计:")
    print(json.dumps(hermes_insight.get_stats(), indent=2))

    print("\n✅ 主动记忆模块就绪")
    print("  • 持久化默认关闭，需显式开启")
    print("  • 敏感信息自动过滤")
