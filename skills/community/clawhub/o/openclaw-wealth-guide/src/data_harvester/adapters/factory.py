"""
适配器工厂
用于创建和管理数据源适配器
"""

import logging
from typing import Dict, Type, Optional

from ..config import SourceConfig, DataSourceType
from .base import SourceAdapter, WebAdapter, ApiAdapter, FileAdapter, DatabaseAdapter
from ..exceptions import ConfigurationError

logger = logging.getLogger(__name__)


class AdapterFactory:
    """适配器工厂类"""
    
    # 适配器类型映射
    _adapter_registry: Dict[DataSourceType, Type[SourceAdapter]] = {
        DataSourceType.WEB: WebAdapter,
        DataSourceType.API: ApiAdapter,
        DataSourceType.FILE: FileAdapter,
        DataSourceType.DATABASE: DatabaseAdapter,
    }
    
    # 自定义适配器注册表
    _custom_adapters: Dict[str, Type[SourceAdapter]] = {}
    
    @classmethod
    def create_adapter(cls, config: SourceConfig) -> SourceAdapter:
        """
        创建适配器实例
        
        Args:
            config: 数据源配置
            
        Returns:
            SourceAdapter: 适配器实例
            
        Raises:
            ConfigurationError: 配置错误或适配器类型不支持
        """
        try:
            # 检查配置有效性
            if not config.enabled:
                logger.warning(f"适配器已禁用: {config.name}")
                # 仍然创建实例，但标记为禁用
            
            # 获取适配器类
            adapter_class = cls._get_adapter_class(config.type)
            if adapter_class is None:
                raise ConfigurationError(f"不支持的数据源类型: {config.type}")
            
            # 创建适配器实例
            adapter = adapter_class(config)
            
            # 验证适配器
            if not adapter.validate():
                logger.warning(f"适配器验证警告: {config.name}")
            
            logger.debug(f"创建适配器: {config.name} ({config.type})")
            return adapter
            
        except Exception as e:
            logger.error(f"创建适配器失败 {config.name}: {e}")
            raise ConfigurationError(f"创建适配器失败 {config.name}: {e}") from e
    
    @classmethod
    def _get_adapter_class(cls, source_type: DataSourceType) -> Optional[Type[SourceAdapter]]:
        """
        获取适配器类
        
        Args:
            source_type: 数据源类型
            
        Returns:
            适配器类，如果找不到则返回None
        """
        # 首先检查自定义适配器
        if source_type.value in cls._custom_adapters:
            return cls._custom_adapters[source_type.value]
        
        # 检查内置适配器
        return cls._adapter_registry.get(source_type)
    
    @classmethod
    def register_adapter(cls, source_type: DataSourceType, adapter_class: Type[SourceAdapter]) -> None:
        """
        注册自定义适配器
        
        Args:
            source_type: 数据源类型
            adapter_class: 适配器类
        """
        if not issubclass(adapter_class, SourceAdapter):
            raise ValueError(f"适配器类必须继承自 SourceAdapter: {adapter_class}")
        
        cls._custom_adapters[source_type.value] = adapter_class
        logger.info(f"注册自定义适配器: {source_type} -> {adapter_class.__name__}")
    
    @classmethod
    def unregister_adapter(cls, source_type: DataSourceType) -> None:
        """
        注销自定义适配器
        
        Args:
            source_type: 数据源类型
        """
        if source_type.value in cls._custom_adapters:
            del cls._custom_adapters[source_type.value]
            logger.info(f"注销自定义适配器: {source_type}")
    
    @classmethod
    def list_available_adapters(cls) -> Dict[str, str]:
        """
        列出可用的适配器
        
        Returns:
            适配器类型和类名的映射
        """
        adapters = {}
        
        # 内置适配器
        for source_type, adapter_class in cls._adapter_registry.items():
            adapters[source_type.value] = adapter_class.__name__
        
        # 自定义适配器
        for source_type, adapter_class in cls._custom_adapters.items():
            adapters[source_type] = adapter_class.__name__
        
        return adapters
    
    @classmethod
    def get_adapter_info(cls, source_type: DataSourceType) -> Dict[str, str]:
        """
        获取适配器信息
        
        Args:
            source_type: 数据源类型
            
        Returns:
            适配器信息
        """
        adapter_class = cls._get_adapter_class(source_type)
        if adapter_class is None:
            return {"type": source_type.value, "available": False}
        
        return {
            "type": source_type.value,
            "available": True,
            "class_name": adapter_class.__name__,
            "module": adapter_class.__module__,
            "description": adapter_class.__doc__ or "无描述"
        }
    
    @classmethod
    def create_adapters_from_configs(cls, configs: Dict[str, SourceConfig]) -> Dict[str, SourceAdapter]:
        """
        从配置字典批量创建适配器
        
        Args:
            configs: 配置字典，键为适配器名称，值为配置
            
        Returns:
            适配器字典
        """
        adapters = {}
        
        for name, config in configs.items():
            try:
                adapter = cls.create_adapter(config)
                adapters[name] = adapter
                logger.info(f"创建适配器成功: {name}")
            except Exception as e:
                logger.error(f"创建适配器失败 {name}: {e}")
                # 根据配置决定是否抛出异常
                if config.strict_mode:
                    raise
        
        return adapters
    
    @classmethod
    def validate_adapter_config(cls, config: SourceConfig) -> Dict[str, Any]:
        """
        验证适配器配置
        
        Args:
            config: 数据源配置
            
        Returns:
            验证结果
        """
        import inspect
        
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "required_fields": [],
            "optional_fields": []
        }
        
        try:
            # 基本验证
            if not config.name:
                result["valid"] = False
                result["errors"].append("适配器名称不能为空")
            
            if not config.type:
                result["valid"] = False
                result["errors"].append("适配器类型不能为空")
            
            # 类型特定验证
            adapter_class = cls._get_adapter_class(config.type)
            if adapter_class:
                # 获取适配器类的参数信息
                init_signature = inspect.signature(adapter_class.__init__)
                
                # 这里可以添加更详细的验证逻辑
                # 例如检查特定类型必需的字段
                if config.type == DataSourceType.WEB and not config.url:
                    result["warnings"].append("Web适配器建议配置URL")
                
                if config.type == DataSourceType.FILE and not config.path:
                    result["errors"].append("文件适配器必须配置路径")
                    result["valid"] = False
                    
            else:
                result["valid"] = False
                result["errors"].append(f"不支持的数据源类型: {config.type}")
            
            # 检查提取规则（如果提供）
            if config.extract_rules:
                if not isinstance(config.extract_rules, dict):
                    result["warnings"].append("提取规则应该是字典格式")
            
            # 检查认证信息
            if config.auth:
                if not isinstance(config.auth, dict):
                    result["warnings"].append("认证信息应该是字典格式")
            
            # 检查超时设置
            if config.timeout <= 0:
                result["warnings"].append(f"超时时间应该大于0，当前值: {config.timeout}")
            
            # 检查重试次数
            if config.retry_count < 0:
                result["warnings"].append(f"重试次数应该大于等于0，当前值: {config.retry_count}")
            
        except Exception as e:
            result["valid"] = False
            result["errors"].append(f"配置验证异常: {e}")
        
        return result