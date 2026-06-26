#!/usr/bin/env python3
"""
JIRA自动分析技能演示脚本
展示如何使用技能功能而不实际连接JIRA
"""

import json
import os
import sys

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入工具函数
from utils import check_required_fields, match_rule

def get_config():
    """读取配置文件"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "config.json")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return {}

def demo_required_fields_check():
    """演示必填信息检查功能"""
    print("🔍 演示：必填信息检查功能")
    print("-" * 60)
    
    test_cases = [
        "星舰环境，web连接器，版本1.2.3，错误日志",
        "云环境，rpa通道，错误日志",
        "飞船环境，乐企通道，版本v2.1.0，trace日志",
        "web连接器，版本1.0.0，日志文件"  # 缺少环境信息
    ]
    
    for i, text in enumerate(test_cases, 1):
        result = check_required_fields(text)
        status = "✅ 通过" if result["is_valid"] else "❌ 未通过"
        
        print(f"测试 {i}: {status}")
        print(f"  工单内容: {text[:60]}...")
        
        if result["is_valid"]:
            print(f"  结果: 工单信息完整")
        else:
            print(f"  结果: 缺少以下信息: {', '.join(result['missing_fields'])}")
            print(f"  建议回复: 请提供相关环境、通道类型、版本号及日志信息")
        
        print()

def demo_rule_matching():
    """演示规则匹配功能"""
    print("🎯 演示：规则匹配与自动分配")
    print("-" * 60)
    
    config = get_config()
    rules = config.get("rules", [])
    
    test_cases = [
        {
            "name": "认证相关工单",
            "text": "用户认证失败，无法登录系统"
        },
        {
            "name": "乐企相关工单",
            "text": "乐企接口调用超时错误"
        },
        {
            "name": "综服通道工单",
            "text": "工行综服通道连接异常"
        },
        {
            "name": "其他工单",
            "text": "系统性能优化建议"
        }
    ]
    
    for test_case in test_cases:
        matched_rule = match_rule(test_case["text"], rules)
        
        if matched_rule:
            rule_name = matched_rule.get("rule_name", "未知规则")
            assignee = matched_rule.get("assignee", "未知负责人")
            reply = matched_rule.get("reply_message", "无回复内容")
            
            print(f"📋 {test_case['name']}")
            print(f"  工单内容: {test_case['text']}")
            print(f"  匹配规则: {rule_name}")
            print(f"  自动指派给: {assignee}")
            print(f"  自动回复: {reply}")
        else:
            print(f"❌ {test_case['name']}: 未匹配到任何规则")
        
        print()

def demo_workflow():
    """演示完整工作流程"""
    print("🔄 演示：完整工单处理流程")
    print("=" * 60)
    
    test_issues = [
        {
            "id": 1,
            "summary": "【认证】用户登录权限验证失败，版本1.3.2，错误日志见附件",
            "description": "星舰环境，web连接器，版本1.3.2，认证失败日志显示权限不足",
            "expected": "认证相关工单 -> 张献文"
        },
        {
            "id": 2,
            "summary": "乐企接口调用超时，版本v2.0.1",
            "description": "飞船环境，乐企通道，版本v2.0.1，调用超时日志",
            "expected": "乐企相关工单 -> 付强"
        },
        {
            "id": 3,
            "summary": "工行综服通道无法连接",
            "description": "云环境，web连接器，连接失败日志",
            "expected": "综服通道相关工单 -> 魏旭峰"
        },
        {
            "id": 4,
            "summary": "系统性能优化建议",
            "description": "星舰环境，rpa通道，版本1.5.0，性能日志",
            "expected": "其他工单 -> 刘巍"
        },
        {
            "id": 5,
            "summary": "系统异常，需要紧急处理",
            "description": "异常日志显示系统崩溃",  # 缺少环境信息和版本号
            "expected": "信息不完整 -> 打回给联系人"
        }
    ]
    
    config = get_config()
    rules = config.get("rules", [])
    
    for issue in test_issues:
        print(f"📄 处理工单 #{issue['id']}: {issue['summary'][:40]}...")
        
        # 1. 检查必填信息
        check_result = check_required_fields(issue["description"])
        
        if not check_result["is_valid"]:
            print(f"   ❌ 信息不完整: 缺少 {', '.join(check_result['missing_fields'])}")
            print(f"   📤 操作: 打回给联系人")
            print(f"   💬 回复: {config.get('config', {}).get('rejection_message', '请补充信息')}")
        else:
            print(f"   ✅ 信息完整: 包含所有必填项")
            
            # 2. 匹配分配规则
            matched_rule = match_rule(issue["description"], rules)
            
            if matched_rule:
                rule_name = matched_rule.get("rule_name", "其他工单")
                assignee = matched_rule.get("assignee", "刘巍")
                reply = matched_rule.get("reply_message", "收到，我会及时处理，请稍后")
                
                print(f"   🎯 匹配规则: {rule_name}")
                print(f"   👤 自动指派给: {assignee}")
                print(f"   💬 自动回复: {reply}")
            else:
                print(f"   ⚠️  未匹配到具体规则，使用默认规则")
                print(f"   👤 自动指派给: 刘巍")
                print(f"   💬 自动回复: 收到，我会及时处理，请稍后")
        
        print()

def show_configuration():
    """显示技能配置"""
    print("⚙️  技能配置信息")
    print("-" * 60)
    
    config = get_config()
    
    if "config" in config:
        jira_config = config["config"]
        print(f"🔗 JIRA地址: {jira_config.get('jira_url')}")
        print(f"👤 登录用户: {jira_config.get('username')}")
        print(f"🔑 密码长度: {len(jira_config.get('password', ''))} 字符")
        print(f"📊 Filter ID: {jira_config.get('filter_id')}")
        print(f"📝 打回消息: {jira_config.get('rejection_message')}")
        print(f"🔄 仅检查新工单: {jira_config.get('check_new_only', False)}")
    
    print(f"\n📋 分配规则数量: {len(config.get('rules', []))}")
    for rule in config.get("rules", []):
        print(f"  • {rule.get('rule_name')}: {len(rule.get('keywords', []))}个关键词 -> {rule.get('assignee')}")

def main():
    """主函数"""
    print("🚀 JIRA自动分析技能演示")
    print("=" * 60)
    
    # 显示配置
    show_configuration()
    print()
    
    # 演示功能
    demo_required_fields_check()
    demo_rule_matching()
    demo_workflow()
    
    print("=" * 60)
    print("🎉 演示完成！")
    print("\n使用说明:")
    print("1. 确保已安装Playwright: python3 -m playwright install chromium")
    print("2. 运行主脚本: python3 scripts/jira_auto_analyze.py")
    print("3. 脚本将自动登录JIRA，分析工单，并处理符合条件的工单")
    print("4. 使用 --dry-run 参数进行测试模式，不实际执行操作")

if __name__ == "__main__":
    main()