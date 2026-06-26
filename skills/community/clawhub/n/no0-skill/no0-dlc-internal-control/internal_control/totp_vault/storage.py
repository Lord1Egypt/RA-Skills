"""
TOTP Vault - 存储层实现
"""
import os
import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from .models import TOTPKey, KeyStatus


class VaultStorage(ABC):
    """Vault 存储抽象基类"""
    
    @abstractmethod
    def store_metadata(self, key: TOTPKey) -> None:
        """存储密钥元数据"""
        pass
    
    @abstractmethod
    def get_metadata(self, key_id: str) -> Optional[TOTPKey]:
        """获取密钥元数据"""
        pass
    
    @abstractmethod
    def list_all_metadata(self) -> List[TOTPKey]:
        """列出所有元数据"""
        pass
    
    @abstractmethod
    def update_usage(self, key_id: str, timestamp: datetime) -> None:
        """更新使用记录"""
        pass
    
    @abstractmethod
    def mark_rotated(self, key_id: str, grace_period_hours: int) -> None:
        """标记密钥已轮换"""
        pass
    
    @abstractmethod
    def delete(self, key_id: str) -> None:
        """删除密钥"""
        pass


class SQLiteStorage(VaultStorage):
    """
    SQLite 元数据存储
    
    实际密钥仍存储在系统钥匙串
    元数据（key_id, context, created_at等）存储在 SQLite
    """
    
    def __init__(self, db_path: str = "~/.openclaw/totp_vault.db"):
        self.db_path = os.path.expanduser(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS totp_keys (
                key_id TEXT PRIMARY KEY,
                context TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used TIMESTAMP,
                use_count INTEGER DEFAULT 0,
                algorithm TEXT DEFAULT 'SHA1',
                digits INTEGER DEFAULT 6,
                interval INTEGER DEFAULT 30,
                status TEXT DEFAULT 'active',
                grace_period_until TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS key_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_id TEXT NOT NULL,
                action TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                details TEXT
            )
        ''')
        
        # 创建索引
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_context_status 
            ON totp_keys(context, status)
        ''')
        
        conn.commit()
        conn.close()
    
    def store_metadata(self, key: TOTPKey) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO totp_keys 
            (key_id, context, created_at, algorithm, digits, interval, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (key.key_id, key.context, key.created_at, 
              key.algorithm, key.digits, key.interval, key.status.value))
        
        conn.commit()
        conn.close()
    
    def get_metadata(self, key_id: str) -> Optional[TOTPKey]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT key_id, context, created_at, last_used, use_count,
                   algorithm, digits, interval, status, grace_period_until
            FROM totp_keys WHERE key_id = ?
        ''', (key_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return TOTPKey(
                key_id=row[0],
                context=row[1],
                created_at=datetime.fromisoformat(row[2]) if isinstance(row[2], str) else row[2],
                last_used=datetime.fromisoformat(row[3]) if row[3] and isinstance(row[3], str) else row[3],
                use_count=row[4] or 0,
                algorithm=row[5],
                digits=row[6],
                interval=row[7],
                status=KeyStatus(row[8]),
                grace_period_until=datetime.fromisoformat(row[9]) if row[9] and isinstance(row[9], str) else None
            )
        return None
    
    def list_all_metadata(self) -> List[TOTPKey]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT key_id, context, created_at, last_used, use_count,
                   algorithm, digits, interval, status, grace_period_until
            FROM totp_keys
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        keys = []
        for row in rows:
            keys.append(TOTPKey(
                key_id=row[0],
                context=row[1],
                created_at=datetime.fromisoformat(row[2]) if isinstance(row[2], str) else row[2],
                last_used=datetime.fromisoformat(row[3]) if row[3] and isinstance(row[3], str) else row[3],
                use_count=row[4] or 0,
                algorithm=row[5],
                digits=row[6],
                interval=row[7],
                status=KeyStatus(row[8]),
                grace_period_until=datetime.fromisoformat(row[9]) if row[9] and isinstance(row[9], str) else None
            ))
        return keys
    
    def update_usage(self, key_id: str, timestamp: datetime) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE totp_keys 
            SET last_used = ?, use_count = use_count + 1
            WHERE key_id = ?
        ''', (timestamp, key_id))
        
        # 记录历史
        cursor.execute('''
            INSERT INTO key_history (key_id, action, details)
            VALUES (?, 'used', ?)
        ''', (key_id, f"Used at {timestamp.isoformat()}"))
        
        conn.commit()
        conn.close()
    
    def mark_rotated(self, key_id: str, grace_period_hours: int) -> None:
        from datetime import timedelta
        grace_until = datetime.now() + timedelta(hours=grace_period_hours)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE totp_keys 
            SET status = 'rotating', grace_period_until = ?
            WHERE key_id = ?
        ''', (grace_until, key_id))
        
        cursor.execute('''
            INSERT INTO key_history (key_id, action, details)
            VALUES (?, 'rotated', ?)
        ''', (key_id, f"Grace period until {grace_until.isoformat()}"))
        
        conn.commit()
        conn.close()
    
    def delete(self, key_id: str) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM totp_keys WHERE key_id = ?', (key_id,))
        
        cursor.execute('''
            INSERT INTO key_history (key_id, action, details)
            VALUES (?, 'deleted', 'Key revoked')
        ''', (key_id,))
        
        conn.commit()
        conn.close()
    
    def get_key_by_context(self, context: str) -> Optional[TOTPKey]:
        """根据上下文获取密钥（用于查找已有密钥）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT key_id, context, created_at, last_used, use_count,
                   algorithm, digits, interval, status, grace_period_until
            FROM totp_keys 
            WHERE context = ? AND status IN ('active', 'rotating')
            ORDER BY created_at DESC
            LIMIT 1
        ''', (context,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return TOTPKey(
                key_id=row[0],
                context=row[1],
                created_at=datetime.fromisoformat(row[2]) if isinstance(row[2], str) else row[2],
                last_used=datetime.fromisoformat(row[3]) if row[3] and isinstance(row[3], str) else row[3],
                use_count=row[4] or 0,
                algorithm=row[5],
                digits=row[6],
                interval=row[7],
                status=KeyStatus(row[8]),
                grace_period_until=datetime.fromisoformat(row[9]) if row[9] and isinstance(row[9], str) else None
            )
        return None