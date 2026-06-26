#!/usr/bin/env python3
"""
核心原则汇总 - 毛泽东思想方法论速查

用法:
    python summary.py
    
或作为模块导入:
    from summary import show_summary
    show_summary()
"""

import sys
from typing import Dict, Any


# 核心原则数据
PRINCIPLES = {
    "矛盾论": {
        "核心观点": "事物发展的根本原因是内因，矛盾有主要矛盾和次要矛盾",
        "方法": ["抓住主要矛盾", "分清主次", "具体分析"],
        "行动": "先解决最重要的事",
        "口诀": "抓主要矛盾",
        "适用": "问题分析、决策优先级"
    },
    "实践论": {
        "核心观点": "认识来源于实践，实践是检验真理的唯一标准",
        "方法": ["调查研究", "试点验证", "边干边学"],
        "行动": "先调研，再决策",
        "口诀": "调查出真知",
        "适用": "决策前验证、方案测试"
    },
    "群众路线": {
        "核心观点": "一切为了群众，一切依靠群众",
        "方法": ["征求意见", "集中起来", "坚持下去"],
        "行动": "依靠大家力量",
        "口诀": "从群众中来，到群众中去",
        "适用": "团队决策、民主决策"
    },
    "独立自主": {
        "核心观点": "主要依靠自己的力量",
        "方法": ["自力更生", "练好内功", "掌握核心"],
        "行动": "主要靠自己也要求",
        "口诀": "自力更生",
        "适用": "资源争取、核心技术"
    },
    "统一战线": {
        "核心观点": "团结一切可以团结的力量",
        "方法": ["分清敌我", "团结多数", "既联合又斗争"],
        "行动": "团结大多数",
        "口诀": "团结多数",
        "适用": "扩大影响、联盟合作"
    },
    "实事求是": {
        "核心观点": "一切从实际出发",
        "方法": ["具体情况具体分析", "不唯书不唯上", "理论联系实际"],
        "行动": "先调研再决策",
        "口诀": "具体问题具体分析",
        "适用": "任何场景"
    },
    "战略战术": {
        "核心观点": "战略上藐视敌人，战术上重视敌人",
        "方法": ["全局自信", "细节认真", "灵活机动"],
        "行动": "大处着眼，小处着手",
        "口诀": "战略藐视，战术重视",
        "适用": "竞争分析、风险评估"
    }
}


def show_summary() -> Dict[str, Any]:
    """
    显示核心原则汇总
    
    Returns:
        原则字典
    """
    print("\n" + "=" * 60)
    print("📚 毛泽东思想核心原则汇总")
    print("=" * 60)
    
    for name, info in PRINCIPLES.items():
        print(f"\n🔹 {name}")
        print(f"   核心: {info['核心观点']}")
        print(f"   口诀: {info['口诀']}")
        print(f"   行动: {info['行动']}")
        print(f"   适用: {info['适用']}")
    
    print("\n" + "=" * 60)
    print("💡 快速口诀")
    print("=" * 60)
    print("""
    矛盾论：抓主要矛盾
    实践论：调查出真知
    群众路线：从群众中来，到群众中去
    独立自主：自力更生
    统一战线：团结多数
    实事求是：具体问题具体分析
    战略战术：战略藐视，战术重视
    """)
    
    print("=" * 60)
    print("🎯 场景应用指南")
    print("=" * 60)
    print("""
    遇到复杂问题 → 用矛盾论抓主要矛盾
    做重大决策 → 用实践论先试点验证
    团队意见多 → 用群众路线统一认识
    资源受限制 → 用独立自力更生
    需要扩大影响 → 用统一战线团结多数
    遇到新情况 → 用实事求是具体分析
    面对强敌 → 用战略战术分析形势
    """)
    
    return PRINCIPLES


def get_principle(name: str) -> Dict[str, Any]:
    """
    获取指定原则的详细信息
    
    Args:
        name: 原则名称
    
    Returns:
        原则详细信息
    
    Example:
        >>> info = get_principle("矛盾论")
        >>> print(info["核心观点"])
        事物发展的根本原因是内因...
    """
    return PRINCIPLES.get(name, {"错误": f"未找到原则: {name}"})


def get_principle_by_scenario(scenario: str) -> Dict[str, Any]:
    """
    根据场景推荐适用原则
    
    Args:
        scenario: 场景描述
    
    Returns:
        推荐的原则
    
    Example:
        >>> result = get_principle_by_scenario("团队意见不统一")
        >>> print(result["推荐原则"]["矛盾论"])
    """
    scenario_map = {
        "问题分析": "矛盾论",
        "决策": "实践论",
        "团队": "群众路线",
        "资源": "独立自主",
        "合作": "统一战线",
        "新情况": "实事求是",
        "竞争": "战略战术"
    }
    
    for key, principle in scenario_map.items():
        if key in scenario:
            return {
                "场景": scenario,
                "推荐原则": principle,
                "详细信息": PRINCIPLES[principle]
            }
    
    return {
        "场景": scenario,
        "推荐原则": "实事求是",
        "详细信息": PRINCIPLES["实事求是"]
    }


def main():
    """命令行入口"""
    # 如果指定了原则名称，显示详细信息
    if len(sys.argv) > 1:
        name = sys.argv[1]
        if name == "--scenario":
            # 场景推荐模式
            scenario = sys.argv[2] if len(sys.argv) > 2 else "一般问题"
            result = get_principle_by_scenario(scenario)
            print(f"\n🎯 场景: {result['场景']}")
            print(f"📌 推荐原则: {result['推荐原则']}")
            print(f"\n详细信息:")
            for k, v in result["详细信息"].items():
                print(f"  {k}: {v}")
        else:
            # 查看指定原则
            info = get_principle(name)
            print(f"\n🔹 {name}")
            for k, v in info.items():
                print(f"   {k}: {v}")
    else:
        # 显示全部
        show_summary()


if __name__ == "__main__":
    main()