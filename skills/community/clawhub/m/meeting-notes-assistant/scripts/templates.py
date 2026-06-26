#!/usr/bin/env python3
"""
会议模板管理
支持创建、编辑、列表、删除自定义模板
"""
import argparse
import json
import sys
from pathlib import Path
import os
import shutil

TEMPLATE_DIR = Path.home() / ".workbuddy" / "meeting_notes_templates"
DEFAULT_TEMPLATES = {
    "简洁版": {
        "description": "简单的标题+列表格式", "sections": ["title", "attendees", "todos"]
    },
    "专业版": {
        "description": "带logo、页眉页脚、时间线", "sections": ["title", "meta", "topics", "todos", "keywords"]
    },
    "立项会": {
        "description": "项目立项会议专用", "sections": ["title", "background", "goals", "team", "timeline", "risks"]
    },
    "周会": {
        "description": "周例会专用", "sections": ["title", "last_week", "this_week", "blockers", "todos"]
    },
    "月度复盘": {
        "description": "月度总结复盘", "sections": ["title", "summary", "achievements", "issues", "next_month"]
    },
    "招聘面试": {
        "description": "面试评价专用", "sections": ["title", "candidate_info", "evaluation", "strengths", "weaknesses", "decision"]
    },
    "技术评审": {
        "description": "技术方案评审", "sections": ["title", "background", "options", "decision", "action_items"]
    }
}
def init_templates():
    """初始化模板目录"""
    TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
    for name, config in DEFAULT_TEMPLATES.items():
        save_template(name, config)
def save_template(name: str, config: dict):
    """保存模板"""
    TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
    filepath = TEMPLATE_DIR / f"{name}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
def load_template(name: str) -> dict:
    """加载模板"""
    filepath = TEMPLATE_DIR / f"{name}.json"
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None
def list_templates() -> list:
    """列出所有模板"""
    if not TEMPLATE_DIR.exists():
        init_templates()
    templates = []
    for f in TEMPLATE_DIR.glob("*.json"):
        name = f.stem
        with open(f, "r", encoding="utf-8") as fp:
            config = json.load(fp)
        templates.append({"name": name, "description": config.get("description", ""), "sections": config.get("sections", [])})
    return templates
def delete_template(name: str) -> bool:
    """删除模板"""
    filepath = TEMPLATE_DIR / f"{name}.json"
    if filepath.exists():
        filepath.unlink()
        return True
    return False
def main():
    parser = argparse.ArgumentParser(description="会议模板管理")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    subparsers.add_parser("list", help="列出所有模板")
    create_parser = subparsers.add_parser("create", help="创建模板")
    create_parser.add_argument("name", help="模板名称")
    create_parser.add_argument("--description", "-d", help="模板描述")
    create_parser.add_argument("--sections", "-s", nargs="+", help="模板包含的章节")
    get_parser = subparsers.add_parser("get", help="获取模板详情")
    get_parser.add_argument("name", help="模板名称")
    delete_parser = subparsers.add_parser("delete", help="删除模板")
    delete_parser.add_argument("name", help="模板名称")
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    if args.command == "list":
        templates = list_templates()
        print("Available templates:")
        for t in templates:
            print(f"  - {t['name']}: {t['description']}")
            print(f"    Sections: {', '.join(t['sections'])}")
    elif args.command == "create":
        config = {"description": args.description or "", "sections": args.sections or []}
        save_template(args.name, config)
        print(f"Template '{args.name}' created")
    elif args.command == "get":
        template = load_template(args.name)
        if template:
            print(json.dumps(template, ensure_ascii=False, indent=2))
        else:
            print(f"Template '{args.name}' not found")
    elif args.command == "delete":
        if delete_template(args.name):
            print(f"Template '{args.name}' deleted")
        else:
            print(f"Template '{args.name}' not found")
if __name__ == "__main__":
    main()