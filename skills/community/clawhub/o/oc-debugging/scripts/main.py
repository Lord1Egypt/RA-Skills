#!/usr/bin/env python3
"""
Debugging Assistant - Main Entry Point
Supports Python and C/C++ debugging
"""

import argparse
import re
import sys
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


def analyze_error(error_text: str) -> dict:
    """Analyze error text and provide insights - supports Python and C"""
    
    # First check if it's a C error
    if is_c_error(error_text):
        return analyze_c_error(error_text)
    
    return analyze_python_error(error_text)


def is_c_error(error_text: str) -> bool:
    """Check if error text is from a C/C++ program"""
    c_indicators = [
        'Segmentation fault',
        'SIGSEGV',
        'SIGABRT',
        'core dumped',
        '==ERROR:',
        'AddressSanitizer',
        'MemorySanitizer',
        'gcc:',
        'clang:',
        'undefined reference',
        'multiple definition',
        'implicit declaration',
    ]
    error_upper = error_text.upper()
    for indicator in c_indicators:
        if indicator.upper() in error_upper:
            return True
    return False


def analyze_c_error(error_text: str) -> dict:
    """Analyze C/C++ errors"""
    result = {
        'error_type': 'C/C++ Error',
        'severity': 'error',
        'root_cause': '',
        'suggestions': [],
    }
    
    lines = error_text.split('\n')
    first_line = lines[0] if lines else ''
    
    # Segmentation fault
    if 'Segmentation fault' in error_text or 'SIGSEGV' in error_text:
        result['error_type'] = 'Segmentation Fault (SIGSEGV)'
        result['severity'] = 'critical'
        result['root_cause'] = 'Memory access violation - accessing invalid/unmapped memory'
        result['suggestions'] = [
            'Check for NULL pointer dereferences',
            'Verify array bounds are not exceeded',
            'Check for use-after-free bugs',
            'Use valgrind: valgrind --leak-check=full ./program',
            'Run with gdb: gdb ./program, then run, then bt (backtrace)',
            'Check stack trace if core dump available',
        ]
        result['gdb_commands'] = [
            'gdb ./program',
            'run',
            'bt  # backtrace',
            'info locals',
            'info registers',
        ]
    
    # Buffer overflow (AddressSanitizer)
    elif 'AddressSanitizer' in error_text:
        result['error_type'] = 'AddressSanitizer Error'
        if 'buffer-overflow' in error_text:
            result['root_cause'] = 'Buffer overflow detected'
            result['suggestions'] = [
                'Check array/buffer bounds',
                'Use safer alternatives (strncpy instead of strcpy)',
                'Check loop bounds carefully',
            ]
        elif 'heap-buffer-overflow' in error_text:
            result['root_cause'] = 'Heap buffer overflow detected'
            result['suggestions'] = [
                'Check malloc/realloc sizes',
                'Verify array indexing on heap buffers',
                'Use valgrind for detailed analysis',
            ]
        elif 'stack-buffer-overflow' in error_text:
            result['root_cause'] = 'Stack buffer overflow detected'
            result['suggestions'] = [
                'Reduce stack buffer sizes',
                'Use heap allocation for large buffers',
                'Check sprintf/strcpy buffer sizes',
            ]
        elif 'use-after-free' in error_text:
            result['root_cause'] = 'Use after free detected'
            result['suggestions'] = [
                'Set pointers to NULL after free',
                'Check for double-free bugs',
                'Review object lifetime management',
            ]
        elif 'heap-use-after-free' in error_text:
            result['root_cause'] = 'Use after free (heap) detected'
            result['suggestions'] = [
                'Check free() locations vs usage',
                'Use smart pointers if using C++',
                'Review ownership semantics',
            ]
        else:
            result['root_cause'] = 'Memory error detected by AddressSanitizer'
            result['suggestions'] = [
                'Read AddressSanitizer output carefully',
                'Check the stack trace provided',
                'Run with ASAN_OPTIONS=detect_stack_use_after_return=1',
            ]
    
    # Memory leak
    elif 'MemorySanitizer' in error_text or 'LeakSanitizer' in error_text:
        result['error_type'] = 'Memory Leak'
        result['severity'] = 'warning'
        result['root_cause'] = 'Allocated memory not freed'
        result['suggestions'] = [
            'Ensure every malloc/calloc has a corresponding free',
            'Check error paths for missed frees',
            'Use valgrind --leak-check=full for details',
            'Consider using automatic memory management',
        ]
    
    # Assertion failure
    elif 'Assertion' in error_text and 'failed' in error_text:
        result['error_type'] = 'Assertion Failed'
        result['root_cause'] = 'assert() condition evaluated to false'
        result['suggestions'] = [
            'Check the assertion condition',
            'Verify preconditions are met',
            'Add more descriptive assertion messages',
        ]
    
    # Compiler errors
    elif 'undefined reference' in error_text:
        result['error_type'] = 'Linker Error'
        result['root_cause'] = 'Function/variable defined but not linked'
        result['suggestions'] = [
            'Check if all source files are compiled',
            'Verify library is linked with -l flag',
            'Check for missing function definitions',
            'Ensure header prototypes match implementations',
        ]
    
    elif 'implicit declaration' in error_text:
        result['error_type'] = 'Implicit Declaration'
        result['root_cause'] = 'Function used without declaration'
        result['suggestions'] = [
            'Add #include for the function header',
            'Declare the function before use',
            'Check for typos in function name',
        ]
    
    # Bus error
    elif 'Bus error' in error_text or 'SIGBUS' in error_text:
        result['error_type'] = 'Bus Error (SIGBUS)'
        result['severity'] = 'critical'
        result['root_cause'] = 'Unaligned memory access or non-existent physical address'
        result['suggestions'] = [
            'Check for misaligned pointer access',
            'Verify memory mapped files',
            'Check pointer arithmetic',
        ]
    
    # Core dumped
    elif 'core dumped' in error_text.lower():
        result['error_type'] = 'Core Dump'
        result['severity'] = 'critical'
        result['root_cause'] = 'Program crashed and generated core dump'
        result['suggestions'] = [
            'Load core dump: gdb ./program core',
            'Or: gdb ./program core.pid',
            'Use bt command to see backtrace',
            'Check ulimit -c to enable core dumps',
        ]
        result['gdb_commands'] = [
            'gdb ./program core',
            'bt full',
            'info locals',
            'info registers',
        ]
    
    else:
        result['root_cause'] = 'Unknown C/C++ error'
        result['suggestions'] = [
            'Check compiler/linker output carefully',
            'Look for file:line number references',
            'Use -g flag for debug symbols',
        ]
    
    # Extract file and line information
    # Pattern: file.c:123 or file.c:123:45
    file_matches = re.findall(r'([\w\-\./]+\.(?:c|cpp|h|hpp)):(\d+)(?::\d+)?', error_text)
    if file_matches:
        result['locations'] = [{'file': f, 'line': int(l)} for f, l in file_matches]
    
    return result


