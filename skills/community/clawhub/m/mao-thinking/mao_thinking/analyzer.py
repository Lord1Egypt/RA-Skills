#!/usr/bin/env python3
"""
矛盾分析器 - 基于毛泽东《矛盾论》的方法论工具

核心思想：
- 事物发展的根本原因是内因
- 矛盾有主要矛盾和次要矛盾
- 抓住主要矛盾是解决问题的关键

用法:
    python analyzer.py "问题描述" 因素1 因素2 因素3
    
或作为模块导入:
    from analyzer import analyze_contradiction
    result = analyze_contradiction("项目延期", ["需求变更", "人手不足", "技术难点"])
"""

import sys
import json
from typing import List, Dict, Any, Optional


# 矛盾论核心原则
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
    }
}


def analyze_contradiction(
    problem: str, 
    factors: List[str],
    weights: Optional[List[int]] = None
) -> Dict[str, Any]:
    """
    矛盾分析器 - 分析问题的主要矛盾
    
    Args:
        problem: 问题描述
        factors: 影响因素列表（按重要性排序）
        weights: 可选权重列表
    
    Returns:
        分析结果字典
    
    Example:
        >>> result = analyze_contradiction(
        ...     problem="项目延期",
        ...     factors=["需求变更", "人手不足", "技术难点", "沟通问题"]
        ... )
        >>> print(result["主要矛盾"])
        需求变更
    """
    if not factors:
        return {
            "status": "error",
            "message": "需要提供至少一个影响因素"
        }
    
    print(f"\n🔍 矛盾分析：{problem}")
    print("=" * 50)
    
    # 分析每个因素
    factor_analysis = []
    for i, f in enumerate(factors):
        weight = weights[i] if weights and i < len(weights) else (10 - i)
        factor_analysis.append({
            "因素": f,
            "权重": weight,
            "重要性": "高" if weight >= 7 else ("中" if weight >= 4 else "低")
        })
        print(f"  {i+1}. {f} (权重: {weight})")
    
    # 确定主要矛盾（第一个因素，或权重最高的）
    if weights:
        primary = max(factor_analysis, key=lambda x: x["权重"])
        main_contradiction = primary["因素"]
    else:
        main_contradiction = factors[0]
    
    # 生成分析结果
    result = {
        "status": "success",
        "问题": problem,
        "主要矛盾": main_contradiction,
        "次要矛盾": factors[1:] if len(factors) > 1 else [],
        "因素分析": factor_analysis,
        "建议": PRINCIPLES["矛盾论"]["行动"],
        "方法论": "抓住主要矛盾，集中力量解决关键问题",
        "分析思路": {
            "step1": "识别所有影响因素",
            "step2": "评估各因素的重要性和关联性",
            "step3": "确定主要矛盾（决定事物性质的核心因素）",
            "step4": "集中资源解决主要矛盾",
            "step5": "在解决主要矛盾的过程中，逐步解决次要矛盾"
        }
    }
    
    print(f"\n💡 主要矛盾：{result['主要矛盾']}")
    print(f"📌 行动建议：{result['建议']}")
    print(f"⚔️ 方法论：{result['方法论']}")
    
    return result


def analyze_from_dict(problem: str, factors_dict: Dict[str, int]) -> Dict[str, Any]:
    """
    从字典形式进行矛盾分析
    
    Args:
        problem: 问题描述
        factors_dict: 因素及其权重的字典 {"因素名": 权重值}
    
    Returns:
        分析结果
    
    Example:
        >>> result = analyze_from_dict(
        ...     problem="找不到工作",
        ...     factors_dict={"缺经验": 9, "竞争大": 7, "期望高": 5}
        ... )
    """
    factors = list(factors_dict.keys())
    weights = list(factors_dict.values())
    return analyze_contradiction(problem, factors, weights)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n用法示例:")
        print("  python analyzer.py \"项目延期\" \"需求变更\" \"人手不足\" \"技术难点\"")
        sys.exit(1)
    
    # 解析参数
    problem = sys.argv[1]
    factors = sys.argv[2:] if len(sys.argv) > 2 else []
    
    if not factors:
        print("错误: 需要提供至少一个影响因素")
        sys.exit(1)
    
    # 执行分析
    result = analyze_contradiction(problem, factors)
    
    # 如果指定了 --json 选项，输出 JSON 格式
    if "--json" in sys.argv:
        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
    
    return result


if __name__ == "__main__":
    main()