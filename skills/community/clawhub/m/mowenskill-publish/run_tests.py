#!/usr/bin/env python3
"""独立运行测试的脚本"""
import sys
import os
import unittest

# 确保路径正确
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "scripts")
sys.path.insert(0, "tests")

# 发现并运行测试
loader = unittest.TestLoader()
suite = loader.discover("tests", pattern="test_*.py")
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
