"""
v3_bridge.py - V3 Bridge 模块

核心设计：
- 纯 asyncio 实现，不依赖外部库
- 管理长任务（>30分钟）的子进程通信
- 通过 stdin/stdout pipe 进行 JSON Line 通信
- 支持心跳检测、超时处理、优雅关闭
"""

import asyncio
import json
import logging
import time
import uuid
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from typing import Dict, List, Optional, Any, AsyncIterator


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("V3Bridge")


class BridgeState(Enum):
    """Bridge 连接状态枚举"""
    DISCONNECTED = auto()   # 未连接
    CONNECTING = auto()     # 连接中
    CONNECTED = auto()      # 已连接
    ERROR = auto()          # 错误状态


class MessageType(Enum):
    """消息类型枚举"""
    PING = "ping"
    PONG = "pong"
    TASK = "task"
    RESULT = "result"
    PROGRESS = "progress"
    CONTROL = "control"
    ERROR = "error"


@dataclass
class BridgeMessage:
    """Bridge 消息数据类"""
    msg_type: MessageType
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    msg_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "msg_type": self.msg_type.value if isinstance(self.msg_type, MessageType) else self.msg_type,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "msg_id": self.msg_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BridgeMessage":
        """从字典构造"""
        return cls(
            msg_type=MessageType(data.get("msg_type", "error")),
            payload=data.get("payload", {}),
            timestamp=data.get("timestamp", time.time()),
            msg_id=data.get("msg_id", str(uuid.uuid4())[:8]),
        )


