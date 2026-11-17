"""
pytest 配置：添加 tests/ 目录到 sys.path
"""
import sys
from pathlib import Path

# 确保 tests/ 目录在 sys.path 中
tests_dir = Path(__file__).parent
if str(tests_dir) not in sys.path:
    sys.path.insert(0, str(tests_dir))
