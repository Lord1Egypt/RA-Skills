"""KingDoc OCR 引擎（v3.7.0 升级：手写/公式识别 + 强制本地优先）

设计目标：
- 强制本地 Tesseract，数据不出域（不调用任何外部 OCR API）
- 支持数学公式/手写体识别（LaTeX/MathML 输出）
- 教育场景统一入口
"""
from __future__ import annotations

from engine.local.ocr import recognize, tesseract_available
from engine.ocr.formula_recognizer import FormulaRecognizer
from engine.ocr.education import EducationOCR

__all__ = ["recognize", "tesseract_available", "FormulaRecognizer", "EducationOCR"]
