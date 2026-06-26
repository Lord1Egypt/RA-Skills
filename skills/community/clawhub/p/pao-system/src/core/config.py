"""
配置管理模块
管理 PAO 系统的配置和设置
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum

import yaml
from pydantic import BaseModel, Field


class LogLevel(str, Enum):
    """日志级别枚举"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class NetworkMode(str, Enum):
    """网络模式枚举"""
    LAN_ONLY = "lan_only"          # 仅局域网
    P2P_RELAY = "p2p_relay"        # P2P带中继
    CLOUD_SYNC = "cloud_sync"      # 云同步


class PrivacyLevel(str, Enum):
    """隐私级别枚举"""
    MINIMAL = "minimal"           # 最小隐私，共享基本信息
    STANDARD = "standard"         # 标准隐私，加密通信
    STRICT = "strict"             # 严格隐私，本地优先
    MAXIMUM = "maximum"           # 最大隐私，无网络


@dataclass
class NetworkConfig:
    """网络配置"""
    mode: NetworkMode = NetworkMode.LAN_ONLY
    discovery_port: int = 8765
    data_port: int = 8766
    relay_servers: list = field(default_factory=lambda: [
        "relay1.pao-system.dev:8767",
        "relay2.pao-system.dev:8767"
    ])
    max_connections: int = 10
    connection_timeout: int = 30  # 秒
    heartbeat_interval: int = 60  # 秒
    enable_upnp: bool = True
    enable_ipv6: bool = True


@dataclass
class SecurityConfig:
    """安全配置"""
    privacy_level: PrivacyLevel = PrivacyLevel.STANDARD
    encryption_enabled: bool = True
    encryption_algorithm: str = "AES256-GCM"
    require_authentication: bool = True
    authentication_timeout: int = 300  # 秒
    max_auth_attempts: int = 3
    enable_firewall: bool = True
    allowed_networks: list = field(default_factory=lambda: [
        "192.168.0.0/16",
        "10.0.0.0/8",
        "172.16.0.0/12"
    ])


@dataclass
class StorageConfig:
    """存储配置"""
    type: str = "sqlite"  # 存储类型
    path: str = field(default_factory=lambda: str(Path.home() / ".pao" / "data" / "pao.db"))
    data_dir: str = field(default_factory=lambda: str(Path.home() / ".pao" / "data"))
    table_name: str = "memories"
    max_storage_mb: int = 1024  # MB
    backup_enabled: bool = True
    backup_interval: int = 3600  # 秒
    backup_count: int = 7
    compression_enabled: bool = True
    encryption_at_rest: bool = True


@dataclass
class MemoryConfig:
    """记忆系统配置"""
    enable_persistent_memory: bool = True
    memory_ttl_days: int = 30  # 记忆保存天数
    max_memory_items: int = 10000
    memory_compression: bool = True
    enable_semantic_search: bool = True
    semantic_search_threshold: float = 0.7
    enable_context_association: bool = True
    context_window_size: int = 10


@dataclass
class LoggingConfig:
    """日志配置"""
    level: LogLevel = LogLevel.INFO
    enable_file_logging: bool = True
    log_dir: str = field(default_factory=lambda: str(Path.home() / ".pao" / "logs"))
    max_log_size_mb: int = 10
    log_backup_count: int = 5
    enable_json_logs: bool = False
    enable_console_logging: bool = True


@dataclass
class PerformanceConfig:
    """性能配置"""
    max_workers: int = 4
    worker_timeout: int = 300  # 秒
    cache_size_mb: int = 100
    enable_gzip: bool = True
    enable_connection_pooling: bool = True
    pool_size: int = 5
    pool_timeout: int = 30  # 秒


