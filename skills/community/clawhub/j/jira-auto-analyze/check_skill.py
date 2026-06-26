#!/usr/bin/env python3
"""
检查技能结构
"""

import os
import json

print("📁 检查JIRA自动分析技能结构")
print("=" * 60)

# 检查技能根目录
skill_dir = "/Users/baiwang/.workbuddy/skills/jira-auto-analyze"
if not os.path.exists(skill_dir):
    print(f"❌ 技能目录不存在: {skill_dir}")
    exit(1)

print(f"✅ 技能目录: {skill_dir}")

# 检查核心文件
files_to_check = [
    ("SKILL.md", "技能主文档"),
    ("INSTALL.md", "安装指南"),
    ("scripts/jira_auto_analyze.py", "主脚本"),
    ("scripts/utils.py", "工具函数"),
    ("config/config.json", "配置文件"),
]

all_files_exist = True
for file_path, description in files_to_check:
    full_path = os.path.join(skill_dir, file_path)
    if os.path.exists(full_path):
        file_size = os.path.getsize(full_path)
        print(f"✅ {description}: {file_path} ({file_size} bytes)")
    else:
        print(f"❌ {description}缺失: {file_path}")
        all_files_exist = False

# 检查配置文件内容
config_path = os.path.join(skill_dir, "config/config.json")
if os.path.exists(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"\n📋 配置文件内容:")
        print(f"   服务地址: {config.get('jira_url', '未设置')}")
        print(f"   用户名: {config.get('username', '未设置')}")
        print(f"   密码长度: {len(config.get('password', ''))} 字符")
        print(f"   分配规则数量: {len(config.get('rules', []))}")
        
        if 'rules' in config:
            print(f"   分配规则:")
            for rule in config['rules']:
                rule_name = rule.get('rule_name', '未知规则')
                assignee = rule.get('assignee', '未知负责人')
                print(f"      - {rule_name} -> {assignee}")
                
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        all_files_exist = False

# 检查SKILL.md内容
skill_md_path = os.path.join(skill_dir, "SKILL.md")
if os.path.exists(skill_md_path):
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read(1000)  # 读取前1000字符
        
        if "# JIRA工单自动分析处理技能" in content:
            print(f"\n📄 SKILL.md包含技能标题")
        
        # 检查关键部分
        sections_to_check = ['使用场景', '核心功能', '使用方法']
        for section in sections_to_check:
            if f"## {section}" in content:
                print(f"✅ SKILL.md包含'{section}'部分")
            else:
                print(f"⚠️  SKILL.md缺少'{section}'部分")
                
    except Exception as e:
        print(f"❌ 读取SKILL.md失败: {e}")

print("\n" + "=" * 60)
if all_files_exist:
    print("🎉 技能结构完整，准备就绪！")
    print("\n安装步骤:")
    print("1. 确保已安装Python 3.7+和Playwright")
    print("2. 将技能文件夹复制到 ~/.workbuddy/skills/ 目录")
    print("3. 在WorkBuddy中使用 'use_skill jira-auto-analyze' 加载技能")
    print("4. 运行 'python3 scripts/jira_auto_analyze.py' 开始处理工单")
else:
    print("⚠️  技能结构不完整，请检查缺失的文件")