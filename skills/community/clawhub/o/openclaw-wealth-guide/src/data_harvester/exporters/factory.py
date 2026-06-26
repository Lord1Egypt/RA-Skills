"""
导出器工厂
用于创建和管理数据导出器
"""

import logging
from typing import Dict, Type, Optional, Any

from ..config import ExportFormat
from .base import Exporter, CsvExporter, JsonExporter, ExcelExporter
from ..exceptions import ConfigurationError

logger = logging.getLogger(__name__)


class ExportFactory:
    """导出器工厂类"""
    
    # 导出器类型映射
    _exporter_registry: Dict[ExportFormat, Type[Exporter]] = {
        ExportFormat.CSV: CsvExporter,
        ExportFormat.JSON: JsonExporter,
        ExportFormat.EXCEL: ExcelExporter,
        # 其他导出器将在后续添加
    }
    
    # 自定义导出器注册表
    _custom_exporters: Dict[str, Type[Exporter]] = {}
    
    @classmethod
    def create_exporter(cls, format: ExportFormat, name: Optional[str] = None, **config) -> Exporter:
        """
        创建导出器实例
        
        Args:
            format: 导出格式
            name: 导出器名称（可选，默认为格式名）
            **config: 导出器配置
            
        Returns:
            Exporter: 导出器实例
            
        Raises:
            ConfigurationError: 配置错误或导出格式不支持
        """
        try:
            # 获取导出器名称
            exporter_name = name or format.value
            
            # 获取导出器类
            exporter_class = cls._get_exporter_class(format)
            if exporter_class is None:
                raise ConfigurationError(f"不支持的导出格式: {format}")
            
            # 创建导出器实例
            exporter = exporter_class(name=exporter_name, **config)
            
            # 验证导出器配置
            if not exporter.validate_config():
                logger.warning(f"导出器配置验证警告: {exporter_name}")
            
            logger.debug(f"创建导出器: {exporter_name} ({format})")
            return exporter
            
        except Exception as e:
            logger.error(f"创建导出器失败 {format}: {e}")
            raise ConfigurationError(f"创建导出器失败 {format}: {e}") from e
    
    @classmethod
    def create_exporter_from_config(cls, config: Dict[str, Any]) -> Exporter:
        """
        从配置字典创建导出器
        
        Args:
            config: 导出器配置字典
            
        Returns:
            Exporter: 导出器实例
        """
        try:
            format_str = config.get("format")
            if not format_str:
                raise ConfigurationError("导出配置缺少format字段")
            
            # 转换为ExportFormat枚举
            try:
                format = ExportFormat(format_str)
            except ValueError:
                raise ConfigurationError(f"不支持的导出格式: {format_str}")
            
            name = config.get("name", format.value)
            enabled = config.get("enabled", True)
            
            # 提取导出器特定配置
            exporter_config = {k: v for k, v in config.items() 
                             if k not in ["format", "name", "enabled"]}
            
            exporter_config["enabled"] = enabled
            
            return cls.create_exporter(format, name=name, **exporter_config)
            
        except Exception as e:
            logger.error(f"从配置创建导出器失败: {e}")
            raise
    
    @classmethod
    def _get_exporter_class(cls, format: ExportFormat) -> Optional[Type[Exporter]]:
        """
        获取导出器类
        
        Args:
            format: 导出格式
            
        Returns:
            导出器类，如果找不到则返回None
        """
        # 首先检查自定义导出器
        if format.value in cls._custom_exporters:
            return cls._custom_exporters[format.value]
        
        # 检查内置导出器
        return cls._exporter_registry.get(format)
    
    @classmethod
    def register_exporter(cls, format: ExportFormat, exporter_class: Type[Exporter]) -> None:
        """
        注册自定义导出器
        
        Args:
            format: 导出格式
            exporter_class: 导出器类
        """
        if not issubclass(exporter_class, Exporter):
            raise ValueError(f"导出器类必须继承自 Exporter: {exporter_class}")
        
        cls._custom_exporters[format.value] = exporter_class
        logger.info(f"注册自定义导出器: {format} -> {exporter_class.__name__}")
    
    @classmethod
    def unregister_exporter(cls, format: ExportFormat) -> None:
        """
        注销自定义导出器
        
        Args:
            format: 导出格式
        """
        if format.value in cls._custom_exporters:
            del cls._custom_exporters[format.value]
            logger.info(f"注销自定义导出器: {format}")
    
    @classmethod
    def list_available_exporters(cls) -> Dict[str, str]:
        """
        列出可用的导出器
        
        Returns:
            导出格式和类名的映射
        """
        exporters = {}
        
        # 内置导出器
        for format, exporter_class in cls._exporter_registry.items():
            exporters[format.value] = exporter_class.__name__
        
        # 自定义导出器
        for format, exporter_class in cls._custom_exporters.items():
            exporters[format] = exporter_class.__name__
        
        return exporters
    
    @classmethod
    def get_exporter_info(cls, format: ExportFormat) -> Dict[str, Any]:
        """
        获取导出器信息
        
        Args:
            format: 导出格式
            
        Returns:
            导出器信息
        """
        exporter_class = cls._get_exporter_class(format)
        if exporter_class is None:
            return {"format": format.value, "available": False}
        
        # 获取默认配置
        default_config = {}
        if hasattr(exporter_class, '__init__'):
            import inspect
            init_signature = inspect.signature(exporter_class.__init__)
            for param_name, param in init_signature.parameters.items():
                if param_name not in ['self', 'name', 'format', 'enabled'] and param.default != inspect.Parameter.empty:
                    default_config[param_name] = param.default
        
        return {
            "format": format.value,
            "available": True,
            "class_name": exporter_class.__name__,
            "module": exporter_class.__module__,
            "description": exporter_class.__doc__ or "无描述",
            "default_config": default_config
        }
    
    @classmethod
    def create_exporters_from_configs(cls, configs: List[Dict[str, Any]]) -> Dict[str, Exporter]:
        """
        从配置列表批量创建导出器
        
        Args:
            configs: 导出器配置列表
            
        Returns:
            导出器字典（名称->实例）
        """
        exporters = {}
        
        for config in configs:
            try:
                exporter = cls.create_exporter_from_config(config)
                exporters[exporter.name] = exporter
                logger.info(f"创建导出器成功: {exporter.name}")
            except Exception as e:
                logger.error(f"创建导出器失败: {e}")
                # 根据需求决定是否抛出异常
                if config.get("strict_mode", False):
                    raise
        
        return exporters
    
    @classmethod
    def validate_exporter_config(cls, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证导出器配置
        
        Args:
            config: 导出器配置
            
        Returns:
            验证结果
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "required_fields": [],
            "optional_fields": []
        }
        
        try:
            # 检查必需字段
            if "format" not in config:
                result["valid"] = False
                result["errors"].append("缺少必需字段: format")
                return result
            
            format_str = config.get("format")
            
            # 检查格式是否支持
            try:
                format = ExportFormat(format_str)
            except ValueError:
                result["valid"] = False
                result["errors"].append(f"不支持的导出格式: {format_str}")
                return result
            
            # 检查名称
            name = config.get("name", format.value)
            if not name:
                result["warnings"].append("导出器名称不能为空，将使用格式名")
            
            # 格式特定验证
            if format == ExportFormat.CSV:
                if "output_path" not in config:
                    result["warnings"].append("CSV导出器建议配置output_path")
                
                if "delimiter" in config and len(config["delimiter"]) != 1:
                    result["warnings"].append("CSV分隔符应该是单个字符")
            
            elif format == ExportFormat.JSON:
                if "output_path" not in config:
                    result["warnings"].append("JSON导出器建议配置output_path")
                
                if "indent" in config and not isinstance(config["indent"], int):
                    result["warnings"].append("JSON缩进应该是整数")
            
            elif format == ExportFormat.EXCEL:
                if "output_path" not in config:
                    result["warnings"].append("Excel导出器建议配置output_path")
                
                # 检查依赖
                try:
                    import pandas as pd
                    import openpyxl
                except ImportError:
                    result["warnings"].append("Excel导出需要pandas和openpyxl库")
            
            # 检查输出路径（如果提供）
            if "output_path" in config:
                output_path = config["output_path"]
                if not isinstance(output_path, str):
                    result["warnings"].append("输出路径应该是字符串")
            
            logger.debug(f"导出器配置验证完成: {format}")
            
        except Exception as e:
            result["valid"] = False
            result["errors"].append(f"配置验证异常: {e}")
        
        return result