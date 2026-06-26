"""
WebSocket 服务器
实现 PAO 系统的 WebSocket 通信服务器
"""

import asyncio
import json
import logging
import ssl
from typing import Dict, Any, Optional, Set, Callable
from datetime import datetime

import websockets
from websockets.server import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosed

from .communication import (
    Message, MessageSerializer, MessageType, Connection,
    create_default_message_handlers, ProtocolError
)
from ..core.device import DeviceInfo

logger = logging.getLogger(__name__)


class WebSocketConnection(Connection):
    """WebSocket 连接实现"""
    
    def __init__(self, connection_id: str, websocket: WebSocketServerProtocol):
        super().__init__(connection_id)
        self.websocket = websocket
        self.remote_address = websocket.remote_address if websocket.remote_address else ("unknown", 0)
        self.device_info: Optional[DeviceInfo] = None
    
    async def connect(self) -> bool:
        """WebSocket连接已经建立，这里只是标记状态"""
        self.is_connected = True
        logger.info(f"WebSocket连接已建立: {self.connection_id}")
        return True
    
    async def disconnect(self) -> None:
        """断开WebSocket连接"""
        self.is_connected = False
        try:
            await self.websocket.close()
        except Exception as e:
            logger.debug(f"关闭WebSocket时出错: {e}")
        logger.info(f"WebSocket连接已断开: {self.connection_id}")
    
    async def send_message(self, message: Message) -> bool:
        """通过WebSocket发送消息"""
        if not self.is_connected:
            logger.warning(f"连接未建立，无法发送消息: {self.connection_id}")
            return False
        
        try:
            # 序列化消息
            data = MessageSerializer.serialize(message)
            
            # 发送消息
            await self.websocket.send(data)
            
            logger.debug(f"消息已发送: {message.header.message_type.value} -> {self.connection_id}")
            return True
            
        except ConnectionClosed:
            logger.warning(f"连接已关闭，无法发送消息: {self.connection_id}")
            self.is_connected = False
            return False
        except Exception as e:
            logger.error(f"发送消息失败: {e}")
            return False
    
    async def receive_message(self) -> Optional[Message]:
        """从WebSocket接收消息"""
        if not self.is_connected:
            return None
        
        try:
            # 接收消息
            data = await self.websocket.recv()
            
            # 反序列化消息
            message = MessageSerializer.deserialize(data)
            
            # 更新活动时间
            self.last_activity = datetime.now()
            
            logger.debug(f"消息已接收: {message.header.message_type.value} <- {self.connection_id}")
            return message
            
        except ConnectionClosed:
            logger.info(f"连接已关闭: {self.connection_id}")
            self.is_connected = False
            return None
        except ProtocolError as e:
            logger.error(f"协议错误: {e}")
            return None
        except Exception as e:
            logger.error(f"接收消息失败: {e}")
            return None
    
    def set_device_info(self, device_info: DeviceInfo) -> None:
        """设置设备信息"""
        self.device_info = device_info
        logger.info(f"设备信息已设置: {device_info.name} ({device_info.device_id})")
    
    def get_device_id(self) -> Optional[str]:
        """获取设备ID"""
        return self.device_info.device_id if self.device_info else None


