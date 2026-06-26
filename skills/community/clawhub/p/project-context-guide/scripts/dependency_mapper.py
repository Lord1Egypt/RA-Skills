"""
依赖映射器 - 分析代码调用关系和影响范围

这个脚本深入分析函数/类级别的调用关系，帮助理解代码修改的影响范围。
"""

import ast
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import json


class DependencyMapper:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.function_calls = defaultdict(set)  # 调用者 -> 被调用的函数
        self.function_callers = defaultdict(set)  # 被调用的函数 -> 调用者
        self.class_inheritance = defaultdict(list)  # 子类 -> 父类
        self.function_locations = {}  # 函数名 -> 文件位置

    def analyze(self) -> Dict:
        """执行完整的依赖映射分析"""
        print(f"分析代码依赖关系: {self.project_root}")

        # 扫描 Python 文件
        python_files = list(self.project_root.rglob('*.py'))
        print(f"找到 {len(python_files)} 个 Python 文件")

        for file_path in python_files:
            self._analyze_python_file(file_path)

        # 生成调用链
        call_chains = self._build_call_chains()

        return {
            'project_root': str(self.project_root),
            'function_calls': {
                caller: list(callees)
                for caller, callees in self.function_calls.items()
            },
            'function_callers': {
                callee: list(callers)
                for callee, callers in self.function_callers.items()
            },
            'class_inheritance': dict(self.class_inheritance),
            'function_locations': self.function_locations,
            'call_chains': call_chains,
            'statistics': {
                'total_functions': len(self.function_locations),
                'total_calls': sum(len(v) for v in self.function_calls.values()),
                'avg_call_depth': self._calculate_avg_depth()
            }
        }

    def _analyze_python_file(self, file_path: Path):
        """分析单个 Python 文件的依赖关系"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)
            analyzer = FunctionCallAnalyzer(file_path)
            analyzer.visit(tree)

            # 合并结果
            for caller, callees in analyzer.function_calls.items():
                self.function_calls[caller].update(callees)
                for callee in callees:
                    self.function_callers[callee].add(caller)

            self.class_inheritance.update(analyzer.class_inheritance)
            self.function_locations.update(analyzer.function_locations)

        except Exception as e:
            print(f"分析文件失败 {file_path}: {e}")

    def _build_call_chains(self) -> List[Dict]:
        """构建调用链（深度前 10 的调用路径）"""
        chains = []

        # 找出所有根函数（不被其他函数调用的函数）
        root_functions = set(self.function_calls.keys()) - set(self.function_callers.keys())

        for root in list(root_functions)[:10]:  # 限制数量
            chain = self._trace_call_chain(root, depth=0, max_depth=5)
            if len(chain) > 1:
                chains.append(chain)

        return chains

    def _trace_call_chain(self, func_name: str, depth: int, max_depth: int,
                          visited: Set[str] = None) -> List[Dict]:
        """追踪调用链"""
        if visited is None:
            visited = set()

        if depth >= max_depth or func_name in visited:
            return []

        visited.add(func_name)
        chain = []

        # 获取函数位置
        location = self.function_locations.get(func_name, {'file': 'unknown', 'line': 0})
        chain.append({
            'function': func_name,
            'file': location['file'],
            'line': location['line'],
            'depth': depth
        })

        # 递归追踪被调用的函数
        callees = self.function_calls.get(func_name, set())
        for callee in list(callees)[:3]:  # 限制分支数量
            sub_chain = self._trace_call_chain(callee, depth + 1, max_depth, visited.copy())
            chain.extend(sub_chain)

        return chain

    def _calculate_avg_depth(self) -> float:
        """计算平均调用深度"""
        if not self.function_calls:
            return 0.0

        total_depth = 0
        count = 0

        for caller in list(self.function_calls.keys())[:100]:  # 采样
            depth = self._calculate_function_depth(caller, 0, set())
            total_depth += depth
            count += 1

        return total_depth / max(count, 1)

    def _calculate_function_depth(self, func_name: str, current_depth: int,
                                   visited: Set[str]) -> int:
        """计算函数调用深度"""
        if func_name in visited or current_depth > 10:
            return current_depth

        visited.add(func_name)

        max_child_depth = current_depth
        for callee in self.function_calls.get(func_name, set()):
            child_depth = self._calculate_function_depth(callee, current_depth + 1, visited)
            max_child_depth = max(max_child_depth, child_depth)

        return max_child_depth

    def get_impact_analysis(self, function_name: str) -> Dict:
        """
        分析函数修改的影响范围

        Args:
            function_name: 要分析的函数名

        Returns:
            影响分析结果
        """
        # 向上：谁调用了这个函数
        callers = self.function_callers.get(function_name, [])

        # 向下：这个函数调用了哪些函数
        callees = self.function_calls.get(function_name, [])

        # 向上递归追踪所有间接调用者
        all_callers = self._trace_upstream(function_name, visited=set())

        # 向下递归追踪所有间接被调用者
        all_callees = self._trace_downstream(function_name, visited=set())

        return {
            'function': function_name,
            'direct_callers': list(callers),
            'direct_callees': list(callees),
            'all_upstream': list(all_callers),
            'all_downstream': list(all_callees),
            'impact_score': len(all_callers) + len(all_callees),
            'location': self.function_locations.get(function_name)
        }

    def _trace_upstream(self, func_name: str, visited: Set[str]) -> Set[str]:
        """向上追踪所有调用者"""
        if func_name in visited:
            return set()

        visited.add(func_name)
        callers = self.function_callers.get(func_name, set())

        all_callers = set(callers)
        for caller in callers:
            all_callers.update(self._trace_upstream(caller, visited))

        return all_callers

    def _trace_downstream(self, func_name: str, visited: Set[str]) -> Set[str]:
        """向下追踪所有被调用者"""
        if func_name in visited:
            return set()

        visited.add(func_name)
        callees = self.function_calls.get(func_name, set())

        all_callees = set(callees)
        for callee in callees:
            all_callees.update(self._trace_downstream(callee, visited))

        return all_callees


class FunctionCallAnalyzer(ast.NodeVisitor):
    """AST 访问器，用于分析函数调用"""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.function_calls = defaultdict(set)
        self.function_callers = defaultdict(set)
        self.class_inheritance = defaultdict(list)
        self.function_locations = {}
        self.current_class = None
        self.current_function = None

    def visit_FunctionDef(self, node):
        """访问函数定义"""
        old_function = self.current_function

        # 构建函数全名
        func_name = node.name
        if self.current_class:
            func_name = f"{self.current_class}.{node.name}"

        self.current_function = func_name

        # 记录函数位置
        self.function_locations[func_name] = {
            'file': str(self.file_path),
            'line': node.lineno
        }

        # 分析函数体中的调用
        self.generic_visit(node)

        self.current_function = old_function

    def visit_ClassDef(self, node):
        """访问类定义"""
        old_class = self.current_class
        self.current_class = node.name

        # 记录继承关系
        for base in node.bases:
            if isinstance(base, ast.Name):
                self.class_inheritance[node.name].append(base.id)
            elif isinstance(base, ast.Attribute):
                self.class_inheritance[node.name].append(ast.unparse(base))

        self.generic_visit(node)
        self.current_class = old_class

    def visit_Call(self, node):
        """访问函数调用"""
        if self.current_function:
            func_name = self._get_call_name(node)
            if func_name:
                self.function_calls[self.current_function].add(func_name)
                self.function_callers[func_name].add(self.current_function)

        self.generic_visit(node)

    def _get_call_name(self, node) -> str:
        """获取调用名称"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return ast.unparse(node.func)
        elif isinstance(node.func, ast.Call):
            return self._get_call_name(node.func)

        return None


