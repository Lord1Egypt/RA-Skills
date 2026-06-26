"""
配置管理模块
使用Pydantic进行配置验证
"""

import yaml
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime

try:
    from pydantic import BaseModel, Field, validator, root_validator
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    # 回退方案
    class BaseModel:
        def __init__(self, **data):
            for key, value in data.items():
                setattr(self, key, value)
    
    def Field(default=..., **kwargs):
        return default
    
    def validator(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    
    def root_validator(*args, **kwargs):
        def decorator(func):
            return func
        return decorator


class DataSourceType(str, Enum):
    """数据源类型"""
    WEB = "web"
    API = "api"
    FILE = "file"
    DATABASE = "database"
    CUSTOM = "custom"


class ExportFormat(str, Enum):
    """导出格式"""
    CSV = "csv"
    EXCEL = "excel"
    JSON = "json"
    XML = "xml"
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MONGO = "mongo"


class ProcessingStrategy(str, Enum):
    """处理策略"""
    CLEAN = "clean"
    TRANSFORM = "transform"
    ENRICH = "enrich"
    VALIDATE = "validate"
    DEDUPLICATE = "deduplicate"


if PYDANTIC_AVAILABLE:
    class SourceConfig(BaseModel):
        """数据源配置"""
        name: str = Field(..., description="数据源名称")
        type: DataSourceType = Field(..., description="数据源类型")
        enabled: bool = Field(True, description="是否启用")
        
        # 类型特定配置
        url: Optional[str] = Field(None, description="URL地址（Web/API类型）")
        path: Optional[str] = Field(None, description="文件路径（File类型）")
        connection_string: Optional[str] = Field(None, description="数据库连接字符串")
        query: Optional[str] = Field(None, description="查询语句/选择器")
        
        # 认证信息
        auth: Optional[Dict[str, Any]] = Field(None, description="认证信息")
        
        # 请求配置
        headers: Optional[Dict[str, str]] = Field(None, description="HTTP头信息")
        params: Optional[Dict[str, Any]] = Field(None, description="请求参数")
        
        # 提取规则
        extract_rules: Optional[Dict[str, Any]] = Field(None, description="数据提取规则")
        
        # 调度配置
        schedule: Optional[str] = Field(None, description="调度表达式（Cron格式）")
        timeout: int = Field(30, description="超时时间（秒）")
        retry_count: int = Field(3, description="重试次数")
        
        # 高级配置
        options: Dict[str, Any] = Field(default_factory=dict, description="高级选项")
        
        class Config:
            use_enum_values = True
        
        @validator('schedule')
        def validate_schedule(cls, v):
            if v and not cls._is_valid_cron(v):
                raise ValueError(f"无效的Cron表达式: {v}")
            return v
        
        @staticmethod
        def _is_valid_cron(cron_expr: str) -> bool:
            """简单的Cron表达式验证"""
            parts = cron_expr.split()
            return len(parts) == 5
        
    class ProcessingConfig(BaseModel):
        """处理配置"""
        enabled: bool = Field(True, description="是否启用处理")
        strategy: List[ProcessingStrategy] = Field(
            default_factory=lambda: [ProcessingStrategy.CLEAN],
            description="处理策略列表"
        )
        
        # 清洗配置
        clean_options: Dict[str, Any] = Field(
            default_factory=lambda: {
                "remove_duplicates": True,
                "remove_null": True,
                "trim_whitespace": True
            },
            description="数据清洗选项"
        )
        
        # 转换配置
        transform_options: Dict[str, Any] = Field(
            default_factory=lambda: {
                "date_format": "%Y-%m-%d",
                "number_precision": 2,
                "encoding": "utf-8"
            },
            description="数据转换选项"
        )
        
        # 验证配置
        validation_rules: Optional[Dict[str, Any]] = Field(None, description="数据验证规则")
        
        # 去重配置
        deduplicate_fields: Optional[List[str]] = Field(None, description="去重字段")
        
        class Config:
            use_enum_values = True
    
    class ExportConfig(BaseModel):
        """导出配置"""
        name: str = Field(..., description="导出器名称")
        format: ExportFormat = Field(..., description="导出格式")
        enabled: bool = Field(True, description="是否启用")
        
        # 输出目标
        output_path: Optional[str] = Field(None, description="输出路径")
        table_name: Optional[str] = Field(None, description="表名（数据库导出）")
        connection_string: Optional[str] = Field(None, description="数据库连接字符串")
        
        # 格式特定配置
        options: Dict[str, Any] = Field(default_factory=dict, description="格式选项")
        
        # 调度配置
        auto_export: bool = Field(False, description="是否自动导出")
        export_schedule: Optional[str] = Field(None, description="导出调度")
        
        class Config:
            use_enum_values = True
    
    class SchedulerConfig(BaseModel):
        """调度器配置"""
        enabled: bool = Field(False, description="是否启用调度器")
        timezone: str = Field("Asia/Shanghai", description="时区")
        max_workers: int = Field(4, description="最大工作线程数")
        job_store: str = Field("memory", description="任务存储类型")
        
        # 监控配置
        monitor_interval: int = Field(60, description="监控间隔（秒）")
        log_level: str = Field("INFO", description="日志级别")
        
        class Config:
            use_enum_values = True
    
    class Config(BaseModel):
        """主配置类"""
        
        # 基本信息
        name: str = Field("Data Harvester", description="采集器名称")
        version: str = Field("1.0.0", description="版本号")
        description: Optional[str] = Field(None, description="描述")
        
        # 数据源配置
        sources: Dict[str, SourceConfig] = Field(default_factory=dict, description="数据源配置")
        
        # 处理配置
        processing: ProcessingConfig = Field(
            default_factory=ProcessingConfig,
            description="处理配置"
        )
        
        # 导出配置
        exports: List[ExportConfig] = Field(default_factory=list, description="导出配置")
        
        # 调度配置
        scheduler: SchedulerConfig = Field(
            default_factory=SchedulerConfig,
            description="调度器配置"
        )
        
        # 系统配置
        strict_mode: bool = Field(False, description="严格模式（错误时抛出异常）")
        log_level: str = Field("INFO", description="日志级别")
        cache_enabled: bool = Field(True, description="是否启用缓存")
        cache_ttl: int = Field(3600, description="缓存过期时间（秒）")
        
        # 性能配置
        max_concurrent: int = Field(5, description="最大并发数")
        request_delay: float = Field(1.0, description="请求延迟（秒）")
        
        # 高级配置
        plugins: List[str] = Field(default_factory=list, description="插件列表")
        custom_settings: Dict[str, Any] = Field(default_factory=dict, description="自定义设置")
        
        class Config:
            use_enum_values = True
        
        @classmethod
        def load(cls, config_path: Optional[str] = None) -> 'Config':
            """
            从文件加载配置
            
            Args:
                config_path: 配置文件路径
                
            Returns:
                Config: 配置实例
            """
            if config_path is None:
                # 使用默认配置
                return cls()
            
            path = Path(config_path)
            if not path.exists():
                raise FileNotFoundError(f"配置文件不存在: {config_path}")
            
            # 根据扩展名选择加载方式
            if path.suffix in ['.yaml', '.yml']:
                with open(path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
            elif path.suffix == '.json':
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                raise ValueError(f"不支持的配置文件格式: {path.suffix}")
            
            return cls(**data)
        
        def save(self, config_path: str) -> None:
            """
            保存配置到文件
            
            Args:
                config_path: 配置文件路径
            """
            path = Path(config_path)
            
            # 根据扩展名选择保存方式
            if path.suffix in ['.yaml', '.yml']:
                with open(path, 'w', encoding='utf-8') as f:
                    yaml.dump(self.dict(), f, default_flow_style=False, allow_unicode=True)
            elif path.suffix == '.json':
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(self.dict(), f, ensure_ascii=False, indent=2)
            else:
                raise ValueError(f"不支持的配置文件格式: {path.suffix}")
            
        def dict(self) -> Dict[str, Any]:
            """转换为字典格式"""
            return super().dict(exclude_none=True)
        
else:
    # Pydantic不可用时的简化版本
    class SourceConfig:
        def __init__(self, **kwargs):
            self.name = kwargs.get('name', '')
            self.type = kwargs.get('type', DataSourceType.WEB)
            self.enabled = kwargs.get('enabled', True)
            self.url = kwargs.get('url')
            self.path = kwargs.get('path')
            self.connection_string = kwargs.get('connection_string')
            self.query = kwargs.get('query')
            self.auth = kwargs.get('auth')
            self.headers = kwargs.get('headers')
            self.params = kwargs.get('params')
            self.extract_rules = kwargs.get('extract_rules')
            self.schedule = kwargs.get('schedule')
            self.timeout = kwargs.get('timeout', 30)
            self.retry_count = kwargs.get('retry_count', 3)
            self.options = kwargs.get('options', {})
    
    class ProcessingConfig:
        def __init__(self, **kwargs):
            self.enabled = kwargs.get('enabled', True)
            self.strategy = kwargs.get('strategy', [ProcessingStrategy.CLEAN])
            self.clean_options = kwargs.get('clean_options', {
                "remove_duplicates": True,
                "remove_null": True,
                "trim_whitespace": True
            })
            self.transform_options = kwargs.get('transform_options', {
                "date_format": "%Y-%m-%d",
                "number_precision": 2,
                "encoding": "utf-8"
            })
            self.validation_rules = kwargs.get('validation_rules')
            self.deduplicate_fields = kwargs.get('deduplicate_fields')
    
    class ExportConfig:
        def __init__(self, **kwargs):
            self.name = kwargs.get('name', '')
            self.format = kwargs.get('format', ExportFormat.CSV)
            self.enabled = kwargs.get('enabled', True)
            self.output_path = kwargs.get('output_path')
            self.table_name = kwargs.get('table_name')
            self.connection_string = kwargs.get('connection_string')
            self.options = kwargs.get('options', {})
            self.auto_export = kwargs.get('auto_export', False)
            self.export_schedule = kwargs.get('export_schedule')
    
    class SchedulerConfig:
        def __init__(self, **kwargs):
            self.enabled = kwargs.get('enabled', False)
            self.timezone = kwargs.get('timezone', 'Asia/Shanghai')
            self.max_workers = kwargs.get('max_workers', 4)
            self.job_store = kwargs.get('job_store', 'memory')
            self.monitor_interval = kwargs.get('monitor_interval', 60)
            self.log_level = kwargs.get('log_level', 'INFO')
    
    class Config:
        def __init__(self, **kwargs):
            self.name = kwargs.get('name', 'Data Harvester')
            self.version = kwargs.get('version', '1.0.0')
            self.description = kwargs.get('description')
            self.sources = kwargs.get('sources', {})
            self.processing = ProcessingConfig(**kwargs.get('processing', {}))
            self.exports = [ExportConfig(**e) for e in kwargs.get('exports', [])]
            self.scheduler = SchedulerConfig(**kwargs.get('scheduler', {}))
            self.strict_mode = kwargs.get('strict_mode', False)
            self.log_level = kwargs.get('log_level', 'INFO')
            self.cache_enabled = kwargs.get('cache_enabled', True)
            self.cache_ttl = kwargs.get('cache_ttl', 3600)
            self.max_concurrent = kwargs.get('max_concurrent', 5)
            self.request_delay = kwargs.get('request_delay', 1.0)
            self.plugins = kwargs.get('plugins', [])
            self.custom_settings = kwargs.get('custom_settings', {})
        
        @classmethod
        def load(cls, config_path: Optional[str] = None) -> 'Config':
            if config_path is None:
                return cls()
            
            path = Path(config_path)
            if not path.exists():
                raise FileNotFoundError(f"配置文件不存在: {config_path}")
            
            if path.suffix in ['.yaml', '.yml']:
                with open(path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
            elif path.suffix == '.json':
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                raise ValueError(f"不支持的配置文件格式: {path.suffix}")
            
            return cls(**data)
        
        def save(self, config_path: str) -> None:
            path = Path(config_path)
            data = self._to_dict()
            
            if path.suffix in ['.yaml', '.yml']:
                with open(path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            elif path.suffix == '.json':
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                raise ValueError(f"不支持的配置文件格式: {path.suffix}")
        
        def _to_dict(self) -> Dict[str, Any]:
            """转换为字典（简化版本）"""
            return {
                'name': self.name,
                'version': self.version,
                'description': self.description,
                'sources': self.sources,
                'processing': self.processing.__dict__,
                'exports': [e.__dict__ for e in self.exports],
                'scheduler': self.scheduler.__dict__,
                'strict_mode': self.strict_mode,
                'log_level': self.log_level,
                'cache_enabled': self.cache_enabled,
                'cache_ttl': self.cache_ttl,
                'max_concurrent': self.max_concurrent,
                'request_delay': self.request_delay,
                'plugins': self.plugins,
                'custom_settings': self.custom_settings
            }