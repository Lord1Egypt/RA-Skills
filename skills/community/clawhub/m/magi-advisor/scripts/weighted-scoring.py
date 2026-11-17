#!/usr/bin/env python3
"""
MAGI 三贤者加权评分工具
用于多方案比选场景，支持三重视角独立打分后加权汇总。
"""

def magi_score(options: dict, weights: dict = None):
    """
    对多个方案进行三贤者加权评分。
    
    参数:
        options: {
            "方案名": {
                "melchior": {"收益": 8, "可行性": 7, "数据支撑": 9},
                "balthasar": {"风险可控": 6, "伦理合规": 9, "长期安全": 7},
                "casper": {"时机匹配": 8, "团队接受度": 7, "趋势契合": 8}
            }
        }
        weights: 各维度权重，默认等权
    
    返回:
        排序后的方案得分列表
    """
    if weights is None:
        weights = {
            "melchior": 0.40,  # 理性分析权重最高
            "balthasar": 0.35, # 风险守护次之
            "casper": 0.25    # 直觉洞察作为补充
        }
    
    results = []
    for name, scores in options.items():
        total = 0
        breakdown = {}
        for persona, weight in weights.items():
            persona_avg = sum(scores[persona].values()) / len(scores[persona])
            weighted = persona_avg * weight
            total += weighted
            breakdown[persona] = {"avg": round(persona_avg, 2), "weighted": round(weighted, 2)}
        
        results.append({
            "name": name,
            "total": round(total, 2),
            "breakdown": breakdown,
            "verdict": " 推荐" if total >= 7.5 else " 有条件推荐" if total >= 6.0 else " 不推荐"
        })
    
    results.sort(key=lambda x: x["total"], reverse=True)
    return results


# 使用示例
if __name__ == "__main__":
    sample_options = {
        "方案A - 激进扩张": {
            "melchior": {"收益": 9, "可行性": 6, "数据支撑": 7},
            "balthasar": {"风险可控": 4, "伦理合规": 8, "长期安全": 5},
            "casper": {"时机匹配": 8, "团队接受度": 5, "趋势契合": 9}
        },
        "方案B - 稳健迭代": {
            "melchior": {"收益": 6, "可行性": 9, "数据支撑": 8},
            "balthasar": {"风险可控": 9, "伦理合规": 9, "长期安全": 8},
            "casper": {"时机匹配": 6, "团队接受度": 8, "趋势契合": 6}
        }
    }
    
    results = magi_score(sample_options)
    for r in results:
        print(f"\n{'='*50}")
        print(f"方案: {r['name']}")
        print(f"综合得分: {r['total']} → {r['verdict']}")
        for persona, detail in r['breakdown'].items():
            print(f"  {persona.upper()}: 均分 {detail['avg']} × 权重 → 贡献 {detail['weighted']}")