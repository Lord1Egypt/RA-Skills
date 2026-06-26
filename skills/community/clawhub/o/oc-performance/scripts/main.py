#!/usr/bin/env python3
"""
Performance - Performance Analysis Tool
Supports Python and C/C++
"""

import argparse
import ast
import re
import sys
import time
from pathlib import Path

# Import C support library
c_support_path = Path(__file__).parent.parent.parent / 'c-support' / 'lib'
if c_support_path.exists():
    sys.path.insert(0, str(c_support_path))
    try:
        from c_parser import CParser
        C_SUPPORT_AVAILABLE = True
    except ImportError:
        C_SUPPORT_AVAILABLE = False
else:
    C_SUPPORT_AVAILABLE = False


class PerformanceAnalyzer:
    """Analyzes code for performance issues - supports Python and C"""

    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        self.c_parser = CParser() if C_SUPPORT_AVAILABLE else None

    def analyze_file(self, filepath: Path) -> list:
        """Analyze a file for performance issues"""
        if filepath.suffix in ['.c', '.h']:
            return self._analyze_c_file(filepath)
        else:
            return self._analyze_python_file(filepath)

    def _analyze_c_file(self, filepath: Path) -> list:
        """Analyze C/C++ file for performance issues"""
        issues = []

        try:
            content = filepath.read_text(encoding='utf-8')
            lines = content.split('\n')
        except Exception as e:
            return [{'line': 0, 'message': f'Parse error: {e}', 'severity': 'error'}]

        # Check for inefficient string operations
        for i, line in enumerate(lines, 1):
            code = line.split('//')[0]

            # strcat in loop
            if 'strcat(' in code or 'strcpy(' in code:
                issues.append({
                    'line': i,
                    'message': f'Potentially inefficient string operation',
                    'severity': 'medium',
                    'suggestion': 'Consider using strncat/strncpy or tracking buffer sizes'
                })

            # printf in loop (I/O in loop)
            if 'printf(' in code or 'fprintf(' in code or 'puts(' in code:
                issues.append({
                    'line': i,
                    'message': 'I/O operation in potentially hot path',
                    'severity': 'low',
                    'suggestion': 'Buffer output or reduce I/O frequency'
                })

            # malloc/free in loop
            if 'malloc(' in code or 'calloc(' in code:
                issues.append({
                    'line': i,
                    'message': 'Dynamic allocation in code',
                    'severity': 'medium',
                    'suggestion': 'Consider pre-allocating or using stack allocation if possible'
                })

            # recursion (simplified check)
            func_match = re.search(r'(\w+)\s*\([^)]*\)', code)
            if func_match:
                func_name = func_match.group(1)
                if func_name in content[:content.find(code)]:
                    # Simple heuristic: function name appears earlier in file
                    pass

        # Check function complexity using parser
        if self.c_parser:
            try:
                info = self.c_parser.parse_file(str(filepath))
                for func in info.functions:
                    if func.body_end and func.line:
                        func_lines = func.body_end - func.line
                        if func_lines > 100:
                            issues.append({
                                'line': func.line,
                                'message': f'Large function "{func.name}" ({func_lines} lines)',
                                'severity': 'medium',
                                'suggestion': 'Consider breaking into smaller functions for better optimization'
                            })
            except Exception:
                pass

        return issues

    def _analyze_python_file(self, filepath: Path) -> list:

        # Check for string concatenation in loops
        issues.extend(self._check_string_concat(tree, lines, filepath))

        # Check for unused imports
        issues.extend(self._check_unused_imports(tree, lines, filepath))

        # Check for nested loops
        issues.extend(self._check_nested_loops(tree, lines, filepath))

        return issues

    def _check_n_plus_one(self, tree: ast.AST, lines: list, filepath: Path) -> list:
        """Check for N+1 query patterns"""
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                # Check if loop body contains database/API calls
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        func_name = self._get_call_name(child)
                        if func_name and any(x in func_name.lower() for x in ['query', 'get', 'fetch', 'find']):
                            issues.append({
                                'line': node.lineno,
                                'message': f'Potential N+1 query: {func_name}() inside loop',
                                'severity': 'high',
                                'suggestion': 'Consider using JOIN or bulk fetch'
                            })

        return issues

    def _check_string_concat(self, tree: ast.AST, lines: list, filepath: Path) -> list:
        """Check for string concatenation in loops"""
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                for child in ast.walk(node):
                    if isinstance(child, ast.AugAssign):
                        if isinstance(child.op, ast.Add):
                            if isinstance(child.target, ast.Name):
                                issues.append({
                                    'line': child.lineno,
                                    'message': 'String concatenation in loop',
                                    'severity': 'medium',
                                    'suggestion': 'Use list + \'\'.join() instead'
                                })

        return issues

    def _check_unused_imports(self, tree: ast.AST, lines: list, filepath: Path) -> list:
        """Check for unused imports"""
        issues = []

        imports = {}
        used_names = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports[alias.asname or alias.name] = node.lineno
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports[alias.asname or alias.name] = node.lineno
            elif isinstance(node, ast.Name):
                used_names.add(node.id)

        for name, line in imports.items():
            if name not in used_names and not name.startswith('_'):
                issues.append({
                    'line': line,
                    'message': f'Unused import: {name}',
                    'severity': 'low',
                    'suggestion': 'Remove unused import'
                })

        return issues

    def _check_nested_loops(self, tree: ast.AST, lines: list, filepath: Path) -> list:
        """Check for nested loops"""
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                for child in ast.iter_child_nodes(node):
                    if isinstance(child, ast.For):
                        issues.append({
                            'line': child.lineno,
                            'message': 'Nested loop detected (O(n²))',
                            'severity': 'high',
                            'suggestion': 'Consider optimizing algorithm or using data structures'
                        })

        return issues

    def _get_call_name(self, node: ast.Call) -> str:
        """Get function call name"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return None


def run_profile(args):
    """Profile code execution"""
    print("\n🔍 Performance Profile")
    print(f"{'='*60}")
    print(f"File: {args.file}")
    if args.function:
        print(f"Function: {args.function}")
    print()
    print("ℹ️  Profiling requires running the code.")
    print("Use Python's built-in cProfile for detailed profiling:")
    print(f"  python3 -m cProfile -o output.prof {args.file}")
    print()
    print("Or use line_profiler for line-by-line profiling:")
    print("  kernprof -l -v {args.file}")


def run_analyze(args):
    """Analyze code for performance issues"""
    analyzer = PerformanceAnalyzer(args.root)

    if args.file:
        filepath = Path(args.file)
        if not filepath.exists():
            print(f"❌ File not found: {args.file}")
            return

        issues = analyzer.analyze_file(filepath)
        files = [(filepath, issues)]
    elif args.dir:
        dirpath = Path(args.dir)
        if not dirpath.exists():
            print(f"❌ Directory not found: {args.dir}")
            return

        files = []
        # Python files
        for py_file in dirpath.rglob('*.py'):
            issues = analyzer.analyze_file(py_file)
            if issues:
                files.append((py_file, issues))
        # C files
        for c_file in dirpath.rglob('*.c'):
            issues = analyzer.analyze_file(c_file)
            if issues:
                files.append((c_file, issues))
    else:
        print("❌ Specify --file or --dir")
        return

    print("\n🔍 Performance Analysis")
    print(f"{'='*60}")

    total_issues = sum(len(issues) for _, issues in files)
    print(f"Files analyzed: {len(files)}")
    print(f"Issues found: {total_issues}")

    for filepath, issues in files:
        if not issues:
            continue

        print(f"\n📄 {filepath}")

        # Sort by severity
        severity_order = {'high': 0, 'medium': 1, 'low': 2, 'error': 3}
        issues.sort(key=lambda x: severity_order.get(x['severity'], 4))

        for issue in issues:
            emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢', 'error': '❌'}.get(issue['severity'], '⚪')
            print(f"  {emoji} Line {issue['line']}: {issue['message']}")
            if 'suggestion' in issue:
                print(f"     💡 {issue['suggestion']}")


def run_benchmark(args):
    """Run benchmark"""
    print("\n⏱️  Benchmark")
    print(f"{'='*60}")
    print(f"File: {args.file}")
    if args.function:
        print(f"Function: {args.function}")
    print()
    print("ℹ️  For accurate benchmarking, use timeit:")
    mod_name = args.file.replace('.py', '').replace('/', '.')
    func_name = args.function or 'main'
    print(f"  python3 -m timeit -n 1000 -r 5 -s 'from {mod_name} import {func_name}' '{func_name}()'")


def main():
    parser = argparse.ArgumentParser(
        description='Performance Analysis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py profile --file src.py
  python3 main.py analyze --file src.py
  python3 main.py analyze --dir src/
  python3 main.py benchmark --file src.py --function foo
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # profile command
    profile_parser = subparsers.add_parser('profile', help='Profile code')
    profile_parser.add_argument('--file', required=True, help='File to profile')
    profile_parser.add_argument('--function', help='Function to profile')
    profile_parser.add_argument('--root', default='.', help='Project root')
    profile_parser.set_defaults(func=run_profile)

    # analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze code')
    analyze_parser.add_argument('--file', help='File to analyze')
    analyze_parser.add_argument('--dir', help='Directory to analyze')
    analyze_parser.add_argument('--root', default='.', help='Project root')
    analyze_parser.set_defaults(func=run_analyze)

    # benchmark command
    benchmark_parser = subparsers.add_parser('benchmark', help='Run benchmark')
    benchmark_parser.add_argument('--file', required=True, help='File to benchmark')
    benchmark_parser.add_argument('--function', help='Function to benchmark')
    benchmark_parser.add_argument('--root', default='.', help='Project root')
    benchmark_parser.set_defaults(func=run_benchmark)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == '__main__':
    main()