def map_dependencies(project_root: str, function_name: str = None,
                     output_file: str = None) -> Dict:
    """
    映射项目依赖关系

    Args:
        project_root: 项目根目录
        function_name: 要分析的特定函数名（可选）
        output_file: 输出 JSON 文件路径（可选）

    Returns:
        依赖映射结果
    """
    mapper = DependencyMapper(project_root)
    report = mapper.analyze()

    if function_name:
        report['impact_analysis'] = mapper.get_impact_analysis(function_name)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"报告已保存到: {output_file}")

    return report


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("用法: python dependency_mapper.py <项目根目录> [函数名] [输出文件]")
        sys.exit(1)

    project_root = sys.argv[1]
    function_name = sys.argv[2] if len(sys.argv) > 2 else None
    output_file = sys.argv[3] if len(sys.argv) > 3 else None

    report = map_dependencies(project_root, function_name, output_file)

    print("\n=== 依赖映射分析摘要 ===")
    print(f"总函数数: {report['statistics']['total_functions']}")
    print(f"总调用数: {report['statistics']['total_calls']}")
    print(f"平均调用深度: {report['statistics']['avg_call_depth']:.2f}")

    if function_name:
        impact = report.get('impact_analysis', {})
        if impact:
            print(f"\n函数 '{function_name}' 的影响分析:")
            print(f"  - 直接调用者: {len(impact['direct_callers'])} 个")
            print(f"  - 直接被调用者: {len(impact['direct_callees'])} 个")
            print(f"  - 影响分数: {impact['impact_score']}")
