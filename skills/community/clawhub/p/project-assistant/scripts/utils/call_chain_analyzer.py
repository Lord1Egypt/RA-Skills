#!/usr/bin/env python3
"""
调用链分析器
分析函数/方法的调用关系，支持多种编程语言
"""

import os
import sys
import json
import re
import time
from typing import Dict, List, Any, Optional, Set, Tuple
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field

# 导入统一常量
try:
    from constants import EXCLUDE_DIRS
except ImportError:
    EXCLUDE_DIRS = {
        '.git', '.svn', '.hg', '.idea', '.vscode',
        'node_modules', 'dist', 'build', 'out', 'bin', 'obj',
        '__pycache__', '.pytest_cache', '.mypy_cache',
        'target', 'vendor', 'CMakeFiles', '_deps',
        '.gradle', 'Pods', 'DerivedData',
        'venv', '.venv', 'env', '.env',
    }


# 保留关键字，排除这些不作为函数名
KEYWORDS = {
    'if', 'else', 'for', 'while', 'switch', 'try', 'catch', 'class',
    'return', 'import', 'from', 'def', 'function', 'const', 'let',
    'var', 'async', 'await', 'new', 'this', 'super', 'extends',
    'public', 'private', 'protected', 'static', 'final', 'abstract',
    'interface', 'implements', 'extends', 'throws', 'throw', 'try',
    'catch', 'finally', 'synchronized', 'volatile', 'native',
    'sizeof', 'typedef', 'struct', 'enum', 'union', 'goto',
    'continue', 'break', 'case', 'default', 'do', 'extern',
    'register', 'auto', 'const', 'signed', 'unsigned',
    'short', 'long', 'int', 'char', 'float', 'double', 'void',
    'print', 'println', 'printf', 'scanf', 'malloc', 'free',
    'len', 'append', 'make', 'copy', 'delete', 'range', 'go',
    'select', 'defer', 'chan', 'map', 'type', 'package',
    'pub', 'mod', 'use', 'crate', 'self', 'ref', 'mut', 'where',
    'trait', 'impl', 'fn', 'loop', 'match', 'move', 'box',
}


@dataclass
class FunctionInfo:
    """函数信息"""
    name: str
    file: str
    start_line: int
    end_line: int
    language: str
    is_async: bool = False
    params: List[str] = field(default_factory=list)
    docstring: Optional[str] = None


@dataclass
class CallInfo:
    """调用信息"""
    caller: str
    callee: str
    caller_file: str
    line_number: int
    call_type: str = 'direct'  # direct, conditional, async


