#!/usr/bin/env python3
"""
解析器模块
提供各种项目配置文件的解析功能

统一返回格式:
    所有解析器返回一个字典，包含以下可选字段:
    - name: 项目/模块名称
    - version: 版本号
    - description: 描述
    - dependencies: 依赖列表
    - frameworks: 使用的框架
    - error: 错误信息
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

# 导入各解析器
from .cmake_parser import parse_cmake, find_cmake_files
from .gradle_parser import parse_gradle, find_gradle_files
from .manifest_parser import parse_manifest, find_manifest
from .package_json_parser import parse_package_json, find_package_json
from .maven_parser import parse_pom, find_pom_files
from .python_parser import (
    parse_requirements,
    parse_pyproject,
    parse_setup_py,
    analyze_python_project,
)
from .go_parser import parse_go_mod, detect_go_framework
from .rust_parser import parse_cargo_toml, detect_rust_framework
from .android_native_parser import (
    parse_android_mk,
    parse_application_mk,
    find_native_files,
    find_jni_functions,
)


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


def normalize_parse_result(result: Dict[str, Any], parser_type: str) -> ParserResult:
    """规范化解析结果

    Args:
        result: 原始解析结果
        parser_type: 解析器类型 (cmake, gradle, package_json, etc.)

    Returns:
        规范化的 ParserResult 对象
    """
    normalized = ParserResult()

    # 根据不同解析器类型进行映射
    name_mapping = {
        'cmake': 'project_name',
        'gradle': 'applicationId',
        'package_json': 'name',
        'maven': 'artifactId',
        'python': 'name',
        'go': 'module',
        'rust': 'name',
        'android_native': 'local_module',
    }

    version_mapping = {
        'cmake': 'project_version',
        'package_json': 'version',
        'maven': 'version',
        'python': 'version',
        'rust': 'version',
        'go': 'go_version',
        'gradle': 'versionName',
    }

    # 映射名称
    name_key = name_mapping.get(parser_type, 'name')
    normalized.name = result.get(name_key, result.get('name', ''))

    # 映射版本
    version_key = version_mapping.get(parser_type, 'version')
    normalized.version = result.get(version_key, result.get('version', ''))

    # 描述
    normalized.description = result.get('description', '')

    # 依赖
    deps = result.get('dependencies', [])
    if isinstance(deps, dict):
        # 转换字典格式为列表格式
        normalized.dependencies = [
            {'name': k, 'version': v}
            for k, v in deps.items()
        ]
    elif isinstance(deps, list):
        normalized.dependencies = deps

    # 开发依赖
    dev_deps = result.get('dev_dependencies', result.get('devDependencies', []))
    if isinstance(dev_deps, dict):
        normalized.dev_dependencies = [
            {'name': k, 'version': v}
            for k, v in dev_deps.items()
        ]
    elif isinstance(dev_deps, list):
        normalized.dev_dependencies = dev_deps

    # 框架
    frameworks = result.get('frameworks', [])
    if isinstance(frameworks, list):
        normalized.frameworks = [
            f.get('name', f) if isinstance(f, dict) else f
            for f in frameworks
        ]

    # 错误
    normalized.error = result.get('error')

    return normalized


__all__ = [
    # 结果类型
    'ParserResult',
    'normalize_parse_result',
    # CMake
    'parse_cmake',
    'find_cmake_files',
    # Gradle
    'parse_gradle',
    'find_gradle_files',
    # Android Manifest
    'parse_manifest',
    'find_manifest',
    # package.json
    'parse_package_json',
    'find_package_json',
    # Maven
    'parse_pom',
    'find_pom_files',
    # Python
    'parse_requirements',
    'parse_pyproject',
    'parse_setup_py',
    'analyze_python_project',
    # Go
    'parse_go_mod',
    'detect_go_framework',
    # Rust
    'parse_cargo_toml',
    'detect_rust_framework',
    # Android Native
    'parse_android_mk',
    'parse_application_mk',
    'find_native_files',
    'find_jni_functions',
]