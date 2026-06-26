#!/usr/bin/env python3
"""
Documentation Generator - API Documentation Generator

Generates API documentation from Python and C code.
"""

import ast
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

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


class APIDocGenerator:
    """Generates API documentation from Python and C source code"""

    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        self.c_parser = CParser() if C_SUPPORT_AVAILABLE else None

    def generate(self, source_dir: str, format: str = 'markdown') -> str:
        """Generate API documentation"""
        source_path = self.root / source_dir

        if not source_path.exists():
            return f"# Error: Source directory '{source_dir}' not found"

        docs = []
        docs.append(f"# API Documentation")
        docs.append("")
        docs.append(f"*Generated from `{source_dir}`*")
        docs.append("")

        # Find all Python files
        py_files = list(source_path.rglob('*.py'))
        for filepath in sorted(py_files):
            if filepath.name.startswith('_'):
                continue
            module_docs = self._process_file(filepath, source_path)
            if module_docs:
                docs.append(module_docs)

        # Find all C files
        c_files = list(source_path.rglob('*.c')) + list(source_path.rglob('*.h'))
        if c_files:
            docs.append("## C/C++ API")
            docs.append("")
            for filepath in sorted(c_files):
                if filepath.name.startswith('_'):
                    continue
                c_docs = self._process_c_file(filepath, source_path)
                if c_docs:
                    docs.append(c_docs)

        return "\n".join(docs)

    def _process_c_file(self, filepath: Path, source_path: Path) -> Optional[str]:
        """Process a C/C++ file"""
        if not self.c_parser:
            return None

        try:
            info = self.c_parser.parse_file(str(filepath))
        except Exception:
            return None

        rel_path = filepath.relative_to(source_path)
        lines = []
        lines.append(f"### File: `{rel_path}`")
        lines.append("")

        has_content = False

        # Document functions
        for func in info.functions:
            has_content = True
            lines.append(f"#### `{func.return_type} {func.name}()`")
            lines.append("")

            # Parameters
            if func.parameters:
                lines.append("**Parameters:**")
                for param in func.parameters:
                    decl = param.get('declaration', 'unknown')
                    lines.append(f"- `{decl}`")
                lines.append("")

            lines.append(f"**Returns:** `{func.return_type}`")
            lines.append("")

            lines.append(f"*Defined at line {func.line}*")
            lines.append("")

        # Document types (structs, enums, unions)
        for type_def in info.types:
            has_content = True
            lines.append(f"#### `{type_def.kind} {type_def.name}`")
            lines.append("")
            if type_def.fields:
                lines.append("**Fields:**")
                for field in type_def.fields:
                    lines.append(f"- `{field}`")
                lines.append("")
            lines.append(f"*Defined at line {type_def.line}*")
            lines.append("")

        # Document macros
        for macro in info.macros:
            has_content = True
            lines.append(f"#### `#define {macro.name}`")
            if macro.value:
                lines.append(f"Value: `{macro.value}`")
            lines.append(f"*Defined at line {macro.line}*")
            lines.append("")

        if not has_content:
            return None

        return "\n".join(lines)

    def _process_file(self, filepath: Path, source_path: Path) -> Optional[str]:
        """Process a single Python file"""
        try:
            content = filepath.read_text(encoding='utf-8')
            tree = ast.parse(content)
        except Exception:
            return None

        # Get module name
        rel_path = filepath.relative_to(source_path)
        module_name = str(rel_path.with_suffix('')).replace('/', '.').replace('\\', '.')

        lines = []
        lines.append(f"## Module: `{module_name}`")
        lines.append("")

        has_content = False

        # Process classes
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_doc = self._process_class(node, filepath)
                if class_doc:
                    lines.append(class_doc)
                    has_content = True

        # Process functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Skip private functions and methods (handled with classes)
                if node.name.startswith('_'):
                    continue

                # Check if it's a method (has self/cls as first arg)
                if node.args.args and node.args.args[0].arg in ('self', 'cls'):
                    continue

                func_doc = self._process_function(node, filepath)
                if func_doc:
                    lines.append(func_doc)
                    has_content = True

        if not has_content:
            return None

        return "\n".join(lines)

    def _process_class(self, node: ast.ClassDef, filepath: Path) -> Optional[str]:
        """Process a class definition"""
        lines = []
        lines.append(f"### Class: `{node.name}`")
        lines.append("")

        # Get docstring
        docstring = ast.get_docstring(node)
        if docstring:
            lines.append(docstring)
            lines.append("")

        # Process methods
        methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
        for method in methods:
            if method.name.startswith('_'):
                continue

            method_doc = self._process_function(method, filepath, is_method=True)
            if method_doc:
                lines.append(method_doc)

        return "\n".join(lines)

    def _process_function(self, node: ast.FunctionDef, filepath: Path,
                         is_method: bool = False) -> Optional[str]:
        """Process a function definition"""
        lines = []

        prefix = "####" if is_method else "###"
        lines.append(f"{prefix} `{node.name}`")
        lines.append("")

        # Generate signature
        signature = self._generate_signature(node)
        lines.append(f"```python")
        lines.append(f"{signature}")
        lines.append(f"```")
        lines.append("")

        # Get docstring
        docstring = ast.get_docstring(node)
        if docstring:
            # Parse docstring sections
            parsed = self._parse_docstring(docstring)

            if parsed['description']:
                lines.append(parsed['description'])
                lines.append("")

            if parsed['args']:
                lines.append("**Args:**")
                for arg_name, arg_desc in parsed['args'].items():
                    lines.append(f"- `{arg_name}`: {arg_desc}")
                lines.append("")

            if parsed['returns']:
                lines.append(f"**Returns:** {parsed['returns']}")
                lines.append("")

            if parsed['raises']:
                lines.append(f"**Raises:** {parsed['raises']}")
                lines.append("")

            if parsed['example']:
                lines.append(f"**Example:**")
                lines.append(f"```python")
                lines.append(parsed['example'])
                lines.append(f"```")
                lines.append("")

        return "\n".join(lines)

    def _generate_signature(self, node: ast.FunctionDef) -> str:
        """Generate function signature"""
        args = []

        # Regular arguments
        for i, arg in enumerate(node.args.args):
            arg_str = arg.arg

            # Add type annotation
            if arg.annotation:
                if isinstance(arg.annotation, ast.Name):
                    arg_str += f": {arg.annotation.id}"
                elif isinstance(arg.annotation, ast.Constant):
                    arg_str += f": {arg.annotation.value}"
                elif isinstance(arg.annotation, ast.Subscript):
                    arg_str += f": {self._format_subscript(arg.annotation)}"

            # Add default value
            defaults_start = len(node.args.args) - len(node.args.defaults)
            if i >= defaults_start:
                default = node.args.defaults[i - defaults_start]
                arg_str += f" = {self._format_default(default)}"

            args.append(arg_str)

        # *args
        if node.args.vararg:
            args.append(f"*{node.args.vararg.arg}")

        # **kwargs
        if node.args.kwarg:
            args.append(f"**{node.args.kwarg.arg}")

        # Return type
        return_type = ""
        if node.returns:
            if isinstance(node.returns, ast.Name):
                return_type = f" -> {node.returns.id}"
            elif isinstance(node.returns, ast.Constant):
                return_type = f" -> {node.returns.value}"

        return f"def {node.name}({', '.join(args)}){return_type}"

    def _format_subscript(self, node: ast.Subscript) -> str:
        """Format subscript type (e.g., List[str])"""
        if isinstance(node.value, ast.Name):
            base = node.value.id
            if isinstance(node.slice, ast.Name):
                return f"{base}[{node.slice.id}]"
            elif isinstance(node.slice, ast.Constant):
                return f"{base}[{node.slice.value}]"
        return str(node)

    def _format_default(self, node: ast.expr) -> str:
        """Format default value"""
        if isinstance(node, ast.Constant):
            return repr(node.value)
        elif isinstance(node, ast.NameConstant):
            return repr(node.value)
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.List):
            return "[]"
        elif isinstance(node, ast.Dict):
            return "{}"
        return "..."

    def _parse_docstring(self, docstring: str) -> Dict[str, Any]:
        """Parse docstring into sections"""
        result = {
            'description': '',
            'args': {},
            'returns': '',
            'raises': '',
            'example': ''
        }

        lines = docstring.split('\n')

        # First paragraph is description
        description_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped in ('Args:', 'Arguments:', 'Returns:', 'Raises:', 'Example:', 'Examples:'):
                break
            description_lines.append(line)

        result['description'] = '\n'.join(description_lines).strip()

        # Parse sections
        current_section = None
        section_content = []

        for line in lines[len(description_lines):]:
            stripped = line.strip()

            if stripped in ('Args:', 'Arguments:'):
                current_section = 'args'
                section_content = []
            elif stripped == 'Returns:':
                if current_section == 'args' and section_content:
                    result['args'] = self._parse_args(section_content)
                current_section = 'returns'
                section_content = []
            elif stripped in ('Raises:', 'Exceptions:'):
                if current_section == 'args' and section_content:
                    result['args'] = self._parse_args(section_content)
                current_section = 'raises'
                section_content = []
            elif stripped in ('Example:', 'Examples:'):
                if current_section == 'args' and section_content:
                    result['args'] = self._parse_args(section_content)
                current_section = 'example'
                section_content = []
            else:
                section_content.append(line)

        # Process final section
        if current_section == 'args' and section_content:
            result['args'] = self._parse_args(section_content)
        elif current_section == 'returns':
            result['returns'] = '\n'.join(section_content).strip()
        elif current_section == 'raises':
            result['raises'] = '\n'.join(section_content).strip()
        elif current_section == 'example':
            result['example'] = '\n'.join(section_content).strip()

        return result

    def _parse_args(self, lines: List[str]) -> Dict[str, str]:
        """Parse Args section"""
        args = {}
        current_arg = None
        current_desc = []

        for line in lines:
            stripped = line.strip()

            # Check for new argument (starts with name or - name)
            match = re.match(r'^[-\s]*(\w+)[\s:]*(.*)', stripped)
            if match and not line.startswith(' ' * 8):  # Not indented too much
                if current_arg:
                    args[current_arg] = ' '.join(current_desc).strip()
                current_arg = match.group(1)
                current_desc = [match.group(2)] if match.group(2) else []
            elif current_arg and stripped:
                current_desc.append(stripped)

        if current_arg:
            args[current_arg] = ' '.join(current_desc).strip()

        return args


def main():
    import argparse

    parser = argparse.ArgumentParser(description='API Documentation Generator')
    parser.add_argument('--source', '-s', required=True, help='Source directory')
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--root', '-r', default='.', help='Project root')
    parser.add_argument('--format', '-f', default='markdown', choices=['markdown', 'html'])

    args = parser.parse_args()

    generator = APIDocGenerator(args.root)
    docs = generator.generate(args.source, args.format)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(docs, encoding='utf-8')
        print(f"✅ API documentation written to: {args.output}")
    else:
        print(docs)


if __name__ == '__main__':
    main()
