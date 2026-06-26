#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill包完整性检查脚本
验证所有必需文件是否存在且格式正确
"""

import os
import sys
import json

def check_skill_package():
    """检查skill包的完整性"""
    print("=" * 80)
    print("🔍 AI智能结算助手 Pro - Skill包完整性检查")
    print("=" * 80)
    print()
    
    # 必需文件列表
    required_files = {
        'SKILL.md': '技能文档（OpenClaw必需）',
        'settlement_engine.py': '核心结算引擎',
        'package.json': '包信息文件'
    }
    
    # 推荐文件列表
    recommended_files = {
        'README.md': 'Skill包说明',
        'INSTALL.md': '安装指南',
        'RELEASE.md': '发布说明',
        'test_topic_rule.py': '测试脚本',
        'UPDATE_v1.1.0.md': '更新日志'
    }
    
    all_ok = True
    
    # 检查必需文件
    print("📋 检查必需文件...")
    for filename, desc in required_files.items():
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  ✅ {filename} ({size:,} bytes) - {desc}")
        else:
            print(f"  ❌ {filename} - {desc} [缺失！]")
            all_ok = False
    
    print()
    
    # 检查推荐文件
    print("📋 检查推荐文件...")
    for filename, desc in recommended_files.items():
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  ✅ {filename} ({size:,} bytes) - {desc}")
        else:
            print(f"  ⚠️  {filename} - {desc} [可选]")
    
    print()
    
    # 检查package.json格式
    if os.path.exists('package.json'):
        print("📋 验证package.json格式...")
        try:
            with open('package.json', 'r', encoding='utf-8') as f:
                pkg = json.load(f)
            
            required_fields = ['name', 'version', 'description']
            for field in required_fields:
                if field in pkg:
                    print(f"  ✅ {field}: {pkg[field]}")
                else:
                    print(f"  ❌ {field}: [缺失！]")
                    all_ok = False
        except Exception as e:
            print(f"  ❌ JSON解析失败: {e}")
            all_ok = False
    
    print()
    
    # 检查SKILL.md格式
    if os.path.exists('SKILL.md'):
        print("📋 验证SKILL.md格式...")
        try:
            with open('SKILL.md', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查前置元数据
            if content.startswith('---'):
                print("  ✅ 包含前置元数据（frontmatter）")
                
                # 检查必需字段
                required_meta = ['name:', 'description:', 'metadata:']
                for meta in required_meta:
                    if meta in content[:500]:
                        print(f"  ✅ 包含 {meta}")
                    else:
                        print(f"  ⚠️  缺少 {meta}")
            else:
                print("  ⚠️  缺少前置元数据")
            
            # 检查内容长度
            if len(content) > 1000:
                print(f"  ✅ 文档内容充实 ({len(content):,} 字符)")
            else:
                print(f"  ⚠️  文档内容较少 ({len(content):,} 字符)")
                
        except Exception as e:
            print(f"  ❌ 读取失败: {e}")
            all_ok = False
    
    print()
    
    # 检查Python文件语法
    if os.path.exists('settlement_engine.py'):
        print("📋 检查Python语法...")
        try:
            with open('settlement_engine.py', 'r', encoding='utf-8') as f:
                code = f.read()
            compile(code, 'settlement_engine.py', 'exec')
            print("  ✅ settlement_engine.py 语法正确")
        except SyntaxError as e:
            print(f"  ❌ settlement_engine.py 语法错误: {e}")
            all_ok = False
    
    if os.path.exists('test_topic_rule.py'):
        try:
            with open('test_topic_rule.py', 'r', encoding='utf-8') as f:
                code = f.read()
            compile(code, 'test_topic_rule.py', 'exec')
            print("  ✅ test_topic_rule.py 语法正确")
        except SyntaxError as e:
            print(f"  ❌ test_topic_rule.py 语法错误: {e}")
            all_ok = False
    
    print()
    print("=" * 80)
    
    if all_ok:
        print("✅ Skill包完整性检查通过！")
        print("🎉 可以安全地将此包用于OpenClaw")
        return 0
    else:
        print("❌ 检查发现问题，请修复后再使用")
        return 1


if __name__ == '__main__':
    exit_code = check_skill_package()
    sys.exit(exit_code)
