"""
Heartbeat Module - 心跳模块

PAO系统的核心机制之一：
- 设备定期发送心跳，证明自己还活着
- 心跳管理器追踪所有设备的心跳状态
- 超时未心跳的设备标记为离线
- 支持心跳状态变化的回调通知
"""

import asyncio
import logging
import time
from typing import Dict, Callable, Optional, List, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


class HeartbeatStatus(str, Enum):
    """心跳状态"""
    ALIVE = "alive"      # 设备存活
    WARNING = "warning"  # 心跳警告（快超时）
    DEAD = "dead"        # 设备离线


@dataclass
class HeartbeatInfo:
    """心跳信息"""
    device_id: str
    last_heartbeat: float  # 时间戳
    status: HeartbeatStatus = HeartbeatStatus.ALIVE
    consecutive_failures: int = 0  # 连续失败次数

    def time_since_heartbeat(self) -> float:
        """距离上次心跳的秒数"""
        return time.time() - self.last_heartbeat


@dataclass
class HeartbeatConfig:
    """心跳配置"""
    interval: int = 30              # 心跳间隔（秒）
    timeout: int = 90               # 超时时间（秒），超过这个时间没心跳认为离线
    warning_threshold: float = 0.7  # 警告阈值，timeout的70%时触发warning状态
    check_interval: int = 10        # 检查间隔（秒）


class HeartbeatCallback:
    """心跳回调函数类型"""
    # 回调签名: (device_id: str, old_status: HeartbeatStatus, new_status: HeartbeatStatus) -> None
    pass


class HeartbeatManager:
    """
    心跳管理器

    核心功能：
    1. 追踪所有设备的心跳状态
    2. 定期检查超时设备
    3. 状态变化时通知订阅者
    4. 本设备也向其他设备发送心跳
    """

    def __init__(self, device_id: str, config: Optional[HeartbeatConfig] = None):
        """
        初始化心跳管理器

        Args:
            device_id: 本设备ID
            config: 心跳配置
        """
        self.device_id = device_id
        self.config = config or HeartbeatConfig()

        # 心跳信息存储: device_id -> HeartbeatInfo
        self._heartbeats: Dict[str, HeartbeatInfo] = {}

        # 回调函数列表
        self._callbacks: List[Callable] = []

        # 任务
        self._send_task: Optional[asyncio.Task] = None
        self._check_task: Optional[asyncio.Task] = None
        self._running = False

        # 外部通信接口（发送心跳用）
        self._sender: Optional[Any] = None

        logger.info(f"心跳管理器初始化完成 [设备: {device_id}]")

    def set_sender(self, sender: Any):
        """
        设置发送器（通常是Communication模块）

        Args:
            sender: 有 send_message 方法的对象
        """
        self._sender = sender

    def register_callback(self, callback: Callable):
        """
        注册心跳状态变化回调

        Args:
            callback: 回调函数，签名: (device_id, old_status, new_status) -> None
        """
        self._callbacks.append(callback)
        logger.debug(f"已注册心跳回调: {callback.__name__ if hasattr(callback, '__name__') else str(callback)}")

    def _notify_status_change(self, device_id: str, old_status: HeartbeatStatus, new_status: HeartbeatStatus):
        """通知所有回调设备状态变化"""
        if old_status == new_status:
            return

        logger.info(f"设备状态变化 [{device_id}]: {old_status.value} -> {new_status.value}")

        for callback in self._callbacks:
            try:
                callback(device_id, old_status, new_status)
            except Exception as e:
                logger.error(f"执行心跳回调失败: {e}")

    async def start(self):
        """启动心跳管理器"""
        if self._running:
            logger.warning("心跳管理器已在运行")
            return

        self._running = True

        # 启动心跳发送任务
        self._send_task = asyncio.create_task(self._heartbeat_sender())

        # 启动心跳检查任务
        self._check_task = asyncio.create_task(self._heartbeat_checker())

        logger.info("心跳管理器已启动")

    async def stop(self):
        """停止心跳管理器"""
        if not self._running:
            return

        self._running = False

        # 取消任务
        if self._send_task:
            self._send_task.cancel()
            try:
                await self._send_task
            except asyncio.CancelledError:
                pass

        if self._check_task:
            self._check_task.cancel()
            try:
                await self._check_task
            except asyncio.CancelledError:
                pass

        logger.info("心跳管理器已停止")

    async def _heartbeat_sender(self):
        """定期发送本设备心跳"""
        while self._running:
            try:
                await asyncio.sleep(self.config.interval)

                if self._sender:
                    # 通过通信模块发送心跳
                    success = await self._sender.send_message(
                        peer_id="broadcast",  # 广播心跳
                        content={
                            "device_id": self.device_id,
                            "timestamp": time.time(),
                            "type": "heartbeat_request"
                        },
                        msg_type="heartbeat"
                    )

                    if success:
                        logger.debug(f"心跳已发送 [设备: {self.device_id}]")
                    else:
                        logger.warning(f"心跳发送失败 [设备: {self.device_id}]")

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"心跳发送异常: {e}")

    async def _heartbeat_checker(self):
        """定期检查所有设备的心跳状态"""
        while self._running:
            try:
                await asyncio.sleep(self.config.check_interval)

                now = time.time()
                timeout_threshold = self.config.timeout
                warning_threshold = self.config.timeout * self.config.warning_threshold

                for device_id, info in list(self._heartbeats.items()):
                    elapsed = now - info.last_heartbeat

                    old_status = info.status

                    if elapsed >= timeout_threshold:
                        info.status = HeartbeatStatus.DEAD
                    elif elapsed >= warning_threshold:
                        info.status = HeartbeatStatus.WARNING

                    if old_status != info.status:
                        self._notify_status_change(device_id, old_status, info.status)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"心跳检查异常: {e}")

    def receive_heartbeat(self, device_id: str, timestamp: float):
        """
        收到其他设备的心跳

        Args:
            device_id: 发送心跳的设备ID
            timestamp: 心跳时间戳
        """
        if device_id not in self._heartbeats:
            # 新设备
            self._heartbeats[device_id] = HeartbeatInfo(
                device_id=device_id,
                last_heartbeat=timestamp,
                status=HeartbeatStatus.ALIVE
            )
            logger.info(f"新设备心跳注册 [{device_id}]")
        else:
            info = self._heartbeats[device_id]
            old_status = info.status

            info.last_heartbeat = timestamp
            info.status = HeartbeatStatus.ALIVE
            info.consecutive_failures = 0

            if old_status != HeartbeatStatus.ALIVE:
                self._notify_status_change(device_id, old_status, HeartbeatStatus.ALIVE)

        logger.debug(f"收到心跳 [{device_id}] elapsed={time.time() - timestamp:.1f}s")

    def get_status(self, device_id: str) -> Optional[HeartbeatStatus]:
        """
        获取设备心跳状态

        Args:
            device_id: 设备ID

        Returns:
            HeartbeatStatus 或 None（设备不存在）
        """
        info = self._heartbeats.get(device_id)
        return info.status if info else None

    def get_all_status(self) -> Dict[str, HeartbeatStatus]:
        """
        获取所有设备的心跳状态

        Returns:
            device_id -> HeartbeatStatus 的字典
        """
        return {
            device_id: info.status
            for device_id, info in self._heartbeats.items()
        }

    def get_device_info(self, device_id: str) -> Optional[HeartbeatInfo]:
        """
        获取设备详细信息

        Args:
            device_id: 设备ID

        Returns:
            HeartbeatInfo 或 None
        """
        return self._heartbeats.get(device_id)

    def get_online_devices(self) -> List[str]:
        """
        获取所有在线设备ID

        Returns:
            在线设备ID列表
        """
        return [
            device_id
            for device_id, info in self._heartbeats.items()
            if info.status != HeartbeatStatus.DEAD
        ]

    def get_alive_devices(self) -> List[str]:
        """
        获取所有存活设备ID（完全正常）

        Returns:
            存活设备ID列表
        """
        return [
            device_id
            for device_id, info in self._heartbeats.items()
            if info.status == HeartbeatStatus.ALIVE
        ]

    def remove_device(self, device_id: str):
        """
        移除设备心跳追踪

        Args:
            device_id: 设备ID
        """
        if device_id in self._heartbeats:
            del self._heartbeats[device_id]
            logger.info(f"移除设备心跳追踪 [{device_id}]")

    def get_summary(self) -> Dict[str, Any]:
        """
        获取心跳管理器摘要

        Returns:
            包含统计信息的字典
        """
        alive = warning = dead = 0

        for info in self._heartbeats.values():
            if info.status == HeartbeatStatus.ALIVE:
                alive += 1
            elif info.status == HeartbeatStatus.WARNING:
                warning += 1
            else:
                dead += 1

        return {
            "device_id": self.device_id,
            "total_devices": len(self._heartbeats),
            "alive": alive,
            "warning": warning,
            "dead": dead,
            "config": {
                "interval": self.config.interval,
                "timeout": self.config.timeout,
                "check_interval": self.config.check_interval
            }
        }


