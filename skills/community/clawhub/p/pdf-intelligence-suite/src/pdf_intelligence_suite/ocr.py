"""
PDF OCR文字识别模块
使用pytesseract实现扫描件文字识别
"""

import os
import io
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass

import pytesseract
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes
import numpy as np


@dataclass
class OCRResult:
    """OCR识别结果"""
    text: str
    confidence: float
    page: int
    bbox: Optional[tuple] = None
    
    def __repr__(self):
        return f"OCRResult(text='{self.text[:30]}...', confidence={self.confidence:.2f})"


class OCRProcessor:
    """PDF OCR处理器"""
    
    def __init__(
        self, 
        languages: Optional[List[str]] = None,
        dpi: int = 300,
        ocr_config: str = '--psm 6'
    ):
        """
        初始化OCR处理器
        
        Args:
            languages: 语言列表，如 ['chi_sim', 'eng']
            dpi: 转换图片的DPI（越高越清晰但越慢）
            ocr_config: Tesseract额外配置
        """
        self.languages = languages or ['eng']
        self.dpi = dpi
        self.ocr_config = ocr_config
        self.lang_string = '+'.join(self.languages)
    
    def process_pdf(
        self, 
        pdf_path: str,
        pages: Optional[List[int]] = None,
        first_page: Optional[int] = None,
        last_page: Optional[int] = None
    ) -> str:
        """
        对PDF进行OCR识别
        
        Args:
            pdf_path: PDF文件路径
            pages: 指定页面列表（优先级最高）
            first_page: 起始页（从1开始）
            last_page: 结束页（从1开始）
            
        Returns:
            识别出的完整文本
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        # 转换PDF为图片
        if pages:
            # 转换指定页面
            images = []
            for page_num in pages:
                page_images = convert_from_path(
                    pdf_path,
                    dpi=self.dpi,
                    first_page=page_num + 1,
                    last_page=page_num + 1
                )
                images.extend(page_images)
        else:
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                first_page=first_page,
                last_page=last_page
            )
        
        # 对每张图片进行OCR
        text_parts = []
        for i, image in enumerate(images):
            text = self.process_image(image)
            text_parts.append(f"--- Page {i+1} ---\n{text}")
        
        return "\n\n".join(text_parts)
    
    def process_image(self, image: Union[Image.Image, np.ndarray]) -> str:
        """
        对单张图片进行OCR
        
        Args:
            image: PIL Image或numpy数组
            
        Returns:
            识别出的文本
        """
        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        
        text = pytesseract.image_to_string(
            image,
            lang=self.lang_string,
            config=self.ocr_config
        )
        return text.strip()
    
    def process_pdf_with_data(
        self, 
        pdf_path: str,
        pages: Optional[List[int]] = None
    ) -> List[Dict[str, Any]]:
        """
        对PDF进行OCR并返回详细数据
        
        Returns:
            包含文本、位置、置信度的详细结果列表
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        # 转换PDF为图片
        if pages:
            images = []
            for page_num in pages:
                page_images = convert_from_path(
                    pdf_path,
                    dpi=self.dpi,
                    first_page=page_num + 1,
                    last_page=page_num + 1
                )
                images.extend(page_images)
            page_numbers = pages
        else:
            images = convert_from_path(pdf_path, dpi=self.dpi)
            page_numbers = list(range(len(images)))
        
        results = []
        for page_num, image in zip(page_numbers, images):
            page_data = pytesseract.image_to_data(
                image,
                lang=self.lang_string,
                config=self.ocr_config,
                output_type=pytesseract.Output.DICT
            )
            
            # 解析数据
            n_boxes = len(page_data['text'])
            for i in range(n_boxes):
                if int(page_data['conf'][i]) > 0:  # 过滤低置信度
                    result = {
                        'text': page_data['text'][i],
                        'confidence': page_data['conf'][i] / 100.0,
                        'page': page_num,
                        'bbox': (
                            page_data['left'][i],
                            page_data['top'][i],
                            page_data['width'][i],
                            page_data['height'][i]
                        ),
                        'block_num': page_data['block_num'][i],
                        'par_num': page_data['par_num'][i],
                        'line_num': page_data['line_num'][i],
                        'word_num': page_data['word_num'][i]
                    }
                    results.append(result)
        
        return results
    
    def process_pdf_structured(
        self, 
        pdf_path: str,
        pages: Optional[List[int]] = None
    ) -> List[Dict[str, Any]]:
        """
        结构化输出OCR结果（按段落组织）
        
        Returns:
            按页面和段落组织的文本
        """
        raw_data = self.process_pdf_with_data(pdf_path, pages)
        
        # 按页面和段落组织
        structured = {}
        for item in raw_data:
            page = item['page']
            block = item['block_num']
            par = item['par_num']
            
            key = (page, block, par)
            if key not in structured:
                structured[key] = {
                    'page': page,
                    'block': block,
                    'paragraph': par,
                    'texts': [],
                    'confidences': []
                }
            
            if item['text'].strip():
                structured[key]['texts'].append(item['text'])
                structured[key]['confidences'].append(item['confidence'])
        
        # 构建最终结果
        results = []
        for key in sorted(structured.keys()):
            data = structured[key]
            results.append({
                'page': data['page'],
                'block': data['block'],
                'paragraph': data['paragraph'],
                'text': ' '.join(data['texts']),
                'avg_confidence': np.mean(data['confidences']) if data['confidences'] else 0
            })
        
        return results
    
    def extract_tables_with_ocr(
        self, 
        pdf_path: str,
        pages: Optional[List[int]] = None
    ) -> List[Dict[str, Any]]:
        """
        使用OCR识别PDF中的表格
        
        Returns:
            识别出的表格数据
        """
        # 首先尝试使用pdfplumber提取
        try:
            import pdfplumber
            tables_data = []
            
            with pdfplumber.open(pdf_path) as pdf:
                page_indices = pages if pages else range(len(pdf.pages))
                
                for page_num in page_indices:
                    if 0 <= page_num < len(pdf.pages):
                        page = pdf.pages[page_num]
                        tables = page.extract_tables()
                        
                        for table in tables:
                            if table:
                                tables_data.append({
                                    'page': page_num,
                                    'data': table,
                                    'method': 'pdfplumber'
                                })
            
            # 如果没有找到表格，使用OCR+布局分析
            if not tables_data:
                # 这里可以实现更复杂的OCR表格识别
                pass
            
            return tables_data
            
        except Exception as e:
            # 如果pdfplumber失败，返回OCR结果
            text = self.process_pdf(pdf_path, pages)
            return [{'page': pages or [0], 'text': text, 'method': 'ocr'}]
    
    def get_available_languages(self) -> List[str]:
        """
        获取系统已安装的Tesseract语言包
        
        Returns:
            语言代码列表
        """
        try:
            langs = pytesseract.get_languages()
            return langs
        except Exception as e:
            return ['eng']  # 默认返回英语
    
    def check_tesseract_installation(self) -> Dict[str, Any]:
        """
        检查Tesseract安装状态
        
        Returns:
            安装状态信息
        """
        try:
            version = pytesseract.get_tesseract_version()
            langs = self.get_available_languages()
            return {
                'installed': True,
                'version': str(version),
                'languages': langs,
                'language_count': len(langs)
            }
        except Exception as e:
            return {
                'installed': False,
                'error': str(e),
                'message': '请确保已安装Tesseract OCR引擎'
            }
