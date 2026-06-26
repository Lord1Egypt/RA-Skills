"""
WebSocket 客户端
实现 PAO 系统的 WebSocket 通信客户端
"""

import asyncio
import logging
import ssl
from typing import Dict, Any, Optional, Callable
from datetime import datetime

import websockets
from websockets.client import WebSocketClientProtocol
from websockets.exceptions import ConnectionClosed

from .communication import (
    Message, MessageSerializer, MessageType, Connection,
    create_default_message_handlers, MessageFactory, ProtocolError
)
from ..core.device import DeviceInfo

logger = logging.getLogger(__name__)


class WebSocketClientConnection(Connection):
    """WebSocket 客户端连接"""
    
    def __init__(self, connection_id: str, uri: str, device_info: Optional[DeviceInfo] = None):
        super().__init__(connection_id)
        self.uri = uri
        self.device_info = device_info
        self.websocket: Optional[WebSocketClientProtocol] = None
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 3
        self.reconnect_delay = 1  # 初始重连延迟（秒）
    
    async def connect(self) -> bool:
        """连接到WebSocket服务器"""
        if self.is_connected:
            logger.warning("连接已经建立")
            return True
        
        logger.info(f"连接到服务器: {self.uri}")
        
        try:
            # 建立WebSocket连接
            self.websocket = await websockets.connect(
                self.uri,
                ping_interval=30,
                ping_timeout=10,
                close_timeout=10
            )
            
            self.is_connected = True
            self.reconnect_attempts = 0
            self.reconnect_delay = 1
            
            logger.info(f"连接成功: {self.uri}")
            
            # 发送设备信息（如果有）
            if self.device_info:
                await self._send_device_info()
            
            return True
            
        except Exception as e:
            logger.error(f"连接失败: {e}")
            self.is_connected = False
            return False
    
    async def disconnect(self) -> None:
        """断开连接"""
        self.is_connected = False
        if self.websocket:
            try:
                await self.websocket.close()
            except Exception as e:
                logger.debug(f"关闭连接时出错: {e}")
        self.websocket = None
        logger.info(f"连接已断开: {self.uri}")
    
    async def _send_device_info(self) -> None:
        """发送设备信息"""
        if not self.device_info or not self.is_connected:
            return
        
        try:
            factory = MessageFactory(self.device_info.device_id)
            device_msg = factory.create_device_info_message(
                self.device_info.to_dict()
            )
            await self.send_message(device_msg)
            logger.info(f"设备信息已发送: {self.device_info.name}")
        except Exception as e:
            logger.error(f"发送设备信息失败: {e}")
    
    async def send_message(self, message: Message) -> bool:
        """发送消息"""
        if not self.is_connected or not self.websocket:
            logger.warning("连接未建立，无法发送消息")
            return False
        
        try:
            # 序列化消息
            data = MessageSerializer.serialize(message)
            
            # 发送消息
            await self.websocket.send(data)
            
            logger.debug(f"消息已发送: {message.header.message_type.value}")
            return True
            
        except ConnectionClosed:
            logger.warning("连接已关闭，无法发送消息")
            self.is_connected = False
            return False
        except Exception as e:
            logger.error(f"发送消息失败: {e}")
            return False
    
    async def receive_message(self) -> Optional[Message]:
        """接收消息"""
        if not self.is_connected or not self.websocket:
            return None
        
        try:
            # 接收消息
            data = await self.websocket.recv()
            
            # 反序列化消息
            message = MessageSerializer.deserialize(data)
            
            # 更新活动时间
            self.last_activity = datetime.now()
            
            logger.debug(f"消息已接收: {message.header.message_type.value}")
            return message
            
        except ConnectionClosed:
            logger.info("连接已关闭")
            self.is_connected = False
            return None
        except ProtocolError as e:
            logger.error(f"协议错误: {e}")
            return None
        except Exception as e:
            logger.error(f"接收消息失败: {e}")
            return None
    
    async def reconnect(self) -> bool:
        """重新连接"""
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            logger.error(f"达到最大重连次数: {self.max_reconnect_attempts}")
            return False
        
        self.reconnect_attempts += 1
        delay = self.reconnect_delay * (2 ** (self.reconnect_attempts - 1))  # 指数退避
        
        logger.info(f"尝试重连 ({self.reconnect_attempts}/{self.max_reconnect_attempts})，等待 {delay} 秒")
        
        try:
            await asyncio.sleep(delay)
            
            # 断开旧连接
            await self.disconnect()
            
            # 建立新连接
            success = await self.connect()
            
            if success:
                logger.info("重连成功")
                return True
            else:
                logger.warning("重连失败")
                return False
                
        except Exception as e:
            logger.error(f"重连过程中出错: {e}")
            return False
    
    async def keepalive(self, interval: int = 30) -> None:
        """保持连接活跃"""
        factory = MessageFactory(self.device_info.device_id if self.device_info else "unknown")
        
        while self.is_connected:
            try:
                await asyncio.sleep(interval)
                
                if self.is_connected:
                    # 发送心跳
                    ping_msg = factory.create_ping_message()
                    success = await self.send_message(ping_msg)
                    
                    if not success:
                        logger.warning("心跳发送失败，尝试重连")
                        await self.reconnect()
                        
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"保持活跃任务出错: {e}")


