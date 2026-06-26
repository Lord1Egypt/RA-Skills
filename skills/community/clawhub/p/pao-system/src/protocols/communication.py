"""
基础通信协议
定义 PAO 系统设备间的通信协议和消息格式
"""

import json
import uuid
import asyncio
import logging
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional, Union, List, Callable
from dataclasses import dataclass, field, asdict

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class MessageType(str, Enum):
    """消息类型枚举"""
    # 控制消息
    HELLO = "hello"               # 连接问候
    PING = "ping"                 # 心跳检测
    PONG = "pong"                 # 心跳响应
    ACK = "ack"                   # 确认响应
    ERROR = "error"               # 错误消息
    
    # 设备管理
    DEVICE_INFO = "device_info"   # 设备信息
    DEVICE_STATE = "device_state" # 设备状态
    DEVICE_LIST = "device_list"   # 设备列表
    
    # 数据同步
    SYNC_REQUEST = "sync_request" # 同步请求
    SYNC_DATA = "sync_data"       # 同步数据
    SYNC_COMPLETE = "sync_complete" # 同步完成
    
    # 记忆系统
    MEMORY_QUERY = "memory_query" # 记忆查询
    MEMORY_RESPONSE = "memory_response" # 记忆响应
    MEMORY_UPDATE = "memory_update" # 记忆更新
    
    # 技能管理
    SKILL_REQUEST = "skill_request" # 技能请求
    SKILL_RESPONSE = "skill_response" # 技能响应
    SKILL_UPDATE = "skill_update" # 技能更新
    
    # 文件传输
    FILE_INFO = "file_info"       # 文件信息
    FILE_CHUNK = "file_chunk"     # 文件分块
    FILE_COMPLETE = "file_complete" # 文件传输完成


class MessagePriority(int, Enum):
    """消息优先级"""
    LOW = 0          # 低优先级，可延迟
    NORMAL = 1       # 正常优先级
    HIGH = 2         # 高优先级
    CRITICAL = 3     # 关键优先级，立即处理


@dataclass
class MessageHeader:
    """消息头"""
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    message_type: MessageType = MessageType.HELLO
    priority: MessagePriority = MessagePriority.NORMAL
    source_device: str = ""  # 发送设备ID
    target_device: str = ""  # 目标设备ID，为空表示广播
    timestamp: datetime = field(default_factory=datetime.now)
    ttl: int = 300  # 消息生存时间（秒）
    requires_ack: bool = False
    correlation_id: Optional[str] = None  # 关联ID，用于请求-响应匹配
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "message_id": self.message_id,
            "message_type": self.message_type.value,
            "priority": self.priority.value,
            "source_device": self.source_device,
            "target_device": self.target_device,
            "timestamp": self.timestamp.isoformat(),
            "ttl": self.ttl,
            "requires_ack": self.requires_ack,
            "correlation_id": self.correlation_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MessageHeader":
        """从字典创建"""
        header = cls()
        header.message_id = data.get("message_id", header.message_id)
        header.message_type = MessageType(data.get("message_type", MessageType.HELLO.value))
        header.priority = MessagePriority(data.get("priority", MessagePriority.NORMAL.value))
        header.source_device = data.get("source_device", header.source_device)
        header.target_device = data.get("target_device", header.target_device)
        header.ttl = data.get("ttl", header.ttl)
        header.requires_ack = data.get("requires_ack", header.requires_ack)
        header.correlation_id = data.get("correlation_id", header.correlation_id)
        
        # 解析时间戳
        if "timestamp" in data:
            header.timestamp = datetime.fromisoformat(data["timestamp"])
        
        return header


class Message(BaseModel):
    """消息基类"""
    header: MessageHeader
    payload: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            MessageType: lambda v: v.value,
            MessagePriority: lambda v: v.value
        }
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return self.json()
    
    @classmethod
    def from_json(cls, json_str: str) -> "Message":
        """从JSON字符串创建"""
        data = json.loads(json_str)
        return cls(
            header=MessageHeader.from_dict(data["header"]),
            payload=data.get("payload", {})
        )
    
    def is_expired(self) -> bool:
        """检查消息是否过期"""
        now = datetime.now()
        age = (now - self.header.timestamp).total_seconds()
        return age > self.header.ttl
    
    def create_response(self, message_type: MessageType, payload: Dict[str, Any] = None) -> "Message":
        """创建响应消息"""
        if payload is None:
            payload = {}
        
        # 创建响应头
        response_header = MessageHeader(
            message_type=message_type,
            source_device=self.header.target_device,  # 交换源和目标
            target_device=self.header.source_device,
            correlation_id=self.header.message_id  # 关联原始消息
        )
        
        return Message(header=response_header, payload=payload)
    
    def create_ack(self) -> "Message":
        """创建确认消息"""
        return self.create_response(MessageType.ACK, {
            "original_message_id": self.header.message_id,
            "status": "received"
        })


