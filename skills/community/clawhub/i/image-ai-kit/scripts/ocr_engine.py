"""
OCR Engine - OCR文字识别 (基于 Tesseract)
"""

import pytesseract
from PIL import Image
from typing import Optional, List, Dict, Union
import os


class OCREngine:
    """OCR文字识别引擎"""
    
    def __init__(self, lang: str = 'eng', config: str = ''):
        """
        初始化OCR引擎
        
        Args:
            lang: 语言 (chi_sim+eng, eng, chi_sim, etc.)
            config: 额外配置
        """
        self.lang = lang
        self.config = config
    
    def extract_text(self, image_path: Union[str, Image.Image]) -> str:
        """
        提取图像中的文字
        
        Args:
            image_path: 图像路径或PIL图像对象
        
        Returns:
            识别出的文字
        """
        if isinstance(image_path, str):
            image = Image.open(image_path)
        else:
            image = image_path
        
        # 预处理：转为灰度
        if image.mode != 'L':
            image = image.convert('L')
        
        text = pytesseract.image_to_string(
            image,
            lang=self.lang,
            config=self.config
        )
        
        return text.strip()
    
    def extract_boxes(self, image_path: Union[str, Image.Image]) -> List[Dict]:
        """
        提取文字及位置信息
        
        Returns:
            [{text, x, y, width, height}, ...]
        """
        if isinstance(image_path, str):
            image = Image.open(image_path)
        else:
            image = image_path
        
        data = pytesseract.image_to_data(
            image,
            lang=self.lang,
            output_type=pytesseract.Output.DICT
        )
        
        boxes = []
        for i in range(len(data['text'])):
            if int(data['conf'][i]) > 0:  # 只保留有置信度的结果
                boxes.append({
                    'text': data['text'][i],
                    'x': data['left'][i],
                    'y': data['top'][i],
                    'width': data['width'][i],
                    'height': data['height'][i],
                    'conf': data['conf'][i]
                })
        
        return boxes
    
    def extract_to_file(self, image_path: str, output_path: str,
                       format: str = 'txt'):
        """
        提取文字并保存到文件
        
        Args:
            format: 输出格式 (txt, pdf, hocr)
        """
        image = Image.open(image_path)
        
        if format == 'txt':
            text = self.extract_text(image)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
        elif format == 'pdf':
            # 需要安装 tesseract 的 pdf 支持
            pdf = pytesseract.image_to_pdf_or_hocr(image, lang=self.lang)
            with open(output_path, 'wb') as f:
                f.write(pdf)
        elif format == 'hocr':
            hocr = pytesseract.image_to_pdf_or_hocr(
                image,
                lang=self.lang,
                extension='hocr'
            )
            with open(output_path, 'wb') as f:
                f.write(hocr)
        
        print(f"OCR结果已保存: {output_path}")
    
    def extract_table(self, image_path: str) -> List[List[str]]:
        """
        尝试提取表格内容
        
        Returns:
            二维数组表示的表格
        """
        # 这里简化处理，实际可能需要更复杂的表格检测
        text = self.extract_text(image_path)
        lines = text.split('\n')
        
        table = []
        for line in lines:
            # 尝试按空格或制表符分割
            row = [cell.strip() for cell in line.split() if cell.strip()]
            if row:
                table.append(row)
        
        return table
    
    @staticmethod
    def get_available_languages() -> List[str]:
        """获取可用的语言列表"""
        try:
            langs = pytesseract.get_languages()
            return list(langs)
        except Exception as e:
            print(f"获取语言列表失败: {e}")
            return []


if __name__ == '__main__':
    print("OCREngine 初始化成功")
    print(f"可用语言: {', '.join(OCREngine.get_available_languages()[:10])}...")
