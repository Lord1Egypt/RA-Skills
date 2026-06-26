"""
v3_worker.py - V3 Bridge Worker 子进程

被 V3Bridge 通过 subprocess 启动，通过 stdin/stdout JSON Line 协议通信。
支持 PING/PONG、TASK 执行（带进度）、CONTROL 指令。
"""

import json
import logging
import signal
import sys
import time
import uuid
from enum import Enum
from typing import Any, Dict, Optional


# 配置日志输出到 stderr，避免污染 stdout 的 JSON Line 协议
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("V3Worker")


class MessageType(Enum):
    """消息类型枚举 - 与 v3_bridge.py 保持一致"""
    PING = "ping"
    PONG = "pong"
    TASK = "task"
    RESULT = "result"
    PROGRESS = "progress"
    CONTROL = "control"
    ERROR = "error"


class WorkerState(Enum):
    """Worker 状态枚举"""
    IDLE = "idle"           # 空闲
    RUNNING = "running"     # 执行任务中
    SHUTTING_DOWN = "shutting_down"  # 正在关闭


class V3Worker:
    """V3 Worker - 子进程工作器"""

    def __init__(self):
        self.state = WorkerState.IDLE
        self.current_task_id: Optional[str] = None
        self.shutdown_requested = False
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """设置信号处理器 - Windows 兼容"""
        try:
            signal.signal(signal.SIGTERM, self._handle_signal)
            signal.signal(signal.SIGINT, self._handle_signal)
            logger.info("信号处理器已设置")
        except ValueError:
            # Windows 某些环境下可能不支持
            logger.warning("当前环境不支持信号处理")

    def _handle_signal(self, signum, frame):
        """信号处理回调"""
        sig_name = "SIGTERM" if signum == signal.SIGTERM else "SIGINT"
        logger.info(f"收到 {sig_name} 信号，准备优雅退出")
        self.shutdown_requested = True

    def send_message(self, msg_type: MessageType, payload: Dict[str, Any], msg_id: Optional[str] = None):
        """发送 JSON Line 消息到 stdout"""
        message = {
            "msg_type": msg_type.value,
            "payload": payload,
            "timestamp": time.time(),
            "msg_id": msg_id or str(uuid.uuid4())[:8],
        }
        try:
            line = json.dumps(message, ensure_ascii=False)
            print(line, flush=True)
            logger.debug(f"发送消息: {msg_type.value}, msg_id={message['msg_id']}")
        except Exception as e:
            logger.error(f"发送消息失败: {e}")

    def send_error(self, error_msg: str, msg_id: Optional[str] = None):
        """发送错误消息"""
        logger.error(f"发送错误: {error_msg}")
        self.send_message(MessageType.ERROR, {"error": error_msg}, msg_id)

    def handle_ping(self, payload: Dict[str, Any], msg_id: Optional[str] = None):
        """处理 PING 消息 - 回复 PONG"""
        logger.debug("收到 PING，回复 PONG")
        self.send_message(MessageType.PONG, {"timestamp": time.time()}, msg_id)

    def handle_control(self, payload: Dict[str, Any], msg_id: Optional[str] = None):
        """处理 CONTROL 消息"""
        action = payload.get("action", "")
        logger.info(f"收到 CONTROL 指令: {action}")

        if action == "shutdown":
            self.shutdown_requested = True
            self.send_message(MessageType.RESULT, {"status": "shutting_down"}, msg_id)
        elif action == "pause":
            # 暂停功能预留
            self.send_message(MessageType.RESULT, {"status": "pause_not_implemented"}, msg_id)
        elif action == "resume":
            # 恢复功能预留
            self.send_message(MessageType.RESULT, {"status": "resume_not_implemented"}, msg_id)
        elif action == "cancel":
            # 取消功能预留
            self.send_message(MessageType.RESULT, {"status": "cancel_not_implemented"}, msg_id)
        else:
            self.send_error(f"未知的 control action: {action}", msg_id)

    def execute_task(self, payload: Dict[str, Any], msg_id: Optional[str] = None):
        """
        执行 TASK 任务
        - 模拟分步执行，定期发送 PROGRESS
        - 完成后发送 RESULT
        """
        task_id = payload.get("task_id") or str(uuid.uuid4())[:8]
        content = payload.get("content", "")
        total_steps = payload.get("total_steps", 5)  # 默认 5 步

        logger.info(f"开始执行任务: {task_id}, 内容: {content[:50]}..., 总步数: {total_steps}")

        self.state = WorkerState.RUNNING
        self.current_task_id = task_id

        try:
            # 模拟分步执行
            for step in range(1, total_steps + 1):
                if self.shutdown_requested:
                    logger.info("任务执行被中断（关闭请求）")
                    self.send_error("任务被中断：Worker 正在关闭", msg_id)
                    return

                progress = int((step / total_steps) * 100)
                detail = f"执行步骤 {step}/{total_steps}"

                logger.debug(f"任务 {task_id} 进度: {progress}%")

                # 发送进度更新
                self.send_message(
                    MessageType.PROGRESS,
                    {
                        "task_id": task_id,
                        "progress": progress,
                        "detail": detail,
                        "step": step,
                        "total_steps": total_steps,
                    },
                    msg_id,
                )

                # 模拟工作耗时
                time.sleep(0.5)

            # 任务完成，发送结果
            result = {
                "task_id": task_id,
                "result": f"任务完成: {content}",
                "completed_at": time.time(),
            }
            logger.info(f"任务 {task_id} 完成")
            self.send_message(MessageType.RESULT, result, msg_id)

        except Exception as e:
            logger.exception("任务执行异常")
            self.send_error(f"任务执行失败: {str(e)}", msg_id)
        finally:
            self.state = WorkerState.IDLE
            self.current_task_id = None

    def process_message(self, line: str):
        """处理单条 JSON Line 消息"""
        line = line.strip()
        if not line:
            return

        try:
            data = json.loads(line)
        except json.JSONDecodeError as e:
            logger.warning(f"JSON 解析失败: {e}, 原始数据: {line[:100]}")
            self.send_error(f"JSON 解析失败: {e}")
            return

        msg_type = data.get("msg_type", "")
        payload = data.get("payload", {})
        msg_id = data.get("msg_id")

        logger.debug(f"收到消息: {msg_type}, msg_id={msg_id}")

        try:
            if msg_type == MessageType.PING.value:
                self.handle_ping(payload, msg_id)
            elif msg_type == MessageType.CONTROL.value:
                self.handle_control(payload, msg_id)
            elif msg_type == MessageType.TASK.value:
                # 检查是否已有任务在运行
                if self.state == WorkerState.RUNNING:
                    self.send_error("已有任务正在执行，请等待完成", msg_id)
                else:
                    self.execute_task(payload, msg_id)
            else:
                logger.warning(f"未知消息类型: {msg_type}")
                self.send_error(f"未知消息类型: {msg_type}", msg_id)
        except Exception as e:
            logger.exception(f"处理消息异常: {msg_type}")
            self.send_error(f"处理消息失败: {str(e)}", msg_id)

    def run(self):
        """主循环 - 从 stdin 读取并处理消息"""
        logger.info("V3 Worker 已启动，等待消息...")

        try:
            while not self.shutdown_requested:
                try:
                    line = sys.stdin.readline()
                    if not line:
                        # stdin 已关闭
                        logger.info("stdin 已关闭，Worker 退出")
                        break

                    self.process_message(line)

                except KeyboardInterrupt:
                    logger.info("收到键盘中断")
                    break
                except Exception as e:
                    logger.exception("主循环异常")
                    self.send_error(f"主循环异常: {str(e)}")

        finally:
            self.state = WorkerState.SHUTTING_DOWN
            logger.info("V3 Worker 已停止")


def main():
    """入口函数"""
    worker = V3Worker()
    worker.run()


if __name__ == "__main__":
    main()
