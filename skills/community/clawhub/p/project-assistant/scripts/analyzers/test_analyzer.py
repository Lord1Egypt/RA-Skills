#!/usr/bin/env python3
"""
测试分析器
分析项目测试覆盖率和测试模式
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field

# 导入统一常量
try:
    from constants import EXCLUDE_DIRS
except ImportError:
    EXCLUDE_DIRS = {
        '.git', '.svn', '.hg', '.idea', '.vscode',
        'node_modules', 'build', 'dist', 'out', 'bin', 'obj',
        '__pycache__', '.pytest_cache', '.mypy_cache',
        'target', 'vendor', 'CMakeFiles', '_deps',
        '.gradle', 'Pods', 'DerivedData',
        'venv', '.venv', 'env', '.env',
    }

# 添加日志支持
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)


@dataclass
class TestFile:
    """测试文件信息"""
    path: str
    framework: str
    test_count: int = 0
    test_cases: List[str] = field(default_factory=list)


@dataclass
class TestCoverage:
    """测试覆盖率信息"""
    total_source_files: int = 0
    total_test_files: int = 0
    covered_files: Set[str] = field(default_factory=set)
    uncovered_files: Set[str] = field(default_factory=set)


class TestAnalyzer:
    """测试分析器"""

    # 测试文件模式
    TEST_FILE_PATTERNS = {
        'pytest': {
            'pattern': r'test_.*\.py|.*_test\.py',
            'framework': 'pytest',
            'test_case_pattern': r'def\s+(test_\w+)\s*\(',
        },
        'unittest': {
            'pattern': r'test.*\.py',
            'framework': 'unittest',
            'test_case_pattern': r'def\s+(test\w*)\s*\(',
        },
        'jest': {
            'pattern': r'.*\.test\.(js|ts|jsx|tsx)|.*\.spec\.(js|ts|jsx|tsx)',
            'framework': 'jest',
            'test_case_pattern': r'(?:it|test|describe)\s*\(\s*[\'"]([^\'"]+)[\'"]',
        },
        'mocha': {
            'pattern': r'.*\.test\.(js|ts)|.*\.spec\.(js|ts)',
            'framework': 'mocha',
            'test_case_pattern': r'(?:it|describe)\s*\(\s*[\'"]([^\'"]+)[\'"]',
        },
        'junit': {
            'pattern': r'.*Test\.java|.*Tests\.java',
            'framework': 'junit',
            'test_case_pattern': r'@Test\s*(?:public\s+)?void\s+(\w+)',
        },
        'googletest': {
            'pattern': r'.*_test\.cpp|.*_test\.cc|.*Test\.cpp',
            'framework': 'googletest',
            'test_case_pattern': r'TEST(?:_[FP])?\s*\(\s*\w+\s*,\s*(\w+)',
        },
        'vitest': {
            'pattern': r'.*\.test\.(js|ts|jsx|tsx)|.*\.spec\.(js|ts|jsx|tsx)',
            'framework': 'vitest',
            'test_case_pattern': r'(?:it|test|describe)\s*\(\s*[\'"]([^\'"]+)[\'"]',
        },
        'kotest': {
            'pattern': r'.*Test\.kt|.*Spec\.kt',
            'framework': 'kotest',
            'test_case_pattern': r'test\s*\(\s*[\'"]([^\'"]+)[\'"]',
        },
    }

    # 源文件扩展名
    SOURCE_EXTENSIONS = {
        '.py', '.js', '.ts', '.jsx', '.tsx',
        '.java', '.kt', '.cpp', '.cc', '.c', '.go', '.rs',
    }

    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir).resolve()
        self.test_files: List[TestFile] = []
        self.coverage = TestCoverage()
        self.frameworks: Set[str] = set()

    def analyze(self) -> Dict[str, Any]:
        """执行分析"""
        logger.info(f"开始测试分析: {self.project_dir}")

        self._find_test_files()
        self._analyze_coverage()

        return self._generate_report()

    def _find_test_files(self) -> None:
        """查找所有测试文件"""
        for root, dirs, files in os.walk(self.project_dir):
            # 排除特定目录
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            # 优先检查测试目录
            rel_path = os.path.relpath(root, self.project_dir)
            is_test_dir = any(part in ['test', 'tests', '__tests__', 'spec', 'specs']
                            for part in Path(rel_path).parts)

            for f in files:
                file_path = Path(root) / f

                for framework, config in self.TEST_FILE_PATTERNS.items():
                    if re.match(config['pattern'], f):
                        self._analyze_test_file(file_path, framework, config)
                        self.frameworks.add(framework)
                        break

                # 统计源文件
                ext = Path(f).suffix.lower()
                if ext in self.SOURCE_EXTENSIONS and not self._is_test_file(f):
                    self.coverage.total_source_files += 1

    def _analyze_test_file(self, file_path: Path, framework: str, config: Dict) -> None:
        """分析单个测试文件"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # 提取测试用例
            test_cases = []
            for match in re.finditer(config['test_case_pattern'], content, re.MULTILINE):
                test_cases.append(match.group(1))

            rel_path = str(file_path.relative_to(self.project_dir))

            self.test_files.append(TestFile(
                path=rel_path,
                framework=config['framework'],
                test_count=len(test_cases),
                test_cases=test_cases[:20],  # 限制输出
            ))

            self.coverage.total_test_files += 1

            # 标记覆盖的源文件
            self._mark_covered_files(rel_path)

        except Exception as e:
            logger.debug(f"分析测试文件失败 {file_path}: {e}")

    def _is_test_file(self, filename: str) -> bool:
        """检查是否是测试文件"""
        lower_name = filename.lower()
        return any(
            re.match(config['pattern'], filename)
            for config in self.TEST_FILE_PATTERNS.values()
        )

    def _mark_covered_files(self, test_file: str) -> None:
        """标记被测试覆盖的源文件"""
        # 简单映射：test_foo.py -> foo.py
        test_name = Path(test_file).stem

        for pattern in ['test_', '_test', 'Test', 'Tests', '.test', '.spec', '_spec']:
            if test_name.startswith(pattern):
                source_name = test_name[len(pattern):]
            elif test_name.endswith(pattern):
                source_name = test_name[:-len(pattern)]
            else:
                continue

            # 查找对应的源文件
            for ext in self.SOURCE_EXTENSIONS:
                potential_source = self.project_dir / f"{source_name}{ext}"
                if potential_source.exists():
                    self.coverage.covered_files.add(str(potential_source.relative_to(self.project_dir)))
                    break

    def _analyze_coverage(self) -> None:
        """分析覆盖率"""
        # 计算未覆盖文件
        for root, dirs, files in os.walk(self.project_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for f in files:
                ext = Path(f).suffix.lower()
                if ext in self.SOURCE_EXTENSIONS and not self._is_test_file(f):
                    rel_path = str((Path(root) / f).relative_to(self.project_dir))
                    if rel_path not in self.coverage.covered_files:
                        self.coverage.uncovered_files.add(rel_path)

    def _generate_report(self) -> Dict[str, Any]:
        """生成报告"""
        # 计算覆盖率
        total = self.coverage.total_source_files
        covered = len(self.coverage.covered_files)
        coverage_percent = (covered / total * 100) if total > 0 else 0

        return {
            'summary': {
                'frameworks': list(self.frameworks),
                'total_test_files': self.coverage.total_test_files,
                'total_source_files': total,
                'total_test_cases': sum(f.test_count for f in self.test_files),
                'coverage_percent': round(coverage_percent, 1),
            },
            'test_files': [
                {
                    'path': tf.path,
                    'framework': tf.framework,
                    'test_count': tf.test_count,
                    'test_cases': tf.test_cases[:10],
                }
                for tf in self.test_files
            ],
            'uncovered_files': list(self.coverage.uncovered_files)[:50],
        }


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: test_analyzer.py <project_dir>")
        sys.exit(1)

    project_dir = sys.argv[1]

    analyzer = TestAnalyzer(project_dir)
    result = analyzer.analyze()
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()