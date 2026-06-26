#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
星舰工单处理规则演示脚本
展示新增的星舰工单自动处理功能
"""

import sys
import os

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import check_required_fields, match_rule, create_rejection_comment, load_config

def main():
    """演示星舰工单处理规则"""
    
    print("🚀 JIRA星舰工单处理规则演示")
    print("=" * 60)
    
    # 加载配置
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
    config = load_config(config_path)
    rules = config.get('rules', [])
    
    # 演示案例
    demo_cases = [
        {
            "title": "案例1：完整星舰工单",
            "description": "星舰环境web连接器版本2.1.0，认证失败，日志见附件",
            "notes": "包含所有必填信息，应自动分配给崔征明"
        },
        {
            "title": "案例2：星舰工单但信息不全",
            "description": "星舰有问题，帮忙处理一下",
            "notes": "缺少通道类型、版本号、日志信息，应自动退回"
        },
        {
            "title": "案例3：混合关键词工单（星舰+认证）",
            "description": "星舰环境rpa版本1.5认证授权失败，有error日志",
            "notes": "星舰优先级最高，仍分配给崔征明"
        },
        {
            "title": "案例4：非星舰认证工单",
            "description": "飞船环境web连接器版本3.0认证问题，日志如下",
            "notes": "应分配给张献文"
        },
        {
            "title": "案例5：信息完全不完整",
            "description": "系统有问题，请处理",
            "notes": "应退回并提示规范文档链接"
        }
    ]
    
    for i, case in enumerate(demo_cases, 1):
        print(f"\n📋 {i}. {case['title']}")
        print(f"📝 工单描述：{case['description']}")
        print(f"📌 预期：{case['notes']}")
        print("-" * 40)
        
        # 检查信息完整性
        check_result = check_required_fields(case['description'])
        
        if check_result['is_valid']:
            print("✅ 工单信息完整")
            
            # 匹配规则
            matched_rule = match_rule(case['description'], rules)
            
            if matched_rule:
                print(f"📊 匹配规则：{matched_rule.get('rule_name')}")
                print(f"👤 分配负责人：{matched_rule.get('assignee')}")
                print(f"💬 自动回复：{matched_rule.get('reply_message')}")
                
                # 显示匹配详情
                env = check_result['field_details']['环境']['value']
                channel = check_result['field_details']['通道类型']['value']
                version = check_result['field_details']['项目版本号']['value']
                log = check_result['field_details']['相关日志']['value']
                
                print(f"🔍 提取信息：")
                print(f"   - 环境：{env}")
                print(f"   - 通道类型：{channel}")
                print(f"   - 版本号：{version}")
                print(f"   - 日志：{log}")
            else:
                print("❌ 未匹配到任何规则")
        else:
            print("❌ 工单信息不完整")
            print(f"🔍 缺失信息：{', '.join(check_result['missing_fields'])}")
            
            # 生成打回消息
            rejection_msg = create_rejection_comment(check_result['missing_fields'], config)
            print(f"💬 自动退回消息：")
            print(f"   {rejection_msg[:100]}...")
    
    # 显示当前规则配置
    print("\n" + "=" * 60)
    print("📋 当前配置规则（按优先级排序）：")
    
    sorted_rules = sorted(rules, key=lambda x: x.get('priority', 0), reverse=True)
    for rule in sorted_rules:
        priority = rule.get('priority', 1)
        name = rule.get('rule_name')
        keywords = rule.get('keywords', [])
        assignee = rule.get('assignee')
        
        priority_star = "⭐" * min(priority, 5)
        print(f"\n{priority_star} {name}")
        print(f"   负责人：{assignee}")
        if keywords:
            print(f"   关键词：{', '.join(keywords)}")
        if 'reply_message' in rule:
            print(f"   回复：{rule['reply_message']}")
    
    # 显示打回配置
    print("\n" + "=" * 60)
    print("📝 信息不完整工单处理配置：")
    rejection_msg = config.get('config', {}).get('rejection_message', '')
    if rejection_msg:
        print(f"💬 打回消息：")
        print(f"   {rejection_msg}")
    
    print("\n" + "=" * 60)
    print("🎯 规则总结：")
    print("1. 星舰工单具有最高优先级（priority=10）")
    print("2. 信息完整的星舰工单自动分配给崔征明")
    print("3. 信息不完整的工单自动退回，包含规范文档链接")
    print("4. 其他规则按关键词匹配分数排序")
    print("5. 所有处理都自动记录日志")
    
    print("\n🚀 星舰工单处理规则配置完成！")

if __name__ == '__main__':
    main()