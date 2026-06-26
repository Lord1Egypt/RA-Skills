#!/usr/bin/env python3
"""
OCR Engine Selector - Intelligent selection based on content analysis.
"""

import re
from pathlib import Path
from typing import List, Optional


def detect_chinese(text: str) -> bool:
    """Check if text contains Chinese characters."""
    return bool(re.search(r'[\u4e00-\u9fff]', text))


def detect_language_hint(image_name: str) -> str:
    """Detect likely language from image filename using word boundary matching."""
    name_lower = image_name.lower()
    
    chinese_indicators = ['中文', 'chinese', 'cn', '汉字', '简体', '繁体']
    english_indicators = ['english', 'eng', 'menu']
    
    # Use word boundary matching to avoid substring false positives
    # e.g., 'en.' should not match 'screen.png'
    def _match_indicator(name: str, indicator: str) -> bool:
        return bool(re.search(r'(?<![a-z])' + re.escape(indicator) + r'(?![a-z])', name))
    
    for ind in chinese_indicators:
        if ind in name_lower:
            return 'chinese'
    
    for ind in english_indicators:
        if _match_indicator(name_lower, ind):
            return 'english'
    
    return 'auto'


def analyze_image_complexity(image_path: str) -> str:
    """Analyze image to determine complexity level."""
    name_lower = Path(image_path).name.lower()
    
    complex_patterns = ['menu', 'invoice', 'contract', 'certificate', 
                       'exam', 'form', 'table', 'receipt', '发票', '合同']
    
    simple_patterns = ['screenshot', 'snap', 'capture', 'screen', '截图']
    
    if any(p in name_lower for p in complex_patterns):
        return 'complex'
    if any(p in name_lower for p in simple_patterns):
        return 'simple'
    
    return 'medium'


def select_ocr_strategy(
    image_path: str,
    force_engine: Optional[str] = None
) -> dict:
    """
    Select OCR strategy based on image analysis.
    
    Returns:
        dict with 'engines' list and 'strategy' description
    """
    if force_engine:
        return {
            'engines': [force_engine],
            'strategy': f'forced: {force_engine}'
        }
    
    name_lower = Path(image_path).name.lower()
    complexity = analyze_image_complexity(image_path)
    lang_hint = detect_language_hint(image_path)
    
    # Simple + English → RapidOCR only (fast)
    if complexity == 'simple' and lang_hint == 'english':
        return {
            'engines': ['rapidocr'],
            'strategy': 'simple English - fast mode'
        }
    
    # Complex or Chinese → RapidOCR + pix2tex (full)
    if complexity == 'complex' or lang_hint == 'chinese':
        return {
            'engines': ['rapidocr', 'pix2tex'],
            'strategy': f'complex/{lang_hint} - full mode'
        }
    
    # Medium complexity - try both
    return {
        'engines': ['rapidocr', 'pix2tex'],
        'strategy': 'medium complexity - full mode'
    }


def select_best_ocr_result(results: List[dict]) -> dict:
    """
    Select best OCR result from multiple engines.
    
    Args:
        results: List of {'text': str, 'engine': str, 'confidence': float}
        
    Returns:
        Best result dict
    """
    if not results:
        return {'text': '', 'confidence': 0, 'engine': None}
    
    valid = [r for r in results if r.get('text', '').strip()]
    
    if not valid:
        return {'text': '', 'confidence': 0, 'engine': None, 'error': 'all failed'}
    
    # Simple scoring: prefer non-empty, use engine order as tiebreaker
    best = valid[0]
    best['selected_engine'] = best.get('engine', 'unknown')
    
    return best