#!/usr/bin/env python3
"""
C/C++代码分析器
"""

import os
import re
from typing import Dict, List, Any, Set
from .base_analyzer import BaseAnalyzer


class CAnalyzer(BaseAnalyzer):
    """C/C++代码分析器"""

    def analyze(self) -> Dict[str, Any]:
        """分析C/C++项目"""
        # 使用列表作为结果，避免JSON序列化问题
        result = {
            'type': 'c/c++',
            'source_files': [],
            'header_files': [],
            'total_lines': 0,
            'functions': [],
            'includes': [],  # 使用列表而非集合
            'macros': [],    # 使用列表而非集合
        }

        # 内部使用集合去重，最后转换为列表
        includes_set: Set[str] = set()
        macros_set: Set[str] = set()

        try:
            # 查找源文件
            result['source_files'] = self.find_files(['.c', '.cpp', '.cc', '.cxx'])
            result['header_files'] = self.find_files(['.h', '.hpp', '.hxx'])

            # 统计行数
            for f in result['source_files'] + result['header_files']:
                result['total_lines'] += self.count_lines(f)

            # 分析函数
            for f in result['source_files'][:20]:  # 限制分析数量
                self._analyze_file(f, includes_set, macros_set, result['functions'])

        except Exception:
            # 即使发生异常也确保结果是可序列化的
            pass
        finally:
            # 确保集合被转换为列表
            result['includes'] = list(includes_set)[:20]
            result['macros'] = list(macros_set)[:20]

        return result

    def _analyze_file(self, file_path: str, includes_set: Set[str],
                      macros_set: Set[str], functions: List[Dict[str, str]]) -> None:
        """分析单个文件

        Args:
            file_path: 文件路径
            includes_set: include集合（用于去重）
            macros_set: 宏集合（用于去重）
            functions: 函数列表
        """
        content = self.read_file(file_path)
        if not content:
            return

        # 提取include
        for match in re.finditer(r'#include\s*[<"]([^>"]+)[>"]', content):
            includes_set.add(match.group(1))

        # 提取宏定义
        for match in re.finditer(r'#define\s+(\w+)', content):
            macros_set.add(match.group(1))

        # 提取函数定义 (简单匹配)
        for match in re.finditer(r'\b(\w+)\s*\([^)]*\)\s*\{', content):
            func_name = match.group(1)
            # 排除关键字
            keywords = {'if', 'while', 'for', 'switch', 'main', 'catch', 'else', 'try'}
            if func_name not in keywords:
                functions.append({
                    'name': func_name,
                    'file': os.path.basename(file_path)
                })