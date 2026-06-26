"""
本地记忆系统
实现 AI 记忆的存储、检索和管理
"""

import json
import time
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict, field
from pathlib import Path

import aiofiles
from pydantic import BaseModel, Field


class MemoryType(str, Enum):
    """记忆类型"""
    CONVERSATION = "conversation"      # 对话记忆
    KNOWLEDGE = "knowledge"            # 知识记忆
    TASK = "task"                      # 任务记忆
    PREFERENCE = "preference"          # 偏好记忆
    CONTEXT = "context"                # 上下文记忆
    SYSTEM = "system"                  # 系统记忆


class MemoryPriority(int, Enum):
    """记忆优先级"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class MemoryMetadata:
    """记忆元数据"""
    source: str = ""                    # 来源（设备ID或用户ID）
    confidence: float = 1.0             # 置信度（0.0-1.0）
    access_count: int = 0               # 访问次数
    last_accessed: float = 0.0          # 最后访问时间戳
    created_at: float = field(default_factory=time.time)  # 创建时间戳
    tags: List[str] = field(default_factory=list)         # 标签
    expires_at: Optional[float] = None  # 过期时间戳（None表示永不过期）


class MemoryItem(BaseModel):
    """记忆项"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: MemoryType
    content: Dict[str, Any]
    priority: MemoryPriority = MemoryPriority.MEDIUM
    metadata: MemoryMetadata = Field(default_factory=MemoryMetadata)
    
    # 时间戳
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)
    
    # 关联信息
    related_memories: List[str] = Field(default_factory=list)  # 关联记忆ID
    device_id: Optional[str] = None  # 创建此记忆的设备ID
    
    class Config:
        use_enum_values = True


class MemoryQuery(BaseModel):
    """记忆查询条件"""
    
    type: Optional[MemoryType] = None
    content_key: Optional[str] = None
    content_value: Optional[Any] = None
    min_priority: Optional[MemoryPriority] = None
    tags: Optional[List[str]] = None
    source: Optional[str] = None
    device_id: Optional[str] = None
    created_after: Optional[float] = None
    created_before: Optional[float] = None
    limit: int = 100
    offset: int = 0


