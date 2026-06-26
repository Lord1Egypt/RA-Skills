#!/usr/bin/env python3
"""
技能初始化测试
"""

import os
import sys
import json

def test_config_loading():
    """测试配置文件加载"""
    print("🧪 测试配置文件加载")
    print("-" * 60)
    
    config_path = "config/config.json"
    
    if not os.path.exists(config_path):
        print(f"❌ 配置文件不存在: {config_path}")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        required_keys = ['jira_url', 'username', 'password', 'rules']
        
        for key in required_keys:
            if key not in config:
                print(f"❌ 配置缺少必要字段: {key}")
                return False
        
        print(f"✅ 配置文件加载成功")
        print(f"   JIRA地址: {config['jira_url']}")
        print(f"   用户名: {config['username']}")
        print(f"   密码: {'*' * len(config['password'])}")
        print(f"   分配规则数量: {len(config['rules'])}")
        
        # 显示规则
        print(f"\n📋 分配规则:")
        for rule in config['rules']:
            print(f"   - {rule['rule_name']} -> {rule['assignee']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置文件加载失败: {e}")
        return False

def test_skill_structure():
    """测试技能目录结构"""
    print("\n🧪 测试技能目录结构")
    print("-" * 60)
    
    required_dirs = [
        '.',
        'config',
        'scripts',
        'references'
    ]
    
    required_files = [
        'SKILL.md',
        'INSTALL.md',
        'config/config.json',
        'scripts/jira_auto_analyze.py',
        'scripts/utils.py',
        'scripts/test_functions.py'
    ]
    
    all_passed = True
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ 目录存在: {dir_path}")
        else:
            print(f"❌ 目录缺失: {dir_path}")
            all_passed = False
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ 文件存在: {file_path}")
        else:
            print(f"❌ 文件缺失: {file_path}")
            all_passed = False
    
    return all_passed

def test_skill_md():
    """测试SKILL.md文件"""
    print("\n🧪 测试SKILL.md文件")
    print("-" * 60)
    
    skill_md_path = "SKILL.md"
    
    if not os.path.exists(skill_md_path):
        print(f"❌ SKILL.md文件不存在")
        return False
    
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_sections = [
            '# JIRA工单自动分析处理技能',
            '## 使用场景',
            '## 核心功能',
            '## 使用方法'
        ]
        
        all_sections_found = True
        for section in required_sections:
            if section in content:
                print(f"✅ 包含必要部分: {section}")
            else:
                print(f"❌ 缺少必要部分: {section}")
                all_sections_found = False
        
        return all_sections_found
        
    except Exception as e:
        print(f"❌ 读取SKILL.md失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 JIRA自动分析技能初始化测试")
    print("=" * 60)
    
    # 切换工作目录到技能根目录
    original_dir = os.getcwd()
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(skill_dir)
    
    try:
        test_results = []
        
        test_results.append(("目录结构", test_skill_structure()))
        test_results.append(("配置文件", test_config_loading()))
        test_results.append(("技能文档", test_skill_md()))
        
        print("\n📊 测试总结")
        print("=" * 60)
        
        total_tests = len(test_results)
        passed_tests = sum(1 for _, passed in test_results if passed)
        
        for test_name, passed in test_results:
            status = "✅ 通过" if passed else "❌ 失败"
            print(f"{status} {test_name}")
        
        print("-" * 60)
        print(f"总计: {passed_tests}/{total_tests} 项测试通过")
        
        if passed_tests == total_tests:
            print("\n🎉 技能初始化测试全部通过！")
            print("技能已准备就绪，可以安装使用。")
            return 0
        else:
            print("\n⚠️  部分测试失败，请修复上述问题")
            return 1
            
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    sys.exit(main())