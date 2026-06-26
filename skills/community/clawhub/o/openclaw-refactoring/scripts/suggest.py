#!/usr/bin/env python3
"""
Refactoring - Suggestion Engine

Analyzes code and provides refactoring suggestions based on code smells.
"""

import ast
from pathlib import Path
from typing import Dict, List, Any


class SuggestionEngine:
    """Provides refactoring suggestions"""

    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()

    def analyze(self, target_path: str) -> List[Dict[str, Any]]:
        """Analyze code and return suggestions"""
        suggestions = []

        target = Path(target_path)
        if not target.is_absolute():
            target = self.root / target

        if target.is_file():
            suggestions.extend(self._analyze_file(target))
        elif target.is_dir():
            for py_file in target.rglob('*.py'):
                if py_file.is_file():
                    suggestions.extend(self._analyze_file(py_file))

        return suggestions

    def _analyze_file(self, filepath: Path) -> List[Dict[str, Any]]:
        """Analyze a single file"""
        suggestions = []

        try:
            content = filepath.read_text(encoding='utf-8')
            lines = content.split('\n')
            tree = ast.parse(content)
        except Exception:
            return suggestions

        # Check file length
        if len(lines) > 300:
            suggestions.append({
                'type': 'Large File',
                'severity': 'warning',
                'message': f'File has {len(lines)} lines',
                'location': f'{filepath.relative_to(self.root)}',
                'suggestion': 'Consider splitting into smaller modules'
            })

        # Analyze functions and classes
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                suggestions.extend(self._analyze_function(node, filepath, lines))
            elif isinstance(node, ast.ClassDef):
                suggestions.extend(self._analyze_class(node, filepath, lines))

        return suggestions

    def _analyze_function(self, node: ast.FunctionDef, filepath: Path, lines: List[str]) -> List[Dict[str, Any]]:
        """Analyze a function for refactoring suggestions"""
        suggestions = []

        # Check function length
        if node.end_lineno and node.lineno:
            func_lines = node.end_lineno - node.lineno
            if func_lines > 50:
                suggestions.append({
                    'type': 'Long Method',
                    'severity': 'warning',
                    'message': f'Function "{node.name}" is {func_lines} lines long',
                    'location': f'{filepath.relative_to(self.root)}:{node.lineno}',
                    'suggestion': 'Extract smaller methods'
                })

        # Check parameter count
        param_count = len(node.args.args) + len(node.args.kwonlyargs)
        if node.args.vararg:
            param_count += 1
        if node.args.kwarg:
            param_count += 1

        if param_count > 5:
            suggestions.append({
                'type': 'Long Parameter List',
                'severity': 'info',
                'message': f'Function "{node.name}" has {param_count} parameters',
                'location': f'{filepath.relative_to(self.root)}:{node.lineno}',
                'suggestion': 'Consider using a config object or data class'
            })

        # Check complexity
        complexity = self._calculate_complexity(node)
        if complexity > 10:
            suggestions.append({
                'type': 'High Complexity',
                'severity': 'warning',
                'message': f'Function "{node.name}" has complexity {complexity}',
                'location': f'{filepath.relative_to(self.root)}:{node.lineno}',
                'suggestion': 'Simplify conditionals or extract methods'
            })

        # Check for missing docstring
        if not ast.get_docstring(node) and not node.name.startswith('_'):
            suggestions.append({
                'type': 'Missing Docstring',
                'severity': 'info',
                'message': f'Function "{node.name}" lacks docstring',
                'location': f'{filepath.relative_to(self.root)}:{node.lineno}',
                'suggestion': 'Add a docstring explaining the function'
            })

        return suggestions

    def _analyze_class(self, node: ast.ClassDef, filepath: Path, lines: List[str]) -> List[Dict[str, Any]]:
        """Analyze a class for refactoring suggestions"""
        suggestions = []

        # Check class length
        if node.end_lineno and node.lineno:
            class_lines = node.end_lineno - node.lineno
            if class_lines > 300:
                suggestions.append({
                    'type': 'Large Class',
                    'severity': 'warning',
                    'message': f'Class "{node.name}" is {class_lines} lines long',
                    'location': f'{filepath.relative_to(self.root)}:{node.lineno}',
                    'suggestion': 'Consider splitting responsibilities'
                })

        # Count methods
        methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
        if len(methods) > 15:
            suggestions.append({
                'type': 'Too Many Methods',
                'severity': 'info',
                'message': f'Class "{node.name}" has {len(methods)} methods',
                'location': f'{filepath.relative_to(self.root)}:{node.lineno}',
                'suggestion': 'Consider extracting helper classes'
            })

        # Check for missing docstring
        if not ast.get_docstring(node):
            suggestions.append({
                'type': 'Missing Docstring',
                'severity': 'info',
                'message': f'Class "{node.name}" lacks docstring',
                'location': f'{filepath.relative_to(self.root)}:{node.lineno}',
                'suggestion': 'Add a class docstring'
            })

        return suggestions

    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.With):
                complexity += 1
            elif isinstance(child, ast.comprehension):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Refactoring Suggestion Engine')
    parser.add_argument('path', nargs='?', default='.', help='Path to analyze')
    parser.add_argument('--root', '-r', default='.', help='Project root')

    args = parser.parse_args()

    engine = SuggestionEngine(args.root)
    suggestions = engine.analyze(args.path)

    print(f"\n🔍 Refactoring Suggestions")
    print(f"{'='*60}")
    print(f"Found {len(suggestions)} suggestion(s)")
    print()

    for suggestion in suggestions:
        severity_emoji = "🔴" if suggestion['severity'] == 'error' else ("⚠️" if suggestion['severity'] == 'warning' else "ℹ️")
        print(f"{severity_emoji}  {suggestion['type']}: {suggestion['message']}")
        print(f"   📍 {suggestion['location']}")
        if suggestion.get('suggestion'):
            print(f"   💡 {suggestion['suggestion']}")
        print()


if __name__ == '__main__':
    main()
