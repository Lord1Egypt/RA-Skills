#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
话题词规则测试示例
"""

from settlement_engine import TopicRule, RuleParser, format_rule_understanding

def test_topic_rule_basic():
    """测试基本话题词匹配（通用场景）"""
    print("=" * 80)
    print("测试1：基本话题词匹配（OR逻辑）- 通用话题词")
    print("=" * 80)
    
    rule = TopicRule(topics=["#春节活动"], logic="OR")
    
    test_cases = [
        ("新年特惠 #春节活动 攻略", True, "完整包含#春节活动"),
        ("新年特惠 #春节活动优惠 攻略", False, "#春节活动优惠 != #春节活动"),
        ("特惠 #春节活动 和 #春节活动优惠", True, "包含完整的#春节活动"),
        ("日常vlog", False, "不包含任何话题词"),
    ]
    
    for title, expected, desc in test_cases:
        result = rule.check(title)
        status = "✅" if result == expected else "❌"
        print(f"{status} {desc}")
        print(f"   标题: {title}")
        print(f"   预期: {expected}, 实际: {result}\n")


def test_topic_rule_and():
    """测试且逻辑（AND）- 通用话题词"""
    print("=" * 80)
    print("测试2：话题词且逻辑（AND）- 通用话题词")
    print("=" * 80)
    
    rule = TopicRule(topics=["#新品发布", "#限时优惠"], logic="AND")
    
    test_cases = [
        ("#新品发布 #限时优惠 快来抢购", True, "两个话题词都有"),
        ("#新品发布 快来购买", False, "缺少#限时优惠"),
        ("#限时优惠 活动进行中", False, "缺少#新品发布"),
        ("普通视频", False, "都没有"),
    ]
    
    for title, expected, desc in test_cases:
        result = rule.check(title)
        status = "✅" if result == expected else "❌"
        print(f"{status} {desc}")
        print(f"   标题: {title}")
        print(f"   预期: {expected}, 实际: {result}\n")


def test_topic_rule_or():
    """测试或逻辑（OR）- 通用话题词"""
    print("=" * 80)
    print("测试3：话题词或逻辑（OR）- 通用话题词")
    print("=" * 80)
    
    rule = TopicRule(topics=["#品牌挑战赛", "#用户故事"], logic="OR")
    
    test_cases = [
        ("#品牌挑战赛 参与指南", True, "包含第一个"),
        ("#用户故事 分享", True, "包含第二个"),
        ("#品牌挑战赛 #用户故事 双重活动", True, "两个都有"),
        ("日常视频", False, "都没有"),
    ]
    
    for title, expected, desc in test_cases:
        result = rule.check(title)
        status = "✅" if result == expected else "❌"
        print(f"{status} {desc}")
        print(f"   标题: {title}")
        print(f"   预期: {expected}, 实际: {result}\n")


def test_rule_parser():
    """测试规则解析器"""
    print("=" * 80)
    print("测试4：自然语言规则解析（通用话题词）")
    print("=" * 80)
    
    test_rules = [
        "总奖金2万元，携带话题 #春节活动 的作者瓜分",
        "总奖金5万，同时携带 #新品发布 和 #限时优惠 的用户瓜分",
        "奖金3万，携带话题 #品牌挑战赛 或 #用户故事 的作者等额瓜分",
        "总奖金4万，携带 #GameEvent 或 #攻略教学 的创作者瓜分",
    ]
    
    for rule_text in test_rules:
        print(f"\n规则描述: {rule_text}")
        topic_rule = RuleParser.parse_topic_rule(rule_text)
        
        if topic_rule:
            print(f"  解析结果:")
            print(f"    话题词: {topic_rule.topics}")
            print(f"    逻辑关系: {topic_rule.logic}")
        else:
            print(f"  解析结果: 无话题词要求")
        print()


def test_format_understanding():
    """测试规则理解格式化输出（通用话题词）"""
    print("=" * 80)
    print("测试5：规则理解格式化输出（通用话题词）")
    print("=" * 80)
    
    rule_text = "总奖金2万元，播放量≥3万，同时携带话题 #春节活动 和 #新年优惠 的作者瓜分"
    pools = RuleParser.parse(rule_text)
    
    if pools:
        understanding = format_rule_understanding(pools)
        print(understanding)
    else:
        print("规则解析失败")


if __name__ == "__main__":
    test_topic_rule_basic()
    test_topic_rule_and()
    test_topic_rule_or()
    test_rule_parser()
    test_format_understanding()
    
    print("\n" + "=" * 80)
    print("所有测试完成！")
    print("=" * 80)
