"""
数据存储系统
提供统一的存储接口，支持多种存储后端
"""

import json
import sqlite3
import aiofiles
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple
from enum import Enum
import asyncio
from dataclasses import dataclass, asdict
from datetime import datetime
import time


class StorageType(str, Enum):
    """存储类型"""
    SQLITE = "sqlite"
    JSON_FILE = "json"
    MEMORY = "memory"


@dataclass
class StorageConfig:
    """存储配置"""
    
    type: StorageType = StorageType.SQLITE
    path: Optional[Path] = None
    table_name: str = "memories"
    max_connections: int = 5
    auto_commit: bool = True


class StorageBackend:
    """存储后端基类"""
    
    async def connect(self) -> None:
        """连接到存储"""
        pass
    
    async def disconnect(self) -> None:
        """断开连接"""
        pass
    
    async def save(self, key: str, data: Dict[str, Any]) -> bool:
        """保存数据"""
        raise NotImplementedError
    
    async def load(self, key: str) -> Optional[Dict[str, Any]]:
        """加载数据"""
        raise NotImplementedError
    
    async def delete(self, key: str) -> bool:
        """删除数据"""
        raise NotImplementedError
    
    async def query(self, conditions: Dict[str, Any], limit: int = 100) -> List[Dict[str, Any]]:
        """查询数据"""
        raise NotImplementedError
    
    async def exists(self, key: str) -> bool:
        """检查数据是否存在"""
        raise NotImplementedError
    
    async def list_keys(self, prefix: str = "") -> List[str]:
        """列出所有键"""
        raise NotImplementedError


