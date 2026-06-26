#!/usr/bin/env python3
"""
简化的JIRA自动分析功能测试
"""

import re

def check_required_fields_simple(text):
    """简化版必填信息检查"""
    text_lower = text.lower()
    
    # 检查环境信息
    env_keywords = ['星舰', '飞船', '云']
    env_found = any(keyword in text_lower for keyword in env_keywords)
    
    # 检查通道类型
    channel_keywords = ['web连接器', 'rpa', '乐企']
    channel_found = any(keyword in text_lower for keyword in channel_keywords)
    
    # 检查项目版本号（云工单除外）
    if '云' in text_lower:
        version_found = True  # 云工单不需要版本号
    else:
        version_pattern = r'(\d+\.\d+\.\d+|v\d+|版本\d+)'
        version_found = bool(re.search(version_pattern, text_lower))
    
    # 检查相关日志
    log_keywords = ['日志', 'log', 'trace', 'error', 'stack']
    log_found = any(keyword in text_lower for keyword in log_keywords)
    
    missing_fields = []
    if not env_found:
        missing_fields.append('环境')
    if not channel_found:
        missing_fields.append('通道类型')
    if not version_found:
        missing_fields.append('项目版本号')
    if not log_found:
        missing_fields.append('相关日志')
    
    return {
        'is_valid': len(missing_fields) == 0,
        'missing_fields': missing_fields
    }

def test_simple():
    """简化测试"""
    print("🧪 简化测试 - 必填信息检查功能")
    print("-" * 60)
    
    test_cases = [
        {
            "name": "完整信息测试",
            "text": "星舰环境，web连接器，版本1.2.3，错误日志",
            "expected_valid": True
        },
        {
            "name": "云环境测试（无版本号）",
            "text": "云环境，rpa通道，错误日志",
            "expected_valid": True
        },
        {
            "name": "缺少环境信息",
            "text": "web连接器，版本v2，日志文件",
            "expected_valid": False
        },
        {
            "name": "缺少通道类型",
            "text": "飞船环境，版本1.0.0，trace日志",
            "expected_valid": False
        },
    ]
    
    all_passed = True
    for test_case in test_cases:
        result = check_required_fields_simple(test_case["text"])
        passed = result["is_valid"] == test_case["expected_valid"]
        
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status} {test_case['name']}")
        print(f"  输入: {test_case['text'][:50]}...")
        print(f"  预期: {'有效' if test_case['expected_valid'] else '无效'}, 实际: {'有效' if result['is_valid'] else '无效'}")
        
        if not result["is_valid"]:
            print(f"  缺失字段: {', '.join(result['missing_fields'])}")
        
        if not passed:
            all_passed = False
        
        print()
    
    print("-" * 60)
    if all_passed:
        print("🎉 所有简化测试通过！")
    else:
        print("⚠️  部分测试失败")
    
    return all_passed

if __name__ == "__main__":
    test_simple()