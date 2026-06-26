"""
廖工AI设计实战 · LiaoGong-OCR
双引擎OCR系统：easyocr + tesseract

Usage:
    from liaogong_ocr import OCREngine
    engine = OCREngine()
    result = engine.process("image.jpg")

    from liaogong_ocr import CHAINS, chain_cross_validate
    img = CHAINS['optimal_phone'](image)

Author: 廖工AI设计实战 (github.com/jnbno1163)
License: MIT
"""

from .engine import OCREngine
from .preprocess import CHAINS, CHAIN_BENCHMARKS, chain_cross_validate

__version__ = "1.0.0"
__author__ = "廖工AI设计实战"
__all__ = ["OCREngine", "CHAINS", "CHAIN_BENCHMARKS", "chain_cross_validate"]
