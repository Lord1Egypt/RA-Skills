#!/usr/bin/env python3
"""
Debugging Assistant - Main Entry Point
"""

import argparse
import re
import sys
from pathlib import Path


def analyze_error(error_text: str) -> dict:
    """Analyze error text and provide insights"""
    result = {
        'error_type': 'Unknown',
        'severity': 'info',
        'root_cause': '',
        'suggestions': [],
    }

    # Python traceback patterns
    if 'Traceback (most recent call last):' in error_text:
        result['error_type'] = 'Python Exception'

        # Extract exception type
        lines = error_text.strip().split('\n')
        for line in reversed(lines):
            if ':' in line and not line.startswith(' '):
                parts = line.split(':', 1)
                exception_type = parts[0].strip()
                message = parts[1].strip() if len(parts) > 1 else ''

                result['exception_type'] = exception_type
                result['message'] = message

                # Classify severity
                if exception_type in ('SyntaxError', 'IndentationError'):
                    result['severity'] = 'error'
                    result['root_cause'] = 'Code syntax issue'
                elif 'Error' in exception_type:
                    result['severity'] = 'error'
                    result['root_cause'] = f'{exception_type}: {message}'
                elif 'Warning' in exception_type:
                    result['severity'] = 'warning'
                    result['root_cause'] = message
                else:
                    result['severity'] = 'error'
                    result['root_cause'] = message

                # Provide suggestions
                if 'ImportError' in exception_type or 'ModuleNotFoundError' in exception_type:
                    result['suggestions'] = [
                        'Check if the module is installed: pip install <module>',
                        'Verify the import path is correct',
                        'Check if you\'re in the correct virtual environment',
                    ]
                elif 'AttributeError' in exception_type:
                    result['suggestions'] = [
                        "Check if the object has the attribute you're accessing",
                        'Verify the object type',
                        'Check for typos in attribute name',
                    ]
                elif 'KeyError' in exception_type:
                    result['suggestions'] = [
                        'Check if the key exists in the dictionary',
                        'Use dict.get() to handle missing keys safely',
                        'Validate data before accessing',
                    ]
                elif 'IndexError' in exception_type:
                    result['suggestions'] = [
                        'Check the length of the list/array before indexing',
                        'Ensure the index is within bounds',
                    ]
                elif 'TypeError' in exception_type:
                    result['suggestions'] = [
                        'Check the types of variables being used',
                        'Ensure function arguments match expected types',
                    ]
                elif 'Connection' in exception_type or 'OperationalError' in exception_type:
                    result['suggestions'] = [
                        'Check network connectivity',
                        'Verify service is running',
                        'Check connection settings',
                    ]

                break

    # Extract file and line information
    file_matches = re.findall(r'File "([^"]+)", line (\d+)', error_text)
    if file_matches:
        result['locations'] = [{'file': f, 'line': int(l)} for f, l in file_matches]

    return result


def run_analyze_error(args):
    """Analyze error"""
    if args.file:
        error_text = Path(args.file).read_text(encoding='utf-8')
    else:
        error_text = args.error

    result = analyze_error(error_text)

    print("\n🔍 Error Analysis")
    print(f"{'='*60}")
    print(f"Type: {result.get('error_type', 'Unknown')}")
    print(f"Severity: {result.get('severity', 'unknown').upper()}")

    if 'exception_type' in result:
        print(f"Exception: {result['exception_type']}")
    if 'message' in result:
        print(f"Message: {result['message']}")

    print()
    print("Root Cause:")
    print(f"  {result.get('root_cause', 'Unknown')}")

    if result.get('locations'):
        print()
        print("Locations:")
        for loc in result['locations']:
            print(f"  - {loc['file']}:{loc['line']}")

    if result.get('suggestions'):
        print()
        print("Suggested Fixes:")
        for i, suggestion in enumerate(result['suggestions'], 1):
            print(f"  {i}. {suggestion}")


