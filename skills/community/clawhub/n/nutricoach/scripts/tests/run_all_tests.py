#!/usr/bin/env python3
"""
NutriCoach 单元测试运行器
运行所有测试并生成报告
"""

import unittest
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test modules
from test_nutrition_calc import (
    TestNutritionCalculation,
    TestFoodDatabase,
    TestPantryCalculations,
    TestDataValidation
)
from test_database import (
    TestDatabaseSchema,
    TestDatabaseOperations,
    TestDataIntegrity
)


def run_all_tests():
    """Run all test suites and generate report."""
    print("=" * 70)
    print("NutriCoach 单元测试")
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestNutritionCalculation,
        TestFoodDatabase,
        TestPantryCalculations,
        TestDataValidation,
        TestDatabaseSchema,
        TestDatabaseOperations,
        TestDataIntegrity
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 70)
    print("测试摘要")
    print("=" * 70)
    print(f"总测试数: {result.testsRun}")
    print(f"通过: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, trace in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\n出错的测试:")
        for test, trace in result.errors:
            print(f"  - {test}")
    
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
