#!/usr/bin/env python3
"""
HTML 文件写入工具

将 AI 生成的 HTML 内容写入文件。本脚本不做任何模板渲染或数据处理，
仅负责安全地将内容落盘。

Usage:
    python write_html.py --content "<html>...</html>" --output report.html
    echo "<html>...</html>" | python write_html.py --output report.html
    python write_html.py --input-file content.html --output report.html
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def validate_html(content):
    """
    做最小化的 HTML 结构验证。
    不保证语义正确性，仅检查基本的文档完整性。
    """
    issues = []
    stripped = content.strip()

    if not stripped:
        issues.append("内容为空")
        return issues

    # 检查是否包含 <html 或 <!DOCTYPE（放宽要求，允许 HTML fragment）
    has_html_tag = re.search(r'<\s*html', stripped, re.IGNORECASE) is not None
    has_doctype = re.search(r'<\s*!doctype', stripped, re.IGNORECASE) is not None

    if not has_html_tag and not has_doctype:
        issues.append("内容缺少 <html> 或 <!DOCTYPE> 标签，可能不是完整 HTML 文档")

    # 检查常见的未闭合标签（简单的计数匹配）
    open_tags = len(re.findall(r'<\s*(script|style|div|table|thead|tbody|tr|td|th|ul|ol|li|p|span|a|h[1-6]|section|article|header|footer|main|nav)\s*[^/]*?>', stripped, re.IGNORECASE))
    close_tags = len(re.findall(r'<\s*/\s*(script|style|div|table|thead|tbody|tr|td|th|ul|ol|li|p|span|a|h[1-6]|section|article|header|footer|main|nav)\s*>', stripped, re.IGNORECASE))
    self_closing = len(re.findall(r'<\s*(br|hr|img|input|meta|link|area|base|col|embed|param|source|track|wbr)\s*[^>]*?/>', stripped, re.IGNORECASE))

    # 放宽检查：只报警告，不阻止写入
    if open_tags > close_tags + self_closing:
        issues.append(f"可能存在未闭合标签（开: {open_tags}, 闭: {close_tags}）")

    return issues


def validate_path(output_path):
    """验证输出路径是否合法且可写。"""
    path = Path(output_path)

    # 禁止写入系统关键目录（简化检查）
    dangerous_prefixes = ['/etc', '/sys', '/proc', '/dev', 'C:\\Windows', 'C:\\Program Files']
    abs_path = str(path.resolve()).lower()
    for prefix in dangerous_prefixes:
        if abs_path.startswith(prefix.lower()):
            return False, f"禁止写入系统目录: {prefix}"

    # 确保父目录存在或可创建
    parent = path.parent
    try:
        parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        return False, f"无法创建目录 {parent}: {e}"

    # 检查是否可写
    try:
        if path.exists() and not path.is_file():
            return False, f"路径已存在且不是文件: {output_path}"
        # 测试写入权限
        if path.exists():
            if not os.access(path, os.W_OK):
                return False, f"文件不可写: {output_path}"
        else:
            if not os.access(parent, os.W_OK):
                return False, f"目录不可写: {parent}"
    except OSError as e:
        return False, f"权限检查失败: {e}"

    return True, ""


def write_html(content, output_path, validate=True):
    """
    将 HTML 内容写入文件。

    Args:
        content: HTML 字符串
        output_path: 输出文件路径
        validate: 是否执行 HTML 结构验证

    Returns:
        dict: {"success": bool, "file": str, "message": str, "warnings": [str]}
    """
    # 路径验证
    path_ok, path_err = validate_path(output_path)
    if not path_ok:
        return {
            "success": False,
            "file": None,
            "message": path_err,
            "warnings": []
        }

    # HTML 验证（仅警告，不阻止）
    warnings = []
    if validate:
        warnings = validate_html(content)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        file_size = Path(output_path).stat().st_size

        return {
            "success": True,
            "file": str(Path(output_path).resolve()),
            "size": file_size,
            "message": f"成功写入 HTML 文件: {output_path} ({file_size} bytes)",
            "warnings": warnings
        }
    except Exception as e:
        return {
            "success": False,
            "file": None,
            "message": f"写入失败: {e}",
            "warnings": warnings
        }


def main():
    parser = argparse.ArgumentParser(description="HTML 文件写入工具")
    parser.add_argument("--output", "-o", required=True, help="输出 HTML 文件路径")
    parser.add_argument("--content", "-c", default=None, help="HTML 内容字符串（与 --input-file / stdin 互斥）")
    parser.add_argument("--input-file", "-i", default=None, help="从文件读取 HTML 内容")
    parser.add_argument("--no-validate", action="store_true", help="跳过 HTML 结构验证")
    parser.add_argument("--encoding", default="utf-8", help="输入文件编码（默认 utf-8）")

    args = parser.parse_args()

    # 确定内容来源优先级: --content > --input-file > stdin
    content = None
    source_desc = ""

    if args.content is not None:
        content = args.content
        source_desc = "命令行参数"
    elif args.input_file is not None:
        try:
            with open(args.input_file, "r", encoding=args.encoding) as f:
                content = f.read()
            source_desc = f"文件: {args.input_file}"
        except Exception as e:
            print(json.dumps({
                "success": False,
                "message": f"读取输入文件失败: {e}"
            }, ensure_ascii=False, indent=2))
            sys.exit(1)
    else:
        # 从 stdin 读取
        content = sys.stdin.read()
        source_desc = "标准输入"

    if content is None or content.strip() == "":
        print(json.dumps({
            "success": False,
            "message": "HTML 内容为空，请通过 --content、--input-file 或管道提供内容"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    result = write_html(content, args.output, validate=not args.no_validate)
    result["source"] = source_desc

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
