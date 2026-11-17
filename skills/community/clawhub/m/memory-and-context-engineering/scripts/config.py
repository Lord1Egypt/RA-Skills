"""
Agent Memory System - 统一配置管理

提供集中化的配置管理，支持环境变量覆盖和配置文件加载。
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisConfig(BaseModel):
    """Redis 配置"""
    host: str = Field(default="localhost", description="Redis 主机地址")
    port: int = Field(default=6379, description="Redis 端口")
    db: int = Field(default=0, description="Redis 数据库编号")
    password: Optional[str] = Field(default=None, description="Redis 密码")
    ssl: bool = Field(default=False, description="是否使用 SSL")
    socket_timeout: float = Field(default=5.0, description="Socket 超时时间（秒）")
    max_connections: int = Field(default=20, description="最大连接数")
    
    @property
    def url(self) -> str:
        """生成 Redis URL"""
        scheme = "rediss" if self.ssl else "redis"
        auth = f":{self.password}@" if self.password else ""
        return f"{scheme}://{auth}{self.host}:{self.port}/{self.db}"


class StorageConfig(BaseModel):
    """存储配置"""
    base_path: str = Field(default="./data", description="基础存储路径")
    perception_path: str = Field(default="./data/perception", description="感知记忆存储路径")
    short_term_path: str = Field(default="./data/short_term", description="短期记忆存储路径")
    long_term_path: str = Field(default="./data/long_term", description="长期记忆存储路径")
    state_path: str = Field(default="./data/state", description="状态存储路径")
    backup_path: str = Field(default="./data/backup", description="备份存储路径")


class MemoryConfig(BaseModel):
    """记忆配置"""
    # 感知记忆
    perception_max_capacity: int = Field(default=1000, description="感知记忆最大容量")
    perception_ttl_seconds: int = Field(default=3600, description="感知记忆 TTL（秒）")
    
    # 短期记忆
    short_term_max_capacity: int = Field(default=5000, description="短期记忆最大容量")
    short_term_ttl_seconds: int = Field(default=86400, description="短期记忆 TTL（秒）")
    
    # 长期记忆
    long_term_max_capacity: int = Field(default=50000, description="长期记忆最大容量")
    
    # 压缩配置
    compression_enabled: bool = Field(default=True, description="是否启用压缩")
    compression_ratio: float = Field(default=0.7, description="压缩目标比例")


class LoggingConfig(BaseModel):
    """日志配置"""
    level: str = Field(default="INFO", description="日志级别")
    format: str = Field(default="json", description="日志格式（json/text）")
    output: str = Field(default="stdout", description="日志输出（stdout/file）")
    file_path: Optional[str] = Field(default=None, description="日志文件路径")
    max_bytes: int = Field(default=10 * 1024 * 1024, description="日志文件最大大小")
    backup_count: int = Field(default=5, description="日志文件备份数量")


class PerformanceConfig(BaseModel):
    """性能配置"""
    # 缓存配置
    cache_enabled: bool = Field(default=True, description="是否启用缓存")
    cache_max_size: int = Field(default=1000, description="缓存最大条目数")
    cache_ttl_seconds: int = Field(default=3600, description="缓存 TTL（秒）")
    
    # 批处理配置
    batch_enabled: bool = Field(default=True, description="是否启用批处理")
    batch_size: int = Field(default=100, description="批处理大小")
    batch_timeout_seconds: float = Field(default=5.0, description="批处理超时时间")
    
    # 异步写入配置
    async_write_enabled: bool = Field(default=True, description="是否启用异步写入")
    async_write_queue_size: int = Field(default=10000, description="异步写入队列大小")


class SecurityConfig(BaseModel):
    """安全配置"""
    # 加密配置
    encryption_enabled: bool = Field(default=True, description="是否启用加密")
    encryption_key_path: Optional[str] = Field(default=None, description="加密密钥路径")
    
    # 路径安全
    path_validation_enabled: bool = Field(default=True, description="是否启用路径验证")
    allowed_base_dirs: list = Field(default_factory=list, description="允许的基础目录")
    
    # 隐私配置
    privacy_consent_required: bool = Field(default=True, description="是否需要隐私同意")
    data_retention_days: int = Field(default=365, description="数据保留天数")


class AgentMemoryConfig(BaseSettings):
    """
    Agent Memory System 统一配置
    
    支持环境变量覆盖，环境变量前缀为 AGENT_MEMORY_
    """
    
    model_config = SettingsConfigDict(
        env_prefix="AGENT_MEMORY_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # 子配置
    redis: RedisConfig = Field(default_factory=RedisConfig)
    storage: StorageConfig = Field(default_factory=StorageConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    
    # 全局配置
    debug: bool = Field(default=False, description="是否启用调试模式")
    environment: str = Field(default="development", description="运行环境")
    
    def get_storage_path(self, name: str) -> Path:
        """获取存储路径"""
        path_map = {
            "base": self.storage.base_path,
            "perception": self.storage.perception_path,
            "short_term": self.storage.short_term_path,
            "long_term": self.storage.long_term_path,
            "state": self.storage.state_path,
            "backup": self.storage.backup_path,
        }
        path_str = path_map.get(name, self.storage.base_path)
        path = Path(path_str)
        path.mkdir(parents=True, exist_ok=True)
        return path


# 全局配置实例
_config: Optional[AgentMemoryConfig] = None


def get_config() -> AgentMemoryConfig:
    """获取全局配置实例"""
    global _config
    if _config is None:
        _config = AgentMemoryConfig()
    return _config


def reload_config() -> AgentMemoryConfig:
    """重新加载配置"""
    global _config
    _config = AgentMemoryConfig()
    return _config


def update_config(updates: Dict[str, Any]) -> None:
    """
    更新配置
    
    Args:
        updates: 配置更新字典
    """
    config = get_config()
    for key, value in updates.items():
        if hasattr(config, key):
            setattr(config, key, value)