class CallChainAnalyzer:
    """调用链分析器"""

    # 不同语言的函数定义模式
    FUNCTION_PATTERNS = {
        'python': [
            (r'^(?:async\s+)?def\s+(\w+)\s*\(([^)]*)\):', 'python'),
        ],
        'javascript': [
            (r'^(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)', 'javascript'),
            (r'^(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\(([^)]*)\)\s*=>', 'javascript'),
            (r'^(\w+)\s*:\s*(?:async\s*)?function\s*\(([^)]*)\)', 'javascript'),
        ],
        'typescript': [
            (r'^(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)(?:\s*:\s*[^{]+)?', 'typescript'),
            (r'^(?:export\s+)?(?:const|let)\s+(\w+)\s*=\s*(?:async\s*)?\(([^)]*)\)(?:\s*:\s*[^=]+)?\s*=>', 'typescript'),
            (r'^(?:public|private|protected)?\s*(?:async\s+)?(\w+)\s*\(([^)]*)\)(?:\s*:\s*[^{]+)?\s*\{', 'typescript'),
        ],
        'java': [
            (r'^(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?(?:synchronized\s+)?(?:\w+(?:<[^>]+>)?)\s+(\w+)\s*\(([^)]*)\)', 'java'),
        ],
        'c': [
            (r'^(?:static\s+)?(?:inline\s+)?(?:\w+\s+)+(\w+)\s*\(([^)]*)\)\s*\{', 'c'),
        ],
        'cpp': [
            (r'^(?:(?:\w+\s+)+)?(\w+)\s*\(([^)]*)\)(?:\s*const)?(?:\s*override)?(?:\s*final)?\s*(?::\s*[^{]+)?\s*\{', 'cpp'),
            (r'^(\w+)::(\w+)\s*\(([^)]*)\)', 'cpp'),
        ],
        'go': [
            (r'^func\s+(?:\(([^)]+)\)\s+)?(\w+)\s*\(([^)]*)\)', 'go'),
        ],
        'rust': [
            (r'^(?:pub\s+)?(?:async\s+)?fn\s+(\w+)\s*(?:<[^>]+>)?\s*\(([^)]*)\)', 'rust'),
        ],
    }

    # 导入模式
    IMPORT_PATTERNS = {
        'python': [
            r'from\s+([\w.]+)\s+import\s+(?:\(([^)]+)\)|(.+))',
            r'import\s+([\w.,\s]+)',
        ],
        'javascript': [
            r'import\s+(?:(\{[^}]+\})|(\w+)|(?:\*\s+as\s+(\w+)))\s+from\s+[\'"]([^\'"]+)[\'"]',
            r'require\s*\([\'"]([^\'"]+)[\'"]\)',
        ],
        'typescript': [
            r'import\s+(?:(\{[^}]+\})|(\w+)|(?:\*\s+as\s+(\w+)))\s+from\s+[\'"]([^\'"]+)[\'"]',
        ],
        'java': [
            r'import\s+([\w.]+);',
        ],
        'go': [
            r'import\s+[\'"]([^\'"]+)[\'"]',
            r'import\s+\(\s*((?:[^)]+\s*)+)\)',
        ],
        'rust': [
            r'use\s+([\w:]+)',
        ],
    }

    # 语言对应的文件扩展名
    EXT_MAP = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.mjs': 'javascript',
        '.cjs': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.mts': 'typescript',
        '.java': 'java',
        '.c': 'c',
        '.h': 'c',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        '.hpp': 'cpp',
        '.hxx': 'cpp',
        '.go': 'go',
        '.rs': 'rust',
    }

    def __init__(self, project_dir: str, max_workers: int = 4):
        self.project_dir = os.path.abspath(project_dir)
        self.max_workers = max_workers

        # 存储结构
        self.functions: Dict[str, FunctionInfo] = {}  # {file:name: FunctionInfo}
        self.calls: Dict[str, List[CallInfo]] = defaultdict(list)  # {caller: [CallInfo]}
        self.callers: Dict[str, List[str]] = defaultdict(list)  # {callee: [caller]}
        self.imports: Dict[str, Dict[str, List[str]]] = {}  # {file: {module: [symbols]}}

        # 索引
        self._function_index: Dict[str, List[str]] = defaultdict(list)  # {name: [file:name]}
        self._file_functions: Dict[str, Set[str]] = {}  # {file: {func_names}}

    def detect_language(self, file_path: str) -> Optional[str]:
        """检测文件语言"""
        ext = os.path.splitext(file_path)[1].lower()
        return self.EXT_MAP.get(ext)

    def analyze(self) -> Dict[str, Any]:
        """执行完整分析"""
        start_time = time.time()

        # 收集所有源文件
        source_files = self._collect_source_files()

        # 并行分析文件
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._analyze_file, f): f
                for f in source_files
            }

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    file_path = futures[future]
                    print(f"Warning: Failed to analyze {file_path}: {e}", file=sys.stderr)

        # 构建调用关系
        self._build_call_graph()

        elapsed = time.time() - start_time

        return {
            'summary': {
                'total_functions': len(self.functions),
                'total_files': len(self._file_functions),
                'total_calls': sum(len(c) for c in self.calls.values()),
                'analysis_time': f"{elapsed:.2f}s",
            },
            'functions': {k: self._function_to_dict(v) for k, v in self.functions.items()},
            'call_graph': {
                'calls': {k: [self._call_to_dict(c) for c in v] for k, v in self.calls.items()},
                'callers': dict(self.callers),
            },
        }

    def _collect_source_files(self) -> List[str]:
        """收集所有源代码文件"""
        source_files = []

        for root, dirs, files in os.walk(self.project_dir):
            # 排除特定目录
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in self.EXT_MAP:
                    source_files.append(os.path.join(root, f))

        return source_files

    def _analyze_file(self, file_path: str) -> None:
        """分析单个文件"""
        lang = self.detect_language(file_path)
        if not lang:
            return

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            return

        lines = content.split('\n')
        rel_path = os.path.relpath(file_path, self.project_dir).replace('\\', '/')

        # 提取导入
        self._extract_imports(rel_path, content, lang)

        # 提取函数定义
        functions = self._extract_functions(rel_path, content, lines, lang)

        # 存储函数信息
        self._file_functions[rel_path] = set()
        for func in functions:
            key = f"{rel_path}:{func.name}"
            self.functions[key] = func
            self._function_index[func.name].append(key)
            self._file_functions[rel_path].add(func.name)

    def _extract_imports(self, file_path: str, content: str, lang: str) -> None:
        """提取导入语句"""
        patterns = self.IMPORT_PATTERNS.get(lang, [])
        imports = {}

        for pattern in patterns:
            for match in re.finditer(pattern, content, re.MULTILINE):
                groups = match.groups()
                module = groups[0] if groups else ''
                if module:
                    symbols = []
                    if len(groups) > 1 and groups[1]:
                        # 解构导入 {a, b, c}
                        symbols = [s.strip() for s in groups[1].strip('{}').split(',')]
                    imports[module] = symbols

        self.imports[file_path] = imports

    def _extract_functions(self, file_path: str, content: str, lines: List[str],
                          lang: str) -> List[FunctionInfo]:
        """提取函数定义"""
        functions = []
        patterns = self.FUNCTION_PATTERNS.get(lang, [])

        # 找到所有函数定义位置
        func_matches = []
        for pattern, pattern_lang in patterns:
            for match in re.finditer(pattern, content, re.MULTILINE):
                # 根据模式确定函数名位置
                groups = match.groups()
                if not groups:
                    continue

                # Go 语言特殊处理: func (receiver) name(params)
                if lang == 'go' and len(groups) >= 3:
                    func_name = groups[1]  # 第二个捕获组是函数名
                else:
                    func_name = groups[0]

                if func_name in KEYWORDS:
                    continue

                start_line = content[:match.start()].count('\n') + 1
                func_matches.append((func_name, start_line, match, pattern_lang))

        # 按行号排序
        func_matches.sort(key=lambda x: x[1])

        # 确定每个函数的范围
        for i, (name, start_line, match, func_lang) in enumerate(func_matches):
            # 函数结束位置：下一个函数开始或文件结束
            if i + 1 < len(func_matches):
                end_line = func_matches[i + 1][1] - 1
            else:
                end_line = len(lines)

            # 尝试找到实际结束位置（匹配括号）
            actual_end = self._find_function_end(lines, start_line - 1, lang)
            if actual_end:
                end_line = min(end_line, actual_end)

            # 提取参数
            groups = match.groups()
            params = []
            if len(groups) >= 2 and groups[1]:
                params = self._parse_params(groups[1], lang)

            # 检测是否异步
            match_text = match.group(0)
            is_async = 'async' in match_text

            # 提取 docstring
            docstring = self._extract_docstring(lines, start_line - 1, lang)

            func = FunctionInfo(
                name=name,
                file=file_path,
                start_line=start_line,
                end_line=end_line,
                language=func_lang,
                is_async=is_async,
                params=params,
                docstring=docstring,
            )
            functions.append(func)

        return functions

    def _find_function_end(self, lines: List[str], start_idx: int, lang: str) -> Optional[int]:
        """找到函数的结束行（通过括号匹配）"""
        brace_count = 0
        in_function = False

        for i in range(start_idx, len(lines)):
            line = lines[i]

            # 跳过字符串和注释
            line = self._strip_comments(line, lang)

            for char in line:
                if char == '{':
                    brace_count += 1
                    in_function = True
                elif char == '}':
                    brace_count -= 1
                    if in_function and brace_count == 0:
                        return i + 1  # 返回行号（1-indexed）

        return None

    def _strip_comments(self, line: str, lang: str) -> str:
        """移除行内注释"""
        # 简单实现，移除 // 和 # 后的内容
        if lang in ('c', 'cpp', 'java', 'javascript', 'typescript', 'go', 'rust'):
            if '//' in line:
                line = line[:line.index('//')]
        elif lang == 'python':
            if '#' in line:
                line = line[:line.index('#')]
        return line

    def _parse_params(self, params_str: str, lang: str) -> List[str]:
        """解析函数参数"""
        if not params_str.strip():
            return []

        params = []
        # 简单分割，可能需要更复杂的解析
        for param in params_str.split(','):
            param = param.strip()
            if param:
                # 提取参数名（通常是最后一个词）
                parts = param.split()
                if parts:
                    # 处理带默认值的情况
                    param_name = parts[-1].split('=')[0].strip()
                    # 处理类型注解
                    if ':' in param_name:
                        param_name = param_name.split(':')[0].strip()
                    params.append(param_name)

        return params

    def _extract_docstring(self, lines: List[str], func_idx: int, lang: str) -> Optional[str]:
        """提取函数文档字符串"""
        if func_idx <= 0:
            return None

        prev_line = lines[func_idx - 1].strip()

        # Python docstring
        if lang == 'python' and prev_line.endswith('"""'):
            # 查找开始
            for i in range(func_idx - 2, max(func_idx - 10, -1), -1):
                if '"""' in lines[i]:
                    return '\n'.join(lines[i:func_idx]).strip()

        # JSDoc / JavaDoc / Javadoc style
        if prev_line == '*/':
            for i in range(func_idx - 2, max(func_idx - 20, -1), -1):
                if '/**' in lines[i]:
                    doc = '\n'.join(lines[i:func_idx])
                    # 清理注释符号
                    doc = re.sub(r'/\*\*|\*/|\s*\*\s?', ' ', doc)
                    return doc.strip()

        return None

    def _build_call_graph(self) -> None:
        """构建调用图"""
        for file_path, func_names in self._file_functions.items():
            for func_name in func_names:
                key = f"{file_path}:{func_name}"
                func_info = self.functions[key]

                # 获取函数体
                try:
                    abs_path = os.path.join(self.project_dir, file_path)
                    with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()

                    func_body = ''.join(lines[func_info.start_line - 1:func_info.end_line])
                    self._extract_calls_from_body(key, func_body, file_path, func_names)
                except Exception:
                    pass

    def _extract_calls_from_body(self, caller_key: str, body: str,
                                  file_path: str, local_funcs: Set[str]) -> None:
        """从函数体提取调用"""
        caller_name = self.functions[caller_key].name

        # 通用的函数调用模式
        call_pattern = r'\b(\w+)\s*\('

        for match in re.finditer(call_pattern, body):
            callee = match.group(1)

            # 排除关键字和控制结构
            if callee in KEYWORDS:
                continue

            # 排除自身调用
            if callee == caller_name:
                continue

            # 检查是否是局部函数调用
            if callee in local_funcs:
                line_in_func = body[:match.start()].count('\n')
                call_line = self.functions[caller_key].start_line + line_in_func

                call_info = CallInfo(
                    caller=caller_key,
                    callee=f"{file_path}:{callee}",
                    caller_file=file_path,
                    line_number=call_line,
                )
                self.calls[caller_key].append(call_info)
                self.callers[f"{file_path}:{callee}"].append(caller_key)

    def find_function(self, func_name: str) -> List[Dict[str, Any]]:
        """查找函数定义位置"""
        results = []

        # 精确匹配
        if func_name in self._function_index:
            for key in self._function_index[func_name]:
                if key in self.functions:
                    func = self.functions[key]
                    results.append({
                        'file': func.file,
                        'line': func.start_line,
                        'end_line': func.end_line,
                        'function': func.name,
                        'language': func.language,
                    })

        # 模糊匹配（如果精确匹配没有结果）
        if not results:
            for name in self._function_index:
                if func_name.lower() in name.lower():
                    for key in self._function_index[name]:
                        if key in self.functions:
                            func = self.functions[key]
                            results.append({
                                'file': func.file,
                                'line': func.start_line,
                                'end_line': func.end_line,
                                'function': func.name,
                                'language': func.language,
                            })

        return results

    def get_call_chain(self, func_name: str, depth: int = 3,
                       direction: str = 'both') -> Dict[str, Any]:
        """获取调用链

        Args:
            func_name: 函数名
            depth: 递归深度
            direction: 'calls' (被调) | 'called_by' (调用者) | 'both'
        """
        definitions = self.find_function(func_name)

        if not definitions:
            return {
                'error': f'Function not found: {func_name}',
                'suggestions': self._suggest_similar(func_name),
            }

        result = {
            'function': func_name,
            'definitions': definitions,
            'calls': [],
            'called_by': [],
        }

        for defn in definitions:
            key = f"{defn['file']}:{func_name}"

            if direction in ('calls', 'both'):
                result['calls'].extend(self._get_calls_recursive(key, depth))

            if direction in ('called_by', 'both'):
                result['called_by'].extend(self._get_callers_recursive(key, depth))

        return result

    def _get_calls_recursive(self, caller_key: str, depth: int,
                             visited: Optional[Set[str]] = None) -> List[Dict]:
        """递归获取调用链"""
        if visited is None:
            visited = set()

        if depth <= 0 or caller_key in visited:
            return []

        visited.add(caller_key)
        calls = []

        for call_info in self.calls.get(caller_key, []):
            callee_key = call_info.callee
            call_data = {
                'function': callee_key.split(':')[-1],
                'file': call_info.caller_file,
                'line': call_info.line_number,
                'children': self._get_calls_recursive(callee_key, depth - 1, visited.copy())
            }
            calls.append(call_data)

        return calls

    def _get_callers_recursive(self, callee_key: str, depth: int,
                               visited: Optional[Set[str]] = None) -> List[Dict]:
        """递归获取调用者链"""
        if visited is None:
            visited = set()

        if depth <= 0 or callee_key in visited:
            return []

        visited.add(callee_key)
        callers = []

        for caller_key in self.callers.get(callee_key, []):
            if caller_key in self.functions:
                func = self.functions[caller_key]
                caller_data = {
                    'function': func.name,
                    'file': func.file,
                    'line': func.start_line,
                    'parents': self._get_callers_recursive(caller_key, depth - 1, visited.copy())
                }
                callers.append(caller_data)

        return callers

    def _suggest_similar(self, func_name: str) -> List[str]:
        """建议相似的函数名"""
        suggestions = []
        name_lower = func_name.lower()

        for name in self._function_index.keys():
            if name_lower in name.lower() or name.lower() in name_lower:
                suggestions.append(name)
                if len(suggestions) >= 5:
                    break

        return suggestions

    def get_impact_analysis(self, func_name: str) -> Dict[str, Any]:
        """影响分析：修改某函数会影响哪些代码"""
        definitions = self.find_function(func_name)

        if not definitions:
            return {'error': f'Function not found: {func_name}'}

        all_callers = []
        all_test_callers = []

        for defn in definitions:
            key = f"{defn['file']}:{func_name}"

            # 收集所有调用者
            for caller_key in self.callers.get(key, []):
                if caller_key in self.functions:
                    caller = self.functions[caller_key]
                    caller_info = {
                        'function': caller.name,
                        'file': caller.file,
                        'line': caller.start_line,
                    }

                    # 检查是否是测试文件
                    if self._is_test_file(caller.file):
                        all_test_callers.append(caller_info)
                    else:
                        all_callers.append(caller_info)

        return {
            'function': func_name,
            'definitions': definitions,
            'direct_callers': all_callers,
            'test_callers': all_test_callers,
            'total_impact': len(all_callers) + len(all_test_callers),
        }

    def _is_test_file(self, file_path: str) -> bool:
        """判断是否是测试文件"""
        test_patterns = ['test', 'spec', '_test.', '.test.', '_spec.', '.spec.']
        lower_path = file_path.lower()
        return any(p in lower_path for p in test_patterns)

    def _function_to_dict(self, func: FunctionInfo) -> Dict:
        """转换函数信息为字典"""
        return {
            'name': func.name,
            'file': func.file,
            'start_line': func.start_line,
            'end_line': func.end_line,
            'language': func.language,
            'is_async': func.is_async,
            'params': func.params,
            'docstring': func.docstring,
        }

    def _call_to_dict(self, call: CallInfo) -> Dict:
        """转换调用信息为字典"""
        return {
            'caller': call.caller,
            'callee': call.callee,
            'line': call.line_number,
            'type': call.call_type,
        }


