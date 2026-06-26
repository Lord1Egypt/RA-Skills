#!/usr/bin/env python3
"""
内容检查 CLI v1.0

⚠️ DEPRECATED - 此文件已废弃
============================
新架构不再使用此文件。

新架构流程：
1. get_tasks_cli.py 提取检查任务（纯逻辑）
2. review_module.js 使用 aiExecutor 调用 AI（OpenClaw架构）

此文件保留作为备份参考。

原使用方式：
    python3 content_check_cli.py --prd <prd_file> [--output <output_file>]
    python3 content_check_cli.py --prd <prd_file> --format json
"""

import argparse
import json
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from semantic import CHECK_ITEMS, SectionParser, SectionMatcher, AIContentChecker
from semantic.check_items import Priority
from semantic.ai_checker import ContentIssue


def run_content_check(prd_content: str, api_config: dict = None) -> dict:
    """
    执行内容检查

    参数:
        prd_content: PRD 文档内容
        api_config: API 配置（可选）

    返回:
        检查结果字典
    """
    # 输出到 stderr，避免干扰 JSON 输出
    import sys
    print("\n🔍 开始内容检查...", file=sys.stderr)

    # 创建匹配器
    matcher = SectionMatcher()

    # 获取检查任务
    doc_tasks, sec_tasks, func_tasks = matcher.match(prd_content)
    all_tasks = doc_tasks + sec_tasks + func_tasks

    print(f"   文档级任务：{len(doc_tasks)}", file=sys.stderr)
    print(f"   章节级任务：{len(sec_tasks)}", file=sys.stderr)
    print(f"   功能点级任务：{len(func_tasks)}", file=sys.stderr)
    print(f"   总计：{len(all_tasks)} 个检查任务", file=sys.stderr)

    # 创建检查器
    checker = AIContentChecker(api_config)

    # 执行检查
    issues = checker.check_all(all_tasks)

    # 按优先级分组
    core_issues = [i for i in issues if i.priority == Priority.CORE]
    improve_issues = [i for i in issues if i.priority == Priority.IMPROVE]
    optimize_issues = [i for i in issues if i.priority == Priority.OPTIMIZE]

    print(f"\n📊 检查结果：", file=sys.stderr)
    print(f"   核心问题：{len(core_issues)}", file=sys.stderr)
    print(f"   完善问题：{len(improve_issues)}", file=sys.stderr)
    print(f"   优化问题：{len(optimize_issues)}", file=sys.stderr)

    # 转换为可序列化格式
    result = {
        "total_issues": len(issues),
        "core_issues": len(core_issues),
        "improve_issues": len(improve_issues),
        "optimize_issues": len(optimize_issues),
        "issues": [
            {
                "id": f"{issue.check_item.id}-{idx}",
                "check_item_id": issue.check_item.id,
                "check_item_name": issue.check_item.name,
                "priority": issue.priority.value,
                "section_title": issue.section_title,
                "description": issue.issue_description,
                "suggestion": issue.suggestion,
                "original_text": issue.original_text
            }
            for idx, issue in enumerate(issues)
        ],
        "grouped_issues": {
            "core": [
                {
                    "id": f"{issue.check_item.id}-{idx}",
                    "check_item_name": issue.check_item.name,
                    "section_title": issue.section_title,
                    "description": issue.issue_description,
                    "suggestion": issue.suggestion,
                    "original_text": issue.original_text
                }
                for idx, issue in enumerate(core_issues)
            ],
            "improve": [
                {
                    "id": f"{issue.check_item.id}-{idx}",
                    "check_item_name": issue.check_item.name,
                    "section_title": issue.section_title,
                    "description": issue.issue_description,
                    "suggestion": issue.suggestion,
                    "original_text": issue.original_text
                }
                for idx, issue in enumerate(improve_issues)
            ],
            "optimize": [
                {
                    "id": f"{issue.check_item.id}-{idx}",
                    "check_item_name": issue.check_item.name,
                    "section_title": issue.section_title,
                    "description": issue.issue_description,
                    "suggestion": issue.suggestion,
                    "original_text": issue.original_text
                }
                for idx, issue in enumerate(optimize_issues)
            ]
        }
    }

    return result


def main():
    parser = argparse.ArgumentParser(description="PRD 内容检查 CLI")
    parser.add_argument("--prd", required=True, help="PRD 文件路径")
    parser.add_argument("--output", help="输出文件路径")
    parser.add_argument("--format", choices=["json", "text"], default="json", help="输出格式")
    parser.add_argument("--api-key", help="API 密钥")
    parser.add_argument("--api-base", help="API Base URL")

    args = parser.parse_args()

    # 读取 PRD
    with open(args.prd, "r", encoding="utf-8") as f:
        prd_content = f.read()

    # API 配置
    api_config = None
    if args.api_key:
        api_config = {
            "api_key": args.api_key,
            "base_url": args.api_base or "https://api.openai.com/v1"
        }

    # 执行检查
    result = run_content_check(prd_content, api_config)

    # 输出
    if args.format == "json":
        output = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        lines = []
        lines.append(f"# 内容检查报告")
        lines.append(f"\n## 概览")
        lines.append(f"- 核心问题：{result['core_issues']}")
        lines.append(f"- 完善问题：{result['improve_issues']}")
        lines.append(f"- 优化问题：{result['optimize_issues']}")

        for group_name, group_label in [("core", "核心问题"), ("improve", "完善问题"), ("optimize", "优化问题")]:
            group_issues = result["grouped_issues"][group_name]
            if group_issues:
                lines.append(f"\n## {group_label}")
                for issue in group_issues:
                    lines.append(f"\n### {issue['check_item_name']}")
                    lines.append(f"- 章节：{issue['section_title']}")
                    lines.append(f"- 问题：{issue['description']}")
                    lines.append(f"- 建议：{issue['suggestion']}")

        output = "\n".join(lines)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\n✅ 结果已保存到：{args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()