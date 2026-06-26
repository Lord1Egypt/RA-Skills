#!/usr/bin/env python3
"""
代码分析器基类
"""

import os
import re
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class BaseAnalyzer(ABC):
    """代码分析器基类"""

    def __init__(self, target_dir: str):
        self.target_dir = target_dir
        self.result = {}

    @abstractmethod
    def analyze(self) -> Dict[str, Any]:
        """执行分析"""
        pass

    def read_file(self, file_path: str) -> Optional[str]:
        """读取文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except (IOError, OSError):
            return None

    def find_files(self, extensions: List[str], exclude_dirs: set = None) -> List[str]:
        """查找指定扩展名的文件"""
        if exclude_dirs is None:
            exclude_dirs = {'.git', 'node_modules', 'build', 'dist', 'out'}

        files = []
        for root, dirs, filenames in os.walk(self.target_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for f in filenames:
                for ext in extensions:
                    if f.endswith(ext):
                        files.append(os.path.join(root, f))
                        break
        return files

    def count_lines(self, file_path: str) -> int:
        """统计文件行数"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return len(f.readlines())
        except (IOError, OSError):
            return 0

    def grep_pattern(self, pattern: str, file_path: str) -> List[str]:
        """在文件中搜索模式"""
        matches = []
        content = self.read_file(file_path)
        if content:
            for match in re.finditer(pattern, content, re.MULTILINE):
                matches.append(match.group(0))
        return matches