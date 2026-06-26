"""
PDF Intelligence Suite
PDF智能处理套件

一个功能强大的PDF文档处理工具集，支持文本提取、表格识别、OCR、格式转换等。
"""

__version__ = "1.0.0"
__author__ = "ClawHub Skills"
__license__ = "MIT"

# 主要模块导出
from .extractor import PDFExtractor
from .tables import TableExtractor
from .ocr import OCRProcessor
from .converter import PDFConverter
from .manipulator import PDFManipulator
from .security import PDFSecurity
from .utils import (
    get_pdf_info,
    validate_pdf,
    create_sample_pdf
)

__all__ = [
    "PDFExtractor",
    "TableExtractor", 
    "OCRProcessor",
    "PDFConverter",
    "PDFManipulator",
    "PDFSecurity",
    "get_pdf_info",
    "validate_pdf",
    "create_sample_pdf",
]
