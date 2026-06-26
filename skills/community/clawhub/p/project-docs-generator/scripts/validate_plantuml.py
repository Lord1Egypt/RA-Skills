#!/usr/bin/env python3
"""
PlantUML 语法验证工具

用法:
    python validate_plantuml.py <markdown-file-or-directory>
    python validate_plantuml.py ./docs --verbose
    python validate_plantuml.py ./README.md --max-elements 25

功能:
    1. 提取 Markdown 文件中的 PlantUML 代码块
    2. 验证语法正确性
    3. 检查图表复杂度（元素数量）
    4. 生成拆分建议
"""

import os
import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Config:
    """配置参数"""

    max_elements: int = 25
    max_lines: int = 60
    check_syntax: bool = True
    verbose: bool = False


@dataclass
class SyntaxError:
    """语法错误"""

    message: str
    line: int = -1


@dataclass
class Metrics:
    """图表指标"""

    nodes: int = 0
    arrows: int = 0
    actions: int = 0
    notes: int = 0
    participants: int = 0
    total: int = 0
    lines: int = 0


@dataclass
class SplitSuggestion:
    """拆分建议"""

    type: str
    strategy: str
    example: str = ""


@dataclass
class BlockResult:
    """代码块验证结果"""

    name: str
    metrics: Metrics
    syntax_errors: List[SyntaxError] = field(default_factory=list)
    suggestions: List[SplitSuggestion] = field(default_factory=list)
    status: str = "passed"


@dataclass
class FileResult:
    """文件验证结果"""

    file: str
    blocks: List[BlockResult] = field(default_factory=list)
    total: int = 0
    passed: int = 0
    warnings: int = 0
    errors: int = 0


# 常见语法错误模式
SYNTAX_PATTERNS = [
    # note right of 在组件图中需要别名
    (
        r"note\s+right\s+of\s+\[[^\]]+\]",
        "note right of [Component] 无效，请使用 as 别名",
    ),
    # -x-> 箭头不支持
    (r"-x->", "-x-> 箭头语法不支持，请使用 ..>"),
    # 外部 include
    (r"!include\s+<[^>]+>", "!include 外部引用可能导致问题"),
    # 颜色语法在 package 上
    (r'package\s+"[^"]+"\s+#[A-Za-z]+', "package 上使用 #Color 可能不支持"),
]


def count_elements(plantuml: str) -> Metrics:
    """统计图表元素"""
    metrics = Metrics()
    metrics.lines = len(plantuml.split("\n"))

    # 节点统计
    metrics.nodes = len(re.findall(r"^\s*\[[^\]]+\]", plantuml, re.MULTILINE))
    metrics.nodes += len(re.findall(r"^\s*component\s+", plantuml, re.MULTILINE))
    metrics.nodes += len(re.findall(r"^\s*package\s+", plantuml, re.MULTILINE))
    metrics.nodes += len(re.findall(r"^\s*database\s+", plantuml, re.MULTILINE))
    metrics.nodes += len(re.findall(r"^\s*queue\s+", plantuml, re.MULTILINE))
    metrics.nodes += len(re.findall(r"^\s*entity\s+", plantuml, re.MULTILINE))
    metrics.nodes += len(re.findall(r"^\s*actor\s+", plantuml, re.MULTILINE))

    # 箭头统计
    metrics.arrows = len(re.findall(r"-->|<--|->|<-|\.\.>|<\.\.", plantuml))

    # 动作统计（活动图）
    metrics.actions = len(re.findall(r"^\s*:[^;]+;", plantuml, re.MULTILINE))

    # 注释统计
    metrics.notes = len(re.findall(r"note\s+(right|left|top|bottom)", plantuml))

    # 参与者统计
    metrics.participants = len(
        re.findall(r"^\s*participant\s+", plantuml, re.MULTILINE)
    )

    # 总计
    metrics.total = (
        metrics.nodes
        + metrics.arrows
        + metrics.actions
        + metrics.notes
        + metrics.participants
    )

    return metrics


def find_line_number(text: str, pattern: str, flags: int = 0) -> int:
    """查找匹配行号"""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if re.search(pattern, line, flags):
            return i + 1
    return -1


def check_syntax(plantuml: str) -> List[SyntaxError]:
    """检查语法问题"""
    errors = []

    for item in SYNTAX_PATTERNS:
        if len(item) == 3:
            pattern, message, flags = item
        else:
            pattern, message = item
            flags = 0

        if re.search(pattern, plantuml, flags):
            line = find_line_number(plantuml, pattern, flags)
            errors.append(SyntaxError(message=message, line=line))

    # 检查 @startuml/@enduml 配对
    start_count = len(re.findall(r"@startuml", plantuml))
    end_count = len(re.findall(r"@enduml", plantuml))
    if start_count != end_count:
        errors.append(
            SyntaxError(
                message=f"@startuml/@enduml 配对不匹配: {start_count} vs {end_count}"
            )
        )

    return errors


def extract_plantuml(content: str) -> List[Dict[str, Any]]:
    """提取 PlantUML 块"""
    blocks = []
    # 匹配 ```plantuml ... @startuml name ... @enduml ... ```
    pattern = r"```plantuml\n(@startuml\s+(\w+).*?@enduml)\n```"

    for match in re.finditer(pattern, content, re.DOTALL):
        blocks.append(
            {
                "full": match.group(0),
                "code": match.group(1),
                "name": match.group(2) or "unnamed",
                "start_index": match.start(),
            }
        )

    return blocks


