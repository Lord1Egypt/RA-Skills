"""
公文格式转换技能 - Official Doc Formatter
将 Markdown 文档转换为符合 GB/T 9704-2012 党政机关公文格式的 Word 文档

使用方式:
    from official_doc import md_to_docx
    md_to_docx(md_content, output_path)
"""

from .md2docx import md_to_docx

__version__ = "1.1.0"
__all__ = ["md_to_docx"]