class WebSocketServer:
    """WebSocket 服务器"""
    
    def __init__(
        self,
        host: str = "0.0.0.0",
        port: int = 8765,
        ssl_context: Optional[ssl.SSLContext] = None,
        on_connection_open: Optional[Callable] = None,
        on_connection_close: Optional[Callable] = None
    ):
        self.host = host
        self.port = port
        self.ssl_context = ssl_context
        
        # 回调函数
        self.on_connection_open = on_connection_open
        self.on_connection_close = on_connection_close
        
        # 连接管理
        self.connections: Dict[str, WebSocketConnection] = {}
        self.connection_counter = 0
        
        # 服务器状态
        self.server = None
        self.is_running = False
        self.server_task: Optional[asyncio.Task] = None
        
        # 消息广播锁
        self.broadcast_lock = asyncio.Lock()
    
    def generate_connection_id(self) -> str:
        """生成连接ID"""
        self.connection_counter += 1
        return f"ws-{self.connection_counter:06d}"
    
    async def start(self) -> None:
        """启动WebSocket服务器"""
        if self.is_running:
            logger.warning("WebSocket服务器已经在运行")
            return
        
        logger.info(f"启动WebSocket服务器: {self.host}:{self.port}")
        
        try:
            # 创建服务器
            self.server = await websockets.serve(
                self._handle_connection,
                self.host,
                self.port,
                ssl=self.ssl_context,
                ping_interval=30,  # 30秒发送一次ping
                ping_timeout=10,   # 10秒ping超时
                close_timeout=10   # 10秒关闭超时
            )
            
            self.is_running = True
            logger.info(f"WebSocket服务器已启动: {self.host}:{self.port}")
            
            # 启动连接清理任务
            self.server_task = asyncio.create_task(self._cleanup_task())
            
        except Exception as e:
            logger.error(f"启动WebSocket服务器失败: {e}")
            raise
    
    async def stop(self) -> None:
        """停止WebSocket服务器"""
        if not self.is_running:
            return
        
        logger.info("停止WebSocket服务器...")
        
        # 停止清理任务
        if self.server_task and not self.server_task.done():
            self.server_task.cancel()
            try:
                await self.server_task
            except asyncio.CancelledError:
                pass
        
        # 关闭所有连接
        await self._close_all_connections()
        
        # 停止服务器
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        
        self.is_running = False
        logger.info("WebSocket服务器已停止")
    
    async def _handle_connection(self, websocket: WebSocketServerProtocol, path: str) -> None:
        """处理新连接"""
        connection_id = self.generate_connection_id()
        connection = WebSocketConnection(connection_id, websocket)
        
        # 注册默认消息处理器
        create_default_message_handlers(connection)
        
        # 添加到连接管理
        self.connections[connection_id] = connection
        
        # 连接建立回调
        if self.on_connection_open:
            try:
                await self.on_connection_open(connection)
            except Exception as e:
                logger.error(f"连接打开回调出错: {e}")
        
        logger.info(f"新连接建立: {connection_id} ({websocket.remote_address})")
        
        try:
            # 连接建立
            await connection.connect()
            
            # 消息处理循环
            await self._message_loop(connection)
            
        except ConnectionClosed:
            logger.info(f"连接正常关闭: {connection_id}")
        except Exception as e:
            logger.error(f"连接处理出错: {e}")
        finally:
            # 连接关闭
            await self._cleanup_connection(connection_id)
    
    async def _message_loop(self, connection: WebSocketConnection) -> None:
        """消息处理循环"""
        while connection.is_connected:
            try:
                # 接收消息
                message = await connection.receive_message()
                if message is None:
                    # 连接已关闭
                    break
                
                # 处理消息
                await connection.handle_message(message)
                
                # 检查是否需要发送ACK
                if message.header.requires_ack:
                    ack_message = message.create_ack()
                    await connection.send_message(ack_message)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"消息处理循环出错: {e}")
                # 发送错误消息
                error_msg = Message(
                    header=connection.create_message_header(MessageType.ERROR),
                    payload={
                        "error": "internal_error",
                        "message": str(e)
                    }
                )
                await connection.send_message(error_msg)
    
    async def _cleanup_connection(self, connection_id: str) -> None:
        """清理连接"""
        if connection_id not in self.connections:
            return
        
        connection = self.connections[connection_id]
        
        # 连接关闭回调
        if self.on_connection_close:
            try:
                await self.on_connection_close(connection)
            except Exception as e:
                logger.error(f"连接关闭回调出错: {e}")
        
        # 断开连接
        await connection.disconnect()
        
        # 从连接管理中移除
        del self.connections[connection_id]
        
        logger.info(f"连接已清理: {connection_id}")
    
    async def _close_all_connections(self) -> None:
        """关闭所有连接"""
        logger.info(f"关闭所有连接 ({len(self.connections)} 个)")
        
        # 复制连接ID列表，避免在迭代时修改字典
        connection_ids = list(self.connections.keys())
        
        for connection_id in connection_ids:
            await self._cleanup_connection(connection_id)
    
    async def _cleanup_task(self) -> None:
        """清理任务，定期检查连接状态"""
        while self.is_running:
            try:
                await asyncio.sleep(60)  # 每分钟检查一次
                
                # 检查连接超时
                now = datetime.now()
                timeout_connections = []
                
                for connection_id, connection in self.connections.items():
                    time_since_activity = (now - connection.last_activity).total_seconds()
                    if time_since_activity > 300:  # 5分钟无活动
                        timeout_connections.append(connection_id)
                
                # 清理超时连接
                for connection_id in timeout_connections:
                    logger.info(f"清理超时连接: {connection_id}")
                    await self._cleanup_connection(connection_id)
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"清理任务出错: {e}")
    
    async def broadcast_message(self, message: Message, exclude_connection_ids: Set[str] = None) -> int:
        """广播消息到所有连接"""
        if exclude_connection_ids is None:
            exclude_connection_ids = set()
        
        sent_count = 0
        
        async with self.broadcast_lock:
            for connection_id, connection in self.connections.items():
                if connection_id in exclude_connection_ids:
                    continue
                
                if connection.is_connected:
                    try:
                        success = await connection.send_message(message)
                        if success:
                            sent_count += 1
                    except Exception as e:
                        logger.warning(f"广播消息失败 ({connection_id}): {e}")
        
        logger.debug(f"广播消息到 {sent_count} 个连接")
        return sent_count
    
    def get_connection(self, connection_id: str) -> Optional[WebSocketConnection]:
        """获取连接"""
        return self.connections.get(connection_id)
    
    def get_connection_by_device_id(self, device_id: str) -> Optional[WebSocketConnection]:
        """根据设备ID获取连接"""
        for connection in self.connections.values():
            if connection.device_info and connection.device_info.device_id == device_id:
                return connection
        return None
    
    def list_connections(self) -> list:
        """列出所有连接"""
        return list(self.connections.values())
    
    def get_connection_count(self) -> int:
        """获取连接数量"""
        return len(self.connections)
    
    def get_device_connections(self) -> Dict[str, WebSocketConnection]:
        """获取设备连接映射"""
        device_connections = {}
        for connection in self.connections.values():
            if connection.device_info:
                device_connections[connection.device_info.device_id] = connection
        return device_connections


