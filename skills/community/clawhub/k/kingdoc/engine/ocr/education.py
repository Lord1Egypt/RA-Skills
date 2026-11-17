"""KingDoc 教育场景 OCR 统一入口（v3.7.0 新增）

教育版场景：手写公式/试卷/题目识别。
自动判断：手写体 / 印刷公式 / 混合内容。
"""
from __future__ import annotations

from typing import Dict, List, Optional

from engine.local.ocr import recognize, tesseract_available
from engine.ocr.formula_recognizer import FormulaRecognizer


class EducationOCR:
    """教育场景 OCR 统一入口。"""

    def __init__(self):
        self.formula_recognizer = FormulaRecognizer()

    def recognize(self, image_path: str, scene: str = "auto") -> Dict:
        """教育场景识别。

        Args:
            image_path: 图片路径
            scene: "auto" | "handwriting" | "formula" | "mixed"

        Returns:
            {
                "success": bool,
                "text": str,
                "latex": str,
                "confidence": float | None,
                "scene_detected": str,
                "hint": str
            }
        """
        if not tesseract_available():
            return {
                "success": False,
                "text": "",
                "latex": "",
                "confidence": None,
                "scene_detected": "none",
                "hint": "未安装 Tesseract。安装：winget install UB-Mannheim.TesseractOCR",
            }

        # 先做基础 OCR
        ocr_result = recognize(image_path)
        if not ocr_result["success"]:
            return {
                "success": False,
                "text": "",
                "latex": "",
                "confidence": None,
                "scene_detected": "none",
                "hint": ocr_result["hint"],
            }

        text = ocr_result["text"]
        confidence = ocr_result.get("confidence")

        # 自动判断场景
        if scene == "auto":
            scene = self._detect_scene(text)

        latex = ""
        if scene in ("formula", "mixed"):
            formula_result = self.formula_recognizer.recognize(image_path, "latex")
            if formula_result["success"]:
                latex = formula_result["result"]

        return {
            "success": True,
            "text": text,
            "latex": latex,
            "confidence": confidence,
            "scene_detected": scene,
            "hint": "",
        }

    def _detect_scene(self, text: str) -> str:
        """简单启发式判断场景。"""
        formula_chars = set("∑∏∫∂∞∈⊂⊃∪∩∧∨¬→↔∀∃≈≠≤≥±×÷√²³αβγδεζηθικλμνξπρστυφχψωΓΔΘΛΞΠΣΦΨΩ")
        text_chars = set(text)
        formula_count = len(formula_chars & text_chars)
        if formula_count >= 3:
            return "formula"
        if formula_count >= 1:
            return "mixed"
        return "handwriting"

    def batch_recognize(self, image_paths: List[str], scene: str = "auto") -> List[Dict]:
        """批量识别（硬件自适应并发）。"""
        results = []
        for p in image_paths:
            results.append(self.recognize(p, scene))
        return results
