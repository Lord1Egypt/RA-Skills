#!/usr/bin/env python3
"""
形势分析器 - 基于毛泽东战略思想的形势分析工具

核心思想：
- 战略上藐视敌人，战术上重视敌人
- 敌进我退，敌退我追
- 农村包围城市，集中优势兵力各个击破

用法:
    python situator.py "形势描述" 我方实力(1-10) 对方实力(1-10)
    
或作为模块导入:
    from situator import situation_analysis
    result = situation_analysis("面临竞争", 6, 8)
"""

import sys
import json
from typing import Dict, Any, Tuple


# 战略判断标准
STRATEGY_MAP = {
    "进攻": {
        "ratio_range": (1.0, float('inf')),
        "strategy": "战略进攻",
        "tactic": "稳步推进，不轻敌",
        "spirit": "战略上藐视敌人，战术上重视敌人",
        "action": "主动出击，扩大战果"
    },
    "相持": {
        "ratio_range": (0.5, 1.0),
        "strategy": "战略相持",
        "tactic": "保存实力，等待时机",
        "spirit": "敌进我退，敌退我追",
        "action": "稳固防守，积累力量"
    },
    "防御": {
        "ratio_range": (0, 0.5),
        "strategy": "战略防御",
        "tactic": "战略性撤退，积蓄力量",
        "spirit": "农村包围城市，曲线救国",
        "action": "转进有利地形，待机反击"
    }
}


def calculate_strategy(ratio: float) -> Dict[str, Any]:
    """根据实力比判断战略类型"""
    for strategy_type, info in STRATEGY_MAP.items():
        min_val, max_val = info["ratio_range"]
        if min_val <= ratio < max_val:
            return {
                "类型": strategy_type,
                "strategy": info["strategy"],
                "tactic": info["tactic"],
                "spirit": info["spirit"],
                "action": info["action"]
            }
    # 默认返回进攻
    return {
        "类型": "进攻",
        "strategy": STRATEGY_MAP["进攻"]["strategy"],
        "tactic": STRATEGY_MAP["进攻"]["tactic"],
        "spirit": STRATEGY_MAP["进攻"]["spirit"],
        "action": STRATEGY_MAP["进攻"]["action"]
    }


def situation_analysis(
    situation: str, 
    our_strength: int, 
    enemy_strength: int,
    include_details: bool = True
) -> Dict[str, Any]:
    """
    形势分析器 - 战略藐视，战术重视
    
    Args:
        situation: 形势描述
        our_strength: 我方实力 (1-10)
        enemy_strength: 敌方实力 (1-10)
        include_details: 是否包含详细分析
    
    Returns:
        战略建议字典
    
    Example:
        >>> result = situation_analysis(
        ...     situation="面临创业挑战",
        ...     our_strength=5,
        ...     enemy_strength=9
        ... )
        >>> print(result["战略判断"])
        战略相持
    """
    # 验证输入
    our_strength = max(1, min(10, our_strength))
    enemy_strength = max(1, min(10, enemy_strength))
    
    ratio = our_strength / enemy_strength
    
    print(f"\n🗺️ 形势分析：{situation}")
    print("=" * 50)
    print(f"⚔️ 双方实力: 我方 {our_strength} vs 对方 {enemy_strength}")
    print(f"📊 实力比: {ratio:.2f}")
    
    # 计算战略判断
    strategy_info = calculate_strategy(ratio)
    
    # 构建结果
    result = {
        "status": "success",
        "形势": situation,
        "我方实力": our_strength,
        "敌方实力": enemy_strength,
        "实力比": round(ratio, 2),
        "战略类型": strategy_info["类型"],
        "战略判断": strategy_info["strategy"],
        "战术建议": strategy_info["tactic"],
        "指导思想": strategy_info["spirit"],
        "行动建议": strategy_info["action"]
    }
    
    # 添加详细分析
    if include_details:
        result["详细分析"] = {
            "优势分析": f"我方实力{our_strength}分，主要优势在于" + _get_strength_advantage(our_strength),
            "劣势分析": f"对方实力{enemy_strength}分，主要威胁在于" + _get_strength_threat(enemy_strength),
            "时机判断": _get_timing_advice(strategy_info["类型"]),
            "风险提示": _get_risk_warning(strategy_info["类型"])
        }
    
    # 打印结果
    print(f"\n📈 战略判断: {result['战略判断']}")
    print(f"🎯 战术建议: {result['战术建议']}")
    print(f"🧘 指导思想: {result['指导思想']}")
    print(f"🚀 行动建议: {result['行动建议']}")
    
    return result


def _get_strength_advantage(strength: int) -> str:
    """获取实力优势描述"""
    if strength >= 8:
        return "资源丰富，团队强大，品牌影响力强"
    elif strength >= 6:
        return "有一定积累，具备竞争力"
    elif strength >= 4:
        return "灵活机动，适应性强"
    else:
        return "成本低，干劲足，学习能力强"


def _get_strength_threat(strength: int) -> str:
    """获取实力威胁描述"""
    if strength >= 8:
        return "规模大、资源多、市场份额高"
    elif strength >= 6:
        return "有一定实力，竞争压力大"
    else:
        return "可能有一定实力，但并非不可战胜"


def _get_timing_advice(strategy_type: str) -> str:
    """获取时机建议"""
    timing_map = {
        "进攻": "时机成熟，可以主动出击",
        "相持": "时机未到，需要继续积蓄力量",
        "防御": "保存实力为主，等待战略转折点"
    }
    return timing_map.get(strategy_type, "密切关注形势变化")


def _get_risk_warning(strategy_type: str) -> str:
    """获取风险提示"""
    risk_map = {
        "进攻": "注意不要轻敌冒进，避免被对手反击",
        "相持": "避免消耗战，注意保存实力",
        "防御": "防止被对手完全压制，及时寻找突破口"
    }
    return risk_map.get(strategy_type, "保持警惕")


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n用法示例:")
        print("  python situator.py \"面临竞争\" 6 8")
        print("  python situator.py \"创业挑战\" 4 10")
        sys.exit(1)
    
    # 解析参数
    situation = sys.argv[1]
    our = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    enemy = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    
    # 执行分析
    result = situation_analysis(situation, our, enemy)
    
    # 如果指定了 --json 选项，输出 JSON 格式
    if "--json" in sys.argv:
        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
    
    return result


if __name__ == "__main__":
    main()