class HeartbeatProtocol:
    """
    心跳协议处理器

    处理心跳相关的协议消息
    """

    @staticmethod
    def create_heartbeat_message(sender_id: str) -> Dict:
        """
        创建心跳消息

        Args:
            sender_id: 发送者设备ID

        Returns:
            心跳消息字典
        """
        return {
            "type": "heartbeat",
            "sender_id": sender_id,
            "timestamp": time.time()
        }

    @staticmethod
    def create_heartbeat_response(sender_id: str, target_id: str) -> Dict:
        """
        创建心跳响应消息

        Args:
            sender_id: 发送者设备ID
            target_id: 目标设备ID

        Returns:
            心跳响应消息字典
        """
        return {
            "type": "heartbeat_response",
            "sender_id": sender_id,
            "target_id": target_id,
            "timestamp": time.time()
        }

    @staticmethod
    def is_heartbeat_message(message: Dict) -> bool:
        """
        判断是否为心跳消息

        Args:
            message: 消息字典

        Returns:
            bool
        """
        msg_type = message.get("type", "")
        return msg_type in ("heartbeat", "heartbeat_response")

    @staticmethod
    def parse_heartbeat(message: Dict) -> Optional[Dict]:
        """
        解析心跳消息

        Args:
            message: 消息字典

        Returns:
            解析后的数据或None
        """
        if not HeartbeatProtocol.is_heartbeat_message(message):
            return None

        return {
            "type": message.get("type"),
            "sender_id": message.get("sender_id"),
            "timestamp": message.get("timestamp", 0)
        }
