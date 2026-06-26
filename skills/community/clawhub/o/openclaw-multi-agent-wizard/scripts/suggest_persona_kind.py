#!/usr/bin/env python3
"""Suggest a starter persona kind from an agent display name.

Usage:
  python scripts/suggest_persona_kind.py 产品助理
  python scripts/suggest_persona_kind.py 研发助理 数据助理 写作助理
"""

from __future__ import annotations

import argparse
import json
import sys


RULES = [
    ("product", ["产品", "需求", "规划", "pm", "product"]),
    ("project", ["项目", "项目经理", "交付", "pmo", "project", "delivery"]),
    ("engineering", ["研发", "技术", "开发", "代码", "工程", "engineer", "dev"]),
    ("data", ["数据", "指标", "分析", "报表", "bi", "data", "metric", "analytics"]),
    ("writing", ["写作", "文案", "润色", "撰稿", "表达", "writing", "copy", "editor"]),
    ("research", ["研究", "调研", "检索", "资料", "research", "search", "investigation"]),
    ("operations", ["运营", "增长", "内容", "活动", "客服", "ops", "operation"]),
    ("life", ["生活", "个人", "家庭", "日常", "提醒", "life"]),
]


def classify(name: str) -> str:
    lower = name.lower()
    for kind, keywords in RULES:
        if any(keyword in lower for keyword in keywords):
            return kind
    return "generic"


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser()
    parser.add_argument("names", nargs="+")
    args = parser.parse_args()

    payload = {
        "agents": [
            {
                "display_name": name,
                "suggested_kind": classify(name),
            }
            for name in args.names
        ]
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
