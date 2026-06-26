"""
映射器基类
所有目标系统映射器必须继承此类
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

# Import from core module
from core.data_structures import (
    BankStatementData, MappedRecord, MappingResult, ValidationResult
)


class BaseMapper(ABC):
    """银行对账单映射器基类"""

    @abstractmethod
    def map(self, source_data: BankStatementData, **kwargs) -> MappingResult:
        """
        将源数据映射到目标系统格式

        Args:
            source_data: 源银行对账单数据
            **kwargs: 额外参数

        Returns:
            MappingResult: 映射结果
        """
        pass

    @abstractmethod
    def validate(self, mapping_result: MappingResult) -> ValidationResult:
        """
        验证映射结果

        Args:
            mapping_result: 映射结果

        Returns:
            ValidationResult: 验证结果
        """
        pass

    @property
    @abstractmethod
    def target_system(self) -> str:
        """返回目标系统名称"""
        pass

    @property
    @abstractmethod
    def required_fields(self) -> List[str]:
        """返回必填字段列表"""
        pass


class MappingConfigError(Exception):
    """映射配置错误"""

    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(message)
        self.field = field


class MappingValueError(Exception):
    """映射值转换错误"""

    def __init__(self, message: str, value: Any = None, field: Optional[str] = None):
        super().__init__(message)
        self.value = value
        self.field = field
