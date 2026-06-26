#!/usr/bin/env python3
"""
Workflow-based Skill Initializer
基于官方 skill-creator 的 init_skill.py，扩展支持从 workflow.json 初始化

Usage:
    # 从 workflow.json 生成（新增功能）
    init_skill.py workflow.json --output generated-skills/

    # 传统方式（兼容官方）
    init_skill.py <skill-name> --path <output-directory>
"""

import sys
import json
from pathlib import Path


# ===== 模板定义（参考官方 skill-creator）=====

SKILL_TEMPLATE = """---
name: {skill_name}
description: {description}
---

# {display_name}

## 概述

{overview}

## 快速开始

用户示例：
```
{example_usage}
```

## 必需参数

{parameters_section}

## 执行流程

本 Skill 将执行以下步骤：

{steps_summary}

## 注意事项

{platform_notes}
"""


# ===== 工具函数 =====

def sanitize_skill_name(name):
    """
    确保 skill 名称符合规范：^[a-z0-9-]+$
    """
    # 移除或替换不符合的字符
    name = name.lower()
    name = name.replace('_', '-')
    # 只保留 a-z, 0-9, -
    import re
    name = re.sub(r'[^a-z0-9-]', '', name)
    # 移除开头和结尾的 -
    name = name.strip('-')
    # 移除连续的 --
    name = re.sub(r'-+', '-', name)
    return name


def title_case_skill_name(skill_name):
    """
    将连字符分隔的 skill 名称转为标题格式
    douyin-drama-collection → Douyin Drama Collection
    """
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def generate_display_name(skill_name, description):
    """
    生成中文显示名称
    优先使用 description 的第一句话
    """
    if description:
        # 尝试提取第一句话
        if '，' in description:
            return description.split('，')[0]
        elif '。' in description:
            return description.split('。')[0]
        elif '、' in description:
            return description.split('、')[0]
        else:
            # 如果没有标点，截取前30个字符
            return description[:30] if len(description) > 30 else description
    else:
        return title_case_skill_name(skill_name)


def generate_parameters_section(parameters):
    """生成参数说明部分"""
    if not parameters:
        return "无必需参数"

    lines = []
    for param in parameters:
        name = param.get('name', '')
        param_type = param.get('type', 'string')
        required = "必需" if param.get('required', True) else "可选"
        desc = param.get('description', '')
        example = param.get('example', '')

        lines.append(f"- **{name}** ({param_type}, {required})")
        if desc:
            lines.append(f"  - 说明：{desc}")
        if example:
            lines.append(f"  - 示例：`{example}`")

    return '\n'.join(lines)


def generate_steps_summary(steps):
    """生成步骤简要列表"""
    summary_lines = []
    for step in steps:
        step_num = step.get('step', 0)
        description = step.get('description', '')
        tool_name = step.get('tool_name', step.get('tool', 'unknown'))

        if description:
            summary_lines.append(f"{step_num}. {description}")
        else:
            summary_lines.append(f"{step_num}. 调用 {tool_name}")

    return '\n'.join(summary_lines)


def get_platform_notes(platform):
    """获取平台特定注意事项"""
    notes_map = {
        "抖音": """- 需要合理控制请求频率，避免触发反爬虫机制
- 虚拟滚动可能导致部分内容未加载，需要多次滚动
- 某些用户主页可能设置为私密，无法访问""",

        "小红书": """- 需要已登录小红书账号
- 图片格式：jpg/png，大小 <20MB
- 标题长度 ≤20 字符
- 正文长度 ≤1000 字符""",

        "default": """- 确保网络连接稳定
- 浏览器环境正常
- 必需参数完整"""
    }

    return notes_map.get(platform, notes_map['default'])


# ===== 主要功能函数 =====

