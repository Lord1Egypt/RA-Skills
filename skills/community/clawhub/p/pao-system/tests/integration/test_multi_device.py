"""多设备集成测试"""
import asyncio
import pytest
import sys
sys.path.insert(0, 'src')

from device_discovery import DeviceDiscovery
from communication import Communication
from sync import SyncManager


@pytest.fixture
async def device_a():
    """设备A"""
    device = DeviceDiscovery(name="Device-A")
    await device.start()
    yield device
    await device.stop()


@pytest.fixture
async def device_b():
    """设备B"""
    device = DeviceDiscovery(name="Device-B")
    await device.start()
    yield device
    await device.stop()


@pytest.mark.asyncio
async def test_device_discovery(device_a, device_b):
    """测试设备发现"""
    await asyncio.sleep(2)  # 等待发现

    devices_a = device_a.get_discovered_devices()
    devices_b = device_b.get_discovered_devices()

    assert len(devices_a) >= 1
    assert len(devices_b) >= 1


@pytest.mark.asyncio
async def test_device_communication(device_a, device_b):
    """测试设备间通信"""
    comm_a = Communication(device_a)
    comm_b = Communication(device_b)

    await comm_a.connect_to(device_b.device_id)
    await asyncio.sleep(1)

    # 发送消息
    sent = await comm_a.send_message(device_b.device_id, {"type": "test", "content": "hello"})
    assert sent

    await comm_a.disconnect()
    await comm_b.disconnect()


@pytest.mark.asyncio
async def test_sync_between_devices(device_a, device_b):
    """测试设备间同步"""
    sync_a = SyncManager(device_a)
    sync_b = SyncManager(device_b)

    await sync_a.connect_peer(device_b.device_id)
    await sync_b.connect_peer(device_a.device_id)
    await asyncio.sleep(1)

    # 模拟数据同步
    test_data = {"key": "value", "timestamp": asyncio.get_event_loop().time()}
    await sync_a.sync_data(test_data)

    await asyncio.sleep(2)

    # 验证同步结果
    synced_data = sync_b.get_received_data()
    assert len(synced_data) > 0

    await sync_a.disconnect()
    await sync_b.disconnect()
