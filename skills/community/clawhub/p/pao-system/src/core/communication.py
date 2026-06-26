"""
Communication Module - 通信模块

提供设备间的消息传递功能
"""

import asyncio
import json
import logging
from typing import Dict, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class MessageType(str, Enum):
    """消息类型"""
    TEXT = "text"
    SYNC = "sync"
    COMMAND = "command"
    RESPONSE = "response"
    HEARTBEAT = "heartbeat"


@dataclass
class Message:
    """消息"""
    msg_id: str
    msg_type: MessageType
    sender: str
    receiver: str
    content: Any
    timestamp: float


class Communication:
    """
    通信管理器

    负责设备间的消息发送和接收
    """

    def __init__(self, device_id: str, config=None):
        self.device_id = device_id
        self.config = config
        self.connections: Dict[str, asyncio.StreamWriter] = {}
        self.message_handlers: Dict[MessageType, Callable] = {}
        self._running = False
        self._heartbeat_task: Optional[asyncio.Task] = None

    async def connect_to(self, peer_id: str, host: str = "localhost", port: int = 8765) -> bool:
        """
        连接到对等节点

        Args:
            peer_id: 对等节点ID
            host: 主机地址
            port: 端口

        Returns:
            bool: 连接是否成功
        """
        try:
            reader, writer = await asyncio.open_connection(host, port)
            self.connections[peer_id] = writer
            logger.info(f"已连接到 {peer_id}")
            return True
        except Exception as e:
            logger.error(f"连接失败: {e}")
            return False

    async def disconnect(self):
        """断开所有连接"""
        self._running = False

        for peer_id, writer in self.connections.items():
            writer.close()
            await writer.wait_closed()

        self.connections.clear()
        logger.info("已断开所有连接")

    async def disconnect_peer(self, peer_id: str):
        """断开指定对等节点的连接"""
        if peer_id in self.connections:
            writer = self.connections[peer_id]
            writer.close()
            await writer.wait_closed()
            del self.connections[peer_id]
            logger.info(f"已断开与 {peer_id} 的连接")

    async def send_message(self, peer_id: str, content: Any,
                          msg_type: MessageType = MessageType.TEXT) -> bool:
        """
        发送消息

        Args:
            peer_id: 对等节点ID
            content: 消息内容
            msg_type: 消息类型

        Returns:
            bool: 发送是否成功
        """
        if peer_id not in self.connections:
            logger.warning(f"未连接到 {peer_id}")
            return False

        try:
            message = Message(
                msg_id=f"{self.device_id}_{asyncio.get_event_loop().time()}",
                msg_type=msg_type,
                sender=self.device_id,
                receiver=peer_id,
                content=content,
                timestamp=asyncio.get_event_loop().time()
            )

            data = json.dumps({
                "msg_id": message.msg_id,
                "msg_type": message.msg_type.value,
                "sender": message.sender,
                "receiver": message.receiver,
                "content": message.content,
                "timestamp": message.timestamp
            })

            writer = self.connections[peer_id]
            writer.write(data.encode())
            await writer.drain()
            return True

        except Exception as e:
            logger.error(f"发送消息失败: {e}")
            return False

    def register_handler(self, msg_type: MessageType, handler: Callable):
        """注册消息处理器"""
        self.message_handlers[msg_type] = handler

    async def start_heartbeat(self, interval: int = 30):
        """启动心跳"""
        self._running = True

        async def heartbeat():
            while self._running:
                await asyncio.sleep(interval)
                for peer_id in self.connections:
                    await self.send_message(peer_id, {}, MessageType.HEARTBEAT)

        self._heartbeat_task = asyncio.create_task(heartbeat())

    def get_connected_peers(self) -> list:
        """获取已连接的节点列表"""
        return list(self.connections.keys())

    def is_connected(self, peer_id: str) -> bool:
        """检查是否连接到指定节点"""
        return peer_id in self.connections
