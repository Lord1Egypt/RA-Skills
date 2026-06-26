#!/usr/bin/env python3
"""
Test barcode matching flow.
"""

import json
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'scripts'))

from food_matcher import match_and_compare, format_comparison

# Mock OCR result with barcode that exists in database
MOCK_BARCODE_MATCH = {
    "status": "success",
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
        }
    }
}

# Same barcode but different nutrition (should suggest update)
MOCK_BARCODE_UPDATE = {
    "status": "success",
    "structured": {
        "product_name": "乐事原味薯片",
        "brand": "乐事",
        "net_weight": "75g",
        "barcode": "6941234567890",
        "nutrition_per_100g": {
            "calories": 550,  # Changed
            "protein": 6.5,   # Changed
            "carbs": 55.0,    # Changed
            "fat": 36.0,      # Changed
            "fiber": 3.0      # Changed
        }
    }
}


def test_barcode_scenarios():
    """Test different barcode scenarios."""
    print("=" * 60)
    print("测试条形码匹配场景")
    print("=" * 60)
    print()
    
    # First, add a food with barcode to database
    print("1. 先添加带条形码的商品到数据库...")
    print("   商品: 乐事原味薯片")
    print("   条形码: 6941234567890")
    print()
    
    # Simulate adding to database (in real usage, this would be done via add-custom)
    print("2. 测试场景 A: 相同条形码，相同营养数据")
    print("-" * 60)
    result = match_and_compare("robert", MOCK_BARCODE_MATCH)
    print(format_comparison(result))
    print()
    print("预期结果: barcode_exact + action=use_existing")
    print(f"实际结果: match_type={result.get('match_type')}, action={result.get('action')}")
    print()
    
    print("3. 测试场景 B: 相同条形码，不同营养数据")
    print("-" * 60)
    result = match_and_compare("robert", MOCK_BARCODE_UPDATE)
    print(format_comparison(result))
    print()
    print("预期结果: barcode_exact + action=update (因为营养变化>5%)")
    print(f"实际结果: match_type={result.get('match_type')}, action={result.get('action')}")
    print()
    
    print("4. 测试场景 C: 无条形码，仅名称匹配")
    print("-" * 60)
    no_barcode = {
        "status": "success",
        "structured": {
            "product_name": "薯片",
            "brand": None,
            "barcode": None,
            "nutrition_per_100g": {
                "calories": 536,
                "protein": 7.0,
                "carbs": 53.0,
                "fat": 35.0,
                "fiber": 3.5
            }
        }
    }
    result = match_and_compare("robert", no_barcode)
    print(format_comparison(result))
    print()
    print(f"实际结果: match_type={result.get('match_type')}, action={result.get('action')}")


if __name__ == '__main__':
    test_barcode_scenarios()
