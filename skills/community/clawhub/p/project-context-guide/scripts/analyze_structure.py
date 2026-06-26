"""
项目结构分析器 - 生成模块依赖图

这个脚本分析项目结构，识别核心模块、文件依赖关系和关键入口点。
"""

import os
import ast
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import json


class ProjectStructureAnalyzer:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.file_dependencies = defaultdict(set)
        self.module_structure = defaultdict(list)
        self.entry_points = []
        self.core_modules = []

    def analyze(self) -> Dict:
        """执行完整的项目结构分析"""
        print(f"分析项目结构: {self.project_root}")

        # 1. 扫描所有代码文件
        code_files = self._find_code_files()
        print(f"找到 {len(code_files)} 个代码文件")

        # 2. 分析每个文件的依赖关系
        for file_path in code_files:
            self._analyze_file_dependencies(file_path)

        # 3. 识别入口点（main 函数、app 初始化等）
        self._identify_entry_points(code_files)

        # 4. 识别核心模块（高引用次数）
        self._identify_core_modules()

        # 5. 构建模块层级结构
        self._build_module_structure(code_files)

        # 6. 生成分析报告
        return self._generate_report()

    def _find_code_files(self) -> List[Path]:
        """查找所有代码文件"""
        code_files = []
        extensions = ['.py', '.js', '.ts', '.tsx', '.java', '.go']

        for ext in extensions:
            code_files.extend(self.project_root.rglob(f'*{ext}'))

        return code_files

    def _analyze_file_dependencies(self, file_path: Path):
        """分析单个文件的依赖关系"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if file_path.suffix == '.py':
                self._parse_python_dependencies(file_path, content)
            elif file_path.suffix in ['.js', '.ts', '.tsx']:
                self._parse_javascript_dependencies(file_path, content)
            # 可以扩展其他语言的解析

        except Exception as e:
            print(f"解析文件失败 {file_path}: {e}")

    def _parse_python_dependencies(self, file_path: Path, content: str):
        """解析 Python 文件的依赖"""
        try:
            tree = ast.parse(content)
            imports = []

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)

            # 过滤并记录本地模块依赖
            for imp in imports:
                if self._is_local_module(imp):
                    self.file_dependencies[str(file_path)].add(imp)

        except SyntaxError:
            pass

    def _parse_javascript_dependencies(self, file_path: Path, content: str):
        """解析 JavaScript/TypeScript 文件的依赖"""
        import re

        # 简单的 import 语句匹配
        patterns = [
            r'import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]',
            r'require\([\'"]([^\'"]+)[\'"]\)',
            r'import\([\'"]([^\'"]+)[\'"]\)',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if not match.startswith('.') and not match.startswith('/'):
                    # 记录外部依赖
                    self.file_dependencies[str(file_path)].add(match)

    def _is_local_module(self, module_name: str) -> bool:
        """判断是否为本地模块"""
        # 简单判断：如果模块名与项目中的目录匹配
        module_path = self.project_root / module_name.replace('.', os.sep)
        return module_path.exists()

    def _identify_entry_points(self, code_files: List[Path]):
        """识别项目入口点"""
        for file_path in code_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                if file_path.suffix == '.py':
                    if 'if __name__' in content or 'app.run(' in content or 'main()' in content:
                        self.entry_points.append(str(file_path))
                elif file_path.suffix in ['.js', '.ts']:
                    if 'ReactDOM.render' in content or 'new App' in content or 'main()' in content:
                        self.entry_points.append(str(file_path))

            except Exception:
                continue

    def _identify_core_modules(self):
        """识别核心模块（被引用次数最多的文件）"""
        # 计算每个文件被引用的次数
        reference_count = defaultdict(int)

        for file_path, deps in self.file_dependencies.items():
            for dep in deps:
                reference_count[dep] += 1

        # 取前 10 个最常被引用的模块
        sorted_modules = sorted(reference_count.items(), key=lambda x: x[1], reverse=True)
        self.core_modules = sorted_modules[:10]

    def _build_module_structure(self, code_files: List[Path]):
        """构建模块层级结构"""
        for file_path in code_files:
            rel_path = file_path.relative_to(self.project_root)
            parts = list(rel_path.parts[:-1])  # 去掉文件名，保留目录

            if parts:
                module_level = '.'.join(parts[:2])  # 取前两级作为模块
                self.module_structure[module_level].append(str(file_path))

    def _generate_report(self) -> Dict:
        """生成分析报告"""
        return {
            'project_root': str(self.project_root),
            'entry_points': self.entry_points,
            'core_modules': [
                {'module': m, 'reference_count': c} for m, c in self.core_modules
            ],
            'module_structure': dict(self.module_structure),
            'file_dependencies': {
                k: list(v) for k, v in self.file_dependencies.items()
            },
            'statistics': {
                'total_files': len(self.file_dependencies),
                'total_dependencies': sum(len(v) for v in self.file_dependencies.values()),
                'avg_dependencies': sum(len(v) for v in self.file_dependencies.values()) / max(len(self.file_dependencies), 1)
            }
        }


def analyze_project(project_root: str, output_file: str = None) -> Dict:
    """
    分析项目结构

    Args:
        project_root: 项目根目录路径
        output_file: 输出 JSON 文件路径（可选）

    Returns:
        分析报告字典
    """
    analyzer = ProjectStructureAnalyzer(project_root)
    report = analyzer.analyze()

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"报告已保存到: {output_file}")

    return report


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("用法: python analyze_structure.py <项目根目录> [输出文件]")
        sys.exit(1)

    project_root = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    report = analyze_project(project_root, output_file)

    # 打印摘要
    print("\n=== 项目结构分析摘要 ===")
    print(f"入口点: {len(report['entry_points'])} 个")
    for ep in report['entry_points']:
        print(f"  - {ep}")

    print(f"\n核心模块 (Top 10):")
    for module in report['core_modules']:
        print(f"  - {module['module']}: {module['reference_count']} 次引用")

    print(f"\n统计:")
    print(f"  - 总文件数: {report['statistics']['total_files']}")
    print(f"  - 总依赖数: {report['statistics']['total_dependencies']}")
    print(f"  - 平均依赖数: {report['statistics']['avg_dependencies']:.2f}")
