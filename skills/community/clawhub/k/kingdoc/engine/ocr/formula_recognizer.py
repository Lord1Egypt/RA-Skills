"""KingDoc 数学公式识别器（v3.7.0 新增，教育场景）

目标：识别手写/印刷数学公式，输出 LaTeX/MathML。
实现：本地 Tesseract + 启发式后处理（零第三方依赖）。
降级：若无公式模型，返回 Tesseract 原始识别结果 + 安装指引。
"""
from __future__ import annotations

import re
from typing import Dict, Optional


class FormulaRecognizer:
    """数学公式识别器：图片 → LaTeX/MathML。"""

    # 常见符号的 LaTeX 映射
    SYMBOL_MAP = {
        "∑": "\\sum", "∏": "\\prod", "∫": "\\int", "∂": "\\partial",
        "∞": "\\infty", "∈": "\\in", "∉": "\\notin", "⊂": "\\subset",
        "⊃": "\\supset", "∪": "\\cup", "∩": "\\cap", "∧": "\\wedge",
        "∨": "\\vee", "¬": "\\neg", "→": "\\rightarrow", "↔": "\\leftrightarrow",
        "∀": "\\forall", "∃": "\\exists", "∄": "\\nexists", "≈": "\\approx",
        "≠": "\\neq", "≤": "\\leq", "≥": "\\geq", "±": "\\pm",
        "×": "\\times", "÷": "\\cdot", "·": "\\cdot", "√": "\\sqrt",
        "²": "^2", "³": "^3", "¹": "^1", "⁰": "^0",
        "α": "\\alpha", "β": "\\beta", "γ": "\\gamma", "δ": "\\delta",
        "ε": "\\epsilon", "ζ": "\\zeta", "η": "\\eta", "θ": "\\theta",
        "ι": "\\iota", "κ": "\\kappa", "λ": "\\lambda", "μ": "\\mu",
        "ν": "\\nu", "ξ": "\\xi", "ο": "\\omicron", "π": "\\pi",
        "ρ": "\\rho", "σ": "\\sigma", "τ": "\\tau", "υ": "\\upsilon",
        "φ": "\\phi", "χ": "\\chi", "ψ": "\\psi", "ω": "\\omega",
        "Γ": "\\Gamma", "Δ": "\\Delta", "Θ": "\\Theta", "Λ": "\\Lambda",
        "Ξ": "\\Xi", "Π": "\\Pi", "Σ": "\\Sigma", "Φ": "\\Phi",
        "Ψ": "\\Psi", "Ω": "\\Omega",
    }

    def __init__(self):
        self._tesseract_available = None

    def recognize(self, image_path: str, output_format: str = "latex") -> Dict:
        """识别数学公式图片。

        Args:
            image_path: 图片路径
            output_format: "latex" | "mathml" | "text"

        Returns:
            {
                "success": bool,
                "result": str,      # LaTeX/MathML/文本
                "format": str,
                "confidence": float | None,
                "hint": str
            }
        """
        try:
            from engine.local.ocr import recognize, tesseract_available
            if not tesseract_available():
                return self._fail("未安装 Tesseract，无法识别公式。")

            ocr_result = recognize(image_path)
            if not ocr_result["success"]:
                return self._fail(ocr_result["hint"])

            raw_text = ocr_result["text"]
            if output_format == "latex":
                result = self._to_latex(raw_text)
            elif output_format == "mathml":
                result = self._to_mathml(raw_text)
            else:
                result = raw_text

            return {
                "success": True,
                "result": result,
                "format": output_format,
                "confidence": ocr_result.get("confidence"),
                "hint": "",
            }
        except Exception as e:
            return self._fail(f"公式识别失败：{e}")

    def _to_latex(self, text: str) -> str:
        """将 OCR 原始文本转换为 LaTeX。"""
        result = text
        # 替换已知符号
        for symbol, latex in self.SYMBOL_MAP.items():
            result = result.replace(symbol, f" {latex} ")
        # 分数模式：a/b → \frac{a}{b}
        result = re.sub(r'(\d+)\s*/\s*(\d+)', r'\\frac{\1}{\2}', result)
        # 上标：x^2 → x^{2}
        result = re.sub(r'(\w)\^(\d+)', r'\1^{\2}', result)
        # 下标：x_1 → x_{1}
        result = re.sub(r'(\w)_(\d+)', r'\1_{\2}', result)
        # 清理多余空格
        result = re.sub(r'\s+', ' ', result).strip()
        return result

    def _to_mathml(self, text: str) -> str:
        """将 OCR 原始文本转换为简单 MathML。"""
        # 极简 MathML 包装
        latex = self._to_latex(text)
        return f"<math><mrow><mi>{latex}</mi></mrow></math>"

    def _fail(self, msg: str) -> Dict:
        return {
            "success": False,
            "result": "",
            "format": "",
            "confidence": None,
            "hint": msg + "\n安装 Tesseract：winget install UB-Mannheim.TesseractOCR",
        }
