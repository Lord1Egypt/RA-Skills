#!/usr/bin/env python3
"""
validate_mermaid.py - Mermaid 图表语法验证工具

用法:
    python3 validate_mermaid.py <markdown_file>

功能:
    从 Markdown 文件中提取所有 ```mermaid 代码块，并对每个代码块进行基础语法检查。
    检查项包括：
    1. 图表类型声明是否合法
    2. 括号和引号是否匹配
    3. 代码块是否为空
"""

import sys
import re
from pathlib import Path


VALID_DIAGRAM_TYPES = [
    "graph", "flowchart", "sequenceDiagram", "classDiagram",
    "stateDiagram", "stateDiagram-v2", "erDiagram", "journey",
    "gantt", "pie", "quadrantChart", "requirementDiagram",
    "gitGraph", "mindmap", "timeline", "sankey-beta",
    "xychart-beta", "block-beta",
]


def extract_mermaid_blocks(content: str) -> list[tuple[int, str]]:
    """从 Markdown 内容中提取所有 mermaid 代码块及其起始行号。"""
    blocks = []
    pattern = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
    for match in pattern.finditer(content):
        line_num = content[:match.start()].count("\n") + 1
        blocks.append((line_num, match.group(1).strip()))
    return blocks


def validate_block(line_num: int, block: str) -> list[str]:
    """对单个 Mermaid 代码块执行基础语法检查。"""
    errors = []

    if not block:
        errors.append(f"  行 {line_num}: 代码块为空。")
        return errors

    first_line = block.split("\n")[0].strip()
    diagram_type = first_line.split(" ")[0].split("(")[0]

    if diagram_type not in VALID_DIAGRAM_TYPES:
        errors.append(
            f"  行 {line_num}: 未知的图表类型 '{diagram_type}'。"
            f" 合法类型包括: {', '.join(VALID_DIAGRAM_TYPES[:5])}..."
        )

    # erDiagram 和 classDiagram 使用 {} 定义实体/类，不需要配对检查
    SKIP_BRACKET_TYPES = {"erDiagram", "classDiagram"}
    if diagram_type not in SKIP_BRACKET_TYPES:
        bracket_pairs = {"(": ")", "[": "]", "{": "}"}
        stack = []
        for i, char in enumerate(block):
            if char in bracket_pairs:
                stack.append((char, i))
            elif char in bracket_pairs.values():
                if not stack:
                    errors.append(f"  行 {line_num}: 存在多余的右括号 '{char}'。")
                else:
                    open_char, _ = stack.pop()
                    if bracket_pairs[open_char] != char:
                        errors.append(
                            f"  行 {line_num}: 括号不匹配，期望 '{bracket_pairs[open_char]}' 但得到 '{char}'。"
                        )
        if stack:
            for open_char, pos in stack:
                errors.append(
                    f"  行 {line_num}: 存在未关闭的左括号 '{open_char}'。"
                )

    for quote_char in ['"', "'"]:
        count = block.count(quote_char)
        if count % 2 != 0:
            errors.append(f"  行 {line_num}: 引号 '{quote_char}' 数量不匹配（共 {count} 个）。")

    return errors


def main():
    if len(sys.argv) != 2:
        print("用法: python3 validate_mermaid.py <markdown_file>")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"错误: 文件不存在 - {filepath}")
        sys.exit(1)

    try:
        content = filepath.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            content = filepath.read_text(encoding="gbk")
            print(f"⚠️  检测到非 UTF-8 编码，已使用 GBK 编码读取。\n")
        except Exception as e:
            print(f"错误: 无法读取文件 - {e}")
            sys.exit(1)
    blocks = extract_mermaid_blocks(content)

    if not blocks:
        print(f"✅ 在 '{filepath.name}' 中未发现 Mermaid 代码块。")
        sys.exit(0)

    print(f"在 '{filepath.name}' 中发现 {len(blocks)} 个 Mermaid 代码块。")
    if len(blocks) > 5:
        print(f"正在验证，请稍候...\n")
    else:
        print()

    total_errors = 0
    for i, (line_num, block) in enumerate(blocks, 1):
        if len(blocks) > 5 and i % 5 == 0:
            print(f"  [进度] 已处理 {i}/{len(blocks)} 个代码块...")
        errors = validate_block(line_num, block)
        if errors:
            print(f"❌ 代码块 #{i} (起始行 {line_num}):")
            for err in errors:
                print(err)
            total_errors += len(errors)
        else:
            print(f"✅ 代码块 #{i} (起始行 {line_num}): 基础语法检查通过。")

    if len(blocks) > 5:
        print()
    print(f"\n--- 检查完成 ---")
    if total_errors > 0:
        print(f"共发现 {total_errors} 个问题。")
        sys.exit(1)
    else:
        print(f"✅ 所有 {len(blocks)} 个代码块均通过检查。")
        sys.exit(0)


if __name__ == "__main__":
    main()