def analyze_python_error(error_text: str) -> dict:
    """Analyze Python errors"""
    result = {
        'error_type': 'Unknown',
        'severity': 'info',
        'root_cause': '',
        'suggestions': [],
    }

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

    if result.get('gdb_commands'):
        print()
        print("GDB Commands:")
        for cmd in result['gdb_commands']:
            print(f"  {cmd}")


def run_suggest_breakpoints(args):
    """Suggest breakpoints for Python or C"""
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

    # Determine file type and use appropriate analyzer
    if file_path.suffix in ['.c', '.h']:
        suggestions = _suggest_c_breakpoints(lines, args.function)
    else:
        suggestions = _suggest_python_breakpoints(lines, args.function)

    # Sort by priority
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    suggestions.sort(key=lambda x: priority_order.get(x['priority'], 3))

    current_priority = None
    for sugg in suggestions[:20]:  # Limit output
        if sugg['priority'] != current_priority:
            current_priority = sugg['priority']
            print(f"\n{current_priority.upper()} Priority:")

        print(f"  Line {sugg['line']}: {sugg['description']}")


def _suggest_python_breakpoints(lines: list, function_name: str = None) -> list:
    """Suggest breakpoints for Python code"""
    suggestions = []

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Function definitions
        if stripped.startswith('def ') and not stripped.startswith('def __'):
            func_name = stripped[4:].split('(')[0]
            if not function_name or func_name == function_name:
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

    return suggestions


