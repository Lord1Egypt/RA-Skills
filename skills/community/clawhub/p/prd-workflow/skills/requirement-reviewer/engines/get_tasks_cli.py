#!/usr/bin/env python3
"""
检查任务提取 CLI v1.0

只负责解析章节和匹配检查项，返回任务列表（不执行AI检查）
供 Node.js 调用，Node.js 使用 aiExecutor 执行 AI 检查

使用方式：
    python3 get_tasks_cli.py --prd <prd_file> --format json
"""

import argparse
import json
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from semantic import CHECK_ITEMS, SectionParser, SectionMatcher
from semantic.check_items import Priority


def get_check_tasks(prd_content: str) -> dict:
    """
    提取检查任务

    参数:
        prd_content: PRD 文档内容

    返回:
        任务列表（JSON格式）
    """
    # 输出到 stderr，避免干扰 JSON 输出
    print("\n📋 开始提取检查任务...", file=sys.stderr)

    # 创建匹配器
    matcher = SectionMatcher()

    # 获取检查任务
    doc_tasks, sec_tasks, func_tasks = matcher.match(prd_content)
    all_tasks = doc_tasks + sec_tasks + func_tasks

    print(f"   文档级任务：{len(doc_tasks)}", file=sys.stderr)
    print(f"   章节级任务：{len(sec_tasks)}", file=sys.stderr)
    print(f"   功能点级任务：{len(func_tasks)}", file=sys.stderr)
    print(f"   总计：{len(all_tasks)} 个检查任务", file=sys.stderr)

    # 转换为可序列化格式
    tasks_json = []
    for idx, task in enumerate(all_tasks):
        task_data = {
            "id": f"task-{idx}",
            "check_item": {
                "id": task.check_item.id,
                "name": task.check_item.name,
                "description": task.check_item.description,
                "priority": task.check_item.priority.value,
                "check_points": task.check_item.check_points,
                "example_good": task.check_item.example_good,
                "example_bad": task.check_item.example_bad
            },
            "section": {
                "title": task.section.title if task.section else "全文",
                "level": task.section.level if task.section else 0
            },
            "content": task.content[:3000] if len(task.content) > 3000 else task.content  # 限制长度
        }
        tasks_json.append(task_data)

    return {
        "total_tasks": len(all_tasks),
        "doc_tasks": len(doc_tasks),
        "sec_tasks": len(sec_tasks),
        "func_tasks": len(func_tasks),
        "tasks": tasks_json
    }


def main():
    parser = argparse.ArgumentParser(description="提取检查任务 CLI")
    parser.add_argument("--prd", required=True, help="PRD 文件路径")
    parser.add_argument("--format", choices=["json", "text"], default="json", help="输出格式")

    args = parser.parse_args()

    # 读取 PRD
    with open(args.prd, "r", encoding="utf-8") as f:
        prd_content = f.read()

    # 提取任务
    result = get_check_tasks(prd_content)

    # 输出
    if args.format == "json":
        output = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        lines = []
        lines.append(f"# 检查任务列表")
        lines.append(f"\n## 概览")
        lines.append(f"- 文档级：{result['doc_tasks']}")
        lines.append(f"- 章节级：{result['sec_tasks']}")
        lines.append(f"- 功能点级：{result['func_tasks']}")
        lines.append(f"- 总计：{result['total_tasks']}")

        lines.append(f"\n## 任务详情")
        for task in result["tasks"]:
            lines.append(f"\n### {task['check_item']['name']}")
            lines.append(f"- ID: {task['id']}")
            lines.append(f"- 优先级：{task['check_item']['priority']}")
            lines.append(f"- 章节：{task['section']['title']}")

        output = "\n".join(lines)

    print(output)


if __name__ == "__main__":
    main()