class V3Bridge:
    """V3 Bridge - 子进程通信桥接器"""

    def __init__(self, heartbeat_interval: float = 5.0, heartbeat_timeout: float = 15.0):
        self.heartbeat_interval = heartbeat_interval
        self.heartbeat_timeout = heartbeat_timeout
        self._state = BridgeState.DISCONNECTED
        self._process: Optional[asyncio.subprocess.Process] = None
        self._reader_task: Optional[asyncio.Task] = None
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._inbox: asyncio.Queue[BridgeMessage] = asyncio.Queue()
        self._last_pong_time: float = 0.0
        self._lock = asyncio.Lock()
        self._shutdown = False
        self._pending_rpc: Dict[str, asyncio.Future] = {}

    async def connect(self, command: List[str], env: Optional[Dict[str, str]] = None) -> bool:
        """启动子进程并建立 stdin/stdout pipe 通信"""
        async with self._lock:
            if self._state in (BridgeState.CONNECTED, BridgeState.CONNECTING):
                logger.warning("Bridge 已经处于连接状态")
                return False

            self._state = BridgeState.CONNECTING
            self._shutdown = False

        try:
            # Windows 兼容：使用 stdin/stdout pipe
            proc_env = {**dict(asyncio.get_event_loop()._default_executor or {}), **(env or {})}
            # 修正：合并环境变量
            import os
            proc_env = {**os.environ, **(env or {})}

            self._process = await asyncio.create_subprocess_exec(
                *command,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=proc_env,
            )

            self._state = BridgeState.CONNECTED
            self._last_pong_time = time.time()

            # 启动读取循环和心跳循环
            self._reader_task = asyncio.create_task(self._reader_loop())
            self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())

            logger.info(f"Bridge 已连接，子进程 PID={self._process.pid}")
            return True

        except Exception as e:
            logger.error(f"Bridge 连接失败: {e}")
            self._state = BridgeState.ERROR
            return False

    async def disconnect(self, graceful: bool = True) -> None:
        """断开连接"""
        self._shutdown = True

        # 发送优雅关闭指令
        if graceful and self._state == BridgeState.CONNECTED and self._process and self._process.stdin:
            try:
                shutdown_msg = BridgeMessage(
                    msg_type=MessageType.CONTROL,
                    payload={"action": "shutdown"}
                )
                await self._send_raw(shutdown_msg)
                logger.info("已发送优雅关闭指令")
                # 等待子进程退出
                try:
                    await asyncio.wait_for(self._process.wait(), timeout=5.0)
                    logger.info("子进程已优雅退出")
                except asyncio.TimeoutError:
                    logger.warning("子进程优雅退出超时，将强制终止")
            except Exception as e:
                logger.error(f"发送关闭指令失败: {e}")

        # 取消后台任务
        for task in (self._reader_task, self._heartbeat_task):
            if task and not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        self._reader_task = None
        self._heartbeat_task = None

        # 终止子进程
        if self._process and self._process.returncode is None:
            try:
                self._process.kill()
                await self._process.wait()
                logger.info("子进程已强制终止")
            except Exception as e:
                logger.error(f"强制终止子进程失败: {e}")

        self._process = None
        self._state = BridgeState.DISCONNECTED
        logger.info("Bridge 已断开")

    async def _send_raw(self, message: BridgeMessage) -> bool:
        """底层发送方法"""
        if not self._process or not self._process.stdin:
            return False
        try:
            line = json.dumps(message.to_dict(), ensure_ascii=False) + "\n"
            self._process.stdin.write(line.encode("utf-8"))
            await self._process.stdin.drain()
            return True
        except Exception as e:
            logger.error(f"发送消息失败: {e}")
            return False

    async def send(self, message: BridgeMessage) -> bool:
        """发送消息"""
        async with self._lock:
            if self._state != BridgeState.CONNECTED:
                logger.warning("Bridge 未连接，无法发送消息")
                return False
            return await self._send_raw(message)

    async def recv(self, timeout: float = 30.0) -> Optional[BridgeMessage]:
        """接收消息"""
        if self._state != BridgeState.CONNECTED:
            return None
        try:
            return await asyncio.wait_for(self._inbox.get(), timeout=timeout)
        except asyncio.TimeoutError:
            logger.warning(f"接收消息超时（{timeout}秒）")
            return None

    async def call(self, method: str, params: Dict[str, Any], timeout: float = 60.0) -> Dict[str, Any]:
        """同步 RPC 调用"""
        call_id = str(uuid.uuid4())[:8]
        future: asyncio.Future[BridgeMessage] = asyncio.get_event_loop().create_future()
        self._pending_rpc[call_id] = future

        message = BridgeMessage(
            msg_type=MessageType.TASK,
            payload={"method": method, "params": params, "call_id": call_id}
        )

        if not await self.send(message):
            self._pending_rpc.pop(call_id, None)
            return {"success": False, "error": "发送失败，Bridge 未连接"}

        try:
            result = await asyncio.wait_for(future, timeout=timeout)
            return {
                "success": True,
                "data": result.payload.get("data"),
                "call_id": call_id,
            }
        except asyncio.TimeoutError:
            self._pending_rpc.pop(call_id, None)
            return {"success": False, "error": f"RPC 调用超时（{timeout}秒）", "call_id": call_id}
        except Exception as e:
            self._pending_rpc.pop(call_id, None)
            return {"success": False, "error": str(e), "call_id": call_id}

    def is_alive(self) -> bool:
        """检查连接存活"""
        if self._state != BridgeState.CONNECTED:
            return False
        if not self._process:
            return False
        return self._process.returncode is None

    def get_state(self) -> BridgeState:
        """获取状态"""
        return self._state

    async def _heartbeat_loop(self) -> None:
        """心跳循环"""
        logger.info("心跳循环已启动")
        while not self._shutdown and self._state == BridgeState.CONNECTED:
            try:
                await asyncio.sleep(self.heartbeat_interval)

                if self._shutdown or self._state != BridgeState.CONNECTED:
                    break

                # 检查上次 PONG 是否超时
                elapsed = time.time() - self._last_pong_time
                if elapsed > self.heartbeat_timeout:
                    logger.error(f"心跳超时：{elapsed:.1f}s 未收到 PONG")
                    self._state = BridgeState.ERROR
                    break

                # 发送 PING
                ping_msg = BridgeMessage(
                    msg_type=MessageType.PING,
                    payload={"timestamp": time.time()}
                )
                if not await self._send_raw(ping_msg):
                    logger.error("发送 PING 失败")
                    self._state = BridgeState.ERROR
                    break

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"心跳循环异常: {e}")
                self._state = BridgeState.ERROR
                break

        logger.info("心跳循环已退出")

    async def _reader_loop(self) -> None:
        """消息读取循环"""
        logger.info("消息读取循环已启动")
        if not self._process or not self._process.stdout:
            logger.error("stdout pipe 不可用")
            self._state = BridgeState.ERROR
            return

        try:
            while not self._shutdown and self._state == BridgeState.CONNECTED:
                line = await self._process.stdout.readline()
                if not line:
                    logger.info("子进程 stdout 已关闭")
                    break

                try:
                    data = json.loads(line.decode("utf-8").strip())
                    message = BridgeMessage.from_dict(data)
                except (json.JSONDecodeError, ValueError) as e:
                    logger.warning(f"收到非法 JSON 消息: {line.decode('utf-8', errors='replace').strip()}, 错误: {e}")
                    continue

                # 处理 PONG
                if message.msg_type == MessageType.PONG:
                    self._last_pong_time = time.time()
                    logger.debug(f"收到 PONG，msg_id={message.msg_id}")
                    continue

                # 处理 RPC 响应
                call_id = message.payload.get("call_id")
                if call_id and call_id in self._pending_rpc:
                    future = self._pending_rpc.pop(call_id)
                    if not future.done():
                        future.set_result(message)
                    continue

                # 其他消息放入收件箱
                await self._inbox.put(message)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"消息读取循环异常: {e}")
        finally:
            self._state = BridgeState.ERROR
            # 取消所有 pending 的 RPC
            for future in self._pending_rpc.values():
                if not future.done():
                    future.cancel()
            self._pending_rpc.clear()
            logger.info("消息读取循环已退出")


