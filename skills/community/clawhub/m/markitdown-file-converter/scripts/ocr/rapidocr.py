#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RapidOCR engine - fast local OCR for Chinese and English text.
"""

from pathlib import Path
from typing import Optional

from utils.deps import is_rapidocr, is_latexocr, pip_install


def run_rapidocr(input_path: Path) -> str:
    """Run RapidOCR for general text recognition."""
    if not is_rapidocr():
        try:
            pip_install("rapidocr-onnxruntime")
        except Exception:
            print("[ocr] rapidocr-onnxruntime install failed")
            return ""
    
    try:
        from rapidocr_onnxruntime import RapidOCR
        
        engine = RapidOCR()
        result, _ = engine(str(input_path))
        
        if result:
            lines = [line[1] for line in result]
            text = "\n".join(lines)
            print(f"[ocr] RapidOCR: {len(lines)} line(s) from {input_path.name}")
            return text
        else:
            print(f"[ocr] RapidOCR: no text in {input_path.name}")
            return ""
    
    except Exception as e:
        print(f"[ocr] RapidOCR failed: {e}")
        return ""


def run_latexocr(input_path: Path) -> str:
    """Run pix2tex (LaTeX-OCR) for math formula recognition."""
    if not is_latexocr():
        try:
            pip_install("pix2tex")
        except Exception:
            print("[ocr] pix2tex install failed, skipping LaTeX OCR")
            return ""
    
    try:
        from PIL import Image as PILImage
        from pix2tex.cli import LatexOCR
        
        model = LatexOCR()
        img = PILImage.open(str(input_path))
        result = model(img)
        latex = result.strip() if result else ""
        
        if latex:
            print(f"[ocr] LaTeX-OCR: formula from {input_path.name}")
            return latex
        else:
            print(f"[ocr] LaTeX-OCR: no formula in {input_path.name}")
            return ""
    
    except Exception as e:
        print(f"[ocr] LaTeX-OCR failed: {e}")
        return ""


# LaTeX validation pattern
_LATEX_MATH_TOKENS = __import__("re").compile(
    r"\\(?:frac|sqrt|int|sum|prod|lim|sin|cos|tan|log|ln|alpha|beta|gamma|"
    r"pi|infty|partial|nabla|cdot|times|pm|mp|leq|geq|neq|approx|equiv|"
    r"infty|rightarrow|leftarrow|Rightarrow|Leftarrow|mathbf|mathrm|"
    r"overline|underline|mathcal|operatorname|big|Big|left|right|quad|"
    r"hline|begin|end|text|boldsymbol|hat|bar|vec|dot|ddot|tilde|"
    r"binom|choose|bmod|pmod|mathrm|mathbb|mathsf|mathfrak)"
)


def looks_like_latex(text: str) -> bool:
    """Check if the pix2tex output looks like a real LaTeX formula."""
    import re
    
    # Must contain at least one backslash (LaTeX command)
    if "\\" not in text:
        return False
    
    # Check balanced braces
    if text.count("{") > 0 and abs(text.count("{") - text.count("}")) > 2:
        return False
    
    # Must contain at least one recognized math command
    if _LATEX_MATH_TOKENS.search(text):
        return True
    
    # Must contain math operators like ^, _ 
    math_ops = sum(1 for c in text if c in "^_{}=")
    if math_ops >= 2:
        return True
    
    return False