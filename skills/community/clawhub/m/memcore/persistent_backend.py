"""
Persistent Backend for Enhanced MemCore
增强版 MemCore 的持久化存储后端
支持 SQLite 和 JSON 文件两种模式
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from dataclasses import asdict
from contextlib import contextmanager
import threading


class SQLiteBackend:
    """
    SQLite 持久化后端
    支持:
    - 情景记忆存储
    - 用户记忆存储
    - 触发器存储
    - 遗忘分数索引
    - 语义检索
    """
    
    def __init__(self, db_path: str = "~/.memcore/memory.db"):
        self.db_path = os.path.expanduser(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # 线程安全的连接池
        self._local = threading.local()
        self._init_database()
    
    @property
    def conn(self):
        """获取线程本地连接"""
        if not hasattr(self._local, 'conn') or self._local.conn is None:
            self._local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._local.conn.row_factory = sqlite3.Row
        return self._local.conn
    
    def _init_database(self):
        """初始化数据库表结构"""
        cursor = self.conn.cursor()
        
        # 情景记忆表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS episodic_memory (
                id TEXT PRIMARY KEY,
                episode_type TEXT NOT NULL,
                context_summary TEXT NOT NULL,
                conclusion TEXT NOT NULL,
                content TEXT NOT NULL,
                related_topics TEXT,  -- JSON 数组
                participants TEXT,    -- JSON 数组
                priority INTEGER DEFAULT 3,
                access_count INTEGER DEFAULT 0,
                compression_level INTEGER DEFAULT 0,
                forgetting_score REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 用户记忆表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_memory (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                value_type TEXT DEFAULT 'str',
                priority INTEGER DEFAULT 3,
                confidence REAL DEFAULT 1.0,
                source TEXT DEFAULT 'explicit',
                verification_count INTEGER DEFAULT 0,
                is_outdated BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, key)
            )
        """)
        
        # 触发器表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_triggers (
                id TEXT PRIMARY KEY,
                keywords TEXT NOT NULL,  -- JSON 数组
                target_memory_ids TEXT NOT NULL,  -- JSON 数组
                trigger_count INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 任务记忆表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS task_memory (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                goal TEXT NOT NULL,
                task_type TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                steps TEXT,  -- JSON 数组
                current_step INTEGER DEFAULT 0,
                results TEXT,  -- JSON 对象
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 知识库表（支持向量检索）
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_memory (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                embedding BLOB,  -- 向量嵌入
                metadata TEXT,   -- JSON 对象
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建索引优化查询
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_episodic_topics 
            ON episodic_memory(related_topics)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_episodic_forgetting 
            ON episodic_memory(forgetting_score, priority)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_memory 
            ON user_memory(user_id, key)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_task_user 
            ON task_memory(user_id, status)
        """)
        
        self.conn.commit()
        print(f"💾 数据库初始化完成: {self.db_path}")
    
    # ========== 情景记忆 CRUD ==========
    
    def save_episodic_memory(self, episode: 'EpisodicMemoryEntry') -> bool:
        """保存/更新情景记忆"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO episodic_memory (
                id, episode_type, context_summary, conclusion, content,
                related_topics, participants, priority, access_count,
                compression_level, forgetting_score, created_at, last_accessed
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            episode.id,
            episode.episode_type,
            episode.context_summary,
            episode.conclusion,
            json.dumps(episode.content, ensure_ascii=False),
            json.dumps(episode.related_topics, ensure_ascii=False),
            json.dumps(episode.participants, ensure_ascii=False),
            episode.priority.value if hasattr(episode.priority, 'value') else episode.priority,
            episode.access_count,
            episode.compression_level,
            episode.get_forgetting_score(),
            episode.timestamp.isoformat(),
            episode.last_accessed.isoformat()
        ))
        
        self.conn.commit()
        return True
    
    def load_episodic_memories(
        self,
        topic: Optional[str] = None,
        episode_type: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict]:
        """加载情景记忆"""
        cursor = self.conn.cursor()
        
        query = "SELECT * FROM episodic_memory WHERE 1=1"
        params = []
        
        if topic:
            query += " AND related_topics LIKE ?"
            params.append(f'%"{topic}"%')
        
        if episode_type:
            query += " AND episode_type = ?"
            params.append(episode_type)
        
        query += " ORDER BY priority DESC, last_accessed DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        return [self._row_to_episode_dict(row) for row in rows]
    
    def _row_to_episode_dict(self, row: sqlite3.Row) -> Dict:
        """将数据库行转换为字典"""
        return {
            'id': row['id'],
            'episode_type': row['episode_type'],
            'context_summary': row['context_summary'],
            'conclusion': row['conclusion'],
            'content': json.loads(row['content']),
            'related_topics': json.loads(row['related_topics']) if row['related_topics'] else [],
            'participants': json.loads(row['participants']) if row['participants'] else [],
            'priority': row['priority'],
            'access_count': row['access_count'],
            'compression_level': row['compression_level'],
            'timestamp': datetime.fromisoformat(row['created_at']),
            'last_accessed': datetime.fromisoformat(row['last_accessed'])
        }
    
    def update_episode_access(self, episode_id: str):
        """更新记忆访问时间"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE episodic_memory 
            SET access_count = access_count + 1, 
                last_accessed = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (episode_id,))
        self.conn.commit()
    
    def delete_episodic_memory(self, episode_id: str) -> bool:
        """删除情景记忆"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM episodic_memory WHERE id = ?", (episode_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_high_forgetting_risk_memories(self, threshold: float = 0.8) -> List[str]:
        """获取高遗忘风险的记忆ID"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id FROM episodic_memory 
            WHERE forgetting_score > ? AND priority < 5
        """, (threshold,))
        return [row['id'] for row in cursor.fetchall()]
    
    # ========== 用户记忆 CRUD ==========
    
    def save_user_memory(self, user_id: str, key: str, value: Any, **metadata) -> bool:
        """保存用户记忆"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO user_memory (
                id, user_id, key, value, value_type, priority,
                confidence, source, verification_count, is_outdated,
                last_accessed
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            f"{user_id}_{key}",
            user_id,
            key,
            json.dumps(value, ensure_ascii=False),
            metadata.get('value_type', type(value).__name__),
            metadata.get('priority', 3),
            metadata.get('confidence', 1.0),
            metadata.get('source', 'explicit'),
            metadata.get('verification_count', 0),
            metadata.get('is_outdated', False)
        ))
        
        self.conn.commit()
        return True
    
    def load_user_memory(self, user_id: str, key: Optional[str] = None) -> Union[Dict, List[Dict]]:
        """加载用户记忆"""
        cursor = self.conn.cursor()
        
        if key:
            cursor.execute("""
                SELECT * FROM user_memory WHERE user_id = ? AND key = ? AND is_outdated = 0
            """, (user_id, key))
            row = cursor.fetchone()
            return self._row_to_user_dict(row) if row else None
        else:
            cursor.execute("""
                SELECT * FROM user_memory WHERE user_id = ? AND is_outdated = 0
                ORDER BY priority DESC, last_accessed DESC
            """, (user_id,))
            return [self._row_to_user_dict(row) for row in cursor.fetchall()]
    
    def _row_to_user_dict(self, row: sqlite3.Row) -> Dict:
        """转换用户记忆行"""
        return {
            'id': row['id'],
            'user_id': row['user_id'],
            'key': row['key'],
            'value': json.loads(row['value']),
            'priority': row['priority'],
            'confidence': row['confidence'],
            'source': row['source'],
            'verification_count': row['verification_count'],
            'created_at': row['created_at'],
            'last_accessed': row['last_accessed']
        }
    
    # ========== 触发器 CRUD ==========
    
    def save_trigger(self, trigger: 'MemoryTrigger') -> bool:
        """保存触发器"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO memory_triggers (
                id, keywords, target_memory_ids, trigger_count, is_active
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            trigger.id,
            json.dumps(trigger.keywords, ensure_ascii=False),
            json.dumps(trigger.target_memory_ids, ensure_ascii=False),
            trigger.trigger_count,
            trigger.is_active
        ))
        
        self.conn.commit()
        return True
    
    def load_triggers(self) -> List[Dict]:
        """加载所有活跃触发器"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM memory_triggers WHERE is_active = 1
        """)
        
        triggers = []
        for row in cursor.fetchall():
            triggers.append({
                'id': row['id'],
                'keywords': json.loads(row['keywords']),
                'target_memory_ids': json.loads(row['target_memory_ids']),
                'trigger_count': row['trigger_count']
            })
        return triggers
    
    def increment_trigger_count(self, trigger_id: str):
        """增加触发器计数"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE memory_triggers 
            SET trigger_count = trigger_count + 1 
            WHERE id = ?
        """, (trigger_id,))
        self.conn.commit()
    
    # ========== 统计和维护 ==========
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆统计信息"""
        cursor = self.conn.cursor()
        
        stats = {}
        
        # 各表计数
        for table in ['episodic_memory', 'user_memory', 'memory_triggers', 'task_memory']:
            cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            stats[table] = cursor.fetchone()['count']
        
        # 平均遗忘分数
        cursor.execute("""
            SELECT AVG(forgetting_score) as avg_score 
            FROM episodic_memory
        """)
        result = cursor.fetchone()
        stats['avg_forgetting_score'] = result['avg_score'] if result else 0
        
        # 高风险记忆数
        cursor.execute("""
            SELECT COUNT(*) as count FROM episodic_memory 
            WHERE forgetting_score > 0.8
        """)
        stats['high_risk_memories'] = cursor.fetchone()['count']
        
        return stats
    
    def cleanup_old_memories(self, days: int = 30, priority_threshold: int = 2):
        """清理旧记忆（低优先级且长时间未访问）"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            DELETE FROM episodic_memory 
            WHERE priority <= ? 
            AND last_accessed < datetime('now', '-{} days')
        """.format(days), (priority_threshold,))
        
        deleted = cursor.rowcount
        self.conn.commit()
        return deleted
    
    def vacuum(self):
        """优化数据库空间"""
        self.conn.execute("VACUUM")


class JSONBackend:
    """
    JSON 文件后端（轻量级，适合单机部署）
    """
    
    def __init__(self, data_dir: str = "~/.memcore/data"):
        self.data_dir = os.path.expanduser(data_dir)
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _get_file_path(self, category: str) -> str:
        return os.path.join(self.data_dir, f"{category}.json")
    
    def save(self, category: str, data: Dict):
        """保存数据到 JSON"""
        filepath = self._get_file_path(category)
        
        # 读取现有数据
        existing = {}
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                existing = json.load(f)
        
        # 更新
        existing.update(data)
        
        # 写回
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=2, default=str)
    
    def load(self, category: str) -> Dict:
        """从 JSON 读取数据"""
        filepath = self._get_file_path(category)
        
        if not os.path.exists(filepath):
            return {}
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def delete(self, category: str, key: str):
        """删除数据"""
        filepath = self._get_file_path(category)
        
        if not os.path.exists(filepath):
            return
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if key in data:
            del data[key]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)


# 测试代码
if __name__ == "__main__":
    print("🧠 测试 Persistent Backend...")
    
    # 测试 SQLite 后端
    backend = SQLiteBackend(db_path="~/.memcore/test.db")
    
    # 测试统计
    stats = backend.get_memory_stats()
    print(f"📊 当前统计: {stats}")
    
    print("✅ 后端测试完成!")
