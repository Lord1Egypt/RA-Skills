#!/usr/bin/env python3
"""结构化记忆模板：会议纪要/项目决策/学习笔记等"""

import argparse
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.filelock import safe_write

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"

TEMPLATES = {
    "meeting": {
        "name": "会议纪要",
        "format": """# {date} 会议纪要

## 基本信息
- **日期：** {date}
- **参与者：** {participants}
- **会议类型：** {meeting_type}

## 议题
{topics}

## 讨论内容
{content}

## 决议
{decisions}

## 待办事项
{todos}

## 下次会议
- **时间：** {next_date}
- **议题：** {next_topics}
""",
        "fields": ["participants", "meeting_type", "topics", "content", "decisions", "todos", "next_date", "next_topics"],
    },
    "decision": {
        "name": "项目决策",
        "format": """# {date} 决策记录

## 决策主题
{title}

## 背景
{background}

## 方案对比
{options}

## 最终决策
**选择：** {choice}
**原因：** {reason}

## 影响范围
{impact}

## 风险评估
{risks}

## 关联人
{stakeholders}
""",
        "fields": ["title", "background", "options", "choice", "reason", "impact", "risks", "stakeholders"],
    },
    "learning": {
        "name": "学习笔记",
        "format": """# {date} 学习笔记

## 主题
{topic}

## 来源
{source}

## 核心要点
{key_points}

## 详细笔记
{notes}

## 个人思考
{thoughts}

## 后续计划
{next_steps}

## 关联知识
{related}
""",
        "fields": ["topic", "source", "key_points", "notes", "thoughts", "next_steps", "related"],
    },
    "project": {
        "name": "项目里程碑",
        "format": """# {date} 项目进展

## 项目名称
{project_name}

## 当前阶段
{stage}

## 本期完成
{completed}

## 进行中
{in_progress}

## 遇到的问题
{issues}

## 下一阶段目标
{next_goals}

## 资源需求
{resources}
""",
        "fields": ["project_name", "stage", "completed", "in_progress", "issues", "next_goals", "resources"],
    },
    "review": {
        "name": "周报/复盘",
        "format": """# {date} {review_type}

## 本周/期概览
{overview}

## 完成事项
{achievements}

## 未完成事项
{incomplete}

## 经验教训
{lessons}

## 下周/期计划
{plan}

## 需要支持
{support_needed}
""",
        "fields": ["review_type", "overview", "achievements", "incomplete", "lessons", "plan", "support_needed"],
    },
}


def create_from_template(template_name: str, date_str: str | None = None,
                         values: dict | None = None, output: Path | None = None) -> str:
    """使用模板创建记忆"""
    if template_name not in TEMPLATES:
        available = ", ".join(f"'{k}' ({v['name']})" for k, v in TEMPLATES.items())
        raise ValueError(f"未知模板: {template_name}\n可用模板: {available}")

    template = TEMPLATES[template_name]
    date = date_str or datetime.now().strftime("%Y-%m-%d")
    values = values or {}

    # 填充模板
    content = template["format"].format(date=date, **values)

    # 如果指定了输出路径，写入文件
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        safe_write(output, content)
        return str(output)

    return content


def list_templates():
    """列出所有可用模板"""
    print("=" * 60)
    print("📝 可用模板")
    print("=" * 60)
    for key, tmpl in TEMPLATES.items():
        fields = ", ".join(f"`{f}`" for f in tmpl["fields"][:5])
        if len(tmpl["fields"]) > 5:
            fields += f" 等{len(tmpl['fields'])}个字段"
        print(f"\n  📋 {key} — {tmpl['name']}")
        print(f"     字段: {fields}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="结构化记忆模板")
    sub = p.add_subparsers(dest="command")

    # 创建
    create = sub.add_parser("create", help="从模板创建")
    create.add_argument("template", help="模板名称")
    create.add_argument("--date", "-d", default=None)
    create.add_argument("--output", "-o", default=None, help="输出文件路径")
    create.add_argument("--json-values", default=None, help="JSON 格式的字段值")
    create.add_argument("--field", "-f", action="append", nargs=2, metavar=("KEY", "VALUE"),
                        help="字段值（可多次使用）")

    # 列出
    sub.add_parser("list", help="列出模板")

    args = p.parse_args()

    if args.command == "list":
        list_templates()

    elif args.command == "create":
        values = {}
        if args.json_values:
            import json
            values = json.loads(args.json_values)
        if args.field:
            for key, value in args.field:
                values[key] = value

        output = Path(args.output) if args.output else None
        md = DEFAULT_MEMORY_DIR

        if output is None:
            # 默认输出到 conversations 目录
            date = args.date or datetime.now().strftime("%Y-%m-%d")
            output = md / "conversations" / f"{date}.md"

        result = create_from_template(args.template, args.date, values, output)
        print(f"✅ 已生成: {result}")

    else:
        list_templates()
