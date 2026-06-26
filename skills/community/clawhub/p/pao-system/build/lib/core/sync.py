"""
记忆同步系统
实现跨设备的记忆同步和冲突解决
"""

import json
import time
import hashlib
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import asyncio
from datetime import datetime, timedelta

from .memory import MemorySystem, MemoryItem, MemoryQuery, MemoryType
from .device import DeviceInfo


class SyncStatus(str, Enum):
    """同步状态"""
    PENDING = "pending"        # 等待同步
    SYNCING = "syncing"        # 同步中
    COMPLETED = "completed"    # 同步完成
    FAILED = "failed"          # 同步失败
    CONFLICT = "conflict"      # 冲突需要解决


class SyncDirection(str, Enum):
    """同步方向"""
    PUSH = "push"              # 推送（本地→远程）
    PULL = "pull"              # 拉取（远程→本地）
    BIDIRECTIONAL = "bidirectional"  # 双向同步


class SyncStrategy(str, Enum):
    """同步策略"""
    LAST_WRITE_WINS = "last_write_wins"    # 最后写入获胜
    MANUAL_MERGE = "manual_merge"          # 手动合并
    AUTO_MERGE = "auto_merge"              # 自动合并
    SOURCE_PRIORITY = "source_priority"    # 源设备优先


@dataclass
class SyncOperation:
    """同步操作"""
    
    id: str
    memory_id: str
    device_id: str
    direction: SyncDirection
    status: SyncStatus = SyncStatus.PENDING
    timestamp: float = field(default_factory=time.time)
    retry_count: int = 0
    error_message: Optional[str] = None
    
    # 冲突相关
    conflict_resolution: Optional[Dict[str, Any]] = None
    merged_memory_id: Optional[str] = None


@dataclass
class SyncSession:
    """同步会话"""
    
    id: str
    source_device_id: str
    target_device_id: str
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    status: SyncStatus = SyncStatus.PENDING
    strategy: SyncStrategy = SyncStrategy.LAST_WRITE_WINS
    
    # 同步统计
    total_memories: int = 0
    synced_memories: int = 0
    failed_memories: int = 0
    conflict_memories: int = 0
    
    # 操作列表
    operations: List[SyncOperation] = field(default_factory=list)


class ConflictResolver:
    """冲突解决器"""
    
    @staticmethod
    def resolve_last_write_wins(local_memory: MemoryItem, remote_memory: MemoryItem) -> MemoryItem:
        """最后写入获胜策略"""
        if local_memory.updated_at > remote_memory.updated_at:
            return local_memory
        else:
            return remote_memory
    
    @staticmethod
    def resolve_source_priority(local_memory: MemoryItem, remote_memory: MemoryItem, source_device_id: str) -> MemoryItem:
        """源设备优先策略"""
        if local_memory.device_id == source_device_id:
            return local_memory
        elif remote_memory.device_id == source_device_id:
            return remote_memory
        else:
            # 回退到最后写入获胜
            return ConflictResolver.resolve_last_write_wins(local_memory, remote_memory)
    
    @staticmethod
    def auto_merge(local_memory: MemoryItem, remote_memory: MemoryItem) -> MemoryItem:
        """自动合并策略"""
        # 创建合并后的记忆
        merged = MemoryItem(
            id=local_memory.id,
            type=local_memory.type,
            content=local_memory.content.copy(),
            priority=max(local_memory.priority, remote_memory.priority),
            metadata=local_memory.metadata,
            device_id=local_memory.device_id,  # 保持本地设备ID
            related_memories=list(set(local_memory.related_memories + remote_memory.related_memories))
        )
        
        # 合并内容（简单合并策略）
        for key, value in remote_memory.content.items():
            if key not in merged.content:
                merged.content[key] = value
            elif isinstance(value, dict) and isinstance(merged.content[key], dict):
                # 递归合并字典
                merged.content[key] = {**merged.content[key], **value}
            elif isinstance(value, list) and isinstance(merged.content[key], list):
                # 合并列表（去重）
                merged.content[key] = list(set(merged.content[key] + value))
        
        # 合并元数据
        merged.metadata.access_count = max(
            local_memory.metadata.access_count,
            remote_memory.metadata.access_count
        )
        merged.metadata.last_accessed = max(
            local_memory.metadata.last_accessed,
            remote_memory.metadata.last_accessed
        )
        
        # 合并标签
        merged.metadata.tags = list(set(local_memory.metadata.tags + remote_memory.metadata.tags))
        
        # 更新最后访问时间
        merged.metadata.last_accessed = time.time()
        merged.updated_at = time.time()
        
        return merged
    
    @staticmethod
    def detect_conflict(local_memory: MemoryItem, remote_memory: MemoryItem) -> bool:
        """检测冲突"""
        if local_memory.type != remote_memory.type:
            return True
        
        # 检查内容是否相同
        if local_memory.content != remote_memory.content:
            return True
        
        # 检查优先级是否相同
        if local_memory.priority != remote_memory.priority:
            return True
        
        return False