def load_workflow(workflow_path):
    """加载 workflow.json 文件"""
    with open(workflow_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def init_skill_from_workflow(workflow_path):
    """
    从 workflow.json 初始化 Skill（新增功能）
    自动在当前工作目录的 workflow-skills/ 下创建 Skill

    Args:
        workflow_path: workflow.json 文件路径

    Returns:
        生成的 Skill 目录路径，失败返回 None
    """
    try:
        # 加载 workflow
        workflow = load_workflow(workflow_path)

        # 提取关键信息
        raw_name = workflow.get('name', '')
        skill_name = sanitize_skill_name(raw_name)
        description = workflow.get('description', '')
        platform = workflow.get('platform', 'web')
        parameters = workflow.get('parameters', [])
        steps = workflow.get('steps', [])

        if not skill_name:
            print(f"❌ 错误：无效的 skill 名称: '{raw_name}'")
            return None

        # 固定输出到当前工作目录的 workflow-skills/
        output_dir = Path.cwd() / "workflow-skills"
        output_dir.mkdir(parents=True, exist_ok=True)

        # 创建 Skill 目录
        skill_dir = output_dir / skill_name

        if skill_dir.exists():
            print(f"❌ 错误：Skill 目录已存在: {skill_dir}")
            return None

        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ 创建 Skill 目录: {skill_dir}")

        # 生成内容
        display_name = generate_display_name(skill_name, description)
        overview = description if description else f"基于 workflow 自动生成的 {platform} 自动化 Skill"

        # 生成示例用法
        if parameters:
            first_param = parameters[0]
            example_usage = f"提供 {first_param.get('description', '参数')}，例如：{first_param['name']}={first_param.get('example', '...')}"
        else:
            example_usage = "执行自动化任务"

        parameters_section = generate_parameters_section(parameters)
        steps_summary = generate_steps_summary(steps)
        platform_notes = get_platform_notes(platform)

        # 生成 SKILL.md
        skill_content = SKILL_TEMPLATE.format(
            skill_name=skill_name,
            description=description,
            display_name=display_name,
            overview=overview,
            example_usage=example_usage,
            parameters_section=parameters_section,
            steps_summary=steps_summary,
            platform_notes=platform_notes
        )

        skill_md_path = skill_dir / 'SKILL.md'
        skill_md_path.write_text(skill_content, encoding='utf-8')
        print("✅ 创建 SKILL.md")

        # 注意：不创建空的 scripts/ 目录
        # 如果后续需要添加辅助脚本，可以手动创建

        # 完成
        print(f"\n✅ Skill '{skill_name}' 初始化成功！")
        print(f"   位置: {skill_dir}")
        print(f"   平台: {platform}")
        print(f"   参数数量: {len(parameters)}")
        print(f"   步骤数量: {len(steps)}")
        print("\n下一步:")
        print("1. 编辑 SKILL.md，补充详细的执行步骤")
        print("2. 运行验证: scripts/validate_skill.py")
        print("3. 测试 Skill 功能")

        return skill_dir

    except FileNotFoundError:
        print(f"❌ 错误：找不到文件: {workflow_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ 错误：JSON 格式错误: {e}")
        return None
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        return None


def init_skill(skill_name, path):
    """
    传统方式初始化 Skill（兼容官方 skill-creator）
    生成带 TODO 的模板文件

    Args:
        skill_name: Skill 名称
        path: 输出路径

    Returns:
        生成的 Skill 目录路径，失败返回 None
    """
    # 确保 skill 名称符合规范
    skill_name = sanitize_skill_name(skill_name)

    print("⚠️  传统模式：生成带 TODO 的模板")
    print("   建议使用 workflow.json 模式以自动填充内容")

    skill_dir = Path(path).resolve() / skill_name

    if skill_dir.exists():
        print(f"❌ 错误：Skill 目录已存在: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ 创建 Skill 目录: {skill_dir}")

        # 生成简化的 TODO 模板
        skill_title = title_case_skill_name(skill_name)

        todo_skill_content = f"""---
name: {skill_name}
description: [TODO: 详细说明 Skill 的功能和使用场景]
---

# {skill_title}

## 概述

[TODO: 1-2句话说明 Skill 的功能]

## 快速开始

[TODO: 提供使用示例]

## 必需参数

[TODO: 列出必需参数]

## 执行流程

[TODO: 说明执行步骤]

## 注意事项

[TODO: 补充特定注意事项]
"""

        skill_md_path = skill_dir / 'SKILL.md'
        skill_md_path.write_text(todo_skill_content, encoding='utf-8')
        print("✅ 创建 SKILL.md (带 TODO)")

        # 注意：不创建空的 scripts/ 目录
        # 如果后续需要添加辅助脚本，可以手动创建

        print(f"\n✅ Skill '{skill_name}' 目录已创建: {skill_dir}")
        print("\n下一步:")
        print("1. 编辑 SKILL.md 完成 TODO 项")
        print("2. 或使用 workflow.json 自动生成内容")

        return skill_dir

    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  # 从 workflow.json 生成（推荐）")
        print("  init_skill.py workflow-workflows/[skill-name]-workflow.json")
        print("  # 自动在当前工作目录的 workflow-skills/ 下创建")
        print()
        print("  # 传统方式（生成TODO模板）")
        print("  init_skill.py <skill-name> --path <output-directory>")
        sys.exit(1)

    first_arg = sys.argv[1]

    # 判断是 workflow.json 模式还是传统模式
    if first_arg.endswith('.json'):
        # workflow.json 模式
        workflow_path = first_arg

        print(f"🚀 从 workflow.json 生成 Skill")
        print(f"   Workflow: {workflow_path}")
        print(f"   输出目录: [当前工作目录]/workflow-skills/")
        print()

        result = init_skill_from_workflow(workflow_path)

        sys.exit(0 if result else 1)

    else:
        # 传统模式
        if len(sys.argv) < 4 or sys.argv[2] != '--path':
            print("错误：传统模式需要 --path 参数")
            print("用法: init_skill.py <skill-name> --path <output-directory>")
            sys.exit(1)

        skill_name = first_arg
        path = sys.argv[3]

        print(f"🚀 传统模式初始化 Skill: {skill_name}")
        print(f"   输出路径: {path}")
        print()

        result = init_skill(skill_name, path)

        sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
