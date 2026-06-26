"""
PDF文本提取模块
使用PyPDF2和pdfplumber实现高质量的文本提取
"""

import io
from typing import List, Optional, Dict, Any, Union, Tuple
from dataclasses import dataclass

import PyPDF2
import pdfplumber


@dataclass
class TextElement:
    """文本元素，包含内容和位置信息"""
    text: str
    page: int
    bbox: Tuple[float, float, float, float]  # x0, y0, x1, y1
    font: Optional[str] = None
    size: Optional[float] = None
    
    def __repr__(self):
        return f"TextElement(text='{self.text[:30]}...', page={self.page}, bbox={self.bbox})"


class PDFExtractor:
    """PDF文本提取器"""
    
    def __init__(self):
        self._current_pdf = None
        self._plumber_pdf = None
    
    def extract_text(
        self, 
        pdf_path: str, 
        pages: Optional[List[int]] = None,
        preserve_layout: bool = False
    ) -> str:
        """
        从PDF提取文本
        
        Args:
            pdf_path: PDF文件路径
            pages: 指定页面索引列表（从0开始），None表示所有页面
            preserve_layout: 是否保留布局（使用pdfplumber）
            
        Returns:
            提取的文本字符串
        """
        if preserve_layout:
            return self._extract_with_plumber(pdf_path, pages)
        else:
            return self._extract_with_pypdf2(pdf_path, pages)
    
    def _extract_with_pypdf2(
        self, 
        pdf_path: str, 
        pages: Optional[List[int]] = None
    ) -> str:
        """使用PyPDF2提取文本"""
        text_parts = []
        
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            
            page_indices = pages if pages else range(num_pages)
            
            for page_num in page_indices:
                if 0 <= page_num < num_pages:
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    if text:
                        text_parts.append(text)
        
        return "\n\n".join(text_parts)
    
    def _extract_with_plumber(
        self, 
        pdf_path: str, 
        pages: Optional[List[int]] = None
    ) -> str:
        """使用pdfplumber提取文本（保留布局）"""
        text_parts = []
        
        with pdfplumber.open(pdf_path) as pdf:
            page_indices = pages if pages else range(len(pdf.pages))
            
            for page_num in page_indices:
                if 0 <= page_num < len(pdf.pages):
                    page = pdf.pages[page_num]
                    text = page.extract_text(layout=True)
                    if text:
                        text_parts.append(text)
        
        return "\n\n--- Page Break ---\n\n".join(text_parts)
    
    def extract_with_layout(
        self, 
        pdf_path: str, 
        pages: Optional[List[int]] = None
    ) -> List[TextElement]:
        """
        提取带位置信息的文本元素
        
        Returns:
            TextElement对象列表
        """
        elements = []
        
        with pdfplumber.open(pdf_path) as pdf:
            page_indices = pages if pages else range(len(pdf.pages))
            
            for page_num in page_indices:
                if 0 <= page_num < len(pdf.pages):
                    page = pdf.pages[page_num]
                    chars = page.chars
                    
                    # 按字符分组形成单词/文本块
                    if chars:
                        for char in chars:
                            elem = TextElement(
                                text=char.get('text', ''),
                                page=page_num,
                                bbox=(
                                    char.get('x0', 0),
                                    char.get('top', 0),
                                    char.get('x1', 0),
                                    char.get('bottom', 0)
                                ),
                                font=char.get('fontname'),
                                size=char.get('size')
                            )
                            elements.append(elem)
        
        return elements
    
    def extract_by_bbox(
        self, 
        pdf_path: str, 
        page: int, 
        bbox: Tuple[float, float, float, float]
    ) -> str:
        """
        按边界框提取指定区域的文本
        
        Args:
            pdf_path: PDF文件路径
            page: 页码（从0开始）
            bbox: 边界框 (x0, top, x1, bottom)
            
        Returns:
            区域内的文本
        """
        with pdfplumber.open(pdf_path) as pdf:
            if 0 <= page < len(pdf.pages):
                pdf_page = pdf.pages[page]
                cropped = pdf_page.crop(bbox)
                return cropped.extract_text() or ""
        return ""
    
    def extract_lines(
        self, 
        pdf_path: str, 
        pages: Optional[List[int]] = None
    ) -> List[Dict[str, Any]]:
        """
        提取文本行及其位置信息
        
        Returns:
            包含行文本和元信息的字典列表
        """
        lines = []
        
        with pdfplumber.open(pdf_path) as pdf:
            page_indices = pages if pages else range(len(pdf.pages))
            
            for page_num in page_indices:
                if 0 <= page_num < len(pdf.pages):
                    page = pdf.pages[page_num]
                    page_lines = page.extract_text().split('\n') if page.extract_text() else []
                    
                    for line_text in page_lines:
                        if line_text.strip():
                            lines.append({
                                'text': line_text,
                                'page': page_num,
                                'stripped': line_text.strip()
                            })
        
        return lines
    
    def extract_words(
        self, 
        pdf_path: str, 
        pages: Optional[List[int]] = None
    ) -> List[Dict[str, Any]]:
        """
        提取单词及其位置信息
        
        Returns:
            单词信息列表
        """
        words = []
        
        with pdfplumber.open(pdf_path) as pdf:
            page_indices = pages if pages else range(len(pdf.pages))
            
            for page_num in page_indices:
                if 0 <= page_num < len(pdf.pages):
                    page = pdf.pages[page_num]
                    page_words = page.extract_words()
                    
                    for word in page_words:
                        words.append({
                            'text': word.get('text', ''),
                            'page': page_num,
                            'x0': word.get('x0'),
                            'y0': word.get('top'),
                            'x1': word.get('x1'),
                            'y1': word.get('bottom'),
                        })
        
        return words
    
    def search_text(
        self, 
        pdf_path: str, 
        keyword: str, 
        case_sensitive: bool = False
    ) -> List[Dict[str, Any]]:
        """
        在PDF中搜索关键词
        
        Args:
            pdf_path: PDF文件路径
            keyword: 搜索关键词
            case_sensitive: 是否区分大小写
            
        Returns:
            匹配结果列表
        """
        results = []
        
        if not case_sensitive:
            keyword = keyword.lower()
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                
                if not case_sensitive:
                    search_text = text.lower()
                else:
                    search_text = text
                
                if keyword in search_text:
                    # 找到匹配，获取更多上下文
                    lines = text.split('\n')
                    for line_num, line in enumerate(lines):
                        check_line = line if case_sensitive else line.lower()
                        if keyword in check_line:
                            results.append({
                                'page': page_num,
                                'line': line_num,
                                'text': line.strip(),
                                'keyword': keyword
                            })
        
        return results
    
    def close(self):
        """关闭打开的PDF资源"""
        if self._plumber_pdf:
            self._plumber_pdf.close()
            self._plumber_pdf = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