class MemorySystem:
    """记忆系统"""
    
    def __init__(self, storage_path: Optional[Path] = None):
        """
        初始化记忆系统
        
        Args:
            storage_path: 存储路径，如果为None则使用默认路径
        """
        if storage_path is None:
            storage_path = Path.home() / ".pao" / "memories"
        
        self.storage_path = Path(storage_path)
        self.memories: Dict[str, MemoryItem] = {}
        
        # 创建存储目录
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # 索引
        self.type_index: Dict[MemoryType, List[str]] = {}
        self.tag_index: Dict[str, List[str]] = {}
        self.device_index: Dict[str, List[str]] = {}
        
    async def load(self) -> None:
        """从存储加载所有记忆"""
        try:
            memory_files = list(self.storage_path.glob("*.json"))
            
            for file_path in memory_files:
                try:
                    async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                        content = await f.read()
                    
                    data = json.loads(content)
                    memory = MemoryItem(**data)
                    
                    # 添加到内存
                    self.memories[memory.id] = memory
                    
                    # 更新索引
                    self._add_to_indices(memory)
                    
                except Exception as e:
                    print(f"加载记忆文件 {file_path} 失败: {e}")
        
        except Exception as e:
            print(f"加载记忆系统失败: {e}")
    
    async def save(self, memory: MemoryItem) -> None:
        """
        保存记忆
        
        Args:
            memory: 要保存的记忆
        """
        try:
            # 更新时间戳
            memory.updated_at = time.time()
            
            # 保存到内存
            self.memories[memory.id] = memory
            
            # 更新索引
            self._add_to_indices(memory)
            
            # 保存到文件
            file_path = self.storage_path / f"{memory.id}.json"
            
            async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
                await f.write(memory.model_dump_json(indent=2))

            # 更新访问统计
            memory.metadata.access_count += 1
            memory.metadata.last_accessed = time.time()
            
        except Exception as e:
            print(f"保存记忆失败: {e}")
            raise
    
    async def get(self, memory_id: str) -> Optional[MemoryItem]:
        """
        获取记忆
        
        Args:
            memory_id: 记忆ID
            
        Returns:
            记忆项，如果不存在则返回None
        """
        memory = self.memories.get(memory_id)
        
        if memory:
            # 更新访问统计
            memory.metadata.access_count += 1
            memory.metadata.last_accessed = time.time()
            
            # 异步保存更新
            asyncio.create_task(self._update_memory_file(memory))
        
        return memory
    
    async def query(self, query: MemoryQuery) -> List[MemoryItem]:
        """
        查询记忆
        
        Args:
            query: 查询条件
            
        Returns:
            匹配的记忆列表
        """
        results = []
        
        for memory in self.memories.values():
            if self._matches_query(memory, query):
                results.append(memory)
        
        # 按创建时间排序（最新的在前面）
        results.sort(key=lambda m: m.created_at, reverse=True)
        
        # 应用分页
        start = query.offset
        end = start + query.limit
        return results[start:end]
    
    async def delete(self, memory_id: str) -> bool:
        """
        删除记忆
        
        Args:
            memory_id: 记忆ID
            
        Returns:
            是否成功删除
        """
        try:
            memory = self.memories.get(memory_id)
            if not memory:
                return False
            
            # 从内存中删除
            del self.memories[memory_id]
            
            # 从索引中删除
            self._remove_from_indices(memory)
            
            # 删除文件
            file_path = self.storage_path / f"{memory_id}.json"
            if file_path.exists():
                file_path.unlink()
            
            return True
        
        except Exception as e:
            print(f"删除记忆失败: {e}")
            return False
    
    async def update(self, memory_id: str, updates: Dict[str, Any]) -> Optional[MemoryItem]:
        """
        更新记忆
        
        Args:
            memory_id: 记忆ID
            updates: 更新字段
            
        Returns:
            更新后的记忆，如果不存在则返回None
        """
        memory = await self.get(memory_id)
        if not memory:
            return None
        
        # 应用更新
        for key, value in updates.items():
            if hasattr(memory, key):
                setattr(memory, key, value)
        
        memory.updated_at = time.time()
        
        # 保存更新
        await self.save(memory)
        
        return memory
    
    async def cleanup_expired(self) -> int:
        """
        清理过期记忆
        
        Returns:
            清理的记忆数量
        """
        current_time = time.time()
        expired_ids = []
        
        for memory_id, memory in self.memories.items():
            if memory.metadata.expires_at and memory.metadata.expires_at < current_time:
                expired_ids.append(memory_id)
        
        # 删除过期记忆
        deleted_count = 0
        for memory_id in expired_ids:
            if await self.delete(memory_id):
                deleted_count += 1
        
        return deleted_count
    
    def get_stats(self) -> Dict[str, Any]:
        """
        获取统计信息
        
        Returns:
            统计信息字典
        """
        return {
            "total_memories": len(self.memories),
            "by_type": {
                type_.value: len(memories) 
                for type_, memories in self.type_index.items()
            },
            "by_device": {
                device_id: len(memories)
                for device_id, memories in self.device_index.items()
            },
            "oldest_memory": min(
                [m.created_at for m in self.memories.values()] or [0]
            ),
            "newest_memory": max(
                [m.created_at for m in self.memories.values()] or [0]
            )
        }

    async def add_memory(self, memory_type: str, content: Any, priority: int = 2) -> str:
        """添加记忆"""
        mem_type = MemoryType.CONVERSATION
        for mt in MemoryType:
            if mt.value == memory_type:
                mem_type = mt
                break
        # 确保priority是有效的枚举值
        valid_priority = max(1, min(4, priority))
        memory = MemoryItem(
            id=str(uuid.uuid4()),
            type=mem_type,
            content=content,
            priority=valid_priority,
            metadata=MemoryMetadata()
        )
        await self.save(memory)
        return memory.id

    async def search_memories(self, query: str, limit: int = 10) -> list:
        """搜索记忆"""
        memory_query = MemoryQuery(keyword=query, limit=limit)
        results = await self.query(memory_query)
        return [m.content for m in results]

    def _add_to_indices(self, memory: MemoryItem) -> None:
        """添加到索引"""
        # 类型索引
        if memory.type not in self.type_index:
            self.type_index[memory.type] = []
        if memory.id not in self.type_index[memory.type]:
            self.type_index[memory.type].append(memory.id)
        
        # 标签索引
        for tag in memory.metadata.tags:
            if tag not in self.tag_index:
                self.tag_index[tag] = []
            if memory.id not in self.tag_index[tag]:
                self.tag_index[tag].append(memory.id)
        
        # 设备索引
        if memory.device_id:
            if memory.device_id not in self.device_index:
                self.device_index[memory.device_id] = []
            if memory.id not in self.device_index[memory.device_id]:
                self.device_index[memory.device_id].append(memory.id)
    
    def _remove_from_indices(self, memory: MemoryItem) -> None:
        """从索引中删除"""
        # 类型索引
        if memory.type in self.type_index:
            if memory.id in self.type_index[memory.type]:
                self.type_index[memory.type].remove(memory.id)
        
        # 标签索引
        for tag in memory.metadata.tags:
            if tag in self.tag_index and memory.id in self.tag_index[tag]:
                self.tag_index[tag].remove(memory.id)
        
        # 设备索引
        if memory.device_id and memory.device_id in self.device_index:
            if memory.id in self.device_index[memory.device_id]:
                self.device_index[memory.device_id].remove(memory.id)
    
    def _matches_query(self, memory: MemoryItem, query: MemoryQuery) -> bool:
        """检查记忆是否匹配查询条件"""
        if query.type and memory.type != query.type:
            return False
        
        if query.content_key and query.content_value:
            if query.content_key not in memory.content:
                return False
            if memory.content[query.content_key] != query.content_value:
                return False
        
        if query.min_priority and memory.priority.value < query.min_priority.value:
            return False
        
        if query.tags:
            if not all(tag in memory.metadata.tags for tag in query.tags):
                return False
        
        if query.source and memory.metadata.source != query.source:
            return False
        
        if query.device_id and memory.device_id != query.device_id:
            return False
        
        if query.created_after and memory.created_at < query.created_after:
            return False
        
        if query.created_before and memory.created_at > query.created_before:
            return False
        
        return True
    
    async def _update_memory_file(self, memory: MemoryItem) -> None:
        """异步更新记忆文件"""
        try:
            file_path = self.storage_path / f"{memory.id}.json"
            async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
                await f.write(memory.model_dump_json(indent=2))
        except Exception as e:
            print(f"异步更新记忆文件失败: {e}")


import asyncio