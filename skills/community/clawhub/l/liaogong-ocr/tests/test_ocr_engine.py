#!/usr/bin/env python3
"""Smoke tests for ocr_engine.py and preprocess.py."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_engine_import():
    """OCR engine should import without loading models."""
    from liaogong_ocr import OCREngine
    engine = OCREngine()
    assert engine._easyocr_reader is None  # lazy init
    assert engine._tesseract_path is None
    print("✓ Engine imports without loading models")


def test_preprocess_import():
    """Preprocess module exports all chains."""
    from liaogong_ocr import CHAINS, CHAIN_BENCHMARKS
    assert len(CHAINS) >= 6
    assert 'optimal_phone' in CHAINS
    assert len(CHAIN_BENCHMARKS) >= 6
    print(f"✓ {len(CHAINS)} chains available")


def test_tesseract_detection():
    """Tesseract should be found on this system."""
    from liaogong_ocr import OCREngine
    engine = OCREngine()
    path = engine._find_tesseract()
    assert path is not None, "Tesseract not found — install it or check PATH"
    print(f"✓ Tesseract found at: {path}")


def test_preprocess_chains():
    """Each chain should accept and return a PIL Image."""
    from PIL import Image
    from liaogong_ocr import CHAINS

    img = Image.new('RGB', (100, 100), color='gray')
    for name, chain_fn in CHAINS.items():
        try:
            result = chain_fn(img)
            assert isinstance(result, Image.Image), f"{name} returned {type(result)}"
        except ImportError:
            pass  # skip chains that need numpy if not installed
    print(f"✓ All chains produce valid PIL Images")


if __name__ == '__main__':
    test_engine_import()
    test_preprocess_import()
    test_tesseract_detection()
    test_preprocess_chains()
    print("\n✓ All tests passed!")
