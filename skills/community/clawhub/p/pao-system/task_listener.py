"""
Task Listener - 目标工作区任务监听器

功能：
- 接收任务请求
- 执行任务并返回结果
- 支持回调通知

运行方式：
    python task_listener.py [--port 8765] [--ws-id workspace_xxx]
"""

import asyncio
import json
import logging
import time
import uuid
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import asdict

# 导入协议定义
import sys
from pathlib import Path
_project_root = Path(__file__).parent
sys.path.insert(0, str(_project_root))
from src.protocols.task_protocol import (
    TaskMessage, TaskStatus, MessageType, WorkerInfo
)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)


class TaskExecutor:
    """任务执行器 - 可扩展的任务执行逻辑"""
    
    def __init__(self, ws_id: str):
        self.ws_id = ws_id
        self._handlers: Dict[str, callable] = {}
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """注册默认任务处理器"""
        # 可以在这里扩展更多任务类型
        self.register("echo", self._handle_echo)
        self.register("data_query", self._handle_data_query)
        self.register("file_search", self._handle_file_search)
        self.register("code_analysis", self._handle_code_analysis)
        self.register("web_fetch", self._handle_web_fetch)
    
    def register(self, task_type: str, handler: callable):
        """注册任务处理器"""
        self._handlers[task_type] = handler
    
    async def execute(self, task: TaskMessage) -> Dict[str, Any]:
        """执行任务"""
        handler = self._handlers.get(task.task_type)
        
        if not handler:
            return {
                "status": "failed",
                "error": f"未知任务类型: {task.task_type}"
            }
        
        try:
            # 执行任务
            result = await handler(task)
            return {
                "status": "completed",
                "result": result
            }
        except Exception as e:
            logger.exception(f"任务执行失败: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    # ==================== 默认任务处理器 ====================
    
    async def _handle_echo(self, task: TaskMessage) -> Dict[str, Any]:
        """回声测试任务"""
        return {
            "echo": task.task_params.get("message", "hello"),
            "ws_id": self.ws_id,
            "timestamp": time.time()
        }
    
    async def _handle_data_query(self, task: TaskMessage) -> Dict[str, Any]:
        """数据查询任务（示例）"""
        query = task.task_params.get("query", "")
        
        # 这里可以接入金融数据 API
        # 示例返回
        return {
            "query": query,
            "data": f"模拟数据查询结果: {query}",
            "ws_id": self.ws_id,
            "timestamp": time.time()
        }
    
    async def _handle_file_search(self, task: TaskMessage) -> Dict[str, Any]:
        """文件搜索任务"""
        pattern = task.task_params.get("pattern", "")
        path = task.task_params.get("path", ".")
        
        # 简单的文件搜索
        from pathlib import Path
        base = Path(path)
        results = list(base.glob(pattern))[:10]  # 最多返回10个
        
        return {
            "pattern": pattern,
            "count": len(results),
            "files": [str(f) for f in results],
            "ws_id": self.ws_id
        }
    
    async def _handle_code_analysis(self, task: TaskMessage) -> Dict[str, Any]:
        """代码分析任务"""
        file_path = task.task_params.get("file_path", "")
        
        if not file_path:
            return {"error": "缺少 file_path 参数"}
        
        try:
            p = Path(file_path)
            if p.exists():
                content = p.read_text(encoding='utf-8')
                return {
                    "file": file_path,
                    "lines": len(content.split('\n')),
                    "size": len(content),
                    "ws_id": self.ws_id
                }
            else:
                return {"error": f"文件不存在: {file_path}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def _handle_web_fetch(self, task: TaskMessage) -> Dict[str, Any]:
        """网页抓取任务"""
        url = task.task_params.get("url", "")
        
        if not url:
            return {"error": "缺少 url 参数"}
        
        try:
            import httpx
            resp = httpx.get(url, timeout=30)
            return {
                "url": url,
                "status": resp.status_code,
                "length": len(resp.text),
                "ws_id": self.ws_id
            }
        except Exception as e:
            return {"error": str(e)}


class TaskListener:
    """任务监听器 - WebSocket Server"""
    
    def __init__(self, ws_id: str, ws_name: str, host: str = "0.0.0.0", port: int = 8765):
        self.ws_id = ws_id
        self.ws_name = ws_name
        self.host = host
        self.port = port
        self.executor = TaskExecutor(ws_id)
        
        self._tasks: Dict[str, TaskMessage] = {}
        self._server: Optional[asyncio.Server] = None
        self._clients: Dict[str, asyncio.WebSocket] = {}
    
    async def start(self):
        """启动监听器"""
        logger.info(f"🚀 启动 TaskListener: {self.ws_id} @ {self.host}:{self.port}")
        
        self._server = await asyncio.start_server(
            self._handle_client,
            self.host,
            self.port,
            ws_handler=self._ws_handler
        )
        
        logger.info(f"✅ TaskListener 已启动: ws://{self.host}:{self.port}")
        logger.info(f"   工作区: {self.ws_id} ({self.ws_name})")
        
        async with self._server:
            await self._server.serve_forever()
    
    async def _handle_client(self, reader, writer):
        """处理 TCP 连接"""
        addr = writer.get_extra_info('peername')
        logger.info(f"🔌 新连接: {addr}")
        
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                
                # 处理 JSON 消息
                try:
                    msg = json.loads(data.decode())
                    await self._process_message(msg, writer)
                except json.JSONDecodeError:
                    logger.warning(f"无效的 JSON: {data[:100]}")
        
        except Exception as e:
            logger.exception(f"连接错误: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
    
    async def _ws_handler(self, websocket, path):
        """处理 WebSocket 连接"""
        client_id = str(uuid.uuid4())[:8]
        self._clients[client_id] = websocket
        logger.info(f"🔌 WebSocket 连接: {client_id}")
        
        try:
            async for msg_data in websocket:
                await self._process_message(json.loads(msg_data), websocket)
        except Exception as e:
            logger.exception(f"WebSocket 错误: {e}")
        finally:
            del self._clients[client_id]
    
    async def _process_message(self, msg: Dict[str, Any], writer):
        """处理接收到的消息"""
        msg_type = msg.get("msg_type", "")
        
        if msg_type == MessageType.TASK_REQUEST.value:
            await self._handle_task_request(msg)
        
        elif msg_type == MessageType.REGISTRATION.value:
            await self._handle_registration(msg)
        
        elif msg_type == MessageType.TASK_CANCEL.value:
            await self._handle_task_cancel(msg)
        
        else:
            logger.warning(f"未知消息类型: {msg_type}")
    
    async def _handle_task_request(self, msg: Dict[str, Any]):
        """处理任务请求"""
        # 构建任务对象
        task = TaskMessage(
            msg_id=msg.get("msg_id", ""),
            msg_type=msg.get("msg_type", ""),
            sender_ws=msg.get("sender_ws", ""),
            sender_name=msg.get("sender_name", ""),
            task_id=msg.get("task_id", ""),
            task_type=msg.get("task_type", ""),
            task_action=msg.get("task_action", ""),
            task_params=msg.get("task_params", {}),
            priority=msg.get("priority", 5),
            callback_url=msg.get("callback_url", ""),
            status=TaskStatus.ASSIGNED.value
        )
        
        logger.info(f"📥 收到任务: [{task.task_id}] {task.task_type} - {task.task_action}")
        
        # 执行任务
        task.status = TaskStatus.RUNNING.value
        task.started_at = time.time()
        
        result = await self.executor.execute(task)
        
        # 更新任务状态
        task.status = result.get("status", TaskStatus.COMPLETED.value)
        task.completed_at = time.time()
        task.result = result.get("result")
        task.error = result.get("error")
        
        # 如果有回调地址，发送结果
        if task.callback_url:
            await self._send_callback(task)
        
        # 直接返回结果给发送者
        response = TaskMessage(
            msg_type=MessageType.TASK_RESULT.value,
            sender_ws=self.ws_id,
            sender_name=self.ws_name,
            task_id=task.task_id,
            status=task.status,
            result=task.result,
            error=task.error,
            completed_at=task.completed_at
        )
        
        logger.info(f"✅ 任务完成: [{task.task_id}] 状态: {task.status}")
        
        # 发送响应（需要从 _clients 找到发送者）
        # 这里简化处理，实际需要记录发送者信息
        return asdict(response)
    
    async def _send_callback(self, task: TaskMessage):
        """发送回调结果"""
        callback_url = task.callback_url
        
        if not callback_url:
            return
        
        logger.info(f"📤 发送回调: {callback_url}")
        
        result_msg = {
            "msg_type": MessageType.TASK_RESULT.value,
            "task_id": task.task_id,
            "sender_ws": self.ws_id,
            "status": task.status,
            "result": task.result,
            "error": task.error,
            "completed_at": task.completed_at
        }
        
        try:
            import httpx
            # 支持 ws:// 或 http://
            if callback_url.startswith("ws://"):
                # WebSocket 回调
                async with httpx.AsyncClient() as client:
                    # 注意：httpx 不支持 ws，需要用 websockets
                    pass
            else:
                async with httpx.AsyncClient() as client:
                    resp = await client.post(callback_url, json=result_msg, timeout=30)
                    logger.info(f"回调响应: {resp.status_code}")
        except Exception as e:
            logger.error(f"回调失败: {e}")
    
    async def _handle_registration(self, msg: Dict[str, Any]):
        """处理注册消息"""
        logger.info(f"📝 注册: {msg.get('sender_ws')} - {msg.get('sender_name')}")
    
    async def _handle_task_cancel(self, msg: Dict[str, Any]):
        """处理取消任务"""
        task_id = msg.get("task_id")
        if task_id in self._tasks:
            self._tasks[task_id].status = TaskStatus.CANCELLED.value
    
    def stop(self):
        """停止监听器"""
        if self._server:
            self._server.close()


async def main():
    parser = argparse.ArgumentParser(description="Task Listener")
    parser.add_argument("--ws-id", default="ws_default", help="工作区ID")
    parser.add_argument("--ws-name", default="默认工作区", help="工作区名称")
    parser.add_argument("--host", default="0.0.0.0", help="监听地址")
    parser.add_argument("--port", type=int, default=8765, help="监听端口")
    
    args = parser.parse_args()
    
    listener = TaskListener(
        ws_id=args.ws_id,
        ws_name=args.ws_name,
        host=args.host,
        port=args.port
    )
    
    try:
        await listener.start()
    except KeyboardInterrupt:
        logger.info("🛑 停止监听器")
        listener.stop()


if __name__ == "__main__":
    asyncio.run(main())