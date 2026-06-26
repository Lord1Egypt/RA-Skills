#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JIRA自动分析功能测试脚本
用于测试核心功能而不需要实际访问JIRA
"""

import sys
import os

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 定义测试函数，避免导入问题
def check_required_fields(text: str) -> dict:
    """检查文本中是否包含四项必填信息"""
    text_lower = text.lower()
    
    required_fields = {
        '环境': ['星舰', '飞船', '云'],
        '通道类型': ['web连接器', 'rpa', '乐企'],
        '项目版本号': r'(\d+\.\d+\.\d+|v\d+|版本\d+)',
        '相关日志': ['日志', 'log', 'trace', 'error', 'stack']
    }
    
    missing_fields = []
    
    # 检查环境信息
    env_found = False
    for env in required_fields['环境']:
        if env in text_lower:
            env_found = True
            break
    if not env_found:
        missing_fields.append('环境（星舰、飞船、云）')
    
    # 检查通道类型
    channel_found = False
    for channel in required_fields['通道类型']:
        if channel in text_lower:
            channel_found = True
            break
    if not channel_found:
        missing_fields.append('通道类型（web连接器、rpa、乐企）')
    
    # 检查项目版本号（云工单除外）
    import re
    version_found = False
    if '云' in text_lower:
        # 云工单不需要版本号
        version_found = True
    else:
        version_pattern = required_fields['项目版本号']
        if re.search(version_pattern, text_lower):
            version_found = True
    if not version_found:
        missing_fields.append('项目相关服务模块版本号')
    
    # 检查相关日志
    log_found = False
    for log_keyword in required_fields['相关日志']:
        if log_keyword in text_lower:
            log_found = True
            break
    if not log_found:
        missing_fields.append('相关日志信息')
    
    return {
        'is_valid': len(missing_fields) == 0,
        'missing_fields': missing_fields
    }

def calculate_match_score(text: str, keywords: list) -> float:
    """计算文本与关键词的匹配分数"""
    if not text or not keywords:
        return 0.0
    
    text_lower = text.lower()
    matches = 0
    
    for keyword in keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in text_lower:
            matches += 1
            # 如果关键词较长，给予更高权重
            weight = min(len(keyword) / 10, 1.0)
            matches += weight
    
    # 计算分数：匹配的关键词数量 / 总关键词数量
    score = matches / len(keywords) if keywords else 0
    return min(score, 1.0)  # 确保不超过1.0

def match_rule(text: str, rules: list) -> dict:
    """根据文本内容匹配分配规则"""
    text_lower = text.lower()
    best_match = None
    best_score = 0
    
    for rule in rules:
        keywords = rule.get('keywords', [])
        if not keywords:  # 跳过空关键词规则（如"其他工单"）
            continue
            
        match_score = calculate_match_score(text_lower, keywords)
        
        if match_score > best_score:
            best_score = match_score
            best_match = rule
    
    # 如果匹配分数大于0，返回匹配的规则
    if best_match and best_score > 0:
        return best_match
    
    # 否则返回"其他工单"规则
    other_rule = next((r for r in rules if r.get('rule_name') == '其他工单'), None)
    return other_rule

def format_issue_display(issue: dict) -> str:
    """格式化工单显示信息"""
    lines = []
    lines.append(f"工单号: {issue.get('issue_key', '未知')}")
    lines.append(f"状态: {issue.get('status', '未知')}")
    lines.append(f"概要: {issue.get('summary', '无')[:80]}...")
    
    if issue.get('is_valid'):
        lines.append(f"有效性: ✅ 通过")
        lines.append(f"匹配规则: {issue.get('rule_matched', '其他工单')}")
        lines.append(f"建议分配: {issue.get('suggested_assignee', '刘巍')}")
        lines.append(f"回复内容: {issue.get('suggested_reply', '收到，我会及时处理，请稍后')}")
    else:
        lines.append(f"有效性: ❌ 未通过")
        lines.append(f"缺少信息: {', '.join(issue.get('missing_fields', []))}")
    
    return "\n".join(lines)

def test_required_fields():
    """测试必填信息检查功能"""
    print("🧪 测试必填信息检查功能")
    print("-" * 60)
    
    test_cases = [
        {
            "name": "完整信息测试",
            "text": "星舰环境，web连接器，版本1.2.3，错误日志",
            "expected": True
        },
        {
            "name": "云环境测试（无版本号）",
            "text": "云环境，rpa通道，错误日志",
            "expected": True
        },
        {
            "name": "缺少环境信息",
            "text": "web连接器，版本v2，日志文件",
            "expected": False
        },
        {
            "name": "缺少通道类型",
            "text": "飞船环境，版本1.0.0，trace日志",
            "expected": False
        },
        {
            "name": "缺少版本号（非云环境）",
            "text": "星舰环境，乐企通道，error日志",
            "expected": False
        },
        {
            "name": "缺少日志信息",
            "text": "飞船环境，rpa通道，版本2.1.0",
            "expected": False
        },
        {
            "name": "英文关键词测试",
            "text": "starship environment, web connector, version 2.3.1, error log",
            "expected": True
        }
    ]
    
    all_passed = True
    for test_case in test_cases:
        result = check_required_fields(test_case["text"])
        passed = result["is_valid"] == test_case["expected"]
        
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status} {test_case['name']}")
        
        if not passed:
            print(f"  输入: {test_case['text']}")
            print(f"  预期: {test_case['expected']}, 实际: {result['is_valid']}")
            print(f"  缺失字段: {result['missing_fields']}")
            all_passed = False
        
        print()
    
    return all_passed

def test_match_score():
    """测试匹配分数计算功能"""
    print("🧪 测试匹配分数计算功能")
    print("-" * 60)
    
    test_cases = [
        {
            "name": "完全匹配",
            "text": "认证勾选授权",
            "keywords": ["认证", "勾选", "授权"],
            "expected_min": 0.8
        },
        {
            "name": "部分匹配",
            "text": "认证相关工单",
            "keywords": ["认证", "勾选", "授权"],
            "expected_min": 0.3
        },
        {
            "name": "无匹配",
            "text": "普通工单",
            "keywords": ["认证", "勾选", "授权"],
            "expected_max": 0.2
        },
        {
            "name": "乐企匹配",
            "text": "乐企接口调用失败",
            "keywords": ["乐企", "leqi", "LEQI"],
            "expected_min": 0.8
        }
    ]
    
    all_passed = True
    for test_case in test_cases:
        score = calculate_match_score(test_case["text"], test_case["keywords"])
        
        if "expected_min" in test_case:
            passed = score >= test_case["expected_min"]
            condition = f">= {test_case['expected_min']}"
        else:
            passed = score <= test_case["expected_max"]
            condition = f"<= {test_case['expected_max']}"
        
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status} {test_case['name']}")
        print(f"  分数: {score:.2f} {condition}")
        
        if not passed:
            all_passed = False
        
        print()
    
    return all_passed

def test_rule_matching():
    """测试规则匹配功能"""
    print("🧪 测试规则匹配功能")
    print("-" * 60)
    
    # 测试规则
    rules = [
        {
            "rule_name": "认证相关工单",
            "keywords": ["认证", "勾选", "授权", "权限", "token", "登录", "Auth"],
            "assignee": "张献文",
            "jira_username": "zhangxianwen",
            "reply_message": "请献文协助处理此工单"
        },
        {
            "rule_name": "乐企相关工单",
            "keywords": ["乐企", "leqi", "LEQI"],
            "assignee": "付强",
            "jira_username": "fuqiang",
            "reply_message": "请付强协助处理此工单"
        },
        {
            "rule_name": "综服通道相关工单",
            "keywords": ["综服", "通道", "银行", "工行", "中行", "农行", "建行", "招行"],
            "assignee": "魏旭峰",
            "jira_username": "weixufeng",
            "reply_message": "请旭峰协助处理此工单"
        },
        {
            "rule_name": "其他工单",
            "keywords": [],
            "assignee": "刘巍",
            "jira_username": "liuwei1",
            "reply_message": "收到，我会及时处理，请稍后"
        }
    ]
    
    test_cases = [
        {
            "name": "认证工单匹配",
            "text": "认证失败需要处理",
            "expected_rule": "认证相关工单"
        },
        {
            "name": "乐企工单匹配",
            "text": "乐企接口调用异常",
            "expected_rule": "乐企相关工单"
        },
        {
            "name": "综服工单匹配",
            "text": "工行综服通道问题",
            "expected_rule": "综服通道相关工单"
        },
        {
            "name": "其他工单匹配",
            "text": "普通性能优化需求",
            "expected_rule": "其他工单"
        }
    ]
    
    all_passed = True
    for test_case in test_cases:
        matched_rule = match_rule(test_case["text"], rules)
        
        if matched_rule:
            rule_name = matched_rule.get("rule_name", "未知规则")
            passed = rule_name == test_case["expected_rule"]
            status = "✅ 通过" if passed else "❌ 失败"
            
            print(f"{status} {test_case['name']}")
            print(f"  匹配规则: {rule_name}")
            print(f"  负责人: {matched_rule.get('assignee')}")
            print(f"  回复: {matched_rule.get('reply_message')}")
            
            if not passed:
                print(f"  预期规则: {test_case['expected_rule']}")
                all_passed = False
        else:
            print(f"❌ 失败 {test_case['name']}")
            print(f"  未匹配到任何规则")
            all_passed = False
        
        print()
    
    return all_passed

def test_issue_format():
    """测试工单格式化功能"""
    print("🧪 测试工单格式化功能")
    print("-" * 60)
    
    test_issue = {
        "issue_key": "XS-12345",
        "status": "新建",
        "summary": "【工行】综服通道认证失败，版本v1.2.3，错误日志见附件",
        "is_valid": True,
        "missing_fields": [],
        "rule_matched": "综服通道相关工单",
        "suggested_assignee": "魏旭峰",
        "suggested_reply": "请旭峰协助处理此工单"
    }
    
    formatted = format_issue_display(test_issue)
    print("格式化输出:")
    print("-" * 40)
    print(formatted)
    print("-" * 40)
    
    # 检查关键信息是否包含
    required_info = [
        "XS-12345",
        "新建",
        "综服通道认证失败",
        "✅ 通过",
        "综服通道相关工单",
        "魏旭峰"
    ]
    
    all_found = True
    for info in required_info:
        if info in formatted:
            print(f"✅ 包含: {info}")
        else:
            print(f"❌ 缺失: {info}")
            all_found = False
    
    print()
    return all_found

def main():
    """主测试函数"""
    print("🚀 JIRA自动分析功能测试套件")
    print("=" * 60)
    
    test_results = []
    
    # 运行所有测试
    test_results.append(("必填信息检查", test_required_fields()))
    test_results.append(("匹配分数计算", test_match_score()))
    test_results.append(("规则匹配", test_rule_matching()))
    test_results.append(("工单格式化", test_issue_format()))
    
    # 显示测试总结
    print("📊 测试总结")
    print("=" * 60)
    
    total_tests = len(test_results)
    passed_tests = sum(1 for _, passed in test_results if passed)
    
    for test_name, passed in test_results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status} {test_name}")
    
    print("-" * 60)
    print(f"总计: {passed_tests}/{total_tests} 项测试通过")
    
    if passed_tests == total_tests:
        print("🎉 所有测试通过！")
        return 0
    else:
        print("⚠️  部分测试失败，请检查相关问题")
        return 1

if __name__ == "__main__":
    sys.exit(main())