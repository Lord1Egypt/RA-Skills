#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试星舰工单处理规则
验证新增的星舰工单自动分配功能
"""

import sys
import os

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import check_required_fields, match_rule, calculate_match_score, load_config

def test_xingjian_detection():
    """测试星舰工单检测功能"""
    
    print("🧪 测试星舰工单处理规则")
    print("=" * 50)
    
    # 测试用例
    test_cases = [
        {
            "name": "完整星舰工单",
            "text": "星舰环境web连接器版本1.2.3日志文件见附件",
            "expected_rule": "星舰工单",
            "expected_assignee": "崔征明",
            "expected_reply": "星舰工单请及时处理，有问题可沟通"
        },
        {
            "name": "星舰工单但信息不全",
            "text": "星舰环境有问题，请处理",
            "expected_valid": False,
            "expected_missing_fields": ["通道类型（web连接器、rpa、乐企）", "项目相关服务模块版本号", "相关日志信息"]
        },
        {
            "name": "非星舰完整工单",
            "text": "飞船环境rpa版本2.0有日志错误",
            "expected_rule": "其他工单",
            "expected_assignee": "刘巍"
        },
        {
            "name": "认证相关工单",
            "text": "飞船环境web连接器版本1.0认证失败日志如下",
            "expected_rule": "认证相关工单",
            "expected_assignee": "张献文"
        }
    ]
    
    # 加载配置
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
    config = load_config(config_path)
    rules = config.get('rules', [])
    
    all_passed = True
    
    for test_case in test_cases:
        print(f"\n📋 测试: {test_case['name']}")
        print(f"   文本: {test_case['text'][:50]}...")
        
        # 检查必填信息
        check_result = check_required_fields(test_case['text'])
        
        if 'expected_valid' in test_case:
            # 测试信息完整性检查
            is_valid = check_result['is_valid']
            expected = test_case['expected_valid']
            
            if is_valid == expected:
                print(f"   ✅ 信息完整性检查通过")
                
                if not is_valid:
                    print(f"   🟡 缺失字段: {', '.join(check_result['missing_fields'])}")
            else:
                print(f"   ❌ 信息完整性检查失败")
                print(f"      预期: {expected}, 实际: {is_valid}")
                all_passed = False
                
        elif check_result['is_valid']:
            # 测试规则匹配
            matched_rule = match_rule(test_case['text'], rules)
            
            if matched_rule:
                rule_name = matched_rule.get('rule_name', '未知')
                assignee = matched_rule.get('assignee', '未知')
                reply = matched_rule.get('reply_message', '未知')
                
                # 检查规则匹配
                if rule_name == test_case.get('expected_rule'):
                    print(f"   ✅ 规则匹配通过: {rule_name}")
                else:
                    print(f"   ❌ 规则匹配失败")
                    print(f"      预期: {test_case.get('expected_rule')}, 实际: {rule_name}")
                    all_passed = False
                
                # 检查分配人
                if assignee == test_case.get('expected_assignee'):
                    print(f"   ✅ 分配人正确: {assignee}")
                else:
                    print(f"   ❌ 分配人错误")
                    print(f"      预期: {test_case.get('expected_assignee')}, 实际: {assignee}")
                    all_passed = False
                
                # 检查回复消息（如果指定）
                if 'expected_reply' in test_case:
                    if reply == test_case['expected_reply']:
                        print(f"   ✅ 回复消息正确: {reply}")
                    else:
                        print(f"   ❌ 回复消息错误")
                        print(f"      预期: {test_case['expected_reply']}")
                        print(f"      实际: {reply}")
                        all_passed = False
            else:
                print(f"   ❌ 未匹配到任何规则")
                all_passed = False
        else:
            print(f"   ❌ 工单信息不完整，无法测试规则匹配")
            print(f"      缺失字段: {', '.join(check_result['missing_fields'])}")
            all_passed = False
    
    # 测试优先级
    print("\n" + "=" * 50)
    print("🧪 测试星舰工单优先级")
    
    # 同时包含星舰和其他关键词的工单
    mixed_text = "星舰环境web连接器版本1.0认证失败，有日志"
    
    matched_rule = match_rule(mixed_text, rules)
    if matched_rule and matched_rule.get('rule_name') == '星舰工单':
        print(f"   ✅ 星舰工单优先级测试通过")
        print(f"      即使包含'认证'关键词，仍优先匹配星舰工单")
    else:
        print(f"   ❌ 星舰工单优先级测试失败")
        all_passed = False
    
    # 测试打回消息
    print("\n" + "=" * 50)
    print("🧪 测试打回消息格式")
    
    from utils import create_rejection_comment
    
    missing_fields = ["环境（星舰、飞船、云）", "通道类型（web连接器、rpa、乐企）"]
    rejection_msg = create_rejection_comment(missing_fields, config)
    
    if "http://confluence.51baiwang.com/pages/viewpage.action?pageId=80049485" in rejection_msg:
        print(f"   ✅ 打回消息包含规范文档链接")
    else:
        print(f"   ❌ 打回消息缺少规范文档链接")
        all_passed = False
    
    if "缺少以下必填信息" in rejection_msg:
        print(f"   ✅ 打回消息格式正确")
    else:
        print(f"   ❌ 打回消息格式错误")
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有测试通过！星舰工单处理规则已正确配置")
    else:
        print("⚠️  部分测试失败，请检查配置")
    
    return all_passed

def main():
    """主函数"""
    success = test_xingjian_detection()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()