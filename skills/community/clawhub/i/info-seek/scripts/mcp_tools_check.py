#!/usr/bin/env python3
"""mcp_tools_check.py — G11 拆分模块变更一致性守护（A2 · v1.0.1）

对 scripts/mcp_tools_*.py 做 AST 符号自检：
  1. 模块内引用但未导入/未定义的符号（排除 builtins / 函数局部赋值 / 参数）
  2. 常见遗漏：sys / Path / INFOSEEK_ROOT 等公共符号
  3. 工具函数名与门面绑定一致性（门面 import 的工具函数在模块中存在）

用法：
  python scripts/mcp_tools_check.py            # 全检
  python scripts/mcp_tools_check.py --quiet    # 仅失败输出

退出码：0 全通过；1 存在缺失符号。
（A2 守护：本次 G11 拆分曾因 mcp_tools_async/analysis/keys 缺 import sys 导致
  research_v3 stdio 调用 NameError → QCM 全链路 partial，本脚本防复发。）
"""
import ast
import builtins
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent
ROOT = SCRIPTS.parent

COMMON_SYMBOLS = {
    'INFOSEEK_ROOT', 'ensure_dirs', 'ARCHIVES_DIR', 'INFOSEEK_DIR',
    'DB_PATH', 'LOG_PATH', 'AUTH_TOKEN', 'mask_token', 'WORKSPACE',
    'SERVER_VERSION', 'TOOL_CALL_COUNTER', 'AUDIT_LOG_PATH', 'CORE_DIR',
    'SKILL_VERSION',  # v1.8.1 版本单源真源（对外唯一版本）
}
BUILTINS = set(dir(builtins)) | {'__file__', '__name__', '__doc__', '__package__'}


def imported_names(tree: ast.AST) -> set:
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                names.add(a.asname or a.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            for a in node.names:
                names.add(a.asname or a.name)
    return names


def assigned_names(tree: ast.AST) -> set:
    defined = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    defined.add(t.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            defined.add(node.target.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defined.add(node.name)
        elif isinstance(node, (ast.For, ast.AsyncFor)):
            target = node.target
            if isinstance(target, ast.Name):
                defined.add(target.id)
            elif isinstance(target, (ast.Tuple, ast.List)):
                for e in target.elts:
                    if isinstance(e, ast.Name):
                        defined.add(e.id)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            defined.add(node.name)
        elif isinstance(node, ast.With):
            for wi in node.items:
                if wi.optional_vars and isinstance(wi.optional_vars, ast.Name):
                    defined.add(wi.optional_vars.id)
        elif isinstance(node, ast.comprehension):
            target = node.target
            if isinstance(target, ast.Name):
                defined.add(target.id)
            elif isinstance(target, (ast.Tuple, ast.List)):
                for e in target.elts:
                    if isinstance(e, ast.Name):
                        defined.add(e.id)
    return defined


def func_params(tree: ast.AST) -> set:
    params = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for a in node.args.args:
                params.add(a.arg)
            if node.args.vararg:
                params.add(node.args.vararg.arg)
            for a in node.args.kwonlyargs:
                params.add(a.arg)
            if node.args.kwarg:
                params.add(node.args.kwarg.arg)
        elif isinstance(node, ast.Lambda):
            for a in node.args.args:
                params.add(a.arg)
    return params


def check_module(path: Path) -> list:
    """返回缺失符号列表 [(name, line), ...]"""
    src = path.read_text(encoding='utf-8')
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return [(f"SyntaxError: {e}", 0)]
    defined = imported_names(tree) | assigned_names(tree) | func_params(tree) | BUILTINS
    missing = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id not in defined:
            missing.append((node.id, node.lineno))
    return missing


def main() -> int:
    quiet = '--quiet' in sys.argv
    modules = sorted(SCRIPTS.glob('mcp_tools_*.py'))
    all_missing = {}
    for path in modules:
        missing = check_module(path)
        if missing:
            all_missing[path.name] = missing
            print(f"[FAIL] {path.name}:")
            for name, line in missing:
                print(f"    L{line}: 引用未定义符号 '{name}'"
                      + ("（公共符号，检查是否缺 import）" if name in COMMON_SYMBOLS else ""))
        elif not quiet:
            print(f"[OK]   {path.name}")

    # 门面绑定一致性：门面 import 的 mcp_tools 符号须存在
    try:
        sys.path.insert(0, str(SCRIPTS))
        import infoseek_mcp_server as m  # noqa: F401
        print("[OK]   门面可导入（绑定一致性）")
    except Exception as e:
        print(f"[FAIL] 门面导入失败: {type(e).__name__}: {e}")
        all_missing.setdefault('infoseek_mcp_server.py', []).append((str(e)[:80], 0))

    if all_missing:
        print(f"\n=== 符号自检: FAIL（{len(all_missing)} 模块存在问题）===")
        return 1
    print("\n=== 符号自检: ALL OK（{} 模块）===".format(len(modules) + 1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