def run_suggest_breakpoints(args):
    """Suggest breakpoints"""
    file_path = Path(args.file)

    if not file_path.exists():
        print(f"❌ File not found: {args.file}")
        return

    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
    except Exception as e:
        print(f"❌ Could not read file: {e}")
        return

    print(f"\n🔍 Breakpoint Suggestions for {args.file}")
    print(f"{'='*60}")

    suggestions = []

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Function definitions
        if stripped.startswith('def ') and not stripped.startswith('def __'):
            func_name = stripped[4:].split('(')[0]
            suggestions.append({
                'line': i,
                'type': 'function',
                'description': f'Entry point: {func_name}()',
                'priority': 'high'
            })

        # Conditional logic
        if stripped.startswith(('if ', 'elif ', 'else:')):
            suggestions.append({
                'line': i,
                'type': 'condition',
                'description': 'Conditional branch',
                'priority': 'medium'
            })

        # External calls (HTTP, DB, etc.)
        external_patterns = ['requests.', 'http', 'open(', 'cursor.', 'execute', 'fetch']
        if any(p in stripped for p in external_patterns):
            suggestions.append({
                'line': i,
                'type': 'external',
                'description': 'External call',
                'priority': 'high'
            })

        # Exception handling
        if stripped.startswith(('try:', 'except', 'finally:')):
            suggestions.append({
                'line': i,
                'type': 'exception',
                'description': 'Error handling',
                'priority': 'medium'
            })

    # Sort by priority
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    suggestions.sort(key=lambda x: priority_order.get(x['priority'], 3))

    current_priority = None
    for sugg in suggestions[:20]:  # Limit output
        if sugg['priority'] != current_priority:
            current_priority = sugg['priority']
            print(f"\n{current_priority.upper()} Priority:")

        print(f"  Line {sugg['line']}: {sugg['description']}")


def run_trace(args):
    """Trace function execution"""
    file_path = Path(args.file)

    if not file_path.exists():
        print(f"❌ File not found: {args.file}")
        return

    try:
        content = file_path.read_text(encoding='utf-8')
        import ast
        tree = ast.parse(content)
    except Exception as e:
        print(f"❌ Could not parse file: {e}")
        return

    print(f"\n🔍 Execution Trace for {args.function}")
    print(f"{'='*60}")

    # Find the target function
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == args.function:
            print(f"\nFunction: {args.function}")
            print(f"Line: {node.lineno}")
            print()

            # Analyze function body
            calls = []
            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Name):
                        calls.append(child.func.id)
                    elif isinstance(child.func, ast.Attribute):
                        calls.append(child.func.attr)

            if calls:
                print("Function calls:")
                for call in set(calls):
                    print(f"  - {call}()")
            else:
                print("No function calls found")

            return

    print(f"❌ Function '{args.function}' not found in {args.file}")


def main():
    parser = argparse.ArgumentParser(
        description='Debugging Assistant',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py analyze-error "Traceback..."
  python3 main.py analyze-error --file error.log
  python3 main.py suggest-breakpoints --file src.py
  python3 main.py trace --file src.py --function foo
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # analyze-error command
    error_parser = subparsers.add_parser('analyze-error', help='Analyze error')
    error_parser.add_argument('error', nargs='?', help='Error text')
    error_parser.add_argument('--file', '-f', help='Error log file')
    error_parser.set_defaults(func=run_analyze_error)

    # suggest-breakpoints command
    bp_parser = subparsers.add_parser('suggest-breakpoints', help='Suggest breakpoints')
    bp_parser.add_argument('--file', required=True, help='Source file')
    bp_parser.add_argument('--function', help='Target function')
    bp_parser.set_defaults(func=run_suggest_breakpoints)

    # trace command
    trace_parser = subparsers.add_parser('trace', help='Trace execution')
    trace_parser.add_argument('--file', required=True, help='Source file')
    trace_parser.add_argument('--function', required=True, help='Function to trace')
    trace_parser.set_defaults(func=run_trace)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == '__main__':
    main()