class PAOConfig(BaseModel):
    """PAO 系统主配置"""
    
    # 基本配置
    device_name: str = Field(default_factory=lambda: f"pao-{os.getlogin()}")
    device_id: str = Field(default_factory=lambda: str(hash(os.getlogin() + os.environ.get('COMPUTERNAME', ''))))
    version: str = "0.1.0"
    
    # 子系统配置
    network: NetworkConfig = Field(default_factory=NetworkConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig)
    
    # 功能开关
    enable_discovery: bool = True
    enable_sync: bool = True
    enable_memory_sharing: bool = True
    enable_skill_evolution: bool = False  # 第一阶段不启用
    enable_context_awareness: bool = False  # 第一阶段不启用
    
    # 高级设置
    auto_start: bool = False
    debug_mode: bool = False
    developer_mode: bool = False
    
    class Config:
        json_encoders = {
            # 处理枚举类型
            LogLevel: lambda v: v.value,
            NetworkMode: lambda v: v.value,
            PrivacyLevel: lambda v: v.value
        }


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_dir: Optional[str] = None):
        if config_dir is None:
            config_dir = str(Path.home() / ".pao")
        
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / "config.yaml"
        self.secrets_file = self.config_dir / "secrets.yaml"
        
        # 确保目录存在
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载配置
        self.config = self._load_or_create_config()
        self.secrets = self._load_or_create_secrets()
    
    def _load_or_create_config(self) -> PAOConfig:
        """加载或创建配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f) or {}
                return PAOConfig(**config_data)
            except Exception as e:
                logging.warning(f"加载配置文件失败，使用默认配置: {e}")
                return PAOConfig()
        else:
            config = PAOConfig()
            self.save_config(config)
            return config
    
    def _load_or_create_secrets(self) -> Dict[str, Any]:
        """加载或创建密钥文件"""
        if self.secrets_file.exists():
            try:
                with open(self.secrets_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                logging.warning(f"加载密钥文件失败: {e}")
                return {}
        else:
            secrets = self._generate_default_secrets()
            self.save_secrets(secrets)
            return secrets
    
    def _generate_default_secrets(self) -> Dict[str, Any]:
        """生成默认密钥"""
        import secrets
        import base64
        
        return {
            "encryption_key": base64.b64encode(secrets.token_bytes(32)).decode('utf-8'),
            "auth_token": secrets.token_hex(32),
            "device_secret": secrets.token_hex(16),
            "relay_tokens": {}
        }
    
    def save_config(self, config: Optional[PAOConfig] = None) -> None:
        """保存配置"""
        if config is None:
            config = self.config
        
        # 转换为字典
        config_dict = config.dict()
        
        # 保存到文件
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config_dict, f, default_flow_style=False, allow_unicode=True, indent=2)
        
        logging.info(f"配置已保存到: {self.config_file}")
    
    def save_secrets(self, secrets: Optional[Dict[str, Any]] = None) -> None:
        """保存密钥"""
        if secrets is None:
            secrets = self.secrets
        
        # 保存到文件
        with open(self.secrets_file, 'w', encoding='utf-8') as f:
            yaml.dump(secrets, f, default_flow_style=False, allow_unicode=True)
        
        # 设置文件权限（仅在Unix系统）
        if os.name != 'nt':
            os.chmod(self.secrets_file, 0o600)
        
        logging.info(f"密钥已保存到: {self.secrets_file}")
    
    def update_config(self, updates: Dict[str, Any]) -> PAOConfig:
        """更新配置"""
        # 深度合并更新
        import copy
        
        current_dict = self.config.dict()
        updated_dict = self._deep_merge(current_dict, updates)
        
        # 创建新配置
        self.config = PAOConfig(**updated_dict)
        self.save_config()
        
        return self.config
    
    def _deep_merge(self, base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
        """深度合并字典"""
        result = copy.deepcopy(base)
        
        for key, value in updates.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get_config_path(self, *args) -> Path:
        """获取配置目录下的路径"""
        return self.config_dir.joinpath(*args)
    
    def get_data_path(self, *args) -> Path:
        """获取数据目录下的路径"""
        data_dir = Path(self.config.storage.data_dir)
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir.joinpath(*args)
    
    def get_log_path(self, *args) -> Path:
        """获取日志目录下的路径"""
        log_dir = Path(self.config.logging.log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir.joinpath(*args)
    
    def setup_logging(self) -> None:
        """设置日志系统"""
        import sys
        
        log_config = self.config.logging
        
        # 配置根日志记录器
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, log_config.level.value))
        
        # 清除现有处理器
        root_logger.handlers.clear()
        
        # 控制台处理器
        if log_config.enable_console_logging:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, log_config.level.value))
            console_format = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_format)
            root_logger.addHandler(console_handler)
        
        # 文件处理器
        if log_config.enable_file_logging:
            log_file = self.get_log_path("pao.log")
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(getattr(logging, log_config.level.value))
            
            if log_config.enable_json_logs:
                import json_log_formatter
                formatter = json_log_formatter.JSONFormatter()
            else:
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
            
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)


def load_config(config_dir: Optional[str] = None) -> PAOConfig:
    """快速加载配置"""
    manager = ConfigManager(config_dir)
    return manager.config


def get_config_manager(config_dir: Optional[str] = None) -> ConfigManager:
    """获取配置管理器实例"""
    return ConfigManager(config_dir)


def create_default_config() -> PAOConfig:
    """创建默认配置"""
    return PAOConfig()


if __name__ == "__main__":
    # 测试配置管理
    config = create_default_config()
    print("默认配置:", json.dumps(config.dict(), indent=2, ensure_ascii=False))
    
    # 测试配置管理器
    manager = get_config_manager()
    print(f"配置目录: {manager.config_dir}")
    print(f"设备名称: {manager.config.device_name}")