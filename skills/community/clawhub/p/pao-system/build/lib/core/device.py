"""
设备模型定义
定义 PAO 系统中的设备实体和状态
"""

import uuid
import socket
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass, field
from pydantic import BaseModel, Field


class DeviceType(str, Enum):
    """设备类型枚举"""
    DESKTOP = "desktop"
    LAPTOP = "laptop"
    PHONE = "phone"
    TABLET = "tablet"
    SERVER = "server"
    IOT = "iot"
    UNKNOWN = "unknown"


class DeviceStatus(str, Enum):
    """设备状态枚举"""
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    IDLE = "idle"
    SLEEPING = "sleeping"


class DeviceCapability(str, Enum):
    """设备能力枚举"""
    COMPUTE = "compute"          # 计算能力
    STORAGE = "storage"          # 存储能力
    MEMORY = "memory"           # 记忆存储
    DISPLAY = "display"         # 显示能力
    INPUT = "input"             # 输入能力
    NETWORK = "network"         # 网络能力
    SENSORS = "sensors"         # 传感器能力


@dataclass
class DeviceInfo:
    """设备基本信息"""
    device_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Unknown Device"
    device_type: DeviceType = DeviceType.UNKNOWN
    hostname: str = field(default_factory=socket.gethostname)
    ip_address: str = field(default_factory=lambda: socket.gethostbyname(socket.gethostname()))
    mac_address: str = ""
    os_name: str = ""
    os_version: str = ""
    
    # 设备能力
    capabilities: List[DeviceCapability] = field(default_factory=list)
    
    # 资源信息
    cpu_cores: int = 0
    memory_gb: int = 0
    storage_gb: int = 0
    
    # 网络信息
    port: int = 8765  # 默认通信端口
    protocol_version: str = "1.0.0"
    
    # 元数据
    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "device_id": self.device_id,
            "name": self.name,
            "device_type": self.device_type.value,
            "hostname": self.hostname,
            "ip_address": self.ip_address,
            "mac_address": self.mac_address,
            "os_name": self.os_name,
            "os_version": self.os_version,
            "capabilities": [cap.value for cap in self.capabilities],
            "cpu_cores": self.cpu_cores,
            "memory_gb": self.memory_gb,
            "storage_gb": self.storage_gb,
            "port": self.port,
            "protocol_version": self.protocol_version,
            "first_seen": self.first_seen.isoformat(),
            "last_seen": self.last_seen.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeviceInfo":
        """从字典创建"""
        device = cls()
        device.device_id = data.get("device_id", device.device_id)
        device.name = data.get("name", device.name)
        device.device_type = DeviceType(data.get("device_type", DeviceType.UNKNOWN.value))
        device.hostname = data.get("hostname", device.hostname)
        device.ip_address = data.get("ip_address", device.ip_address)
        device.mac_address = data.get("mac_address", device.mac_address)
        device.os_name = data.get("os_name", device.os_name)
        device.os_version = data.get("os_version", device.os_version)
        
        # 处理能力列表
        capabilities = data.get("capabilities", [])
        device.capabilities = [DeviceCapability(cap) for cap in capabilities]
        
        device.cpu_cores = data.get("cpu_cores", device.cpu_cores)
        device.memory_gb = data.get("memory_gb", device.memory_gb)
        device.storage_gb = data.get("storage_gb", device.storage_gb)
        device.port = data.get("port", device.port)
        device.protocol_version = data.get("protocol_version", device.protocol_version)
        
        # 时间戳
        if "first_seen" in data:
            device.first_seen = datetime.fromisoformat(data["first_seen"])
        if "last_seen" in data:
            device.last_seen = datetime.fromisoformat(data["last_seen"])
        
        return device
    
    def update_last_seen(self):
        """更新最后出现时间"""
        self.last_seen = datetime.now()
    
    def get_capability_score(self, capability: DeviceCapability) -> int:
        """获取设备特定能力的评分"""
        if capability not in self.capabilities:
            return 0
        
        # 根据能力类型和设备规格打分
        scores = {
            DeviceCapability.COMPUTE: self.cpu_cores * 100,
            DeviceCapability.STORAGE: self.storage_gb * 10,
            DeviceCapability.MEMORY: self.memory_gb * 50,
            DeviceCapability.DISPLAY: 100 if DeviceCapability.DISPLAY in self.capabilities else 0,
            DeviceCapability.INPUT: 80 if DeviceCapability.INPUT in self.capabilities else 0,
            DeviceCapability.NETWORK: 150,
            DeviceCapability.SENSORS: 50 if DeviceCapability.SENSORS in self.capabilities else 0,
        }
        
        return scores.get(capability, 0)


class DeviceState(BaseModel):
    """设备状态信息"""
    device_id: str
    status: DeviceStatus = DeviceStatus.ONLINE
    current_load: float = 0.0  # 0-1 表示负载程度
    available_memory_mb: int = 0
    available_storage_mb: int = 0
    network_latency_ms: int = 0
    active_connections: int = 0
    last_heartbeat: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class DeviceRegistry:
    """设备注册表，管理已知设备"""
    
    def __init__(self):
        self.devices: Dict[str, DeviceInfo] = {}
        self.device_states: Dict[str, DeviceState] = {}
    
    def register_device(self, device: DeviceInfo) -> None:
        """注册新设备"""
        self.devices[device.device_id] = device
        self.device_states[device.device_id] = DeviceState(
            device_id=device.device_id,
            status=DeviceStatus.ONLINE
        )
    
    def unregister_device(self, device_id: str) -> None:
        """注销设备"""
        if device_id in self.devices:
            del self.devices[device_id]
        if device_id in self.device_states:
            del self.device_states[device_id]
    
    def update_device_state(self, device_id: str, state: DeviceState) -> None:
        """更新设备状态"""
        if device_id in self.device_states:
            self.device_states[device_id] = state
    
    def get_device(self, device_id: str) -> Optional[DeviceInfo]:
        """获取设备信息"""
        return self.devices.get(device_id)
    
    def get_device_state(self, device_id: str) -> Optional[DeviceState]:
        """获取设备状态"""
        return self.device_states.get(device_id)
    
    def list_devices(self) -> List[DeviceInfo]:
        """列出所有设备"""
        return list(self.devices.values())
    
    def list_online_devices(self) -> List[DeviceInfo]:
        """列出在线设备"""
        online_devices = []
        for device_id, state in self.device_states.items():
            if state.status == DeviceStatus.ONLINE and device_id in self.devices:
                online_devices.append(self.devices[device_id])
        return online_devices
    
    def find_device_by_capability(self, capability: DeviceCapability) -> List[DeviceInfo]:
        """根据能力查找设备"""
        return [
            device for device in self.devices.values()
            if capability in device.capabilities
        ]
    
    def cleanup_offline_devices(self, timeout_seconds: int = 300) -> None:
        """清理离线超时的设备"""
        now = datetime.now()
        to_remove = []
        
        for device_id, state in self.device_states.items():
            time_since_heartbeat = (now - state.last_heartbeat).total_seconds()
            if time_since_heartbeat > timeout_seconds:
                to_remove.append(device_id)
        
        for device_id in to_remove:
            self.unregister_device(device_id)