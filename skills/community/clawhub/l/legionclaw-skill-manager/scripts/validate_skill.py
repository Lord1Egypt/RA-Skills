#!/usr/bin/env python3
"""
LegionClaw 技能校验脚本 — 检查 SKILL.md 格式与目录结构

用法:
    validate_skill.py <skill_directory>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Optional

try:
    import yaml
except ModuleNotFoundError:
    yaml = None

MAX_SKILL_NAME_LENGTH = 64
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+(-[\w.]+)?(\+[\w.]+)?$")
REQUIRED_SECTIONS = ("何时使用", "目标", "执行步骤", "错误处理")


def _extract_frontmatter(content: str) -> Optional[str]:
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i])
    return None


def _parse_simple_frontmatter(frontmatter_text: str) -> Optional[dict[str, str]]:
    parsed: dict[str, str] = {}
    current_key: Optional[str] = None
    for raw_line in frontmatter_text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        is_indented = raw_line[:1].isspace()
        if is_indented:
            if current_key is None:
                return None
            current_value = parsed[current_key]
            parsed[current_key] = (
                f"{current_value}\n{stripped}" if current_value else stripped
            )
            continue
        if ":" not in stripped:
            return None
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            return None
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        parsed[key] = value
        current_key = key
    return parsed


def _validate_name(name: str) -> Optional[str]:
    if not isinstance(name, str):
        return f"name 必须是字符串，实际为 {type(name).__name__}"
    name = name.strip()
    if not name:
        return "name 不能为空"
    if not re.match(r"^[a-z][a-z0-9-]*$", name):
        return f"name '{name}' 必须为 kebab-case 且以字母开头"
    if name.endswith("-") or "--" in name:
        return f"name '{name}' 不能以连字符结尾或包含连续连字符"
    if len(name) > MAX_SKILL_NAME_LENGTH:
        return f"name 过长 ({len(name)} 字符)，最大 {MAX_SKILL_NAME_LENGTH} 字符"
    return None


def _validate_version(version: str) -> Optional[str]:
    if not isinstance(version, str):
        return f"version 必须是字符串，实际为 {type(version).__name__}"
    version = version.strip()
    if not version:
        return "version 不能为空"
    if not SEMVER_PATTERN.match(version):
        return f"version '{version}' 不符合语义化版本格式 (如 1.0.0)"
    return None


def _validate_description(description: str) -> Optional[str]:
    if not isinstance(description, str):
        return f"description 必须是字符串，实际为 {type(description).__name__}"
    description = description.strip()
    if not description:
        return "description 不能为空"
    if description.startswith("[TODO"):
        return "description 仍为 TODO 占位符，请完成编写"
    if len(description) > 1024:
        return f"description 过长 ({len(description)} 字符)，最大 1024 字符"
    return None


def validate_skill(skill_path: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []

    if not skill_path.is_dir():
        return False, [f"目录不存在: {skill_path}"]

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, ["缺少 SKILL.md"]

    try:
        content = skill_md.read_text(encoding="utf-8")
    except OSError as e:
        return False, [f"无法读取 SKILL.md: {e}"]

    frontmatter_text = _extract_frontmatter(content)
    if frontmatter_text is None:
        errors.append("frontmatter 格式无效（需以 --- 包裹的 YAML）")
        frontmatter: dict = {}
    elif yaml is not None:
        try:
            loaded = yaml.safe_load(frontmatter_text)
            if not isinstance(loaded, dict):
                errors.append("frontmatter 必须是 YAML 字典")
                frontmatter = {}
            else:
                frontmatter = loaded
        except yaml.YAMLError as e:
            errors.append(f"frontmatter YAML 解析失败: {e}")
            frontmatter = {}
    else:
        parsed = _parse_simple_frontmatter(frontmatter_text)
        if parsed is None:
            errors.append("frontmatter YAML 解析失败（未安装 PyYAML 时仅支持简单格式）")
            frontmatter = {}
        else:
            frontmatter = parsed

    if "name" not in frontmatter:
        errors.append("frontmatter 缺少 name 字段")
    else:
        name_err = _validate_name(frontmatter["name"])
        if name_err:
            errors.append(name_err)
        elif frontmatter["name"].strip() != skill_path.name:
            errors.append(
                f"name '{frontmatter['name']}' 与目录名 '{skill_path.name}' 不一致"
            )

    if "version" not in frontmatter:
        errors.append("frontmatter 缺少 version 字段")
    else:
        version_err = _validate_version(frontmatter["version"])
        if version_err:
            errors.append(version_err)

    if "description" not in frontmatter:
        errors.append("frontmatter 缺少 description 字段")
    else:
        desc_err = _validate_description(frontmatter["description"])
        if desc_err:
            errors.append(desc_err)

    if "disable-model-invocation" in frontmatter:
        val = frontmatter["disable-model-invocation"]
        if not isinstance(val, bool):
            errors.append("disable-model-invocation 必须为布尔值 true/false")

    body = content
    if frontmatter_text is not None:
        body = content.split("---", 2)[-1] if content.count("---") >= 2 else content

    for section in REQUIRED_SECTIONS:
        if f"## {section}" not in body:
            errors.append(f"缺少必需章节: ## {section}")

    if "[TODO" in body:
        errors.append("SKILL.md 正文仍包含 TODO 占位符，请完成编写")

    return len(errors) == 0, errors


def main() -> None:
    if len(sys.argv) != 2:
        print("用法: python validate_skill.py <skill_directory>")
        sys.exit(1)

    skill_path = Path(sys.argv[1]).resolve()
    valid, messages = validate_skill(skill_path)

    if valid:
        print(f"[OK] 技能 '{skill_path.name}' 校验通过")
        sys.exit(0)

    print(f"[ERROR] 技能 '{skill_path.name}' 校验失败:")
    for msg in messages:
        print(f"  - {msg}")
    sys.exit(1)


if __name__ == "__main__":
    main()
