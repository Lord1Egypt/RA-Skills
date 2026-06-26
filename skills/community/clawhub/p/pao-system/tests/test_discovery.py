"""
设备发现测试
测试 PAO 系统的设备发现功能
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from pathlib import Path
import sys

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.device import (
    DeviceInfo, DeviceType, DeviceCapability, DeviceRegistry, DeviceState, DeviceStatus
)
from src.core.discovery import DeviceDiscoveryService, DiscoveryConfig
from src.core.config import PAOConfig


class TestDeviceInfo:
    """设备信息测试"""
    
    def test_device_info_creation(self):
        """测试设备信息创建"""
        device = DeviceInfo(
            name="Test Device",
            device_type=DeviceType.LAPTOP,
            ip_address="192.168.1.100",
            port=8765
        )
        
        assert device.name == "Test Device"
        assert device.device_type == DeviceType.LAPTOP
        assert device.ip_address == "192.168.1.100"
        assert device.port == 8765
        assert len(device.device_id) > 0
    
    def test_device_info_to_dict(self):
        """测试设备信息转换为字典"""
        device = DeviceInfo(
            name="Test Device",
            device_type=DeviceType.LAPTOP,
            capabilities=[DeviceCapability.COMPUTE, DeviceCapability.DISPLAY]
        )
        
        data = device.to_dict()
        
        assert data["name"] == "Test Device"
        assert data["device_type"] == "laptop"
        assert "compute" in data["capabilities"]
        assert "display" in data["capabilities"]
        assert "first_seen" in data
        assert "last_seen" in data
    
    def test_device_info_from_dict(self):
        """测试从字典创建设备信息"""
        data = {
            "device_id": "test-id-123",
            "name": "Test Device",
            "device_type": "laptop",
            "ip_address": "192.168.1.100",
            "port": 8765,
            "capabilities": ["compute", "storage"],
            "first_seen": "2024-01-01T00:00:00",
            "last_seen": "2024-01-01T12:00:00"
        }
        
        device = DeviceInfo.from_dict(data)
        
        assert device.device_id == "test-id-123"
        assert device.name == "Test Device"
        assert device.device_type == DeviceType.LAPTOP
        assert device.ip_address == "192.168.1.100"
        assert device.port == 8765
        assert DeviceCapability.COMPUTE in device.capabilities
        assert DeviceCapability.STORAGE in device.capabilities
    
    def test_update_last_seen(self):
        """测试更新最后出现时间"""
        import time
        device = DeviceInfo()
        original_last_seen = device.last_seen
        
        # 等待一小段时间
        time.sleep(0.01)
        
        device.update_last_seen()
        
        assert device.last_seen > original_last_seen
    
    def test_capability_score(self):
        """测试能力评分"""
        device = DeviceInfo(
            cpu_cores=4,
            memory_gb=16,
            storage_gb=512,
            capabilities=[DeviceCapability.COMPUTE, DeviceCapability.STORAGE, DeviceCapability.MEMORY]
        )
        
        compute_score = device.get_capability_score(DeviceCapability.COMPUTE)
        storage_score = device.get_capability_score(DeviceCapability.STORAGE)
        memory_score = device.get_capability_score(DeviceCapability.MEMORY)
        network_score = device.get_capability_score(DeviceCapability.NETWORK)  # 未包含的能力
        
        assert compute_score == 400  # 4 cores * 100
        assert storage_score == 5120  # 512 GB * 10
        assert memory_score == 800  # 16 GB * 50
        assert network_score == 0  # 未包含的能力


class TestDeviceRegistry:
    """设备注册表测试"""
    
    def setup_method(self):
        """测试设置"""
        self.registry = DeviceRegistry()
        self.device1 = DeviceInfo(
            device_id="device-1",
            name="Device 1",
            device_type=DeviceType.DESKTOP
        )
        self.device2 = DeviceInfo(
            device_id="device-2",
            name="Device 2",
            device_type=DeviceType.PHONE
        )
    
    def test_register_device(self):
        """测试注册设备"""
        self.registry.register_device(self.device1)
        
        assert "device-1" in self.registry.devices
        assert self.registry.devices["device-1"].name == "Device 1"
        assert "device-1" in self.registry.device_states
    
    def test_unregister_device(self):
        """测试注销设备"""
        self.registry.register_device(self.device1)
        self.registry.register_device(self.device2)
        
        self.registry.unregister_device("device-1")
        
        assert "device-1" not in self.registry.devices
        assert "device-2" in self.registry.devices
        assert "device-1" not in self.registry.device_states
    
    def test_get_device(self):
        """测试获取设备"""
        self.registry.register_device(self.device1)
        
        device = self.registry.get_device("device-1")
        assert device is not None
        assert device.name == "Device 1"
        
        device = self.registry.get_device("non-existent")
        assert device is None
    
    def test_list_devices(self):
        """测试列出设备"""
        self.registry.register_device(self.device1)
        self.registry.register_device(self.device2)
        
        devices = self.registry.list_devices()
        
        assert len(devices) == 2
        device_names = [device.name for device in devices]
        assert "Device 1" in device_names
        assert "Device 2" in device_names
    
    def test_list_online_devices(self):
        """测试列出在线设备"""
        self.registry.register_device(self.device1)
        self.registry.register_device(self.device2)
        
        # 设置设备2为离线
        self.registry.device_states["device-2"].status = DeviceStatus.OFFLINE
        
        online_devices = self.registry.list_online_devices()
        
        assert len(online_devices) == 1
        assert online_devices[0].device_id == "device-1"
    
    def test_find_device_by_capability(self):
        """测试根据能力查找设备"""
        device1 = DeviceInfo(
            device_id="device-1",
            capabilities=[DeviceCapability.COMPUTE, DeviceCapability.STORAGE]
        )
        device2 = DeviceInfo(
            device_id="device-2",
            capabilities=[DeviceCapability.DISPLAY]
        )
        
        self.registry.register_device(device1)
        self.registry.register_device(device2)
        
        compute_devices = self.registry.find_device_by_capability(DeviceCapability.COMPUTE)
        display_devices = self.registry.find_device_by_capability(DeviceCapability.DISPLAY)
        network_devices = self.registry.find_device_by_capability(DeviceCapability.NETWORK)
        
        assert len(compute_devices) == 1
        assert compute_devices[0].device_id == "device-1"
        
        assert len(display_devices) == 1
        assert display_devices[0].device_id == "device-2"
        
        assert len(network_devices) == 0
    
    def test_cleanup_offline_devices(self):
        """测试清理离线设备"""
        import time
        from datetime import datetime, timedelta
        
        self.registry.register_device(self.device1)
        self.registry.register_device(self.device2)
        
        # 设置设备1的最后心跳时间在超时范围内
        self.registry.device_states["device-1"].last_heartbeat = datetime.now()
        
        # 设置设备2的最后心跳时间在超时范围外（6分钟前）
        self.registry.device_states["device-2"].last_heartbeat = datetime.now() - timedelta(minutes=6)
        
        # 清理超时设备（5分钟超时）
        self.registry.cleanup_offline_devices(timeout_seconds=300)
        
        devices = self.registry.list_devices()
        
        assert len(devices) == 1
        assert devices[0].device_id == "device-1"


class TestDeviceDiscoveryService:
    """设备发现服务测试"""
    
    def setup_method(self):
        """测试设置"""
        self.config = PAOConfig(
            device_name="Test-Device",
            enable_discovery=True
        )
        self.device_registry = DeviceRegistry()
        
        # 模拟回调
        self.on_device_discovered = Mock()
        self.on_device_lost = Mock()
    
    @pytest.mark.asyncio
    async def test_service_creation(self):
        """测试服务创建"""
        service = DeviceDiscoveryService(
            config=self.config,
            device_registry=self.device_registry,
            on_device_discovered=self.on_device_discovered,
            on_device_lost=self.on_device_lost
        )
        
        assert service.config == self.config
        assert service.device_registry == self.device_registry
        assert service.on_device_discovered == self.on_device_discovered
        assert service.on_device_lost == self.on_device_lost
        
        # 测试本地设备信息
        assert service.local_device is not None
        assert service.local_device.name == "Test-Device"
    
    @pytest.mark.asyncio
    async def test_detect_device_type(self):
        """测试设备类型检测"""
        service = DeviceDiscoveryService(
            config=self.config,
            device_registry=self.device_registry
        )
        
        # 模拟平台检测
        with patch('platform.system', return_value='Windows'):
            with patch('platform.node', return_value='MY-LAPTOP'):
                device_type = service._detect_device_type()
                assert device_type == DeviceType.LAPTOP
        
        with patch('platform.system', return_value='Linux'):
            with patch('platform.machine', return_value='x86_64'):
                device_type = service._detect_device_type()
                assert device_type == DeviceType.SERVER
        
        with patch('platform.system', return_value='Android'):
            device_type = service._detect_device_type()
            assert device_type == DeviceType.PHONE
    
    @pytest.mark.asyncio
    async def test_detect_capabilities(self):
        """测试能力检测"""
        service = DeviceDiscoveryService(
            config=self.config,
            device_registry=self.device_registry
        )
        
        with patch('platform.system', return_value='Windows'):
            with patch('psutil.disk_usage', return_value=Mock(total=100 * 1024**3)):  # 100GB
                with patch('psutil.virtual_memory', return_value=Mock(total=8 * 1024**3)):  # 8GB
                    capabilities = service._detect_capabilities()
                    
                    # 应该包含基本能力
                    capability_values = [cap.value for cap in capabilities]
                    assert "compute" in capability_values
                    assert "network" in capability_values
    
    @pytest.mark.asyncio
    async def test_start_stop_service(self):
        """测试启动停止服务"""
        # 模拟 zeroconf
        with patch('src.core.discovery.AsyncZeroconf') as mock_zeroconf:
            with patch('src.core.discovery.AsyncServiceInfo') as mock_service_info:
                mock_zeroconf_instance = AsyncMock()
                mock_zeroconf.return_value = mock_zeroconf_instance
                
                mock_service_info_instance = AsyncMock()
                mock_service_info.return_value = mock_service_info_instance
                
                service = DeviceDiscoveryService(
                    config=self.config,
                    device_registry=self.device_registry
                )
                
                # 启动服务
                await service.start()
                
                assert service.is_running
                mock_zeroconf_instance.async_register_service.assert_called_once()
                
                # 停止服务
                await service.stop()
                
                assert not service.is_running
                mock_zeroconf_instance.async_close.assert_called_once()


class TestIntegration:
    """集成测试"""
    
    @pytest.mark.asyncio
    async def test_device_discovery_and_registration(self):
        """测试设备发现和注册集成"""
        config = PAOConfig(device_name="Integration-Test")
        device_registry = DeviceRegistry()
        
        discovered_devices = []
        
        def on_device_discovered(device):
            discovered_devices.append(device)
        
        service = DeviceDiscoveryService(
            config=config,
            device_registry=device_registry,
            on_device_discovered=on_device_discovered
        )
        
        # 手动注册一个模拟设备
        mock_device = DeviceInfo(
            device_id="mock-device-001",
            name="Mock Device",
            device_type=DeviceType.LAPTOP,
            ip_address="192.168.1.50",
            port=8765
        )
        
        device_registry.register_device(mock_device)
        
        # 检查设备是否被注册
        devices = device_registry.list_devices()
        assert len(devices) == 2  # 本地设备 + 模拟设备
        assert discovered_devices == []  # 回调没有被调用，因为是手动注册
        
        # 测试设备查找
        compute_devices = device_registry.find_device_by_capability(DeviceCapability.COMPUTE)
        # 至少应该包含本地设备
        assert len(compute_devices) >= 1


if __name__ == "__main__":
    # 运行所有测试
    pytest.main([__file__, "-v"])