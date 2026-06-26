#!/usr/bin/env python3
"""
TDD - Test Generator

Generates test cases from code analysis.
"""

import ast
import inspect
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple


class TestGenerator:
    """Generates test cases from Python code"""

    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        self.test_dir = self.root / 'tests'

    def generate_for_function(self, func_name: str, file_path: Path) -> str:
        """Generate tests for a specific function"""
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content)
        except Exception as e:
            return f"# Error parsing file: {e}"

        # Find the function
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == func_name:
                return self._generate_function_tests(node, file_path)

        return f"# Function '{func_name}' not found in {file_path}"

    def generate_for_file(self, file_path: Path) -> str:
        """Generate tests for all functions in a file"""
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content)
        except Exception as e:
            return f"# Error parsing file: {e}"

        tests = []
        module_name = file_path.stem

        # Generate imports
        tests.append(f"import pytest")
        tests.append(f"from {module_name} import *")
        tests.append("")

        # Find all functions and classes
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not node.name.startswith('_'):  # Skip private functions
                    test = self._generate_function_tests(node, file_path, standalone=False)
                    tests.append(test)
                    tests.append("")
            elif isinstance(node, ast.ClassDef):
                test = self._generate_class_tests(node, file_path)
                tests.append(test)
                tests.append("")

        return "\n".join(tests)

    def _generate_function_tests(self, node: ast.FunctionDef, file_path: Path,
                                  standalone: bool = True) -> str:
        """Generate tests for a single function"""
        func_name = node.name
        lines = []

        if standalone:
            module_name = file_path.stem
            lines.append(f"import pytest")
            lines.append(f"from {module_name} import {func_name}")
            lines.append("")

        # Generate test function
        lines.append(f"def test_{func_name}():")
        lines.append(f'    """Test {func_name} function"""')

        # Analyze parameters
        params = self._analyze_params(node)

        # Generate normal case
        lines.append("    # Normal case")
        args_str = self._generate_args(params)
        lines.append(f"    result = {func_name}({args_str})")
        lines.append(f"    assert result is not None")
        lines.append("")

        # Generate edge cases
        lines.append("    # Edge cases")
        for i, edge_args in enumerate(self._generate_edge_cases(params), 1):
            lines.append(f"    # Case {i}: {edge_args['description']}")
            args_str = ", ".join(f"{k}={v}" for k, v in edge_args['args'].items())
            lines.append(f"    result = {func_name}({args_str})")
            if edge_args.get('should_raise'):
                lines.append(f"    # Should raise {edge_args['should_raise']}")
            else:
                lines.append(f"    assert result is not None")
            lines.append("")

        return "\n".join(lines)

    def _generate_class_tests(self, node: ast.ClassDef, file_path: Path) -> str:
        """Generate tests for a class"""
        class_name = node.name
        lines = []

        lines.append(f"class Test{class_name}:")
        lines.append(f'    """Tests for {class_name}"""')
        lines.append("")

        # Find methods
        methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]

        for method in methods:
            if method.name == '__init__':
                # Generate setup
                lines.append("    def setup_method(self):")
                lines.append(f"        self.obj = {class_name}()")
                lines.append("")
            elif not method.name.startswith('_'):
                # Generate test for method
                lines.append(f"    def test_{method.name}(self):")
                lines.append(f'        """Test {method.name} method"""')
                lines.append(f"        result = self.obj.{method.name}()")
                lines.append(f"        assert result is not None")
                lines.append("")

        return "\n".join(lines)

    def _analyze_params(self, node: ast.FunctionDef) -> List[Dict[str, Any]]:
        """Analyze function parameters"""
        params = []

        for arg in node.args.args:
            param_info = {
                'name': arg.arg,
                'type': None,
                'default': None
            }

            # Get type annotation
            if arg.annotation:
                if isinstance(arg.annotation, ast.Name):
                    param_info['type'] = arg.annotation.id
                elif isinstance(arg.annotation, ast.Constant):
                    param_info['type'] = arg.annotation.value

            params.append(param_info)

        # Match defaults
        defaults_start = len(params) - len(node.args.defaults)
        for i, default in enumerate(node.args.defaults):
            if isinstance(default, ast.Constant):
                params[defaults_start + i]['default'] = default.value

        return params

    def _generate_args(self, params: List[Dict[str, Any]]) -> str:
        """Generate arguments string for test"""
        args = []
        for p in params:
            name = p['name']
            if name == 'self':
                continue

            if p.get('default') is not None:
                args.append(f"{name}={repr(p['default'])}")
            elif p['type'] == 'int':
                args.append(f"{name}=42")
            elif p['type'] == 'float':
                args.append(f"{name}=3.14")
            elif p['type'] == 'str':
                args.append(f"{name}='test'")
            elif p['type'] == 'bool':
                args.append(f"{name}=True")
            elif p['type'] == 'list':
                args.append(f"{name}=[1, 2, 3]")
            elif p['type'] == 'dict':
                args.append(f"{name}={{'key': 'value'}}")
            else:
                args.append(f"{name}=None")

        return ", ".join(args)

    def _generate_edge_cases(self, params: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate edge case arguments"""
        cases = []

        # Empty/null cases
        for p in params:
            if p['name'] == 'self':
                continue

            if p['type'] in ('str', 'list', 'dict'):
                cases.append({
                    'description': f'empty {p["name"]}',
                    'args': {p['name']: "''" if p['type'] == 'str' else '[]' if p['type'] == 'list' else '{}'},
                    'should_raise': None
                })
            elif p['type'] in ('int', 'float'):
                cases.append({
                    'description': f'zero {p["name"]}',
                    'args': {p['name']: 0},
                    'should_raise': None
                })
                cases.append({
                    'description': f'negative {p["name"]}',
                    'args': {p['name']: -1},
                    'should_raise': 'ValueError'
                })

        return cases[:3]  # Limit edge cases


def main():
    import argparse

    parser = argparse.ArgumentParser(description='TDD Test Generator')
    parser.add_argument('--file', '-f', required=True, help='Source file')
    parser.add_argument('--function', help='Specific function to test')
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--root', '-r', default='.', help='Project root')

    args = parser.parse_args()

    generator = TestGenerator(args.root)
    file_path = Path(args.file)

    if not file_path.is_absolute():
        file_path = Path(args.root) / file_path

    if args.function:
        result = generator.generate_for_function(args.function, file_path)
    else:
        result = generator.generate_for_file(file_path)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result, encoding='utf-8')
        print(f"✅ Tests written to: {args.output}")
    else:
        print(result)


if __name__ == '__main__':
    main()