class WebSocketClient:
    """WebSocket 客户端管理器"""
    
    def __init__(
        self,
        device_info: DeviceInfo,
        on_message: Optional[Callable[[Message], None]] = None,
        on_connect: Optional[Callable[[], None]] = None,
        on_disconnect: Optional[Callable[[], None]] = None
    ):
        self.device_info = device_info
        self.connection: Optional[WebSocketClientConnection] = None
        
        # 回调函数
        self.on_message = on_message
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        
        # 任务管理
        self.message_task: Optional[asyncio.Task] = None
        self.keepalive_task: Optional[asyncio.Task] = None
        
        # 状态
        self.is_connected = False
        self.is_running = False
    
    async def connect(self, uri: str) -> bool:
        """连接到服务器"""
        if self.is_connected:
            logger.warning("客户端已经连接")
            return True
        
        logger.info(f"连接到服务器: {uri}")
        
        # 创建连接
        self.connection = WebSocketClientConnection(
            connection_id=f"client-{self.device_info.device_id[:8]}",
            uri=uri,
            device_info=self.device_info
        )
        
        # 注册默认消息处理器
        create_default_message_handlers(self.connection)
        
        # 注册自定义消息处理器
        if self.on_message:
            self.connection.register_handler(MessageType.HELLO, self._handle_message)
            self.connection.register_handler(MessageType.DEVICE_INFO, self._handle_message)
            self.connection.register_handler(MessageType.SYNC_REQUEST, self._handle_message)
            self.connection.register_handler(MessageType.MEMORY_QUERY, self._handle_message)
        
        # 建立连接
        success = await self.connection.connect()
        if not success:
            logger.error("连接失败")
            return False
        
        self.is_connected = True
        self.is_running = True
        
        # 启动消息处理任务
        self.message_task = asyncio.create_task(self._message_loop())
        
        # 启动保持活跃任务
        self.keepalive_task = asyncio.create_task(self.connection.keepalive())
        
        # 连接成功回调
        if self.on_connect:
            try:
                self.on_connect()
            except Exception as e:
                logger.error(f"连接回调出错: {e}")
        
        logger.info("客户端连接成功")
        return True
    
    async def disconnect(self) -> None:
        """断开连接"""
        if not self.is_connected:
            return
        
        logger.info("断开客户端连接")
        
        self.is_running = False
        self.is_connected = False
        
        # 取消任务
        if self.message_task and not self.message_task.done():
            self.message_task.cancel()
            try:
                await self.message_task
            except asyncio.CancelledError:
                pass
        
        if self.keepalive_task and not self.keepalive_task.done():
            self.keepalive_task.cancel()
            try:
                await self.keepalive_task
            except asyncio.CancelledError:
                pass
        
        # 断开连接
        if self.connection:
            await self.connection.disconnect()
            self.connection = None
        
        # 断开回调
        if self.on_disconnect:
            try:
                self.on_disconnect()
            except Exception as e:
                logger.error(f"断开回调出错: {e}")
        
        logger.info("客户端已断开")
    
    async def _message_loop(self) -> None:
        """消息处理循环"""
        while self.is_running and self.connection and self.connection.is_connected:
            try:
                # 接收消息
                message = await self.connection.receive_message()
                if message is None:
                    # 连接已关闭
                    logger.warning("连接关闭，尝试重连")
                    if await self.connection.reconnect():
                        continue
                    else:
                        logger.error("重连失败，停止消息循环")
                        break
                
                # 处理消息
                await self.connection.handle_message(message)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"消息处理循环出错: {e}")
                await asyncio.sleep(1)  # 避免快速循环
    
    async def _handle_message(self, message: Message, connection: Connection) -> None:
        """处理消息（用于回调）"""
        if self.on_message:
            try:
                self.on_message(message)
            except Exception as e:
                logger.error(f"消息回调出错: {e}")
    
    async def send_message(self, message: Message) -> bool:
        """发送消息"""
        if not self.is_connected or not self.connection:
            logger.warning("客户端未连接，无法发送消息")
            return False
        
        return await self.connection.send_message(message)
    
    async def send_with_ack(self, message: Message, timeout: int = 10) -> Optional[Message]:
        """发送消息并等待确认"""
        if not self.is_connected or not self.connection:
            logger.warning("客户端未连接，无法发送消息")
            return None
        
        return await self.connection.send_with_ack(message, timeout)
    
    def get_connection_status(self) -> Dict[str, Any]:
        """获取连接状态"""
        if not self.connection:
            return {"connected": False, "status": "not_connected"}
        
        return {
            "connected": self.connection.is_connected,
            "uri": self.connection.uri,
            "reconnect_attempts": self.connection.reconnect_attempts,
            "last_activity": self.connection.last_activity.isoformat() if self.connection.last_activity else None
        }


