"""
解析器基类
所有银行对账单解析器必须继承此类
"""

from abc import ABC, abstractmethod
from typing import Optional
import os

# Import from core module
from core.data_structures import BankStatementData


class BaseParser(ABC):
    """银行对账单解析器基类"""

    @abstractmethod
    def detect_format(self, file_path: str) -> bool:
        """
        检测文件格式是否匹配

        Args:
            file_path: 文件路径

        Returns:
            True if format matches this parser, False otherwise
        """
        pass

    @abstractmethod
    def parse(self, file_path: str, **kwargs) -> BankStatementData:
        """
        解析银行对账单文件

        Args:
            file_path: 文件路径
            **kwargs: 额外参数

        Returns:
            解析后的银行对账单数据

        Raises:
            ParseError: 解析失败时抛出
        """
        pass

    def validate_file(self, file_path: str) -> bool:
        """
        验证文件是否存在且可读

        Args:
            file_path: 文件路径

        Returns:
            True if file exists and is readable
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        if not os.path.isfile(file_path):
            raise ValueError(f"Not a file: {file_path}")

        if os.path.getsize(file_path) == 0:
            raise ValueError(f"File is empty: {file_path}")

        return True

    @property
    @abstractmethod
    def format_name(self) -> str:
        """返回格式名称，用于日志和错误信息"""
        pass


class ParseError(Exception):
    """解析错误"""

    def __init__(self, message: str, line_number: Optional[int] = None, raw_data: Optional[str] = None):
        super().__init__(message)
        self.line_number = line_number
        self.raw_data = raw_data


class UnsupportedFormatError(Exception):
    """不支持的格式错误"""

    def __init__(self, message: str, supported_formats: Optional[list] = None):
        super().__init__(message)
        self.supported_formats = supported_formats or []
