"""
安全实现模块
提供基础的 FTS 搜索功能，无需私有包
"""

import sqlite3
import json
import uuid
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from .interfaces.search import ISearchEngine
from .interfaces.memory import IMemoryStore


class SafeFTSSearchEngine(ISearchEngine):
    """
    安全 FTS 搜索引擎
    纯 Python + SQLite FTS5 实现
    """

    def __init__(self, db_path: str = None):
        """
        初始化搜索引擎

        Args:
            db_path: 数据库路径，默认 ~/.openclaw/memory-tdai/memories.db
        """
        if db_path is None:
            db_path = Path.home() / ".openclaw" / "memory-tdai" / "memories.db"

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """初始化数据库"""
        conn = self._get_conn()
        cursor = conn.cursor()

        # 创建记忆表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                metadata TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)

        # 创建 FTS 索引
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts
            USING fts5(content, content='memories', content_rowid='rowid')
        """)

        # 创建触发器
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
                INSERT INTO memories_fts(rowid, content) VALUES (new.rowid, new.content);
            END
        """)

        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
                INSERT INTO memories_fts(memories_fts, rowid, content)
                VALUES('delete', old.rowid, old.content);
            END
        """)

        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
                INSERT INTO memories_fts(memories_fts, rowid, content)
                VALUES('delete', old.rowid, old.content);
                INSERT INTO memories_fts(rowid, content) VALUES (new.rowid, new.content);
            END
        """)

        conn.commit()
        conn.close()

    def _get_conn(self) -> sqlite3.Connection:
        """获取数据库连接"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def search(self, query: str, top_k: int = 10) -> Dict[str, Any]:
        """搜索记忆"""
        import time
        start = time.time()

        conn = self._get_conn()
        cursor = conn.cursor()

        try:
            # FTS 搜索
            cursor.execute("""
                SELECT m.id, m.content, m.metadata, m.created_at
                FROM memories m
                JOIN memories_fts fts ON m.rowid = fts.rowid
                WHERE memories_fts MATCH ?
                ORDER BY bm25(memories_fts)
                LIMIT ?
            """, (query, top_k))

            results = []
            for row in cursor.fetchall():
                results.append({
                    "id": row["id"],
                    "content": row["content"],
                    "metadata": json.loads(row["metadata"]) if row["metadata"] else {},
                    "created_at": row["created_at"]
                })

            return {
                "query": query,
                "results": results,
                "total": len(results),
                "latency_ms": (time.time() - start) * 1000,
                "backend": "safe_fts"
            }
        except Exception as e:
            # FTS 失败时降级到 LIKE
            cursor.execute("""
                SELECT id, content, metadata, created_at
                FROM memories
                WHERE content LIKE ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (f"%{query}%", top_k))

            results = []
            for row in cursor.fetchall():
                results.append({
                    "id": row["id"],
                    "content": row["content"],
                    "metadata": json.loads(row["metadata"]) if row["metadata"] else {},
                    "created_at": row["created_at"]
                })

            return {
                "query": query,
                "results": results,
                "total": len(results),
                "latency_ms": (time.time() - start) * 1000,
                "backend": "safe_like"
            }
        finally:
            conn.close()

    def add(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """添加记忆"""
        memory_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        metadata = metadata or {}

        conn = self._get_conn()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO memories (id, content, metadata, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (memory_id, content, json.dumps(metadata), now, now))

            conn.commit()
            return memory_id
        finally:
            conn.close()

    def delete(self, memory_id: str) -> bool:
        """删除记忆"""
        conn = self._get_conn()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    def get(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """获取单条记忆"""
        conn = self._get_conn()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT id, content, metadata, created_at, updated_at
                FROM memories WHERE id = ?
            """, (memory_id,))

            row = cursor.fetchone()
            if row:
                return {
                    "id": row["id"],
                    "content": row["content"],
                    "metadata": json.loads(row["metadata"]) if row["metadata"] else {},
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"]
                }
            return None
        finally:
            conn.close()


class SafeMemoryStore(IMemoryStore):
    """
    安全记忆存储
    """

    def __init__(self, db_path: str = None):
        self.engine = SafeFTSSearchEngine(db_path)

    def store(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        return self.engine.add(content, metadata)

    def retrieve(self, memory_id: str) -> Optional[Dict[str, Any]]:
        return self.engine.get(memory_id)

    def list(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        result = self.engine.search("*", top_k=limit)
        return result.get("results", [])

    def count(self) -> int:
        conn = self.engine._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) as count FROM memories")
            return cursor.fetchone()["count"]
        finally:
            conn.close()


# 便捷函数
def get_search_engine(db_path: str = None) -> ISearchEngine:
    """获取搜索引擎实例"""
    return SafeFTSSearchEngine(db_path)


def get_memory_store(db_path: str = None) -> IMemoryStore:
    """获取记忆存储实例"""
    return SafeMemoryStore(db_path)
