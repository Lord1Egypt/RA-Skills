#!/usr/bin/env python3
"""
毛泽东思想实践工具 - Mao Zedong Thought Practice Toolkit

基于毛泽东选集核心思想的方法论工具集

使用方法:
    python mao_thinking.py <command> [options]
    
Commands:
    analyze      - 矛盾分析：分析问题的主要矛盾
    decide       - 决策助手：结合群众路线做决策  
    situation    - 形势分析：战略藐视 vs 战术重视
    summary      - 核心原则汇总
"""

import sys
import json
from typing import List, Dict, Any


# ========== 核心原则数据 ==========
PRINCIPLES = {
    "矛盾论": {
        "核心观点": "事物发展的根本原因是内因，矛盾有主要矛盾和次要矛盾",
        "方法": ["抓住主要矛盾", "分清主次", "具体分析"],
        "行动": "先解决最重要的事"
    },
    "实践论": {
        "核心观点": "认识来源于实践，实践是检验真理的唯一标准",
        "方法": ["调查研究", "试点验证", "边干边学"],
        "行动": "先调研，再决策"
    },
    "群众路线": {
        "核心观点": "一切为了群众，一切依靠群众",
        "方法": ["征求意见", "集中起来", "坚持下去"],
        "行动": "依靠大家力量"
    },
    "独立自主": {
        "核心观点": "主要依靠自己的力量",
        "方法": ["自力更生", "练好内功", "掌握核心"],
        "行动": "主要靠自己也要求"
    },
    "统一战线": {
        "核心观点": "团结一切可以团结的力量",
        "方法": ["分清敌我", "团结多数", "既联合又斗争"],
        "行动": "团结大多数"
    },
    "实事求是": {
        "核心观点": "一切从实际出发",
        "方法": ["具体情况具体分析", "不唯书不唯上", "理论联系实际"],
        "行动": "先调研再决策"
    }
}


def analyze_contradiction(problem: str, factors: List[str]) -> Dict[str, Any]:
    """
    矛盾分析器 - 分析问题的主要矛盾
    
    Args:
        problem: 描述问题
        factors: 影响因素列表
    
    Returns:
        分析结果字典
    """
    print(f"\n🔍 矛盾分析：{problem}")
    print("=" * 50)
    
    # 分析每个因素的重要性
    print("\n📊 因素分析：")
    for i, f in enumerate(factors, 1):
        print(f"  {i}. {f}")
    
    # 根据矛盾论给出分析
    result = {
        "问题": problem,
        "主要矛盾": factors[0] if factors else "待分析",
        "次要矛盾": factors[1:] if len(factors) > 1 else [],
        "建议": PRINCIPLES["矛盾论"]["行动"],
        "方法论": "抓住主要矛盾，集中力量解决关键问题"
    }
    
    print(f"\n💡 主要矛盾：{result['主要矛盾']}")
    print(f"📌 行动建议：{result['建议']}")
    print(f"⚔️ 方法论：{result['方法论']}")
    
    return result


def mass_line_decide(decision: str, options: List[Dict]) -> Dict[str, Any]:
    """
    群众路线决策助手
    
    Args:
        decision: 决策问题
        options: 可选方案列表，每个包含 name, pros, cons
    
    Returns:
        决策建议
    """
    print(f"\n🤝 群众路线决策：{decision}")
    print("=" * 50)
    
    # 收集各方意见
    print("\n📋 方案分析：")
    for opt in options:
        print(f"\n【{opt['name']}】")
        print(f"  优点: {', '.join(opt.get('pros', []))}")
        print(f"  缺点: {', '.join(opt.get('cons', []))}")
    
    # 评分：群众基础分 + 可行性分
    scored = []
    for opt in options:
        score = 50  # 基础分
        score += len(opt.get('pros', [])) * 10  # 优点加分
        score -= len(opt.get('cons', [])) * 5   # 缺点减分
        scored.append((opt['name'], score))
    
    scored.sort(key=lambda x: x[1], reverse=True)
    winner = scored[0]
    
    result = {
        "决策问题": decision,
        "推荐方案": winner[0],
        "得分": winner[1],
        "全部评分": scored,
        "方法论": "从群众中来，到群众中去"
    }
    
    print(f"\n🏆 推荐方案：{winner[0]} (得分: {winner[1]})")
    print(f"💡 方法论：{result['方法论']}")
    
    return result


def situation_analysis(situation: str, our_strength: int, enemy_strength: int) -> Dict[str, Any]:
    """
    形势分析器 - 战略藐视，战术重视
    
    Args:
        situation: 形势描述
        our_strength: 我方实力 (1-10)
        enemy_strength: 敌方实力 (1-10)
    
    Returns:
        战略建议
    """
    print(f"\n🗺️ 形势分析：{situation}")
    print("=" * 50)
    
    ratio = our_strength / max(enemy_strength, 1)
    
    if ratio >= 1:
        strategy = "战略进攻"
        tactic = "稳步推进，不轻敌"
        spirit = "战略上藐视敌人，战术上重视敌人"
    elif ratio >= 0.5:
        strategy = "战略相持"
        tactic = "保存实力，等待时机"
        spirit = "敌进我退，敌退我追"
    else:
        strategy = "战略防御"
        tactic = "战略性撤退，积蓄力量"
        spirit = "农村包围城市，曲线救国"
    
    result = {
        "形势": situation,
        "我方实力": our_strength,
        "敌方实力": enemy_strength,
        "战略判断": strategy,
        "战术建议": tactic,
        "指导思想": spirit
    }
    
    print(f"\n⚔️ 双方实力比: {our_strength}:{enemy_strength} = {ratio:.2f}")
    print(f"📈 战略判断: {strategy}")
    print(f"🎯 战术建议: {tactic}")
    print(f"🧘 指导思想: {spirit}")
    
    return result


def show_summary():
    """显示核心原则汇总"""
    print("\n" + "=" * 60)
    print("📚 毛泽东思想核心原则汇总")
    print("=" * 60)
    
    for name, info in PRINCIPLES.items():
        print(f"\n🔹 {name}")
        print(f"   核心: {info['核心观点']}")
        print(f"   行动: {info['行动']}")
    
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
    """)
    
    return PRINCIPLES


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        show_summary()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "analyze":
        # 矛盾分析示例
        problem = sys.argv[2] if len(sys.argv) > 2 else "事业发展遇到瓶颈"
        factors = sys.argv[3:] if len(sys.argv) > 3 else ["能力不足", "资源有限", "时机未到", "竞争激烈"]
        analyze_contradiction(problem, factors)
        
    elif command == "decide":
        # 决策助手示例
        decision = sys.argv[2] if len(sys.argv) > 2 else "如何选择工作"
        options = [
            {"name": "A公司", "pros": ["工资高", "平台大"], "cons": ["加班多", "离家远"]},
            {"name": "B公司", "pros": ["离家近", "不加班"], "cons": ["工资低", "发展慢"]}
        ]
        if len(sys.argv) > 3:
            options = json.loads(sys.argv[3])
        mass_line_decide(decision, options)
        
    elif command == "situation":
        # 形势分析示例
        situation = sys.argv[2] if len(sys.argv) > 2 else "面临激烈竞争"
        our = int(sys.argv[3]) if len(sys.argv) > 3 else 6
        enemy = int(sys.argv[4]) if len(sys.argv) > 4 else 8
        situation_analysis(situation, our, enemy)
        
    elif command == "summary":
        show_summary()
        
    else:
        print(f"未知命令: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()