class SQLiteBackend(StorageBackend):
    """SQLite 存储后端"""
    
    def __init__(self, config: StorageConfig):
        self.config = config
        self.connection: Optional[sqlite3.Connection] = None
        
        # 确保路径存在
        if self.config.path:
            path = self.config.path if isinstance(self.config.path, Path) else Path(self.config.path)
            path.parent.mkdir(parents=True, exist_ok=True)
    
    async def connect(self) -> None:
        """连接到 SQLite 数据库"""
        if self.config.path is None:
            raise ValueError("SQLite 存储需要指定路径")
        
        # SQLite 连接是同步的，但我们在异步环境中使用
        self.connection = sqlite3.connect(
            str(self.config.path),
            check_same_thread=False
        )
        
        # 启用外键和 WAL 模式
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.execute("PRAGMA journal_mode = WAL")
        
        # 创建表
        await self._create_tables()
    
    async def disconnect(self) -> None:
        """断开连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    async def save(self, key: str, data: Dict[str, Any]) -> bool:
        """保存数据到 SQLite"""
        if not self.connection:
            await self.connect()
        
        try:
            # 序列化数据
            data_json = json.dumps(data, ensure_ascii=False)
            
            # 插入或更新
            cursor = self.connection.execute(
                f"""
                INSERT OR REPLACE INTO {self.config.table_name} 
                (key, data, created_at, updated_at) 
                VALUES (?, ?, ?, ?)
                """,
                (key, data_json, time.time(), time.time())
            )
            
            if self.config.auto_commit:
                self.connection.commit()
            
            return cursor.rowcount > 0
        
        except Exception as e:
            print(f"SQLite 保存失败: {e}")
            return False
    
    async def load(self, key: str) -> Optional[Dict[str, Any]]:
        """从 SQLite 加载数据"""
        if not self.connection:
            await self.connect()
        
        try:
            cursor = self.connection.execute(
                f"SELECT data FROM {self.config.table_name} WHERE key = ?",
                (key,)
            )
            
            row = cursor.fetchone()
            if row:
                return json.loads(row[0])
            
            return None
        
        except Exception as e:
            print(f"SQLite 加载失败: {e}")
            return None
    
    async def delete(self, key: str) -> bool:
        """从 SQLite 删除数据"""
        if not self.connection:
            await self.connect()
        
        try:
            cursor = self.connection.execute(
                f"DELETE FROM {self.config.table_name} WHERE key = ?",
                (key,)
            )
            
            if self.config.auto_commit:
                self.connection.commit()
            
            return cursor.rowcount > 0
        
        except Exception as e:
            print(f"SQLite 删除失败: {e}")
            return False
    
    async def query(self, conditions: Dict[str, Any], limit: int = 100) -> List[Dict[str, Any]]:
        """查询 SQLite 数据"""
        if not self.connection:
            await self.connect()
        
        try:
            # 构建查询条件
            where_clauses = []
            params = []
            
            for key, value in conditions.items():
                where_clauses.append(f"json_extract(data, '$.{key}') = ?")
                params.append(value)
            
            where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
            
            # 执行查询
            cursor = self.connection.execute(
                f"""
                SELECT data FROM {self.config.table_name} 
                WHERE {where_sql} 
                ORDER BY updated_at DESC 
                LIMIT ?
                """,
                (*params, limit)
            )
            
            results = []
            for row in cursor.fetchall():
                results.append(json.loads(row[0]))
            
            return results
        
        except Exception as e:
            print(f"SQLite 查询失败: {e}")
            return []
    
    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        if not self.connection:
            await self.connect()
        
        try:
            cursor = self.connection.execute(
                f"SELECT 1 FROM {self.config.table_name} WHERE key = ?",
                (key,)
            )
            
            return cursor.fetchone() is not None
        
        except Exception as e:
            print(f"SQLite 检查存在失败: {e}")
            return False
    
    async def list_keys(self, prefix: str = "") -> List[str]:
        """列出所有键"""
        if not self.connection:
            await self.connect()
        
        try:
            if prefix:
                cursor = self.connection.execute(
                    f"SELECT key FROM {self.config.table_name} WHERE key LIKE ?",
                    (f"{prefix}%",)
                )
            else:
                cursor = self.connection.execute(
                    f"SELECT key FROM {self.config.table_name}"
                )
            
            return [row[0] for row in cursor.fetchall()]
        
        except Exception as e:
            print(f"SQLite 列出键失败: {e}")
            return []
    
    async def _create_tables(self) -> None:
        """创建数据库表"""
        if not self.connection:
            return
        
        self.connection.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.config.table_name} (
                key TEXT PRIMARY KEY,
                data TEXT NOT NULL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL
            )
        """)
        
        # 创建索引
        self.connection.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_updated_at 
            ON {self.config.table_name} (updated_at)
        """)
        
        self.connection.commit()


class JSONFileBackend(StorageBackend):
    """JSON 文件存储后端"""
    
    def __init__(self, config: StorageConfig):
        self.config = config
        self.data: Dict[str, Dict[str, Any]] = {}
        
        # 确保路径存在
        if self.config.path:
            path = self.config.path if isinstance(self.config.path, Path) else Path(self.config.path)
            path.parent.mkdir(parents=True, exist_ok=True)
    
    async def connect(self) -> None:
        """连接到 JSON 文件存储"""
        if self.config.path and self.config.path.exists():
            await self._load_from_file()
    
    async def disconnect(self) -> None:
        """断开连接并保存到文件"""
        if self.config.path:
            await self._save_to_file()
    
    async def save(self, key: str, data: Dict[str, Any]) -> bool:
        """保存数据到 JSON 文件"""
        try:
            # 添加时间戳
            if "created_at" not in data:
                data["created_at"] = time.time()
            data["updated_at"] = time.time()
            
            # 保存到内存
            self.data[key] = data
            
            # 异步保存到文件
            asyncio.create_task(self._save_to_file())
            
            return True
        
        except Exception as e:
            print(f"JSON 文件保存失败: {e}")
            return False
    
    async def load(self, key: str) -> Optional[Dict[str, Any]]:
        """从 JSON 文件加载数据"""
        return self.data.get(key)
    
    async def delete(self, key: str) -> bool:
        """从 JSON 文件删除数据"""
        try:
            if key in self.data:
                del self.data[key]
                
                # 异步保存到文件
                asyncio.create_task(self._save_to_file())
                
                return True
            
            return False
        
        except Exception as e:
            print(f"JSON 文件删除失败: {e}")
            return False
    
    async def query(self, conditions: Dict[str, Any], limit: int = 100) -> List[Dict[str, Any]]:
        """查询 JSON 文件数据"""
        results = []
        
        for item in self.data.values():
            match = True
            
            for key, value in conditions.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            
            if match:
                results.append(item)
        
        # 按更新时间排序
        results.sort(key=lambda x: x.get("updated_at", 0), reverse=True)
        
        return results[:limit]
    
    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        return key in self.data
    
    async def list_keys(self, prefix: str = "") -> List[str]:
        """列出所有键"""
        if prefix:
            return [key for key in self.data.keys() if key.startswith(prefix)]
        
        return list(self.data.keys())
    
    async def _load_from_file(self) -> None:
        """从文件加载数据"""
        if not self.config.path or not self.config.path.exists():
            return
        
        try:
            async with aiofiles.open(self.config.path, "r", encoding="utf-8") as f:
                content = await f.read()
                self.data = json.loads(content)
        
        except Exception as e:
            print(f"加载 JSON 文件失败: {e}")
            self.data = {}
    
    async def _save_to_file(self) -> None:
        """保存数据到文件"""
        if not self.config.path:
            return
        
        try:
            async with aiofiles.open(self.config.path, "w", encoding="utf-8") as f:
                await f.write(json.dumps(self.data, indent=2, ensure_ascii=False))
        
        except Exception as e:
            print(f"保存 JSON 文件失败: {e}")


class MemoryBackend(StorageBackend):
    """内存存储后端（用于测试）"""
    
    def __init__(self, config: StorageConfig):
        self.config = config
        self.data: Dict[str, Dict[str, Any]] = {}
    
    async def save(self, key: str, data: Dict[str, Any]) -> bool:
        """保存数据到内存"""
        try:
            if "created_at" not in data:
                data["created_at"] = time.time()
            data["updated_at"] = time.time()
            
            self.data[key] = data
            return True
        
        except Exception as e:
            print(f"内存保存失败: {e}")
            return False
    
    async def load(self, key: str) -> Optional[Dict[str, Any]]:
        """从内存加载数据"""
        return self.data.get(key)
    
    async def delete(self, key: str) -> bool:
        """从内存删除数据"""
        try:
            if key in self.data:
                del self.data[key]
                return True
            
            return False
        
        except Exception as e:
            print(f"内存删除失败: {e}")
            return False
    
    async def query(self, conditions: Dict[str, Any], limit: int = 100) -> List[Dict[str, Any]]:
        """查询内存数据"""
        results = []
        
        for item in self.data.values():
            match = True
            
            for key, value in conditions.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            
            if match:
                results.append(item)
        
        # 按更新时间排序
        results.sort(key=lambda x: x.get("updated_at", 0), reverse=True)
        
        return results[:limit]
    
    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        return key in self.data
    
    async def list_keys(self, prefix: str = "") -> List[str]:
        """列出所有键"""
        if prefix:
            return [key for key in self.data.keys() if key.startswith(prefix)]
        
        return list(self.data.keys())


class StorageManager:
    """存储管理器"""
    
    def __init__(self, config: Optional[StorageConfig] = None):
        self.config = config or StorageConfig()
        self.backend: Optional[StorageBackend] = None
        
    async def initialize(self) -> None:
        """初始化存储"""
        # 根据配置创建后端
        if self.config.type == StorageType.SQLITE:
            self.backend = SQLiteBackend(self.config)
        
        elif self.config.type == StorageType.JSON_FILE:
            self.backend = JSONFileBackend(self.config)
        
        elif self.config.type == StorageType.MEMORY:
            self.backend = MemoryBackend(self.config)
        
        else:
            raise ValueError(f"不支持的存储类型: {self.config.type}")
        
        # 连接后端
        await self.backend.connect()
    
    async def close(self) -> None:
        """关闭存储"""
        if self.backend:
            await self.backend.disconnect()
    
    async def save(self, key: str, data: Dict[str, Any]) -> bool:
        """保存数据"""
        if not self.backend:
            await self.initialize()
        
        return await self.backend.save(key, data)
    
    async def load(self, key: str) -> Optional[Dict[str, Any]]:
        """加载数据"""
        if not self.backend:
            await self.initialize()
        
        return await self.backend.load(key)
    
    async def delete(self, key: str) -> bool:
        """删除数据"""
        if not self.backend:
            await self.initialize()
        
        return await self.backend.delete(key)
    
    async def query(self, conditions: Dict[str, Any], limit: int = 100) -> List[Dict[str, Any]]:
        """查询数据"""
        if not self.backend:
            await self.initialize()
        
        return await self.backend.query(conditions, limit)
    
    async def exists(self, key: str) -> bool:
        """检查数据是否存在"""
        if not self.backend:
            await self.initialize()
        
        return await self.backend.exists(key)
    
    async def list_keys(self, prefix: str = "") -> List[str]:
        """列出所有键"""
        if not self.backend:
            await self.initialize()
        
        return await self.backend.list_keys(prefix)
    
    async def migrate_data(self, source_backend: StorageBackend, target_backend: StorageBackend) -> int:
        """
        迁移数据
        
        Args:
            source_backend: 源存储后端
            target_backend: 目标存储后端
            
        Returns:
            迁移的数据数量
        """
        migrated_count = 0
        
        try:
            # 获取所有键
            keys = await source_backend.list_keys()
            
            for key in keys:
                # 加载数据
                data = await source_backend.load(key)
                if data:
                    # 保存到目标
                    if await target_backend.save(key, data):
                        migrated_count += 1
            
            return migrated_count
        
        except Exception as e:
            print(f"数据迁移失败: {e}")
            return migrated_count