class LongTaskExecutor:
    """长任务执行器 - 基于 V3Bridge"""

    def __init__(self, bridge: V3Bridge):
        self.bridge = bridge
        self._tasks: Dict[str, Dict[str, Any]] = {}

    async def execute(self, task_content: str) -> AsyncIterator[Dict[str, Any]]:
        """执行长任务，yield 进度更新"""
        task_id = str(uuid.uuid4())[:8]
        self._tasks[task_id] = {
            "task_id": task_id,
            "content": task_content,
            "status": "running",
            "progress": 0,
        }

        message = BridgeMessage(
            msg_type=MessageType.TASK,
            payload={"task_id": task_id, "content": task_content}
        )

        if not await self.bridge.send(message):
            yield {"task_id": task_id, "status": "error", "error": "发送任务失败"}
            return

        yield {"task_id": task_id, "status": "started", "progress": 0}

        while True:
            msg = await self.bridge.recv(timeout=30.0)
            if msg is None:
                self._tasks[task_id]["status"] = "error"
                yield {"task_id": task_id, "status": "error", "error": "接收消息超时"}
                break

            if msg.msg_type == MessageType.PROGRESS:
                progress = msg.payload.get("progress", 0)
                self._tasks[task_id]["progress"] = progress
                yield {
                    "task_id": task_id,
                    "status": "progress",
                    "progress": progress,
                    "detail": msg.payload.get("detail", ""),
                }

            elif msg.msg_type == MessageType.RESULT:
                self._tasks[task_id]["status"] = "completed"
                yield {
                    "task_id": task_id,
                    "status": "completed",
                    "result": msg.payload.get("result"),
                }
                break

            elif msg.msg_type == MessageType.ERROR:
                self._tasks[task_id]["status"] = "error"
                yield {
                    "task_id": task_id,
                    "status": "error",
                    "error": msg.payload.get("error", "未知错误"),
                }
                break

    async def pause(self, task_id: str) -> bool:
        """暂停任务"""
        message = BridgeMessage(
            msg_type=MessageType.CONTROL,
            payload={"action": "pause", "task_id": task_id}
        )
        if await self.bridge.send(message):
            if task_id in self._tasks:
                self._tasks[task_id]["status"] = "paused"
            return True
        return False

    async def resume(self, task_id: str) -> bool:
        """恢复任务"""
        message = BridgeMessage(
            msg_type=MessageType.CONTROL,
            payload={"action": "resume", "task_id": task_id}
        )
        if await self.bridge.send(message):
            if task_id in self._tasks:
                self._tasks[task_id]["status"] = "running"
            return True
        return False

    async def cancel(self, task_id: str) -> bool:
        """取消任务"""
        message = BridgeMessage(
            msg_type=MessageType.CONTROL,
            payload={"action": "cancel", "task_id": task_id}
        )
        if await self.bridge.send(message):
            if task_id in self._tasks:
                self._tasks[task_id]["status"] = "cancelled"
            return True
        return False

    def get_progress(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取任务进度"""
        return self._tasks.get(task_id)


# ========== 测试入口 ==========

async def _test():
    """测试 V3Bridge 基础通信、心跳、超时"""
    print("=" * 50)
    print("V3Bridge 测试")
    print("=" * 50)

    # 1. 简单的 echo 子进程测试
    print("\n1. 测试 echo 子进程通信")
    bridge = V3Bridge(heartbeat_interval=2.0, heartbeat_timeout=5.0)

    # 使用 Python 内联脚本创建一个 echo 服务端
    echo_script = """
import sys, json, time

def send(msg):
    line = json.dumps(msg, ensure_ascii=False)
    print(line, flush=True)

try:
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            msg = json.loads(line.strip())
            msg_type = msg.get("msg_type")
            if msg_type == "ping":
                send({"msg_type": "pong", "payload": msg.get("payload", {}), "msg_id": msg.get("msg_id", "")})
            elif msg_type == "control" and msg.get("payload", {}).get("action") == "shutdown":
                send({"msg_type": "result", "payload": {"status": "shutting_down"}, "msg_id": msg.get("msg_id", "")})
                break
            else:
                # echo back
                send({"msg_type": "result", "payload": {"echo": msg.get("payload")}, "msg_id": msg.get("msg_id", "")})
        except Exception as e:
            send({"msg_type": "error", "payload": {"error": str(e)}, "msg_id": ""})
except Exception:
    pass
"""

    import sys
    command = [sys.executable, "-c", echo_script]

    ok = await bridge.connect(command)
    print(f"   连接结果: {ok}")
    print(f"   当前状态: {bridge.get_state().name}")

    # 发送一个普通消息
    msg = BridgeMessage(msg_type=MessageType.TASK, payload={"hello": "world"})
    sent = await bridge.send(msg)
    print(f"   发送消息: {sent}")

    reply = await bridge.recv(timeout=5.0)
    if reply:
        print(f"   收到回复: {reply.to_dict()}")
    else:
        print("   未收到回复")

    # 2. 测试 RPC call
    print("\n2. 测试 RPC call")
    result = await bridge.call("test_method", {"foo": "bar"}, timeout=5.0)
    print(f"   RPC 结果: {result}")

    # 3. 测试心跳检测
    print("\n3. 测试心跳检测（等待 6 秒）")
    await asyncio.sleep(6)
    print(f"   当前状态: {bridge.get_state().name}")
    print(f"   是否存活: {bridge.is_alive()}")

    # 4. 测试优雅关闭
    print("\n4. 测试优雅关闭")
    await bridge.disconnect(graceful=True)
    print(f"   关闭后状态: {bridge.get_state().name}")

    # 5. 测试超时处理（连接到一个不响应 PONG 的进程）
    print("\n5. 测试心跳超时处理")
    dead_script = """
import sys
while True:
    line = sys.stdin.readline()
    if not line:
        break
"""
    dead_bridge = V3Bridge(heartbeat_interval=1.0, heartbeat_timeout=2.0)
    ok2 = await dead_bridge.connect([sys.executable, "-c", dead_script])
    print(f"   连接结果: {ok2}")
    print(f"   等待心跳超时...")
    await asyncio.sleep(4)
    print(f"   当前状态: {dead_bridge.get_state().name}")
    await dead_bridge.disconnect(graceful=False)
    print(f"   断开连接")

    # 6. 测试 LongTaskExecutor
    print("\n6. 测试 LongTaskExecutor")
    exec_bridge = V3Bridge(heartbeat_interval=2.0, heartbeat_timeout=5.0)

    progress_script = """
import sys, json, time

def send(msg):
    print(json.dumps(msg, ensure_ascii=False), flush=True)

try:
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        msg = json.loads(line.strip())
        msg_type = msg.get("msg_type")
        payload = msg.get("payload", {})
        if msg_type == "ping":
            send({"msg_type": "pong", "payload": {}, "msg_id": msg.get("msg_id", "")})
        elif msg_type == "task":
            task_id = payload.get("task_id", "")
            for i in [25, 50, 75, 100]:
                send({"msg_type": "progress", "payload": {"task_id": task_id, "progress": i, "detail": f"step {i}"}, "msg_id": "p" + str(i)})
                time.sleep(0.2)
            send({"msg_type": "result", "payload": {"task_id": task_id, "result": "done"}, "msg_id": "r1"})
        elif msg_type == "control" and payload.get("action") == "shutdown":
            break
except Exception:
    pass
"""
    ok3 = await exec_bridge.connect([sys.executable, "-c", progress_script])
    print(f"   连接结果: {ok3}")

    executor = LongTaskExecutor(exec_bridge)
    async for update in executor.execute("测试长任务"):
        print(f"   进度更新: {update}")

    await exec_bridge.disconnect(graceful=True)

    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(_test())
