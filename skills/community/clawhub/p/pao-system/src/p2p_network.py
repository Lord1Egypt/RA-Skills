"""
P2P Network Module - P2P网络优化模块

提供连接池管理、断线重连、消息队列等功能
"""

import asyncio
import logging
import time
from typing import Dict, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import uuid

logger = logging.getLogger(__name__)


class ConnectionState(Enum):
    """连接状态"""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    RECONNECTING = "reconnecting"
    FAILED = "failed"


@dataclass
class ConnectionInfo:
    """连接信息"""
    peer_id: str
    peer_name: str
    state: ConnectionState = ConnectionState.DISCONNECTED
    connected_at: float = 0
    last_heartbeat: float = 0
    reconnect_attempts: int = 0
    max_reconnect_attempts: int = 5
    latency_ms: float = 0


@dataclass
class Message:
    """消息结构"""
    msg_id: str
    msg_type: str
    payload: dict
    created_at: float = field(default_factory=time.time)
    retry_count: int = 0
    max_retries: int = 3


class ConnectionPool:
    """连接池管理器"""
    
    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.connections: Dict[str, ConnectionInfo] = {}
        self.connection_lock = asyncio.Lock()
        self._callbacks: Dict[str, callable] = {}
        
    async def add_connection(self, peer_id: str, peer_name: str) -> ConnectionInfo:
        """添加新连接"""
        async with self.connection_lock:
            if peer_id in self.connections:
                return self.connections[peer_id]
            
            if len(self.connections) >= self.max_connections:
                # 移除最老的连接
                oldest = min(
                    self.connections.values(),
                    key=lambda x: x.connected_at
                )
                await self.remove_connection(oldest.peer_id)
            
            conn_info = ConnectionInfo(
                peer_id=peer_id,
                peer_name=peer_name,
                state=ConnectionState.CONNECTING,
                connected_at=time.time()
            )
            self.connections[peer_id] = conn_info
            logger.info(f"添加连接到池: {peer_id}")
            return conn_info
    
    async def update_state(self, peer_id: str, state: ConnectionState) -> None:
        """更新连接状态"""
        async with self.connection_lock:
            if peer_id in self.connections:
                self.connections[peer_id].state = state
                if state == ConnectionState.CONNECTED:
                    self.connections[peer_id].connected_at = time.time()
                    self.connections[peer_id].reconnect_attempts = 0
    
    async def remove_connection(self, peer_id: str) -> None:
        """移除连接"""
        async with self.connection_lock:
            if peer_id in self.connections:
                del self.connections[peer_id]
                logger.info(f"从池中移除连接: {peer_id}")
    
    async def get_connection(self, peer_id: str) -> Optional[ConnectionInfo]:
        """获取连接信息"""
        return self.connections.get(peer_id)
    
    async def get_all_connections(self) -> Dict[str, ConnectionInfo]:
        """获取所有连接"""
        return self.connections.copy()
    
    def register_callback(self, event: str, callback: callable) -> None:
        """注册状态变化回调"""
        self._callbacks[event] = callback
    
    async def trigger_callback(self, event: str, *args, **kwargs) -> None:
        """触发回调"""
        if event in self._callbacks:
            try:
                await self._callbacks[event](*args, **kwargs)
            except Exception as e:
                logger.error(f"回调执行失败: {e}")


class ReconnectionManager:
    """断线重连管理器"""
    
    def __init__(self, base_delay: float = 1.0, max_delay: float = 60.0):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self._reconnect_tasks: Dict[str, asyncio.Task] = {}
        self._running = False
    
    def calculate_delay(self, attempt: int) -> float:
        """计算重连延迟（指数退避）"""
        delay = min(self.base_delay * (2 ** attempt), self.max_delay)
        # 添加随机抖动
        import random
        return delay * (0.5 + random.random() * 0.5)
    
    async def start_reconnect(
        self,
        peer_id: str,
        connect_func: callable,
        max_attempts: int = 5
    ) -> bool:
        """启动重连"""
        if peer_id in self._reconnect_tasks:
            logger.warning(f"重连任务已存在: {peer_id}")
            return False
        
        self._running = True
        task = asyncio.create_task(
            self._reconnect_loop(peer_id, connect_func, max_attempts)
        )
        self._reconnect_tasks[peer_id] = task
        return True
    
    async def stop_reconnect(self, peer_id: str) -> None:
        """停止重连"""
        if peer_id in self._reconnect_tasks:
            self._reconnect_tasks[peer_id].cancel()
            del self._reconnect_tasks[peer_id]
            logger.info(f"停止重连任务: {peer_id}")
    
    async def _reconnect_loop(
        self,
        peer_id: str,
        connect_func: callable,
        max_attempts: int
    ) -> None:
        """重连循环"""
        attempt = 0
        while attempt < max_attempts and self._running:
            delay = self.calculate_delay(attempt)
            logger.info(f"等待 {delay:.1f}秒后重连 {peer_id} (尝试 {attempt + 1}/{max_attempts})")
            
            await asyncio.sleep(delay)
            
            try:
                success = await connect_func(peer_id)
                if success:
                    logger.info(f"重连成功: {peer_id}")
                    return
            except Exception as e:
                logger.error(f"重连失败: {peer_id}, {e}")
            
            attempt += 1
        
        logger.warning(f"重连次数耗尽: {peer_id}")
    
    def stop_all(self) -> None:
        """停止所有重连任务"""
        self._running = False
        for task in self._reconnect_tasks.values():
            task.cancel()
        self._reconnect_tasks.clear()


