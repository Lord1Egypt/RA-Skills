#!/usr/bin/env python3
"""
TODO/FIXME 提取器
从源代码中提取 TODO、FIXME、HACK、XXX 等注释
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

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
class TodoItem:
    """TODO 项"""
    type: str  # TODO, FIXME, HACK, XXX, NOTE
    text: str
    file: str
    line: int
    author: Optional[str] = None
    priority: Optional[str] = None  # high, medium, low
    category: Optional[str] = None  # bug, feature, refactor, docs, test


class TodoExtractor:
    """TODO/FIXME 提取器"""

    # 注释类型模式
    TODO_PATTERNS = {
        'python': [
            r'#\s*(TODO|FIXME|HACK|XXX|NOTE)\s*[:\(]?\s*(.+?)(?:\s*--\s*(.+))?$',
        ],
        'javascript': [
            r'//\s*(TODO|FIXME|HACK|XXX|NOTE)\s*[:\(]?\s*(.+?)(?:\s*--\s*(.+))?$',
            r'/\*\s*(TODO|FIXME|HACK|XXX|NOTE)\s*[:\(]?\s*(.+?)(?:\s*--\s*(.+))?\s*\*/',
        ],
        'java': [
            r'//\s*(TODO|FIXME|HACK|XXX|NOTE)\s*[:\(]?\s*(.+?)(?:\s*--\s*(.+))?$',
            r'/\*\*\s*(TODO|FIXME|HACK|XXX|NOTE)\s*[:\(]?\s*(.+?)(?:\s*--\s*(.+))?\s*\*/',
        ],
        'c': [
            r'//\s*(TODO|FIXME|HACK|XXX|NOTE)\s*[:\(]?\s*(.+?)(?:\s*--\s*(.+))?$',
            r'/\*\s*(TODO|FIXME|HACK|XXX|NOTE)\s*[:\(]?\s*(.+?)(?:\s*--\s*(.+))?\s*\*/',
        ],
        'shell': [
            r'#\s*(TODO|FIXME|HACK|XXX|NOTE)\s*[:\(]?\s*(.+?)(?:\s*--\s*(.+))?$',
        ],
    }

    # 文件扩展名到语言的映射
    EXT_LANG_MAP = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'javascript',
        '.tsx': 'javascript',
        '.mjs': 'javascript',
        '.java': 'java',
        '.kt': 'java',
        '.kts': 'java',
        '.c': 'c',
        '.cpp': 'c',
        '.cc': 'c',
        '.cxx': 'c',
        '.h': 'c',
        '.hpp': 'c',
        '.sh': 'shell',
        '.bash': 'shell',
        '.zsh': 'shell',
    }

    # 优先级关键词
    PRIORITY_KEYWORDS = {
        'high': ['urgent', 'critical', 'important', 'asap', 'blocker'],
        'low': ['later', 'someday', 'maybe', 'optional'],
    }

    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir).resolve()
        self.todos: List[TodoItem] = []

    def extract(self) -> Dict[str, Any]:
        """提取所有 TODO 项"""
        logger.info(f"开始提取 TODO/FIXME: {self.project_dir}")

        self._scan_files()

        return self._generate_report()

    def _scan_files(self) -> None:
        """扫描所有源文件"""
        for root, dirs, files in os.walk(self.project_dir):
            # 排除特定目录
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for f in files:
                ext = Path(f).suffix.lower()
                lang = self.EXT_LANG_MAP.get(ext)

                if lang:
                    file_path = Path(root) / f
                    self._extract_from_file(file_path, lang)

    def _extract_from_file(self, file_path: Path, lang: str) -> None:
        """从单个文件提取 TODO"""
        patterns = self.TODO_PATTERNS.get(lang, [])
        if not patterns:
            return

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            rel_path = str(file_path.relative_to(self.project_dir))

            for line_num, line in enumerate(lines, 1):
                for pattern in patterns:
                    for match in re.finditer(pattern, line, re.IGNORECASE):
                        todo_type = match.group(1).upper()
                        text = match.group(2).strip() if len(match.groups()) > 1 else ''
                        author = match.group(3).strip() if len(match.groups()) > 2 else None

                        # 检测优先级
                        priority = self._detect_priority(text)

                        # 检测类别
                        category = self._detect_category(text)

                        self.todos.append(TodoItem(
                            type=todo_type,
                            text=text,
                            file=rel_path,
                            line=line_num,
                            author=author,
                            priority=priority,
                            category=category,
                        ))

        except Exception as e:
            logger.debug(f"处理文件失败 {file_path}: {e}")

    def _detect_priority(self, text: str) -> Optional[str]:
        """检测优先级"""
        text_lower = text.lower()
        for priority, keywords in self.PRIORITY_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    return priority
        return 'medium'

    def _detect_category(self, text: str) -> Optional[str]:
        """检测类别"""
        text_lower = text.lower()

        if any(kw in text_lower for kw in ['bug', 'fix', 'error', 'issue']):
            return 'bug'
        if any(kw in text_lower for kw in ['feature', 'add', 'implement', 'new']):
            return 'feature'
        if any(kw in text_lower for kw in ['refactor', 'clean', 'improve', 'optimize']):
            return 'refactor'
        if any(kw in text_lower for kw in ['doc', 'comment', 'readme']):
            return 'docs'
        if any(kw in text_lower for kw in ['test', 'spec', 'coverage']):
            return 'test'

        return None

    def _generate_report(self) -> Dict[str, Any]:
        """生成报告"""
        # 按类型统计
        type_counts = {}
        for todo in self.todos:
            type_counts[todo.type] = type_counts.get(todo.type, 0) + 1

        # 按优先级统计
        priority_counts = {}
        for todo in self.todos:
            if todo.priority:
                priority_counts[todo.priority] = priority_counts.get(todo.priority, 0) + 1

        # 按类别统计
        category_counts = {}
        for todo in self.todos:
            if todo.category:
                category_counts[todo.category] = category_counts.get(todo.category, 0) + 1

        return {
            'summary': {
                'total': len(self.todos),
                'by_type': type_counts,
                'by_priority': priority_counts,
                'by_category': category_counts,
            },
            'todos': [
                {
                    'type': t.type,
                    'text': t.text,
                    'file': t.file,
                    'line': t.line,
                    'author': t.author,
                    'priority': t.priority,
                    'category': t.category,
                }
                for t in self.todos
            ],
        }

    def generate_markdown_report(self) -> str:
        """生成 Markdown 格式的报告"""
        lines = [
            "# TODO/FIXME 报告",
            "",
            f"> 生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')} | 总计: {len(self.todos)} 项",
            "",
            "## 统计",
            "",
            "### 按类型",
            "",
            "| 类型 | 数量 |",
            "|------|------|",
        ]

        type_counts = {}
        for todo in self.todos:
            type_counts[todo.type] = type_counts.get(todo.type, 0) + 1

        for t, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            lines.append(f"| {t} | {count} |")

        lines.extend([
            "",
            "## 详情",
            "",
        ])

        # 按文件分组
        by_file = {}
        for todo in self.todos:
            if todo.file not in by_file:
                by_file[todo.file] = []
            by_file[todo.file].append(todo)

        for file_path, todos in sorted(by_file.items()):
            lines.append(f"### `{file_path}`")
            lines.append("")
            for todo in todos:
                priority_badge = f"[{todo.priority}]" if todo.priority else ""
                lines.append(f"- {todo.type} {priority_badge} (L{todo.line}): {todo.text}")
            lines.append("")

        return "\n".join(lines)


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: todo_extractor.py <project_dir> [--md]")
        print("\nOptions:")
        print("  --md    Generate markdown report")
        sys.exit(1)

    project_dir = sys.argv[1]
    generate_md = '--md' in sys.argv

    extractor = TodoExtractor(project_dir)

    if generate_md:
        extractor.extract()
        print(extractor.generate_markdown_report())
    else:
        result = extractor.extract()
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()