async def create_websocket_client(
    device_info: DeviceInfo,
    server_host: str = "localhost",
    server_port: int = 8765,
    use_ssl: bool = False
) -> WebSocketClient:
    """创建WebSocket客户端"""
    
    protocol = "wss" if use_ssl else "ws"
    uri = f"{protocol}://{server_host}:{server_port}"
    
    client = WebSocketClient(device_info)
    return client


async def demo_websocket_client():
    """演示WebSocket客户端"""
    import sys
    import signal
    
    import os
    _server_host = os.environ.get("PAO_WS_HOST", "localhost")
    _server_port = os.environ.get("PAO_WS_PORT", "8765")
    _server_url = f"ws://{_server_host}:{_server_port}"
    
    print("=== PAO WebSocket 客户端演示 ===")
    print(f"连接到服务器: {_server_url}")
    print("按 Ctrl+C 停止客户端")
    print()
    
    # 创建设备信息
    from ..core.device import DeviceInfo, DeviceType
    device_info = DeviceInfo(
        name="Demo-Client",
        device_type=DeviceType.DESKTOP,
        ip_address="127.0.0.1",
        port=8765
    )
    
    # 定义回调函数
    def on_connect():
        print("✅ 连接到服务器")
    
    def on_disconnect():
        print("❌ 与服务器断开连接")
    
    def on_message(message):
        print(f"📨 收到消息: {message.header.message_type.value}")
        if message.payload:
            print(f"   载荷: {json.dumps(message.payload, indent=2, ensure_ascii=False)}")
    
    # 创建客户端
    client = WebSocketClient(
        device_info=device_info,
        on_connect=on_connect,
        on_disconnect=on_disconnect,
        on_message=on_message
    )
    
    # 设置信号处理
    def signal_handler(signum, frame):
        print("\n接收到停止信号")
        asyncio.create_task(client.disconnect())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal.signal)
    
    try:
        # 连接到服务器
        success = await client.connect(_server_url)
        if not success:
            print("连接失败，请确保服务器正在运行")
            return
        
        # 发送测试消息
        from .communication import MessageFactory
        factory = MessageFactory(device_info.device_id)
        
        print("\n发送测试消息...")
        
        # 发送问候消息
        hello_msg = factory.create_hello_message({
            "name": device_info.name,
            "type": device_info.device_type.value
        })
        
        ack = await client.send_with_ack(hello_msg, timeout=5)
        if ack:
            print("✅ 收到服务器确认")
        else:
            print("❌ 未收到服务器确认")
        
        # 保持运行
        print("\n客户端运行中...")
        counter = 0
        
        while client.is_connected:
            await asyncio.sleep(5)
            
            # 定期发送消息
            counter += 1
            test_msg = factory.create_device_info_message({
                "counter": counter,
                "timestamp": datetime.now().isoformat()
            })
            
            success = await client.send_message(test_msg)
            if success:
                print(f"📤 发送消息 #{counter}")
            else:
                print(f"❌ 发送消息失败 #{counter}")
                
    except KeyboardInterrupt:
        print("\n用户中断")
    except Exception as e:
        print(f"客户端错误: {e}")
    finally:
        if client.is_connected:
            await client.disconnect()
    
    print("客户端已停止")


if __name__ == "__main__":
    import json
    
    # 设置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 运行演示
    asyncio.run(demo_websocket_client())