#!/usr/bin/env python3
"""
配置文件写入器
- 生成 SOUL.md 配置文件
- 写入到正确位置
"""

import os

def get_soul_path():
    """获取 SOUL.md 文件路径"""
    workspace = os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace")
    return os.path.join(workspace, "SOUL.md")

def generate_soul_content(role_name, role_position, core_tasks, communication_style):
    """生成 SOUL.md 内容"""
    content = f"""# SOUL.md - {role_name}

## 角色定位
{role_position}

## 核心任务
{core_tasks}

## 沟通风格
{communication_style}
"""
    return content

def write_soul_file(content):
    """写入 SOUL.md 文件"""
    soul_path = get_soul_path()
    
    # 备份现有文件（如果存在）
    if os.path.exists(soul_path):
        backup_path = soul_path + ".backup"
        os.rename(soul_path, backup_path)
        print(f"已备份现有配置到: {backup_path}")
    
    # 写入新文件
    with open(soul_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"配置已写入: {soul_path}")
    return soul_path

def apply_template(template):
    """应用角色模板"""
    content = template["soul_content"]
    return write_soul_file(content)

if __name__ == "__main__":
    # 测试代码
    test_content = generate_soul_content(
        "测试助手",
        "一个测试角色",
        "- 测试任务1\n- 测试任务2",
        "友好、专业"
    )
    print("生成的配置内容：")
    print(test_content)