def print_call_chain(chain: Dict, indent: int = 0) -> str:
    """格式化打印调用链"""
    lines = []
    prefix = '  ' * indent

    if 'error' in chain:
        return chain['error']

    func_name = chain.get('function', 'unknown')
    definitions = chain.get('definitions', [])

    if definitions:
        defn = definitions[0]
        lines.append(f"{prefix}{func_name}() [{defn['file']}:{defn['line']}]")
    else:
        lines.append(f"{prefix}{func_name}()")

    for call in chain.get('calls', []):
        lines.append(f"{prefix}  → {print_call_chain(call, indent + 1)}")

    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: call_chain_analyzer.py <project_dir> [function_name] [--depth=N] [--direction=calls|called_by|both]")
        print("\nOptions:")
        print("  --depth=N       Call chain depth (default: 3)")
        print("  --direction=X   Direction: calls, called_by, or both (default: both)")
        print("  --impact        Show impact analysis instead of call chain")
        sys.exit(1)

    project_dir = sys.argv[1]
    func_name = None
    depth = 3
    direction = 'both'
    show_impact = False

    # 解析参数
    for arg in sys.argv[2:]:
        if arg.startswith('--depth='):
            depth = int(arg.split('=')[1])
        elif arg.startswith('--direction='):
            direction = arg.split('=')[1]
        elif arg == '--impact':
            show_impact = True
        elif not arg.startswith('--'):
            func_name = arg

    analyzer = CallChainAnalyzer(project_dir)

    if func_name:
        if show_impact:
            result = analyzer.get_impact_analysis(func_name)
        else:
            analyzer.analyze()
            result = analyzer.get_call_chain(func_name, depth, direction)
    else:
        result = analyzer.analyze()

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()