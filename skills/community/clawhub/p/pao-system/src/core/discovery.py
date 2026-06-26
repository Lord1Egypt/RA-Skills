"""
设备发现服务
使用 Zeroconf 实现局域网内的设备自动发现
"""

import asyncio
import socket
import logging
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
from contextlib import asynccontextmanager

import zeroconf
from zeroconf.asyncio import AsyncZeroconf, AsyncServiceInfo, AsyncServiceBrowser

from .device import DeviceInfo, DeviceType, DeviceCapability
from .config import PAOConfig

logger = logging.getLogger(__name__)


@dataclass
class DiscoveryConfig:
    """发现服务配置"""
    service_type: str = "_pao._tcp.local."
    service_name: str = "pao-device"
    domain: str = "local."
    port: int = 8765
    scan_interval: int = 30  # 扫描间隔（秒）
    timeout: int = 10  # 发现超时（秒）
    retry_count: int = 3  # 重试次数


class DeviceDiscoveryService:
    """设备发现服务"""
    
    def __init__(
        self,
        config: PAOConfig,
        device_registry,
        on_device_discovered: Optional[Callable[[DeviceInfo], None]] = None,
        on_device_lost: Optional[Callable[[str], None]] = None
    ):
        self.config = config
        self.device_registry = device_registry
        self.on_device_discovered = on_device_discovered
        self.on_device_lost = on_device_lost
        
        self.discovery_config = DiscoveryConfig()
        self.zeroconf: Optional[AsyncZeroconf] = None
        self.service_browser: Optional[AsyncServiceBrowser] = None
        self.service_info: Optional[AsyncServiceInfo] = None
        
        # 运行状态
        self.is_running = False
        self.discovery_task: Optional[asyncio.Task] = None
        
        # 本地设备信息
        self.local_device = self._create_local_device_info()
    
    def _create_local_device_info(self) -> DeviceInfo:
        """创建本地设备信息"""
        device = DeviceInfo()
        device.name = self.config.device_name
        device.device_type = self._detect_device_type()
        device.capabilities = self._detect_capabilities()
        
        # 获取系统信息
        import platform
        import psutil
        
        device.os_name = platform.system()
        device.os_version = platform.version()
        device.cpu_cores = psutil.cpu_count(logical=False) or 1
        device.memory_gb = psutil.virtual_memory().total // (1024**3)
        
        # 存储信息
        try:
            device.storage_gb = psutil.disk_usage('/').total // (1024**3)
        except:
            device.storage_gb = 0
        
        # MAC地址
        try:
            import uuid
            device.mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                                         for elements in range(0, 8*6, 8)][::-1])
        except:
            device.mac_address = "unknown"
        
        return device
    
    def _detect_device_type(self) -> DeviceType:
        """检测设备类型"""
        import platform
        
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        if "linux" in system:
            # 可能是服务器或IoT
            if "arm" in machine or "aarch" in machine:
                return DeviceType.IOT
            else:
                return DeviceType.SERVER
        elif "windows" in system or "darwin" in system:
            # 桌面设备
            if "laptop" in platform.node().lower():
                return DeviceType.LAPTOP
            return DeviceType.DESKTOP
        elif "android" in system:
            return DeviceType.PHONE
        elif "ios" in system:
            return DeviceType.TABLET
        else:
            return DeviceType.UNKNOWN
    
    def _detect_capabilities(self) -> list:
        """检测设备能力"""
        capabilities = []
        
        # 所有设备都有计算和网络能力
        capabilities.append(DeviceCapability.COMPUTE)
        capabilities.append(DeviceCapability.NETWORK)
        
        import platform
        import psutil
        
        # 存储能力
        if psutil.disk_usage('/').total > 0:
            capabilities.append(DeviceCapability.STORAGE)
        
        # 内存能力
        if psutil.virtual_memory().total > 0:
            capabilities.append(DeviceCapability.MEMORY)
        
        # 显示能力（根据平台判断）
        system = platform.system().lower()
        if system in ['windows', 'darwin', 'linux']:
            # 尝试检测是否有显示
            try:
                import os
                if 'DISPLAY' in os.environ or system != 'linux':
                    capabilities.append(DeviceCapability.DISPLAY)
                    capabilities.append(DeviceCapability.INPUT)
            except:
                pass
        
        return capabilities
    
    async def start(self) -> None:
        """启动发现服务"""
        if self.is_running:
            logger.warning("发现服务已经在运行")
            return
        
        logger.info(f"启动设备发现服务: {self.local_device.name}")
        
        # 创建 Zeroconf 实例
        self.zeroconf = AsyncZeroconf()
        
        # 注册本地服务
        await self._register_service()
        
        # 启动服务浏览器
        await self._start_browser()
        
        # 设置运行状态
        self.is_running = True
        
        # 启动定期扫描任务
        self.discovery_task = asyncio.create_task(self._periodic_discovery())
        
        logger.info("设备发现服务启动完成")
    
    async def stop(self) -> None:
        """停止发现服务"""
        if not self.is_running:
            return
        
        logger.info("停止设备发现服务")
        
        # 取消定期任务
        if self.discovery_task and not self.discovery_task.done():
            self.discovery_task.cancel()
            try:
                await self.discovery_task
            except asyncio.CancelledError:
                pass
        
        # 取消服务注册
        if self.service_info and self.zeroconf:
            await self.zeroconf.async_unregister_service(self.service_info)
        
        # 关闭浏览器
        if self.service_browser:
            self.service_browser.cancel()
        
        # 关闭 Zeroconf
        if self.zeroconf:
            await self.zeroconf.async_close()
        
        self.is_running = False
        logger.info("设备发现服务已停止")
    
    async def _register_service(self) -> None:
        """注册本地设备服务"""
        service_type = self.discovery_config.service_type
        service_name = f"{self.local_device.name}.{service_type}"
        
        # 服务属性
        properties = self.local_device.to_dict()
        
        # 创建服务信息
        self.service_info = AsyncServiceInfo(
            service_type,
            service_name,
            addresses=[socket.inet_aton(self.local_device.ip_address)],
            port=self.discovery_config.port,
            properties=properties,
            server=f"{self.local_device.hostname}.local."
        )
        
        # 注册服务
        if self.zeroconf:
            await self.zeroconf.async_register_service(self.service_info)
            logger.info(f"已注册服务: {service_name}")
    
    async def _start_browser(self) -> None:
        """启动服务浏览器"""
        if not self.zeroconf:
            return
        
        # 创建浏览器回调
        listener = self._create_service_listener()
        
        # 启动浏览器
        self.service_browser = AsyncServiceBrowser(
            self.zeroconf.zeroconf,
            self.discovery_config.service_type,
            listener
        )
        
        logger.info("服务浏览器已启动")
    
    def _create_service_listener(self):
        """创建服务监听器"""
        class ServiceListener:
            def __init__(self, discovery_service):
                self.discovery_service = discovery_service
            
            def add_service(self, zeroconf, service_type, name):
                asyncio.create_task(
                    self.discovery_service._on_service_added(zeroconf, service_type, name)
                )
            
            def remove_service(self, zeroconf, service_type, name):
                asyncio.create_task(
                    self.discovery_service._on_service_removed(zeroconf, service_type, name)
                )
            
            def update_service(self, zeroconf, service_type, name):
                asyncio.create_task(
                    self.discovery_service._on_service_updated(zeroconf, service_type, name)
                )
        
        return ServiceListener(self)
    
    async def _on_service_added(self, zeroconf, service_type, name) -> None:
        """处理服务添加事件"""
        logger.info(f"发现新服务: {name}")
        
        # 获取服务信息
        info = await AsyncServiceInfo.async_from_zeroconf(zeroconf, service_type, name)
        if info:
            await self._process_service_info(info)
    
    async def _on_service_removed(self, zeroconf, service_type, name) -> None:
        """处理服务移除事件"""
        logger.info(f"服务移除: {name}")
        
        # 从设备ID中提取设备ID
        device_id = name.split('.')[0]
        
        # 通知设备丢失
        if self.on_device_lost:
            self.on_device_lost(device_id)
    
    async def _on_service_updated(self, zeroconf, service_type, name) -> None:
        """处理服务更新事件"""
        logger.debug(f"服务更新: {name}")
        
        # 重新获取服务信息
        info = await AsyncServiceInfo.async_from_zeroconf(zeroconf, service_type, name)
        if info:
            await self._process_service_info(info)
    
    async def _process_service_info(self, info: AsyncServiceInfo) -> None:
        """处理服务信息"""
        try:
            # 解析设备信息
            properties = info.properties or {}
            
            # 转换为设备信息
            device_info = DeviceInfo.from_dict({
                **properties,
                "ip_address": socket.inet_ntoa(info.addresses[0]) if info.addresses else "0.0.0.0",
                "port": info.port,
                "hostname": info.server.rstrip('.local.')
            })
            
            # 更新最后出现时间
            device_info.update_last_seen()
            
            # 注册设备
            self.device_registry.register_device(device_info)
            
            logger.info(f"发现设备: {device_info.name} ({device_info.device_type.value})")
            
            # 通知回调
            if self.on_device_discovered:
                self.on_device_discovered(device_info)
                
        except Exception as e:
            logger.error(f"处理服务信息失败: {e}")
    
    async def _periodic_discovery(self) -> None:
        """定期发现任务"""
        while self.is_running:
            try:
                await asyncio.sleep(self.discovery_config.scan_interval)
                
                # 主动扫描
                await self._active_scan()
                
                # 清理离线设备
                self.device_registry.cleanup_offline_devices()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"定期发现任务出错: {e}")
    
    async def _active_scan(self) -> None:
        """主动扫描网络中的设备"""
        if not self.zeroconf:
            return
        
        # 使用 Zeroconf 主动查询服务
        try:
            services = await self.zeroconf.async_get_service_info(
                self.discovery_config.service_type,
                f"{self.local_device.name}.{self.discovery_config.service_type}"
            )
            
            if services:
                await self._process_service_info(services)
                
        except Exception as e:
            logger.debug(f"主动扫描出错: {e}")
    
    async def discover_devices(self, timeout: Optional[int] = None) -> list:
        """主动发现设备（阻塞方式）"""
        if timeout is None:
            timeout = self.discovery_config.timeout
        
        # 记录当前设备数量
        initial_count = len(self.device_registry.list_devices())
        
        # 等待一段时间
        await asyncio.sleep(timeout)
        
        # 返回新发现的设备
        current_count = len(self.device_registry.list_devices())
        new_devices = current_count - initial_count
        
        logger.info(f"发现 {new_devices} 个新设备")
        return self.device_registry.list_devices()


@asynccontextmanager
async def discovery_service(config: PAOConfig, device_registry):
    """发现服务的上下文管理器"""
    service = DeviceDiscoveryService(config, device_registry)
    try:
        await service.start()
        yield service
    finally:
        await service.stop()


async def demo_discovery():
    """演示设备发现功能"""
    from .config import load_config
    
    config = load_config()
    from .device import DeviceRegistry
    
    device_registry = DeviceRegistry()
    
    # 创建设备发现服务
    async with discovery_service(config, device_registry) as service:
        print(f"本地设备: {service.local_device.name}")
        print("开始发现设备...")
        
        # 等待10秒发现设备
        devices = await service.discover_devices(timeout=10)
        
        print(f"\n发现 {len(devices)} 个设备:")
        for device in devices:
            print(f"  - {device.name} ({device.device_type.value}) "
                  f"[{device.ip_address}:{device.port}]")
        
        # 保持运行
        print("\n按 Ctrl+C 停止...")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("停止发现服务")


if __name__ == "__main__":
    import asyncio
    asyncio.run(demo_discovery())