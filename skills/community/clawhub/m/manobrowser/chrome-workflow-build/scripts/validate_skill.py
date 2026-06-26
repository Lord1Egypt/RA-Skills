#!/usr/bin/env python3
"""
Skill 验证脚本
基于官方 skill-creator 的 quick_validate.py，扩展支持 workflow 场景的验证

验证内容：
- YAML frontmatter 格式和必需字段
- Skill 名称格式（^[a-z0-9-]+$）
- 必需文件存在性
- SKILL.md 长度限制
- 描述内容规范
"""

import sys
import os
import re
import json
from pathlib import Path


def validate_skill(skill_path):
    """
    验证 Skill 的结构和内容

    Args:
        skill_path: Skill 目录路径

    Returns:
        (is_valid, result_dict): 验证结果元组
    """
    skill_path = Path(skill_path)

    errors = []
    warnings = []

    # 1. 检查 SKILL.md 是否存在
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        errors.append("SKILL.md 文件不存在")
        return False, {
            "is_valid": False,
            "error_count": len(errors),
            "warning_count": 0,
            "errors": errors,
            "warnings": []
        }

    # 2. 读取 SKILL.md 内容
    try:
        content = skill_md.read_text(encoding='utf-8')
    except Exception as e:
        errors.append(f"无法读取 SKILL.md: {e}")
        return False, {
            "is_valid": False,
            "error_count": len(errors),
            "warning_count": 0,
            "errors": errors,
            "warnings": []
        }

    # 3. 验证 YAML frontmatter
    if not content.startswith('---'):
        errors.append("SKILL.md 缺少 YAML frontmatter（文件必须以 '---' 开头）")
    else:
        # 提取 frontmatter
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            errors.append("YAML frontmatter 格式无效（缺少结束的 '---'）")
        else:
            frontmatter = match.group(1)

            # 检查必需字段：name
            if 'name:' not in frontmatter:
                errors.append("frontmatter 缺少必需字段 'name'")
            else:
                # 提取并验证 name
                name_match = re.search(r'name:\s*(.+)', frontmatter)
                if name_match:
                    name = name_match.group(1).strip()
                    # 验证命名规范：^[a-z0-9-]+$
                    if not re.match(r'^[a-z0-9-]+$', name):
                        errors.append(
                            f"Skill 名称 '{name}' 不符合规范，必须是小写字母、数字和连字符的组合（^[a-z0-9-]+$）"
                        )
                    # 检查不合理的连字符使用
                    if name.startswith('-') or name.endswith('-'):
                        errors.append(f"Skill 名称 '{name}' 不能以连字符开头或结尾")
                    if '--' in name:
                        errors.append(f"Skill 名称 '{name}' 不能包含连续的连字符")

                    # 检查名称与目录名是否一致
                    if skill_path.name != name:
                        warnings.append(
                            f"Skill 名称 '{name}' 与目录名 '{skill_path.name}' 不一致，建议保持一致"
                        )

            # 检查必需字段：description
            if 'description:' not in frontmatter:
                errors.append("frontmatter 缺少必需字段 'description'")
            else:
                # 提取并验证 description
                desc_match = re.search(r'description:\s*(.+)', frontmatter)
                if desc_match:
                    description = desc_match.group(1).strip()

                    # 检查是否包含尖括号（可能是未填充的占位符）
                    if '<' in description or '>' in description:
                        errors.append("description 不能包含尖括号（< 或 >）")

                    # 检查是否为 TODO 占位符
                    if description.startswith('[TODO'):
                        warnings.append("description 仍然是 TODO 占位符，需要补充实际内容")

                    # 检查长度
                    if len(description) < 10:
                        warnings.append("description 过短，建议至少 10 个字符")
                    elif len(description) > 200:
                        warnings.append("description 过长，建议不超过 200 个字符")

    # 4. 检查文件长度
    line_count = len(content.splitlines())
    if line_count > 500:
        warnings.append(f"SKILL.md 有 {line_count} 行，超过建议的 500 行限制")

    # 5. 检查主要章节是否存在
    required_sections = ['## 概述', '## 快速开始', '## 必需参数', '## 执行流程']
    for section in required_sections:
        if section not in content:
            warnings.append(f"建议添加 '{section}' 章节")

    # 6. 检查是否有 TODO 占位符
    todo_count = content.count('[TODO')
    if todo_count > 0:
        warnings.append(f"文件中有 {todo_count} 处 [TODO] 占位符需要补充")

    # 7. 检查 scripts 目录（可选）
    scripts_dir = skill_path / 'scripts'
    if scripts_dir.exists() and scripts_dir.is_dir():
        # 列出脚本文件
        script_files = list(scripts_dir.glob('*.py'))
        if script_files:
            # 这是正常的，不需要警告
            pass

    # 构造结果
    is_valid = len(errors) == 0

    result = {
        "is_valid": is_valid,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings
    }

    return is_valid, result


def print_validation_result(result):
    """
    打印验证结果（友好格式）

    Args:
        result: 验证结果字典
    """
    if result["is_valid"]:
        print("✅ Skill 验证通过！")
    else:
        print("❌ Skill 验证失败")

    print()

    if result["error_count"] > 0:
        print(f"错误 ({result['error_count']}):")
        for i, error in enumerate(result["errors"], 1):
            print(f"  {i}. {error}")
        print()

    if result["warning_count"] > 0:
        print(f"警告 ({result['warning_count']}):")
        for i, warning in enumerate(result["warnings"], 1):
            print(f"  {i}. {warning}")
        print()

    if result["is_valid"]:
        if result["warning_count"] == 0:
            print("Skill 结构完全符合规范！")
        else:
            print("Skill 结构基本符合规范，建议处理上述警告。")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python validate_skill.py <skill-directory>")
        print()
        print("示例: python validate_skill.py workflow-skills/douyin-drama-collection")
        sys.exit(1)

    skill_path = sys.argv[1]

    # 检查目录是否存在
    if not os.path.isdir(skill_path):
        print(f"❌ 错误：目录不存在: {skill_path}")
        sys.exit(1)

    # 执行验证
    is_valid, result = validate_skill(skill_path)

    # 检查是否需要 JSON 输出
    if '--json' in sys.argv:
        # 输出 JSON 格式（供 Claude 使用）
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 输出友好格式（供人类阅读）
        print(f"验证 Skill: {skill_path}")
        print()
        print_validation_result(result)

    # 返回状态码
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