class MessageQueue:
    """消息队列"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._queue: deque = deque(maxlen=max_size)
        self._pending: Dict[str, Message] = {}
        self._lock = asyncio.Lock()
        self._callbacks: Dict[str, callable] = {}
    
    async def enqueue(self, msg_type: str, payload: dict) -> str:
        """入队消息"""
        async with self._lock:
            msg_id = str(uuid.uuid4())
            msg = Message(msg_id=msg_id, msg_type=msg_type, payload=payload)
            self._queue.append(msg)
            self._pending[msg_id] = msg
            logger.debug(f"消息入队: {msg_id}, 类型: {msg_type}")
            return msg_id
    
    async def dequeue(self) -> Optional[Message]:
        """出队消息"""
        async with self._lock:
            if self._queue:
                msg = self._queue.popleft()
                return msg
            return None
    
    async def get_pending(self, msg_id: str) -> Optional[Message]:
        """获取待确认消息"""
        return self._pending.get(msg_id)
    
    async def confirm(self, msg_id: str) -> bool:
        """确认消息已送达"""
        async with self._lock:
            if msg_id in self._pending:
                del self._pending[msg_id]
                logger.debug(f"消息已确认: {msg_id}")
                return True
            return False
    
    async def retry(self, msg_id: str) -> bool:
        """重试消息"""
        async with self._lock:
            if msg_id in self._pending:
                msg = self._pending[msg_id]
                if msg.retry_count < msg.max_retries:
                    msg.retry_count += 1
                    self._queue.append(msg)
                    logger.info(f"消息重试: {msg_id}, 次数: {msg.retry_count}")
                    return True
                else:
                    del self._pending[msg_id]
                    logger.warning(f"消息重试次数耗尽: {msg_id}")
            return False
    
    async def size(self) -> int:
        """获取队列大小"""
        return len(self._queue)
    
    async def pending_count(self) -> int:
        """获取待确认消息数"""
        return len(self._pending)


class P2PNetworkManager:
    """P2P网络管理器（整合模块）"""
    
    def __init__(self):
        self.connection_pool = ConnectionPool()
        self.reconnect_manager = ReconnectionManager()
        self.message_queue = MessageQueue()
        self._running = False
        
    async def start(self) -> None:
        """启动P2P网络"""
        self._running = True
        logger.info("P2P网络管理器已启动")
    
    async def stop(self) -> None:
        """停止P2P网络"""
        self._running = False
        self.reconnect_manager.stop_all()
        logger.info("P2P网络管理器已停止")
    
    async def connect(self, peer_id: str, peer_name: str) -> bool:
        """连接到对等节点"""
        conn_info = await self.connection_pool.add_connection(peer_id, peer_name)
        
        try:
            # 模拟连接建立
            await asyncio.sleep(0.1)
            await self.connection_pool.update_state(peer_id, ConnectionState.CONNECTED)
            conn_info.last_heartbeat = time.time()
            logger.info(f"已连接到: {peer_id}")
            return True
        except Exception as e:
            logger.error(f"连接失败: {peer_id}, {e}")
            await self.connection_pool.update_state(peer_id, ConnectionState.FAILED)
            return False
    
    async def disconnect(self, peer_id: str) -> None:
        """断开连接"""
        self.reconnect_manager.stop_reconnect(peer_id)
        await self.connection_pool.remove_connection(peer_id)
        logger.info(f"已断开: {peer_id}")
    
    async def send_message(self, peer_id: str, msg_type: str, payload: dict) -> Optional[str]:
        """发送消息"""
        conn_info = await self.connection_pool.get_connection(peer_id)
        if not conn_info or conn_info.state != ConnectionState.CONNECTED:
            # 消息入队等待发送
            return await self.message_queue.enqueue(msg_type, payload)
        
        msg_id = await self.message_queue.enqueue(msg_type, payload)
        # 模拟发送
        await asyncio.sleep(0.01)
        await self.message_queue.confirm(msg_id)
        return msg_id
    
    async def get_status(self) -> dict:
        """获取网络状态"""
        connections = await self.connection_pool.get_all_connections()
        return {
            "running": self._running,
            "connections": {
                peer_id: {
                    "state": conn.state.value,
                    "latency_ms": conn.latency_ms,
                    "last_heartbeat": conn.last_heartbeat
                }
                for peer_id, conn in connections.items()
            },
            "queue_size": await self.message_queue.size(),
            "pending_messages": await self.message_queue.pending_count()
        }