class SyncEngine:
    """同步引擎"""
    
    def __init__(self, memory_system: MemorySystem, local_device_id: str):
        self.memory_system = memory_system
        self.local_device_id = local_device_id
        
        # 同步会话管理
        self.sessions: Dict[str, SyncSession] = {}
        self.pending_operations: Dict[str, SyncOperation] = {}
        
        # 同步配置
        self.sync_interval: int = 300  # 同步间隔（秒）
        self.max_retries: int = 3
        self.batch_size: int = 50
        
        # 设备连接管理
        self.connected_devices: Dict[str, DeviceInfo] = {}
        
        # 运行状态
        self.is_running = False
        self.sync_task: Optional[asyncio.Task] = None
    
    async def start(self) -> None:
        """启动同步引擎"""
        if self.is_running:
            return
        
        self.is_running = True
        
        # 启动定期同步任务
        self.sync_task = asyncio.create_task(self._periodic_sync())
    
    async def stop(self) -> None:
        """停止同步引擎"""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # 取消同步任务
        if self.sync_task:
            self.sync_task.cancel()
            try:
                await self.sync_task
            except asyncio.CancelledError:
                pass
        
        # 等待所有同步会话完成
        await self._wait_for_sessions()
    
    async def sync_with_device(self, device_id: str, strategy: SyncStrategy = SyncStrategy.LAST_WRITE_WINS) -> SyncSession:
        """
        与指定设备同步
        
        Args:
            device_id: 设备ID
            strategy: 同步策略
            
        Returns:
            同步会话
        """
        if device_id not in self.connected_devices:
            raise ValueError(f"设备未连接: {device_id}")
        
        # 创建同步会话
        session_id = hashlib.md5(f"{self.local_device_id}_{device_id}_{time.time()}".encode()).hexdigest()[:12]
        session = SyncSession(
            id=session_id,
            source_device_id=self.local_device_id,
            target_device_id=device_id,
            strategy=strategy
        )
        
        self.sessions[session_id] = session
        
        # 开始同步
        asyncio.create_task(self._execute_sync_session(session))
        
        return session
    
    async def get_sync_status(self, session_id: str) -> Optional[SyncSession]:
        """获取同步状态"""
        return self.sessions.get(session_id)
    
    async def list_sync_sessions(self, device_id: Optional[str] = None) -> List[SyncSession]:
        """列出同步会话"""
        if device_id:
            return [
                session for session in self.sessions.values()
                if session.source_device_id == device_id or session.target_device_id == device_id
            ]
        
        return list(self.sessions.values())
    
    async def add_device(self, device: DeviceInfo) -> None:
        """添加设备"""
        self.connected_devices[device.device_id] = device
    
    async def remove_device(self, device_id: str) -> None:
        """移除设备"""
        if device_id in self.connected_devices:
            del self.connected_devices[device_id]
    
    async def _execute_sync_session(self, session: SyncSession) -> None:
        """执行同步会话"""
        session.status = SyncStatus.SYNCING
        
        try:
            # 获取需要同步的记忆
            local_memories = await self._get_memories_for_sync(session.target_device_id)
            session.total_memories = len(local_memories)
            
            # 分批同步
            for i in range(0, len(local_memories), self.batch_size):
                batch = local_memories[i:i + self.batch_size]
                
                # 同步批次
                await self._sync_batch(session, batch)
                
                # 更新进度
                session.synced_memories = min(session.total_memories, i + self.batch_size)
                
                # 短暂休眠，避免过载
                await asyncio.sleep(0.1)
            
            # 标记完成
            session.status = SyncStatus.COMPLETED
            session.end_time = time.time()
            
        except Exception as e:
            session.status = SyncStatus.FAILED
            session.end_time = time.time()
            print(f"同步会话失败: {e}")
    
    async def _sync_batch(self, session: SyncSession, memories: List[MemoryItem]) -> None:
        """同步一批记忆"""
        for memory in memories:
            try:
                # 创建同步操作
                operation = SyncOperation(
                    id=hashlib.md5(f"{memory.id}_{session.id}".encode()).hexdigest()[:8],
                    memory_id=memory.id,
                    device_id=session.target_device_id,
                    direction=SyncDirection.BIDIRECTIONAL
                )
                
                # 执行同步
                success = await self._sync_single_memory(session, memory, operation)
                
                if success:
                    operation.status = SyncStatus.COMPLETED
                    session.synced_memories += 1
                else:
                    operation.status = SyncStatus.FAILED
                    session.failed_memories += 1
                
                # 添加到会话
                session.operations.append(operation)
                
            except Exception as e:
                print(f"同步记忆失败 {memory.id}: {e}")
                session.failed_memories += 1
    
    async def _sync_single_memory(self, session: SyncSession, memory: MemoryItem, operation: SyncOperation) -> bool:
        """同步单个记忆"""
        try:
            # 这里应该调用远程设备的API来获取远程记忆
            # 由于第二阶段只实现本地同步，这里模拟远程记忆
            remote_memory = await self._simulate_remote_memory(memory, session.target_device_id)
            
            if not remote_memory:
                # 远程不存在，直接推送
                return await self._push_memory(memory, session.target_device_id)
            
            # 检测冲突
            if ConflictResolver.detect_conflict(memory, remote_memory):
                session.conflict_memories += 1
                operation.status = SyncStatus.CONFLICT
                
                # 根据策略解决冲突
                resolved_memory = await self._resolve_conflict(
                    memory, remote_memory, session.strategy, session.source_device_id
                )
                
                # 更新本地和远程
                await self.memory_system.save(resolved_memory)
                await self._push_memory(resolved_memory, session.target_device_id)
                
                operation.conflict_resolution = {"strategy": session.strategy.value}
                operation.merged_memory_id = resolved_memory.id
            
            else:
                # 无冲突，更新较新的版本
                if memory.updated_at > remote_memory.updated_at:
                    await self._push_memory(memory, session.target_device_id)
                else:
                    await self.memory_system.save(remote_memory)
            
            return True
        
        except Exception as e:
            operation.error_message = str(e)
            operation.retry_count += 1
            
            if operation.retry_count < self.max_retries:
                # 重试
                await asyncio.sleep(2 ** operation.retry_count)  # 指数退避
                return await self._sync_single_memory(session, memory, operation)
            
            return False
    
    async def _push_memory(self, memory: MemoryItem, target_device_id: str) -> bool:
        """推送记忆到远程设备"""
        # 第二阶段：模拟推送成功
        # 实际实现中应该通过WebSocket或HTTP API发送到远程设备
        print(f"推送记忆 {memory.id} 到设备 {target_device_id}")
        return True
    
    async def _pull_memory(self, memory_id: str, source_device_id: str) -> Optional[MemoryItem]:
        """从远程设备拉取记忆"""
        # 第二阶段：模拟拉取
        # 实际实现中应该通过WebSocket或HTTP API从远程设备获取
        print(f"从设备 {source_device_id} 拉取记忆 {memory_id}")
        
        # 模拟返回一个记忆
        return None
    
    async def _get_memories_for_sync(self, target_device_id: str) -> List[MemoryItem]:
        """获取需要同步的记忆"""
        # 查询所有需要同步到目标设备的记忆
        query = MemoryQuery(
            device_id=self.local_device_id,
            limit=1000
        )
        
        memories = await self.memory_system.query(query)
        
        # 过滤：只同步最近修改过的记忆
        recent_memories = [
            memory for memory in memories
            if memory.updated_at > time.time() - 86400  # 24小时内
        ]
        
        return recent_memories
    
    async def _simulate_remote_memory(self, memory: MemoryItem, device_id: str) -> Optional[MemoryItem]:
        """模拟远程记忆（用于测试）"""
        # 50%的概率返回模拟的远程记忆
        import random
        if random.random() > 0.5:
            return None
        
        # 创建模拟的远程记忆
        remote_memory = MemoryItem(
            id=memory.id,
            type=memory.type,
            content=memory.content.copy(),
            priority=memory.priority,
            metadata=memory.metadata,
            device_id=device_id,
            related_memories=memory.related_memories.copy()
        )
        
        # 稍微修改内容以模拟冲突
        if isinstance(remote_memory.content, dict) and len(remote_memory.content) > 0:
            first_key = list(remote_memory.content.keys())[0]
            if isinstance(remote_memory.content[first_key], str):
                remote_memory.content[first_key] += " (远程修改)"
        
        # 设置不同的更新时间（可能更旧或更新）
        remote_memory.updated_at = memory.updated_at + random.uniform(-3600, 3600)
        
        return remote_memory
    
    async def _resolve_conflict(self, local_memory: MemoryItem, remote_memory: MemoryItem, 
                               strategy: SyncStrategy, source_device_id: str) -> MemoryItem:
        """解决冲突"""
        if strategy == SyncStrategy.LAST_WRITE_WINS:
            return ConflictResolver.resolve_last_write_wins(local_memory, remote_memory)
        
        elif strategy == SyncStrategy.SOURCE_PRIORITY:
            return ConflictResolver.resolve_source_priority(local_memory, remote_memory, source_device_id)
        
        elif strategy == SyncStrategy.AUTO_MERGE:
            return ConflictResolver.auto_merge(local_memory, remote_memory)
        
        else:
            # 默认使用最后写入获胜
            return ConflictResolver.resolve_last_write_wins(local_memory, remote_memory)
    
    async def _periodic_sync(self) -> None:
        """定期同步"""
        while self.is_running:
            try:
                # 等待同步间隔
                await asyncio.sleep(self.sync_interval)
                
                # 与所有连接的设备同步
                for device_id in list(self.connected_devices.keys()):
                    try:
                        await self.sync_with_device(device_id)
                    except Exception as e:
                        print(f"与设备 {device_id} 定期同步失败: {e}")
            
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"定期同步任务出错: {e}")
                await asyncio.sleep(60)  # 出错后等待1分钟
    
    async def _wait_for_sessions(self, timeout: float = 30.0) -> None:
        """等待所有同步会话完成"""
        start_time = time.time()
        
        while self.sessions:
            # 检查超时
            if time.time() - start_time > timeout:
                print(f"等待同步会话超时，剩余 {len(self.sessions)} 个会话")
                break
            
            # 检查是否有活跃的会话
            active_sessions = [
                session for session in self.sessions.values()
                if session.status in [SyncStatus.PENDING, SyncStatus.SYNCING]
            ]
            
            if not active_sessions:
                break
            
            # 等待一段时间
            await asyncio.sleep(1)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取同步统计信息"""
        total_sessions = len(self.sessions)
        completed_sessions = len([s for s in self.sessions.values() if s.status == SyncStatus.COMPLETED])
        failed_sessions = len([s for s in self.sessions.values() if s.status == SyncStatus.FAILED])
        
        total_operations = 0
        completed_operations = 0
        failed_operations = 0
        conflict_operations = 0
        
        for session in self.sessions.values():
            total_operations += len(session.operations)
            completed_operations += len([op for op in session.operations if op.status == SyncStatus.COMPLETED])
            failed_operations += len([op for op in session.operations if op.status == SyncStatus.FAILED])
            conflict_operations += len([op for op in session.operations if op.status == SyncStatus.CONFLICT])
        
        return {
            "connected_devices": len(self.connected_devices),
            "total_sessions": total_sessions,
            "completed_sessions": completed_sessions,
            "failed_sessions": failed_sessions,
            "total_operations": total_operations,
            "completed_operations": completed_operations,
            "failed_operations": failed_operations,
            "conflict_operations": conflict_operations
        }