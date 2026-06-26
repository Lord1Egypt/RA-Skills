#!/usr/bin/env python3
"""
解析器基类
提供统一的解析器接口和通用方法
"""

import os
import sys
import json
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ParserResult:
    """统一的解析结果格式"""
    name: str = ''
    version: str = ''
    description: str = ''
    dependencies: List[Dict[str, str]] = field(default_factory=list)
    dev_dependencies: List[Dict[str, str]] = field(default_factory=list)
    frameworks: List[str] = field(default_factory=list)
    build_system: str = ''
    language: str = ''
    entry_points: List[str] = field(default_factory=list)
    config_files: List[str] = field(default_factory=list)
    modules: List[Dict[str, Any]] = field(default_factory=list)
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'dependencies': self.dependencies,
            'dev_dependencies': self.dev_dependencies,
            'frameworks': self.frameworks,
            'build_system': self.build_system,
            'language': self.language,
            'entry_points': self.entry_points,
            'config_files': self.config_files,
            'modules': self.modules,
            'error': self.error,
        }


class BaseParser(ABC):
    """解析器基类"""

    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir).resolve()
        self.result = ParserResult()

    @abstractmethod
    def parse(self) -> ParserResult:
        """执行解析，子类必须实现"""
        pass

    @classmethod
    @abstractmethod
    def find_files(cls, project_dir: str) -> List[str]:
        """查找相关配置文件，子类必须实现"""
        pass

    def read_file(self, file_path: Path) -> Optional[str]:
        """读取文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except (IOError, OSError) as e:
            self.result.error = f"读取文件失败: {e}"
            return None

    def read_json_file(self, file_path: Path) -> Optional[Dict]:
        """读取 JSON 文件"""
        content = self.read_file(file_path)
        if content:
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                self.result.error = f"JSON 解析失败: {e}"
        return None

    def add_dependency(self, name: str, version: str = '',
                       dep_type: str = 'runtime', source: str = '') -> None:
        """添加依赖"""
        dep = {
            'name': name,
            'version': version,
            'type': dep_type,
        }
        if source:
            dep['source'] = source

        if dep_type == 'dev':
            self.result.dev_dependencies.append(dep)
        else:
            self.result.dependencies.append(dep)

    def add_framework(self, name: str, version: str = '') -> None:
        """添加框架"""
        framework = {'name': name}
        if version:
            framework['version'] = version
        self.result.frameworks.append(name)

    def file_exists(self, filename: str) -> bool:
        """检查文件是否存在"""
        return (self.project_dir / filename).exists()

    def find_files_by_pattern(self, pattern: str) -> List[Path]:
        """按模式查找文件"""
        return list(self.project_dir.glob(pattern))

    def find_files_by_extension(self, extension: str) -> List[Path]:
        """按扩展名查找文件"""
        return list(self.project_dir.rglob(f'*{extension}'))


def create_main_function(parser_class, parser_name: str, file_extensions: List[str] = None):
    """创建统一的 main 函数

    Args:
        parser_class: 解析器类
        parser_name: 解析器名称（用于帮助信息）
        file_extensions: 文件扩展名列表（用于查找文件）

    Returns:
        main 函数
    """
    def main():
        if len(sys.argv) < 2:
            print(f"Usage: {parser_name} <project_dir> [--find-files]")
            print(f"\nOptions:")
            print(f"  --find-files    Find {parser_name} config files only")
            sys.exit(1)

        project_dir = sys.argv[1]
        find_files_only = '--find-files' in sys.argv

        if find_files_only:
            files = parser_class.find_files(project_dir)
            print(json.dumps({'files': files}, indent=2))
        else:
            parser = parser_class(project_dir)
            result = parser.parse()
            print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

    return main


__all__ = [
    'ParserResult',
    'BaseParser',
    'create_main_function',
]