import json
import socket
import sys
import threading
import traceback
import logging
from concurrent.futures import Future
from typing import Any, Dict, Optional

# 引入调度引擎和配置
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dispatcher.dispatcher import DispatcherEngine
import config.settings as settings

logger = logging.getLogger(__name__)

class AdaptiveGateway:
    """自适应触发网关 (Adaptive Trigger Gateway)
    
    负责接收跨语言的 RPC/IPC 请求，
    比如套接字（Socket）或子进程标准输入输出（Stdio），
    并将其路由至调度引擎 (DispatcherEngine)。
    它支持阻塞等待结果（同步调用）和即刻返回（异步调用），
    屏蔽了底层的路由细节。
    """
    def __init__(self, dispatcher: DispatcherEngine):
        self.dispatcher = dispatcher
        self._running = False
        self._socket_thread: Optional[threading.Thread] = None
        self._stdio_thread: Optional[threading.Thread] = None
        self._server_socket: Optional[socket.socket] = None

    def process_payload(self, raw_data: str) -> str:
        """解析请求、调用调度引擎、生成响应"""
        try:
            req = json.loads(raw_data)
        except json.JSONDecodeError:
            return json.dumps({"status": "error", "error": "无效的 JSON 格式"})

        req_id = req.get("id", "unknown_request")
        route_type = req.get("route_type")
        payload = req.get("payload")
        mode = req.get("mode", "sync")  # sync(同步) 或 async(异步)
        args = req.get("args", [])
        kwargs = req.get("kwargs", {})

        if not route_type or not payload:
            return json.dumps({
                "id": req_id,
                "status": "error",
                "error": "缺少 route_type 或 payload 字段"
            })

        try:
            # 连接调度引擎
            future: Future = self.dispatcher.dispatch(route_type, payload, *args, **kwargs)
            
            if mode == "sync":
                # 同步模式：阻塞等待
                result = future.result()
                return json.dumps({
                    "id": req_id,
                    "status": "success",
                    "result": result
                })
            elif mode == "async":
                # 异步模式：即刻返回
                return json.dumps({
                    "id": req_id,
                    "status": "pending",
                    "message": "异步请求已受理"
                })
            else:
                return json.dumps({
                    "id": req_id,
                    "status": "error",
                    "error": f"未知的 mode: {mode}"
                })
        except Exception as e:
            logger.error(f"网关执行异常: {traceback.format_exc()}")
            return json.dumps({
                "id": req_id,
                "status": "error",
                "error": str(e)
            })

    def _socket_worker(self, host: str, port: int):
        """基于 Socket 的跨语言进程间通信"""
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self._server_socket.bind((host, port))
            self._server_socket.listen(5)
            self._server_socket.settimeout(1.0)
            logger.info(f"Socket 监听已开启：{host}:{port}")
        except Exception as e:
            logger.error(f"Socket 绑定失败: {e}")
            self._running = False
            return
            
        while self._running:
            try:
                conn, addr = self._server_socket.accept()
            except socket.timeout:
                continue
            except Exception as e:
                if self._running:
                    logger.error(f"Socket accept 异常: {e}")
                break
                
            # 启动线程处理连接
            def handle_client(client_conn):
                with client_conn:
                    try:
                        # 假设单次请求不超过设定的缓冲区大小
                        data = client_conn.recv(settings.GATEWAY_BUFFER_SIZE)
                        if not data:
                            return
                        response_str = self.process_payload(data.decode('utf-8'))
                        client_conn.sendall(response_str.encode('utf-8'))
                    except Exception as e:
                        logger.error(f"处理客户端连接异常: {e}")
            
            # 启动线程处理请求
            threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

    def start_socket_server(self, host: str = settings.GATEWAY_HOST, port: int = settings.GATEWAY_PORT):
        """启动 Socket 监听服务"""
        if self._running:
            return
        self._running = True
        self._socket_thread = threading.Thread(target=self._socket_worker, args=(host, port), daemon=True)
        self._socket_thread.start()

    def _stdio_worker(self):
        """基于子进程标准输入输出的 IPC"""
        logger.info("标准输入输出监听启动")
        while self._running:
            try:
                # 读取一行作为 JSON 请求
                line = sys.stdin.readline()
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue
                
                # 处理请求
                response_str = self.process_payload(line)
                # 将响应输出
                sys.stdout.write(response_str + '\n')
                sys.stdout.flush()
            except Exception as e:
                logger.error(f"读取标准输入异常: {e}")
                
    def start_stdio_server(self):
        """启动 Stdio 监听服务"""
        if self._running:
            return
        self._running = True
        self._stdio_thread = threading.Thread(target=self._stdio_worker, daemon=True)
        self._stdio_thread.start()

    def stop(self):
        """停止所有服务"""
        self._running = False
        if self._server_socket:
            try:
                self._server_socket.close()
            except:
                pass
        
        # 等待线程结束
        if self._socket_thread and self._socket_thread.is_alive():
            self._socket_thread.join(timeout=2.0)
            
        logger.info("网关已停止")
