"""
Heartbeat Module Tests - 心跳模块测试
"""

import pytest
import asyncio
import time
from unittest.mock import AsyncMock, MagicMock

from src.core.heartbeat import (
    HeartbeatManager,
    HeartbeatConfig,
    HeartbeatStatus,
    HeartbeatInfo,
    HeartbeatProtocol
)


class TestHeartbeatInfo:
    """测试HeartbeatInfo数据类"""

    def test_heartbeat_info_creation(self):
        """测试心跳信息创建"""
        info = HeartbeatInfo(
            device_id="test_device",
            last_heartbeat=time.time()
        )

        assert info.device_id == "test_device"
        assert info.status == HeartbeatStatus.ALIVE
        assert info.consecutive_failures == 0

    def test_time_since_heartbeat(self):
        """测试距离上次心跳的时间计算"""
        past_time = time.time() - 30
        info = HeartbeatInfo(
            device_id="test_device",
            last_heartbeat=past_time
        )

        elapsed = info.time_since_heartbeat()
        assert 29 <= elapsed <= 31  # 允许1秒误差


class TestHeartbeatConfig:
    """测试心跳配置"""

    def test_default_config(self):
        """测试默认配置"""
        config = HeartbeatConfig()

        assert config.interval == 30
        assert config.timeout == 90
        assert config.warning_threshold == 0.7
        assert config.check_interval == 10

    def test_custom_config(self):
        """测试自定义配置"""
        config = HeartbeatConfig(
            interval=60,
            timeout=180,
            warning_threshold=0.5
        )

        assert config.interval == 60
        assert config.timeout == 180
        assert config.warning_threshold == 0.5


class TestHeartbeatManager:
    """测试心跳管理器"""

    @pytest.fixture
    def manager(self):
        """创建心跳管理器实例"""
        return HeartbeatManager("test_device")

    @pytest.fixture
    def manager_with_config(self):
        """创建带自定义配置的心跳管理器"""
        config = HeartbeatConfig(
            interval=1,  # 1秒间隔方便测试
            timeout=3,   # 3秒超时
            check_interval=1  # 1秒检查间隔
        )
        return HeartbeatManager("test_device", config)

    def test_manager_initialization(self, manager):
        """测试管理器初始化"""
        assert manager.device_id == "test_device"
        assert len(manager._heartbeats) == 0
        assert len(manager._callbacks) == 0
        assert manager._running is False

    def test_register_callback(self, manager):
        """测试注册回调"""
        callback_called = []

        def callback(device_id, old, new):
            callback_called.append((device_id, old, new))

        manager.register_callback(callback)
        assert len(manager._callbacks) == 1

    @pytest.mark.asyncio
    async def test_start_stop(self, manager):
        """测试启动和停止"""
        await manager.start()
        assert manager._running is True
        assert manager._send_task is not None
        assert manager._check_task is not None

        await manager.stop()
        assert manager._running is False

    @pytest.mark.asyncio
    async def test_receive_heartbeat_new_device(self, manager):
        """测试接收新设备心跳"""
        manager.receive_heartbeat("device_1", time.time())

        assert "device_1" in manager._heartbeats
        assert manager.get_status("device_1") == HeartbeatStatus.ALIVE

    @pytest.mark.asyncio
    async def test_receive_heartbeat_existing_device(self, manager):
        """测试接收已存在设备心跳"""
        # 先注册设备
        manager.receive_heartbeat("device_1", time.time())

        # 模拟设备离线后重新上线
        await asyncio.sleep(0.1)
        manager.receive_heartbeat("device_1", time.time())

        assert manager.get_status("device_1") == HeartbeatStatus.ALIVE

    @pytest.mark.asyncio
    async def test_status_change_callback(self, manager):
        """测试状态变化回调"""
        callback_results = []

        def callback(device_id, old, new):
            callback_results.append((device_id, old, new))

        manager.register_callback(callback)

        # 接收心跳触发状态变化
        manager.receive_heartbeat("device_1", time.time())

        # 等待异步回调执行
        await asyncio.sleep(0.1)

        # 验证回调被调用
        assert len(callback_results) > 0

    def test_get_status_nonexistent(self, manager):
        """测试获取不存在的设备状态"""
        status = manager.get_status("nonexistent")
        assert status is None

    def test_get_online_devices(self, manager):
        """测试获取在线设备"""
        manager.receive_heartbeat("device_1", time.time())
        manager.receive_heartbeat("device_2", time.time())

        online = manager.get_online_devices()
        assert "device_1" in online
        assert "device_2" in online

    def test_get_alive_devices(self, manager):
        """测试获取存活设备"""
        manager.receive_heartbeat("device_1", time.time())
        manager.receive_heartbeat("device_2", time.time())

        alive = manager.get_alive_devices()
        assert "device_1" in alive
        assert "device_2" in alive

    def test_remove_device(self, manager):
        """测试移除设备"""
        manager.receive_heartbeat("device_1", time.time())
        manager.remove_device("device_1")

        assert "device_1" not in manager._heartbeats

    def test_get_summary(self, manager):
        """测试获取摘要信息"""
        manager.receive_heartbeat("device_1", time.time())
        manager.receive_heartbeat("device_2", time.time())

        summary = manager.get_summary()

        assert summary["device_id"] == "test_device"
        assert summary["total_devices"] == 2
        assert summary["alive"] == 2
        assert summary["warning"] == 0
        assert summary["dead"] == 0

    def test_get_device_info(self, manager):
        """测试获取设备详细信息"""
        manager.receive_heartbeat("device_1", time.time())

        info = manager.get_device_info("device_1")
        assert info is not None
        assert info.device_id == "device_1"
        assert info.status == HeartbeatStatus.ALIVE

    @pytest.mark.asyncio
    async def test_timeout_detection(self, manager_with_config):
        """测试超时检测"""
        manager = manager_with_config

        # 注册设备，但心跳很旧
        old_time = time.time() - 10  # 10秒前的心跳
        manager.receive_heartbeat("device_1", old_time)

        # 初始状态应该是ALIVE（刚注册）
        # 等待检查任务运行
        await asyncio.sleep(2)

        # 状态应该变为DEAD
        status = manager.get_status("device_1")
        assert status == HeartbeatStatus.DEAD