class ProtocolError(Exception):
    """协议错误"""
    pass


class MessageSerializer:
    """消息序列化器"""
    
    @staticmethod
    def serialize(message: Message) -> bytes:
        """序列化消息为字节"""
        try:
            json_str = message.to_json()
            # 添加消息长度前缀
            data = json_str.encode('utf-8')
            length = len(data).to_bytes(4, 'big')
            return length + data
        except Exception as e:
            logger.error(f"序列化消息失败: {e}")
            raise ProtocolError(f"序列化失败: {e}")
    
    @staticmethod
    def deserialize(data: bytes) -> Message:
        """从字节反序列化消息"""
        try:
            # 解析消息长度
            if len(data) < 4:
                raise ProtocolError("数据长度不足")
            
            length = int.from_bytes(data[:4], 'big')
            if len(data) < 4 + length:
                raise ProtocolError("数据不完整")
            
            # 解析JSON
            json_str = data[4:4+length].decode('utf-8')
            return Message.from_json(json_str)
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}")
            raise ProtocolError(f"JSON解析失败: {e}")
        except Exception as e:
            logger.error(f"反序列化消息失败: {e}")
            raise ProtocolError(f"反序列化失败: {e}")


class Connection:
    """连接抽象类"""
    
    def __init__(self, connection_id: str):
        self.connection_id = connection_id
        self.is_connected = False
        self.last_activity = datetime.now()
        self.message_handlers: Dict[MessageType, List[Callable]] = {}
        self.ack_callbacks: Dict[str, Callable] = {}
    
    async def connect(self) -> bool:
        """建立连接"""
        raise NotImplementedError
    
    async def disconnect(self) -> None:
        """断开连接"""
        raise NotImplementedError
    
    async def send_message(self, message: Message) -> bool:
        """发送消息"""
        raise NotImplementedError
    
    async def receive_message(self) -> Optional[Message]:
        """接收消息"""
        raise NotImplementedError
    
    def register_handler(self, message_type: MessageType, handler: Callable) -> None:
        """注册消息处理器"""
        if message_type not in self.message_handlers:
            self.message_handlers[message_type] = []
        self.message_handlers[message_type].append(handler)
    
    def unregister_handler(self, message_type: MessageType, handler: Callable) -> None:
        """注销消息处理器"""
        if message_type in self.message_handlers:
            self.message_handlers[message_type].remove(handler)
    
    async def handle_message(self, message: Message) -> None:
        """处理消息"""
        # 检查消息是否过期
        if message.is_expired():
            logger.warning(f"消息已过期: {message.header.message_id}")
            return
        
        # 更新活动时间
        self.last_activity = datetime.now()
        
        # 查找消息处理器
        handlers = self.message_handlers.get(message.header.message_type, [])
        
        if not handlers:
            logger.debug(f"没有注册的消息处理器: {message.header.message_type}")
            return
        
        # 调用所有处理器
        for handler in handlers:
            try:
                await handler(message, self)
            except Exception as e:
                logger.error(f"消息处理器出错: {e}")
    
    async def send_with_ack(self, message: Message, timeout: int = 10) -> Optional[Message]:
        """发送消息并等待确认"""
        if not message.header.requires_ack:
            message.header.requires_ack = True
        
        # 创建等待事件
        ack_event = asyncio.Event()
        ack_response = None
        
        def ack_callback(response_message: Message):
            nonlocal ack_response
            ack_response = response_message
            ack_event.set()
        
        # 注册ACK回调
        self.ack_callbacks[message.header.message_id] = ack_callback
        
        try:
            # 发送消息
            success = await self.send_message(message)
            if not success:
                return None
            
            # 等待ACK
            try:
                await asyncio.wait_for(ack_event.wait(), timeout=timeout)
                return ack_response
            except asyncio.TimeoutError:
                logger.warning(f"等待ACK超时: {message.header.message_id}")
                return None
                
        finally:
            # 清理回调
            self.ack_callbacks.pop(message.header.message_id, None)


