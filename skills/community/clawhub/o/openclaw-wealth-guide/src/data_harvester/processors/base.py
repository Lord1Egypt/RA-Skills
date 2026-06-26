"""
处理器基类模块
定义数据处理器的通用接口
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime

from ..exceptions import ProcessingError

logger = logging.getLogger(__name__)


@dataclass
class ProcessingResult:
    """处理结果数据类"""
    success: bool
    data: Any
    processor: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "success": self.success,
            "processor": self.processor,
            "timestamp": self.timestamp.isoformat(),
            "data_size": len(self.data) if isinstance(self.data, list) else 1,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "metadata": self.metadata
        }


class DataProcessor(ABC):
    """数据处理器基类"""
    
    def __init__(self, name: str, enabled: bool = True, **config):
        """
        初始化处理器
        
        Args:
            name: 处理器名称
            enabled: 是否启用
            **config: 处理器配置
        """
        self.name = name
        self.enabled = enabled
        self.config = config
        
        # 统计信息
        self.process_count = 0
        self.success_count = 0
        self.error_count = 0
        self.total_process_time = 0.0
        
        logger.debug(f"初始化处理器: {self.name}")
    
    def process(self, data: Any, **kwargs) -> ProcessingResult:
        """
        处理数据（包装方法，包含错误处理和统计）
        
        Args:
            data: 输入数据
            **kwargs: 额外参数
            
        Returns:
            ProcessingResult: 处理结果
        """
        if not self.enabled:
            return ProcessingResult(
                success=True,
                data=data,
                processor=self.name,
                warnings=["处理器已禁用，跳过处理"]
            )
        
        import time
        start_time = time.time()
        self.process_count += 1
        
        try:
            logger.debug(f"开始处理数据: {self.name}")
            
            # 合并配置参数和传递的参数
            process_kwargs = {**self.config, **kwargs}
            
            # 执行实际的数据处理
            processed_data = self._process_impl(data, **process_kwargs)
            
            # 验证返回数据
            if processed_data is None:
                raise ProcessingError(f"处理器返回空数据: {self.name}")
            
            # 统计成功
            end_time = time.time()
            process_time = end_time - start_time
            self.total_process_time += process_time
            self.success_count += 1
            
            result = ProcessingResult(
                success=True,
                data=processed_data,
                processor=self.name,
                metadata={
                    "processing_time": process_time,
                    "input_size": self._get_data_size(data),
                    "output_size": self._get_data_size(processed_data)
                }
            )
            
            logger.debug(
                f"数据处理成功: {self.name}, "
                f"耗时: {process_time:.2f}s"
            )
            
            return result
            
        except Exception as e:
            # 统计失败
            end_time = time.time()
            process_time = end_time - start_time
            self.total_process_time += process_time
            self.error_count += 1
            
            error_msg = f"数据处理失败 {self.name}: {e}"
            logger.error(error_msg, exc_info=True)
            
            return ProcessingResult(
                success=False,
                data=data,  # 返回原始数据以便继续处理
                processor=self.name,
                errors=[error_msg],
                metadata={"processing_time": process_time}
            )
    
    @abstractmethod
    def _process_impl(self, data: Any, **kwargs) -> Any:
        """
        实际的数据处理实现（子类必须实现）
        
        Args:
            data: 输入数据
            **kwargs: 处理参数
            
        Returns:
            处理后的数据
        """
        pass
    
    def _get_data_size(self, data: Any) -> str:
        """获取数据大小的可读字符串"""
        if data is None:
            return "0 bytes"
        
        if isinstance(data, (list, tuple)):
            return f"{len(data)} items"
        elif isinstance(data, dict):
            return f"{len(data)} keys"
        elif isinstance(data, (str, bytes)):
            return f"{len(data)} chars"
        else:
            return "1 item"
    
    def get_stats(self) -> Dict[str, Any]:
        """获取处理器统计信息"""
        avg_time = 0
        if self.process_count > 0:
            avg_time = self.total_process_time / self.process_count
        
        success_rate = 0
        if self.process_count > 0:
            success_rate = (self.success_count / self.process_count) * 100
        
        return {
            "name": self.name,
            "enabled": self.enabled,
            "process_count": self.process_count,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "success_rate": f"{success_rate:.1f}%",
            "total_process_time": f"{self.total_process_time:.2f}s",
            "average_process_time": f"{avg_time:.2f}s"
        }
    
    def validate_config(self) -> bool:
        """
        验证处理器配置
        
        Returns:
            bool: 配置是否有效
        """
        try:
            if not self.name:
                logger.error("处理器名称不能为空")
                return False
            
            logger.debug(f"处理器配置验证通过: {self.name}")
            return True
            
        except Exception as e:
            logger.error(f"处理器配置验证失败 {self.name}: {e}")
            return False


class CleanProcessor(DataProcessor):
    """数据清洗处理器"""
    
    def __init__(self, name: str = "clean", **config):
        default_config = {
            "remove_duplicates": True,
            "remove_null": True,
            "trim_whitespace": True,
            "normalize_text": True,
            "encoding": "utf-8",
            "case_sensitive": False,
        }
        default_config.update(config)
        super().__init__(name, **default_config)
    
    def _process_impl(self, data: Any, **kwargs) -> Any:
        """
        清洗数据
        
        Args:
            data: 输入数据
            **kwargs: 清洗参数
            
        Returns:
            清洗后的数据
        """
        remove_duplicates = kwargs.get("remove_duplicates", True)
        remove_null = kwargs.get("remove_null", True)
        trim_whitespace = kwargs.get("trim_whitespace", True)
        normalize_text = kwargs.get("normalize_text", True)
        encoding = kwargs.get("encoding", "utf-8")
        
        if data is None:
            return data
        
        # 处理列表数据
        if isinstance(data, list):
            return self._clean_list(data, remove_duplicates, remove_null, 
                                  trim_whitespace, normalize_text, encoding)
        
        # 处理字典数据
        elif isinstance(data, dict):
            return self._clean_dict(data, remove_null, trim_whitespace, 
                                  normalize_text, encoding)
        
        # 处理字符串数据
        elif isinstance(data, str):
            return self._clean_string(data, trim_whitespace, normalize_text, encoding)
        
        # 其他类型直接返回
        else:
            return data
    
    def _clean_list(self, data_list: List, remove_duplicates: bool, remove_null: bool,
                   trim_whitespace: bool, normalize_text: bool, encoding: str) -> List:
        """清洗列表数据"""
        cleaned = []
        
        for item in data_list:
            # 处理空值
            if remove_null and item is None:
                continue
            
            # 递归处理嵌套结构
            if isinstance(item, (list, dict, str)):
                item = self._process_impl(item, 
                    remove_duplicates=remove_duplicates,
                    remove_null=remove_null,
                    trim_whitespace=trim_whitespace,
                    normalize_text=normalize_text,
                    encoding=encoding
                )
            
            cleaned.append(item)
        
        # 去重
        if remove_duplicates and cleaned:
            # 简单去重（对于简单类型）
            try:
                unique_items = []
                seen = set()
                for item in cleaned:
                    if isinstance(item, (str, int, float, bool)):
                        item_key = str(item)
                    else:
                        item_key = str(item)
                    
                    if item_key not in seen:
                        seen.add(item_key)
                        unique_items.append(item)
                cleaned = unique_items
            except:
                # 如果去重失败，保持原样
                pass
        
        return cleaned
    
    def _clean_dict(self, data_dict: Dict, remove_null: bool, trim_whitespace: bool,
                   normalize_text: bool, encoding: str) -> Dict:
        """清洗字典数据"""
        cleaned = {}
        
        for key, value in data_dict.items():
            # 处理空值
            if remove_null and value is None:
                continue
            
            # 清理键名
            cleaned_key = key
            if trim_whitespace and isinstance(key, str):
                cleaned_key = key.strip()
            
            # 递归处理值
            if isinstance(value, (list, dict, str)):
                value = self._process_impl(value, 
                    remove_duplicates=False,  # 字典内部不去重
                    remove_null=remove_null,
                    trim_whitespace=trim_whitespace,
                    normalize_text=normalize_text,
                    encoding=encoding
                )
            
            cleaned[cleaned_key] = value
        
        return cleaned
    
    def _clean_string(self, text: str, trim_whitespace: bool, 
                     normalize_text: bool, encoding: str) -> str:
        """清洗字符串数据"""
        cleaned = text
        
        # 去除空白字符
        if trim_whitespace:
            cleaned = cleaned.strip()
        
        # 文本标准化
        if normalize_text:
            import unicodedata
            # 标准化Unicode字符
            cleaned = unicodedata.normalize('NFKC', cleaned)
            
            # 替换全角字符为半角
            cleaned = ''.join(
                chr(ord(c) - 0xFEE0) if '\uFF01' <= c <= '\uFF5E' else c 
                for c in cleaned
            )
        
        # 编码处理
        try:
            cleaned = cleaned.encode(encoding).decode(encoding)
        except:
            # 编码失败，尝试utf-8
            try:
                cleaned = cleaned.encode('utf-8', errors='ignore').decode('utf-8')
            except:
                pass
        
        return cleaned


class TransformProcessor(DataProcessor):
    """数据转换处理器"""
    
    def __init__(self, name: str = "transform", **config):
        default_config = {
            "date_format": "%Y-%m-%d %H:%M:%S",
            "number_precision": 2,
            "encoding": "utf-8",
            "timezone": "Asia/Shanghai",
            "convert_types": True,
        }
        default_config.update(config)
        super().__init__(name, **default_config)
    
    def _process_impl(self, data: Any, **kwargs) -> Any:
        """
        转换数据
        
        Args:
            data: 输入数据
            **kwargs: 转换参数
            
        Returns:
            转换后的数据
        """
        date_format = kwargs.get("date_format", "%Y-%m-%d %H:%M:%S")
        number_precision = kwargs.get("number_precision", 2)
        convert_types = kwargs.get("convert_types", True)
        
        if data is None:
            return data
        
        # 处理列表数据
        if isinstance(data, list):
            return [
                self._transform_item(item, date_format, number_precision, convert_types)
                for item in data
            ]
        
        # 处理字典数据
        elif isinstance(data, dict):
            return {
                key: self._transform_item(value, date_format, number_precision, convert_types)
                for key, value in data.items()
            }
        
        # 处理单个值
        else:
            return self._transform_item(data, date_format, number_precision, convert_types)
    
    def _transform_item(self, item: Any, date_format: str, 
                       number_precision: int, convert_types: bool) -> Any:
        """转换单个数据项"""
        if not convert_types or item is None:
            return item
        
        # 尝试转换为日期时间
        if isinstance(item, str):
            item = self._try_convert_datetime(item, date_format)
        
        # 尝试转换为数字
        if isinstance(item, str):
            item = self._try_convert_number(item, number_precision)
        
        # 处理布尔值
        if isinstance(item, str):
            item = self._try_convert_boolean(item)
        
        return item
    
    def _try_convert_datetime(self, value: str, date_format: str) -> Any:
        """尝试将字符串转换为日期时间"""
        from datetime import datetime
        
        # 常见日期时间格式
        formats = [
            date_format,
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%a, %d %b %Y %H:%M:%S %Z",
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(value, fmt)
                return dt.strftime(date_format)
            except ValueError:
                continue
        
        # 不是日期时间格式，返回原值
        return value
    
    def _try_convert_number(self, value: str, precision: int) -> Any:
        """尝试将字符串转换为数字"""
        try:
            # 尝试整数
            return int(value)
        except ValueError:
            try:
                # 尝试浮点数
                num = float(value)
                if precision >= 0:
                    return round(num, precision)
                return num
            except ValueError:
                # 不是数字，返回原值
                return value
    
    def _try_convert_boolean(self, value: str) -> Any:
        """尝试将字符串转换为布尔值"""
        lower_value = value.lower().strip()
        
        true_values = ["true", "yes", "1", "on", "enabled"]
        false_values = ["false", "no", "0", "off", "disabled"]
        
        if lower_value in true_values:
            return True
        elif lower_value in false_values:
            return False
        else:
            return value