async def create_websocket_server(
    host: str = "0.0.0.0",
    port: int = 8765,
    ssl_cert: Optional[str] = None,
    ssl_key: Optional[str] = None
) -> WebSocketServer:
    """创建WebSocket服务器"""
    
    ssl_context = None
    if ssl_cert and ssl_key:
        try:
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain(ssl_cert, ssl_key)
            logger.info(f"启用SSL: {ssl_cert}")
        except Exception as e:
            logger.error(f"加载SSL证书失败: {e}")
            raise
    
    server = WebSocketServer(host=host, port=port, ssl_context=ssl_context)
    return server


async def demo_websocket_server():
    """演示WebSocket服务器"""
    import sys
    import signal
    
    print("=== PAO WebSocket 服务器演示 ===")
    print(f"启动服务器: 0.0.0.0:8765")
    print("按 Ctrl+C 停止服务器")
    print()
    
    # 定义连接回调
    async def on_connection_open(connection):
        print(f"🔗 新连接: {connection.connection_id}")
        
        # 发送欢迎消息
        from .communication import MessageFactory
        factory = MessageFactory("server")
        welcome_msg = factory.create_hello_message({
            "name": "PAO Server",
            "version": "1.0.0",
            "message": "欢迎连接到PAO服务器"
        })
        await connection.send_message(welcome_msg)
    
    async def on_connection_close(connection):
        print(f"🔌 连接关闭: {connection.connection_id}")
    
    # 创建服务器
    server = WebSocketServer(
        host="0.0.0.0",
        port=8765,
        on_connection_open=on_connection_open,
        on_connection_close=on_connection_close
    )
    
    # 设置信号处理
    def signal_handler(signum, frame):
        print("\n接收到停止信号")
        asyncio.create_task(server.stop())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal.signal)
    
    try:
        # 启动服务器
        await server.start()
        
        # 保持运行
        while server.is_running:
            await asyncio.sleep(1)
            
            # 显示连接状态
            count = server.get_connection_count()
            print(f"\r活动连接: {count}", end="", flush=True)
            
    except KeyboardInterrupt:
        print("\n用户中断")
    except Exception as e:
        print(f"服务器错误: {e}")
    finally:
        if server.is_running:
            await server.stop()
    
    print("\n服务器已停止")


if __name__ == "__main__":
    # 设置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 运行演示
    asyncio.run(demo_websocket_server())