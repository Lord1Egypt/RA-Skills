#!/usr/bin/env python3
"""
Test OCR flow with mock data.
"""

import json
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'scripts'))

from food_matcher import match_and_compare, format_comparison

# Mock OCR result for testing
MOCK_OCR_RESULT = {
    "status": "success",
    "engine": "kimi",
    "text": "乐事原味薯片\n净含量: 75克\n营养成分表 (每100g)\n能量: 536千卡\n蛋白质: 7.0克\n脂肪: 35.0克\n碳水化合物: 53.0克\n膳食纤维: 3.5克",
    "structured": {
        "product_name": "乐事原味薯片",
        "brand": "乐事",
        "net_weight": "75g",
        "barcode": "6941234567890",
        "nutrition_per_100g": {
            "calories": 536,
            "protein": 7.0,
            "carbs": 53.0,
            "fat": 35.0,
            "fiber": 3.5
        },
        "confidence": "high"
    }
}


def test_matching():
    """Test matching against database."""
    print("=" * 60)
    print("测试 OCR 结果匹配")
    print("=" * 60)
    print()
    
    print("模拟 OCR 结果:")
    print(json.dumps(MOCK_OCR_RESULT["structured"], indent=2, ensure_ascii=False))
    print()
    
    # Test matching
    result = match_and_compare("robert", MOCK_OCR_RESULT)
    
    print("匹配结果:")
    print(format_comparison(result))
    print()
    
    # Also output JSON for debugging
    print("完整 JSON:")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def test_with_existing_food():
    """Test with a food that exists in database."""
    print("\n" + "=" * 60)
    print("测试已有食物匹配")
    print("=" * 60)
    print()
    
    # Mock OCR for existing food (slightly different values)
    mock_existing = {
        "status": "success",
        "structured": {
            "product_name": "薯片",
            "brand": "未知",
            "net_weight": "100g",
            "nutrition_per_100g": {
                "calories": 540,  # Slightly different
                "protein": 7.0,
                "carbs": 54.0,
                "fat": 36.0,
                "fiber": 3.5
            }
        }
    }
    
    print("OCR 识别: 薯片 (热量 540 vs 数据库 536)")
    result = match_and_compare("robert", mock_existing)
    print(format_comparison(result))


if __name__ == '__main__':
    test_matching()
    test_with_existing_food()
