#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地 Tesseract OCR 模块
提供 LocalOCR 类用于本地 OCR 识别
"""

import sys
from pathlib import Path

try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

class LocalOCR:
    def __init__(self):
        self.tesseract_available = False  # 脚本期望的属性名
        if not TESSERACT_AVAILABLE:
            print("[LocalOCR] pytesseract 或 PIL 未安装")
            return
        
        try:
            version = pytesseract.get_tesseract_version()
            self.tesseract_available = True
            print(f"[LocalOCR] Tesseract 已安装 (v{version})")
        except Exception as e:
            print(f"[LocalOCR] Tesseract 未安装或未配置: {e}")
            self.tesseract_available = False
    
    def recognize(self, image_path: str) -> dict:
        """识别图片，返回标准格式"""
        if not self.tesseract_available:
            return {"success": False, "text": "", "error": "Tesseract不可用"}
        
        try:
            img = Image.open(image_path)
            # 同时使用简体中文和英文
            text = pytesseract.image_to_string(img, lang='chi_sim+eng')
            
            if not text or not text.strip():
                return {"success": False, "text": "", "error": "识别结果为空"}
            
            return {"success": True, "text": text.strip()}
        except Exception as e:
            return {"success": False, "text": "", "error": str(e)}

if __name__ == "__main__":
    ocr = LocalOCR()
    if len(sys.argv) > 1:
        result = ocr.recognize(sys.argv[1])
        print(result)
