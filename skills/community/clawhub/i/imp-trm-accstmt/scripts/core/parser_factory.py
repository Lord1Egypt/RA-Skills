"""
解析器工厂
根据文件类型自动选择合适的解析器
"""

import os
from typing import Optional, List
from functools import lru_cache

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from parsers.base_parser import BaseParser, UnsupportedFormatError
from parsers.mt940_parser import MT940Parser
from parsers.excel_parser import ExcelParser
from parsers.pdf_parser import PDFParser


class ParserFactory:
    """解析器工厂"""

    # 支持的解析器注册表
    _parsers: List[BaseParser] = []

    @classmethod
    def register_parser(cls, parser: BaseParser):
        """注册解析器"""
        cls._parsers.append(parser)

    @classmethod
    def get_parser(cls, file_path: str) -> BaseParser:
        """
        根据文件获取合适的解析器

        Args:
            file_path: 文件路径

        Returns:
            匹配的解析器实例

        Raises:
            UnsupportedFormatError: 没有找到匹配的解析器
        """
        if not cls._parsers:
            cls._register_default_parsers()

        # 尝试每个解析器
        for parser in cls._parsers:
            if parser.detect_format(file_path):
                return parser

        # 没有找到匹配的解析器
        supported = [p.format_name for p in cls._parsers]
        raise UnsupportedFormatError(
            f"无法识别文件格式: {os.path.basename(file_path)}",
            supported_formats=supported
        )

    @classmethod
    def _register_default_parsers(cls):
        """注册默认解析器"""
        # MT940 解析器（优先级高，因为MT940格式特殊）
        cls.register_parser(MT940Parser())

        # Excel 通用解析器（用于国内各家银行）
        cls.register_parser(ExcelParser())

        # PDF 解析器（支持文本型与可插拔 OCR）
        cls.register_parser(PDFParser())

        # 未来可以添加更多解析器:
        # cls.register_parser(CSVParser())

    @classmethod
    def detect_format(cls, file_path: str) -> Optional[str]:
        """
        检测文件格式

        Args:
            file_path: 文件路径

        Returns:
            格式名称，如果没有匹配返回 None
        """
        try:
            parser = cls.get_parser(file_path)
            return parser.format_name
        except UnsupportedFormatError:
            return None

    @classmethod
    def supported_formats(cls) -> List[str]:
        """获取支持的格式列表"""
        if not cls._parsers:
            cls._register_default_parsers()
        return [p.format_name for p in cls._parsers]


@lru_cache(maxsize=32)
def get_parser(file_path: str) -> BaseParser:
    """
    获取解析器的便捷函数

    Args:
        file_path: 文件路径

    Returns:
        匹配的解析器实例
    """
    return ParserFactory.get_parser(file_path)


def create_parser(format_name: str) -> Optional[BaseParser]:
    """
    根据格式名称创建解析器

    Args:
        format_name: 格式名称 (如 'MT940', 'CSV'等)

    Returns:
        解析器实例，如果没有匹配的格式返回 None
    """
    if not ParserFactory._parsers:
        ParserFactory._register_default_parsers()

    for parser in ParserFactory._parsers:
        if parser.format_name.lower() == format_name.lower():
            return parser

    return None
