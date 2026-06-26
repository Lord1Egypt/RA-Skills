#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速验证星舰工单处理规则
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import match_rule, load_config

def verify_xingjian_priority():
    """验证星舰工单优先级"""
    config = load_config(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json'))
    rules = config['rules']
    
    # 测试混合工单
    test_texts = [
        ("纯星舰工单", "星舰环境有问题", "星舰工单"),
        ("星舰+认证", "星舰环境认证失败", "星舰工单"),
        ("星舰+乐企", "星舰环境乐企问题", "星舰工单"),
        ("认证+星舰", "认证问题星舰环境", "星舰工单"),
        ("纯认证工单", "飞船认证问题", "认证相关工单"),
        ("纯乐企工单", "乐企有问题", "乐企相关工单"),
    ]
    
    print("🔍 验证星舰工单优先级")
    print("=" * 50)
    
    all_pass = True
    for name, text, expected_rule in test_texts:
        matched = match_rule(text, rules)
        actual_rule = matched['rule_name'] if matched else "无匹配"
        
        if actual_rule == expected_rule:
            print(f"✅ {name}: {actual_rule}")
        else:
            print(f"❌ {name}: 期望={expected_rule}, 实际={actual_rule}")
            all_pass = False
    
    print("\n📋 规则优先级（从高到低）：")
    sorted_rules = sorted(rules, key=lambda x: x.get('priority', 0), reverse=True)
    for rule in sorted_rules:
        print(f"  {rule['rule_name']} (priority={rule.get('priority', 1)})")
    
    return all_pass

if __name__ == '__main__':
    success = verify_xingjian_priority()
    sys.exit(0 if success else 1)