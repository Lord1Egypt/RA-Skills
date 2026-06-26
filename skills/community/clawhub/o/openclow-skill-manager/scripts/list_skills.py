#!/usr/bin/env python3
"""
列出所有已安装的 Skills 及其功能介绍
"""

import os
import subprocess

SKILLS_DIR = os.path.expanduser("~/.openclaw/workspace/skills")

def get_skill_description(skill_path):
    """从 SKILL.md 中提取 description"""
    skill_md = os.path.join(skill_path, "SKILL.md")
    if os.path.exists(skill_md):
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
            # 找到 description 行
            for line in content.split('\n'):
                if 'description:' in line.lower():
                    # 提取 description
                    desc = line.split('description:')[1].strip()
                    # 去掉开头的 " 或 '
                    desc = desc.strip('"').strip("'")
                    return desc[:100]  # 限制长度
    return "无描述"

def list_skills():
    """列出所有 skills"""
    if not os.path.exists(SKILLS_DIR):
        print("Skills 目录不存在")
        return
    
    skills = sorted(os.listdir(SKILLS_DIR))
    
    print(f"\n📦 已安装 Skills ({len(skills)} 个)\n")
    print("=" * 70)
    
    for skill in skills:
        skill_path = os.path.join(SKILLS_DIR, skill)
        if os.path.isdir(skill_path):
            desc = get_skill_description(skill_path)
            print(f"\n🔹 {skill}")
            print(f"   {desc}")

def main():
    list_skills()
    
    # 也显示 clawhub 安装的
    print("\n\n📦 ClawHub 安装的 Skills:")
    print("=" * 70)
    result = subprocess.run(['clawhub', 'list'], capture_output=True, text=True)
    print(result.stdout)

if __name__ == "__main__":
    main()
