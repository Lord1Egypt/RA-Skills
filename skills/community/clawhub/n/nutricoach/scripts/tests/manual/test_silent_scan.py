#!/usr/bin/env python3
"""
Test silent scan mode.
"""

import json
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'scripts'))

from food_analyzer import process_scan_result

class MockArgs:
    def __init__(self, user="robert", verbose=False, threshold=10.0):
        self.user = user
        self.verbose = verbose
        self.threshold = threshold

# Test Case 1: Barcode match, small diff (< threshold)
TEST_SMALL_DIFF = {
    "match_type": "barcode_exact",
    "action": "use_existing",
    "matches": [{"name": "乐事原味薯片", "barcode": "6941234567890"}],
    "comparison": {
        "nutrition_diff": {
            "calories": {"diff_pct": 2.0},
            "protein": {"diff_pct": 0},
            "carbs": {"diff_pct": 1.0},
            "fat": {"diff_pct": 0},
            "fiber": {"diff_pct": 0}
        },
        "significant_changes": []
    }
}

# Test Case 2: Barcode match, large diff (> threshold)
TEST_LARGE_DIFF = {
    "match_type": "barcode_exact",
    "action": "update",
    "matches": [{"name": "乐事原味薯片", "barcode": "6941234567890"}],
    "comparison": {
        "nutrition_diff": {
            "calories": {"diff_pct": 15.0},
            "protein": {"diff_pct": -8.0},
            "carbs": {"diff_pct": 12.0},
            "fat": {"diff_pct": 0},
            "fiber": {"diff_pct": 0}
        },
        "significant_changes": ["calories", "carbs"]
    }
}

# Test Case 3: No match
TEST_NO_MATCH = {
    "match_type": "none",
    "action": "add_new",
    "matches": []
}


def test_scenarios():
    print("=" * 60)
    print("测试静默扫描模式")
    print("=" * 60)
    print()
    
    # Mock OCR data
    ocr_data = {
        "structured": {
            "product_name": "乐事原味薯片",
            "brand": "乐事",
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
    
    args = MockArgs()
    
    # Test 1: Small diff - should use existing silently
    print("1. 条形码匹配，差异小 (< 10%)")
    print("-" * 60)
    result = process_scan_result(args, ocr_data, TEST_SMALL_DIFF)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print()
    
    # Test 2: Large diff - should suggest update
    print("2. 条形码匹配，差异大 (> 10%)")
    print("-" * 60)
    result = process_scan_result(args, ocr_data, TEST_LARGE_DIFF)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print()
    
    # Test 3: No match - should add new
    print("3. 无匹配 - 自动新增")
    print("-" * 60)
    result = process_scan_result(args, ocr_data, TEST_NO_MATCH)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    test_scenarios()