class MessageFactory:
    """消息工厂类"""
    
    def __init__(self, source_device_id: str):
        self.source_device_id = source_device_id
    
    def create_hello_message(self, device_info: Dict[str, Any]) -> Message:
        """创建设备问候消息"""
        header = MessageHeader(
            message_type=MessageType.HELLO,
            source_device=self.source_device_id,
            requires_ack=True
        )
        return Message(header=header, payload={"device_info": device_info})
    
    def create_ping_message(self) -> Message:
        """创建心跳消息"""
        header = MessageHeader(
            message_type=MessageType.PING,
            source_device=self.source_device_id,
            priority=MessagePriority.LOW
        )
        return Message(header=header, payload={"timestamp": datetime.now().isoformat()})
    
    def create_device_info_message(self, device_info: Dict[str, Any], target_device: str = "") -> Message:
        """创建设备信息消息"""
        header = MessageHeader(
            message_type=MessageType.DEVICE_INFO,
            source_device=self.source_device_id,
            target_device=target_device
        )
        return Message(header=header, payload={"device_info": device_info})
    
    def create_sync_request_message(self, sync_type: str, target_device: str = "") -> Message:
        """创建同步请求消息"""
        header = MessageHeader(
            message_type=MessageType.SYNC_REQUEST,
            source_device=self.source_device_id,
            target_device=target_device,
            requires_ack=True
        )
        return Message(header=header, payload={"sync_type": sync_type})
    
    def create_memory_query_message(self, query: Dict[str, Any], target_device: str = "") -> Message:
        """创建记忆查询消息"""
        header = MessageHeader(
            message_type=MessageType.MEMORY_QUERY,
            source_device=self.source_device_id,
            target_device=target_device,
            requires_ack=True
        )
        return Message(header=header, payload={"query": query})
    
    def create_error_message(self, error_code: str, error_message: str, 
                           original_message_id: str = "") -> Message:
        """创建错误消息"""
        header = MessageHeader(
            message_type=MessageType.ERROR,
            source_device=self.source_device_id,
            priority=MessagePriority.HIGH
        )
        payload = {
            "error_code": error_code,
            "error_message": error_message
        }
        if original_message_id:
            payload["original_message_id"] = original_message_id
        
        return Message(header=header, payload=payload)


# 预定义的消息处理器
async def handle_ping_message(message: Message, connection: Connection) -> None:
    """处理心跳消息"""
    # 创建PONG响应
    pong_message = message.create_response(MessageType.PONG, {
        "original_timestamp": message.payload.get("timestamp"),
        "response_timestamp": datetime.now().isoformat()
    })
    await connection.send_message(pong_message)


async def handle_hello_message(message: Message, connection: Connection) -> None:
    """处理问候消息"""
    logger.info(f"收到问候消息来自: {message.header.source_device}")
    # 发送ACK
    ack_message = message.create_ack()
    await connection.send_message(ack_message)


async def handle_ack_message(message: Message, connection: Connection) -> None:
    """处理确认消息"""
    correlation_id = message.header.correlation_id
    if correlation_id and hasattr(connection, 'ack_callbacks'):
        callback = connection.ack_callbacks.get(correlation_id)
        if callback:
            callback(message)


def create_default_message_handlers(connection: Connection) -> None:
    """创建默认消息处理器"""
    connection.register_handler(MessageType.PING, handle_ping_message)
    connection.register_handler(MessageType.HELLO, handle_hello_message)
    connection.register_handler(MessageType.ACK, handle_ack_message)


if __name__ == "__main__":
    # 测试消息序列化
    factory = MessageFactory("test-device-001")
    hello_msg = factory.create_hello_message({"name": "Test Device"})
    
    print("原始消息:", hello_msg.dict())
    
    # 序列化测试
    serializer = MessageSerializer()
    serialized = serializer.serialize(hello_msg)
    print(f"序列化大小: {len(serialized)} 字节")
    
    # 反序列化测试
    deserialized = serializer.deserialize(serialized)
    print("反序列化消息:", deserialized.dict())
    
    # 测试消息过期
    import time
    time.sleep(1)
    print("消息是否过期:", hello_msg.is_expired())