def _suggest_c_breakpoints(lines: list, function_name: str = None) -> list:
    """Suggest breakpoints for C code"""
    suggestions = []
    import re

    for i, line in enumerate(lines, 1):
        code = line.split('//')[0]  # Remove comments
        stripped = code.strip()

        # Function definitions
        func_match = re.match(r'(\w+)\s+(\w+)\s*\([^)]*\)\s*\{?', stripped)
        if func_match and func_match.group(1) not in ['if', 'for', 'while', 'switch', 'return']:
            func_name = func_match.group(2)
            if not function_name or func_name == function_name:
                suggestions.append({
                    'line': i,
                    'type': 'function',
                    'description': f'Entry point: {func_name}()',
                    'priority': 'high'
                })

        # Memory allocation
        alloc_patterns = ['malloc(', 'calloc(', 'realloc(', 'strdup(']
        for pattern in alloc_patterns:
            if pattern in code:
                suggestions.append({
                    'line': i,
                    'type': 'memory',
                    'description': f'Memory allocation: {pattern}',
                    'priority': 'high'
                })

        # Pointer dereferences
        if re.search(r'\*\w+\s*=', code) or re.search(r'->\w+', code):
            suggestions.append({
                'line': i,
                'type': 'pointer',
                'description': 'Pointer dereference',
                'priority': 'high'
            })

        # Dangerous functions
        dangerous = ['strcpy(', 'strcat(', 'sprintf(', 'gets(', 'scanf(']
        for d in dangerous:
            if d in code:
                suggestions.append({
                    'line': i,
                    'type': 'dangerous',
                    'description': f'Dangerous function: {d}',
                    'priority': 'medium'
                })

        # Conditional logic
        if re.match(r'\s*(if|else if|else|switch|case)\s*[\(\{]', stripped):
            suggestions.append({
                'line': i,
                'type': 'condition',
                'description': 'Conditional branch',
                'priority': 'medium'
            })

        # Loops
        if re.match(r'\s*(for|while)\s*\(', stripped):
            suggestions.append({
                'line': i,
                'type': 'loop',
                'description': 'Loop entry',
                'priority': 'medium'
            })

        # Return statements
        if stripped.startswith('return'):
            suggestions.append({
                'line': i,
                'type': 'return',
                'description': 'Function return',
                'priority': 'low'
            })

    return suggestions


def run_trace(args):
    """Trace function execution - supports Python and C"""
    file_path = Path(args.file)

    if not file_path.exists():
        print(f"❌ File not found: {args.file}")
        return

    print(f"\n🔍 Execution Trace for {args.function}")
    print(f"{'='*60}")

    # Dispatch based on file type
    if file_path.suffix in ['.c', '.h']:
        _trace_c_function(file_path, args.function)
    else:
        _trace_python_function(file_path, args.function)


def _trace_python_function(file_path: Path, function_name: str):
    """Trace Python function execution"""
    try:
        content = file_path.read_text(encoding='utf-8')
        import ast
        tree = ast.parse(content)
    except Exception as e:
        print(f"❌ Could not parse file: {e}")
        return

    # Find the target function
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            print(f"\nFunction: {function_name}")
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

    print(f"❌ Function '{function_name}' not found in {file_path}")


def _trace_c_function(file_path: Path, function_name: str):
    """Trace C function execution using c_parser"""
    if not C_SUPPORT_AVAILABLE:
        print("❌ C tracing requires c-support library")
        print("   Install: pip install tree-sitter tree-sitter-c pycparser")
        return

    try:
        parser = CParser()
        info = parser.parse_file(str(file_path))
    except Exception as e:
        print(f"❌ Could not parse file: {e}")
        return

    # Find the target function
    target_func = None
    for func in info.functions:
        if func.name == function_name:
            target_func = func
            break

    if not target_func:
        print(f"❌ Function '{function_name}' not found in {file_path}")
        return

    print(f"\nFunction: {function_name}")
    print(f"Return type: {target_func.return_type}")
    print(f"Line: {target_func.line}")
    print()

    if target_func.parameters:
        print("Parameters:")
        for param in target_func.parameters:
            print(f"  - {param.get('declaration', 'unknown')}")
        print()

    # Extract function calls from body
    try:
        content = file_path.read_text(encoding='utf-8')
        func_bodies = parser.extract_function_bodies(str(file_path))
        if function_name in func_bodies:
            body = func_bodies[function_name]
            import re
            # Find function calls
            calls = re.findall(r'\b(\w+)\s*\(', body)
            # Filter out keywords
            calls = [c for c in calls if c not in ['if', 'for', 'while', 'switch', 'sizeof', 'return']]
            if calls:
                print("Function calls:")
                for call in set(calls):
                    print(f"  - {call}()")
            else:
                print("No function calls found")
    except Exception:
        pass

    print()
    print("GDB commands to trace:")
    print(f"  gdb {file_path.parent / file_path.stem}")
    print(f"  break {function_name}")
    print(f"  run")
    print(f"  step      # Step into functions")
    print(f"  next      # Step over functions")
    print(f"  finish    # Run until function returns")


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
