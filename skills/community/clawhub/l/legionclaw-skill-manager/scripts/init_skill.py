#!/usr/bin/env python3
"""
LegionClaw 技能初始化脚本 — 从模板创建技能目录

用法:
    init_skill.py <skill-name> --path <path> [--resources scripts,references,assets]

示例:
    init_skill.py my-new-skill --path skills
    init_skill.py my-api-skill --path skills --resources scripts,references
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MAX_SKILL_NAME_LENGTH = 64
ALLOWED_RESOURCES = {"scripts", "references", "assets"}

SKILL_TEMPLATE = """---
name: {skill_name}
version: 1.0.0
description: "[TODO: 一句话说明技能用途和触发场景，包含触发关键词]"
disable-model-invocation: false
---

# {skill_title}

## 何时使用

- **技能名**：用户点名 `{skill_name}`，或需要**[TODO: 核心功能]**。
- **常见说法**（不限于此）：[TODO: 说法1]、[TODO: 说法2]、[TODO: 说法3]。

## 目标

[TODO: 简明描述技能要完成的核心任务]

## 执行步骤

1. [TODO: 步骤1]
2. [TODO: 步骤2]
3. [TODO: 步骤3]

## 错误处理

- **[TODO: 错误类型]**：[TODO: 处理方式]
"""


def normalize_skill_name(skill_name: str) -> str:
    normalized = skill_name.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    normalized = re.sub(r"-{2,}", "-", normalized)
    return normalized


def title_case_skill_name(skill_name: str) -> str:
    return " ".join(word.capitalize() for word in skill_name.split("-"))


def parse_resources(raw_resources: str) -> list[str]:
    if not raw_resources:
        return []
    resources = [item.strip() for item in raw_resources.split(",") if item.strip()]
    invalid = sorted({item for item in resources if item not in ALLOWED_RESOURCES})
    if invalid:
        allowed = ", ".join(sorted(ALLOWED_RESOURCES))
        print(f"[ERROR] 未知资源类型: {', '.join(invalid)}")
        print(f"   允许的类型: {allowed}")
        sys.exit(1)
    deduped: list[str] = []
    seen: set[str] = set()
    for resource in resources:
        if resource not in seen:
            deduped.append(resource)
            seen.add(resource)
    return deduped


def init_skill(
    skill_name: str,
    path: str,
    resources: list[str],
) -> Path | None:
    skill_dir = Path(path).resolve() / skill_name

    if skill_dir.exists():
        print(f"[ERROR] 技能目录已存在: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"[OK] 创建技能目录: {skill_dir}")
    except OSError as e:
        print(f"[ERROR] 创建目录失败: {e}")
        return None

    skill_title = title_case_skill_name(skill_name)
    skill_md_path = skill_dir / "SKILL.md"
    try:
        skill_md_path.write_text(
            SKILL_TEMPLATE.format(skill_name=skill_name, skill_title=skill_title),
            encoding="utf-8",
        )
        print("[OK] 创建 SKILL.md")
    except OSError as e:
        print(f"[ERROR] 创建 SKILL.md 失败: {e}")
        return None

    for resource in resources:
        resource_dir = skill_dir / resource
        resource_dir.mkdir(exist_ok=True)
        print(f"[OK] 创建 {resource}/")

    print(f"\n[OK] 技能 '{skill_name}' 初始化完成: {skill_dir}")
    print("\n后续步骤:")
    print("1. 编辑 SKILL.md，完成所有 TODO 项")
    if resources:
        print("2. 向 scripts/、references/、assets/ 添加所需资源")
    else:
        print("2. 按需创建 scripts/、references/、assets/ 目录")
    print("3. 运行 validate_skill.py 校验技能结构")

    return skill_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="从模板创建 LegionClaw 技能目录")
    parser.add_argument("skill_name", help="技能名称（自动规范为 kebab-case）")
    parser.add_argument("--path", required=True, help="技能输出目录，如 skills")
    parser.add_argument(
        "--resources",
        default="",
        help="逗号分隔的资源目录: scripts,references,assets",
    )
    args = parser.parse_args()

    raw_skill_name = args.skill_name
    skill_name = normalize_skill_name(raw_skill_name)
    if not skill_name:
        print("[ERROR] 技能名必须包含至少一个字母或数字")
        sys.exit(1)
    if len(skill_name) > MAX_SKILL_NAME_LENGTH:
        print(
            f"[ERROR] 技能名 '{skill_name}' 过长 ({len(skill_name)} 字符)，"
            f"最大 {MAX_SKILL_NAME_LENGTH} 字符"
        )
        sys.exit(1)
    if skill_name != raw_skill_name:
        print(f"提示: 技能名已从 '{raw_skill_name}' 规范为 '{skill_name}'")

    resources = parse_resources(args.resources)

    print(f"初始化技能: {skill_name}")
    print(f"   位置: {args.path}")
    print(f"   资源: {', '.join(resources) if resources else '无（按需创建）'}")
    print()

    result = init_skill(skill_name, args.path, resources)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
