r"""
write_guard.py — 文件写入守卫钩子

功能：
  1. 扫描指定脚本目录，检测直接使用 `open(... "w" ...)` / `os.remove()` / `os.unlink()` 的调用
  2. 替代方案推荐：safe_write() / safe_delete()
  3. 可作为 workflow_state 的钩子调用，在执行文件写入操作前进行校验

用法:
  python scripts/write_guard.py scan <scripts_dir>    # 扫描违规写入
  python scripts/write_guard.py check <filepath>      # 检查单个文件
"""

import ast
import os
import sys
from pathlib import Path


# ── 禁止操作模式 ──────────────────────────────────────────
FORBIDDEN_PATTERNS = [
    ('open_write', "open(..., 'w', ...)", "应使用 safe_write()"),
    ('open_write_bytes', "open(..., 'wb', ...)", "应使用 safe_write()"),
    ('os_remove', "os.remove()", "应使用 safe_delete()"),
    ('os_unlink', "os.unlink()", "应使用 safe_delete()"),
]


def scan_file(filepath: str) -> list:
    """扫描单个文件，返回违规操作列表"""
    results = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
    except Exception as e:
        return [{"file": filepath, "error": str(e)}]

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return [{"file": filepath, "error": "语法解析失败"}]

    for node in ast.walk(tree):
        # open() 写模式
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "open":
                if node.args and len(node.args) >= 2:
                    mode_arg = node.args[1]
                    if isinstance(mode_arg, ast.Constant) and isinstance(mode_arg.value, str):
                        if mode_arg.value.startswith("w"):
                            lineno = getattr(node, 'lineno', 0)
                            results.append({
                                "file": filepath,
                                "line": lineno,
                                "code": ast.get_source_segment(source, node) or "open()",
                                "violation": "open_write",
                                "message": "直接使用 open(... 'w' ...) 写入文件",
                                "suggestion": "使用 safe_write() 替代",
                            })

            # os.remove / os.unlink
            if isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                    if node.func.attr in ("remove", "unlink"):
                        lineno = getattr(node, 'lineno', 0)
                        results.append({
                            "file": filepath,
                            "line": lineno,
                            "code": ast.get_source_segment(source, node) or f"os.{node.func.attr}()",
                            "violation": f"os_{node.func.attr}",
                            "message": f"直接使用 os.{node.func.attr}() 删除文件",
                            "suggestion": "使用 safe_delete() 替代",
                        })

    return results


def scan_directory(scripts_dir: str) -> list:
    """扫描整个 scripts 目录"""
    all_results = []
    for fname in sorted(os.listdir(scripts_dir)):
        if not fname.endswith(".py"):
            continue
        fpath = os.path.join(scripts_dir, fname)
        if os.path.isfile(fpath):
            results = scan_file(fpath)
            # 排除 safe_write.py 自身（它本来就该调用这些操作）
            if fname == "safe_write.py":
                continue
            all_results.extend(results)
    return all_results


def print_report(results: list):
    """打印扫描报告"""
    if not results:
        print("[write_guard] ✅ 无违规写入操作")
        return

    print(f"[write_guard] ⚠ 发现 {len(results)} 处违规操作:")
    by_file = {}
    for r in results:
        by_file.setdefault(r["file"], []).append(r)

    for fpath, items in sorted(by_file.items()):
        rel = os.path.basename(fpath)
        print(f"\n  {rel}:")
        for item in items:
            print(f"    行 {item['line']:>4d} | {item['violation']:<15s} | {item['message']}")
            print(f"          代码: {item['code'][:60]}")
            print(f"          建议: {item['suggestion']}")


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python scripts/write_guard.py scan <scripts_dir>")
        print("  python scripts/write_guard.py check <filepath>")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "scan":
        if len(sys.argv) < 3:
            print("[write_guard] 缺少 scripts_dir 参数")
            sys.exit(1)
        scripts_dir = sys.argv[2]
        if not os.path.isdir(scripts_dir):
            print(f"[write_guard] 目录不存在: {scripts_dir}")
            sys.exit(1)
        results = scan_directory(scripts_dir)
        print_report(results)
        # 如果有违规，exit code = 1
        if results:
            sys.exit(1)

    elif cmd == "check":
        if len(sys.argv) < 3:
            print("[write_guard] 缺少 filepath 参数")
            sys.exit(1)
        fpath = sys.argv[2]
        if not os.path.isfile(fpath):
            print(f"[write_guard] 文件不存在: {fpath}")
            sys.exit(1)
        results = scan_file(fpath)
        print_report(results)

    else:
        print(f"[write_guard] 未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