def generate_split_suggestions(
    block: Dict[str, Any], config: Config
) -> List[SplitSuggestion]:
    """生成拆分建议"""
    suggestions = []
    metrics = count_elements(block["code"])

    if metrics.total <= config.max_elements:
        return suggestions

    code = block["code"]

    # 分析图表类型
    has_sequence = "participant" in code or "actor" in code
    has_component = "[" in code or "package" in code
    has_activity = ":" in code and ";" in code

    if has_sequence:
        suggestions.append(
            SplitSuggestion(
                type="sequence",
                strategy="按阶段拆分",
                example="""
// 原图：完整流程
// 拆分后：
// - 阶段一：连接建立
// - 阶段二：消息处理
// - 阶段三：响应返回
""",
            )
        )

    if has_component:
        suggestions.append(
            SplitSuggestion(
                type="component",
                strategy="按层级/模块拆分",
                example="""
// 原图：整体架构（87 元素）
// 拆分后：
// - 概览图（~20 元素）：展示主要层次
// - 前端层详图（~15 元素）
// - 后端层详图（~15 元素）
// - 数据层详图（~15 元素）
""",
            )
        )

    if has_activity:
        suggestions.append(
            SplitSuggestion(
                type="activity",
                strategy="按阶段/泳道拆分",
                example="""
// 原图：完整流程
// 拆分后：
// - 阶段一：初始化
// - 阶段二：核心处理
// - 阶段三：清理/完成
""",
            )
        )

    return suggestions


def validate_file(file_path: str, config: Config) -> FileResult:
    """验证单个文件"""
    result = FileResult(file=file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = extract_plantuml(content)
    result.total = len(blocks)

    for block in blocks:
        metrics = count_elements(block["code"])
        syntax_errors = check_syntax(block["code"]) if config.check_syntax else []
        suggestions = generate_split_suggestions(block, config)

        block_result = BlockResult(
            name=block["name"],
            metrics=metrics,
            syntax_errors=syntax_errors,
            suggestions=suggestions,
            status="passed",
        )

        # 判断状态
        if len(syntax_errors) > 0:
            block_result.status = "error"
            result.errors += 1
        elif metrics.total > config.max_elements or metrics.lines > config.max_lines:
            block_result.status = "warning"
            result.warnings += 1
        else:
            result.passed += 1

        result.blocks.append(block_result)

    return result


def format_output(result: FileResult, config: Config) -> str:
    """格式化输出"""
    lines = []
    lines.append(f"\n📄 {result.file}")
    lines.append("─" * 50)

    for block in result.blocks:
        if block.status == "passed":
            icon = "✅"
        elif block.status == "warning":
            icon = "⚠️"
        else:
            icon = "❌"

        lines.append(f"\n{icon} {block.name}")
        lines.append(f"   元素: {block.metrics.total} | 行数: {block.metrics.lines}")

        if config.verbose:
            lines.append(
                f"   节点: {block.metrics.nodes} | 箭头: {block.metrics.arrows} | 动作: {block.metrics.actions}"
            )

        if block.syntax_errors:
            lines.append("   语法错误:")
            for err in block.syntax_errors:
                line_info = f" (行 {err.line})" if err.line > 0 else ""
                lines.append(f"   - {err.message}{line_info}")

        if block.suggestions:
            lines.append("   拆分建议:")
            for sug in block.suggestions:
                lines.append(f"   - [{sug.type}] {sug.strategy}")

    lines.append("\n" + "─" * 50)
    lines.append(
        f"总计: {result.total} | ✅ 通过: {result.passed} | ⚠️ 警告: {result.warnings} | ❌ 错误: {result.errors}"
    )

    return "\n".join(lines)


def process_path(input_path: str, config: Config) -> List[FileResult]:
    """递归处理目录"""
    results = []
    path = Path(input_path)

    if path.is_dir():
        for md_file in path.rglob("*.md"):
            results.append(validate_file(str(md_file), config))
    elif path.is_file() and input_path.endswith(".md"):
        results.append(validate_file(input_path, config))

    return results


def main():
    parser = argparse.ArgumentParser(
        description="PlantUML 语法验证工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python validate_plantuml.py ./docs
    python validate_plantuml.py README.md --verbose
    python validate_plantuml.py ./docs --max-elements 30
""",
    )
    parser.add_argument("path", help="要验证的文件或目录路径")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    parser.add_argument(
        "--max-elements", type=int, default=25, help="单个图表最大元素数（默认 25）"
    )
    parser.add_argument(
        "--max-lines", type=int, default=60, help="单个图表最大行数（默认 60）"
    )
    parser.add_argument("--no-syntax", action="store_true", help="跳过语法检查")

    args = parser.parse_args()

    config = Config(
        max_elements=args.max_elements,
        max_lines=args.max_lines,
        check_syntax=not args.no_syntax,
        verbose=args.verbose,
    )

    # 执行验证
    results = process_path(args.path, config)

    # 输出结果
    total_errors = 0
    total_warnings = 0

    for result in results:
        print(format_output(result, config))
        total_errors += result.errors
        total_warnings += result.warnings

    # 总结
    print("\n" + "═" * 50)
    print(f"验证完成！共 {len(results)} 个文件")
    print(f"❌ 错误: {total_errors} | ⚠️ 警告: {total_warnings}")

    # 退出码
    sys.exit(1 if total_errors > 0 else 0)


if __name__ == "__main__":
    main()