class TestHeartbeatProtocol:
    """测试心跳协议"""

    def test_create_heartbeat_message(self):
        """测试创建心跳消息"""
        msg = HeartbeatProtocol.create_heartbeat_message("sender_1")

        assert msg["type"] == "heartbeat"
        assert msg["sender_id"] == "sender_1"
        assert "timestamp" in msg

    def test_create_heartbeat_response(self):
        """测试创建心跳响应"""
        msg = HeartbeatProtocol.create_heartbeat_response("sender_1", "target_1")

        assert msg["type"] == "heartbeat_response"
        assert msg["sender_id"] == "sender_1"
        assert msg["target_id"] == "target_1"
        assert "timestamp" in msg

    def test_is_heartbeat_message(self):
        """测试心跳消息识别"""
        assert HeartbeatProtocol.is_heartbeat_message({"type": "heartbeat"}) is True
        assert HeartbeatProtocol.is_heartbeat_message({"type": "heartbeat_response"}) is True
        assert HeartbeatProtocol.is_heartbeat_message({"type": "text"}) is False
        assert HeartbeatProtocol.is_heartbeat_message({}) is False

    def test_parse_heartbeat(self):
        """测试解析心跳消息"""
        msg = {
            "type": "heartbeat",
            "sender_id": "device_1",
            "timestamp": time.time()
        }

        parsed = HeartbeatProtocol.parse_heartbeat(msg)

        assert parsed is not None
        assert parsed["type"] == "heartbeat"
        assert parsed["sender_id"] == "device_1"

    def test_parse_non_heartbeat(self):
        """测试解析非心跳消息"""
        msg = {"type": "text", "content": "hello"}

        parsed = HeartbeatProtocol.parse_heartbeat(msg)
        assert parsed is None


class TestHeartbeatIntegration:
    """心跳模块集成测试"""

    @pytest.mark.asyncio
    async def test_multi_device_heartbeat(self):
        """测试多设备心跳追踪"""
        manager = HeartbeatManager("central_device")

        # 模拟多个设备发送心跳
        for i in range(5):
            manager.receive_heartbeat(f"device_{i}", time.time())

        assert len(manager.get_online_devices()) == 5
        assert len(manager.get_alive_devices()) == 5

        await manager.stop()

    @pytest.mark.asyncio
    async def test_heartbeat_with_mock_sender(self):
        """测试带模拟发送器的心跳"""
        manager = HeartbeatManager("test_device")

        # 创建模拟发送器
        mock_sender = MagicMock()
        mock_sender.send_message = AsyncMock(return_value=True)
        manager.set_sender(mock_sender)

        await manager.start()

        # 等待几个心跳周期
        await asyncio.sleep(3.5)

        # 验证发送器被调用
        assert mock_sender.send_message.called

        await manager.stop()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
