"""
PDF Parser Module
使用 pypdf 解析 PDF 文件
"""

import io
from pathlib import Path
from typing import Union
from pypdf import PdfReader


class PDFParserError(Exception):
    """PDF解析异常"""
    pass


class PDFParser:
    """PDF 解析器"""

    def parse(self, pdf_path: Union[str, Path]) -> str:
        """
        解析 PDF 文件并提取文本内容

        Args:
            pdf_path: PDF 文件路径

        Returns:
            提取的文本内容

        Raises:
            FileNotFoundError: 文件不存在
            ValueError: 无法提取有效内容
        """
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise PDFParserError(f"PDF file not found: {pdf_path}")

        try:
            reader = PdfReader(str(pdf_path))
        except Exception as e:
            raise PDFParserError(f"Failed to read PDF: {e}")

        if len(reader.pages) == 0:
            raise PDFParserError("PDF has no pages")

        texts = []
        for page_num, page in enumerate(reader.pages, 1):
            try:
                text = page.extract_text()
                if text and text.strip():
                    texts.append(f"--- Page {page_num} ---\n{text.strip()}")
            except Exception as e:
                # 跳过无法解析的页面
                continue

        content = '\n\n'.join(texts)

        if not content or len(content.strip()) < 100:
            raise PDFParserError("Could not extract meaningful content from PDF")

        return content.strip()

    def parse_file(self, file_obj) -> str:
        """
        从文件对象解析 PDF

        Args:
            file_obj: 文件对象（已打开的二进制文件）

        Returns:
            提取的文本内容
        """
        try:
            pdf_bytes = file_obj.read()
            return self.parse_bytes(pdf_bytes)
        except Exception as e:
            raise PDFParserError(f"Failed to read PDF from file object: {e}")

    def parse_bytes(self, pdf_bytes: bytes) -> str:
        """
        从字节流解析 PDF

        Args:
            pdf_bytes: PDF 文件字节

        Returns:
            提取的文本内容
        """
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
        except Exception as e:
            raise PDFParserError(f"Failed to read PDF from bytes: {e}")

        texts = []
        for page_num, page in enumerate(reader.pages, 1):
            try:
                text = page.extract_text()
                if text and text.strip():
                    texts.append(f"--- Page {page_num} ---\n{text.strip()}")
            except Exception:
                continue

        content = '\n\n'.join(texts)

        if not content or len(content.strip()) < 100:
            raise PDFParserError("Could not extract meaningful content from PDF")

        return content.strip()

    def extract_pages(self, pdf_path: Union[str, Path]) -> list:
        """
        逐页提取PDF文本

        Args:
            pdf_path: PDF文件路径

        Returns:
            每页文本的列表
        """
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise PDFParserError(f"PDF file not found: {pdf_path}")

        try:
            reader = PdfReader(str(pdf_path))
        except Exception as e:
            raise PDFParserError(f"Failed to read PDF: {e}")

        pages = []
        for page in reader.pages:
            try:
                text = page.extract_text()
                pages.append(text if text else "")
            except Exception:
                pages.append("")

        return pages


def parse_pdf(pdf_path: Union[str, Path]) -> str:
    """
    便捷函数：解析 PDF 文件

    Args:
        pdf_path: PDF 文件路径

    Returns:
        提取的文本内容
    """
    parser = PDFParser()
    return parser.parse(pdf_path)
